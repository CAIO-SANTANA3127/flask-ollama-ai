import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2:1b"

payload = {
    "model": MODELO,
    "messages": [
        {
            "role": "system",
            "content": "Classifique o produto abaixo em uma das categorias: Higiene Pessoal, Moda ou Casa e dê uma descrição da categoria."
        },
        {
            "role": "user",
            "content": "Escovas de dentes"
        }
    ],
    "stream": False
}

response = requests.post(OLLAMA_URL, json=payload)
response.raise_for_status()

print(response.json()["message"]["content"])
