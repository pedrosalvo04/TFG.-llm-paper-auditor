"""Skills específicos para análisis del Estado del Arte (SOTA)"""
import json
import time
import requests
from typing import Any, Dict, List
from backend.skills.base_skill import BaseSkill
from backend.common.config import (
    SEMANTIC_SCHOLAR_API_KEY,
    SEMANTIC_SCHOLAR_BASE_URL,
    SEMANTIC_SCHOLAR_YEAR_RANGE,
    SEMANTIC_SCHOLAR_LIMIT,
    SEMANTIC_SCHOLAR_FIELDS
)


class ThematicCoverageSkill(BaseSkill):
    """
    Skill para identificar subtemas, áreas técnicas y año del paper.
    
    Analiza el contenido del manuscrito para extraer información temática
    relevante que guiará la búsqueda del estado del arte.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrae cobertura temática del paper.
        
        Args:
            context: Debe contener 'paper_text'.
        
        Returns:
            Diccionario con 'thematic_data' (subtemas, areas_tecnicas, año_paper).
        """
        if not self.validate_context(context, ['paper_text']):
            return {'thematic_data': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'thematic_data': {}}
        
        self.log_execution("🔍 Identificando subtemas y cobertura temática...")
        
        paper_text = context['paper_text']
        
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
            response = self.llm_client.generate(prompt)
            thematic_data = self.parse_json_response(response.text)
            
            year = thematic_data.get("año_paper")
            if year:
                self.log_execution(f"✅ Año detectado: {year}")
            else:
                self.log_execution("⚠️ No se pudo detectar el año", level="warning")
            
            self.log_execution(f"Subtemas: {thematic_data.get('subtemas', [])}")
            return {'thematic_data': thematic_data}
        except Exception as e:
            self.log_execution(f"❌ Error extrayendo cobertura temática: {str(e)}", level="error")
            return {'thematic_data': {"subtemas": [], "areas_tecnicas": [], "año_paper": None}}


class QueryGenerationSkill(BaseSkill):
    """
    Skill para generar queries de búsqueda especializadas.
    
    Crea búsquedas en inglés optimizadas para encontrar literatura
    reciente relacionada con el paper analizado.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera queries de búsqueda.
        
        Args:
            context: Debe contener 'paper_text' y 'thematic_data'.
        
        Returns:
            Diccionario con 'search_queries'.
        """
        if not self.validate_context(context, ['paper_text', 'thematic_data']):
            return {'search_queries': []}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'search_queries': []}
        
        self.log_execution("🔎 Generando queries de búsqueda...")
        
        paper_text = context['paper_text']
        thematic_data = context['thematic_data']
        
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
            response = self.llm_client.generate(prompt)
            queries = self.parse_json_response(response.text).get("queries", [])
            self.log_execution(f"✅ Queries generadas: {queries}")
            return {'search_queries': queries}
        except Exception as e:
            self.log_execution(f"❌ Error generando queries: {str(e)}", level="error")
            return {'search_queries': []}


