from pathlib import Path

from src.chart_generator import generate_likert_scale_chart, read_file_to_df
from src import constants


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "files" / "answers" / "answers.csv"



def run_all_likert_scale_charts() -> None:
    """
    Generates Likert scale charts for all questions defined in the constants.QUESTIONS_MAP.
    The charts are saved in the DEFAULT_OUTPUT_DIR.

    Returns:
        None    
    """

    df = read_file_to_df(str(DATA_FILE))
    print(df.columns)
    print(df.head(5))
    print(df.describe())

    for question, details in constants.QUESTIONS_MAP.items():
        if details["question_type"] == "likert_scale":
            column_name = question
            question_number = details["question_number"]
            output_path = generate_likert_scale_chart(
                df=df, 
                column_name=column_name,
                question_number=question_number
            )
            print(f"Chart for question {question_number} saved at: {output_path}")