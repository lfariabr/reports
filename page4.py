import streamlit as st
import pandas as pd
import plotly.express as px

def render_page4():
    # Carregando a base
    df_leads_ano_e_mes_categoria_merged = pd.read_csv('G:\\Meu Drive\\LUIS\\WORK\\18digital\\pro-corpo\\Lab Programação\\projeto_dashboard_historico\\df_leads_all_categoria_merged_reduced.csv')
    st.markdown('# LEADS PAGOS X AGENDA')
    st.markdown('##### Aqui temos a visão geral dos leads que + comparecem.')
    
    # filtros específicos
    excluir_lojas = ['HOMA', 'PLÁSTICA', 'CENTRAL']
    lista_de_lojas_df = [
        'CAMPINAS', 'COPACABANA', 'HOMA', 'JARDINS', 'LONDRINA', 'MOEMA',
        'SANTOS', 'TATUAPÉ', 'BELO HORIZONTE', 'BARRA DA TIJUCA',
        'SANTO AMARO', 'TIJUCA', 'SOROCABA', 'PIRACICABA', 'IPIRANGA',
        'TUCURUVI', 'LAPA', 'ITAIM','RIBEIRÃO PRETO', 'OSASCO',
        'PLÁSTICA', 'MOOCA', 'ALPHAVILLE'
    ]
    fontes_pagas = [
        'Google Pesquisa','Facebook postlink','Google Display','Facebook Leads', 'Instagram Leads', 'Instagram',
        'Bing Pesquisa','SMS', 'Facebook e instagram','leadsolution','Vivo Ads','Kwanko','BOTOX CO2 FACEBOOK',
        'TATUAGEM FACEBOOK','SEMANA SEM RUGAS FACEBOOK','BOTOX PREENCHIMENTO FACEBOOK','Google Pesquisa com Display'
    ]
    df_leads_ano_e_mes_categoria_merged = df_leads_ano_e_mes_categoria_merged[
        df_leads_ano_e_mes_categoria_merged['Unidade'].isin(lista_de_lojas_df) &
        df_leads_ano_e_mes_categoria_merged['Fonte'].isin(fontes_pagas) &
        ~df_leads_ano_e_mes_categoria_merged['Unidade'].isin(excluir_lojas)
    ]
    # Filtros no sidebar
    st.sidebar.markdown('### Filtros Página 4')
    unidades = st.sidebar.multiselect("Unidade", options=sorted(df_leads_ano_e_mes_categoria_merged["Unidade"].unique()))
    anos = st.sidebar.multiselect("Ano", options=df_leads_ano_e_mes_categoria_merged["ano"].unique())
    meses_ano = st.sidebar.multiselect("Mês/Ano", options=df_leads_ano_e_mes_categoria_merged["mes_ano"].unique())
    fontes = st.sidebar.multiselect("Fonte", options=sorted(df_leads_ano_e_mes_categoria_merged["Fonte"].unique()))
    categorias = st.sidebar.multiselect("Categoria", options=sorted(df_leads_ano_e_mes_categoria_merged["Categoria"].unique()))
    comparecimento = st.sidebar.multiselect("Quando compareceu?", options=df_leads_ano_e_mes_categoria_merged["Quando compareceu?"].unique())

    df_filtered = df_leads_ano_e_mes_categoria_merged.copy()

    # Aplicando todos os filtros, exceto "Quando compareceu?"
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

    # Leads por Ano com e Sem Comparecimento
    st.subheader("Leads (Total)")
    col1, col2 = st.columns(2)

    with col1:
        leads_per_year = df_filtered['ano'].value_counts().reset_index()
        leads_per_year.columns = ['ano', 'Count']
        fig_leads_per_year = px.bar(leads_per_year, x='ano', y='Count', title="Leads por Ano")
        st.plotly_chart(fig_leads_per_year)

    # Filtrando para exibir comparecimento = True
    with col2:
        leads_per_year_true = df_filtered[df_filtered['Tem lead?'] == "True"]['ano'].value_counts().reset_index()
        leads_per_year_true.columns = ['ano', 'Count']
        fig_leads_per_year_true = px.bar(leads_per_year_true, x='ano', y='Count', title="Leads por Ano que Comparecem")
        st.plotly_chart(fig_leads_per_year_true)
    
    # Leads por Loja com e Sem Comparecimento
    st.subheader("Leads (Por Loja)")
    col1, col2 = st.columns(2)

    with col1:
        leads_per_unit = df_filtered['Unidade'].value_counts().reset_index()
        leads_per_unit.columns = ['Unidade', 'Count']
        fig_leads_per_unit = px.bar(leads_per_unit, x='Unidade', y='Count', title="Leads por Unidade")
        st.plotly_chart(fig_leads_per_unit)

    with col2:
        leads_per_unit_true = df_filtered[df_filtered['Tem lead?'] == "True"]['Unidade'].value_counts().reset_index()
        leads_per_unit_true.columns = ['Unidade', 'Count']
        fig_leads_per_unit_true = px.bar(leads_per_unit_true, x='Unidade', y='Count', title="Leads por Unidade Que Comparecem")
        st.plotly_chart(fig_leads_per_unit_true)

    # Aplicando o filtro "Quando compareceu?" nos gráficos que devem respeitar este filtro
    if comparecimento:
        df_filtered = df_filtered[df_filtered["Quando compareceu?"].isin(comparecimento)]

    # Gráficos de Pizza
    st.subheader("Principais responsáveis por comparecimento")
    col1, col2 = st.columns(2)

    with col1:
        category_lead_true = df_filtered[df_filtered['Tem lead?'] == "True"]['Categoria'].value_counts().reset_index()
        category_lead_true.columns = ['Categoria', 'Count']
        fig_cat_lead_true = px.pie(category_lead_true, names='Categoria', values='Count', title="Categoria dos Leads que Comparecem")
        st.plotly_chart(fig_cat_lead_true)

    with col2:
        source_lead_true = df_filtered[df_filtered['Tem lead?'] == "True"]['Fonte'].value_counts().reset_index()
        source_lead_true.columns = ['Fonte', 'Count']
        fig_source_lead_true = px.pie(source_lead_true, names='Fonte', values='Count', title="Fonte dos Leads que Comparecem")
        st.plotly_chart(fig_source_lead_true)

    # Quarta Divisão: Razão entre total de leads por loja e total de leads que comparecem
    st.subheader("Razão: Total de Leads por Loja / Leads que Comparecem (%)")

    # Calcular o total de leads por loja após aplicar os filtros
    total_leads_por_loja = df_filtered.groupby('Unidade').size().reset_index(name='Total Leads')

    # Calcular o total de leads que comparecem por loja após aplicar os filtros
    leads_que_comparecem_por_loja = df_filtered[df_filtered['Tem lead?'] == "True"].groupby('Unidade').size().reset_index(name='Leads que Comparecem')

    # Merge dos dois DataFrames
    razao_leads = pd.merge(total_leads_por_loja, leads_que_comparecem_por_loja, on='Unidade', how='left')

    # Evitar divisão por zero
    razao_leads['Leads que Comparecem'].replace(0, pd.NA, inplace=True)

    # Calcular a razão em %
    razao_leads['Razão (%)'] = (razao_leads['Leads que Comparecem'] / razao_leads['Total Leads']) * 100

    # Criar o gráfico de barras com a razão em %
    fig_razao_leads = px.line(razao_leads, x='Unidade', y='Razão (%)', title="Razão: Total de Leads por Loja / Leads que Comparecem (%)")
    st.plotly_chart(fig_razao_leads)
