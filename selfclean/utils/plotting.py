from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import Dataset
from torchvision import transforms

from matplotlib.gridspec import GridSpec
import textwrap

from ..cleaner.issue_manager import IssueManager
from ..core.src.utils.plotting import create_subtitle, denormalize_image


def plot_inspection_result(
    issue_manager: IssueManager,
    dataset: Dataset,
    plot_top_N: int,
    labels: Optional[Union[np.ndarray, list]] = None,
    output_path: Optional[Union[str, Path]] = None,
    figsize: tuple = (10, 8),
):
    rows = len(issue_manager.keys)
    if issue_manager["near_duplicates"] is not None:
        rows += 1
    fig, ax = plt.subplots(rows, plot_top_N, figsize=figsize)
    ax_idx = 0

    near_duplicate_issues = issue_manager["near_duplicates"]
    if near_duplicate_issues is not None:
        for i, (idx1, idx2) in enumerate(near_duplicate_issues["indices"][:plot_top_N]):
            ax[ax_idx, i].imshow(
                transforms.ToPILImage()(denormalize_image(dataset[int(idx1)][0]))
            )
            ax[ax_idx + 1, i].imshow(
                transforms.ToPILImage()(denormalize_image(dataset[int(idx2)][0]))
            )
            ax[ax_idx, i].set_xticks([])
            ax[ax_idx, i].set_yticks([])
            ax[ax_idx + 1, i].set_xticks([])
            ax[ax_idx + 1, i].set_yticks([])
            ax[ax_idx, i].set_title(f"Ranking: {i + 1}, Idx: {int(idx1)}", fontsize=6)
            ax[ax_idx + 1, i].set_title(f"Idx: {int(idx2)}", fontsize=6)
        ax_idx += 2

    off_topic_issues = issue_manager["off_topic_samples"]
    if off_topic_issues is not None:
        for i, idx in enumerate(off_topic_issues["indices"][:plot_top_N]):
            ax[ax_idx, i].imshow(
                transforms.ToPILImage()(denormalize_image(dataset[int(idx)][0]))
            )
            ax[ax_idx, i].set_title(f"Ranking: {i + 1}, Idx: {int(idx)}", fontsize=6)
            ax[ax_idx, i].set_xticks([])
            ax[ax_idx, i].set_yticks([])
        ax_idx += 1

    label_error_issues = issue_manager["label_errors"]
    if label_error_issues is not None:
        for i, idx in enumerate(label_error_issues["indices"][:plot_top_N]):
            class_label = labels[idx] if labels is not None else None
            ax[ax_idx, i].imshow(
                transforms.ToPILImage()(denormalize_image(dataset[int(idx)][0]))
            )
            ax[ax_idx, i].set_title(
                f"Ranking: {i + 1}\nIdx: {int(idx)}\nLbl: {class_label}",
                fontsize=6,
            )
            ax[ax_idx, i].set_xticks([])
            ax[ax_idx, i].set_yticks([])

    ax_idx = 0
    grid = plt.GridSpec(rows, plot_top_N)
    if near_duplicate_issues is not None:
        create_subtitle(
            fig,
            grid[ax_idx, ::],
            "Near-Duplicate Ranking",
            fontsize=12,
        )
        ax_idx += 2
    if off_topic_issues is not None:
        create_subtitle(
            fig,
            grid[ax_idx, ::],
            "Off-Topic Samples Ranking",
            fontsize=12,
        )
        ax_idx += 1
    if label_error_issues is not None:
        create_subtitle(
            fig,
            grid[ax_idx, ::],
            "Label Error Ranking",
            fontsize=12,
        )

    fig.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path_ = Path(f'{output_path}.png')
        counter = 1
        while (output_path_.exists()):
            output_path_ = output_path.with_stem(f"{output_path.stem}_{counter}.png")
            counter += 1
        plt.savefig(output_path, bbox_inches="tight")
    plt.show()


