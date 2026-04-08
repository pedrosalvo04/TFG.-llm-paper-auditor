import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go
from src.parser import convert_pdf_to_markdown
from src.validator import PaperAuditor
from src.chatbot import PaperChatbot
from src.sota_analyzer import SotaAnalyzer

if "resultado" not in st.session_state:
    st.session_state.resultado = None

if 'sota_analyzer' not in st.session_state:
    st.session_state.sota_analyzer = SotaAnalyzer()

st.set_page_config(page_title="Nature Auditor Pro", layout="wide", page_icon="🔬")

st.markdown("""
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
        background-color: #2d3436 !important; /* Gris grafito oscuro */
        border-radius: 15px !important; 
        padding: 5px !important;
    }

    /* 🛠️ EL TRUCO PARA ELIMINAR LÍNEAS DUPLICADAS */
    [data-testid="stTable"] table {
        border-collapse: collapse !important; /* Une los bordes en una sola línea */
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
    """, unsafe_allow_html=True)

st.title("💻 Auditor de Papers en Ciencias de la Computación")
st.markdown("---")

# Inicialización de módulos
if 'auditor' not in st.session_state:
    st.session_state.auditor = PaperAuditor()

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = PaperChatbot()

def calcular_puntuacion(revision):
    puntos = 0
    aplicables = 0
    for item in revision:
        estado = item.get("estado", "").upper()
        if "N/A" in estado or "NO APLICA" in estado or "⚪" in estado:
            continue
        
        if "CUMPLE TOTALMENTE" in estado or "🟢" in estado:
            puntos += 1.0
            aplicables += 1
        elif "CUMPLE MAYORMENTE" in estado or "🔵" in estado:
            puntos += 0.75
            aplicables += 1
        elif "CUMPLE PARCIALMENTE" in estado or "🟡" in estado:
            puntos += 0.5
            aplicables += 1
        elif "CUMPLE MÍNIMAMENTE" in estado or "🟠" in estado:
            puntos += 0.25
            aplicables += 1
        elif "NO CUMPLE" in estado or "🔴" in estado:
            aplicables += 1
    
    if aplicables == 0: return 0
    return round((puntos / aplicables) * 100)

def dibujar_medidor(score):
    if score >= 80:
        color_barra = "#00cc44"
    elif score >= 50:
        color_barra = "#ff9900"
    else:
        color_barra = "#ff4b4b"

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Índice de Reproducibilidad", 'font': {'size': 20}},
        number = {'suffix': "%", 'font': {'size': 40}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 10},
            'bar': {
                'color': color_barra,
                'thickness': 1,
                'line': {'color': "black", 'width': 3} 
            },
            'bgcolor': "white",
            # 👇 Borde exterior de la gauge más grueso
            'borderwidth': 2, 
            'bordercolor': "black",
            
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 75, 75, 0.25)"},
                {'range': [50, 80], 'color': "rgba(255, 153, 0, 0.25)"},
                {'range': [80, 100], 'color': "rgba(0, 204, 68, 0.25)"}],
        }
    ))
    
    # 👇 Hacemos el fondo del gráfico transparente para que el CSS actúe
    fig.update_layout(
        height=300, 
        margin=dict(l=10, r=10, t=40, b=25),
        paper_bgcolor="rgba(0,0,0,0)", # Totalmente transparente
        font={'color': "#E5E7EB"}
    )
    return fig

# ---------------------------------------------------------
# LÓGICA PRINCIPAL DE LA APLICACIÓN
# ---------------------------------------------------------

uploaded_file = st.file_uploader("Sube el PDF del artículo científico", type="pdf")

