from ddgs import DDGS
import streamlit as st
from groq import Groq


def buscar_bruto(pergunta):
    """Busca resultados crus no DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(
                pergunta,
                region="br-pt",
                max_results=3
            ))

        if not resultados:
            return None

        texto_bruto = ""
        for r in resultados:
            titulo = r['title']
            for lixo in [
                " - Wikipédia, a enciclopédia livre",
                " - Wikipedia",
                " | Wikipédia",
            ]:
                titulo = titulo.replace(lixo, "")

            texto_bruto += f"Fonte: {titulo}\n{r['body']}\n\n"

        return texto_bruto.strip()

    except Exception as e:
        print(f"Erro na busca: {e}")
        return None


def reescrever_com_voz_eva(pergunta, texto_bruto):
    """Usa a API gratuita da Groq (Llama) para reescrever os
    resultados num texto único, natural, na voz da EVA."""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        prompt = f"""Você é a EVA, uma assistente virtual brasileira descontraída, simpática e direta.

Alguém te perguntou: "{pergunta}"

Você encontrou estas informações em uma busca na internet:

{texto_bruto}

Reescreva isso como se VOCÊ já soubesse a resposta, num texto corrido e natural (não use bullet points, não cite as fontes, não repita a mesma informação duas vezes). Seja direta, use no máximo 3-4 frases, e pode usar um emoji se fizer sentido. Não invente nada que não esteja nas informações acima. Responda em português do Brasil."""

        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print(f"Erro ao reescrever com IA: {e}")
        return None


def pesquisar(pergunta):
    """Busca na internet e reescreve o resultado na voz da EVA.
    Se a reescrita falhar por qualquer motivo, cai no texto bruto
    como plano B, pra nunca deixar o usuário sem resposta."""
    texto_bruto = buscar_bruto(pergunta)

    if not texto_bruto:
        return None

    resposta_reescrita = reescrever_com_voz_eva(pergunta, texto_bruto)

    if resposta_reescrita:
        return resposta_reescrita

    # plano B: se a IA falhar (sem chave, rate limit, etc.),
    # ainda devolve algo útil em vez de travar
    return texto_bruto
