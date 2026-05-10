# Module Index
<!-- Source: module_index_writer | Extractions: extracted_backend_core_01.md, extracted_backend_skills_01.md, extracted_frontend_01.md, extracted_root_tests_scratch_01.md | Cross-refs: cross_ref_resolution_cross_ref_root_to_backend.md, cross_ref_resolution_cross_ref_root_to_frontend.md -->

---

## Module Inventory Overview

### Summary Table

| Module | Source Cluster | File Count | Paths | Purpose Summary | Source |
|--------|---------------|------------|-------|-----------------|--------|
| `backend_core` | `cluster_backend_core_01` | 12 | `backend/` (common/, services/, utils/) | Core LLM infrastructure: Google Gemini client with retry/backoff, 6-phase audit pipeline orchestrator (PaperAuditor), chatbot service (PaperChatbot/Chatbot alias), SOTA analyzer (SotaAnalyzer), PDF-to-Markdown chunked converter, centralized prompts (6 templates), config constants, and colored logging. | [extracted_backend_core_01.md § 1. File Index] |
| `backend_skills` | `cluster_backend_skills_01` | 7 | `backend/skills/` | Skill layer: 15 exported symbols covering auditor skills (extraction/evaluation/metrics/aggregation), chatbot skills (conversational response, context validation), SOTA skills (thematic coverage, query generation, Semantic Scholar search, gap analysis, cross-validation), regex detection skills (limitations, software versions, hardware details), plus non-exported skills (HybridHyperparameterExtractionSkill, ChecklistVerificationSkill, 9 regex detection skills). | [extracted_backend_skills_01.md § 1. Skill Registry] |
| `frontend` | `cluster_frontend_01` | 14 | `frontend/` (app.py, config.py, components/, styles/, utils/) | Streamlit single-page application: page config/styles/session-state initialization, file upload (PDF/TXT/MD), backend audit invocation, audit results rendering (compliance table, metrics, expanders), SOTA analysis section, chatbot interface, downloadable Markdown report. | [extracted_frontend_01.md § 1. File Index] |
| `root` | `cluster_root_tests_scratch_01` | 21 | root level + tests/ + scratch/ + backend/scratch/ | CLI utility scripts (md_to_pdf, pdf_to_md, create_test_pdf, list_models), legacy root app.py entry point, integration/unit test files (test_auditor_refactor, test_imports, test_skills_integration, tests/test_audit_state, tests/test_rag_*, tests/test_section_splitter), and exploration/scratch scripts. | [extracted_root_tests_scratch_01.md § 1. File Index] |

### Cross-Module Dependency Graph

**Directed dependency summary:**

| Dependent | Depends On | Mechanism | Source |
|-----------|-----------|-----------|--------|
| `frontend` → `backend_core` | `PaperAuditor`, `PaperChatbot`, `SotaAnalyzer`, `convert_pdf_to_markdown` | `st.session_state.auditor`, `st.session_state.chatbot`, `st.session_state.sota_analyzer` instantiated in `frontend/utils/session_state.py`; `convert_pdf_to_markdown` called in `frontend/components/file_uploader.py` | [extracted_frontend_01.md § 3. Session State]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_027] |
| `backend_skills` → `backend_core` | `LLMClient`, `get_logger`, prompt templates (`get_extraction_prompt`, `get_map_extraction_prompt`, `get_reduce_extraction_prompt`, `get_evaluation_prompt`, `get_verification_prompt`), config constants (`EMBEDDING_MODEL_NAME`, `EVALUATION_MODEL_NAME`, `REDUCE_MODEL_NAME`) | Direct Python import from `backend.common.llm_client`, `backend.common.config`, `backend.common.prompts`, `backend.utils.logger` | [extracted_backend_skills_01.md § 3.4 LLM Prompt Templates]; [extracted_backend_core_01.md § 3.1 LLM Client] |
| `backend_core` (services) → `backend_skills` | `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ChecklistVerificationSkill`, `HybridHyperparameterExtractionSkill` | Instantiated in `PaperAuditor.__init__`; `ConversationalResponseSkill`, `ContextValidationSkill` in `PaperChatbot.__init__`; 5 SOTA skills in `SotaAnalyzer.__init__` | [extracted_backend_core_01.md § 3.2, 3.3, 3.5]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_009] |
| `root` (tests) → `backend_core` | `PaperAuditor`, `LLMClient`, `get_extraction_prompt`, `get_evaluation_prompt`, `get_logger`, config constants | Test files import and instantiate backend_core classes directly | [extracted_root_tests_scratch_01.md § 8]; [cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY] |
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
| `backend/common/prompts.py` | `get_extraction_prompt` | Function | `(paper_text: str, red_flags: dict) -> str`. Full-paper extraction prompt for `InformationExtractionSkill` (used in single-fragment fallback). | [extracted_backend_core_01.md § 2.2 Prompt 1] |
| `backend/common/prompts.py` | `get_map_extraction_prompt` | Function | `(fragment_text: str) -> str`. Per-fragment extraction prompt for MAP phase of `InformationExtractionSkill`. | [extracted_backend_core_01.md § 2.2 Prompt 2] |
| `backend/common/prompts.py` | `get_reduce_extraction_prompt` | Function | `(map_results: list) -> str`. Consolidation prompt for REDUCE phase; `map_results` serialized via `json.dumps(map_results, indent=2)`. | [extracted_backend_core_01.md § 2.2 Prompt 3] |
| `backend/common/prompts.py` | `get_evaluation_signals` | Function | `(extracted_info: dict) -> dict`. NOT a prompt template; computes a `signals` dict (keys: `reproducibility`, `open_access`, `statistics`, `compute_resource`, `licenses`, `crowdsourcing`) consumed by `get_evaluation_prompt`. | [extracted_backend_core_01.md § 2.2 Prompt 4] |
| `backend/common/prompts.py` | `get_evaluation_prompt` | Function | `(extracted_info: dict, red_flags: dict) -> str`. NeurIPS Area Chair evaluation prompt for all 16 checklist items; `extracted_info` serialized via `json.dumps(..., indent=2, ensure_ascii=False)`. | [extracted_backend_core_01.md § 2.2 Prompt 5] |
| `backend/common/prompts.py` | `get_verification_prompt` | Function | `(item_key: str, item_data: dict, paper_context: str) -> str`. Strict verification prompt for `ChecklistVerificationSkill`; checks for false positives and false negatives per checklist item. | [extracted_backend_core_01.md § 2.2 Prompt 6] |
| `backend/common/config.py` | `GOOGLE_API_KEY` | Constant (`str \| None`) | Loaded from env var `"GOOGLE_API_KEY"` via `load_dotenv()`. No default. | [extracted_backend_core_01.md § 2.1 API Keys] |
| `backend/common/config.py` | `SEMANTIC_SCHOLAR_API_KEY` | Constant (`str \| None`) | Loaded from env var `"SEMANTIC_SCHOLAR_API_KEY"`. No default. | [extracted_backend_core_01.md § 2.1 API Keys] |
| `backend/common/config.py` | `EMBEDDING_MODEL_NAME` | Constant (`str`) | `"gemini-embedding-2"`. Used for RAG embeddings. | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `MAP_MODEL_NAME` | Constant (`str`) | `"gemini-3.1-flash-lite-preview"`. Triage and Map phase extraction. | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `REDUCE_MODEL_NAME` | Constant (`str`) | `"gemini-3.1-flash-lite-preview"`. Orchestration and Consolidation (Reduce phase). | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `EXTRACTION_MODEL_NAME` | Constant (`str`) | `"gemini-3.1-flash-lite-preview"`. Initial extraction (General Analysis). | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `EVALUATION_MODEL_NAME` | Constant (`str`) | `"gemini-3.1-flash-lite-preview"`. Final evaluation (Senior Area Chair). | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `VERIFICATION_MODEL_NAME` | Constant (`str`) | `"gemini-3.1-flash-lite-preview"`. Strict verification (Auditor 2). | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `MODEL_NAME` | Constant (`str`) | `= EXTRACTION_MODEL_NAME` (alias). Default model for `LLMClient`. | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `RAG_MODEL_NAME` | Constant (`str`) | `= MAP_MODEL_NAME` (alias). Default model for RAG. | [extracted_backend_core_01.md § 2.1 Model Name Constants] |
| `backend/common/config.py` | `AUDIT_TEMPERATURE` | Constant (`float`) | `0.0`. Used in `AUDIT_CONFIG`. | [extracted_backend_core_01.md § 2.1 Temperature Constants] |
| `backend/common/config.py` | `CHAT_TEMPERATURE` | Constant (`float`) | `0.2`. Used in `CHAT_CONFIG`. | [extracted_backend_core_01.md § 2.1 Temperature Constants] |
| `backend/common/config.py` | `SOTA_TEMPERATURE` | Constant (`float`) | `0.1`. Used in `SOTA_CONFIG`. | [extracted_backend_core_01.md § 2.1 Temperature Constants] |
| `backend/common/config.py` | `AUDIT_CONFIG` | Constant (`dict`) | `{"response_mime_type": "application/json", "temperature": 0.0, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384}`. Used by all 5 PaperAuditor LLMClient instances. | [extracted_backend_core_01.md § 2.1 Generation Config] |
| `backend/common/config.py` | `CHAT_CONFIG` | Constant (`dict`) | `{"temperature": 0.2}`. Used by PaperChatbot. | [extracted_backend_core_01.md § 2.1 Generation Config] |
| `backend/common/config.py` | `SOTA_CONFIG` | Constant (`dict`) | `{"response_mime_type": "application/json", "temperature": 0.1}`. Used by SotaAnalyzer. | [extracted_backend_core_01.md § 2.1 Generation Config] |
| `backend/common/config.py` | `SEMANTIC_SCHOLAR_BASE_URL` | Constant (`str`) | `"https://api.semanticscholar.org/graph/v1/paper/search"` | [extracted_backend_core_01.md § 2.1 Semantic Scholar Constants] |
| `backend/common/config.py` | `SEMANTIC_SCHOLAR_YEAR_RANGE` | Constant (`str`) | `"2023-2026"` | [extracted_backend_core_01.md § 2.1 Semantic Scholar Constants] |
| `backend/common/config.py` | `SEMANTIC_SCHOLAR_LIMIT` | Constant (`int`) | `5` (results per query) | [extracted_backend_core_01.md § 2.1 Semantic Scholar Constants] |
| `backend/common/config.py` | `SEMANTIC_SCHOLAR_FIELDS` | Constant (`str`) | `"paperId,title,authors,year,citationCount,abstract,url"` | [extracted_backend_core_01.md § 2.1 Semantic Scholar Constants] |
| `backend/common/config.py` | `CleanNetworkLogs` | Class | `logging.Filter` subclass; `filter(self, record)` suppresses HuggingFace HEAD/GET log lines. | [extracted_backend_core_01.md § 2.1 CleanNetworkLogs filter] |
| `backend/utils/logger.py` | `get_logger` | Function | `(name: str) -> logging.Logger`. Returns a colored StreamHandler logger at `INFO` level. Format: `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` with datefmt `'%H:%M:%S'`. Propagation disabled. Deduplicates handlers. | [extracted_backend_core_01.md § 6.1 Logger Configuration] |
| `backend/utils/logger.py` | `Colors` | Class | ANSI color code constants: `BLUE="\033[94m"`, `CYAN="\033[96m"`, `GREEN="\033[92m"`, `YELLOW="\033[93m"`, `RED="\033[91m"`, `MAGENTA="\033[95m"`, `BOLD="\033[1m"`, `RESET="\033[0m"`. | [extracted_backend_core_01.md § 2.3 Other Constants — logger.py] |
| `backend/utils/logger.py` | `ColoredFormatter` | Class | `logging.Formatter` subclass. `format(self, record)`: routes "HTTP Request" messages to CYAN; other messages use level-based color (`DEBUG→BLUE`, `INFO→GREEN`, `WARNING→YELLOW`, `ERROR→RED`, `CRITICAL→BOLD+RED`). | [extracted_backend_core_01.md § 6.1 Logger Configuration] |

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

