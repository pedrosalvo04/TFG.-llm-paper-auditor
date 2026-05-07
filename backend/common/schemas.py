"""
Schemas Pydantic para Structured Outputs del pipeline de auditoría.

Cada clase define el contrato exacto de respuesta JSON que se le pide al LLM
mediante `response_schema` en la `generation_config` de Gemini.

Ventajas frente al parsing manual con regex:
  - Elimina json.loads() + re.sub() + el loop de stack de llaves.
  - La garantía de validez JSON la asume el proveedor del modelo.
  - Errores de schema se detectan antes de llegar a la lógica de negocio.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Schema para la fase MAP (extracción por fragmento)
# ---------------------------------------------------------------------------

class MapFragmentResult(BaseModel):
    """
    Resultado de la extracción de UN fragmento del paper (fase MAP).
    Usado en InformationExtractionSkill y HybridHyperparameterExtractionSkill.
    """
    thought_process: str = Field(
        description="Internal reasoning about the technical details found in this fragment."
    )
    paper_title: str = Field(default="NOT FOUND")
    authors: List[str] = Field(default_factory=list)
    context_mapping: List[str] = Field(
        default_factory=list,
        description="List of sections identified in this fragment (e.g. Abstract, Experiments, Appendix)."
    )
    code: Dict[str, Any] = Field(default_factory=dict)
    data: Dict[str, Any] = Field(default_factory=dict)
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    hardware: Dict[str, Any] = Field(default_factory=dict)
    statistics: Dict[str, Any] = Field(default_factory=dict)
    architecture: Dict[str, Any] = Field(default_factory=dict)
    baseline_comparison: Dict[str, Any] = Field(default_factory=dict)
    software_versions: Dict[str, Any] = Field(default_factory=dict)
    limitations_quality: Dict[str, Any] = Field(default_factory=dict)
    problematic_phrases: List[str] = Field(default_factory=list)
    theory_and_proofs: Dict[str, Any] = Field(default_factory=dict)
    broader_impacts_extraction: Dict[str, Any] = Field(default_factory=dict)
    llm_usage_extraction: Dict[str, Any] = Field(default_factory=dict)
    human_subjects_extraction: Dict[str, Any] = Field(default_factory=dict)
    licenses_extraction: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Schema para la fase REDUCE (consolidación)
# ---------------------------------------------------------------------------

class ReduceExtractionResult(BaseModel):
    """
    Resultado consolidado de todos los fragmentos MAP.
    Usado en InformationExtractionSkill (fase REDUCE).
    """
    thought_process: str = Field(
        description="Final synthesis of the paper's technical rigor and reproducibility."
    )
    paper_type: str = Field(
        default="ML/AI",
        description="'ML/AI' or 'INVALID - Not ML/AI'."
    )
    invalid_reason: str = Field(default="")
    paper_title: str = Field(default="NOT FOUND")
    authors: List[str] = Field(default_factory=list)
    context_mapping: List[str] = Field(default_factory=list)
    code: Dict[str, Any] = Field(default_factory=dict)
    data: Dict[str, Any] = Field(default_factory=dict)
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    hardware: Dict[str, Any] = Field(default_factory=dict)
    statistics: Dict[str, Any] = Field(default_factory=dict)
    architecture: Dict[str, Any] = Field(default_factory=dict)
    baseline_comparison: Dict[str, Any] = Field(default_factory=dict)
    software_versions: Dict[str, Any] = Field(default_factory=dict)
    limitations_quality: Dict[str, Any] = Field(default_factory=dict)
    problematic_phrases: List[str] = Field(default_factory=list)
    theory_and_proofs: Dict[str, Any] = Field(default_factory=dict)
    broader_impacts_extraction: Dict[str, Any] = Field(default_factory=dict)
    llm_usage_extraction: Dict[str, Any] = Field(default_factory=dict)
    human_subjects_extraction: Dict[str, Any] = Field(default_factory=dict)
    licenses_extraction: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Schema para la evaluación NeurIPS
# ---------------------------------------------------------------------------

class ChecklistItemSchema(BaseModel):
    answer: str = Field(description="Exactly one of: 'Yes', 'No', or 'N/A'.")
    evidence: str = Field(default="", description="Verbatim quote and section if answer is Yes.")
    justification: str = Field(default="", description="Technical explanation of the answer.")
    is_no_justified: bool = Field(default=False)


class EvaluationResultSchema(BaseModel):
    """
    Resultado completo de la evaluación NeurIPS 2026.
    Usado en ReproducibilityEvaluationSkill.
    """
    claims: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    limitations: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    theory_assumptions_proofs: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    experimental_result_reproducibility: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    open_access_data_code: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    experimental_setting_details: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    experiment_statistical_significance: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    experiments_compute_resource: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    code_of_ethics: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    broader_impacts: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    safeguards: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    licenses: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    assets: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    crowdsourcing_human_subjects: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    irb_approvals: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)
    declaration_llm_usage: ChecklistItemSchema = Field(default_factory=ChecklistItemSchema)


# ---------------------------------------------------------------------------
# Schema para la verificación del Auditor 2 (Self-Correction)
# ---------------------------------------------------------------------------

class VerificationResultSchema(BaseModel):
    """
    Resultado de verificar UN ítem del checklist.
    Usado en ChecklistVerificationSkill.
    """
    answer: str = Field(description="Exactly one of: 'Yes', 'No', or 'N/A'.")
    evidence: str = Field(default="", description="Detailed verbatim quote and section.")
    justification: str = Field(
        default="",
        description="Technical explanation of why the answer is correct or why it was corrected."
    )
    is_no_justified: bool = Field(default=False)
    was_corrected: bool = Field(
        default=False,
        description="True if the answer changed from the initial evaluation."
    )


# ---------------------------------------------------------------------------
# Schema para la extracción RAG de hiperparámetros
# ---------------------------------------------------------------------------

class RAGFragmentResult(BaseModel):
    """
    Resultado de la extracción de UN chunk del RAG (fase MAP del pipeline híbrido).
    Usado en HybridHyperparameterExtractionSkill.
    """
    thought_process: str = Field(
        description="Internal reasoning about the technical details found, comparing reported values."
    )
    learning_rate: str = Field(default="NOT FOUND")
    batch_size: str = Field(default="NOT FOUND")
    epochs: str = Field(default="NOT FOUND")
    optimizer: str = Field(default="NOT FOUND")
    warmup_steps: str = Field(default="NOT FOUND")
    weight_decay: str = Field(default="NOT FOUND")
    random_seed: str = Field(default="NOT FOUND")
    betas: str = Field(default="NOT FOUND")
    epsilon: str = Field(default="NOT FOUND")
    training_steps: str = Field(default="NOT FOUND")
    total_tokens: str = Field(default="NOT FOUND")
    hardware: str = Field(default="NOT FOUND")
    latency_metrics: str = Field(default="NOT FOUND")


class RAGReduceResult(BaseModel):
    """
    Resultado consolidado del pipeline RAG (fase REDUCE).
    Coincide con el modelo Hyperparameters legacy para compatibilidad.
    """
    thought_process: str = Field(
        description="Final synthesis of hyperparameter extraction across all paper fragments."
    )
    learning_rate: str = Field(default="NOT FOUND")
    batch_size: str = Field(default="NOT FOUND")
    epochs: str = Field(default="NOT FOUND")
    optimizer: str = Field(default="NOT FOUND")
    warmup_steps: str = Field(default="NOT FOUND")
    weight_decay: str = Field(default="NOT FOUND")
    random_seed: str = Field(default="NOT FOUND")
    betas: str = Field(default="NOT FOUND")
    epsilon: str = Field(default="NOT FOUND")
    training_steps: str = Field(default="NOT FOUND")
    total_tokens: str = Field(default="NOT FOUND")
    hardware: str = Field(default="NOT FOUND")
    latency_metrics: str = Field(default="NOT FOUND")
