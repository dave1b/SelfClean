import gc
from pathlib import Path
from typing import Optional, Union
import torch
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
        mask_token_id = 103
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
        self.print_model_summary = print_model_summary
        self.model = ElectraModel(self.config["model"]["base_model"])
        self.model.to(self.device)
        self.model = self.distribute_model(self.model)
        self.val_dataset = val_dataset
        self.mask_token_id = mask_token_id

        if wandb_logging:
            import wandb
            wandb.watch(self.model, log="all")

        if self.print_model_summary:
            summary(self.model, input_size=(self.config["batch_size"], self.config.get("max_length", 128)))

    def fit(self) -> ElectraModel:
        """Training loop with validation support."""
        params_groups = get_params_groups(self.model)
        optimizer_name = self.config["optimizer"]["name"]
        optimizer_cls = get_optimizer_type(optimizer_name=optimizer_name)
        optimizer = optimizer_cls(params_groups, **self.config["optimizer"]["args"])

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

        # Load the model from checkpoint if provided
        to_restore = {"epoch": 1, "config": self.config}
        restart_from_checkpoint(
            self.get_ckp_path / "model_best.pth",
            run_variables=to_restore,
            state_dict=self.model,
            optimizer=optimizer)
        self.start_epoch = to_restore["epoch"]
        self.config = to_restore["config"]

        # Save the config.yaml file
        self._save_config_file(self.run_dir / "checkpoints")

        # Training loop
        n_iter = 0
        best_val_loss = float('inf')  # Track best validation loss
        progress_bar = tqdm(
            range(self.start_epoch, self.config["epochs"] + 1),
            desc="Self-supervised pre-training",
        )

        for epoch in progress_bar:
            if isinstance(self.train_dataset.sampler, DistributedSampler):
                self.train_dataset.sampler.set_epoch(epoch - 1)

            # Train for one epoch
            train_loss = self._train_epoch(epoch, optimizer, lr_schedule, wd_schedule, n_iter)

            # Validate if validation dataset is provided
            if self.val_dataset is not None:
                val_loss = self._validate_epoch(epoch)
                if self.wandb_logging:
                    import wandb
                    wandb.log({
                        "val_loss": val_loss,
                        "epoch": epoch
                    })
                progress_bar.set_description(
                    f"Epoch: {epoch}, Train loss: {train_loss:.6f}, Val loss: {val_loss:.6f}"
                )

                # Save best model based on validation loss
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    save_model(
                        run_dir=self.run_dir,
                        model=self.model.backbone,
                        epoch=epoch
                    )

                    if self.wandb_logging:
                        wandb.log({
                            "best_val_loss": best_val_loss,
                            "best_epoch": epoch
                        })
            else:
                progress_bar.set_description(f"Epoch: {epoch}, Train loss: {train_loss:.6f}")

            # Save model periodically
            if epoch % self.config["save_every_n_epochs"] == 0 or epoch == self.config["epochs"]:
                save_model(
                    run_dir=self.run_dir,
                    model=self.model.backbone,
                    epoch=epoch,
                )

            n_iter += len(self.train_dataset)

        # Return the backbone model
        if self.multi_gpu:
            backbone = self.model.module
        else:
            backbone = self.model.backbone
        return backbone

    def _train_epoch(self, epoch: int, optimizer, lr_schedule, wd_schedule, n_iter: int) -> float:
        """Train for one epoch and return average loss."""
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

            input_ids = batch['input_ids'].to(self.device, non_blocking=True)
            attention_masks = batch['attention_mask'].to(self.device, non_blocking=True)
            corrupted_ids, labels = self.generate_corrupted_input(input_ids, attention_masks)

            optimizer.zero_grad()

            outputs = self.model(
                input_ids=corrupted_ids,
                attention_mask=attention_masks,
                labels=labels
            )

            embeddings = outputs.logits
            loss = outputs.loss

            self.check_loss_nan(loss.detach())

            loss.backward()

            if self.config["clip_grad"]:
                _ = clip_gradients(self.model, self.config["clip_grad"])

            optimizer.step()

            if n_iter % 100 == 0:
                with torch.no_grad():
                    entropy = calculate_embedding_entropy(embeddings.cpu())
                    ent_avg, ent_min, ent_max, ent_std, ent_med = entropy

            total_loss += loss.item() * input_ids.size(0)
            total_samples += input_ids.size(0)

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

        # Return average loss
        return total_loss / total_samples

    def _validate_epoch(self, epoch: int) -> float:
        """Validate for one epoch and return average loss."""
        self.model.eval()
        total_loss = 0.0
        total_samples = 0

        with torch.no_grad():
            for batch in self.val_dataset:
                # Move batch to device

                input_ids = batch['input_ids'].to(self.device, non_blocking=True)
                attention_masks = batch['attention_mask'].to(self.device, non_blocking=True)
                corrupted_ids, labels = self.generate_corrupted_input(input_ids, attention_masks)

                # Forward pass (validation doesn't need gradients)
                outputs = self.model(
                    input_ids=corrupted_ids,
                    attention_mask=attention_masks,
                    labels=labels
                )

                # Get loss
                loss = outputs.loss

                # Accumulate loss
                total_loss += loss.item() * input_ids.size(0)
                total_samples += input_ids.size(0)

        # Return average validation loss
        return total_loss / total_samples

    def generate_corrupted_input(self, input_ids, attention_mask, replace_prob=0.15):

        # 1. Random mask
        mask_arr = (torch.rand(input_ids.shape, device=input_ids.device) < replace_prob)

        # 2. Replace masked tokens with [MASK] for generator
        masked_ids = input_ids.clone()
        masked_ids[mask_arr] = self.mask_token_id

        # 3. Run generator
        with torch.no_grad():
            gen_logits = self.model.generator(input_ids=masked_ids, attention_mask=attention_mask).logits

        # 4. Sample predictions for masked positions
        sampled = torch.multinomial(torch.softmax(gen_logits[mask_arr], -1), 1).squeeze(-1)

        # 5. Create replaced sequence
        corrupted = input_ids.clone()
        corrupted[mask_arr] = sampled

        # 6. Create ELECTRA labels
        is_replaced = (corrupted != input_ids).long()

        return corrupted, is_replaced


