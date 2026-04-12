"""Componente de gráfico medidor de reproducibilidad"""
import plotly.graph_objects as go

def create_gauge_chart(score):
    """Crea un gráfico de medidor (gauge) para mostrar el índice de reproducibilidad"""
    if score >= 80:
        color_barra = "#00cc44"
    elif score >= 50:
        color_barra = "#ff9900"
    else:
        color_barra = "#ff4b4b"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Índice de Reproducibilidad", 'font': {'size': 20}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 10},
            'bar': {
                'color': color_barra,
                'thickness': 1,
                'line': {'color': "black", 'width': 3}
            },
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 75, 75, 0.25)"},
                {'range': [50, 80], 'color': "rgba(255, 153, 0, 0.25)"},
                {'range': [80, 100], 'color': "rgba(0, 204, 68, 0.25)"}
            ],
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#E5E7EB"}
    )
    return fig
