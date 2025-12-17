import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.2:1b",
        "messages": [
            {"role": "user", "content": "Explique o que é IA"}
        ],
        "stream": False
    }
)

response.raise_for_status()
data = response.json()

print("Tokens de entrada:", data["prompt_eval_count"])
print("Tokens de saída:", data["eval_count"])
print("Total:", data["prompt_eval_count"] + data["eval_count"])
