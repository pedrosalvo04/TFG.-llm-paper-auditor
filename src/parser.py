from docling.document_converter import DocumentConverter

def convert_pdf_to_markdown(pdf_path):
    """
    Esta es la función que app.py está buscando.
    """
    try:
        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        return result.document.export_to_markdown()
    except Exception as e:
        return f"Error en Docling: {str(e)}"