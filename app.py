import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go
from src.parser import convert_pdf_to_markdown
from src.validator import PaperAuditor

st.set_page_config(page_title="Nature Auditor Pro", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stTable { background-color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Auditor Integral de Manuscritos")
st.markdown("---")

if 'auditor' not in st.session_state:
    st.session_state.auditor = PaperAuditor()

def calcular_puntuacion(revision):
    """Calcula la nota sobre 100% basándose en los estados, ignorando N/A."""
    puntos = 0
    aplicables = 0
    
    for item in revision:
        estado = item.get("estado", "").upper()
        if "N/A" in estado or "NO APLICA" in estado or "⚪" in estado:
            continue # Ignoramos los que no aplican
            
        aplicables += 1
        if "CUMPLE" in estado and "NO" not in estado:
            puntos += 1
        elif "PARCIAL" in estado:
            puntos += 0.5
            
    if aplicables == 0: return 0
    return int((puntos / aplicables) * 100)

def dibujar_medidor(score):
    """Dibuja un gráfico circular tipo velocímetro con Plotly."""
    if score >= 80:
        color_barra = "#00cc44" # Verde
    elif score >= 50:
        color_barra = "#ff9900" # Naranja
    else:
        color_barra = "#ff4b4b" # Rojo

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Índice de Reproducibilidad", 'font': {'size': 20}},
        number = {'suffix': "%", 'font': {'size': 40}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color_barra},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 75, 75, 0.1)"},
                {'range': [50, 80], 'color': "rgba(255, 153, 0, 0.1)"},
                {'range': [80, 100], 'color': "rgba(0, 204, 68, 0.1)"}],
        }
    ))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
    return fig

uploaded_file = st.file_uploader("Sube el PDF del artículo científico", type="pdf")

if uploaded_file:
    if not os.path.exists("temp"):
        os.makedirs("temp")
    temp_path = os.path.join("temp", uploaded_file.name)

    with st.status("🚀 Procesando documento...", expanded=True) as status:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("📂 Extrayendo texto y tablas...")
        md_text = convert_pdf_to_markdown(temp_path)
        
        st.write("🧠 Auditando con la Checklist de Nature...")
        resultado = st.session_state.auditor.audit(md_text)
        
        status.update(label="✅ Análisis completado", state="complete", expanded=False)

    if "revision" in resultado:
        st.success("Auditoría Finalizada")
        
        # Calculamos la puntuación
        puntuacion = calcular_puntuacion(resultado["revision"])
        
        # DISEÑO EN COLUMNAS: Izquierda (Veredicto y Gráfico), Derecha (Tabla)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🏁 Veredicto Principal")
            st.info(resultado.get("veredicto_final", ""))
            
            # Dibujamos el gráfico
            st.plotly_chart(dibujar_medidor(puntuacion), use_container_width=True)
            
        with col2:
            st.subheader("📊 Desglose de Criterios")
            df = pd.DataFrame(resultado["revision"])
            df = df[["categoria", "estado", "hallazgo", "recomendacion"]]
            st.dataframe(df, use_container_width=True, hide_index=True)

        # Preparación del informe para descarga
        reporte_descargable = f"# Informe de Auditoría: {uploaded_file.name}\n\n"
        reporte_descargable += f"**Índice de Reproducibilidad:** {puntuacion}%\n\n"
        reporte_descargable += f"## Veredicto Final\n{resultado.get('veredicto_final', '')}\n\n"
        reporte_descargable += "## Detalles de la Revisión\n\n"
        
        for item in resultado["revision"]:
            reporte_descargable += f"### {item['categoria']}\n"
            reporte_descargable += f"- **Estado:** {item['estado']}\n"
            reporte_descargable += f"- **Hallazgo:** {item['hallazgo']}\n"
            reporte_descargable += f"- **Recomendación:** {item['recomendacion']}\n\n"

        st.markdown("---")
        st.download_button(
            label="📥 Descargar Informe Completo (.md)",
            data=reporte_descargable,
            file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md",
            mime="text/markdown"
        )
        
    elif "error" in resultado:
        st.error(f"Error en la auditoría: {resultado['error']}")

    if os.path.exists(temp_path):
        os.remove(temp_path)

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nature_Logo_2020.svg/1200px-Nature_Logo_2020.svg.png", width=150)
    st.markdown("### Sobre el TFG")
    st.write("Herramienta desarrollada para automatizar la auditoría de transparencia en artículos científicos usando LLMs.")