"""Componente de barra lateral"""
import streamlit as st
from frontend.config import SIDEBAR_DESCRIPTION

def render_sidebar():
    """Renderiza la barra lateral con información del proyecto"""
    with st.sidebar:
        st.markdown("## 🤖 IA Paper Auditor")
        st.markdown("---")
        
        st.markdown("### ℹ️ Sobre el Proyecto")
        st.info(SIDEBAR_DESCRIPTION)
        
        st.markdown("### 📖 ¿Cómo funciona?")
        with st.expander("Ver instrucciones", expanded=False):
            st.markdown(
                """
                1. **Configura la auditoría**: Elige entre usar los criterios por defecto (ej. NeurIPS) o sube tus propios criterios.
                2. **Sube tu Paper**: Carga el documento en formato PDF, TXT o Markdown.
                3. **Auditoría Automática**: El sistema evaluará el documento frente a los criterios y buscará posibles limitaciones u omisiones.
                4. **Revisión**: Analiza los resultados, puntuaciones y recomendaciones.
                5. **Descarga**: Exporta el reporte final de la auditoría.
                """
            )
            
        st.markdown("---")
        st.caption("Desarrollado para el Trabajo de Fin de Grado.")
