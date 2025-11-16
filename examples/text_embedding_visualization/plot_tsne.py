from pandas import DataFrame
import pandas as pd
from torch import Tensor
from sklearn.manifold import TSNE
import plotly.express as px
import numpy as np

def plot_tsne_1d(embeddings: Tensor, df: DataFrame, perplexity=30, color_label="category") -> Tensor:
    tsne = TSNE(
        n_components=1,  # Always 2 for 2D visualization
        random_state=42,  # Reproducibility
        perplexity=perplexity,  # Balanced for 10k samples (default: 30)
        max_iter=10000,  # Sufficient convergence (default: 250)
        early_exaggeration=12,  # Default (helps cluster separation)
        learning_rate=200,  # Default (adjust if clusters look squashed)
        init='pca',  # Initialize with PCA for stability
        metric='cosine'  # Use cosine for sentence embeddings (L2 is default)
    )

    task_id_to_y = {task_id: np.random.uniform(-2, 2)
                for task_id in df["task_id"].unique()}

    embeddings_tsne_1d = tsne.fit_transform(embeddings)
    final_df = pd.DataFrame({
        "x": embeddings_tsne_1d[:, 0],
        "y": df["task_id"].map(task_id_to_y),
        "correct": df["correct"],  # Binary (0/1)
        "category": df["category"],  # Categorical
        "task_id": df["task_id"],
        "formatted_text": df["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    fig = px.scatter(
        final_df,
        x="x",
        y="y",
        color=color_label,
        symbol="correct",
        symbol_map={0: "circle", 1: "diamond"},
        custom_data=["category", "correct", "task_id", "formatted_text"],
        title="t-SNE: Category (Color), perplexity={0}".format(perplexity),
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Remove color legend and customize symbol legend
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


def plot_tsne(embeddings: Tensor, df: DataFrame, perplexity=30, color_label="category") -> Tensor:
    tsne = TSNE(
        n_components=2,  # Always 2 for 2D visualization
        random_state=42,  # Reproducibility
        perplexity=perplexity,  # Balanced for 10k samples (default: 30)
        max_iter=10000,  # Sufficient convergence (default: 250)
        early_exaggeration=12,  # Default (helps cluster separation)
        learning_rate=200,  # Default (adjust if clusters look squashed)
        init='pca',  # Initialize with PCA for stability
        metric='cosine'  # Use cosine for sentence embeddings (L2 is default)
    )
    embeddings_tsne_2d = tsne.fit_transform(embeddings)
    final_df = pd.DataFrame({
        "x": embeddings_tsne_2d[:, 0],
        "y": embeddings_tsne_2d[:, 1],
        "correct": df["correct"],  # Binary (0/1)
        "category": df["category"],  # Categorical
        "task_id": df["task_id"],
        "formatted_text": df["text"].apply(lambda x: '<br>'.join(x[i:i + 50] for i in range(0, len(x), 50))),
    })

    fig = px.scatter(
        final_df,
        x="x",
        y="y",
        color=color_label,
        symbol="correct",
        symbol_map={0: "circle", 1: "diamond"},
        custom_data=["category", "correct", "task_id", "formatted_text"],
        title="t-SNE: Category (Color), perplexity={0}".format(perplexity),
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    # Remove color legend and customize symbol legend
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