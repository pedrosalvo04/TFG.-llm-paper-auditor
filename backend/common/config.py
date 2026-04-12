"""Configuración centralizada del backend"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

# Configuración de modelos
MODEL_NAME = "models/gemini-3.1-flash-lite-preview"

# Temperaturas por servicio
AUDIT_TEMPERATURE = 0.0
CHAT_TEMPERATURE = 0.2
SOTA_TEMPERATURE = 0.1

# Configuración de auditoría
AUDIT_CONFIG = {
    "response_mime_type": "application/json",
    "temperature": AUDIT_TEMPERATURE,
    "top_k": 1,
    "top_p": 0.1
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
