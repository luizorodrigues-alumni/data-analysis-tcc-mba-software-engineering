from pathlib import Path

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = BASE_DIR / "files" / "charts"


def read_file_to_df(path: str) -> pd.DataFrame:
	return pd.read_csv(path)


def generate_likert_scale_chart(
    df: pd.DataFrame,
    column_name: str,
    question_number: int,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    
    # Ensure that all Likert scale options (1 to 5) appear in the chart, even when there are no responses for some options.
    response_counts = (
        df[column_name]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    response_counts.plot(
        kind="bar",
        ax=ax,
        color="#4c84e3",
    )

    ax.set_title("")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = output_dir / f"likert_chart_{question_number}.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path


def generate_heatmap_chart(
    df: pd.DataFrame,
    output_path: Path,
    percentage: bool = True,
    xlabel: str = "",
    ylabel: str = "",
) -> Path:
    """
    Generates a heatmap chart from the given DataFrame and saves it to the specified output path.

    Args:
        df (pd.DataFrame): The DataFrame containing the data for the heatmap.
        output_path (Path): The path where the heatmap image will be saved.
        percentage (bool): If True, the heatmap will be scaled to show percentages (0 to 100). Default is True.
        xlabel (str): Label for the x-axis. Default is an empty string.
        ylabel (str): Label for the y-axis. Default is an empty string.
    Returns:
        output_path (Path): The path where the heatmap image was saved.    
    """

    fig, ax = plt.subplots(figsize=(12, 8))
    heatmap_kwargs = {
        "annot": True,
        "fmt": ".2f",
        "cmap": "YlGnBu",
        "cbar": True,
        "linewidths": 0.5,
        "linecolor": "lightgray",
        "square": True,
    }

    # Percentage scale heatmap should have a color bar ranging from 0 to 100
    if percentage:
        heatmap_kwargs["vmin"] = 0
        heatmap_kwargs["vmax"] = 100
        heatmap_kwargs["cbar_kws"] = {"label": "Percentual (%)"}

    # Generate the heatmap and configure its appearance
    sns.heatmap(df, ax=ax, **heatmap_kwargs)
    ax.set_title("Heatmap")
    ax.set_xlabel(xlabel, labelpad=15)
    ax.set_ylabel(ylabel, labelpad=15)
    ax.tick_params(axis="x", pad=8)
    ax.tick_params(axis="y", pad=8)
    fig.tight_layout()

    # Save the heatmap figure
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path