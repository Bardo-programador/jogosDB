import streamlit as st
import pandas as pd
from scrapy import cmdline
from scripts import run
# Configurar o Streamlit

st.title("Promoções da Steam")

# Executar a raspagem 
with st.spinner("Atualizando"):
    run('scrapy crawl steam_especiais')
steam = pd.read_json("dados/steam.jsonl", lines=True)

##Exibir os dados
filtro = st.text_input("Procure por um jogo") ##Cria um filtro para o nome do jogo
st.markdown("## Lista de jogos em promoção da Steam")
for index, row in steam.iterrows():
    nome_minusculo = row['name'][0].lower() ##Transforma o nome do jogo em minusculo
    if nome_minusculo.find(filtro.lower()) != -1:
        nome = row['name'][0] # Como o nome é uma lista, pegamos o primeiro elemento
        preco = row['price'][0] # Como o preço é uma lista, pegamos o primeiro elemento
        link = row['link'] # O link não é uma lista, então não precisamos pegar o primeiro elemento
        st.markdown(f"- [{nome}]({link}) - USD$ {preco}") # Exibimos o nome, o link e o preço formatado em MarkDown
