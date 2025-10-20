from torch.utils.data import Dataset
import pandas as pd
from typing import Dict, Any, Tuple
import torch

class HellaSwagDataset(Dataset):
    def __init__(self, json_path: str, tokenizer, max_length: int = 128):
        """HellaSwag dataset that returns tokenized sentences and labels."""
        # Load and validate data
        df = pd.read_json(json_path)
        self._validate_data(df)

        # Create data points
        self.data = self._create_data_points(df)
        self.tokenizer = tokenizer
        self.max_length = max_length

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
                "task_id": idx
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

    def __getitem__(self, idx) -> Tuple[Dict[str, torch.Tensor], int]:
        """Return tokenized sentence and label."""
        # Get the text and label
        text = self.data.iloc[idx]["text"]
        label = self.data.iloc[idx]["correct"]

        inputs = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )

        # Remove batch dimension from tokenized inputs
        inputs = {k: v.squeeze(0) for k, v in inputs.items()}

        return inputs, label
