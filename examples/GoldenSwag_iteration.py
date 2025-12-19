import json
import shutil
import time
from pathlib import Path
from typing import List, Optional, Dict, Any

import pandas as pd
from loguru import logger
from datetime import datetime
from selfclean import SelfClean
from selfclean.cleaner.issue_manager import IssueTypes

# Constants
CONTAMINATED_PATHS = [
    Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_CATEGORY_ERRORS.json'),
    Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_LABEL_ERRORS.json'),
    Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_NEAR_DUPLICATES.json'),
    Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_NEAR_DUPLICATES_QUESTIONS.json'),
    Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_OFF_TOPIC_SAMPLES.json'),
]

ISSUES_TO_DETECT: List[IssueTypes] = [
    IssueTypes.CATEGORY_ERRORS,
    IssueTypes.LABEL_ERRORS,
    IssueTypes.NEAR_DUPLICATES_Q,
    IssueTypes.NEAR_DUPLICATES,
    IssueTypes.OFF_TOPIC_SAMPLES,
]

BASE_MODELS = [
    "golden_swag_train_electra_bert_1",
    "golden_swag_train_electra_bert_6",
    "golden_swag_train_electra_bert_22",

    "golden_swag_train_simcse_bert_1",
    "golden_swag_train_simcse_bert_4",
    "golden_swag_train_simcse_bert_8",

    "golden_swag_train_mae_bert_1",
    "golden_swag_train_mae_bert_7",
    "golden_swag_train_mae_bert_15",
]

PRETRAINING_TYPES = ["simcse", "electra", "mae"]


def get_issue_type_from_path(path: Path) -> Optional[IssueTypes]:
    for issue in ISSUES_TO_DETECT:
        if issue.value.upper() in str(path):
            return issue
    return None


def clear_cache(cache_path: Path):
    if cache_path.is_dir():
        shutil.rmtree(cache_path)


def generate_markdown_table(data: Dict[str, Any], base_output_path: Path) -> None:
    for issue_type in ISSUES_TO_DETECT:
        issue_key = issue_type.value
        if issue_key not in data:
            continue

        issue_data = data[issue_key]
        rows = []

        for model, metrics in issue_data.items():
            row = {
                "Model": model,
                "AP": metrics.get("AP", "N/A"),
                "AUROC": metrics.get("AUROC", "N/A")
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        markdown_table = df.to_markdown(tablefmt="github", index=False)

        output_path = base_output_path / f"{issue_key}.md"
        with open(output_path, 'w') as f:
            f.write(f"# {issue_key.replace('_', ' ').title()}\n\n")
            f.write(markdown_table)



def evaluate():
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_output_path = Path(__file__).parent.parent / "examples" / "output" / "goldenswag" / timestamp_str
    base_output_path.mkdir(parents=True, exist_ok=False)

    summarized_log_dict = {}
    summarized_log_dict['timestamp'] = timestamp_str
    for issue in ISSUES_TO_DETECT:
        summarized_log_dict[issue.value] = {}

    number_of_runs = len(ISSUES_TO_DETECT) * len(CONTAMINATED_PATHS) * len(PRETRAINING_TYPES)

    for i, contaminated_path in enumerate(CONTAMINATED_PATHS):
        logger.info(f"Start performing run {i}/{number_of_runs}")
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

        for model in BASE_MODELS:
            pretraining_type = None
            for type in PRETRAINING_TYPES:
                if type in model:
                    pretraining_type = type
                    break

            logger.info(
                f"Starting evaluation {issue_to_detect.value} from {contaminated_path.name}, with pretraining_type={pretraining_type}, base_model={model}")
            start_time = time.time()
            output_path = Path(
                __file__).parent.parent / "examples" / "output" / "goldenswag" / timestamp_str / f"{issue_to_detect.value}_{model}"
            output_path.mkdir(parents=False, exist_ok=True)

            selfclean = SelfClean(plot_top_N=400, output_path=output_path)
            issue_manager, _ = selfclean.run_on_text_dataset(
                dataset_path=contaminated_path,
                contamination_log_path=log_file,
                pretraining_type=pretraining_type,
                epochs=0,
                batch_size=32,
                dataset_name="hellaswag",
                base_model=model,
                wandb_logging=False,
                issues_to_detect=[issue_to_detect]
            )
            summarized_log_dict[issue_to_detect.value][model] = {
                **{'data': contaminated_path.name},
                **issue_manager.metric_dict
            }

            elapsed_time = (time.time() - start_time) / 60
            logger.success(f"Finished {issue_to_detect.value} in {elapsed_time:.2f} minutes")

    with open(base_output_path / "summary.json", 'w') as f:
        json.dump(summarized_log_dict, f, indent=2)
    generate_markdown_table(summarized_log_dict, base_output_path)


def main():
    cache_dir = Path(__file__).parent / ".cache"
    clear_cache(cache_dir)
    evaluate()
    clear_cache(cache_dir)


if __name__ == "__main__":
    main()
