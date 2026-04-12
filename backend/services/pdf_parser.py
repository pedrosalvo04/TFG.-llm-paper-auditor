"""Servicio de parsing de archivos PDF"""
import pymupdf4llm
from backend.utils.logger import get_logger

logger = get_logger(__name__)

def convert_pdf_to_markdown(pdf_path):
    """
    Convierte un PDF a formato Markdown optimizado para LLMs
    
    Args:
        pdf_path: Ruta al archivo PDF
        
    Returns:
        Texto en formato Markdown
    """
    try:
        logger.info(f"Convirtiendo PDF a Markdown: {pdf_path}")
        md_text = pymupdf4llm.to_markdown(pdf_path)
        logger.info(f"✅ PDF convertido exitosamente ({len(md_text)} caracteres)")
        return md_text
    except Exception as e:
        logger.error(f"❌ Error en la extracción del PDF: {str(e)}")
        return f"❌ Error en la extracción del PDF: {str(e)}"
