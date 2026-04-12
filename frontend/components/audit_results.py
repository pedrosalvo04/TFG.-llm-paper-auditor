"""Componente de visualización de resultados de auditoría"""
import streamlit as st
import pandas as pd
from frontend.components.gauge_chart import create_gauge_chart
from frontend.utils.scoring import calcular_puntuacion

def render_audit_results(resultado, uploaded_file):
    """Renderiza los resultados de la auditoría con el medidor y la tabla de criterios"""
    st.success("Auditoría Finalizada")
    
    puntuacion = calcular_puntuacion(resultado["revision"])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(f"🏁 Veredicto: {uploaded_file.name}")
        st.info(resultado.get("veredicto_final", ""))
        st.plotly_chart(create_gauge_chart(puntuacion), use_container_width=True)
        
        tiempo = resultado.get('metricas', {}).get('tiempo_segundos', 'N/A')
        caracteres = resultado.get('metricas', {}).get('caracteres_leidos', 'N/A')
        st.caption(f"⏱️ **Tiempo IA:** {tiempo}s | 📄 **Caracteres:** {caracteres}")
    
    with col2:
        st.subheader("📊 Desglose de Criterios")
        df = pd.DataFrame(resultado["revision"])
        df = df[["categoria", "estado", "hallazgo", "recomendacion"]]
        df.set_index("categoria", inplace=True)
        st.table(df)
    
    return puntuacion

def generate_report(resultado, uploaded_file, puntuacion):
    """Genera el informe descargable en formato Markdown"""
    reporte = f"# Informe de Auditoría: {uploaded_file.name}\n\n"
    reporte += f"**Índice de Reproducibilidad:** {puntuacion}%\n\n"
    reporte += f"## Veredicto Final\n{resultado.get('veredicto_final', '')}\n\n"
    reporte += "## Detalles de la Revisión\n\n"
    
    for item in resultado["revision"]:
        reporte += f"### {item['categoria']}\n"
        reporte += f"- **Estado:** {item['estado']}\n"
        reporte += f"- **Hallazgo:** {item['hallazgo']}\n"
        reporte += f"- **Recomendación:** {item['recomendacion']}\n\n"
    
    return reporte
