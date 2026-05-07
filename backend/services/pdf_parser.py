"""
Servicio de parsing de archivos PDF con extracción estructural.

Expone dos funciones:
  - convert_pdf_to_markdown(): comportamiento anterior (compatible con .txt/.md)
  - convert_pdf_to_structured(): NUEVO — devuelve chunks estructurales usando
    la representación interna de Docling (secciones + tablas como nodos independientes).

El chunking estructural resuelve el problema crítico del RAG:
RecursiveCharacterTextSplitter cortaba tablas de hiperparámetros a mitad, haciéndolas
inútiles para el LLM. Ahora cada tabla es un chunk independiente con metadatos.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from typing import List, Optional

from backend.utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Dataclass que representa un chunk estructural del paper
# ---------------------------------------------------------------------------

@dataclass
class StructuralChunk:
    """
    Unidad mínima de contenido estructural extraída por Docling.

    Atributos
    ----------
    chunk_type : str
        "section" para texto de sección, "table" para tabla.
    content : str
        Contenido en markdown (para secciones) o tabla markdown (para tablas).
    section_title : str
        Título de la sección padre (o encabezado más cercano).
    page_num : int
        Número de página aproximado (base 1).
    table_caption : str
        Pie de tabla si existe (solo para chunk_type="table").
    table_description : str
        Descripción generada por LLM del contenido de la tabla.
        Se rellena más tarde en el RAG skill. Vacío por defecto.
    """
    chunk_type: str          # "section" | "table"
    content: str
    section_title: str = ""
    page_num: int = 0
    table_caption: str = ""
    table_description: str = ""  # Rellenado por el LLM en el RAG skill

    def to_embed_text(self) -> str:
        """
        Texto que se vectorizará. Para tablas usa la descripción LLM si disponible,
        si no usa el contenido crudo (la tabla en markdown).
        """
        if self.chunk_type == "table":
            header = f"[TABLA] {self.section_title}"
            if self.table_description:
                return f"{header}\n{self.table_description}\n\n{self.content}"
            if self.table_caption:
                return f"{header}: {self.table_caption}\n\n{self.content}"
            return f"{header}\n\n{self.content}"
        return f"[SECCIÓN: {self.section_title}]\n\n{self.content}"

    def to_rag_document(self) -> str:
        """Texto completo que se almacena en ChromaDB como documento."""
        return self.to_embed_text()


# ---------------------------------------------------------------------------
# Función pública: convert_pdf_to_markdown (compatibilidad hacia atrás)
# ---------------------------------------------------------------------------

def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Convierte un PDF a formato Markdown usando Docling.
    Preserva tablas y listas. Compatible con la versión anterior.
    """
    try:
        logger.info(f"Convirtiendo PDF a Markdown con Docling (por bloques): {pdf_path}")

        from docling.datamodel.base_models import InputFormat
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from pypdf import PdfReader, PdfWriter

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True

        try:
            import torch
            if torch.cuda.is_available():
                logger.info("🚀 GPU detectada. Docling usará CUDA.")
            else:
                logger.info("ℹ️ Sin GPU. Usando CPU para Docling.")
        except ImportError:
            pass

        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )

        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        logger.info(f"📄 Total de páginas: {total_pages}")

        full_md_text = ""
        chunk_size = 5

        for i in range(0, total_pages, chunk_size):
            start_page = i
            end_page = min(i + chunk_size, total_pages)
            logger.info(f"⏳ Procesando páginas {start_page + 1}–{end_page}...")

            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_path = tmp_file.name
                writer.write(tmp_path)

            try:
                result = converter.convert(tmp_path)
                full_md_text += result.document.export_to_markdown() + "\n\n"
                logger.info(f"✅ Bloque {start_page + 1}–{end_page} completado.")
            except Exception as block_error:
                logger.error(f"❌ Error en bloque {start_page + 1}–{end_page}: {block_error}")
                full_md_text += (
                    f"\n\n> [!ERROR] Error al procesar páginas "
                    f"{start_page + 1}–{end_page}: {block_error}\n\n"
                )
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        logger.info(f"🚀 Conversión completada ({len(full_md_text)} caracteres)")
        return full_md_text

    except Exception as e:
        logger.error(f"❌ Error en la extracción del PDF: {e}")
        return f"❌ Error en la extracción del PDF: {e}"


