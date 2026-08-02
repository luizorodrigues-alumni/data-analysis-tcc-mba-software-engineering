from pathlib import Path

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
    # Garantir que todas as opções da escala Likert (1 a 5) apareçam no gráfico,
    # mesmo quando não houver nenhuma resposta para alguma opção.
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