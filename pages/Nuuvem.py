import streamlit as st
from scripts import verificarAgenda
import pandas as pd
import datetime

st.title("Promoções da Nuuvem")
# Raspagem de dados e cronometro até a próxima raspagem
verificarAgenda("dados/nuuvem_agenda.txt", "scrapy crawl nuuvem_especiais")
# Exibição dos dados    
nuuvem = pd.read_json("dados/nuuvem.jsonl", lines=True) ##Lê o arquivo jsonl
filtro = st.text_input("Procure por um jogo") ##Cria um filtro para o nome do jogo
for index, row in nuuvem.iterrows():
    nome_minusculo = row['name'].lower() ##Transforma o nome do jogo em minusculo
    if nome_minusculo.find(filtro.lower()) != -1:
        nome = row['name'] # Como o nome é uma lista, pegamos o primeiro elemento
        preco = row['price'] # Como o preço é uma lista, pegamos o primeiro elemento
        link = row['link'] # O link não é uma lista, então não precisamos pegar o primeiro elemento
        st.markdown(f"- [{nome}]({link}) - R$ {preco}") # Exibimos o nome, o link e o preço formatado em MarkDown

