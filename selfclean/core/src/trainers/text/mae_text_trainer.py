from pathlib import Path
from typing import Optional, Union

import torch
from torch import nn
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
        additional_arch_info: str = "",
        print_model_summary: bool = False,
        wandb_logging: bool = True,
        wandb_project_name="SSL",
    ):
        super().__init__(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            config=config,
            config_path=config_path,
            arch_name=f"MAE{additional_arch_info}",
            additional_run_info=additional_run_info,
            wandb_logging=wandb_logging,
            wandb_project_name=wandb_project_name,
        )
        self.loss = nn.CrossEntropyLoss().to(self.device)
        self.print_model_summary = print_model_summary
        # create model
        self.model = BertMae(self.config["model"]["base_model"], self.config["model"]["encoder_mask_ratio"],
                             self.config["model"]["decoder_mask_ratio"])
        self.model.to(self.device)
        self.model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.model)
        self.model = self.distribute_model(self.model)
        if wandb_logging:
            import wandb

            wandb.watch(self.model, log="all")
        if self.print_model_summary:
            summary(self.model, input_size=(self.config["batch_size"], 3, 224, 224))

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

        # log embedding before training
        self._log_embeddings(
            model=self.model,
            log_self_attention=self.config["visualize_attention"],
            log_mae=True,
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
            if isinstance(self.train_dataset.sampler, DistributedSampler):
                self.train_dataset.sampler.set_epoch(epoch - 1)
            self.model.train()
            for sentences, *_ in self.train_dataset:
                # update weight decay and learning rate according to their schedule
                self.update_optim_from_schedulers(
                    optimizer=optimizer,
                    lr_schedule=lr_schedule,
                    wd_schedule=wd_schedule,
                    n_iter=n_iter,
                )
                # move batch to device
                sentences = {k: v.to(self.device) for k, v in sentences.items()}

                optimizer.zero_grad()

                embeddings, logits = self.model(input_ids=sentences["input_ids"], attention_mask=sentences["attention_mask"])
                loss = self.loss(logits.view(-1, logits.size(-1)), sentences["input_ids"].view(-1))

                self.check_loss_nan(loss.detach())
                loss.backward()

                if self.config["clip_grad"]:
                    _ = clip_gradients(self.model, self.config["clip_grad"])
                optimizer.step()

                with torch.no_grad():
                    entropy = calculate_embedding_entropy(
                        embeddings=embeddings.cpu(),
                    )
                    ent_avg, ent_min, ent_max, ent_std, ent_med = entropy

                progress_bar.set_description(f"Epoch: {epoch}, Train loss: {loss:.6f}")
                lr = optimizer.param_groups[0]["lr"]
                wd = optimizer.param_groups[0]["weight_decay"]
                log_dict = {
                    "train_loss": loss,
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

            # log the embeddings if wanted (included online evaluation)
            if epoch % self.config["embed_vis_every_n_epochs"] == 0:
                self._log_embeddings(
                    model=self.model,
                    log_self_attention=self.config["visualize_attention"],
                    log_mae=True,
                    log_dict={
                        "counters/epoch": epoch,
                        "counters/train_step": n_iter,
                    },
                )

            # save the model
            if epoch % self.config["save_every_n_epochs"] == 0 or epoch == self.config["epochs"]:
                save_model(run_dir=self.run_dir, model=self.model.encoder, epoch=epoch)

        if self.multi_gpu:
            backbone = self.model.module
        else:
            backbone = self.model.encoder
        model = backbone
        return model
