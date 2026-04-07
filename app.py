import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go
from src.parser import convert_pdf_to_markdown
from src.validator import PaperAuditor
from src.chatbot import PaperChatbot

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
    
    /* 🎨 1. FONDOS MÁS OSCUROS (#27374D - Un Azul/Gris más profundo y oscuro) */
    [data-testid="stPlotlyChart"] {
        background-color: #27374D !important; 
        border-radius: 15px !important; 
        padding: 10px !important; 
    }

    [data-testid="stTable"] > div, .stTable {
        background-color: #27374D !important; 
        border-radius: 15px !important; 
        overflow: hidden !important; 
    }
    
    /* 💥 2. CABECERAS (Categoría, Estado, Hallazgo...) */
    [data-testid="stTable"] th, [data-testid="stTable"] th *, .stTable th {
        color: #63B3ED !important; /* Azul vivo que resalta sobre el fondo oscuro */
        font-size: 16px !important; /* Fuente más pequeña que antes */
        font-weight: 700 !important; /* Un poco menos gruesa */
        background-color: transparent !important;
        
        /* SIN SUBRAYAR */
        border-bottom: none !important; 
        text-decoration: none !important; 
    }

    /* 📝 3. CONTENIDO DE LA TABLA Y ESTADOS */
    [data-testid="stTable"] td, [data-testid="stTable"] td *, .stTable td {
        background-color: transparent !important; 
        color: #E2E8F0 !important; 
        font-size: 14px !important; /* Fuente de los puntos a analizar más pequeña */
        font-weight: 400 !important; 
        
        /* ESTADOS SIN SUBRAYAR Y SIN LÍNEAS DIVISORIAS */
        border-bottom: none !important; 
        text-decoration: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Auditor Integral de Manuscritos")
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
        aplicables += 1
        if "CUMPLE" in estado and "NO" not in estado:
            puntos += 1
        elif "PARCIAL" in estado:
            puntos += 0.5
    if aplicables == 0: return 0
    return int((puntos / aplicables) * 100)

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
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {
                'color': color_barra,
                # 👇 Borde interior un poco más grueso
                'line': {'color': "black", 'width': 2} 
            },
            'bgcolor': "white",
            # 👇 Borde exterior de la gauge más grueso
            'borderwidth': 2, 
            'bordercolor': "black",
            
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 75, 75, 0.35)"},
                {'range': [50, 80], 'color': "rgba(255, 153, 0, 0.35)"},
                {'range': [80, 100], 'color': "rgba(0, 204, 68, 0.35)"}],
        }
    ))
    
    # 👇 Hacemos el fondo del gráfico transparente para que el CSS actúe
    fig.update_layout(
        height=300, 
        margin=dict(l=10, r=10, t=40, b=30),
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
            
            st.write("🧠 Auditando con la Checklist de Nature...")
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
            st.subheader("🏁 Veredicto Principal")
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
        # CHATBOT INTERACTIVO (AHORA ARRIBA DE LA DESCARGA)
        # ---------------------------------------------------------
        st.markdown("---")
        st.header("💬 Pregunta al Revisor")
        st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt_usuario := st.chat_input("Ej: ¿En qué página falla el paper en su estadística?"):
            
            st.session_state.messages.append({"role": "user", "content": prompt_usuario})
            with st.chat_message("user"):
                st.markdown(prompt_usuario)

            history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])

            with st.chat_message("assistant"):
                with st.spinner("El revisor está analizando tu consulta..."):
                    respuesta_ia = st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)
                    st.markdown(respuesta_ia)
            
            st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})

        # ---------------------------------------------------------
        # DESCARGA DEL INFORME (AHORA AL FINAL DEL TODO)
        # ---------------------------------------------------------
        reporte_descargable = f"# Informe de Auditoría: {uploaded_file.name}\n\n**Índice de Reproducibilidad:** {puntuacion}%\n\n## Veredicto Final\n{resultado.get('veredicto_final', '')}\n\n## Detalles de la Revisión\n\n"
        for item in resultado["revision"]:
            reporte_descargable += f"### {item['categoria']}\n- **Estado:** {item['estado']}\n- **Hallazgo:** {item['hallazgo']}\n- **Recomendación:** {item['recomendacion']}\n\n"

        st.markdown("---")
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
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nature_Logo_2020.svg/1200px-Nature_Logo_2020.svg.png", width=150)
    st.markdown("### Sobre el TFG")
    st.write("Herramienta desarrollada para automatizar la auditoría de transparencia en artículos científicos usando LLMs.")