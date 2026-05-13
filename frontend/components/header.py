"""Componente de cabecera de la aplicación"""
import streamlit as st
from frontend.config import TITLE, LOGO_PATH

def render_header():
    """Renderiza el logo y el título principal"""
    col_logo1, col_logo2, col_logo3 = st.columns([2, 1, 2])
    with col_logo2:
        st.markdown('<div class="main-logo">', unsafe_allow_html=True)
        st.image(LOGO_PATH, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    st.title(TITLE)
    st.markdown("---")
