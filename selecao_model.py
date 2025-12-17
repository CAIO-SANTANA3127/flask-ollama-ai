import requests

OLLAMA_BASE = "http://localhost:11434"
MODELO_PADRAO = "llama3.2:1b"
MODELO_CONTEXTO_MAIOR = "llama3:instruct"  # precisa estar instalado

# =========================
# Utilidades
# =========================
def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except IOError as e:
        raise RuntimeError(f"Erro ao ler arquivo: {e}")

def contar_tokens(modelo, texto):
    payload = {
        "model": modelo,
        "prompt": texto
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE}/api/tokenize",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return len(response.json().get("tokens", []))

    except requests.exceptions.RequestException as e:
        print("⚠️ Não foi possível contar tokens via API:", e)
        print("Usando estimativa simples...")
        return int(len(texto.split()) * 1.3)

# =========================
# Prompts
# =========================
prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

Formato de saída:
cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("dados/lista_de_compras_100_clientes.csv")

# =========================
# 1️⃣ Contagem de tokens
# =========================
tokens_entrada = contar_tokens(
    MODELO_PADRAO,
    prompt_sistema + prompt_usuario
)

print(f"Número de tokens na entrada: {tokens_entrada}")

# =========================
# 2️⃣ Escolha dinâmica do modelo
# =========================
CONTEXTO_LLAMA3 = 8192
TAMANHO_ESPERADO_SAIDA = 2048

modelo_escolhido = MODELO_PADRAO

if tokens_entrada >= CONTEXTO_LLAMA3 - TAMANHO_ESPERADO_SAIDA:
    modelo_escolhido = MODELO_CONTEXTO_MAIOR

print(f"Modelo escolhido: {modelo_escolhido}")

# =========================
# 3️⃣ Chamada ao Ollama
# =========================
payload = {
    "model": modelo_escolhido,
    "messages": [
        {"role": "system", "content": prompt_sistema.strip()},
        {"role": "user", "content": prompt_usuario.strip()}
    ],
    "stream": False,
    "options": {
        "temperature": 0
    }
}

response = requests.post(
    f"{OLLAMA_BASE}/api/chat",
    json=payload,
    timeout=120
)
response.raise_for_status()

data = response.json()

print("\nResposta do modelo:\n")
print(data["message"]["content"])

print("\nUso de tokens:")
print("Tokens de entrada:", data.get("prompt_eval_count"))
print("Tokens de saída:", data.get("eval_count"))
