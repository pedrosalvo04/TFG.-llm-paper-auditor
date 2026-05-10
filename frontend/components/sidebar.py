"""Componente de barra lateral"""
import streamlit as st
from frontend.config import SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION

def render_sidebar():
    """Renderiza la barra lateral con información del proyecto"""
    with st.sidebar:
        st.image(SIDEBAR_IMAGE, width=150)
        st.markdown("### Sobre el TFG")
        st.write(SIDEBAR_DESCRIPTION)
