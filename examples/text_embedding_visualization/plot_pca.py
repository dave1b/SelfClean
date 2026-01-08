from typing import Tuple
import plotly.subplots as sp
from pandas import DataFrame
import pandas as pd
from sklearn.decomposition import PCA
from torch import Tensor
import plotly.express as px
import numpy as np


def plot_pca(embeddings: Tensor, df: DataFrame, color_label="category") -> Tensor:
    pca = PCA(
        n_components=2,  # 2D for visualization
        random_state=42  # Reproducibility
    )
    embeddings_2d_pca = pca.fit_transform(embeddings)

    # Create DataFrame with formatted text for hover
    final_df_pca = pd.DataFrame({
        "x": embeddings_2d_pca[:, 0],
        "y": embeddings_2d_pca[:, 1],
        "correct": df["correct"],  # Binary (0/1)
        "category": df["category"],  # Categorical
        "task_id": df["task_id"],
        "formatted_text": df["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create Plotly figure
    fig = px.scatter(
        final_df_pca,
        x="x",
        y="y",
        color=color_label,  # Color by category
        symbol="correct",  # Symbol by correctness
        symbol_map={0: "circle", 1: "diamond"},
        custom_data=["category", "correct", "task_id", "formatted_text"],
        title=f"PCA (PC1: {pca.explained_variance_ratio_[0]:.2f}, PC2: {pca.explained_variance_ratio_[1]:.2f})",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Remove color legend and customize symbol legend
    fig.update_traces(showlegend=False)
    fig.update_layout(
        xaxis_title="PC1",
        yaxis_title="PC2",
        legend_title_text="Correctness",
        legend=dict(
            itemsizing='constant',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )

    # Add custom legend entries for symbols only
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        name="Incorrect",
        showlegend=True
    )
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="diamond", color="gray"),
        name="Correct",
        showlegend=True
    )

    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Task ID:</b> %{customdata[2]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[3]}<extra></extra>"
    )

    # Add explained variance annotation
    fig.add_annotation(
        x=0.5,
        y=1.15,
        xref="paper",
        yref="paper",
        text=f"Total Variance Explained: {sum(pca.explained_variance_ratio_) * 100:.1f}%",
        showarrow=False,
        font=dict(size=12)
    )
    fig.update_layout(width=1000, height=700)
    fig.show()


def plot_pca_1d(embeddings: Tensor, df: DataFrame, color_label="category") -> Tensor:
    pca = PCA(
        n_components=1,  # 1D for visualization
        random_state=42  # Reproducibility
    )
    embeddings_1d_pca = pca.fit_transform(embeddings)
    # Create DataFrame with formatted text for hover
    # Create a mapping of task_id to random y-value
    task_id_to_y = {task_id: np.random.uniform(-2, 2)
                    for task_id in df["task_id"].unique()}

    # Create DataFrame with consistent y-values for each task_id
    final_df_pca = pd.DataFrame({
        "x": embeddings_1d_pca[:, 0],
        "y": df["task_id"].map(task_id_to_y),  # Map task_id to its random y-value
        "correct": df["correct"],  # Binary (0/1)
        "category": df["category"],  # Categorical
        "task_id": df["task_id"],
        "formatted_text": df["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create Plotly figure
    fig = px.scatter(
        final_df_pca,
        x="x",
        y="y",
        color=color_label,  # Color by category
        symbol="correct",  # Symbol by correctness
        symbol_map={0: "circle", 1: "diamond"},
        custom_data=["category", "correct", "task_id", "formatted_text"],
        title=f"PCA (PC1: {pca.explained_variance_ratio_[0]:.2f})",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    # Remove color legend and customize symbol legend
    fig.update_traces(showlegend=False)
    fig.update_layout(
        xaxis_title="PC1",
        yaxis_title="",
        legend_title_text="Correctness",
        legend=dict(
            itemsizing='constant',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )
    # Add custom legend entries for symbols only
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        name="Incorrect",
        showlegend=True
    )
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="diamond", color="gray"),
        name="Correct",
        showlegend=True
    )
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Task ID:</b> %{customdata[2]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[3]}<extra></extra>"
    )
    # Add explained variance annotation
    fig.add_annotation(
        x=0.5,
        y=1.15,
        xref="paper",
        yref="paper",
        text=f"Variance Explained: {pca.explained_variance_ratio_[0] * 100:.1f}%",
        showarrow=False,
        font=dict(size=12)
    )
    fig.update_layout(width=1000, height=700)
    fig.show()

def plot_pca_2d_comparing(
    embeddings_1: Tensor,
    embeddings_2: Tensor,
    df: pd.DataFrame,
    color_label="category"
) -> None:
    # Stack embeddings and add a column to distinguish model type
    embeddings_1_np = embeddings_1.detach().cpu().numpy()
    embeddings_2_np = embeddings_2.detach().cpu().numpy()
    all_embeddings = np.vstack([embeddings_1_np, embeddings_2_np])

    # Fit PCA on all embeddings
    pca = PCA(n_components=2, random_state=42)
    all_embeddings_2d_pca = pca.fit_transform(all_embeddings)

    # Split back into two sets
    embeddings_1_2d = all_embeddings_2d_pca[:len(embeddings_1_np)]
    embeddings_2_2d = all_embeddings_2d_pca[len(embeddings_1_np):]

    # Create DataFrames for each model's embeddings
    df_1 = df.copy()
    df_1["x"] = embeddings_1_2d[:, 0]
    df_1["y"] = embeddings_1_2d[:, 1]
    df_1["model_type"] = "Finetuned: NO"

    df_2 = df.copy()
    df_2["x"] = embeddings_2_2d[:, 0]
    df_2["y"] = embeddings_2_2d[:, 1]
    df_2["model_type"] = "Finetuned: YES"

    # Combine DataFrames
    final_df_pca = pd.concat([df_1, df_2], ignore_index=True)

    # Create Plotly figure
    fig = px.scatter(
        final_df_pca,
        x="x",
        y="y",
        color=color_label,  # Color by category
        symbol="model_type",  # Symbol by model type
        symbol_map={"Finetuned: NO": "circle", "Finetuned: YES": "diamond"},
        custom_data=["category", "model_type", "task_id", "formatted_text"],
        title=f"PCA (PC1: {pca.explained_variance_ratio_[0]:.2f}, PC2: {pca.explained_variance_ratio_[1]:.2f})",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Customize legend
    fig.update_layout(
        xaxis_title="PC1",
        yaxis_title="PC2",
        legend_title_text="Model Type & Category",
        legend=dict(
            itemsizing='constant',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )

    # Add custom legend entries for symbols
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        name="Finetuned: NO",
        showlegend=True
    )
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="diamond", color="gray"),
        name="Finetuned: YES",
        showlegend=True
    )

    # Hover template
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Model Type:</b> %{customdata[1]}<br>" +
                      "<b>Task ID:</b> %{customdata[2]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[3]}<extra></extra>"
    )

    # Add explained variance annotation
    fig.add_annotation(
        x=0.5,
        y=1.15,
        xref="paper",
        yref="paper",
        text=f"Total Variance Explained: {sum(pca.explained_variance_ratio_) * 100:.1f}%",
        showarrow=False,
        font=dict(size=12)
    )

    fig.update_layout(width=1000, height=700)
    fig.show()

