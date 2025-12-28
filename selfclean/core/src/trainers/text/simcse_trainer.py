import gc
from pathlib import Path
from typing import List, Optional, Union, Dict
from loguru import logger

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, DistributedSampler
from torchinfo import summary
from tqdm.auto import tqdm

from ....src.models.text.simcse.model import BertSimCSE
from ....src.losses.nt_xent import NTXentLoss
from ....src.models.utils import ModelType, cosine_scheduler
from ....src.optimizers.utils import get_optimizer_type
from ....src.pkg.wrappers import ViTWrapper, Wrapper
from ....src.trainers.base_trainer import Trainer
from ....src.utils.metrics import calculate_embedding_entropy
from ....src.utils.utils import (
    clip_gradients,
    get_world_size,
    restart_from_checkpoint,
    save_checkpoint, save_model,
)

class SimCSETrainer(Trainer):
    def __init__(
        self,
        train_dataset: DataLoader,
        config: dict,
        val_dataset: Optional[DataLoader] = None,
        config_path: Optional[Union[str, Path]] = None,
        additional_run_info: str = "",
        print_model_summary: bool = False,
        wandb_logging: bool = True,
        wandb_project_name="SSL",
    ):
        super().__init__(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            config=config,
            config_path=config_path,
            arch_name=f"SimCSE_{train_dataset.dataset.name}",
            additional_run_info=additional_run_info,
            wandb_logging=wandb_logging,
            wandb_project_name=wandb_project_name,
        )
        self.loss = NTXentLoss(self.device, config["batch_size"], **config["loss"])
        self.loss = self.loss.to(self.device)
        self.model = BertSimCSE(base_model=self.config["model"]["base_model"])
        self.model = self.model.to(self.device)
        self.model = self.distribute_model(self.model)
        if wandb_logging:
            import wandb
            wandb.watch(self.model, log="all")
        if print_model_summary:
            summary(self.model, input_size=(self.config["batch_size"], 3, 224, 224))

    def fit(self) -> torch.nn.Module:
        logger.info(f"Start training {self.arch_name}")
        optimizer_cls = get_optimizer_type(self.config["optim"])
        optimizer = optimizer_cls(
            params=self.model.parameters(),
            lr=self.config["lr"],
            weight_decay=self.config["weight_decay"],
        )
        lr_schedule = cosine_scheduler(
            self.config["lr"] * (self.config["batch_size"] * get_world_size()) / 256.0,
            self.config["min_lr"],
            self.config["epochs"],
            len(self.train_dataset),
            warmup_epochs=min(self.config["warmup_epochs"], self.config["epochs"]),
        )
        wd_schedule = cosine_scheduler(
            self.config["weight_decay"],
            self.config["weight_decay_end"],
            self.config["epochs"],
            len(self.train_dataset),
        )
        to_restore = {"epoch": 1, "config": self.config}
        restart_from_checkpoint(
            self.get_ckp_path / "model_best.pth",
            run_variables=to_restore,
            state_dict=self.model,
            optimizer=optimizer,
            loss=self.loss,
        )
        self.start_epoch = to_restore["epoch"]
        self.config = to_restore["config"]
        self._save_config_file(self.run_dir / "checkpoints")
        n_iter = 0
        best_val_loss = float('inf')  # Track best validation loss
        progress_bar = tqdm(
            range(self.start_epoch, self.config["epochs"] + 1),
            desc="Self-supervised pre-training",
        )
        for epoch in progress_bar:
            if type(self.train_dataset.sampler) is DistributedSampler:
                self.train_dataset.sampler.set_epoch(epoch - 1)
            self.model.train()
            train_loss = self._train_epoch(epoch, optimizer, lr_schedule, wd_schedule, n_iter)
            # Validate if validation dataset is provided
            if self.val_dataset is not None:
                val_loss = self._validate_epoch(epoch)
                if self.wandb_logging:
                    import wandb
                    wandb.log({"val_loss": val_loss, "epoch": epoch})
                progress_bar.set_description(
                    f"Epoch: {epoch}, Train loss: {train_loss:.6f}, Val loss: {val_loss:.6f}"
                )
                # Save best model based on validation loss
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    save_model(run_dir=self.run_dir, model=self.model.backbone, epoch=epoch)
                    if self.wandb_logging:
                        wandb.log({"best_val_loss": best_val_loss, "best_epoch": epoch})
            else:
                progress_bar.set_description(f"Epoch: {epoch}, Train loss: {train_loss:.6f}")
            # Save model periodically
            if epoch % self.config["save_every_n_epochs"] == 0 or epoch == self.config["epochs"]:
                save_model(run_dir=self.run_dir, model=self.model.backbone, epoch=epoch)
        if self.multi_gpu:
            backbone = self.model.module.backbone
        else:
            backbone = self.model.backbone
        return backbone

    def _train_epoch(self, epoch: int, optimizer, lr_schedule, wd_schedule, n_iter: int) -> float:
        self.model.train()
        total_loss = 0.0
        total_samples = 0
        for batch in self.train_dataset:
            self.update_optim_from_schedulers(
                optimizer=optimizer,
                lr_schedule=lr_schedule,
                wd_schedule=wd_schedule,
                n_iter=n_iter,
            )
            n_iter += 1
            sentences = {
                'input_ids': batch['input_ids'].to(self.device, non_blocking=True),
                'attention_mask': batch['attention_mask'].to(self.device, non_blocking=True)
            }
            optimizer.zero_grad()
            loss, embeddings = self._model_step(self.model, sentences)
            if n_iter % 100 == 0:
                with torch.no_grad():
                    entropy = calculate_embedding_entropy(embeddings.cpu())
                    ent_avg, ent_min, ent_max, ent_std, ent_med = entropy
            self.check_loss_nan(loss.detach())
            loss.backward()
            if self.config["clip_grad"]:
                _ = clip_gradients(self.model, self.config["clip_grad"])
            optimizer.step()
            total_loss += loss.item() * sentences['input_ids'].size(0)
            total_samples += sentences['input_ids'].size(0)
            if self.wandb_logging:
                import wandb
                wandb.log({
                    "train_loss": loss.item(),
                    "lr": optimizer.param_groups[0]["lr"],
                    "weight_decay": optimizer.param_groups[0]["weight_decay"],
                    "entropy/train_ent_avg": ent_avg if n_iter % 100 == 0 else None,
                    "entropy/train_ent_min": ent_min if n_iter % 100 == 0 else None,
                    "entropy/train_ent_max": ent_max if n_iter % 100 == 0 else None,
                    "entropy/train_ent_std": ent_std if n_iter % 100 == 0 else None,
                    "entropy/train_ent_med": ent_med if n_iter % 100 == 0 else None,
                    "counters/epoch": epoch,
                    "counters/train_step": n_iter,
                })

        return total_loss / total_samples

    def _validate_epoch(self, epoch: int) -> float:
        self.model.eval()
        total_loss = 0.0
        total_samples = 0
        with torch.no_grad():
            for batch in self.val_dataset:
                sentences = {
                    'input_ids': batch['input_ids'].to(self.device, non_blocking=True),
                    'attention_mask': batch['attention_mask'].to(self.device, non_blocking=True)
                }
                loss, _ = self._model_step(self.model, sentences)
                total_loss += loss.item() * sentences['input_ids'].size(0)
                total_samples += sentences['input_ids'].size(0)
        return total_loss / total_samples

    def _model_step(self, model, sentences: Dict[str, torch.Tensor]):
        embs_1, projs_1 = model(sentences['input_ids'], sentences['attention_mask'])
        embs_2, projs_2 = model(sentences['input_ids'], sentences['attention_mask'])
        embeddings = torch.cat([embs_1, embs_2])
        loss = self.loss(projs_1, projs_2)
        return loss, embeddings
