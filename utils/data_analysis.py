import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def gerar_boxplot_duracao(df_eqp: pd.DataFrame):
    fig = px.box(
        df_eqp,
        y='Duracao_horas',
        title='Boxplot de Duração das Falhas',
        labels={'Duracao_horas': 'Duração (horas)'}
    )
    fig.update_layout(
        height=300,
        width=800,
        margin=dict(t=30, b=30, l=30, r=30),
        template="plotly_white"
    )
    return fig

def gerar_pareto_falhas(df: pd.DataFrame):
    df_pareto = df.groupby('Falha')['Duracao_horas']\
        .sum().sort_values(ascending=False).reset_index()
    df_pareto['Acumulado'] = df_pareto['Duracao_horas'].cumsum()
    df_pareto['Percentual'] = 100 * df_pareto['Duracao_horas'] / df_pareto['Duracao_horas'].sum()
    df_pareto['Percentual Acumulado'] = df_pareto['Percentual'].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_pareto['Falha'],
        y=df_pareto['Duracao_horas'],
        name='Tempo Total de Parada (horas)',
        marker=dict(color='royalblue')
    ))

    fig.add_trace(go.Scatter(
        x=df_pareto['Falha'],
        y=df_pareto['Percentual Acumulado'],
        name='Acumulado (%)',
        yaxis='y2',
        marker=dict(color='crimson'),
        mode='lines+markers'
    ))

    fig.update_layout(
        title='Pareto - Falhas com Maior Tempo de Parada',
        width=800,
        xaxis=dict(title='Tipo de Falha'),
        yaxis=dict(title='Tempo Total de Parada (horas)'),
        yaxis2=dict(
            title='Acumulado (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        height=400,
        legend=dict(x=1, y=1, orientation='v', bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=50, b=30, l=40, r=30),
        template="plotly_white"
    )

    return fig

def gerar_pareto_equipamentos(df: pd.DataFrame):
    df_eqp = df.groupby('Equipamento')['Duracao_horas'].sum().sort_values(ascending=False).reset_index()
    df_eqp['Acumulado'] = df_eqp['Duracao_horas'].cumsum()
    df_eqp['Percentual'] = 100 * df_eqp['Duracao_horas'] / df_eqp['Duracao_horas'].sum()
    df_eqp['Percentual Acumulado'] = df_eqp['Percentual'].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_eqp['Equipamento'],
        y=df_eqp['Duracao_horas'],
        name='Tempo Total de Parada (horas)',
        marker=dict(color='royalblue')
    ))

    fig.add_trace(go.Scatter(
        x=df_eqp['Equipamento'],
        y=df_eqp['Percentual Acumulado'],
        name='Acumulado (%)',
        yaxis='y2',
        marker=dict(color='crimson'),
        mode='lines+markers'
    ))

    fig.update_layout(
        title='Pareto - Equipamentos com Maior Tempo de Parada',
        width=800,
        xaxis=dict(title='Equipamento'),
        yaxis=dict(title='Tempo Total de Parada (horas)'),
        yaxis2=dict(
            title='Acumulado (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        height=400,
        legend=dict(x=1, y=1, orientation='v', bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=50, b=30, l=40, r=30),
        template="plotly_white"
    )

    return fig

def gerar_mapa_calor(df: pd.DataFrame):
    df['AnoMes'] = df['Data hora in'].dt.to_period("M").astype(str)
    df_heat = df.groupby(['Equipamento', 'AnoMes'])['Duracao_horas'].sum().reset_index()

    fig = px.density_heatmap(
        df_heat,
        x="AnoMes",
        y="Equipamento",
        z="Duracao_horas",
        title="Mapa de Calor - Horas Paradas por Equipamento e Mês",
        labels={"Duracao_horas": "Horas Paradas"},
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        xaxis_title="Mês/Ano",
        yaxis_title="Equipamento",
        height=400,
        margin=dict(t=40, b=40, l=40, r=40),
        template="plotly_white"
    )
    return fig