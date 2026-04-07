import os
import google.generativeai as genai
import json
import logging
import time
from dotenv import load_dotenv

# 1. Configuración del sistema de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Cargamos las variables del entorno
load_dotenv()

class PaperAuditor:
    def __init__(self):
        self.model_name = "gemini-3.1-flash-lite-preview"
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("CRÍTICO: No se encontró la GOOGLE_API_KEY en el .env")
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")
            
        genai.configure(api_key=api_key)
        
        # Configuración determinista
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.0,
                "top_k": 1,
                "top_p": 0.1
            }
        )
        logger.info(f"✅ Modelo {self.model_name} inicializado correctamente (temperature=0.0).")

    def audit(self, paper_text):
        """
        Analiza el texto y registra métricas de rendimiento.
        """
        # Log de inicio
        caracteres = len(paper_text)
        logger.info(f"Iniciando auditoría. Tamaño del documento: {caracteres} caracteres.")
        
        prompt = f"""
        Actúa como un Auditor Editorial de Nature Portfolio. 
        Evalúa el manuscrito frente a TODOS los puntos de la 'Reporting Summary'.
        
        CRITERIOS A EVALUAR:
        1. Estadística: Informar n, tests, significancia y si son tests de una o dos colas.
        2. Software y Código: Disponibilidad, versiones y repositorios (GitHub/Zenodo).
        3. Disponibilidad de Datos: Declaración de acceso y DOIs de los datasets.
        4. Diseño Experimental: Tamaño de muestra, exclusión de datos, aleatorización y cegamiento.
        5. Materiales (Si aplica): Validación de anticuerpos, líneas celulares y autenticación.
        6. Ética y Humanos (Si aplica): Consentimiento informado, comité de ética y datos clínicos.
        7. Reproducibilidad: Detalles suficientes de la metodología.

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
        
        start_time = time.time() # ⏱️ Arranca el cronómetro
        
        try:
            logger.info("Enviando petición a la API de Gemini...")
            response = self.model.generate_content(prompt)
            
            end_time = time.time() # ⏱️ Para el cronómetro
            execution_time = round(end_time - start_time, 2)
            
            logger.info(f"✅ Respuesta recibida con éxito en {execution_time} segundos.")
            
            # Intentamos extraer métricas de tokens si la API los devuelve
            try:
                tokens_prompt = response.usage_metadata.prompt_token_count
                tokens_resp = response.usage_metadata.candidates_token_count
                logger.info(f"📊 Consumo de Tokens -> Entrada: {tokens_prompt} | Salida: {tokens_resp}")
            except Exception:
                logger.info("📊 Métrica de tokens no disponible en esta llamada.")

            # Parsear el JSON devuelto
            resultado_json = json.loads(response.text)
            
            # Inyectamos nuestras propias métricas en el resultado para que app.py pueda usarlas
            resultado_json["metricas"] = {
                "tiempo_segundos": execution_time,
                "caracteres_leidos": caracteres
            }
            
            return resultado_json

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}