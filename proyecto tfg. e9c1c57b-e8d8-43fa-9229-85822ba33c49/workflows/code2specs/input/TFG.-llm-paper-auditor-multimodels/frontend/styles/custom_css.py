"""Estilos CSS personalizados para la aplicación"""
import streamlit as st

CUSTOM_CSS = """
    <style>
    /* Fondo general de la app */
    .stApp {
        background-color: #374151 !important; 
    }

    /* Limpiamos la interfaz */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {background-color: transparent !important;} 
    
    /* 🎨 1. CONTENEDOR DE LA TABLA */
    [data-testid="stTable"] {
        background-color: #2d3436 !important;
        border-radius: 15px !important; 
        padding: 5px !important;
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
        background-color: #3d4446 !important;
        border: 1px solid #4a4a4a !important; 
        padding: 12px !important;
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
        background-color: #2d3436 !important;
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

    /* 🎨 4. FONDO DEL GRÁFICO (A juego con la tabla) */
    [data-testid="stPlotlyChart"] {
        background-color: #2d3436 !important; 
        border-radius: 15px !important; 
        padding: 10px !important; 
    }
    </style>
"""

def apply_custom_styles():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
