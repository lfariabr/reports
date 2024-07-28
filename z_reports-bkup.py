#######################
#######################
# Libraries

import os
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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
    color_theme_list = [
        'Magma', 'Blues', 'Inferno',  'Plasma', 'Rainbow',
        'Viridis', 'Cividis', 'Turbo', 'YlGnBu', 'YlOrRd', 'Electric', 'Hot', 'Portland']
    
    default_theme_index = color_theme_list.index("Electric")
    selected_color_theme = st.selectbox('Selecione a cor do tema:', color_theme_list, index=default_theme_index)

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
    df_filtered_sorted = df_filtered.sort_values(by="Comparecimentos", ascending=False)

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
    
    with col2:
        st.markdown('#### Histórico da Loja')
        st.dataframe(df_filtered_sorted, hide_index=True)

    #######################
    # Gráficos
    
    #######################
    # Agrupando por ano e somando os valores após aplicar os filtros
    df_yearly_totals = df_filtered.groupby('ano').sum().reset_index()

    # visão ano
    st.markdown("## Visão por Ano")

    fig_leads_ano = px.bar(df_yearly_totals, x='ano', y='Leads', color='Leads', color_continuous_scale=selected_color_theme, title='Leads')
    fig_agendamentos_ano = px.bar(df_yearly_totals, x='ano', y='Agendamentos', color='Agendamentos', color_continuous_scale=selected_color_theme, title='Agendamentos')
    fig_comparecimentos_ano = px.bar(df_yearly_totals, x='ano', y='Comparecimentos', color='Comparecimentos', color_continuous_scale=selected_color_theme, title='Comparecimentos')

    # Leads
    st.plotly_chart(fig_leads_ano)

    # Agendamentos e Comparecimentos
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_agendamentos_ano)

    with col2:
        st.plotly_chart(fig_comparecimentos_ano)

    #######################
    # visão mês
    # Agrupando por ano e somando os valores após aplicar os filtros
    df_monthly_totals = df_filtered.groupby('mes_ano').sum().reset_index()

    st.markdown("## Visão por Mês")
    fig_leads_mes = px.bar(df_monthly_totals, x='mes_ano', y='Leads', color='Leads', color_continuous_scale=selected_color_theme, title='Leads')
    fig_agendamentos_mes = px.bar(df_monthly_totals, x='mes_ano', y='Agendamentos', color='Agendamentos', color_continuous_scale=selected_color_theme, title='Agendamentos')
    fig_comparecimentos_mes = px.bar(df_monthly_totals, x='mes_ano', y='Comparecimentos', color='Comparecimentos', color_continuous_scale=selected_color_theme, title='Comparecimentos')

    # Leads
    st.plotly_chart(fig_leads_mes)

    # Agendamentos e Comparecimentos
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_agendamentos_mes)

    with col2:
        st.plotly_chart(fig_comparecimentos_mes)

#######################
####################### PÁGINA 2

