#######################
#######################
# Libraries

import os
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
#######################
# Page config

st.set_page_config(
    page_title="Pró-Corpo Labs Reports CRM",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"),

alt.themes.enable("ggplot2")

#######################
#######################
# Load data

# Abrindo o arquivo:
df_lojas_anos_e_mes = pd.read_csv('G:\\Meu Drive\\LUIS\\WORK\\18digital\\pro-corpo\\Lab Programação\\projeto_dashboard_historico/df_lojas_ano_e_mes.csv')

# Filtros no arquivo
lista_de_lojas_df = ['CAMPINAS', 'COPACABANA', 'HOMA', 'JARDINS', 'LONDRINA', 'MOEMA',
                    'SANTOS', 'TATUAPÉ', 'BELO HORIZONTE', 'BARRA DA TIJUCA',
                    'SANTO AMARO', 'TIJUCA', 'SOROCABA', 'PIRACICABA', 'IPIRANGA',
                    'TUCURUVI', 'LAPA', 'ITAIM','RIBEIRÃO PRETO', 'OSASCO',
                    'PLÁSTICA', 'MOOCA', 'ALPHAVILLE']

df_lojas_anos_e_mes = df_lojas_anos_e_mes[df_lojas_anos_e_mes['Unidade'].isin(lista_de_lojas_df)]

#######################
#######################
# Sidebar

with st.sidebar:
    st.title('Pró-Corpo Lab')

    # Navegação de páginas
    st.markdown('### Relatórios')
    page = st.radio("",["1 - Funil","2 - Leads"], index=0)

    # Navegação entre anos e lojas
    st.markdown('### Filtros')
    year_list = list(df_lojas_anos_e_mes['ano'].unique())[::-1]
    stores_list = list(df_lojas_anos_e_mes['Unidade'].unique())[::-1]
    stores_list.sort()

    year_list.insert(0,"Total")
    stores_list.insert(0,"Total")

    # Multi select com a opção "all"
    selected_years = st.multiselect(
        'Selecione o Ano:', year_list, default="Total")
    
    selected_stores = st.multiselect(
        'Selecione a Unidade:', stores_list, default="Total")

    # Navegação temas
    color_theme_list = ['Magma', 'Blues', 'Inferno',  'Plasma', 'Rainbow']
    selected_color_theme = st.selectbox('Selecione a cor do tema:', color_theme_list)

    # Aplicando os filtros considerando opções "all"
    if "Total" in selected_years:
        filtered_years = year_list[1:] # Todos os anos, exceto "ALL"
    
    else:
        filtered_years = selected_years

    if "Total" in selected_stores:
        filtered_stores = stores_list[1:] # Todas as lojas, menos "Total"

    else: 
        filtered_stores = selected_stores

    # Aplicar ambos os filtros
    df_filtered = df_lojas_anos_e_mes[(df_lojas_anos_e_mes['ano'].isin(filtered_years)) & (df_lojas_anos_e_mes['Unidade'].isin(filtered_stores))]
    df_filtered_sorted = df_filtered.sort_values(by="Leads", ascending=False)

    # Converter a coluna 'ano' para string
    df_filtered['ano'] = df_filtered['ano'].astype(str)

#######################
#######################
# Dados

#######################
####################### PÁGINA 1
if page == "1 - Funil":
    st.markdown('# Funil')
    st.markdown('##### Aqui veremos a visão geral do funil para loja e período selecionado!')

    col1, col2 = st.columns(2)

    with col2:
        st.markdown('#### Histórico da Loja')
        st.dataframe(df_filtered_sorted, hide_index=True)

    with col1:
        # st.markdown('#### Resumo da Unidade')
        selected_store = selected_stores[0] if len(selected_stores) == 1 else "Várias Unidades"

        total_leads = int(df_filtered['Leads'].sum())
        total_agendamentos = int(df_filtered['Agendamentos'].sum())
        total_comparecimentos = int(df_filtered['Comparecimentos'].sum())

        # Fazendo as taxas que queremos ver
        percent_agendamentos = (total_agendamentos / total_leads * 100) if total_leads > 0 else 0
        percent_comparecimentos = (total_comparecimentos / total_agendamentos * 100) if total_agendamentos > 0 else 0

        #Exibindo o painel de resumo
        st.markdown(
        f"""
        <div style="font-size: 14px; color: Fuchsia;">Unidade</div>
        <div style="font-size: 36px;">{selected_store}
        """,
        unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="font-size: 14px; color: Fuchsia;">Leads</div>
            <div style="font-size: 36px; ">{total_leads:,}
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="font-size: 14px; color: Fuchsia;">Agendamentos</div>
            <div style="font-size: 36px;">{total_agendamentos:,} <span style="font-size: 12px; color: gray;">({percent_agendamentos:.2f}%)</span></div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="font-size: 14px; color: Fuchsia;">Comparecimentos</div>
            <div style="font-size: 36px;">{total_comparecimentos:,} <span style="font-size: 12px; color: gray;">({percent_comparecimentos:.2f}%)</span></div>
            """,
            unsafe_allow_html=True
        )


    #######################
    # Gráficos

    fig_leads = px.bar(df_filtered_sorted, x='mes_ano', y='Leads', color='Leads', color_continuous_scale=selected_color_theme, title='Leads')
    fig_agendamentos = px.bar(df_filtered_sorted, x='mes_ano', y='Agendamentos', color='Agendamentos', color_continuous_scale=selected_color_theme, title='Agendamentos')
    fig_comparecimentos = px.bar(df_filtered_sorted, x='mes_ano', y='Comparecimentos', color='Comparecimentos', color_continuous_scale=selected_color_theme, title='Comparecimentos')

    st.plotly_chart(fig_leads)

    # Dividindo os gráficos de Agendamentos e Comparecimentos em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_agendamentos)

    with col2:
        st.plotly_chart(fig_comparecimentos)

#######################
####################### PÁGINA 2
if page == "2 - Leads":

    st.markdown('# Leads')
    st.markdown('##### Aqui veremos os detalhes dos leads da loja e período selecionado!')
    st.markdown('')
    st.markdown('')


    col1, col2 = st.columns(2)

    with col2:
        st.markdown('#### Histórico da Loja')
        st.dataframe(df_filtered_sorted, hide_index=True)

    with col1:
        # st.markdown('#### Resumo da Unidade')
        selected_store = selected_stores[0] if len(selected_stores) == 1 else "Várias Unidades"

        total_leads = int(df_filtered['Leads'].sum())
        total_agendamentos = int(df_filtered['Agendamentos'].sum())
        total_comparecimentos = int(df_filtered['Comparecimentos'].sum())

        # Fazendo as taxas que queremos ver
        percent_agendamentos = (total_agendamentos / total_leads * 100) if total_leads > 0 else 0
        percent_comparecimentos = (total_comparecimentos / total_agendamentos * 100) if total_agendamentos > 0 else 0

        #Exibindo o painel de resumo
        st.markdown(
        f"""
        <div style="font-size: 14px; color: Fuchsia;">Unidade</div>
        <div style="font-size: 36px;">{selected_store}
        """,
        unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="font-size: 14px; color: Fuchsia;">Leads</div>
            <div style="font-size: 36px; ">{total_leads:,}
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="font-size: 14px; color: Fuchsia;">Agendamentos</div>
            <div style="font-size: 36px;">{total_agendamentos:,} <span style="font-size: 12px; color: gray;">({percent_agendamentos:.2f}%)</span></div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="font-size: 14px; color: Fuchsia;">Comparecimentos</div>
            <div style="font-size: 36px;">{total_comparecimentos:,} <span style="font-size: 12px; color: gray;">({percent_comparecimentos:.2f}%)</span></div>
            """,
            unsafe_allow_html=True
        )


    #######################
    # Gráficos

    fig_leads = px.bar(df_filtered_sorted, x='mes_ano', y='Leads', color='Leads', color_continuous_scale=selected_color_theme, title='Leads')
    fig_agendamentos = px.bar(df_filtered_sorted, x='mes_ano', y='Agendamentos', color='Agendamentos', color_continuous_scale=selected_color_theme, title='Agendamentos')
    fig_comparecimentos = px.bar(df_filtered_sorted, x='mes_ano', y='Comparecimentos', color='Comparecimentos', color_continuous_scale=selected_color_theme, title='Comparecimentos')

    st.plotly_chart(fig_leads)

    # Dividindo os gráficos de Agendamentos e Comparecimentos em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_agendamentos)

    with col2:
        st.plotly_chart(fig_comparecimentos)