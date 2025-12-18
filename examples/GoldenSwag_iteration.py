import json
import time
from pathlib import Path
from typing import List, Optional

import pandas as pd
from loguru import logger
from datetime import datetime
from selfclean import SelfClean
from selfclean.cleaner.issue_manager import IssueTypes

# Constants
CONTAMINATED_PATHS = [
    Path('../experiment/datasets/GoldenSwag/golden_swag_train_synthetic_CATEGORY_ERRORS.json'),
    Path('../experiment/datasets/GoldenSwag/golden_swag_train_synthetic_LABEL_ERRORS.json'),
    Path('../experiment/datasets/GoldenSwag/golden_swag_train_synthetic_NEAR_DUPLICATES.json'),
    Path('../experiment/datasets/GoldenSwag/golden_swag_train_synthetic_NEAR_DUPLICATES_QUESTIONS.json'),
    Path('../experiment/datasets/GoldenSwag/golden_swag_train_synthetic_OFF_TOPIC_SAMPLES.json'),
]

ISSUES_TO_DETECT: List[IssueTypes] = [
    IssueTypes.OFF_TOPIC_SAMPLES,
    # IssueTypes.NEAR_DUPLICATES_Q,
    # IssueTypes.NEAR_DUPLICATES,
    IssueTypes.LABEL_ERRORS,
    # IssueTypes.CATEGORY_ERRORS
]


def get_issue_type_from_path(path: Path) -> Optional[IssueTypes]:
    for issue in ISSUES_TO_DETECT:
        if issue.value.upper() in str(path):
            return issue
    return None


def evaluate(pretraining_type: str, base_model: str):
    logger.info(f"Starting evaluation with pretraining_type={pretraining_type}, base_model={base_model}")

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = Path(__file__).parent.parent / "examples" / "output" / f"goldenswag_{pretraining_type}" / timestamp_str
    output_path.mkdir(parents=True, exist_ok=False)

    summarized_log_dict = {}
    summarized_log_dict['timestamp'] = timestamp_str  # Add timestamp as a top-level key

    for contaminated_path in CONTAMINATED_PATHS:
        if not contaminated_path.exists():
            logger.warning(f"Path does not exist: {contaminated_path}")
            continue

        issue_to_detect = get_issue_type_from_path(contaminated_path)
        if issue_to_detect is None:
            logger.warning(f"Could not determine issue type for path: {contaminated_path}")
            continue

        log_file = contaminated_path.parent / f"{contaminated_path.stem}_logs.json"

        if not log_file.exists():
            logger.warning(f"Contamination log file not found: {log_file}")
            continue

        logger.info(f"Processing {issue_to_detect.value} from {contaminated_path.name}")
        start_time = time.time()

        selfclean = SelfClean(plot_top_N=400, output_path=output_path)
        issue_manager, _ = selfclean.run_on_text_dataset(
            dataset_path=contaminated_path,
            contamination_log_path=log_file,
            pretraining_type=pretraining_type,
            epochs=0,
            batch_size=32,
            dataset_name="hellaswag",
            base_model=base_model,
            wandb_logging=False,
            issues_to_detect=[issue_to_detect]
        )
        summarized_log_dict[issue_to_detect.value] = {
            **{'data': contaminated_path.name, 'base_model': base_model},
            **issue_manager.metric_dict
        }

        elapsed_time = (time.time() - start_time) / 60
        logger.success(f"Finished {issue_to_detect.value} in {elapsed_time:.2f} minutes")

    with open(output_path / "summary.json", 'w') as f:
        json.dump(summarized_log_dict, f, indent=2)


def main():
    evaluate(pretraining_type="simcse", base_model="golden_swag_train_simcse_bert")


if __name__ == "__main__":
    main()
