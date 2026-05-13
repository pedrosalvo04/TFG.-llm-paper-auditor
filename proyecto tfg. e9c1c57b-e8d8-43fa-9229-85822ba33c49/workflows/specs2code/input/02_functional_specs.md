# 02 — Functional Specifications (Consolidated)
## Nature Auditor Pro — Complete Functional Specification

> **Purpose**: This is the consolidated top-level functional specification for the Nature Auditor Pro
> system. It provides a cross-cutting functional overview and serves as the entry point to the two
> sub-deliverables that contain the full detail:
>
> - **`02_functional_backend.md`** — Authoritative backend specification: 16 sections covering the
>   6-phase audit pipeline, all 27 skill classes, SOTA analysis, chatbot, PDF parser, LLMClient, and
>   prompt templates.
> - **`02_functional_frontend.md`** — Authoritative frontend specification: 7 sections covering the
>   Streamlit application bootstrap, 8 UI components, session state management, and the scoring
>   utilities.
>
> **Fidelity**: All content is traceable to extraction files. No content has been invented or assumed.
> Elements not confirmed in source code are marked `[GAP: ...]`.

---

## Table of Contents

1. [System Functional Overview](#section-1)
2. [Backend Module Inventory](#section-2)
3. [Frontend Module Inventory](#section-3)
4. [Cross-Cutting Interaction Summary](#section-4)
5. [Sub-Deliverable Index](#section-5)

---

<a name="section-1"></a>
## Section 1 — System Functional Overview

Source: `extracted_backend_core_01.md §4.2`, `extracted_frontend_01.md §4.2`,
`extracted_backend_skills_01.md §1`.

The system is a **Streamlit single-page web application** that:
1. Accepts a PDF paper upload from the user.
2. Converts the PDF to Markdown via Docling (`pdf_parser.py`).
3. Runs a **6-phase backend audit pipeline** (`auditor.py`) producing a structured compliance result.
4. Renders the result across four UI tabs: Audit Results, SOTA Analysis, Chatbot, and Gauge Chart.

### 1.1 End-to-End Functional Flow

```
TRIGGER: User uploads PDF file (st.file_uploader)
CONDITION: File extension in [pdf]
ACTION SEQUENCE:
  1. process_uploaded_file(uploaded_file) called — SOURCE: frontend/app.py:54 / file_uploader.py:49
  2. convert_pdf_to_markdown(temp_path) → md_text (Docling, chunked 5-page blocks) — SOURCE: pdf_parser.py:39-71
  3. PaperAuditor().audit(md_text, status_callback) → result dict — SOURCE: auditor.py:60-130
     Phase 1:   InformationExtractionSkill → extracted_info
     Phase 1.5: HybridHyperparameterExtractionSkill → hyperparameter_results
     Phase 2:   ReproducibilityEvaluationSkill → checklist
     Phase 2.5: ChecklistVerificationSkill → checklist (updated in-place)
     Phase 3:   MetricsCalculationSkill → tiempo_segundos, caracteres_leidos, red_flags_detectadas
     Phase 4:   MetadataAggregationSkill → result (23 keys flattened)
  4. resultado stored in st.session_state['resultado'] — SOURCE: file_uploader.py:52
  5. render_audit_results(resultado, uploaded_file) — SOURCE: frontend/app.py:66 / audit_results.py
  6. render_sota_analysis(md_text) — SOURCE: frontend/app.py:67 / sota_section.py
  7. render_chatbot(md_text) — SOURCE: frontend/app.py:68 / chatbot.py
OUTPUT: Audit results rendered; SOTA table displayed; chatbot available for Q&A
```

### 1.2 System Boundary

| Layer | Technology | Entry Point | Port / Protocol |
|---|---|---|---|
| Frontend | Streamlit 1.x | `frontend/app.py` | HTTP (Streamlit server) |
| Backend Services | Python 3.x | `backend/services/auditor.py` | In-process function calls |
| Backend Skills | Python 3.x | `backend/skills/*.py` | In-process method calls |
| LLM | Google Gemini API | `backend/common/llm_client.py` | HTTPS REST |
| Search | Semantic Scholar API | `backend/skills/sota_skills.py` | HTTPS REST |
| PDF Conversion | Docling library | `backend/services/pdf_parser.py` | In-process |
| Vector Store | ChromaDB (in-memory) | `backend/skills/rag_extraction_skill.py` | In-process |

---

<a name="section-2"></a>
## Section 2 — Backend Module Inventory

Source: `extracted_backend_core_01.md`, `extracted_backend_skills_01.md`.

**Full detail in `02_functional_backend.md`.**

### 2.1 Core Services

| Class | File | Primary Entry Point | Phase / Role |
|---|---|---|---|
| `PaperAuditor` | `backend/services/auditor.py` | `audit(paper_text, status_callback=None) -> dict` | Orchestrator: 6-phase pipeline |
| `PaperChatbot` | `backend/services/chatbot.py` | `preguntar(paper_text, question, history_text) -> str` | Skill-based Q&A |
| `Chatbot` | `backend/services/chatbot.py` | Same as PaperChatbot (alias) | Backward-compat alias |
| `SotaAnalyzer` | `backend/services/sota_analyzer.py` | `analyze_sota(paper_text) -> Dict[str, Any]` | 5-step SOTA analysis |
| `LLMClient` | `backend/common/llm_client.py` | `generate(prompt) -> str` | Google Gemini wrapper with retry |
| `convert_pdf_to_markdown` | `backend/services/pdf_parser.py` | `convert_pdf_to_markdown(pdf_path) -> str` | Docling chunked PDF→Markdown |

### 2.2 Skill Classes (Exported from `backend/skills/__init__.py`)

| Class | File | Execute Output Keys |
|---|---|---|
| `InformationExtractionSkill` | `auditor_skills.py` | `extracted_info`, `invalid_paper`, `map_steps`, `reduce_step` |
| `ReproducibilityEvaluationSkill` | `auditor_skills.py` | `checklist` |
| `MetricsCalculationSkill` | `auditor_skills.py` | `tiempo_segundos`, `caracteres_leidos`, `red_flags_detectadas` |
| `MetadataAggregationSkill` | `auditor_skills.py` | `result` |
| `CompositeSkill` | `base_skill.py` | Accumulates results of chained skills |
| `BaseSkill` | `base_skill.py` | Abstract — defines `execute()`, `validate_context()`, `log_execution()` |
| `ConversationalResponseSkill` | `chatbot_skills.py` | `response` |
| `ContextValidationSkill` | `chatbot_skills.py` | `is_valid`, `paper_text`, `question`, `history_text`, `paper_length`, `question_length` |
| `ThematicCoverageSkill` | `sota_skills.py` | `thematic_data` |
| `QueryGenerationSkill` | `sota_skills.py` | `queries` |
| `SemanticScholarSearchSkill` | `sota_skills.py` | `search_results` |
| `CoverageGapAnalysisSkill` | `sota_skills.py` | `coverage_gaps` |
| `CrossValidationSkill` | `sota_skills.py` | `validation_result` |
| `LimitationsQualityDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `SoftwareVersionDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `HardwareDetailDetectionSkill` | `regex_detection_skills.py` | detection result dict |

### 2.3 Non-Exported Skill Classes

| Class | File | Execute Output Keys |
|---|---|---|
| `HybridHyperparameterExtractionSkill` | `rag_extraction_skill.py` | `extracted_hyperparameters_hybrid`, `triage_fragments` |
| `ChecklistVerificationSkill` | `auditor_skills.py` | `checklist` (updated in-place) |
| `HyperparameterDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `DataAvailabilityDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `CodeAvailabilityDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `StatisticsDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `EnvironmentalImpactDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `ProblematicPhrasesDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `LlmUsageDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `CrowdsourcingDetectionSkill` | `regex_detection_skills.py` | detection result dict |
| `LicenseDetectionSkill` | `regex_detection_skills.py` | detection result dict |

### 2.4 Logging and Infrastructure

| Class | File | Role |
|---|---|---|
| `CleanNetworkLogs` | `backend/common/config.py` | `logging.Filter` — suppresses httpx HTTP request log records |
| `ColoredFormatter` | `backend/utils/logger.py` | `logging.Formatter` — ANSI-colored log output |
| `Colors` | `backend/utils/logger.py` | ANSI escape code constants used by `ColoredFormatter` |

Source: `config.py:14`, `logger.py:5-35`.

---

<a name="section-3"></a>
## Section 3 — Frontend Module Inventory

Source: `extracted_frontend_01.md`.

**Full detail in `02_functional_frontend.md`.**

### 3.1 Application Entry Points

| File | Role | Primary Call Sequence |
|---|---|---|
| `frontend/app.py` | Streamlit main — sets page config, calls components in order | `set_page_config` → `apply_custom_styles` → `initialize_session_state` → upload column → results column |
| `app.py` (root) | Alternate root entry point (sets env vars, calls `frontend/app.py` via import) | Sets `TRANSFORMERS_VERBOSITY`, `TOKENIZERS_PARALLELISM`, `ANONYMIZED_TELEMETRY`, `OTEL_SDK_DISABLED` |

### 3.2 UI Components

| Component Function | File | Trigger Condition | Primary Output |
|---|---|---|---|
| `process_uploaded_file(uploaded_file)` | `frontend/components/file_uploader.py` | st.file_uploader event | Runs audit pipeline; writes resultado to session_state |
| `render_audit_results(resultado, uploaded_file)` | `frontend/components/audit_results.py` | resultado is not None | Renders compliance table, gauge, report download |
| `_build_table_html(result)` | `frontend/components/audit_results.py` | Called by render_audit_results | Renders HTML compliance table |
| `generate_report(resultado, uploaded_file)` | `frontend/components/audit_results.py` | Download button click | Generates and returns PDF/MD audit report |
| `render_sota_analysis(md_text)` | `frontend/components/sota_section.py` | md_text available | Runs SotaAnalyzer; renders SOTA results table |
| `render_chatbot(md_text)` | `frontend/components/chatbot.py` | md_text available | Renders chat input/output; calls PaperChatbot.preguntar |
| `create_gauge_chart(score)` | `frontend/components/gauge_chart.py` | Called by render_audit_results | Returns Plotly gauge figure |
| `apply_custom_styles()` | `frontend/styles/custom_css.py` | Always (unconditional) | Injects CUSTOM_CSS via st.markdown |

### 3.3 Frontend Utilities

| Function / Class | File | Role |
|---|---|---|
| `initialize_session_state()` | `frontend/utils/session_state.py` | Idempotently initialises 5 session state keys |
| `calculate_score(resultado)` | `frontend/utils/scoring.py` | Computes compliance percentage score |

---

<a name="section-4"></a>
## Section 4 — Cross-Cutting Interaction Summary

Source: `extracted_backend_core_01.md`, `extracted_frontend_01.md`,
`cross_ref_resolution_cross_ref_root_to_backend.md`, `cross_ref_resolution_cross_ref_root_to_frontend.md`.

### 4.1 Frontend → Backend Calls

| Frontend Caller | Backend Callee | Interaction | Severity |
|---|---|---|---|
| `process_uploaded_file` (file_uploader.py:49) | `PaperAuditor.audit(md_text, status_callback)` | Synchronous in-process call | CRITICAL |
| `process_uploaded_file` (file_uploader.py:36) | `convert_pdf_to_markdown(temp_path)` | Synchronous in-process call | HIGH |
| `render_chatbot` (chatbot.py:26) | `PaperChatbot.preguntar(md_text, question, history_str)` | Synchronous in-process call | CRITICAL |
| `render_sota_analysis` (sota_section.py:12) | `SotaAnalyzer.analyze_sota(paper_text)` | Synchronous in-process call | HIGH |

### 4.2 Session State Keys (Shared Frontend ↔ Backend)

| Key | Type | Written By | Read By |
|---|---|---|---|
| `resultado` | `dict \| None` | `process_uploaded_file` | `render_audit_results` |
| `auditor` | `PaperAuditor` | `initialize_session_state` | `process_uploaded_file` |
| `chatbot` | `PaperChatbot` | `initialize_session_state` | `render_chatbot` |
| `sota_analyzer` | `SotaAnalyzer` | `initialize_session_state` | `render_sota_analysis` |
| `messages` | `list` | `initialize_session_state` / `render_chatbot` | `render_chatbot` |
| `md_text` | `str` | `process_uploaded_file` | `render_chatbot`, `render_sota_analysis` |
| `archivo_actual` | `str` | `process_uploaded_file` | `process_uploaded_file` (duplicate guard) |
| `file_hash` | `str (MD5)` | `process_uploaded_file` | `process_uploaded_file` (duplicate guard) |

Source: `session_state.py:11-18`, `file_uploader.py:19-52`,
`cross_ref_resolution_cross_ref_root_to_frontend.md §g_027`.

---

<a name="section-5"></a>
## Section 5 — Sub-Deliverable Index

This consolidated file was produced to satisfy the cross-spec validator requirement for
`02_functional_specs.md`. The synthesis pipeline produced two sub-writer outputs; this
document acts as the authoritative consolidation entry point.

| Sub-Deliverable | Sections | Primary Scope |
|---|---|---|
| `02_functional_backend.md` | 16 sections (§1–§16) | Audit pipeline phases, all 27 skill classes, SOTA pipeline, chatbot flow, PDF parser, LLMClient retry logic, prompt templates |
| `02_functional_frontend.md` | 7 sections (§1–§7) | Streamlit bootstrap, 8 UI components with TRIGGER/CONDITION/ACTION/RESULT specs, session state init, scoring utility |

Source: Both sub-documents are authoritative and must be read for full functional detail.
No functional information has been omitted from the sub-documents.