| Package | How Used | Source |
|---------|----------|--------|
| `google-generativeai` | `genai.Client` for LLM generation and embedding calls; `genai.Client.models.generate_content`, `models.embed_content` | [extracted_backend_core_01.md § 3.1]; [extracted_root_tests_scratch_01.md § 2] |
| `docling` | `DocumentConverter` for PDF-to-Markdown chunked conversion in `pdf_parser.py`; `PdfPipelineOptions`, `PdfFormatOption`, `InputFormat` | [extracted_backend_core_01.md § 4.1 PDF Parse Pipeline] |
| `python-dotenv` | `load_dotenv()` at `config.py:27` loads `GOOGLE_API_KEY` and `SEMANTIC_SCHOLAR_API_KEY` from `.env` | [extracted_backend_core_01.md § 2.1 API Keys] |
| `pydantic` | `BaseModel` used in `rag_extraction_skill.py` for `Hyperparameters` Pydantic model; used as `response_schema` in fallback REDUCE call | [extracted_backend_skills_01.md § 4.1]; [extracted_root_tests_scratch_01.md § 2] |
| `pypdf` | `PdfReader` and `PdfWriter` for per-chunk PDF splitting in `pdf_parser.py` | [extracted_backend_core_01.md § 4.1 PDF Parse Pipeline] |
| `chromadb` | In-memory `chromadb.Client()` for RAG vector store in `HybridHyperparameterExtractionSkill`; collection `"paper_chunks"` created/deleted per execution | [extracted_backend_skills_01.md § 4.3 Step 3] |
| `httpx` | HTTP POST to Google embedding batch API in `HybridHyperparameterExtractionSkill` (bypasses SDK) | [extracted_backend_skills_01.md § 4.3 Step 2] |
| `requests` | HTTP GET to Semantic Scholar API in `SemanticScholarSearchSkill` | [extracted_backend_skills_01.md § 6.2 SemanticScholarSearchSkill] |
| `torch` | `torch.cuda.is_available()` for GPU detection in `pdf_parser.py` (informational only) | [extracted_backend_core_01.md § 4.1 Step 1] |
| `streamlit` | Imported inline in `LLMClient.generate` for `st.toast(...)` retry notification; inner try/except swallows `Exception` in non-Streamlit environments | [extracted_backend_core_01.md § 3.1 LLM Client] |

---

## backend_skills Module

**Source cluster:** `cluster_backend_skills_01`
**Extraction file:** `extracted_backend_skills_01.md`

### Exported Skills (15 symbols in `__init__.py`)

`SOURCE: __init__.py:36` — `__all__` list at lines 36–52 exports exactly **15** symbols (corrected from earlier draft of 14 — see PURGE LOG in extraction).

