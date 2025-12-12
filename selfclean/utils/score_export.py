import concurrent.futures
from loguru import logger
import os
import time
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import dask.dataframe as dd
from selfclean.cleaner.issue_manager import IssueManager, IssueTypes
from selfclean.core.src.utils.utils import ram_usage


def generate_prediction_parquet(
    issue_manager: IssueManager,
    dataset: List,
    output_path: Optional[Union[str, Path]] = None,
    pretraining_type: str = "undefined",
    max_workers: int = max(os.cpu_count() - 4, 16),
    batch_size: int = 1_000_000,
) -> Dict:
    """
    Generate a Parquet file with issue scores and indices for each issue type.
    Optimized for processing large datasets efficiently with parallel processing.
    """
    logger.info(f"Generating prediction parquet, parallelism={max_workers}, batch_size={batch_size}")
    start_time = time.time()

    def get_sample_id(idx: int, issue_type: str) -> str:
        """Optimized helper function to get sample ID based on issue type."""
        if issue_type == "near_duplicates_questions/context":
            return dataset.get_context_only_text(int(idx))[1]
        return dataset[int(idx)][7]

    def process_batch(issue_type: str, batch_indices, batch_auto_issues, batch_scores, is_near_duplicate: bool, batch_id) -> str:
        """
        Process a batch of entries and return a list of results.
        Optimized to minimize memory usage and maximize speed.
        """
        batch_results = []
        batch_auto_issues_len = len(batch_auto_issues)

        # Pre-allocate list for results
        batch_results = [None] * len(batch_indices)

        for i, idx in enumerate(batch_indices):
            if i >= batch_auto_issues_len:
                break  # Skip if no prediction available (e.g. context duplication contamination)
            is_issue = batch_auto_issues[i]

            score = round(batch_scores[i], 5)

            if is_near_duplicate:
                idx1, idx2 = idx
                id1 = get_sample_id(idx1, issue_type)
                id2 = get_sample_id(idx2, issue_type)

                batch_results[i] = {
                    "id_1": id1,
                    "id_2": id2,
                    "score": score,
                    "issue_type": issue_type,
                    "prediction": is_issue,
                    'id': None,
                }
            else:
                id = get_sample_id(idx, issue_type)

                batch_results[i] = {
                    "id": id,
                    "score": score,
                    "issue_type": issue_type,
                    "prediction": is_issue,
                    "id_1": None,
                    "id_2": None,
                }

        # Filter out None values (from skipped entries)
        temp_file_path = f"./.temp/temp_batch_{batch_id}.parquet"
        batch_df = pd.DataFrame(batch_results)
        batch_df.to_parquet(temp_file_path, index=False)  # Use Parquet for efficiency
        return temp_file_path

    def process_issue_type(issue_type: str, issue_data: Dict) -> dd.DataFrame:
        """
        Process a specific issue type in parallel batches and return a DataFrame.
        """
        auto_issues = issue_data["auto_issues"]
        indices = issue_data["indices"]
        scores = issue_data.get("scores", [None] * len(indices))
        is_near_duplicate = issue_type in ["near_duplicates", "near_duplicates_questions/context"]

        # Convert to numpy arrays for faster processing
        auto_issues_np = np.array(auto_issues)
        scores_np = np.array(scores)

        num_batches = (len(indices) + batch_size - 1) // batch_size

        split_points = np.arange(1, num_batches) * batch_size

        batched_indices = np.split(indices, split_points)
        batched_auto_issues = np.split(auto_issues_np, split_points)
        batched_scores = np.split(scores_np, split_points)

        result_files = []

        temp_dir = Path("./.temp")
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Use ThreadPoolExecutor for parallel batch processing
        with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
            # Submit all tasks at once
            futures = [
                executor.submit(process_batch, issue_type, *batch_data, is_near_duplicate, i)
                for i, batch_data in enumerate(zip(batched_indices, batched_auto_issues, batched_scores))
            ]

            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if i % max(1, len(batched_indices) // 10) == 0:
                    logger.info(f"---- Processing {issue_type}: batch {i + 1}/{len(batched_indices)}, {ram_usage()}")

                temp_file_path = future.result()
                if temp_file_path:
                    result_files.append(temp_file_path)

        # Combine all batch DataFrame paths with dask
        result_df = dd.read_parquet(result_files)

        # Because dask df -> not in memory
        return result_df

    combined_df = None

    # Create metadata
    metadata = {
        "dataset_name": getattr(dataset, "name", "unknown"),
        "dataset_size": len(dataset),
        "generated_on": str(pd.Timestamp.now()),
        "issue_types": list[issue_manager.issue_dict.keys()],
        "pretraining_type": pretraining_type,
    }

    # Process each issue type in auto_clean_dict
    for issue_type, issue_data in issue_manager.issue_dict.items():
        logger.info(f"Starting generating prediction export for {issue_type}")
        df = process_issue_type(issue_type, issue_data)
        if combined_df is None:
            combined_df = df
        else:
            combined_df = combined_df.append(df)
        logger.info(f"Completed processing for {issue_type}. Found {len(df)} entries.")

    # Combine all DataFrames
    if len(combined_df.index) > 0:

        path = output_path / 'predictions_dask'
        combined_df.to_parquet(
            path,
            engine='pyarrow',
            compression='snappy'
        )

        # combined_df.to_json(output_path_.with_suffix(".json"), orient="records", lines=False)
        logger.info(f"Finished in {(time.time() - start_time) / 60:.2f} minutes, predictions saved to {path} ")

        return {
            "data_path": path,
            "metadata": metadata,
        }
    else:
        logger.info("No issues found to save.")
        return {"data": pd.DataFrame(), "metadata": metadata}


def generate_issue_scores_parquet(
    issue_manager: IssueManager,
    dataset: List,
    output_path: Optional[Union[str, Path]] = None,
    include_all_scores: bool = True
) -> Dict:
    """
    Generate a Parquet file with issue scores and indices for each issue type.
    Parquet format provides better performance and compression than JSON.

    Args:
        issue_manager: IssueManager containing issue data from SelfClean
        dataset: The dataset containing the original samples
        output_path: Path to save the Parquet file
        include_all_scores: If True, includes all scores. If False, only includes top issues.

    Returns:
        Dictionary containing all issue scores and indices
    """

    def process_issue_type(issue_type: str, issues: Dict) -> pd.DataFrame:
        """Process a specific issue type and return a DataFrame with scores and indices."""
        data = []

        if issues is None:
            return pd.DataFrame()

        # Get all indices and scores
        indices = issues["indices"]
        scores = issues.get("scores", [None] * len(indices))

        for idx, score in zip(indices, scores):
            if issue_type in ["near_duplicates", "near_duplicates_questions/context"]:
                # Handle near duplicates (pairs of indices)
                idx1, idx2 = idx
                factor = 1
                if issue_type == "near_duplicates_questions/context":
                    factor = 4

                # Get the unique IDs for each sample
                id1 = dataset[int(idx1) * factor][7] if isinstance(dataset[int(idx1)], (list, tuple)) else f"idx_{int(idx1) * factor}"
                id2 = dataset[int(idx2) * factor][7] if isinstance(dataset[int(idx2)], (list, tuple)) else f"idx_{int(idx2) * factor}"

                data.append({
                    "id_1": id1,
                    "id_2": id2,
                    "score": round(float(score), 5) if score is not None else None,
                    "issue_type": issue_type
                })
            else:
                # Handle single indices
                factor = 1
                if issue_type == "off_topic_samples":
                    factor = 1
                elif issue_type in ["label_errors", "category_errors"]:
                    factor = 1

                # Get the unique ID for the sample
                sample_id = dataset[int(idx) * factor][7] if isinstance(dataset[int(idx)], (list, tuple)) else f"idx_{int(idx) * factor}"

                data.append({
                    "id": sample_id,
                    "score": round(float(score), 5) if score is not None else None,
                    "issue_type": issue_type
                })

        return pd.DataFrame(data)

    # Initialize a list to hold all DataFrames
    all_dfs = []

    # Process each issue type
    issue_types = {
        IssueTypes.NEAR_DUPLICATES_Q.value: "near_duplicates_questions",
        IssueTypes.NEAR_DUPLICATES.value: "near_duplicates",
        IssueTypes.OFF_TOPIC_SAMPLES.value: "off_topic_samples",
        IssueTypes.LABEL_ERRORS.value: "label_errors",
        IssueTypes.CATEGORY_ERRORS.value: "category_errors"
    }

    # Create metadata DataFrame
    metadata = {
        "dataset_name": getattr(dataset, "name", "unknown"),
        "dataset_size": len(dataset),
        "generated_on": str(pd.Timestamp.now()),
        "issue_types": list(issue_types.values())
    }

    # Process each issue type and collect DataFrames
    for enum_type, json_key in issue_types.items():
        issues = issue_manager.get_issues(enum_type)
        if issues is not None:
            if include_all_scores:
                # Include all scores
                df = process_issue_type(enum_type, issues)
                if not df.empty:
                    all_dfs.append(df)
            else:
                # Only include top issues (first 100 or all if less)
                top_n = min(100, len(issues["indices"])) if issues.get("indices") else 0
                if top_n > 0:
                    top_issues = {
                        "indices": issues["indices"][:top_n],
                        "scores": issues["scores"][:top_n] if "scores" in issues else [None] * top_n
                    }
                    df = process_issue_type(enum_type, top_issues)
                    if not df.empty:
                        all_dfs.append(df)

    # Combine all DataFrames
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Add metadata as attributes
        combined_df.attrs = metadata

        # Save to Parquet file if output_path is provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path_ = Path(f'{output_path}.parquet')
            counter = 1

            while output_path_.exists():
                output_path_ = output_path.with_stem(f"{output_path.stem}_{counter}.parquet")
                counter += 1

            combined_df.to_parquet(output_path_, engine='pyarrow')
            combined_df.to_json(output_path_.with_suffix(".json"), orient="records", lines=False)
            logger.info(f"Issue scores saved to {output_path_}")

        return {
            "data": combined_df,
            "metadata": metadata
        }
    else:
        logger.info("No issues found to save.")
        return {"data": pd.DataFrame(), "metadata": metadata}
