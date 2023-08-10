import streamlit as st
import pandas as pd
from scrapy import cmdline
from scripts import run
# Configurar o Streamlit

st.title("Promoções da Steam")

# Executar a raspagem ao clicar no botão
run('scrapy crawl steam_especiais')
steam = pd.read_json("dados/steam.jsonl", lines=True)
st.dataframe(steam)