| Skill Class | Base Class | Origin Module | Purpose | Key Methods/Attributes (from extraction) | Source |
|-------------|-----------|---------------|---------|------------------------------------------|--------|
| `BaseSkill` | `ABC` | `backend.skills.base_skill` | Abstract base for all skills. Declares `execute(self, context: Dict[str, Any]) -> Dict[str, Any]` as abstract method. | `__init__(llm_client, config)`, `validate_context(context, required_keys) -> bool`, `log_execution(message, level="info")` | [extracted_backend_skills_01.md § 2. Base Skill Interface] |
| `InformationExtractionSkill` | `BaseSkill` | `backend.skills.auditor_skills` | Map-Reduce LLM extraction over paper fragments. MAP: sections-based fragmentation (max 4 fragments); per-fragment LLM call to `get_map_extraction_prompt`; `time.sleep(2)` between fragments. REDUCE: consolidation via `get_reduce_extraction_prompt`; fallback to `llm_client.client.models.generate_content`. Post-REDUCE: invalid-paper gate, `thought_process` and `context_mapping` field normalization. | `execute(context: {'paper_text': str}) -> {'extracted_info', 'invalid_paper', 'map_steps', 'reduce_step'}` | [extracted_backend_skills_01.md § 3.2 InformationExtractionSkill] |
| `ReproducibilityEvaluationSkill` | `BaseSkill` | `backend.skills.auditor_skills` | NeurIPS checklist evaluation (16 items: Yes/No/N/A + evidence/justification). Calls `get_evaluation_signals` then `get_evaluation_prompt`. JSON repair: trailing-comma regex on `JSONDecodeError`. HTTP 503/UNAVAILABLE → user-facing error message. | `execute(context: {'extracted_info', 'red_flags'}) -> {'evaluation', 'evaluation_signals'}` | [extracted_backend_skills_01.md § 3.2 ReproducibilityEvaluationSkill] |
| `MetricsCalculationSkill` | `BaseSkill` | `backend.skills.auditor_skills` | Computes `tiempo_segundos`, `caracteres_leidos`, `red_flags_detectadas` from context. `critical_flags` count excludes keys starting with `"tiene_"`, `"menciona_"`, `"_"`, `"cantidad_"`, `"puntos_"`. | `execute(context: {'paper_text', 'red_flags', 'execution_time'}) -> {'metrics': {'tiempo_segundos', 'caracteres_leidos', 'red_flags_detectadas'}}` | [extracted_backend_skills_01.md § 3.2 MetricsCalculationSkill] |
| `MetadataAggregationSkill` | `BaseSkill` | `backend.skills.auditor_skills` | Aggregates 23 fields from context into final audit result dict. Maps all 16 NeurIPS checklist items from `evaluation`, plus `informacion_extraida`, `red_flags`, `metricas`, `general_analysis_map`, `general_analysis_reduce`, `hybrid_triage_fragments`, `evaluation_signals`. | `execute(context) -> flat dict with 23 keys` | [extracted_backend_skills_01.md § 3.2 MetadataAggregationSkill] |
| `ConversationalResponseSkill` | `BaseSkill` | `backend.skills.chatbot_skills` | Generates chatbot response using LLM given paper text, question, and conversation history. | [GAP: exact method signature and prompt for ConversationalResponseSkill not extracted in detail] | [extracted_backend_skills_01.md § 1.1 Exported Symbols] |
| `ContextValidationSkill` | `BaseSkill` | `backend.skills.chatbot_skills` | Validates chatbot context (no LLM client required). Returns `{'is_valid': bool, 'error': str}` on failure. | [GAP: exact validation logic for ContextValidationSkill not extracted in detail] | [extracted_backend_skills_01.md § 1.1 Exported Symbols] |
| `ThematicCoverageSkill` | `BaseSkill` | `backend.skills.sota_skills` | Extracts subtemas, areas_tecnicas, año_paper from paper text (first 15000 + last 5000 chars). LLM call returns JSON `{"subtemas": list, "areas_tecnicas": list, "año_paper": int\|null}`. | `execute(context: {'paper_text'}) -> {'thematic_data': {'subtemas', 'areas_tecnicas', 'año_paper'}}` | [extracted_backend_skills_01.md § 6.2 ThematicCoverageSkill] |
| `QueryGenerationSkill` | `BaseSkill` | `backend.skills.sota_skills` | Generates 3 Semantic Scholar search queries in English (2 general + 1 specific) from paper text (first 8000 chars) and thematic data. | `execute(context: {'paper_text', 'thematic_data'}) -> {'search_queries': ['query1', 'query2', 'query3']}` | [extracted_backend_skills_01.md § 6.2 QueryGenerationSkill] |
| `SemanticScholarSearchSkill` | `BaseSkill` | `backend.skills.sota_skills` | HTTP GET to Semantic Scholar API (`SEMANTIC_SCHOLAR_BASE_URL`) for each query; 0.5s sleep between queries; HTTP 429 → 2s sleep; deduplication by `paperId`; sorts by `citationCount` desc; returns top 10. No LLM client required. | `execute(context: {'search_queries'}) -> {'sota_papers': list}` (max 10, deduplicated) | [extracted_backend_skills_01.md § 6.2 SemanticScholarSearchSkill]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_018] |
| `CoverageGapAnalysisSkill` | `BaseSkill` | `backend.skills.sota_skills` | Analyzes intro (first 5000 chars) and references (last 10000 chars) to identify subtemas with poor bibliographic coverage. LLM returns `{"areas_debiles": [{"subtema", "diagnostico"}]}`. | `execute(context: {'paper_text', 'thematic_data'}) -> {'coverage_gaps': {'areas_debiles': list}}` | [extracted_backend_skills_01.md § 6.2 CoverageGapAnalysisSkill] |
| `CrossValidationSkill` | `BaseSkill` | `backend.skills.sota_skills` | Cross-validates paper citations against Semantic Scholar results; returns final SOTA validation result with `papers_omitidos`, `cobertura_tematica`, `conclusion_sota` plus `metadata`. If `sota_papers` is empty, returns pre-built result without LLM call. | `execute(context: {'paper_text', 'sota_papers', 'thematic_data', 'coverage_gaps'}) -> validation_result dict` | [extracted_backend_skills_01.md § 6.2 CrossValidationSkill] |
| `LimitationsQualityDetectionSkill` | `BaseSkill` | `backend.skills.regex_detection_skills` | Regex-based detection of limitations section quality. Exported; negation-aware. | `execute(context: {'paper_text'}) -> {'limitations_flags': {'tiene_seccion_limitaciones', 'limitaciones_vagas', 'puntos_especificos_limitaciones'}}` | [extracted_backend_skills_01.md § 5.1, 5.3]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_017] |
| `SoftwareVersionDetectionSkill` | `BaseSkill` | `backend.skills.regex_detection_skills` | Regex-based detection of software version mentions (PyTorch/TensorFlow/JAX/Python/CUDA/etc.). Exported; negation-aware. | `execute(context: {'paper_text'}) -> {'software_flags': {'tiene_versiones_software', 'cantidad_versiones'}}` | [extracted_backend_skills_01.md § 5.1, 5.3]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_017] |
| `HardwareDetailDetectionSkill` | `BaseSkill` | `backend.skills.regex_detection_skills` | Regex-based detection of hardware details (GPU model, count, memory, training time). Exported; negation-aware. | `execute(context: {'paper_text'}) -> {'hardware_detail_flags': {'tiene_gpu_model', 'tiene_gpu_count', 'tiene_gpu_memory', 'tiene_training_time'}}` | [extracted_backend_skills_01.md § 5.1, 5.3]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_017] |

#### Business Rules for Exported Skills

RULE: INVALID_PAPER_GATE
- TRIGGER: After REDUCE phase of `InformationExtractionSkill.execute`
- CONDITION: `extracted_info.get('paper_type', '').startswith('INVALID')`
- ACTION IF TRUE: Return `{'extracted_info': extracted_info, 'invalid_paper': True, 'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')}` — halts further processing
- ACTION IF FALSE: Continue to post-REDUCE field validation
- SOURCE: `auditor_skills.py:152`

RULE: CHECKLIST_ITEM_SELECTION (for ChecklistVerificationSkill — not exported, see below)
- TRIGGER: `ChecklistVerificationSkill.execute` call
- CONDITION: Item is in `priority_items` list (`['claims', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiments_compute_resource', 'experiment_statistical_significance', 'licenses', 'declaration_llm_usage']`) AND exists in `evaluation` AND value is dict
- ACTION IF TRUE: Item added to `to_check`; fill remaining slots (to reach 8) with `answer in ['No', 'N/A']` items
- SOURCE: `auditor_skills.py:340`

---

### Non-Exported Skills

