import streamlit as st
import pandas as pd
from scrapy import cmdline
import subprocess
# Configurar o Streamlit
def run(STRING):
    comando = STRING.split()

    # Executar o comando do Scrapy
    resultado = subprocess.run(comando, capture_output=True, text=True)
st.title("Promoções da Steam")

# Executar a raspagem ao clicar no botão
# cmdline.execute("scrapy crawl steam_especiais".split())
run('scrapy crawl steam_especiais')
steam = pd.read_json("dados/steam.jsonl", lines=True)
st.dataframe(steam)
