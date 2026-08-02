from pathlib import Path

from src.chart_generator import generate_likert_scale_chart, read_file_to_df


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "files" / "answers.csv"

QUESTIONS = [
    (
        1,
        "Com que frequência o seu time de engenharia é forçado a assumir o desenvolvimento de requisitos para os quais ainda não possui o conhecimento técnico validado ou as habilidades necessárias mapeadas?",
    ),
    (
        2,
        "Com que frequência um prazo é prometido ao negócio ou cliente antes de a equipe de engenharia conseguir estimar se ele é viável?",
    ),
    (
        3,
        "Com que frequência a necessidade de grandes alterações arquiteturais ou a falta de componentes essenciais de software só é descoberta após o início oficial da codificação?",
    ),
    (
        4,
        "Com que frequência as dependências externas e integrações críticas (outros times, APIs, sistemas legados) são devidamente testadas e validadas pela engenharia antes do compromisso de entrega ser firmado com os stakeholders?",
    ),
    (
        5,
        "Com que frequência os requisitos não-funcionais (como limites de escalabilidade, performance e segurança) são discutidos e definidos junto com a área de produto logo na fase de concepção/ideação?",
    ),
    (
        6,
        "Com que frequência o time técnico consegue vetar ou pausar uma ideia baseando-se no alto custo de infraestrutura ou na inviabilidade operacional antes que ela vire um ticket fechado no backlog?",
    ),
    (
        7,
        "Com que frequência você recebe acesso a métricas, dados de uso ou feedbacks que comprovem se o código ou a funcionalidade que você entregou está gerando valor real para o usuário?",
    ),
    (
        8,
        "Com que frequência o seu time gasta alto esforço técnico (arquitetura, banco de dados, integrações) em funcionalidades que acabam tendo pouca ou nenhuma adoção pelos usuários finais após o lançamento?",
    ),
    (
        9,
        "Com que frequência a equipe técnica precisa refazer telas ou alterar o código porque o usuário final achou a funcionalidade confusa ou difícil de usar?",
    ),
    (
        10,
        "Com que frequência restrições críticas do negócio (como regras complexas de compliance, adequações à LGPD ou limites de orçamento) são descobertas de surpresa apenas nas fases de deploy ou produção?",
    ),
    (
        11,
        "Com que frequência você ou sua equipe sentem desmotivação ao desenvolver funcionalidades por não entenderem o propósito real ou o impacto de negócio que elas deveriam gerar?",
    ),
]


def run_all_charts() -> None:
	df = read_file_to_df(str(DATA_FILE))
	print(df.columns)
	print(df.head(5))
	print(df.describe())

	for question_number, column_name in QUESTIONS:
		generate_likert_scale_chart(
			df=df,
			column_name=column_name,
			question_number=question_number,
		)