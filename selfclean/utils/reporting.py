from pathlib import Path
from typing import Optional, Union, Dict, List
import pandas as pd
from loguru import logger
from IPython.display import Markdown, display
import textwrap

from selfclean.cleaner.auto_cleaning_mixin import AutoCleaningMixin
from selfclean.cleaner.issue_manager import IssueManager


def generate_markdown_report(
    issue_manager: IssueManager,
    dataset: List,
    model_name: str,
    top_n: int,
    output_path: Optional[Union[str, Path]] = None,
    max_text_length: int = 700,
    wrap_width: int = 50,
    contamination_log=None,
    pooling_type = None
) -> str:
    """
    Generate a markdown report for data quality issues.

    Args:
        issue_manager: Dictionary containing issue data from SelfClean
        dataset: The dataset containing the original samples
        top_n: Number of top issues to display for each category
        output_path: Path to save the markdown report
        max_text_length: Maximum length of displayed text
        wrap_width: Width for text wrapping

    Returns:
        Markdown report as a string
    """

    def wrap_text(text: str) -> str:
        return text
        """Wrap text and truncate if too long."""
        if not isinstance(text, str):
            return str(text)

        # Truncate if too long
        if len(text) > max_text_length:
            text = text[:max_text_length] + "..."

        # Wrap text
        return textwrap.fill(text, width=wrap_width)

    def create_issue_table(issues: Dict, issue_type: str, dataset: List, description: str) -> str:
        """Create a markdown table for a specific issue type."""

        # Create table data
        table_data = []
        for i, idx in enumerate(issues["indices"][:top_n]):
            if issue_type == "near_duplicates":
                # Handle near duplicates (pairs of indices)
                idx1, idx2 = idx
                text1 = wrap_text(dataset[int(idx1)][3])
                text2 = wrap_text(dataset[int(idx2)][3])

                id1 = dataset[int(idx1)][7]
                id2 = dataset[int(idx2)][7]

                if contamination_log_provided:
                    pred_index = pd.MultiIndex.from_tuples([(id1, id2)])
                    is_contaminated = pred_index.isin(contamination_indexes)

                score = issues["scores"][i] if "scores" in issues else "N/A"

                row = {
                    "Rank": i + 1,
                    "Index 1": id1,
                    "Index 2": id2,
                    "Text 1": text1,
                    "Text 2": text2,
                    "Score": f"{score:.4f}" if isinstance(score, (int, float)) else score,
                }
                if autocleaned:
                    row["Autoclean Prediction"] = issues.get('auto_issues')[i]
                if contamination_log_provided:
                    row["Synthetic Contaminated"] = is_contaminated
                table_data.append(row)

            elif issue_type == "near_duplicates_questions":
                # Handle near duplicates (pairs of indices)
                idx1, idx2 = idx
                text1 = wrap_text(dataset.get_context_only_text(int(idx1))[0])
                text2 = wrap_text(dataset.get_context_only_text(int(idx2))[0])

                id1 = dataset.get_context_only_text(int(idx1))[1]
                id2 = dataset.get_context_only_text(int(idx2))[1]

                if contamination_log_provided:
                    pred_index = pd.MultiIndex.from_tuples([(id1, id2)])
                    is_contaminated = pred_index.isin(contamination_indexes)

                score = issues["scores"][i] if "scores" in issues else "N/A"

                row = {
                    "Rank": i + 1,
                    "Index 1": id1,
                    "Index 2": id2,
                    "Text 1": text1,
                    "Text 2": text2,
                    "Score": f"{score:.4f}" if isinstance(score, (int, float)) else score,
                }
                if autocleaned:
                    row["Autoclean Prediction"] = issues.get('auto_issues')[i]
                if contamination_log_provided:
                    row["Synthetic Contaminated"] = is_contaminated
                table_data.append(row)

            else:
                # Handle single indices
                text = wrap_text(dataset[int(idx)][3])
                category = dataset[int(idx)][2]
                true_label = dataset[int(idx)][1]
                score = issues["scores"][i] if "scores" in issues else "N/A"
                id_ = dataset[int(idx)][7]

                if contamination_log_provided:
                    is_contaminated = id_ in contamination_ids

                row = {
                    "Rank": i + 1,
                    "Index": id_,
                    "Text": text,
                    "Score": f"{score:.4f}" if isinstance(score, (int, float)) else score,
                }

                row["Answer Correct"] = true_label
                row["Category"] = category
                if autocleaned:
                    row["Autoclean Prediction"] = issues.get('auto_issues')[i]
                if contamination_log_provided:
                    row["Synthetic Contaminated"] = is_contaminated
                table_data.append(row)

        # Create DataFrame and convert to markdown
        df = pd.DataFrame(table_data)

        # Set index to Rank for better display
        if "Rank" in df.columns:
            df.set_index("Rank", inplace=True)

        # Generate markdown table
        md_table = f"## {issue_type.replace('_', ' ').title()}\n\n"
        md_table += f"{description}\n\n" if description else ""
        md_table += df.to_markdown(tablefmt="github")
        md_table += "\n\n"
        return md_table

    # Create the full report
    autocleaned = True if 'auto_issues' in issue_manager.issue_dict else False
    contamination_log_provided = True if contamination_log is not None else False
    if contamination_log_provided:
        if {'id_1', 'id_2'}.issubset(contamination_log.columns):
            contamination_indexes = pd.MultiIndex.from_arrays([
                contamination_log['id_1'].astype(str),
                contamination_log['id_2'].astype(str)
            ])
        if 'id' in contamination_log.columns:
            contamination_ids = set(contamination_log['id'].astype(str).dropna())

    metrics = pd.DataFrame.from_dict(issue_manager.metric_dict, orient='index', columns=['Value'])
    report = "# Data Quality Report\n\n"
    report += f"**Generated on**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"**Dataset type**: {dataset.name}\n\n"
    report += f"**Dataset name**: {dataset.path.name}\n\n"
    report += f"**Dataset size**: {len(dataset)} samples\n\n"
    report += f"**Model used**: {model_name}\n\n"
    if pooling_type is not None:
        report += f"**Pooling Type**: {pooling_type}\n\n"
    if autocleaned:
        report += AutoCleaningMixin.get_hyperparameters() + "\n\n"
    report += f"### Evaluation Metrics:\n\n {metrics.to_markdown(tablefmt='github')} \n\n\n"

    report += f"Top {top_n} issues per category\n\n"

    # Add near duplicates (questions)
    if issue_manager["near_duplicates_questions"] is not None:
        # assert that dataset has method get_context_only_text
        assert hasattr(dataset,
                       'get_context_only_text'), "Dataset must have method get_context_only_text to properly return context_only texts."
        description = "Near duplicate questions based only on context question similarity."
        report += create_issue_table(issue_manager["near_duplicates_questions"], "near_duplicates_questions", dataset, description)
        report += "\n\n"

    # Add near duplicates
    if issue_manager["near_duplicates"] is not None:
        description = "Near duplicate questions based on combined question and answer similarity."
        report += create_issue_table(issue_manager["near_duplicates"], "near_duplicates", dataset, description)
        report += "\n\n"

    # Add off-topic samples
    if issue_manager["off_topic_samples"] is not None:
        description = "Off-topic samples based on combined question and answer."
        report += create_issue_table(issue_manager["off_topic_samples"], "off_topic_samples", dataset, description)
        report += "\n\n"

    # Add label errors
    if issue_manager["label_errors"] is not None:
        description = "Label errors based only on Label."
        report += create_issue_table(issue_manager["label_errors"], "label_errors", dataset, description)
        report += "\n\n"

    # Add category errors
    if issue_manager["category_errors"] is not None:
        description = "Category errors based only on Category."
        report += create_issue_table(issue_manager["category_errors"], "category_errors", dataset, description)
        report += "\n\n"

    # Save to file if output_path is provided
    if output_path:
        path = output_path / 'report.md'
        output_path.mkdir(exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Report saved to {path}")

    display_markdown_report(report)
    return report


# Helper function to display the report in a Jupyter notebook
def display_markdown_report(report: str):
    """Display the markdown report in a Jupyter notebook."""
    display(Markdown(report))
