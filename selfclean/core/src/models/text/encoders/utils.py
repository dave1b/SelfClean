from typing import Callable, Tuple
import torch.nn as nn
from transformers import models as transformers_models

from .....src.models.text.encoders.llm import bert, distilbert, roberta, bert_mlm, pretrained_bert_mae

LLM_DICT = {
    "bert": bert,
    "pretrained_bert_mae": pretrained_bert_mae,
    "roberta": roberta,
    "distilbert": distilbert,
    "bert_mlm": bert_mlm,
}

def get_encoder_tokenizer_class(base_model_name: str) -> Tuple[nn.Module, nn.Module]:
    encoder, tokenizer = LLM_DICT.get(base_model_name, None)()
    if encoder is None:
        if base_model_name in transformers_models.__dict__.keys():
            encoder = transformers_models.__dict__[base_model_name]
        else:
            raise ValueError(f"Invalid base model name: {base_model_name}")
    return encoder, tokenizer
