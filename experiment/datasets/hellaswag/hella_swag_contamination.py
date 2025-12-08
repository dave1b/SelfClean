from pathlib import Path
import pandas as pd
import random
import json
from typing import List, Optional, Set

from duckdb.experimental.spark import DataFrame

from experiment.datasets.llm_api_util import generate_near_duplicate_mistral


class HellaSwagContaminator:
    def __init__(self, contamination_percent: float = 0.1):
        """
        Initialize the contaminator with the percentage of items to contaminate.
        :param contamination_percent: Percentage of items to contaminate (0.0 to 1.0).
        """
        self.contamination_percent = contamination_percent
        self.contamination_records = []
        self.contaminated_indices: Set[int, str] = set()  # Track contaminated 'ind' values to avoid overlap

    def hs_contamination(
        self,
        file: Path,
        contamination_types: List[str] = [
            "question_duplication_contamination",
            "answer_duplicate_contamination",
            "off_topic_contamination",
            "category_contamination",
            "label_contamination"
        ]
    ) -> pd.DataFrame:
        """
        Contaminate the dataset according to the specified types.
        :param df: Input DataFrame with HellaSwag data.
        :param contamination_types: List of contamination types to apply.
        :param output_contamination_log: Path to save the contamination log as JSON.
        :return: Contaminated DataFrame.
        """
        self.contamination_records = []
        self.contaminated_indices = set()

        df = pd.read_json(file, encoding='utf-8')

        if "question_duplication_contamination" in contamination_types:
            df = self._question_duplication_contamination(df)
        if "answer_duplicate_contamination" in contamination_types:
            df = self._answer_duplicate_contamination(df)
        if "off_topic_contamination" in contamination_types:
            df = self._off_topic_contamination(df)
        if "category_contamination" in contamination_types:
            df = self._category_contamination(df)
        if "label_contamination" in contamination_types:
            df = self._label_contamination(df)

        contaminated_path = Path(f"{file.stem}_{contamination_type}.json")
        contaminated_log_path = Path(f"{file.stem}_{contamination_type}_logs.json")

        self._save_file(contaminated_path, df)
        self._save_file(contaminated_log_path, self.contamination_records)

        return df

    def _get_uncontaminated_indices(self, df: pd.DataFrame) -> List[int]:
        """Return a list of 'ind' values that have not been contaminated yet."""
        all_indices = set(df['ind'].tolist())
        uncontaminated_indices = list(all_indices - self.contaminated_indices)
        return uncontaminated_indices

    def _question_duplication_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate by adding a near-duplicate question using Mistral."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]  # Get the DataFrame index for the 'ind' value
            original_ctx = df.at[row_index, 'ctx']
            contaminated_ctx = generate_near_duplicate_mistral(original_ctx)

            # Add the near-duplicate as a new row (without answers)
            new_ind = f"x{ind}"
            new_row = df.loc[row_index].copy()
            new_row['ind'] = new_ind  # Assign a unique identifier for the new row
            new_row['ctx'] = contaminated_ctx
            new_row['endings'] = []  # No answers for the near-duplicate question
            new_row['label'] = -1  # Mark as invalid

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            self.contamination_records.append({"type": "question_duplication_contamination", "id_1": ind, "id_2": new_ind, "id": None})
            self.contaminated_indices.add(ind)
            self.contaminated_indices.add(new_ind)

        return df

    def _answer_duplicate_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate by adding a fifth near-duplicate answer using Mistral."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]  # Get the DataFrame index for the 'ind' value
            # Randomly select one of the four endings to duplicate
            correct_ending = df.at[row_index, 'label']
            # one of the four endings to duplicate but not the correct one
            answer_index = random.choice([i for i in range(4) if i != correct_ending])

            original_ending = df.at[row_index, 'endings'][answer_index]
            contaminated_ending = generate_near_duplicate_mistral(original_ending)

            # Add the near-duplicate as a fifth answer
            df.at[row_index, 'endings'].append(contaminated_ending)
            self.contamination_records.append(
                {"type": "answer_duplicate_contamination", "id_1": f"{ind}-{answer_index}", "id_2": f"{ind}-4", "id": None})
            self.contaminated_indices.add(ind)

        return df

    def _off_topic_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate one of the answer options ('endings') with off-topic text."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        off_topic_texts = [
            "print('Hello, World!'), for i in range(10): pass",
            "`!##^ The capital of Fr$nce is P$ris. ####",
            "def fibonacci(n): a, b = 0, 1; for _ in range(n): a, b = b, a + b; return a",
            "<html><head><title>Test</title></head><body><h1>Hello World</h1></body></html>",
            "SELECT * FROM users WHERE age > 30;",
            "E = mc^2; F = ma; a^2 + b^2 = c^2",
        ]

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]  # Get the DataFrame index for the 'ind' value
            # Randomly select one of the four endings to contaminate
            answer_index = random.randint(0, 3)
            df.at[row_index, 'endings'][answer_index] = random.choice(off_topic_texts)
            self.contamination_records.append({"type": "off_topic_contamination", "id": f"{ind}-{answer_index}", "id_1": None, "id_2": None})
            self.contaminated_indices.add(ind)

        return df

    def _category_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate the 'activity_label' (category) column."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]  # Get the DataFrame index for the 'ind' value
            original_category = df.at[row_index, 'activity_label']
            possible_categories = df['activity_label'].unique()
            contaminated_category = random.choice([cat for cat in possible_categories if cat != original_category])
            df.at[row_index, 'activity_label'] = contaminated_category
            self.contamination_records.append({"type": "category_contamination", "id": ind, "id_1": None, "id_2": None})
            self.contaminated_indices.add(ind)

        return df

    def _label_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate the 'label' (correct answer index) column."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]  # Get the DataFrame index for the 'ind' value
            original_label = df.at[row_index, 'label']
            contaminated_label = random.choice([i for i in range(4) if i != original_label])
            df.at[row_index, 'label'] = contaminated_label
            self.contamination_records.append({"type": "label_contamination", "id": ind, "id_1": None, "id_2": None})
            self.contaminated_indices.add(ind)

        return df

    @staticmethod
    def _save_file(output_path: Path, data: DataFrame | List):
        """Save the contamination records to a JSON file."""
        if isinstance(data, list):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        elif isinstance(data, pd.DataFrame):
            data.to_json(output_path, orient="records")


if __name__ == "__main__":
    # Example usage
    contamination_type = "question_duplication_contamination"
    # "answer_duplicate_contamination"
    # "off_topic_contamination"
    # "category_contamination"
    # "label_contamination"

    file_path = Path("hellaswag_train_0.01ksubset.json")

    contaminator = HellaSwagContaminator(contamination_percent=0.1)

    contaminated_df = contaminator.hs_contamination(
        file_path,
        contamination_types=[contamination_type]
    )