if page == "2 - Leads":

    # Load a different dataset
    df_leads_ano_e_mes_categoria = pd.read_csv('G:\\Meu Drive\\LUIS\\WORK\\18digital\\pro-corpo\\Lab Programação\\projeto_dashboard_historico\\df_leads_ano_e_mes_categoria.csv')

    # Excluir lojas específicas
    excluir_lojas = ['HOMA', 'PLÁSTICA', 'CENTRAL']  # Adicione as lojas que você deseja excluir

    # Filtros no arquivo
    lista_de_lojas_df = ['CAMPINAS', 'COPACABANA', 'HOMA', 'JARDINS', 'LONDRINA', 'MOEMA',
                        'SANTOS', 'TATUAPÉ', 'BELO HORIZONTE', 'BARRA DA TIJUCA',
                        'SANTO AMARO', 'TIJUCA', 'SOROCABA', 'PIRACICABA', 'IPIRANGA',
                        'TUCURUVI', 'LAPA', 'ITAIM','RIBEIRÃO PRETO', 'OSASCO',
                        'PLÁSTICA', 'MOOCA', 'ALPHAVILLE']

    df_leads_ano_e_mes_categoria = df_leads_ano_e_mes_categoria[df_leads_ano_e_mes_categoria['Unidade'].isin(lista_de_lojas_df) & ~df_leads_ano_e_mes_categoria['Unidade'].isin(excluir_lojas)]

    st.sidebar.markdown('### Filtros Página 2')

    # Filtros específicos para a página 2
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

    # Agrupar os dados conforme os filtros aplicados
    df_grouped_ano = df_filtered.groupby(['ano']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_fonte = df_filtered.groupby(['Fonte']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_unidade = df_filtered.groupby(['Unidade']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_categoria = df_filtered.groupby(['Categoria']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
    df_grouped_mes_ano = df_filtered.groupby(['mes_ano']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})

    col1, col2 = st.columns(2)

    with col1:

        fig_ano = px.bar(df_grouped_ano, x='ano', y='Total de Leads', color='ano', title='Leads por Ano')
        st.plotly_chart(fig_ano)

    with col2:

        fig_fonte = px.pie(df_grouped_fonte, names='Fonte', values='Total de Leads', title='Leads por Fonte')
        st.plotly_chart(fig_fonte)

    col1, col2 = st.columns(2)

    with col1:

        fig_unidade = px.bar(df_grouped_unidade, x='Unidade', y='Total de Leads', color='Unidade', title='Leads por Unidade')
        st.plotly_chart(fig_unidade)

    with col2:

        fig_categoria = px.pie(df_grouped_categoria, names='Categoria', values='Total de Leads', title='Leads por Categoria')
        st.plotly_chart(fig_categoria)

    col1, col2 = st.columns(2)

    with col1:

        fig_mes_ano = px.bar(df_grouped_mes_ano, x='mes_ano', y='Total de Leads', color='mes_ano', title='Leads por Mês/Ano')
        st.plotly_chart(fig_mes_ano)

    with col2:
        st.markdown('#### Dados Brutos')
        st.dataframe(df_filtered[['ano', 'mes_ano', 'Unidade', 'Fonte', 'Categoria', 'Total de Leads']], hide_index=True)

    col1, col2 = st.columns(2)

    with col1:

        df_categoria_ano = df_filtered.groupby(['ano', 'Categoria']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
        fig_categoria_ano = px.bar(df_categoria_ano, x='ano', y='Total de Leads', color='Categoria', title='Categoria por Ano')
        st.plotly_chart(fig_categoria_ano)

    with col2:

        df_categoria_mes_ano = df_filtered.groupby(['mes_ano', 'Categoria']).agg({'Total de Leads': 'sum'}).reset_index().rename(columns={'Total de Leads': 'Total de Leads'})
        fig_categoria_mes_ano = px.bar(df_categoria_mes_ano, x='mes_ano', y='Total de Leads', color='Categoria', title='Categoria por Ano e Mês')
        st.plotly_chart(fig_categoria_mes_ano)

 # Adicionando novos gráficos sugeridos

    # Heatmap de Correlation
    col1, col2 = st.columns(2)
    
    # Filtrando dados para o heatmap de correlação
    corr_df = df_filtered[['Total de Leads', 'ano', 'mes_ano', 'Fonte', 'Unidade']].copy()

    # Convertendo colunas categóricas em numéricas para correlação
    corr_df['Fonte'] = corr_df['Fonte'].astype('category').cat.codes
    corr_df['Unidade'] = corr_df['Unidade'].astype('category').cat.codes
    corr_df['mes_ano'] = corr_df['mes_ano'].astype('category').cat.codes

    # Calculando a matriz de correlação
    corr_matrix = corr_df.corr()

    # Gerando o heatmap de correlação
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Heatmap de Correlação')
        fig_corr = plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='viridis')
        plt.title('Heatmap de Correlação')
        st.pyplot(fig_corr)

    # Gráfico de Área Empilhada
    with col2:
        st.markdown('#### Gráfico de Área Empilhada')
        df_area = df_filtered.groupby(['ano', 'Categoria']).agg({'Total de Leads': 'sum'}).reset_index()
        fig_area = px.area(df_area, x='ano', y='Total de Leads', color='Categoria', title='Gráfico de Área Empilhada')
        st.plotly_chart(fig_area)

    # Gráfico de Linha com Pontos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Gráfico de Linha com Pontos')
        df_line = df_filtered.groupby(['mes_ano']).agg({'Total de Leads': 'sum'}).reset_index()
        fig_line = px.line(df_line, x='mes_ano', y='Total de Leads', markers=True, title='Gráfico de Linha com Pontos')
        st.plotly_chart(fig_line)

    # Gráfico de Boxplot
    with col2:
        st.markdown('#### Gráfico de Boxplot')
        fig_box = px.box(df_filtered, x='Categoria', y='Total de Leads', title='Gráfico de Boxplot')
        st.plotly_chart(fig_box)

