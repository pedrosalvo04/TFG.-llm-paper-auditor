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
from backend.common.prompt_engine import (
    get_thematic_coverage_prompt,
    get_query_generation_prompt,
    get_coverage_gap_prompt,
    get_cross_validation_prompt
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
        
        prompt = get_thematic_coverage_prompt(paper_text)
        
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
        
        prompt = get_query_generation_prompt(subtemas_str, areas_str, paper_text)
        
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
                "limit": SEMANTIC_SCHOLAR_LIMIT,
                "fields": SEMANTIC_SCHOLAR_FIELDS
            }
            
            if SEMANTIC_SCHOLAR_YEAR_RANGE:
                params["year"] = SEMANTIC_SCHOLAR_YEAR_RANGE
            
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
        )[:30]
        
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
        
        prompt = get_coverage_gap_prompt(paper_text, subtemas_str)
        
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
        
        prompt = get_cross_validation_prompt(paper_text, sota_context, subtemas_str)
        
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
                for p in sota_papers[:30]
            ]
            
            return {'validation_results': validation_results}
        except Exception as e:
            self.log_execution(f"❌ Error en validación cruzada: {str(e)}", level="error")
            return {'validation_results': {"error": str(e)}}
