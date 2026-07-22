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

from frontend.components.header import render_header
from frontend.components.file_uploader import extract_text_from_file, run_audit
from frontend.components.audit_results import render_audit_results, generate_report
from frontend.utils.pdf_generator import generate_pdf_report
from frontend.components.sota_section import render_sota_analysis

render_sidebar()
render_header()

# 5. Configuración de la Auditoría
st.subheader("Configuración")
criteria_mode = st.radio(
    "Selecciona el modo de evaluación:",
    options=["neurips", "free"],
    format_func=lambda x: "NeurIPS 2026 (Por defecto)" if x == "neurips" else "Criterios Libres"
)

criteria_text = None
if criteria_mode == "free":
    from frontend.components.file_uploader import extract_text_from_file_generic
    criteria_file = st.file_uploader(
        "Sube el documento con los criterios (PDF, TXT o Markdown)", 
        type=["pdf", "txt", "md"],
        key="criteria_uploader"
    )
    if criteria_file:
        criteria_text = extract_text_from_file_generic(criteria_file)
        if not criteria_text:
            st.warning("No se pudo extraer texto del archivo de criterios.")
    else:
        st.info("Sube un archivo con los criterios de evaluación para continuar.")

st.markdown("---")
# Carga de Documento Principal
uploaded_files = st.file_uploader(
    "Sube el/los artículo(s) científico(s) a auditar (PDF, TXT o Markdown)", 
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

# Solo ejecutar si tenemos el paper y, si es modo free, también los criterios
can_run = len(uploaded_files) > 0 and (criteria_mode == "neurips" or (criteria_mode == "free" and criteria_text))

if can_run:
    if len(uploaded_files) == 1:
        uploaded_file = uploaded_files[0]
        current_file_hash = f"{uploaded_file.name}_{criteria_mode}"
        if criteria_mode == "free" and criteria_file:
            current_file_hash += f"_{criteria_file.name}"
            
        if st.session_state.get('last_file_hash') != current_file_hash:
            st.session_state.resultado = None
            if 'sota_results' in st.session_state:
                del st.session_state.sota_results
            st.session_state.last_file_hash = current_file_hash

        md_text = extract_text_from_file(uploaded_file)
        
        # Iniciar auditoría automáticamente si no hay resultados y no está en progreso
        if md_text and not st.session_state.get('resultado') and not st.session_state.get('audit_in_progress'):
            st.session_state.audit_in_progress = True
            run_audit(md_text, criteria_mode, criteria_text)
            st.session_state.audit_in_progress = False
            st.rerun()
        else:
            if st.button("🔄 Nueva Auditoría / Forzar Recálculo"):
                st.session_state.resultado = None
                if 'sota_results' in st.session_state:
                    del st.session_state.sota_results
                st.rerun()

            # 6. Renderizar Resultados (Modo individual)
            if st.session_state.get('resultado'):
                resultado = st.session_state.resultado
                
                if "error" in resultado:
                    st.error(f"❌ La auditoría falló: {resultado['error']}")
                else:
                    # Mostrar tabla visual
                    puntuacion = render_audit_results(resultado, uploaded_file)
                    
                    # Renderizar sección de análisis del Estado del Arte (SOTA)
                    render_sota_analysis(md_text)
                    
                    st.markdown("---")
                    st.subheader("📄 Descargar Informe")
                    col_md, col_pdf = st.columns(2)
                    
                    with col_md:
                        reporte_md = generate_report(resultado, uploaded_file, puntuacion)
                        st.download_button(
                            label="📥 Descargar Informe Markdown (.md)",
                            data=reporte_md,
                            file_name=f"auditoria_gemini_basico_{uploaded_file.name.replace('.pdf', '')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                        
                    with col_pdf:
                        with st.spinner("Compilando PDF..."):
                            try:
                                reporte_pdf = generate_pdf_report(resultado, uploaded_file, puntuacion)
                                st.download_button(
                                    label="📥 Descargar Informe PDF (.pdf)",
                                    data=reporte_pdf,
                                    file_name=f"auditoria_gemini_basico_{uploaded_file.name.replace('.pdf', '')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            except Exception as pdf_error:
                                st.error(f"Error al generar PDF: {str(pdf_error)}")
    else:
        # Modo Lote (Batch)
        st.info(f"📁 Modo Lote Activo: {len(uploaded_files)} artículos cargados.")
        if st.button(f"🚀 Procesar {len(uploaded_files)} documentos secuencialmente"):
            st.session_state.audit_in_progress = True
            progress_bar = st.progress(0, text="Iniciando procesamiento en lote...")
            
            for i, f in enumerate(uploaded_files):
                progress_bar.progress(i / len(uploaded_files), text=f"⏳ Procesando {i+1}/{len(uploaded_files)}: {f.name}...")
                
                # Resetear resultado por si acaso para forzar un calculo limpio
                st.session_state.archivo_actual = "" # Forzar a que extract_text_from_file lo procese de nuevo
                st.session_state.file_hash = ""
                st.session_state.resultado = None
                
                md_text = extract_text_from_file(f)
                
                if md_text:
                    run_audit(md_text, criteria_mode, criteria_text)
                    st.success(f"✅ {f.name} procesado y guardado correctamente.")
                    
            progress_bar.progress(1.0, text="✅ Procesamiento en lote completado.")
            st.session_state.audit_in_progress = False
            st.success("🎉 Todos los documentos han sido procesados y guardados automáticamente en tu escritorio (C:\\Users\\pedro\\Desktop\\papers IA resultado).")
