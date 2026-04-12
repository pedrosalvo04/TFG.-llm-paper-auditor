"""Cliente LLM compartido para todos los servicios"""
import google.generativeai as genai
from backend.common.config import GOOGLE_API_KEY, MODEL_NAME
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    """Cliente reutilizable para interactuar con Gemini"""
    
    def __init__(self, generation_config=None):
        """
        Inicializa el cliente LLM con configuración personalizada
        
        Args:
            generation_config: Diccionario con configuración de generación
        """
        if not GOOGLE_API_KEY:
            logger.error("CRÍTICO: No se encontró la GOOGLE_API_KEY en el .env")
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")
        
        genai.configure(api_key=GOOGLE_API_KEY)
        
        self.model_name = MODEL_NAME
        self.generation_config = generation_config or {}
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )
        
        logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")
    
    def generate(self, prompt):
        """
        Genera contenido usando el modelo
        
        Args:
            prompt: Texto del prompt
            
        Returns:
            Respuesta del modelo
        """
        try:
            response = self.model.generate_content(prompt)
            return response
        except Exception as e:
            logger.error(f"❌ Error generando contenido: {str(e)}")
            raise
