"""Cliente LLM compartido para todos los servicios"""
from google import genai
from backend.common.config import GOOGLE_API_KEY, MODEL_NAME
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    """Cliente reutilizable para interactuar con Gemini"""
    
    def __init__(self, model_name=None, generation_config=None):
        """
        Inicializa el cliente LLM con configuración personalizada
        
        Args:
            model_name: Nombre del modelo a usar
            generation_config: Diccionario con configuración de generación
        """
        if not GOOGLE_API_KEY:
            logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")
        
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        
        self.model_name = model_name or MODEL_NAME
        self.generation_config = generation_config or {}
        
        logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")
    
    def generate(self, prompt):
        """
        Genera contenido usando el modelo, con reintentos automáticos
        y backoff exponencial en caso de saturación (503) o límites de cuota (429).
        """
        import time
        import streamlit as st
        import random
        
        max_retries = 5 # Aumentado para mayor resiliencia
        base_delay = 2  # Reducido para que la espera no sea tan larga al principio
        
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
                
                # Identificar si el error es reintentable (Saturación o Cuota)
                is_retryable = any(code in error_msg.upper() for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"])
                
                if attempt < max_retries and is_retryable:
                    # Backoff exponencial: delay = base * 2^attempt + jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    
                    logger.warning(f"⚠️ Error API Gemini [{self.model_name}]: {error_msg}. Reintento {attempt + 1}/{max_retries} en {delay:.1f}s...")
                    
                    # Mostrar el aviso visual en el frontend sin bloquear la interfaz
                    try:
                        st.toast(f"⏳ Gemini saturado (Alta demanda). Reintento {attempt + 1}/{max_retries} en {int(delay)}s...", icon="⏳")
                    except Exception:
                        pass # Por si se ejecuta fuera de Streamlit
                        
                    # Esperar antes del siguiente intento
                    time.sleep(delay)
                else:
                    # Si no es reintentable o ya agotamos intentos, lanzamos el error
                    if attempt >= max_retries:
                        logger.error(f"❌ Error crítico tras {max_retries} reintentos: {error_msg}")
                    else:
                        logger.error(f"❌ Error no reintentable detectado: {error_msg}")
                    raise
