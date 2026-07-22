"""Servicio de análisis del Estado del Arte (SOTA) - Refactorizado con Skills"""
from typing import Dict, Any, List
from backend.common.llm_client import LLMClient
from backend.common.config import SOTA_CONFIG
from backend.common.logger import get_logger
from backend.skills.sota_skills import (
    ThematicCoverageSkill,
    QueryGenerationSkill,
    SemanticScholarSearchSkill,
    CrossValidationSkill,
    PaperRankingSkill
)
from backend.skills.clustering_skill import PaperClusteringSkill

logger = get_logger(__name__)


class SotaAnalyzer:
    """
    Analizador del Estado del Arte en papers científicos.

    Pipeline (6 pasos + 2 nuevos):
    1. ThematicCoverageSkill    – identifica subtemas y áreas técnicas
    2. QueryGenerationSkill     – genera queries de búsqueda
    3. SemanticScholarSearchSkill – recupera hasta 20 papers
    3b. PaperClusteringSkill    – clustering semántico + similitud vs usuario
    3c. PaperRankingSkill       – selecciona top-10 por criterio configurable
    4. CrossValidationSkill     – validación cruzada sobre el top-10
    """

    def __init__(self):
        """Inicializa el analizador SOTA con todos los skills necesarios"""
        llm_client = LLMClient(generation_config=SOTA_CONFIG)

        self.thematic_skill = ThematicCoverageSkill(llm_client=llm_client)
        self.query_skill = QueryGenerationSkill(llm_client=llm_client)
        self.search_skill = SemanticScholarSearchSkill()
        self.clustering_skill = PaperClusteringSkill(llm_client=llm_client)
        self.ranking_skill = PaperRankingSkill(llm_client=llm_client)
        self.validation_skill = CrossValidationSkill(llm_client=llm_client)

        logger.info("✅ Analizador SOTA inicializado con skills")


    def analyze_sota(
        self,
        paper_text: str,
        ranking_criterion: str = "citations"
    ) -> Dict[str, Any]:
        """
        Función orquestadora principal del análisis SOTA.

        Args:
            paper_text: Texto completo del paper a analizar.
            ranking_criterion: Criterio para seleccionar el top-10 que se analiza
                en profundidad. Valores válidos:
                - 'citations'  : top-10 por número de citas (default).
                - 'similarity' : top-10 por similitud coseno con el paper del usuario.
                - 'llm'        : top-10 según score de relevancia subjetiva del LLM.

        Returns:
            Diccionario con resultados completos del análisis, incluyendo
            'ranking_criterion' para que la UI pueda mostrarlo.
        """
        logger.info(
            f"🚀 Iniciando análisis SOTA | criterio ranking: '{ranking_criterion}'"
        )

        # Contexto compartido entre skills
        context = {
            'paper_text': paper_text,
            'ranking_criterion': ranking_criterion,
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

        # Paso 3: Buscar papers en Semantic Scholar (hasta 20)
        search_result = self.search_skill.execute(context)
        context.update(search_result)

        # Paso 3b: Clustering semántico (embeddings + KMeans + similitud vs usuario)
        clustering_result = self.clustering_skill.execute(context)
        context.update(clustering_result)

        # Paso 3c: Selección del top-10 según criterio elegido
        ranking_result = self.ranking_skill.execute(context)
        context.update(ranking_result)

        # Paso 4: Validación cruzada — se ejecuta sobre todos para cachear
        validation_result = self.validation_skill.execute(context)
        cached_validation = validation_result.get('validation_results', {})
        context['cached_validation'] = cached_validation
        
        final_results = dict(cached_validation)
        
        # Reordenar y filtrar para devolver los papers en el orden exacto de ranked_papers
        ranked_papers = context.get('ranked_papers', [])
        ordered_data = self._filter_and_order_results(cached_validation, ranked_papers)
        final_results['papers_analizados'] = ordered_data['papers_analizados']
        final_results['papers_omitidos'] = ordered_data['papers_omitidos']

        # Metadata
        thematic_data = context.get('thematic_data', {})
        sota_papers = context.get('sota_papers', [])
        search_queries = context.get('search_queries', [])

        final_results["metadata"] = {
            "subtemas_identificados": thematic_data.get("subtemas", []),
            "areas_tecnicas": thematic_data.get("areas_tecnicas", []),
            "año_paper_estudiado": thematic_data.get("año_paper"),
            "total_papers_recuperados": len(sota_papers),
            "total_papers_analizados": len(ranked_papers),
            "queries_ejecutadas": len(search_queries),
            "ranking_criterion": ranking_criterion,
        }

        # Resultados de clustering
        final_results["clustering"] = {
            "user_similarities": context.get("user_similarities", []),
            "diversity_score": context.get("diversity_score"),
            "cluster_summary": context.get("cluster_summary", {}),
        }

        # Exponer qué criterio se usó (para la UI)
        final_results["ranking_criterion"] = ranking_criterion

        # Guardar el contexto para permitir re-análisis rápidos
        self.last_context = context

        logger.info("✅ Análisis SOTA completado exitosamente")
        return final_results

    def update_ranking_and_reanalyze(self, ranking_criterion: str, target_cluster_id: str | int = "all") -> Dict[str, Any]:
        """
        Re-ejecuta la selección de top-10, análisis de gaps y validación cruzada
        usando los papers previamente descargados y agrupados.
        """
        if getattr(self, 'last_context', None) is None:
            return {"error": "No hay un análisis previo disponible en caché para actualizar."}

        logger.info(f"🔄 Re-analizando SOTA con nuevo criterio de ranking: '{ranking_criterion}' y cluster: '{target_cluster_id}'")

        # Restaurar el contexto anterior y actualizar el criterio
        context = self.last_context.copy()
        context['ranking_criterion'] = ranking_criterion
        context['target_cluster_id'] = target_cluster_id

        # Paso 3c: Nueva selección del top-10
        ranking_result = self.ranking_skill.execute(context)
        context.update(ranking_result)

        # Paso 4: Reutilizar validación cruzada cacheada y reordenar por el nuevo criterio
        cached_validation = context.get('cached_validation', {})
        final_results = dict(cached_validation)
        
        ranked_papers = context.get('ranked_papers', [])
        ordered_data = self._filter_and_order_results(cached_validation, ranked_papers)
        final_results['papers_analizados'] = ordered_data['papers_analizados']
        final_results['papers_omitidos'] = ordered_data['papers_omitidos']

        # Reconstruir Metadata
        thematic_data = context.get('thematic_data', {})
        sota_papers = context.get('sota_papers', [])
        ranked_papers = context.get('ranked_papers', [])
        search_queries = context.get('search_queries', [])

        final_results["metadata"] = {
            "subtemas_identificados": thematic_data.get("subtemas", []),
            "areas_tecnicas": thematic_data.get("areas_tecnicas", []),
            "año_paper_estudiado": thematic_data.get("año_paper"),
            "total_papers_recuperados": len(sota_papers),
            "total_papers_analizados": len(ranked_papers),
            "queries_ejecutadas": len(search_queries),
            "ranking_criterion": ranking_criterion,
            "target_cluster_id": target_cluster_id,
        }

        # Mantener los resultados del clustering original, pero filtrar visualización si es necesario
        user_similarities = context.get("user_similarities", [])
        if target_cluster_id != "all":
            target_cluster_str = str(target_cluster_id)
            # Encontrar los títulos que pertenecen al cluster
            filtered_titles = {
                p.get('title') for p in sota_papers 
                if str(p.get('cluster_id', '')) == target_cluster_str
            }
            user_similarities = [us for us in user_similarities if us.get('title') in filtered_titles]

        final_results["clustering"] = {
            "user_similarities": user_similarities,
            "diversity_score": context.get("diversity_score"),
            "cluster_summary": context.get("cluster_summary", {}),
        }

        final_results["ranking_criterion"] = ranking_criterion
        
        # Actualizar la caché
        self.last_context = context

        logger.info("✅ Re-análisis SOTA completado exitosamente")
        return final_results

    def _filter_and_order_results(
        self,
        cached_validation: Dict[str, Any],
        ranked_papers: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Filtra y reordena 'papers_analizados' y 'papers_omitidos' siguiendo
        estrictamente la secuencia de 'ranked_papers' (según el criterio de ordenación elegido).
        """
        val_analizados = cached_validation.get('papers_analizados', [])
        val_omitidos = cached_validation.get('papers_omitidos', [])

        ordered_analizados = []
        ordered_omitidos = []

        for rp in ranked_papers:
            rp_title = rp.get('title', '').lower().strip()
            if not rp_title:
                continue

            # Buscar en analizados
            found_analizado = False
            for p in val_analizados:
                t = p.get('titulo', '').lower().strip()
                if rp_title in t or t in rp_title:
                    ordered_analizados.append(p)
                    found_analizado = True
                    break

            if not found_analizado:
                ordered_analizados.append({
                    "titulo": rp.get('title'),
                    "año": rp.get('year'),
                    "citas": rp.get('citationCount', 0),
                    "url": rp.get('url', 'N/A'),
                    "autores": rp.get('authors', [])
                })

            # Buscar en omitidos
            for p in val_omitidos:
                t = p.get('titulo', '').lower().strip()
                if rp_title in t or t in rp_title:
                    ordered_omitidos.append(p)
                    break

        return {
            'papers_analizados': ordered_analizados,
            'papers_omitidos': ordered_omitidos
        }
