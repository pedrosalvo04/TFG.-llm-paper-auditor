"""Componente de carga y procesamiento de archivos (PDF, TXT, MD)"""
import streamlit as st
import os
from backend.services.pdf_parser import convert_pdf_to_structured

def process_uploaded_file(uploaded_file):
    """Procesa el archivo subido (PDF, TXT, MD) y guarda el resultado en session_state"""
    import hashlib
    
    # Calcular hash del contenido para detectar cambios
    file_content = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_content).hexdigest()
    
    # Verificar si es un archivo nuevo o diferente
    if ("archivo_actual" not in st.session_state or 
        st.session_state.archivo_actual != uploaded_file.name or
        st.session_state.get('file_hash') != file_hash):
        
        st.session_state.archivo_actual = uploaded_file.name
        st.session_state.file_hash = file_hash
        st.session_state.messages = []
        st.session_state.structural_chunks = []  # Reset chunks estructurales
        
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        temp_path = os.path.join("temp", uploaded_file.name)
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Guardar archivo
        with open(temp_path, "wb") as f:
            f.write(file_content)
        
        # Procesar según el tipo de archivo
        with st.spinner("📂 Extrayendo texto y estructura del documento..."):
            if file_extension == 'pdf':
                # Extracción estructural: markdown + chunks de Docling (secciones + tablas)
                md_text, structural_chunks = convert_pdf_to_structured(temp_path)
                st.session_state.md_text = md_text
                st.session_state.structural_chunks = structural_chunks
                if structural_chunks:
                    n_tables = sum(1 for c in structural_chunks if getattr(c, 'chunk_type', '') == 'table')
                    n_sections = sum(1 for c in structural_chunks if getattr(c, 'chunk_type', '') == 'section')
                    st.toast(
                        f"🏗️ Estructura extraída: {n_sections} secciones, {n_tables} tablas",
                        icon="📊"
                    )
            elif file_extension in ['txt', 'md']:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    st.session_state.md_text = f.read()
                st.session_state.structural_chunks = []  # Sin chunks para texto plano
            else:
                st.error(f"❌ Formato no soportado: {file_extension}")
                return None, {'error': f'Formato no soportado: {file_extension}'}
        
        # Auditar (pasar structural_chunks al auditor)
        with st.spinner("🧠 Analizando el documento..."):
            st.session_state.resultado = st.session_state.auditor.audit(
                st.session_state.md_text,
                structural_chunks=st.session_state.get('structural_chunks', [])
            )
        
        st.success("✅ Análisis completado")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    # Siempre retornar desde session_state
    md_text = st.session_state.get('md_text', '')
    resultado = st.session_state.get('resultado', {})
    
    return md_text, resultado
