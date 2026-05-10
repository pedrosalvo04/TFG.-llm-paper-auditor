"""Gestión del estado de sesión de Streamlit"""
import streamlit as st
from backend.services.auditor import PaperAuditor
from backend.services.chatbot import PaperChatbot
from backend.services.sota_analyzer import SotaAnalyzer

def initialize_session_state():
    """Inicializa todas las variables de estado de sesión necesarias"""
    if "resultado" not in st.session_state:
        st.session_state.resultado = None
    
    if 'auditor' not in st.session_state:
        st.session_state.auditor = PaperAuditor()
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = PaperChatbot()
    
    if 'sota_analyzer' not in st.session_state:
        st.session_state.sota_analyzer = SotaAnalyzer()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "audit_in_progress" not in st.session_state:
        st.session_state.audit_in_progress = False
