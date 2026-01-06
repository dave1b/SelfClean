from selfclean.cleaner.issue_manager import IssueTypes
import json
import pandas as pd

issues_to_detect = [
    IssueTypes.CATEGORY_ERRORS,
    IssueTypes.LABEL_ERRORS,
    IssueTypes.NEAR_DUPLICATES_Q,
    IssueTypes.NEAR_DUPLICATES,
    IssueTypes.OFF_TOPIC_SAMPLES,
]

embedding_poolings = [
    "cls",
    "mean_pooling",
    "first_last_average",
    "max"
]
top_k_values = [1, 2, 3, 4]

# Load the JSON file
with open('summary.json', 'r') as f:
    data = json.load(f)

# Initialize a dictionary to store the top x results per issue type and pooling type
top_results = {issue: {pooling: [] for pooling in embedding_poolings} for issue in issues_to_detect}

# Extract the AP and AUROC values for each issue type and pooling type
for issue in issues_to_detect:
    issue_key = issue.value  # Assuming IssueTypes are enums with .value attribute
    for model in data[issue_key]:
        for pooling in embedding_poolings:
            if pooling in data[issue_key][model]:
                metrics = data[issue_key][model][pooling]
                top_results[issue][pooling].append({
                    "Model": model,
                    "AP": metrics["AP"],
                    "AUROC": metrics["AUROC"]
                })

    # Sort for each pooling type
    for pooling in embedding_poolings:
        top_results[issue][pooling].sort(key=lambda x: x["AP"], reverse=True)

# Calculate the average AP and AUROC per embedding type, per issue type, for each top-k
avg_results_per_issue = {issue: {pooling: {k: {"AP": 0, "AUROC": 0} for k in top_k_values} for pooling in embedding_poolings} for issue in issues_to_detect}

for issue in issues_to_detect:
    for pooling in embedding_poolings:
        for k in top_k_values:
            top_k = top_results[issue][pooling][:k]
            if top_k:
                avg_ap = sum(r["AP"] for r in top_k) / len(top_k)
                avg_auroc = sum(r["AUROC"] for r in top_k) / len(top_k)
                avg_results_per_issue[issue][pooling][k] = {"AP": avg_ap, "AUROC": avg_auroc}

# Calculate the overall average for each top-k
avg_results = {pooling: {k: {"AP": [], "AUROC": []} for k in top_k_values} for pooling in embedding_poolings}

for issue in issues_to_detect:
    for pooling in embedding_poolings:
        for k in top_k_values:
            top_k = top_results[issue][pooling][:k]
            for result in top_k:
                avg_results[pooling][k]["AP"].append(result["AP"])
                avg_results[pooling][k]["AUROC"].append(result["AUROC"])

# Calculate the overall average for each top-k
for pooling in embedding_poolings:
    for k in top_k_values:
        if avg_results[pooling][k]["AP"]:
            avg_ap = sum(avg_results[pooling][k]["AP"]) / len(avg_results[pooling][k]["AP"])
            avg_auroc = sum(avg_results[pooling][k]["AUROC"]) / len(avg_results[pooling][k]["AUROC"])
        else:
            avg_ap, avg_auroc = 0, 0
        avg_results[pooling][k] = {"AP": avg_ap, "AUROC": avg_auroc}

# Prepare DataFrames for markdown output
with open("pooling_summary.md", "w") as md_file:
    md_file.write("# Pooling Summary\n\n")

    # Per-Issue-Type Averages
    md_file.write("## Per-Issue-Type Averages\n")
    for issue in issues_to_detect:
        md_file.write(f"### {issue.name}\n")
        rows = []
        for pooling in embedding_poolings:
            row = {"Embedding Type": pooling}
            for k in top_k_values:
                row[f"Average AP (top {k})"] = f"{avg_results_per_issue[issue][pooling][k]['AP']:.4f}"
                row[f"Average AUROC (top {k})"] = f"{avg_results_per_issue[issue][pooling][k]['AUROC']:.4f}"
            rows.append(row)
        df = pd.DataFrame(rows)
        markdown_table = df.to_markdown(tablefmt="github", index=False)
        md_file.write(f"{markdown_table}\n\n")

    # Overall Averages
    md_file.write("## Overall Averages (across all issue types)\n")
    rows = []
    for pooling in embedding_poolings:
        row = {"Embedding Type": pooling}
        for k in top_k_values:
            row[f"Average AP (top {k} per issue type)"] = f"{avg_results[pooling][k]['AP']:.4f}"
            row[f"Average AUROC (top {k} per issue type)"] = f"{avg_results[pooling][k]['AUROC']:.4f}"
        rows.append(row)
    df = pd.DataFrame(rows)
    markdown_table = df.to_markdown(tablefmt="github", index=False)
    md_file.write(f"{markdown_table}\n")
