"""Componente de gráfico medidor de calidad NeurIPS"""
import plotly.graph_objects as go

def create_gauge_chart(score):
    """Crea un gráfico de medidor (gauge) para mostrar la calidad del paper según NeurIPS"""
    # Escala NeurIPS realista:
    # 87.5-100%: Strong Accept (verde oscuro)
    # 75-87.5%: Accept (verde)
    # 62.5-75%: Borderline (amarillo)
    # 50-62.5%: Weak Reject (naranja)
    # 25-50%: Reject (rojo)
    # 0-25%: Strong Reject (rojo oscuro)
    
    if score >= 87.5:
        color_barra = "#00aa00"  # Verde oscuro - Strong Accept
        label = "Strong Accept"
    elif score >= 75:
        color_barra = "#00cc44"  # Verde - Accept
        label = "Accept"
    elif score >= 62.5:
        color_barra = "#ffcc00"  # Amarillo - Borderline
        label = "Borderline"
    elif score >= 50:
        color_barra = "#ff9900"  # Naranja - Weak Reject
        label = "Weak Reject"
    elif score >= 25:
        color_barra = "#ff4b4b"  # Rojo - Reject
        label = "Reject"
    else:
        color_barra = "#cc0000"  # Rojo oscuro - Strong Reject
        label = "Strong Reject"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Quality Score<br><sub>{label}</sub>", 'font': {'size': 18}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 10, 'tickmode': 'linear', 'tick0': 0, 'dtick': 25},
            'bar': {
                'color': color_barra,
                'thickness': 0.8,
                'line': {'color': "black", 'width': 2}
            },
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 25], 'color': "rgba(204, 0, 0, 0.2)"},      # Strong Reject
                {'range': [25, 50], 'color': "rgba(255, 75, 75, 0.2)"},   # Reject
                {'range': [50, 62.5], 'color': "rgba(255, 153, 0, 0.2)"}, # Weak Reject
                {'range': [62.5, 75], 'color': "rgba(255, 204, 0, 0.2)"}, # Borderline
                {'range': [75, 87.5], 'color': "rgba(0, 204, 68, 0.2)"},  # Accept
                {'range': [87.5, 100], 'color': "rgba(0, 170, 0, 0.2)"}   # Strong Accept
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 62.5  # Línea en Borderline
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#E5E7EB"}
    )
    return fig
