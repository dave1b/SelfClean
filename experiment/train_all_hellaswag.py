from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Callable, Optional

import wandb
from loguru import logger

from experiment.datasets.hellaswag.hella_swag_dataset import HellaSwagDataset
from selfclean.core.src.models.text.encoders.utils import get_encoder_tokenizer_class
from experiment.ELECTRA.train import ELECTRA_STANDARD_HYPERPARAMETERS, train_electra
from experiment.MAE.train import MAE_TEXT_STANDARD_HYPERPARAMETERS, train_mae_text
from experiment.SimCSE.train import SIMCSE_STANDARD_HYPERPARAMETERS, train_simcse
from experiment.MLM.train import MLM_TEXT_STANDARD_HYPERPARAMETERS, train_mlm_text

CONTAMINATED_PATHS = [
    Path("datasets/hellaswag/hellaswag_train_first_10k.json"),
]

VAL_DATASET_PATH = Path("datasets/hellaswag/hellaswag_val_first_2500.json")

HYPERPARAMETERS = {
    # "mae": MAE_TEXT_STANDARD_HYPERPARAMETERS,
    "simcse": SIMCSE_STANDARD_HYPERPARAMETERS,
    "electra": ELECTRA_STANDARD_HYPERPARAMETERS,
    # "mlm": MLM_TEXT_STANDARD_HYPERPARAMETERS,
}


# Training configurations
TRAIN_CONFIGS = {
    "mae": {"epochs": 35, "batch_size": 16, "ssl_pre_training": True, "save_every_n_epochs": 1},
    "simcse": {"epochs": 35, "batch_size": 24, "ssl_pre_training": True, "save_every_n_epochs": 1},
    "electra": {"epochs": 35, "batch_size": 64, "ssl_pre_training": True, "save_every_n_epochs": 1},
    "mlm": {"epochs": 35, "batch_size": 32, "ssl_pre_training": True, "save_every_n_epochs": 1},
}


def log_training_start(ssl_method: str, issue_type: str) -> None:
    logger.info(f"Starting {ssl_method.upper()} training for issue type: {issue_type}")


def log_training_end(ssl_method: str, duration: timedelta) -> None:
    logger.info(f"Finished {ssl_method.upper()} training after: {duration}")

def start_train_mlm(train_dataset, val_dataset):
    start = datetime.now()
    log_training_start("mlm", train_dataset.name)
    model = train_mlm_text(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        **TRAIN_CONFIGS["mlm"],
        hyperparameters=HYPERPARAMETERS["mlm"],
    )
    log_training_end("mlm", datetime.now() - start)
    return model

def start_train_mae(train_dataset, val_dataset):
    start = datetime.now()
    log_training_start("mae", train_dataset.name)
    model = train_mae_text(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        **TRAIN_CONFIGS["mae"],
        hyperparameters=HYPERPARAMETERS["mae"],
    )
    log_training_end("mae", datetime.now() - start)
    return model


def start_train_simcse(train_dataset, val_dataset):
    start = datetime.now()
    log_training_start("simcse", train_dataset.name)
    model = train_simcse(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        **TRAIN_CONFIGS["simcse"],
        hyperparameters=HYPERPARAMETERS["simcse"],
    )
    log_training_end("simcse", datetime.now() - start)
    return model


def start_train_electra(train_dataset, val_dataset):
    start = datetime.now()
    log_training_start("electra", train_dataset.name)
    model = train_electra(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        **TRAIN_CONFIGS["electra"],
        hyperparameters=HYPERPARAMETERS["electra"],
    )
    log_training_end("electra", datetime.now() - start)
    return model


TRAIN_FUNCTIONS: Dict[str, Callable] = {
    "electra": start_train_electra,
    # "mlm": start_train_mlm,
    # "mae": start_train_mae,
    "simcse": start_train_simcse,
}


def load_val_dataset(ssl_method: str) -> HellaSwagDataset:
    _, tokenizer = get_encoder_tokenizer_class(HYPERPARAMETERS[ssl_method]["model"]["base_model"])
    return HellaSwagDataset(
        json_path=VAL_DATASET_PATH,
        tokenizer=tokenizer,
        pre_tokenize=True,
    )


def load_train_dataset(path: Path, ssl_method: str, issue_type: str) -> HellaSwagDataset:
    _, tokenizer = get_encoder_tokenizer_class(HYPERPARAMETERS[ssl_method]["model"]["base_model"])
    return HellaSwagDataset(
        json_path=path,
        tokenizer=tokenizer,
        pre_tokenize=True,
        name=f"hellaswag_{ssl_method}_{issue_type}",
    )


def train_all() -> None:
    logger.info("Starting training for all SSL methods and issue types...")
    logger.info(f"Will run training for {len(CONTAMINATED_PATHS) * len(TRAIN_FUNCTIONS)} combinations")

    for path in CONTAMINATED_PATHS:
        issue_type = "default"
        for ssl_method, train_function in TRAIN_FUNCTIONS.items():
            val_dataset = load_val_dataset(ssl_method)
            train_dataset = load_train_dataset(path, ssl_method, issue_type)
            train_function(train_dataset, val_dataset)
            wandb.finish()


if __name__ == "__main__":
    train_all()
