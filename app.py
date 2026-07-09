import streamlit as st
import json
import os
import time
import random
import difflib

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="EVA - Assistente Virtual Evolutiva",
    page_icon="🧬",
    layout="wide"
)

NOME_IA = "EVA"
AVATAR_IA = "🧬"
AVATAR_USER = "🙂"

# =====================================
# ESTILO
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
    .confianca-badge {
        display: inline-block;
        font-size: 0.75rem;
        padding: 2px 10px;
        border-radius: 999px;
        margin-top: 4px;
        background-color: #2a2d3a;
        color: #b8bcc8;
    }
    .copiar-btn {
        background-color: #1e2130;
        color: #b8bcc8;
        border: 1px solid #2a2d3a;
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 0.72rem;
        cursor: pointer;
        margin-top: 6px;
    }
    .copiar-btn:hover {
        background-color: #2a2d3a;
        color: #ffffff;
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
    """Procura resposta exata primeiro, depois por similaridade (fuzzy).
    Retorna (resposta, tipo, score) onde tipo é 'exata' ou 'aproximada'."""
    pergunta = pergunta.lower().strip()

    if pergunta in memoria:
        return memoria[pergunta], "exata", 1.0

    if not memoria:
        return None, None, 0.0

    candidatos = difflib.get_close_matches(
        pergunta,
        memoria.keys(),
        n=1,
        cutoff=0.75
    )

    if candidatos:
        score = difflib.SequenceMatcher(None, pergunta, candidatos[0]).ratio()
        return memoria[candidatos[0]], "aproximada", score

    return None, None, 0.0

# Perguntas sugeridas para quem não sabe por onde começar
SUGESTOES = [
    "oi",
    "qual a capital do brasil",
    "quanto é 7x7",
    "receita de brigadeiro",
    "quem foi ronnie coleman",
    "por que o céu é azul",
]


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

if "nao_soube" not in st.session_state:
    st.session_state.nao_soube = 0

if "pergunta_pendente" not in st.session_state:
    st.session_state.pergunta_pendente = None


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title(f"{AVATAR_IA} {NOME_IA}")
st.sidebar.caption("Assistente Virtual Evolutiva")

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Estatísticas")

col_a, col_b = st.sidebar.columns(2)
col_a.metric("Conhecimentos", len(memoria))
col_b.metric("Mensagens", len(st.session_state.mensagens))

col_c, col_d = st.sidebar.columns(2)
col_c.metric("Aprendidos", st.session_state.aprendidos)
col_d.metric("Não soube", st.session_state.nao_soube)

st.sidebar.markdown("---")

st.sidebar.subheader("🔍 Buscar na memória")
busca = st.sidebar.text_input("Digite um termo...", label_visibility="collapsed", placeholder="Ex: futebol, receita, brasil...")

if busca.strip():
    encontrados = [k for k in memoria.keys() if busca.lower().strip() in k.lower()][:8]
    if encontrados:
        for item in encontrados:
            with st.sidebar.expander(f"💬 {item}"):
                st.write(memoria[item])
    else:
        st.sidebar.caption("Nada encontrado com esse termo.")
else:
    st.sidebar.subheader("🧠 Últimos conhecimentos")
    ultimos = list(memoria.keys())[-5:]
    if ultimos:
        for item in reversed(ultimos):
            st.sidebar.write("•", item)
    else:
        st.sidebar.write("Nenhum conhecimento.")

st.sidebar.markdown("---")

col_e, col_f = st.sidebar.columns(2)

with col_e:
    if st.button("🗑 Limpar chat"):
        st.session_state.mensagens = []
        st.rerun()

with col_f:
    st.download_button(
        "⬇️ Exportar",
        data=json.dumps(memoria, ensure_ascii=False, indent=4),
        file_name="memoria_eva.json",
        mime="application/json",
        use_container_width=True
    )


# =====================================
# TÍTULO
# =====================================

st.title(f"{AVATAR_IA} {NOME_IA}")
st.caption("Assistente Virtual Evolutiva — aprende com cada conversa")

progresso = min(len(memoria) / 400, 1.0)
st.progress(progresso)
st.caption(f"{len(memoria)} conhecimentos na base")


# =====================================
# MENSAGEM DE BOAS-VINDAS + SUGESTÕES
# =====================================

if not st.session_state.mensagens:
    st.info(f"👋 Oi! Eu sou a **{NOME_IA}**. Pode me perguntar qualquer coisa, ou clicar em uma sugestão abaixo pra começar:")

    cols = st.columns(3)
    for i, sugestao in enumerate(SUGESTOES):
        with cols[i % 3]:
            if st.button(sugestao, key=f"sugestao_{i}", use_container_width=True):
                st.session_state.pergunta_pendente = sugestao


# =====================================
# HISTÓRICO
# =====================================

for idx, msg in enumerate(st.session_state.mensagens):
    avatar = AVATAR_IA if msg["autor"] == "assistant" else AVATAR_USER
    with st.chat_message(msg["autor"], avatar=avatar):
        st.write(msg["texto"])
        if msg.get("badge"):
            st.markdown(f'<span class="confianca-badge">{msg["badge"]}</span>', unsafe_allow_html=True)
        if msg["autor"] == "assistant":

# =====================================
# CHAT
# =====================================

pergunta_digitada = st.chat_input(f"Digite sua pergunta para a {NOME_IA}...")

pergunta = pergunta_digitada or st.session_state.pergunta_pendente
st.session_state.pergunta_pendente = None

if pergunta:

    st.session_state.mensagens.append(
        {
            "autor": "user",
            "texto": pergunta
        }
    )

    with st.chat_message("user", avatar=AVATAR_USER):
        st.write(pergunta)

    with st.chat_message("assistant", avatar=AVATAR_IA):
        placeholder = st.empty()

        with st.spinner(f"{NOME_IA} está pensando..."):
            time.sleep(0.5)
            resposta, tipo, score = procurar_resposta(pergunta)

        badge = None

        if resposta is not None:
            texto_final = resposta
            if tipo == "aproximada":
                badge = f"🔎 correspondência aproximada ({int(score * 100)}% de similaridade)"
        else:
            st.session_state.nao_soube += 1
            st.session_state.ensinar = True
            st.session_state.pergunta_atual = pergunta.lower().strip()
            texto_final = "🤔 Ainda não sei responder isso.\n\nPode me ensinar abaixo, assim eu evoluo!"

        # Efeito de digitação, letra por letra
        texto_exibido = ""
        for char in texto_final:
            texto_exibido += char
            placeholder.markdown(texto_exibido)
            time.sleep(0.012)

        if badge:
            st.markdown(f'<span class="confianca-badge">{badge}</span>', unsafe_allow_html=True)

    st.session_state.mensagens.append(
        {
            "autor": "assistant",
            "texto": texto_final,
            "badge": badge
        }
    )

    st.rerun()


# =====================================
# ENSINAR A EVA
# =====================================

if st.session_state.ensinar:

    st.divider()

    st.subheader(f"📚 Ensinar a {NOME_IA}")
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
                    "texto": "✅ Aprendi! Obrigado por me ajudar a evoluir."
                }
            )

            st.session_state.ensinar = False

            st.rerun()

        else:
            st.warning("Digite uma resposta antes de salvar.")

    if cancelar_clicado:
        st.session_state.ensinar = False
        st.rerun()
