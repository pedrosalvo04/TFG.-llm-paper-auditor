"""Módulo de skills para agentes IA"""

# Base Skill
from backend.skills.base_skill import BaseSkill

# Auditor Skills
from backend.skills.auditor_skills import (
    InformationExtractionSkill,
    ReproducibilityEvaluationSkill,
    MetricsCalculationSkill,
    MetadataAggregationSkill,
    ChecklistVerificationSkill
)

# RAG Skills
from backend.skills.rag_extraction_skill import (
    HybridHyperparameterExtractionSkill,
    Hyperparameters
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

# Regex Detection Skills
from backend.skills.regex_detection_skills import (
    LimitationsQualityDetectionSkill,
    SoftwareVersionDetectionSkill,
    HardwareDetailDetectionSkill,
    HyperparameterDetectionSkill,
    DataAvailabilityDetectionSkill,
    CodeAvailabilityDetectionSkill,
    StatisticsDetectionSkill,
    EnvironmentalImpactDetectionSkill,
    ProblematicPhrasesDetectionSkill,
    LlmUsageDetectionSkill,
    CrowdsourcingDetectionSkill,
    LicenseDetectionSkill
)

__all__ = [
    'BaseSkill',
    'InformationExtractionSkill',
    'ReproducibilityEvaluationSkill',
    'MetricsCalculationSkill',
    'MetadataAggregationSkill',
    'ChecklistVerificationSkill',
    'HybridHyperparameterExtractionSkill',
    'Hyperparameters',
    'ConversationalResponseSkill',
    'ContextValidationSkill',
    'ThematicCoverageSkill',
    'QueryGenerationSkill',
    'SemanticScholarSearchSkill',
    'CoverageGapAnalysisSkill',
    'CrossValidationSkill',
    'LimitationsQualityDetectionSkill',
    'SoftwareVersionDetectionSkill',
    'HardwareDetailDetectionSkill',
    'HyperparameterDetectionSkill',
    'DataAvailabilityDetectionSkill',
    'CodeAvailabilityDetectionSkill',
    'StatisticsDetectionSkill',
    'EnvironmentalImpactDetectionSkill',
    'ProblematicPhrasesDetectionSkill',
    'LlmUsageDetectionSkill',
    'CrowdsourcingDetectionSkill',
    'LicenseDetectionSkill',
]
