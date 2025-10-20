import gc
import os
import platform
from distutils import dist
from typing import List, Optional, Union
from experiment.SimCSE.hella_swag_dataset import HellaSwagDataset
from selfclean.core.src.models.text.encoders.utils import get_encoder_tokenizer_class
from selfclean.core.src.trainers.text.simcse_trainer import SimCSETrainer

import torch
from torch.utils.data import Dataset, DataLoader, DistributedSampler


def cleanup():
    if is_dist_avail_and_initialized():
        dist.destroy_process_group()


def is_dist_avail_and_initialized():
    if not dist.is_available():
        return False
    if not dist.is_initialized():
        return False
    return True


SIMCSE_STANDARD_HYPERPARAMETERS = {
    "optim": "adamw",
    "lr": 0.0005,
    "min_lr": "1e-6",
    "weight_decay": "0.04",
    "weight_decay_end": 0.4,
    "warmup_epochs": 10,
    "momentum_teacher": 0.996,
    "clip_grad": 3.0,
    "apply_l2_norm": True,
    "model": {
        "out_dim": 4096,
        "emb_dim": 192,
        "base_model": "bert",
        "model_type": "BERT",
        "use_bn_in_head": False,
        "norm_last_layer": True,
        "student": {
            "drop_path_rate": 0.1,
        },
        "teacher": {
            "drop_path_rate": 0.1,
        },
        "eval": {"n_last_blocks": 4, "avgpool_patchtokens": False},
        "encoder": {
            "out_dim": 256,
            "patch_size": None,
        }
    },
    "loss": {
        "temperature": 0.04,
        "use_cosine_similarity": True,
    },
    "optimizer": {"freeze_last_layer": 1},
    "visualize_attention": False,
}


def train_simcse(
    dataset: Dataset,
    epochs: int = 2,
    batch_size: int = 32,
    ssl_pre_training: bool = True,
    save_every_n_epochs: int = 10,
    work_dir: Optional[str] = None,
    hyperparameters: dict = SIMCSE_STANDARD_HYPERPARAMETERS,
    num_workers: Optional[int] = os.cpu_count(),
    # logging
    additional_run_info: str = "",
    wandb_logging: bool = False,
    wandb_project_name: str = "SelfClean",
):
    assert all(
        key in hyperparameters for key in SIMCSE_STANDARD_HYPERPARAMETERS
    ), "`hyperparameters` need to contain all standard hyperparameters."

    hyperparameters["epochs"] = epochs
    hyperparameters["batch_size"] = batch_size
    hyperparameters["ssl_pre_training"] = ssl_pre_training
    hyperparameters["save_every_n_epochs"] = save_every_n_epochs
    if work_dir is not None:
        hyperparameters["work_dir"] = work_dir

    if torch.cuda.is_available():
        sampler = DistributedSampler(dataset, shuffle=True)
        kwargs = {"sampler": sampler}
    else:
        kwargs = {"shuffle": True}

    # due to a problem with worker spawning on apple silicon
    # we set it here to 0
    kwargs["num_workers"] = num_workers
    if platform.machine().lower() == "arm64":
        kwargs["num_workers"] = 0

    if torch.cuda.is_available():
        sampler = DistributedSampler(dataset, shuffle=True)
        kwargs = {"sampler": sampler}
    else:
        kwargs = {"shuffle": True}

    train_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        drop_last=False,
        pin_memory=True,
        **kwargs,
    )

    trainer = SimCSETrainer(
        train_dataset=train_loader,
        config=hyperparameters,
        additional_run_info=additional_run_info,
        wandb_logging=wandb_logging,
        wandb_project_name=wandb_project_name,
    )
    model = trainer.fit()
    del trainer, train_loader
    gc.collect()
    cleanup()
    return model


if __name__ == "__main__":
    tokenizer = get_encoder_tokenizer_class("bert")[1]
    dataset = HellaSwagDataset("../datasets/hellaswag/hellaswag_small.json", tokenizer)
    print("Training SimCSE")
    train_simcse(dataset, 2, 32, True, 1, None, SIMCSE_STANDARD_HYPERPARAMETERS, os.cpu_count())
