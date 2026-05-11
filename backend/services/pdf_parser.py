"""Servicio de parsing de archivos PDF"""
from docling.document_converter import DocumentConverter
from backend.common.logger import get_logger

logger = get_logger(__name__)

def convert_pdf_to_markdown(pdf_path, use_gpu=False):
    """
    Convierte un PDF a formato Markdown optimizado para LLMs usando Docling,
    preservando tablas y listas.
    
    Args:
        pdf_path: Ruta al archivo PDF
        use_gpu: Si se debe intentar usar aceleración por GPU (CUDA)
        
    Returns:
        Texto en formato Markdown
    """
    try:
        logger.info(f"Convirtiendo PDF a Markdown con Docling (Modo Robusto por Bloques): {pdf_path}")
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
        
        # Configurar dispositivo (CPU o GPU)
        import torch
        cuda_available = torch.cuda.is_available()
        
        if use_gpu:
            if cuda_available:
                device = "cuda"
                logger.info("🚀 GPU detectada y solicitada. Usando CUDA para Docling.")
            else:
                device = "cpu"
                logger.warning("⚠️ GPU solicitada pero CUDA no está disponible en este sistema. Usando CPU.")
        else:
            device = "cpu"
            logger.info("ℹ️ Usando dispositivo CPU para Docling (GPU no solicitada).")
            
        pipeline_options.accelerator_options.device = device
        
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
            logger.info(f"⏳ Procesando bloque de páginas: {start_page+1} a {end_page}...")
            
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
                logger.info(f"✅ Bloque {start_page+1}-{end_page} completado.")
            except Exception as block_error:
                logger.error(f"❌ Error en bloque {start_page+1}-{end_page}: {str(block_error)}")
                full_md_text += f"\n\n> [!ERROR] Error al procesar páginas {start_page+1}-{end_page}: {str(block_error)}\n\n"
            finally:
                # Limpiar archivo temporal
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        logger.info(f"🚀 Conversión total completada ({len(full_md_text)} caracteres)")
        return full_md_text
    except Exception as e:
        logger.error(f"❌ Error en la extracción del PDF: {str(e)}")
        return f"❌ Error en la extracción del PDF: {str(e)}"
