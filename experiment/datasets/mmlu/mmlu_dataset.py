import math
from typing import Dict, Any, Tuple, List, Optional
import torch
import pandas as pd
from torch.utils.data import Dataset
from transformers import BatchEncoding
from tqdm.auto import tqdm
import json
from pathlib import Path


class MMLUDataset(Dataset):
    """Optimized MMLU dataset with pre-tokenization and caching."""

    def __init__(self, json_path: Path, tokenizer, max_length: int = 128,
                 cache_dir: Optional[str] = None, pre_tokenize: bool = True):
        """
        Args:
            json_path: Path to JSON file containing the dataset
            tokenizer: Hugging Face tokenizer
            max_length: Maximum sequence length
            cache_dir: Directory to cache pre-tokenized data
            pre_tokenize: Whether to pre-tokenize the dataset
        """
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.provide_tokenized_context = False
        self.name = "MMLU"
        self.path = json_path
        self.context_only_id_start = None

        # Load and validate data
        self._load_and_validate_data(json_path)

        # Pre-tokenize if requested
        if pre_tokenize:
            self._pre_tokenize_all(json_path, cache_dir)

    def _load_and_validate_data(self, path: Path) -> None:
        """Load and validate the dataset."""

        # Load with more efficient JSON parser if file is large
        if path.stat().st_size > 100 * 1024 * 1024:  # >100MB
            with open(path, 'r', encoding='utf-8') as f:
                self.raw_data = [json.loads(line) for line in tqdm(f, desc="Loading JSON")]
            self.df = pd.DataFrame(self.raw_data)
        else:
            self.df = pd.read_json(path, encoding='utf-8')

        # Validate required columns
        required_columns = ['question', 'choices', 'answer', 'subject']
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")

        # Create data points
        self.data_points = self._create_data_points_efficient()

        # iterate from last to first and find index where label == -1
        for i in range(len(self.data_points)-1, -1, -1):
            if self.data_points[i]['correct'] != -1:
                self.context_only_id_start = i
                break

    def _create_data_points_efficient(self) -> List[Dict[str, Any]]:
        """Create data points more efficiently using list comprehensions."""
        data_points = []

        for idx, entry in self.df.iterrows():
            context = entry["question"]
            correct_ending = entry["choices"][entry["answer"]]
            wrong_endings = [entry["choices"][i] for i in range(4) if i != entry["answer"]]

            # Add correct ending
            data_points.append({
                "text": f"{context} {correct_ending}",
                "correct": 1,
                "category": entry["subject"],
                "task_id": idx,
                "context_only": context
            })

            # Add wrong endings using list comprehension for efficiency
            data_points.extend({
                "text": f"{context} {wrong}",
                "correct": 0,
                "category": entry["subject"],
                "task_id": idx,
                "context_only": None
            } for wrong in wrong_endings)

        return data_points

    def _pre_tokenize_all(self, json_path: str, cache_dir: Optional[str] = None) -> None:
        """Pre-tokenize all texts and cache results."""
        cache_path = None
        if cache_dir:
            cache_dir = Path(cache_dir)
            cache_dir.mkdir(parents=True, exist_ok=True)
            file_name = Path(json_path).stem
            cache_path = cache_dir / f"{file_name}_{self.max_length}.pt"

            # Try to load cached tokenized data
            if cache_path.exists():
                self.tokenized_data = torch.load(cache_path, weights_only=False)
                return

        # Show progress bar for tokenization
        self.tokenized_data = []
        for item in tqdm(self.data_points, desc="Pre-tokenizing dataset"):
            tokenized = self.tokenizer(
                item["text"],
                padding='max_length',
                truncation=True,
                max_length=self.max_length,
                return_tensors='pt',
                return_token_type_ids=False
            )
            # Store as BatchEncoding for efficiency
            self.tokenized_data.append(tokenized)

        # Save to cache if directory provided
        if cache_path:
            torch.save(self.tokenized_data, cache_path)

    def _tokenize(self, text: str) -> BatchEncoding:
        """Tokenize a single text string."""
        return self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt',
            return_token_type_ids=False
        )

    def __len__(self) -> int:
        return len(self.data_points)

    def __getitem__(self, idx: int) -> tuple[dict[Any, Any], Any, Any, Any, dict[Any, Any], bool, str | None | Any, Any]:
        """Return tokenized sentence and label with optimized access."""
        item = self.data_points[idx]
        id = item["task_id"]
        label = item["correct"]
        category = item["category"]
        text = item["text"]

        # Use pre-tokenized data if available
        if hasattr(self, 'tokenized_data'):
            inputs = self.tokenized_data[idx]
            # Convert to regular dict and remove batch dimension
            inputs = {k: v.squeeze(0) for k, v in inputs.items()}
        else:
            # Tokenize on the fly if not pre-tokenized
            inputs = self._tokenize(text)
            inputs = {k: v.squeeze(0) for k, v in inputs.items()}

        # Handle context if needed
        context_flag = False
        context_text = None
        context_inputs = {k: v.clone() for k, v in inputs.items()}  # Shallow copy is sufficient

        if self.provide_tokenized_context:
            context_text = item["context_only"]
            if isinstance(context_text, str):
                context_inputs = self._tokenize(context_text)
                context_inputs = {k: v.squeeze(0) for k, v in context_inputs.items()}
                context_flag = True

        return inputs, label, category, text, context_inputs, context_flag, context_text, id

    def get_context_only_text(self, idx: int) -> Tuple[str, str]:
        """Return the context-only text for a given index, if available."""
        id_x_4 = idx * 4
        if id_x_4 <= self.context_only_id_start:
            data_point = self.data_points[id_x_4]
        else:
            diff = id_x_4 - self.context_only_id_start
            index = self.context_only_id_start + (diff // 4) + (diff % 4)
            data_point = self.data_points[index]
        return data_point["context_only"], data_point["task_id"].split('-')[0]

    def set_provide_tokenized_context(self, provide: bool) -> None:
        """Set whether to provide tokenized context separately."""
        self.provide_tokenized_context = provide

    def get_collate_fn(self):
        """Return a collate function for DataLoader that handles dynamic padding."""
        def collate_fn(batch):
            # Separate components
            inputs_list, labels, categories, texts, context_inputs_list, context_flags, context_text, id = zip(*batch)

            # Stack labels and convert to tensor
            labels = torch.stack(labels) if torch.is_tensor(labels[0]) else torch.tensor(labels)

            # Handle inputs with dynamic padding
            input_ids = torch.stack([item['input_ids'] for item in inputs_list])
            attention_masks = torch.stack([item['attention_mask'] for item in inputs_list])

            # Handle context inputs if needed
            context_inputs = None
            if any(context_flags):
                context_input_ids = torch.stack([item['input_ids'] for item in context_inputs_list])
                context_attention_masks = torch.stack([item['attention_mask'] for item in context_inputs_list])
                context_inputs = {
                    'input_ids': context_input_ids,
                    'attention_mask': context_attention_masks
                }

            return {
                'input_ids': input_ids,
                'attention_mask': attention_masks,
                'labels': labels,
                'categories': categories,
                'texts': texts,
                'context_inputs': context_inputs,
                'context_text': context_text,
                'ids': id
            }
        return collate_fn
