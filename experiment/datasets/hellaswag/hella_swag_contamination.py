import pandas as pd
import random
import json
from typing import List, Dict, Optional

class HellaSwagContaminator:
    def __init__(self, contamination_percent: float = 0.1):
        """
        Initialize the contaminator with the percentage of items to contaminate.
        :param contamination_percent: Percentage of items to contaminate (0.0 to 1.0).
        """
        self.contamination_percent = contamination_percent
        self.contamination_records = []

    def hs_contamination(
        self,
        df: pd.DataFrame,
        contamination_types: List[str] = ["question_contamination", "answer_contamination", "category_contamination", "label_contamination"],
        output_contamination_log: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Contaminate the dataset according to the specified types.
        :param df: Input DataFrame with HellaSwag data.
        :param contamination_types: List of contamination types to apply.
        :param output_contamination_log: Path to save the contamination log as JSON.
        :return: Contaminated DataFrame.
        """
        self.contamination_records = []

        if "question_contamination" in contamination_types:
            df = self._question_contamination(df)
        if "answer_contamination" in contamination_types:
            df = self._answer_contamination(df)
        if "category_contamination" in contamination_types:
            df = self._category_contamination(df)
        if "label_contamination" in contamination_types:
            df = self._label_contamination(df)

        if output_contamination_log:
            self._save_contamination_log(output_contamination_log)

        return df

    def _question_duplication_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        # Contaminate the 'ctx' (question/context) column by almost duplicating it. It should only be a near duplicate.
        # for that create a new entry which is a near duplicate of an existing one, it should not contain any answers
        return df

    def _answer_duplicate_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        # Contaminate one of the answer options ('endings'). by almost duplicating it. It should only be a near duplicate.
        # for that create a fith answer which is a near duplicate of one of the existing answers
        num_to_contaminate = int(len(df) * self.contamination_percent)
        indices = random.sample(range(len(df)), num_to_contaminate)

        for ind in indices:
            # Randomly select one of the four endings to contaminate
            answer_index = random.randint(0, 3)
            original_ending = df.at[ind, 'endings'][answer_index]
            # Example contamination: shuffle words in the ending
            contaminated_ending = ' '.join(random.sample(original_ending.split(), len(original_ending.split())))
            df.at[ind, 'endings'][answer_index] = contaminated_ending
            self.contamination_records.append({"type": "answer_contamination", "ind": f"{ind}-{answer_index}"})

        return df

    def _off_topic_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate one of the answer options ('endings')."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        indices = random.sample(range(len(df)), num_to_contaminate)

        for ind in indices:
            # Randomly select one of the four endings to contaminate
            answer_index = random.randint(0, 3)
            original_ending = df.at[ind, 'endings'][answer_index]
            # Example contamination: shuffle words in the ending
            contaminated_ending = ' '.join(random.sample(original_ending.split(), len(original_ending.split())))
            df.at[ind, 'endings'][answer_index] = contaminated_ending
            self.contamination_records.append({"type": "answer_contamination", "ind": f"{ind}-{answer_index}"})

        return df

    def _category_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate the 'activity_label' or 'split_type' (category) column."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        indices = random.sample(range(len(df)), num_to_contaminate)

        for ind in indices:
            original_category = df.at[ind, 'activity_label']
            # Example contamination: replace with a random category
            possible_categories = df['activity_label'].unique()
            contaminated_category = random.choice([cat for cat in possible_categories if cat != original_category])
            df.at[ind, 'activity_label'] = contaminated_category
            self.contamination_records.append({"type": "category_contamination", "ind": ind})

        return df

    def _label_contamination(self, df: pd.DataFrame) -> pd.DataFrame:
        """Contaminate the 'label' (correct answer index) column."""
        num_to_contaminate = int(len(df) * self.contamination_percent)
        indices = random.sample(range(len(df)), num_to_contaminate)

        for ind in indices:
            original_label = df.at[ind, 'label']
            # Example contamination: change to a random incorrect label
            contaminated_label = random.choice([i for i in range(4) if i != original_label])
            df.at[ind, 'label'] = contaminated_label
            self.contamination_records.append({"type": "label_contamination", "ind": ind})

        return df

    def _save_contamination_log(self, output_path: str) -> None:
        """Save the contamination records to a JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.contamination_records, f, indent=4)

if __name__ == "__main__":
    # Example usage
    df = pd.read_json("../../data/hellaswag/hellaswag_test.json", encoding='utf-8')
    contaminator = HellaSwagContaminator(contamination_percent=0.025)
    contaminated_df = contaminator.hs_contamination(
        df,
        contamination_types=["question_contamination", "answer_contamination", "category_contamination", "label_contamination"],
        output_contamination_log="../../data/hellaswag/contamination_log.json"
    )

    # Optionally, save the contaminated DataFrame
    contaminated_df.to_json("../../data/hellaswag/hellaswag_test_contaminated.json", orient="records", encoding='utf-8')
