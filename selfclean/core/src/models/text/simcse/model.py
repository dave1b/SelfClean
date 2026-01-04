import torch.nn as nn
import torch.nn.functional as F
from ..encoders.utils import get_encoder_tokenizer_class


class SimCSEModel(nn.Module):
    def __init__(self, base_model: str):
        super(SimCSEModel, self).__init__()
        self.backbone, _ = get_encoder_tokenizer_class(base_model)
        self.backbone.dropout = nn.Dropout(p=0.1)
        n_feat = self.backbone.config.hidden_size

        # Projection MLP
        self.dense1 = nn.Linear(n_feat, n_feat)
        self.dense2 = nn.Linear(n_feat, n_feat)
        self.dropout = nn.Dropout(0.1)  # Match backbone dropout
        nn.init.xavier_uniform_(self.dense1.weight)
        nn.init.xavier_uniform_(self.dense2.weight)

    def forward(self, input_ids, attention_mask):
        outputs = self.backbone(input_ids, attention_mask)
        cls_embedding = outputs.last_hidden_state[:, 0, :]   # [CLS] token representation

        z = self.dense1(cls_embedding)
        z = F.relu(z)
        z = self.dropout(z)
        z = self.dense2(z)
        z = F.normalize(z, dim=1)
        return cls_embedding, z
