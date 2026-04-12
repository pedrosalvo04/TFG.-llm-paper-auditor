"""Aplicación principal del Auditor de Papers - Frontend Modular"""
import streamlit as st

# IMPORTANTE: configure_page() debe ser lo primero
st.set_page_config(
    page_title="Nature Auditor Pro",
    layout="wide",
    page_icon="🔬"
)

from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION
from frontend.styles.custom_css import apply_custom_styles
from frontend.utils.session_state import initialize_session_state
from frontend.components.file_uploader import process_uploaded_file
from frontend.components.audit_results import render_audit_results, generate_report
from frontend.components.sota_section import render_sota_analysis
from frontend.components.chatbot import render_chatbot

# Configuración inicial
apply_custom_styles()
initialize_session_state()

# Título principal
st.title(TITLE)
st.markdown("---")

# Carga de archivo
uploaded_file = st.file_uploader("Sube el PDF del artículo científico", type="pdf")

if uploaded_file:
    md_text, resultado = process_uploaded_file(uploaded_file)
    
    if "revision" in resultado:
        puntuacion = render_audit_results(resultado, uploaded_file)
        render_sota_analysis(md_text)
        render_chatbot(md_text)
        
        # Descarga del informe
        st.markdown("---")
        st.subheader("📄 Descargar Informe")
        reporte = generate_report(resultado, uploaded_file, puntuacion)
        st.download_button(
            label="📥 Descargar Informe Completo (.md)",
            data=reporte,
            file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md",
            mime="text/markdown"
        )
    elif "error" in resultado:
        st.error(f"Error en la auditoría: {resultado['error']}")

# Barra lateral
with st.sidebar:
    st.image(SIDEBAR_IMAGE, width=150)
    st.markdown("### Sobre el TFG")
    st.write(SIDEBAR_DESCRIPTION)