| Skill Class | Reason Not Exported | Purpose | Source |
|-------------|--------------------|---------| -------|
| `CompositeSkill` | Absent from `__init__.py`; not imported in `__init__.py`; defined at `base_skill.py:83` | Chains multiple skills sequentially, accumulating context. `execute(context)` copies initial context, iterates over `self.skills` list; per skill: calls `skill.execute(accumulated_context)` and updates accumulated context with result; on exception: logs error at `level="error"` and records `error_{skill_name}` key, then continues to next skill. | [base_skill.py:83-124] |
| `HybridHyperparameterExtractionSkill` | Absent from `__init__.py` | RAG-based hyperparameter extraction using ChromaDB + Google embedding API + Pydantic schema. 8-step pipeline: logical chunking (split on `\n\n+`), batch embedding (15 chunks/batch, 15s sleep between batches), ChromaDB population, 13-query RAG retrieval, relevance scoring (piecewise distance→0-100), MAP LLM per-chunk extraction, REDUCE consolidation, regex cleaning. Returns `{'extracted_hyperparameters_hybrid': dict, 'triage_fragments': list}`. | [extracted_backend_skills_01.md § 4. RAG Extraction Skill] |
| `ChecklistVerificationSkill` | Absent from `__init__.py`; defined at `auditor_skills.py:319` | Strict second-pass verification of up to 8 checklist items (priority items + `No`/`N/A` items). Per-item: calls `get_verification_prompt`, parses response, overwrites `evaluation[item_key]` with verified result including `was_refined` flag. | [extracted_backend_skills_01.md § 3.2 ChecklistVerificationSkill] |
| `HyperparameterDetectionSkill` | Absent from `__init__.py` | Regex-based detection with table-first search priority. Patterns for: `optimizer`, `learning_rate`, `batch_size`, `epochs`, `warmup`, `weight_decay`, `betas`, `epsilon`, `vague`. Returns `{'hyperparameter_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `DataAvailabilityDetectionSkill` | Absent from `__init__.py` | Regex detection: `datos_propietarios`, `datos_sin_acceso`, `tiene_doi_datos`, `cannot_release_data`. Returns `{'data_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `CodeAvailabilityDetectionSkill` | Absent from `__init__.py` | Regex detection: `codigo_propietario`, `sin_repositorio`, `tiene_github`, `cannot_release_code`. Returns `{'code_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `StatisticsDetectionSkill` | Absent from `__init__.py` | Regex detection: `sin_intervalos_confianza`, `sin_significancia`, `sin_multiple_runs`. Returns `{'statistics_flags': results}`. Table-search priority applies. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `EnvironmentalImpactDetectionSkill` | Absent from `__init__.py` | Regex detection: `tiene_carbon_footprint`, `tiene_energy_consumption`, `tiene_pue`. Returns `{'environmental_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `ProblematicPhrasesDetectionSkill` | Absent from `__init__.py` | Regex detection: `competitive_concerns`, `cannot_release`, `remain_confidential`. Returns `{'problematic_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `LlmUsageDetectionSkill` | Absent from `__init__.py` | Regex detection: `usa_llm_como_herramienta`. Returns `{'llm_usage_flags': {'usa_llm_como_herramienta': bool}}`. | [extracted_backend_skills_01.md § 5.2, 5.3] |
| `CrowdsourcingDetectionSkill` | Absent from `__init__.py` | Regex detection with negation gate: `usa_crowdsourcing`, `usa_datasets_humanos`, `sin_compensacion_mencionada`. Negation gate (`NEGATION_CROWD` pattern match) suppresses active-crowdsourcing scan. Returns `{'crowdsourcing_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3, 5.4]; [extracted_root_tests_scratch_01.md § RULE-18] |
| `LicenseDetectionSkill` | Absent from `__init__.py` | Regex detection: `menciona_licencia` (EXPLICIT_LICENSE pattern), `usa_datasets_conocidos` (KNOWN_DATASETS pattern), `posible_licencia_faltante` = `usa_datasets_conocidos AND NOT menciona_licencia`. Returns `{'license_flags': results}`. | [extracted_backend_skills_01.md § 5.2, 5.3, 5.4]; [extracted_root_tests_scratch_01.md § RULE-19] |

**Non-exported helper infrastructure in `regex_detection_skills.py`:**

| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| `NEGATION_WINDOW` | `int = 60` | Number of preceding characters checked for negation context | [extracted_backend_skills_01.md § 5.2 Module-level] |
| `NEGATION_PATTERNS` | `re.Pattern` (IGNORECASE) | Compiled regex detecting negation phrases in 60-char preceding window | [extracted_backend_skills_01.md § 5.2 Module-level] |
| `_is_negated(text, match_start)` | Function | Returns `True` if `NEGATION_PATTERNS` matches in `text[max(0, match_start-60):match_start]` | [extracted_backend_skills_01.md § 5.2 Module-level] |
| `_search_with_negation(pattern, text, flags)` | Function | Wrapper around `re.search` that discards matches where `_is_negated` is True | [extracted_backend_skills_01.md § 5.2 Module-level] |
| `TableExtractionHelper` | Plain class (not BaseSkill) | `extract_tables(text)`: extracts table content via 3 patterns (`Table N:`, pipe tables `\|...\|`, tab-separated tables) for table-first search in `HyperparameterDetectionSkill` and `StatisticsDetectionSkill` | [extracted_backend_skills_01.md § 5.2 TableExtractionHelper] |

### External Dependencies (backend_skills)

| Package | How Used | Source |
|---------|----------|--------|
| `backend_core` (internal) | `LLMClient` (all LLM-using skills), prompt templates from `backend.common.prompts`, config constants from `backend.common.config` (`EMBEDDING_MODEL_NAME`, `EVALUATION_MODEL_NAME`, `REDUCE_MODEL_NAME`), `get_logger` | [extracted_backend_skills_01.md § 3.4 LLM Prompt Templates]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_010, g_012, g_019, g_023] |
| `pydantic` | `BaseModel` for `Hyperparameters` schema in `HybridHyperparameterExtractionSkill`; used as `response_schema` in REDUCE fallback | [extracted_backend_skills_01.md § 4.1 Pydantic model] |
| `chromadb` | In-memory vector store for RAG in `HybridHyperparameterExtractionSkill` | [extracted_backend_skills_01.md § 4.3 Step 3] |
| `httpx` | Batch embedding API calls in `HybridHyperparameterExtractionSkill` | [extracted_backend_skills_01.md § 4.3 Step 2] |
| `requests` | Semantic Scholar HTTP GET in `SemanticScholarSearchSkill` | [extracted_backend_skills_01.md § 6.2 SemanticScholarSearchSkill] |
| `langchain-text-splitters` (or equivalent) | `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)` as fallback chunker in `InformationExtractionSkill` when no Markdown sections detected | [extracted_backend_skills_01.md § 3.2 InformationExtractionSkill — Phase MAP] |
| `re`, `json`, `time`, `os` | Standard library; used throughout regex detection skills, JSON parsing, inter-fragment sleep | [extracted_backend_skills_01.md § 3.2, 4.3, 5] |

---

## frontend Module

**Source cluster:** `cluster_frontend_01`
**Extraction file:** `extracted_frontend_01.md`

### Entry Point

| File | Purpose | Source |
|------|---------|--------|
| `frontend/app.py` | Main Streamlit application entry point (77 lines). Sets page config first (`st.set_page_config(page_title="NeurIPS 2026 Checklist Auditor", layout="wide", page_icon="🔬")`). Suppresses environment noise (TRANSFORMERS_VERBOSITY, TOKENIZERS_PARALLELISM, ANONYMIZED_TELEMETRY, OTEL_SDK_DISABLED, warnings). Orchestrates: `apply_custom_styles()`, `initialize_session_state()`, file uploader, audit invocation, result rendering, SOTA, chatbot, report download, sidebar. | [extracted_frontend_01.md § 4.2 Top-level rendering order] |

[NOTE: The root-level `app.py` (74 lines, page_title `"Nature Auditor Pro"`) is a legacy entry point — see Section 5 (root module). The canonical entry point for the modular frontend is `frontend/app.py`. Cross-ref: `extracted_root_tests_scratch_01.md § 3. Application Entry Point`.]

**Rendering order in `frontend/app.py`:**
1. `st.set_page_config(...)` — SOURCE: `app.py:6-10`
2. `apply_custom_styles()` — SOURCE: `app.py:21`
3. `initialize_session_state()` — SOURCE: `app.py:22`
4. `st.title(TITLE)` — SOURCE: `app.py:25`
5. `st.markdown("---")` — SOURCE: `app.py:26`
6. "Limpiar y subir nuevo archivo" button — SOURCE: `app.py:29-32`
7. `st.file_uploader(...)` accepting `["pdf", "txt", "md"]` — SOURCE: `app.py:34`
8. If `uploaded_file`: `process_uploaded_file()`, branch on resultado, `render_audit_results()`, `render_sota_analysis()`, `render_chatbot()`, download button — SOURCE: `app.py:37-65`
9. Sidebar: `st.image(SIDEBAR_IMAGE, width=150)`, `st.markdown("### Sobre el TFG")`, `st.write(SIDEBAR_DESCRIPTION)` — SOURCE: `app.py:73-76`

---

### UI Components (frontend/components/)

| File | Component Name | Streamlit Widgets Used | Purpose | Screens/Views It Renders | Source |
|------|---------------|----------------------|---------|--------------------------|--------|
| `frontend/components/file_uploader.py` | `process_uploaded_file` | `st.spinner`, `st.status`, `st.success`, `st.error` | Handles file upload (PDF/TXT/MD), MD extraction (via `convert_pdf_to_markdown` for PDF or `open(..., 'r', encoding='utf-8').read()` for TXT/MD), deduplication by MD5 hash, auditor invocation. Writes/reads `st.session_state`. | Upload spinner, status widget during audit, success/error messages | [extracted_frontend_01.md § 5.1]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_004] |
| `frontend/components/audit_results.py` | `render_audit_results` | `st.success`, `st.header`, `st.metric`, `st.subheader`, `st.caption`, `st.html`, `st.expander`, `st.info`, `st.json`, `st.warning`, `st.markdown`, `st.code` | Renders full audit results page: success banner, verdict block (valid/risk), 4-column metrics row, RAG Ficha Técnica, compliance table (`_build_table_html`), 3 expanders (Analysis Pipeline, Hybrid Extraction, Evaluation). Returns `health` dict. | Audit results page with verdict, metrics, compliance table, 3 expanders | [extracted_frontend_01.md § 5.2]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_005] |
| `frontend/components/chatbot.py` | `render_chatbot` | `st.markdown`, `st.header`, `st.caption`, `st.chat_message`, `st.text_input` (key=`"chat_input"`), `st.button` (key=`"send_button"`), `st.spinner`, `st.rerun` | Renders interactive chat section. Reads/writes `st.session_state.messages`. Calls `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)`. | Chat interface with message history, text input, send button | [extracted_frontend_01.md § 5.3]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_007] |
| `frontend/components/gauge_chart.py` | `create_gauge_chart` | Plotly `Figure` (gauge indicator) — no Streamlit widgets directly | Pure function `create_gauge_chart(score) -> plotly.Figure`. Creates gauge chart with NeurIPS quality tiers: `[87.5,100]→"Strong Accept"`, `[75,87.5)→"Accept"`, `[62.5,75)→"Borderline"`, `[50,62.5)→"Weak Reject"`, `[25,50)→"Reject"`, `[0,25)→"Strong Reject"`. Threshold line at 62.5 (red, width 4). | Gauge chart widget (rendered by caller via `st.plotly_chart`) | [extracted_frontend_01.md § 2.4 NeurIPS Quality Score Tiers] |
| `frontend/components/sota_section.py` | `render_sota_analysis` | `st.markdown`, `st.subheader`, `st.button`, `st.spinner`, Streamlit dataframe/table widgets | Renders SOTA analysis section. On button press: calls `st.session_state.sota_analyzer.analyze_sota(md_text)`, renders conclusion, papers dataframe, missing-paper recommendations via `_render_missing_papers`. Does NOT write to `st.session_state` directly. | SOTA analysis section with button, spinner, papers table | [extracted_frontend_01.md § 5.5]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_007] |

**COMPLETENESS CHECK:** All 6 components verified present in extraction:
- `audit_results.py` ✓ — [extracted_frontend_01.md § 5.2]
- `chatbot.py` ✓ — [extracted_frontend_01.md § 5.3]
- `file_uploader.py` ✓ — [extracted_frontend_01.md § 5.1]
- `gauge_chart.py` ✓ — [extracted_frontend_01.md § 2.4]
- `sota_section.py` ✓ — [extracted_frontend_01.md § 5.5]
- `custom_css.py` ✓ — [extracted_frontend_01.md § 6]

#### process_uploaded_file — Field Details

**Signature:** `process_uploaded_file(uploaded_file) -> (md_text: str, resultado: dict)`
SOURCE: `file_uploader.py:6`

**Deduplication condition (new file detected when ANY is true):**
1. `"archivo_actual" not in st.session_state`
2. `st.session_state.archivo_actual != uploaded_file.name`
3. `st.session_state.get('file_hash') != hashlib.md5(uploaded_file.getvalue()).hexdigest()`

SOURCE: `file_uploader.py:15-17`

**Session state writes (new file only):**
- `st.session_state.archivo_actual = uploaded_file.name` — SOURCE: `file_uploader.py:19`
- `st.session_state.file_hash = hashlib.md5(...).hexdigest()` — SOURCE: `file_uploader.py:20`
- `st.session_state.messages = []` — SOURCE: `file_uploader.py:21`
- `st.session_state.md_text = <extracted text>` — SOURCE: `file_uploader.py:35-39`
- `st.session_state.resultado = st.session_state.auditor.audit(st.session_state.md_text, status_callback=update_status)` — SOURCE: `file_uploader.py:49-52`

**Saturation error classification keywords:** `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` — SOURCE: `file_uploader.py:60`

**Accepted file extensions:** `["pdf", "txt", "md"]` — SOURCE: `app.py:34`

**Temp directory:** `os.makedirs("temp")`; writes to `temp/<filename>`; deletes after processing — SOURCE: `file_uploader.py:23-24, 94-95`

**Return:** `(st.session_state.get('md_text', ''), st.session_state.get('resultado', {}))` — SOURCE: `file_uploader.py:98-100`

#### render_audit_results — Field Details

**Signature:** `render_audit_results(resultado: dict, uploaded_file) -> dict`

Returns `health` dict from `get_checklist_health(resultado)`.

**`_build_table_html(items: list) -> str`** — SOURCE: `audit_results.py:7-87`

HTML table with columns: `#`, `Item del Checklist`, `Respuesta`, `Evidencia / Justificacion`.

