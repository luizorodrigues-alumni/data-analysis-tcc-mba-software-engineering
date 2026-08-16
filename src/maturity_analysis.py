from pathlib import Path
from typing import Any

import pandas as pd

from src.constants import NUMBER_TO_QUESTIONS_MAP, MATURITY_LEVELS_MAP
from src.chart_generator import generate_heatmap_chart, read_file_to_df
from src.data_treatment.data_preprocessing import data_preprocessing


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "files" / "answers" / "answers.csv"
MATURITY_ANALYSIS_DIR = BASE_DIR / "files" / "maturity_analysis"
PREDOMINANT_LEVEL_COLUMN = "nivel_predominante"
PREDOMINANT_LEVEL_MEDIAN_COLUMN = "nivel_predominante_mediana"


def _get_question_columns(question_numbers: list[int]) -> list[str]:
    """
    Retrieves the column names corresponding to the given question numbers from the NUMBER_TO_QUESTIONS_MAP.
    Args:
        question_numbers (list[int]): A list of question numbers for which to retrieve the column names.
    Returns:
        list[str]: A list of column names corresponding to the provided question numbers.
    """
    return [NUMBER_TO_QUESTIONS_MAP[q_num] for q_num in question_numbers]


def _calculate_scores_by_level(df: pd.DataFrame) -> None:
    """
    Calculates the mean and median scores for each maturity level based on the specified questions.
    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses.
    Returns:
        None: The function modifies the DataFrame in place by adding new columns for each maturity level's mean and median scores.    
    """
    for level, meta in MATURITY_LEVELS_MAP.items():
        col_names = _get_question_columns(meta["questions"])

        # Converts to numeric to ensure consistent mean/median calculation.
        for col in col_names:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        col_score_name = f"score_nivel_{level}"
        df[col_score_name] = df[col_names].mean(axis=1)
        df[f"{col_score_name}_median"] = df[col_names].median(axis=1)


def _determine_predominant_level(row: pd.Series, score_suffix: str = "") -> int:
    """
    Determines the predominant maturity level for a given respondent based on their scores for each level.
    Args:
        row (pd.Series): A row from the DataFrame representing a respondent's scores.
        score_suffix (str): An optional suffix to specify which score to use (e.g., "_median" for median scores). Default is an empty string for mean scores.
    Returns:
        int: The predominant maturity level (0 if no level meets the threshold).    
    """

    scores = [
        (level, row[f"score_nivel_{level}{score_suffix}"])
        for level in MATURITY_LEVELS_MAP
    ]
    valid_scores = [(level, score) for level, score in scores if pd.notna(score)]

    if not valid_scores:
        return 0

    # In case of a tie, chooses the highest level.
    max_level, max_score = max(valid_scores, key=lambda item: (item[1], item[0]))
    return max_level if max_score >= 3.5 else 0


def _add_predominant_levels(df: pd.DataFrame) -> None:
    """
    Adds the predominant maturity level and the median-based predominant level to the DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses with maturity scores.
    Returns:
        None: The function modifies the DataFrame in place by adding two new columns for the predominant maturity level and the median-based predominant level.
    """
    df[PREDOMINANT_LEVEL_COLUMN] = df.apply(_determine_predominant_level, axis=1)
    df[PREDOMINANT_LEVEL_MEDIAN_COLUMN] = df.apply(
        lambda row: _determine_predominant_level(row, "_median"),
        axis=1,
    )


