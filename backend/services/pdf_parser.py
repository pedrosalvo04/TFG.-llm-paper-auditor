"""Servicio de parsing de archivos PDF"""
from docling.document_converter import DocumentConverter
from backend.utils.logger import get_logger

import logging
logger = get_logger(__name__)
logging.getLogger("docling").setLevel(logging.ERROR)

def convert_pdf_to_markdown(pdf_path):
    """
    Convierte un PDF a formato Markdown optimizado para LLMs usando Docling,
    preservando tablas y listas.
    
    Args:
        pdf_path: Ruta al archivo PDF
        
    Returns:
        Texto en formato Markdown
    """
    try:
        logger.log(25, f"Convirtiendo PDF a Markdown con Docling (Modo Robusto por Bloques): {pdf_path}")
        from docling.datamodel.base_models import InputFormat
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from pypdf import PdfReader, PdfWriter
        import os
        import tempfile
        
        # Configurar Docling (Sin OCR para velocidad, pero con Tablas activas)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        
        # Intentar usar GPU (CUDA) si está disponible (Docling lo detectará automáticamente vía torch)
        import torch
        if torch.cuda.is_available():
            logger.info("🚀 GPU detectada. Docling usará aceleración CUDA automáticamente.")
        else:
            logger.info("ℹ️ No se detectó GPU compatible. Usando CPU para Docling.")
        
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        # Leer el PDF original
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        logger.info(f"📄 Total de páginas detectadas: {total_pages}")
        
        full_md_text = ""
        chunk_size = 5 # Procesar de 5 en 5 páginas para no saturar la RAM
        
        for i in range(0, total_pages, chunk_size):
            start_page = i
            end_page = min(i + chunk_size, total_pages)
            
            # Crear PDF temporal para el bloque
            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_path = tmp_file.name
                writer.write(tmp_path)
            
            try:
                # Convertir el bloque
                result = converter.convert(tmp_path)
                block_md = result.document.export_to_markdown()
                full_md_text += block_md + "\n\n"
                logger.info(f"  ⏳ Procesadas páginas {start_page+1}-{end_page} de {total_pages}")
            except Exception as block_error:
                logger.error(f"  ❌ Error en páginas {start_page+1}-{end_page}: {str(block_error)}")
                full_md_text += f"\n\n> [!ERROR] Error al procesar páginas {start_page+1}-{end_page}: {str(block_error)}\n\n"
            finally:
                # Limpiar archivo temporal
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        logger.log(25, f"🚀 Conversión total completada ({len(full_md_text)} caracteres)")
        return full_md_text
    except Exception as e:
        logger.error(f"❌ Error en la extracción del PDF: {str(e)}")
        return f"❌ Error en la extracción del PDF: {str(e)}"
