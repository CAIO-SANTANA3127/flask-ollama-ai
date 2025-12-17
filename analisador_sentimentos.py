import requests
import os
import re
import unicodedata

os.makedirs("./dados", exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2:1b"

def nome_arquivo_seguro(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except IOError:
        return None

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisador_sentimentos(produto):
    prompt_sistema = """
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.
    """

    arquivo_base = nome_arquivo_seguro(produto)
    prompt_usuario = carrega(f"./dados/avaliacoes-{arquivo_base}.txt")

    if not prompt_usuario:
        print(f"Avaliações não encontradas para: {produto}")
        return

    print(f"Iniciou a análise de sentimentos do produto: {produto}")

    payload = {
        "model": MODELO,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        texto_resposta = response.json()["message"]["content"]
        salva(f"./dados/analise-{arquivo_base}.txt", texto_resposta)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao comunicar com o Ollama: {e}")

lista_de_produtos = [
    "Camisetas de algodão orgânico",
    "Jeans feitos com materiais reciclados",
    "Maquiagem mineral"
]

for produto in lista_de_produtos:
    analisador_sentimentos(produto)
