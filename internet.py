from duckduckgo_search import DDGS

def pesquisar(pergunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pergunta, max_results=3))

        if not resultados:
            return None

        resposta = ""

        for r in resultados:
            resposta += f"• {r['title']}\n"
            resposta += f"{r['body']}\n\n"

        return resposta

    except:
        return None
