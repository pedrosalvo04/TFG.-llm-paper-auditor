<<<<<<< Updated upstream
"""Skill híbrido para extracción usando RAG y esquemas estructurados"""
import json
import re
from typing import Any, Dict
from pydantic import BaseModel, Field
from backend.skills.base_skill import BaseSkill
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from backend.common.config import RAG_MODEL_NAME

class Hyperparameters(BaseModel):
    learning_rate: str = Field(description="Learning rate value, e.g., '1e-4', '0.001', '3 x 10^-4', or 'NOT FOUND'")
    batch_size: str = Field(description="Batch size value, e.g., '32', '256', or 'NOT FOUND'")
    epochs: str = Field(description="Number of epochs, e.g., '100', '10', or 'NOT FOUND'")
    optimizer: str = Field(description="Optimizer name, e.g., 'AdamW', 'SGD', or 'NOT FOUND'")
    warmup_steps: str = Field(description="Warmup steps or ratio, e.g., '1000', '0.1', or 'NOT FOUND'")
    weight_decay: str = Field(description="Weight decay value, e.g., '0.01', '1e-5', or 'NOT FOUND'")
    random_seed: str = Field(description="Random seed value, e.g., '42', or 'NOT FOUND'")
    betas: str = Field(description="Adam betas, e.g., '(0.9, 0.999)', or 'NOT FOUND'")
    epsilon: str = Field(description="Adam epsilon, e.g., '1e-8', or 'NOT FOUND'")
    hardware: str = Field(description="Hardware details, e.g., '8x NVIDIA A100', '1 TPU v4', or 'NOT FOUND'")
