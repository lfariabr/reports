import streamlit as st
import plotly.express as px

def render_page1(selected_years, selected_stores, selected_color_theme, df_filtered_sorted):
    st.markdown('# FUNIL')
    st.markdown('##### Aqui temos a visão geral do funil para loja e período selecionado!')

    col1, col2 = st.columns(2)

    with col1:
        selected_store = selected_stores[0] if len(selected_stores) == 1 else "Várias Unidades"
        total_leads = int(df_filtered_sorted['Leads'].sum())
        total_agendamentos = int(df_filtered_sorted['Agendamentos'].sum())
        total_comparecimentos = int(df_filtered_sorted['Comparecimentos'].sum())

        percent_agendamentos = (total_agendamentos / total_leads * 100) if total_leads > 0 else 0
        percent_comparecimentos = (total_comparecimentos / total_agendamentos * 100) if total_agendamentos > 0 else 0

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

    df_yearly_totals = df_filtered_sorted.groupby('ano').sum().reset_index()

    st.markdown("## Visão por Ano")

    fig_leads_ano = px.bar(df_yearly_totals, x='ano', y='Leads', color='Leads', color_continuous_scale=selected_color_theme, title='Leads')
    fig_agendamentos_ano = px.bar(df_yearly_totals, x='ano', y='Agendamentos', color='Agendamentos', color_continuous_scale=selected_color_theme, title='Agendamentos')
    fig_comparecimentos_ano = px.bar(df_yearly_totals, x='ano', y='Comparecimentos', color='Comparecimentos', color_continuous_scale=selected_color_theme, title='Comparecimentos')

    st.plotly_chart(fig_leads_ano)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_agendamentos_ano)
    with col2:
        st.plotly_chart(fig_comparecimentos_ano)

    df_monthly_totals = df_filtered_sorted.groupby('mes_ano').sum().reset_index()

    st.markdown("## Visão por Mês")
    fig_leads_mes = px.bar(df_monthly_totals, x='mes_ano', y='Leads', color='Leads', color_continuous_scale=selected_color_theme, title='Leads')
    fig_agendamentos_mes = px.bar(df_monthly_totals, x='mes_ano', y='Agendamentos', color='Agendamentos', color_continuous_scale=selected_color_theme, title='Agendamentos')
    fig_comparecimentos_mes = px.bar(df_monthly_totals, x='mes_ano', y='Comparecimentos', color='Comparecimentos', color_continuous_scale=selected_color_theme, title='Comparecimentos')

    st.plotly_chart(fig_leads_mes)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_agendamentos_mes)
    with col2:
        st.plotly_chart(fig_comparecimentos_mes)
