from pandas import DataFrame
import numpy as np
import plotly.express as px
import umap
import pandas as pd
from torch import Tensor
import torch


def plot_umap(embeddings: Tensor, df: DataFrame, n_neighbors=15, min_dist=0.1, color_label="category", finetuned=False) -> Tensor:
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
        title=f"UMAP: {color_label} (Color), n_neighbors={n_neighbors}, min_dist={min_dist}, finetuned_model={finetuned}",
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


def plot_umap_1d(embeddings: Tensor, df: DataFrame, n_neighbors=15, min_dist=0.1, color_label="category", finetuned=False) -> Tensor:
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
        title=f"UMAP: {color_label} (Color), n_neighbors={n_neighbors}, min_dist={min_dist}, finetuned_model={finetuned}",
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


import pandas as pd
import plotly.express as px
import umap
from torch import Tensor


def plot_umap_compared(
    embeddings: Tensor,
    embeddings_finetuned: Tensor,
    df: pd.DataFrame,
    n_neighbors=15,
    min_dist=0.1,
    color_label="category"
) -> Tensor:
    """Plot UMAP visualization comparing regular and fine-tuned embeddings.

    Args:
        embeddings: Input embeddings tensor (regular Model)
        embeddings_finetuned: Input embeddings tensor (fine-tuned Model)
        df: DataFrame containing 'correct', 'category', 'text', and 'task_id' columns
        n_neighbors: Controls local vs global structure (15 is default)
        min_dist: Minimum distance between embedded points (0.1 is default)
        color_label: Column name for coloring points (default: "category")

    Returns:
        Tensor: 2D UMAP embeddings
    """
    # Concatenate embeddings and add a column for model type
    embeddings_all = torch.cat([embeddings, embeddings_finetuned], dim=0)
    df_all = pd.concat([df, df.copy()], ignore_index=True)
    df_all["model_type"] = ["NO"] * len(df) + ["YES"] * len(df)

    # Fit UMAP
    reducer = umap.UMAP(
        n_components=2,
        random_state=42,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric='cosine',
        init='pca'
    )
    embeddings_umap_2d = reducer.fit_transform(embeddings_all)

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_umap_2d[:, 0],
        "y": embeddings_umap_2d[:, 1],
        "correct": df_all["correct"],
        "category": df_all["category"],
        "task_id": df_all["task_id"],
        "model_type": df_all["model_type"],
        "formatted_text": df_all["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create Plotly figure
    fig = px.scatter(
        final_df,
        x="x",
        y="y",
        color=color_label,
        symbol="model_type",
        symbol_map={"NO": "circle", "YES": "square"},
        custom_data=["category", "correct", "model_type", "task_id", "formatted_text"],
        title=f"UMAP: {color_label} (Color), Model Type (Symbol), n_neighbors={n_neighbors}, min_dist={min_dist}",
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
        )
    )

    # Add custom legend entries for symbols
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        name="Regular Model",
        showlegend=True
    )
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="square", color="gray"),
        name="Fine-tuned Model",
        showlegend=True
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Finetuned Model:</b> %{customdata[2]}<br>" +
                      "<b>Task ID:</b> %{customdata[3]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[4]}<extra></extra>"
    )
    fig.update_layout(width=1000, height=700)
    fig.show()
    return embeddings_umap_2d

import umap
import plotly.express as px
import pandas as pd
import torch
from torch import Tensor

