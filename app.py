import streamlit as st
import json
import os
import time

st.set_page_config(
    page_title="IA que Aprende",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 IA que Aprende")
st.caption("Uma IA que aprende novas respostas com o usuário.")

base_arquivo = "base.json"
memoria_arquivo = "memoria.json"

# -------------------------
# Carregar memória
# -------------------------
if os.path.exists(base_arquivo):
    with open(base_arquivo, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    memoria = {}

if os.path.exists(memoria_arquivo):
    with open(memoria_arquivo, "r", encoding="utf-8") as f:
        memoria.update(json.load(f))

def salvar():
    with open(memoria_arquivo, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

# -------------------------
# Session State
# -------------------------
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "ensinar" not in st.session_state:
    st.session_state.ensinar = False

if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = ""

# -------------------------
# Histórico do Chat
# -------------------------
for msg in st.session_state.mensagens:
    with st.chat_message(msg["autor"]):
        st.write(msg["texto"])

# -------------------------
# Entrada do usuário
# -------------------------
pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:

    st.session_state.mensagens.append(
        {"autor": "user", "texto": pergunta}
    )

    pergunta_lower = pergunta.lower().strip()

    with st.spinner("Pensando..."):
        time.sleep(1)

        if pergunta_lower in memoria:

            resposta = memoria[pergunta_lower]

            st.session_state.mensagens.append(
                {"autor": "assistant", "texto": resposta}
            )

            st.rerun()

        else:

            resposta = "🤔 Ainda não sei responder isso.\n\nPode me ensinar?"

            st.session_state.mensagens.append(
                {"autor": "assistant", "texto": resposta}
            )

            st.session_state.ensinar = True
            st.session_state.pergunta_atual = pergunta_lower

            st.rerun()

# -------------------------
# Ensinar IA
# -------------------------
if st.session_state.ensinar:

    st.divider()

    st.subheader("📚 Ensinar IA")

    resposta_nova = st.text_input(
        "Digite a resposta correta:"
    )

    if st.button("Salvar Conhecimento"):

        memoria[st.session_state.pergunta_atual] = resposta_nova
        salvar()

        st.session_state.mensagens.append(
            {
                "autor": "assistant",
                "texto": "✅ Aprendi! Nunca mais vou esquecer essa resposta."
            }
        )

        st.session_state.ensinar = False

        st.rerun()
