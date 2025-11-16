from pathlib import Path

from selfclean import SelfClean

selfclean = SelfClean(
    plot_top_N=7,
    # auto_cleaning=True,
)

# Run with SimCSE
results = selfclean.run_on_text_dataset(
    dataset_path=Path("../experiment/datasets/hellaswag/hellaswag_train_0.01ksubset.json"),
    pretraining_type="simcse",
    epochs=0,
    batch_size=32,
    dataset_name="hellaswag",
    base_model="pretrained_bert_hellaSwag_simcse",
)

# Or run with MAE
# results = selfclean.run_on_text_dataset(
#     dataset_path=Path("../experiment/datasets/hellaswag/hellaswag_train_0.01ksubset.json"),
#     pretraining_type="mae",
#     epochs=0,
#     batch_size=32,
#     dataset_name="hellaswag",
#     base_model="pretrained_bert_hellaSwag_mae",
# )
