import streamlit as st
import pandas as pd
import json
import os
from src.parser import convert_pdf_to_markdown
from src.validator import PaperAuditor

# 1. Configuración de la interfaz
st.set_page_config(page_title="Nature Auditor Pro", layout="wide", page_icon="🔬")

st.title("🔬 Auditor Integral de Manuscritos")
st.markdown("---")

# Inicializamos el auditor en la sesión para evitar recargas innecesarias
if 'auditor' not in st.session_state:
    st.session_state.auditor = PaperAuditor()

# 2. Selector de archivos
uploaded_file = st.file_uploader("Sube el PDF del artículo científico", type="pdf")

if uploaded_file:
    # Crear carpeta temporal si no existe
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    temp_path = os.path.join("temp", uploaded_file.name)

    with st.status("🚀 Procesando documento...", expanded=True) as status:
        # Guardar archivo temporalmente
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Paso 1: Extraer Markdown
        st.write("📂 Extrayendo texto y tablas (Docling)...")
        md_text = convert_pdf_to_markdown(temp_path)
        
        # Paso 2: Auditoría con Gemini 3.1 Flash Lite
        st.write("🧠 Analizando criterios de Nature Portfolio...")
        resultado = st.session_state.auditor.audit(md_text)
        
        status.update(label="✅ Análisis completado", state="complete", expanded=False)

    # 3. Visualización de Resultados
    if "revision" in resultado:
        st.success("Auditoría Finalizada")
        
        # Sección de Veredicto
        st.subheader("🏁 Veredicto del Revisor")
        st.info(resultado.get("veredicto_final", "No se proporcionó un veredicto general."))

        # Sección de Tabla de Cumplimiento
        st.subheader("📊 Desglose de Criterios")
        
        # Convertimos la lista de revisión a un DataFrame de Pandas
        df = pd.DataFrame(resultado["revision"])
        
        # Reordenamos las columnas para que se lea mejor
        columnas = ["categoria", "estado", "hallazgo", "recomendacion"]
        df = df[columnas]
        
        # Mostramos la tabla interactiva
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 4. Preparación del informe para descarga
        # Convertimos el diccionario a un texto Markdown bonito para evitar el error de binarios
        reporte_descargable = f"# Informe de Auditoría: {uploaded_file.name}\n\n"
        reporte_descargable += f"## Veredicto Final\n{resultado.get('veredicto_final', '')}\n\n"
        reporte_descargable += "## Detalles de la Revisión\n\n"
        
        for item in resultado["revision"]:
            reporte_descargable += f"### {item['categoria']}\n"
            reporte_descargable += f"- **Estado:** {item['estado']}\n"
            reporte_descargable += f"- **Hallazgo:** {item['hallazgo']}\n"
            reporte_descargable += f"- **Recomendación:** {item['recomendacion']}\n\n"

        st.markdown("---")
        
        # El botón de descarga ahora recibe 'reporte_descargable' que es un STRING
        st.download_button(
            label="📥 Descargar Informe en Markdown",
            data=reporte_descargable,
            file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md",
            mime="text/markdown"
        )
        
    elif "error" in resultado:
        st.error(f"Error en la auditoría: {resultado['error']}")
    else:
        st.error("La IA devolvió un formato inesperado. Inténtalo de nuevo.")

    # 5. Limpieza de residuos
    if os.path.exists(temp_path):
        os.remove(temp_path)

# Sidebar informativa
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nature_Logo_2020.svg/1200px-Nature_Logo_2020.svg.png", width=150)
    st.markdown("### Sobre el TFG")
    st.write("Esta herramienta utiliza Gemini 3.1 Flash Lite para auditar la transparencia científica.")
    st.write("---")
    st.caption("Desarrollado para la validación automática de Reporting Summaries.")