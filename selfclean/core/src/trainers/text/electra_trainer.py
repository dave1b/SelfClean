import gc
from pathlib import Path
from typing import Optional, Union
import torch
from torch.cuda.amp import GradScaler, autocast
from loguru import logger
from torch.utils.data import DataLoader, DistributedSampler
from torchinfo import summary
from tqdm.auto import tqdm
from ...models.text.electra.model import ElectraModel
from ....src.models.utils import cosine_scheduler, get_params_groups
from ....src.optimizers.utils import get_optimizer_type
from ....src.trainers.base_trainer import Trainer
from ....src.utils.metrics import calculate_embedding_entropy
from ....src.utils.utils import (
    clip_gradients,
    get_world_size,
    restart_from_checkpoint,
    save_model,
)

class ElectraTrainer(Trainer):
    def __init__(
        self,
        train_dataset: DataLoader,
        config: dict,
        val_dataset: Optional[DataLoader] = None,
        config_path: Optional[Union[str, Path]] = None,
        additional_run_info: str = "",
        print_model_summary: bool = False,
        wandb_logging: bool = True,
        wandb_project_name: str = "SSL",
        mask_token_id: int = 103,
    ):
        super().__init__(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            config=config,
            config_path=config_path,
            arch_name=f"ELECTRA_{train_dataset.dataset.name}",
            additional_run_info=additional_run_info,
            wandb_logging=wandb_logging,
            wandb_project_name=wandb_project_name,
        )
        self.model = ElectraModel(base_model=self.config["model"]["base_model"])
        self.model = self.model.to(self.device)
        self.model = self.distribute_model(self.model)
        self.mask_token_id = mask_token_id
        self.scaler_gen = GradScaler()
        self.scaler_disc = GradScaler()

        if wandb_logging:
            import wandb
            wandb.watch(self.model, log="all")

        if print_model_summary:
            summary(self.model, input_size=(self.config["batch_size"], self.config.get("max_length", 128)))

    def fit(self) -> torch.nn.Module:
        logger.info(f"Start training {self.arch_name}")
        params_groups = get_params_groups(self.model)
        optimizer_cls = get_optimizer_type(self.config["optim"])
        optimizer_gen = get_optimizer_type(self.config["optim"])(
            params=self.model.generator.parameters(),
            lr=self.config.get("lr_generator", 5e-4),
            weight_decay=self.config["weight_decay"],
        )
        optimizer_disc = get_optimizer_type(self.config["optim"])(
            params=self.model.backbone.parameters(),
            lr=self.config.get("lr_discriminator", 2e-5),
            weight_decay=self.config["weight_decay"],
        )
        lr_schedule_gen = cosine_scheduler(
            self.config["lr_generator"] * (self.config["batch_size"] * get_world_size()) / 256.0,
            self.config["min_lr"],
            self.config["epochs"],
            len(self.train_dataset),
            warmup_epochs=min(self.config["warmup_epochs"], self.config["epochs"]),
        )
        lr_schedule_disc = cosine_scheduler(
            self.config["lr_discriminator"] * (self.config["batch_size"] * get_world_size()) / 256.0,
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
        self.start_epoch = to_restore["epoch"]
        self.config = to_restore["config"]
        self._save_config_file(self.run_dir / "checkpoints")
        n_iter = 0
        best_val_loss = float('inf')
        progress_bar = tqdm(
            range(self.start_epoch, self.config["epochs"] + 1),
            desc="Self-supervised pre-training",
        )
        for epoch in progress_bar:
            if type(self.train_dataset.sampler) is DistributedSampler:
                self.train_dataset.sampler.set_epoch(epoch - 1)
            self.model.train()
            train_loss = self._train_epoch(epoch, optimizer_gen, optimizer_disc, lr_schedule_gen, lr_schedule_disc, wd_schedule, n_iter)
            if self.val_dataset is not None:
                val_loss = self._validate_epoch(epoch)
                if self.wandb_logging:
                    import wandb
                    wandb.log({"val_loss": val_loss, "epoch": epoch})
                progress_bar.set_description(
                    f"Epoch: {epoch}, Train loss: {train_loss:.6f}, Val loss: {val_loss:.6f}"
                )
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    save_model(run_dir=self.run_dir, model=self.model.backbone, epoch=epoch)
                    if self.wandb_logging:
                        wandb.log({"best_val_loss": best_val_loss, "best_epoch": epoch})
            else:
                progress_bar.set_description(f"Epoch: {epoch}, Train loss: {train_loss:.6f}")
            if epoch % self.config["save_every_n_epochs"] == 0 or epoch == self.config["epochs"]:
                save_model(run_dir=self.run_dir, model=self.model.backbone, epoch=epoch)
        if self.multi_gpu:
            backbone = self.model.module.backbone
        else:
            backbone = self.model.backbone
        return backbone

    def _train_epoch(self, epoch: int, optimizer_gen, optimizer_disc, lr_schedule_gen, lr_schedule_disc, wd_schedule, n_iter: int) -> float:
        self.model.train()
        total_loss = 0.0
        total_samples = 0
        for batch in self.train_dataset:
            self.update_optim_from_schedulers(
                optimizer=optimizer_gen,
                lr_schedule=lr_schedule_gen,
                wd_schedule=wd_schedule,
                n_iter=n_iter,
            )
            self.update_optim_from_schedulers(
                optimizer=optimizer_disc,
                lr_schedule=lr_schedule_disc,
                wd_schedule=wd_schedule,
                n_iter=n_iter,
            )
            n_iter += 1
            input_ids = batch['input_ids'].to(self.device, non_blocking=True)
            attention_masks = batch['attention_mask'].to(self.device, non_blocking=True)

            # Generate corrupted input and get generator loss
            with autocast():
                corrupted_ids, labels, mlm_loss = self.generate_corrupted_input(input_ids, attention_masks)

            optimizer_gen.zero_grad(set_to_none=True)
            self.scaler_gen.scale(mlm_loss).backward()
            if self.config["clip_grad"]:
                self.scaler_gen.unscale_(optimizer_gen)
                _ = clip_gradients(self.model.generator, self.config["clip_grad"])
            self.scaler_gen.step(optimizer_gen)
            self.scaler_gen.update()

            # Discriminator forward/backward
            optimizer_disc.zero_grad(set_to_none=True)
            with autocast():
                outputs = self.model(
                    input_ids=corrupted_ids,
                    attention_mask=attention_masks,
                    labels=labels
                )
                disc_loss = outputs.loss

            self.check_loss_nan(disc_loss.detach())
            self.scaler_disc.scale(disc_loss).backward()
            if self.config["clip_grad"]:
                self.scaler_disc.unscale_(optimizer_disc)
                _ = clip_gradients(self.model.backbone, self.config["clip_grad"])
            self.scaler_disc.step(optimizer_disc)
            self.scaler_disc.update()
            embeddings = outputs.logits

            if n_iter % 100 == 0:
                with torch.no_grad():
                    entropy = calculate_embedding_entropy(embeddings.cpu())
                    ent_avg, ent_min, ent_max, ent_std, ent_med = entropy
            total_loss += disc_loss.item() * input_ids.size(0)
            total_samples += input_ids.size(0)
            if self.wandb_logging:
                import wandb
                wandb.log({
                    "train_loss/disc_loss": disc_loss.item(),
                    "train_loss/mlm_loss": mlm_loss.item(),
                    "lr_disc": optimizer_disc.param_groups[0]["lr"],
                    "weight_decay_disc": optimizer_disc.param_groups[0]["weight_decay"],
                    "lr_gen": optimizer_gen.param_groups[0]["lr"],
                    "weight_decay_gen": optimizer_gen.param_groups[0]["weight_decay"],
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
                input_ids = batch['input_ids'].to(self.device, non_blocking=True)
                attention_masks = batch['attention_mask'].to(self.device, non_blocking=True)
                corrupted_ids, labels = self.generate_corrupted_input(input_ids, attention_masks)
                with autocast():
                    outputs = self.model(
                        input_ids=corrupted_ids,
                        attention_mask=attention_masks,
                        labels=labels
                    )
                    loss = outputs.loss
                total_loss += loss.item() * input_ids.size(0)
                total_samples += input_ids.size(0)
        return total_loss / total_samples

    def generate_corrupted_input(self, input_ids, attention_mask, replace_prob=0.15):
        mask_arr = (torch.rand(input_ids.shape, device=input_ids.device) < replace_prob)
        masked_ids = input_ids.clone()
        masked_ids[mask_arr] = self.mask_token_id
        with autocast():
            gen_outputs = self.model.generator(
                input_ids=masked_ids,
                attention_mask=attention_mask,
                labels=input_ids  # Generator tries to predict original tokens
            )
        mlm_loss = gen_outputs.loss
        sampled = torch.multinomial(torch.softmax(gen_outputs.logits[mask_arr], -1), 1).squeeze(-1)
        corrupted = input_ids.clone()
        corrupted[mask_arr] = sampled
        is_replaced = (corrupted != input_ids).long()
        return corrupted, is_replaced, mlm_loss