if uploaded_file:
    # 🛡️ ESCUDO DE MEMORIA
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

    resultado = st.session_state.resultado
    md_text = st.session_state.md_text

    # RENDEREZADO DE LA INTERFAZ
    if "revision" in resultado:
        st.success("Auditoría Finalizada")
        
        puntuacion = calcular_puntuacion(resultado["revision"])
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader(f"🏁 Veredicto: {uploaded_file.name}")
            st.info(resultado.get("veredicto_final", ""))
            st.plotly_chart(dibujar_medidor(puntuacion), use_container_width=True)
            
            tiempo = resultado.get('metricas', {}).get('tiempo_segundos', 'N/A')
            caracteres = resultado.get('metricas', {}).get('caracteres_leidos', 'N/A')
            st.caption(f"⏱️ **Tiempo IA:** {tiempo}s | 📄 **Caracteres:** {caracteres}")
            
        with col2:
            st.subheader("📊 Desglose de Criterios")
            df = pd.DataFrame(resultado["revision"])
            df = df[["categoria", "estado", "hallazgo", "recomendacion"]]
            
            # 👇 SOLUCIÓN A LA TABLA: Usamos 'categoria' como índice y st.table para forzar el ajuste de texto
            df.set_index("categoria", inplace=True)
            st.table(df)


        # ---------------------------------------------------------
        # ANÁLISIS DE ESTADO DEL ARTE (SOTA)
        # ---------------------------------------------------------
        st.markdown("---")
        st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")
        
        if st.button("Ejecutar Análisis de Literatura Reciente"):
            with st.spinner("Conectando con Semantic Scholar y validando bibliografía..."):
                resultado_sota = st.session_state.sota_analyzer.analyze_sota(md_text)
                
                if "error" not in resultado_sota:
                    st.success("Análisis completado")
                    
                    # Conclusión SOTA
                    st.markdown("### 📝 Conclusión")
                    st.info(resultado_sota.get('conclusion_sota', ''))
                    
                    # Obtener papers omitidos del análisis
                    papers_omitidos = resultado_sota.get("papers_omitidos", [])
                    df_papers = pd.DataFrame(resultado_sota.get("papers_analizados", []))
                    año_paper_estudiado = resultado_sota.get("metadata", {}).get("año_paper_estudiado")
                    
                    if not df_papers.empty and papers_omitidos:
                        # Preparar datos
                        df_papers['authors_display'] = df_papers['autores'].apply(
                            lambda x: ', '.join([a.get('name', '') for a in x[:2]]) + (' et al.' if len(x) > 2 else '') if isinstance(x, list) else 'N/A'
                        )
                        
                        # Renombrar columnas para display
                        df_papers.rename(columns={'titulo': 'title', 'año': 'year', 'citas': 'citationCount'}, inplace=True)
                        
                        # Crear set de títulos omitidos (no citados)
                        titulos_omitidos = {p['titulo'].lower().strip() for p in papers_omitidos}
                        
                        # Filtrar solo papers NO citados
                        def es_omitido(titulo):
                            titulo_lower = titulo.lower().strip()
                            for omitido in titulos_omitidos:
                                if omitido in titulo_lower or titulo_lower in omitido:
                                    return True
                            return False
                        
                        df_papers['es_omitido'] = df_papers['title'].apply(es_omitido)
                        df_no_citados = df_papers[df_papers['es_omitido'] == True]
                        
                        # Mostrar SOLO recomendaciones de no citados en formato tabla
                        if not df_no_citados.empty:
                            st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")
                            st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")
                            
                            # Crear DataFrame para la tabla
                            tabla_recomendaciones = []
                            for _, paper in df_no_citados.iterrows():
                                # Buscar la justificación
                                justificacion = ""
                                relevancia = ""
                                subtema = ""
                                titulo_paper = paper['title'].lower().strip()
                                
                                for omitido in papers_omitidos:
                                    titulo_omitido = omitido['titulo'].lower().strip()
                                    if titulo_omitido in titulo_paper or titulo_paper in titulo_omitido:
                                        justificacion = omitido.get('justificacion', '')
                                        relevancia = omitido.get('relevancia', '')
                                        subtema = omitido.get('subtema_relacionado', '')
                                        break
                                
                                # Determinar si es posterior
                                es_posterior = "✅ Sí" if año_paper_estudiado and paper['year'] > año_paper_estudiado else "❌ No"
                                if not año_paper_estudiado:
                                    es_posterior = "?"
                                
                                tabla_recomendaciones.append({
                                    "Título": paper['title'],
                                    "Autores": paper['authors_display'],
                                    "Año": paper['year'],
                                    "Posterior": es_posterior,
                                    "Citas": paper['citationCount'],
                                    "Relevancia": relevancia,
                                    "Subtema": subtema,
                                    "Justificación": justificacion
                                })
                            
                            df_recomendaciones = pd.DataFrame(tabla_recomendaciones)
                            
                            # Mostrar tabla con configuración de columnas
                            st.dataframe(
                                df_recomendaciones,
                                hide_index=True,
                                use_container_width=True,
                                column_config={
                                    "Título": st.column_config.TextColumn("Título", width="large"),
                                    "Autores": st.column_config.TextColumn("Autores", width="medium"),
                                    "Año": st.column_config.NumberColumn("Año", width="small"),
                                    "Posterior": st.column_config.TextColumn("Posterior al tuyo", width="small"),
                                    "Citas": st.column_config.NumberColumn("Citas", width="small"),
                                    "Relevancia": st.column_config.TextColumn("Relevancia", width="small"),
                                    "Subtema": st.column_config.TextColumn("Subtema", width="medium"),
                                    "Justificación": st.column_config.TextColumn("Justificación", width="large")
                                }
                            )
                            
                            if año_paper_estudiado:
                                st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")
                            else:
                                st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")
                        else:
                            st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")
                    elif not papers_omitidos:
                        st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")
                else:
                    st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")
        # ---------------------------------------------------------
        # CHATBOT INTERACTIVO
        # ---------------------------------------------------------
        st.markdown("---")
        st.header("💬 Pregunta al Revisor")
        st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt_usuario = st.text_input("Escribe tu pregunta:", key="chat_input", placeholder="Ej: ¿En qué página falla el paper en su estadística?")
        
        if st.button("Enviar", key="send_button") and prompt_usuario:
            
            st.session_state.messages.append({"role": "user", "content": prompt_usuario})
            
            history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])

            with st.spinner("El revisor está analizando tu consulta..."):
                respuesta_ia = st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)
            
            st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
            st.rerun()

        # ---------------------------------------------------------
        # DESCARGA DEL INFORME
        # ---------------------------------------------------------
        st.markdown("---")
        st.subheader("📄 Descargar Informe")
        reporte_descargable = f"# Informe de Auditoría: {uploaded_file.name}\n\n**Índice de Reproducibilidad:** {puntuacion}%\n\n## Veredicto Final\n{resultado.get('veredicto_final', '')}\n\n## Detalles de la Revisión\n\n"
        for item in resultado["revision"]:
            reporte_descargable += f"### {item['categoria']}\n- **Estado:** {item['estado']}\n- **Hallazgo:** {item['hallazgo']}\n- **Recomendación:** {item['recomendacion']}\n\n"

        st.download_button(
            label="📥 Descargar Informe Completo (.md)",
            data=reporte_descargable,
            file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md",
            mime="text/markdown"
        )
            
    elif "error" in resultado:
        st.error(f"Error en la auditoría: {resultado['error']}")

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png", width=150)
    st.markdown("### Sobre el TFG")
    st.write("Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs.")