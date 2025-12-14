import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from loguru import logger


def split_train_validation(
    json_path: Path,
    split_ratio: float = 0.2,
    random_seed: int = 42
):
    """
    Load a DataFrame from a JSON file and split it into training and validation sets.
    """

    df = pd.read_json(json_path)

    # Split the DataFrame into training and validation sets
    train_df, val_df = train_test_split(
        df,
        test_size=split_ratio,
        random_state=random_seed
    )

    logger.info(f"Train size: {len(train_df)}")
    logger.info(f"Validation size: {len(val_df)}")

    train_path = json_path.parent / "golden_swag_train.json"
    validation_path = json_path.parent / "golden_swag_validation.json"

    train_df.to_json(train_path, orient="records", lines=False)
    val_df.to_json(validation_path, orient="records", lines=False)


json_path = Path("golden_swag.json")
split_train_validation(json_path=json_path, split_ratio=0.2, random_seed=42)
