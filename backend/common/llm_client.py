"""Cliente LLM compartido para todos los servicios"""
from google import genai
from backend.common.config import GOOGLE_API_KEY, MODEL_NAME
from backend.common.logger import get_logger

logger = get_logger(__name__)

import requests
import json
import logging
from backend.common.config import MODEL_NAME

logger = logging.getLogger(__name__)

class LLMResponse:
    def __init__(self, text):
        self.text = text

class LLMClient:
    """Cliente reutilizable para interactuar con Ollama localmente (qwen2.5)"""
    
    def __init__(self, model_name=None, generation_config=None):
        """
        Inicializa el cliente LLM con configuración personalizada
        
        Args:
            model_name: Nombre del modelo a usar
            generation_config: Diccionario con configuración de generación
        """
        self.api_url = "http://localhost:11434/api/generate"
        # Forzamos qwen2.5 por defecto
        self.model_name = model_name if (model_name and "qwen2.5" in model_name) else "qwen2.5" 
        self.generation_config = generation_config or {}
        
        logger.info(f"✅ Cliente LLM inicializado (Ollama): {self.model_name}")
        self._check_ollama_status()
            
    def _check_ollama_status(self):
        """Verifica que el demonio de Ollama esté en ejecución y avisa si no lo está."""
        import streamlit as st
        try:
            requests.get("http://localhost:11434/", timeout=2)
        except requests.exceptions.RequestException:
            error_msg = "⚠️ OLLAMA NO ESTÁ EN EJECUCIÓN. Asegúrate de iniciar Ollama en tu máquina (puerto 11434)."
            logger.warning(error_msg)
            try:
                st.warning(error_msg, icon="⚠️")
            except Exception:
                pass
    
    def generate(self, prompt):
        """
        Genera contenido usando el modelo local Ollama.
        """
        import streamlit as st
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"  # Forzar salida en formato JSON estructurado
        }
        
        options = {
            "num_ctx": 32768  # qwen2.5 soporta ventana grande, ponemos suficiente para el prompt unico
        }
        
        if self.generation_config:
            if "temperature" in self.generation_config:
                options["temperature"] = self.generation_config["temperature"]
            if "top_p" in self.generation_config:
                options["top_p"] = self.generation_config["top_p"]
            if "top_k" in self.generation_config:
                options["top_k"] = self.generation_config["top_k"]
            if "max_output_tokens" in self.generation_config:
                options["num_predict"] = self.generation_config["max_output_tokens"]
                
        payload["options"] = options

        try:
            logger.info(f"Iniciando generación con modelo local: {self.model_name}...")
            
            response = requests.post(self.api_url, json=payload, timeout=None)
            response.raise_for_status()
            
            result = response.json()
            
            return LLMResponse(text=result.get("response", ""))
            
        except requests.exceptions.ConnectionError:
            error_msg = "No se pudo conectar a Ollama. Por favor, verifica que el demonio de Ollama esté ejecutándose (localhost:11434)."
            logger.error(f"❌ {error_msg}")
            try:
                st.error(f"❌ {error_msg}", icon="🚨")
            except Exception:
                pass
            raise ConnectionError(error_msg)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error en la petición a Ollama: {str(e)}"
            logger.error(f"❌ {error_msg}")
            try:
                st.error(f"❌ {error_msg}", icon="🚨")
            except Exception:
                pass
            raise Exception(error_msg)

