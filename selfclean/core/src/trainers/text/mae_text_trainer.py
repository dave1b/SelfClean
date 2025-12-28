import gc
from pathlib import Path
from typing import Optional, Union

import torch
from torch import nn
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader, DistributedSampler
from torchinfo import summary
from tqdm.auto import tqdm

from ...models.text.mae.model import BertMae
from ....src.models.utils import cosine_scheduler, get_params_groups
from ....src.optimizers.utils import get_optimizer_type
from ....src.trainers.base_trainer import Trainer
from ....src.utils.metrics import calculate_embedding_entropy
from ....src.utils.utils import (
    clip_gradients,
    get_world_size,
    restart_from_checkpoint,
    save_checkpoint, save_model,
)

class MAETextTrainer(Trainer):
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
            arch_name=f"MAE_{train_dataset.dataset.name}",
            additional_run_info=additional_run_info,
            wandb_logging=wandb_logging,
            wandb_project_name=wandb_project_name,
        )
        self.loss = nn.CrossEntropyLoss().to(self.device)
        self.print_model_summary = print_model_summary
        # create model
        self.model = BertMae(self.config["model"]["base_model"], self.config["model"]["encoder_mask_ratio"])
        self.model.to(self.device)
        self.model = self.distribute_model(self.model)
        if wandb_logging:
            import wandb
            wandb.watch(self.model, log="all")
        if self.print_model_summary:
            summary(self.model, input_size=(self.config["batch_size"], 3, 224, 224))
        self.scaler = GradScaler()

    def fit(self) -> BertMae:
        # create optimizer
        params_groups = get_params_groups(self.model)
        optimizer_name = self.config["optimizer"]["name"]
        optimizer_cls = get_optimizer_type(optimizer_name=optimizer_name)
        optimizer = optimizer_cls(params_groups, **self.config["optimizer"]["args"])
        # create schedulers
        lr_schedule = cosine_scheduler(
            # linear scaling rule
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
        # load the model from checkpoint if provided
        to_restore = {"epoch": 1, "config": self.config}
        restart_from_checkpoint(
            self.get_ckp_path / "model_best.pth",
            run_variables=to_restore,
            state_dict=self.model,
            optimizer=optimizer,
            loss=self.loss)
        self.start_epoch = to_restore["epoch"]
        self.config = to_restore["config"]
        # save the config.yaml file
        self._save_config_file(self.run_dir / "checkpoints")
        # training loop
        n_iter = 0
        best_val_loss = float('inf')
        progress_bar = tqdm(
            range(self.start_epoch, self.config["epochs"] + 1),
            desc="Self-supervised pre-training",
        )
        for epoch in progress_bar:
            if isinstance(self.train_dataset.sampler, DistributedSampler):
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
                    save_model(run_dir=self.run_dir, model=self.model.encoder, epoch=epoch)
                    if self.wandb_logging:
                        wandb.log({"best_val_loss": best_val_loss, "best_epoch": epoch})
            else:
                progress_bar.set_description(f"Epoch: {epoch}, Train loss: {train_loss:.6f}")
            # save the model
            if epoch % self.config["save_every_n_epochs"] == 0 or epoch == self.config["epochs"]:
                save_model(run_dir=self.run_dir, model=self.model.encoder, epoch=epoch)
            n_iter += len(self.train_dataset)
        if self.multi_gpu:
            backbone = self.model.module
        else:
            backbone = self.model.encoder
        model = backbone
        return model

    def _train_epoch(self, epoch: int, optimizer, lr_schedule, wd_schedule, n_iter: int) -> float:
        self.model.train()
        total_loss = 0.0
        total_samples = 0
        for batch in self.train_dataset:
            # update weight decay and learning rate according to their schedule
            self.update_optim_from_schedulers(
                optimizer=optimizer,
                lr_schedule=lr_schedule,
                wd_schedule=wd_schedule,
                n_iter=n_iter,
            )
            # move batch to device
            sentences = {
                'input_ids': batch['input_ids'].to(self.device, non_blocking=True),
                'attention_mask': batch['attention_mask'].to(self.device, non_blocking=True)
            }
            optimizer.zero_grad(set_to_none=True)

            with autocast():
                embeddings, logits, rand_mask = self.model(sentences["input_ids"], sentences["attention_mask"])
                # Targets are the original input_ids at the positions where we masked
                targets = sentences["input_ids"][rand_mask]
                # Logits at the same positions
                masked_logits = logits[rand_mask]
                loss = self.loss(masked_logits, targets)

            self.check_loss_nan(loss.detach())
            self.scaler.scale(loss).backward()
            if self.config["clip_grad"]:
                self.scaler.unscale_(optimizer)
                _ = clip_gradients(self.model, self.config["clip_grad"])
            self.scaler.step(optimizer)
            self.scaler.update()
            total_loss += loss.item() * sentences['input_ids'].size(0)
            total_samples += sentences['input_ids'].size(0)
            if n_iter % 25 == 0:  # Calculate entropy every 25 iterations
                with torch.no_grad():
                    entropy = calculate_embedding_entropy(embeddings.cpu())
                    ent_avg, ent_min, ent_max, ent_std, ent_med = entropy
            lr = optimizer.param_groups[0]["lr"]
            wd = optimizer.param_groups[0]["weight_decay"]
            log_dict = {
                "train_loss": loss,
                "lr": lr,
                "weight_decay": wd,
                "entropy/train_ent_avg": ent_avg if n_iter % 25 == 0 else None,
                "entropy/train_ent_min": ent_min if n_iter % 25 == 0 else None,
                "entropy/train_ent_max": ent_max if n_iter % 25 == 0 else None,
                "entropy/train_ent_std": ent_std if n_iter % 25 == 0 else None,
                "entropy/train_ent_med": ent_med if n_iter % 25 == 0 else None,
                "counters/epoch": epoch,
                "counters/train_step": n_iter,
            }
            if self.wandb_logging:
                import wandb
                wandb.log(log_dict)
            n_iter += 1
            if n_iter % 100 == 0:  # Clean up every 100 iterations
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
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

                with autocast():
                    embeddings, logits, rand_mask = self.model(sentences["input_ids"], sentences["attention_mask"])
                    targets = sentences["input_ids"][rand_mask]
                    masked_logits = logits[rand_mask]
                    loss = self.loss(masked_logits, targets)
                total_loss += loss.item() * sentences['input_ids'].size(0)
                total_samples += sentences['input_ids'].size(0)
        return total_loss / total_samples
