"""Componente de chatbot interactivo"""
import streamlit as st

def render_chatbot(md_text):
    """Renderiza la sección del chatbot interactivo"""
    st.markdown("---")
    st.header("💬 Pregunta al Revisor")
    st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt_usuario = st.text_input(
        "Escribe tu pregunta:",
        key="chat_input",
        placeholder="Ej: ¿En qué página falla el paper en su estadística?"
    )
    
    if st.button("Enviar", key="send_button") and prompt_usuario:
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
        
        with st.spinner("El revisor está analizando tu consulta..."):
            respuesta_ia = st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)
        
        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
        st.rerun()
