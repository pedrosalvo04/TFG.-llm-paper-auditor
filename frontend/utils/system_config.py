"""Configuración del sistema y entorno"""
import os
import warnings
import logging

def setup_environment():
    """Configura variables de entorno y filtros de warnings"""
    # Eliminar logs molestos de transformers y huggingface
    os.environ["TRANSFORMERS_VERBOSITY"] = "error"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Desactivar OpenTelemetry
    os.environ["OTEL_SDK_DISABLED"] = "true"

    # Filtros de warnings
    warnings.filterwarnings("ignore", message=".*Accessing.*__path__.*")
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    
    # Nivel de log para transformers
    logging.getLogger("transformers").setLevel(logging.ERROR)
