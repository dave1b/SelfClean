import pandas as pd
from pathlib import Path
from experiment.performance_assesser import PerformanceAssesser
from selfclean import SelfClean
from selfclean.cleaner.issue_manager import IssueTypes

selfclean = SelfClean(
    plot_top_N=50,
    auto_cleaning=True,
    output_path=Path(__file__).parent.parent / "examples" / "output" / "mmlu_simcse",

)

# run with SimCSE
results, prediction_parquet = selfclean.run_on_text_dataset(
    dataset_path=Path("../experiment/datasets/mmlu/mmlu_test_10percent.json"),
    pretraining_type="simcse",
    epochs=0,
    batch_size=32,
    dataset_name="mmlu",
    base_model="pretrained_bert_mmlu_simcse",
    issues_to_detect=[IssueTypes.NEAR_DUPLICATES_Q],
)

contamination_log_path = Path("../experiment/datasets/hellaswag/hellaswag_train_0.01ksubset_question_duplication_contamination_logs.json")
contamination_log = pd.read_json(contamination_log_path)

pa = PerformanceAssesser(prediction=prediction_parquet, contamination_log=contamination_log)
pa.assess_performance()

# # run with MAE
# results = selfclean.run_on_text_dataset(
#     dataset_path=Path("../experiment/datasets/mmlu/mmlu_test_small.json"),
#     pretraining_type="mae",
#     epochs=0,
#     batch_size=32,
#     dataset_name="mmlu",
#     base_model="pretrained_bert_mmlu_mae",
# )
