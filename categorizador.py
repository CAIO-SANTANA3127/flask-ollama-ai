import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2:1b"  # pode trocar por mistral, phi3, etc.


def categoriza_produto(nome_produto, lista_categorias_possiveis):
    categorias_formatadas = [c.strip() for c in lista_categorias_possiveis.split(",")]

    prompt_sistema = f"""
            Você é um categorizador de produtos EXTREMAMENTE RESTRITO.

            REGRAS OBRIGATÓRIAS:
            - Você DEVE escolher UMA categoria EXATAMENTE igual a uma das categorias abaixo
            - NÃO invente categorias
            - NÃO explique
            - NÃO use texto adicional
            - Se o produto não se encaixar, escolha a categoria MAIS PRÓXIMA

            CATEGORIAS VÁLIDAS (use exatamente como está):
            {", ".join([c.strip() for c in lista_categorias_possiveis.split(",")])}

            FORMATO DE SAÍDA (OBRIGATÓRIO):
            Categoria: <nome exato da categoria>
            """

    payload = {
        "model": MODELO,
        "messages": [
            {
                "role": "system",
                "content": prompt_sistema.strip()
            },
            {
                "role": "user",
                "content": nome_produto
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    return response.json()["message"]["content"]


# ========= EXECUÇÃO =========

categorias_validas = input("Informe as categorias válidas (separadas por vírgula): ")

while True:
    nome_produto = input("Digite o nome do produto (ENTER para sair): ").strip()
    if not nome_produto:
        break

    try:
        texto_resposta = categoriza_produto(nome_produto, categorias_validas)
        print("\n" + texto_resposta + "\n")
    except Exception as e:
        print(f"Erro ao categorizar produto: {e}")
