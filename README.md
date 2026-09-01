# Análise de Dados do TCC - MBA em Engenharia de Software

Este projeto tem como objetivo analisar as respostas de um questionário de pesquisa acadêmica e transformar os dados em indicadores de maturidade, relatórios qualitativos e visualizações gráficas.

A finalidade principal é apoiar a pesquisa de TCC do programa de pós-graduação em MBA em Engenharia de Software, permitindo:

- identificar o nível de maturidade dos participantes;
- comparar maturidade por perfil, setor e experiência;
- analisar respostas qualitativas relacionadas a impactos e exemplos de projetos;
- gerar gráficos e relatórios em arquivos CSV e imagens.

---

## Objetivo do projeto

O código processa os dados de pesquisa e produz:

- análise de maturidade por nível;
- cruzamentos entre maturidade e perfil dos respondentes;
- relatórios de frequência para respostas qualitativas;
- gráficos de escala Likert;
- heatmaps para visualização comparativa.

---

## Estrutura do projeto

```text
data-analysis/
├── files/
│   ├── answers/
│   ├── likert_charts/
│   ├── maturity_analysis/
│   └── qualitative_reports/
├── src/
│   ├── chart_generator.py
│   ├── constants.py
│   ├── main.py
│   ├── maturity_analysis.py
│   ├── qualitative_analysis.py
│   ├── run_charts.py
│   └── data_treatment/
│       └── data_preprocessing.py
├── .gitignore
├── README.md
└── requirements.txt
```

> A pasta `files/` fica vazia no repositório e é usada para armazenar os arquivos exportados durante a execução do projeto. Ela está ignorada pelo Git para não versionar dados sensíveis ou gerados pela análise.

---

## Requisitos

O projeto utiliza Python com as bibliotecas:

- pandas
- matplotlib
- seaborn

---

## Como configurar o ambiente

No diretório do projeto, execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Como executar

A execução principal está em `src/main.py`.

```bash
cd data-analysis
source .venv/bin/activate
python src/main.py
```

Esse comando irá:

1. gerar gráficos de escala Likert;
2. calcular a maturidade dos respondentes;
3. criar cruzamentos por perfil;
4. gerar relatórios qualitativos;
5. exportar os arquivos para a pasta `files/`.

---

## Saídas geradas

Os dados e gráficos são salvos em diretórios dentro de `files/`, como:

- `files/maturity_analysis/`
- `files/qualitative_reports/`
- `files/likert_charts/`

Esses arquivos incluem:

- CSVs com resultados agregados;
- gráficos em PNG;
- relatórios de frequência e cruzamentos.

---

## Observações

- O projeto foi desenvolvido para análise de dados de pesquisa acadêmica.
- Os arquivos de entrada devem estar na pasta `files/answers/`.
- O ponto de entrada principal é `src/main.py`, que orquestra todo o fluxo de geração dos resultados.
- A pasta `files/` está no `.gitignore` para preservar a limpeza do repositório e evitar versionar dados de pesquisa gerados.

---
