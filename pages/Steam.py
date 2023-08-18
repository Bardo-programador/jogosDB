import streamlit as st
import pandas as pd
from scrapy import cmdline
from scripts import run
# Configurar o Streamlit

st.title("Promoções da Steam")

# Executar a raspagem ao clicar no botão
run('scrapy crawl steam_especiais')
steam = pd.read_json("dados/steam.jsonl", lines=True)

##Exibir os dados

st.markdown("## Lista de jogos em promoção da Steam")
for index, row in steam.iterrows():
    nome = row['name'][0] # Como o nome é uma lista, pegamos o primeiro elemento
    preco = row['price'][0] # Como o preço é uma lista, pegamos o primeiro elemento
    link = row['link'] # O link não é uma lista, então não precisamos pegar o primeiro elemento
    st.markdown(f"- [{nome}]({link}) - USD$ {preco}") # Exibimos o nome, o link e o preço formatado em MarkDown
