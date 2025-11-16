import gc
import os
import platform
from datetime import datetime
from typing import List, Optional, Union

import torch
from torch.utils.data import Dataset, DataLoader, DistributedSampler
from pathlib import Path

from experiment.datasets.hellaswag.hella_swag_dataset import HellaSwagDataset
from selfclean.core.src.models.text.encoders.utils import get_encoder_tokenizer_class
from selfclean.core.src.trainers.text.electra_trainer import ElectraTrainer
from selfclean.core.src.trainers.text.mae_text_trainer import MAETextTrainer
from selfclean.core.src.utils.utils import init_distributed_mode, cleanup

ELECTRA_STANDARD_HYPERPARAMETERS = {
    "optimizer": {
        "name": "adamw",
        "args": {}
    },
    "lr": 0.0005,
    "min_lr": 1e-6,
    "weight_decay": 0.04,
    "weight_decay_end": 0.4,
    "warmup_epochs": 10,
    "momentum_teacher": 0.996,
    "clip_grad": 3.0,
    "apply_l2_norm": True,
    "model": {
        "out_dim": None,
        "emb_dim": None,
        "base_model": "electra",
        "model_type": "BERT",
        "use_bn_in_head": False,
        "norm_last_layer": True,
        "eval": {"n_last_blocks": 4, "avgpool_patchtokens": False},
        "encoder": {
            "out_dim": 756,
            "patch_size": None,
        },
    },
    "visualize_attention": False,
    "embed_vis_every_n_epochs": 1
}


def train_electra(
    dataset: Dataset,
    epochs: int = 2,
    batch_size: int = 32,
    ssl_pre_training: bool = True,
    save_every_n_epochs: int = 10,
    work_dir: Optional[str] = None,
    hyperparameters: dict = ELECTRA_STANDARD_HYPERPARAMETERS,
    num_workers: Optional[int] = min(8, os.cpu_count()),
    # logging
    additional_run_info: str = "",
    wandb_logging: bool = True,
    wandb_project_name: str = "SelfClean",
):
    assert all(
        key in hyperparameters for key in ELECTRA_STANDARD_HYPERPARAMETERS
    ), "`hyperparameters` need to contain all standard hyperparameters."

    hyperparameters["epochs"] = epochs
    hyperparameters["batch_size"] = batch_size
    hyperparameters["ssl_pre_training"] = ssl_pre_training
    hyperparameters["save_every_n_epochs"] = save_every_n_epochs
    if work_dir is not None:
        hyperparameters["work_dir"] = work_dir

    init_distributed_mode()
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

    train_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        collate_fn=dataset.get_collate_fn(),
        drop_last=True,
        pin_memory=True,
        **kwargs,
    )

    trainer = ElectraTrainer(
        train_dataset=train_loader,
        config=hyperparameters,
        additional_run_info=additional_run_info,
        wandb_logging=wandb_logging,
        wandb_project_name=wandb_project_name,
    )
    model = trainer.fit()
    del trainer, train_loader
    gc.collect()
    if torch.cuda.is_available():
        cleanup()
    return model


if __name__ == "__main__":
    start = datetime.now()
    tokenizer = get_encoder_tokenizer_class("electra")[1]

    hellaswag_dataset_path = Path(__file__).parent.parent / "datasets" / "hellaswag" / "hellaswag_train.json"
    mmlu_dataset_path = Path(__file__).parent.parent / "datasets" / "mmlu" / "mmlu_test.json"

    dataset = HellaSwagDataset(
        json_path=hellaswag_dataset_path,
        tokenizer=tokenizer,
        cache_dir="./cache",
        pre_tokenize=True  # Enable pre-tokenization
    )

    print("Training ELECTRA Text")
    model = train_electra(dataset, 5, 32, True, 1, None, ELECTRA_STANDARD_HYPERPARAMETERS)
    print(f'Finished ELECTRA training after: {datetime.now() - start}')