=======
"""
Skill híbrido para extracción de hiperparámetros usando RAG + Structured Outputs.

Mejoras de esta versión:
  1. Chunking Estructural: si el contexto contiene `structural_chunks` (generados
     por Docling en pdf_parser.py), se usan en lugar de RecursiveCharacterTextSplitter.
     Cada sección del paper es un chunk, cada tabla es un chunk INDEPENDIENTE.
     Esto resuelve el problema de las tablas de hiperparámetros partidas a mitad.

  2. Inyección de Tablas: los chunks de tipo "table" se describen con un LLM ligero
     antes de vectorizarlos ("Esta tabla resume los hiperparámetros de SFT..."),
     y la descripción es lo que se vectoriza (la tabla cruda se conserva como metadato).

  3. Structured Outputs: las fases MAP y REDUCE usan response_schema (RAGFragmentResult
     y RAGReduceResult). Elimina json.loads() + re.sub() + el loop de stack de llaves.

  4. Sin time.sleep() manuales: los reintentos de embeddings usan tenacity.
     El backoff del LLM lo gestiona LLMClient automáticamente.

  5. Fallback transparente: si no hay structural_chunks (paper subido como .txt/.md),
     se usa RecursiveCharacterTextSplitter como antes.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

import chromadb
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from backend.skills.base_skill import BaseSkill
from backend.common.config import MAP_MODEL_NAME, REDUCE_MODEL_NAME, EMBEDDING_MODEL_NAME
from backend.common.schemas import RAGFragmentResult, RAGReduceResult
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------------------------------
# Reintento para la API de Embeddings (httpx, no LLMClient)
# ---------------------------------------------------------------------------

@retry(
    retry=retry_if_exception_type(Exception),
    wait=wait_exponential(multiplier=1, min=5, max=60),
    stop=stop_after_attempt(4),
    reraise=True,
)
def _batch_embed(url: str, requests_payload: list) -> list:
    """
    Llama a la API de Embeddings con Exponential Backoff.
    Reemplaza el time.sleep(15) manual entre batches.
    """
    response = httpx.post(url, json={"requests": requests_payload}, timeout=60.0)
    if response.status_code in (429, 503):
        raise Exception(f"Rate limit/unavailable: {response.status_code} {response.text[:200]}")
    if response.status_code != 200:
        raise Exception(f"Error embeddings API: {response.status_code} {response.text[:500]}")
    return [emb["values"] for emb in response.json().get("embeddings", [])]


# ---------------------------------------------------------------------------
# Skill principal
# ---------------------------------------------------------------------------
>>>>>>> Stashed changes

class HybridHyperparameterExtractionSkill(BaseSkill):
    """
    Extrae hiperparámetros usando un pipeline híbrido:
      Chunking Estructural (Docling) → Embeddings → ChromaDB RAG
      → MAP (Structured Output por chunk) → REDUCE (consolidación)
    """

    # Queries semánticas para recuperar chunks relevantes del vectorstore
    RAG_QUERIES = [
        "training details optimization hyperparameters",
        "learning rate schedule step size warmup decay",
        "batch size mini-batch micro-batch global batch size",
        "epochs training steps iterations convergence",
        "optimizer Adam SGD AdamW RMSprop momentum betas",
        "weight decay L2 regularization",
        "random seed reproducibility initialization",
        "hardware GPU TPU NVIDIA AMD cluster infrastructure",
        "hyperparameters configuration settings appendix table",
        "experimental setup implementation details training configuration",
        "SFT supervised fine-tuning instruction tuning",
        "pre-training pretraining protocols",
        "hyperparameter table training setup ablation",
    ]

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ["paper_text"]):
            return {"extracted_hyperparameters_hybrid": {}}

        self.log_execution("🔍 Iniciando Hybrid RAG + Structured Extraction de Hiperparámetros...")
        paper_text = context["paper_text"]

        try:
<<<<<<< Updated upstream
            # 1. Chunking
            self.log_execution("Fragmentando el texto de forma exhaustiva...")
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=300)
            chunks = splitter.split_text(paper_text)
            self.log_execution(f"📄 Texto fragmentado en {len(chunks)} chunks.")
            
            # 2. Embedding & RAG
            self.log_execution("Generando embeddings para RAG (SentenceTransformers local)...")
            
            # Usamos SentenceTransformer local porque la API gratuita de Gemini 
            # solo permite 100 peticiones por minuto para embeddings, lo que 
            # rompe al procesar papers largos de +100 chunks.
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(chunks).tolist()
            
            chroma_client = chromadb.Client()
            try:
                chroma_client.delete_collection("paper_chunks")
            except:
                pass
            collection = chroma_client.create_collection(name="paper_chunks")
            
            ids = [str(i) for i in range(len(chunks))]
            collection.add(
                embeddings=embeddings,
                documents=chunks,
                ids=ids
            )
            
            queries = [
                "training details optimization hyperparameters",
                "learning rate schedule step size warmup decay learning rate",
                "batch size mini-batch micro-batch optimization global batch size",
                "epochs training steps iterations convergence training duration",
                "optimizer Adam SGD AdamW RMSprop momentum betas optimizer settings",
                "weight decay L2 regularization weight decay",
                "random seed reproducibility seed fixed seed initialization",
                "hardware GPU TPU NVIDIA AMD cluster infrastructure hardware setup",
                "hyperparameters configuration settings parameters appendix details",
                "experimental setup implementation details training configuration",
                "SFT Supervised Fine-tuning instruction tuning training schedule",
                "pre-training pretraining phase training protocols",
                "hyperparameter tuning iterations schedule iterations iterations"
            ]
            
            query_embeddings = model.encode(queries).tolist()
            results = collection.query(
                query_embeddings=query_embeddings,
                n_results=25
            )
            
            # Combinar fragmentos relevantes únicos
            relevant_chunks = set()
            for doc_list in results['documents']:
                for doc in doc_list:
                    relevant_chunks.add(doc)
            
            rag_context = "\n\n...\n\n".join(relevant_chunks)
            self.log_execution(f"🎯 Contexto filtrado por RAG: {len(relevant_chunks)} chunks únicos recuperados ({len(rag_context)} caracteres totales).")
            
            # 3. Structured Extraction using Gemini
            prompt = f"""
            You are a rigorous NeurIPS reviewer and an expert AI researcher. 
            Your task is to comprehensively analyze the following relevant excerpts of a paper to extract EXACT hyperparameters and training details.
            
            IMPORTANT: Many modern papers have MULTIPLE training phases (e.g., Pre-training, SFT, RLHF, Fine-tuning). 
            - Look for hyperparameters in ALL phases.
            - If you find different values for different phases (e.g., Pre-training batch size is 1280 but SFT batch size is 256), extract the one that seems most representative of the main model or report the most prominent one.
            - Be extremely careful with 'epochs' and 'learning rate' in the SFT/Fine-tuning sections, as they are often stated clearly there.
            
            EXCERPTS:
            {rag_context}
            
            Extract the values and return them strictly matching the JSON schema. 
            If a value is not explicitly stated after reviewing all excerpts, output 'NOT FOUND'. Do not guess or hallucinate.
            """
            
            self.log_execution(f"🧠 Consultando a LLM ({RAG_MODEL_NAME}) para extracción estructurada...")
            response = self.llm_client.client.models.generate_content(
                model=RAG_MODEL_NAME,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': Hyperparameters,
                    'temperature': 0.0
                }
            )
            
            extracted_json = json.loads(response.text)
            self.log_execution(f"📥 Respuesta cruda del LLM:\n{json.dumps(extracted_json, indent=2)}")
            
            # 4. Regex Cleaning
            cleaned_data = self._clean_with_regex(extracted_json)
            
            self.log_execution("✅ Hyperparametros extraídos exitosamente usando pipeline híbrido")
            return {'extracted_hyperparameters_hybrid': cleaned_data}
            
=======
            # ------------------------------------------------------------------
            # 1. Construir chunks — estructurales (Docling) o de caracteres
            # ------------------------------------------------------------------
            structural_chunks = context.get("structural_chunks")

            if structural_chunks:
                self.log_execution(
                    f"🏗️ Usando Chunking Estructural de Docling: "
                    f"{len(structural_chunks)} chunks "
                    f"({sum(1 for c in structural_chunks if c.chunk_type == 'table')} tablas, "
                    f"{sum(1 for c in structural_chunks if c.chunk_type == 'section')} secciones)."
                )
                texts, metadatas = self._prepare_structural_texts(structural_chunks)
            else:
                self.log_execution(
                    "⚠️ No hay structural_chunks (paper como texto). "
                    "Usando fallback RecursiveCharacterTextSplitter."
                )
                texts, metadatas = self._prepare_character_texts(paper_text)

            self.log_execution(f"📄 Total de textos a vectorizar: {len(texts)}")

            # ------------------------------------------------------------------
            # 2. Embedding con Exponential Backoff (reemplaza time.sleep(15))
            # ------------------------------------------------------------------
            embeddings = self._embed_texts(texts)
            self.log_execution(f"✅ Embeddings generados para {len(texts)} chunks.")

            # ------------------------------------------------------------------
            # 3. Vectorstore ChromaDB en memoria
            # ------------------------------------------------------------------
            collection = self._build_chromadb(texts, embeddings)

            # ------------------------------------------------------------------
            # 4. RAG: recuperar chunks relevantes
            # ------------------------------------------------------------------
            relevant_chunks, chunk_distances = self._retrieve_relevant_chunks(collection)
            self.log_execution(
                f"🎯 RAG: {len(relevant_chunks)} chunks únicos recuperados."
            )

            # ------------------------------------------------------------------
            # 5. Fase MAP: extracción estructurada por chunk (Structured Outputs)
            # ------------------------------------------------------------------
            self.log_execution(
                f"🧠 [Fase MAP] Extrayendo de {len(relevant_chunks)} fragmentos "
                f"con {MAP_MODEL_NAME}..."
            )
            extracted_fragments = self._map_phase(relevant_chunks, chunk_distances, metadatas, texts)

            # ------------------------------------------------------------------
            # 6. Fase REDUCE: consolidación (Structured Outputs)
            # ------------------------------------------------------------------
            self.log_execution(
                f"🧠 [Fase REDUCE] Consolidando {len(extracted_fragments)} extracciones "
                f"con {REDUCE_MODEL_NAME}..."
            )
            extracted_json = self._reduce_phase(extracted_fragments)
            self.log_execution(
                f"📥 Respuesta consolidada:\n{json.dumps(extracted_json, indent=2)}"
            )

            # ------------------------------------------------------------------
            # 7. Post-normalización numérica
            # ------------------------------------------------------------------
            cleaned_data = self._clean_with_regex(extracted_json)

            self.log_execution("✅ Hiperparámetros extraídos con pipeline híbrido RAG estructural.")
            return {
                "extracted_hyperparameters_hybrid": cleaned_data,
                "triage_fragments": extracted_fragments,
            }

>>>>>>> Stashed changes
        except Exception as e:
            self.log_execution(f"❌ Error en la extracción híbrida: {str(e)}", level="error")
            return {"extracted_hyperparameters_hybrid": {}, "hybrid_extraction_error": str(e)}

    # ------------------------------------------------------------------
    # Preparación de textos a vectorizar
    # ------------------------------------------------------------------

    def _prepare_structural_texts(self, structural_chunks) -> tuple[List[str], List[dict]]:
        """
        Convierte StructuralChunks en textos a vectorizar.

        Para tablas: usa tabla_description si está disponible, sino genera
        un header descriptivo con el título de sección + caption.
        La tabla cruda siempre se conserva en los metadatos.
        """
        texts: List[str] = []
        metadatas: List[dict] = []

        for chunk in structural_chunks:
            embed_text = chunk.to_embed_text()
            texts.append(embed_text)
            metadatas.append({
                "chunk_type": chunk.chunk_type,
                "section_title": chunk.section_title,
                "page_num": chunk.page_num,
                "raw_content": chunk.content,
                "table_caption": chunk.table_caption,
            })

        return texts, metadatas

    def _prepare_character_texts(self, paper_text: str) -> tuple[List[str], List[dict]]:
        """Fallback: chunking por caracteres (comportamiento legacy)."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
        chunks = splitter.split_text(paper_text)
        texts = chunks
        metadatas = [
            {"chunk_type": "text", "section_title": "", "page_num": 0,
             "raw_content": c, "table_caption": ""}
            for c in chunks
        ]
        return texts, metadatas

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    def _embed_texts(self, texts: List[str]) -> List[list]:
        """Genera embeddings en batches con backoff automático."""
        api_key = os.getenv("GOOGLE_API_KEY")
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{EMBEDDING_MODEL_NAME}:batchEmbedContents?key={api_key}"
        )

        embeddings: List[list] = []
        batch_size = 15

        for i in range(0, len(texts), batch_size):
            batch = texts[i: i + batch_size]
            requests_payload = [
                {
                    "model": f"models/{EMBEDDING_MODEL_NAME}",
                    "content": {"parts": [{"text": t}]},
                }
                for t in batch
            ]
            batch_embeddings = _batch_embed(url, requests_payload)
            embeddings.extend(batch_embeddings)
            self.log_execution(
                f"  → Batch {i // batch_size + 1}: {len(batch_embeddings)} embeddings."
            )

        return embeddings

    # ------------------------------------------------------------------
    # Vectorstore
    # ------------------------------------------------------------------

    def _build_chromadb(self, texts: List[str], embeddings: List[list]):
        """Crea la colección ChromaDB en memoria y añade los embeddings."""
        chroma_client = chromadb.Client()
        try:
            chroma_client.delete_collection("paper_chunks")
        except Exception:
            pass
        collection = chroma_client.create_collection(name="paper_chunks")
        collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=[str(i) for i in range(len(texts))],
        )
        return collection

    def _retrieve_relevant_chunks(self, collection) -> tuple[List[str], Dict[str, float]]:
        """Recupera los chunks más relevantes para las queries de RAG."""
        q_emb_res = self.llm_client.client.models.embed_content(
            model=EMBEDDING_MODEL_NAME, contents=self.RAG_QUERIES
        )
        query_embeddings = [e.values for e in q_emb_res.embeddings]

        results = collection.query(query_embeddings=query_embeddings, n_results=10)

        # Combinar únicos conservando la distancia mínima (mayor relevancia)
        chunk_relevance: Dict[str, float] = {}
        for docs, dists in zip(results["documents"], results["distances"]):
            for doc, dist in zip(docs, dists):
                if doc not in chunk_relevance or dist < chunk_relevance[doc]:
                    chunk_relevance[doc] = dist

        sorted_chunks = sorted(chunk_relevance.items(), key=lambda x: x[1])
        return [c[0] for c in sorted_chunks], {c[0]: c[1] for c in sorted_chunks}

    # ------------------------------------------------------------------
    # MAP phase
    # ------------------------------------------------------------------

    def _map_phase(
        self,
        relevant_chunks: List[str],
        chunk_distances: Dict[str, float],
        metadatas: List[dict],
        all_texts: List[str],
    ) -> List[dict]:
        """Extrae hiperparámetros de cada chunk con Structured Output."""
        # Mapa texto → metadato para enriquecer cada fragmento
        text_to_meta = {t: m for t, m in zip(all_texts, metadatas)}
        extracted_fragments: List[dict] = []

        for idx, chunk_text in enumerate(relevant_chunks):
            distance = chunk_distances.get(chunk_text, 1.0)
            relevance_score = self._distance_to_score(distance)
            meta = text_to_meta.get(chunk_text, {})
            chunk_type = meta.get("chunk_type", "text")
            section = meta.get("section_title", "")
            raw_content = meta.get("raw_content", chunk_text)

            # Prompt adaptado al tipo de chunk
            if chunk_type == "table":
                caption = meta.get("table_caption", "")
                prompt = (
                    f"You are a rigorous NeurIPS reviewer. Analyze this TABLE from section "
                    f"'{section}'{f' (caption: {caption})' if caption else ''}.\n"
                    f"Extract ALL hyperparameters and training metrics present in the table.\n\n"
                    f"TABLE CONTENT:\n{raw_content}\n\n"
                    "Use 'NOT FOUND' for fields not present in this table.\n"
                    "Pay special attention to: learning rate, batch size, optimizer, "
                    "training steps, hardware, weight decay."
                )
            else:
                prompt = (
                    f"You are a rigorous NeurIPS reviewer analyzing a TEXT SECTION "
                    f"titled '{section}'.\n"
                    f"Extract all hyperparameters, scale metrics, and performance data.\n\n"
                    f"FIELDS: learning_rate, batch_size, epochs, training_steps, total_tokens, "
                    f"optimizer, warmup_steps, weight_decay, hardware, latency_metrics.\n\n"
                    f"TEXT:\n{raw_content}\n\n"
                    "Use 'NOT FOUND' for missing fields."
                )

            try:
                # Structured Output: RAGFragmentResult garantiza JSON válido
                response = self.llm_client.generate(prompt, response_schema=RAGFragmentResult)
                fragment_data = json.loads(response.text)
                fragment_data["_relevance_score"] = relevance_score
                fragment_data["_chunk_text"] = raw_content
                fragment_data["_chunk_type"] = chunk_type
                fragment_data["_section_title"] = section
                extracted_fragments.append(fragment_data)
            except Exception as e:
                self.log_execution(
                    f"⚠️ Error extrayendo fragmento {idx} ({chunk_type}/{section}): {e}",
                    level="warning",
                )

        return extracted_fragments

    # ------------------------------------------------------------------
    # REDUCE phase
    # ------------------------------------------------------------------

    def _reduce_phase(self, extracted_fragments: List[dict]) -> dict:
        """Consolida todos los fragmentos MAP en un único JSON."""
        reduce_prompt = (
            "You are a senior AI researcher consolidating hyperparameter extractions from a paper.\n"
            "Below are independent extractions from TEXT SECTIONS and TABLES.\n"
            "NOTE: TABLE extractions are more reliable than text extractions for exact values.\n\n"
            "RULES:\n"
            "- Prefer TABLE extractions over text extractions for numeric values.\n"
            "- If there are conflicts, prefer the most specific/exact value.\n"
            "- If an extraction says 'NOT FOUND', ignore it if another found a valid value.\n"
            "- If no valid value is found across all fragments, output 'NOT FOUND'.\n"
            "- DO NOT guess or hallucinate.\n\n"
            f"EXTRACTIONS:\n{json.dumps(extracted_fragments, indent=2)}"
        )

        # Structured Output: RAGReduceResult garantiza JSON válido
        reduce_response = self.llm_client.generate(
            reduce_prompt, response_schema=RAGReduceResult
        )
        return json.loads(reduce_response.text)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _distance_to_score(distance: float) -> int:
        """Convierte distancia ChromaDB (menor=mejor) a score de confianza 0-100."""
        if distance < 0.4:
            return int(95 - distance * 25)
        elif distance < 0.7:
            return int(85 - (distance - 0.4) * 180)
        else:
            return max(5, int(31 - (distance - 0.7) * 50))

    def _clean_with_regex(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-normalización numérica de los valores extraídos.
        Solo convierte strings a tipos numéricos. No parsea JSON.
        """
        cleaned: Dict[str, Any] = {}
        for key, value in data.items():
            str_val = str(value).strip()
            if str_val.upper() in ("NOT FOUND", "N/A", "NONE", "MISSING") or not str_val:
                cleaned[key] = "NOT FOUND"
                continue

            if key in ("learning_rate", "weight_decay"):
                match = re.search(
                    r"(\d+(?:\.\d+)?)\s*(?:[x*]\s*10\s*\^?\s*\(?\s*(-\d+)\s*\)?|e(-\d+))",
                    str_val, re.IGNORECASE,
                )
                if match:
                    base = float(match.group(1))
                    exp = int(match.group(2) if match.group(2) else match.group(3))
                    cleaned[key] = float(f"{base * (10 ** exp):.8f}")
                else:
                    m = re.search(r"0\.\d+", str_val)
                    cleaned[key] = float(m.group()) if m else str_val

            elif key in ("batch_size", "epochs", "random_seed"):
                m = re.search(r"\b\d+\b", str_val)
                cleaned[key] = int(m.group()) if m else str_val

            else:
                cleaned[key] = str_val

        return cleaned
