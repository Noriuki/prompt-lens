"""Base de conhecimento para RAG: boas práticas de prompts para LLMs."""

KNOWLEDGE_CHUNKS = [
    "Seja específico nas instruções. Em vez de 'escreva um texto', use 'escreva um parágrafo de 3 a 5 frases sobre X, em tom formal'.",
    "Inclua o papel ou persona do modelo quando fizer sentido: 'Você é um revisor técnico. Revise o seguinte código...'.",
    "Forneça exemplos do formato desejado (few-shot). Um exemplo de entrada e saída esperada aumenta muito a qualidade da resposta.",
    "Estruture o prompt em seções claras: Contexto, Instrução, Formato de saída, Restrições. Use títulos ou marcadores.",
    "Evite ambiguidade. Especifique se a resposta deve ser em português, o tamanho aproximado, e se há restrições (sem listas, sem código, etc.).",
    "Para tarefas longas, quebre em passos numerados. O modelo tende a seguir melhor uma sequência explícita.",
    "Se a resposta for técnica, defina termos ou convenções no início do prompt para alinhar o vocabulário.",
    "Peça que o modelo raciocine passo a passo quando a tarefa for complexa: 'Explique seu raciocínio antes de dar a resposta final'.",
    "Indique claramente o formato de saída: JSON, markdown, lista, parágrafo. Isso reduz erros de parsing.",
    "Revise prompts que falham: adicione mais contexto, exemplos ou restrinja o escopo em vez de apenas repetir.",
]