def plot_inspection_result_text(
    issue_manager,
    dataset,
    plot_top_N: int = 5,
    output_path: Optional[Union[str, Path]] = None,
    figsize: tuple = (28, 22),
    h1_font_size: int = 15,
    h2_font_size: int = 12,
    h3_font_size: int = 12,
):
    rows = 0
    height_ratios = []
    if issue_manager["near_duplicates_questions/context"] is not None:
        rows += 3
        height_ratios.extend([0.8, 1.2, 1.2])
    if issue_manager["near_duplicates"] is not None:
        rows += 3
        height_ratios.extend([0.8, 1.2, 1.2])
    if issue_manager["off_topic_samples"] is not None:
        rows += 2
        height_ratios.extend([0.8, 1.2])
    if issue_manager["label_errors"] is not None:
        rows += 2
        height_ratios.extend([0.8, 1.2])
    if issue_manager["category_errors"] is not None:
        rows += 4
        height_ratios.extend([0.8, 1.2, 0.8, 1.2])

    fig = plt.figure(figsize=figsize)
    grid = GridSpec(
        rows, plot_top_N, figure=fig,
        hspace=0.6,
        wspace=0.4,
        left=0.02, right=0.98, top=0.96, bottom=0.03,
        height_ratios=height_ratios
    )
    row_idx = 0

    def wrap_text(text, max_line_length=40):
        """Wrap text to a specified line length."""
        wrapper = textwrap.TextWrapper(width=max_line_length, break_long_words=False)
        return "\n".join(wrapper.wrap(text))

    def truncate_text(text, max_chars=300):
        """Limit text length and add ellipsis."""
        return text if len(text) <= max_chars else text[:max_chars - 3] + "..."

    def make_ax_text(ax, text, facecolor, edgecolor):
        """Render fixed-size text box with better title spacing."""
        ax.text(
            0.5, 0.5,
            text,
            ha='center', va='center',
            wrap=True,
            fontsize=h3_font_size,
            bbox=dict(facecolor=facecolor, alpha=0.85, boxstyle='round,pad=1', edgecolor=edgecolor, linewidth=0.8)
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_axis_off()

    # ==== Near Duplicates (Questions/Context) ====
    if issue_manager["near_duplicates_questions/context"] is not None:
        for i in range(plot_top_N):
            ax = fig.add_subplot(grid[row_idx, i])
            ax.set_axis_off()
            if i == 0:
                ax.text(0.5, 0.4, "Near-Duplicate for question/context only Ranking",
                        ha='center', va='bottom',
                        fontsize=h1_font_size, fontweight='bold')
        row_idx += 1

        near_duplicate_issues = issue_manager["near_duplicates"]
        for i, (idx1, idx2) in enumerate(near_duplicate_issues["indices"][:plot_top_N]):
            text1 = wrap_text(truncate_text(dataset[int(idx1)][3]))
            text2 = wrap_text(truncate_text(dataset[int(idx2)][3]))

            ax = fig.add_subplot(grid[row_idx, i])
            make_ax_text(ax, text1, "lightblue", "gray")
            ax.set_title(
                f"Ranking: {i + 1}, Idx: {int(idx1)}",
                fontsize=h2_font_size, pad=20, y=1.05
            )

            ax = fig.add_subplot(grid[row_idx + 1, i])
            make_ax_text(ax, text2, "lightblue", "gray")
            ax.set_title(f"Idx: {int(idx2)}", fontsize=h2_font_size, pad=20, y=1.05)
        row_idx += 2

    # ==== Near Duplicates ====
    if issue_manager["near_duplicates"] is not None:
        for i in range(plot_top_N):
            ax = fig.add_subplot(grid[row_idx, i])
            ax.set_axis_off()
            if i == 0:
                ax.text(0.5, 0.4, "Near-Duplicate Ranking",
                        ha='center', va='bottom',
                        fontsize=h1_font_size, fontweight='bold')
        row_idx += 1

        near_duplicate_issues = issue_manager["near_duplicates"]
        for i, (idx1, idx2) in enumerate(near_duplicate_issues["indices"][:plot_top_N]):
            text1 = wrap_text(truncate_text(dataset[int(idx1)][3]))
            text2 = wrap_text(truncate_text(dataset[int(idx2)][3]))

            ax = fig.add_subplot(grid[row_idx, i])
            make_ax_text(ax, text1, "lightblue", "gray")
            ax.set_title(
                f"Ranking: {i + 1}, Idx: {int(idx1)}",
                fontsize=h2_font_size, pad=20, y=1.05
            )

            ax = fig.add_subplot(grid[row_idx + 1, i])
            make_ax_text(ax, text2, "lightblue", "gray")
            ax.set_title(f"Idx: {int(idx2)}", fontsize=h2_font_size, pad=20, y=1.05)
        row_idx += 2

    # ==== Off-topic Samples ====
    if issue_manager["off_topic_samples"] is not None:
        for i in range(plot_top_N):
            ax = fig.add_subplot(grid[row_idx, i])
            ax.set_axis_off()
            if i == 0:
                ax.text(0.5, 0.4, "Off-Topic Samples Ranking",
                        ha='center', va='bottom',
                        fontsize=h1_font_size, fontweight='bold')
        row_idx += 1

        off_topic_issues = issue_manager["off_topic_samples"]
        for i, idx in enumerate(off_topic_issues["indices"][:plot_top_N]):
            text = wrap_text(truncate_text(dataset[int(idx)][3]))
            category = dataset[int(idx)][2]
            ax = fig.add_subplot(grid[row_idx, i])
            make_ax_text(ax, text, "lightyellow", "orange")
            title = f"Ranking: {i + 1}, Idx: {int(idx)}"
            if category != "N/A":
                title += f"\nCategory: {category}"
            ax.set_title(title, fontsize=h2_font_size, pad=20, y=1.05)
        row_idx += 1

    # ==== Label Errors ====
    if issue_manager["label_errors"] is not None:
        for i in range(plot_top_N):
            ax = fig.add_subplot(grid[row_idx, i])
            ax.set_axis_off()
            if i == 0:
                ax.text(0.5, 0.4, "Wrong Label Error Ranking",
                        ha='center', va='bottom',
                        fontsize=h1_font_size, fontweight='bold')
        row_idx += 1

        label_error_issues = issue_manager["label_errors"]
        for i, idx in enumerate(label_error_issues["indices"][:plot_top_N]):
            text = wrap_text(truncate_text(dataset[int(idx)][3]))
            true_label = dataset[int(idx)][1]
            category = dataset[int(idx)][2]
            ax = fig.add_subplot(grid[row_idx, i])
            make_ax_text(ax, text, "lightcoral", "red")
            title = f"Ranking: {i + 1}, Idx: {int(idx)}"
            if true_label != "N/A":
                title += f"\nTrue: {true_label}"
            # if category != "N/A":
            #     title += f"\nCategory: {category}"
            ax.set_title(title, fontsize=h2_font_size, pad=20, y=1.05)
        row_idx += 1

    # ==== Category Errors ====
    if issue_manager["category_errors"] is not None:
        for i in range(plot_top_N):
            ax = fig.add_subplot(grid[row_idx, i])
            ax.set_axis_off()
            if i == 0:
                ax.text(0.5, 0.4, "Wrong Category Error Ranking",
                        ha='center', va='bottom',
                        fontsize=h1_font_size, fontweight='bold')
        row_idx += 1

        category_error_issues = issue_manager["category_errors"]
        for i, idx in enumerate(category_error_issues["indices"][:plot_top_N]):
            text = wrap_text(truncate_text(dataset[int(idx)][3]))
            true_label = dataset[int(idx)][1]
            category = dataset[int(idx)][2]
            ax = fig.add_subplot(grid[row_idx, i])
            make_ax_text(ax, text, "lightcoral", "red")
            title = f"Ranking: {i + 1}, Idx: {int(idx)}"
            if category != "N/A":
                title += f"\nCategory: {category}"
            if true_label != "N/A":
                title += f"\nTrue: {true_label}"
            ax.set_title(title, fontsize=h2_font_size, pad=20, y=1.05)
        row_idx += 1

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.98])

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path_ = Path(f'{output_path}.png')
        counter = 1
        while (output_path_.exists()):
            output_path_ = output_path.with_stem(f"{output_path.stem}_{counter}.png")
            counter += 1
        plt.savefig(output_path_, bbox_inches="tight", dpi=200)
    # plt.show()

