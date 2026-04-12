"""Servicio de chatbot interactivo"""
from backend.common.llm_client import LLMClient
from backend.common.config import CHAT_CONFIG
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class PaperChatbot:
    """Chatbot para interactuar sobre papers auditados"""
    
    def __init__(self):
        """Inicializa el chatbot con temperatura más alta para conversación natural"""
        self.llm_client = LLMClient(generation_config=CHAT_CONFIG)
        logger.info("✅ Módulo de Chatbot inicializado correctamente")

    def preguntar(self, paper_text, question, history_text):
        """
        Envía la pregunta del usuario junto con el contexto del paper al modelo
        
        Args:
            paper_text: Texto completo del paper
            question: Pregunta del usuario
            history_text: Historial de conversación
            
        Returns:
            Respuesta del chatbot
        """
        prompt = f"""
        Eres el Revisor Editorial de una conferencia de alto impacto en Ciencias de la Computación (ACM, IEEE, NeurIPS, etc.) que acaba de auditar este paper. 
        El autor/usuario tiene una duda sobre tu revisión o sobre el contenido del artículo.
        
        TUS REGLAS ESTRICTAS:
        1. Responde de forma profesional, clara y basándote ÚNICAMENTE en el texto proporcionado.
        2. Si te preguntan por algo que NO está en el paper, dilo directamente. No inventes.
        3. Si te piden justificar un fallo, cita las secciones relevantes del texto.
        4. Enfoca tus respuestas en aspectos de reproducibilidad, código, datos, y experimentación computacional.

        CONTENIDO DEL PAPER:
        {paper_text}

        HISTORIAL BREVE DE LA CONVERSACIÓN:
        {history_text}

        PREGUNTA DEL USUARIO:
        {question}
        """
        
        try:
            logger.info("Enviando pregunta al Chatbot...")
            response = self.llm_client.generate(prompt)
            return response.text
        except Exception as e:
            logger.error(f"❌ Error en el chatbot: {str(e)}")
            return f"❌ Hubo un error de conexión con el revisor: {str(e)}"
