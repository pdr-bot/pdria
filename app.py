import streamlit as st
import json
import os
import time
from rapidfuzz import process, fuzz

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="IA que Aprende",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# ESTILO (deixa a interface mais bonita)
# =====================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f1116 0%, #1a1d29 100%);
    }
    section[data-testid="stSidebar"] {
        background-color: #161925;
        border-right: 1px solid #2a2d3a;
    }
    div[data-testid="stMetric"] {
        background-color: #1e2130;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 10px 14px;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 4px 8px;
    }
    h1 {
        background: linear-gradient(90deg, #7f5af0, #2cb67d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7f5af0, #2cb67d);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# ARQUIVOS
# =====================================

BASE_ARQUIVO = "base.json"
MEMORIA_ARQUIVO = "memoria.json"

# =====================================
# CARREGAR MEMÓRIA
# =====================================

memoria = {}

if os.path.exists(BASE_ARQUIVO):
    with open(BASE_ARQUIVO, "r", encoding="utf-8") as f:
        memoria.update(json.load(f))

if os.path.exists(MEMORIA_ARQUIVO):
    with open(MEMORIA_ARQUIVO, "r", encoding="utf-8") as f:
        memoria.update(json.load(f))


def salvar():
    with open(MEMORIA_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)


def procurar_resposta(pergunta):
    """Procura resposta exata primeiro, depois por similaridade (fuzzy)."""
    pergunta = pergunta.lower().strip()

    # Resposta exata
    if pergunta in memoria:
        return memoria[pergunta]

    if not memoria:
        return None

    # Procurar pergunta parecida
    resultado = process.extractOne(
        pergunta,
        memoria.keys(),
        scorer=fuzz.ratio
    )

    if resultado:
        pergunta_encontrada, similaridade, _ = resultado
        if similaridade >= 75:
            return memoria[pergunta_encontrada]

    return None


# =====================================
# SESSION STATE
# =====================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "ensinar" not in st.session_state:
    st.session_state.ensinar = False

if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = ""

if "aprendidos" not in st.session_state:
    st.session_state.aprendidos = 0


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🤖 IA que Aprende")

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Estatísticas")

st.sidebar.metric("Conhecimentos", len(memoria))
st.sidebar.metric("Mensagens", len(st.session_state.mensagens))
st.sidebar.metric("Aprendidos nesta sessão", st.session_state.aprendidos)

st.sidebar.markdown("---")

st.sidebar.subheader("🧠 Últimos conhecimentos")

ultimos = list(memoria.keys())[-5:]

if ultimos:
    for item in reversed(ultimos):
        st.sidebar.write("•", item)
else:
    st.sidebar.write("Nenhum conhecimento.")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Limpar conversa"):
    st.session_state.mensagens = []
    st.rerun()


# =====================================
# TÍTULO
# =====================================

st.title("🤖 IA que Aprende")

progresso = min(len(memoria) / 100, 1.0)

st.progress(progresso)

st.caption(f"{len(memoria)} conhecimentos aprendidos")


# =====================================
# HISTÓRICO
# =====================================

for msg in st.session_state.mensagens:
    with st.chat_message(msg["autor"]):
        st.write(msg["texto"])


# =====================================
# CHAT
# =====================================

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:

    st.session_state.mensagens.append(
        {
            "autor": "user",
            "texto": pergunta
        }
    )

    with st.spinner("Pensando..."):
        time.sleep(1)

        resposta = procurar_resposta(pergunta)

        if resposta is not None:

            st.session_state.mensagens.append(
                {
                    "autor": "assistant",
                    "texto": resposta
                }
            )

        else:

            st.session_state.mensagens.append(
                {
                    "autor": "assistant",
                    "texto": "🤔 Ainda não sei responder isso.\n\nPode me ensinar abaixo."
                }
            )

            st.session_state.ensinar = True
            st.session_state.pergunta_atual = pergunta.lower().strip()

    st.rerun()


# =====================================
# ENSINAR IA
# =====================================

if st.session_state.ensinar:

    st.divider()

    st.subheader("📚 Ensinar IA")
    st.caption(f"Pergunta: **{st.session_state.pergunta_atual}**")

    resposta_nova = st.text_input(
        "Digite a resposta correta:"
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        salvar_clicado = st.button("💾 Salvar Conhecimento")

    with col2:
        cancelar_clicado = st.button("❌ Cancelar")

    if salvar_clicado:

        if resposta_nova.strip():

            memoria[st.session_state.pergunta_atual] = resposta_nova
            salvar()

            st.session_state.aprendidos += 1

            st.session_state.mensagens.append(
                {
                    "autor": "assistant",
                    "texto": "✅ Aprendi! Obrigado por me ensinar."
                }
            )

            st.session_state.ensinar = False

            st.rerun()

        else:
            st.warning("Digite uma resposta antes de salvar.")

    if cancelar_clicado:
        st.session_state.ensinar = False
        st.rerun()
