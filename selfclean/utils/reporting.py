from pathlib import Path
from typing import Optional, Union, Dict, List
import pandas as pd
from IPython.display import Markdown, display
import textwrap

from selfclean.cleaner.issue_manager import IssueManager


def generate_markdown_report(
    issue_manager: IssueManager,
    dataset: List,
    model_name: str,
    top_n: int,
    output_path: Optional[Union[str, Path]] = None,
    max_text_length: int = 400,
    wrap_width: int = 50
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
            if issue_type in ["near_duplicates", "near_duplicates_questions/context"]:
                factor = 1
                tuple_index = 3
                if issue_type == "near_duplicates_questions/context":
                    factor = 4
                    tuple_index = 6
                # Handle near duplicates (pairs of indices)
                idx1, idx2 = idx
                text1 = wrap_text(dataset[int(idx1)*factor][tuple_index] if isinstance(dataset[int(idx1)], (list, tuple)) else dataset[int(idx1)].get("text", ""))
                text2 = wrap_text(dataset[int(idx2)*factor][tuple_index] if isinstance(dataset[int(idx2)], (list, tuple)) else dataset[int(idx2)].get("text", ""))

                score = issues["scores"][i] if "scores" in issues else "N/A"

                table_data.append({
                    "Rank": i+1,
                    # "Index 1": int(idx1)*factor,
                    # "Index 2": int(idx2)*factor,
                    "Index 1": dataset[int(idx1)*factor][7],
                    "Index 2": dataset[int(idx2)*factor][7],
                    "Text 1": text1,
                    "Text 2": text2,
                    "Score": f"{score:.4f}" if isinstance(score, (int, float)) else score
                })
            else:
                # Handle single indices
                text = wrap_text(dataset[int(idx)][3] if isinstance(dataset[int(idx)], (list, tuple)) else dataset[int(idx)].get("text", ""))
                category = dataset[int(idx)][2] if isinstance(dataset[int(idx)], (list, tuple)) else dataset[int(idx)].get("category", "N/A")
                true_label = dataset[int(idx)][1] if isinstance(dataset[int(idx)], (list, tuple)) else dataset[int(idx)].get("correct", "N/A")
                score = issues["scores"][i] if "scores" in issues else "N/A"

                row = {
                    "Rank": i+1,
                    "Index": dataset[int(idx)][7],
                    "Text": text,
                    "Score": f"{score:.4f}" if isinstance(score, (int, float)) else score
                }

                if issue_type == "off_topic_samples":
                    row["Category"] = category
                elif issue_type in ["label_errors", "category_errors"]:
                    row["True Label"] = true_label
                    row["Category"] = category

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
    report = "# Data Quality Report\n\n"
    report += f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"Dataset type: {dataset.name}\n\n"
    report += f"Dataset name: {dataset.path.name}\n\n"
    report += f"Dataset size: {len(dataset)} samples\n\n"
    report += f"Model used: {model_name}\n\n"

    report += f"Top {top_n} issues per category\n\n"

    # Add near duplicates (questions)
    if issue_manager["near_duplicates_questions/context"] is not None:
        description = "Near duplicate questions based only on context question similarity."
        report += create_issue_table(issue_manager["near_duplicates_questions/context"], "near_duplicates_questions/context", dataset, description)
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
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path_ = Path(f'{output_path}.md')
        counter = 1
        while output_path_.exists():
            output_path_ = output_path.with_stem(f"{output_path.stem}_{counter}.md")
            counter += 1
        with open(output_path_, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {output_path_}")

    display_markdown_report(report)
    return report

# Helper function to display the report in a Jupyter notebook
def display_markdown_report(report: str):
    """Display the markdown report in a Jupyter notebook."""
    display(Markdown(report))