def _build_summary_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a summary DataFrame containing the count and percentage of respondents for each maturity level.
    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses with maturity levels.
    Returns:
        pd.DataFrame: A summary DataFrame with columns for maturity level, label, count, and percentage of respondents.
    """
    level_counts = df[PREDOMINANT_LEVEL_COLUMN].value_counts().to_dict()
    total_respondents = len(df)

    if total_respondents == 0:
        raise ValueError(
            "Nenhum respondente encontrado. O arquivo CSV pode estar vazio ou mal formatado."
        )

    summary_data: list[dict[str, Any]] = []

    for level, meta in MATURITY_LEVELS_MAP.items():
        count = int(level_counts.get(level, 0))
        percentage = (count / total_respondents) * 100
        summary_data.append(
            {
                "Nível": level,
                "Rótulo": meta["label"],
                "Quantidade de Pessoas": count,
                "Percentual (%)": round(percentage, 2),
            }
        )

    count_0 = int(level_counts.get(0, 0))
    percentage_0 = (count_0 / total_respondents) * 100
    summary_data.append(
        {
            "Nível": 0,
            "Rótulo": "Nível 0 - Inconsistente (Sem maturidade clara)",
            "Quantidade de Pessoas": count_0,
            "Percentual (%)": round(percentage_0, 2),
        }
    )

    return pd.DataFrame(summary_data)


def _export_maturity_outputs(df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    """
    Exports the maturity analysis results to CSV files in the MATURITY_ANALYSIS_DIR.
    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses with maturity levels.
        summary_df (pd.DataFrame): The summary DataFrame with counts and percentages for each maturity level.
    Returns:
        None
    """

    summary_file_path = MATURITY_ANALYSIS_DIR / "maturity_levels_summary.csv"
    summary_file_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_file_path, index=False)
    print("Maturity Analysis: \n", summary_df)

    df_file_path = MATURITY_ANALYSIS_DIR / "maturity_analysis_by_score.csv"
    df.to_csv(df_file_path, index=False)


def run_maturity_analysis_by_score() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Runs the maturity analysis by calculating scores for each maturity level, determining the predominant level for each respondent, and generating a summary DataFrame. The results are exported to CSV files in the MATURITY
    ANALYSIS_DIR.
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the DataFrame with maturity scores and the summary DataFrame with counts and percentages for each maturity level.
    """

    raw_df = read_file_to_df(DATA_FILE)
    df = data_preprocessing(df=raw_df)

    _calculate_scores_by_level(df)
    _add_predominant_levels(df)

    summary_df = _build_summary_dataframe(df)
    _export_maturity_outputs(df, summary_df)

    return df, summary_df


def generate_profile_cross_analysis(df: pd.DataFrame) -> None:
    """
    Generates cross-analysis charts and CSV files comparing maturity levels with role, experience, and sector.
    The charts are saved in the MATURITY_ANALYSIS_DIR.
    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses with maturity levels.
    Returns:
        None    
    """

    col_role = NUMBER_TO_QUESTIONS_MAP[2]
    col_exp = NUMBER_TO_QUESTIONS_MAP[4]
    col_sector = NUMBER_TO_QUESTIONS_MAP[5]

    cross_analyses = [
        {"name": "por_setor", "column": col_sector, "title": "Maturidade vs Setor"},
        {"name": "por_papel", "column": col_role, "title": "Maturidade vs Papel"},
        {
            "name": "por_experiencia",
            "column": col_exp,
            "title": "Maturidade vs Experiência",
        },
    ]

    for analysis in cross_analyses:
        col = analysis["column"]

        # Cross tabulation with normalization to get percentages
        crosstab_df = pd.crosstab(
            index=df[col],
            columns=df[PREDOMINANT_LEVEL_MEDIAN_COLUMN], # Use the median-based predominant level for cross-analysis
            normalize="index",
        ) * 100

        crosstab_df = crosstab_df.round(2)

        crosstab_df.columns = [f"Nível {c}" for c in crosstab_df.columns]
        file_path = MATURITY_ANALYSIS_DIR / f"crosstab_maturidade_{analysis['name']}.csv"

        crosstab_df.reset_index().to_csv(file_path, index=False)
        print(f"Exportado: {file_path.name}")

        generate_heatmap_chart(
            df=crosstab_df,
            output_path=MATURITY_ANALYSIS_DIR / f"heatmap_maturidade_{analysis['name']}.png",
            xlabel="Nível de Maturidade",
        )