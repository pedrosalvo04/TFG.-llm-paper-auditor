"""Componente de carga y procesamiento de archivos PDF"""
import streamlit as st
import os
from backend.services.pdf_parser import convert_pdf_to_markdown

def process_uploaded_file(uploaded_file):
    """Procesa el archivo PDF subido y guarda el resultado en session_state"""
    # Verificar si es un archivo nuevo
    if "archivo_actual" not in st.session_state or st.session_state.archivo_actual != uploaded_file.name:
        st.session_state.archivo_actual = uploaded_file.name
        st.session_state.messages = []
        
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        temp_path = os.path.join("temp", uploaded_file.name)
        
        with st.status("🚀 Procesando documento...", expanded=True) as status:
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write("📂 Extrayendo texto y tablas...")
            st.session_state.md_text = convert_pdf_to_markdown(temp_path)
            
            st.write("🧠 Auditando con estándares de reproducibilidad computacional...")
            st.session_state.resultado = st.session_state.auditor.audit(st.session_state.md_text)
            
            status.update(label="✅ Análisis completado", state="complete", expanded=False)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
