
QUESTIONS_MAP= {
    'Em qual Região você atua hoje?': {
        'question_number': 1,
        'question_type': 'multiple_choice',
        'question_section': 'Profile Mapping',
    },
    'Qual seu papel atualmente?' : {
        'question_number': 2,
        'question_type': 'multiple_choice',
        'question_section': 'Profile Mapping',
    },
    'Caso tenha escolhido "Outro" na pergunta anterior, informe abaixo o papel correto.': {
        'question_number': 3,
        'question_type': 'text',
        'question_section': 'Profile Mapping',
    },
    'Qual seu nível de Experiência?': {
        'question_number': 4,
        'question_type': 'multiple_choice',
        'question_section': 'Profile Mapping',
    },
    'Em qual setor principal atua a empresa em que você trabalha atualmente?': {
        'question_number': 5,
        'question_type': 'multiple_choice',
        'question_section': 'Profile Mapping',
    },
    'Caso tenha escolhido "Outro" na pergunta anterior, informe abaixo o setor correto.': {
        'question_number': 6,
        'question_type': 'text',
        'question_section': 'Profile Mapping',
    },
    'Com que frequência o seu time de engenharia é forçado a assumir o desenvolvimento de requisitos para os quais ainda não possui o conhecimento técnico validado ou as habilidades necessárias mapeadas?': {
        'question_number': 7,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência um prazo é prometido ao negócio ou cliente antes de a equipe de engenharia conseguir estimar se ele é viável?': {
        'question_number': 8,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência a necessidade de grandes alterações arquiteturais ou a falta de componentes essenciais de software só é descoberta após o início oficial da codificação?': {
        'question_number': 9,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência as dependências externas e integrações críticas (outros times, APIs, sistemas legados) são devidamente testadas e validadas pela engenharia antes do compromisso de entrega ser firmado com os stakeholders?': {
        'question_number': 10,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência os requisitos não-funcionais (como limites de escalabilidade, performance e segurança) são discutidos e definidos junto com a área de produto logo na fase de concepção/ideação?': {
        'question_number': 11,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência o time técnico consegue vetar ou pausar uma ideia baseando-se no alto custo de infraestrutura ou na inviabilidade operacional antes que ela vire um ticket fechado no backlog?': {
        'question_number': 12,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência você recebe acesso a métricas, dados de uso ou feedbacks que comprovem se o código ou a funcionalidade que você entregou está gerando valor real para o usuário?': {
        'question_number': 13,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência o seu time gasta alto esforço técnico (arquitetura, banco de dados, integrações) em funcionalidades que acabam tendo pouca ou nenhuma adoção pelos usuários finais após o lançamento?': {
        'question_number': 14,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência a equipe técnica precisa refazer telas ou alterar o código porque o usuário final achou a funcionalidade confusa ou difícil de usar?': {
        'question_number': 15,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência restrições críticas do negócio (como regras complexas de compliance, adequações à LGPD ou limites de orçamento) são descobertas de surpresa apenas nas fases de deploy ou produção?': {
        'question_number': 16,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Com que frequência você ou sua equipe sentem desmotivação ao desenvolver funcionalidades por não entenderem o propósito real ou o impacto de negócio que elas deveriam gerar?': {
        'question_number': 17,
        'question_type': 'likert_scale',
        'question_section': 'Business Risk',
    },
    'Em sua experiência prática, qual é o maior impacto negativo (seja na arquitetura, na qualidade do código ou na motivação do time) quando a engenharia não participa das etapas iniciais da concepção das soluções?': {
        'question_number': 18,
        'question_type': 'text',
        'question_section': 'Business Risk',
    },
    'Toda a minha experiência na área de "produtos" da minha atual empresa foi marcada negativamente por todas as questões deste formulário; absolutamente tudo aconteceu e os impactos foram muito ruins; sinceramente não conheço uma pessoa que não acredite que não tenha passado pela cabeça procurar outro emprego, migrar de área, buscar outros projetos para não ter que ficar na mesma área. É algo que nem sempre é falado explicitamente mas o "clima" é subentendido na equipe toda.': {
        'question_number': 19,
        'question_type': 'text',
        'question_section': 'Business Risk',
    },

}

NUMBER_TO_QUESTIONS_MAP = {
    details['question_number']: question
    for question, details in QUESTIONS_MAP.items()
}