Row background color rules (SOURCE: `audit_results.py:18-32`):
- `pending_justification == True` → `"#450a0a"` (deep red — Critical risk)
- `missing_evidence == True` OR `alert_msg` non-empty → `"#452e0a"` (amber/orange — Warning)
- `"yes" in answer (lower)` → `"#064e3b"` (emerald green — OK)
- All other cases → `"#111827"` (neutral dark)

Badge styles for Yes/No/N/A (SOURCE: `audit_results.py:10-16`):
- `"yes" in answer (lower)` → `background:#065f46; color:#6ee7b7; text:"Yes"`
- `"no" in answer (lower)` → `background:#7f1d1d; color:#fca5a5; text:"No"`
- else (N/A) → `background:#1e3a5f; color:#93c5fd; text:"N/A"`

**`generate_report(resultado: dict, uploaded_file, health=None) -> str`** — SOURCE: `audit_results.py:287`
[cross_ref_resolution_cross_ref_root_to_frontend.md § g_006]

Pure function (no Streamlit widgets). Returns Markdown report string. Structure:
- `# NeurIPS 2026 Checklist Audit Report`
- `**Paper:** {uploaded_file.name}`
- `**Veredicto:** {status_label}` — "Checklist Valido" or "Riesgo de Desk Reject"
- `**Items con problemas:** {pending} de {total}`
- `---`
- `## Tabla de Cumplimiento` with Markdown table: `| # | Item | Respuesta | Evidencia / Justificacion |`
- Per-item row: optional suffix `" [RIESGO: sin justificacion]"` or `" [RIESGO: sin evidencia]"`
- Footer: `_Generado por Auditor NeurIPS 2026._`

---

### Utilities (frontend/utils/)

