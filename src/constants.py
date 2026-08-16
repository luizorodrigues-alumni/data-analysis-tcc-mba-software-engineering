
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
    'Você se lembra de algum projeto específico onde a falta de planejamento ou discovery gerou um débito técnico grave ou um retrabalho massivo? Se sentir confortável, descreva brevemente o que aconteceu (sem citar nomes de empresas).': {
        'question_number': 19,
        'question_type': 'text',
        'question_section': 'Business Risk',
    },

}

NUMBER_TO_QUESTIONS_MAP = {
    details['question_number']: question
    for question, details in QUESTIONS_MAP.items()
}

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

QUALITATIVE_CATEGORIES_PROMPT = """
Analise a resposta qualitativa abaixo e identifique todas as categorias de análise presentes.

A análise deve ser feita utilizando exclusivamente as definições operacionais apresentadas abaixo.

## Categorias e definições operacionais

1. debito_tecnico
Definição: Menção a acúmulo de problemas técnicos que aumentam o custo futuro de manutenção ou evolução do sistema/produto.

Exemplos de evidências:
- dívida técnica
- código difícil de manter
- necessidade futura de refatoração
- solução que dificulta evolução
- acúmulo de problemas técnicos decorrentes de decisões anteriores

Não classifique como debito_tecnico apenas porque a resposta menciona um problema técnico. Deve existir evidência de acúmulo, impacto futuro ou aumento do custo de manutenção/evolução.

2. retrabalho
Definição: Necessidade de refazer, alterar ou descartar trabalho que já havia sido realizado.

Exemplos de evidências:
- refazer uma solução
- alterar uma implementação já concluída
- reconstruir uma funcionalidade
- corrigir algo que poderia ter sido evitado anteriormente
- esforço desperdiçado devido a decisões ou requisitos anteriores

3. desalinhamento
Definição: Falta de alinhamento entre engenharia, produto, negócio, usuário, objetivos ou expectativas.

Exemplos de evidências:
- engenharia não compreender o objetivo do produto
- produto e engenharia possuírem expectativas diferentes
- requisitos não estarem alinhados
- falta de contexto de negócio para a engenharia
- solução não corresponder ao que o cliente/usuário esperava
- engenharia atuar apenas como executora de decisões tomadas por outras áreas

4. desmotivacao
Definição: Impactos sobre motivação, engajamento, pertencimento, voz ou retenção do time.

Exemplos de evidências:
- desmotivação
- sentimento de não ser ouvido
- sensação de falta de participação
- perda de engajamento
- sentimento de isolamento
- intenção de procurar outro emprego ou deixar a equipe
- desgaste emocional ou profissional decorrente da situação

Não classifique como desmotivacao apenas porque a situação é descrita como difícil ou problemática. Deve existir evidência de impacto sobre as pessoas ou sobre o time.

5. inviabilidade
Definição: Solução tecnicamente inviável, inadequada, mal dimensionada ou incompatível com restrições técnicas.

Exemplos de evidências:
- solução impossível ou inadequada tecnicamente
- arquitetura que não suporta a necessidade
- dimensionamento incorreto
- incompatibilidade com infraestrutura existente
- requisitos que não podem ser atendidos tecnicamente
- solução concebida sem considerar restrições técnicas relevantes

6. valor
Definição: Impacto sobre o valor percebido pelo usuário, cliente ou negócio, ou sobre a capacidade da solução de gerar valor.

Exemplos de evidências:
- cliente não percebe valor na funcionalidade
- funcionalidade não resolve o problema do usuário
- solução que não gera valor para o negócio
- feature que nasce sem utilidade
- esforço realizado sem retorno percebido
- produto que não atende à necessidade que deveria solucionar

7. qualidade
Definição: Impacto sobre qualidade, robustez, manutenção, confiabilidade ou qualidade da entrega/produto.

Exemplos de evidências:
- código menos robusto
- baixa qualidade da entrega
- problemas de confiabilidade
- código difícil de manter
- falhas em produção
- inconsistências
- solução de baixa qualidade
- redução da qualidade do produto final

## Regras de classificação

1. Uma resposta pode possuir zero, uma ou várias categorias.

2. Atribua uma categoria somente quando houver evidência textual suficiente na resposta para sustentá-la.

3. Não atribua uma categoria apenas porque ela poderia ser uma consequência lógica ou provável da situação descrita.

4. Diferencie evidência explícita de inferência:
   - Evidência explícita: a resposta afirma diretamente o problema ou impacto.
   - Inferência: o problema poderia ocorrer, mas não foi mencionado pelo respondente.
   
   Classifique somente quando houver evidência explícita ou uma relação diretamente sustentada pelo texto.

5. Uma mesma evidência pode justificar mais de uma categoria quando o trecho realmente apresentar múltiplos impactos.

6. Não tente forçar todas as respostas a possuírem uma categoria. Se nenhuma categoria estiver presente, retorne uma lista vazia.

7. A classificação deve considerar somente o conteúdo da resposta e o contexto da pergunta fornecida. Não utilize informações externas.

8. Preserve o sentido original da resposta. Não interprete além do que foi declarado pelo respondente.

9. Para cada categoria identificada, forneça um trecho literal da resposta que sirva como evidência da classificação.

10. Não invente ou parafraseie a evidência. O campo "evidencia" deve conter um trecho literal da resposta original.

11. Caso uma resposta mencione uma consequência sem deixar claro sua causa, classifique apenas a consequência efetivamente mencionada.

12. Em caso de dúvida entre atribuir ou não uma categoria, prefira NÃO atribuir a categoria. O objetivo é maximizar a precisão da codificação, evitando falsos positivos.

## Formato de saída

Retorne exclusivamente um JSON válido, sem texto adicional:

{{
  "categorias": [
    {{
      "categoria": "nome_do_codigo (ex: debito_tecnico, retrabalho, desalinhamento, desmotivacao, inviabilidade, valor, qualidade)",
      "evidencia": "trecho literal da resposta que justifica a classificação",
      "confianca": valor entre 0 e 1, representando o nível de confiança na classificação
    }}
  ]
}}

Se nenhuma categoria estiver presente:

{{
  "categorias": []
}}

## Pergunta

{pergunta}

## Resposta

{resposta}

"""