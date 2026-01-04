import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
from loguru import logger
from datetime import datetime

from selfclean import SelfClean
from selfclean.cleaner.issue_manager import IssueTypes
from selfclean.core.src.pkg.helper import EmbeddingPoolingType

# Unified configuration
CONFIG = {
    "contaminated_paths": {
        IssueTypes.NEAR_DUPLICATES: Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_NEAR_DUPLICATES.json'),
        IssueTypes.NEAR_DUPLICATES_Q: Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_NEAR_DUPLICATES_QUESTIONS.json'),
        IssueTypes.OFF_TOPIC_SAMPLES: Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_OFF_TOPIC_SAMPLES.json'),
        IssueTypes.CATEGORY_ERRORS: Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_CATEGORY_ERRORS.json'),
        IssueTypes.LABEL_ERRORS: Path('../experiment/datasets/goldenswag/golden_swag_train_synthetic_LABEL_ERRORS.json'),
    },

    "models": {
        IssueTypes.NEAR_DUPLICATES: [
            "bert",
            "deberta",
            # SimCSE models
            # "golden_swag_train_simcse_NEAR_DUPLICATES_1",
            # "golden_swag_train_simcse_NEAR_DUPLICATES_10",
            # "golden_swag_train_simcse_NEAR_DUPLICATES_20",
            "golden_swag_train_simcse_NEAR_DUPLICATES_35",
            # Electra models
            # "golden_swag_train_electra_NEAR_DUPLICATE_1",
            # "golden_swag_train_electra_NEAR_DUPLICATE_10",
            # "golden_swag_train_electra_NEAR_DUPLICATE_20",
            "golden_swag_train_electra_NEAR_DUPLICATE_35",
            # MAE models
            # "golden_swag_train_mae_NEAR_DUPLICATE_1",
            # "golden_swag_train_mae_NEAR_DUPLICATE_10",
            # "golden_swag_train_mae_NEAR_DUPLICATE_20",
            "golden_swag_train_mae_NEAR_DUPLICATE_35",
            # MLM models
            # "golden_swag_train_mlm_NEAR_DUPLICATE_1",
            # "golden_swag_train_mlm_NEAR_DUPLICATE_10",
            # "golden_swag_train_mlm_NEAR_DUPLICATE_20",
            "golden_swag_train_mlm_NEAR_DUPLICATE_35",
        ],
        IssueTypes.NEAR_DUPLICATES_Q: [
            "bert",
            "deberta",
            # SimCSE models
            # "golden_swag_train_simcse_NEAR_DUPLICATES_Q_1",
            # "golden_swag_train_simcse_NEAR_DUPLICATES_Q_10",
            # "golden_swag_train_simcse_NEAR_DUPLICATES_Q_20",
            "golden_swag_train_simcse_NEAR_DUPLICATES_Q_35",
            # Electra models
            # "golden_swag_train_electra_NEAR_DUPLICATE_Q_1",
            # "golden_swag_train_electra_NEAR_DUPLICATE_Q_10",
            # "golden_swag_train_electra_NEAR_DUPLICATE_Q_20",
            "golden_swag_train_electra_NEAR_DUPLICATE_Q_35",
            # MAE models
            # "golden_swag_train_mae_NEAR_DUPLICATE_Q_1",
            # "golden_swag_train_mae_NEAR_DUPLICATE_Q_10",
            # "golden_swag_train_mae_NEAR_DUPLICATE_Q_20",
            "golden_swag_train_mae_NEAR_DUPLICATE_Q_35",
            # MLM models
            # "golden_swag_train_mlm_NEAR_DUPLICATE_Q_1",
            # "golden_swag_train_mlm_NEAR_DUPLICATE_Q_10",
            # "golden_swag_train_mlm_NEAR_DUPLICATE_Q_20",
            "golden_swag_train_mlm_NEAR_DUPLICATE_Q_35",
        ],
        IssueTypes.OFF_TOPIC_SAMPLES: [
            "bert",
            "deberta",
            # SimCSE models
            # "golden_swag_train_simcse_OFF_TOPIC_1",
            # "golden_swag_train_simcse_OFF_TOPIC_10",
            # "golden_swag_train_simcse_OFF_TOPIC_20",
            "golden_swag_train_simcse_OFF_TOPIC_35",
            # Electra models
            # "golden_swag_train_electra_OFF_TOPIC_1",
            # "golden_swag_train_electra_OFF_TOPIC_10",
            # "golden_swag_train_electra_OFF_TOPIC_20",
            "golden_swag_train_electra_OFF_TOPIC_35",
            # MAE models
            # "golden_swag_train_mae_OFF_TOPIC_1",
            # "golden_swag_train_mae_OFF_TOPIC_10",
            # "golden_swag_train_mae_OFF_TOPIC_20",
            "golden_swag_train_mae_OFF_TOPIC_35",
            # MLM models
            # "golden_swag_train_mlm_OFF_TOPIC_1",
            # "golden_swag_train_mlm_OFF_TOPIC_10",
            # "golden_swag_train_mlm_OFF_TOPIC_20",
            "golden_swag_train_mlm_OFF_TOPIC_35",
        ],
        "general": [
            "bert",
            "deberta",
            # SimCSE models
            # "golden_swag_train_simcse_1",
            # "golden_swag_train_simcse_10",
            # "golden_swag_train_simcse_20",
            "golden_swag_train_simcse_35",
            # Electra models
            # "golden_swag_train_electra_1",
            # "golden_swag_train_electra_10",
            # "golden_swag_train_electra_20",
            "golden_swag_train_electra_35",
            # MAE models
            # "golden_swag_train_mae_1",
            # "golden_swag_train_mae_10",
            # "golden_swag_train_mae_20",
            "golden_swag_train_mae_35",
            # MLM models
            # "golden_swag_train_mlm_1",
            # "golden_swag_train_mlm_10",
            # "golden_swag_train_mlm_20",
            "golden_swag_train_mlm_35",
            # without weight sharing
            # "golden_swag_train_electra_w_weight_1",
            # "golden_swag_train_electra_w_weight_10",
            # "golden_swag_train_electra_w_weight_20",
            # "golden_swag_train_electra_w_weight_35",
        ]
    },

    "pretraining_types": ["simcse", "electra", "mae", "bert", "mlm"],

    "issues_to_detect": [
        IssueTypes.CATEGORY_ERRORS,
        IssueTypes.LABEL_ERRORS,
        IssueTypes.NEAR_DUPLICATES_Q,
        IssueTypes.NEAR_DUPLICATES,
        IssueTypes.OFF_TOPIC_SAMPLES,
    ],

    "selfclean_params": {
        "plot_top_N": 400,
        "epochs": 0,
        "batch_size": 32,
        "dataset_name": "hellaswag",
        "wandb_logging": False
    },

    "embedding_poolings": [
        EmbeddingPoolingType.CLS,
        EmbeddingPoolingType.MEAN,
        EmbeddingPoolingType.FIRST_LAST_AVERAGE,
        EmbeddingPoolingType.MAX
    ]
}

