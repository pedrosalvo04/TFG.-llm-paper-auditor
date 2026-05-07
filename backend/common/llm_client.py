"""
Cliente LLM compartido para todos los servicios.

Mejoras LLMOps respecto a la versión anterior:
  - Reintentos con Exponential Backoff mediante `tenacity` (elimina time.sleep manual).
  - Soporte nativo para `response_schema` (Structured Outputs de Gemini).
  - Separación de errores retryable (503, 429) de errores fatales (400, auth).
  - Telemetría básica: logging de uso de tokens por llamada.
"""
from __future__ import annotations

import logging
from typing import Any, Optional, Type

from google import genai
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from backend.common.config import GOOGLE_API_KEY, MODEL_NAME
from backend.utils.logger import get_logger

logger = get_logger(__name__)
_tenacity_logger = logging.getLogger("tenacity.retry")


# ---------------------------------------------------------------------------
# Predicado de reintentos: solo reintentamos errores transitorios
# ---------------------------------------------------------------------------

def _is_retryable_error(exc: BaseException) -> bool:
    """
    Devuelve True únicamente para errores que tienen sentido reintentar:
      - 503 UNAVAILABLE (servidor saturado)
      - 429 RESOURCE_EXHAUSTED (rate limit / cuota)
    Los errores 400 (prompt inválido) o 401 (auth) son fatales y NO se reintentan.
    """
    msg = str(exc).upper()
    return any(code in msg for code in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "QUOTA"))


# ---------------------------------------------------------------------------
# Cliente LLM
# ---------------------------------------------------------------------------

class LLMClient:
<<<<<<< Updated upstream
    """Cliente reutilizable para interactuar con Gemini"""
    
    def __init__(self, generation_config=None):
        """
        Inicializa el cliente LLM con configuración personalizada
        
        Args:
            generation_config: Diccionario con configuración de generación
        """
=======
    """
    Cliente reutilizable para interactuar con los modelos Gemini de Google.

    Parámetros
    ----------
    model_name : str, opcional
        Nombre del modelo. Por defecto usa MODEL_NAME de config.
    generation_config : dict, opcional
        Configuración base de generación (temperatura, max_tokens, etc.).
        Puede incluir `response_schema` para Structured Outputs.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        generation_config: Optional[dict] = None,
    ) -> None:
>>>>>>> Stashed changes
        if not GOOGLE_API_KEY:
            logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
<<<<<<< Updated upstream
        
        self.model_name = MODEL_NAME
=======
        self.model_name = model_name or MODEL_NAME
>>>>>>> Stashed changes
        self.generation_config = generation_config or {}

        logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def generate(self, prompt: str, response_schema: Optional[Type[Any]] = None):
        """
        Genera contenido usando el modelo configurado.

        Aplica Exponential Backoff automático ante errores retryables (503/429).
        Si se proporciona `response_schema`, se usa Structured Output de Gemini,
        lo que garantiza que el JSON devuelto sea válido sin necesidad de parsing manual.

        Parámetros
        ----------
        prompt : str
            El prompt a enviar al modelo.
        response_schema : Type[BaseModel], opcional
            Clase Pydantic que define el esquema de respuesta esperado.
            Si se proporciona, sobreescribe cualquier `response_schema` en
            `self.generation_config`.

        Devuelve
        --------
        google.genai.types.GenerateContentResponse
        """
        config = dict(self.generation_config)

        if response_schema is not None:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = response_schema

        return self._generate_with_retry(prompt, config)

    # ------------------------------------------------------------------
    # Implementación interna con tenacity
    # ------------------------------------------------------------------

    @retry(
        retry=retry_if_exception(_is_retryable_error),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(4),
        before_sleep=before_sleep_log(_tenacity_logger, logging.WARNING),
        reraise=True,
    )
    def _generate_with_retry(self, prompt: str, config: dict):
        """
        Llamada real a la API de Gemini con lógica de reintento incorporada.

        `tenacity` gestiona automáticamente:
          - Espera inicial de 4 s, duplicándose con cada intento (hasta 60 s).
          - Máximo 4 intentos (3 reintentos).
          - Log automático antes de cada reintento.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )
            # Telemetría básica: log de uso de tokens
            self._log_token_usage(response)
            return response
        except Exception as exc:
            if _is_retryable_error(exc):
                # Mostrar aviso visual en Streamlit si está disponible
                self._notify_streamlit_retry(exc)
            raise

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    @staticmethod
    def _log_token_usage(response) -> None:
        """Registra el uso de tokens si el modelo lo reporta."""
        try:
            usage = getattr(response, "usage_metadata", None)
            if usage:
                logger.debug(
                    f"📊 Tokens — prompt: {usage.prompt_token_count}, "
                    f"candidates: {usage.candidates_token_count}, "
                    f"total: {usage.total_token_count}"
                )
<<<<<<< Updated upstream
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
=======
        except Exception:
            pass  # No es crítico si el modelo no reporta uso

    @staticmethod
    def _notify_streamlit_retry(exc: BaseException) -> None:
        """Muestra un toast en Streamlit si está disponible (no bloquea)."""
        try:
            import streamlit as st
            st.toast("⚠️ Gemini saturado. Reintentando con backoff exponencial...", icon="⏳")
        except Exception:
            pass  # Se ejecuta fuera de Streamlit o Streamlit no está disponible
>>>>>>> Stashed changes
