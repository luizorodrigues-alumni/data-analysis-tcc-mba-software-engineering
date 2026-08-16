from pathlib import Path

from src.constants import NUMBER_TO_QUESTIONS_MAP
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
    # 1. Definir as colunas de texto originais para saber quem respondeu
    q18_col = NUMBER_TO_QUESTIONS_MAP[18]
    q19_col = NUMBER_TO_QUESTIONS_MAP[19]
    
    # Lista base das categorias criadas manualmente
    base_categories = [
        'debito_tecnico', 'retrabalho', 'desalinhamento', 
        'desmotivação', 'inviabilidade', 'valor', 'qualidade'
    ]
    
    # Função interna para calcular as frequências de um grupo
    def calculate_frequencies(df_subset: pd.DataFrame, suffix: str, total_valid: int) -> pd.DataFrame:
        data = []
        for cat in base_categories:
            col_name = f"{cat}{suffix}"
            
            # Verifica se a coluna realmente existe no DataFrame
            if col_name in df_subset.columns:
                # Converte para int (caso esteja como True/False ou string '1'/'0') e soma
                count = df_subset[col_name].fillna(0).astype(int).sum()
                
                # Proteção contra divisão por zero
                percentage = (count / total_valid) * 100 if total_valid > 0 else 0
                
                # Formata o nome para o relatório (ex: 'debito_tecnico' -> 'Debito Tecnico')
                label = cat.replace('_', ' ').title()
                
                data.append({
                    'Categoria': label,
                    'Quantidade de Pessoas': count,
                    'Percentual (%)': round(percentage, 2)
                })
                
        # Ordena do maior percentual para o menor para facilitar a leitura
        report_df = pd.DataFrame(data).sort_values(by='Percentual (%)', ascending=False)
        return report_df

    # ==========================================
    # RELATÓRIO 1: Pergunta 18 (Impacto Negativo)
    # ==========================================
    # Filtra apenas quem escreveu mais de 5 caracteres
    mask_q18 = df[q18_col].notna() & (df[q18_col].astype(str).str.strip().str.len() > 5)
    df_q18_validos = df[mask_q18]
    total_validos_q18 = len(df_q18_validos)
    
    report_q1 = calculate_frequencies(df_q18_validos, '1', total_validos_q18)
    
    # ==========================================
    # RELATÓRIO 2: Pergunta 19 (Exemplo de Projeto)
    # ==========================================
    mask_q19 = df[q19_col].notna() & (df[q19_col].astype(str).str.strip().str.len() > 5)
    df_q19_validos = df[mask_q19]
    total_validos_q19 = len(df_q19_validos)
    
    report_q2 = calculate_frequencies(df_q19_validos, '2', total_validos_q19)

    # Exibe resumos no terminal
    print(f"--- Relatório Pergunta 18 ---")
    print(f"Total de respondentes válidos: {total_validos_q18}")
    print(report_q1.to_string(index=False))
    print("\n")
    
    print(f"--- Relatório Pergunta 19 ---")
    print(f"Total de respondentes válidos: {total_validos_q19}")
    print(report_q2.to_string(index=False))
    
    # Exportação (Opcional)
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