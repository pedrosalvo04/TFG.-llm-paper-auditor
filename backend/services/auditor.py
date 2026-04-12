"""Servicio de auditoría de papers"""
import json
import time
from backend.common.llm_client import LLMClient
from backend.common.config import AUDIT_CONFIG
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class PaperAuditor:
    """Auditor de reproducibilidad en papers científicos"""
    
    def __init__(self):
        """Inicializa el auditor con configuración determinista"""
        self.llm_client = LLMClient(generation_config=AUDIT_CONFIG)
        logger.info("✅ Auditor de papers inicializado correctamente")

    def audit(self, paper_text):
        """
        Analiza el texto y registra métricas de rendimiento
        
        Args:
            paper_text: Texto del paper en formato markdown
            
        Returns:
            Diccionario con resultados de la auditoría
        """
        caracteres = len(paper_text)
        logger.info(f"Iniciando auditoría. Tamaño del documento: {caracteres} caracteres")
        
        prompt = f"""
        Actúa como un Auditor Editorial de revistas de alto impacto en Ciencias de la Computación (ACM, IEEE, NeurIPS, ICML, CVPR, etc.).
        Evalúa el manuscrito frente a los estándares de reproducibilidad y transparencia en investigación computacional.
        
        CRITERIOS A EVALUAR:
        1. Estadística y Experimentación: Informar n, métricas de evaluación, tests estadísticos, significancia, intervalos de confianza.
        2. Código y Software: Disponibilidad del código fuente, repositorios (GitHub/GitLab), versiones de librerías, dependencias, instrucciones de ejecución.
        3. Datos y Datasets: Disponibilidad de datasets, preprocesamiento, splits (train/val/test), DOIs, licencias de uso.
        4. Diseño Experimental: Descripción de hiperparámetros, semillas aleatorias, número de ejecuciones, hardware utilizado (GPU/CPU), tiempo de entrenamiento.
        5. Modelos y Arquitecturas: Detalles completos de la arquitectura, pesos preentrenados, checkpoints, configuración del modelo.
        6. Reproducibilidad: Suficientes detalles para replicar los experimentos, scripts de entrenamiento/evaluación, entornos (Docker/Conda).
        7. Comparación con Baselines: Comparación justa con métodos del estado del arte, mismos datasets y métricas.

        INSTRUCCIÓN DE SALIDA:
        Devuelve EXCLUSIVAMENTE un objeto JSON con esta estructura:
        {{
          "revision": [
            {{
              "categoria": "Nombre de la categoría",
              "estado": "🟢 CUMPLE TOTALMENTE / 🔵 CUMPLE MAYORMENTE / 🟡 CUMPLE PARCIALMENTE / 🟠 CUMPLE MÍNIMAMENTE / 🔴 NO CUMPLE / ⚪ N/A",
              "hallazgo": "Breve explicación basada en el texto",
              "recomendacion": "Qué debe añadir el autor"
            }}
          ],
          "veredicto_final": "Resumen general"
        }}

        GUÍA DE ESTADOS:
        - 🟢 CUMPLE TOTALMENTE: Toda la información requerida está presente y es completa
        - 🔵 CUMPLE MAYORMENTE: Información casi completa, solo faltan detalles menores
        - 🟡 CUMPLE PARCIALMENTE: Información presente pero incompleta o ambigua
        - 🟠 CUMPLE MÍNIMAMENTE: Información muy limitada o apenas mencionada
        - 🔴 NO CUMPLE: Información ausente o completamente inadecuada
        - ⚪ N/A: No aplica a este tipo de estudio

        TEXTO DEL ARTÍCULO:
        {paper_text}
        """
        
        start_time = time.time()
        
        try:
            logger.info("Enviando petición a la API de Gemini...")
            response = self.llm_client.generate(prompt)
            
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            
            logger.info(f"✅ Respuesta recibida con éxito en {execution_time} segundos")
            
            # Intentamos extraer métricas de tokens si la API los devuelve
            try:
                tokens_prompt = response.usage_metadata.prompt_token_count
                tokens_resp = response.usage_metadata.candidates_token_count
                logger.info(f"📊 Consumo de Tokens -> Entrada: {tokens_prompt} | Salida: {tokens_resp}")
            except Exception:
                logger.info("📊 Métrica de tokens no disponible en esta llamada")

            # Parsear el JSON devuelto
            resultado_json = json.loads(response.text)
            
            # Inyectamos métricas en el resultado
            resultado_json["metricas"] = {
                "tiempo_segundos": execution_time,
                "caracteres_leidos": caracteres
            }
            
            return resultado_json

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
