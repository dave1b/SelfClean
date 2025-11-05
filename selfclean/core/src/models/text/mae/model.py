from transformers import BertConfig, BertModel

from ..encoders.utils import get_encoder_tokenizer_class

import torch
import torch.nn as nn

class BertMae(nn.Module):
    def __init__(self, base_model: str, encoder_mask_ratio: float = 0.75, decoder_mask_ratio: float = 0.25):
        super(BertMae, self).__init__()
        self.encoder, tokenizer = get_encoder_tokenizer_class(base_model)
        decoder_config = BertConfig(
            num_hidden_layers=2,
            hidden_size=self.encoder.config.hidden_size,
            intermediate_size=self.encoder.config.intermediate_size,
            num_attention_heads=self.encoder.config.num_attention_heads,
            is_decoder=True,
            add_cross_attention=True
        )
        self.decoder = BertModel(decoder_config)

        self.encoder_mask_ratio = encoder_mask_ratio
        self.decoder_mask_ratio = decoder_mask_ratio
        self.mask_token_id = tokenizer.mask_token_id

        # Projection layer to map encoder hidden size to vocab size for reconstruction
        self.proj = nn.Linear(self.encoder.config.hidden_size, self.encoder.config.vocab_size)

    def forward(self, input_ids, attention_mask=None):

        if self.training:
            batch_size, seq_length = input_ids.shape

            # Create a random mask for the encoder input
            encoder_mask = torch.rand(batch_size, seq_length, device=input_ids.device) < self.encoder_mask_ratio
            masked_input = input_ids.clone()
            masked_input[encoder_mask] = self.mask_token_id

            # Encode the masked input
            encoder_outputs = self.encoder(input_ids=masked_input, attention_mask=attention_mask)
            encoder_hidden_states = encoder_outputs.last_hidden_state  # Shape: [batch_size, seq_length, hidden_size]

            decoder_input_ids = torch.full_like(input_ids, self.mask_token_id)

            # Decoder forward pass: use encoder_hidden_states for cross-attention
            decoder_outputs = self.decoder(
                input_ids=decoder_input_ids,
                attention_mask=attention_mask,
                encoder_hidden_states=encoder_hidden_states,
                encoder_attention_mask=attention_mask,
            )
            decoder_hidden_states = decoder_outputs.last_hidden_state  # Shape: [batch_size, seq_length, hidden_size]

            # Project decoder hidden states to vocab size for loss calculation
            reconstructed_token_logits = self.proj(decoder_hidden_states)  # Shape: [batch_size, seq_length, vocab_size]

            return encoder_hidden_states, reconstructed_token_logits
        else:
            # In evaluation mode, just return the encoder outputs
            encoder_outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
            return encoder_outputs

    def get_encoder_model(self):
        return self.encoder
