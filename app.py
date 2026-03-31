import streamlit as st
import json
import os

st.title("🤖 IA que aprende")

arquivo = "memoria.json"

# Carregar memória
if os.path.exists(arquivo):
    with open(arquivo, "r") as f:
        memoria = json.load(f)
else:
    memoria = {
        "olá": "Olá! Como posso ajudar?",
        "tudo bem?": "Tudo sim! E você?",
        "qual é seu nome?": "Eu sou uma IA que aprende com você!"
    }

# Função para salvar memória
def salvar():
    with open(arquivo, "w") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

# Entrada do usuário
pergunta = st.text_input("Pergunte algo:")

if pergunta:
    pergunta_lower = pergunta.lower()
    
    # Verifica se já existe resposta
    if pergunta_lower in memoria:
        st.write(memoria[pergunta_lower])
    else:
        # Se não existe, pede para usuário fornecer a resposta
        resposta = st.text_input(f"Não sei responder '{pergunta}'. Qual seria a resposta correta?")
        if resposta:
            memoria[pergunta_lower] = resposta
            salvar()
            st.write("Perfeito! Agora eu sei essa resposta.")
