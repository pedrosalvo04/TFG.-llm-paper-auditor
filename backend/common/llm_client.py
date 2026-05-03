"""Cliente LLM compartido para todos los servicios"""
from google import genai
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
            logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")
        
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        
        self.model_name = MODEL_NAME
        self.generation_config = generation_config or {}
        
        logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")
    
    def generate(self, prompt):
        """
        Genera contenido usando el modelo, con reintentos automáticos
        en caso de saturación (503) o límites de cuota.
        """
        import time
        import streamlit as st
        
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=self.generation_config
                )
                return response
            except Exception as e:
                error_msg = str(e)
                if attempt < max_retries:
                    logger.warning(f"⚠️ Error API Gemini: {error_msg}. Reintentando ({attempt + 1}/{max_retries})...")
                    # Mostrar el aviso visual en el frontend sin bloquear la interfaz
                    try:
                        st.toast(f"⚠️ Gemini saturado (Alta demanda). Reintentando ({attempt + 1}/{max_retries})...", icon="⏳")
                    except Exception:
                        pass # Por si se ejecuta fuera de Streamlit
                        
                    # Esperar 4 segundos antes de reintentar
                    time.sleep(4)
                else:
                    logger.error(f"❌ Error crítico tras {max_retries} reintentos: {error_msg}")
                    try:
                        st.error(f"❌ La API de Gemini sigue saturada o fallando tras {max_retries} reintentos. Vuelve a intentarlo en unos minutos.")
                    except Exception:
                        pass
                    raise
