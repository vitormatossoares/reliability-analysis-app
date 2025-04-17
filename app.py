import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.weibull_analysis import calcular_ttf_weibull, gerar_graficos_weibull_interativos_completo
from utils.data_analysis import gerar_boxplot_duracao, gerar_pareto_falhas, gerar_pareto_equipamentos, gerar_mapa_calor

st.set_page_config(layout="wide")
st.title("🔧 Análise de Confiabilidade - Distribuição Weibull")

# Botão de download do modelo
with open("data/exemplo.csv", "rb") as file:
    st.download_button(
        label="📅 Baixar modelo de planilha",
        data=file,
        file_name="modelo_weibull.csv",
        mime="text/csv"
    )

# Upload do usuário
uploaded_file = st.file_uploader("📂 Envie a planilha com os dados de falhas (.xlsx ou .csv)", type=["xlsx", "csv"])
if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)

    # Conversão e ordenação
    df['Data hora in'] = pd.to_datetime(df['Data hora in'])
    df['Data hora fim'] = pd.to_datetime(df['Data hora fim'])
    df = df.sort_values(by=['Equipamento', 'Data hora in']).reset_index(drop=True)

    # Calcular a duração do evento
    df['Duracao_horas'] = (df['Data hora fim'] - df['Data hora in']).dt.total_seconds() / 3600
    df['AnoMes'] = df['Data hora in'].dt.to_period('M').astype(str)

    # Filtro por equipamento
    equipamentos = list(df['Equipamento'].dropna().unique())
    equipamentos_opcao = ["Todos"] + equipamentos
    equipamento_selecionado = st.selectbox("🛠️ Selecione o Equipamento", equipamentos_opcao)

    if equipamento_selecionado != "Todos":
        df = df[df['Equipamento'] == equipamento_selecionado].copy()

    # Calcular TTF
    df['TTF_horas'] = (df['Data hora in'] - df['Data hora fim'].shift(1)).dt.total_seconds() / 3600
    ttf = df['TTF_horas'].dropna()

    st.subheader("📊 Dados Filtrados")
    st.dataframe(df)

    st.markdown("---")
    
    st.markdown("---")
    st.subheader("🌎 Mapa de Calor - Horas Paradas por Mês/Ano")
    fig_calor = gerar_mapa_calor(df)
    st.plotly_chart(fig_calor, use_container_width=True)
    
    st.subheader("📊 Pareto por Equipamento")
    fig_pareto_eqp = gerar_pareto_equipamentos(df)
    st.plotly_chart(fig_pareto_eqp, use_container_width=True)
    
    st.subheader("📉 Pareto das Falhas por Tipo")
    fig_pareto_falhas = gerar_pareto_falhas(df)
    st.plotly_chart(fig_pareto_falhas, use_container_width=True)


    if len(ttf) >= 3:
        df, beta, eta, ttf = calcular_ttf_weibull(df)
        qq_img, fig_conf, fig_falha, analise = gerar_graficos_weibull_interativos_completo(ttf, beta, eta)

        st.markdown("---")
        st.subheader("📈 QQ Plot Weibull")
        st.image(qq_img, caption="QQ Plot Weibull")

        st.subheader("📉 Curvas de Confiabilidade e Probabilidade de Falha")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_conf, use_container_width=True)
        with col2:
            st.plotly_chart(fig_falha, use_container_width=True)

        st.markdown("---")
        st.subheader("📌 Resultado da Análise Weibull")
        if equipamento_selecionado != "Todos":
            st.markdown(f"**Equipamento:** `{equipamento_selecionado}`")
        st.markdown(f"**Beta (β):** `{beta:.2f}`")
        st.markdown(f"**Eta (η):** `{eta:.2f}` horas")
        st.markdown(analise)
    else:
        st.warning("Esse conjunto de dados não possui dados suficientes para análise de Weibull (mínimo de 3 TTFs).")


# Rodapé
st.markdown("---")
st.markdown("**Autores:** Vitor Matos Soares · Leonardo Silva Harmendani · João Antônio Nicholls")
