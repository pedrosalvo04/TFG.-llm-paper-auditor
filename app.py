"""Punto de entrada principal de la aplicación"""
import streamlit as st
import warnings
import logging
import os

# Eliminar logs molestos de transformers y huggingface
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", message=".*Accessing.*__path__.*")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("transformers").setLevel(logging.ERROR)

# Desactivar telemetría de ChromaDB y OpenTelemetry para evitar conflictos en Streamlit
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["OTEL_SDK_DISABLED"] = "true"

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
uploaded_file = st.file_uploader(
    "Sube el artículo científico (PDF, TXT o Markdown)", 
    type=["pdf", "txt", "md"]
)

if uploaded_file:
    process_uploaded_file(uploaded_file)
    
    # Acceder directamente desde session_state como en el original
    resultado = st.session_state.get('resultado')
    md_text = st.session_state.get('md_text')
    
    if resultado and "error" in resultado:
        st.error(f"❌ Error en la auditoría: {resultado['error']}")
    elif resultado and "evaluation_error" in resultado:
        st.error(f"❌ Error del LLM: {resultado['evaluation_error']}")
        st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")
    elif resultado and resultado.get("peer_review_scores") and len(resultado["peer_review_scores"]) > 0:
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
        st.json(resultado)

# Barra lateral
with st.sidebar:
    st.image(SIDEBAR_IMAGE, width=150)
    st.markdown("### Sobre el TFG")
    st.write(SIDEBAR_DESCRIPTION)
