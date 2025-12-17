import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2:1b"  # mistral, phi3, etc.

payload = {
    "model": MODELO,
    "messages": [
        {
            "role": "system",
            "content": "Liste apenas os nomes dos produtos, sem considerar descrição."
        },
        {
            "role": "user",
            "content": "Liste 3 produtos sustentáveis"
        }
    ],
    "stream": False,
    "options": {
        "temperature": 0
    }
}

try:
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )
    response.raise_for_status()

    data = response.json()

    # Conteúdo gerado pelo modelo
    print("Resposta do modelo:\n")
    print(data["message"]["content"])

    # Tokens usados (opcional, mas recomendado)
    print("\nUso de tokens:")
    print("Tokens de entrada:", data.get("prompt_eval_count"))
    print("Tokens de saída:", data.get("eval_count"))

except requests.exceptions.RequestException as e:
    print("Erro ao comunicar com o Ollama:", e)
