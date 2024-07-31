import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def render_page2():

    # Carregando a base de dados tratada
    df_leads_ano_e_mes_categoria = pd.read_csv('G:\\Meu Drive\\LUIS\\WORK\\18digital\\pro-corpo\\Lab Programação\\projeto_dashboard_historico\\df_leads_ano_e_mes_categoria.csv')
    st.markdown('# LEADS')
    st.markdown('##### Aqui temos a visão geral de todos os leads, de todas as fontes')

    # Aplicando filtros específicos
    excluir_lojas = ['HOMA', 'PLÁSTICA', 'CENTRAL']
    lista_de_lojas_df = [
        'CAMPINAS', 'COPACABANA', 'HOMA', 'JARDINS', 'LONDRINA', 'MOEMA',
        'SANTOS', 'TATUAPÉ', 'BELO HORIZONTE', 'BARRA DA TIJUCA',
        'SANTO AMARO', 'TIJUCA', 'SOROCABA', 'PIRACICABA', 'IPIRANGA',
        'TUCURUVI', 'LAPA', 'ITAIM','RIBEIRÃO PRETO', 'OSASCO',
        'PLÁSTICA', 'MOOCA', 'ALPHAVILLE'
    ]

    df_leads_ano_e_mes_categoria = df_leads_ano_e_mes_categoria[
        df_leads_ano_e_mes_categoria['Unidade'].isin(lista_de_lojas_df) &
        ~df_leads_ano_e_mes_categoria['Unidade'].isin(excluir_lojas)
    ]

    # Sidebar adicional para filtrar dados da página 2 
    st.sidebar.markdown('### Filtros Página 2')
    unidades = st.sidebar.multiselect("Unidade", options=sorted(df_leads_ano_e_mes_categoria["Unidade"].unique()))
    anos = st.sidebar.multiselect("Ano", options=df_leads_ano_e_mes_categoria["ano"].unique())
    meses_ano = st.sidebar.multiselect("Mês/Ano", options=df_leads_ano_e_mes_categoria["mes_ano"].unique())
    fontes = st.sidebar.multiselect("Fonte", options=sorted(df_leads_ano_e_mes_categoria["Fonte"].unique()))
    categorias = st.sidebar.multiselect("Categoria", options=sorted(df_leads_ano_e_mes_categoria["Categoria"].unique()))

    df_filtered = df_leads_ano_e_mes_categoria.copy()

    if unidades:
        df_filtered = df_filtered[df_filtered["Unidade"].isin(unidades)]
    if anos:
        df_filtered = df_filtered[df_filtered["ano"].isin(anos)]
    if meses_ano:
        df_filtered = df_filtered[df_filtered["mes_ano"].isin(meses_ano)]
    if fontes:
        df_filtered = df_filtered[df_filtered["Fonte"].isin(fontes)]
    if categorias:
        df_filtered = df_filtered[df_filtered["Categoria"].isin(categorias)]

    df_grouped_ano = df_filtered.groupby(['ano']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_fonte = df_filtered.groupby(['Fonte']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_unidade = df_filtered.groupby(['Unidade']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_categoria = df_filtered.groupby(['Categoria']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_mes_ano = df_filtered.groupby(['mes_ano']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})

    # Div #1: Gráfico de barra Leads Ano a Ano + Gráfico de pizza Visão das fontes de lead
    col1, col2 = st.columns(2)

    with col1:
        fig_ano = px.bar(df_grouped_ano, x='ano', y='Total de Leads', color='ano', title='Leads por Ano')
        st.plotly_chart(fig_ano)

    with col2:
        fig_fonte = px.pie(df_grouped_fonte, names='Fonte', values='Total de Leads', title='Leads por Fonte')
        st.plotly_chart(fig_fonte)

    # Div #2: Barra leads por unidade(total) e Pizza leads por categoria
    col1, col2 = st.columns(2)
    with col1:
        fig_unidade = px.bar(df_grouped_unidade, x='Unidade', y='Total de Leads', color='Unidade', title='Leads por Unidade')
        st.plotly_chart(fig_unidade)
    with col2:
        fig_categoria = px.pie(df_grouped_categoria, names='Categoria', values='Total de Leads', title='Leads por Categoria')
        st.plotly_chart(fig_categoria)

    # Div #3: Barra leads por unidade/mes_ano e dados brutos
    col1, col2 = st.columns(2)
    with col1:
        fig_mes_ano = px.bar(df_grouped_mes_ano, x='mes_ano', y='Total de Leads', color='mes_ano', title='Leads por Mês/Ano')
        st.plotly_chart(fig_mes_ano)
    with col2:
        st.markdown('#### Dados Brutos')
        st.dataframe(df_filtered[['ano', 'mes_ano', 'Unidade', 'Fonte', 'Categoria', 'Total de Leads']], hide_index=True)
    
    # Div #4: Visão de categoria por ano e ano/mês
    col1, col2 = st.columns(2)
    with col1:
        df_categoria_ano = df_filtered.groupby(['ano', 'Categoria']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
        fig_categoria_ano = px.bar(df_categoria_ano, x='ano', y='Total de Leads', color='Categoria', title='Categoria por Ano')
        st.plotly_chart(fig_categoria_ano)
    with col2:
        df_categoria_mes_ano = df_filtered.groupby(['mes_ano', 'Categoria']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
        fig_categoria_mes_ano = px.bar(df_categoria_mes_ano, x='mes_ano', y='Total de Leads', color='Categoria', title='Categoria por Ano e Mês')
        st.plotly_chart(fig_categoria_mes_ano)

    # Div #5: Heatmap e área
    col1, col2 = st.columns(2)

    corr_df = df_filtered[['Total de Leads', 'ano', 'mes_ano', 'Fonte', 'Unidade']].copy()
    corr_df['Fonte'] = corr_df['Fonte'].astype('category').cat.codes
    corr_df['Unidade'] = corr_df['Unidade'].astype('category').cat.codes
    corr_df['mes_ano'] = corr_df['mes_ano'].astype('category').cat.codes
    corr_matrix = corr_df.corr()

    with col1:
        # st.markdown('#### Heatmap de Correlação')
        fig_corr = plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='viridis')
        plt.title('Heatmap de Correlação')
        st.pyplot(fig_corr)

    with col2:
        # st.markdown('#### Gráfico de Área Empilhada')
        df_area = df_filtered.groupby(['ano', 'Categoria']).agg({'Total de Leads': 'sum'}).reset_index()
        fig_area = px.area(df_area, x='ano', y='Total de Leads', color='Categoria', title='Categoria dos Leads x Ano Empilhada')
        st.plotly_chart(fig_area)

    # Div #6: Visão de categoria por ano e ano/mês
    col1, col2 = st.columns(2)
    with col1:
        # st.markdown('#### Gráfico de Linha com Pontos')
        df_line = df_filtered.groupby(['mes_ano']).agg({'Total de Leads': 'sum'}).reset_index()
        fig_line = px.line(df_line, x='mes_ano', y='Total de Leads', markers=True, title='Entrada de Leads Mês/Ano')
        st.plotly_chart(fig_line)
    with col2:
        # st.markdown('#### Boxplot')
        fig_box = px.box(df_filtered, x='Categoria', y='Total de Leads', title='Boxplot')
        st.plotly_chart(fig_box)
