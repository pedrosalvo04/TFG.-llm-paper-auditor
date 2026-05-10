"""Servicio de chatbot interactivo refactorizado con arquitectura de skills"""
from backend.common.llm_client import LLMClient
from backend.common.config import CHAT_CONFIG
from backend.common.logger import get_logger
from backend.skills.chatbot_skills import (
    ConversationalResponseSkill,
    ContextValidationSkill
)

logger = get_logger(__name__)

class PaperChatbot:
    """Chatbot para interactuar sobre papers auditados usando arquitectura de skills"""
    
    def __init__(self):
        """Inicializa el chatbot con temperatura más alta para conversación natural"""
        self.llm_client = LLMClient(generation_config=CHAT_CONFIG)
        
        # Inicializar skills con el cliente LLM
        self.response_skill = ConversationalResponseSkill(llm_client=self.llm_client)
        self.validation_skill = ContextValidationSkill()
        
        logger.info("✅ Módulo de Chatbot inicializado con arquitectura de skills")

    def preguntar(self, paper_text, question, history_text):
        """
        Envía la pregunta del usuario junto con el contexto del paper al modelo
        usando la arquitectura de skills.
        
        Args:
            paper_text: Texto completo del paper
            question: Pregunta del usuario
            history_text: Historial de conversación
            
        Returns:
            Respuesta del chatbot
        """
        # Preparar contexto
        context = {
            'paper_text': paper_text,
            'question': question,
            'history_text': history_text
        }
        
        # Skill 1: Validar contexto
        validation_result = self.validation_skill.execute(context)
        
        if not validation_result.get('is_valid', False):
            error_msg = validation_result.get('error', 'Error desconocido')
            logger.error(f"❌ Validación fallida: {error_msg}")
            return f"❌ Error de validación: {error_msg}"
        
        # Skill 2: Generar respuesta conversacional
        response_result = self.response_skill.execute(context)
        
        return response_result.get('response', '❌ Error generando respuesta')


class Chatbot(PaperChatbot):
    """Alias para compatibilidad con tests"""
    pass
