import streamlit as st
import json
import os

st.title("🤖 IA que aprende")

# Arquivo que contém respostas pré-definidas
base_arquivo = "base.json"  # <- seu arquivo com respostas iniciais
memoria_arquivo = "memoria.json"  # <- arquivo que vai armazenar aprendizado novo

# Carregar base
if os.path.exists(base_arquivo):
    with open(base_arquivo, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    memoria = {}

# Carregar memória já aprendida, se existir
if os.path.exists(memoria_arquivo):
    with open(memoria_arquivo, "r", encoding="utf-8") as f:
        memoria_aprendida = json.load(f)
        memoria.update(memoria_aprendida)

# Função para salvar aprendizado novo
def salvar():
    with open(memoria_arquivo, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

# Session state
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "ensinar" not in st.session_state:
    st.session_state.ensinar = False
if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = ""

# Input
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

# Ensino de nova resposta
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