def plot_frac_cut(dist, logit_scores, bins, q1, q2, cutoff, loc, scale, path):
    with plt.style.context(["science", "std-colors", "grid"]):
        dist_name = dist.__class__.__name__.split("_")[0]
        fig, ax = plt.subplots(1, 1, figsize=(4, 3))
        subplot_frac_cut(
            ax,
            logit_scores,
            bins,
            q1,
            q2,
            cutoff,
            dist,
            loc,
            scale,
        )
        ax.legend()

        plt.title(dist_name)
        if path is not None:
            plt.savefig(path, bbox_inches="tight")
        plt.show()
        plt.close(fig)
        plt.figure().clear()
        plt.close("all")
        plt.close()
        plt.cla()
        plt.clf()


def subplot_frac_cut(ax, logit_scores, bins, q1, q2, cutoff, dist, loc, scale):
    ax.axvline(
        x=q1,
        color="green",
        linestyle=":",
        linewidth=1.4,
        label="left-tail range",
    )
    ax.axvline(
        x=q2,
        color="green",
        linestyle=":",
        linewidth=1.4,
    )
    ax.axvspan(q1, q2, alpha=0.5, color="green")
    ax.hist(
        logit_scores,
        bins=bins,
        histtype="step",
        density=True,
        log=True,
        label="scores",
        linewidth=1.4,
    )
    x_grid = np.linspace(cutoff, q2, 101)
    y_grid = dist.pdf((x_grid - loc) / scale) / scale
    ax.plot(x_grid, y_grid, label="distribution fit", color="orange")
    ax.axvline(
        x=cutoff,
        color="orange",
        label="outlier cutoff",
        linestyle="--",
        linewidth=1.4,
    )
    ax.set_ylabel("Probability Density", fontsize=18)
    ax.set_xlabel(r"$\tilde{s}$", fontsize=18)


def plot_sensitivity(result, ylabel: str, xlabel: str):
    with plt.style.context(["science", "std-colors", "grid"]):
        fig, ax = plt.subplots(1, 1, figsize=(4, 3))
        subplot_sensitivity(ax, result, ylabel, xlabel)
        plt.show()
        plt.close(fig)
        plt.figure().clear()
        plt.close("all")
        plt.close()
        plt.cla()
        plt.clf()


def subplot_sensitivity(ax, result, ylabel: str, xlabel: str):
    ax.plot(result[:, 0], result[:, 1], marker="o")
    ax.plot(result[:, 0], result[:, 0])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_xlabel(xlabel, fontsize=18)
