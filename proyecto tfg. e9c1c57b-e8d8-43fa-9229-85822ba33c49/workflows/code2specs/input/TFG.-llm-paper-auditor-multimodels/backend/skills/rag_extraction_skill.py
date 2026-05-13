"""Skill híbrido para extracción usando RAG y esquemas estructurados"""
import json
import re
from typing import Any, Dict
from pydantic import BaseModel, Field
from backend.skills.base_skill import BaseSkill
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from backend.common.config import MAP_MODEL_NAME, REDUCE_MODEL_NAME, EMBEDDING_MODEL_NAME

class Hyperparameters(BaseModel):
    thought_process: str = Field(description="Internal reasoning about the technical details found in this fragment, specifically comparing reported values like compute hours vs efficiency claims.")
    learning_rate: str = Field(description="Learning rate value, e.g., '1e-4', '0.001', '3 x 10^-4', or 'NOT FOUND'")
    batch_size: str = Field(description="Batch size value, e.g., '32', '256', or 'NOT FOUND'")
    epochs: str = Field(description="Number of epochs, e.g., '100', '10', or 'NOT FOUND'")
    optimizer: str = Field(description="Optimizer name, e.g., 'AdamW', 'SGD', or 'NOT FOUND'")
    warmup_steps: str = Field(description="Warmup steps or ratio, e.g., '1000', '0.1', or 'NOT FOUND'")
    weight_decay: str = Field(description="Weight decay value, e.g., '0.01', '1e-5', or 'NOT FOUND'")
    random_seed: str = Field(description="Random seed value, e.g., '42', or 'NOT FOUND'")
    betas: str = Field(description="Adam betas, e.g., '(0.9, 0.999)', or 'NOT FOUND'")
    epsilon: str = Field(description="Adam epsilon, e.g., '1e-8', or 'NOT FOUND'")
    training_steps: str = Field(description="Total optimization steps, e.g., '100k', '50000', or 'NOT FOUND'")
    total_tokens: str = Field(description="Total tokens trained on, e.g., '3T', '100B', or 'NOT FOUND'")
    hardware: str = Field(description="Hardware details, e.g., '8x NVIDIA A100', '1 TPU v4', or 'NOT FOUND'")
    latency_metrics: str = Field(description="Performance metrics like latency or throughput, e.g., '2% increase', '100 tokens/sec', or 'NOT FOUND'")

