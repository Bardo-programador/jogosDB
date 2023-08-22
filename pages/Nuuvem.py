import streamlit as st
from scripts import run
import pandas as pd
import datetime
import os
try:
    if not os.path.exists("dados"):
        os.mkdir("dados")
    open("dados/agenda.txt", 'x').close()
except:
    pass
st.title("Promoções da Nuuvem")
# Raspagem de dados e cronometro até a próxima raspagem
with open("dados/agenda.txt", 'r') as agenda:
    hora_agendada = agenda.read() ##Lê a hora agendada
if hora_agendada == "": ##Se estiver vazio, agenda para o dia seguinte
        nova_agenda = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1) ## Formata a nova agenda para o dia seguinte as 00:00
        hora_agendada = str(nova_agenda) ##Variavel da agenda é atualizada
        run("scrapy crawl nuuvem_especiais") ##Faz o web scraping na nuuvem
        with open("dados/agenda.txt", 'w') as agenda:
            agenda.write(str(nova_agenda)) ##Salva a nova agenda para o dia seguinte as 00:00
hora_agendada = datetime.datetime.strptime(hora_agendada, "%Y-%m-%d %H:%M:%S") ##Transforma a string em datetime
if hora_agendada <= datetime.datetime.now(): ##Se a hora agendada for menor que a hora atual, atualiza
        with st.spinner("Atualizando..."):
            run("scrapy crawl nuuvem_especiais") 
            with open('dados/agenda.txt', 'w') as agenda: ##Salva a nova agenda para o dia seguinte as 00:00
                nova_agenda = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                agenda.write(str(nova_agenda + datetime.timedelta(days=1)))

# Exibição dos dados    
nuuvem = pd.read_json("dados/nuuvem.jsonl", lines=True) ##Lê o arquivo jsonl
filtro = st.text_input("Procure por um jogo") ##Cria um filtro para o nome do jogo
for index, row in nuuvem.iterrows():
    nome_minusculo = row['name'].lower() ##Transforma o nome do jogo em minusculo
    if nome_minusculo.find(filtro) != -1:
        nome = row['name'] # Como o nome é uma lista, pegamos o primeiro elemento
        preco = row['price'] # Como o preço é uma lista, pegamos o primeiro elemento
        link = row['link'] # O link não é uma lista, então não precisamos pegar o primeiro elemento
        st.markdown(f"- [{nome}]({link}) - R$ {preco}") # Exibimos o nome, o link e o preço formatado em MarkDown

