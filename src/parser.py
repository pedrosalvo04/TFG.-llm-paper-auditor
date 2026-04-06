import pymupdf4llm

def convert_pdf_to_markdown(pdf_path):
    """
    Convierte un PDF a formato Markdown optimizado para LLMs.
    Es ultra rápido y consume muy poca memoria RAM.
    """
    try:
        # Lee el PDF y lo transforma a Markdown conservando tablas
        md_text = pymupdf4llm.to_markdown(pdf_path)
        return md_text
    except Exception as e:
        return f"❌ Error en la extracción del PDF: {str(e)}"