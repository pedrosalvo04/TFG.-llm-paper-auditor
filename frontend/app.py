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
if st.button("🔄 Limpiar y subir nuevo archivo"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

uploaded_file = st.file_uploader("Sube el PDF del artículo científico", type=["pdf", "txt", "md"])

if uploaded_file:
    md_text, resultado = process_uploaded_file(uploaded_file)
if uploaded_file:
    md_text, resultado = process_uploaded_file(uploaded_file)
    
    # Verificar errores primero
    if resultado and "error" in resultado:
        st.error(f"❌ Error en la auditoría: {resultado['error']}")
    elif resultado and "evaluation_error" in resultado:
        st.error(f"❌ Error del LLM: {resultado['evaluation_error']}")
        st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")
        st.info("💡 Tip: Recarga la página o sube el archivo nuevamente.")
    elif resultado and resultado.get("peer_review_scores") and len(resultado["peer_review_scores"]) > 0:
        # Renderizar resultados
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
    elif resultado:
        st.error("⚠️ La auditoría no generó resultados válidos.")
        st.info("Posibles causas: respuesta vacía del LLM o JSON inválido.")
    else:
        st.warning("⚠️ No hay resultado disponible.")

# Barra lateral
with st.sidebar:
    st.image(SIDEBAR_IMAGE, width=150)
    st.markdown("### Sobre el TFG")
    st.write(SIDEBAR_DESCRIPTION)
