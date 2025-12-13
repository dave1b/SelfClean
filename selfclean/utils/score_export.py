import gc
import os
import shutil
import time
import numpy as np
import pandas as pd
import concurrent.futures
from loguru import logger
import concurrent.futures
from pathlib import Path
import dask.dataframe as dd
from typing import Dict, List, Optional, Union, Tuple
from selfclean.cleaner.issue_manager import IssueManager, IssueTypes
from selfclean.core.src.utils.utils import ram_usage


def generate_prediction_parquet(
    issue_manager: IssueManager,
    dataset: List,
    output_path: Optional[Union[str, Path]] = None,
    pretraining_type: str = "undefined",
    max_workers: int = max(os.cpu_count() - 4, 16),
    batch_size: int = 50_000,
) -> Dict:
    """
    Generate a Parquet file with issue scores and indices for each issue type.
    Optimized for processing large datasets efficiently with parallel processing.
    """
    logger.info(f"Generating prediction parquet, parallelism={max_workers}, batch_size={batch_size}")
    start_time = time.time()

    def get_sample_id(idx: np.ndarray, issue_type: str) -> str:
        """Optimized helper function to get sample ID based on issue type."""
        if issue_type == "near_duplicates_questions/context":
            return dataset.get_context_only_id(idx)
        return dataset.get_id(idx)

    def process_batch(issue_type: str, batch_indices, batch_auto_issues, batch_scores, is_near_duplicate: bool, batch_id, unique_id) -> str:
        """
        Process a batch of entries and return a list of results.
        Optimized to minimize memory usage and maximize speed.
        """
        min_len = min(len(batch_indices), len(batch_auto_issues), len(batch_scores))
        batch_indices = batch_indices[:min_len]
        batch_auto_issues = batch_auto_issues[:min_len]
        batch_scores = batch_scores[:min_len]


        scores = np.round(batch_scores, 5)
        prediction = batch_auto_issues
        issue_type_col = pd.Series([issue_type] * min_len)

        if is_near_duplicate:
            # Near Duplicates: indices are pairs (idx1, idx2)
            idx1_arr = batch_indices[:, 0]
            idx2_arr = batch_indices[:, 1]

            id1_arr = get_sample_id(idx1_arr, issue_type)
            id2_arr = get_sample_id(idx2_arr, issue_type)

            batch_df = pd.DataFrame({
                "id_1": id1_arr,
                "id_2": id2_arr,
                "score": scores,
                "issue_type": issue_type_col,
                "prediction": prediction,
                'id': None,
            })
        else:
            # Single Index
            id_arr = get_sample_id(batch_indices, issue_type)

            batch_df = pd.DataFrame({
                "id": id_arr,
                "score": scores,
                "issue_type": issue_type_col,
                "prediction": prediction,
                "id_1": None,
                "id_2": None,
            })

        # Filter out None values (from skipped entries)
        temp_file_path = f"./.temp/{unique_id}/temp_batch_{batch_id}.parquet"
        batch_df.to_parquet(temp_file_path, index=False)  # Use Parquet for efficiency
        return temp_file_path


    def process_issue_type(issue_type: str, issue_data: Dict) -> dd.DataFrame:
        """
            Process a specific issue type using concurrent.futures for parallel batch processing.
            Refactored to use an efficient batch_iterator to avoid loading all batches into memory.
            """
        max_workers = os.cpu_count() - 4
        logger.info(f"Starting optimized processing for {issue_type}, max_workers={max_workers}, batch_size={batch_size}")
        auto_issues_np = np.array(issue_data["auto_issues"])
        indices_np = np.array(issue_data["indices"])
        scores_data = np.array(issue_data["scores"])
        scores_np = np.array(scores_data)  # Convert scores to numpy array for slicing

        is_near_duplicate = issue_type in ["near_duplicates", "near_duplicates_questions/context"]
        total_entries = len(indices_np)

        unique_id = str(int(time.time() * 1000))
        Path(f"./.temp/{unique_id}").mkdir(parents=True)

        def batch_iterator():
            """Generator to yield slices (batches) without pre-materializing all of them."""
            for start in range(0, total_entries, batch_size):
                end = min(start + batch_size, total_entries)
                batch_id = start // batch_size

                yield (
                    indices_np[start:end],
                    auto_issues_np[start:end],
                    scores_np[start:end],
                    batch_id,
                    unique_id
                )

        result_files = []
        num_batches = (total_entries + batch_size - 1) // batch_size

        with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
            futures = [
                executor.submit(
                    process_batch,
                    issue_type,
                    batch_indices,
                    batch_auto_issues,
                    batch_scores,
                    is_near_duplicate,
                    batch_id,
                    unique_id
                )
                for batch_indices, batch_auto_issues, batch_scores, batch_id, unique_id in batch_iterator()
            ]

            gc.collect()
            log_divisor = max(1, num_batches // 10)

            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if i % log_divisor == 0:
                    logger.info(f"---- Processed batch {i + 1}/{num_batches}, {ram_usage()}")

                temp_file_path = future.result()
                if temp_file_path:
                    result_files.append(temp_file_path)

        if not result_files:
            logger.warning(f"No results generated for {issue_type}. Returning empty Dask DataFrame.")
            meta = pd.DataFrame(columns=['id', 'id_1', 'id_2', 'score', 'prediction'], dtype=str)
            return dd.from_pandas(meta.iloc[0:0], npartitions=1)

        result_ddf = dd.read_parquet(result_files)
        logger.info(f"Finished Dask read for {issue_type}. Number of partitions: {result_ddf.npartitions}")

        return result_ddf

    metadata = {
        "dataset_name": getattr(dataset, "name", "unknown"),
        "dataset_size": len(dataset),
        "generated_on": str(pd.Timestamp.now()),
        "issue_types": list[issue_manager.issue_dict.keys()],
        "pretraining_type": pretraining_type,
    }

    all_issue_dfs = []

    # Process each issue type in auto_clean_dict
    for issue_type, issue_data in issue_manager.issue_dict.items():
        logger.info(f"Starting generating prediction export for {issue_type}")

        df = process_issue_type(issue_type, issue_data)

        if len(df.index) > 0:
            all_issue_dfs.append(df)
            logger.info(f"Completed processing for {issue_type}. Found {len(df)} entries.")
        else:
            logger.info(f"Completed processing for {issue_type}. Found 0 entries.")

    # Combine all DataFrames efficiently in one go
    if all_issue_dfs:
        combined_df = dd.concat(all_issue_dfs, axis=0)

        path = output_path / 'predictions_dask'
        combined_df.to_parquet(
            path,
            engine='pyarrow',
            compression='snappy'
        )

        temp_dir = Path(f"./.temp/")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        logger.info(f"Finished in {(time.time() - start_time) / 60:.2f} minutes, predictions saved to {path} ")

        return {
            "data_path": path,
            "metadata": metadata,
        }
    else:
        logger.info("No issues found to save.")
        return {"data": pd.DataFrame(), "metadata": metadata}
