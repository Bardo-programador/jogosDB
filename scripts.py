import os
import datetime
import streamlit as st
import subprocess

def run(STRING):
    comando = STRING.split()

    # Executar o comando do Scrapy
    resultado = subprocess.run(comando, capture_output=True, text=True)
     
def verificarAgenda(caminho_agenda, comando):
    diretorio = "/".join(caminho_agenda.split("/")[:-1])
    try:
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
        open(caminho_agenda, 'x').close()
    except:
        pass
    # Raspagem de dados e cronometro até a próxima raspagem
    with open(caminho_agenda, 'r') as agenda:
        hora_agendada = agenda.read() ##Lê a hora agendada
    if hora_agendada == "": ##Se estiver vazio, agenda para o dia seguinte
            nova_agenda = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1) ## Formata a nova agenda para o dia seguinte as 00:00
            hora_agendada = str(nova_agenda) ##Variavel da agenda é atualizada
            with st.spinner("Atualizando..."):
                run(comando) ##Faz o web scraping
            with open(caminho_agenda, 'w') as agenda:
                agenda.write(str(nova_agenda)) ##Salva a nova agenda para o dia seguinte as 00:00
    hora_agendada = datetime.datetime.strptime(hora_agendada, "%Y-%m-%d %H:%M:%S") ##Transforma a string em datetime
    if hora_agendada <= datetime.datetime.now(): ##Se a hora agendada for menor que a hora atual, atualiza
        with st.spinner("Atualizando..."):
            run(comando) 
        with open(caminho_agenda, 'w') as agenda: ##Salva a nova agenda para o dia seguinte as 00:00
            nova_agenda = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            agenda.write(str(nova_agenda + datetime.timedelta(days=1)))

