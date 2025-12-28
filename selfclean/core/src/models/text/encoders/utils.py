from typing import Callable, Tuple
import torch.nn as nn
from transformers import models as transformers_models
from .....src.models.text.encoders.llm import *

LLM_DICT = {
    # Base models
    "bert": bert,
    "roberta": roberta,
    "distilbert": distilbert,
    "bert_mlm": bert_mlm,
    "electra": electra,
    "deberta": deberta,

    # SimCSE models
    "golden_swag_train_simcse_1": golden_swag_train_simcse_1,
    "golden_swag_train_simcse_12": golden_swag_train_simcse_12,
    "golden_swag_train_simcse_25": golden_swag_train_simcse_25,
    "golden_swag_train_simcse_NEAR_DUPLICATES_1": golden_swag_train_simcse_NEAR_DUPLICATES_1,
    "golden_swag_train_simcse_NEAR_DUPLICATES_12": golden_swag_train_simcse_NEAR_DUPLICATES_12,
    "golden_swag_train_simcse_NEAR_DUPLICATES_25": golden_swag_train_simcse_NEAR_DUPLICATES_25,
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_1": golden_swag_train_simcse_NEAR_DUPLICATES_Q_1,
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_12": golden_swag_train_simcse_NEAR_DUPLICATES_Q_12,
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_25": golden_swag_train_simcse_NEAR_DUPLICATES_Q_25,
    "golden_swag_train_simcse_OFF_TOPIC_1": golden_swag_train_simcse_OFF_TOPIC_1,
    "golden_swag_train_simcse_OFF_TOPIC_12": golden_swag_train_simcse_OFF_TOPIC_12,
    "golden_swag_train_simcse_OFF_TOPIC_25": golden_swag_train_simcse_OFF_TOPIC_25,

    # Electra models
    "golden_swag_train_electra_1": golden_swag_train_electra_1,
    "golden_swag_train_electra_25": golden_swag_train_electra_25,
    "golden_swag_train_electra_50": golden_swag_train_electra_50,
    "golden_swag_train_electra_NEAR_DUPLICATE_1": golden_swag_train_electra_NEAR_DUPLICATE_1,
    "golden_swag_train_electra_NEAR_DUPLICATE_25": golden_swag_train_electra_NEAR_DUPLICATE_25,
    "golden_swag_train_electra_NEAR_DUPLICATE_50": golden_swag_train_electra_NEAR_DUPLICATE_50,
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_1": golden_swag_train_electra_NEAR_DUPLICATE_Q_1,
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_25": golden_swag_train_electra_NEAR_DUPLICATE_Q_25,
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_50": golden_swag_train_electra_NEAR_DUPLICATE_Q_50,
    "golden_swag_train_electra_OFF_TOPIC_1": golden_swag_train_electra_OFF_TOPIC_1,
    "golden_swag_train_electra_OFF_TOPIC_25": golden_swag_train_electra_OFF_TOPIC_25,
    "golden_swag_train_electra_OFF_TOPIC_50": golden_swag_train_electra_OFF_TOPIC_50,

    # MAE models
    "golden_swag_train_mae_1": golden_swag_train_mae_1,
    "golden_swag_train_mae_17": golden_swag_train_mae_17,
    "golden_swag_train_mae_35": golden_swag_train_mae_35,
    "golden_swag_train_mae_NEAR_DUPLICATE_1": golden_swag_train_mae_NEAR_DUPLICATE_1,
    "golden_swag_train_mae_NEAR_DUPLICATE_17": golden_swag_train_mae_NEAR_DUPLICATE_17,
    "golden_swag_train_mae_NEAR_DUPLICATE_35": golden_swag_train_mae_NEAR_DUPLICATE_35,
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_1": golden_swag_train_mae_NEAR_DUPLICATE_Q_1,
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_17": golden_swag_train_mae_NEAR_DUPLICATE_Q_17,
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_35": golden_swag_train_mae_NEAR_DUPLICATE_Q_35,
    "golden_swag_train_mae_OFF_TOPIC_1": golden_swag_train_mae_OFF_TOPIC_1,
    "golden_swag_train_mae_OFF_TOPIC_17": golden_swag_train_mae_OFF_TOPIC_17,
    "golden_swag_train_mae_OFF_TOPIC_35": golden_swag_train_mae_OFF_TOPIC_35,
}

def get_encoder_tokenizer_class(base_model_name: str) -> Tuple[nn.Module, nn.Module]:
    encoder, tokenizer = LLM_DICT.get(base_model_name, None)()
    if encoder is None:
        if base_model_name in transformers_models.__dict__.keys():
            encoder = transformers_models.__dict__[base_model_name]
        else:
            raise ValueError(f"Invalid base model name: {base_model_name}")
    return encoder, tokenizer