# ---------------------------------------------------------------------------
# Función pública NUEVA: convert_pdf_to_structured
# ---------------------------------------------------------------------------

def convert_pdf_to_structured(pdf_path: str) -> tuple[str, List[StructuralChunk]]:
    """
    Convierte un PDF a markdown Y extrae chunks estructurales usando Docling.

    Devuelve
    --------
    (markdown_text, structural_chunks)
        markdown_text : str
            Texto completo del paper en formato markdown (para el LLM general).
        structural_chunks : List[StructuralChunk]
            Lista de chunks estructurales para el RAG:
            - Cada sección lógica → un StructuralChunk de tipo "section".
            - Cada tabla → un StructuralChunk de tipo "table" (nodo independiente).

    El objetivo es que ninguna tabla quede partida a la mitad por un corte de caracteres.
    """
    try:
        logger.info(f"🔬 Extracción estructural con Docling: {pdf_path}")

        from docling.datamodel.base_models import InputFormat
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from pypdf import PdfReader, PdfWriter

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True

        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )

        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        full_md_text = ""
        all_chunks: List[StructuralChunk] = []
        chunk_size = 5

        for i in range(0, total_pages, chunk_size):
            start_page = i
            end_page = min(i + chunk_size, total_pages)
            logger.info(f"⏳ Extracción estructural páginas {start_page + 1}–{end_page}...")

            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_path = tmp_file.name
                writer.write(tmp_path)

            try:
                result = converter.convert(tmp_path)
                doc = result.document

                # Markdown completo del bloque
                block_md = doc.export_to_markdown()
                full_md_text += block_md + "\n\n"

                # Extraer chunks estructurales del bloque
                block_chunks = _extract_structural_chunks(doc, page_offset=start_page)
                all_chunks.extend(block_chunks)

                logger.info(
                    f"✅ Bloque {start_page + 1}–{end_page}: "
                    f"{len(block_chunks)} chunks estructurales extraídos."
                )
            except Exception as block_error:
                logger.error(f"❌ Error en bloque {start_page + 1}–{end_page}: {block_error}")
                full_md_text += (
                    f"\n\n> [!ERROR] Error al procesar páginas "
                    f"{start_page + 1}–{end_page}: {block_error}\n\n"
                )
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        logger.info(
            f"🏗️ Extracción estructural completada: {len(all_chunks)} chunks "
            f"({sum(1 for c in all_chunks if c.chunk_type == 'table')} tablas, "
            f"{sum(1 for c in all_chunks if c.chunk_type == 'section')} secciones)"
        )
        return full_md_text, all_chunks

    except Exception as e:
        logger.error(f"❌ Error en extracción estructural: {e}. Fallback a markdown simple.")
        # Fallback: devolver markdown sin chunks estructurales
        md = convert_pdf_to_markdown(pdf_path)
        return md, []


# ---------------------------------------------------------------------------
# Helper interno: extrae chunks de un DoclingDocument
# ---------------------------------------------------------------------------

