import streamlit as st
from scripts import verificarAgenda, exibirJogos
import pandas as pd
import datetime

with st.sidebar:
    preco_limite = st.slider(min_value=0, value=20,max_value=250, step=10, label="Preço máximo") ##Cria um filtro para o preço máximo


st.title("Promoções da Nuuvem")
# Raspagem de dados e cronometro até a próxima raspagem
verificarAgenda("dados/nuuvem_agenda.txt", "scrapy crawl nuuvem_especiais")
# Exibição dos dados    
nuuvem = pd.read_json("dados/nuuvem.jsonl", lines=True) ##Lê o arquivo jsonl
filtro = st.text_input("Procure por um jogo") ##Cria um filtro para o nome do jogo
exibirJogos(nuuvem, preco_limite, filtro) ##Exibe os jogos de acordo com o filtro e o preço limite
