import os
import json
import logging
import requests
import time
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class SotaAnalyzer:
    def __init__(self):
        # Utiliza el mismo modelo que tu auditor
        self.model_name = "models/gemini-3.1-flash-lite-preview"
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("No se encontró la GOOGLE_API_KEY en el .env")
            
        genai.configure(api_key=api_key)
        
        # API Key de Semantic Scholar
        self.s2_api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        
        # Configuración forzando JSON como salida
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.1 # Ligera creatividad para generar queries variadas
            }
        )

    def extract_thematic_coverage(self, paper_text):
        """Identifica subtemas, áreas y año del manuscrito."""
        prompt = f"""
        Analiza este manuscrito científico e identifica:
        1. Los 3-5 subtemas principales que aborda
        2. Las áreas técnicas específicas que cubre
        3. El año de publicación o envío (busca en: encabezado, pie de página, sección de metadata, fecha de envío/aceptación, copyright)
        
        IMPORTANTE para el año:
        - Busca patrones como "2024", "Published: 2023", "Submitted: 2022", "Copyright © 2024"
        - Si encuentras múltiples fechas (envío, revisión, aceptación), usa la más reciente
        - Si no encuentras ninguna fecha clara, devuelve null
        - NO inventes el año, debe estar explícitamente en el texto
        
        Devuelve EXCLUSIVAMENTE un JSON:
        {{
            "subtemas": ["subtema 1", "subtema 2", ...],
            "areas_tecnicas": ["área 1", "área 2", ...],
            "año_paper": 2024
        }}
        
        TEXTO (primeras páginas y últimas páginas donde suelen estar las fechas):
        INICIO:
        {paper_text[:15000]}
        
        FINAL:
        {paper_text[-5000:]}
        """
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            year = result.get("año_paper")
            if year:
                logger.info(f"Año del paper detectado: {year}")
            else:
                logger.warning("No se pudo detectar el año del paper")
            return result
        except Exception as e:
            logger.error(f"Error extrayendo cobertura temática: {str(e)}")
            return {"subtemas": [], "areas_tecnicas": [], "año_paper": None}

    def extract_search_queries(self, paper_text, thematic_data):
        """Paso 1: Extrae queries especializadas en inglés usando LLM (aumentadas a 6)."""
        subtemas_str = ", ".join(thematic_data.get("subtemas", []))
        areas_str = ", ".join(thematic_data.get("areas_tecnicas", []))
        
        prompt = f"""
        Actúa como un investigador senior en Ciencias de la Computación.
        Analiza el siguiente manuscrito científico.
        
        SUBTEMAS IDENTIFICADOS: {subtemas_str}
        ÁREAS TÉCNICAS: {areas_str}
        
        Genera 3 búsquedas especializadas EN INGLÉS para encontrar SOTA reciente:
        - 2 queries generales sobre el tema principal (amplias)
        - 1 query específica sobre el subtema más relevante
        
        IMPORTANTE: Usa términos amplios y comunes, evita ser demasiado específico.
        
        Devuelve EXCLUSIVAMENTE un JSON:
        {{
            "queries": ["query 1", "query 2", "query 3"]
        }}
        
        TEXTO DEL MANUSCRITO:
        {paper_text[:8000]}
        """
        try:
            response = self.model.generate_content(prompt)
            queries = json.loads(response.text).get("queries", [])
            logger.info(f"Queries generadas: {queries}")
            return queries
        except Exception as e:
            logger.error(f"Error generando queries: {str(e)}")
            return []

    def fetch_semantic_scholar(self, queries):
        """Paso 2: Busca en Semantic Scholar literatura 2023-2026 de alto impacto (aumentado a 10 papers)."""
        base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        sota_papers = []
        
        headers = {}
        if self.s2_api_key:
            headers["x-api-key"] = self.s2_api_key
            logger.info("Usando API Key de Semantic Scholar")
        
        for i, q in enumerate(queries):
            if i > 0:
                time.sleep(0.5)
                
            params = {
                "query": q,
                "year": "2023-2026",
                "limit": 5,
                "fields": "paperId,title,authors,year,citationCount,abstract,url"
            }
            
            try:
                logger.info(f"Buscando: {q}")
                response = requests.get(base_url, params=params, headers=headers, timeout=15)
                logger.info(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    logger.info(f"Papers encontrados: {len(data)}")
                    if len(data) == 0:
                        logger.warning(f"Query sin resultados: {q}")
                    sota_papers.extend(data)
                elif response.status_code == 429:
                    logger.warning("Rate limit alcanzado, esperando...")
                    time.sleep(2)
                else:
                    logger.warning(f"Error {response.status_code} para query: {q}")
            except Exception as e:
                logger.error(f"Error en API: {str(e)}")
                
        unique_papers = {p['paperId']: p for p in sota_papers if p.get('paperId')}.values()
        sorted_papers = sorted(unique_papers, key=lambda x: x.get('citationCount', 0), reverse=True)
        
        logger.info(f"Total papers únicos: {len(sorted_papers)}")
        return sorted_papers[:10]

    def analyze_coverage_gaps(self, paper_text, thematic_data):
        """Analiza gaps de cobertura bibliográfica por subtema."""
        subtemas_str = ", ".join(thematic_data.get("subtemas", []))
        
        prompt = f"""
        Analiza la cobertura bibliográfica de este manuscrito.
        
        SUBTEMAS IDENTIFICADOS: {subtemas_str}
        
        TEXTO (inicio y referencias):
        INICIO: {paper_text[:5000]}
        REFERENCIAS: {paper_text[-10000:]}
        
        Identifica qué subtemas tienen POCA o NULA cobertura bibliográfica.
        
        Devuelve JSON:
        {{
            "areas_debiles": [
                {{
                    "subtema": "nombre del subtema",
                    "diagnostico": "por qué tiene baja cobertura"
                }}
            ]
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Error analizando gaps: {str(e)}")
            return {"areas_debiles": []}

    def cross_validate(self, paper_text, sota_papers, thematic_data):
        """Paso 3: Identifica SOLO papers omitidos relevantes con justificación detallada."""
        if not sota_papers:
            return {
                "papers_omitidos": [],
                "cobertura_tematica": {"areas_debiles": []},
                "conclusion_sota": "No se encontraron artículos recientes (2023-2026) en Semantic Scholar."
            }
        
        logger.info(f"Analizando {len(sota_papers)} papers candidatos...")
        for i, p in enumerate(sota_papers[:3]):
            logger.info(f"  [{i+1}] {p['title'][:80]}... ({p['year']}, {p['citationCount']} citas)")
            
        sota_context = "\n\n".join([
            f"[{i+1}] Título: {p['title']}\nAño: {p['year']}\nCitas: {p['citationCount']}\nURL: {p.get('url', 'N/A')}\nAbstract: {(p.get('abstract') or 'No abstract')[:400]}"
            for i, p in enumerate(sota_papers)
        ])
        
        subtemas_str = ", ".join(thematic_data.get("subtemas", []))

        prompt = f"""
        Actúa como Revisor Editorial Experto.
        
        MANUSCRITO ORIGINAL:
        INICIO: {paper_text[:5000]}
        REFERENCIAS: {paper_text[-15000:]}
        
        SUBTEMAS DEL MANUSCRITO: {subtemas_str}
        
        PAPERS SOTA CANDIDATOS (2023-2026):
        {sota_context}
        
        TAREA:
        Identifica papers OMITIDOS (no citados) que sean RELEVANTES para el manuscrito.
        
        CRITERIOS:
        - Descartar si el título es similar al manuscrito (es el propio paper)
        - Descartar si ya está citado en referencias
        - Incluir si aporta valor al tema tratado
        - Justificar por qué debería citarse
        - Indicar qué subtema fortalece
        
        IMPORTANTE: Si encuentras papers relevantes, inclúyelos. No seas demasiado restrictivo.
        Selecciona hasta 5 papers omitidos más relevantes, ordenados por importancia.
        
        Devuelve JSON:
        {{
            "papers_omitidos": [
                {{
                    "titulo": "título exacto",
                    "año": 2024,
                    "citas": 150,
                    "url": "url",
                    "relevancia": "Alta/Media",
                    "subtema_relacionado": "subtema que fortalece",
                    "justificacion": "Por qué es crucial citarlo y dónde encajaría (sección específica)"
                }}
            ],
            "conclusion_sota": "Evaluación de la frescura bibliográfica y cobertura actual"
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            
            logger.info(f"Papers omitidos identificados: {len(result.get('papers_omitidos', []))}")
            
            # Añadir análisis de gaps de cobertura
            coverage_gaps = self.analyze_coverage_gaps(paper_text, thematic_data)
            result["cobertura_tematica"] = coverage_gaps
            
            # Añadir lista de papers analizados para referencia
            result["papers_analizados"] = [
                {
                    "titulo": p['title'],
                    "año": p['year'],
                    "citas": p['citationCount'],
                    "url": p.get('url', 'N/A'),
                    "autores": p.get('authors', [])
                }
                for p in sota_papers[:10]
            ]
            
            return result
        except Exception as e:
            logger.error(f"Error en validación cruzada: {str(e)}")
            return {"error": str(e)}

    def analyze_sota(self, paper_text):
        """Función orquestadora principal con análisis de cobertura temática."""
        logger.info("Iniciando análisis SOTA con cobertura temática...")
        
        # Paso 1: Análisis temático
        thematic_data = self.extract_thematic_coverage(paper_text)
        logger.info(f"Subtemas: {thematic_data.get('subtemas', [])}")
        
        # Paso 2: Generar queries aumentadas
        queries = self.extract_search_queries(paper_text, thematic_data)
        
        if not queries:
            return {"error": "No se pudieron generar queries."}
            
        # Paso 3: Búsqueda ampliada
        papers = self.fetch_semantic_scholar(queries)
        
        # Paso 4: Validación cruzada con análisis de cobertura
        resultado = self.cross_validate(paper_text, papers, thematic_data)
        
        # Metadata
        resultado["metadata"] = {
            "subtemas_identificados": thematic_data.get("subtemas", []),
            "areas_tecnicas": thematic_data.get("areas_tecnicas", []),
            "año_paper_estudiado": thematic_data.get("año_paper"),
            "total_papers_analizados": len(papers),
            "queries_ejecutadas": len(queries)
        }
        
        return resultado
    