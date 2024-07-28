import streamlit as st
    
def render_sidebar(df_lojas_anos_e_mes):

    st.sidebar.title('Pró-Corpo Lab')
    st.sidebar.markdown('### Relatórios')
    page = st.sidebar.radio("", ["1 - Funil",
                                  "2 - Leads",
                                  "3 - Leags Pagos"
                                  ], index=0)

    st.sidebar.markdown('### Filtros')
    year_list = list(df_lojas_anos_e_mes['ano'].unique())[::-1]
    stores_list = list(df_lojas_anos_e_mes['Unidade'].unique())[::-1]
    stores_list.sort()

    year_list.insert(0, "Total")
    stores_list.insert(0, "Total")

    selected_years = st.sidebar.multiselect('Selecione o Ano:', year_list, default="Total")
    selected_stores = st.sidebar.multiselect('Selecione a Unidade:', stores_list, default="Total")

    color_theme_list = [
        'Magma', 'Blues', 'Inferno',  'Plasma', 'Rainbow',  
        'Viridis', 'Cividis', 'Turbo', 'YlGnBu', 'YlOrRd', 'Electric', 'Hot', 'Portland'
    ]
    
    default_theme_index = color_theme_list.index("Electric")
    selected_color_theme = st.sidebar.selectbox('Selecione a cor do tema:', color_theme_list, index=default_theme_index)

    if "Total" in selected_years:
        filtered_years = year_list[1:]
    else:
        filtered_years = selected_years

    if "Total" in selected_stores:
        filtered_stores = stores_list[1:]
    else:
        filtered_stores = selected_stores

    df_filtered = df_lojas_anos_e_mes[
        (df_lojas_anos_e_mes['ano'].isin(filtered_years)) &
        (df_lojas_anos_e_mes['Unidade'].isin(filtered_stores))
    ]
    df_filtered_sorted = df_filtered.sort_values(by="Comparecimentos", ascending=False)
    df_filtered['ano'] = df_filtered['ano'].astype(str)

    return page, selected_years, selected_stores, selected_color_theme, df_filtered_sorted