| File | Functions/Symbols | Purpose | Source |
|------|------------------|---------|--------|
| `frontend/utils/scoring.py` | `CHECKLIST_KEYS` (list, 16 elements), `CHECKLIST_LABELS` (dict, 16 entries), `get_checklist_health(evaluation: dict) -> dict` | Defines the 16 NeurIPS checklist keys and display labels; `get_checklist_health` computes `status` ("valid"/"risk"), `pending_count`, `total`, and `items` list (one dict per key). Early-exit when evaluation is falsy returns `{"status": "risk", "items": [], "pending_count": 0, "total": 0}`. | [extracted_frontend_01.md § 2.3, § 7.1]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_013] |
| `frontend/utils/session_state.py` | `initialize_session_state() -> None` | Initializes 5 session state keys with guard `if "key" not in st.session_state` (idempotent). Keys: `resultado=None`, `auditor=PaperAuditor()`, `chatbot=PaperChatbot()`, `sota_analyzer=SotaAnalyzer()`, `messages=[]`. | [extracted_frontend_01.md § 3. Session State]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_027] |

**`get_checklist_health` — detailed return structure** (SOURCE: `scoring.py:37`):

```
RETURN: dict with keys:
  - status: str — "valid" if pending_count == 0, else "risk"  (SOURCE: scoring.py:122-123)
  - pending_count: int — count of items that triggered a risk rule  (SOURCE: scoring.py:122-126)
  - total: int — len(items); always 16 when evaluation is non-empty  (SOURCE: scoring.py:127)
  - items: list of dicts — one per CHECKLIST_KEYS entry, each with:
      - "key":                  str   — CHECKLIST_KEYS key string
      - "label":                str   — from CHECKLIST_LABELS.get(key, key)
      - "answer":               str   — stripped answer or "—" if empty
      - "evidence":             str   — evidence if present, else justification, else "—"
      - "justification":        str   — stripped justification (may be empty)
      - "is_no_justified":      bool  — normalized from raw (str "true"/"false" or bool)
      - "pending_justification": bool — True when "no" in answer AND (not is_no_justified OR not justification)
      - "missing_evidence":     bool  — True when "yes" in answer AND (not evidence AND not justification)
      - "alert_msg":            str   — risk description; special suffix for "crowdsourcing_human_subjects"
    (SOURCE: scoring.py:110-120)
```

**CHECKLIST_KEYS** (ordered list, 16 elements) — SOURCE: `scoring.py:8-15`:
```
["claims", "limitations", "theory_assumptions_proofs", "experimental_result_reproducibility",
 "open_access_data_code", "experimental_setting_details", "experiment_statistical_significance",
 "experiments_compute_resource", "code_of_ethics", "broader_impacts", "safeguards",
 "licenses", "assets", "crowdsourcing_human_subjects", "irb_approvals", "declaration_llm_usage"]
```

**CHECKLIST_LABELS** — SOURCE: `scoring.py:17-34`:
```
"claims"                              → "1. Claims"
"limitations"                         → "2. Limitations"
"theory_assumptions_proofs"           → "3. Theory, Assumptions & Proofs"
"experimental_result_reproducibility" → "4. Experimental Result Reproducibility"
"open_access_data_code"               → "5. Open Access to Data and Code"
"experimental_setting_details"        → "6. Experimental Setting / Details"
"experiment_statistical_significance" → "7. Experiment Statistical Significance"
"experiments_compute_resource"        → "8. Experiments Compute Resource"
"code_of_ethics"                      → "9. Code of Ethics"
"broader_impacts"                     → "10. Broader Impacts"
"safeguards"                          → "11. Safeguards"
"licenses"                            → "12. Licenses"
"assets"                              → "13. Assets"
"crowdsourcing_human_subjects"        → "14. Crowdsourcing & Human Subjects"
"irb_approvals"                       → "15. IRB Approvals"
"declaration_llm_usage"               → "16. Declaration of LLM Usage"
```

**Session State — all keys** — SOURCE: `session_state.py:7-22` + `file_uploader.py`:

| Key | Type | Initial Value | Set When | Read When | Cleared When |
|-----|------|---------------|----------|-----------|--------------|
| `resultado` | `dict \| None` | `None` (session_state.py:8-9) | After `auditor.audit()` or on error (file_uploader.py:50, 85, 76) | app.py:40-68; audit_results.py:90,287 | "Limpiar" button (app.py:30-32) |
| `auditor` | `PaperAuditor` | `PaperAuditor()` (session_state.py:12-13) | On first load | file_uploader.py:49 | "Limpiar" button |
| `chatbot` | `PaperChatbot` | `PaperChatbot()` (session_state.py:15-16) | On first load | chatbot.py:26 | "Limpiar" button |
| `sota_analyzer` | `SotaAnalyzer` | `SotaAnalyzer()` (session_state.py:18-19) | On first load | sota_section.py:12 | "Limpiar" button |
| `messages` | `list` of dicts | `[]` (session_state.py:21-22) | On first load; reset on new file (file_uploader.py:21) | chatbot.py:10,23 | "Limpiar" button; new file upload |
| `archivo_actual` | `str` | not initialized | file_uploader.py:19 (set to `uploaded_file.name`) | file_uploader.py:16 | Not cleared (lazy) |
| `file_hash` | `str` (MD5 hex) | not initialized | file_uploader.py:20 | file_uploader.py:17 | Not cleared (lazy) |
| `md_text` | `str` | not initialized | file_uploader.py:36 (PDF) or :39 (TXT/MD) | chatbot.py:26; sota_section.py:12; app.py:53-54; file_uploader.py:98 | Not cleared (lazy) |

**Cross-module dependency:** `initialize_session_state` instantiates `PaperAuditor()`, `PaperChatbot()`, `SotaAnalyzer()` — directly coupling `frontend` to `backend_core`. SOURCE: `session_state.py:12-19`.

---

### Styles

| File | Purpose | CSS Classes/Variables Listed | Source |
|------|---------|------------------------------|--------|
| `frontend/styles/custom_css.py` | Defines `CUSTOM_CSS` string constant (lines 4-83) and `apply_custom_styles() -> None` (lines 85-86). `apply_custom_styles` calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)`. | `.stApp` (dark grey bg `#374151`), `#MainMenu` (hidden), `footer` (hidden), `header` (transparent), `[data-testid="stTable"]` (dark bg `#2d3436`, rounded corners), `[data-testid="stTable"] table/th/tbody th/td` (full border/color/font styling), `[data-testid="stPlotlyChart"]` (dark bg `#2d3436`, rounded corners) | [extracted_frontend_01.md § 6. Custom CSS]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_026] |

---

### Config