def generate_markdown_table(data: Dict[str, Any], base_output_path: Path) -> None:
    """Generate Markdown tables for each issue type, sorted by AP in descending order."""
    for issue_type in CONFIG["issues_to_detect"]:
        issue_key = issue_type.value
        if issue_key not in data:
            logger.warning(f"No data found for issue type: {issue_key}")
            continue

        issue_data = data[issue_key]
        rows = []

        # Create a list of all results with pooling type information
        for model, pooling_results in issue_data.items():
            for pooling_type, metrics in pooling_results.items():
                row = {
                    "Model": model,
                    "AP": metrics.get("AP", "N/A"),
                    "AUROC": metrics.get("AUROC", "N/A"),
                    "Pooling Type": pooling_type
                }
                rows.append(row)

        df = pd.DataFrame(rows)
        if len(df) != 0:
            df = df.sort_values(by="AP", ascending=False)

        markdown_table = df.to_markdown(tablefmt="github", index=False)

        output_path = base_output_path / f"{issue_key}.md"
        with open(output_path, 'w') as f:
            f.write(f"# {issue_key.replace('_', ' ').title()}\n\n")
            f.write(markdown_table)
        logger.info(f"Generated markdown table for {issue_key} at {output_path}")

def setup_output_directory() -> Path:
    """Create a timestamped output directory."""
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_output_path = Path(__file__).parent.parent / "examples" / "output" / "goldenswag" / timestamp_str
    base_output_path.mkdir(parents=True, exist_ok=False)
    logger.info(f"Created output directory: {base_output_path}")
    return base_output_path

