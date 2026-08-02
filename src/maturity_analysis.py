from pathlib import Path

import pandas as pd

from src.chart_generator import read_file_to_df
from src.settings import questions_map


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "files" / "answers" / "answers.csv"
SUMMARY_FILE = BASE_DIR / "files" / "charts" / "maturity_levels_summary.csv"
HIGH_LIKERT_VALUES = {4, 5}
MATURITY_LEVELS_MAP = {
    1: {
        'label': 'Nível 1 - Orientado por intuição',
        'description': 'Execução top-down e sem processos de discovery',
        'questions': [7, 8, 9],
    },
    2: {
        'label': 'Nível 2 - Orientado por projetos',
        'description': 'Fábrica de features e ausência de roadmap compartilhado',
        'questions': [8, 14, 17],
    },
    3: {
        'label': 'Nível 3 - Orientado por clientes',
        'description': 'Reatividade e visão de curto prazo',
        'questions': [9, 15, 16],
    },
    4: {
        'label': 'Nível 4 - Orientado por oportunidades',
        'description': 'Priorização por oportunidade e validação de negócio',
        'questions': [11, 12, 10],
    },
    5: {
        'label': 'Nível 5 - Orientado por estratégia',
        'description': 'Colaboração irrestrita e acesso a dados sem fricção',
        'questions': [11, 12, 13],
    },
}
NUMBER_TO_QUESTION_MAP = {
    details['question_number']: question
    for question, details in questions_map.items()
}


def run_maturity_analysis_by_score() -> pd.DataFrame:
    df = read_file_to_df(DATA_FILE)
    
    # 1. Calcula o Score (Média) de cada Nível para cada respondente
    for level, meta in MATURITY_LEVELS_MAP.items():
        required_q_numbers = meta['questions']
        col_names = [NUMBER_TO_QUESTION_MAP[q_num] for q_num in required_q_numbers]
        
        # Converte as colunas para numérico (caso o pandas tenha lido como string)
        for col in col_names:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        col_score_name = f'score_nivel_{level}'
        # Tira a média das respostas daquele nível para cada linha
        df[col_score_name] = df[col_names].mean(axis=1)

    # 2. Define o Nível Predominante de cada pessoa
    def determine_predominant_level(row):
        # Cria um dicionário com os scores da pessoa: {1: 4.3, 2: 2.0, 3: 3.5...}
        scores = {level: row[f'score_nivel_{level}'] for level in MATURITY_LEVELS_MAP.keys()}
        
        # Descobre qual nível teve a maior nota
        max_level = max(scores, key=scores.get)
        max_score = scores[max_level]
        
        # Critério de corte: A média precisa ser pelo menos 3.5 para ser considerado "Maduro" naquele nível.
        # Se a maior nota da pessoa for 3.3, ela é "inconsistente" (Nível 0)
        if max_score >= 3.5:
            return max_level
        else:
            return 0  # Nível 0 - Ad-hoc / Inconsistente
            
    df['nivel_predominante'] = df.apply(determine_predominant_level, axis=1)

    # 3. Sumariza para ver quantas pessoas caíram em cada "caixote"
    level_counts = df['nivel_predominante'].value_counts().reset_index()
    level_counts.columns = ['Nível', 'Quantidade de Pessoas']
    
    # 4. Formata para o CSV final
    total_respondents = len(df)
    if total_respondents == 0:
        raise ValueError("Nenhum respondente encontrado. O arquivo CSV pode estar vazio ou mal formatado.")
    summary_data = []
    
    # Adiciona os níveis de 1 a 5
    for level, meta in MATURITY_LEVELS_MAP.items():
        count_series = level_counts[level_counts['Nível'] == level]['Quantidade de Pessoas']
        count = count_series.values[0] if not count_series.empty else 0
        percentage = (count / total_respondents) * 100 
        
        summary_data.append({
            'Nível': level,
            'Rótulo': meta['label'],
            'Quantidade de Pessoas': count,
            'Percentual (%)': round(percentage, 2)
        })
        
    # Adiciona a linha do Nível 0 (Não Classificados / Ad-hoc)
    count_0_series = level_counts[level_counts['Nível'] == 0]['Quantidade de Pessoas']
    count_0 = count_0_series.values[0] if not count_0_series.empty else 0
    percentage_0 = (count_0 / total_respondents) * 100 if total_respondents > 0 else 0
    
    summary_data.append({
        'Nível': 0,
        'Rótulo': 'Nível 0 - Inconsistente (Sem maturidade clara)',
        'Quantidade de Pessoas': count_0,
        'Percentual (%)': round(percentage_0, 2)
    })

    # Export
    summary_df = pd.DataFrame(summary_data)
    print("Maturity Analysis: \n", summary_df)
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(SUMMARY_FILE, index=False)
    
    return summary_df