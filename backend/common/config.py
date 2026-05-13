"""Configuración centralizada del backend"""
import os
import warnings
import logging
from dotenv import load_dotenv

# Supresión estricta de logs y warnings de librerías de IA
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

# Filtrar logs repetitivos de red (HuggingFace) y OCR
class CleanNetworkLogs(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        # Ocultar peticiones de verificación de caché de HuggingFace que ensucian la consola
        if "huggingface.co" in msg and ("HEAD" in msg or "GET" in msg):
            return False
        return True

logging.getLogger("httpx").addFilter(CleanNetworkLogs())
logging.getLogger("RapidOCR").setLevel(logging.WARNING)
logging.getLogger("docling").setLevel(logging.WARNING)
logging.getLogger("onnxruntime").setLevel(logging.ERROR)

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

# Configuración de modelos
# Modelo rápido y con razonamiento para Triage y Extracción Masiva (Fase Map)
MAP_MODEL_NAME = "gemini-3.1-flash-lite-preview"
# Modelo pesado y analítico para Orquestación y Consolidación (Fase Reduce) - Flash Lite para mayor velocidad
REDUCE_MODEL_NAME = "gemini-3.1-flash-lite-preview"
# Modelo para Extracción Inicial (General Analysis) - Flash Live
EXTRACTION_MODEL_NAME = "gemini-3.1-flash-lite-preview"
# Modelo para Evaluación Final (Senior Area Chair) - Flash Lite para mayor cuota
EVALUATION_MODEL_NAME = "gemini-3.1-flash-lite-preview"
# Modelo para Verificación Estricta (Auditor 2) - Pro para máxima precisión
VERIFICATION_MODEL_NAME = "gemini-3.1-flash-lite-preview"

#resto de modelos:
"""
--- AVAILABLE MODELS ---
Name: models/gemini-2.5-flash, Display Name: Gemini 2.5 Flash
Name: models/gemini-2.5-pro, Display Name: Gemini 2.5 Pro
Name: models/gemini-2.0-flash, Display Name: Gemini 2.0 Flash
Name: models/gemini-2.0-flash-001, Display Name: Gemini 2.0 Flash 001
Name: models/gemini-2.0-flash-lite-001, Display Name: Gemini 2.0 Flash-Lite 001
Name: models/gemini-2.0-flash-lite, Display Name: Gemini 2.0 Flash-Lite
Name: models/gemini-2.5-flash-preview-tts, Display Name: Gemini 2.5 Flash Preview TTS
Name: models/gemini-2.5-pro-preview-tts, Display Name: Gemini 2.5 Pro Preview TTS
Name: models/gemma-3-1b-it, Display Name: Gemma 3 1B
Name: models/gemma-3-4b-it, Display Name: Gemma 3 4B
Name: models/gemma-3-12b-it, Display Name: Gemma 3 12B
Name: models/gemma-3-27b-it, Display Name: Gemma 3 27B
Name: models/gemma-3n-e4b-it, Display Name: Gemma 3n E4B
Name: models/gemma-3n-e2b-it, Display Name: Gemma 3n E2B
Name: models/gemma-4-26b-a4b-it, Display Name: Gemma 4 26B A4B IT
Name: models/gemma-4-31b-it, Display Name: Gemma 4 31B IT
Name: models/gemini-flash-latest, Display Name: Gemini Flash Latest
Name: models/gemini-flash-lite-latest, Display Name: Gemini Flash-Lite Latest
Name: models/gemini-pro-latest, Display Name: Gemini Pro Latest
Name: models/gemini-2.5-flash-lite, Display Name: Gemini 2.5 Flash-Lite
Name: models/gemini-2.5-flash-image, Display Name: Nano Banana
Name: models/gemini-3-pro-preview, Display Name: Gemini 3 Pro Preview
Name: models/gemini-3-flash-preview, Display Name: Gemini 3 Flash Preview
Name: models/gemini-3.1-pro-preview, Display Name: Gemini 3.1 Pro Preview
Name: models/gemini-3.1-pro-preview-customtools, Display Name: Gemini 3.1 Pro Preview Custom Tools
Name: models/gemini-3.1-flash-lite-preview, Display Name: Gemini 3.1 Flash Lite Preview
Name: models/gemini-3-pro-image-preview, Display Name: Nano Banana Pro
Name: models/nano-banana-pro-preview, Display Name: Nano Banana Pro
Name: models/gemini-3.1-flash-image-preview, Display Name: Nano Banana 2
Name: models/lyria-3-clip-preview, Display Name: Lyria 3 Clip Preview
Name: models/lyria-3-pro-preview, Display Name: Lyria 3 Pro Preview
Name: models/gemini-3.1-flash-tts-preview, Display Name: Gemini 3.1 Flash TTS Preview
Name: models/gemini-robotics-er-1.5-preview, Display Name: Gemini Robotics-ER 1.5 Preview
Name: models/gemini-robotics-er-1.6-preview, Display Name: Gemini Robotics-ER 1.6 Preview
Name: models/gemini-2.5-computer-use-preview-10-2025, Display Name: Gemini 2.5 Computer Use Preview 10-2025
Name: models/deep-research-max-preview-04-2026, Display Name: Deep Research Max Preview (Apr-21-2026)
Name: models/deep-research-preview-04-2026, Display Name: Deep Research Preview (Apr-21-2026)
Name: models/deep-research-pro-preview-12-2025, Display Name: Deep Research Pro Preview (Dec-12-2025)
Name: models/gemini-embedding-001, Display Name: Gemini Embedding 001
Name: models/gemini-embedding-2-preview, Display Name: Gemini Embedding 2 Preview
Name: models/gemini-embedding-2, Display Name: Gemini Embedding 2
Name: models/aqa, Display Name: Model that performs Attributed Question Answering.
Name: models/imagen-4.0-generate-001, Display Name: Imagen 4
Name: models/imagen-4.0-ultra-generate-001, Display Name: Imagen 4 Ultra
Name: models/imagen-4.0-fast-generate-001, Display Name: Imagen 4 Fast
Name: models/veo-2.0-generate-001, Display Name: Veo 2
Name: models/veo-3.0-generate-001, Display Name: Veo 3
Name: models/veo-3.0-fast-generate-001, Display Name: Veo 3 fast
Name: models/veo-3.1-generate-preview, Display Name: Veo 3.1
Name: models/veo-3.1-fast-generate-preview, Display Name: Veo 3.1 fast
Name: models/veo-3.1-lite-generate-preview, Display Name: Veo 3.1 lite
Name: models/gemini-2.5-flash-native-audio-latest, Display Name: Gemini 2.5 Flash Native Audio Latest
Name: models/gemini-2.5-flash-native-audio-preview-09-2025, Display Name: Gemini 2.5 Flash Native Audio Preview 09-2025
Name: models/gemini-2.5-flash-native-audio-preview-12-2025, Display Name: Gemini 2.5 Flash Native Audio Preview 12-2025
Name: models/gemini-3.1-flash-live-preview, Display Name: Gemini 3.1 Flash Live Preview
"""
# Variables por compatibilidad o uso por defecto si no se especifica
MODEL_NAME = EXTRACTION_MODEL_NAME

# Temperaturas por servicio
AUDIT_TEMPERATURE = 0.0
CHAT_TEMPERATURE = 0.2
SOTA_TEMPERATURE = 0.3

# Configuración de auditoría (Extracción)
AUDIT_CONFIG = {
    "response_mime_type": "application/json",
    "temperature": AUDIT_TEMPERATURE,
    "top_k": 1,
    "top_p": 0.1,
    "max_output_tokens": 16384
}

# Configuración de evaluación (Senior Area Chair) - Más creativa para mejores justificaciones
EVALUATION_CONFIG = {
    "response_mime_type": "application/json",
    "temperature": 0.0,
    "top_k": 40,
    "top_p": 0.95,
    "max_output_tokens": 16384
}

# Configuración de chat
CHAT_CONFIG = {
    "temperature": CHAT_TEMPERATURE
}

# Configuración de SOTA
SOTA_CONFIG = {
    "response_mime_type": "application/json",
    "temperature": SOTA_TEMPERATURE
}

# Semantic Scholar
SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_YEAR_RANGE = None  # Sin restricción de tiempo por defecto
SEMANTIC_SCHOLAR_LIMIT = 15
SEMANTIC_SCHOLAR_FIELDS = "paperId,title,authors,year,citationCount,abstract,url"