def get_pretraining_type(model_name: str) -> Optional[str]:
    """Extract pretraining type from model name."""
    for pretraining_type in CONFIG["pretraining_types"]:
        if pretraining_type in model_name:
            return pretraining_type
    return None

def calculate_number_of_run():
    count = 0
    num_poolings = len(CONFIG["embedding_poolings"])
    for issue_type, path in CONFIG["contaminated_paths"].items():
        models = CONFIG["models"].get(issue_type, CONFIG["models"]["general"])
        count += len(models) * num_poolings
    return count

def evaluate() -> None:
    """Run evaluation for all configurations."""
    base_output_path = setup_output_directory()
    summarized_log_dict = {"timestamp": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}

    # Initialize data structure for all issue types
    for issue in CONFIG["issues_to_detect"]:
        summarized_log_dict[issue.value] = {}

    # Calculate total number of runs
    total_runs = calculate_number_of_run()

    logger.info(f"Starting evaluation with {total_runs} total runs")

    run_count = 1

    for issue_type, path in CONFIG["contaminated_paths"].items():
        if not path.exists():
            logger.warning(f"Path does not exist: {path}")
            continue

        log_file = path.parent / f"{path.stem}_logs.json"
        if not log_file.exists():
            logger.warning(f"Contamination log file not found: {log_file}")
            continue

        models = CONFIG["models"].get(issue_type, CONFIG["models"]["general"])

        for model in models:
            pretraining_type = get_pretraining_type(model)
            if not pretraining_type:
                logger.warning(f"Could not determine pretraining type for model: {model}")
                continue

            # Initialize model entry in the log dict
            if model not in summarized_log_dict[issue_type.value]:
                summarized_log_dict[issue_type.value][model] = {}

            for pooling_type in CONFIG["embedding_poolings"]:
                logger.info(f"Run {run_count}/{total_runs}: Evaluating {issue_type.value} with {model} and {pooling_type.value} pooling")

                output_path = base_output_path / f"{issue_type.value}_{model}_{pooling_type.value}"
                output_path.mkdir(parents=True, exist_ok=True)

                start_time = time.time()

                try:
                    selfclean = SelfClean(
                        plot_top_N=CONFIG["selfclean_params"]["plot_top_N"],
                        output_path=output_path
                    )

                    issue_manager, _ = selfclean.run_on_text_dataset(
                        dataset_path=path,
                        contamination_log_path=log_file,
                        pretraining_type=pretraining_type,
                        **{k: v for k, v in CONFIG["selfclean_params"].items() if k != "plot_top_N"},
                        base_model=model,
                        issues_to_detect=[issue_type],
                        cache_dir=None,
                        pooling_type=pooling_type
                    )

                    # Store metrics with pooling type as key
                    summarized_log_dict[issue_type.value][model][pooling_type.value] = {
                        **{'data': path.name},
                        **issue_manager.metric_dict
                    }

                    elapsed_time = (time.time() - start_time) / 60
                    logger.success(f"Completed {issue_type.value} with {model} and {pooling_type.value} pooling in {elapsed_time:.2f} minutes")

                except Exception as e:
                    logger.error(f"Error evaluating {issue_type.value} with {model} and {pooling_type.value} pooling: {str(e)}")
                    summarized_log_dict[issue_type.value][model][pooling_type.value] = {
                        "error": str(e),
                        "data": path.name
                    }

                run_count += 1

    # Save summary and generate tables
    summary_path = base_output_path / "summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summarized_log_dict, f, indent=2)
    logger.info(f"Saved summary to {summary_path}")

    generate_markdown_table(summarized_log_dict, base_output_path)

def main() -> None:
    """Main function to run the evaluation pipeline."""
    try:
        evaluate()
    except Exception as e:
        logger.exception(f"Error during evaluation: {str(e)}")

if __name__ == "__main__":
    main()
