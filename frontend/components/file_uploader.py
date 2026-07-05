"""Componente de carga y procesamiento de archivos (PDF, TXT, MD)"""
import streamlit as st
import os
from backend.services.pdf_parser import convert_pdf_to_markdown

def extract_text_from_file_generic(uploaded_file):
    """Extrae el texto de un archivo sin afectar el session_state global."""
    if not uploaded_file: return None
    
    file_content = uploaded_file.getvalue()
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    temp_path = os.path.join("temp", uploaded_file.name)
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    with open(temp_path, "wb") as f:
        f.write(file_content)
    
    extracted_text = None
    with st.spinner(f"📂 Leyendo {uploaded_file.name}..."):
        if file_extension == 'pdf':
            extracted_text = convert_pdf_to_markdown(temp_path)
        elif file_extension in ['txt', 'md']:
            with open(temp_path, 'r', encoding='utf-8') as f:
                extracted_text = f.read()
        else:
            st.error(f"❌ Formato no soportado: {file_extension}")
            
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    return extracted_text

def extract_text_from_file(uploaded_file):
    """Extrae el texto del archivo subido (PDF, TXT, MD) y lo guarda en session_state"""
    import hashlib
    
    # Calcular hash del contenido para detectar cambios
    file_content = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_content).hexdigest()
    
    # Verificar si es un archivo nuevo o diferente (o si cambiaron las opciones)
    if ("archivo_actual" not in st.session_state or 
        st.session_state.archivo_actual != uploaded_file.name or
        st.session_state.get('file_hash') != file_hash):
        
        st.session_state.archivo_actual = uploaded_file.name
        st.session_state.file_hash = file_hash
        st.session_state.messages = []
        st.session_state.resultado = None # Resetear resultado al subir nuevo archivo
        st.session_state.md_text = None
        st.session_state.uploaded_file_obj = uploaded_file # Guardar referencia para reportes
        
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

def run_audit(md_text, criteria_mode="neurips", criteria_text=None):
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
                criteria_mode=criteria_mode,
                criteria_text=criteria_text
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
            tracker_placeholder.markdown(get_phase_tracker_html(5), unsafe_allow_html=True)
                
            status.update(label="✅ Análisis completado", state="complete", expanded=False)
            st.success("✅ Análisis completado")

            # --- NUEVO: Guardar automáticamente en el escritorio ---
            try:
                from frontend.components.audit_results import generate_report
                from frontend.utils.scoring import get_checklist_health
                from frontend.utils.pdf_generator import generate_pdf_report
                
                health = get_checklist_health(st.session_state.resultado)
                reporte_contenido = generate_report(st.session_state.resultado, st.session_state.uploaded_file_obj, health)
                
                # Ruta solicitada por el usuario
                save_dir = r"C:\Users\pedro\Desktop\papers IA resultado"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                base_name = os.path.splitext(st.session_state.archivo_actual)[0]
                
                # Guardar reporte Markdown
                filename_md = f"auditoria_qwen2.5_basico_{base_name}.md"
                save_path_md = os.path.join(save_dir, filename_md)
                with open(save_path_md, "w", encoding="utf-8") as f:
                    f.write(reporte_contenido)
                
                # Guardar reporte PDF
                filename_pdf = f"auditoria_qwen2.5_basico_{base_name}.pdf"
                save_path_pdf = os.path.join(save_dir, filename_pdf)
                reporte_pdf = generate_pdf_report(st.session_state.resultado, st.session_state.uploaded_file_obj, health)
                with open(save_path_pdf, "wb") as f:
                    f.write(reporte_pdf)
                
                st.info(f"💾 Informes guardados automáticamente en: {save_dir}")
            except Exception as save_error:
                st.warning(f"⚠️ No se pudo guardar el informe automáticamente: {str(save_error)}")
            # -------------------------------------------------------

            return st.session_state.resultado

        except Exception as e:
            # Solo capturamos si no es una interrupción de Streamlit
            status.update(label="❌ Error inesperado", state="error", expanded=True)
            st.error(f"❌ Error inesperado: {str(e)}")
            st.session_state.resultado = {"error": str(e)}
            return st.session_state.resultado

