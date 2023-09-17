import os
import datetime
import streamlit as st
import subprocess
from string import punctuation
def __run(STRING):
    comando = STRING.split()

    # Executar o comando do Scrapy
    resultado = subprocess.run(comando, capture_output=True, text=True)
     
def verificarAgenda(caminho_agenda, comando):
    """
    Verifica se a hora agendada já passou, se sim, atualiza os dados

    Args:
        caminho_agenda (str): Caminho do arquivo de agenda
        comando (str): Comando do Scrapy
    """
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
                __run(comando) ##Faz o web scraping
            with open(caminho_agenda, 'w') as agenda:
                agenda.write(str(nova_agenda)) ##Salva a nova agenda para o dia seguinte as 00:00
    hora_agendada = datetime.datetime.strptime(hora_agendada, "%Y-%m-%d %H:%M:%S") ##Transforma a string em datetime
    if hora_agendada <= datetime.datetime.now(): ##Se a hora agendada for menor que a hora atual, atualiza
        with st.spinner("Atualizando..."):
            __run(comando) 
        with open(caminho_agenda, 'w') as agenda: ##Salva a nova agenda para o dia seguinte as 00:00
            nova_agenda = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            agenda.write(str(nova_agenda + datetime.timedelta(days=1)))

def exibirJogos(df_jogos, preco_limite, filtro):
    """
    Exibe os jogos de acordo com o filtro e o preço limite

    Args:
        df_jogos (DataFrame): DataFrame com os jogos
        preco_limite (int): Preço máximo do jogo
        filtro (str): Nome do jogo
    
    Returns:
        None
    """
    for index, row in df_jogos.iterrows():
        nome_minusculo = row['name'].lower() ##Transforma o nome do jogo em minusculo
        nome = row['name'] # Como o nome é uma lista, pegamos o primeiro elemento
        preco_float = row['price'] # Variável usada para o filtro de preço
        if type(preco_float) == str:
            for i in preco_float:
                if i in punctuation or i.isalpha():
                    preco_float = preco_float.replace(i, "") # O preço é uma string, então precisamos remover os caracteres especiais 
            preco_float = float(preco_float)/100 # divide por 100 pois a formatacao elimina os dois ultimos digitos

        preco_bruto = row['price']
        link = row['link'] # pega o link do jogo
        if nome_minusculo.find(filtro.lower()) != -1 and (preco_float <= preco_limite or preco_limite == 250):
            st.markdown(f"- [{nome}]({link}) - {preco_bruto}") # Exibimos o nome, o link e o preço formatado em MarkDown

