"""Servicio de análisis del Estado del Arte (SOTA) - Refactorizado con Skills"""
from typing import Dict, Any
from backend.common.llm_client import LLMClient
from backend.common.config import SOTA_CONFIG
from backend.common.logger import get_logger
from backend.skills.sota_skills import (
    ThematicCoverageSkill,
    QueryGenerationSkill,
    SemanticScholarSearchSkill,
    CrossValidationSkill
)
from backend.skills.clustering_skill import PaperClusteringSkill

logger = get_logger(__name__)


class SotaAnalyzer:
    """
    Analizador del Estado del Arte en papers científicos.

    Pipeline:
    1. ThematicCoverageSkill      – identifica subtemas y áreas técnicas
    2. QueryGenerationSkill       – genera queries de búsqueda
    3. SemanticScholarSearchSkill – recupera hasta 20 papers ordenados por citas
    4. PaperClusteringSkill       – clustering semántico + similitud vs usuario
    5. CrossValidationSkill       – validación cruzada sobre los 20 papers
    """

    def __init__(self):
        """Inicializa el analizador SOTA con todos los skills necesarios"""
        llm_client = LLMClient(generation_config=SOTA_CONFIG)

        self.thematic_skill = ThematicCoverageSkill(llm_client=llm_client)
        self.query_skill = QueryGenerationSkill(llm_client=llm_client)
        self.search_skill = SemanticScholarSearchSkill()
        self.clustering_skill = PaperClusteringSkill(llm_client=llm_client)
        self.validation_skill = CrossValidationSkill(llm_client=llm_client)

        logger.info("✅ Analizador SOTA inicializado con skills (ordenado por citas)")


    def analyze_sota(
        self,
        paper_text: str,
        ranking_criterion: str = "citations"
    ) -> Dict[str, Any]:
        """
        Función orquestadora principal del análisis SOTA.
        Recupera y analiza hasta 20 papers candidatos ordenados por citaciones.

        Args:
            paper_text: Texto completo del paper a analizar.
            ranking_criterion: Mantenido por compatibilidad (siempre 'citations').

        Returns:
            Diccionario con resultados completos del análisis.
        """
        logger.info("🚀 Iniciando análisis SOTA (20 papers ordenados por citas)")

        # Contexto compartido entre skills
        context = {
            'paper_text': paper_text,
            'ranking_criterion': 'citations',
        }

        # Paso 1: Análisis temático
        thematic_result = self.thematic_skill.execute(context)
        context.update(thematic_result)

        if not context.get('thematic_data'):
            return {"error": "No se pudo extraer información temática del paper."}

        # Paso 2: Generar queries de búsqueda
        query_result = self.query_skill.execute(context)
        context.update(query_result)

        if not context.get('search_queries'):
            return {"error": "No se pudieron generar queries de búsqueda."}

        # Paso 3: Buscar papers en Semantic Scholar (hasta 20 ordenados por citas)
        search_result = self.search_skill.execute(context)
        context.update(search_result)

        # Paso 4: Clustering semántico (embeddings + KMeans + similitud vs usuario)
        clustering_result = self.clustering_skill.execute(context)
        context.update(clustering_result)

        # Paso 5: Validación cruzada sobre todos los papers recuperados (hasta 20)
        validation_result = self.validation_skill.execute(context)
        final_results = validation_result.get('validation_results', {})

        # Asegurar ordenación estricta por número de citas descendente
        if 'papers_analizados' in final_results and isinstance(final_results['papers_analizados'], list):
            final_results['papers_analizados'].sort(key=lambda p: p.get('citas', 0), reverse=True)

        if 'papers_omitidos' in final_results and isinstance(final_results['papers_omitidos'], list):
            final_results['papers_omitidos'].sort(key=lambda p: p.get('citas', 0), reverse=True)

        # Metadata
        thematic_data = context.get('thematic_data', {})
        sota_papers = context.get('sota_papers', [])
        search_queries = context.get('search_queries', [])

        final_results["metadata"] = {
            "subtemas_identificados": thematic_data.get("subtemas", []),
            "areas_tecnicas": thematic_data.get("areas_tecnicas", []),
            "año_paper_estudiado": thematic_data.get("año_paper"),
            "total_papers_recuperados": len(sota_papers),
            "total_papers_analizados": len(final_results.get('papers_analizados', sota_papers)),
            "queries_ejecutadas": len(search_queries),
            "ranking_criterion": "citations",
        }

        # Resultados de clustering
        final_results["clustering"] = {
            "user_similarities": context.get("user_similarities", []),
            "diversity_score": context.get("diversity_score"),
            "cluster_summary": context.get("cluster_summary", {}),
        }

        final_results["ranking_criterion"] = "citations"

        # Guardar contexto
        self.last_context = context

        logger.info(f"✅ Análisis SOTA completado exitosamente ({len(final_results.get('papers_analizados', []))} papers analizados)")
        return final_results

    def update_ranking_and_reanalyze(self, ranking_criterion: str = "citations", target_cluster_id: str | int = "all") -> Dict[str, Any]:
        """Método de compatibilidad hacia atrás: devuelve el último contexto disponible."""
        if getattr(self, 'last_context', None) is None:
            return {"error": "No hay un análisis previo disponible en caché para actualizar."}
        return self.analyze_sota(self.last_context.get('paper_text', ''), ranking_criterion='citations')

