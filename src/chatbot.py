import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class PaperChatbot:
    def __init__(self):
        """
        Constructor: Inicializa el modelo para conversación.
        """
        self.model_name = "gemini-3.1-flash-lite-preview"
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("CRÍTICO: No se encontró la GOOGLE_API_KEY en el .env")
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")
            
        genai.configure(api_key=api_key)
        
        # Para el chat subimos un poquito la temperatura (0.2) para que el lenguaje
        # sea más natural y fluido, pero sin llegar a alucinar.
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.2,
            }
        )
        logger.info("✅ Módulo de Chatbot inicializado correctamente.")

    def preguntar(self, paper_text, question, history_text):
        """
        Envía la pregunta del usuario junto con el contexto del paper al modelo.
        """
        prompt = f"""
        Eres el Revisor Editorial de Nature que acaba de auditar este paper científico. 
        El autor/usuario tiene una duda sobre tu revisión o sobre el contenido del artículo.
        
        TUS REGLAS ESTRICTAS:
        1. Responde de forma profesional, clara y basándote ÚNICAMENTE en el texto proporcionado.
        2. Si te preguntan por algo que NO está en el paper, dilo directamente. No inventes.
        3. Si te piden justificar un fallo, cita las secciones relevantes del texto.

        CONTENIDO DEL PAPER:
        {paper_text}

        HISTORIAL BREVE DE LA CONVERSACIÓN:
        {history_text}

        PREGUNTA DEL USUARIO:
        {question}
        """
        
        try:
            logger.info("Enviando pregunta al Chatbot...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"❌ Error en el chatbot: {str(e)}")
            return f"❌ Hubo un error de conexión con el revisor: {str(e)}"