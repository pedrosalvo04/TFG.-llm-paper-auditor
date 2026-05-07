"""
Estado global tipado de la auditoría (AuditState).

Reemplaza el diccionario `context: Dict[str, Any]` no tipado que se pasaba
entre skills. Usar Pydantic garantiza:
  - Autocompletado en el IDE.
  - Validación de tipos en tiempo de ejecución.
  - Eliminación de KeyError silenciosos.
  - Documentación inline del contrato de datos.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Sub-modelos de información extraída
# ---------------------------------------------------------------------------

class CodeInfo(BaseModel):
    repository_url: str = "NOT FOUND"
    negative_phrase: str = "NOT FOUND"
    dependencies: str = "NOT FOUND"
    instructions: str = "no"
    release_mention: str = "NOT FOUND"


class DataInfo(BaseModel):
    dataset_name: str = "NOT FOUND"
    access_url: str = "NOT FOUND"
    negative_phrase: str = "NOT FOUND"
    preprocessing: str = "NOT FOUND"
    splits: str = "NOT FOUND"
    release_mention: str = "NOT FOUND"


class HyperparametersInfo(BaseModel):
    optimizer: str = "NOT FOUND"
    learning_rate: str = "NOT FOUND"
    batch_size: str = "NOT FOUND"
    epochs: str = "NOT FOUND"
    training_steps: str = "NOT FOUND"
    total_tokens: str = "NOT FOUND"
    warmup: str = "NOT FOUND"
    weight_decay: str = "NOT FOUND"
    betas: str = "NOT FOUND"
    epsilon: str = "NOT FOUND"
    vague_phrase: str = "NOT FOUND"
    table_reference: str = "NOT FOUND"


class HardwareInfo(BaseModel):
    gpu_cpu: str = "NOT FOUND"
    num_gpus: str = "NOT FOUND"
    memory: str = "NOT FOUND"
    time: str = "NOT FOUND"
    carbon_footprint: str = "NOT FOUND"
    energy_consumption: str = "NOT FOUND"
    pue: str = "NOT FOUND"
    throughput: str = "NOT FOUND"
    latency_metrics: str = "NOT FOUND"


class StatisticsInfo(BaseModel):
    confidence_intervals: str = "no"
    significance_tests: str = "no"
    num_runs: str = "NOT FOUND"


class ArchitectureInfo(BaseModel):
    description: str = "NOT FOUND"
    weights_available: str = "no"
    release_mention: str = "NOT FOUND"


class BaselineComparisonInfo(BaseModel):
    compared_models: List[str] = Field(default_factory=list)
    has_comparative_tables: str = "no"
    same_metrics: str = "no"
    results_section: str = "NOT FOUND"


class SoftwareVersionsInfo(BaseModel):
    framework: str = "NOT FOUND"
    python_version: str = "NOT FOUND"
    cuda_version: str = "NOT FOUND"
    dependency_file: str = "no"


class LimitationsInfo(BaseModel):
    has_section: str = "no"
    specific_points: List[str] = Field(default_factory=list)
    quantified_issues: str = "no"


class TheoryAndProofsInfo(BaseModel):
    has_theoretical_results: str = "not found"
    assumptions_stated: str = "NOT FOUND"
    proofs_included: str = "not found"
    appendix_reference: str = "NOT FOUND"


class BroaderImpactsInfo(BaseModel):
    has_impact_statement: str = "not found"
    appendix_reference: str = "NOT FOUND"
    concerns_discussed: List[str] = Field(default_factory=list)


class LLMUsageInfo(BaseModel):
    models_used_in_methodology: List[str] = Field(default_factory=list)
    purpose_in_methodology: str = "NOT FOUND"
    used_for_writing: str = "not mentioned"
    writing_declaration_quote: str = "NOT FOUND"


class HumanSubjectsInfo(BaseModel):
    uses_human_annotation: str = "no"
    compensation_details: str = "NOT FOUND"
    instructions_provided: str = "no"


class LicensesInfo(BaseModel):
    assets_used: List[str] = Field(default_factory=list)
    licenses_named: List[str] = Field(default_factory=list)
    missing_licenses_for_some_assets: str = "no"


# ---------------------------------------------------------------------------
# Modelo de información extraída completo
# ---------------------------------------------------------------------------

class ExtractedInfo(BaseModel):
    thought_process: str = ""
    paper_type: str = "ML/AI"
    invalid_reason: str = ""
    paper_title: str = "NOT FOUND"
    authors: List[str] = Field(default_factory=list)
    context_mapping: List[str] = Field(default_factory=list)
    code: CodeInfo = Field(default_factory=CodeInfo)
    data: DataInfo = Field(default_factory=DataInfo)
    hyperparameters: HyperparametersInfo = Field(default_factory=HyperparametersInfo)
    hardware: HardwareInfo = Field(default_factory=HardwareInfo)
    statistics: StatisticsInfo = Field(default_factory=StatisticsInfo)
    architecture: ArchitectureInfo = Field(default_factory=ArchitectureInfo)
    baseline_comparison: BaselineComparisonInfo = Field(default_factory=BaselineComparisonInfo)
    software_versions: SoftwareVersionsInfo = Field(default_factory=SoftwareVersionsInfo)
    limitations_quality: LimitationsInfo = Field(default_factory=LimitationsInfo)
    problematic_phrases: List[str] = Field(default_factory=list)
    theory_and_proofs: TheoryAndProofsInfo = Field(default_factory=TheoryAndProofsInfo)
    broader_impacts_extraction: BroaderImpactsInfo = Field(default_factory=BroaderImpactsInfo)
    llm_usage_extraction: LLMUsageInfo = Field(default_factory=LLMUsageInfo)
    human_subjects_extraction: HumanSubjectsInfo = Field(default_factory=HumanSubjectsInfo)
    licenses_extraction: LicensesInfo = Field(default_factory=LicensesInfo)


# ---------------------------------------------------------------------------
# Modelo de un ítem del checklist NeurIPS
# ---------------------------------------------------------------------------

class ChecklistItem(BaseModel):
    answer: str = "N/A"           # "Yes" | "No" | "N/A"
    evidence: str = ""
    justification: str = ""
    is_no_justified: bool = False
    verified: bool = False         # True si pasó por ChecklistVerificationSkill
    was_refined: bool = False      # True si la verificación refinó la justificación


# ---------------------------------------------------------------------------
# Modelo de evaluación completa
# ---------------------------------------------------------------------------

class EvaluationResult(BaseModel):
    claims: ChecklistItem = Field(default_factory=ChecklistItem)
    limitations: ChecklistItem = Field(default_factory=ChecklistItem)
    theory_assumptions_proofs: ChecklistItem = Field(default_factory=ChecklistItem)
    experimental_result_reproducibility: ChecklistItem = Field(default_factory=ChecklistItem)
    open_access_data_code: ChecklistItem = Field(default_factory=ChecklistItem)
    experimental_setting_details: ChecklistItem = Field(default_factory=ChecklistItem)
    experiment_statistical_significance: ChecklistItem = Field(default_factory=ChecklistItem)
    experiments_compute_resource: ChecklistItem = Field(default_factory=ChecklistItem)
    code_of_ethics: ChecklistItem = Field(default_factory=ChecklistItem)
    broader_impacts: ChecklistItem = Field(default_factory=ChecklistItem)
    safeguards: ChecklistItem = Field(default_factory=ChecklistItem)
    licenses: ChecklistItem = Field(default_factory=ChecklistItem)
    assets: ChecklistItem = Field(default_factory=ChecklistItem)
    crowdsourcing_human_subjects: ChecklistItem = Field(default_factory=ChecklistItem)
    irb_approvals: ChecklistItem = Field(default_factory=ChecklistItem)
    declaration_llm_usage: ChecklistItem = Field(default_factory=ChecklistItem)


# ---------------------------------------------------------------------------
# Estado global de la auditoría
# ---------------------------------------------------------------------------

class AuditState(BaseModel):
    """
    Estado tipado que fluye por todo el pipeline de auditoría.

    Reemplaza el `context: Dict[str, Any]` no tipado de la arquitectura anterior.
    Cada skill recibe y devuelve una instancia de AuditState parcialmente populada.
    """

    # — Input principal —
    paper_text: str

    # — Flags de control de flujo —
    invalid_paper: bool = False
    invalid_reason: Optional[str] = None

    # — Resultados de extracción (Fase 1) —
    extracted_info: Optional[Dict[str, Any]] = None      # dict nativo para compatibilidad con el frontend
    map_steps: List[Dict[str, Any]] = Field(default_factory=list)
    reduce_step: Optional[Dict[str, Any]] = None
    original_extraction_raw: Optional[Dict[str, Any]] = None

    # — Resultados de extracción RAG (Fase 1.5) —
    extracted_hyperparameters_hybrid: Optional[Dict[str, Any]] = None
    triage_fragments: List[Dict[str, Any]] = Field(default_factory=list)
    hybrid_extraction_error: Optional[str] = None

    # — Resultados de evaluación (Fase 2) —
    evaluation: Optional[Dict[str, Any]] = None          # dict nativo para compatibilidad con el frontend
    evaluation_signals: Optional[Dict[str, str]] = None

    # — Red flags heredadas de regex (compatibilidad) —
    red_flags: Dict[str, Any] = Field(default_factory=dict)

    # — Métricas de ejecución (Fase 3) —
    metrics: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    caracteres: int = 0

    # — Errores no fatales —
    extraction_error: Optional[str] = None
    evaluation_error: Optional[str] = None

    class Config:
        # Permite campos extra provenientes de skills legacy sin romper la validación
        extra = "allow"

    # ------------------------------------------------------------------
    # Helpers de conversión para compatibilidad con el frontend (dict)
    # ------------------------------------------------------------------

    def to_frontend_dict(self) -> Dict[str, Any]:
        """
        Construye el diccionario final que espera el frontend Streamlit.
        Mantiene las mismas claves de siempre para no romper app.py.
        """
        evaluation = self.evaluation or {}
        return {
            "claims": evaluation.get("claims", {}),
            "limitations": evaluation.get("limitations", {}),
            "theory_assumptions_proofs": evaluation.get("theory_assumptions_proofs", {}),
            "experimental_result_reproducibility": evaluation.get("experimental_result_reproducibility", {}),
            "open_access_data_code": evaluation.get("open_access_data_code", {}),
            "experimental_setting_details": evaluation.get("experimental_setting_details", {}),
            "experiment_statistical_significance": evaluation.get("experiment_statistical_significance", {}),
            "experiments_compute_resource": evaluation.get("experiments_compute_resource", {}),
            "code_of_ethics": evaluation.get("code_of_ethics", {}),
            "broader_impacts": evaluation.get("broader_impacts", {}),
            "safeguards": evaluation.get("safeguards", {}),
            "licenses": evaluation.get("licenses", {}),
            "assets": evaluation.get("assets", {}),
            "crowdsourcing_human_subjects": evaluation.get("crowdsourcing_human_subjects", {}),
            "irb_approvals": evaluation.get("irb_approvals", {}),
            "declaration_llm_usage": evaluation.get("declaration_llm_usage", {}),
            "informacion_extraida": self.extracted_info or {},
            "red_flags": self.red_flags,
            "metricas": self.metrics or {},
            "general_analysis_map": self.map_steps,
            "general_analysis_reduce": self.reduce_step or {},
            "hybrid_triage_fragments": self.triage_fragments,
            "evaluation_signals": self.evaluation_signals or {},
            "extracted_hyperparameters_hybrid": self.extracted_hyperparameters_hybrid or {},
            "original_extraction_raw": self.original_extraction_raw or {},
        }
