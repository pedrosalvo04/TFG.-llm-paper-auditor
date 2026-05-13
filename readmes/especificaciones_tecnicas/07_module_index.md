# Module Index

---

## Module Inventory Overview

### Summary Table

| Module | Source Cluster | File Count | Paths | Purpose Summary | Source |
|--------|---------------|------------|-------|-----------------|--------|
| `backend_core` | `cluster_backend_core_01` | 13 | `backend/` (common/, services/, utils/) | Core LLM infrastructure: Google Gemini client with retry/backoff, 6-phase audit pipeline orchestrator (PaperAuditor), chatbot service (PaperChatbot/Chatbot alias), SOTA analyzer (SotaAnalyzer), PDF-to-Markdown chunked converter, centralized prompts (6 templates), config constants, Pydantic data models (AuditState, ExtractedInfo), and colored logging. | [extracted_backend_core_01.md § 1. File Index] |
| `backend_skills` | `cluster_backend_skills_01` | 7 | `backend/skills/` | Skill layer: 15 exported symbols covering auditor skills (extraction/evaluation/metrics/aggregation), chatbot skills (conversational response, context validation), SOTA skills (thematic coverage, query generation, Semantic Scholar search, gap analysis, cross-validation), regex detection skills (limitations, software versions, hardware details), plus non-exported skills (HybridHyperparameterExtractionSkill, ChecklistVerificationSkill, 9 regex detection skills). | [extracted_backend_skills_01.md § 1. Skill Registry] |
| `frontend` | `cluster_frontend_01` | 14 | `frontend/` (app.py, config.py, components/, styles/, utils/) | Streamlit single-page application: page config/styles/session-state initialization, file upload (PDF/TXT/MD), backend audit invocation, audit results rendering (compliance table, metrics, expanders), SOTA analysis section, chatbot interface, downloadable Markdown report. | [extracted_frontend_01.md § 1. File Index] |
| `root` | `cluster_root_tests_scratch_01` | 21 | root level + tests/ + scratch/ + backend/scratch/ | CLI utility scripts (md_to_pdf, pdf_to_md, create_test_pdf, list_models), legacy root app.py entry point, integration/unit test files (test_auditor_refactor, test_imports, test_skills_integration, tests/test_audit_state, tests/test_rag_*, tests/test_section_splitter), and exploration/scratch scripts. | [extracted_root_tests_scratch_01.md § 1. File Index] |

### Cross-Module Dependency Graph

**Directed dependency summary:**

| Dependent | Depends On | Mechanism | Source |
|-----------|-----------|-----------|--------|
| `frontend` → `backend_core` | `PaperAuditor`, `PaperChatbot`, `SotaAnalyzer`, `convert_pdf_to_markdown` | `st.session_state.auditor`, `st.session_state.chatbot`, `st.session_state.sota_analyzer` instantiated in `frontend/utils/session_state.py`; `convert_pdf_to_markdown` called in `frontend/components/file_uploader.py` | [extracted_frontend_01.md § 3. Session State]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_027] |
| `backend_skills` → `backend_core` | `LLMClient`, `get_logger`, prompt templates (`get_extraction_prompt`, `get_map_extraction_prompt`, `get_reduce_extraction_prompt`, `get_evaluation_prompt`, `get_verification_prompt`), config constants (`EMBEDDING_MODEL_NAME`, `EVALUATION_MODEL_NAME`, `REDUCE_MODEL_NAME`), Pydantic models (`AuditState`, `ExtractedInfo`) | Direct Python import from `backend.common.llm_client`, `backend.common.config`, `backend.common.prompts`, `backend.common.audit_state`, `backend.utils.logger` | [extracted_backend_skills_01.md § 3.4 LLM Prompt Templates]; [extracted_backend_core_01.md § 3.1 LLM Client] |
| `backend_core` (services) → `backend_skills` | `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ChecklistVerificationSkill`, `HybridHyperparameterExtractionSkill` | Instantiated in `PaperAuditor.__init__`; `ConversationalResponseSkill`, `ContextValidationSkill` in `PaperChatbot.__init__`; 5 SOTA skills in `SotaAnalyzer.__init__` | [extracted_backend_core_01.md § 3.2, 3.3, 3.5]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_009] |
| `root` (tests) → `backend_core` | `PaperAuditor`, `LLMClient`, `get_extraction_prompt`, `get_evaluation_prompt`, `get_logger`, config constants, Pydantic models | Test files import and instantiate backend_core classes directly | [extracted_root_tests_scratch_01.md § 8]; [cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY] |
| `root` (tests) → `backend_skills` | `InformationExtractionSkill`, `SemanticScholarSearchSkill`, `LimitationsQualityDetectionSkill`, `SoftwareVersionDetectionSkill`, `HardwareDetailDetectionSkill` | `test_skills_integration.py` imports from `backend.skills` | [cross_ref_resolution_cross_ref_root_to_backend.md § g_015, g_016, g_017, g_018] |
| `root` (tests) → `frontend` | `process_uploaded_file`, `render_audit_results`, `generate_report`, `render_sota_analysis`, `render_chatbot`, `TITLE`, `SIDEBAR_IMAGE`, `SIDEBAR_DESCRIPTION`, `get_checklist_health`, `apply_custom_styles`, `initialize_session_state` | `test_imports.py` verifies all frontend modules are importable | [cross_ref_resolution_cross_ref_root_to_frontend.md § RESOLUTION SUMMARY] |