def run_batch_audit(uploaded_files, criteria_mode="neurips", criteria_text=None):
    """Ejecuta el proceso de auditoría sobre múltiples archivos de manera silenciosa y guarda los resultados."""
    if not uploaded_files:
        st.error("⚠️ No hay archivos para procesar.")
        return

    total = len(uploaded_files)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    save_dir = r"C:\Users\pedro\Desktop\papers IA resultado"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    success_count = 0
    error_count = 0

    from frontend.components.audit_results import generate_report
    from frontend.utils.scoring import get_checklist_health
    from frontend.utils.pdf_generator import generate_pdf_report

    for i, file in enumerate(uploaded_files):
        status_text.text(f"Procesando {i+1}/{total}: {file.name}...")
        
        # 1. Extraer texto
        md_text = extract_text_from_file_generic(file)
        if not md_text:
            error_count += 1
            st.warning(f"No se pudo extraer texto de {file.name}")
            progress_bar.progress((i + 1) / total)
            continue

        # 2. Auditar silenciosamente (sin logs detallados para no sobrecargar UI)
        try:
            resultado = st.session_state.auditor.audit(
                md_text, 
                status_callback=None, # Silenciar logs
                criteria_mode=criteria_mode,
                criteria_text=criteria_text
            )
            
            if resultado and "error" not in resultado:
                # 3. Guardar reportes
                base_name = os.path.splitext(file.name)[0]
                health = get_checklist_health(resultado)
                
                # MD
                reporte_contenido = generate_report(resultado, file, health)
                save_path_md = os.path.join(save_dir, f"auditoria_qwen2.5_basico_{base_name}.md")
                with open(save_path_md, "w", encoding="utf-8") as f:
                    f.write(reporte_contenido)
                
                # PDF
                try:
                    reporte_pdf = generate_pdf_report(resultado, file, health)
                    save_path_pdf = os.path.join(save_dir, f"auditoria_qwen2.5_basico_{base_name}.pdf")
                    with open(save_path_pdf, "wb") as f:
                        f.write(reporte_pdf)
                except Exception as pdf_error:
                    st.warning(f"Aviso: No se pudo generar PDF para {file.name}: {pdf_error}")
                
                success_count += 1
            else:
                error_count += 1
                st.error(f"Error procesando {file.name}: {resultado.get('error', 'Desconocido')}")
                
        except Exception as e:
            error_count += 1
            st.error(f"Error inesperado en {file.name}: {str(e)}")

        progress_bar.progress((i + 1) / total)
    
    status_text.text("¡Procesamiento por lotes finalizado!")
    st.success(f"✅ Se procesaron {total} archivos. Éxitos: {success_count}. Errores: {error_count}.")
    st.info(f"💾 Todos los informes se han guardado en: {save_dir}")

def run_determinism_test(uploaded_file, criteria_mode="neurips", criteria_text=None):
    """Ejecuta el proceso de auditoría sobre el mismo archivo 9 veces y genera un ZIP."""
    import zipfile
    import io

    if not uploaded_file:
        st.error("⚠️ No hay archivo para procesar.")
        return None

    iterations = 9
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    save_dir = r"C:\Users\pedro\Desktop\papers IA resultado"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    success_count = 0
    error_count = 0

    from frontend.components.audit_results import generate_report
    from frontend.utils.scoring import get_checklist_health
    from frontend.utils.pdf_generator import generate_pdf_report
    
    # 1. Extraer texto
    md_text = extract_text_from_file_generic(uploaded_file)
    if not md_text:
        st.error(f"No se pudo extraer texto de {uploaded_file.name}")
        return None

    base_name = os.path.splitext(uploaded_file.name)[0]

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(iterations):
            status_text.text(f"Ejecutando iteración {i+1}/{iterations} de la prueba de determinismo...")
            
            try:
                resultado = st.session_state.auditor.audit(
                    md_text, 
                    status_callback=None, # Silenciar logs
                    criteria_mode=criteria_mode,
                    criteria_text=criteria_text
                )
                
                if resultado and "error" not in resultado:
                    health = get_checklist_health(resultado)
                    
                    # MD
                    reporte_contenido = generate_report(resultado, uploaded_file, health)
                    md_filename = f"determinismo_{base_name}_iter_{i+1}.md"
                    
                    # Guardar en disco local también por si acaso
                    save_path_md = os.path.join(save_dir, md_filename)
                    with open(save_path_md, "w", encoding="utf-8") as f:
                        f.write(reporte_contenido)
                        
                    # Añadir al ZIP
                    zip_file.writestr(md_filename, reporte_contenido)
                    
                    # PDF
                    try:
                        reporte_pdf = generate_pdf_report(resultado, uploaded_file, health)
                        pdf_filename = f"determinismo_{base_name}_iter_{i+1}.pdf"
                        
                        save_path_pdf = os.path.join(save_dir, pdf_filename)
                        with open(save_path_pdf, "wb") as f:
                            f.write(reporte_pdf)
                            
                        zip_file.writestr(pdf_filename, reporte_pdf)
                    except Exception as pdf_error:
                        st.warning(f"Aviso: No se pudo generar PDF para iteración {i+1}: {pdf_error}")
                    
                    success_count += 1
                else:
                    error_count += 1
                    st.error(f"Error en iteración {i+1}: {resultado.get('error', 'Desconocido')}")
                    
            except Exception as e:
                error_count += 1
                st.error(f"Error inesperado en iteración {i+1}: {str(e)}")

            progress_bar.progress((i + 1) / iterations)
        
    status_text.text("¡Prueba de determinismo finalizada!")
    st.success(f"✅ Se completaron {iterations} iteraciones. Éxitos: {success_count}. Errores: {error_count}.")
    st.info(f"💾 Los informes de la prueba se han guardado localmente en: {save_dir}")
    
    return zip_buffer.getvalue()