| File | Config Keys/Constants | Values (if extracted) | Source |
|------|----------------------|----------------------|--------|
| `frontend/config.py` | `TITLE` | `"💻 Auditor de Papers en Ciencias de la Computación"` — SOURCE: `config.py:3` | [extracted_frontend_01.md § 2.1]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_008] |
| `frontend/config.py` | `SIDEBAR_IMAGE` | `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"` — SOURCE: `config.py:4` | [extracted_frontend_01.md § 2.1]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_008] |
| `frontend/config.py` | `SIDEBAR_DESCRIPTION` | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` — SOURCE: `config.py:5` | [extracted_frontend_01.md § 2.1]; [cross_ref_resolution_cross_ref_root_to_frontend.md § g_008] |

---

### External Dependencies (frontend)

| Package | How Used | Source |
|---------|----------|--------|
| `streamlit` | Web UI framework for all components; page config, widgets, session state, download button | [extracted_frontend_01.md § 1. File Index]; [extracted_root_tests_scratch_01.md § 2] |
| `hashlib` | MD5 hash of uploaded file content for deduplication in `file_uploader.py` | [extracted_frontend_01.md § 5.1] |
| `plotly` | `create_gauge_chart` returns a Plotly `Figure`; rendered via `st.plotly_chart` (caller) | [extracted_frontend_01.md § 2.4] |
| `backend_core` (internal cross-module) | `PaperAuditor`, `PaperChatbot`, `SotaAnalyzer` (via session_state); `convert_pdf_to_markdown` (via file_uploader) | [cross_ref_resolution_cross_ref_root_to_frontend.md § g_027, g_004] |

---

## root Module (scripts, tests, scratch)

**Source cluster:** `cluster_root_tests_scratch_01`
**Extraction file:** `extracted_root_tests_scratch_01.md`
**Cross-ref resolutions applied from:** `cross_ref_resolution_cross_ref_root_to_backend.md`, `cross_ref_resolution_cross_ref_root_to_frontend.md`

### Test Files (tests/)

| File | Test Class(es) / Functions | What Is Tested | Mocking Strategy | Source |
|------|---------------------------|----------------|-----------------|--------|
| `test_auditor_refactor.py` (84 lines, root level) | `test_auditor_initialization`, `test_regex_patterns`, `test_preprocess_method`, `test_prompts_module` | `PaperAuditor` initialization (has expected skill attributes); `REGEX_PATTERNS` dict non-empty; `PaperAuditor._preprocess_paper(text)` returns dict (UNRESOLVED — method absent in current source, see below); `get_extraction_prompt` and `get_evaluation_prompt` return non-empty strings. | No mocking; real `PaperAuditor()` instantiated (requires `GOOGLE_API_KEY`); each test function returns `True/False` and wraps in `try/except Exception`. | [extracted_root_tests_scratch_01.md § 8 RULE-10]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_009] |
| `test_imports.py` (38 lines, root level) | Individual import test functions | All frontend modules importable: `frontend.config`, `frontend.styles.custom_css`, `frontend.utils.session_state`, `frontend.components.file_uploader`, `frontend.components.audit_results`, `frontend.components.sota_section`, `frontend.components.chatbot` | No mocking; verifies module-level imports do not raise exceptions | [extracted_root_tests_scratch_01.md § 1 File Index]; [cross_ref_resolution_cross_ref_root_to_frontend.md § RESOLUTION SUMMARY] |
| `test_skills_integration.py` (148 lines, root level) | Several test blocks | (1) Imports: all `backend.skills` exported symbols importable; (2) Services imports: `PaperAuditor`, `PaperChatbot`, `SotaAnalyzer` importable; (3) Service initialization (real instances, requires API key); (4) `PaperAuditor` has exactly 6 skill attributes; (5) `Chatbot` has exactly 2 skill attributes; (6) `SotaAnalyzer` has exactly 5 skill attributes; (7) `SemanticScholarSearchSkill.execute({'search_queries': []})` returns dict with `'sota_papers'` key | No mocking for most; `SemanticScholarSearchSkill` invoked with empty queries (no real HTTP call needed). Errors call `sys.exit(1)`. | [extracted_root_tests_scratch_01.md § RULE-10, RULE-11, RULE-12, RULE-13]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_015, g_016, g_017, g_018] |
| `tests/test_audit_state.py` (23 lines) | Datamodel unit tests | `AuditState(paper_text="Test content")` defaults: `invalid_paper==False`, `execution_time==0.0`; `to_frontend_dict()` output contains `claims`, `informacion_extraida`, `metricas` keys; `ExtractedInfo().code.repository_url == "NOT FOUND"`; `ExtractedInfo().hyperparameters.optimizer == "NOT FOUND"` | No mocking; pure datamodel assertions | [extracted_root_tests_scratch_01.md § RULE-14, RULE-15, RULE-16, RULE-17]; [cross_ref_resolution_cross_ref_root_to_backend.md § g_014] — NOTE: `AuditState`, `ExtractedInfo`, `ChecklistItem` are UNRESOLVED in `backend/common/` (no `audit_state.py` found in extraction) |
| `tests/test_rag_logical_splitter.py` (32 lines) | RAG chunk splitting tests | `re.split(r'\n\n+', paper_text_norm)` + filter `len(c.strip()) > 10` produces correct chunk list; minimum length > 10 enforced | No mocking; pure text-processing assertions | [extracted_root_tests_scratch_01.md § RULE-08, § 9.6] |
| `tests/test_section_splitter.py` (68 lines) | Section fragmentation tests | `TestSkill.get_fragments(paper_text)` produces exactly 4 fragments from a 6-section equal-content paper; section split pattern `r'\n(?=#+ )'`; target = `total_chars / 4`; max 3 fragments before last | No mocking; inline `TestSkill` class defined in test | [extracted_root_tests_scratch_01.md § RULE-09, § 9.7] |

**[NOTE — `_preprocess_paper` UNRESOLVED]:**  
`test_auditor_refactor.py:31` calls `auditor._preprocess_paper(text)` and asserts `isinstance(red_flags, dict)`. However, the current `PaperAuditor` source contains only `__init__` and `audit` methods — `_preprocess_paper` is not defined. The current `audit` method initializes `context = {'paper_text': paper_text, 'red_flags': {}}` with an empty dict (SOURCE: `auditor.py:78`), suggesting `_preprocess_paper` was removed during refactoring. Manual extraction from pre-refactor commit history is required to recover the original contract.  
[cross_ref_resolution_cross_ref_root_to_backend.md § g_009 — PaperAuditor._preprocess_paper — UNRESOLVED]

**[NOTE — `AuditState`, `ExtractedInfo`, `ChecklistItem` UNRESOLVED]:**  
`tests/test_audit_state.py` imports these datamodels from the backend, but `backend/common/audit_state.py` was not found in the extraction. These models are tested but their source module is absent from the cluster.  
[cross_ref_resolution_cross_ref_root_to_backend.md § g_014 — UNRESOLVED]

---

### Scratch / Exploration Scripts (scratch/, backend/scratch/)

| File | Purpose | Source |
|------|---------|--------|
| `backend/scratch/test_embed.py` (22 lines) | Tests Google GenAI `embed_content` API response structure: calls `client.models.embed_content(model="gemini-embedding-2", contents=["hello", "world", "test"])`, prints `res.embeddings` structure and `len(res.embeddings[0].values)`. | [extracted_root_tests_scratch_01.md § 1 File Index; § 7.5] |
| `backend/scratch/test_embed2.py` (19 lines) | Same as `test_embed.py` with additional `except Exception as e` error handling; prints "embed_content error: {e}". | [extracted_root_tests_scratch_01.md § 1 File Index; § 7.6] |
| `scratch/check_st.py` (6 lines) | Checks for `st.html` and `st.iframe` Streamlit attribute existence (compatibility check). | [extracted_root_tests_scratch_01.md § 1 File Index] |
| `scratch/patch_skills.py` (84 lines) | One-time script that rewrites `CrowdsourcingDetectionSkill` and `LicenseDetectionSkill` class bodies in `backend/skills/regex_detection_skills.py` via AST-validated string replacement. Uses class boundary markers: `'class CrowdsourcingDetectionSkill(BaseSkill):'`, `'class LicenseDetectionSkill(BaseSkill):'`, `'class LimitationsQualityDetectionSkill(BaseSkill):'`. | [extracted_root_tests_scratch_01.md § 1 File Index; § RULE-18, RULE-19, RULE-20] |
| `scratch/repro_hyperparams.py` (23 lines) | Reproduces hyperparameter detection on a real paper file using `HybridHyperparameterExtractionSkill` or equivalent. | [extracted_root_tests_scratch_01.md § 1 File Index] |
| `scratch/test_checklist_health.py` (34 lines) | Tests `get_checklist_health()` with a mock evaluation dict using all 16 CHECKLIST_KEYS; asserts `health['status'] == 'risk'` when `answer='No'` with `is_no_justified=False`. | [extracted_root_tests_scratch_01.md § 1 File Index; § RULE-07] |
| `scratch/test_llm_retry.py` (50 lines) | Unit test for `LLMClient` retry logic (mock-based, no real LLM). Tests: (a) success after 2 failures → 3 total calls, 2 sleeps; (b) exhaustion after all 5 retries → 6 total calls, 5 sleeps. | [extracted_root_tests_scratch_01.md § 1 File Index; § RULE-05, RULE-06] |
| `scratch/test_rag_split.py` (35 lines) | Defines and tests a naive `get_rag_chunks(paper_text)` split function: `re.split(r'\n\n+', paper_text)` + strip. No minimum length filter (contrast with `tests/test_rag_logical_splitter.py`). | [extracted_root_tests_scratch_01.md § 1 File Index; § 9.5] |

---

### Production Utility Scripts (root level)

| File | Purpose | CLI Args / Inputs / Outputs (from extraction) | Source |
|------|---------|----------------------------------------------|--------|
| `create_test_pdf.py` (160 lines) | Generates `paper_test_con_errores.pdf` — a synthetic ML paper with intentionally vague/low-quality content for auditor testing. Entry: `if __name__ == "__main__": create_test_paper_pdf()` | No CLI args. Output: `paper_test_con_errores.pdf` in CWD. Requires `reportlab` (not in `requirements.txt` — GAP-025). | [extracted_root_tests_scratch_01.md § 4.3, § 7.3] |
| `list_models.py` (15 lines) | Lists all Google GenAI models available for configured API key via `client.models.list()`. | No CLI args. Reads `GOOGLE_API_KEY` from env. Prints `"ID: {m.name} | Display Name: {m.display_name}"`. No `if __name__` guard — executes on import. | [extracted_root_tests_scratch_01.md § 5, § 7.4] |
| `md_to_pdf.py` (264 lines) | CLI tool to convert Markdown/TXT files or folders to PDF using `reportlab`. Requires `reportlab` (GAP-025) and optionally `markdown2` (GAP-026 — always `ImportError` in standard install, but `HAS_MARKDOWN` flag is never read downstream so no functional impact). | Args: `<input.md>` [output.pdf] [--size letter\|a4] OR `--folder <folder_path>` [--output <out_folder>] [--size letter\|a4]. Output: PDF file(s). | [extracted_root_tests_scratch_01.md § 4.1, § 7.1] |
| `pdf_to_md.py` (125 lines) | CLI tool to convert PDF files or folders to Markdown using `pymupdf4llm`. | Args: `<input.pdf>` [output.md] OR `--folder <folder_path>` [--output <out_folder>]. Output: `.md` file(s). | [extracted_root_tests_scratch_01.md § 4.2, § 7.2] |
| `app.py` (74 lines, root) | Legacy Streamlit entry point. Page config: `page_title="Nature Auditor Pro"`, `layout="wide"`, `page_icon="🔬"`. Imports same frontend symbols as `frontend/app.py`. Functionally equivalent but uses `page_title="Nature Auditor Pro"` instead of `"NeurIPS 2026 Checklist Auditor"`. | No CLI args. Streamlit web app (same port as `frontend/app.py`). Accepts `["pdf", "txt", "md"]`. | [extracted_root_tests_scratch_01.md § 3. Application Entry Point] |

#### md_to_pdf.py — Function Details

**`parse_markdown_to_elements(md_text, styles) -> list`** — SOURCE: `md_to_pdf.py:23`

| Line pattern | Reportlab Output |
|-------------|-----------------|
| Empty string after `.strip()` | `Spacer(1, 0.1*inch)` |
| Starts with `'# '` NOT `'## '` | `Paragraph(line[2:].strip(), styles['Heading1'])` + `Spacer(1, 0.2*inch)` |
| Starts with `'## '` NOT `'### '` | `Paragraph(line[3:].strip(), styles['Heading2'])` + `Spacer(1, 0.15*inch)` |
| Starts with `'### '` | `Paragraph(line[4:].strip(), styles['Heading3'])` + `Spacer(1, 0.1*inch)` |
| Starts with `'- '` OR `'* '` | `Paragraph('• ' + line[2:].strip(), styles['Normal'])` |
| `line[0].isdigit()` AND `line[1:3] in ['. ', ') ']` | `Paragraph(line, styles['Normal'])` (numbered list) |
| Starts with ` ``` ` | Collect until next ` ``` `; `Preformatted(code_text, styles['Code'])` + `Spacer(1, 0.1*inch)` |
| Starts with `'---'` OR `'==='` | `Spacer(1, 0.1*inch)` + `Paragraph('<hr/>', styles['Normal'])` + `Spacer(1, 0.1*inch)` |
| All other lines | Naive `**` → `<b></b>`, `*` → `<i></i>` replacement; `Paragraph(text, styles['Normal'])` |

SOURCE: `md_to_pdf.py:38-99`

**`convert_to_pdf(input_path, output_path=None, page_size='letter') -> str | None`** — SOURCE: `md_to_pdf.py:103`

Validation: rejects if file not found or extension not in `['md', 'txt', 'markdown']`. Default output path: `input_path.rsplit('.', 1)[0] + '.pdf'`. PDF margins: right=72, left=72, top=72, bottom=18 (points). Style overrides: Normal (fontSize=11, leading=14, alignment=TA_JUSTIFY), Heading1 (18, #1a1a1a, spaceAfter=12), Heading2 (14, #2d2d2d, spaceAfter=10), Heading3 (12, #404040, spaceAfter=8), Code (Courier, size=9, leftIndent=20, rightIndent=20, textColor=#2d2d2d, backColor=#f5f5f5, borderPadding=5). Page estimate: `len(elements) // 30`.

