"""Servicio de análisis del Estado del Arte (SOTA) - Refactorizado con Skills"""
from typing import Dict, Any
from backend.common.llm_client import LLMClient
from backend.common.config import SOTA_CONFIG
from backend.utils.logger import get_logger
from backend.skills.sota_skills import (
    ThematicCoverageSkill,
    QueryGenerationSkill,
    SemanticScholarSearchSkill,
    CoverageGapAnalysisSkill,
    CrossValidationSkill
)

logger = get_logger(__name__)


class SotaAnalyzer:
    """
    Analizador del Estado del Arte en papers científicos.
    
    Utiliza un conjunto de skills especializados para:
    - Identificar subtemas y cobertura temática
    - Generar queries de búsqueda
    - Buscar papers en Semantic Scholar
    - Analizar gaps de cobertura
    - Validar y detectar omisiones bibliográficas
    """
    
    def __init__(self):
        """Inicializa el analizador SOTA con todos los skills necesarios"""
        llm_client = LLMClient(generation_config=SOTA_CONFIG)
        
        # Inicializar skills
        self.thematic_skill = ThematicCoverageSkill(llm_client=llm_client)
        self.query_skill = QueryGenerationSkill(llm_client=llm_client)
        self.search_skill = SemanticScholarSearchSkill()
        self.gap_skill = CoverageGapAnalysisSkill(llm_client=llm_client)
        self.validation_skill = CrossValidationSkill(llm_client=llm_client)
        
        logger.info("✅ Analizador SOTA inicializado con skills")


    def analyze_sota(self, paper_text: str) -> Dict[str, Any]:
        """
        Función orquestadora principal del análisis SOTA.
        
        Ejecuta secuencialmente todos los skills necesarios para el análisis
        completo del estado del arte.
        
        Args:
            paper_text: Texto completo del paper a analizar.
        
        Returns:
            Diccionario con resultados completos del análisis.
        """
        logger.info("🚀 Iniciando análisis SOTA con arquitectura basada en skills...")
        
        # Contexto compartido entre skills
        context = {'paper_text': paper_text}
        
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
        
        # Paso 3: Buscar papers en Semantic Scholar
        search_result = self.search_skill.execute(context)
        context.update(search_result)
        
        # Paso 4: Analizar gaps de cobertura
        gap_result = self.gap_skill.execute(context)
        context.update(gap_result)
        
        # Paso 5: Validación cruzada
        validation_result = self.validation_skill.execute(context)
        final_results = validation_result.get('validation_results', {})
        
        # Añadir metadata
        thematic_data = context.get('thematic_data', {})
        sota_papers = context.get('sota_papers', [])
        search_queries = context.get('search_queries', [])
        
        final_results["metadata"] = {
            "subtemas_identificados": thematic_data.get("subtemas", []),
            "areas_tecnicas": thematic_data.get("areas_tecnicas", []),
            "año_paper_estudiado": thematic_data.get("año_paper"),
            "total_papers_analizados": len(sota_papers),
            "queries_ejecutadas": len(search_queries)
        }
        
        logger.info("✅ Análisis SOTA completado exitosamente")
        return final_results