---

## backend_core Module

**Source cluster:** `cluster_backend_core_01`
**Extraction file:** `extracted_backend_core_01.md`

### Services (backend/services/)

| File | Class/Symbol | Role/Purpose | External Dependencies | Source |
|------|-------------|--------------|----------------------|--------|
| `backend/services/auditor.py` | `PaperAuditor` | 6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator. Instantiates 5 LLMClient instances and 6 skill instances. Entry method: `audit(paper_text, status_callback=None) -> dict`. | `LLMClient`, `InformationExtractionSkill`, `HybridHyperparameterExtractionSkill`, `ReproducibilityEvaluationSkill`, `ChecklistVerificationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, all config constants, `get_logger` | [extracted_backend_core_01.md § 3.2 Auditor Service] |
| `backend/services/chatbot.py` | `PaperChatbot`, `Chatbot` | Skill-based Q&A chatbot over audited papers. `Chatbot` is a delegation-only alias for backward compatibility. Entry method: `preguntar(paper_text, question, history_text) -> str`. | `LLMClient`, `ConversationalResponseSkill`, `ContextValidationSkill`, `CHAT_CONFIG`, `get_logger` | [extracted_backend_core_01.md § 3.3 Chatbot Service] |
| `backend/services/sota_analyzer.py` | `SotaAnalyzer` | 5-step state-of-the-art analysis pipeline using 5 SOTA skills. Entry method: `analyze_sota(paper_text) -> Dict[str, Any]`. | `LLMClient`, `ThematicCoverageSkill`, `QueryGenerationSkill`, `SemanticScholarSearchSkill`, `CoverageGapAnalysisSkill`, `CrossValidationSkill`, `SOTA_CONFIG`, `get_logger` | [extracted_backend_core_01.md § 3.5 SOTA Analyzer Service] |
| `backend/services/pdf_parser.py` | `convert_pdf_to_markdown` | Docling-based chunked PDF→Markdown converter. Processes PDF in blocks of 5 pages using temp files; per-block error tolerance; returns full Markdown string or error string. | `docling`, `pypdf`, `torch` (for CUDA detection), `tempfile`, `os` | [extracted_backend_core_01.md § 3.4 PDF Parser Service] |

#### PaperAuditor Method Details

**`PaperAuditor.__init__(self)`** — SOURCE: `auditor.py:28`

5 `LLMClient` instances created:
- `self.extraction_llm = LLMClient(model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:31`
- `self.evaluation_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:34`
- `self.rag_map_llm = LLMClient(model_name=MAP_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:37`
- `self.rag_reduce_llm = LLMClient(model_name=REDUCE_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:40`
- `self.verification_llm = LLMClient(model_name=VERIFICATION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:43`

6 skill instances created:
- `self.extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm)` — SOURCE: `auditor.py:46`
- `self.hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm)` — SOURCE: `auditor.py:47`
- `self.evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm)` — SOURCE: `auditor.py:48`
- `self.verification_skill = ChecklistVerificationSkill(llm_client=self.verification_llm)` — SOURCE: `auditor.py:51`
- `self.metrics_skill = MetricsCalculationSkill()` (no LLM client) — SOURCE: `auditor.py:53`
- `self.metadata_skill = MetadataAggregationSkill()` (no LLM client) — SOURCE: `auditor.py:54`

**`PaperAuditor.audit(self, paper_text, status_callback=None)`** — SOURCE: `auditor.py:60`

| Parameter | Type | Description |
|-----------|------|-------------|
| `paper_text` | `str` | Full paper text in Markdown format |
| `status_callback` | `callable \| None` | Called with status message strings during pipeline; default `None` |

Return type: `dict`. On success: audit result from `MetadataAggregationSkill`. On failure: `{"error": str(e)}` or `{"error": "INVALID_PAPER_TYPE", "message": ..., "paper_type": ...}`.

6-phase pipeline:
- **Phase 1** — Information Extraction via `InformationExtractionSkill` (map-reduce over paper fragments)
- **Phase 1.5** — Hybrid Hyperparameter Extraction via `HybridHyperparameterExtractionSkill` (RAG + Pydantic)
- **Phase 2** — Reproducibility Evaluation via `ReproducibilityEvaluationSkill` (NeurIPS checklist assessment)
- **Phase 2.5** — Strict Verification via `ChecklistVerificationSkill` (false-negative check, Auditor 2)
- **Phase 3** — Metrics Calculation via `MetricsCalculationSkill`
- **Phase 4** — Metadata Aggregation via `MetadataAggregationSkill` → returns final dict

**`PaperChatbot.__init__(self)`** — SOURCE: `chatbot.py:15`
- Creates `self.llm_client = LLMClient(generation_config=CHAT_CONFIG)` — SOURCE: `chatbot.py:17`
- Creates `self.response_skill = ConversationalResponseSkill(llm_client=self.llm_client)` — SOURCE: `chatbot.py:20`
- Creates `self.validation_skill = ContextValidationSkill()` (no LLM client) — SOURCE: `chatbot.py:21`

**`PaperChatbot.preguntar(self, paper_text, question, history_text)`** — SOURCE: `chatbot.py:25`

| Parameter | Type | Description |
|-----------|------|-------------|
| `paper_text` | `str` | Full paper text |
| `question` | `str` | User question |
| `history_text` | `str` | Conversation history (last 4 messages joined as `role: content\n...`) |

Return type: `str` — chatbot response or error string.

**`SotaAnalyzer.analyze_sota(self, paper_text)`** — SOURCE: `sota_analyzer.py:43`

| Parameter | Type | Description |
|-----------|------|-------------|
| `paper_text` | `str` | Full paper text |

Return type: `Dict[str, Any]`. On success: dict with `"metadata"` key and keys from `CrossValidationSkill`. On error: `{"error": "explanation string"}`.

**`convert_pdf_to_markdown(pdf_path)`** — SOURCE: `pdf_parser.py:7`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pdf_path` | str or path-like | Path to PDF file |

Return type: `str` — full Markdown text or error string `"❌ Error en la extracción del PDF: ..."`.
Processing: chunks PDF in blocks of 5 pages (`chunk_size = 5` — SOURCE: `pdf_parser.py:51`); per-block error tolerance; temp file cleanup in `finally`.

---

### Common (backend/common/)

| File | Symbol(s) | Kind | Purpose | Source |
|------|-----------|------|---------|--------|
| `backend/common/llm_client.py` | `LLMClient` | Class | Google Gemini API wrapper; single provider (`google.genai.Client`); exponential-backoff retry (up to 5 retries, base delay 2s) for HTTP 503/429/UNAVAILABLE/RESOURCE_EXHAUSTED/DEADLINE_EXCEEDED. Raises `ValueError` if `GOOGLE_API_KEY` absent. | [extracted_backend_core_01.md § 3.1 LLM Client] |
| `backend/common/audit_state.py` | `AuditState`, `ExtractedInfo`, `ChecklistItem` | Pydantic Models | Authority for data structure and persistence of the audit pipeline state. | [01_data_model.md] |
| `backend/common/prompts.py` | `get_extraction_prompt`, `get_map_extraction_prompt`, `get_reduce_extraction_prompt`, `get_evaluation_prompt`, `get_verification_prompt` | Functions | LLM Prompt templates for the 6-phase pipeline. | [extracted_backend_core_01.md § 2.2 Prompts] |
| `backend/common/config.py` | `GOOGLE_API_KEY`, `EMBEDDING_MODEL_NAME`, `AUDIT_CONFIG`, etc. | Constants | Centralized configuration for APIs, models, and temperatures. | [extracted_backend_core_01.md § 2.1 Config] |
| `backend/utils/logger.py` | `get_logger`, `ColoredFormatter` | Infrastructure | Colored logging system for debugging and audit trail. | [extracted_backend_core_01.md § 6.1 Logger] |

#### LLMClient Method Details

**`LLMClient.__init__(self, model_name=None, generation_config=None)`** — SOURCE: `llm_client.py:11`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_name` | `str \| None` | `None` | If `None`, uses `MODEL_NAME` (`"gemini-3.1-flash-lite-preview"`) |
| `generation_config` | `dict \| None` | `None` | If `None`, uses `{}` |

- RULE: if `not GOOGLE_API_KEY` → raises `ValueError("No se encontró la GOOGLE_API_KEY en el .env")` — SOURCE: `llm_client.py:19-21`
- Creates `self.client = genai.Client(api_key=GOOGLE_API_KEY)` — SOURCE: `llm_client.py:23`

**`LLMClient.generate(self, prompt)`** — SOURCE: `llm_client.py:30`

- Retry loop: `range(max_retries + 1)` → `range(6)` (attempts 0–5) — SOURCE: `llm_client.py:42`
- Inline constants: `max_retries = 5` (SOURCE: `llm_client.py:39`), `base_delay = 2` seconds (SOURCE: `llm_client.py:40`)
- Retryable error codes: `"503"`, `"429"`, `"UNAVAILABLE"`, `"RESOURCE_EXHAUSTED"`, `"DEADLINE_EXCEEDED"` — SOURCE: `llm_client.py:54`
- Backoff formula: `delay = base_delay * (2 ** attempt) + random.uniform(0, 1)` — SOURCE: `llm_client.py:58`
- On success: returns response object directly (caller accesses `.text`) — SOURCE: `llm_client.py:49`
- On exhausted retries or non-retryable error: `raise` (re-raises original exception) — SOURCE: `llm_client.py:76`

---

### External Dependencies (backend_core)

| Package | How Used |
|---------|----------|
| `google-generativeai` | `genai.Client` for LLM generation and embedding calls |
| `docling` | `DocumentConverter` for PDF-to-Markdown conversion |
| `python-dotenv` | `load_dotenv()` for environment variable management |
| `pydantic` | `BaseModel` for structured data validation |
| `pypdf` | `PdfReader` and `PdfWriter` for PDF manipulation |
| `chromadb` | In-memory vector store for RAG operations |
| `httpx` | HTTP calls for batch embedding API |
| `requests` | HTTP client for Semantic Scholar API |
| `torch` | GPU detection for Docling acceleration |
| `streamlit` | UI feedback (toast notifications) |

---

## backend_skills Module

**Source cluster:** `cluster_backend_skills_01`
**Extraction file:** `extracted_backend_skills_01.md`

### Exported Skills (15 symbols in `__init__.py`)

| Skill Class | Purpose |
|-------------|---------|
| `InformationExtractionSkill` | Map-Reduce LLM extraction over paper fragments. |
| `ReproducibilityEvaluationSkill` | NeurIPS checklist evaluation (16 items). |
| `MetricsCalculationSkill` | Computes execution metrics and red flags. |
| `MetadataAggregationSkill` | Aggregates all results into the final audit dict. |
| `ThematicCoverageSkill` | Extracts subtopics and technical areas. |
| `QueryGenerationSkill` | Generates Semantic Scholar search queries. |
| `SemanticScholarSearchSkill` | Performs bibliographic search. |
| `CoverageGapAnalysisSkill` | Identifies missing bibliographic subtopics. |
| `CrossValidationSkill` | Validates paper citations against SOTA. |
| `LimitationsQualityDetectionSkill` | Regex-based detection of limitations quality. |
| `SoftwareVersionDetectionSkill` | Regex-based detection of software versions. |
| `HardwareDetailDetectionSkill` | Regex-based detection of hardware details. |
| `ConversationalResponseSkill` | Chatbot response generation. |
| `ContextValidationSkill` | Chatbot context validation. |
| `BaseSkill` | Abstract base for all skills. |

#### Business Rules for Exported Skills

RULE: INVALID_PAPER_GATE
- TRIGGER: After REDUCE phase of `InformationExtractionSkill.execute`
- CONDITION: `extracted_info.get('paper_type', '').startswith('INVALID')`
- ACTION IF TRUE: Return `invalid_paper: True` — halts further processing

---

### Non-Exported Skills

| Skill Class | Purpose |
|-------------|---------|
| `HybridHyperparameterExtractionSkill` | RAG-based extraction using ChromaDB + Gemini Embeddings. |
| `ChecklistVerificationSkill` | Strict second-pass verification (Auditor 2) for up to 8 items. |
| `HyperparameterDetectionSkill` | Regex-based detection of optimization parameters. |
| `DataAvailabilityDetectionSkill` | Regex detection of data access and DOIs. |
| `CodeAvailabilityDetectionSkill` | Regex detection of code repositories and GitHub. |
| `StatisticsDetectionSkill` | Regex detection of confidence intervals and significance. |
| `EnvironmentalImpactDetectionSkill` | Regex detection of carbon footprint and energy usage. |
| `LicenseDetectionSkill` | Regex detection of dataset licenses. |

---

## frontend Module

**Source cluster:** `cluster_frontend_01`

### Entry Point
`frontend/app.py`: Main Streamlit application orchestrator.

### UI Components (frontend/components/)
- `file_uploader.py`: Handles PDF/TXT/MD ingestion and audit invocation.
- `audit_results.py`: Renders compliance table, metrics, and expanders.
- `chatbot.py`: Interactive Q&A interface.
- `sota_section.py`: Bibliographic analysis results.
- `gauge_chart.py`: Plotly-based quality score visualization.

### Utilities (frontend/utils/)
- `scoring.py`: Computes checklist health and pending risk items.
- `session_state.py`: Idempotent initialization of backend services.

---

## root Module (scripts, tests, scratch)

### Test Files (tests/)
- `tests/test_audit_state.py`: Verified datamodel unit tests for `AuditState` and `ExtractedInfo`.
- `test_skills_integration.py`: Verifies all 15 skills and 3 core services are importable and initializable.
- `test_auditor_refactor.py`: Verifies `PaperAuditor` initialization and prompt logic.
- `tests/test_rag_logical_splitter.py`: Logic tests for RAG chunking.

### Production Utility Scripts (root level)
- `md_to_pdf.py`: Markdown-to-PDF conversion via `reportlab`.
- `pdf_to_md.py`: PDF-to-Markdown conversion via `pymupdf4llm`.
- `create_test_pdf.py`: Synthetic paper generator for stress-testing.
- `list_models.py`: Utility to list available Gemini models.
