import streamlit as st
from sklearn.linear_model import LinearRegression

x = [[1], [2], [3], [4], [5]]
y = [2, 4, 5, 8, 10]

modelo = LinearRegression()
modelo.fit(x, y)

st.title("IA de previsão de nota")

horas = st.slider("Horas de estudo", 0, 10)

if st.button("Prever"):
    resultado = modelo.predict([[horas]])
    st.write(f"Nota prevista: {resultado[0]:.2f}")
import streamlit as st
import json
import os

st.title("🤖 IA que aprende - Pedro")

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
    base_fixa = {}
