import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Union
from selfclean.cleaner.issue_manager import IssueManager, IssueTypes


def generate_issue_scores_json(
    issue_manager: IssueManager,
    dataset: List,
    output_path: Optional[Union[str, Path]] = None,
    include_all_scores: bool = True
) -> Dict:
    """
    Generate a JSON file with issue scores and indices for each issue type.

    Args:
        issue_manager: IssueManager containing issue data from SelfClean
        dataset: The dataset containing the original samples
        output_path: Path to save the JSON file
        include_all_scores: If True, includes all scores. If False, only includes top issues.

    Returns:
        Dictionary containing all issue scores and indices
    """

    def process_issue_type(issue_type: str, issues: Dict) -> List[Dict]:
        """Process a specific issue type and return a list of dictionaries with scores and indices."""
        processed = []

        if issues is None:
            return processed

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

                processed.append({
                    "id_1": id1,
                    "id_2": id2,
                    "score": round(float(score), 5) if score is not None else None
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

                processed.append({
                    "id": sample_id,
                    "score": round(float(score), 5) if score is not None else None
                })

        return processed

    # Initialize the output dictionary
    output = {}

    # Process each issue type
    issue_types = {
        IssueTypes.NEAR_DUPLICATES_Q.value: "near_duplicates_questions",
        IssueTypes.NEAR_DUPLICATES.value: "near_duplicates",
        IssueTypes.OFF_TOPIC_SAMPLES.value: "off_topic_samples",
        IssueTypes.LABEL_ERRORS.value: "label_errors",
        IssueTypes.CATEGORY_ERRORS.value: "category_errors"
    }

    for enum_type, json_key in issue_types.items():
        issues = issue_manager.get_issues(enum_type)
        if issues is not None:
            if include_all_scores:
                # Include all scores
                output[json_key] = process_issue_type(enum_type, issues)
            else:
                # Only include top issues (first 100 or all if less)
                top_n = min(100, len(issues["indices"])) if issues.get("indices") else 0
                if top_n > 0:
                    top_issues = {
                        "indices": issues["indices"][:top_n],
                        "scores": issues["scores"][:top_n] if "scores" in issues else [None] * top_n
                    }
                    output[json_key] = process_issue_type(enum_type, top_issues)

    # Add metadata
    output["metadata"] = {
        "dataset_name": getattr(dataset, "name", "unknown"),
        "dataset_size": len(dataset),
        "generated_on": str(pd.Timestamp.now()),
        "issue_types": list(issue_types.values())
    }

    # Save to file if output_path is provided
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path_ = Path(f'{output_path}.json')
        counter = 1
        # Handle case where file already exists
        while output_path_.exists():
            output_path_ = output_path.with_stem(f"{output_path.stem}_{counter}.json")
            counter += 1

        with open(output_path_, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"Issue scores saved to {output_path_}")

    return output
