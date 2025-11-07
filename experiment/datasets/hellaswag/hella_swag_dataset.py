from copy import deepcopy

from torch.utils.data import Dataset
import pandas as pd
from typing import Dict, Any, Tuple
import torch

class HellaSwagDataset(Dataset):
    def __init__(self, json_path: str, tokenizer, max_length: int = 128):
        """HellaSwag dataset that returns tokenized sentences and labels."""
        # Load and validate data
        df = pd.read_json(json_path, encoding="utf-8")
        self._validate_data(df)

        # Create data points
        self.data = self._create_data_points(df)
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.provide_tokenized_context = False

    def _validate_data(self, df: pd.DataFrame) -> None:
        """Validate that the dataset has the required structure."""
        required_columns = ['ctx', 'endings', 'label', 'activity_label']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Dataset is missing required columns: {missing}")

    def _create_data_points(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create data points from the raw dataset."""
        data_points = []

        for idx, entry in df.iterrows():
            context = entry["ctx"]
            correct_ending = entry["endings"][entry["label"]]
            wrong_endings = [entry["endings"][i] for i in [0, 1, 2, 3] if i != entry["label"]]

            # Add correct ending
            data_points.append({
                "text": context + " " + correct_ending,
                "correct": 1,
                "category": entry["activity_label"],
                "task_id": idx,
                "context_only": context
            })

            # Add wrong endings
            for wrong in wrong_endings:
                data_points.append({
                    "text": context + " " + wrong,
                    "correct": 0,
                    "category": entry["activity_label"],
                    "task_id": idx
                })

        return pd.DataFrame(data_points)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx) -> Tuple[Dict[str, torch.Tensor], int, str, str, Dict[str, torch.Tensor], bool]:
        """Return tokenized sentence and label."""
        # Get the text and label
        text = self.data.iloc[idx]["text"]
        label = self.data.iloc[idx]["correct"]
        category = self.data.iloc[idx]["category"]

        inputs = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )
        # Remove batch dimension from tokenized inputs
        inputs = {k: v.squeeze(0) for k, v in inputs.items()}

        context_flag = False
        context_inputs = deepcopy(inputs)
        if self.provide_tokenized_context:
            context = self.data.iloc[idx]["context_only"]
            if isinstance(context, str):
                context_inputs = self.tokenizer(
                    context,
                    padding='max_length',
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors='pt'
                )
                context_inputs = {k: v.squeeze(0) for k, v in context_inputs.items()}
                context_flag = True

        return inputs, label, category, text, context_inputs, context_flag

    def set_provide_tokenized_context(self, provide: bool) -> None:
        """Set whether to provide tokenized context separately."""
        self.provide_tokenized_context = provide
