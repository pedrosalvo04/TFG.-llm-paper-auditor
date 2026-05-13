"""Componente de carga y procesamiento de archivos (PDF, TXT, MD)"""
import streamlit as st
import os
from backend.services.pdf_parser import convert_pdf_to_markdown

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
                return None, {'error': f'Formato no soportado: {file_extension}'}
        
        # Auditar con logs de progreso
        with st.status("🧠 Analizando el documento...", expanded=True) as status:
            def update_status(msg):
                st.write(msg)
            
            st.session_state.resultado = st.session_state.auditor.audit(
                st.session_state.md_text, 
                status_callback=update_status
            )
            
            # Si hubo un error en la auditoría, verificamos si es por saturación
            resultado = st.session_state.resultado
            if resultado and "error" in resultado:
                error_msg = str(resultado['error'])
                
                # Detectar errores de saturación/demanda (503, 429, etc)
                is_saturation = any(x in error_msg.upper() for x in ["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"])
                
                if is_saturation:
                    status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)
                    st.error("### ⚠️ El servicio de IA está saturado")
                    
                    with st.expander("🔍 Detalles técnicos y solución", expanded=True):
                        st.write("El modelo Gemini está experimentando una demanda extremadamente alta en este momento y no ha podido completar la tarea tras 5 reintentos automáticos.")
                        st.info("Este es un problema temporal de Google. Puedes esperar unos minutos e intentar reanudar, o cancelar la ejecución actual.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Reintentar ahora", use_container_width=True):
                            st.rerun()
                    with col2:
                        if st.button("🚫 Cancelar ejecución", use_container_width=True):
                            st.session_state.resultado = {"error": "Ejecución cancelada por el usuario debido a saturación de API."}
                            st.stop()
                    
                    st.stop() # Detener flujo normal si hay error de saturación
                else:
                    # Otros errores generales
                    status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)
                    st.error(f"❌ Error crítico: {error_msg}")
                    # Limpiar resultados anteriores para no mostrar datos inconsistentes
                    st.session_state.resultado = {"error": error_msg}
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    st.stop()
            
            status.update(label="✅ Análisis completado", state="complete", expanded=False)
            
        st.success("✅ Análisis completado")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    # Siempre retornar desde session_state
    md_text = st.session_state.get('md_text', '')
    resultado = st.session_state.get('resultado', {})
    
    return md_text, resultado
