"""Punto de entrada principal de la aplicación"""
import streamlit as st
import warnings
import logging
import os

# iniciar env: .\.venv\Scripts\Activate.ps1
# ejecutar app: streamlit run app.py

#******************************************

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

# Pantalla de carga inicial (solo la primera vez)
if 'initialized' not in st.session_state:
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
        <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #0f172a !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%),
                radial-gradient(at 0% 100%, rgba(59, 130, 246, 0.1) 0px, transparent 50%) !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999999 !important;
            backdrop-filter: blur(20px) !important;
        }
        .loader-card {
            background: rgba(30, 41, 59, 0.7) !important;
            backdrop-filter: blur(16px) !important;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            width: 420px;
            animation: fadeIn 0.8s ease;
        }
        .loader-dna {
            width: 100%;
            height: 80px;
            margin-bottom: 25px;
            position: relative;
        }
        .dot {
            width: 16px;
            height: 16px;
            background: #3b82f6;
            border-radius: 50%;
            position: absolute;
            top: 40%;
            animation: dna-bounce 2s infinite ease-in-out;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
        }
        .dot.strand-2 {
            background: #10b981;
            animation-delay: -1s !important;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
        }
        @keyframes dna-bounce {
            0%, 100% { transform: translateY(0) scale(0.8); opacity: 0.4; }
            50% { transform: translateY(-45px) scale(1.4); opacity: 1; }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .loading-text {
            color: #FFFFFF;
            font-size: 1.5rem;
            font-weight: 800;
            margin-top: 20px;
            letter-spacing: -0.5px;
        }
        .loading-subtext {
            color: #94a3b8;
            font-size: 1rem;
            margin-top: 12px;
            font-weight: 400;
        }
        </style>
        <div class="loading-overlay">
            <div class="loader-card">
                <div class="loader-dna">
                    <!-- Strand 1 -->
                    <div class="dot" style="left: 15%; animation-delay: 0s;"></div>
                    <div class="dot" style="left: 32.5%; animation-delay: 0.2s;"></div>
                    <div class="dot" style="left: 50%; animation-delay: 0.4s;"></div>
                    <div class="dot" style="left: 67.5%; animation-delay: 0.6s;"></div>
                    <div class="dot" style="left: 85%; animation-delay: 0.8s;"></div>
                    <!-- Strand 2 -->
                    <div class="dot strand-2" style="left: 15%; animation-delay: 0s;"></div>
                    <div class="dot strand-2" style="left: 32.5%; animation-delay: 0.2s;"></div>
                    <div class="dot strand-2" style="left: 50%; animation-delay: 0.4s;"></div>
                    <div class="dot strand-2" style="left: 67.5%; animation-delay: 0.6s;"></div>
                    <div class="dot strand-2" style="left: 85%; animation-delay: 0.8s;"></div>
                </div>
                <div class="loading-text">Nature Auditor Pro</div>
                <div class="loading-subtext">Iniciando motor de análisis científico...</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Pequeño retardo para asegurar que la animación se vea
    import time
    time.sleep(2.5)
    
    # IMPORTACIÓN DIFERIDA: Solo importamos lo pesado mientras la pantalla de carga es visible
    from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION
    from frontend.styles.custom_css import apply_custom_styles
    from frontend.utils.session_state import initialize_session_state
    
    apply_custom_styles()
    initialize_session_state()
    st.session_state.initialized = True
    loading_placeholder.empty()
else:
    # Importación rápida para reruns
    from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION
    from frontend.styles.custom_css import apply_custom_styles
    from frontend.utils.session_state import initialize_session_state
    
    apply_custom_styles()
    initialize_session_state()

# Importar componentes de UI
from frontend.components.file_uploader import extract_text_from_file, run_audit
from frontend.components.audit_results import render_audit_results, generate_report
from frontend.components.sota_section import render_sota_analysis
from frontend.components.chatbot import render_chatbot

# Logo y Título principal
col_logo1, col_logo2, col_logo3 = st.columns([2, 1, 2])
with col_logo2:
    st.markdown('<div class="main-logo">', unsafe_allow_html=True)
    st.image("C:\\Users\\pedro\\.gemini\\antigravity\\brain\\c69d8679-6953-4d08-beab-6e93a072f601\\ai_paper_auditor_logo_1778356878673.png", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

st.title(TITLE)
st.markdown("---")

# Carga de archivo
uploaded_file = st.file_uploader(
    "Sube el artículo científico (PDF, TXT o Markdown)", 
    type=["pdf", "txt", "md"]
)

if uploaded_file:
    # 1. Extraer texto (esto es rápido y no gasta tokens de auditoría)
    md_text = extract_text_from_file(uploaded_file)
    
    # 2. Mostrar opciones y botón de inicio si no hay resultado previo
    if not st.session_state.get('resultado'):
        st.info("📄 Archivo cargado correctamente. Configura las opciones y pulsa 'Iniciar Auditoría'.")
        
        # Opciones encima del botón
        use_rag = st.toggle(
            "Utilizar RAG (Recomendado)", 
            value=False, 
            help="Extrae hiperparámetros y detalles técnicos con mayor precisión usando búsqueda semántica."
        )
        
        # Botón de inicio de auditoría
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            is_auditing = st.session_state.get('audit_in_progress', False)
            btn_label = "⏳ Auditando..." if is_auditing else "🚀 Iniciar Auditoría"
            
            if st.button(btn_label, width="stretch", key="start_audit_btn", type="primary", disabled=is_auditing):
                st.session_state.audit_in_progress = True
                st.rerun()
        
        # Ejecución diferida para que el botón se muestre como deshabilitado inmediatamente
        if st.session_state.get('audit_in_progress'):
            run_audit(md_text, use_rag=use_rag)
            st.session_state.audit_in_progress = False
            st.rerun()
    else:
        # Botón para resetear y volver a auditar si se desea
        if st.button("🔄 Nueva Auditoría / Cambiar Opciones"):
            st.session_state.resultado = None
            st.rerun()

    # 3. Mostrar resultados si existen
    resultado = st.session_state.get('resultado')
    md_text = st.session_state.get('md_text')
    
    if resultado and "error" in resultado:
        st.error(f"❌ Error en la auditoría: {resultado['error']}")
    elif resultado and "evaluation_error" in resultado:
        st.error(f"❌ Error del LLM: {resultado['evaluation_error']}")
        st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")
    elif resultado and resultado.get("claims"):
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
