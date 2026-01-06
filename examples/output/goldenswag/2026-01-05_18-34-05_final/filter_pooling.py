import json

import pandas as pd
from loguru import logger

from selfclean.cleaner.issue_manager import IssueTypes

issues_to_detect = [
    IssueTypes.CATEGORY_ERRORS,
    IssueTypes.LABEL_ERRORS,
    IssueTypes.NEAR_DUPLICATES_Q,
    IssueTypes.NEAR_DUPLICATES,
    IssueTypes.OFF_TOPIC_SAMPLES,
]

pool_filter = "cls"

with open('summary.json', 'r') as f:
    data = json.load(f)


for issue_type in issues_to_detect:
    issue_key = issue_type.value
    if issue_key not in data:
        logger.warning(f"No data found for issue type: {issue_key}")
        continue

    issue_data = data[issue_key]
    rows = []

    # Create a list of all results with pooling type information
    for model, pooling_results in issue_data.items():
        for pooling_type, metrics in pooling_results.items():
            if pool_filter == pooling_type:
                row = {
                    "Model": model,
                    "AP": metrics.get("AP", "N/A"),
                    "AUROC": metrics.get("AUROC", "N/A"),
                    "Pooling Type": pooling_type
                }
                rows.append(row)

    df = pd.DataFrame(rows)
    if len(df) != 0:
        df = df.sort_values(by="AP", ascending=False)

    markdown_table = df.to_markdown(tablefmt="github", index=False)

    output_path = f"{issue_key}_{pool_filter}.md"
    with open(output_path, 'w') as f:
        f.write(f"# {issue_key.replace('_', ' ').title()}\n\n")
        f.write(markdown_table)
    logger.info(f"Generated markdown table for {issue_key} at {output_path}")