import plotly.express as px
import pandas as pd
import torch
from torch import Tensor
from sklearn.decomposition import PCA


def plot_pca_3d_combined(
    embeddings_finetuned: Tensor,
    embeddings: Tensor,
    df: pd.DataFrame,
    color_label="category",
    model_finetuned_name="",
    model_2_name="",
) -> Tensor:
    """Plot 3D PCA visualization comparing regular and fine-tuned embeddings.

    Args:
        embeddings: Input embeddings tensor (regular Model)
        embeddings_finetuned: Input embeddings tensor (fine-tuned Model)
        df: DataFrame containing 'correct', 'category', 'text', and 'task_id' columns
        color_label: Column name for coloring points (default: "category")

    Returns:
        Tensor: 3D PCA embeddings
    """
    # Concatenate embeddings and add a column for model type
    embeddings_all = torch.cat([embeddings, embeddings_finetuned], dim=0)
    df_all = pd.concat([df, df.copy()], ignore_index=True)
    df_all["model_type"] = ["NO"] * len(df) + ["YES"] * len(df)

    # Fit PCA for 3D
    pca = PCA(n_components=3, random_state=42)
    embeddings_pca_3d = pca.fit_transform(embeddings_all)

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_pca_3d[:, 0],
        "y": embeddings_pca_3d[:, 1],
        "z": embeddings_pca_3d[:, 2],
        "correct": df_all["correct"],
        "category": df_all["category"],
        "task_id": df_all["task_id"],
        "model_type": df_all["model_type"],
        "off_topic": df_all["off_topic"],
        "formatted_text": df_all["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create 3D Plotly figure
    fig = px.scatter_3d(
        final_df,
        x="x",
        y="y",
        z="z",
        color=color_label,
        symbol="model_type",
        symbol_map={"NO": "circle", "YES": "square"},
        custom_data=["category", "correct", "model_type", "task_id", "formatted_text", "off_topic"],
        title=f"PCA: (PC1: {pca.explained_variance_ratio_[0]:.2f}, PC2: {pca.explained_variance_ratio_[1]:.2f}, PC3: {pca.explained_variance_ratio_[2]:.2f}), {color_label[0].upper() + color_label[1:]} (Color)",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Customize legend
    fig.update_traces(showlegend=False)
    fig.update_layout(
        legend_title_text="Model Type",
        legend=dict(
            itemsizing='constant',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        scene=dict(
            xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
            yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
            zaxis_title=f"PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)"
        )
    )

    # Add custom legend entries for symbols
    fig.add_scatter3d(
        x=[None], y=[None], z=[None],
        mode="markers",
        marker=dict(size=10, symbol="square", color="gray"),
        name=model_finetuned_name,
        # name="SimCSE fine-tuned DeBERTaV3",
        showlegend=True
    )
    fig.add_scatter3d(
        x=[None], y=[None], z=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        # name="Base DeBERTaV3",
        name=model_2_name,
        showlegend=True
    )


    # Update hover template
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Finetuned Model:</b> %{customdata[2]}<br>" +
                      "<b>Task ID:</b> %{customdata[3]}<br>" +
                      "<b>Off-Topic:</b> %{customdata[5]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[4]}<extra></extra>"
    )
    fig.update_layout(width=1000, height=700)
    fig.show()
    # return embeddings_pca_3d



def plot_pca_3d_side_by_side(
    embeddings: torch.Tensor,
    embeddings_finetuned: torch.Tensor,
    df: pd.DataFrame,
    color_label: str = "category"
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Plot 3D PCA visualizations for regular and fine-tuned embeddings side by side.

    Args:
        embeddings: Input embeddings tensor (regular Model)
        embeddings_finetuned: Input embeddings tensor (fine-tuned Model)
        df: DataFrame containing 'correct', 'category', 'text', and 'task_id' columns
        color_label: Column name for coloring points (default: "category")

    Returns:
        Tuple[Tensor, Tensor]: 3D PCA embeddings for both models
    """
    # Fit PCA for 3D for each model separately
    pca = PCA(n_components=3, random_state=42)
    embeddings_pca_3d = pca.fit_transform(embeddings)
    embeddings_finetuned_pca_3d = pca.fit_transform(embeddings_finetuned)

    # Create DataFrames for each model
    df_base = df.copy()
    df_finetuned = df.copy()

    df_base["formatted_text"] = df_base["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50)))
    df_finetuned["formatted_text"] = df_finetuned["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50)))

    # Create subplots
    fig = sp.make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
        subplot_titles=(
            f"Base Model PCA (PC1: {pca.explained_variance_ratio_[0]:.2f}, PC2: {pca.explained_variance_ratio_[1]:.2f}, PC3: {pca.explained_variance_ratio_[2]:.2f})",
            f"Fine-tuned Model PCA (PC1: {pca.explained_variance_ratio_[0]:.2f}, PC2: {pca.explained_variance_ratio_[1]:.2f}, PC3: {pca.explained_variance_ratio_[2]:.2f})"
        )
    )

    # Add base model plot
    fig_base = px.scatter_3d(
        df_base,
        x=embeddings_pca_3d[:, 0],
        y=embeddings_pca_3d[:, 1],
        z=embeddings_pca_3d[:, 2],
        color=color_label,
        custom_data=["category", "correct", "task_id", "formatted_text", "off_topic"],
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    for trace in fig_base.data:
        fig.add_trace(trace, row=1, col=1)

    # Add fine-tuned model plot
    fig_finetuned = px.scatter_3d(
        df_finetuned,
        x=embeddings_finetuned_pca_3d[:, 0],
        y=embeddings_finetuned_pca_3d[:, 1],
        z=embeddings_finetuned_pca_3d[:, 2],
        color=color_label,
        custom_data=["category", "correct", "task_id", "formatted_text", "off_topic"],
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    for trace in fig_finetuned.data:
        fig.add_trace(trace, row=1, col=2)

    # Update hover template for both subplots
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Task ID:</b> %{customdata[2]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[3]}<extra></extra>"
    )

    # Update layout
    fig.update_layout(
        width=1400, height=700,
        scene=dict(
            xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
            yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
            zaxis_title=f"PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)"
        ),
        scene2=dict(
            xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
            yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
            zaxis_title=f"PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)"
        )
    )

    fig.show()
    # return embeddings_pca_3d, embeddings_finetuned_pca_3d



from enum import Enum
import torch
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

class EmbeddingPoolingType(Enum):
    CLS = "cls"
    MEAN = "mean_pooling"
    FIRST_LAST_AVERAGE = "first_last_average"
    MAX = "max"

def plot_pca_3d_combined(
    embeddings_cls: Tensor,
    embeddings_mean: Tensor,
    embeddings_first_last: Tensor,
    embeddings_max: Tensor,
    df: pd.DataFrame,
    color_label="category",
    model_name="",
) -> Tensor:
    """Plot 3D PCA visualization comparing embeddings from different pooling types.

    Args:
        embeddings_cls: Input embeddings tensor (CLS pooling)
        embeddings_mean: Input embeddings tensor (Mean pooling)
        embeddings_first_last: Input embeddings tensor (First-Last Average pooling)
        embeddings_max: Input embeddings tensor (Max pooling)
        df: DataFrame containing 'correct', 'category', 'text', and 'task_id' columns
        color_label: Column name for coloring points (default: "category")
        model_name: Name of the model for legend

    Returns:
        Tensor: 3D PCA embeddings
    """
    # Concatenate all embeddings and create a DataFrame with pooling type info
    embeddings_all = torch.cat([embeddings_cls, embeddings_mean, embeddings_first_last, embeddings_max], dim=0)
    df_all = pd.concat([df] * 4, ignore_index=True)
    df_all["pooling_type"] = (
        [EmbeddingPoolingType.CLS.value] * len(df) +
        [EmbeddingPoolingType.MEAN.value] * len(df) +
        [EmbeddingPoolingType.FIRST_LAST_AVERAGE.value] * len(df) +
        [EmbeddingPoolingType.MAX.value] * len(df)
    )

    # Fit PCA for 3D
    pca = PCA(n_components=3, random_state=42)
    embeddings_pca_3d = pca.fit_transform(embeddings_all)

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_pca_3d[:, 0],
        "y": embeddings_pca_3d[:, 1],
        "z": embeddings_pca_3d[:, 2],
        "correct": df_all["correct"],
        "category": df_all["category"],
        "task_id": df_all["task_id"],
        "pooling_type": df_all["pooling_type"],
        "off_topic": df_all["off_topic"],
        "formatted_text": df_all["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create 3D Plotly figure
    fig = px.scatter_3d(
        final_df,
        x="x",
        y="y",
        z="z",
        color="pooling_type",  # Color by pooling type
        symbol="pooling_type",  # Symbol by pooling type (optional)
        custom_data=["category", "correct", "pooling_type", "task_id", "formatted_text", "off_topic"],
        title=f"PCA: (PC1: {pca.explained_variance_ratio_[0]:.2f}, PC2: {pca.explained_variance_ratio_[1]:.2f}, PC3: {pca.explained_variance_ratio_[2]:.2f}), {color_label[0].upper() + color_label[1:]} (Color)",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Customize legend
    fig.update_traces(showlegend=True)
    fig.update_layout(
        legend_title_text="Pooling Type",
        legend=dict(
            itemsizing='constant',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        scene=dict(
            xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
            yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
            zaxis_title=f"PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)"
        )
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Pooling Type:</b> %{customdata[2]}<br>" +
                      "<b>Task ID:</b> %{customdata[3]}<br>" +
                      "<b>Off-Topic:</b> %{customdata[5]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[4]}<extra></extra>"
    )
    fig.update_layout(width=1000, height=700)
    fig.show()