def plot_umap_3d_compared(
    embeddings: Tensor,
    embeddings_finetuned: Tensor,
    df: pd.DataFrame,
    n_neighbors=15,
    min_dist=0.1,
    color_label="category"
) -> Tensor:
    """Plot 3D UMAP visualization comparing regular and fine-tuned embeddings.

    Args:
        embeddings: Input embeddings tensor (regular Model)
        embeddings_finetuned: Input embeddings tensor (fine-tuned Model)
        df: DataFrame containing 'correct', 'category', 'text', and 'task_id' columns
        n_neighbors: Controls local vs global structure (15 is default)
        min_dist: Minimum distance between embedded points (0.1 is default)
        color_label: Column name for coloring points (default: "category")

    Returns:
        Tensor: 3D UMAP embeddings
    """
    # Concatenate embeddings and add a column for model type
    embeddings_all = torch.cat([embeddings, embeddings_finetuned], dim=0)
    df_all = pd.concat([df, df.copy()], ignore_index=True)
    df_all["model_type"] = ["NO"] * len(df) + ["YES"] * len(df)

    # Fit UMAP for 3D
    reducer = umap.UMAP(
        n_components=3,
        random_state=42,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric='cosine',
        init='pca'
    )
    embeddings_umap_3d = reducer.fit_transform(embeddings_all)

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_umap_3d[:, 0],
        "y": embeddings_umap_3d[:, 1],
        "z": embeddings_umap_3d[:, 2],
        "correct": df_all["correct"],
        "category": df_all["category"],
        "task_id": df_all["task_id"],
        "model_type": df_all["model_type"],
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
        custom_data=["category", "correct", "model_type", "task_id", "formatted_text"],
        title=f"3D UMAP: {color_label} (Color), n_neighbors={n_neighbors}, min_dist={min_dist}",
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
            xaxis_title="UMAP 1",
            yaxis_title="UMAP 2",
            zaxis_title="UMAP 3"
        )
    )

    # Add custom legend entries for symbols
    fig.add_scatter3d(
        x=[None], y=[None], z=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        name="Regular Model",
        showlegend=True
    )
    fig.add_scatter3d(
        x=[None], y=[None], z=[None],
        mode="markers",
        marker=dict(size=10, symbol="square", color="gray"),
        name="Fine-tuned Model",
        showlegend=True
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Finetuned Model:</b> %{customdata[2]}<br>" +
                      "<b>Task ID:</b> %{customdata[3]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[4]}<extra></extra>"
    )
    fig.update_layout(width=1000, height=700)
    fig.show()
    return embeddings_umap_3d



def plot_umap_1d_compared(embeddings_1: Tensor, embeddings_2: Tensor, df: DataFrame, n_neighbors=15, min_dist=0.1, color_label="category",
                          finetuned=False) -> Tensor:
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
        title=f"UMAP: {color_label} (Color), n_neighbors={n_neighbors}, min_dist={min_dist}, finetuned_model={finetuned}",
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


def plot_umap_1d_compared(
    embeddings_1: Tensor,
    embeddings_2: Tensor,
    df: pd.DataFrame,
    n_neighbors=15,
    min_dist=0.1,
    color_label="category"
) -> Tensor:
    """Plot 1D UMAP visualization comparing regular and fine-tuned embeddings.

    Args:
        embeddings_1: Input embeddings tensor (regular BERT)
        embeddings_2: Input embeddings tensor (fine-tuned BERT)
        df: DataFrame containing 'correct', 'category', 'text', and 'task_id' columns
        n_neighbors: Controls local vs global structure (15 is default)
        min_dist: Minimum distance between embedded points (0.1 is default)
        color_label: Column name for coloring points (default: "category")

    Returns:
        Tensor: 1D UMAP embeddings
    """
    # Concatenate embeddings and add a column for model type
    embeddings_all = torch.cat([embeddings_1, embeddings_2], dim=0)
    df_all = pd.concat([df, df.copy()], ignore_index=True)
    df_all["model_type"] = ["NO"] * len(df) + ["YES"] * len(df)

    # Fit UMAP
    reducer = umap.UMAP(
        n_components=1,
        random_state=42,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric='cosine',
        init='pca'
    )
    embeddings_umap_1d = reducer.fit_transform(embeddings_all)

    # Assign random y-values for visualization
    task_id_to_y = {task_id: np.random.uniform(-2, 2)
                    for task_id in df_all["task_id"].unique()}

    # Create DataFrame with formatted text for hover
    final_df = pd.DataFrame({
        "x": embeddings_umap_1d[:, 0],
        "y": df_all["task_id"].map(task_id_to_y),
        "correct": df_all["correct"],
        "category": df_all["category"],
        "task_id": df_all["task_id"],
        "model_type": df_all["model_type"],
        "formatted_text": df_all["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    # Create Plotly figure
    fig = px.scatter(
        final_df,
        x="x",
        y="y",
        color=color_label,
        symbol="model_type",
        symbol_map={"NO": "circle", "YES": "square"},
        custom_data=["category", "correct", "model_type", "task_id", "formatted_text"],
        title=f"UMAP 1D: {color_label} (Color), Model Type (Symbol), n_neighbors={n_neighbors}, min_dist={min_dist}",
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
    )

    # Add custom legend entries for symbols
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="circle", color="gray"),
        name="Regular BERT",
        showlegend=True
    )
    fig.add_scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, symbol="square", color="gray"),
        name="Fine-tuned BERT",
        showlegend=True
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>Category:</b> %{customdata[0]}<br>" +
                      "<b>Correct:</b> %{customdata[1]}<br>" +
                      "<b>Model:</b> %{customdata[2]}<br>" +
                      "<b>Task ID:</b> %{customdata[3]}<br><br>" +
                      "<b>Text:</b><br>%{customdata[4]}<extra></extra>"
    )

    fig.update_layout(width=1000, height=700)
    fig.show()
    return embeddings_umap_1d
