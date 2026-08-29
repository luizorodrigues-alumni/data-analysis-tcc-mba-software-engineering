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

    # Display summaries in the terminal
    print(f"--- Report Question 18 ---")
    print(f"Total valid respondents: {total_validos_q18}")
    print(report_q1.to_string(index=False))
    print("\n")
    
    print(f"--- Report Question 19 ---")
    print(f"Total valid respondents: {total_validos_q19}")
    print(report_q2.to_string(index=False))
    
    # Export (Optional)
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULT_DIR = BASE_DIR / "files" / "qualitative_reports"
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    file_name_q18 = "frequencia_qualitativa_p18.csv"
    file_name_q19 = "frequencia_qualitativa_p19.csv"

    report_q1.to_csv(RESULT_DIR / file_name_q18, index=False)
    print(f"Exported: {file_name_q18}")

    report_q2.to_csv(RESULT_DIR / file_name_q19, index=False)
    print(f"Exported: {file_name_q19}")
    
    return report_q1, report_q2


def generate_maturity_vs_qualitative_cross_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correlates the maturity level (nivel_predominante_mediana) with consolidated 
    qualitative categories (questions 18 and 19 combined).
    
    Args:
        df (pd.DataFrame): The DataFrame containing responses and already-marked categories.
    Returns:
        pd.DataFrame: DataFrame with cross-tabulation (frequency in % per level).
    """
    q18_col = NUMBER_TO_QUESTIONS_MAP[18]
    q19_col = NUMBER_TO_QUESTIONS_MAP[19]
    
    base_categories = [
        'debito_tecnico', 'retrabalho', 'desalinhamento', 
        'desmotivação', 'inviabilidade', 'valor', 'qualidade'
    ]
    
    # 1. Filter for valid respondents
    # A respondent is considered valid for this analysis if they answered Q18 OR Q19
    mask_q18 = df[q18_col].notna() & (df[q18_col].astype(str).str.strip().str.len() > 5)
    mask_q19 = df[q19_col].notna() & (df[q19_col].astype(str).str.strip().str.len() > 5)
    
    valid_mask = mask_q18 | mask_q19
    df_valid = df[valid_mask].copy()
    
    # 2. Consolidation of categories (Multi-label)
    # If the person marked True in 1 OR in 2, the consolidated will be True
    consolidated_cols = []
    for cat in base_categories:
        col1 = f"{cat}1"
        col2 = f"{cat}2"
        
        # Pulls data safely, converting to boolean
        val1 = df_valid[col1].fillna(0).astype(bool) if col1 in df_valid.columns else False
        val2 = df_valid[col2].fillna(0).astype(bool) if col2 in df_valid.columns else False
        
        consolidated_col = f"{cat}_consolidado"
        df_valid[consolidated_col] = val1 | val2
        consolidated_cols.append(consolidated_col)
        
    # 3. Cross-Tabulation (Cross-Analysis)
    # Group by median maturity level
    grouped = df_valid.groupby('nivel_predominante_mediana')
    
    # Since the consolidated columns are boolean (True=1, False=0), 
    # mean * 100 gives us exactly the percentage of incidence per level!
    cross_analysis = grouped[consolidated_cols].mean() * 100
    
    # Count how many valid respondents fall into each level
    cross_analysis['Total de Respondentes'] = grouped.size()
    
    # 4. Formatting and Cleanup for Final Report
    cross_analysis = cross_analysis.round(2).reset_index()
    
    # Rename columns from "debito_tecnico_consolidado" to "Debito Tecnico"
    rename_map = {f"{cat}_consolidado": cat.replace('_', ' ').title() for cat in base_categories}
    cross_analysis = cross_analysis.rename(columns=rename_map)
    
    # Reorder columns to place "Total" right after "Level"
    final_cols = ['nivel_predominante_mediana', 'Total de Respondentes'] + list(rename_map.values())
    cross_analysis = cross_analysis[final_cols]
    
    # Display in terminal
    print("--- Cross-Analysis: Maturity vs Qualitative (Consolidated) ---")
    print(cross_analysis.to_string(index=False))
    print("\n")
    
    # 5. Export
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULT_DIR = BASE_DIR / "files" / "qualitative_reports"
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    file_name = "crosstab_maturidade_vs_qualitativo_consolidado.csv"
    cross_analysis.to_csv(RESULT_DIR / file_name, index=False)
    print(f"Exported: {file_name}")
    
    return cross_analysis


def run_qualitative_analysis(df: pd.DataFrame) -> None:
    """
    Runs the qualitative analysis, generating reports for questions 18 and 19,
    and performing a cross-analysis with maturity levels.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the survey responses.
    Returns:
        None
    """
    # Generate qualitative reports for questions 18 and 19
    generate_qualitative_reports(df)
    
    # Generate cross-analysis between maturity levels and qualitative categories
    generate_maturity_vs_qualitative_cross_analysis(df)