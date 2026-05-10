"""Componente de carga y procesamiento de archivos (PDF, TXT, MD)"""
import streamlit as st
import os
from backend.services.pdf_parser import convert_pdf_to_markdown

def extract_text_from_file(uploaded_file):
    """Extrae el texto del archivo subido (PDF, TXT, MD) y lo guarda en session_state"""
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
        st.session_state.resultado = None # Resetear resultado al subir nuevo archivo
        st.session_state.md_text = None
        
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        temp_path = os.path.join("temp", uploaded_file.name)
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Guardar archivo
        with open(temp_path, "wb") as f:
            f.write(file_content)
        
        # Procesar según el tipo de archivo
        with st.spinner("📂 Extrayendo texto..."):
            if file_extension == 'pdf':
                st.session_state.md_text = convert_pdf_to_markdown(temp_path)
            elif file_extension in ['txt', 'md']:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    st.session_state.md_text = f.read()
            else:
                st.error(f"❌ Formato no soportado: {file_extension}")
                return None
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return st.session_state.get('md_text')

def run_audit(md_text, use_rag=True):
    """Ejecuta el proceso de auditoría sobre el texto proporcionado"""
    if not md_text:
        st.error("⚠️ No hay texto para auditar.")
        return None

    # Auditar con logs de progreso
    with st.status("🧠 Analizando el documento...", expanded=True) as status:
        from frontend.components.phase_tracker import get_phase_tracker_html
        
        # El tracker se queda fijo arriba de los logs dentro del status
        tracker_placeholder = st.empty()
        st.markdown("---") # Separador visual
        
        def update_status(msg, phase_index=None):
            # Escribir el log
            st.write(msg)
            
            # Actualizar el tracker en la parte superior
            if phase_index is not None:
                tracker_placeholder.markdown(get_phase_tracker_html(phase_index), unsafe_allow_html=True)
        
        # Inicializar el tracker
        tracker_placeholder.markdown(get_phase_tracker_html(0), unsafe_allow_html=True)
            
        try:
            st.session_state.resultado = st.session_state.auditor.audit(
                md_text, 
                status_callback=update_status,
                use_rag=use_rag
            )
            
            # Si hubo un error en la auditoría, verificamos si es por saturación
            resultado = st.session_state.resultado
            if resultado and "error" in resultado:
                error_msg = str(resultado['error'])
                
                # Detectar errores de saturación/demanda
                is_saturation = any(x in error_msg.upper() for x in ["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"])
                
                if is_saturation:
                    status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)
                    st.error("### ⚠️ El servicio de IA está saturado")
                    
                    with st.expander("🔍 Detalles técnicos y solución", expanded=True):
                        st.write("El modelo Gemini está experimentando una demanda extremadamente alta. Intentos fallidos tras 5 reintentos.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Reintentar ahora", width="stretch"):
                            st.rerun()
                    with col2:
                        if st.button("🚫 Cancelar ejecución", width="stretch"):
                            st.session_state.resultado = {"error": "Ejecución cancelada por el usuario."}
                            st.stop()
                    
                    st.stop()
                else:
                    status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)
                    st.error(f"❌ Error crítico: {error_msg}")
                    st.session_state.resultado = {"error": error_msg}
                    st.stop()
            
            # Forzar actualización final del tracker
            tracker_placeholder.markdown(get_phase_tracker_html(7), unsafe_allow_html=True)
                
            status.update(label="✅ Análisis completado", state="complete", expanded=False)
            st.success("✅ Análisis completado")
            return st.session_state.resultado

        except Exception as e:
            # Solo capturamos si no es una interrupción de Streamlit
            status.update(label="❌ Error inesperado", state="error", expanded=True)
            st.error(f"❌ Error inesperado: {str(e)}")
            st.session_state.resultado = {"error": str(e)}
            return st.session_state.resultado

