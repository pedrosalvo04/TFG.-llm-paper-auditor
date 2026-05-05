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

class HybridHyperparameterExtractionSkill(BaseSkill):
    """Extrae hiperparámetros usando un pipeline híbrido (RAG + Pydantic/Gemini + Regex)"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'extracted_hyperparameters_hybrid': {}}
            
        self.log_execution("🔍 Iniciando Hybrid RAG + Structured Extraction de Hyperparametros...", level="notice")
        paper_text = context['paper_text']
        
        try:
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
            
            # Capturar el Top 1 de cada "Agente" (Query)
            top_fragments = {}
            for i, query in enumerate(queries):
                if results['documents'] and len(results['documents']) > i and results['documents'][i]:
                    top_fragments[query] = results['documents'][i][0] # El primer resultado es el más relevante
            
            # Combinar fragmentos relevantes únicos para el contexto final
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
            
            self.log_execution(f"🧠 Consultando a LLM ({RAG_MODEL_NAME}) para extracción estructurada...", level="notice")
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
            
            self.log_execution("✅ Hyperparametros extraídos exitosamente usando pipeline híbrido", level="notice")
            return {
                'extracted_hyperparameters_hybrid': cleaned_data,
                'rag_debug_context': rag_context,
                'rag_top_fragments': top_fragments,
                'final_rag_prompt': prompt
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
