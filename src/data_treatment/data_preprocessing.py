
import re
import unicodedata

import pandas as pd

from src import constants


ROLE_COLUMN_NUMBER = 2
ROLE_DETAIL_COLUMN_NUMBER = 3

def _normalize_text(value: str) -> str:
	"""
	Function to normalize text by removing accents, converting to lowercase, and stripping whitespace.
    Args:
        value (str): The text to be normalized.
    Returns:
        str: The normalized text.
	"""
	normalized = unicodedata.normalize("NFKD", value)
	normalized = normalized.encode("ascii", "ignore").decode("ascii")
	normalized = normalized.lower().strip()
	normalized = re.sub(r"\s+", " ", normalized)
	return normalized


def data_preprocess_role_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to preprocess the role column in the DataFrame. It normalizes the text in the role and role detail columns,
    and updates the role column based on specific conditions related to the role detail.

    Args:
        df (pd.DataFrame): The input DataFrame containing the survey responses.
    Returns:
        pd.DataFrame: The DataFrame with the preprocessed role column.
    """
    number_to_question_map = constants.NUMBER_TO_QUESTIONS_MAP
    role_column = number_to_question_map[ROLE_COLUMN_NUMBER]
    role_detail_column = number_to_question_map[ROLE_DETAIL_COLUMN_NUMBER]


    # Normalize the role and role detail columns
    processed_df = df.copy()
    role_normalized = processed_df[role_column].fillna("").astype(str).map(_normalize_text)
    role_detail_normalized = processed_df[role_detail_column].fillna("").astype(str).map(_normalize_text)

    # Update the role column for respondents who selected "Outro" and provided a detail that matches "Full Stack" or "Fullstack"
    is_other_role = role_normalized.isin({"outro", "outros"})
    is_full_stack_detail = role_detail_normalized.str.contains(
        r"\b(full\s*[- ]?\s*stack|fullstack)\b",
        regex=True,
    )
    processed_df.loc[
        is_other_role & is_full_stack_detail,
        role_column,
    ] = "Engenheiro(a) de Software Full-stack"

    # Update the role column for respondents who selected "Outro" and provided a detail that matches "Gestor"
    is_manager_detail = role_detail_normalized.str.contains(
        r"\b(gestor|coordenador|líder)\b",
        regex=True,
    )
    processed_df.loc[
        is_other_role & is_manager_detail,
        role_column,
    ] = "Gestor(a) de Engenharia de Software"

    print("columns after preprocessing:\n", processed_df[role_column].value_counts()) 
    return processed_df


def data_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to run all preprocessing steps on the DataFrame.
    """
    df = data_preprocess_role_column(df)
    return df