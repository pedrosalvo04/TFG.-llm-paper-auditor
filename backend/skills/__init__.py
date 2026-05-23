"""Módulo de skills para agentes IA"""

# Base Skill
from backend.skills.base_skill import BaseSkill

# Auditor Skills
from backend.skills.auditor_skills import (
    InformationExtractionSkill,
    SectionMappingSkill,
    NeurIPSComplianceSkill,
    MetricsCalculationSkill,
    MetadataAggregationSkill
)


# SOTA Skills
from backend.skills.sota_skills import (
    ThematicCoverageSkill,
    QueryGenerationSkill,
    SemanticScholarSearchSkill,
    CoverageGapAnalysisSkill,
    CrossValidationSkill,
    PaperRankingSkill
)

# Clustering Skill
from backend.skills.clustering_skill import PaperClusteringSkill

__all__ = [
    'BaseSkill',
    'InformationExtractionSkill',
    'SectionMappingSkill',
    'NeurIPSComplianceSkill',
    'MetricsCalculationSkill',
    'MetadataAggregationSkill',
    'ThematicCoverageSkill',
    'QueryGenerationSkill',
    'SemanticScholarSearchSkill',
    'CoverageGapAnalysisSkill',
    'CrossValidationSkill',
    'PaperRankingSkill',
    'PaperClusteringSkill',
]
