import torch
import torch.nn as nn
import torch.nn.functional as F
from ..encoders.utils import get_encoder_tokenizer_class

class BertSimCSE(nn.Module):
    def __init__(self, base_model: str):
        super(BertSimCSE, self).__init__()
        encoder_cls, _ = get_encoder_tokenizer_class(base_model)
        self.backbone = encoder_cls
        n_feat = self.backbone.config.hidden_size
        # Projection MLP
        self.dense1 = nn.Linear(n_feat, n_feat)
        self.dense2 = nn.Linear(n_feat, n_feat)
        self.dropout = nn.Dropout(0.1)  # Match backbone dropout
        nn.init.xavier_uniform_(self.dense1.weight)
        nn.init.xavier_uniform_(self.dense2.weight)

    def forward(self, **kwargs):
        outputs = self.backbone(**kwargs, output_hidden_states=True)
        hidden_states = outputs.hidden_states
        cls_embedding = hidden_states[-1][:, 0, :]


        if self.training:
            z = self.dense1(cls_embedding)
            z = F.relu(z)
            z = self.dropout(z)
            z = self.dense2(z)
            z = F.normalize(z, dim=1)
            return cls_embedding, z
        else:
            return cls_embedding

