from pandas import DataFrame
import pandas as pd
from torch import Tensor
import plotly.express as px
import umap
import numpy as np

def plot_umap(embeddings: Tensor, df: DataFrame, n_neighbors=15, min_dist=0.1, color_label="category") -> Tensor:
    """Plot UMAP visualization with the same style as your t-SNE plot.

    Args:
        embeddings: Input embeddings tensor
        df: DataFrame containing 'correct', 'category', and 'text' columns
        n_neighbors: Controls local vs global structure (15 is default)
        min_dist: Minimum distance between embedded points (0.1 is default)

    Returns:
        Tensor: 2D UMAP embeddings
    """
    # Fit UMAP
    reducer = umap.UMAP(
        n_components=2,  # 2D for visualization
        random_state=42,  # Reproducibility
        n_neighbors=n_neighbors,  # Balances local/global structure
        min_dist=min_dist,  # Controls how tightly points are packed
        metric='cosine',  # Use cosine for sentence embeddings
        init='pca'  # Initialize with PCA for stability
    )
    embeddings_umap_2d = reducer.fit_transform(embeddings)

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_umap_2d[:, 0],
        "y": embeddings_umap_2d[:, 1],
        "correct": df["correct"],  # Binary (0/1)
        "category": df["category"],  # Categorical
        "task_id": df["task_id"],
        "formatted_text": df["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create Plotly figure with same styling as t-SNE
    fig = px.scatter(
        final_df,
        x="x",
        y="y",
        color=color_label,  # Color by category
        symbol="correct",  # Symbol by correctness
        symbol_map={0: "circle", 1: "diamond"},
        custom_data=["category", "correct", "task_id", "formatted_text"],
        title=f"UMAP: {color_label} (Color), n_neighbors={n_neighbors}, min_dist={min_dist}",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Remove color legend and customize symbol legend (same as t-SNE)
    fig.update_traces(showlegend=False)
    fig.update_layout(
        legend_title_text="Correctness",
        legend=dict(
            itemsizing='constant',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
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
    fig.update_layout(width=1000, height=700)
    fig.show()


def plot_umap_1d(embeddings: Tensor, df: DataFrame, n_neighbors=15, min_dist=0.1, color_label="category") -> Tensor:
    reducer = umap.UMAP(
        n_components=1,  # 2D for visualization
        random_state=42,  # Reproducibility
        n_neighbors=n_neighbors,  # Balances local/global structure
        min_dist=min_dist,  # Controls how tightly points are packed
        metric='cosine',  # Use cosine for sentence embeddings
        init='pca'  # Initialize with PCA for stability
    )
    embeddings_umap_1d = reducer.fit_transform(embeddings)

    task_id_to_y = {task_id: np.random.uniform(-2, 2)
                    for task_id in df["task_id"].unique()}

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_umap_1d[:, 0],
        "y": df["task_id"].map(task_id_to_y),
        "correct": df["correct"],  # Binary (0/1)
        "category": df["category"],  # Categorical
        "task_id": df["task_id"],
        "formatted_text": df["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create Plotly figure with same styling as t-SNE
    fig = px.scatter(
        final_df,
        x="x",
        y="y",
        color=color_label,  # Color by category
        symbol="correct",  # Symbol by correctness
        symbol_map={0: "circle", 1: "diamond"},
        custom_data=["category", "correct", "task_id", "formatted_text"],
        title=f"UMAP: {color_label} (Color), n_neighbors={n_neighbors}, min_dist={min_dist}",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Remove color legend and customize symbol legend (same as t-SNE)
    fig.update_traces(showlegend=False)
    fig.update_layout(
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

    fig.update_layout(width=1000, height=700)
    fig.show()