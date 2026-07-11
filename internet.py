from ddgs import DDGS

def pesquisar(pergunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(
                pergunta,
                region="br-pt",
                max_results=3
            ))

        if not resultados:
            return None

        resposta = ""
        for r in resultados:
            titulo = r['title']

            # remove sufixos comuns de wikipedia/enciclopédia no título
            for lixo in [
                " - Wikipédia, a enciclopédia livre",
                " - Wikipedia",
                " | Wikipédia",
            ]:
                titulo = titulo.replace(lixo, "")

            resposta += f"• {titulo}\n"
            resposta += f"{r['body']}\n\n"

        return resposta.strip()

    except Exception as e:
        print(f"Erro na pesquisa: {e}")
        return None
