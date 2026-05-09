from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class ChecklistItem(BaseModel):
    """Modelo para un ítem individual del checklist de NeurIPS"""
    answer: str = Field(..., description="Yes, No, or N/A")
    evidence: Optional[str] = Field(None, description="Cita o fragmento de texto que respalda la respuesta")
    justification: Optional[str] = Field(None, description="Razonamiento detrás de la evaluación")
    verified: bool = Field(False, description="Si ha pasado por la fase de verificación estricta")
    was_corrected: bool = Field(False, description="Si la respuesta cambió durante la verificación")

class ExtractedInfo(BaseModel):
    """Modelo para la información técnica extraída del paper"""
    paper_title: str = "Unknown"
    authors: List[str] = []
    paper_type: str = "Unknown"
    thought_process: str = ""
    hyperparameters: Dict[str, Any] = {}
    hardware: Any = {}
    context_mapping: List[str] = []

class AuditState(BaseModel):
    """Estado completo de una auditoría"""
    paper_text: str
    extracted_info: ExtractedInfo
    evaluation: Dict[str, ChecklistItem] = {}
    metrics: Dict[str, Any] = {}
    execution_time: float = 0.0
    red_flags: Dict[str, bool] = {}
    
    class Config:
        arbitrary_types_allowed = True
