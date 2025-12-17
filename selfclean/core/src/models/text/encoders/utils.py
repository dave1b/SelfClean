from typing import Callable, Tuple
import torch.nn as nn
from transformers import models as transformers_models

from .....src.models.text.encoders.llm import bert, distilbert, roberta, bert_mlm, pretrained_bert_hellaSwag_mae, electra, \
    pretrained_bert_hellaSwag_simcse, pretrained_bert_mmlu_simcse, pretrained_bert_mmlu_mae, golden_swag_train_simcse_bert, \
    golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q, golden_swag_train_simcse_bert_NEAR_DUPLICATES, golden_swag_train_electra_bert

LLM_DICT = {
    "bert": bert,
    "roberta": roberta,
    "distilbert": distilbert,
    "bert_mlm": bert_mlm,
    "electra": electra,
    "pretrained_bert_hellaSwag_simcse": pretrained_bert_hellaSwag_simcse,
    "pretrained_bert_mmlu_simcse": pretrained_bert_mmlu_simcse,
    "pretrained_bert_hellaSwag_mae": pretrained_bert_hellaSwag_mae,
    "pretrained_bert_mmlu_mae": pretrained_bert_mmlu_mae,
    "golden_swag_train_simcse_bert": golden_swag_train_simcse_bert,
    "golden_swag_train_electra_bert": golden_swag_train_electra_bert,
    "golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q": golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q,
    "golden_swag_train_simcse_bert_NEAR_DUPLICATES": golden_swag_train_simcse_bert_NEAR_DUPLICATES,
}


def get_encoder_tokenizer_class(base_model_name: str) -> Tuple[nn.Module, nn.Module]:
    encoder, tokenizer = LLM_DICT.get(base_model_name, None)()
    if encoder is None:
        if base_model_name in transformers_models.__dict__.keys():
            encoder = transformers_models.__dict__[base_model_name]
        else:
            raise ValueError(f"Invalid base model name: {base_model_name}")
    return encoder, tokenizer
