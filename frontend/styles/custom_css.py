"""Estilos CSS personalizados para la aplicación"""
import streamlit as st

CUSTOM_CSS = """
    <style>
    /* Fondo general de la app con efecto Mesh Gradient moderno */
    .stApp {
        background-color: #0f172a !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(59, 130, 246, 0.1) 0px, transparent 50%),
            linear-gradient(to bottom, #0f172a, #1e293b) !important;
        background-attachment: fixed !important;
    }

    /* Sutil textura de rejilla profesional */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    header {background-color: transparent !important;} 

    /* 🖼️ ESTILO DEL LOGO PRINCIPAL */
    .main-logo img {
        border-radius: 20px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4) !important;
        transition: all 0.5s ease !important;
        animation: float 4s ease-in-out infinite;
    }
    
    .main-logo img:hover {
        transform: scale(1.05) rotate(2deg) !important;
        box-shadow: 0 20px 50px rgba(16, 185, 129, 0.2) !important;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* 🏆 TÍTULO PRINCIPAL PREMIUM */
    h1 {
        text-align: center !important;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        padding-top: 1rem !important;
        padding-bottom: 1.5rem !important;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    h1::after {
        content: "";
        display: block;
        width: 150px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #94a3b8, transparent);
        margin: 15px auto 0;
        border-radius: 10px;
        opacity: 0.5;
    }
    
    /* 🚀 BOTÓN DE INICIO (ANCHO, BAJO, FUENTE EXPANDIDA) */
    button[kind="primary"] {
        background-color: #064e3b !important; /* Verde Esmeralda Oscuro */
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
        padding: 0.1rem 5rem !important; /* Más ancho, menos alto */
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 25px rgba(6, 78, 59, 0.4) !important;
        width: 100% !important;
        min-height: 2.8rem !important; /* Altura muy reducida */
        line-height: 1 !important;
        letter-spacing: 2.5px !important; /* Equilibrio: ni tan juntas ni tan separadas */
        word-spacing: 8px !important;     /* Espacio sutil entre palabras */
        text-transform: uppercase !important;
    }

    button[kind="primary"]:hover {
        background-color: #10b981 !important; /* Verde Brillante */
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4) !important;
    }

    button[kind="primary"]:active {
        transform: translateY(0) !important;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* 🎨 1. CONTENEDORES PRINCIPALES (Tablas, Expanders, Alertas, Status) */
    [data-testid="stTable"], 
    [data-testid="stExpander"], 
    [data-testid="stMetric"],
    [data-testid="stStatusContainer"] {
        background-color: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important; 
        padding: 15px !important;
        border: none !important; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 1.2rem !important;
    }

    /* 🔔 ESTILO ESPECIAL PARA ALERTAS (st.info, st.success, etc) */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        border: none !important;
        border-left: 4px solid rgba(255, 255, 255, 0.3) !important; /* Línea neutral en lugar de azul */
        color: #FFFFFF !important;
    }
    .stAlert p {
        color: #FFFFFF !important;
        font-weight: 400 !important;
    }

    /* 🛡️ ELIMINACIÓN AGRESIVA DE BORDES EN EXPANDERS */
    [data-testid="stExpander"], 
    [data-testid="stExpander"] * {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Ajuste específico para Expanders (Header) */
    [data-testid="stExpander"] summary:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
    }

    /* 🛠️ EL TRUCO PARA ELIMINAR LÍNEAS DUPLICADAS */
    [data-testid="stTable"] table {
        border-collapse: collapse !important;
        width: 100% !important;
        border: none !important;
    }
    
    /* 💥 2. CABECERAS (Categoría, Estado, Hallazgo...) */
    [data-testid="stTable"] th {
        color: #FFFFFF !important;
        font-size: 16px !important; 
        font-weight: 800 !important; 
        background-color: #1f2937 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        padding: 14px !important;
        text-transform: capitalize !important;
    }
    [data-testid="stTable"] th * {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        text-decoration: none !important;
        border: none !important;
        text-transform: capitalize !important;
    }
    [data-testid="stTable"] tbody th {
        color: #FFFFFF !important;
        font-size: 16px !important;
        background-color: transparent !important;
    }
    [data-testid="stTable"] tbody th * {
        color: #FFFFFF !important;
        font-size: 16px !important;
        background-color: transparent !important;
    }

    /* 📝 3. CELDAS DE CONTENIDO (Puntos a analizar) */
    [data-testid="stTable"] td {
        color: #E2E8F0 !important; 
        font-size: 13.5px !important;
        font-weight: 400 !important; 
        background-color: transparent !important;
        border: 1px solid #4a4a4a !important; 
        padding: 12px !important;
    }
    [data-testid="stTable"] td * {
        color: #E2E8F0 !important;
        font-size: 13.5px !important;
        font-weight: 400 !important;
        text-decoration: none !important;
        border: none !important;
    }

    /* 🎨 4. FONDO DEL GRÁFICO (Estilo Coherente) */
    [data-testid="stPlotlyChart"] {
        background-color: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important; 
        padding: 15px !important; 
        border: none !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    }

    /* 🧭 PHASE TRACKER STYLES */
    .stepper-wrapper {
      display: flex;
      justify-content: space-between;
      margin-bottom: 25px;
      padding: 25px;
      background: rgba(255, 255, 255, 0.12) !important;
      backdrop-filter: blur(15px) !important;
      border-radius: 12px;
      border: none !important;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    }

    .stepper-item {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
      transition: all 0.3s ease;
    }

    .stepper-item::before {
      position: absolute;
      content: "";
      border-bottom: 2px solid #4a4a4a;
      width: 100%;
      top: 20px;
      left: -50%;
      z-index: 2;
    }

    .stepper-item::after {
      position: absolute;
      content: "";
      border-bottom: 2px solid #4a4a4a;
      width: 100%;
      top: 20px;
      left: 50%;
      z-index: 2;
    }

    .stepper-item:first-child::before {
      content: none;
    }

    .stepper-item:last-child::after {
      content: none;
    }

    .stepper-item .step-counter {
      position: relative;
      z-index: 5;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #4a4a4a; /* Gris para pendientes */
      color: #fff;
      margin-bottom: 6px;
      font-weight: bold;
      border: 2px solid #4a4a4a;
      transition: all 0.3s ease;
    }

    .stepper-item .step-name {
      color: #94a3b8;
      font-size: 11px;
      text-align: center;
      font-weight: 500;
    }

    /* States */
    .stepper-item.completed .step-counter {
      background-color: #23c483;
      border-color: #23c483;
      color: white;
    }

    .stepper-item.completed .step-name {
      color: #23c483;
    }

    .stepper-item.completed::after {
      border-bottom-color: #23c483;
    }

    .stepper-item.active .step-counter {
      background-color: #3b82f6;
      border-color: #3b82f6;
      color: white;
      box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
      animation: pulse 2s infinite;
    }

    .stepper-item.active .step-name {
      color: #3b82f6;
      font-weight: bold;
    }

    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.1); }
      100% { transform: scale(1); }
    }

    /* 🌀 LOADING SCREEN STYLES */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(55, 65, 81, 0.9);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999999 !important; /* Forzar por encima de todo Streamlit */
        backdrop-filter: blur(12px) !important;
    }

    .loader-card {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(16px) !important;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        border: 1px solid rgba(255, 255, 255, 0.12);
        text-align: center;
        max-width: 420px;
        animation: fadeIn 0.5s ease;
    }

    .loader-dna {
        width: 100px;
        height: 100px;
        margin: 0 auto 20px;
        position: relative;
    }

    /* DNA Animation using CSS */
    .dot {
        width: 12px;
        height: 12px;
        background: #3b82f6;
        border-radius: 50%;
        position: absolute;
        top: 50%; /* Centrar verticalmente en el contenedor DNA */
        animation: dna-bounce 2s infinite ease-in-out;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
    }

    .dot.strand-2 {
        background: #10b981;
        animation-delay: -1s !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }

    @keyframes dna-bounce {
        0%, 100% { transform: translateY(0) scale(0.8); opacity: 0.3; }
        50% { transform: translateY(-50px) scale(1.2); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .loading-text {
        color: #FFFFFF;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 15px;
        letter-spacing: 0.5px;
    }

    .loading-subtext {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 8px;
    }
    </style>
"""

def apply_custom_styles():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
