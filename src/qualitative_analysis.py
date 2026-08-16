from pathlib import Path

from constants import NUMBER_TO_QUESTIONS_MAP
import pandas as pd

def generate_qualitative_reports(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates qualitative reports based on the survey responses for questions 18 and 19.
    The function calculates the frequency of specific categories mentioned in the responses and generates two separate reports:
    1. Report for Question 18 (Impacto Negativo)
    2. Report for Question 19 (Exemplo de Projeto)

    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses.
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two DataFrames:
            - The first DataFrame corresponds to the report for Question 18.
            - The second DataFrame corresponds to the report for Question 19.
    """
    # 1. Define the original text columns to know who responded
    q18_col = NUMBER_TO_QUESTIONS_MAP[18]
    q19_col = NUMBER_TO_QUESTIONS_MAP[19]
    
    # Base list of manually created categories
    base_categories = [
        'debito_tecnico', 'retrabalho', 'desalinhamento', 
        'desmotivação', 'inviabilidade', 'valor', 'qualidade'
    ]
    
    # Internal function to calculate frequencies of a group
    def calculate_frequencies(df_subset: pd.DataFrame, suffix: str, total_valid: int) -> pd.DataFrame:
        data = []
        for cat in base_categories:
            col_name = f"{cat}{suffix}"
            
            # Checks if the column actually exists in the DataFrame
            if col_name in df_subset.columns:
                # Converts to int (if it is True/False or string '1'/'0') and sums
                count = df_subset[col_name].fillna(0).astype(int).sum()
                
                # Protection against division by zero
                percentage = (count / total_valid) * 100 if total_valid > 0 else 0
                
                # Formats the name for the report (e.g.: 'debito_tecnico' -> 'Debito Tecnico')
                label = cat.replace('_', ' ').title()
                
                data.append({
                    'Categoria': label,
                    'Quantidade de Pessoas': count,
                    'Percentual (%)': round(percentage, 2)
                })
                
        # Sorts from highest to lowest percentage to facilitate reading
        report_df = pd.DataFrame(data).sort_values(by='Percentual (%)', ascending=False)
        return report_df

    # ==========================================
    # REPORT 1: Question 18 (Negative Impact)
    # ==========================================
    # Filters only those who wrote more than 5 characters
    mask_q18 = df[q18_col].notna() & (df[q18_col].astype(str).str.strip().str.len() > 5)
    df_q18_validos = df[mask_q18]
    total_validos_q18 = len(df_q18_validos)
    
    report_q1 = calculate_frequencies(df_q18_validos, '1', total_validos_q18)
    
    # ==========================================
    # REPORT 2: Question 19 (Project Example)
    # ==========================================
    mask_q19 = df[q19_col].notna() & (df[q19_col].astype(str).str.strip().str.len() > 5)
    df_q19_validos = df[mask_q19]
    total_validos_q19 = len(df_q19_validos)
    
    report_q2 = calculate_frequencies(df_q19_validos, '2', total_validos_q19)

    # Displays summaries in the terminal
    print(f"--- Report Question 18 ---")
    print(f"Total de respondentes válidos: {total_validos_q18}")
    print(report_q1.to_string(index=False))
    print("\n")
    
    print(f"--- Report Question 19 ---")
    print(f"Total de respondentes válidos: {total_validos_q19}")
    print(report_q2.to_string(index=False))
    
    # Export (Optional)
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULT_DIR = BASE_DIR / "files" / "qualitative_reports"
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    file_name_q18 = "frequencia_qualitativa_p18.csv"
    file_name_q19 = "frequencia_qualitativa_p19.csv"

    report_q1.to_csv(RESULT_DIR / file_name_q18, index=False)
    print(f"Exportado: {file_name_q18}")

    report_q2.to_csv(RESULT_DIR / file_name_q19, index=False)
    print(f"Exportado: {file_name_q19}")
    
    return report_q1, report_q2