class SemanticScholarSearchSkill(BaseSkill):
    """
    Skill para buscar papers en Semantic Scholar.
    
    Realiza búsquedas en la API de Semantic Scholar filtrando por
    año y ordenando por impacto (citaciones).
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Busca papers en Semantic Scholar.
        
        Args:
            context: Debe contener 'search_queries'.
        
        Returns:
            Diccionario con 'sota_papers'.
        """
        if not self.validate_context(context, ['search_queries']):
            return {'sota_papers': []}
        
        queries = context['search_queries']
        if not queries:
            self.log_execution("No hay queries para buscar", level="warning")
            return {'sota_papers': []}
        
        self.log_execution(f"🌐 Buscando en Semantic Scholar ({len(queries)} queries)...")
        
        headers = {}
        if SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY
            self.log_execution("Usando API Key de Semantic Scholar")
        
        sota_papers = []
        
        for i, q in enumerate(queries):
            if i > 0:
                time.sleep(0.5)
                
            params = {
                "query": q,
                "year": SEMANTIC_SCHOLAR_YEAR_RANGE,
                "limit": SEMANTIC_SCHOLAR_LIMIT,
                "fields": SEMANTIC_SCHOLAR_FIELDS
            }
            
            try:
                self.log_execution(f"Buscando: {q}")
                response = requests.get(
                    SEMANTIC_SCHOLAR_BASE_URL, 
                    params=params, 
                    headers=headers, 
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    self.log_execution(f"Encontrados: {len(data)} papers")
                    if len(data) == 0:
                        self.log_execution(f"⚠️ Query sin resultados: {q}", level="warning")
                    sota_papers.extend(data)
                elif response.status_code == 429:
                    self.log_execution("⚠️ Rate limit alcanzado, esperando...", level="warning")
                    time.sleep(2)
                else:
                    self.log_execution(
                        f"⚠️ Error {response.status_code} para query: {q}", 
                        level="warning"
                    )
            except Exception as e:
                self.log_execution(f"❌ Error en API: {str(e)}", level="error")
        
        # Eliminar duplicados y ordenar por citaciones
        unique_papers = {p['paperId']: p for p in sota_papers if p.get('paperId')}.values()
        sorted_papers = sorted(
            unique_papers, 
            key=lambda x: x.get('citationCount', 0), 
            reverse=True
        )[:10]
        
        self.log_execution(f"✅ Total papers únicos: {len(sorted_papers)}")
        return {'sota_papers': sorted_papers}


class CoverageGapAnalysisSkill(BaseSkill):
    """
    Skill para analizar gaps de cobertura bibliográfica.
    
    Identifica qué subtemas tienen poca o nula cobertura en las
    referencias del paper analizado.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza gaps de cobertura.
        
        Args:
            context: Debe contener 'paper_text' y 'thematic_data'.
        
        Returns:
            Diccionario con 'coverage_gaps'.
        """
        if not self.validate_context(context, ['paper_text', 'thematic_data']):
            return {'coverage_gaps': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'coverage_gaps': {}}
        
        self.log_execution("📉 Analizando gaps de cobertura bibliográfica...")
        
        paper_text = context['paper_text']
        thematic_data = context['thematic_data']
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
            response = self.llm_client.generate(prompt)
            coverage_gaps = self.parse_json_response(response.text)
            self.log_execution(f"✅ Gaps identificados: {len(coverage_gaps.get('areas_debiles', []))}")
            return {'coverage_gaps': coverage_gaps}
        except Exception as e:
            self.log_execution(f"❌ Error analizando gaps: {str(e)}", level="error")
            return {'coverage_gaps': {"areas_debiles": []}}


class CrossValidationSkill(BaseSkill):
    """
    Skill para validación cruzada y detección de omisiones.
    
    Identifica papers relevantes del SOTA que no fueron citados
    en el manuscrito analizado.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza validación cruzada.
        
        Args:
            context: Debe contener 'paper_text', 'sota_papers', 'thematic_data', 'coverage_gaps'.
        
        Returns:
            Diccionario con 'validation_results'.
        """
        required_keys = ['paper_text', 'sota_papers', 'thematic_data']
        if not self.validate_context(context, required_keys):
            return {'validation_results': {}}
        
        sota_papers = context['sota_papers']
        if not sota_papers:
            return {
                'validation_results': {
                    "papers_omitidos": [],
                    "cobertura_tematica": {"areas_debiles": []},
                    "conclusion_sota": "No se encontraron artículos recientes (2023-2026) en Semantic Scholar."
                }
            }
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'validation_results': {}}
        
        self.log_execution(f"🔬 Validando {len(sota_papers)} papers candidatos...")
        
        paper_text = context['paper_text']
        thematic_data = context['thematic_data']
        coverage_gaps = context.get('coverage_gaps', {"areas_debiles": []})
        
        # Mostrar los primeros papers para debugging
        for i, p in enumerate(sota_papers[:3]):
            self.log_execution(
                f"  [{i+1}] {p['title'][:80]}... ({p['year']}, {p['citationCount']} citas)"
            )
        
        sota_context = "\n\n".join([
            f"[{i+1}] Título: {p['title']}\nAño: {p['year']}\nCitas: {p['citationCount']}\n"
            f"URL: {p.get('url', 'N/A')}\nAbstract: {(p.get('abstract') or 'No abstract')[:400]}"
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
            response = self.llm_client.generate(prompt)
            validation_results = self.parse_json_response(response.text)
            
            self.log_execution(
                f"✅ Papers omitidos identificados: {len(validation_results.get('papers_omitidos', []))}"
            )
            
            # Añadir análisis de gaps de cobertura
            validation_results["cobertura_tematica"] = coverage_gaps
            
            # Añadir lista de papers analizados para referencia
            validation_results["papers_analizados"] = [
                {
                    "titulo": p['title'],
                    "año": p['year'],
                    "citas": p['citationCount'],
                    "url": p.get('url', 'N/A'),
                    "autores": p.get('authors', [])
                }
                for p in sota_papers[:10]
            ]
            
            return {'validation_results': validation_results}
        except Exception as e:
            self.log_execution(f"❌ Error en validación cruzada: {str(e)}", level="error")
            return {'validation_results': {"error": str(e)}}
