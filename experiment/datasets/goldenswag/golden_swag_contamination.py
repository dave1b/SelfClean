import time
from pathlib import Path
import pandas as pd
import random
import json
import numpy as np
from loguru import logger
from typing import List, Set, Dict, Any
from datetime import datetime

from tqdm import tqdm

from experiment.datasets.goldenswag.off_topic_texts import get_off_topic_answer
from experiment.datasets.llm_api_util import generate_near_duplicate_mistral
from selfclean.cleaner.issue_manager import IssueTypes

seeded_random = random.Random(42)

class GoldenSwagContaminator:
    def __init__(self, contamination_ratios: Dict[IssueTypes, float]):
        self.contamination_ratios = contamination_ratios
        self.contaminated_indices: Set[int] = set()

    def hs_contamination(self, file: Path, contamination_types: List[IssueTypes]) -> None:
        for contamination_type in contamination_types:
            if contamination_type == IssueTypes.NEAR_DUPLICATES_Q:
                self._question_duplication_contamination(file)
            elif contamination_type == IssueTypes.NEAR_DUPLICATES:
                self._answer_duplicate_contamination(file)
            elif contamination_type == IssueTypes.OFF_TOPIC_SAMPLES:
                self._off_topic_contamination(file)
            elif contamination_type == IssueTypes.CATEGORY_ERRORS:
                self._category_contamination(file)
            elif contamination_type == IssueTypes.LABEL_ERRORS:
                self._label_contamination(file)

    def _get_uncontaminated_indices(self, df: pd.DataFrame) -> List[int]:
        all_indices = set(df['ind'].tolist())
        return list(all_indices - self.contaminated_indices)

    @staticmethod
    def _replace_unicode_character(text: str) -> str:
        replace_dict = {
            "’" : "'",
            "–" : ", ",
            "°" : "º"
        }
        for char in text:
            if char in replace_dict:
                text = text.replace(char, replace_dict[char])
        return text


    def _question_duplication_contamination(self, file: Path) -> None:
        df = pd.read_json(file, encoding='utf-8')
        contamination_records = []
        num_to_contaminate = int(len(df) * self.contamination_ratios[IssueTypes.NEAR_DUPLICATES_Q])
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = seeded_random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in tqdm(indices, desc="Generating near duplicates for questions"):
            row_index = df[df['ind'] == ind].index[0]
            original_ctx = df.at[row_index, 'ctx']
            contaminated_ctx = generate_near_duplicate_mistral(original_ctx)
            cleaned_contaminated_ctx = self._replace_unicode_character(contaminated_ctx)
            new_ind = f"x{ind}"
            new_row = df.loc[row_index].copy()
            new_row['ind'] = new_ind
            new_row['ctx'] = cleaned_contaminated_ctx
            new_row['endings'] = []
            new_row['label'] = -1
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            contamination_records.append({
                "type": "question_duplication",
                "id_1": ind,
                "id_2": new_ind,
                "original_ctx": original_ctx,
                "contaminated_ctx": cleaned_contaminated_ctx,
                "timestamp": datetime.now().isoformat()
            })
            self.contaminated_indices.add(ind)
            time.sleep(0.1)

        self._save_contamination_results(file, df, contamination_records, IssueTypes.NEAR_DUPLICATES_Q)

    def _answer_duplicate_contamination(self, file: Path) -> None:
        df = pd.read_json(file, encoding='utf-8')
        contamination_records = []
        num_to_contaminate = int(len(df) * self.contamination_ratios[IssueTypes.NEAR_DUPLICATES])
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = seeded_random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in tqdm(indices, desc="Generating near duplicates for answers"):
            row_index = df[df['ind'] == ind].index[0]
            correct_ending = df.at[row_index, 'label']
            answer_index = random.choice([i for i in range(4) if i != correct_ending])
            original_ending = df.at[row_index, 'endings'][answer_index]
            contaminated_ending = generate_near_duplicate_mistral(original_ending)
            cleaned_contaminated_ctx = self._replace_unicode_character(contaminated_ending)
            df.at[row_index, 'endings'].append(cleaned_contaminated_ctx)
            contamination_records.append({
                "type": "answer_duplicate",
                "id_1": f"{ind}-{answer_index}",
                "id_2": f"{ind}-4",
                "original_ending": original_ending,
                "contaminated_ending": cleaned_contaminated_ctx,
                "timestamp": datetime.now().isoformat()
            })
            self.contaminated_indices.add(ind)
            time.sleep(0.1)

        self._save_contamination_results(file, df, contamination_records, IssueTypes.NEAR_DUPLICATES)

    def _off_topic_contamination(self, file: Path) -> None:
        df = pd.read_json(file, encoding='utf-8')
        contamination_records = []
        num_to_contaminate = int(len(df) * self.contamination_ratios[IssueTypes.OFF_TOPIC_SAMPLES])
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = seeded_random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]
            answer_index = random.randint(0, 3)
            original_ending = df.at[row_index, 'endings'][answer_index]
            contaminated_ending = seeded_random.choice(get_off_topic_answer())
            df.at[row_index, 'endings'][answer_index] = contaminated_ending
            contamination_records.append({
                "type": "off_topic",
                "id": f"{ind}-{answer_index}",
                "original_ending": original_ending,
                "contaminated_ending": contaminated_ending,
                "timestamp": datetime.now().isoformat()
            })
            self.contaminated_indices.add(ind)

        self._save_contamination_results(file, df, contamination_records, IssueTypes.OFF_TOPIC_SAMPLES)

    def _category_contamination(self, file: Path) -> None:
        df = pd.read_json(file, encoding='utf-8')
        contamination_records = []
        num_to_contaminate = int(len(df) * self.contamination_ratios[IssueTypes.CATEGORY_ERRORS]) // 4
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = seeded_random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]
            original_category = df.at[row_index, 'activity_label']
            possible_categories = df['activity_label'].unique()
            contaminated_category = random.choice([cat for cat in possible_categories if cat != original_category])
            df.at[row_index, 'activity_label'] = contaminated_category
            for i in [0,1,2,3]:
                id = f"{ind}-{i}"
                contamination_records.append({
                    "type": "category_error",
                    "id": id,
                    "original_category": original_category,
                    "contaminated_category": contaminated_category,
                    "timestamp": datetime.now().isoformat()
                })
                self.contaminated_indices.add(id)

        self._save_contamination_results(file, df, contamination_records, IssueTypes.CATEGORY_ERRORS)

    def _label_contamination(self, file: Path) -> None:
        df = pd.read_json(file, encoding='utf-8')
        contamination_records = []
        num_to_contaminate = int(len(df) * self.contamination_ratios[IssueTypes.LABEL_ERRORS]) // 2
        uncontaminated_indices = self._get_uncontaminated_indices(df)
        indices = seeded_random.sample(uncontaminated_indices, min(num_to_contaminate, len(uncontaminated_indices)))

        for ind in indices:
            row_index = df[df['ind'] == ind].index[0]
            original_label = df.at[row_index, 'label']
            contaminated_label = random.choice([i for i in range(4) if i != original_label])
            df.at[row_index, 'label'] = contaminated_label
            contamination_records.append({
                "type": "label_error",
                "id": f"{ind}-{original_label}",
                "original_label": original_label,
                "contaminated_label": contaminated_label,
                "timestamp": datetime.now().isoformat()
            })
            contamination_records.append({
                "type": "label_error",
                "id": f"{ind}-{contaminated_label}",
                "original_label": original_label,
                "contaminated_label": contaminated_label,
                "timestamp": datetime.now().isoformat()
            })
            self.contaminated_indices.add(ind)

        self._save_contamination_results(file, df, contamination_records, IssueTypes.LABEL_ERRORS)

    def _save_contamination_results(
        self,
        file: Path,
        df: pd.DataFrame,
        contamination_records: List[Dict[str, Any]],
        contamination_type: IssueTypes
    ) -> None:
        contaminated_path = file.with_stem(f"{file.stem}_synthetic_{contamination_type.value.upper()}")
        contaminated_log_path = file.with_stem(f"{file.stem}_synthetic_{contamination_type.value.upper()}_logs")

        def convert_types(obj):
            if isinstance(obj, (np.int64, np.int32)):
                return int(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        df.to_json(contaminated_path, orient="records", indent=4)
        with open(contaminated_log_path, 'w', encoding='utf-8') as f:
            json.dump(contamination_records, f, indent=4, default=convert_types)
        logger.info(f"Saved {len(contamination_records)} {contamination_type} contamination records to {contaminated_log_path}.")

if __name__ == "__main__":
    contamination_types = [
        IssueTypes.OFF_TOPIC_SAMPLES,
        IssueTypes.NEAR_DUPLICATES_Q,
        IssueTypes.NEAR_DUPLICATES,
        IssueTypes.LABEL_ERRORS,
        IssueTypes.CATEGORY_ERRORS
    ]
    contamination_ratios = {
        IssueTypes.OFF_TOPIC_SAMPLES: 0.05,
        IssueTypes.NEAR_DUPLICATES_Q: 0.05,
        IssueTypes.NEAR_DUPLICATES: 0.05,
        IssueTypes.LABEL_ERRORS: 0.1,
        IssueTypes.CATEGORY_ERRORS: 0.1,
    }
    file_path = Path("golden_swag_train.json")
    contaminator = GoldenSwagContaminator(contamination_ratios)
    contaminator.hs_contamination(file_path, contamination_types)
