import streamlit as st
import json
import os

st.title("🤖 IA que aprende")

arquivo = "memoria.json"

# carregar memória
if os.path.exists(arquivo):
    with open(arquivo, "r") as f:
        memoria = json.load(f)
else:
    memoria = {}

pergunta = st.text_input("Pergunte algo:")

def salvar():
    with open(arquivo, "w") as f:
        json.dump(memoria, f)

if pergunta:
    pergunta = pergunta.lower()

    if pergunta in memoria:
        st.success(memoria[pergunta])
    else:
        st.warning("Não sei responder isso ainda 😅")
        
        resposta_nova = st.text_input("Me ensina:")

        if st.button("Aprender"):
            memoria[pergunta] = resposta_nova
            salvar()
            st.success("Aprendi! 😎")
# carregar base fixa
if os.path.exists("base.json"):
    with open("base.json", "r") as f:
        base_fixa = json.load(f)
else:
    base_fixa = {}import json

def carregar_base():
    try:
        with open("base.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def responder(pergunta, base):
    pergunta = pergunta.lower().strip()

    # resposta exata
    if pergunta in base:
        return base[pergunta]

    # tentativa inteligente (palavra-chave)
    for chave in base:
        if chave in pergunta:
            return base[chave]

    return "Não sei ainda 😅, mas posso aprender!"def aprender(pergunta, resposta):
    base = carregar_base()
    base[pergunta] = resposta

    with open("base.json", "w", encoding="utf-8") as f:
        json.dump(base, f, indent=4, ensure_ascii=False)
