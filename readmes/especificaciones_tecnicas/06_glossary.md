# 06 — Domain Glossary

This document defines the technical terms, domain concepts, and programmatic constants used in the NeurIPS 2026 Reproducibility Auditor.

## 1. Core Domain Concepts

### 1.1 NeurIPS 2026 Reproducibility Checklist
The authoritative set of 16 transparency criteria required for paper submissions. Items include Claims, Limitations, Theory, Experimental Reproducibility, Data/Code Availability, etc.

### 1.2 Audit Pipeline
The sequence of 6 automated phases executed by the `PaperAuditor` to evaluate a paper.
1. **FASE 1**: Information Extraction (General metadata).
2. **FASE 1.5**: Hybrid Hyperparameter Extraction (RAG-based).
3. **FASE 2**: Reproducibility Evaluation (Scoring against the 16 checklist items).
4. **FASE 2.5**: Strict Verification (Auditor 2 check for false negatives).
5. **FASE 3**: Metrics Calculation (Aggregate scores).
6. **FASE 4**: Metadata Aggregation (Assembly for frontend).

### 1.3 MAP/REDUCE Extraction
A pattern used to process long documents.
- **MAP**: The paper is split into fragments; the LLM extracts information from each fragment independently.
- **REDUCE**: The per-fragment results are consolidated into a single master JSON.

### 1.4 Hybrid Hyperparameter Extraction
A combination of three techniques:
1. **Regex**: To find candidate mentions in text and tables.
2. **RAG**: To retrieve relevant chunks from a vector store (ChromaDB).
3. **LLM Extraction**: To produce structured data from the retrieved context.

## 2. Programmatic Constants

### 2.1 Checklist Keys (`CHECKLIST_KEYS`)
The machine-readable keys used in the evaluation dictionary.
- `claims`, `limitations`, `theory_assumptions_proofs`, `experimental_result_reproducibility`, `open_access_data_code`, `experimental_setting_details`, `experiment_statistical_significance`, `experiments_compute_resource`, `code_of_ethics`, `broader_impacts`, `safeguards`, `licenses`, `assets`, `crowdsourcing_human_subjects`, `irb_approvals`, `declaration_llm_usage`.

### 2.2 Quality Tier Labels
Labels displayed in the gauge chart based on the reproducibility score:
- **Strong Accept** (≥ 87.5%)
- **Accept** (≥ 75%)
- **Borderline** (≥ 62.5%)
- **Weak Reject** (≥ 50%)
- **Reject** (≥ 25%)
- **Strong Reject** (< 25%)

### 2.3 Model Names
- `EXTRACTION_MODEL_NAME`: Default model for FASE 1.
- `MAP_MODEL_NAME` / `REDUCE_MODEL_NAME`: Models used in fragmentation phases.
- `EVALUATION_MODEL_NAME`: "Senior Area Chair" persona model.
- `VERIFICATION_MODEL_NAME`: "Auditor 2" persona model.

## 3. Technical Equivalences

| Backend Term | Frontend Term | Meaning |
|---|---|---|
| `paper_text` | `md_text` | The full Markdown content of the paper. |
| `extracted_info` | `informacion_extraida` | The dict containing all technical metadata. |
| `evaluation` | `resultado` | The dict containing the checklist item scores. |
| `metricas` | `summary_scores` | Aggregate reproducibility and coverage metrics. |
| `status == "risk"` | "Red Warning" | Indicates a desk-reject risk in the UI. |
| `is_no_justified` | "Justificado" | Boolean indicating if a negative answer has a valid reason. |

## 4. API Endpoints
- **Semantic Scholar**: `https://api.semanticscholar.org/graph/v1/paper/search`
- **Google GenAI**: `https://generativelanguage.googleapis.com/v1beta/`
