import httpx
import json
import os
from dotenv import load_dotenv
from ia.schemas import InsightResponse
from ia.prompt import SYSTEM_PROMPT, montar_prompt

# carrega as variáveis do arquivo .env
load_dotenv()

# pega as chaves uma vez só no início — se não existir no .env quebra aqui com erro claro
NVIDIA_API_KEY = os.environ["NVIDIA_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# configurações de cada provider — só URL e modelo, chave já tá nas variáveis acima
PROVIDERS = {
    "kimi": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model": "moonshotai/kimi-k2",
    },
    "claude": {
        "base_url": "https://api.anthropic.com/v1",
        "model": "claude-sonnet-4-20250514",
    },
}


def _chamar_kimi(cfg: dict, user_prompt: str) -> str:
    resp = httpx.post(
        f"{cfg['base_url']}/chat/completions",
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": cfg["model"],
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            # temperature baixa porque você quer respostas precisas, não criativas
            "temperature": 0.3,
            "max_tokens": 1024,
        },
        # timeout pra não ficar esperando eternamente se a API travar
        timeout=30,
    )

    # transforma erros HTTP (400, 500) em exceções Python
    resp.raise_for_status()

    # padrão OpenAI — resposta vem em choices[0].message.content
    return resp.json()["choices"][0]["message"]["content"]


def _chamar_claude(cfg: dict, user_prompt: str) -> str:
    resp = httpx.post(
        f"{cfg['base_url']}/messages",
        headers={
            # Anthropic usa x-api-key em vez de Authorization: Bearer
            "x-api-key": ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            # Anthropic exige esse header pra controle de versão da API
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": cfg["model"],
            # Anthropic separa o system do messages — não fica dentro da lista
            "system": SYSTEM_PROMPT,
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
        },
        timeout=30,
    )

    resp.raise_for_status()

    # padrão Anthropic — resposta vem em content[0].text
    return resp.json()["content"][0]["text"]


def gerar_insights(kpis: dict, cotacoes: dict, provider: str = "kimi") -> InsightResponse:
    # monta o texto com os dados financeiros que vai ser enviado pra IA
    prompt = montar_prompt(kpis, cotacoes)

    # decide qual provider usar — kimi é gratuito e padrão, claude só pra premium
    if provider == "claude":
        raw = _chamar_claude(PROVIDERS["claude"], prompt)
    else:
        raw = _chamar_kimi(PROVIDERS["kimi"], prompt)

    # a IA às vezes envolve o JSON em ```json ... ``` — isso remove
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    # converte o texto JSON em dicionário Python
    dados = json.loads(raw)

    # valida com o schema — se faltar campo ou tipo errado, Pydantic joga erro claro
    return InsightResponse(**dados)