import streamlit as st
import pandas as pd
import tempfile

from utils.weibull_analysis import calcular_ttf_weibull, gerar_graficos_weibull_interativos_completo

st.set_page_config(layout="wide")
st.title("🔧 Análise de Confiabilidade - Distribuição Weibull")

# Botão de download do modelo
with open("data/exemplo.csv", "rb") as file:
    st.download_button(
        label="📥 Baixar modelo de planilha",
        data=file,
        file_name="modelo_weibull.csv",
        mime="text/csv"
    )

# Upload do usuário
uploaded_file = st.file_uploader("📂 Envie a planilha com os dados de falhas (.xlsx ou .csv)", type=["xlsx", "csv"])
if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    df, beta, eta, ttf = calcular_ttf_weibull(df)

    st.subheader("📊 Dados Processados")
    st.dataframe(df)

    # Geração dos gráficos e análise
    qq_img, fig_conf, fig_falha, analise = gerar_graficos_weibull_interativos_completo(ttf, beta, eta)

    st.subheader("🟦 QQ Plot (Weibull)")
    st.image(qq_img)

    st.subheader("📈 Curva de Confiabilidade R(t)")
    st.plotly_chart(fig_conf, use_container_width=True)

    st.subheader("📉 Curva de Probabilidade de Falha 1 - R(t)")
    st.plotly_chart(fig_falha, use_container_width=True)

    st.subheader("📌 Resultado da Análise Weibull")
    st.markdown(f"**Beta (β)**: `{beta:.2f}`")
    st.markdown(f"**Eta (η)**: `{eta:.2f}` horas")
    st.markdown(analise)

# Rodapé
st.markdown("---")
st.markdown("**Autores:** Vitor Matos Soares · Leonardo Silva Harmendani · João Antônio Nicholls")