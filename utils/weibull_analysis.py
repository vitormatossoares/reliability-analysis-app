import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import weibull_min, probplot
import io

def calcular_ttf_weibull(df):
    df['Data hora in'] = pd.to_datetime(df['Data hora in'])
    df['Data hora fim'] = pd.to_datetime(df['Data hora fim'])

    # Ordenar
    df = df.sort_values(by='Data hora in').reset_index(drop=True)

    # Calcular TTF como: in atual - fim anterior
    df['TTF_horas'] = (df['Data hora in'] - df['Data hora fim'].shift(1)).dt.total_seconds() / 3600

    # Eliminar valores nulos (primeira linha)
    ttf = df['TTF_horas'].dropna()

    # Ajuste da Weibull
    shape, loc, scale = weibull_min.fit(ttf, floc=0)

    return df, shape, scale, ttf



def gerar_graficos_weibull_interativos_completo(ttf, beta, eta):
    # 1. QQ Plot (imagem)
    fig_qq, ax = plt.subplots(figsize=(4, 3))
    probplot(ttf, dist=weibull_min(c=beta, scale=eta), plot=ax)
    ax.set_title("QQ Plot Weibull")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)

    # 2. Curva de Confiabilidade R(t)
    x = np.linspace(0, max(ttf) * 1.5, 100)
    R = np.exp(-(x / eta) ** beta)
    fig_conf = go.Figure()
    fig_conf.add_trace(go.Scatter(x=x, y=R * 100, mode="lines", name="Confiabilidade R(t)"))
    fig_conf.add_shape(type="line", x0=eta, x1=eta, y0=0, y1=100,
                       line=dict(color="red", dash="dash"))
    fig_conf.update_layout(
        title="Curva de Confiabilidade R(t)",
        xaxis_title="Tempo (horas)",
        yaxis_title="Confiabilidade (%)",
        height=400
    )

    # 3. Curva de Probabilidade de Falha
    F = (1 - R) * 100
    fig_falha = go.Figure()
    fig_falha.add_trace(go.Scatter(x=x, y=F, mode="lines", name="Probabilidade de Falha", line=dict(color="orange")))
    fig_falha.update_layout(
        title="Curva de Probabilidade de Falha",
        xaxis_title="Tempo (horas)",
        yaxis_title="Probabilidade (%)",
        height=400
    )

    # Análise textual automática
    if beta < 1:
        analise = ":red[🔴 Falhas infantis ou aleatórias (β < 1)]"
    elif 1 <= beta < 3:
        analise = ":orange[🟠 Desgaste progressivo (1 ≤ β < 3)]"
    elif beta >= 3:
        analise = ":green[🟢 Desgaste acelerado (β ≥ 3)]"
    else:
        analise = ":gray[⚪ Indeterminado]"

    return buf, fig_conf, fig_falha, analise
