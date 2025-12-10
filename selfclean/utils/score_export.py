import concurrent.futures
import os
from pathlib import Path

import pandas as pd
from typing import Dict, List, Optional, Union
from selfclean.cleaner.issue_manager import IssueManager, IssueTypes


def generate_prediction_parquet(
    auto_clean_dict: Dict,
    dataset: List,
    output_path: Optional[Union[str, Path]] = None,
    pretraining_type: str = "undefined",
    include_all: bool = False,
    max_workers: int = os.cpu_count() // 2,
    batch_size: int = 1_000_000,
) -> Dict:
    """
    Generate a Parquet file with issue scores and indices for each issue type.
    Processes entries in parallel batches for efficiency.
    """
    print(f"Generating prediction parquet with include_all={include_all}, parallelism={max_workers}, batch_size={batch_size}")

    def process_batch(issue_type: str, batch_indices: List, batch_auto_issues: List, batch_scores: List, is_near_duplicate: bool) -> List[dict]:
        """Process a batch of entries and return a list of results."""
        batch_results = []
        for i, idx in enumerate(batch_indices):
            is_issue = batch_auto_issues[i]
            score = round(batch_scores[i], 5)
            if not (include_all or is_issue):
                continue
            if is_near_duplicate:
                idx1, idx2 = idx
                if issue_type == "near_duplicates_questions/context":
                    id1 = dataset.get_context_only_text(int(idx1))[1]
                    id2 = dataset.get_context_only_text(int(idx2))[1]
                else:
                    id1 = dataset[int(idx1)][7]
                    id2 = dataset[int(idx2)][7]
                batch_results.append({
                    "id_1": id1,
                    "id_2": id2,
                    "score": score,
                    "issue_type": issue_type,
                    "prediction": is_issue,
                    'id': None,
                })
            else:
                sample_id = dataset[int(idx)][7]
                batch_results.append({
                    "id": sample_id,
                    "score": score,
                    "issue_type": issue_type,
                    "prediction": is_issue,
                    "id_1": None,
                    "id_2": None,
                })
        return batch_results

    def process_issue_type(issue_type: str, issue_data: Dict) -> pd.DataFrame:
        """Process a specific issue type in parallel batches and return a DataFrame."""
        auto_issues = issue_data["auto_issues"]
        indices = issue_data["indices"]
        scores = issue_data.get("scores", [None] * len(indices))
        is_near_duplicate = issue_type in ["near_duplicates", "near_duplicates_questions/context"]

        # Split into batches
        batches = [
            (indices[i:i + batch_size], auto_issues[i:i + batch_size], scores[i:i + batch_size])
            for i in range(0, len(indices), batch_size)
            if i < len(auto_issues)
        ]

        # Use ThreadPoolExecutor for parallel batch processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(process_batch, issue_type, batch_indices, batch_auto_issues, batch_scores, is_near_duplicate)
                for batch_indices, batch_auto_issues, batch_scores in batches
            ]
            # Collect results as they complete
            results = []
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if i % max(1, len(batches) // 10) == 0:
                    print(f"Processing {issue_type}: batch {i}/{len(batches)}")
                results.extend(future.result())

        return pd.DataFrame(results)

    all_dfs = []
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
        df = process_issue_type(issue_type, issue_data)
        if not df.empty:
            all_dfs.append(df)

    # Combine all DataFrames
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        # Add metadata as attributes
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
            combined_df.to_parquet(output_path_, engine='pyarrow')
            combined_df.to_json(output_path_.with_suffix(".json"), orient="records", lines=False)
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
