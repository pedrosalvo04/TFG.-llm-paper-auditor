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


# Chatbot Skills
from backend.skills.chatbot_skills import (
    ConversationalResponseSkill,
    ContextValidationSkill
)

# SOTA Skills
from backend.skills.sota_skills import (
    ThematicCoverageSkill,
    QueryGenerationSkill,
    SemanticScholarSearchSkill,
    CoverageGapAnalysisSkill,
    CrossValidationSkill
)

__all__ = [
    'BaseSkill',
    'InformationExtractionSkill',
    'SectionMappingSkill',
    'NeurIPSComplianceSkill',
    'MetricsCalculationSkill',
    'MetadataAggregationSkill',
    'ConversationalResponseSkill',
    'ContextValidationSkill',
    'ThematicCoverageSkill',
    'QueryGenerationSkill',
    'SemanticScholarSearchSkill',
    'CoverageGapAnalysisSkill',
    'CrossValidationSkill',
]
