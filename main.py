import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from sidebar import render_sidebar
from page1 import render_page1
from page2 import render_page2
from page3 import render_page3
from page4 import render_page4

st.set_page_config(
    page_title="Pró-Corpo Labs Reports CRM",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("ggplot2")

# Carregando o CSV tratado
df_lojas_anos_e_mes = pd.read_csv('G:\\Meu Drive\\LUIS\\WORK\\18digital\\pro-corpo\\Lab Programação\\projeto_dashboard_historico/df_lojas_ano_e_mes.csv')

# Lista de lojas válidas
lista_de_lojas_df = [
    'CAMPINAS', 'COPACABANA', 'JARDINS', 'LONDRINA', 'MOEMA',
    'SANTOS', 'TATUAPÉ', 'BELO HORIZONTE', 'BARRA DA TIJUCA',
    'SANTO AMARO', 'TIJUCA', 'SOROCABA', 'PIRACICABA', 'IPIRANGA',
    'TUCURUVI', 'LAPA', 'ITAIM','RIBEIRÃO PRETO', 'OSASCO',
    'MOOCA', 'ALPHAVILLE'
]

# Aplicando o filtro de lojas
df_lojas_anos_e_mes = df_lojas_anos_e_mes[df_lojas_anos_e_mes['Unidade'].isin(lista_de_lojas_df)]

# Sidebar
page, selected_years, selected_stores, selected_color_theme, df_filtered_sorted = render_sidebar(df_lojas_anos_e_mes)

# Controle das páginas
if page == "1 - Funil":
    render_page1(selected_years, selected_stores, selected_color_theme, df_filtered_sorted)
elif page == "2 - Leads":
    render_page2()
elif page == "3 - Leags Pagos":
    render_page3()
elif page == "4 - Leags x Agenda":
    render_page4()
