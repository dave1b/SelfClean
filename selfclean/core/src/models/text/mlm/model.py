from ..encoders.utils import get_encoder_tokenizer_class
import torch
import torch.nn as nn

class MlmModel(nn.Module):
    def __init__(self, base_model: str, mlm_probability: float = 0.15):
        super(MlmModel, self).__init__()
        self.backbone, tokenizer = get_encoder_tokenizer_class(base_model)
        self.mlm_probability = mlm_probability
        self.mask_token_id = tokenizer.mask_token_id
        self.cls_token_id = tokenizer.cls_token_id
        self.sep_token_id = tokenizer.sep_token_id
        self.vocab_size = self.backbone.config.vocab_size

    def forward(self, input_ids, attention_mask):
        # Create a random mask for MLM
        batch_size, seq_length = input_ids.shape
        rand_mask = torch.rand(batch_size, seq_length, device=input_ids.device) < self.mlm_probability
        # Do not mask special tokens
        rand_mask = rand_mask & (attention_mask == 1) & (input_ids != self.cls_token_id) & (input_ids != self.sep_token_id)

        masked_input = input_ids.clone()
        masked_input[rand_mask] = self.mask_token_id

        outputs = self.backbone(input_ids=masked_input, attention_mask=attention_mask)
        logits = outputs.logits

        return logits, rand_mask