def _extract_structural_chunks(doc, page_offset: int = 0) -> List[StructuralChunk]:
    """
    Recorre el DoclingDocument y construye StructuralChunks.

    Estrategia:
      - Acumula texto bajo cada encabezado en un chunk de tipo "section".
      - Cada tabla se extrae como chunk independiente de tipo "table".
      - Los textos muy cortos (<50 chars) se agregan al chunk de sección actual.
    """
    chunks: List[StructuralChunk] = []
    current_section_title = "Introduction"
    current_section_content: List[str] = []
    current_page = page_offset + 1

    MIN_SECTION_LENGTH = 50  # chars mínimos para no crear chunks triviales

    def flush_section():
        """Guarda el texto acumulado de la sección actual como chunk."""
        text = "\n\n".join(current_section_content).strip()
        if len(text) >= MIN_SECTION_LENGTH:
            chunks.append(StructuralChunk(
                chunk_type="section",
                content=text,
                section_title=current_section_title,
                page_num=current_page,
            ))
        current_section_content.clear()

    try:
        # Docling expone los elementos del cuerpo del documento
        # Iterar sobre los items del documento para extraer estructura
        body_children = []

        # Intentar acceder al cuerpo del documento de varias formas
        # según la versión de Docling instalada
        if hasattr(doc, 'body') and hasattr(doc.body, 'children'):
            body_children = doc.body.children
        elif hasattr(doc, 'main_text'):
            body_children = doc.main_text

        # Si no hay estructura accesible, fallback a export_to_markdown
        if not body_children:
            logger.debug("Docling: usando iteración por texts/tables (API alternativa).")
            return _extract_chunks_via_iterators(doc, page_offset)

        for item_ref in body_children:
            try:
                item = item_ref.resolve(doc)
            except AttributeError:
                item = item_ref

            label = getattr(item, 'label', '') or ''
            label_str = str(label).lower()

            # Detectar número de página
            if hasattr(item, 'prov') and item.prov:
                prov = item.prov[0] if isinstance(item.prov, list) else item.prov
                current_page = getattr(prov, 'page_no', current_page) + page_offset

            # Encabezados → nueva sección
            if 'section' in label_str or 'heading' in label_str or 'title' in label_str:
                flush_section()
                title_text = getattr(item, 'text', '') or ''
                current_section_title = title_text.strip() or current_section_title

            # Tablas → chunk independiente
            elif 'table' in label_str:
                flush_section()  # Guardar texto previo
                try:
                    table_md = item.export_to_markdown()
                except Exception:
                    try:
                        table_md = str(item.data) if hasattr(item, 'data') else str(item)
                    except Exception:
                        table_md = "[tabla no exportable]"

                caption = ""
                if hasattr(item, 'captions') and item.captions:
                    cap = item.captions[0]
                    caption = getattr(cap, 'text', '') or ''

                chunks.append(StructuralChunk(
                    chunk_type="table",
                    content=table_md,
                    section_title=current_section_title,
                    page_num=current_page,
                    table_caption=caption,
                ))

            # Texto normal → agregar a la sección actual
            else:
                text = getattr(item, 'text', '') or ''
                if text.strip():
                    current_section_content.append(text.strip())

        # Guardar última sección
        flush_section()

    except Exception as e:
        logger.warning(f"⚠️ Error en extracción estructural por items: {e}. Usando iteradores.")
        return _extract_chunks_via_iterators(doc, page_offset)

    return chunks


def _extract_chunks_via_iterators(doc, page_offset: int = 0) -> List[StructuralChunk]:
    """
    Fallback: extrae chunks usando los iteradores de alto nivel de Docling
    (doc.texts + doc.tables) cuando la API de items no está disponible.
    """
    chunks: List[StructuralChunk] = []
    current_section = "Document"

    # Textos: agrupar por sección
    section_texts: dict = {}

    texts = getattr(doc, 'texts', []) or []
    for text_item in texts:
        label = str(getattr(text_item, 'label', '')).lower()
        text = getattr(text_item, 'text', '') or ''

        if not text.strip():
            continue

        if 'heading' in label or 'section' in label or 'title' in label:
            current_section = text.strip()
        else:
            if current_section not in section_texts:
                section_texts[current_section] = []
            section_texts[current_section].append(text.strip())

    for section_title, texts_list in section_texts.items():
        content = "\n\n".join(texts_list)
        if len(content) >= 50:
            chunks.append(StructuralChunk(
                chunk_type="section",
                content=content,
                section_title=section_title,
                page_num=page_offset + 1,
            ))

    # Tablas: cada una como chunk independiente
    tables = getattr(doc, 'tables', []) or []
    for table_item in tables:
        try:
            table_md = table_item.export_to_markdown()
        except Exception:
            table_md = str(table_item)

        caption = ""
        if hasattr(table_item, 'captions') and table_item.captions:
            caption = getattr(table_item.captions[0], 'text', '') or ''

        chunks.append(StructuralChunk(
            chunk_type="table",
            content=table_md,
            section_title=current_section,
            page_num=page_offset + 1,
            table_caption=caption,
        ))

    return chunks
