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
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

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

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

# Configuración de modelos
# Modelo rápido y ligero para auditoría general y chatbot
MODEL_NAME = "gemini-3.1-flash-lite-preview"
# Modelo pesado y analítico para extracción exhaustiva (RAG)
RAG_MODEL_NAME = "gemini-3.1-flash-lite-preview"

# Temperaturas por servicio
AUDIT_TEMPERATURE = 0.0
CHAT_TEMPERATURE = 0.2
SOTA_TEMPERATURE = 0.1

# Configuración de auditoría
AUDIT_CONFIG = {
    "response_mime_type": "application/json",
    "temperature": AUDIT_TEMPERATURE,
    "top_k": 1,
    "top_p": 0.1,
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
SEMANTIC_SCHOLAR_YEAR_RANGE = "2023-2026"
SEMANTIC_SCHOLAR_LIMIT = 5
SEMANTIC_SCHOLAR_FIELDS = "paperId,title,authors,year,citationCount,abstract,url"
