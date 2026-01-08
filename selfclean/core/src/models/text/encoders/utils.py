from typing import Callable, Tuple
import torch.nn as nn
from transformers import models as transformers_models
from .....src.models.text.encoders.llm import *

LLM_DICT = {
    # Base models
    "bert": bert,
    "roberta": roberta,
    "distilbert": distilbert,
    "electra": electra,
    "deberta": deberta,
    "deberta_mlm": deberta_mlm,
    "electra_electra": electra_electra,

    # HellaSwag fine-tuned models
    "hella_swag_electra": hella_swag_electra,
    "hella_swag_simcse": hella_swag_simcse,

    # SimCSE models
    # General
    "golden_swag_train_simcse_1": golden_swag_train_simcse_1,
    "golden_swag_train_simcse_10": golden_swag_train_simcse_10,
    "golden_swag_train_simcse_20": golden_swag_train_simcse_20,
    "golden_swag_train_simcse_35": golden_swag_train_simcse_35,

    # Near duplicates
    "golden_swag_train_simcse_NEAR_DUPLICATES_1": golden_swag_train_simcse_NEAR_DUPLICATES_1,
    "golden_swag_train_simcse_NEAR_DUPLICATES_10": golden_swag_train_simcse_NEAR_DUPLICATES_10,
    "golden_swag_train_simcse_NEAR_DUPLICATES_20": golden_swag_train_simcse_NEAR_DUPLICATES_20,
    "golden_swag_train_simcse_NEAR_DUPLICATES_35": golden_swag_train_simcse_NEAR_DUPLICATES_35,

    # Near duplicates in questions
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_1": golden_swag_train_simcse_NEAR_DUPLICATES_Q_1,
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_10": golden_swag_train_simcse_NEAR_DUPLICATES_Q_10,
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_20": golden_swag_train_simcse_NEAR_DUPLICATES_Q_20,
    "golden_swag_train_simcse_NEAR_DUPLICATES_Q_35": golden_swag_train_simcse_NEAR_DUPLICATES_Q_35,

    # Off-topic
    "golden_swag_train_simcse_OFF_TOPIC_1": golden_swag_train_simcse_OFF_TOPIC_1,
    "golden_swag_train_simcse_OFF_TOPIC_10": golden_swag_train_simcse_OFF_TOPIC_10,
    "golden_swag_train_simcse_OFF_TOPIC_20": golden_swag_train_simcse_OFF_TOPIC_20,
    "golden_swag_train_simcse_OFF_TOPIC_35": golden_swag_train_simcse_OFF_TOPIC_35,

    # Electra models
    # General
    "golden_swag_train_electra_1": golden_swag_train_electra_1,
    "golden_swag_train_electra_10": golden_swag_train_electra_10,
    "golden_swag_train_electra_20": golden_swag_train_electra_20,
    "golden_swag_train_electra_35": golden_swag_train_electra_35,

    # General models without weight sharing
    "golden_swag_train_electra_w_weight_1": golden_swag_train_electra_w_weight_1,
    "golden_swag_train_electra_w_weight_10": golden_swag_train_electra_w_weight_10,
    "golden_swag_train_electra_w_weight_20": golden_swag_train_electra_w_weight_20,
    "golden_swag_train_electra_w_weight_35": golden_swag_train_electra_w_weight_35,

    # Near duplicates
    "golden_swag_train_electra_NEAR_DUPLICATE_1": golden_swag_train_electra_NEAR_DUPLICATE_1,
    "golden_swag_train_electra_NEAR_DUPLICATE_10": golden_swag_train_electra_NEAR_DUPLICATE_10,
    "golden_swag_train_electra_NEAR_DUPLICATE_20": golden_swag_train_electra_NEAR_DUPLICATE_20,
    "golden_swag_train_electra_NEAR_DUPLICATE_35": golden_swag_train_electra_NEAR_DUPLICATE_35,

    # Near duplicates in questions
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_1": golden_swag_train_electra_NEAR_DUPLICATE_Q_1,
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_10": golden_swag_train_electra_NEAR_DUPLICATE_Q_10,
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_20": golden_swag_train_electra_NEAR_DUPLICATE_Q_20,
    "golden_swag_train_electra_NEAR_DUPLICATE_Q_35": golden_swag_train_electra_NEAR_DUPLICATE_Q_35,

    # Off-topic
    "golden_swag_train_electra_OFF_TOPIC_1": golden_swag_train_electra_OFF_TOPIC_1,
    "golden_swag_train_electra_OFF_TOPIC_10": golden_swag_train_electra_OFF_TOPIC_10,
    "golden_swag_train_electra_OFF_TOPIC_20": golden_swag_train_electra_OFF_TOPIC_20,
    "golden_swag_train_electra_OFF_TOPIC_35": golden_swag_train_electra_OFF_TOPIC_35,

    # MAE models
    # General
    "golden_swag_train_mae_1": golden_swag_train_mae_1,
    "golden_swag_train_mae_10": golden_swag_train_mae_10,
    "golden_swag_train_mae_20": golden_swag_train_mae_20,
    "golden_swag_train_mae_35": golden_swag_train_mae_35,

    # Near duplicates
    "golden_swag_train_mae_NEAR_DUPLICATE_1": golden_swag_train_mae_NEAR_DUPLICATE_1,
    "golden_swag_train_mae_NEAR_DUPLICATE_10": golden_swag_train_mae_NEAR_DUPLICATE_10,
    "golden_swag_train_mae_NEAR_DUPLICATE_20": golden_swag_train_mae_NEAR_DUPLICATE_20,
    "golden_swag_train_mae_NEAR_DUPLICATE_35": golden_swag_train_mae_NEAR_DUPLICATE_35,

    # Near duplicates in questions
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_1": golden_swag_train_mae_NEAR_DUPLICATE_Q_1,
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_10": golden_swag_train_mae_NEAR_DUPLICATE_Q_10,
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_20": golden_swag_train_mae_NEAR_DUPLICATE_Q_20,
    "golden_swag_train_mae_NEAR_DUPLICATE_Q_35": golden_swag_train_mae_NEAR_DUPLICATE_Q_35,

    # Off-topic
    "golden_swag_train_mae_OFF_TOPIC_1": golden_swag_train_mae_OFF_TOPIC_1,
    "golden_swag_train_mae_OFF_TOPIC_10": golden_swag_train_mae_OFF_TOPIC_10,
    "golden_swag_train_mae_OFF_TOPIC_20": golden_swag_train_mae_OFF_TOPIC_20,
    "golden_swag_train_mae_OFF_TOPIC_35": golden_swag_train_mae_OFF_TOPIC_35,

    # MLM models
    # General
    "golden_swag_train_mlm_1": golden_swag_train_mlm_1,
    "golden_swag_train_mlm_10": golden_swag_train_mlm_10,
    "golden_swag_train_mlm_20": golden_swag_train_mlm_20,
    "golden_swag_train_mlm_35": golden_swag_train_mlm_35,

    # Near duplicates
    "golden_swag_train_mlm_NEAR_DUPLICATE_1": golden_swag_train_mlm_NEAR_DUPLICATE_1,
    "golden_swag_train_mlm_NEAR_DUPLICATE_10": golden_swag_train_mlm_NEAR_DUPLICATE_10,
    "golden_swag_train_mlm_NEAR_DUPLICATE_20": golden_swag_train_mlm_NEAR_DUPLICATE_20,
    "golden_swag_train_mlm_NEAR_DUPLICATE_35": golden_swag_train_mlm_NEAR_DUPLICATE_35,

    # Near duplicates in questions
    "golden_swag_train_mlm_NEAR_DUPLICATE_Q_1": golden_swag_train_mlm_NEAR_DUPLICATE_Q_1,
    "golden_swag_train_mlm_NEAR_DUPLICATE_Q_10": golden_swag_train_mlm_NEAR_DUPLICATE_Q_10,
    "golden_swag_train_mlm_NEAR_DUPLICATE_Q_20": golden_swag_train_mlm_NEAR_DUPLICATE_Q_20,
    "golden_swag_train_mlm_NEAR_DUPLICATE_Q_35": golden_swag_train_mlm_NEAR_DUPLICATE_Q_35,

    # Off-topic
    "golden_swag_train_mlm_OFF_TOPIC_1": golden_swag_train_mlm_OFF_TOPIC_1,
    "golden_swag_train_mlm_OFF_TOPIC_10": golden_swag_train_mlm_OFF_TOPIC_10,
    "golden_swag_train_mlm_OFF_TOPIC_20": golden_swag_train_mlm_OFF_TOPIC_20,
    "golden_swag_train_mlm_OFF_TOPIC_35": golden_swag_train_mlm_OFF_TOPIC_35,

}

def get_encoder_tokenizer_class(base_model_name: str) -> Tuple[nn.Module, nn.Module]:
    encoder, tokenizer = LLM_DICT.get(base_model_name, None)()
    if encoder is None:
        if base_model_name in transformers_models.__dict__.keys():
            encoder = transformers_models.__dict__[base_model_name]
        else:
            raise ValueError(f"Invalid base model name: {base_model_name}")
    return encoder, tokenizer