class HybridHyperparameterExtractionSkill(BaseSkill):
    """Extrae hiperparámetros usando un pipeline híbrido (RAG + Pydantic/Gemini + Regex)"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'extracted_hyperparameters_hybrid': {}}
            
        self.log_execution("🔍 Iniciando Hybrid RAG + Structured Extraction de Hyperparametros...")
        paper_text = context['paper_text']
        
        try:
            # 1. Chunking Lógico (basado en bloques identificados por Docling)
            self.log_execution("Fragmentando el texto por bloques lógicos (párrafos/tablas)...")
            
            # Split por doble salto de línea (estándar de Docling para separar elementos)
            import re
            paper_text_norm = paper_text.replace('\r\n', '\n')
            raw_chunks = re.split(r'\n\n+', paper_text_norm)
            
            # Limpiar y filtrar chunks vacíos o extremadamente irrelevantes
            chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]
            
            self.log_execution(f"📄 Texto fragmentado en {len(chunks)} bloques lógicos (sin cortes arbitrarios).")
            
            # 2. Embedding & RAG
            self.log_execution(f"Generando embeddings para RAG ({EMBEDDING_MODEL_NAME})...")
            
            # Usamos Gemini API para embeddings en lugar de SentenceTransformer local
            # Agrupamos en bloques pequeños y añadimos pausas para no exceder TPM (30K tokens/min).
            import time
            import os
            import httpx
            
            embeddings = []
            batch_size = 15 # Reducido a 15 para apuntar a 60 RPM (margen muy seguro frente al límite de 100)
            api_key = os.getenv("GOOGLE_API_KEY")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL_NAME}:batchEmbedContents?key={api_key}"
            
            for i in range(0, len(chunks), batch_size):
                if i > 0:
                    time.sleep(15) # Pausa de 15s (15 requests / 15s = 60 requests/min, un 60% del límite)
                
                batch = chunks[i:i+batch_size]
                
                # Bypasseamos el SDK usando httpx directo porque 'embed_content' fusionaba la lista en un único vector
                requests = [{"model": f"models/{EMBEDDING_MODEL_NAME}", "content": {"parts": [{"text": c}]}} for c in batch]
                
                response = httpx.post(url, json={"requests": requests})
                if response.status_code != 200:
                    self.log_execution(f"❌ Error en API Embeddings: {response.text}", level="error")
                    raise Exception(f"Error embeddings API: {response.text}")
                    
                data = response.json()
                for emb in data.get("embeddings", []):
                    embeddings.append(emb["values"])
            
            self.log_execution(f"✅ Embeddings generados para {len(chunks)} chunks.")
            
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
            
            q_emb_res = self.llm_client.client.models.embed_content(
                model=EMBEDDING_MODEL_NAME,
                contents=queries
            )
            query_embeddings = [e.values for e in q_emb_res.embeddings]
            
            results = collection.query(
                query_embeddings=query_embeddings,
                n_results=10
            )
            
            # Combinar fragmentos relevantes únicos manteniendo la mejor distancia (menor score es mejor en Chroma)
            chunk_relevance = {}
            for i in range(len(results['documents'])):
                docs = results['documents'][i]
                dists = results['distances'][i]
                for doc, dist in zip(docs, dists):
                    if doc not in chunk_relevance or dist < chunk_relevance[doc]:
                        chunk_relevance[doc] = dist
            
            # Ordenar por relevancia (distancia ascendente)
            sorted_chunks = sorted(chunk_relevance.items(), key=lambda x: x[1])
            relevant_chunks = [c[0] for c in sorted_chunks]
            chunk_distances = {c[0]: c[1] for c in sorted_chunks}
            
            self.log_execution(f"🎯 Contexto filtrado por RAG: {len(relevant_chunks)} chunks únicos recuperados.")
            
            # 3. MAP Phase: Structured Extraction using Flash Lite
            self.log_execution(f"🧠 [Fase MAP] Extrayendo de {len(relevant_chunks)} fragmentos con {MAP_MODEL_NAME}...")
            
            extracted_fragments = []
            
            for idx, chunk in enumerate(relevant_chunks):
                # Incluir metadatos de relevancia en el objeto final
                distance = chunk_distances.get(chunk, 1.0)
                # Convertir distancia a score de confianza (0-100)
                # Escala recalibrada: distancias < 0.4 son excelentes (85%+), distancias > 0.7 son ruido (<30%)
                if distance < 0.4:
                    relevance_score = int(95 - (distance * 25)) # 0.0 -> 95%, 0.4 -> 85%
                elif distance < 0.7:
                    relevance_score = int(85 - ((distance - 0.4) * 180)) # 0.4 -> 85%, 0.7 -> 31%
                else:
                    relevance_score = max(5, int(31 - ((distance - 0.7) * 50))) # >0.7 -> degradación lenta
                
                prompt = f"""
                You are a rigorous NeurIPS reviewer performing technical triage on a paper fragment.
                Extract all hyperparameters, scale metrics, and performance data found in this text.
                
                FIELDS TO EXTRACT:
                - learning_rate, batch_size, epochs, training_steps, total_tokens, optimizer, warmup_steps, weight_decay, hardware, latency_metrics.
                
                REASONING INSTRUCTIONS:
                - If the fragment contains optimization steps (e.g. "100k steps") or total tokens (e.g. "2 trillion tokens"), extract them as training_steps and total_tokens.
                - Capture any performance data like "latency was less than 2%" or "throughput of 500 tokens/s" under latency_metrics.
                - Be smart about noisy table text (e.g., if columns are misaligned, try to reconstruct the key-value pair logically).
                
                TEXT FRAGMENT:
                {chunk}
                
                RETURN ONLY A VALID JSON OBJECT WITH THE FIELDS ABOVE. Use "NOT FOUND" if missing.
                """
                try:
                    # Usar el método generate con reintentos para evitar 503
                    response = self.llm_client.generate(prompt)
                    raw_text = response.text.strip()
                    
                    # Extracción balanceada de JSON (evita el error "Extra data")
                    start_idx = raw_text.find('{')
                    if start_idx != -1:
                        stack = 0
                        for i in range(start_idx, len(raw_text)):
                            if raw_text[i] == '{': stack += 1
                            elif raw_text[i] == '}':
                                stack -= 1
                                if stack == 0:
                                    raw_text = raw_text[start_idx:i+1]
                                    break
                    
                    fragment_data = json.loads(raw_text)
                    fragment_data['_relevance_score'] = relevance_score
                    fragment_data['_chunk_text'] = chunk
                    extracted_fragments.append(fragment_data)
                    
                    # Pausa para evitar 503
                    time.sleep(1)
                except Exception as e:
                    self.log_execution(f"⚠️ Error extrayendo fragmento {idx}: {str(e)}", level="warning")
            
            # 4. REDUCE Phase: Consolidate with Gemma 4
            self.log_execution("🧠 [Fase REDUCE] Consolidando datos extraídos con Gemma 4...")
            
            reduce_prompt = f"""
            You are a senior AI researcher reviewing a paper's hyperparameter extraction.
            Below is a list of independent extractions from various parts of the paper (e.g., Pre-training, SFT, RLHF).
            Your job is to consolidate them into a single definitive set of hyperparameters.
            
            RULES:
            - If there are conflicts (e.g. SFT batch size is 256, Pre-training is 1280), prefer the final fine-tuning/SFT parameters if obvious, or pick the most representative one.
            - If an extraction says 'NOT FOUND', ignore it if another extraction found a valid value.
            - If no valid value is found across all fragments for a field, output 'NOT FOUND'.
            - Use the 'thought_process' from each fragment to build a final synthesis.
            - TABLE VALIDATION: If multiple fragments cite different tables for the same value, verify which table title and headers match the target hyperparameter (e.g., differentiate between a 'Model Architecture' table and a 'Training Hyperparameters' table).
            - DO NOT guess or hallucinate.
            
            EXTRACTIONS:
            {json.dumps(extracted_fragments, indent=2)}
            """
            
            self.log_execution("🚀 [REDUCE] Consolidando datos con Gemma 4 (TPM Ilimitado)...")
            
            from backend.common.config import EVALUATION_MODEL_NAME
            
            try:
                # Usar el método generate con reintentos para la consolidación
                reduce_response = self.llm_client.generate(reduce_prompt)
                raw_reduce_text = reduce_response.text.strip()
            except Exception as e:
                self.log_execution(f"⚠️ Error con Gemma 4 en RAG, reintentando con {EVALUATION_MODEL_NAME}: {str(e)}", level="warning")
                # Fallback manual con Pydantic si el general falla
                reduce_response = self.llm_client.client.models.generate_content(
                    model=EVALUATION_MODEL_NAME,
                    contents=reduce_prompt,
                    config={
                        'response_mime_type': 'application/json',
                        'response_schema': Hyperparameters,
                        'temperature': 0.0
                    }
                )
                raw_reduce_text = reduce_response.text.strip()
            # Extracción balanceada de JSON (evita el error "Extra data")
            start_idx = raw_reduce_text.find('{')
            if start_idx != -1:
                stack = 0
                for i in range(start_idx, len(raw_reduce_text)):
                    if raw_reduce_text[i] == '{': stack += 1
                    elif raw_reduce_text[i] == '}':
                        stack -= 1
                        if stack == 0:
                            raw_reduce_text = raw_reduce_text[start_idx:i+1]
                            break
            
            try:
                extracted_json = json.loads(raw_reduce_text)
            except json.JSONDecodeError:
                # Intento de reparación de comas extra si falla
                fixed_text = re.sub(r',\s*([\]}])', r'\1', raw_reduce_text)
                extracted_json = json.loads(fixed_text)
            self.log_execution(f"📥 Respuesta consolidada del LLM:\n{json.dumps(extracted_json, indent=2)}")
            
            # 5. Regex Cleaning
            cleaned_data = self._clean_with_regex(extracted_json)
            
            self.log_execution("✅ Hyperparametros extraídos exitosamente usando pipeline híbrido")
            return {
                'extracted_hyperparameters_hybrid': cleaned_data,
                'triage_fragments': extracted_fragments # Para visualización en el frontend
            }
            
        except Exception as e:
            self.log_execution(f"❌ Error en la extracción híbrida: {str(e)}", level="error")
            return {'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str(e)}

    def _clean_with_regex(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Limpia los valores usando expresiones regulares (Regex)"""
        cleaned = {}
        for key, value in data.items():
            str_val = str(value).strip()
            upper_val = str_val.upper()
            if upper_val in ['NOT FOUND', 'N/A', 'NONE', 'MISSING'] or str_val == '':
                cleaned[key] = 'NOT FOUND'
                continue
                
            if key in ['learning_rate', 'weight_decay']:
                # Extraer notación científica tipo "3 x 10^-4" o "1e-4"
                match = re.search(r'(\d+(?:\.\d+)?)\s*(?:[x*]\s*10\s*\^?\s*\(?\s*(-\d+)\s*\)?|e(-\d+))', str_val, re.IGNORECASE)
                if match:
                    base = float(match.group(1))
                    exp = int(match.group(2) if match.group(2) else match.group(3))
                    cleaned[key] = float(f"{base * (10 ** exp):.8f}")
                else:
                    # Intento de extracción de float puro
                    match_float = re.search(r'0\.\d+', str_val)
                    if match_float:
                        cleaned[key] = float(match_float.group())
                    else:
                        cleaned[key] = str_val
            elif key == 'epsilon':
                # Extraer notación científica tipo "1e-8"
                match = re.search(r'1e-\d+', str_val, re.IGNORECASE)
                if match:
                    cleaned[key] = str_val
                else:
                    cleaned[key] = str_val
            elif key in ['batch_size', 'epochs', 'random_seed']:
                # Extraer primer número entero
                match = re.search(r'\b\d+\b', str_val)
                if match:
                    cleaned[key] = int(match.group())
                else:
                    cleaned[key] = str_val
            else:
                cleaned[key] = str_val
        return cleaned
