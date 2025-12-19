import time
from pathlib import Path
from selfclean import SelfClean
from selfclean.cleaner.issue_manager import IssueTypes

start_time = time.time()

selfclean = SelfClean(
    plot_top_N=400,
    auto_cleaning=True,
    output_path=Path(__file__).parent.parent / "examples" / "output" / "goldenswag_simcse",
)

# Run with SimCSE
results, prediction = selfclean.run_on_text_dataset(
    # dataset_path=Path("../experiment/datasets/hellaswag/golden_swag_train_synthetic_CATEGORY_ERRORS.json"),
    dataset_path=Path("../experiment/datasets/hellaswag/hellaswag_train_0.01ksubset.json"),
    pretraining_type="simcse",
    epochs=0,
    batch_size=32,
    dataset_name="hellaswag",
    base_model="golden_swag_train_electra_bert",
    wandb_logging=False,
    issues_to_detect=[
        # IssueTypes.OFF_TOPIC_SAMPLES,
        # IssueTypes.NEAR_DUPLICATES_Q,
        # IssueTypes.NEAR_DUPLICATES,
        # IssueTypes.LABEL_ERRORS,
        IssueTypes.CATEGORY_ERRORS
    ],
    contamination_log_path=Path("../experiment/datasets/hellaswag/golden_swag_train_synthetic_CATEGORY_ERRORS_logs.json")
)
print(f"\nFinished in {(time.time() - start_time) / 60:.2f} minutes")

# Or run with MAE
# results = selfclean.run_on_text_dataset(
#     dataset_path=Path("../experiment/datasets/hellaswag/hellaswag_train_0.01ksubset.json"),
#     pretraining_type="simcse",
#     epochs=0,
#     batch_size=32,
#     dataset_name="hellaswag",
#     base_model="pretrained_bert_hellaSwag_simcse",
# )

# Or run with MAE
# results = selfclean.run_on_text_dataset(
#     dataset_path=Path("../experiment/datasets/hellaswag/hellaswag_train_0.01ksubset.json"),
#     pretraining_type="mae",
#     epochs=5,
#     batch_size=32,
#     dataset_name="hellaswag",
#     base_model="bert",
#     wandb_logging=True
# )
