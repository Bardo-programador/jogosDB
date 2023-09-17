import streamlit as st
from scripts import verificarAgenda, exibirJogos
import pandas as pd
st.title("Promoções da GOG")
verificarAgenda("dados/gog_agenda.txt", "scrapy crawl gog_especiais")
with st.sidebar:
    preco_limite = st.slider(min_value=0, max_value=250, value=20, step=10, label="Preço máximo") ##Cria um filtro para o preço máximo

gog = pd.read_json("dados/gog.jsonl", lines=True)
filtro = st.text_input("Procure por um jogo") ##Cria um filtro para o nome do jogo
exibirJogos(gog, preco_limite, filtro)