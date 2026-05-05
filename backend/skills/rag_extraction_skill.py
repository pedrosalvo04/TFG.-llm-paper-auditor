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

class HybridHyperparameterExtractionSkill(BaseSkill):
    """Extrae hiperparámetros usando un pipeline híbrido (RAG + Pydantic/Gemini + Regex)"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'extracted_hyperparameters_hybrid': {}}
            
        self.log_execution("🔍 Iniciando Hybrid RAG + Structured Extraction de Hyperparametros...")
        paper_text = context['paper_text']
        
        try:
            # 1. Chunking
            self.log_execution("Fragmentando el texto de forma exhaustiva...")
            splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
            chunks = splitter.split_text(paper_text)
            self.log_execution(f"📄 Texto fragmentado en {len(chunks)} chunks.")
            
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
                n_results=10 # Traemos menos por query para no abrumar, pero mapearemos sobre todos
            )
            
            # Combinar fragmentos relevantes únicos
            relevant_chunks = list(set([doc for doc_list in results['documents'] for doc in doc_list]))
            
            self.log_execution(f"🎯 Contexto filtrado por RAG: {len(relevant_chunks)} chunks únicos recuperados.")
            
            # 3. MAP Phase: Structured Extraction using Flash Lite
            self.log_execution(f"🧠 [Fase MAP] Extrayendo de {len(relevant_chunks)} fragmentos con {MAP_MODEL_NAME}...")
            
            extracted_fragments = []
            
            for idx, chunk in enumerate(relevant_chunks):
                prompt = f"""
                You are a rigorous NeurIPS reviewer. Look at this text fragment and extract hyperparameters.
                TEXT:
                {chunk}
                """
                try:
                    response = self.llm_client.client.models.generate_content(
                        model=MAP_MODEL_NAME,
                        contents=prompt,
                        config={
                            'response_mime_type': 'application/json',
                            'response_schema': Hyperparameters,
                            'temperature': 0.0
                        }
                    )
                    raw_text = response.text.strip()
                    if raw_text.startswith("```"):
                        raw_text = re.sub(r'^```(?:json)?\n?|```$', '', raw_text, flags=re.MULTILINE).strip()
                    extracted_fragments.append(raw_text)
                except Exception as e:
                    self.log_execution(f"⚠️ Error extrayendo fragmento {idx}: {str(e)}", level="warning")
            
            # 4. REDUCE Phase: Consolidate with Gemma 4 31B
            self.log_execution(f"🧠 [Fase REDUCE] Consolidando datos extraídos con {REDUCE_MODEL_NAME}...")
            
            reduce_prompt = f"""
            You are a senior AI researcher reviewing a paper's hyperparameter extraction.
            Below is a list of independent extractions from various parts of the paper (e.g., Pre-training, SFT, RLHF).
            Your job is to consolidate them into a single definitive set of hyperparameters.
            
            RULES:
            - If there are conflicts (e.g. SFT batch size is 256, Pre-training is 1280), prefer the final fine-tuning/SFT parameters if obvious, or pick the most representative one.
            - If an extraction says 'NOT FOUND', ignore it if another extraction found a valid value.
            - If no valid value is found across all fragments for a field, output 'NOT FOUND'.
            - DO NOT guess or hallucinate.
            
            EXTRACTIONS:
            {json.dumps(extracted_fragments, indent=2)}
            """
            
            self.log_execution(f"🚀 [REDUCE] Consolidando datos con {REDUCE_MODEL_NAME} (TPM Ilimitado)...")
            
            reduce_response = self.llm_client.client.models.generate_content(
                model=REDUCE_MODEL_NAME,
                contents=reduce_prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': Hyperparameters,
                    'temperature': 0.0
                }
            )
            
            raw_reduce_text = reduce_response.text.strip()
            # Intento de extraer el bloque JSON limpio si hay texto extra alrededor
            json_match = re.search(r'(\{.*\})', raw_reduce_text, re.DOTALL)
            if json_match:
                raw_reduce_text = json_match.group(1)
            
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
            return {'extracted_hyperparameters_hybrid': cleaned_data}
            
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
