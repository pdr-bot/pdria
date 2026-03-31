import streamlit as st
import json
import os

st.set_page_config(page_title="IA que aprende", page_icon="🤖")

arquivo = "memoria.json"

# Carregar memória
if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    # Respostas pré-definidas
    memoria = {
        "olá": "Olá! Como posso ajudar?",
        "tudo bem?": "Tudo sim! E você?",
        "qual é seu nome?": "Eu sou uma IA que aprende com você!"
    }

# Função para salvar memória
def salvar():
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

# Inicializar session state
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "ensinar" not in st.session_state:
    st.session_state.ensinar = False
if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = ""

st.title("🤖 IA que aprende")

# Input principal
pergunta = st.text_input("Digite sua pergunta:")

def processar():
    pergunta_lower = pergunta.strip().lower()
    if pergunta_lower in memoria:
        st.session_state.resposta = memoria[pergunta_lower]
        st.session_state.ensinar = False
    else:
        st.session_state.resposta = f"Não sei responder '{pergunta}'. Me ensine!"
        st.session_state.ensinar = True
        st.session_state.pergunta_atual = pergunta_lower

if st.button("Enviar") and pergunta:
    processar()

# Se precisa ensinar a resposta
if st.session_state.ensinar:
    resposta_usuario = st.text_input(f"Qual seria a resposta correta para '{st.session_state.pergunta_atual}'?")
    if st.button("Salvar Resposta") and resposta_usuario:
        memoria[st.session_state.pergunta_atual] = resposta_usuario
        salvar()
        st.session_state.resposta = "Perfeito! Agora eu sei essa resposta."
        st.session_state.ensinar = False

# Mostrar resposta
if st.session_state.resposta:
    st.write(st.session_state.resposta)
