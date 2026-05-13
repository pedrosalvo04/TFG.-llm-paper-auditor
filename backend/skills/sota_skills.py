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
        )[:20]
        
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
        
        sota_papers = context.get('ranked_papers') or context['sota_papers']
        self.log_execution(
            f"📋 Usando {'ranked' if context.get('ranked_papers') else 'todos los'} papers: {len(sota_papers)}"
        )
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
                for p in sota_papers[:20]
            ]
            
            return {'validation_results': validation_results}
        except Exception as e:
            self.log_execution(f"❌ Error en validación cruzada: {str(e)}", level="error")
            return {'validation_results': {"error": str(e)}}


class PaperRankingSkill(BaseSkill):
    """
    Skill de selección de top-K papers para análisis profundo (CrossValidation).

    Recibe los N papers recuperados (típ. 20) y selecciona los top-10
    según el criterio elegido por el usuario:

    - 'citations'   : Ordena por número de citas desc (determinista, sin LLM).
    - 'similarity'  : Ordena por similitud coseno con el paper del usuario
                      (requiere que PaperClusteringSkill ya haya corrido).
    - 'llm'         : Pide al LLM que puntúe la relevancia subjetiva de
                      cada paper y selecciona los 10 mejor valorados.
    """

    TOP_K = 10

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        sota_papers = context.get('sota_papers', [])
        if not sota_papers:
            return {'ranked_papers': []}

        target_cluster = context.get('target_cluster_id', 'all')
        if target_cluster != 'all':
            filtered_papers = [p for p in sota_papers if str(p.get('cluster_id', '')) == str(target_cluster)]
            if filtered_papers:
                sota_papers = filtered_papers
                self.log_execution(f"🔍 Filtrando a {len(sota_papers)} papers del cluster '{target_cluster}'")
            else:
                self.log_execution(f"⚠️ Ningún paper en el cluster '{target_cluster}', usando todos", level="warning")

        criterion = context.get('ranking_criterion', 'citations')
        self.log_execution(f"🎯 Seleccionando top-{self.TOP_K} papers por criterio: '{criterion}'")

        if criterion == 'citations':
            ranked = self._rank_by_citations(sota_papers)
        elif criterion == 'similarity':
            ranked = self._rank_by_similarity(sota_papers)
        elif criterion == 'llm':
            ranked = self._rank_by_llm(sota_papers, context)
        else:
            self.log_execution(f"⚠️ Criterio desconocido '{criterion}', usando citations", level="warning")
            ranked = self._rank_by_citations(sota_papers)

        self.log_execution(f"✅ Top-{len(ranked)} papers seleccionados para análisis profundo")
        return {'ranked_papers': ranked}

    # ------------------------------------------------------------------
    def _rank_by_citations(self, papers: List[Dict]) -> List[Dict]:
        """Ordena por número de citas desc y devuelve top-K."""
        return sorted(papers, key=lambda p: p.get('citationCount', 0), reverse=True)[: self.TOP_K]

    def _rank_by_similarity(self, papers: List[Dict]) -> List[Dict]:
        """Ordena por user_similarity desc (campo añadido por PaperClusteringSkill)."""
        if not any('user_similarity' in p for p in papers):
            self.log_execution(
                "⚠️ 'user_similarity' no disponible, usando citations como fallback",
                level="warning"
            )
            return self._rank_by_citations(papers)
        return sorted(papers, key=lambda p: p.get('user_similarity', 0.0), reverse=True)[: self.TOP_K]

    def _rank_by_llm(self, papers: List[Dict], context: Dict[str, Any]) -> List[Dict]:
        """Pide al LLM que puntúe la relevancia (0-10) de cada paper y devuelve el top-K."""
        if not self.llm_client:
            self.log_execution("⚠️ Sin LLM, usando citations como fallback", level="warning")
            return self._rank_by_citations(papers)

        paper_text = context.get('paper_text', '')[:3000]
        thematic_data = context.get('thematic_data', {})
        subtemas_str = ", ".join(thematic_data.get('subtemas', []))

        candidates_text = "\n".join([
            f"[{i+1}] {p['title']} ({p['year']}, {p.get('citationCount', 0)} citas)\n"
            f"Abstract: {(p.get('abstract') or '')[:300]}"
            for i, p in enumerate(papers)
        ])

        prompt = (
            f"You are an expert peer reviewer.\n\n"
            f"PAPER BEING ANALYSED (excerpt):\n{paper_text}\n\n"
            f"SUBTOPICS: {subtemas_str}\n\n"
            f"CANDIDATE SOTA PAPERS:\n{candidates_text}\n\n"
            f"TASK: For each candidate paper, assign a relevance score from 0 to 10 "
            f"indicating how important it is for the author to be aware of and potentially "
            f"cite it. Consider topical overlap, methodological similarity, and novelty.\n"
            f"Return ONLY a valid JSON array (no markdown, no explanation): "
            f'[{{"index": 1, "score": 8.5}}, {{"index": 2, "score": 3.0}}, ...]'
        )

        try:
            response = self.llm_client.generate(prompt)
            scores_raw = self.parse_json_response(response.text)

            if isinstance(scores_raw, dict):
                scores_raw = list(scores_raw.values())

            score_map = {}
            for item in scores_raw:
                if isinstance(item, dict):
                    idx = int(item.get('index', -1)) - 1  # 1-based → 0-based
                    scr = float(item.get('score', 0.0))
                    if 0 <= idx < len(papers):
                        score_map[idx] = scr

            scored = []
            for i, p in enumerate(papers):
                p_copy = dict(p)
                p_copy['llm_relevance_score'] = score_map.get(i, 0.0)
                scored.append(p_copy)

            ranked = sorted(scored, key=lambda p: p['llm_relevance_score'], reverse=True)
            self.log_execution(
                f"✅ Scores LLM para {len(score_map)}/{len(papers)} papers"
            )
            return ranked[: self.TOP_K]

        except Exception as e:
            self.log_execution(f"❌ Error en scoring LLM: {e} — usando citations", level="error")
            return self._rank_by_citations(papers)