**`convert_folder(folder_path, output_folder=None, page_size='letter')`** — SOURCE: `md_to_pdf.py:209`

Globs `*.md` + `*.txt`. Tracks `successful`/`failed` counts. Calls `convert_to_pdf` per file.

---

### External Dependencies (root/tests)

| Package | How Used | Source |
|---------|----------|--------|
| `unittest.mock` | `MagicMock`, `patch` in `scratch/test_llm_retry.py` for `LLMClient` retry testing | [extracted_root_tests_scratch_01.md § RULE-05, RULE-06] |
| `reportlab` | `SimpleDocTemplate`, `Paragraph`, `Spacer`, `PageBreak`, `Table`, `TableStyle`, `Preformatted`, `getSampleStyleSheet`, `ParagraphStyle`, `letter`, `A4`, `inch`, `colors`, `TA_CENTER`, `TA_LEFT`, `TA_JUSTIFY` in `md_to_pdf.py` (lines 8–13) and `create_test_pdf.py` (lines 2–6). **NOT listed in `requirements.txt`** — [GAP: GAP-cluster_root_tests_scratch_01-025 — reportlab is a hard undeclared dependency; any environment from `requirements.txt` only fails at module-load time with ModuleNotFoundError] | [extracted_root_tests_scratch_01.md § 2 Missing Dependencies] |
| `pymupdf4llm` | `pymupdf4llm.to_markdown(pdf_path)` in `pdf_to_md.py` | [extracted_root_tests_scratch_01.md § 4.2] |
| `markdown2` | Attempted via `try: import markdown2` in `md_to_pdf.py:15`. **NOT in `requirements.txt`**. `HAS_MARKDOWN` is set `False` on `ImportError` but is never read downstream — no functional gating. Default state is always `HAS_MARKDOWN=False` in standard install. [GAP: GAP-cluster_root_tests_scratch_01-026 — markdown2 is an optional undeclared dependency; its absence is the default] | [extracted_root_tests_scratch_01.md § 2 Missing Dependencies; § 10.5] |
| `google-generativeai` | `genai.Client` in `backend/scratch/test_embed.py` and `test_embed2.py`; `list_models.py` | [extracted_root_tests_scratch_01.md § 7.4, 7.5, 7.6] |
| `sys` | `sys.argv` parsing in CLI scripts; `sys.exit(1)` in `test_skills_integration.py` on fatal errors | [extracted_root_tests_scratch_01.md § 4.1, 4.2, 10.7] |
| `pathlib` | `Path(folder_path).glob(...)` in `convert_folder` functions | [extracted_root_tests_scratch_01.md § 7.8, 7.9] |
| `docling` | `backend/scratch/test_embed.py` (not directly) — indirectly required by `backend_core` | [extracted_root_tests_scratch_01.md § 2] |
| `streamlit` | `scratch/check_st.py` checks `st.html` and `st.iframe` attribute existence | [extracted_root_tests_scratch_01.md § 1 File Index] |
| `ast` | `scratch/patch_skills.py` validates patched file via AST parse before writing | [extracted_root_tests_scratch_01.md § 1 File Index] |
