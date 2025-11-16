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
