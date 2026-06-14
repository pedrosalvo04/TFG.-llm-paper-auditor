"""Cliente LLM compartido para todos los servicios (Versión Local - Ollama)"""
import requests
from dataclasses import dataclass
from backend.common.logger import get_logger

logger = get_logger(__name__)

@dataclass
class LLMResponse:
    text: str

class LLMClient:
    """Cliente reutilizable para interactuar con Ollama local"""
    
    def __init__(self, model_name="qwen2.5", generation_config=None):
        """
        Inicializa el cliente LLM con configuración para Ollama.
        
        Args:
            model_name: Nombre del modelo a usar (ignorará los de Gemini si se fuerza qwen2.5)
            generation_config: Diccionario con configuración de generación (temperatura, etc.)
        """
        # Forzamos qwen2.5 si no se especifica o si viene un modelo de gemini por defecto
        if not model_name or "gemini" in model_name.lower():
            self.model_name = "qwen2.5"
        else:
            self.model_name = model_name
            
        self.generation_config = generation_config or {}
        self.api_url = "http://localhost:11434/api/generate"
        
        logger.info(f"✅ Cliente LLM inicializado: {self.model_name} (Local - Ollama)")
        
        # Verificar si Ollama está en ejecución
        self._check_ollama_status()
            
    def _check_ollama_status(self):
        """Verifica que el demonio de Ollama esté en ejecución y avisa si no lo está."""
        import streamlit as st
        try:
            # Endpoint base de Ollama para verificar estado
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
        Genera contenido usando el modelo local.
        Fuerza la salida en formato JSON y maneja errores de conexión.
        """
        import streamlit as st
        
        # Preparamos el payload base
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"  # Forzar salida en formato JSON estructurado (Ollama lo soporta nativamente)
        }
        
        # Opciones base obligatorias para lectura de documentos
        options = {
            "num_ctx": 32768  # 32k tokens de ventana de contexto (fundamental para no cortar los papers)
        }
        
        # Si generation_config tiene parámetros compatibles, los mapeamos a 'options' en Ollama
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
            
            # Realizamos la petición HTTP a Ollama sin timeout para inferencia local pesada
            response = requests.post(self.api_url, json=payload, timeout=None)
            response.raise_for_status()
            
            result = response.json()
            
            # Ollama devuelve la respuesta en la clave 'response'
            # Envolvemos el resultado en LLMResponse para mantener compatibilidad con response.text
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
