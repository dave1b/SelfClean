import gc
from pathlib import Path
from typing import List, Optional, Union, Dict

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
        # create model
        self.model = BertSimCSE(
            base_model=self.config["model"]["base_model"]
        )
        self.model = self.model.to(self.device)
        self.model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.model)
        self.model = self.distribute_model(self.model)

        if wandb_logging:
            import wandb

            wandb.watch(self.model, log="all")
        if print_model_summary:
            summary(self.model, input_size=(self.config["batch_size"], 3, 224, 224))

    def fit(self) -> torch.nn.Module:
        # create optimizer
        optimizer_cls = get_optimizer_type(self.config["optim"])
        optimizer = optimizer_cls(
            params=self.model.parameters(),
            lr=self.config["lr"],
            weight_decay=self.config["weight_decay"],
        )

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
            loss=self.loss,
        )
        self.start_epoch = to_restore["epoch"]
        self.config = to_restore["config"]

        # save the config.yaml file
        self._save_config_file(self.run_dir / "checkpoints")

        # log embedding before training
        self._log_embeddings(
            model=self.model,
            patch_size=self.config["model"]["encoder"]["patch_size"],
            log_self_attention=self.config["visualize_attention"],
            log_dict={
                "counters/epoch": 0,
                "counters/train_step": 0,
            },
        )

        # training loop
        n_iter = 0
        progress_bar = tqdm(
            range(self.start_epoch, self.config["epochs"] + 1),
            desc="Self-supervised pre-training",
        )
        for epoch in progress_bar:
            if type(self.train_dataset.sampler) is DistributedSampler:
                self.train_dataset.sampler.set_epoch(epoch - 1)
            self.model.train()
            for batch in self.train_dataset:
                # update weight decay and learning rate according to their schedule
                self.update_optim_from_schedulers(
                    optimizer=optimizer,
                    lr_schedule=lr_schedule,
                    wd_schedule=wd_schedule,
                    n_iter=n_iter,
                )

                sentences = {
                    'input_ids': batch['input_ids'].to(self.device, non_blocking=True),
                    'attention_mask': batch['attention_mask'].to(self.device, non_blocking=True)
                }

                # zero the parameter gradients
                optimizer.zero_grad()

                # --- forward pass ---
                loss, embeddings = self._model_step(self.model, sentences)

                if n_iter % 25 == 0:  # Calculate entropy every 25 iterations
                    with torch.no_grad():
                        entropy = calculate_embedding_entropy(embeddings.cpu())
                        ent_avg, ent_min, ent_max, ent_std, ent_med = entropy

                # check if loss is not infinite
                self.check_loss_nan(loss.detach())

                # update model
                loss.backward()
                if self.config["clip_grad"]:
                    _ = clip_gradients(self.model, self.config["clip_grad"])
                optimizer.step()

                # log metrics
                progress_bar.set_description(f"Epoch: {epoch}, Train loss: {loss:.6f}")
                lr = optimizer.param_groups[0]["lr"]
                wd = optimizer.param_groups[0]["weight_decay"]
                log_dict = {
                    "train_loss": loss,
                    "train_step": n_iter,
                    "lr": lr,
                    "weight_decay": wd,
                    "entropy/train_ent_avg": ent_avg,
                    "entropy/train_ent_min": ent_min,
                    "entropy/train_ent_max": ent_max,
                    "entropy/train_ent_std": ent_std,
                    "entropy/train_ent_med": ent_med,
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

            # log the embeddings if wanted
            if epoch % self.config["embed_vis_every_n_epochs"] == 0:
                self._log_embeddings(
                    model=self.model,
                    patch_size=self.config["model"]["encoder"]["patch_size"],
                    log_self_attention=self.config["visualize_attention"],
                    log_dict={
                        "counters/epoch": epoch,
                        "counters/train_step": n_iter,
                    },
                )

            # save the model
            if epoch % self.config["save_every_n_epochs"] == 0 or epoch == self.config["epochs"]:
                save_model(run_dir=self.run_dir, model=self.model.backbone, epoch=epoch)

        if self.multi_gpu:
            backbone = self.model.module.backbone
        else:
            backbone = self.model.backbone
        model = backbone
        return model

    def _model_step(self, model, sentences: Dict[str, torch.Tensor]):
        # Get the embeddings and projections for the same sentences (two views)
        embs_1, projs_1 = model(sentences['input_ids'], sentences['attention_mask'])  # First view
        embs_2, projs_2 = model(sentences['input_ids'], sentences['attention_mask'])  # Second view

        # Normalize projections
        projs_1 = torch.stack([F.normalize(proj, dim=0) for proj in projs_1])
        projs_2 = torch.stack([F.normalize(proj, dim=0) for proj in projs_2])

        # Stack embeddings for entropy calculation
        embeddings = torch.cat([embs_1, embs_2])

        # Calculate the loss for the batch
        loss = self.loss(projs_1, projs_2)  # Pass the two views of the batch

        return loss, embeddings
