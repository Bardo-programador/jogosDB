import streamlit as st
import pandas as pd
from scrapy import cmdline
from scripts import verificarAgenda, exibirJogos
# Configurar o Streamlit

st.title("Promoções da Steam")

# Executar a raspagem 
verificarAgenda("dados/steam_agenda.txt", "scrapy crawl steam_especiais")
with st.sidebar:
    preco_limite = st.slider(min_value=0, max_value=250, value=20, step=10, label="Preço máximo") ##Cria um filtro para o preço máximo

steam = pd.read_json("dados/steam.jsonl", lines=True)
##Exibir os dados
filtro = st.text_input("Procure por um jogo") ##Cria um filtro para o nome do jogo
exibirJogos(steam, preco_limite, filtro) ##Exibe os jogos de acordo com o filtro e o preço limite