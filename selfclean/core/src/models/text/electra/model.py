import torch.nn as nn

from ..encoders.utils import get_encoder_tokenizer_class


class ElectraModel(nn.Module):
    def __init__(self, base_model):
        super(ElectraModel, self).__init__()
        self.backbone, _ = get_encoder_tokenizer_class(base_model)

    def forward(self, input_ids, attention_mask, labels):
        if self.backbone.training:
            token_type_ids = None
            outputs = self.backbone(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
                labels=labels,
            )
            return outputs
        else:
            outputs = self.backbone(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )
            return outputs
