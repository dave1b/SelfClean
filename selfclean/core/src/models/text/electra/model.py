import torch.nn as nn
from transformers import ElectraForMaskedLM

from ..encoders.utils import get_encoder_tokenizer_class


class ElectraModel(nn.Module):
    def __init__(self, base_model):
        super(ElectraModel, self).__init__()
        self.backbone, _ = get_encoder_tokenizer_class(base_model)
        self.generator = ElectraForMaskedLM.from_pretrained('google/electra-small-generator')

    def forward(self, input_ids, attention_mask, labels):
        outputs = self.backbone(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )
        return outputs
