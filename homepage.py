import streamlit as st
import pandas as pd

st.set_page_config(page_title='JogosDB', page_icon=':video_game:', layout='wide', initial_sidebar_state='auto')
st.title('JogosDB')

st.markdown("""
## Bem-vindo ao JogosDB, aqui você vê promoções de seus jogos favoritos!
Atualmente as lojas suportadas são:
- [Nuuvem](https://www.nuuvem.com/)
- [Steam](https://store.steampowered.com/)
""")