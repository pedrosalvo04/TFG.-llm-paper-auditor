"""Punto de entrada principal de la aplicación"""
import streamlit as st
from frontend.utils.system_config import setup_environment
from frontend.config import PAGE_TITLE

# 1. Configuración de entorno y página (DEBE ser lo primero)
setup_environment()
st.set_page_config(
    page_title=PAGE_TITLE,
    layout="wide",
    page_icon="🔬"
)

# 2. Importaciones de configuración y estilos
from frontend.styles.custom_css import apply_custom_styles
from frontend.utils.session_state import initialize_session_state

# 3. Inicialización con pantalla de carga
if 'initialized' not in st.session_state:
    from frontend.components.loader import render_initial_loader
    loading_placeholder = render_initial_loader()
    
    apply_custom_styles()
    initialize_session_state()
    
    st.session_state.initialized = True
    loading_placeholder.empty()
else:
    apply_custom_styles()
    initialize_session_state()

from frontend.components.sidebar import render_sidebar

# 4. Importación de componentes de UI
from frontend.components.header import render_header
from frontend.components.file_uploader import extract_text_from_file, run_audit
from frontend.components.audit_results import render_audit_results, generate_report
from frontend.components.sota_section import render_sota_analysis
from frontend.components.chatbot import render_chatbot

# 4. Renderizado de la App
render_sidebar()
render_header()

uploaded_file = st.file_uploader(
    "Sube el artículo científico (PDF, TXT o Markdown)", 
    type=["pdf", "txt", "md"]
)

if uploaded_file:
    md_text = extract_text_from_file(uploaded_file)
    
    if not st.session_state.get('resultado'):
        st.info("📄 Archivo cargado correctamente. Pulsa 'Iniciar Auditoría' para comenzar el análisis.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            is_auditing = st.session_state.get('audit_in_progress', False)
            btn_label = "⏳ Auditando..." if is_auditing else "🚀 Iniciar Auditoría"
            
            if st.button(btn_label, width="stretch", key="start_audit_btn", type="primary", disabled=is_auditing):
                st.session_state.audit_in_progress = True
                st.rerun()
        
        if st.session_state.get('audit_in_progress'):
            run_audit(md_text)
            st.session_state.audit_in_progress = False
            st.rerun()
    else:
        if st.button("🔄 Nueva Auditoría / Cambiar Opciones"):
            st.session_state.resultado = None
            st.rerun()

    # Resultados y herramientas adicionales
    resultado = st.session_state.get('resultado')
    md_text = st.session_state.get('md_text')
    
    if resultado:
        if "error" in resultado or "evaluation_error" in resultado:
            error_msg = resultado.get("error") or resultado.get("evaluation_error")
            st.error(f"❌ Error: {error_msg}")
        elif resultado.get("claims"):
            puntuacion = render_audit_results(resultado, uploaded_file)
            render_sota_analysis(md_text)
            render_chatbot(md_text)
            
            st.markdown("---")
            st.subheader("📄 Descargar Informe")
            reporte = generate_report(resultado, uploaded_file, puntuacion)
            st.download_button(
                label="📥 Descargar Informe Completo (.md)",
                data=reporte,
                file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md",
                mime="text/markdown"
            )
