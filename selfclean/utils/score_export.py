import concurrent.futures
import os
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from selfclean.cleaner.issue_manager import IssueManager, IssueTypes

def generate_prediction_parquet(
    auto_clean_dict: Dict,
    dataset: List,
    output_path: Optional[Union[str, Path]] = None,
    pretraining_type: str = "undefined",
    include_all: bool = False,
    max_workers: int = min(16, os.cpu_count() or 1),
    batch_size: int = 100_000,
) -> Dict:
    """
    Generate a Parquet file with issue scores and indices for each issue type.
    Optimized for processing large datasets efficiently with parallel processing.
    """
    print(f"Generating prediction parquet with include_all={include_all}, parallelism={max_workers}, batch_size={batch_size}")

    def get_sample_id(idx: int, issue_type: str) -> str:
        """Optimized helper function to get sample ID based on issue type."""
        if issue_type == "near_duplicates_questions/context":
            return dataset.get_context_only_text(int(idx))[1]
        return dataset[int(idx)][7]

    def process_batch(
        issue_type: str,
        batch_data: Tuple[List, List[bool], List[float]],
        is_near_duplicate: bool
    ) -> List[dict]:
        """
        Process a batch of entries and return a list of results.
        Optimized to minimize memory usage and maximize speed.
        """
        batch_indices, batch_auto_issues, batch_scores = batch_data
        batch_results = []

        # Pre-allocate list for results
        batch_results = [None] * len(batch_indices)

        for i, idx in enumerate(batch_indices):
            is_issue = batch_auto_issues[i]
            if not (include_all or is_issue):
                continue

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
        return [result for result in batch_results if result is not None]

    def process_issue_type(issue_type: str, issue_data: Dict) -> pd.DataFrame:
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

        # Create batches
        num_batches = (len(indices) + batch_size - 1) // batch_size
        batches = []

        for i in range(num_batches):
            start = i * batch_size
            end = min((i + 1) * batch_size, len(indices))

            if start >= end:
                continue

            batch_indices = indices[start:end]
            batch_auto_issues = auto_issues_np[start:end]
            batch_scores = scores_np[start:end]

            batches.append((batch_indices, batch_auto_issues, batch_scores))

        # Use ThreadPoolExecutor for parallel batch processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks at once
            futures = [
                executor.submit(process_batch, issue_type, batch, is_near_duplicate)
                for batch in batches
            ]

            # Process results as they complete
            results = []
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if i % max(1, len(batches) // 10) == 0:
                    print(f"Processing {issue_type}: batch {i+1}/{len(batches)}")

                batch_result = future.result()
                if batch_result:
                    results.extend(batch_result)

        # Create DataFrame in one operation
        if results:
            return pd.DataFrame(results)
        return pd.DataFrame()

    # Initialize a list to hold all DataFrames
    all_dfs = []

    # Create metadata
    metadata = {
        "dataset_name": getattr(dataset, "name", "unknown"),
        "dataset_size": len(dataset),
        "generated_on": str(pd.Timestamp.now()),
        "issue_types": list(auto_clean_dict.keys()),
        "include_all": include_all,
        "pretraining_type": pretraining_type,
    }

    # Process each issue type in auto_clean_dict
    for issue_type, issue_data in auto_clean_dict.items():
        print(f"Starting processing for {issue_type}")
        df = process_issue_type(issue_type, issue_data)
        if not df.empty:
            all_dfs.append(df)
            print(f"Completed processing for {issue_type}. Found {len(df)} entries.")

    # Combine all DataFrames
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True, copy=False)

        combined_df.attrs = metadata

        # Save to Parquet file if output_path is provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Ensure unique filename
            output_path_ = output_path.with_suffix('.parquet')
            counter = 1
            while output_path_.exists():
                output_path_ = output_path.with_stem(f"{output_path.stem}_{counter}").with_suffix('.parquet')
                counter += 1

            combined_df.to_parquet(
                output_path_,
                engine='pyarrow',
                compression='snappy',
                index=False
            )

            # combined_df.to_json(output_path_.with_suffix(".json"), orient="records", lines=False)

            print(f"Issue scores saved to {output_path_}")

        return {
            "data": combined_df,
            "metadata": metadata,
        }
    else:
        print("No issues found to save.")
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
            print(f"Issue scores saved to {output_path_}")

        return {
            "data": combined_df,
            "metadata": metadata
        }
    else:
        print("No issues found to save.")
        return {"data": pd.DataFrame(), "metadata": metadata}
