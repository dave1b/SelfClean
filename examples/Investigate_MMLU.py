from pathlib import Path

from selfclean import SelfClean

selfclean = SelfClean(
    plot_top_N=7,
    # auto_cleaning=True,
)

# run with SimCSE
results = selfclean.run_on_text_dataset(
    dataset_path=Path("../experiment/datasets/mmlu/mmlu_test_small.json"),
    pretraining_type="simcse",
    epochs=0,
    batch_size=32,
    dataset_name="mmlu",
    base_model="pretrained_bert_mmlu_simcse",
)

# run with MAE
results = selfclean.run_on_text_dataset(
    dataset_path=Path("../experiment/datasets/mmlu/mmlu_test_small.json"),
    pretraining_type="mae",
    epochs=0,
    batch_size=32,
    dataset_name="mmlu",
    base_model="pretrained_bert_mmlu_mae",
)
