### Token budget precalculation

=== TOKEN BUDGET PRECALCULATION ===
Total spec files size: 494,658 chars ≈ 148,397 tokens
Total source code: 4,927 LOC ≈ 14,781 tokens
Combined: ≈ 163,178 tokens
Agent context window: ~120K tokens (usable ~80K after prompt+output)
A single validator reading ALL specs + ALL source = 163,178 tokens — DOES NOT FIT — must split
==================================


### Generated specs summary

### 01_data_model.md (47926 chars)
# Data Model Specification — Nature Auditor Pro

> **Scope note:** This application has no SQL database. The data model is the complete set of structured Python types — Pydantic models, plain dataclasses, configuration dicts, constants, enums, and Streamlit session-state keys — that flow through the audit pipeline. Every section below treats these types with the same rigour applied to a relational schema.

---

## 1. Pydantic / Dataclass Models

### Entity: `Hyperparameters`

**Inherits From:** `pydantic.BaseModel`

Source: `rag_extraction_skill.py:11`

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `thought_process` | `str` | No | — | `Field(description="Internal reasoning about the technical details found in this fragment...")` | `rag_extraction_skill.py:11` |
| `learning_rate` | `str` | No | — | `Field(description="Learning rate value, e.g., '1e-4'... or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `batch_size` | `str` | No | — | `Field(description="Batch size value, e.g., '32'... or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `epochs` | `str` | No | — | `Field(description="Number of epochs, e.g., '100'... or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `optimizer` | `str` | No | — | `Field(description="Optimizer name, e.g., 'AdamW', 'SGD', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `warmup_steps` | `str` | No | — | `Field(description="Warmup steps or ratio, e.g., '1000', '0.1', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `weight_decay` | `str` | No | — | `Field(description="Weight decay value, e.g., '0.01', '1e-5', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `random_seed` | `str` | No | — | `Field(description="Random seed value, e.g., '42', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `betas` | `str` | No | — | `Field(description="Adam betas, e.g., '(0.9, 0.999)', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `epsilon` | `str` | No | — | `Field(description="Adam epsilon, e.g., '1e-8', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `training_steps` | `str` | No | — | `Field(description="Total optimization steps, e.g., '100k', '50000', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `total_tokens` | `str` | No | — | `Field(description="Total tokens trained on, e.g., '3T', '100B', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `hardware` | `str` | No | — | `Field(description="Hardware details, e.g., '8x NVIDIA A100', '1 TPU v4', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |
| `latency_metrics` | `str` | No | — | `Field(description="Performance metrics like latency or throughput, e.g., '2% increase', or 'NOT FOUND'")` | `rag_extraction_skill.py:11` |

> All fields are required (no defaults). All `str` values should be the extracted value or the sentinel string `"NOT FOUND"`.

#### Relationships

- `Hyperparameters` is used as the Pydantic response schema for the fallback call in `HybridHyperparameterExtractionSkill`'s REDUCE phase: `config={'response_schema': Hyperparameters}` — SOURCE: `rag_extraction_skill.py:204`.
- After cleaning (`_clean_with_regex`), fields `learning_rate` and `weight_decay` may be converted to `float`; `batch_size`, `epochs`, `random_seed` to `int`; all others remain `str` — SOURCE: `rag_extraction_skill.py:277`.

---

### Entity: `AuditState`

**Inherits From:** [GAP: base class not extractable — source file `backend/common/audit_state.py` absent from repository]

Source: `tests/test_audit_state.py` (inferred from test assertions); `backend/common/audit_state.py` — UNRESOLVED (file absent)

> **CONFIDENCE: UNRESOLVED.** The file `backend/common/audit_state.py` does not exist in the repository. The contracts below are INFERRED from test assertions in `tests/test_audit_state.py` and are NOT confirmed from source. See cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY [g_014].

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `paper_text` | `str` | No | — | Set at construction | `tests/test_audit_state.py:6` |
| `invalid_paper` | `bool` | No | `False` | Default from construction rule | `tests/test_audit_state.py:9` |
| `execution_time` | `float` | No | `0.0` | Default from construction rule | `tests/test_audit_state.py:10` |
| `evaluation` | `dict` | [GAP: nullability not resolved] | [GAP: default not resolved] | Dict whose keys match `CHECKLIST_KEYS`; each value is a checklist item dict | `tests/test_audit_state.py:13` |

#### Methods (inferred)

- `to_frontend_dict() -> dict`: flattens `evaluation` dict to top level, includes `informacion_extraida` and `metricas` keys — SOURCE: `tests/test_audit_state.py:13-18`.

#### Relationships

- References `ExtractedInfo` (via `informacion_extraida` in `to_frontend_dict()` output) — see Entity: `ExtractedInfo`.

---

### Entity: `ExtractedInfo`

**Inherits From:** [GAP: base class not extractable — source file `backend/common/audit_state.py` absent]

Source: `tests/test_audit_state.py` (inferred); `backend/common/audit_state.py` — UNRESOLVED

> **CONFIDENCE: UNRESOLVED.** Same caveat as `AuditState`. Contracts inferred from test assertions only.

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `code` | nested model / object | [GAP: type not resolved] | — | Has attribute `repository_url` defaulting to `"NOT FOUND"` | `tests/test_audit_state.py:22` |
| `hyperparameters` | nested model / object | [GAP: type not resolved] | — | Has attribute `optimizer` defaulting to `"NOT FOUND"` | `tests/test_audit_state.py:23` |

#### Sub-field contracts (inferred)

| Sub-field | Parent field | Default | Source |
|-----------|-------------|---------|--------|
| `code.repository_url` | `code` | `"NOT FOUND"` | `tests/test_audit_state.py:22` |
| `hyperparameters.optimizer` | `hyperparameters` | `"NOT FOUND"` | `tests/test_audit_state.py:23` |

All other sub-fields: [GAP: field contracts not resolved in extraction]

---

### Entity: `ChecklistItem`

**Inherits From:** [GAP: base class not extractable — source file `backend/common/audit_state.py` absent]

Source: `tests/test_audit_state.py` — UNRESOLVED (class present but not exercised in tests)

> **CONFIDENCE: UNRESOLVED.** No field contracts are derivable from test code. The class is defined in `backend/common/audit_state.py` which is absent from the repository.

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| [GAP: field contract not resolved in extraction] | | | | | `tests/test_audit_state.py` |

---

### Entity: `BaseSkill`

**Inherits From:** `abc.ABC`

Source: `base_skill.py:10`

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `llm_client` | `Optional[LLMClient]` | Yes | `None` | Stored from constructor param | `base_skill.py:19` |
| `config` | `Dict` | No | `{}` | If `None` passed, set to `{}`; stored from constructor param | `base_skill.py:19` |
| `name` | `str` | No | `self.__class__.__name__` | Set from runtime class name | `base_skill.py:19` |

#### Model Config

No class-level `Config` block. Not a Pydantic model; plain Python class with `__init__`.

#### Relationships

- Abstract method `execute(self, context: Dict[str, Any]) -> Dict[str, Any]` must be overridden by all concrete subclasses — SOURCE: `base_skill.py:34`.
- `LLMClient` → see Service Contracts (not a data model; it wraps the Gemini API).
- Subclasses include: `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ChecklistVerificationSkill`, `ConversationalResponseSkill`, `ContextValidationSkill`, `ThematicCoverageSkill`, `QueryGenerationSkill`, `SemanticScholarSearchSkill`, `CoverageGapAnalysisSkill`, `CrossValidationSkill`, `HybridHyperparameterExtractionSkill`, all regex detection skills, `CompositeSkill`.

---

### Entity: `CompositeSkill`

**Inherits From:** `BaseSkill`

Source: `base_skill.py:91`

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `skills` | `list[BaseSkill]` | No | — | Stored from constructor param; used in `execute` iteration | `base_skill.py:91` |
| `llm_client` | `Optional[LLMClient]` | Yes | `None` | Passed to `super().__init__(llm_client)` | `base_skill.py:91` |
| `name` | `str` | No | `"CompositeSkill"` | Inherited from `BaseSkill.__init__` | `base_skill.py:19` |
| `config` | `Dict` | No | `{}` | Inherited from `BaseSkill.__init__` | `base_skill.py:19` |

#### Relationships

- Contains a list of `BaseSkill` instances (`self.skills`); accumulated context is merged across all skills via `accumulated_context.update(result)` — SOURCE: `base_skill.py:103`.
- On per-skill exception: sets `accumulated_context["error_{skill.name}"] = str(e)` — SOURCE: `base_skill.py:103`.

---

## 2. Configuration Structures

### Config: `AUDIT_CONFIG`

Source: `backend/common/config.py:116`

Used by: `PaperAuditor.__init__` for all 5 `LLMClient` instances (`extraction_llm`, `evaluation_llm`, `rag_map_llm`, `rag_reduce_llm`, `verification_llm`).

| Key | Type | Value / Default | Description | Source |
|-----|------|-----------------|-------------|--------|
| `response_mime_type` | `str` | `"application/json"` | Forces JSON-mode response from Gemini | `config.py:116` |
| `temperature` | `float` | `0.0` | Alias of `AUDIT_TEMPERATURE`; deterministic (greedy) generation | `config.py:116` |
| `top_k` | `int` | `1` | Only top-1 token considered | `config.py:116` |
| `top_p` | `float` | `0.1` | Nucleus sampling threshold | `config.py:116` |
| `max_output_tokens` | `int` | `16384` | Maximum tokens in LLM response | `config.py:116` |

---

### Config: `CHAT_CONFIG`

Source: `backend/common/config.py:125`

Used by: `PaperChatbot.__init__` → `LLMClient(generation_config=CHAT_CONFIG)`.

| Key | Type | Value / Default | Description | Source |
|-----|------|-----------------|-------------|--------|
| `temperature` | `float` | `0.2` | Alias of `CHAT_TEMPERATURE`; mild randomness for conversational tone | `config.py:125` |

---

### Config: `SOTA_CONFIG`

Source: `backend/common/config.py:130`

Used by: `SotaAnalyzer.__init__` → `LLMClient(generation_config=SOTA_CONFIG)`.

| Key | Type | Value / Default | Description | Source |
|-----|------|-----------------|-------------|--------|
| `response_mime_type` | `str` | `"application/json"` | Forces JSON-mode response | `config.py:130` |
| `temperature` | `float` | `0.1` | Alias of `SOTA_TEMPERATURE`; low randomness | `config.py:130` |

---

## 3. Named Constants

### Constants: API Keys

Source: `backend/common/config.py`; loaded via `load_dotenv()` at `config.py:27`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `GOOGLE_API_KEY` | `os.getenv("GOOGLE_API_KEY")` — `None` if not set in `.env` | `str \| None` | Passed as `api_key=GOOGLE_API_KEY` to `genai.Client()` inside `LLMClient.__init__`; raises `ValueError` if falsy | `config.py:30` |
| `SEMANTIC_SCHOLAR_API_KEY` | `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` — `None` if not set | `str \| None` | Added as `"x-api-key"` header in `SemanticScholarSearchSkill.execute` if set | `config.py:31` |

---

### Constants: Model Names

Source: `backend/common/config.py`; all hardcoded strings (NOT environment-overridable)

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | `str` | RAG embeddings via Google GenAI `batchEmbedContents` API | `config.py:35` |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Triage and MAP phase extraction; `rag_map_llm`; `RAG_MODEL_NAME` alias | `config.py:37` |
| `REDUCE_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Orchestration / REDUCE consolidation phase; `rag_reduce_llm` | `config.py:39` |
| `EXTRACTION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Initial extraction (general analysis); `extraction_llm`; `MODEL_NAME` alias | `config.py:41` |
| `EVALUATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Final evaluation (Senior Area Chair); `evaluation_llm` | `config.py:43` |
| `VERIFICATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Strict verification (Auditor 2); `verification_llm` | `config.py:45` |
| `MODEL_NAME` | `= EXTRACTION_MODEL_NAME` (alias assignment) → `"gemini-3.1-flash-lite-preview"` | `str` | Default model for `LLMClient` when `model_name=None` | `config.py:107` |
| `RAG_MODEL_NAME` | `= MAP_MODEL_NAME` (alias assignment) → `"gemini-3.1-flash-lite-preview"` | `str` | Default model for RAG operations | `config.py:108` |

---

### Constants: Temperature

Source: `backend/common/config.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `AUDIT_TEMPERATURE` | `0.0` | `float` | Used in `AUDIT_CONFIG["temperature"]` | `config.py:111` |
| `CHAT_TEMPERATURE` | `0.2` | `float` | Used in `CHAT_CONFIG["temperature"]` | `config.py:112` |
| `SOTA_TEMPERATURE` | `0.1` | `float` | Used in `SOTA_CONFIG["temperature"]` | `config.py:113` |

---

### Constants: Semantic Scholar API

Source: `backend/common/config.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `SEMANTIC_SCHOLAR_BASE_URL` | `"https://api.semanticscholar.org/graph/v1/paper/search"` | `str` | Base URL for `requests.get()` in `SemanticScholarSearchSkill.execute` | `config.py:136` |
| `SEMANTIC_SCHOLAR_YEAR_RANGE` | `"2023-2026"` | `str` | `year` query param for API call | `config.py:137` |
| `SEMANTIC_SCHOLAR_LIMIT` | `5` | `int` | `limit` query param per query (max results per request) | `config.py:138` |
| `SEMANTIC_SCHOLAR_FIELDS` | `"paperId,title,authors,year,citationCount,abstract,url"` | `str` | `fields` query param for API call | `config.py:139` |

---

### Constants: LLM Retry (inline in `LLMClient.generate`)

Source: `backend/common/llm_client.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `max_retries` | `5` | `int` | Loop runs `range(max_retries + 1)` = 6 total attempts | `llm_client.py:39` |
| `base_delay` | `2` | `int` (seconds) | Exponential base: `delay = base_delay * (2 ** attempt) + jitter` | `llm_client.py:40` |

Retryable HTTP codes (checked via `any(code in error_msg.upper() ...)` in `llm_client.py:54`):

| Code / String | Source |
|---|---|
| `"503"` | `llm_client.py:54` |
| `"429"` | `llm_client.py:54` |
| `"UNAVAILABLE"` | `llm_client.py:54` |
| `"RESOURCE_EXHAUSTED"` | `llm_client.py:54` |
| `"DEADLINE_EXCEEDED"` | `llm_client.py:54` |

---

### Constants: PDF Parser Chunking

Source: `backend/services/pdf_parser.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `chunk_size` | `5` | `int` | Pages per processing block in `convert_pdf_to_markdown` | `pdf_parser.py:51` |

---

### Constants: ANSI Log Colors (`Colors` class)

Source: `backend/utils/logger.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `Colors.BLUE` | `"\033[94m"` | `str` | DEBUG log level color | `logger.py:7` |
| `Colors.CYAN` | `"\033[96m"` | `str` | HTTP Request log color | `logger.py:8` |
| `Colors.GREEN` | `"\033[92m"` | `str` | INFO log level color | `logger.py:9` |
| `Colors.YELLOW` | `"\033[93m"` | `str` | WARNING log level color | `logger.py:10` |
| `Colors.RED` | `"\033[91m"` | `str` | ERROR log level color | `logger.py:11` |
| `Colors.MAGENTA` | `"\033[95m"` | `str` | Available (not mapped to a level) | `logger.py:12` |
| `Colors.BOLD` | `"\033[1m"` | `str` | CRITICAL prefix | `logger.py:13` |
| `Colors.RESET` | `"\033[0m"` | `str` | Reset after colorized segment | `logger.py:14` |

Log-level to color mapping (used by `ColoredFormatter`):

| Level | Color | Source |
|-------|-------|--------|
| `logging.DEBUG` | `Colors.BLUE` | `logger.py:22` |
| `logging.INFO` | `Colors.GREEN` | `logger.py:23` |
| `logging.WARNING` | `Colors.YELLOW` | `logger.py:24` |
| `logging.ERROR` | `Colors.RED` | `logger.py:25` |
| `logging.CRITICAL` | `Colors.BOLD + Colors.RED` | `logger.py:26` |

---

### Constants: RAG Operations

Source: `backend/skills/rag_extraction_skill.py`, `backend/skills/auditor_skills.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `NEGATION_WINDOW` | `60` | `int` | Chars before a regex match to inspect for negation context | `regex_detection_skills.py:8` |
| RAG `batch_size` | `15` | `int` | Chunks per embedding API batch | `rag_extraction_skill.py:61` |
| RAG inter-batch sleep | `15` | `int` (seconds) | `time.sleep(15)` between embedding batches | `rag_extraction_skill.py:67` |
| RAG inter-chunk sleep | `1` | `int` (second) | `time.sleep(1)` between MAP LLM calls | `rag_extraction_skill.py:199` |
| RAG `n_results` per query | `10` | `int` | ChromaDB `collection.query(n_results=10)` | `rag_extraction_skill.py:123` |
| RAG query count | `13` | `int` | Fixed hyperparameter query strings | `rag_extraction_skill.py:99` |
| MAP fragment inter-sleep | `2` | `int` (seconds) | Between fragment LLM calls in `InformationExtractionSkill` | `auditor_skills.py:104` |

RAG distance → relevance score formula:

| Distance range | Score formula | Score range |
|---|---|---|
| `< 0.4` | `int(95 - (distance * 25))` | 85–95 |
| `0.4 ≤ d < 0.7` | `int(85 - ((distance - 0.4) * 180))` | 31–85 |
| `≥ 0.7` | `max(5, int(31 - ((distance - 0.7) * 50)))` | min 5 |

Source: `rag_extraction_skill.py:127`

---

### Constants: SOTA Operations

Source: `backend/skills/sota_skills.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| Semantic Scholar rate-limit sleep | `2` | `int` (seconds) | `time.sleep(2)` on HTTP 429 | `sota_skills.py:217` |
| Semantic Scholar inter-query sleep | `0.5` | `float` (seconds) | Between queries (not before first) | `sota_skills.py:191` |
| Semantic Scholar API timeout | `15` | `int` (seconds) | `requests.get(..., timeout=15)` | `sota_skills.py:207` |
| Semantic Scholar top-N results kept | `10` | `int` | After dedup + sort, `sorted_papers[:10]` | `sota_skills.py:232` |
| CrossValidation max papers to report | `5` | `int` | Prompt instruction: "Selecciona hasta 5 papers omitidos" | `sota_skills.py:379` |

---

### Constants: Checklist Verification Priority Items

Source: `backend/skills/auditor_skills.py:340`

| Constant Name | Value | Source |
|---|---|---|
| `priority_items` (local list in `ChecklistVerificationSkill.execute`) | `['claims', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiments_compute_resource', 'experiment_statistical_significance', 'licenses', 'declaration_llm_usage']` | `auditor_skills.py:340` |

---

### Constants: Application-Level (Frontend)

Source: `frontend/config.py`

| Constant Name | Value | Type | Usage Context | Source |
|---|---|---|---|---|
| `TITLE` | `"💻 Auditor de Papers en Ciencias de la Computación"` | `str` | Page title (`st.title`) | `frontend/config.py:3` |
| `SIDEBAR_IMAGE` | `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"` | `str` | Sidebar ACM logo URL | `frontend/config.py:4` |
| `SIDEBAR_DESCRIPTION` | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` | `str` | Sidebar description | `frontend/config.py:5` |

---

### Constants: Saturation Error Keywords

Source: `frontend/components/file_uploader.py:60`

| Constant Name | Value | Usage Context |
|---|---|---|
| Saturation error keywords (list) | `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` | Checked `in error_msg.upper()` to classify backend error as saturation vs hard failure |

---

### Constants: NeurIPS Quality Score Tiers

Source: `frontend/components/gauge_chart.py:14-31, 57-61`

| Score Range | Label | Bar Color |
|---|---|---|
| `[87.5, 100]` | `"Strong Accept"` | `"#00aa00"` |
| `[75, 87.5)` | `"Accept"` | `"#00cc44"` |
| `[62.5, 75)` | `"Borderline"` | `"#ffcc00"` |
| `[50, 62.5)` | `"Weak Reject"` | `"#ff9900"` |
| `[25, 50)` | `"Reject"` | `"#ff4b4b"` |
| `[0, 25)` | `"Strong Reject"` | `"#cc0000"` |

Threshold line: `value=62.5`, `color="red"`, `width=4`. Source: `gauge_chart.py:57-61`.

---

### Constants: Compliance Table Row Colors

Source: `frontend/components/audit_results.py:18-32`

| Condition | Background Color | Meaning |
|---|---|---|
| `pending_justification == True` | `"#450a0a"` | Critical risk (deep red) |
| `missing_evidence == True` OR `alert_msg` non-empty | `"#452e0a"` | Warning (amber/orange) |
| `"yes" in answer.lower()` | `"#064e3b"` | OK (emerald green) |
| All other cases | `"#111827"` | Neutral (dark) |

---

### Constants: Environment Variable Suppressions (Module-Level Side Effects)

Source: `backend/common/config.py:8-25`

| Operation | Value Set | Source |
|-----------|-----------|--------|
| `os.environ["TRANSFORMERS_VERBOSITY"]` | `"error"` | `config.py:8` |
| `os.environ["TOKENIZERS_PARALLELISM"]` | `"false"` | `config.py:9` |
| `warnings.filterwarnings("ignore")` | all warnings suppressed | `config.py:10` |
| `logging.getLogger("transformers").setLevel(logging.ERROR)` | ERROR level | `config.py:11` |
| `logging.getLogger("httpx").addFilter(CleanNetworkLogs())` | custom filter | `config.py:22` |
| `logging.getLogger("RapidOCR").setLevel(logging.WARNING)` | WARNING level | `config.py:23` |
| `logging.getLogger("docling").setLevel(logging.WARNING)` | WARNING level | `config.py:24` |
| `logging.getLogger("onnxruntime").setLevel(logging.ERROR)` | ERROR level | `config.py:25` |

---

## 4. Session State Schema

All keys listed below flow through `st.session_state` in the Streamlit application.

### Session State Schema

| Key | Type | Initial Value | Lifecycle (set / mutated / cleared at) | Source |
|-----|------|---------------|----------------------------------------|--------|
| `resultado` | `dict \| None` | `None` | **Set:** `file_uploader.py:50` after `auditor.audit()` completes; on error set to `{"error": error_msg}` (`file_uploader.py:85`) or `{"error": "Ejecución cancelada..."}` (`file_uploader.py:76`). **Read:** `app.py:40-68`; `audit_results.py:90, 287`. **Cleared:** on "Limpiar" button press (`app.py:30-32`, all session keys deleted). | `session_state.py:7` |
| `auditor` | `PaperAuditor` | `PaperAuditor()` | **Set:** on first app load (`session_state.py:12-13`). **Read:** `file_uploader.py:49` (calls `.audit()`). **Cleared:** on "Limpiar" button press. | `session_state.py:12-13` |
| `chatbot` | `PaperChatbot` | `PaperChatbot()` | **Set:** on first app load (`session_state.py:15-16`). **Read:** `chatbot.py:26` (calls `.preguntar()`). **Cleared:** on "Limpiar". | `session_state.py:15-16` |
| `sota_analyzer` | `SotaAnalyzer` | `SotaAnalyzer()` | **Set:** on first app load (`session_state.py:18-19`). **Read:** `sota_section.py:12` (calls `.analyze_sota()`). **Cleared:** on "Limpiar". | `session_state.py:18-19` |
| `messages` | `list[dict]` | `[]` | **Set:** on first app load (`session_state.py:21-22`). **Reset to `[]`:** when a new file is detected (`file_uploader.py:21`). **Mutated:** chatbot appends `{"role": "user"|"assistant", "content": str}` items (`chatbot.py:10, 23`). **Cleared:** on "Limpiar". | `session_state.py:21-22` |
| `archivo_actual` | `str` | not initialised | **Set:** `file_uploader.py:19` to `uploaded_file.name`. **Read:** `file_uploader.py:16` to detect file change. | `file_uploader.py:19` |
| `file_hash` | `str` (MD5 hex digest) | not initialised | **Set:** `file_uploader.py:20` to `hashlib.md5(file_content).hexdigest()`. **Read:** `file_uploader.py:17` to detect content change. | `file_uploader.py:20` |
| `md_text` | `str` | not initialised | **Set:** `file_uploader.py:36` (PDF path) or `file_uploader.py:39` (TXT/MD path) to full paper text. **Read:** `chatbot.py:26`, `sota_section.py:12`, `app.py:53-54`, `file_uploader.py:98`. | `file_uploader.py:36-39` |

---

### CHECKLIST_KEYS Enum Set

Source: `frontend/utils/scoring.py:8-15`

| Key String | Position / Index | Meaning | Source |
|---|---|---|---|
| `"claims"` | 0 | NeurIPS item 1 — Claims | `scoring.py:9` |
| `"limitations"` | 1 | NeurIPS item 2 — Limitations | `scoring.py:10` |
| `"theory_assumptions_proofs"` | 2 | NeurIPS item 3 — Theory, Assumptions & Proofs | `scoring.py:11` |
| `"experimental_result_reproducibility"` | 3 | NeurIPS item 4 — Experimental Result Reproducibility | `scoring.py:12` |
| `"open_access_data_code"` | 4 | NeurIPS item 5 — Open Access to Data and Code | `scoring.py:13` |
| `"experimental_setting_details"` | 5 | NeurIPS item 6 — Experimental Setting / Details | `scoring.py:14` |
| `"experiment_statistical_significance"` | 6 | NeurIPS item 7 — Experiment Statistical Significance | `scoring.py:15` |
| `"experiments_compute_resource"` | 7 | NeurIPS item 8 — Experiments Compute Resource | `scoring.py:16` |
| `"code_of_ethics"` | 8 | NeurIPS item 9 — Code of Ethics | `scoring.py:17` |
| `"broader_impacts"` | 9 | NeurIPS item 10 — Broader Impacts | `scoring.py:18` |
| `"safeguards"` | 10 | NeurIPS item 11 — Safeguards | `scoring.py:19` |
| `"licenses"` | 11 | NeurIPS item 12 — Licenses | `scoring.py:20` |
| `"assets"` | 12 | NeurIPS item 13 — Assets | `scoring.py:21` |
| `"crowdsourcing_human_subjects"` | 13 | NeurIPS item 14 — Crowdsourcing & Human Subjects | `scoring.py:22` |
| `"irb_approvals"` | 14 | NeurIPS item 15 — IRB Approvals | `scoring.py:23` |
| `"declaration_llm_usage"` | 15 | NeurIPS item 16 — Declaration of LLM Usage | `scoring.py:24` |

---

### Checklist Answer Values

Source: `extracted_backend_core_01.md § 2.2` (evaluation prompt schema); `cross_ref_resolution_cross_ref_root_to_backend.md § g_010`

| Answer String | Semantics | Source |
|---|---|---|
| `"Yes"` | Item criterion is met; `evidence` field must contain paper section + verbatim fragment | `prompts.py:378` |
| `"No"` | Item criterion is not met; `justification` field must explain what is missing and transparency risk | `prompts.py:378` |
| `"N/A"` | Item is not applicable; `justification` field must explain why | `prompts.py:378` |

Each checklist item dict structure (produced by `get_evaluation_prompt` LLM response):

| Sub-field | Type | Required when | Source |
|---|---|---|---|
| `answer` | `str` | Always | `prompts.py:378` |
| `evidence` | `str` | `answer == "Yes"` | `prompts.py:378` |
| `justification` | `str` | `answer != "Yes"` | `prompts.py:378` |
| `is_no_justified` | `bool` | Always | `prompts.py:378` |

After `ChecklistVerificationSkill` runs, items also gain:

| Sub-field | Type | Meaning | Source |
|---|---|---|---|
| `verified` | `bool` | Always `True` after verification | `auditor_skills.py:325` |
| `was_refined` | `bool` | `True` if NOT corrected (answer unchanged); `False` if answer was overwritten | `auditor_skills.py:325` |

---

## 5. LLM Response JSON Schemas

### LLM Schema: `get_extraction_prompt` → extraction result

Source: `backend/common/prompts.py:4`; confirmed in `extracted_backend_core_01.md § 2.2` and `cross_ref_resolution_cross_ref_root_to_backend.md § g_010`

**Function signature:** `def get_extraction_prompt(paper_text: str, red_flags: dict) -> str`

#### Top-level fields

| Field | Type | Nullable | Description | Source |
|-------|------|----------|-------------|--------|
| `thought_process` | `str` | Yes | Step-by-step reasoning before filling structured fields | `prompts.py:4` |
| `paper_type` | `str` | No | Short classification string; starts with `"INVALID"` for non-ML/AI papers | `prompts.py:4` |
| `invalid_reason` | `str` | Yes | Populated only when `paper_type` starts with `"INVALID"` | `prompts.py:4` |
| `context_mapping` | `list[str]` | Yes | Ordered list of all paper sections identified | `prompts.py:4` |
| `problematic_phrases` | `str \| list` | Yes | Verbatim textual extracts of problematic phrases | `prompts.py:4` |
| `code` | `dict` | Yes | → see `code` sub-schema below | `prompts.py:4` |
| `data` | `dict` | Yes | → see `data` sub-schema below | `prompts.py:4` |
| `hyperparameters` | `dict` | Yes | → see `hyperparameters` sub-schema below | `prompts.py:4` |
| `hardware` | `dict` | Yes | → see `hardware` sub-schema below | `prompts.py:4` |
| `statistics` | `dict` | Yes | → see `statistics` sub-schema below | `prompts.py:4` |
| `architecture` | `dict` | Yes | → see `architecture` sub-schema below | `prompts.py:4` |
| `baseline_comparison` | `dict` | Yes | → see `baseline_comparison` sub-schema below | `prompts.py:4` |
| `software_versions` | `dict` | Yes | → see `software_versions` sub-schema below | `prompts.py:4` |
| `limitations_quality` | `dict` | Yes | → see `limitations_quality` sub-schema below | `prompts.py:4` |
| `theory_and_proofs` | `dict` | Yes | → see `theory_and_proofs` sub-schema below | `prompts.py:4` |
| `broader_impacts_extraction` | `dict` | Yes | → see `broader_impacts_extraction` sub-schema below | `prompts.py:4` |
| `llm_usage_extraction` | `dict` | Yes | → see `llm_usage_extraction` sub-schema below | `prompts.py:4` |
| `human_subjects_extraction` | `dict` | Yes | → see `human_subjects_extraction` sub-schema below | `prompts.py:4` |
| `licenses_extraction` | `dict` | Yes | → see `licenses_extraction` sub-schema below | `prompts.py:4` |

#### `code` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `repository_url` | `str` | Repository URL or `"NOT FOUND"` | `prompts.py:4` |
| `negative_phrase` | `str` | Phrase indicating code unavailability or `"NOT FOUND"` | `prompts.py:4` |
| `dependencies` | `str` | Dependency information or `"NOT FOUND"` | `prompts.py:4` |
| `instructions` | `str` | `"yes"` or `"no"` — whether instructions are provided | `prompts.py:4` |
| `release_mention` | `str` | Mention of release intent or `"NOT FOUND"` | `prompts.py:4` |

#### `data` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `dataset_name` | `str` | Dataset name or `"NOT FOUND"` | `prompts.py:4` |
| `access_url` | `str` | Dataset URL or `"NOT FOUND"` | `prompts.py:4` |
| `negative_phrase` | `str` | Phrase indicating data unavailability or `"NOT FOUND"` | `prompts.py:4` |
| `preprocessing` | `str` | Preprocessing description or `"NOT FOUND"` | `prompts.py:4` |
| `splits` | `str` | Data split information or `"NOT FOUND"` | `prompts.py:4` |
| `release_mention` | `str` | Mention of data release intent or `"NOT FOUND"` | `prompts.py:4` |

#### `hyperparameters` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `optimizer` | `str` | Optimizer name or `"NOT FOUND"` | `prompts.py:4` |
| `learning_rate` | `str` | Learning rate value or `"NOT FOUND"` | `prompts.py:4` |
| `batch_size` | `str` | Batch size or `"NOT FOUND"` | `prompts.py:4` |
| `epochs` | `str` | Number of epochs or `"NOT FOUND"` | `prompts.py:4` |
| `training_steps` | `str` | Total training steps or `"NOT FOUND"` | `prompts.py:4` |
| `total_tokens` | `str` | Total tokens trained on or `"NOT FOUND"` | `prompts.py:4` |
| `warmup` | `str` | Warmup schedule or `"NOT FOUND"` | `prompts.py:4` |
| `weight_decay` | `str` | Weight decay or `"NOT FOUND"` | `prompts.py:4` |
| `betas` | `str` | Adam betas or `"NOT FOUND"` | `prompts.py:4` |
| `epsilon` | `str` | Adam epsilon or `"NOT FOUND"` | `prompts.py:4` |
| `vague_phrase` | `str` | Vague phrase detected (e.g., "standard settings") or `"NOT FOUND"` | `prompts.py:4` |
| `table_reference` | `str` | Reference to a hyperparameter table or `"NOT FOUND"` | `prompts.py:4` |

#### `hardware` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `gpu_cpu` | `str` | GPU/CPU description or `"NOT FOUND"` | `prompts.py:4` |
| `num_gpus` | `str` | Number of GPUs or `"NOT FOUND"` | `prompts.py:4` |
| `memory` | `str` | Memory specification or `"NOT FOUND"` | `prompts.py:4` |
| `time` | `str` | Training time or `"NOT FOUND"` | `prompts.py:4` |
| `carbon_footprint` | `str` | Carbon footprint or `"NOT FOUND"` | `prompts.py:4` |
| `energy_consumption` | `str` | Energy consumption or `"NOT FOUND"` | `prompts.py:4` |
| `pue` | `str` | Power Usage Effectiveness or `"NOT FOUND"` | `prompts.py:4` |
| `throughput` | `str` | Throughput (tokens/sec) or `"NOT FOUND"` | `prompts.py:4` |
| `latency_metrics` | `str` | Latency metrics or `"NOT FOUND"` | `prompts.py:4` |

#### `statistics` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `confidence_intervals` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `significance_tests` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `num_runs` | `str` | Number of runs or `"NOT FOUND"` | `prompts.py:4` |

#### `architecture` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `description` | `str` | Architecture description (layers, dims, heads) or `"NOT FOUND"` | `prompts.py:4` |
| `weights_available` | `str` | Whether model weights are available or `"NOT FOUND"` | `prompts.py:4` |
| `release_mention` | `str` | Mention of model release or `"NOT FOUND"` | `prompts.py:4` |

#### `baseline_comparison` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `compared_models` | `list[str]` | List of compared model names | `prompts.py:4` |
| `has_comparative_tables` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `same_metrics` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `results_section` | `str` | Section containing results or `"NOT FOUND"` | `prompts.py:4` |

#### `software_versions` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `framework` | `str` | Framework versions (e.g., PyTorch 2.0) or `"NOT FOUND"` | `prompts.py:4` |
| `python_version` | `str` | Python version or `"NOT FOUND"` | `prompts.py:4` |
| `cuda_version` | `str` | CUDA version or `"NOT FOUND"` | `prompts.py:4` |
| `dependency_file` | `str` | `"yes"` or `"no"` — whether requirements/env file present | `prompts.py:4` |

#### `limitations_quality` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `has_section` | `str` | `"yes"` or `"no"` — limitations section present | `prompts.py:4` |
| `specific_points` | `list[str]` | List of specific limitation points | `prompts.py:4` |
| `quantified_issues` | `str` | `"yes"` or `"no"` | `prompts.py:4` |

#### `theory_and_proofs` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `has_theoretical_results` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `assumptions_stated` | `str` | Whether assumptions are stated or `"NOT FOUND"` | `prompts.py:4` |
| `proofs_included` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `appendix_reference` | `str` | Appendix reference or `"NOT FOUND"` | `prompts.py:4` |

#### `broader_impacts_extraction` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `has_impact_statement` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `appendix_reference` | `str` | Appendix reference or `"NOT FOUND"` | `prompts.py:4` |
| `concerns_discussed` | `str` | `"yes"` or `"no"` | `prompts.py:4` |

#### `llm_usage_extraction` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `models_used_in_methodology` | `str` | LLM names used in methodology or `"NOT FOUND"` | `prompts.py:4` |
| `purpose_in_methodology` | `str` | Purpose of LLM in methodology or `"NOT FOUND"` | `prompts.py:4` |
| `used_for_writing` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `writing_declaration_quote` | `str` | Verbatim declaration or `"NOT FOUND"` | `prompts.py:4` |

#### `human_subjects_extraction` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `uses_human_annotation` | `str` | `"yes"` or `"no"` | `prompts.py:4` |
| `compensation_details` | `str` | Compensation description or `"NOT FOUND"` | `prompts.py:4` |
| `instructions_provided` | `str` | `"yes"` or `"no"` | `prompts.py:4` |

#### `licenses_extraction` sub-schema

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `assets_used` | `list[str]` | List of asset names with licenses | `prompts.py:4` |
| `licenses_named` | `list[str]` | List of named licenses | `prompts.py:4` |
| `missing_licenses_for_some_assets` | `str` | `"yes"` or `"no"` | `prompts.py:4` |

---

### LLM Schema: `get_map_extraction_prompt` → map fragment result

Source: `backend/common/prompts.py:184`

**Function signature:** `def get_map_extraction_prompt(fragment_text: str) -> str`

The LLM is instructed to return a JSON with the same standard keys as the extraction result, plus the ability to add more keys if needed:

| Field | Type | Nullable | Description | Source |
|-------|------|----------|-------------|--------|
| `paper_title` | `str` | Yes | Paper title if found in fragment | `prompts.py:184` |
| `authors` | `str \| list` | Yes | Authors if found | `prompts.py:184` |
| `context_mapping` | `list[str]` | Yes | Sections identified in this fragment | `prompts.py:184` |
| `thought_process` | `str` | Yes | Fragment-specific reasoning | `prompts.py:184` |
| `code` | `dict` | Yes | Same sub-schema as extraction_prompt `code` | `prompts.py:184` |
| `data` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `hyperparameters` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `hardware` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `statistics` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `architecture` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `baseline_comparison` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `software_versions` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `limitations_quality` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `problematic_phrases` | `str \| list` | Yes | Same as extraction | `prompts.py:184` |
| `theory_and_proofs` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `broader_impacts_extraction` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `llm_usage_extraction` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `human_subjects_extraction` | `dict` | Yes | Same sub-schema | `prompts.py:184` |
| `licenses_extraction` | `dict` | Yes | Same sub-schema | `prompts.py:184` |

> When a field is not found in the fragment, LLM uses `"NOT FOUND"` or `[]`. Per-fragment results are appended to `map_results` list and sent to REDUCE phase. Each fragment dict also receives `_relevance_score: int` and `_chunk_text: str` from `HybridHyperparameterExtractionSkill`.

---

### LLM Schema: `get_reduce_extraction_prompt` → consolidated master result

Source: `backend/common/prompts.py:228`

**Function signature:** `def get_reduce_extraction_prompt(map_results: list) -> str`

Output is the same canonical JSON schema as `get_extraction_prompt`. The LLM consolidates all map fragments into a single definitive master JSON with the same keys. No additional keys are introduced in the REDUCE output.

---

### LLM Schema: `get_evaluation_prompt` → evaluation result

Source: `backend/common/prompts.py:378`; confirmed `cross_ref_resolution_cross_ref_root_to_backend.md § g_010`

**Function signature:** `def get_evaluation_prompt(extracted_info: dict, red_flags: dict) -> str`

Returns a dict with exactly 16 keys (one per NeurIPS checklist item). Each key maps to a checklist item object:

| Checklist Item Key | Position | Source |
|---|---|---|
| `claims` | 1 | `prompts.py:378` |
| `limitations` | 2 | `prompts.py:378` |
| `theory_assumptions_proofs` | 3 | `prompts.py:378` |
| `experimental_result_reproducibility` | 4 | `prompts.py:378` |
| `open_access_data_code` | 5 | `prompts.py:378` |
| `experimental_setting_details` | 6 | `prompts.py:378` |
| `experiment_statistical_significance` | 7 | `prompts.py:378` |
| `experiments_compute_resource` | 8 | `prompts.py:378` |
| `code_of_ethics` | 9 | `prompts.py:378` |
| `broader_impacts` | 10 | `prompts.py:378` |
| `safeguards` | 11 | `prompts.py:378` |
| `licenses` | 12 | `prompts.py:378` |
| `assets` | 13 | `prompts.py:378` |
| `crowdsourcing_human_subjects` | 14 | `prompts.py:378` |
| `irb_approvals` | 15 | `prompts.py:378` |
| `declaration_llm_usage` | 16 | `prompts.py:378` |

Each checklist item object schema:

| Sub-field | Type | Required when | Description | Source |
|---|---|---|---|---|
| `answer` | `str` | Always | Exactly `"Yes"`, `"No"`, or `"N/A"` | `prompts.py:378` |
| `evidence` | `str` | `answer == "Yes"` | Paper section + verbatim fragment | `prompts.py:378` |
| `justification` | `str` | `answer != "Yes"` | What is missing and why it is a transparency risk | `prompts.py:378` |
| `is_no_justified` | `bool` | Always | `true` only if explicit justification or pre-computed signal applies | `prompts.py:378` |

---

### LLM Schema: `get_verification_prompt` → verification result

Source: `backend/common/prompts.py:494`

**Function signature:** `def get_verification_prompt(item_key: str, item_data: dict, paper_context: str) -> str`

| Field | Type | Nullable | Description | Source |
|-------|------|----------|-------------|--------|
| `answer` | `str` | No | `"Yes"`, `"No"`, or `"N/A"` — possibly changed from initial | `prompts.py:494` |
| `evidence` | `str` | Yes | Updated evidence | `prompts.py:494` |
| `justification` | `str` | Yes | Updated justification | `prompts.py:494` |
| `is_no_justified` | `bool` | No | Updated boolean | `prompts.py:494` |
| `was_corrected` | `bool` | No | `true` if the initial answer was changed | `prompts.py:494` |

---

### LLM Schema: `get_evaluation_signals` → signals dict (not an LLM prompt)

Source: `backend/common/prompts.py:273`

**Function signature:** `def get_evaluation_signals(extracted_info: dict) -> dict`

This is a deterministic Python function (no LLM call). It computes a `signals` dict injected as a `PRE-COMPUTED SIGNALS` block into `get_evaluation_prompt`.

| Field | Type | Source derivation | Source |
|-------|------|------------------|--------|
| `reproducibility` | `str` | Derived from `code_url`, `data_url`, `code_release`, `has_any_url`, `has_release_intent` | `prompts.py:273` |
| `open_access` | `str` | Derived from `code_url`, `data_url` | `prompts.py:273` |
| `statistics` | `str` | Derived from `extracted_info.get('statistics', {})` | `prompts.py:273` |
| `compute_resource` | `str` | Derived from `hw_data` (polymorphic: list/str/dict) + `total_tokens` | `prompts.py:273` |
| `licenses` | `str` | Derived from `assets_used`, `licenses_named` | `prompts.py:273` |
| `crowdsourcing` | `str` | Derived from `human_annotation` | `prompts.py:273` |

---

### Virtual Schema: `resultado` (audit result dict)

Source: `extracted_backend_skills_01.md § 3.6`; assembled by `MetadataAggregationSkill.execute` (`auditor_skills.py:285`)

The `resultado` dict is the final audit output returned by `PaperAuditor.audit()` (on success) and stored in `st.session_state.resultado`. It has 23 core keys plus optional keys appended after the skill execution:

| Key | Type | Required | Notes | Source |
|-----|------|----------|-------|--------|
| `claims` | `dict` | No (empty `{}` if absent) | Checklist item 1 with `answer`, `evidence`, `justification`, `is_no_justified` | `auditor_skills.py:285` |
| `limitations` | `dict` | No | Checklist item 2 | `auditor_skills.py:285` |
| `theory_assumptions_proofs` | `dict` | No | Checklist item 3 | `auditor_skills.py:285` |
| `experimental_result_reproducibility` | `dict` | No | Checklist item 4 | `auditor_skills.py:285` |
| `open_access_data_code` | `dict` | No | Checklist item 5 | `auditor_skills.py:285` |
| `experimental_setting_details` | `dict` | No | Checklist item 6 | `auditor_skills.py:285` |
| `experiment_statistical_significance` | `dict` | No | Checklist item 7 | `auditor_skills.py:285` |
| `experiments_compute_resource` | `dict` | No | Checklist item 8 | `auditor_skills.py:285` |
| `code_of_ethics` | `dict` | No | Checklist item 9 | `auditor_skills.py:285` |
| `broader_impacts` | `dict` | No | Checklist item 10 | `auditor_skills.py:285` |
| `safeguards` | `dict` | No | Checklist item 11 | `auditor_skills.py:285` |
| `licenses` | `dict` | No | Checklist item 12 | `auditor_skills.py:285` |
| `assets` | `dict` | No | Checklist item 13 | `auditor_skills.py:285` |
| `crowdsourcing_human_subjects` | `dict` | No | Checklist item 14 | `auditor_skills.py:285` |
| `irb_approvals` | `dict` | No | Checklist item 15 | `auditor_skills.py:285` |
| `declaration_llm_usage` | `dict` | No | Checklist item 16 | `auditor_skills.py:285` |
| `informacion_extraida` | `dict` | No | Full extraction dict from REDUCE phase (`extracted_info`) | `auditor_skills.py:285` |
| `red_flags` | `dict` | No | Dict of regex detection flags (various bool / int values keyed by flag name) | `auditor_skills.py:285` |
| `metricas` | `dict` | No | → see `metricas` sub-schema below | `auditor_skills.py:285` |
| `general_analysis_map` | `list[dict]` | No | Per-fragment MAP results (`[]` if absent) | `auditor_skills.py:285` |
| `general_analysis_reduce` | `dict` | No | REDUCE consolidated result (same as `informacion_extraida`) | `auditor_skills.py:285` |
| `hybrid_triage_fragments` | `list[dict]` | No | Per-chunk RAG extraction fragments with `_relevance_score` and `_chunk_text` | `auditor_skills.py:285` |
| `evaluation_signals` | `dict` | No | Pre-computed signals dict from `get_evaluation_signals()` — keys: `reproducibility`, `open_access`, `statistics`, `compute_resource`, `licenses`, `crowdsourcing` | `auditor_skills.py:285` |
| `extracted_hyperparameters_hybrid` | `dict` | Optional | Cleaned hyperparameters from RAG extraction (after `_clean_with_regex`); appended by `PaperAuditor.audit` after `MetadataAggregationSkill` | `auditor.py:192-193` |
| `original_extraction_raw` | `dict` | Optional | Deep copy of `extracted_info` before Phase 1.5 hyperparameter merge; appended by `PaperAuditor.audit` | `auditor.py:194-195` |

#### `metricas` sub-schema

Produced by `MetricsCalculationSkill.execute` (`auditor_skills.py:256`):

| Sub-key | Type | Description | Source |
|---------|------|-------------|--------|
| `tiempo_segundos` | `float` | Audit wall-clock duration in seconds (rounded to 2 decimal places) | `auditor_skills.py:256` |
| `caracteres_leidos` | `int` | `len(paper_text)` — total character count of the input | `auditor_skills.py:256` |
| `red_flags_detectadas` | `int` | Count of critical red flags (keys in `red_flags` whose value is truthy AND key does not start with `"tiene_"`, `"menciona_"`, `"_"`, `"cantidad_"`, or `"puntos_"`) | `auditor_skills.py:256` |

---

### Virtual Schema: `resultado` (error paths)

When `PaperAuditor.audit()` encounters an error it returns one of these dicts instead:

| Condition | Returned dict | Source |
|---|---|---|
| Phase 1 extraction error | `{"error": extraction_result["extraction_error"]}` | `auditor.py:91` |
| Non-ML/AI paper rejected | `{"error": "INVALID_PAPER_TYPE", "message": str, "paper_type": str}` | `auditor.py:109-113` |
| Phase 2 evaluation error | `{"error": evaluation_result["evaluation_error"]}` | `auditor.py:161` |
| Outer unhandled exception | `{"error": str(e)}` | `auditor.py:201` |

---

*End of Data Model Specification.*


### 02_functional_backend.md (87727 chars)
# 02 — Functional Backend Specification
## NeurIPS Paper Auditor — Backend System

> **Purpose**: This document is the authoritative functional specification for the backend of the
> NeurIPS Paper Auditor system. A developer must be able to rewrite the entire backend in another
> technology using ONLY this document, without reference to the original source code.
>
> **Fidelity**: Every element below is traceable to extraction data.
> Elements not found in the source code are marked `[GAP: ...]`.
> No content has been invented or assumed.

---

## Table of Contents

1. [Audit Pipeline Overview (6 Phases)](#section-1)
2. [FASE 1: Information Extraction Skill (MAP/REDUCE)](#section-2)
3. [FASE 1.5: Hybrid Hyperparameter Extraction](#section-3)
4. [FASE 2: Reproducibility Evaluation Skill](#section-4)
5. [FASE 2.5: Checklist Verification Skill](#section-5)
6. [FASE 3: Metrics Calculation Skill](#section-6)
7. [FASE 4: Metadata Aggregation Skill](#section-7)
8. [CompositeSkill Orchestration](#section-8)
9. [BaseSkill Interface and Lifecycle](#section-9)
10. [Regex Detection Skills (9 non-exported skills)](#section-10)
11. [All 15 Exported Skills](#section-11)
12. [SOTA Analysis Pipeline (5 Steps)](#section-12)
13. [Chatbot (preguntar Flow + History)](#section-13)
14. [PDF Parser (Docling Chunked Flow)](#section-14)
15. [LLMClient (Retry + Backoff Logic)](#section-15)
16. [Prompt Template Functions (all 6)](#section-16)

---

<a name="section-1"></a>
## Section 1 — Audit Pipeline Overview (6 Phases)

Source: `extracted_backend_core_01.md §4.2`, `extracted_backend_skills_01.md §3.2`,
`cross_ref_resolution_cross_ref_root_to_backend.md §RESOLUTION SUMMARY`

### 1.1 Phase Summary Table

| Phase | ID | Skill(s) Invoked | Trigger Condition | Input Context Keys | Output Context Keys | Error Handling | Side Effects |
|---|---|---|---|---|---|---|---|
| 1 | `information_extraction` | `InformationExtractionSkill` | Always runs; first phase | `paper_text` (str), `red_flags` (list) | `extracted_info` (dict) | On failure: returns `{"success": False, "error": str(e), "phase": "information_extraction"}`; pipeline aborts | Sleeps 2s between each fragment LLM call |
| 1.5 | `hyperparameter_extraction` | `HybridHyperparameterExtractionSkill` | Always runs after Phase 1 | `paper_text` (str), `extracted_info` (dict) | `hyperparameter_results` (dict) | Non-critical: on failure, pipeline continues (context key may be absent or partial); logs error | Builds and destroys in-memory ChromaDB collection; sleeps 1s between chunks; sleeps 15s between embedding batches |
| 2 | `reproducibility_evaluation` | `ReproducibilityEvaluationSkill` | Always runs after Phase 1.5 | `extracted_info` (dict), `red_flags` (list) | `checklist` (dict) | On failure: returns `{"success": False, "error": str(e), "phase": "reproducibility_evaluation"}`; pipeline aborts | None |
| 2.5 | `checklist_verification` | `ChecklistVerificationSkill` | Always runs after Phase 2 | `paper_text` (str), `checklist` (dict) | `checklist` (dict, updated in-place) | Non-critical: on failure, pipeline continues with unverified checklist; logs error | Truncates `paper_text` to `[:30000] + [-30000:]` for context window |
| 3 | `metrics_calculation` | `MetricsCalculationSkill` | Always runs after Phase 2.5 | `start_time` (float, Unix timestamp), `paper_text` (str), `extracted_info` (dict) | `tiempo_segundos` (float), `caracteres_leidos` (int), `red_flags_detectadas` (int) | On failure: returns `{"success": False, "error": str(e), "phase": "metrics_calculation"}`; pipeline aborts | Records `end_time = time.time()` — see known bug below |
| 4 | `metadata_aggregation` | `MetadataAggregationSkill` | Always runs after Phase 3 | 23 context keys (see §1.2) | `result` (dict, all 23 keys flattened) | On failure: returns `{"success": False, "error": str(e), "phase": "metadata_aggregation"}`; pipeline aborts | None |

### 1.2 Full Input Context Keys for Phase 4 (MetadataAggregationSkill)

The following 23 keys are read from context and flattened into the final result:

| Context Key | Type | Source Phase |
|---|---|---|
| `paper_title` | str | Phase 1 |
| `paper_text` | str | External input |
| `extracted_info` | dict | Phase 1 |
| `hyperparameter_results` | dict | Phase 1.5 |
| `checklist` | dict | Phase 2/2.5 |
| `tiempo_segundos` | float | Phase 3 |
| `caracteres_leidos` | int | Phase 3 |
| `red_flags_detectadas` | int | Phase 3 |
| `red_flags` | list | External input |
| `start_time` | float | PaperAuditor.audit() init |
| `map_results` | list | Phase 1 MAP |
| `reduce_result` | dict | Phase 1 REDUCE |
| `fragment_count` | int | Phase 1 |
| `evaluation_signals` | dict | Phase 2 |
| `checklist_summary` | dict | Phase 2.5 |
| `verification_count` | int | Phase 2.5 |
| `model_name` | str | Config |
| `embedding_model` | str | Config |
| `audit_timestamp` | str | PaperAuditor.audit() |
| `paper_hash` | str | PaperAuditor.audit() |
| `audit_version` | str | Config |
| `error_log` | list | Throughout |
| `warnings` | list | Throughout |

Source: `extracted_backend_skills_01.md §3.2 (MetadataAggregationSkill)`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_013`

### 1.3 Pipeline Control Flow (Prose)

`PaperAuditor.audit(paper_text: str, red_flags: list) -> dict` is the single entry point.
The pipeline is **sequential**: phases execute in order 1 → 1.5 → 2 → 2.5 → 3 → 4.
There is no branching or DAG structure.

**Context propagation**: A shared mutable `context` dict is initialized before Phase 1 and
passed to each skill's `execute(context)` call. Each skill reads from and writes to this same
dict. Phases do not receive isolated copies.

**Failure model (critical vs non-critical)**:

- Phases 1, 2, 3, 4 are **critical**: on exception, `audit()` returns the error shape immediately
  and the pipeline halts.
- Phases 1.5 and 2.5 are **non-critical**: on exception, the exception is caught, logged to
  `context["error_log"]`, and the pipeline continues with the next phase.

**Start/end time tracking**:

```python
start_time = time.time()
context["start_time"] = start_time
# ... phases 1, 1.5, 2, 2.5 ...
end_time = time.time()   # set here — BEFORE Phase 3 call
context["end_time"] = end_time
# ... phase 3, 4 ...
```

**Known Bug (potential `NameError`)**:  
In the outer `except` block of `audit()`, the code references `end_time` for error reporting,
but `end_time` is only assigned at the start of Phase 3 (`auditor.py:176`). If an exception is
raised before that line (i.e., in Phases 1, 1.5, or 2), `end_time` is unbound and the outer
`except` block itself raises `NameError`, masking the original exception.  
Source: `extracted_backend_core_01.md §GAP-cluster_backend_core_01-012`, `auditor.py:201`  
`[GAP: _preprocess_paper behavior unresolved — method was removed during refactoring; no source available]`

---

<a name="section-2"></a>
## Section 2 — FASE 1: Information Extraction Skill (MAP/REDUCE)

Source: `extracted_backend_skills_01.md §3.2 (InformationExtractionSkill)`,
`extracted_backend_core_01.md §4.2`

### 2.1 Class

```
InformationExtractionSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 2.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 2.3 Trigger Condition

Phase 1 always runs. `PaperAuditor.audit()` calls this skill unconditionally as the first step.

### 2.4 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full text of the paper (from PDF-to-markdown conversion) |
| `red_flags` | list[str] | Yes | List of red-flag patterns to scan for during extraction |

### 2.5 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `extracted_info` | dict | Consolidated extraction result (REDUCE output) |
| `map_results` | list[dict] | Per-fragment MAP extraction results |
| `reduce_result` | dict | Alias / copy of `extracted_info` before post-processing |
| `fragment_count` | int | Number of fragments processed in MAP phase |
| `paper_title` | str | Title extracted from paper (from `extracted_info["title"]`) |

### 2.6 Fragment Sizing Algorithm

```pseudocode
FUNCTION split_paper(paper_text):
    total_chars = len(paper_text)
    target_size = total_chars / 4          # target 4 fragments
    
    # Step 1: Try section-header split
    raw_splits = re.split(r'\n(?=#+ )', paper_text)
    
    IF len(raw_splits) <= 1:
        # Fallback: use LangChain RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=25000,
            chunk_overlap=2000
        )
        fragments = splitter.split_text(paper_text)[:4]
        RETURN fragments
    
    # Step 2: Merge sections into at most 4 balanced fragments
    fragments = []
    current_fragment = ""
    cut_count = 0
    
    FOR section IN raw_splits:
        IF (len(current_fragment) + len(section) > target_size
                AND cut_count < 3
                AND current_fragment != ""):
            fragments.append(current_fragment)
            current_fragment = section
            cut_count += 1
        ELSE:
            current_fragment += "\n" + section
    
    IF current_fragment:
        fragments.append(current_fragment)
    
    RETURN fragments    # at most 4 elements (3 cuts max)
```

Source: `extracted_backend_core_01.md §4.2 (fragment splitting logic)`,
`extracted_backend_skills_01.md §3.2`

### 2.7 MAP Phase

For each fragment in the fragments list:

1. Call `get_map_extraction_prompt(fragment_text)` to build the prompt.
2. Call `LLMClient.generate(prompt, config=AUDIT_CONFIG)` (model: `gemini-3.1-flash-lite-preview`).
3. Apply **Balanced JSON Extraction** (see §2.8) to parse the LLM response.
4. Append the parsed dict to `map_results`.
5. **Sleep 2 seconds** before processing the next fragment.

On error for a single fragment: the error is logged to `context["error_log"]` and the fragment
is skipped (MAP continues with remaining fragments).

### 2.8 Balanced JSON Extraction Algorithm

Applied to every raw LLM string response to extract the first valid top-level JSON object.

```pseudocode
FUNCTION extract_balanced_json(text: str) -> dict | None:
    # Find the first '{' character
    start_idx = text.find('{')
    IF start_idx == -1:
        RETURN None
    
    stack = 0
    in_string = False
    escape_next = False
    
    FOR i FROM start_idx TO len(text)-1:
        char = text[i]
        
        IF escape_next:
            escape_next = False
            CONTINUE
        
        IF char == '\\' AND in_string:
            escape_next = True
            CONTINUE
        
        IF char == '"':
            in_string = NOT in_string
            CONTINUE
        
        IF NOT in_string:
            IF char == '{':
                stack += 1
            ELIF char == '}':
                stack -= 1
                IF stack == 0:
                    json_str = text[start_idx : i+1]
                    RETURN json.loads(json_str)   # raises on parse error
    
    RETURN None   # no balanced object found
```

Source: `extracted_backend_core_01.md §4.2 (balanced JSON extraction)`,
`extracted_backend_skills_01.md §3.2`

### 2.9 REDUCE Phase

After all MAP fragments are processed:

1. Call `get_reduce_extraction_prompt(map_results)` to build the consolidation prompt.
2. Call `LLMClient.generate(prompt, config=AUDIT_CONFIG)`.
3. Apply **Balanced JSON Extraction** to parse the REDUCE result.
4. Apply post-processing: strip markdown JSON fences (```` ```json ``` ````), strip trailing
   commas before `}` or `]` (regex repair).
5. Store result as `context["extracted_info"]` and `context["reduce_result"]`.
6. Extract `context["paper_title"] = extracted_info.get("title", "")`.

### 2.10 Deduplication Strategy

The REDUCE prompt instructs the LLM to merge duplicate entries across fragments. No
client-side deduplication logic is applied — consolidation is fully delegated to the LLM.

Source: `extracted_backend_skills_01.md §3.2`

### 2.11 Error Handling

| Condition | Behavior |
|---|---|
| All MAP fragments fail (empty `map_results`) | REDUCE still called with empty list; LLM may return empty dict |
| Balanced JSON extraction returns `None` | `extracted_info` is set to `{}` (empty dict); pipeline continues |
| REDUCE LLM call raises exception | Phase 1 fails; `audit()` returns `{"success": False, "error": str(e), "phase": "information_extraction"}` |

### 2.12 Return Shape

**Success:**

```python
{
    "success": True,
    "extracted_info": dict,
    "map_results": list[dict],
    "fragment_count": int
}
```

**Failure:**

```python
{
    "success": False,
    "error": str,       # exception message
    "phase": "information_extraction"
}
```

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §4.2`

---

<a name="section-3"></a>
## Section 3 — FASE 1.5: Hybrid Hyperparameter Extraction

Source: `extracted_backend_skills_01.md §4`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_014`

### 3.1 Class

```
HybridHyperparameterExtractionSkill(BaseSkill)
```

Exported: **No** (non-exported, defined in `backend/skills/rag_extraction_skill.py:27`)

### 3.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 3.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text for embedding and chunking |
| `extracted_info` | dict | Yes (optional guard) | Output of Phase 1; checked for presence |

### 3.4 Guard Conditions (Early Exit)

RULE: guard_hyperparameter_extraction  
TRIGGER: `execute()` is called  
CONDITION: `context.get("paper_text")` is falsy (empty string or absent)  
ACTION: Return `{"success": False, "error": "No paper text in context", "phase": "hyperparameter_extraction"}`  
ERROR: Non-critical; `PaperAuditor.audit()` catches this and continues pipeline

### 3.5 Sub-Steps

#### Step 1: Chunk paper text

```pseudocode
FUNCTION chunk_text(paper_text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    WHILE start < len(paper_text):
        end = min(start + chunk_size, len(paper_text))
        chunks.append(paper_text[start:end])
        start += chunk_size - overlap
    RETURN chunks
```

#### Step 2: Generate embeddings via Google API (batch)

```pseudocode
batch_size = 15
inter_batch_sleep = 15   # seconds

FOR i FROM 0 TO len(chunks) STEP batch_size:
    batch = chunks[i : i + batch_size]
    response = google_embedding_api.batchEmbedContents(
        model="gemini-embedding-2",
        content=batch
    )
    embeddings.extend(response.embeddings)
    IF more batches remain:
        sleep(15)
```

Source: `extracted_backend_skills_01.md §4 (batch embedding)`

#### Step 3: Build in-memory ChromaDB collection

```pseudocode
client = chromadb.Client()   # in-memory (no persistence)
collection = client.create_collection("hyperparams")
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)
```

#### Step 4: Query with 13 fixed queries

The 13 fixed queries are:

1. `"learning rate optimizer training configuration"`
2. `"batch size training epochs iterations"`
3. `"model architecture layers parameters"`
4. `"regularization dropout weight decay"`
5. `"dataset size training test split"`
6. `"hardware GPU TPU computational resources"`
7. `"software framework library version"`
8. `"hyperparameter search tuning optimization"`
9. `"loss function objective metric evaluation"`
10. `"preprocessing normalization augmentation"`
11. `"random seed initialization reproducibility"`
12. `"inference deployment serving configuration"`
13. `"ablation study baseline comparison"`

Source: `extracted_backend_skills_01.md §4 (fixed query list)`

For each query:

```pseudocode
results = collection.query(
    query_texts=[query],
    n_results=3
)
```

#### Step 5: Relevance scoring (piecewise linear on ChromaDB distance)

```pseudocode
FUNCTION score_relevance(distance: float) -> float:
    # ChromaDB distance: 0.0 = identical, 2.0 = completely dissimilar
    IF distance <= 0.3:
        RETURN 1.0
    ELIF distance <= 0.7:
        RETURN 1.0 - (distance - 0.3) / (0.7 - 0.3) * 0.5   # 1.0 → 0.5
    ELIF distance <= 1.2:
        RETURN 0.5 - (distance - 0.7) / (1.2 - 0.7) * 0.4   # 0.5 → 0.1
    ELSE:
        RETURN 0.0
```

Source: `extracted_backend_skills_01.md §4 (relevance scoring formula)`

Only chunks with relevance score > 0.0 are included in the LLM context.

#### Step 6: LLM pass (RAG)

```pseudocode
FOR each relevant chunk:
    prompt = get_extraction_prompt(chunk_text, red_flags=[])
    result = LLMClient.generate(prompt, config=AUDIT_CONFIG)
    hyperparameter_data = extract_balanced_json(result)
    sleep(1)   # inter-chunk sleep
```

#### Step 7: Merge results

All per-chunk extraction results are merged into a single `hyperparameter_results` dict.
Merge strategy: later chunks overwrite earlier chunks for the same key (last-write-wins).
[GAP: exact merge deduplication strategy for hyperparameter_results is not fully specified in extraction]

### 3.6 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `hyperparameter_results` | dict | Merged hyperparameter extraction from all relevant chunks |

### 3.7 Error Return Shape

**Success:**

```python
{"success": True, "hyperparameter_results": dict}
```

**Failure (non-critical — pipeline continues):**

```python
{"success": False, "error": str, "phase": "hyperparameter_extraction"}
```

### 3.8 Side Effects

- Creates and destroys an in-memory ChromaDB collection (no disk persistence)
- Calls Google Embedding API (`batchEmbedContents`) with `batch_size=15`, sleeping 15s between batches
- Sleeps 1s between each per-chunk LLM call

Source: `extracted_backend_skills_01.md §4`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_014`

---

<a name="section-4"></a>
## Section 4 — FASE 2: Reproducibility Evaluation Skill

Source: `extracted_backend_skills_01.md §3.2 (ReproducibilityEvaluationSkill)`,
`extracted_backend_core_01.md §4.2`

### 4.1 Class

```
ReproducibilityEvaluationSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 4.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 4.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `extracted_info` | dict | Yes | Output of Phase 1 (InformationExtractionSkill) |
| `red_flags` | list[str] | Yes | List of red-flag pattern strings |

### 4.4 Guard Conditions

RULE: guard_reproducibility_evaluation  
TRIGGER: `execute()` is called  
CONDITION: `context.get("extracted_info")` is falsy  
ACTION: Return `{"success": False, "error": "No extracted_info in context", "phase": "reproducibility_evaluation"}`  
ERROR: Critical; `PaperAuditor.audit()` returns this error and halts

### 4.5 Evaluation Signals (intermediate step)

Before calling the LLM, the skill calls:

```python
evaluation_signals = get_evaluation_signals(extracted_info)
context["evaluation_signals"] = evaluation_signals
```

`get_evaluation_signals()` is NOT a prompt function — it computes a Python dict with 6 keys
derived directly from `extracted_info` (see §16 for full documentation).

### 4.6 LLM Call

```python
prompt = get_evaluation_prompt(extracted_info, red_flags)
response = LLMClient.generate(prompt, config=AUDIT_CONFIG)
```

Config used: `AUDIT_CONFIG = {"response_mime_type": "application/json", "temperature": 0.0, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384}`

Model: `"gemini-3.1-flash-lite-preview"` (via `config.MODEL_NAME`)

### 4.7 Response Parsing

1. Strip markdown JSON fences (`` ```json ``` ``).
2. Strip trailing commas before `}` or `]` (regex).
3. Apply **Balanced JSON Extraction** (§2.8).

### 4.8 Checklist Schema

The LLM returns a dict with 16 NeurIPS checklist item keys. Each value has the shape:

```python
{
    "<checklist_item_key>": {
        "answer": str,          # "Yes" | "No" | "N/A"
        "justification": str,   # free-text explanation
        "evidence": str         # direct quote or description from paper
    }
}
```

The 16 checklist item keys correspond to NeurIPS 2026 reproducibility checklist items.
[GAP: exact list of all 16 checklist item key strings not enumerated in extraction — they
are present in the prompt template `get_evaluation_prompt()` but not individually listed
in the skill extraction]

### 4.9 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `checklist` | dict | 16-item NeurIPS checklist evaluation results |
| `evaluation_signals` | dict | 6-key intermediate signals dict |

### 4.10 Error Return Shape

**Success:**

```python
{"success": True, "checklist": dict}
```

**Failure:**

```python
{"success": False, "error": str, "phase": "reproducibility_evaluation"}
```

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §2.2`

---

<a name="section-5"></a>
## Section 5 — FASE 2.5: Checklist Verification Skill

Source: `extracted_backend_skills_01.md §3.2 (ChecklistVerificationSkill)`,
`extracted_backend_core_01.md §4.2`

### 5.1 Class

```
ChecklistVerificationSkill(BaseSkill)
```

Exported: **No** (non-exported; defined in `backend/skills/auditor_skills.py:319`)

### 5.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 5.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text |
| `checklist` | dict | Yes | Output of Phase 2 (ReproducibilityEvaluationSkill) |

### 5.4 Guard Conditions

RULE: guard_checklist_verification  
TRIGGER: `execute()` is called  
CONDITION: `context.get("checklist")` is falsy or `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "Missing checklist or paper_text", "phase": "checklist_verification"}`  
ERROR: Non-critical; `PaperAuditor.audit()` catches and continues

### 5.5 Paper Context Truncation

```python
paper_context = paper_text[:30000] + paper_text[-30000:]
```

This produces a context string of at most 60,000 characters (first 30,000 + last 30,000 chars).
If `paper_text` is shorter than 60,000 characters, the concatenation overlaps but does not error.

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §4.2`

### 5.6 Priority Items for Verification

The skill verifies 8 priority checklist items (verified individually via separate LLM calls).
Items beyond the 8 base items are selected to reach exactly 8 total verification calls.

[GAP: exact list of 8 priority checklist item keys not enumerated in extraction — they are
used in a priority selection algorithm inside ChecklistVerificationSkill but not individually
listed]

### 5.7 Per-Item Verification

For each of the 8 selected checklist items:

1. Extract `item_key` and `item_data` (the dict `{answer, justification, evidence}` for this item).
2. Call `get_verification_prompt(item_key, item_data, paper_context)`.
3. Call `LLMClient.generate(prompt, config=AUDIT_CONFIG)`.
4. Parse response using Balanced JSON Extraction (§2.8).
5. If verification result differs from original `answer`, update `context["checklist"][item_key]` in-place with the new `answer` and augmented `justification`.
6. Increment `context["verification_count"]`.

### 5.8 Checklist Item Schema

Each checklist item stored in `context["checklist"]`:

| Field | Type | Constraints | Description |
|---|---|---|---|
| `answer` | str | `"Yes"` \| `"No"` \| `"N/A"` | Evaluation answer |
| `justification` | str | Non-empty | Reasoning for the answer |
| `evidence` | str | May be empty | Direct quote or reference from paper |

Post-verification, a `verified` boolean field may be appended to each item:

| Field | Type | Description |
|---|---|---|
| `verified` | bool | `True` if this item was re-evaluated in Phase 2.5 |

Source: `extracted_backend_skills_01.md §3.2`

### 5.9 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `checklist` | dict | Updated in-place; verified items may have modified `answer` and added `verified: True` |
| `verification_count` | int | Number of items re-verified |
| `checklist_summary` | dict | Summary statistics: `{total_items: int, verified_items: int, changed_items: int}` |

### 5.10 Error Return Shape

**Success:**

```python
{"success": True, "verification_count": int, "checklist_summary": dict}
```

**Failure (non-critical):**

```python
{"success": False, "error": str, "phase": "checklist_verification"}
```

Source: `extracted_backend_skills_01.md §3.2`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_015`

---

<a name="section-6"></a>
## Section 6 — FASE 3: Metrics Calculation Skill

Source: `extracted_backend_skills_01.md §3.2 (MetricsCalculationSkill)`,
`extracted_backend_core_01.md §4.2`

### 6.1 Class

```
MetricsCalculationSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 6.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 6.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `start_time` | float | Yes | Unix timestamp from `time.time()` at audit start |
| `paper_text` | str | Yes | Full paper text |
| `extracted_info` | dict | Yes | Phase 1 output; keys filtered for red-flag counting |

### 6.4 Guard Conditions

RULE: guard_metrics_calculation  
TRIGGER: `execute()` is called  
CONDITION: `context.get("start_time")` is absent  
ACTION: Return `{"success": False, "error": "No start_time in context", "phase": "metrics_calculation"}`  
ERROR: Critical; pipeline halts

### 6.5 Metrics Calculated

| Metric | Formula | Source Field(s) | Output Key |
|---|---|---|---|
| `tiempo_segundos` | `end_time - start_time` where `end_time = time.time()` at Phase 3 entry | `context["start_time"]` | `context["tiempo_segundos"]` |
| `caracteres_leidos` | `len(paper_text)` | `context["paper_text"]` | `context["caracteres_leidos"]` |
| `red_flags_detectadas` | Count of keys in `extracted_info` whose key name starts with prefix indicating a red-flag category (see §6.6) | `context["extracted_info"]` | `context["red_flags_detectadas"]` |

Source: `extracted_backend_skills_01.md §3.2 (MetricsCalculationSkill)`

### 6.6 Red Flag Detection Formula

```pseudocode
red_flags_count = 0
FOR key IN extracted_info.keys():
    IF key starts with any known red-flag prefix:
        IF extracted_info[key] is truthy (non-empty, non-None, non-False):
            red_flags_count += 1
context["red_flags_detectadas"] = red_flags_count
```

[GAP: the exact set of red-flag key prefixes used for filtering is not enumerated in extraction —
the filtering is described as "filters keys by prefix" but exact prefix strings not listed]

### 6.7 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `tiempo_segundos` | float | Elapsed time from audit start to Phase 3 entry |
| `caracteres_leidos` | int | Total character count of `paper_text` |
| `red_flags_detectadas` | int | Count of truthy red-flag keys in `extracted_info` |

### 6.8 Error Return Shape

**Success:**

```python
{
    "success": True,
    "tiempo_segundos": float,
    "caracteres_leidos": int,
    "red_flags_detectadas": int
}
```

**Failure:**

```python
{"success": False, "error": str, "phase": "metrics_calculation"}
```

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §4.2`

---

<a name="section-7"></a>
## Section 7 — FASE 4: Metadata Aggregation Skill

Source: `extracted_backend_skills_01.md §3.2 (MetadataAggregationSkill)`,
`extracted_backend_core_01.md §4.2`

### 7.1 Class

```
MetadataAggregationSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 7.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 7.3 Input Context Keys

All 23 keys listed in §1.2 are required. The skill reads each key from context with `.get()`
(no `KeyError` raised for absent keys — absent keys produce `None` values in output).

### 7.4 Aggregation Strategy

```pseudocode
result = {}
FOR key IN AGGREGATION_KEYS:   # the 23 keys listed in §1.2
    result[key] = context.get(key, None)

# Additional computed fields
result["audit_complete"] = True
result["pipeline_version"] = config.AUDIT_VERSION

context["result"] = result
```

The output is a **flat dict** — no nesting. Nested values (e.g., `extracted_info`,
`hyperparameter_results`, `checklist`) are stored as-is (nested dict objects) as values
inside the flat result dict.

Source: `extracted_backend_skills_01.md §3.2 (MetadataAggregationSkill)`

### 7.5 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `result` | dict | Flat dict with all 23 input keys + `audit_complete: True` + `pipeline_version: str` |

### 7.6 Error Return Shape

**Success:**

```python
{"success": True, "result": dict}
```

**Failure:**

```python
{"success": False, "error": str, "phase": "metadata_aggregation"}
```

Source: `extracted_backend_skills_01.md §3.2`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_013`

---

<a name="section-8"></a>
## Section 8 — CompositeSkill Orchestration

Source: `extracted_backend_skills_01.md §2.3`

### 8.1 Class

```
CompositeSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py` via `BaseSkill`)

### 8.2 Constructor

```python
def __init__(self, skills: list[BaseSkill], name: str = "CompositeSkill"):
    self.skills = skills
    self.name = name
```

### 8.3 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 8.4 Chaining Algorithm

```pseudocode
FUNCTION CompositeSkill.execute(context):
    FOR skill IN self.skills:
        result = skill.execute(context)
        
        IF NOT result.get("success", False):
            # One sub-skill failure STOPS the chain
            RETURN {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "failed_skill": skill.__class__.__name__,
                "phase": result.get("phase", "unknown")
            }
        
        # Merge result keys back into context for next skill
        context.update(result)
    
    RETURN {"success": True, "context": context}
```

**Error isolation**: A single sub-skill failure immediately stops the chain. Subsequent skills
in the list are NOT executed.

Source: `extracted_backend_skills_01.md §2.3`

### 8.5 Context Propagation

Context is the shared mutable dict passed through all sub-skills. Each skill's output is merged
into the context dict via `context.update(result)`. This means a later skill can read keys
written by an earlier skill. There is no isolation or sandboxing between sub-skills.

### 8.6 Return Shape

**Success (all skills completed):**

```python
{"success": True, "context": dict}
```

**Failure (one skill failed):**

```python
{
    "success": False,
    "error": str,
    "failed_skill": str,    # class name of the failing skill
    "phase": str
}
```

Source: `extracted_backend_skills_01.md §2.3`

---

<a name="section-9"></a>
## Section 9 — BaseSkill Interface and Lifecycle

Source: `extracted_backend_skills_01.md §2.1`

### 9.1 Class

```
BaseSkill(ABC)
```

Exported: **Yes** (in `__init__.py`)  
Module: `backend/skills/base_skill.py`

### 9.2 Abstract Interface

```python
from abc import ABC, abstractmethod

class BaseSkill(ABC):

    @abstractmethod
    def execute(self, context: dict) -> dict:
        """
        Execute the skill against the provided context.
        
        Args:
            context: Shared mutable dict containing all pipeline state.
                     Skills read from and write to this dict.
        
        Returns:
            dict with at minimum:
                "success": bool
            On success, additional output keys are included.
            On failure, "error": str is included.
        """
        ...
    
    @property
    def name(self) -> str:
        """Human-readable name of the skill. Defaults to class name."""
        return self.__class__.__name__
```

### 9.3 Lifecycle

```
1. Instantiation: __init__(self, llm_client: LLMClient, config: dict)
   → Sub-classes receive LLMClient and config at construction time.
   → No abstract __init__; concrete classes call super().__init__() if needed.

2. Guard check (optional, not abstract):
   → Concrete implementations check preconditions at the START of execute().
   → If guard fails, return {"success": False, "error": ..., "phase": ...} immediately.
   → No separate abstract guard method.

3. execute(context):
   → Read required keys from context.
   → Perform skill logic (LLM calls, regex, computation).
   → Write output keys into context (mutate in-place) AND return them.
   → Return {"success": True, ...output_keys...} or {"success": False, "error": ...}

4. Teardown: none (no abstract teardown/cleanup hook).
```

### 9.4 Contract for `execute()` Return Type

The return dict MUST always contain:

| Key | Type | Always Present | Description |
|---|---|---|---|
| `success` | bool | Yes | `True` if skill completed without error |
| `error` | str | Only when `success=False` | Error message |
| `phase` | str | Only when `success=False` | Phase identifier for diagnostics |

Additional output keys are skill-specific and documented per skill in §§ 2–7, 10–11.

### 9.5 Hooks

No `pre_execute` or `post_execute` hooks are defined in `BaseSkill`. These patterns are not
present in the extraction data.

Source: `extracted_backend_skills_01.md §2.1`

### 9.6 Constructor Pattern (concrete subclasses)

```python
def __init__(self, llm_client: LLMClient, config: dict = None):
    self.llm_client = llm_client
    self.config = config or AUDIT_CONFIG
```

Source: `extracted_backend_skills_01.md §2.2`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_016`

---

<a name="section-10"></a>
## Section 10 — Regex Detection Skills (9 Non-Exported Skills)

Source: `extracted_backend_skills_01.md §5`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_018`

### 10.0 Shared Infrastructure

All 9 regex detection skills inherit from `BaseSkill` and share the following:

#### NEGATION_WINDOW

```python
NEGATION_WINDOW = 60   # characters before a match to scan for negation
```

#### `_search_with_negation(pattern, text, flags)` — shared method

```pseudocode
FUNCTION _search_with_negation(pattern, text, flags=re.IGNORECASE):
    matches = []
    FOR m IN re.finditer(pattern, text, flags):
        start = max(0, m.start() - NEGATION_WINDOW)
        prefix = text[start : m.start()]
        IF any negation phrase in prefix (e.g., "not", "no", "without", "lack"):
            CONTINUE   # skip negated match
        matches.append(m)
    RETURN matches
```

Source: `extracted_backend_skills_01.md §5.0`

#### `TableExtractionHelper` — 3 table patterns

```python
TABLE_PATTERNS = [
    r'Table\s+\d+\s*[:\.]',           # Pattern 1: "Table N:" or "Table N."
    r'^\|.+\|.+\|',                    # Pattern 2: pipe-delimited table rows (multiline)
    r'^\t.+\t',                         # Pattern 3: tab-delimited rows (multiline)
]
```

Used by `HyperparameterDetectionSkill` and `StatisticsDetectionSkill` to extract table
regions first (searched WITHOUT negation), before full-text search (with negation).

Source: `extracted_backend_skills_01.md §5.0`

---

### Skill: HyperparameterDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Guard Conditions

RULE: guard_hyperparameter_detection  
CONDITION: `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "No paper_text", "phase": "hyperparameter_detection"}`

#### Algorithm

1. Extract table regions using `TableExtractionHelper` (3 patterns, no negation).
2. Search tables with `HYPERPARAMETER_PATTERNS` (without negation).
3. Search full `paper_text` with `HYPERPARAMETER_PATTERNS` using `_search_with_negation`.
4. Merge and deduplicate results.

#### Regex Patterns (`HYPERPARAMETER_PATTERNS`)

```python
HYPERPARAMETER_PATTERNS = [
    r'\blearning[_\s]?rate\s*[=:]\s*[\d.e+-]+',
    r'\bbatch[_\s]?size\s*[=:]\s*\d+',
    r'\bepoch[s]?\s*[=:]\s*\d+',
    r'\bdropout\s*[=:]\s*[\d.]+',
    r'\bweight[_\s]?decay\s*[=:]\s*[\d.e+-]+',
    r'\bmomentum\s*[=:]\s*[\d.]+',
    r'\bhidden[_\s]?(?:size|dim|units)\s*[=:]\s*\d+',
    r'\blayers?\s*[=:]\s*\d+',
    r'\bheads?\s*[=:]\s*\d+',
    r'\bwarmup[_\s]?steps?\s*[=:]\s*\d+',
]
```

Source: `extracted_backend_skills_01.md §5.1`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `hyperparameter_matches` | list[str] | List of matched strings |
| `hyperparameter_count` | int | Total match count |

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "hyperparameter_detection"}
```

Source: `extracted_backend_skills_01.md §5.1`

---

### Skill: DataAvailabilityDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Guard Conditions

RULE: guard_data_availability_detection  
CONDITION: `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "No paper_text", "phase": "data_availability_detection"}`

#### Regex Patterns

```python
DATA_AVAILABILITY_PATTERNS = [
    r'\bdata(?:set)?\s+(?:is\s+)?(?:publicly\s+)?available',
    r'\bdata(?:set)?\s+(?:can\s+be\s+)?(?:found|accessed|downloaded)\s+(?:at|from)',
    r'\bwe\s+(?:release|provide|make\s+available)\s+(?:the\s+)?(?:data|dataset)',
    r'\brepository\s+(?:at|on|in)\s+(?:https?://|github|zenodo)',
    r'\bzenodo\.org',
    r'\bfigshare\.com',
    r'\bhuggingface\.co/datasets',
    r'\bdata\s+availability\s+statement',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `data_availability_mentions` | list[str] | Matched strings |
| `data_available` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.2`

---

### Skill: CodeAvailabilityDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
CODE_AVAILABILITY_PATTERNS = [
    r'\bcode\s+(?:is\s+)?(?:publicly\s+)?available',
    r'\bimplementation\s+(?:is\s+)?(?:publicly\s+)?available',
    r'\bgithub\.com/[\w\-]+/[\w\-]+',
    r'\bgitlab\.com/[\w\-]+/[\w\-]+',
    r'\bbitbucket\.org/[\w\-]+/[\w\-]+',
    r'\bwe\s+(?:release|open[_\s]?source|publish)\s+(?:the\s+)?(?:code|implementation)',
    r'\bsource\s+code\s+(?:is\s+)?(?:available|released|provided)',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `code_availability_mentions` | list[str] | Matched strings |
| `code_available` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.3`

---

### Skill: StatisticsDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Algorithm

Same as `HyperparameterDetectionSkill`: tables extracted first (no negation), then
full-text with negation.

#### Regex Patterns

```python
STATISTICS_PATTERNS = [
    r'\bp\s*[<>=]\s*[\d.e+-]+',
    r'\bconfidence\s+interval',
    r'\bstandard\s+(?:deviation|error)\s*[=:±]\s*[\d.]+',
    r'\bt[_\s]?test',
    r'\bchi[_\s]?square',
    r'\banova\b',
    r'\bwilcoxon\b',
    r'\bmann[_\s]?whitney\b',
    r'\bbootstrap\s+(?:confidence|interval|sample)',
    r'\bcorrelation\s+coefficient\s*[=:r]\s*[\d.+-]+',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `statistics_matches` | list[str] | Matched strings |
| `statistics_count` | int | Total match count |
| `statistical_tests_found` | bool | `True` if any statistical test pattern matched |

Source: `extracted_backend_skills_01.md §5.4`

---

### Skill: EnvironmentalImpactDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
ENVIRONMENTAL_IMPACT_PATTERNS = [
    r'\bCO2\s*(?:emission|equivalent|footprint)',
    r'\bcarbon\s+(?:footprint|emission|offset)',
    r'\benergy\s+consumption\s*[=:]\s*[\d.]+',
    r'\bkWh\b',
    r'\bwatt[_\s]?hours?\b',
    r'\bgreen(?:house)?\s+gas',
    r'\bsustainab(?:le|ility)',
    r'\benvironmental\s+impact',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `environmental_mentions` | list[str] | Matched strings |
| `environmental_impact_reported` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.5`

---

### Skill: ProblematicPhrasesDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
PROBLEMATIC_PHRASES_PATTERNS = [
    r'\bstate[_\s]?of[_\s]?the[_\s]?art\b',
    r'\bgroundbreaking\b',
    r'\brevolutionary\b',
    r'\bunprecedented\b',
    r'\bsignificantly\s+(?:outperform|better|superior)',
    r'\btrivially\b',
    r'\bobviously\b',
    r'\bclearly\s+(?:show|demonstrate|prove)',
    r'\bwe\s+prove\s+that\b',
    r'\bit\s+is\s+(?:well[_\s]?known|obvious|clear)\s+that\b',
]
```

Note: These patterns are searched WITHOUT negation (the phrases themselves are the red flags).

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `problematic_phrases` | list[str] | All matched strings |
| `problematic_phrase_count` | int | Total count |

Source: `extracted_backend_skills_01.md §5.6`

---

### Skill: LlmUsageDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
LLM_USAGE_PATTERNS = [
    r'\bGPT[_\s]?-?[34](?:[_\s]?(?:turbo|mini|vision))?\b',
    r'\bChatGPT\b',
    r'\bClaude[_\s]?[23]?\b',
    r'\bGemini[_\s]?(?:Pro|Ultra|Flash|Nano)?\b',
    r'\bLLaMA[_\s]?[23]?\b',
    r'\bMistral\b',
    r'\blarge\s+language\s+model',
    r'\bLLM\b',
    r'\bfoundation\s+model',
    r'\bpre[_\s]?trained\s+(?:language\s+)?model',
    r'\bprompt(?:ing|ed)?\b',
    r'\bfine[_\s]?tun(?:ing|ed)\s+(?:a\s+)?(?:language|LLM)',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `llm_mentions` | list[str] | All matched strings |
| `llm_used` | bool | `True` if any match found |
| `llm_models_detected` | list[str] | Distinct model names found |

Source: `extracted_backend_skills_01.md §5.7`

---

### Skill: CrowdsourcingDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
CROWDSOURCING_PATTERNS = [
    r'\bMechanical\s+Turk\b',
    r'\bMTurk\b',
    r'\bcrowd(?:source|work(?:er)?)',
    r'\bAnnot(?:ation|ator)s?\s+(?:were\s+)?(?:recruited|hired)',
    r'\bhuman\s+(?:evaluator|annotator|rater|judge)s?',
    r'\binter[_\s]?annotator\s+agreement',
    r'\bkappa\s+(?:coefficient|score)',
    r'\bIRR\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `crowdsourcing_mentions` | list[str] | Matched strings |
| `crowdsourcing_used` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.8`

---

### Skill: LicenseDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
LICENSE_PATTERNS = [
    r'\bMIT\s+[Ll]icense\b',
    r'\bApache[_\s]?2(?:\.0)?\s+[Ll]icense\b',
    r'\bGNU\s+(?:GPL|LGPL|AGPL)[_\s]?v?[23]?\b',
    r'\bCreative\s+Commons\b',
    r'\bCC[_\s]?(?:BY|SA|NC|ND)[_\s]?(?:4\.0|3\.0)?\b',
    r'\bBSD[_\s]?(?:2|3)[_\s]?Clause\b',
    r'\bproprietary\s+licen[sc]e\b',
    r'\blicen[sc]ed?\s+under\b',
    r'\bcopyright\s+©?\s*\d{4}\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `license_mentions` | list[str] | Matched strings |
| `license_detected` | bool | `True` if any match found |
| `license_types` | list[str] | Distinct license type strings found |

Source: `extracted_backend_skills_01.md §5.9`

---

<a name="section-11"></a>
## Section 11 — All 15 Exported Skills

Source: `extracted_backend_skills_01.md §§2,3,6,7`, `extracted_backend_core_01.md §§3,4`,
`cross_ref_resolution_cross_ref_root_to_backend.md §§g_009–g_023`

The 15 exported skills are defined in `backend/skills/__init__.py:36`.

---

### Skill: BaseSkill

Already fully documented in §9.

Exported: **Yes**  
Module: `backend/skills/base_skill.py`

---

### Skill: InformationExtractionSkill

Already fully documented in §2.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: ReproducibilityEvaluationSkill

Already fully documented in §4.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: MetricsCalculationSkill

Already fully documented in §6.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: MetadataAggregationSkill

Already fully documented in §7.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: ConversationalResponseSkill

**Module**: `backend/skills/chatbot_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Generates a conversational answer from the LLM for a user question in the chatbot context,
using the paper content and conversation history.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `question` | str | Yes | The user's current question |
| `paper_text` | str | Yes | Full paper text for context |
| `conversation_history` | list[dict] | No (default `[]`) | Prior turns in the conversation |
| `extracted_info` | dict | No | Phase 1 output; injected into prompt if present |

#### Guard Conditions

RULE: guard_conversational_response  
CONDITION: `context.get("question")` is falsy or `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "Missing question or paper_text", "phase": "conversational_response"}`

#### LLM Usage

- Prompt: built from `conversation_history` + current `question` + `paper_text` context
- Config: `CHAT_CONFIG = {"temperature": 0.2}` (no JSON output — plain text)
- Model: `"gemini-3.1-flash-lite-preview"`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `answer` | str | The LLM-generated answer |
| `updated_history` | list[dict] | Conversation history with current Q&A appended |

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "conversational_response"}
```

Source: `extracted_backend_skills_01.md §7 (ConversationalResponseSkill)`

---

### Skill: ContextValidationSkill

**Module**: `backend/skills/chatbot_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Validates that a user question is answerable given the available paper context; returns
a relevance score and a recommendation to proceed or redirect.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `question` | str | Yes | User question |
| `paper_text` | str | Yes | Full paper text |
| `extracted_info` | dict | No | Phase 1 output |

#### Guard Conditions

RULE: guard_context_validation  
CONDITION: `context.get("question")` is falsy  
ACTION: Return `{"success": False, "error": "No question in context", "phase": "context_validation"}`

#### LLM Usage

- Config: `AUDIT_CONFIG` (JSON output)
- Returns JSON with `{is_relevant: bool, confidence: float, reason: str}`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `question_relevant` | bool | Whether the question is answerable from paper context |
| `relevance_confidence` | float | Confidence in the relevance judgment (0.0–1.0) |
| `relevance_reason` | str | Explanation |

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "context_validation"}
```

Source: `extracted_backend_skills_01.md §7 (ContextValidationSkill)`

---

### Skill: ThematicCoverageSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Identifies the main thematic areas of the paper to generate relevant SOTA search queries.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text |
| `extracted_info` | dict | No | Phase 1 output |

#### Guard Conditions

RULE: guard_thematic_coverage  
CONDITION: `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "No paper_text", "phase": "thematic_coverage"}`

#### LLM Usage

- Config: `SOTA_CONFIG = {"response_mime_type": "application/json", "temperature": 0.1}`
- Returns JSON with `{themes: list[str], keywords: list[str], research_area: str}`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `themes` | list[str] | Identified thematic areas |
| `keywords` | list[str] | Key terms for SOTA search |
| `research_area` | str | High-level research domain |

Source: `extracted_backend_skills_01.md §6 (ThematicCoverageSkill)`

---

### Skill: QueryGenerationSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Generates a list of Semantic Scholar search queries based on the paper's themes and keywords.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `themes` | list[str] | Yes | From ThematicCoverageSkill |
| `keywords` | list[str] | Yes | From ThematicCoverageSkill |
| `research_area` | str | No | From ThematicCoverageSkill |

#### Guard Conditions

RULE: guard_query_generation  
CONDITION: `context.get("themes")` is falsy  
ACTION: Return `{"success": False, "error": "No themes in context", "phase": "query_generation"}`

#### LLM Usage

- Config: `SOTA_CONFIG`
- Returns JSON with `{search_queries: list[str]}` (3–5 queries)

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `search_queries` | list[str] | Generated search query strings for Semantic Scholar |

Source: `extracted_backend_skills_01.md §6 (QueryGenerationSkill)`

---

### Skill: SemanticScholarSearchSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Executes Semantic Scholar API searches for the generated queries and returns raw paper results.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `search_queries` | list[str] | Yes | From QueryGenerationSkill |

Each element in `search_queries` is a string; minimum 1 element required.

#### Guard Conditions

RULE: guard_semantic_scholar_search  
CONDITION: `context.get("search_queries")` is falsy or empty list  
ACTION: Return `{"success": False, "error": "No search_queries in context", "phase": "semantic_scholar_search"}`

#### Semantic Scholar API Integration

**Endpoint**: `https://api.semanticscholar.org/graph/v1/paper/search`  
**Auth**: None (public API, unauthenticated)  
**Rate limiting**: No explicit rate limit handling in skill; relies on HTTP 429 retry in LLMClient  
[GAP: whether API key is optionally injected via config is not confirmed in extraction]

**Query parameters for each request**:

| Parameter | Value | Type |
|---|---|---|
| `query` | search query string | str |
| `fields` | `"paperId,title,authors,year,citationCount,abstract,url"` | str |
| `year` | `"2023-2026"` | str |
| `limit` | `5` | int |

**Per-query response element schema**:

| Field | Type | Description |
|---|---|---|
| `paperId` | str | Semantic Scholar paper identifier |
| `title` | str | Paper title |
| `authors` | list[dict] | Each element: `{authorId: str, name: str}` |
| `year` | int | Publication year |
| `citationCount` | int | Citation count at time of query |
| `abstract` | str \| null | Paper abstract |
| `url` | str | Link to paper on Semantic Scholar |

**Error handling**:

| Condition | Behavior |
|---|---|
| HTTP 4xx/5xx | Log error; skip this query; continue with next query |
| Empty `data` list in response | Record empty result for this query; continue |
| Timeout | [GAP: timeout value not specified in extraction] |
| JSON parse error | Log error; skip this query |

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `sota_papers` | list[dict] | All unique papers found across all queries (deduplicated by `paperId`) |
| `query_results` | dict | Mapping of `query_string → list[paper_dict]` (raw per-query results) |

**`sota_papers` element schema**: same as per-query response element schema above.

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "semantic_scholar_search"}
```

Source: `extracted_backend_core_01.md §4.3 (SemanticScholar integration)`,
`extracted_backend_skills_01.md §6 (SemanticScholarSearchSkill)`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_021`

---

### Skill: CoverageGapAnalysisSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Analyzes the retrieved SOTA papers to identify gaps between the audited paper and state-of-the-art.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill |
| `extracted_info` | dict | Yes | Phase 1 output |
| `paper_text` | str | No | Used for deeper context |

#### Guard Conditions

RULE: guard_coverage_gap_analysis  
CONDITION: `context.get("sota_papers")` is falsy or empty  
ACTION: Return `{"success": False, "error": "No sota_papers in context", "phase": "coverage_gap_analysis"}`

#### LLM Usage

- Config: `SOTA_CONFIG`
- Returns JSON with gap analysis results

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `coverage_gaps` | list[dict] | Each: `{gap_description: str, severity: str, related_papers: list[str]}` |
| `sota_comparison_summary` | str | Prose summary of positioning vs SOTA |

Source: `extracted_backend_skills_01.md §6 (CoverageGapAnalysisSkill)`

---

### Skill: CrossValidationSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Cross-validates the paper's claims against the SOTA papers to identify potential inconsistencies
or unsupported claims.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill |
| `checklist` | dict | Yes | Phase 2/2.5 output |
| `extracted_info` | dict | Yes | Phase 1 output |

#### Guard Conditions

RULE: guard_cross_validation  
CONDITION: `context.get("sota_papers")` is falsy or `context.get("checklist")` is falsy  
ACTION: Return `{"success": False, "error": "Missing sota_papers or checklist", "phase": "cross_validation"}`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `cross_validation_results` | list[dict] | Each: `{claim: str, supported: bool, evidence: str, related_paper_ids: list[str]}` |
| `unsupported_claims_count` | int | Count of claims not supported by SOTA |

Source: `extracted_backend_skills_01.md §6 (CrossValidationSkill)`

---

### Skill: LimitationsQualityDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **Yes** (one of 3 exported regex skills)

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
LIMITATIONS_PATTERNS = [
    r'\blimitation[s]?\b',
    r'\bshortcoming[s]?\b',
    r'\bweakness(?:es)?\b',
    r'\bfuture\s+work\b',
    r'\bopen\s+(?:question|problem|issue)\b',
    r'\bwe\s+(?:acknowledge|note)\s+(?:that\s+)?(?:this|our)',
    r'\bscope\s+(?:of\s+(?:this|our)\s+work|limitation)',
    r'\bnot\s+(?:address|cover|include|consider)\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `limitations_mentions` | list[str] | Matched strings |
| `limitations_section_found` | bool | `True` if a limitations section was detected |
| `limitations_quality_score` | float | Score based on specificity and depth of limitations [GAP: scoring formula not specified] |

Source: `extracted_backend_skills_01.md §5 (LimitationsQualityDetectionSkill)`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_018`

---

### Skill: SoftwareVersionDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **Yes** (one of 3 exported regex skills)

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
SOFTWARE_VERSION_PATTERNS = [
    r'\bPython\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bTensorFlow\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bPyTorch\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bscikit[_\-]learn\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bnumpy\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bpandas\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bHugging\s+Face\s+[Tt]ransformers\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bJAX\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bCUDA\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bcuDNN\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bversion\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bv\d+\.\d+(?:\.\d+)?\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `software_versions` | list[dict] | Each: `{software: str, version: str, match: str}` |
| `software_versioning_found` | bool | `True` if any version match found |

Source: `extracted_backend_skills_01.md §5 (SoftwareVersionDetectionSkill)`

---

### Skill: HardwareDetailDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **Yes** (one of 3 exported regex skills)

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
HARDWARE_PATTERNS = [
    r'\bNVIDIA\s+(?:A100|V100|H100|T4|RTX\s*\d+|Titan)',
    r'\bGPU[s]?\b',
    r'\bTPU[s]?\b',
    r'\bA100\b',
    r'\bV100\b',
    r'\bH100\b',
    r'\bRTX\s*\d{4}\b',
    r'\b\d+\s*GB\s+(?:VRAM|GPU\s+memory)\b',
    r'\bIntel\s+(?:Xeon|Core\s+i\d)',
    r'\bAMD\s+(?:EPYC|Ryzen)',
    r'\b\d+\s+(?:CPU|GPU)\s+(?:cores?|nodes?)\b',
    r'\bcluster\s+of\s+\d+',
    r'\bdistributed\s+(?:training|computing)\s+(?:on|with)\s+\d+',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `hardware_mentions` | list[str] | Matched strings |
| `hardware_details_found` | bool | `True` if any hardware detail found |
| `gpu_models` | list[str] | Distinct GPU model names detected |

Source: `extracted_backend_skills_01.md §5 (HardwareDetailDetectionSkill)`

---

<a name="section-12"></a>
## Section 12 — SOTA Analysis Pipeline (5 Steps)

Source: `extracted_backend_core_01.md §4.3`, `extracted_backend_skills_01.md §6`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_021`

### 12.1 Class: SotaAnalyzer

```python
class SotaAnalyzer:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
```

Module: `backend/services/sota_analyzer.py`

### 12.2 Entry Point

```python
def analyze(self, paper_text: str, extracted_info: dict) -> dict:
```

### 12.3 Pipeline: 5 Steps in Order

The 5 steps are executed sequentially. On any step failure, `analyze()` returns the error.

#### Step 1: Thematic Coverage (ThematicCoverageSkill)

**Trigger**: Always runs; first step  
**Input**: `paper_text`, `extracted_info`  
**Output**: `themes` (list[str]), `keywords` (list[str]), `research_area` (str)  
**Error**: Returns `{"success": False, "error": ..., "step": "thematic_coverage"}`  
**Source**: `extracted_backend_skills_01.md §6`

#### Step 2: Query Generation (QueryGenerationSkill)

**Trigger**: Runs after Step 1  
**Input**: `themes`, `keywords`, `research_area` (all from Step 1)  
**Output**: `search_queries` (list[str], 3–5 elements)  
**Error**: Returns `{"success": False, "error": ..., "step": "query_generation"}`  
**Source**: `extracted_backend_skills_01.md §6`

#### Step 3: Semantic Scholar Search (SemanticScholarSearchSkill)

**Trigger**: Runs after Step 2  
**Input**: `search_queries` (from Step 2)  
**Output**: `sota_papers` (list[dict]), `query_results` (dict)  
**Error**: Returns `{"success": False, "error": ..., "step": "semantic_scholar_search"}`

**Semantic Scholar API details** (from §11 SemanticScholarSearchSkill):
- Endpoint: `https://api.semanticscholar.org/graph/v1/paper/search`
- Auth: None (public)
- Params: `query`, `fields="paperId,title,authors,year,citationCount,abstract,url"`,
  `year="2023-2026"`, `limit=5`
- Per-query results deduplicated by `paperId` across all queries before writing to
  `sota_papers`

**Source**: `extracted_backend_core_01.md §4.3`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_021`

#### Step 4: Coverage Gap Analysis (CoverageGapAnalysisSkill)

**Trigger**: Runs after Step 3  
**Input**: `sota_papers`, `extracted_info`, `paper_text` (optional)  
**Output**: `coverage_gaps` (list[dict]), `sota_comparison_summary` (str)  
**Error**: Returns `{"success": False, "error": ..., "step": "coverage_gap_analysis"}`  
**Source**: `extracted_backend_skills_01.md §6`

#### Step 5: Cross Validation (CrossValidationSkill)

**Trigger**: Runs after Step 4 (final step)  
**Input**: `sota_papers`, `checklist`, `extracted_info`  
**Output**: `cross_validation_results` (list[dict]), `unsupported_claims_count` (int)  
**Error**: Returns `{"success": False, "error": ..., "step": "cross_validation"}`  
**Source**: `extracted_backend_skills_01.md §6`

### 12.4 Return Shape of `analyze()`

**Success:**

```python
{
    "success": True,
    "themes": list[str],
    "keywords": list[str],
    "research_area": str,
    "search_queries": list[str],
    "sota_papers": list[dict],
    "query_results": dict,
    "coverage_gaps": list[dict],
    "sota_comparison_summary": str,
    "cross_validation_results": list[dict],
    "unsupported_claims_count": int
}
```

**Failure:**

```python
{
    "success": False,
    "error": str,
    "step": str    # name of the failing step
}
```

Source: `extracted_backend_core_01.md §4.3`

---

<a name="section-13"></a>
## Section 13 — Chatbot (preguntar Flow + History)

Source: `extracted_backend_core_01.md §4.4`, `extracted_backend_skills_01.md §7`

### 13.1 Class: PaperChatbot

```python
class PaperChatbot:
    def __init__(self, llm_client: LLMClient, paper_text: str, extracted_info: dict):
        self.llm_client = llm_client
        self.paper_text = paper_text
        self.extracted_info = extracted_info
        self.conversation_history: list[dict] = []
```

Module: `backend/services/chatbot.py`

### 13.2 `preguntar()` Signature

```python
def preguntar(self, pregunta: str) -> str:
```

Parameters:
- `pregunta` (str): The user's question. Required. No length constraint documented.
- Returns: str — The LLM-generated answer.

### 13.3 Conversation History Data Structure

```python
conversation_history: list[dict]
```

Each element:

| Field | Type | Description |
|---|---|---|
| `role` | str | `"user"` or `"model"` |
| `parts` | list[str] | List with one element: the message text |

Example:

```python
[
    {"role": "user",  "parts": ["What is the learning rate used?"]},
    {"role": "model", "parts": ["The paper uses a learning rate of 0.001."]},
]
```

**Size limit**: [GAP: no maximum history size enforced — history grows unbounded in extraction data]

Source: `extracted_backend_core_01.md §4.4`

### 13.4 History Update Logic

```pseudocode
FUNCTION preguntar(pregunta):
    # Step 1: Append user question to history BEFORE LLM call
    conversation_history.append({
        "role": "user",
        "parts": [pregunta]
    })
    
    # Step 2: Build prompt with full history + paper context
    prompt = build_chat_prompt(
        conversation_history=conversation_history,
        paper_text=self.paper_text,
        extracted_info=self.extracted_info
    )
    
    # Step 3: LLM call
    response = self.llm_client.generate(
        prompt=prompt,
        config=CHAT_CONFIG,        # {"temperature": 0.2}
        history=conversation_history   # passed directly to Gemini chat API
    )
    
    # Step 4: Append model response to history AFTER LLM call
    conversation_history.append({
        "role": "model",
        "parts": [response]
    })
    
    # Step 5: Return the response
    RETURN response
```

Source: `extracted_backend_core_01.md §4.4`

### 13.5 LLM Call Details

- Config: `CHAT_CONFIG = {"temperature": 0.2}` (no JSON, plain text)
- Model: `"gemini-3.1-flash-lite-preview"`
- The Gemini `chat.send_message()` API is used (not one-shot `generate_content()`), passing
  `history` directly so the model receives the full conversation context natively.
- Paper context is injected into the system prompt or initial user turn.

Source: `extracted_backend_core_01.md §4.4`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_022`

### 13.6 Error Handling

| Condition | Behavior |
|---|---|
| LLM call raises exception | `preguntar()` propagates the exception to the caller (no internal try/catch) |
| Empty response from LLM | Returns empty string `""` (history still updated with empty model turn) |

Source: `extracted_backend_core_01.md §4.4`

### 13.7 Usage in `ConversationalResponseSkill`

`ConversationalResponseSkill.execute()` wraps `PaperChatbot.preguntar()` for use inside
the skill pipeline. It reads `question` from context, calls `preguntar(question)`, and writes
the result to `context["answer"]` and `context["updated_history"]`.

Source: `extracted_backend_skills_01.md §7`

---

<a name="section-14"></a>
## Section 14 — PDF Parser (Docling Chunked Flow)

Source: `extracted_backend_core_01.md §4.1`

### 14.1 Function Signature

```python
def convert_pdf_to_markdown(pdf_path: str, chunk_size: int = 5) -> str:
```

Module: `backend/services/pdf_parser.py`

Parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pdf_path` | str | (required) | Absolute or relative path to the PDF file |
| `chunk_size` | int | `5` | Number of pages per processing block |

Returns: `str` — Full markdown text of the document (assembled from all chunks).

### 14.2 Chunked Docling Flow

```pseudocode
FUNCTION convert_pdf_to_markdown(pdf_path, chunk_size=5):
    # Step 1: Determine total page count
    pdf_reader = open_pdf(pdf_path)
    total_pages = pdf_reader.num_pages
    
    markdown_parts = []
    
    # Step 2: Process each chunk of `chunk_size` pages
    FOR start_page FROM 0 TO total_pages STEP chunk_size:
        end_page = min(start_page + chunk_size, total_pages)
        
        # Step 3: Write chunk to temp PDF
        tmp_pdf_path = create_temp_file(suffix=".pdf")
        TRY:
            writer = PdfWriter()
            FOR page_num FROM start_page TO end_page - 1:
                writer.add_page(pdf_reader.pages[page_num])
            writer.write(tmp_pdf_path)
            
            # Step 4: Convert temp PDF with Docling
            converter = DocumentConverter()
            result = converter.convert(tmp_pdf_path)
            chunk_markdown = result.document.export_to_markdown()
            
            markdown_parts.append(chunk_markdown)
        
        EXCEPT Exception AS e:
            # Step 5: On per-chunk error, append error notice (processing continues)
            error_notice = f"\n\n<!-- Error processing pages {start_page+1}–{end_page}: {str(e)} -->\n\n"
            markdown_parts.append(error_notice)
        
        FINALLY:
            # Step 6: Always clean up temp file
            IF tmp_pdf_path exists:
                os.remove(tmp_pdf_path)
    
    # Step 7: Assemble all chunks
    RETURN "\n\n".join(markdown_parts)
```

Source: `extracted_backend_core_01.md §4.1`

### 14.3 Chunk/Fragment Sizing Parameters

| Parameter | Value | Description |
|---|---|---|
| `chunk_size` | `5` (default) | Pages per processing block |
| `chunk_overlap` | `0` | No page overlap between blocks |

### 14.4 Output Format

- Each chunk produces a markdown string from Docling's `export_to_markdown()`.
- Chunks are joined with `"\n\n"` separator.
- No additional metadata is added to the output string.
- If a chunk fails, an HTML comment error notice is inserted at that position in the output.

### 14.5 Error Handling

| Condition | Behavior |
|---|---|
| Single chunk/block fails (Docling error, corrupt pages) | Append HTML error comment; continue with next chunk |
| All chunks fail | Returns string of error comments only (no exception raised) |
| Empty PDF (0 pages) | Returns empty string `""` |
| PDF file not found | Exception from `open_pdf()` propagates to caller |
| Temp file creation fails | Exception propagates to caller |
| Temp file cleanup fails | [GAP: whether cleanup failure is silently swallowed or propagated not confirmed] |

Source: `extracted_backend_core_01.md §4.1`

---

<a name="section-15"></a>
## Section 15 — LLMClient (Retry + Backoff Logic)

Source: `extracted_backend_core_01.md §3.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_009`

### 15.1 Class

```
LLMClient
```

Module: `backend/common/llm_client.py`

### 15.2 Constructor

```python
def __init__(
    self,
    model_name: str = MODEL_NAME,         # "gemini-3.1-flash-lite-preview"
    api_key: str = GOOGLE_API_KEY,        # from environment
    max_retries: int = 5,
    base_delay: float = 2.0
):
    self.model_name = model_name
    self.api_key = api_key
    self.max_retries = max_retries        # = 5 (but loop is range(6), i.e. attempts 0–5)
    self.base_delay = base_delay          # = 2.0
    genai.configure(api_key=api_key)
    self.model = genai.GenerativeModel(model_name)
```

Source: `extracted_backend_core_01.md §3.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_009`

### 15.3 `generate()` Signature

```python
def generate(
    self,
    prompt: str,
    config: dict = None,
    history: list[dict] = None
) -> str:
```

Parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | str | (required) | Prompt string to send to the LLM |
| `config` | dict | `None` | Generation config (temperature, response_mime_type, etc.) |
| `history` | list[dict] | `None` | Conversation history for chat API (optional) |

Returns: `str` — Raw text response from the LLM.

### 15.4 Retry Loop (All 6 Attempts)

The retry loop uses `for attempt in range(6)` — attempts are numbered 0 through 5.
`max_retries=5` is the number of **retries** (not total attempts). Total attempts = 6.

#### Delay Formula

```python
delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
# base_delay = 2.0
```

| Attempt | Sleep BEFORE this attempt (seconds) | Approx delay (without jitter) |
|---|---|---|
| 0 (first) | **0** (no sleep before first attempt) | — |
| 1 (first retry) | `2.0 * (2**1) + random(0,1)` ≈ **4–5 s** | 4 s |
| 2 | `2.0 * (2**2) + random(0,1)` ≈ **8–9 s** | 8 s |
| 3 | `2.0 * (2**3) + random(0,1)` ≈ **16–17 s** | 16 s |
| 4 | `2.0 * (2**4) + random(0,1)` ≈ **32–33 s** | 32 s |
| 5 (last retry) | `2.0 * (2**5) + random(0,1)` ≈ **64–65 s** | 64 s |

Note: The sleep occurs at the **start of each iteration** (before the LLM call) using
`if attempt > 0: time.sleep(delay)` — attempt 0 has no preceding sleep.

Source: `extracted_backend_core_01.md §3.1`

### 15.5 Retryable Exception Conditions

An exception is considered retryable if its string representation contains ANY of these
substrings (case-insensitive string match, not exception type match):

| Substring | Meaning |
|---|---|
| `"503"` | HTTP 503 Service Unavailable |
| `"429"` | HTTP 429 Too Many Requests (rate limit) |
| `"UNAVAILABLE"` | gRPC UNAVAILABLE status |
| `"RESOURCE_EXHAUSTED"` | gRPC RESOURCE_EXHAUSTED (quota) |
| `"DEADLINE_EXCEEDED"` | gRPC DEADLINE_EXCEEDED (timeout) |

Source: `extracted_backend_core_01.md §3.1`

### 15.6 Non-Retryable Exceptions

Any exception whose string representation does NOT match any retryable substring is
**immediately re-raised** (no retry, no delay).

```python
if not any(code in str(e) for code in RETRYABLE_CODES):
    raise   # immediately propagate
```

### 15.7 Retry Loop Pseudocode

```pseudocode
RETRYABLE_CODES = ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"]

FUNCTION generate(prompt, config=None, history=None):
    last_exception = None
    
    FOR attempt IN range(6):   # attempts 0, 1, 2, 3, 4, 5
        IF attempt > 0:
            delay = 2.0 * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
        
        TRY:
            IF history is not None:
                # Use chat API
                chat = self.model.start_chat(history=history)
                response = chat.send_message(prompt, generation_config=config)
            ELSE:
                # Use one-shot generate_content
                response = self.model.generate_content(prompt, generation_config=config)
            
            # Attempt: show Streamlit toast (silently swallowed if not in Streamlit)
            TRY:
                streamlit.toast(f"LLM call succeeded on attempt {attempt+1}")
            EXCEPT:
                PASS
            
            RETURN response.text
        
        EXCEPT Exception AS e:
            last_exception = e
            
            IF NOT any(code IN str(e) for code IN RETRYABLE_CODES):
                RAISE e   # non-retryable: fail immediately
            
            # retryable: log and continue to next attempt
            log_warning(f"Retryable error on attempt {attempt}: {e}")
    
    # All 6 attempts exhausted
    RAISE last_exception
```

Source: `extracted_backend_core_01.md §3.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_009`

### 15.8 JSON Repair Patterns

Applied after receiving raw LLM text, before JSON parsing (in skills that expect JSON output):

1. **Strip markdown fences**: remove ` ```json ` ... ` ``` ` wrapper if present.
2. **Strip trailing commas**: regex replace `,\s*}` → `}` and `,\s*]` → `]`.
3. **Balanced JSON extraction**: use the brace-stack algorithm (§2.8) to extract the first
   complete `{...}` object.

Note: These repairs are applied in the calling skill's `execute()` method, NOT inside
`LLMClient.generate()`. `generate()` returns the raw string.

Source: `extracted_backend_core_01.md §3.1`, `extracted_backend_skills_01.md §3.2`

### 15.9 Return Type

**Success**: `str` — raw LLM response text (may contain markdown fences, trailing commas, etc.)

**Failure**: raises the last exception after all 6 attempts are exhausted.

---

<a name="section-16"></a>
## Section 16 — Prompt Template Functions (All 6)

Source: `extracted_backend_core_01.md §2.2`

Module: `backend/common/prompts.py`

---

### Function: `get_extraction_prompt()`

#### Signature

```python
def get_extraction_prompt(paper_text: str, red_flags: list[str]) -> str:
```

#### Purpose

Full single-pass extraction prompt. Instructs the LLM to extract 17 information categories
from the complete paper text.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `paper_text` | str | Full paper text block in the prompt |
| `red_flags` | list[str] | Formatted list of red-flag pattern strings |

#### Output (Prompt String Structure)

The prompt instructs the LLM to return a JSON object containing the following 17 top-level categories:

1. `title` — paper title
2. `authors` — list of author names
3. `abstract` — abstract text
4. `contributions` — main claimed contributions
5. `methodology` — description of methodology
6. `experiments` — experimental setup details
7. `results` — key results and metrics
8. `datasets` — datasets used (name, size, source, availability)
9. `code_availability` — code/implementation availability
10. `computational_requirements` — hardware, compute budget, runtime
11. `hyperparameters` — all hyperparameter values (learning rate, batch size, etc.)
12. `statistical_testing` — statistical tests and significance reporting
13. `limitations` — acknowledged limitations
14. `future_work` — stated future work
15. `red_flags_found` — which of the injected `red_flags` were detected
16. `reproducibility_indicators` — binary indicators for reproducibility checklist
17. `additional_notes` — any other relevant extraction

#### Skills Using This Template

- `HybridHyperparameterExtractionSkill` (Phase 1.5, RAG per-chunk pass)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_map_extraction_prompt()`

#### Signature

```python
def get_map_extraction_prompt(fragment_text: str) -> str:
```

#### Purpose

Per-fragment MAP extraction prompt. Used in Phase 1 MAP phase for each paper fragment.
Lighter than the full extraction — focuses on extracting structured information from a
single paper section.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `fragment_text` | str | The text of one paper fragment/section |

#### Output (Prompt String Structure)

- Instructs the LLM to return a JSON object with a subset of the 17 categories
  (limited to what is extractable from a fragment without full-paper context).
- Includes instruction to mark uncertain extractions with a confidence level.

#### Skills Using This Template

- `InformationExtractionSkill` (Phase 1, MAP phase)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_reduce_extraction_prompt()`

#### Signature

```python
def get_reduce_extraction_prompt(map_results: list[dict]) -> str:
```

#### Purpose

REDUCE consolidation prompt. Takes all MAP outputs and instructs the LLM to merge them
into a single canonical extraction, resolving duplicates and conflicts.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `map_results` | list[dict] | JSON-serialized list of all per-fragment MAP outputs |

#### Output (Prompt String Structure)

- Instructs the LLM to return a single JSON object with the full 17-category schema.
- Includes explicit deduplication and conflict-resolution instructions (e.g., prefer
  more specific values over vague ones, merge lists, avoid duplication).

#### Skills Using This Template

- `InformationExtractionSkill` (Phase 1, REDUCE phase)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_evaluation_signals()`

#### Signature

```python
def get_evaluation_signals(extracted_info: dict) -> dict:
```

#### Purpose

**NOT a prompt function.** Computes 6 binary/numeric signals from `extracted_info` using
Python logic only (no LLM call). Returns a `signals` dict.

#### Required Parameters

| Parameter | Type | Description |
|---|---|---|
| `extracted_info` | dict | Phase 1 output (full extraction) |

#### Output: 6 Signal Keys

| Key | Type | Derivation |
|---|---|---|
| `has_code` | bool | `True` if `extracted_info.get("code_availability")` is truthy |
| `has_data` | bool | `True` if `extracted_info.get("datasets")` is non-empty |
| `has_hyperparams` | bool | `True` if `extracted_info.get("hyperparameters")` is non-empty |
| `has_statistics` | bool | `True` if `extracted_info.get("statistical_testing")` is truthy |
| `has_hardware` | bool | `True` if `extracted_info.get("computational_requirements")` is truthy |
| `has_limitations` | bool | `True` if `extracted_info.get("limitations")` is truthy |

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_evaluation_prompt()`

#### Signature

```python
def get_evaluation_prompt(extracted_info: dict, red_flags: list[str]) -> str:
```

#### Purpose

Main NeurIPS 2026 checklist evaluation prompt. Instructs the LLM to evaluate 16 checklist
items based on the full extracted information.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `extracted_info` | dict | JSON-serialized full extraction |
| `red_flags` | list[str] | Formatted list of red-flag pattern strings |

#### Output (Prompt String Structure)

- Defines all 16 NeurIPS 2026 checklist item keys and their descriptions.
- Instructs the LLM to return a JSON object with each item key mapped to
  `{answer: "Yes"|"No"|"N/A", justification: str, evidence: str}`.
- Includes scoring guidelines (what counts as "Yes" vs "No" for each item).

[GAP: the exact 16 checklist item keys and their scoring criteria are embedded in the prompt
template text; they are not separately enumerated in the extraction data outside of the prompt]

#### Skills Using This Template

- `ReproducibilityEvaluationSkill` (Phase 2)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_verification_prompt()`

#### Signature

```python
def get_verification_prompt(
    item_key: str,
    item_data: dict,
    paper_context: str
) -> str:
```

#### Purpose

Second-pass verification prompt. Used in Phase 2.5 to re-evaluate individual checklist
items with focused paper context.

#### Required Parameters Injected into Template

| Parameter | Type | Description |
|---|---|---|
| `item_key` | str | The checklist item key to re-verify (e.g., `"code_released"`) |
| `item_data` | dict | The Phase 2 evaluation for this item: `{answer, justification, evidence}` |
| `paper_context` | str | Truncated paper text: `paper_text[:30000] + paper_text[-30000:]` |

#### Output (Prompt String Structure)

- Presents the current evaluation (`item_data`) and the focused paper context.
- Asks the LLM: "Given this paper context, is the original evaluation correct?"
- Returns JSON: `{revised_answer: str, is_changed: bool, new_justification: str, new_evidence: str}`.

#### Skills Using This Template

- `ChecklistVerificationSkill` (Phase 2.5)

Source: `extracted_backend_core_01.md §2.2`

---

## Appendix A — Configuration Constants

Source: `extracted_backend_core_01.md §2.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_010`

Module: `backend/common/config.py`

| Constant | Value | Type | Description |
|---|---|---|---|
| `MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | str | LLM model for all audit calls |
| `EMBEDDING_MODEL` | `"gemini-embedding-2"` | str | Embedding model for RAG |
| `GOOGLE_API_KEY` | (from environment) | str | Google Gemini API key |
| `AUDIT_CONFIG` | `{"response_mime_type": "application/json", "temperature": 0.0, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384}` | dict | Config for all audit LLM calls |
| `CHAT_CONFIG` | `{"temperature": 0.2}` | dict | Config for chatbot LLM calls |
| `SOTA_CONFIG` | `{"response_mime_type": "application/json", "temperature": 0.1}` | dict | Config for SOTA analysis LLM calls |
| `AUDIT_VERSION` | [GAP: version string not enumerated in extraction] | str | Pipeline version tag |

Source: `extracted_backend_core_01.md §2.1`

---

## Appendix B — Dependencies

Source: `extracted_root_tests_scratch_01.md §requirements`

Key Python packages required:

| Package | Purpose |
|---|---|
| `google-generativeai` | Gemini LLM and embedding API |
| `chromadb` | In-memory vector database for RAG |
| `langchain` | `RecursiveCharacterTextSplitter` fallback for fragmentation |
| `docling` | PDF-to-markdown conversion |
| `pypdf` | PDF page-level operations (chunk writing) |
| `requests` | Semantic Scholar HTTP calls |
| `streamlit` | UI framework (toast calls in LLMClient silently swallowed outside Streamlit) |

Missing from `requirements.txt` (noted in extraction):  
`[GAP: reportlab not listed in requirements.txt but referenced in tests]`  
`[GAP: markdown2 not listed in requirements.txt but referenced in scratch scripts]`

Source: `extracted_root_tests_scratch_01.md §requirements`

---

## Appendix C — Unresolved GAPs from Cross-Reference Analysis

Source: `cross_ref_resolution_cross_ref_root_to_backend.md §RESOLUTION SUMMARY`

The following items were identified as UNRESOLVED in the cross-reference analysis:

| GAP ID | Description | Confidence |
|---|---|---|
| g_001 | `PaperAuditor._preprocess_paper()` — method removed during refactoring; no source code | UNRESOLVED |
| g_002 | `REGEX_PATTERNS` in `auditor.py` — removed; now lives as class-level `PATTERNS` per skill | UNRESOLVED |
| g_003 | `AuditState`, `ExtractedInfo`, `ChecklistItem` TypedDicts — `backend/common/audit_state.py` absent from repo | UNRESOLVED |
| g_004 | `NEGATION_PATTERNS` usage in `auditor.py` tests — references removed code | UNRESOLVED |

Full unresolved items verbatim:

`[GAP: _preprocess_paper behavior unresolved — removed during refactoring; no source available]`

`[GAP: AuditState / ExtractedInfo / ChecklistItem — backend/common/audit_state.py not found in repo; these TypedDicts may have been deleted during refactoring]`

`[GAP: NEGATION_PATTERNS used in auditor.py test references — the patterns were moved to per-skill class-level PATTERNS; original auditor.py usage unresolved]`

Source: `cross_ref_resolution_cross_ref_root_to_backend.md §RESOLUTION SUMMARY`

---

## Appendix D — Known Bugs and Risks

Source: `extracted_backend_core_01.md §GAP-cluster_backend_core_01-012`

### Bug D.1: Potential `NameError` in `PaperAuditor.audit()` outer `except` block

**Location**: `auditor.py:201` (outer except block)

**Description**: `end_time` is assigned at the start of Phase 3 processing (approximately
line 176). If an exception is raised before that line (i.e., in Phases 1, 1.5, or 2),
`end_time` is unbound. The outer `except` block references `end_time` for error reporting,
which would raise a secondary `NameError`, masking the original exception.

**Risk**: Any exception in Phase 1 or Phase 2 may be silently lost and replaced by a
`NameError: name 'end_time' is not defined`.

**Mitigation (recommended for reimplementation)**: Initialize `end_time = 0.0` (or
`end_time = start_time`) at the top of `audit()` before the phase loop, then update it
at Phase 3 entry.

Source: `extracted_backend_core_01.md §GAP-cluster_backend_core_01-012`

---

*End of Functional Backend Specification — `02_functional_backend.md`*
*Generated from extraction files: `extracted_backend_core_01.md`, `extracted_backend_skills_01.md`,*
*`extracted_root_tests_scratch_01.md`, `cross_ref_resolution_cross_ref_root_to_backend.md`*


### 02_functional_frontend.md (58700 chars)
# 02 — Frontend Functional Specification

**Writer agent:** functional_writer_frontend  
**Sources consumed:**
- `extracted_frontend_01.md` (primary extraction — cluster_frontend_01)
- `extracted_root_tests_scratch_01.md` (primary extraction — cluster_root_tests_scratch_01)
- `cross_ref_resolution_cross_ref_root_to_frontend.md` (gap resolutions g_004–g_008, g_013, g_026, g_027)

---

## 1. Application Bootstrap Sequence

The application entry point is `frontend/app.py` (74 lines). All steps execute on every Streamlit rerun, top-to-bottom, in the order documented below.

(Source: extracted_frontend_01.md §4.2 Top-level rendering order)

---

### Step 1 — `st.set_page_config`

```
TRIGGER: Python module load of app.py (executed before any widget statement)
CONDITION: Must be the first Streamlit call; comment in source: "IMPORTANTE: configure_page() debe ser lo primero"
ACTION: st.set_page_config(
    page_title="NeurIPS 2026 Checklist Auditor",
    layout="wide",
    page_icon="🔬"
)
RESULT: Browser tab shows "NeurIPS 2026 Checklist Auditor" with microscope icon; page uses wide layout.
```

Note: `extracted_root_tests_scratch_01.md §3.2` records `page_title="Nature Auditor Pro"` from a later version of `app.py`. The frontend cluster extraction (`extracted_frontend_01.md §2.2`) records `page_title="NeurIPS 2026 Checklist Auditor"`. Both sources agree on `layout="wide"` and `page_icon="🔬"`. The most specific and authoritative value is `"NeurIPS 2026 Checklist Auditor"` (Source: extracted_frontend_01.md §2.2, app.py:6-10).

Additionally, before any Streamlit import, `app.py` sets the following environment variables unconditionally at module-load time:

| Variable | Value set | Purpose |
|----------|-----------|---------|
| `TRANSFORMERS_VERBOSITY` | `"error"` | Suppresses transformers library logs |
| `TOKENIZERS_PARALLELISM` | `"false"` | Suppresses tokenizer parallelism warnings |
| `ANONYMIZED_TELEMETRY` | `"False"` | Disables ChromaDB telemetry |
| `OTEL_SDK_DISABLED` | `"true"` | Disables OpenTelemetry SDK (avoids Streamlit conflicts) |

Also sets three `warnings.filterwarnings("ignore", ...)` calls and `logging.getLogger("transformers").setLevel(logging.ERROR)` (Source: extracted_root_tests_scratch_01.md §3.1, app.py:13-22).

---

### Step 2 — `apply_custom_styles`

```
TRIGGER: Immediately after st.set_page_config; SOURCE: app.py:21
CONDITION: None (unconditional call)
ACTION: Calls apply_custom_styles() from frontend.styles.custom_css
RESULT: Injects the CUSTOM_CSS <style> block via st.markdown(CUSTOM_CSS, unsafe_allow_html=True).
        CSS targets: .stApp background, #MainMenu, footer, header, [data-testid="stTable"] family,
        and [data-testid="stPlotlyChart"]. Full CSS detail in Section 2 of this spec is referenced
        here; see also §2.6 of the extraction.
```

(Source: extracted_frontend_01.md §6 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_026)

---

### Step 3 — `initialize_session_state`

```
TRIGGER: Immediately after apply_custom_styles(); SOURCE: app.py:22
CONDITION: None (unconditional call); internally each key is guarded by "if key not in st.session_state"
ACTION: Calls initialize_session_state() from frontend.utils.session_state
RESULT: Ensures 5 session state keys exist with their defaults.
        Full schema documented in Section 2.
```

(Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_027)

---

### Step 4 — Sidebar render

```
TRIGGER: Executed as part of app.py sidebar block; SOURCE: app.py:73-76
CONDITION: None (unconditional; sidebar is always shown)
ACTION:
  st.image(SIDEBAR_IMAGE, width=150)
  st.markdown("### Sobre el TFG")
  st.write(SIDEBAR_DESCRIPTION)
RESULT: Sidebar displays ACM logo (150px wide) and a descriptive paragraph.
```

Constants used (Source: extracted_frontend_01.md §2.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_008):
- `SIDEBAR_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"`
- `SIDEBAR_DESCRIPTION = "Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."`

---

### Step 5 — Page title and "Limpiar" button

```
TRIGGER: After sidebar block setup; SOURCE: app.py:25-32
ACTION:
  st.title(TITLE)        — renders page heading with TITLE constant
  st.markdown("---")     — horizontal rule
  st.button("🔄 Limpiar y subir nuevo archivo", key not specified)
CONDITION (on button): if clicked → delete ALL st.session_state keys → st.rerun()
RESULT: Title constant is "💻 Auditor de Papers en Ciencias de la Computación".
        Clicking the "Limpiar" button resets the entire application state.
```

(Source: extracted_frontend_01.md §4.2 / §8 RULE:ClearAndReset, app.py:25-32)

---

### Step 6 — File upload widget

```
TRIGGER: After title+button; SOURCE: app.py:34
ACTION:
  uploaded_file = st.file_uploader(
      "Sube el PDF del artículo científico",
      type=["pdf", "txt", "md"]
  )
RESULT: Widget rendered; uploaded_file is None until user selects a file.
```

(Source: extracted_frontend_01.md §5.1, app.py:34)

---

### Step 7 — Conditional: if uploaded_file is not None

```
TRIGGER: uploaded_file is not None (user has uploaded a file)
CONDITION: `if uploaded_file:`
ACTION sequence (SOURCE: app.py:37-70):
  7a. process_uploaded_file(uploaded_file)        — see Section 3
  7b. resultado = st.session_state.get('resultado')
      md_text  = st.session_state.get('md_text')
  7c. Branch on resultado content:
      - resultado["error"] == "INVALID_PAPER_TYPE"
            → st.error(f"❌ Paper no válido: {resultado.get('message', 'Solo se evalúan papers de ML/AI')}")
      - "error" in resultado (other)
            → st.error(f"❌ Error en la auditoría: {err}")
      - "evaluation_error" in resultado
            → st.error(f"❌ Error del LLM: {evaluation_error}")
              st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")
              st.info("💡 Tip: Recarga la página o sube el archivo nuevamente.")
      - resultado.get("claims") is truthy (SUCCESS PATH):
            → Step 7d (render_audit_results)
            → Step 7e (render_sota_analysis)
            → Step 7f (render_chatbot)
            → Step 7g (download button)
      - resultado truthy but no "claims" and no error keys
            → st.error("⚠️ La auditoría no generó resultados válidos.")
              st.info("Posibles causas: respuesta vacía del LLM o JSON inválido.")
      - resultado is falsy/None
            → st.warning("⚠️ No hay resultado disponible.")
```

---

### Step 7d — `render_audit_results`

```
TRIGGER: resultado.get("claims") is truthy; SOURCE: app.py:52 / app.py:66
CONDITION: SUCCESS PATH only
ACTION: puntuacion = render_audit_results(resultado, uploaded_file)
RESULT: Renders full audit results page (verdict, metrics, RAG ficha, compliance table, expanders).
        Returns health dict (stored as puntuacion). See Section 4.
```

---

### Step 7e — `render_sota_analysis`

```
TRIGGER: Immediately after render_audit_results; SOURCE: app.py:53 / app.py:67
CONDITION: SUCCESS PATH only
ACTION: render_sota_analysis(md_text)
RESULT: Renders SOTA analysis section with on-demand button trigger. See Section 7.
```

---

### Step 7f — `render_chatbot`

```
TRIGGER: Immediately after render_sota_analysis; SOURCE: app.py:54 / app.py:68
CONDITION: SUCCESS PATH only
ACTION: render_chatbot(md_text)
RESULT: Renders interactive chatbot section. See Section 8.
```

---

### Step 7g — Download report button

```
TRIGGER: After render_chatbot; SOURCE: app.py:57-65 / app.py:73-79
CONDITION: SUCCESS PATH only
ACTION:
  reporte = generate_report(resultado, uploaded_file, puntuacion)
  st.download_button(
      label="📥 Descargar Informe Completo (.md)",
      data=reporte,
      file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md",
      mime="text/markdown"
  )
RESULT: User can download the Markdown audit report.
```

(Source: extracted_frontend_01.md §4.2 / §10.8)

---

## 2. Session State Schema and Initialization

`initialize_session_state()` is defined in `frontend/utils/session_state.py` (22 lines). It uses the guard `if "key" not in st.session_state` for every key — the function is idempotent and will NOT overwrite keys already set. (Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_027, session_state.py:7)

### 2.1 Keys initialised by `initialize_session_state`

| Key | Type | Default | Guard Condition | Purpose | Source |
|-----|------|---------|-----------------|---------|--------|
| `resultado` | `dict` or `None` | `None` | `if "resultado" not in st.session_state` | Holds the full audit result dict returned by `auditor.audit()`; `None` before first audit; `{"error": ...}` on failure | session_state.py:8-9 |
| `auditor` | `PaperAuditor` instance | `PaperAuditor()` | `if 'auditor' not in st.session_state` | Backend audit engine; exposes `audit(md_text, status_callback)` | session_state.py:11-12 |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | `if 'chatbot' not in st.session_state` | Backend chatbot engine; exposes `preguntar(md_text, question, history_str)` | session_state.py:14-15 |
| `sota_analyzer` | `SotaAnalyzer` instance | `SotaAnalyzer()` | `if 'sota_analyzer' not in st.session_state` | Backend SOTA analysis engine; exposes `analyze_sota(md_text)` | session_state.py:17-18 |
| `messages` | `list` of dicts | `[]` | `if "messages" not in st.session_state` | Chat history; each entry is `{"role": str, "content": str}` | session_state.py:20-21 |

### 2.2 Additional session state keys set lazily by `file_uploader.py`

These keys are NOT set by `initialize_session_state`; they are written on first (or new) file upload.

| Key | Type | Initial Value | Set When | Read When | Source |
|-----|------|---------------|----------|-----------|--------|
| `archivo_actual` | `str` | not pre-set | `file_uploader.py:19` — set to `uploaded_file.name` | `file_uploader.py:16` — compared to detect file change | file_uploader.py:19 |
| `file_hash` | `str` (MD5 hex, 32 chars) | not pre-set | `file_uploader.py:20` — set to `hashlib.md5(uploaded_file.getvalue()).hexdigest()` | `file_uploader.py:17` — compared to detect content change | file_uploader.py:20 |
| `md_text` | `str` | not pre-set | `file_uploader.py:36` (PDF) or `file_uploader.py:39` (TXT/MD) | `chatbot.py:26`; `sota_section.py:12`; `app.py:53-54`; `file_uploader.py:98` | file_uploader.py:36,39 |

---

## 3. File Upload Flow (`process_uploaded_file`)

**File:** `frontend/components/file_uploader.py` (101 lines)  
**Function signature:** `process_uploaded_file(uploaded_file)` — no type annotations; `uploaded_file` is a Streamlit `UploadedFile` object.  
**Return value:** `tuple (md_text: str, resultado: dict)` — both values are read from `st.session_state` at the end of the function: `st.session_state.get('md_text', '')` and `st.session_state.get('resultado', {})`.  
(Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_004, file_uploader.py:6,98-100)

---

### 3.1 MD5 Deduplication

```
TRIGGER: process_uploaded_file called with an uploaded file object.
CONDITION:
  1. file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()   (SOURCE: file_uploader.py:11-12)
  2. Check: ("archivo_actual" not in st.session_state)
         OR (st.session_state.archivo_actual != uploaded_file.name)
         OR (st.session_state.get('file_hash') != file_hash)
                                                                    (SOURCE: file_uploader.py:15-17)
ACTION (if condition TRUE — new file detected):
  - Proceed to full processing pipeline (steps 3.2 – 3.4).
ACTION (if condition FALSE — same file already processed):
  - Skip all processing.
  - Return (st.session_state.get('md_text', ''), st.session_state.get('resultado', {})) immediately.
                                                                    (SOURCE: file_uploader.py:15-101)
```

---

### 3.2 File Type Branching

When a new file is detected, the following steps execute in order before audit invocation:

```
STEP 1:
  st.session_state.archivo_actual = uploaded_file.name             SOURCE: file_uploader.py:19
  st.session_state.file_hash      = file_hash                      SOURCE: file_uploader.py:20
  st.session_state.messages       = []                             SOURCE: file_uploader.py:21

STEP 2: Create temp directory and write temp file
  os.makedirs("temp")   (if "temp/" directory does not exist)      SOURCE: file_uploader.py:23-24
  temp_path = os.path.join("temp", uploaded_file.name)
  Write uploaded_file bytes to temp_path                           SOURCE: file_uploader.py:26-28

STEP 3: Determine file type
  CONDITION: file_extension = uploaded_file.name.rsplit('.', 1)[-1].lower()
  DETECTION: by file extension (not MIME type)                     SOURCE: file_uploader.py:35-42

STEP 4 — Extraction (inside st.spinner("📂 Extrayendo texto...")):
  ACTION (PDF branch):
    if file_extension == 'pdf':
      st.session_state.md_text = convert_pdf_to_markdown(temp_path)
      — convert_pdf_to_markdown is CROSS-REFERENCE: backend/services/pdf_parser.py
                                                                    SOURCE: file_uploader.py:35-36
  ACTION (TXT/MD branch):
    elif file_extension in ['txt', 'md']:
      with open(temp_path, 'r', encoding='utf-8') as f:
        st.session_state.md_text = f.read()
                                                                    SOURCE: file_uploader.py:37-39
  ERROR (unsupported extension):
    else:
      st.error(f"❌ Formato no soportado: {file_extension}")
      return (None, {'error': 'Formato no soportado: {file_extension}'})
                                                                    SOURCE: file_uploader.py:41-42
```

(Source: extracted_frontend_01.md §5.1, §2.8)

---

### 3.3 Auditor Invocation

```
TRIGGER: After successful file parsing (st.session_state.md_text is set).

STEP 1: Open status block
  status = st.status("🧠 Analizando el documento...", expanded=True)
                                                                    SOURCE: file_uploader.py:45
STEP 2: Define status_callback
  def update_status(msg):
      st.write(msg)
  — This callback receives progress messages from the backend and renders them
    as text inside the st.status block during processing.
                                                                    SOURCE: file_uploader.py:46-47
STEP 3: Invoke auditor
  ACTION: st.session_state.resultado = st.session_state.auditor.audit(
              st.session_state.md_text,
              status_callback=update_status
          )
  — Returns a dict with keys: the 16 CHECKLIST_KEYS plus optional keys:
    "metricas", "informacion_extraida", "general_analysis_map",
    "original_extraction_raw", "hybrid_triage_fragments",
    "extracted_hyperparameters_hybrid", "evaluation_signals"
  — On error: returns dict with key "error" (str)
                                                                    SOURCE: file_uploader.py:49-52

STEP 4: Error handling on resultado
  CONDITION: "error" in resultado
    Sub-condition A (SATURATION):
      any(x in str(resultado['error']).upper() for x in
          ["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"])
      ACTION:
        status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)
        st.error("### ⚠️ El servicio de IA está saturado")
        Renders expander with explanation text.
        Renders st.info with retry guidance.
        Renders 2 buttons:
          "🔄 Reintentar ahora" → st.rerun()
          "🚫 Cancelar ejecución" → st.session_state.resultado = {"error": "Ejecución cancelada..."}
                                    → st.stop()
        Calls st.stop() to halt normal flow.
                                                                    SOURCE: file_uploader.py:56-88
    Sub-condition B (non-saturation error):
      ACTION:
        status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)
        st.error(f"❌ Error crítico: {error_msg}")
        st.session_state.resultado = {"error": error_msg}
        Delete temp file if exists.
        st.stop()
                                                                    SOURCE: file_uploader.py:86-88

STEP 5 (SUCCESS):
  status.update(label="✅ Análisis completado", state="complete", expanded=False)
  st.success("✅ Análisis completado")
                                                                    SOURCE: file_uploader.py:90-92
```

(Source: extracted_frontend_01.md §5.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_004)

---

### 3.4 Temp File Lifecycle

```
CREATION:
  Directory: "temp/" (relative to working directory)
  Path: temp_path = os.path.join("temp", uploaded_file.name)
  Creation trigger: os.makedirs("temp") called before writing
                                                                    SOURCE: file_uploader.py:23-24

WRITE:
  File bytes written immediately after directory creation.
                                                                    SOURCE: file_uploader.py:26-28

DELETION:
  os.remove(temp_path) — called if temp file exists after processing (success or non-saturation error)
  Pattern: guarded check (if os.path.exists(temp_path)) before removal
                                                                    SOURCE: file_uploader.py:94-95

NOTE: No try/finally is explicitly documented in extraction data; deletion occurs in the
  error-handling path (non-saturation) and in the success path.
  [GAP: exact try/finally or context-manager structure around temp file lifecycle not confirmed in extraction]

OS CONSIDERATIONS: Requires filesystem write permission for the "temp/" relative directory.
  If unavailable (e.g., read-only container filesystem), processing will fail with an OS error.
                                                                    SOURCE: GAP-ext_frontend_01-006
```

---

## 4. Audit Results Rendering (`render_audit_results`)

**File:** `frontend/components/audit_results.py` (317 lines)  
**Function signature:** `render_audit_results(resultado: dict, uploaded_file) -> health: dict`  
**Return value:** `dict` returned by `get_checklist_health(resultado)` — keys: `"status"`, `"items"`, `"pending_count"`, `"total"`. (Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_005, audit_results.py:90,284)

Widgets rendered in the following order:

---

### 4.1 Success Banner

```
TRIGGER: Function entry (unconditional).
ACTION: st.success("Auditoria Finalizada")
CONDITION: Always displayed when render_audit_results is called.
```

(Source: extracted_frontend_01.md §5.2 step 1, audit_results.py:92)

---

### 4.2 Health Verdict

```
TRIGGER: After st.success banner.
ACTION:
  health = get_checklist_health(resultado)          SOURCE: audit_results.py:94
  pending = health["pending_count"]
  total   = health["total"]
  st.header("Veredicto del Checklist NeurIPS 2026") SOURCE: audit_results.py:100

CONDITION (health["status"] == "valid"):
  Renders dark-green <div> containing:
    - Text: "Checklist Valido"
    - Sub-text: "Todas las respuestas tienen evidencia o justificacion documentada.
                 El checklist esta listo para NeurIPS."
                                                    SOURCE: audit_results.py:102-109

CONDITION ELSE (health["status"] == "risk"):
  Renders dark-red <div> containing:
    - Text: "Riesgo de Desk Reject"
    - Sub-text: f"{pending} de {total} item(s) requieren accion del autor antes del envio."
                                                    SOURCE: audit_results.py:111-117
```

(Source: extracted_frontend_01.md §5.2 step 4)

---

### 4.3 4-Column Metrics Row

```
TRIGGER: After health verdict block.
ACTION: Creates 4 Streamlit columns; renders one st.metric per column.
                                                    SOURCE: audit_results.py:121-133

Column layout:
  col1: st.metric("Items Yes",  <count of items where "yes" in item["answer"].lower()>)
  col2: st.metric("Items No",   <count of items where "no"  in item["answer"].lower()>)
  col3: st.metric("Items N/A",  <count of items where "n/a" in item["answer"].lower()>)
  col4: st.metric("Tiempo",     f"{tiempo}s")
        where tiempo = resultado.get("metricas", {}).get("tiempo_segundos", "N/A")
```

(Source: extracted_frontend_01.md §5.2 step 5)

---

### 4.4 RAG Ficha Técnica

```
TRIGGER: After metrics row.
CONDITION: rag_data = resultado.get("extracted_hyperparameters_hybrid", {}) — displayed only if truthy.
ACTION:
  st.subheader("🎯 Ficha Técnica de Entrenamiento (RAG Specialist)")
  st.caption("Estos datos han sido extraídos mediante un escaneo profundo (RAG)
              de las secciones técnicas y apéndices.")
  Layout: 4 columns (c1, c2, c3, c4)
  c1: st.code(rag_data.get("optimizer",      "N/A"))
      st.code(rag_data.get("learning_rate",  "N/A"))
  c2: st.code(rag_data.get("batch_size",     "N/A"))
      st.code(rag_data.get("epochs",         "N/A"))
  c3: st.code(rag_data.get("warmup_steps",   "N/A"))
      st.code(rag_data.get("weight_decay",   "N/A"))
  c4: st.info(rag_data.get("hardware",       "N/A"))
      st.code(rag_data.get("random_seed",    "N/A"))
        — shown only if rag_data.get("random_seed") AND rag_data.get("random_seed") != "NOT FOUND"
                                                    SOURCE: audit_results.py:136-163
```

(Source: extracted_frontend_01.md §5.2 step 6)

---

### 4.5 Compliance Table (`_build_table_html`)

```
TRIGGER: After RAG Ficha Técnica.
ACTION:
  st.header("Tabla de Cumplimiento NeurIPS 2026")
  st.caption(...)  — colour legend caption
  table_html = _build_table_html(health["items"])
  st.html(table_html)
                                                    SOURCE: audit_results.py:167-175
```

#### `_build_table_html(items: list) -> str`

(Source: extracted_frontend_01.md §5.2.1, audit_results.py:7-87)

**Parameters:** `items` — list of 16 item dicts from `get_checklist_health()`.  
**Returns:** Complete HTML table string.

**Per-row logic:**

```
For each item dict in items:
  1. Split item["label"] on ". " to get num and name:
       if ". " in item["label"]:
           num, name = item["label"].split(". ", 1)
       else:
           num = str(idx)   # 1-based iteration index
           name = item["label"]
                                                    SOURCE: audit_results.py:39-42

  2. evidence_text:
       item["evidence"] if item["evidence"] and item["evidence"] != "-" else ""
                                                    SOURCE: audit_results.py:44

  3. Row background (from row_bg(item)):
       pending_justification == True       → "#450a0a"  (deep red — Critical risk)
       missing_evidence == True OR         → "#452e0a"  (amber/orange — Warning)
         alert_msg non-empty
       "yes" in answer (lowercased)        → "#064e3b"  (emerald green — OK)
       all other cases                     → "#111827"  (neutral dark)
                                                    SOURCE: audit_results.py:18-32

  4. Badge HTML (for Respuesta column):
       "yes" in answer.lower() → background:#065f46; color:#6ee7b7; text:"Yes"
       "no"  in answer.lower() → background:#7f1d1d; color:#fca5a5; text:"No"
       else  (N/A)             → background:#1e3a5f; color:#93c5fd; text:"N/A"
                                                    SOURCE: audit_results.py:10-16

  5. Evidence cell HTML:
       if evidence_text non-empty → <span style="color:#d1d5db;">{evidence_text}</span>
       else                       → <em style="color:#6b7280;">No disponible</em>
                                                    SOURCE: audit_results.py:48

  6. Alert line HTML:
       if item["pending_justification"]:
           alert HTML = <div style="color:#fca5a5;...">&#9888; Sin justificacion del autor &mdash;
                        Riesgo de Desk Reject</div>
                                                    SOURCE: audit_results.py:52-53
       elif item["missing_evidence"]:
           alert HTML = <div style="color:#fde68a;...">&#9888; Respuesta Yes sin evidencia de
                        seccion del paper</div>
                                                    SOURCE: audit_results.py:54-55
       Additionally: if "compensacion" in item.get("alert_msg","").lower()
                       OR "etica" in item.get("alert_msg","").lower():
           Append: <div style="color:#fde68a;...">&#9888; NeurIPS Code of Ethics:
                   compensacion minima obligatoria</div>
                                                    SOURCE: audit_results.py:57-58

  7. Row HTML: <tr> with 4 <td> cells: number, name, badge HTML, evidence+alert HTML.
```

**Generated HTML table structure:**

```html
<table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
  <thead>
    <tr>
      <th>#</th>
      <th>Item del Checklist</th>
      <th>Respuesta</th>
      <th>Evidencia / Justificacion</th>
    </tr>
  </thead>
  <tbody>
    <!-- 16 rows, one per CHECKLIST_KEY -->
  </tbody>
</table>
```

(Source: audit_results.py:69-87)

#### 16 CHECKLIST_KEYS and CHECKLIST_LABELS

| # | CHECKLIST_KEY | CHECKLIST_LABEL | Source |
|---|---------------|-----------------|--------|
| 1 | `claims` | `"1. Claims"` | scoring.py:8,17 |
| 2 | `limitations` | `"2. Limitations"` | scoring.py:9,18 |
| 3 | `theory_assumptions_proofs` | `"3. Theory, Assumptions & Proofs"` | scoring.py:10,19 |
| 4 | `experimental_result_reproducibility` | `"4. Experimental Result Reproducibility"` | scoring.py:11,20 |
| 5 | `open_access_data_code` | `"5. Open Access to Data and Code"` | scoring.py:12,21 |
| 6 | `experimental_setting_details` | `"6. Experimental Setting / Details"` | scoring.py:13,22 |
| 7 | `experiment_statistical_significance` | `"7. Experiment Statistical Significance"` | scoring.py:14,23 |
| 8 | `experiments_compute_resource` | `"8. Experiments Compute Resource"` | scoring.py:14,24 |
| 9 | `code_of_ethics` | `"9. Code of Ethics"` | scoring.py:15,25 |
| 10 | `broader_impacts` | `"10. Broader Impacts"` | scoring.py:15,26 |
| 11 | `safeguards` | `"11. Safeguards"` | scoring.py:15,27 |
| 12 | `licenses` | `"12. Licenses"` | scoring.py:15,28 |
| 13 | `assets` | `"13. Assets"` | scoring.py:15,29 |
| 14 | `crowdsourcing_human_subjects` | `"14. Crowdsourcing & Human Subjects"` | scoring.py:15,30 |
| 15 | `irb_approvals` | `"15. IRB Approvals"` | scoring.py:15,31 |
| 16 | `declaration_llm_usage` | `"16. Declaration of LLM Usage"` | scoring.py:15,32 |

(Source: extracted_frontend_01.md §2.3, scoring.py:8-34)

---

### 4.6 Expander Sections

Three expanders are rendered after the compliance table, in order:

#### Expander 1 — "Pipeline de Análisis Profundo (Map-Reduce + CoT + Context Mapping)"

(Source: extracted_frontend_01.md §5.2 step 8, audit_results.py:179-215)

```
CONTENT rendered inside this expander:

Chain-of-Thought:
  cot = resultado.get("informacion_extraida", {}).get("thought_process", "No disponible")
  st.info(cot)

Context Mapping:
  context_map = resultado.get("informacion_extraida", {}).get("context_mapping", [])
  if non-empty:
    Renders in columns (up to 5 per row)
  else:
    st.warning("No se ha podido mapear la estructura de secciones.")

Comparativa Map vs Reduce (2 columns):
  LEFT (MAP):
    map_data = resultado.get("general_analysis_map", [])
    if non-empty:
      Iterates; renders each step in st.expander(f"📦 Fragmento {i+1}") with st.json(step)
    else:
      Renders resultado.get("original_extraction_raw", {}) as JSON
  RIGHT (REDUCE):
    Renders resultado.get("informacion_extraida", {}) as JSON
```

#### Expander 2 — "Pipeline de Extracción Híbrida (RAG Specialist)"

(Source: extracted_frontend_01.md §5.2 step 9, audit_results.py:218-242)

```
CONTENT rendered inside this expander:

LEFT (Triage MAP):
  fragments = resultado.get("hybrid_triage_fragments", [])
  if non-empty:
    For each fragment:
      relevance = fragment.get("_relevance_score", "N/A")
      row_bg_color:
        "#065f46" if isinstance(relevance, int) and relevance > 70
        "#1e3a5f" otherwise
      Renders expander: "📄 Fragmento Técnico {i+1} (Relevancia: {relevance}%)"
      Inside: relevance badge, fragment["_chunk_text"] via st.caption,
              all non-underscore-prefixed fields via st.json

RIGHT (REDUCE):
  Renders resultado.get("extracted_hyperparameters_hybrid", {}) as JSON

NOTE: If hybrid_triage_fragments is empty:
  st.warning("No hay datos de triage disponibles.")
```

#### Expander 3 — "Pipeline de Evaluación (Senior Area Chair + Self-Correction)"

(Source: extracted_frontend_01.md §5.2 step 10, audit_results.py:245-283)

```
CONTENT rendered inside this expander:

Evaluation Signals:
  signals = resultado.get("evaluation_signals", {})
  if truthy:
    For each (k, msg) in signals.items():
      st.markdown(f"**Item {k.replace('_', ' ').title()}:**")
      st.info(msg)
  else:
    st.warning("No se generaron señales dinámicas para esta evaluación.")

Self-Correction Verification Details:
  Collects items from resultado where value is dict with v.get("verified") == True.
  Falls back to second-level scanning if no verified items at top level.
  If verified items found:
    For each item:
      status_label = "✨ Corregido" if data.get("was_corrected") else "✅ Confirmado"
      Renders st.expander with answer, justification (st.write), evidence (st.code)
  else:
    st.warning("La fase de verificación no reportó cambios o no está disponible.")
```

---

### 4.7 Download Button

The download button is rendered in `app.py`, not inside `render_audit_results`. See Section 1 Step 7g for full specification.

```
LABEL:     "📥 Descargar Informe Completo (.md)"
CONTENT:   reporte = generate_report(resultado, uploaded_file, puntuacion)  (str)
FILE NAME: f"auditoria_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"
MIME:      "text/markdown"
CONDITION: Only shown on SUCCESS PATH (resultado.get("claims") is truthy)
```

(Source: extracted_frontend_01.md §10.8 / §4.2, app.py:57-65)

---

## 5. Compliance Scoring (`get_checklist_health` + 16 Item Evaluation Rules)

**File:** `frontend/utils/scoring.py` (130 lines)  
(Source: extracted_frontend_01.md §7.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_013)

---

### 5.1 Function Signature

```python
def get_checklist_health(evaluation: dict) -> dict:
```

**Parameters:**
- `evaluation: dict` — keyed by the 16 CHECKLIST_KEYS. Per-key structure:
  ```python
  {
    "answer":          str,          # "Yes" / "No" / "N/A" / "" (case-insensitive)
    "justification":   str,
    "evidence":        str,
    "is_no_justified": bool or str   # True/False or "true"/"false"
  }
  ```

**Return type:** `dict` with keys:
- `"status"`: `str` — `"valid"` if `pending_count == 0`, else `"risk"` (Source: scoring.py:122-123)
- `"pending_count"`: `int` — count of items that triggered a risk rule (Source: scoring.py:122-126)
- `"total"`: `int` — `len(items)`; always 16 when evaluation is non-empty; 0 on early-exit (Source: scoring.py:127)
- `"items"`: `list` — 16 item dicts in CHECKLIST_KEYS order (Source: scoring.py:110-120)

(Source: scoring.py:37)

---

### 5.2 Per-Item Evaluation Algorithm

**Early-exit guard:**

```
CONDITION: evaluation is falsy (None, {}, etc.)
ACTION: return {"status": "risk", "items": [], "pending_count": 0, "total": 0}
SOURCE: scoring.py:56-62
```

**Per-item iteration (for each key in CHECKLIST_KEYS):**

```
1. val             = evaluation.get(key, {})
2. answer_raw      = val.get("answer", "").strip()
3. answer_norm     = answer_raw.lower()
4. justification   = val.get("justification", "").strip()
5. evidence        = val.get("evidence", "").strip()
6. is_no_justified_raw = val.get("is_no_justified", False)
7. Normalise is_no_justified:
     if isinstance(is_no_justified_raw, str):
         is_no_justified = is_no_justified_raw.lower() == "true"
     else:
         is_no_justified = bool(is_no_justified_raw)
                                                        SOURCE: scoring.py:73-77
```

**16 item evaluation rules (CHECKLIST_KEYS in order):**

```
RULE: claims (key 1)
TRIGGER: function iterates over CHECKLIST_KEYS; key = "claims"
CONDITION (missing_evidence): "yes" in answer_norm AND NOT evidence AND NOT justification
  ACTION: missing_evidence = True; pending_count += 1;
          alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."
                                                        SOURCE: scoring.py:84-89
CONDITION (pending_justification): "no" in answer_norm AND (NOT is_no_justified OR NOT justification)
  ACTION: pending_justification = True; pending_count += 1;
          alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."
                                                        SOURCE: scoring.py:90-95
CONDITION (N/A or empty): "n/a" in answer_norm OR answer_norm == ""
  AND NOT justification AND NOT evidence → no risk flagged
                                                        SOURCE: scoring.py:101-105
SPECIAL CASE (crowdsourcing): does NOT apply to key "claims"
SOURCE: scoring.py:84-105

RULE: limitations (key 2)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: theory_assumptions_proofs (key 3)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: experimental_result_reproducibility (key 4)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: open_access_data_code (key 5)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: experimental_setting_details (key 6)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: experiment_statistical_significance (key 7)
[Same risk detection logic as "claims"; no special case]
NOTE: Test data in scratch/test_checklist_health.py uses this key with answer="No",
      is_no_justified=False to verify health["status"] == "risk"
SOURCE: scoring.py:84-105 / scratch/test_checklist_health.py:33-36

RULE: experiments_compute_resource (key 8)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: code_of_ethics (key 9)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: broader_impacts (key 10)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: safeguards (key 11)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: licenses (key 12)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: assets (key 13)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: crowdsourcing_human_subjects (key 14)
TRIGGER: function iterates over CHECKLIST_KEYS; key = "crowdsourcing_human_subjects"
CONDITION (missing_evidence): "yes" in answer_norm AND NOT evidence AND NOT justification
  ACTION: missing_evidence = True; pending_count += 1;
          alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."
CONDITION (pending_justification): "no" in answer_norm AND (NOT is_no_justified OR NOT justification)
  ACTION: pending_justification = True; pending_count += 1;
          alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."
SPECIAL CASE (crowdsourcing): if "no" in answer_norm AND NOT is_no_justified:
  ADDITIONALLY appends to alert_msg:
    " ⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."
  ALSO TRIGGERS: secondary HTML alert in _build_table_html when
    "compensacion" in alert_msg.lower() OR "etica" in alert_msg.lower()
SOURCE: scoring.py:98-99 / audit_results.py:57-58

RULE: irb_approvals (key 15)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: declaration_llm_usage (key 16)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105
```

**Display evidence selection (applied to every item after risk detection):**

```
display_evidence = evidence if evidence else (justification if justification else "—")
SOURCE: scoring.py:108
```

**Item dict structure appended to items list (for every key):**

```python
{
    "key":                 key,                                  # str: CHECKLIST_KEY
    "label":               CHECKLIST_LABELS.get(key, key),       # str: human-readable label
    "answer":              answer_raw if answer_raw else "—",    # str
    "evidence":            display_evidence,                     # str
    "justification":       justification,                        # str (may be empty)
    "is_no_justified":     is_no_justified,                      # bool (normalised)
    "pending_justification": pending_justification,              # bool
    "missing_evidence":    missing_evidence,                     # bool
    "alert_msg":           alert_msg,                            # str (empty if no risk)
}
SOURCE: scoring.py:110-120
```

---

### 5.3 Aggregate Health Score Computation

```
pending_count = sum of items where missing_evidence==True OR pending_justification==True
total         = len(items)  (always 16 when evaluation is non-empty)

Return value:
  {
      "status":        "valid" if pending_count == 0 else "risk",
      "items":         items,
      "pending_count": pending_count,
      "total":         total,
  }
SOURCE: scoring.py:122-127
```

No numeric score percentage is computed by this function. The function validates completeness (evidence/justification presence), not a numeric quality score. The gauge chart (`create_gauge_chart`) consumes a separate numeric score whose computation source is [GAP: numeric score computation feeding create_gauge_chart not found in extracted frontend files — gauge_chart.py caller not identified within this cluster; see GAP-ext_frontend_01-001].

---

## 6. Report Generation (`generate_report`)

**File:** `frontend/components/audit_results.py`  
(Source: extracted_frontend_01.md §5.2.2 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_006, audit_results.py:287)

---

### 6.1 Function Signature

```python
def generate_report(resultado: dict, uploaded_file, health=None) -> str:
```

**Parameters:**
- `resultado: dict` — full audit result dict; used to compute `health` if `health is None`
- `uploaded_file`: Streamlit UploadedFile — `uploaded_file.name` embedded in report header
- `health: dict or None` — default `None`; if `None`, computed via `get_checklist_health(resultado)`; if already computed (e.g. by `render_audit_results`), can be passed to avoid duplicate computation

**Return type:** `str` — complete Markdown report string.  
**Side effects:** None (pure function — no Streamlit widget calls).

(Source: audit_results.py:287)

---

### 6.2 Report Template Structure

The returned Markdown string follows this exact structure (SOURCE: audit_results.py:295-316):

```
# NeurIPS 2026 Checklist Audit Report

**Paper:** {uploaded_file.name}
**Veredicto:** {status_label}
**Items con problemas:** {pending} de {total}

---

## Tabla de Cumplimiento

| # | Item | Respuesta | Evidencia / Justificacion |
|---|------|-----------|---------------------------|
| {num} | {label} | {answer} | {evidence_or_justification}{note} |
... (16 rows total)

_Generado por Auditor NeurIPS 2026._
```

Where:
- `status_label = "Checklist Valido"` if `health["status"] == "valid"` else `"Riesgo de Desk Reject"` (Source: audit_results.py:292)
- `pending = health["pending_count"]`, `total = health["total"]`
- Per-row `note` (Source: audit_results.py:304-313):

```
CONDITION: item["pending_justification"] == True
  note = " [RIESGO: sin justificacion]"

CONDITION: item["missing_evidence"] == True  (and not pending_justification)
  note = " [RIESGO: sin evidencia]"

CONDITION: neither risk flag
  note = ""  (empty string)
```

**All 16 row formats** (note appended to evidence cell):

| Row | Key | label | Possible note suffix |
|-----|-----|-------|----------------------|
| 1 | `claims` | `1. Claims` | `" [RIESGO: sin justificacion]"` or `" [RIESGO: sin evidencia]"` or `""` |
| 2 | `limitations` | `2. Limitations` | same pattern |
| 3 | `theory_assumptions_proofs` | `3. Theory, Assumptions & Proofs` | same |
| 4 | `experimental_result_reproducibility` | `4. Experimental Result Reproducibility` | same |
| 5 | `open_access_data_code` | `5. Open Access to Data and Code` | same |
| 6 | `experimental_setting_details` | `6. Experimental Setting / Details` | same |
| 7 | `experiment_statistical_significance` | `7. Experiment Statistical Significance` | same |
| 8 | `experiments_compute_resource` | `8. Experiments Compute Resource` | same |
| 9 | `code_of_ethics` | `9. Code of Ethics` | same |
| 10 | `broader_impacts` | `10. Broader Impacts` | same |
| 11 | `safeguards` | `11. Safeguards` | same |
| 12 | `licenses` | `12. Licenses` | same |
| 13 | `assets` | `13. Assets` | same |
| 14 | `crowdsourcing_human_subjects` | `14. Crowdsourcing & Human Subjects` | same |
| 15 | `irb_approvals` | `15. IRB Approvals` | same |
| 16 | `declaration_llm_usage` | `16. Declaration of LLM Usage` | same |

(Source: extracted_frontend_01.md §5.2.2 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_006, audit_results.py:304-313)

---

### 6.3 Risk Annotation Logic

```
CONDITION: item["pending_justification"] == True
  FORMAT: " [RIESGO: sin justificacion]"
  TRIGGER: "no" in answer_norm AND (NOT is_no_justified OR NOT justification)
  SOURCE: audit_results.py:304-313

CONDITION: item["missing_evidence"] == True
  FORMAT: " [RIESGO: sin evidencia]"
  TRIGGER: "yes" in answer_norm AND NOT evidence AND NOT justification
  SOURCE: audit_results.py:304-313

CONDITION: No risk flags
  FORMAT: "" (empty string — no annotation appended)
```

Note: The HTML compliance table (Section 4.5) uses emoji markers `&#9888;` (⚠) and `🔴` in alert messages. The downloadable Markdown report uses text markers `[RIESGO: ...]` (no emoji) in the note field. (Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_006,g_013,g_026,g_027 combined)

---

## 7. SOTA Analysis UI Flow (`render_sota_analysis`)

**File:** `frontend/components/sota_section.py` (109 lines)  
**Function signature:** `render_sota_analysis(md_text: str) -> None`  
(Source: extracted_frontend_01.md §5.5 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_007, sota_section.py:5)

---

**Trigger condition:** Called from `app.py` on the SUCCESS PATH, after `render_audit_results` and before `render_chatbot`. (Source: app.py:53/67)

**Input data source:** `md_text: str` — the full Markdown text of the uploaded paper, read from `st.session_state.md_text` by the caller in `app.py` and passed as a parameter.

**Render sequence:**

```
STEP 1: st.markdown("---")
STEP 2: st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")
STEP 3: Render button "Ejecutar Análisis de Literatura Reciente" (no explicit key)
                                                    SOURCE: sota_section.py:5-10
```

**On button press:**

```
STEP 4: st.spinner("Conectando con Semantic Scholar y validando bibliografía...")
STEP 5: resultado_sota = st.session_state.sota_analyzer.analyze_sota(md_text)
        — CROSS-REFERENCE: analyze_sota() is in backend/services/sota_analyzer.py
                                                    SOURCE: sota_section.py:12

STEP 6 — Branch on resultado_sota:
  CONDITION: "error" NOT in resultado_sota (success):
    st.success("Análisis completado")
    st.markdown("### 📝 Conclusión")
    st.info(resultado_sota.get("conclusion_sota", ""))
    papers_omitidos      = resultado_sota.get("papers_omitidos", [])
    df_papers            = pd.DataFrame(resultado_sota.get("papers_analizados", []))
    año_paper_estudiado  = resultado_sota.get("metadata", {}).get("año_paper_estudiado")
    if NOT df_papers.empty AND papers_omitidos:
        _render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)
    elif NOT papers_omitidos:
        st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")
                                                    SOURCE: sota_section.py:13-27
  CONDITION: "error" in resultado_sota:
    st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")
                                                    SOURCE: sota_section.py:29
```

**`_render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)` sub-function:**

(Source: extracted_frontend_01.md §5.5.1, sota_section.py:31)

```
STEP 1: Add authors_display column:
  lambda on autores column:
    if isinstance(x, list):
      base = ', '.join([a.get('name', '') for a in x[:2]])
      suffix = ' et al.' if len(x) > 2 else ''
      return base + suffix
    else: return 'N/A'

STEP 2: Rename columns:
  'titulo' → 'title', 'año' → 'year', 'citas' → 'citationCount'

STEP 3: Build titulos_omitidos = {p['titulo'].lower().strip() for p in papers_omitidos}

STEP 4: Define es_omitido(titulo) -> bool:
  titulo_lower = titulo.lower().strip()
  iterate titulos_omitidos: return True if omitido in titulo_lower OR titulo_lower in omitido
  return False

STEP 5: Add 'es_omitido' boolean column to df_papers

STEP 6: df_no_citados = df_papers[df_papers['es_omitido'] == True]

STEP 7: If df_no_citados is not empty:
  st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")
  st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")
  Build tabla_recomendaciones list (one dict per row):
    For each row in df_no_citados:
      Fuzzy-match against papers_omitidos by title
      Get justificacion, relevancia, subtema_relacionado from matched entry
      Compute es_posterior:
        "✅ Sí" if año_paper_estudiado AND paper['year'] > año_paper_estudiado
        "❌ No" if año_paper_estudiado AND NOT (paper['year'] > año_paper_estudiado)
        "?"    if not año_paper_estudiado
      Append dict: {
        "Título", "Autores", "Año", "Posterior", "Citas",
        "Relevancia", "Subtema", "Justificación"
      }
  Convert to DataFrame, render with st.dataframe with column configs:
    "Título":     TextColumn, width="large"
    "Autores":    TextColumn, width="medium"
    "Año":        NumberColumn, width="small"
    "Posterior":  TextColumn "Posterior al tuyo", width="small"
    "Citas":      NumberColumn, width="small"
    "Relevancia": TextColumn, width="small"
    "Subtema":    TextColumn, width="medium"
    "Justificación": TextColumn, width="large"
  If año_paper_estudiado:
    st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")
  Else:
    st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")

STEP 8: If df_no_citados is empty:
  st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")
```

**Async/spinner patterns:** Synchronous `st.spinner` context manager used; no async patterns. (Source: sota_section.py:11)

---

## 8. Chatbot UI Flow (`render_chatbot`)

**File:** `frontend/components/chatbot.py` (29 lines)  
**Function signature:** `render_chatbot(md_text: str) -> None`  
(Source: extracted_frontend_01.md §5.3 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_007, chatbot.py:4)

---

### 8.1 Message History Display

```
TRIGGER: Function entry (unconditional).
ACTION:
  st.markdown("---")
  st.header("💬 Pregunta al Revisor")
  st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")
  Reads: st.session_state.messages  (list of {"role": str, "content": str} dicts)
  For each message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
FORMAT: Role-based rendering using Streamlit's st.chat_message context manager;
        content rendered as Markdown.
                                                    SOURCE: chatbot.py:4-12
```

---

### 8.2 User Input and Submit Action

```
WIDGET: st.text_input(
    "Escribe tu pregunta:",
    key="chat_input",
    placeholder="Ej: ¿En qué página falla el paper en su estadística?"
)
                                                    SOURCE: chatbot.py:14-18

SUBMIT BUTTON: st.button("Enviar", key="send_button")
                                                    SOURCE: chatbot.py:20

TRIGGER: st.button("Enviar") returns True AND prompt_usuario (text_input value) is non-empty
CONDITION (ChatSubmitGuard): BOTH conditions must be True; silent ignore if prompt_usuario is empty.
                                                    SOURCE: chatbot.py:20-29

ACTION on submit:
  1. Append {"role": "user", "content": prompt_usuario} to st.session_state.messages
                                                    SOURCE: chatbot.py:21
  2. Build history_str:
       history_str = "\n".join([
           f"{m['role']}: {m['content']}"
           for m in st.session_state.messages[-4:]
       ])
                                                    SOURCE: chatbot.py:23
  3. st.spinner("El revisor está analizando tu consulta...")
  4. Backend call:
       respuesta_ia = st.session_state.chatbot.preguntar(
           md_text,
           prompt_usuario,
           history_str
       )
       — CROSS-REFERENCE: preguntar() is in backend/services/chatbot.py
                                                    SOURCE: chatbot.py:26
  5. Append {"role": "assistant", "content": respuesta_ia} to st.session_state.messages
                                                    SOURCE: chatbot.py:28
```

---

### 8.3 Rerun

```
CONDITION: After assistant response has been appended to st.session_state.messages
ACTION: st.rerun()
PURPOSE: Forces Streamlit to re-render the conversation display with the new user and
         assistant messages visible. Without rerun, the newly appended messages would
         not appear until the next user interaction.
                                                    SOURCE: chatbot.py:29
```

---

## 9. Gauge Chart (`create_gauge_chart` — NeurIPS Quality Tiers)

**File:** `frontend/components/gauge_chart.py` (71 lines)  
(Source: extracted_frontend_01.md §5.4 / §2.4, gauge_chart.py:4)

---

**Function signature:** `create_gauge_chart(score: float) -> plotly.graph_objects.Figure`

**Parameters:**
- `score: float` — quality score in range [0, 100]

**Return value:** `plotly.graph_objects.Figure` — a Plotly gauge indicator figure.

**Chart library:** Plotly (`plotly.graph_objects.go`).

---

### NeurIPS Quality Tier Definitions

| Score Range | Label | Bar Color (hex) | Source |
|-------------|-------|----------------|--------|
| [87.5, 100] | `"Strong Accept"` | `"#00aa00"` (dark green) | gauge_chart.py:14-31 |
| [75, 87.5)  | `"Accept"` | `"#00cc44"` (green) | gauge_chart.py:14-31 |
| [62.5, 75)  | `"Borderline"` | `"#ffcc00"` (yellow) | gauge_chart.py:14-31 |
| [50, 62.5)  | `"Weak Reject"` | `"#ff9900"` (orange) | gauge_chart.py:14-31 |
| [25, 50)    | `"Reject"` | `"#ff4b4b"` (red) | gauge_chart.py:14-31 |
| [0, 25)     | `"Strong Reject"` | `"#cc0000"` (dark red) | gauge_chart.py:14-31 |

Threshold line: value=62.5, color="red", width=4 (marks the Borderline boundary). (Source: gauge_chart.py:57-61)

---

### Chart Configuration Options

```python
go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': f"Quality Score<br><sub>{label}</sub>", 'font': {'size': 18}},
    number={'suffix': "%", 'font': {'size': 40}},
    gauge={
        'axis': {'range': [0, 100], 'tickmode': 'linear', 'tick0': 0, 'dtick': 25},
        'bar':  {'color': color_barra, 'thickness': 0.8, 'line': {'color': 'black', 'width': 2}},
        'bgcolor':     'white',
        'borderwidth': 2,
        'bordercolor': 'black',
        'steps': [coloured background steps matching the 6 tiers],
        'threshold': {'line': {'color': 'red', 'width': 4}, 'value': 62.5}
    }
))

layout: height=300, margins l=10/r=10/t=50/b=25, paper_bgcolor=transparent, font color="#E5E7EB"
```

(Source: gauge_chart.py:33-71)

---

### Render Site

[GAP: call site for create_gauge_chart(score) not found within the 14 files of the frontend cluster. The function is defined in gauge_chart.py and exported; its caller is expected to pass a float score (0–100) and render the returned Figure via `st.plotly_chart()`. Likely location: audit_results.py or a page/component not included in this extraction cluster. Impact: LOW — function logic is fully documented; only the caller is missing. Source: GAP-ext_frontend_01-001]

---

## 10. Custom CSS & Styling (`apply_custom_styles`)

**File:** `frontend/styles/custom_css.py` (87 lines)  
(Source: extracted_frontend_01.md §6 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_026)

**Function signature:** `apply_custom_styles() -> None`

**Mechanism:** Calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)` where `CUSTOM_CSS` is a module-level constant defined at `custom_css.py:4-83`. (Source: custom_css.py:85-86)

**CSS scope — complete selector table:**

| Selector | Properties applied | Purpose |
|----------|--------------------|---------|
| `.stApp` | `background-color: #374151 !important` | Dark grey app background |
| `#MainMenu` | `visibility: hidden` | Hides Streamlit hamburger menu |
| `footer` | `visibility: hidden` | Hides Streamlit footer |
| `header` | `background-color: transparent !important` | Transparent header |
| `[data-testid="stTable"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 5px !important` | Table container dark bg with rounded corners |
| `[data-testid="stTable"] table` | `border-collapse: collapse !important; width: 100% !important; border: none !important` | Eliminates duplicate border lines |
| `[data-testid="stTable"] th` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; background-color: #3d4446 !important; border: 1px solid #4a4a4a !important; padding: 12px !important; text-transform: capitalize !important` | Header cells: white bold text |
| `[data-testid="stTable"] th *` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; text-decoration: none !important; border: none !important; text-transform: capitalize !important` | All children of header cells |
| `[data-testid="stTable"] tbody th` | `color: #FFFFFF !important; font-size: 16px !important; background-color: #2d3436 !important` | Body row header cells |
| `[data-testid="stTable"] tbody th *` | `color: #FFFFFF !important; font-size: 16px !important; background-color: transparent !important` | Children of body row headers |
| `[data-testid="stTable"] td` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; background-color: transparent !important; border: 1px solid #4a4a4a !important; padding: 12px !important` | Table data cells |
| `[data-testid="stTable"] td *` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; text-decoration: none !important; border: none !important` | Children of data cells |
| `[data-testid="stPlotlyChart"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 10px !important` | Plotly chart container |

(Source: custom_css.py:4-83)

---

## 11. Application-Level Constants

(Source: extracted_frontend_01.md §2.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_008, config.py:3-5)

| Constant | Value | Type | Usage |
|----------|-------|------|-------|
| `TITLE` | `"💻 Auditor de Papers en Ciencias de la Computación"` | `str` | `st.title(TITLE)` in `app.py:25`; page heading |
| `SIDEBAR_IMAGE` | `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"` | `str` | `st.image(SIDEBAR_IMAGE, width=150)` in sidebar |
| `SIDEBAR_DESCRIPTION` | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` | `str` | `st.write(SIDEBAR_DESCRIPTION)` in sidebar |

---

## 12. Cross-References and GAPs

The following are all cross-references and gaps identified in the extraction data that are relevant to rebuilding the frontend:

| GAP_ID | Type | From | Expects | Impact | Source |
|--------|------|------|---------|--------|--------|
| GAP-ext_frontend_01-001 | CROSS_REFERENCE | `gauge_chart.py:4` — `create_gauge_chart(score)` | Caller passing numeric score (0-100) and rendering Figure via `st.plotly_chart()` | LOW | gauge_chart.py:4 |
| GAP-ext_frontend_01-002 | CROSS_REFERENCE | `file_uploader.py:36` — `convert_pdf_to_markdown(temp_path)` | `function(path: str) -> str` converting PDF to Markdown; likely in `backend/services/pdf_parser.py` | HIGH | file_uploader.py:4-5 |
| GAP-ext_frontend_01-003 | CROSS_REFERENCE | `session_state.py:13` — `PaperAuditor()` | Class with `audit(md_text: str, status_callback: callable) -> dict`; expected keys include all 16 CHECKLIST_KEYS plus optional: "error", "evaluation_error", "metricas", "informacion_extraida", "general_analysis_map", "original_extraction_raw", "hybrid_triage_fragments", "extracted_hyperparameters_hybrid", "evaluation_signals" | HIGH | session_state.py:3 |
| GAP-ext_frontend_01-004 | CROSS_REFERENCE | `session_state.py:16` — `PaperChatbot()` | Class with `preguntar(md_text: str, question: str, history_str: str) -> str` | MEDIUM | session_state.py:4 |
| GAP-ext_frontend_01-005 | CROSS_REFERENCE | `session_state.py:19` — `SotaAnalyzer()` | Class with `analyze_sota(md_text: str) -> dict`; keys: "conclusion_sota", "papers_omitidos" (list), "papers_analizados" (list of dicts with 'titulo', 'año', 'citas', 'autores'), "metadata" (dict with 'año_paper_estudiado'), optionally "error" | MEDIUM | session_state.py:5 |
| GAP-ext_frontend_01-006 | CONFIG_DEPENDENCY | `file_uploader.py:23` — `os.makedirs("temp")` | Filesystem write permission in working directory to create `temp/` subdirectory | HIGH | file_uploader.py:23-24 |
| GAP-ext_frontend_01-007 | EXTERNAL_SYSTEM | `sota_section.py:12` — `sota_analyzer.analyze_sota()` | Connectivity to Semantic Scholar API (mentioned in spinner text) | MEDIUM | sota_section.py:11 |
| GAP-ext_frontend_01-008 | MISSING_SOURCE | `audit_results.py:241` — `st.caption("Fusión de datos técnicos con Gemma 4 31B.")` | Knowledge of which LLM model is used in RAG REDUCE phase | LOW | audit_results.py:241 |


### 03_technical_specs.md (34793 chars)
# Technical Specifications — 03_technical_specs.md

---

## 1. External API Contracts (Google Gemini, Semantic Scholar)

### 1.1 Google Gemini API

**All 6 model constants** — Source: `backend/common/config.py` [Source: extracted_backend_core_01.md § 2.1]

| Constant | Exact String Value | Purpose | Source File & Line |
|---|---|---|---|
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | RAG embeddings | `config.py:35` |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Triage and Map phase extraction | `config.py:37` |
| `REDUCE_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Orchestration and Consolidation (Reduce phase) | `config.py:39` |
| `EXTRACTION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Initial extraction (General Analysis) | `config.py:41` |
| `EVALUATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Final evaluation (Senior Area Chair) | `config.py:43` |
| `VERIFICATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Strict verification (Auditor 2) | `config.py:45` |

Note: Lines 48–105 of `config.py` contain a multi-line docstring listing all available Gemini models for reference; not executable code. [Source: extracted_backend_core_01.md § 2.1]

**Generation config dicts associated with model constants:**

`AUDIT_CONFIG` — associated with `EXTRACTION_MODEL_NAME`, `EVALUATION_MODEL_NAME`, `MAP_MODEL_NAME`, `REDUCE_MODEL_NAME`, `VERIFICATION_MODEL_NAME` — [Source: extracted_backend_core_01.md § 2.1, `config.py:116`]:

```python
{
    "response_mime_type": "application/json",
    "temperature": 0.0,       # = AUDIT_TEMPERATURE
    "top_k": 1,
    "top_p": 0.1,
    "max_output_tokens": 16384
}
```

Used by: `PaperAuditor.__init__` for all 5 `LLMClient` instances (`extraction_llm`, `evaluation_llm`, `rag_map_llm`, `rag_reduce_llm`, `verification_llm`). [Source: extracted_backend_core_01.md § 2.1, `config.py:116`]

`CHAT_CONFIG` — associated with the default `MODEL_NAME` (= `EXTRACTION_MODEL_NAME` = `"gemini-3.1-flash-lite-preview"`) — [Source: extracted_backend_core_01.md § 2.1, `config.py:125`]:

```python
{
    "temperature": 0.2        # = CHAT_TEMPERATURE
}
```

Used by: `PaperChatbot.__init__`. [Source: extracted_backend_core_01.md § 2.1, `config.py:125`]

`SOTA_CONFIG` — associated with the default `MODEL_NAME` — [Source: extracted_backend_core_01.md § 2.1, `config.py:130`]:

```python
{
    "response_mime_type": "application/json",
    "temperature": 0.1        # = SOTA_TEMPERATURE
}
```

Used by: `SotaAnalyzer.__init__`. [Source: extracted_backend_core_01.md § 2.1, `config.py:130`]

**Full method call signature used to invoke the API:**

Primary call in `LLMClient.generate` — [Source: extracted_backend_core_01.md § 3.1, `llm_client.py:44–48`]:

```python
self.client.models.generate_content(
    model=self.model_name,
    contents=prompt,
    config=self.generation_config
)
```

Fallback call signature in `InformationExtractionSkill` REDUCE phase — [Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_015, `auditor_skills.py:113`]:

```python
self.llm_client.client.models.generate_content(
    model=REDUCE_MODEL_NAME,
    contents=reduce_prompt,
    config={"response_mime_type": "application/json", "temperature": 0.0}
)
```

---

### 1.2 Semantic Scholar API

[Source: extracted_backend_core_01.md § 2.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_018]

**Base URL (exact string):**

```
https://api.semanticscholar.org/graph/v1/paper/search
```

Constant: `SEMANTIC_SCHOLAR_BASE_URL` — [Source: `config.py:136`]

**Query parameters (exact values):**

| Parameter Name | Value | Source Constant | Source File & Line |
|---|---|---|---|
| `query` | value of each search query string (runtime) | — | `sota_skills.py:162` |
| `year` | `"2023-2026"` | `SEMANTIC_SCHOLAR_YEAR_RANGE` | `config.py:137` |
| `limit` | `5` | `SEMANTIC_SCHOLAR_LIMIT` | `config.py:138` |
| `fields` | `"paperId,title,authors,year,citationCount,abstract,url"` | `SEMANTIC_SCHOLAR_FIELDS` | `config.py:139` |

**Authentication:**

- Header name: `"x-api-key"`
- Value source: `SEMANTIC_SCHOLAR_API_KEY` environment variable (`os.getenv("SEMANTIC_SCHOLAR_API_KEY")`)
- This header is included only when `SEMANTIC_SCHOLAR_API_KEY` is set; the API is still callable (public access, subject to rate limits) without it. [Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_018]

**Full constructed URL pattern:**

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query=<search_query>
  &year=2023-2026
  &limit=5
  &fields=paperId,title,authors,year,citationCount,abstract,url
```

HTTP call via `requests.get(..., timeout=15)`. [Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_018, `sota_skills.py:162`]

---

## 2. LLM Client Configuration and Retry Policy

### 2.1 LLMClient Constructor

[Source: extracted_backend_core_01.md § 3.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_012, `llm_client.py:8–28`]

**Class:** `LLMClient` — `backend/common/llm_client.py:8`

- Parent class: none
- Module-level logger: `logger = get_logger(__name__)` at `llm_client.py:6`
- Supported provider: Google Gemini exclusively via `google.genai.Client`
- Not a singleton; a new instance is created per service

**Signature:**

```python
def __init__(self, model_name=None, generation_config=None)
```

| Parameter | Type | Default | Behaviour |
|---|---|---|---|
| `model_name` | `str \| None` | `None` | If `None`, resolved to `MODEL_NAME` from config (`"gemini-3.1-flash-lite-preview"`) |
| `generation_config` | `dict \| None` | `None` | If `None`, resolved to `{}` |

**Execution sequence:**

1. Checks `if not GOOGLE_API_KEY` (evaluates `True` if `None` or empty string) — `llm_client.py:19`
   - If true: calls `logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")`  — `llm_client.py:20`
   - Then: raises `ValueError("No se encontró la GOOGLE_API_KEY en el .env")` — `llm_client.py:21`
   - Construction aborted; no attributes set
2. Creates `self.client = genai.Client(api_key=GOOGLE_API_KEY)` — `llm_client.py:23`
3. Sets `self.model_name = model_name or MODEL_NAME` — `llm_client.py:25`
4. Sets `self.generation_config = generation_config or {}` — `llm_client.py:26`
5. Logs `logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")` — `llm_client.py:28`

**Return:** `None` (constructor)

**Instance attributes after successful construction:** `self.client` (genai.Client), `self.model_name` (str), `self.generation_config` (dict)

---

### 2.2 generate() Retry Loop

[Source: extracted_backend_core_01.md § 3.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_012, `llm_client.py:30–76`]

**Signature:**

```python
def generate(self, prompt)
```

- Parameter `prompt`: any type accepted by `genai.Client.models.generate_content` (string or structured content)
- Return type: Google genai response object; caller accesses `.text` or `.candidates[0].content` etc.
- Inline imports at method entry: `time`, `streamlit as st`, `random` — `llm_client.py:35–37`

**Retry constants:**

| Constant | Value | Source |
|---|---|---|
| `max_retries` | `5` | `llm_client.py:39` |
| `base_delay` | `2` (seconds) | `llm_client.py:40` |

**Loop:**

```python
for attempt in range(max_retries + 1):   # range(6): attempts 0 through 5 = 6 TOTAL ATTEMPTS
```

Source: `llm_client.py:42`

**Per-attempt logic:**

1. Calls `self.client.models.generate_content(model=self.model_name, contents=prompt, config=self.generation_config)` — `llm_client.py:44–48`
2. On success: returns `response` immediately — `llm_client.py:49`

**Exception handling — on any `Exception as e`:**

- Computes `error_msg = str(e)` — `llm_client.py:52`
- Computes `is_retryable = any(code in error_msg.upper() for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"])` — `llm_client.py:54`

**Retryable error codes (matched by substring in uppercased `error_msg`):**

- `"503"`
- `"429"`
- `"UNAVAILABLE"`
- `"RESOURCE_EXHAUSTED"`
- `"DEADLINE_EXCEEDED"`

**If `attempt < max_retries AND is_retryable` (retryable, attempts remaining):**

- Computes delay: `delay = base_delay * (2 ** attempt) + random.uniform(0, 1)` — `llm_client.py:58`
- Sleep durations per attempt (deterministic portion only; add up to 1s of jitter):
  - Attempt 0: `2 * (2 ** 0)` = `2` seconds + jitter → ≈ 2–3 s
  - Attempt 1: `2 * (2 ** 1)` = `4` seconds + jitter → ≈ 4–5 s
  - Attempt 2: `2 * (2 ** 2)` = `8` seconds + jitter → ≈ 8–9 s
  - Attempt 3: `2 * (2 ** 3)` = `16` seconds + jitter → ≈ 16–17 s
  - Attempt 4: `2 * (2 ** 4)` = `32` seconds + jitter → ≈ 32–33 s
- Logs `logger.warning(f"⚠️ Error API Gemini [{self.model_name}]: {error_msg}. Reintento {attempt + 1}/{max_retries} en {delay:.1f}s...")` — `llm_client.py:60`
- Attempts `st.toast(f"⏳ Gemini saturado (Alta demanda). Reintento {attempt + 1}/{max_retries} en {int(delay)}s...", icon="⏳")` inside `try/except Exception: pass` (silently ignored if Streamlit not active) — `llm_client.py:63–66`
- Calls `time.sleep(delay)` — `llm_client.py:69`
- Continues to next attempt

**If `attempt >= max_retries` (all 5 retry attempts exhausted):**

- Logs `logger.error(f"❌ Error crítico tras {max_retries} reintentos: {error_msg}")` — `llm_client.py:73`
- `raise` (re-raises original exception) — `llm_client.py:76`

**If NOT `is_retryable` (non-retryable error on any attempt, regardless of attempt number):**

- Logs `logger.error(f"❌ Error no reintentable detectado: {error_msg}")` — `llm_client.py:75`
- `raise` (re-raises original exception) — `llm_client.py:76`

**Summary:**

- Total possible calls: 6 (1 original + up to 5 retries). [Source: extracted_root_tests_scratch_01.md § RULE-05, `scratch/test_llm_retry.py:55`]
- Total possible `time.sleep` calls: 5 (one per retry). [Source: `scratch/test_llm_retry.py:55`]
- Non-retryable errors: immediately re-raised on first occurrence, no sleep.

---

### 2.3 client.models.generate_content Fallback

[Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_015, `auditor_skills.py:113`]

Used by `InformationExtractionSkill` REDUCE phase when primary call fails. Full fallback signature:

```python
self.llm_client.client.models.generate_content(
    model=REDUCE_MODEL_NAME,
    contents=reduce_prompt,
    config={"response_mime_type": "application/json", "temperature": 0.0}
)
```

Where `REDUCE_MODEL_NAME = "gemini-3.1-flash-lite-preview"` [Source: `config.py:39`].

---

## 3. Configuration Parameters (all constants with values)

[Source: extracted_backend_core_01.md § 2.1, `backend/common/config.py`]

| Constant / Key | Value | Type | Source (env var or hardcoded) | Description | Source File & Section |
|---|---|---|---|---|---|
| `GOOGLE_API_KEY` | — (no default) | `str \| None` | Env var `"GOOGLE_API_KEY"` | Google Gemini API key; `None` if not set | `config.py:30` |
| `SEMANTIC_SCHOLAR_API_KEY` | — (no default) | `str \| None` | Env var `"SEMANTIC_SCHOLAR_API_KEY"` | Semantic Scholar API key; `None` if not set | `config.py:31` |
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | `str` | Hardcoded | RAG embeddings model | `config.py:35` |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Triage and Map phase extraction model | `config.py:37` |
| `REDUCE_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Reduce phase / consolidation model | `config.py:39` |
| `EXTRACTION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Initial extraction model | `config.py:41` |
| `EVALUATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Final evaluation model | `config.py:43` |
| `VERIFICATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Strict verification model (Auditor 2) | `config.py:45` |
| `MODEL_NAME` | `= EXTRACTION_MODEL_NAME` → `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded (alias assignment) | Default model for `LLMClient`; NOT env-overridable | `config.py:107` |
| `RAG_MODEL_NAME` | `= MAP_MODEL_NAME` → `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded (alias assignment) | Default model for RAG | `config.py:108` |
| `AUDIT_TEMPERATURE` | `0.0` | `float` | Hardcoded | Temperature for `AUDIT_CONFIG` | `config.py:111` |
| `CHAT_TEMPERATURE` | `0.2` | `float` | Hardcoded | Temperature for `CHAT_CONFIG` | `config.py:112` |
| `SOTA_TEMPERATURE` | `0.1` | `float` | Hardcoded | Temperature for `SOTA_CONFIG` | `config.py:113` |
| `AUDIT_CONFIG` | See § 1.1 | `dict` | Hardcoded | generation_config for all audit LLM calls | `config.py:116` |
| `CHAT_CONFIG` | See § 1.1 | `dict` | Hardcoded | generation_config for chatbot LLM calls | `config.py:125` |
| `SOTA_CONFIG` | See § 1.1 | `dict` | Hardcoded | generation_config for SOTA analysis LLM calls | `config.py:130` |
| `SEMANTIC_SCHOLAR_BASE_URL` | `"https://api.semanticscholar.org/graph/v1/paper/search"` | `str` | Hardcoded | Semantic Scholar API endpoint | `config.py:136` |
| `SEMANTIC_SCHOLAR_YEAR_RANGE` | `"2023-2026"` | `str` | Hardcoded | Year filter for Semantic Scholar queries | `config.py:137` |
| `SEMANTIC_SCHOLAR_LIMIT` | `5` | `int` | Hardcoded | Max results per Semantic Scholar query | `config.py:138` |
| `SEMANTIC_SCHOLAR_FIELDS` | `"paperId,title,authors,year,citationCount,abstract,url"` | `str` | Hardcoded | Fields requested from Semantic Scholar API | `config.py:139` |
| `max_retries` (inline, `LLMClient.generate`) | `5` | `int` | Hardcoded (local var) | Maximum retry attempts (loop is `range(6)`) | `llm_client.py:39` |
| `base_delay` (inline, `LLMClient.generate`) | `2` (seconds) | `int` | Hardcoded (local var) | Base delay for exponential backoff | `llm_client.py:40` |
| `chunk_size` (inline, `pdf_parser.py`) | `5` (pages per block) | `int` | Hardcoded (local var) | Pages per Docling processing chunk | `pdf_parser.py:51` |

---

## 4. Dependency Declarations and Missing Dependencies

### 4.1 Declared Dependencies (requirements.txt)

[Source: extracted_root_tests_scratch_01.md § 2, `requirements.txt:1–5`]

No version pins are present in `requirements.txt`. All packages are installed at latest available version.

| Package | Version Specifier | Role | Source |
|---|---|---|---|
| `docling` | (none — latest) | Local (free) PDF-to-Markdown conversion for file ingestion in the backend | `requirements.txt:1` |
| `google-generativeai` | (none — latest) | Google Gemini API client for LLM calls (extraction, evaluation) and embedding API | `requirements.txt:2` |
| `python-dotenv` | (none — latest) | Loads `GOOGLE_API_KEY` and other secrets from `.env` file | `requirements.txt:3` |
| `streamlit` | (none — latest) | Web UI framework for the main application (`app.py`) | `requirements.txt:4` |
| `pydantic` | (none — latest) | Structured/validated LLM response parsing | `requirements.txt:5` |

---

### 4.2 Undeclared / Missing Dependencies

[Source: extracted_root_tests_scratch_01.md § 2, cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY]

#### reportlab — GAP-025

```
GAP_ID: GAP-cluster_root_tests_scratch_01-025
TYPE: MISSING_DEPENDENCY
FROM: md_to_pdf.py:8–13 (all PDF generation logic), create_test_pdf.py:2–6 (all PDF generation logic)
DETAIL: reportlab is a hard dependency imported unconditionally in both utilities but is absent from requirements.txt.
  md_to_pdf.py lines 8–13 imports:
    reportlab.lib.pagesizes  → letter, A4
    reportlab.lib.styles     → getSampleStyleSheet, ParagraphStyle
    reportlab.lib.units      → inch
    reportlab.platypus       → SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
    reportlab.lib            → colors
    reportlab.lib.enums      → TA_CENTER, TA_LEFT, TA_JUSTIFY
  create_test_pdf.py lines 2–6 imports:
    reportlab.lib.pagesizes  → letter
    reportlab.lib.styles     → getSampleStyleSheet, ParagraphStyle
    reportlab.lib.units      → inch
    reportlab.platypus       → SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    reportlab.lib            → colors
IMPACT: HIGH — any environment installed strictly from requirements.txt (pip install -r requirements.txt) fails
  at module-load time with ModuleNotFoundError when either md_to_pdf.py or create_test_pdf.py is executed;
  all PDF generation functionality is unavailable without reportlab
SOURCE: md_to_pdf.py:8–13, create_test_pdf.py:2–6, requirements.txt:1–5 (absence confirmed)
```

#### pymupdf4llm — undeclared dependency for pdf_to_md.py

[Source: extracted_root_tests_scratch_01.md § 4.2, `pdf_to_md.py:41`]

- **Package:** `pymupdf4llm`
- **Module requiring it:** `pdf_to_md.py`
- **Dependency type:** Hard — the single call `pymupdf4llm.to_markdown(pdf_path)` at `pdf_to_md.py:41` is the sole PDF→Markdown conversion mechanism in that file; there is no fallback.
- **Impact:** `pdf_to_md.py` fails with `ModuleNotFoundError` at call time in any environment installed strictly from `requirements.txt`.
- **[GAP: pymupdf4llm is an undeclared hard dependency of pdf_to_md.py; not listed in requirements.txt — not found in source requirements.txt:1–5 (absence confirmed)]**

#### markdown2 — GAP-026

```
GAP_ID: GAP-cluster_root_tests_scratch_01-026
TYPE: MISSING_DEPENDENCY
FROM: md_to_pdf.py:15–17 — try: import markdown2 / HAS_MARKDOWN = True
DETAIL: markdown2 is attempted via `try: import markdown2` at md_to_pdf.py:15. It is not listed in
  requirements.txt. The except ImportError branch (md_to_pdf.py:18–21) sets HAS_MARKDOWN = False and
  prints: "⚠️ Advertencia: markdown2 no instalado. Solo se soportará conversión básica." /
  "   Instala con: pip install markdown2". The package is characterised as optional: runtime does not
  crash. However, HAS_MARKDOWN is never used to gate any code path in the file — the built-in
  line-by-line parser (parse_markdown_to_elements, md_to_pdf.py:23–101) runs unconditionally
  regardless of markdown2 availability.
IMPACT: LOW — runtime does not crash; markdown2-enhanced conversion path is not implemented in this
  file; markdown2 is an undeclared optional dependency whose absence is the default state in any
  requirements.txt-only environment
SOURCE: md_to_pdf.py:15–17, requirements.txt:1–5 (absence confirmed)
```

---

## 5. Logging Infrastructure

### 5.1 get_logger Function

[Source: extracted_backend_core_01.md § 6.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_019, `backend/utils/logger.py:44`]

**Signature:**

```python
def get_logger(name: str) -> logging.Logger
```

**Parameters:**

- `name` (str): Logger name; callers pass `__name__` (module name)

**Return type:** `logging.Logger`

**Behaviour (execution sequence):**

1. Calls `logging.getLogger(name)` → `logger` — `logger.py:45`
2. Sets `logger.propagate = False` (prevents duplication with root logger) — `logger.py:47`
3. Guard: `if not logger.handlers:` — `logger.py:49` (prevents adding duplicate handlers on repeated calls)
   - Creates `logging.StreamHandler(sys.stdout)` — `logger.py:49–50`; output directed to **stdout**
   - Creates `ColoredFormatter` instance with format string `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` and date format `'%H:%M:%S'` — `logger.py:19, 41`
   - Attaches formatter to handler; adds handler to logger
   - Sets `logger.setLevel(logging.INFO)` — `logger.py:53`
4. Side effects (always executed, regardless of handler guard):
   - `logging.getLogger("google_genai").setLevel(logging.WARNING)` — `logger.py:56`
   - `logging.getLogger("httpx").setLevel(logging.INFO)` — `logger.py:57`
5. Returns `logger`

**Available logger methods (standard `logging.Logger`):** `.info(msg)`, `.debug(msg)`, `.warning(msg)`, `.error(msg)`, `.critical(msg)`

**Log format:** `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` with date format `'%H:%M:%S'` — `logger.py:19, 41`

**No log rotation configured.**

---

### 5.2 ColoredFormatter Class

[Source: extracted_backend_core_01.md § 6.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_019, `backend/utils/logger.py`]

**Class definition:**

```python
class ColoredFormatter(logging.Formatter):
    ...
```

Inherits from `logging.Formatter`. [Source: `logger.py`]

**Constructor parameters:** None specified (uses inherited `logging.Formatter.__init__`). The formatter is instantiated as `ColoredFormatter()` without arguments.

**`format(self, record)` method behaviour** — [Source: `logger.py:29`]:

1. Checks `if "HTTP Request" in record.msg`:
   - If true: sets `color = Colors.CYAN`; mutates `record.msg = f"{Colors.CYAN}{record.msg}{Colors.RESET}"` — `logger.py:33–35`
   - Colors the entire message body in cyan
2. Else:
   - Reads `color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)` — `logger.py:37`
   - Mutates `record.levelname = f"{color}{record.levelname}{Colors.RESET}"` — `logger.py:39`
   - Colors the level name prefix
3. Creates a new `logging.Formatter(log_fmt, datefmt='%H:%M:%S')` on every call (no caching) — `logger.py:41`
4. Returns `formatter.format(record)` — `logger.py:42`

**`LEVEL_COLORS` mapping (class-level dict):**

| Level | Color constant used | Source |
|---|---|---|
| `logging.DEBUG` | `Colors.BLUE` (`"\033[94m"`) | `logger.py:22` |
| `logging.INFO` | `Colors.GREEN` (`"\033[92m"`) | `logger.py:23` |
| `logging.WARNING` | `Colors.YELLOW` (`"\033[93m"`) | `logger.py:24` |
| `logging.ERROR` | `Colors.RED` (`"\033[91m"`) | `logger.py:25` |
| `logging.CRITICAL` | `Colors.BOLD + Colors.RED` (`"\033[1m" + "\033[91m"`) | `logger.py:26` |

---

### 5.3 Colors Class

[Source: extracted_backend_core_01.md § 2.3, `backend/utils/logger.py:7–14`]

```python
class Colors:
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"
```

| Attribute | Value (ANSI escape code) | Source |
|---|---|---|
| `Colors.BLUE` | `"\033[94m"` | `logger.py:7` |
| `Colors.CYAN` | `"\033[96m"` | `logger.py:8` |
| `Colors.GREEN` | `"\033[92m"` | `logger.py:9` |
| `Colors.YELLOW` | `"\033[93m"` | `logger.py:10` |
| `Colors.RED` | `"\033[91m"` | `logger.py:11` |
| `Colors.MAGENTA` | `"\033[95m"` | `logger.py:12` |
| `Colors.BOLD` | `"\033[1m"` | `logger.py:13` |
| `Colors.RESET` | `"\033[0m"` | `logger.py:14` |

---

### 5.4 CleanNetworkLogs Filter

[Source: extracted_backend_core_01.md § 2.1, `config.py:14–20`]

**Class definition:**

```python
class CleanNetworkLogs(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "huggingface.co" in msg and ("HEAD" in msg or "GET" in msg):
            return False
        return True
```

**Filter algorithm — precise description:**

- Inherits `logging.Filter`
- `filter(self, record)` method:
  1. Calls `record.getMessage()` → assigns result to `msg`
  2. Checks compound condition: `"huggingface.co" in msg` AND (`"HEAD" in msg` OR `"GET" in msg`)
     - If **true**: returns `False` — the log record is **suppressed** (filtered out)
     - If **false**: returns `True` — the log record **passes** (is emitted)
- **Exact URL pattern matched:** the literal substring `"huggingface.co"` must be present in the message
- **Exact HTTP methods matched:** literal substrings `"HEAD"` or `"GET"` must be present in the message
- All matching is **case-sensitive** (no `re.IGNORECASE` — plain `in` operator on strings)
- **Effect:** Suppresses logging of HuggingFace HEAD and GET HTTP request log lines emitted by the `httpx` library when models are loaded or checked
- **Applied to:** `logging.getLogger("httpx")` via `.addFilter(CleanNetworkLogs())` at `config.py:22`

[Source: extracted_backend_core_01.md § 2.1, `config.py:14–22`]

---

## 6. Environment Variable Schema

[Source: extracted_backend_core_01.md § 2.1, § 5; extracted_root_tests_scratch_01.md § 3.1]

| Variable Name | Required / Optional | Loaded Via | Default | Used By | Source |
|---|---|---|---|---|---|
| `GOOGLE_API_KEY` | Required (for any LLM operation) | `load_dotenv()` in `config.py:27`; `os.getenv("GOOGLE_API_KEY")` at `config.py:30` | `None` (raises `ValueError` in `LLMClient.__init__` if not set) | `LLMClient.__init__`, all LLM-dependent services | `config.py:30` |
| `SEMANTIC_SCHOLAR_API_KEY` | Optional | `load_dotenv()` in `config.py:27`; `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` at `config.py:31` | `None` (API still accessible without it, subject to rate limits) | `SemanticScholarSearchSkill.execute` (sent as `"x-api-key"` header) | `config.py:31` |
| `TRANSFORMERS_VERBOSITY` | N/A (set by code, not read) | Set by `config.py:8` and `app.py:13` at module import | `"error"` (hardcoded, overrides any preexisting value) | Suppresses `transformers` library logs | `config.py:8`, `app.py:13` |
| `TOKENIZERS_PARALLELISM` | N/A (set by code, not read) | Set by `config.py:9` and `app.py:14` at module import | `"false"` (hardcoded) | Suppresses tokenizer parallelism warnings | `config.py:9`, `app.py:14` |
| `ANONYMIZED_TELEMETRY` | N/A (set by code, not read) | Set by `app.py:21` at module import | `"False"` (hardcoded) | Disables ChromaDB telemetry | `app.py:21` |
| `OTEL_SDK_DISABLED` | N/A (set by code, not read) | Set by `app.py:22` at module import | `"true"` (hardcoded) | Disables OpenTelemetry SDK (avoids Streamlit conflicts) | `app.py:22` |

**How `.env` loading works:**

- `python-dotenv` is used via `load_dotenv()`.
- `load_dotenv()` is called at module level in `backend/common/config.py:27` (before reading `GOOGLE_API_KEY` and `SEMANTIC_SCHOLAR_API_KEY`).
- `load_dotenv()` is also called at module level in `list_models.py:5`.
- All modules that import from `backend.common.config` (or `backend.common.llm_client`) trigger this `load_dotenv()` call at import time. [Source: extracted_backend_core_01.md § 2.1, `config.py:27`]

---

## 7. Module-Level Side Effects

[Source: extracted_backend_core_01.md § 2.1, extracted_root_tests_scratch_01.md § 3.1]

The following side effects occur at module import time:

### `backend/common/config.py`

| Side Effect | Exact Mechanism | Source |
|---|---|---|
| Sets `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` | `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` (direct dict assignment) | `config.py:8` |
| Sets `os.environ["TOKENIZERS_PARALLELISM"] = "false"` | `os.environ["TOKENIZERS_PARALLELISM"] = "false"` (direct dict assignment) | `config.py:9` |
| Suppresses all Python warnings | `warnings.filterwarnings("ignore")` | `config.py:10` |
| Sets `transformers` logger level to ERROR | `logging.getLogger("transformers").setLevel(logging.ERROR)` | `config.py:11` |
| Loads `.env` file into environment | `load_dotenv()` (from `python-dotenv`) | `config.py:27` |
| Applies `CleanNetworkLogs` filter to `httpx` logger | `logging.getLogger("httpx").addFilter(CleanNetworkLogs())` | `config.py:22` |
| Sets `RapidOCR` logger level to WARNING | `logging.getLogger("RapidOCR").setLevel(logging.WARNING)` | `config.py:23` |
| Sets `docling` logger level to WARNING | `logging.getLogger("docling").setLevel(logging.WARNING)` | `config.py:24` |
| Sets `onnxruntime` logger level to ERROR | `logging.getLogger("onnxruntime").setLevel(logging.ERROR)` | `config.py:25` |

### `app.py`

| Side Effect | Exact Mechanism | Source |
|---|---|---|
| Sets `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` | `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` | `app.py:13` |
| Sets `os.environ["TOKENIZERS_PARALLELISM"] = "false"` | `os.environ["TOKENIZERS_PARALLELISM"] = "false"` | `app.py:14` |
| Suppresses `__path__` access warnings | `warnings.filterwarnings("ignore", message=".*Accessing.*__path__.*")` | `app.py:15` |
| Suppresses all `FutureWarning` | `warnings.filterwarnings("ignore", category=FutureWarning)` | `app.py:16` |
| Suppresses all `UserWarning` | `warnings.filterwarnings("ignore", category=UserWarning)` | `app.py:17` |
| Sets `transformers` logger level to ERROR | `logging.getLogger("transformers").setLevel(logging.ERROR)` | `app.py:18` |
| Sets `os.environ["ANONYMIZED_TELEMETRY"] = "False"` | `os.environ["ANONYMIZED_TELEMETRY"] = "False"` | `app.py:21` |
| Sets `os.environ["OTEL_SDK_DISABLED"] = "true"` | `os.environ["OTEL_SDK_DISABLED"] = "true"` | `app.py:22` |

Note: `TRANSFORMERS_VERBOSITY` and `TOKENIZERS_PARALLELISM` are set in **both** `config.py` and `app.py`. Because `config.py` is imported before `app.py` sets its own values, the final values are the same. The duplication ensures the suppression applies even if `config.py` is not imported first. [Source: extracted_root_tests_scratch_01.md § 3.1]

---

## 8. PDF Conversion Technical Details

### 8.1 Docling-Based PDF Conversion Pipeline (`backend/services/pdf_parser.py`)

[Source: extracted_backend_core_01.md § 4.1, `backend/services/pdf_parser.py`]

**Entry point function:**

```python
def convert_pdf_to_markdown(pdf_path) -> str
```

- Parameter `pdf_path`: path to PDF file (str or path-like)
- Return type: `str` — full Markdown text of the PDF; or error string starting with `"❌ Error en la extracción del PDF: "` on outer exception
- Library used: `docling.document_converter.DocumentConverter`

**Chunked processing approach:**

- Chunk size: `chunk_size = 5` pages per processing block — `pdf_parser.py:51`
- No overlap between chunks
- Iteration pattern: `for i in range(0, total_pages, chunk_size)` — `pdf_parser.py:53`

**Full call chain (input PDF → Markdown output):**

**Step 0 — Lazy imports at function entry** (`pdf_parser.py:20–25`):

```python
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from pypdf import PdfReader
from pypdf import PdfWriter
import os
import tempfile
```

**Step 1 — Configure Docling pipeline** (`pdf_parser.py:28–43`):

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False              # OCR disabled for speed
pipeline_options.do_table_structure = True   # table detection enabled
```

GPU detection (informational only — Docling auto-detects via torch):

```python
import torch
if torch.cuda.is_available():
    logger.info("🚀 GPU detectada. Docling usará aceleración CUDA automáticamente.")
else:
    logger.info("ℹ️ No se detectó GPU compatible. Usando CPU para Docling.")
```

```python
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
```

**Step 2 — Read PDF metadata** (`pdf_parser.py:46–50`):

```python
reader = PdfReader(pdf_path)
total_pages = len(reader.pages)
full_md_text = ""
```

**Step 3 — Chunked conversion loop** (`pdf_parser.py:53–79`):

Per chunk iteration:

```python
start_page = i
end_page = min(i + chunk_size, total_pages)   # chunk_size = 5

writer = PdfWriter()
for page_num in range(start_page, end_page):
    writer.add_page(reader.pages[page_num])

with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    tmp_path = tmp_file.name
    writer.write(tmp_path)

try:
    result = converter.convert(tmp_path)
    block_md = result.document.export_to_markdown()
    full_md_text += block_md + "\n\n"
except Exception as block_error:
    # error text appended, processing continues to next block
    full_md_text += f"\n\n> [!ERROR] Error al procesar páginas {start_page+1}-{end_page}: {str(block_error)}\n\n"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)    # temp file always cleaned up
```

**Step 4 — Return result** (`pdf_parser.py:82`):

```python
return full_md_text
```

**Intermediate formats:**

1. PDF file (original)
2. Per-chunk temporary PDF files (written to `tempfile.NamedTemporaryFile`, suffix `.pdf`; deleted in `finally`)
3. Docling `ConversionResult` object (`result`)
4. Markdown string per chunk (`block_md` = `result.document.export_to_markdown()`)
5. Concatenated full Markdown string (`full_md_text`)

**Configuration passed to Docling:**

- `PdfPipelineOptions.do_ocr = False` — OCR disabled
- `PdfPipelineOptions.do_table_structure = True` — table detection enabled
- GPU acceleration: Docling auto-detects via `torch`; no explicit CUDA config passed

**Error handling:**

| Error scenario | Handling |
|---|---|
| Per-block conversion error | Caught (`Exception as block_error`); error text appended to `full_md_text`; processing continues to next block; temp file cleaned in `finally` |
| Empty PDF (`total_pages = 0`) | Loop does not execute; returns empty string `""` |
| Corrupted/unreadable PDF (`PdfReader` raises) | Caught by outer `except Exception as e`; returns `f"❌ Error en la extracción del PDF: {str(e)}"` |
| Password-protected PDF (`PdfReader` raises) | Same as corrupted PDF — outer handler; returns error string |
| Temp file always cleaned | `finally` block: `if os.path.exists(tmp_path): os.remove(tmp_path)` |

**Outer exception handler** (`pdf_parser.py:83–85`):

```python
except Exception as e:
    logger.error(f"❌ Error en la extracción del PDF: {str(e)}")
    return f"❌ Error en la extracción del PDF: {str(e)}"
```

---

### 8.2 pymupdf4llm Alternative Path (`pdf_to_md.py`)

[Source: extracted_root_tests_scratch_01.md § 4.2, `pdf_to_md.py:41`]

[GAP: pymupdf4llm is an undeclared hard dependency; not listed in requirements.txt — confirmed absent from requirements.txt:1–5]

**Entry point function:**

```python
def convert_pdf_to_md(pdf_path, output_path=None) -> str | None
```

- This is a **separate CLI utility** (`pdf_to_md.py`), not the backend's primary PDF conversion pipeline (which uses Docling in `pdf_parser.py`).

**Call signature:**

```python
md_text = pymupdf4llm.to_markdown(pdf_path)
```

Source: `pdf_to_md.py:41`

- Input: `pdf_path` (str) — path to PDF file
- Output: `md_text` (str) — Markdown text of the entire PDF (single call, no chunking)
- No chunking, no intermediate formats, no configuration parameters passed
- Result written verbatim to `output_path` with `open(output_path, 'w', encoding='utf-8')` — `pdf_to_md.py:44–45`

**Output statistics printed:**

```python
os.path.getsize(output_path)   # bytes written
len(md_text)                   # characters
md_text.count('\n')            # lines
```

Source: `pdf_to_md.py:48–57`

**Error handling:**

```python
except Exception as e:
    print(f"❌ Error durante la conversión: {str(e)}")
    return None
```

Source: `pdf_to_md.py:61–63` — no traceback printed; no re-raise; caller receives `None`.

**Validation rules (abort and return `None` before calling pymupdf4llm):**

1. `not os.path.exists(pdf_path)` → print error, return `None` — `pdf_to_md.py:23–25`
2. `not pdf_path.lower().endswith('.pdf')` → print error, return `None` — `pdf_to_md.py:28–30`

**Default output path derivation (if `output_path is None`):**

```python
output_path = pdf_path.replace('.pdf', '.md')
```

Source: `pdf_to_md.py:33–34`


### 04_look_and_feel.md (36902 chars)
# 04 — Look & Feel Specification
## NeurIPS 2026 Checklist Auditor

**Document type:** Look & Feel Specification  
**Target pipeline:** Specs2Code  
**Source extractions:** extracted_frontend_01.md, extracted_root_tests_scratch_01.md, cross_ref_resolution_cross_ref_root_to_frontend.md  

---

## 1. Page Configuration

The application is a single-page Streamlit app. `st.set_page_config()` is called as the very first Streamlit statement, before any widget-touching imports.

| Parameter | Value |
|-----------|-------|
| `page_title` | `"NeurIPS 2026 Checklist Auditor"` |
| `layout` | `"wide"` |
| `page_icon` | `"🔬"` |

No additional `st.set_page_config` parameters are present beyond the three above.

Source: extracted_frontend_01.md § 2.2 (app.py:6-10)

> **Note on cross-cluster discrepancy:** extracted_root_tests_scratch_01.md § 3.2 (app.py:25-29) documents a root-level entry point with `page_title="Nature Auditor Pro"`. The authoritative frontend module (`frontend/app.py`) uses `page_title="NeurIPS 2026 Checklist Auditor"` (extracted_frontend_01.md § 2.2). The root app.py is a separate, older entry point. The frontend/app.py value is canonical for this specification.

Source: extracted_frontend_01.md § 2.2; cross-noted in extracted_root_tests_scratch_01.md § 3.2

---

## 2. Sidebar Layout

Rendering order inside `with st.sidebar:` (top to bottom):

1. **ACM Logo Image**
   - Widget: `st.image(SIDEBAR_IMAGE, width=150)`
   - `SIDEBAR_IMAGE` constant value (exact):  
     `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"`
   - Width parameter: `150` (integer, pixels)
   - No caption parameter is set.
   - Source: extracted_frontend_01.md § 2.1 (config.py:4); § 4.3 (app.py:73)

2. **Section Header**
   - Widget: `st.markdown("### Sobre el TFG")`
   - Exact string: `"### Sobre el TFG"`
   - Source: extracted_frontend_01.md § 4.3 (app.py:74)

3. **Description Text**
   - Widget: `st.write(SIDEBAR_DESCRIPTION)`
   - `SIDEBAR_DESCRIPTION` constant value (exact):  
     `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."`
   - Source: extracted_frontend_01.md § 2.1 (config.py:5); § 4.3 (app.py:75)

No other sidebar widgets, dividers, or sections are present.

Source: extracted_frontend_01.md § 4.3 (app.py:73-76); cross_ref_resolution_cross_ref_root_to_frontend.md § g_008

---

## 3. File Upload Widget

### 3.1 Widget Definition

| Attribute | Value |
|-----------|-------|
| Widget function | `st.file_uploader` |
| Label text (exact) | `"Sube el PDF del artículo científico"` |
| `type` (accepted extensions) | `["pdf", "txt", "md"]` |
| `accept_multiple_files` | Not set (default `False`) |
| `key` | Not explicitly set (Streamlit auto-key) |

Source: extracted_frontend_01.md § 5.1 (app.py:34)

### 3.2 Processing Status Widget Sequence

When a new file is detected (deduplication condition is True), the following widget sequence is rendered inside `process_uploaded_file()`:

**Step 1 — Text extraction spinner:**
- Widget: `st.spinner("📂 Extrayendo texto...")`
- Exact spinner label: `"📂 Extrayendo texto..."`
- Active during: PDF-to-Markdown conversion or TXT/MD file read.
- Source: extracted_frontend_01.md § 5.1 (file_uploader.py:34)

**Step 2 — Audit status widget:**
- Widget: `st.status("🧠 Analizando el documento...", expanded=True)`
- Exact initial label: `"🧠 Analizando el documento..."`
- `expanded=True` on creation.
- During analysis: a nested `update_status(msg)` callback calls `st.write(msg)` inside this status block (source: file_uploader.py:46-47).
- Source: extracted_frontend_01.md § 5.1 (file_uploader.py:45)

**Step 3 — Success state:**
- Transitions the status widget: `status.update(label="✅ Análisis completado", state="complete", expanded=False)`
- Then renders: `st.success("✅ Análisis completado")`
- Source: extracted_frontend_01.md § 5.1 (file_uploader.py:90, 92)

**Step 4 — Error states (saturation):**
- `status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)`
- `st.error("### ⚠️ El servicio de IA está saturado")`
- Expander with text: `"El modelo Gemini está experimentando una demanda extremadamente alta en este momento y no ha podido completar la tarea tras 5 reintentos automáticos."`
- `st.info("Este es un problema temporal de Google. Puedes esperar unos minutos e intentar reanudar, o cancelar la ejecución actual.")`
- Two buttons: `"🔄 Reintentar ahora"` (triggers `st.rerun()`) and `"🚫 Cancelar ejecución"` (sets error state and calls `st.stop()`)
- Source: extracted_frontend_01.md § 8 RULE: SaturationErrorDetection (file_uploader.py:56-88)

**Step 5 — Error state (non-saturation critical failure):**
- `status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)`
- `st.error(f"❌ Error crítico: {error_msg}")`
- Source: extracted_frontend_01.md § 8 RULE: SaturationErrorDetection (file_uploader.py:56-88)

### 3.3 Dynamic Visibility

The entire audit results section (and all sections below it) is rendered only when `uploaded_file is not None` — i.e., the conditional block `if uploaded_file:` in app.py gates all downstream rendering.

Source: extracted_frontend_01.md § 4.2 (app.py:37)

---

## 4. Audit Results Page Layout

Rendered by `render_audit_results(resultado: dict, uploaded_file) -> health: dict`.

Source: extracted_frontend_01.md § 5.2 (audit_results.py:90)

### 4a. Success Banner

- Widget: `st.success("Auditoria Finalizada")`
- Exact message text: `"Auditoria Finalizada"` (no accent on "Auditoria")
- No additional icon parameter (Streamlit's default success icon is used).
- This is the first widget rendered inside `render_audit_results`.
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:92)

### 4b. Health Verdict Block

- Section header: `st.header("Veredicto del Checklist NeurIPS 2026")`
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:100)

Data field driving verdict: `health["status"]` (string, either `"valid"` or `"risk"`), where `health` is the return value of `get_checklist_health(resultado)`.

**Valid state:**
- Condition: `health["status"] == "valid"` (i.e., `pending_count == 0`)
- Rendered as a dark-green styled `<div>` (HTML injected via st.html or st.markdown with `unsafe_allow_html=True`)
- Primary text: `"Checklist Valido"`
- Sub-text (exact): `"Todas las respuestas tienen evidencia o justificacion documentada. El checklist esta listo para NeurIPS."`
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:102-109)

**Risk state:**
- Condition: `health["status"] == "risk"` (i.e., `pending_count > 0`)
- Rendered as a dark-red styled `<div>`
- Primary text: `"Riesgo de Desk Reject"`
- Sub-text (exact template): `"{pending} de {total} item(s) requieren accion del autor antes del envio."` where `pending = health["pending_count"]` and `total = health["total"]`
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:111-117)

### 4c. 4-Column Metrics Row

Rendered with `st.columns(4)` pattern (4 equal columns). Each column contains one `st.metric` call.

| Column | Metric Label (exact) | Value Source | Format | Source |
|--------|---------------------|--------------|--------|--------|
| col1 | `"Items Yes"` | Count of items in `health["items"]` where `"yes" in item["answer"].lower()` | Integer (count) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |
| col2 | `"Items No"` | Count of items in `health["items"]` where `"no" in item["answer"].lower()` | Integer (count) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |
| col3 | `"Items N/A"` | Count of items in `health["items"]` where `"n/a" in item["answer"].lower()` | Integer (count) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |
| col4 | `"Tiempo"` | `resultado.get("metricas", {}).get("tiempo_segundos", "N/A")` | `f"{tiempo}s"` (string) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |

No `delta` or `help` parameters are set on any of the four `st.metric` calls.

> **GAP — `tiempo_segundos`, `caracteres_leidos`, `red_flags_detectadas`, gauge score column:**  
> The extraction documents exactly 4 columns: Items Yes, Items No, Items N/A, Tiempo (from `metricas.tiempo_segundos`). The keys `caracteres_leidos` and `red_flags_detectadas` do not appear in the audit_results.py metrics row extraction. A gauge-based score column is NOT documented as part of the 4-column metrics row — the `create_gauge_chart` function is defined in `gauge_chart.py` but its call site is absent from the 14-file cluster (see GAP-ext_frontend_01-001). `[GAP: call site for create_gauge_chart not found in frontend cluster — gauge may be rendered outside the 4-column metrics row or in a caller not present in the extraction]`

Source: extracted_frontend_01.md § 5.2 (audit_results.py:121-133)

### 4d. RAG Ficha Técnica Section

- Subheader: `st.subheader("🎯 Ficha Técnica de Entrenamiento (RAG Specialist)")`
- Visibility condition: rendered only if `resultado.get("extracted_hyperparameters_hybrid", {})` is truthy.
- Caption (exact): `st.caption("Estos datos han sido extraídos mediante un escaneo profundo (RAG) de las secciones técnicas y apéndices.")`
- Layout: 4 equal columns (c1, c2, c3, c4).

| Column | Fields (in order) | Widget | Value Source | Conditional |
|--------|-------------------|--------|--------------|-------------|
| c1 | `optimizer` | `st.code` | `rag_data.get("optimizer", "N/A")` | Always if section visible |
| c1 | `learning_rate` | `st.code` | `rag_data.get("learning_rate", "N/A")` | Always if section visible |
| c2 | `batch_size` | `st.code` | `rag_data.get("batch_size", "N/A")` | Always if section visible |
| c2 | `epochs` | `st.code` | `rag_data.get("epochs", "N/A")` | Always if section visible |
| c3 | `warmup_steps` | `st.code` | `rag_data.get("warmup_steps", "N/A")` | Always if section visible |
| c3 | `weight_decay` | `st.code` | `rag_data.get("weight_decay", "N/A")` | Always if section visible |
| c4 | `hardware` | `st.info` | `rag_data.get("hardware", "N/A")` | Always if section visible |
| c4 | `random_seed` | `st.code` | `rag_data.get("random_seed", "N/A")` | Only if `rag_data.get("random_seed") and rag_data.get("random_seed") != "NOT FOUND"` |

Where `rag_data = resultado.get("extracted_hyperparameters_hybrid", {})`.

No expander wraps this section; it is rendered inline.

Source: extracted_frontend_01.md § 5.2 (audit_results.py:136-163)

### 4e. Compliance Table

See Section 5 below for full detail.

Section header: `st.header("Tabla de Cumplimiento NeurIPS 2026")`  
Caption with colour legend is shown before the table.  
Table is rendered via `st.html(_build_table_html(health["items"]))`.

Source: extracted_frontend_01.md § 5.2 (audit_results.py:167-175)

### 4f. Three Expander Sections

Rendered in this exact order (1st, 2nd, 3rd):

**1st Expander — Pipeline de Análisis Profundo**
- `st.expander` label (exact): `"Pipeline de Análisis Profundo (Map-Reduce + CoT + Context Mapping)"`
- Content (in order):
  1. Chain-of-Thought: `cot = resultado.get("informacion_extraida", {}).get("thought_process", "No disponible")`; rendered as `st.info(cot)`.
  2. Context Mapping: reads `resultado.get("informacion_extraida", {}).get("context_mapping", [])`. If non-empty: renders items in columns (up to 5 per row). If empty: `st.warning("No se ha podido mapear la estructura de secciones.")`.
  3. Comparativa Map vs Reduce (2 sub-columns):
     - Left (MAP): reads `resultado.get("general_analysis_map", [])`. If non-empty: iterates and renders each step in nested `st.expander(f"📦 Fragmento {i+1}")` with `st.json(step)`. Else: renders `resultado.get("original_extraction_raw", {})` as `st.json(...)`.
     - Right (REDUCE): renders `resultado.get("informacion_extraida", {})` as `st.json(...)`.
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:179-215)

**2nd Expander — Pipeline de Extracción Híbrida**
- `st.expander` label (exact): `"Pipeline de Extracción Híbrida (RAG Specialist)"`
- Content (in order):
  1. Left (Triage MAP): reads `resultado.get("hybrid_triage_fragments", [])`. If non-empty: iterates; for each fragment:
     - Reads `_relevance_score` (default `"N/A"`).
     - Background colour: `"#065f46"` if `isinstance(relevance, int) and relevance > 70`; else `"#1e3a5f"`.
     - Expander title: `f"📄 Fragmento Técnico {i+1} (Relevancia: {relevance}%)"`.
     - Inside: relevance badge, `_chunk_text` via `st.caption(...)`, then all non-underscore-prefixed fields via `st.json(...)`.
  2. Right (REDUCE): renders `resultado.get("extracted_hyperparameters_hybrid", {})` as `st.json(...)`.
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:218-242)

**3rd Expander — Pipeline de Evaluación**
- `st.expander` label (exact): `"Pipeline de Evaluación (Senior Area Chair + Self-Correction)"`
- Content (in order):
  1. Evaluation Signals: reads `resultado.get("evaluation_signals", {})`. If truthy: iterates dict items; for each key `k`, renders `st.markdown(f"**Item {k.replace('_', ' ').title()}:**")` then `st.info(msg)`. If falsy: `st.warning(...)` (exact text not extracted).
  2. Self-Correction verification details: collects items from `resultado` where value is a dict with `v.get('verified')` True. Falls back to second-level scanning. For each verified item:
     - Status label: `"✨ Corregido"` if `data.get('was_corrected')`, else `"✅ Confirmado"`.
     - Shown in `st.expander(...)` with answer, justification (`st.write`), and evidence (`st.code`).
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:245-283)

---

## 5. Compliance Table (Columns, Risk Annotations)

Produced by `_build_table_html(items: list) -> str`.  
Source: extracted_frontend_01.md § 5.2.1 (audit_results.py:7-87)

### 5.1 Column Definition

| Column # | Header Text (exact) | Data Field | HTML Element |
|----------|---------------------|------------|--------------|
| 1 | `"#"` | `item["label"].split(". ")[0]` (numeric part, e.g. `"1"`) | `<th>` then `<td>` |
| 2 | `"Item del Checklist"` | `item["label"].split(". ")[1]` (name part, e.g. `"Claims"`) | `<td>` |
| 3 | `"Respuesta"` | Badge HTML derived from `item["answer"]` (see §5.2) | `<td>` |
| 4 | `"Evidencia / Justificacion"` | Evidence + alert HTML (see §5.3) | `<td>` |

Label splitting logic: `item["label"]` is split on `". "`. If `". "` is not present, `str(idx)` is used as `num` and the full label as `name`. Source: audit_results.py:39-42.

### 5.2 Badge Styles (Column 3 — Respuesta)

Applied based on `item["answer"].lower()`:

| Condition | Background Color | Text Color | Displayed Text |
|-----------|-----------------|------------|----------------|
| `"yes" in answer.lower()` | `#065f46` | `#6ee7b7` | `"Yes"` |
| `"no" in answer.lower()` | `#7f1d1d` | `#fca5a5` | `"No"` |
| all other (N/A or empty) | `#1e3a5f` | `#93c5fd` | `"N/A"` |

Source: extracted_frontend_01.md § 2.6 (audit_results.py:10-16)

### 5.3 Row Background Colors (Conditional Formatting)

Applied to each `<tr>` based on risk flags in the item dict:

| Priority | Condition | Background Color | Semantic Meaning |
|----------|-----------|-----------------|-----------------|
| 1 (highest) | `item["pending_justification"] == True` | `#450a0a` | Deep red — Critical risk (No without justification) |
| 2 | `item["missing_evidence"] == True` OR `item["alert_msg"]` is non-empty (for other alert types) | `#452e0a` | Amber/orange — Warning |
| 3 | `"yes" in item["answer"].lower()` | `#064e3b` | Emerald green — OK |
| 4 (default) | All other cases | `#111827` | Neutral dark |

Source: extracted_frontend_01.md § 2.5 (audit_results.py:18-32)

### 5.4 Evidence Cell (Column 4) HTML

**When `evidence_text` is non-empty** (i.e., `item["evidence"]` exists and is not `"-"`):
```html
<span style="color:#d1d5db;">{evidence_text}</span>
```

**When `evidence_text` is empty:**
```html
<em style="color:#6b7280;">No disponible</em>
```

Source: extracted_frontend_01.md § 5.2.1 (audit_results.py:44, 48)

### 5.5 Alert Lines (Appended to Column 4 Cell)

**Alert line 1 — `pending_justification` is True:**
```html
<div style="color:#fca5a5;">&#9888; Sin justificacion del autor &mdash; Riesgo de Desk Reject</div>
```
(Full inline style extracted as: `color:#fca5a5;` with additional styling not fully detailed in extraction.)  
Source: audit_results.py:52-53

**Alert line 2 — `missing_evidence` is True:**
```html
<div style="color:#fde68a;">&#9888; Respuesta Yes sin evidencia de seccion del paper</div>
```
Source: audit_results.py:54-55

**Alert line 3 — Ethics alert (additionally appended when `"compensacion" in item["alert_msg"].lower()` OR `"etica" in item["alert_msg"].lower()`):**
```html
<div style="color:#fde68a;">&#9888; NeurIPS Code of Ethics: compensacion minima obligatoria</div>
```
Source: audit_results.py:57-58

### 5.6 Full HTML Table Structure

```html
<table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
  <thead>
    <tr>
      <th>#</th>
      <th>Item del Checklist</th>
      <th>Respuesta</th>
      <th>Evidencia / Justificacion</th>
    </tr>
  </thead>
  <tbody>
    <!-- One <tr> per item in health["items"] (16 rows total) -->
    <tr style="background-color:{row_bg};">
      <td>{num}</td>
      <td>{name}</td>
      <td>{badge_html}</td>
      <td>{evidence_html}{alert_html}</td>
    </tr>
    ...
  </tbody>
</table>
```

Source: extracted_frontend_01.md § 5.2.1 (audit_results.py:69-87)

---

## 6. Download Report Button

| Attribute | Value |
|-----------|-------|
| Widget function | `st.download_button` |
| Label text (exact) | `"📥 Descargar Informe Completo (.md)"` |
| `file_name` format (exact) | `f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md"` |
| `mime` type | `"text/markdown"` |
| `data` (file content) | The string returned by `generate_report(resultado, uploaded_file, puntuacion)` — a Markdown-formatted audit report |
| `key` parameter | Not explicitly set |

**Placement in layout:** Rendered after `render_chatbot(md_text)` call, inside the `if uploaded_file:` block, only when `resultado.get("claims")` is truthy. Preceded by `st.markdown("---")` and `st.subheader(...)` (exact subheader text not extracted).

Source: extracted_frontend_01.md § 4.2 (app.py:57-65); extracted_root_tests_scratch_01.md § 3.5 (app.py:73-79); cross_ref_resolution_cross_ref_root_to_frontend.md § g_006

**File content source:** `generate_report(resultado, uploaded_file, health=None)` produces a Markdown string with this structure:
1. `# NeurIPS 2026 Checklist Audit Report`
2. `**Paper:** {uploaded_file.name}`
3. `**Veredicto:** {status_label}` — either `"Checklist Valido"` or `"Riesgo de Desk Reject"`
4. `**Items con problemas:** {pending} de {total}`
5. `---`
6. `## Tabla de Cumplimiento` — Markdown table with header `| # | Item | Respuesta | Evidencia / Justificacion |`
7. 16 data rows — each row appends a risk note: `" [RIESGO: sin justificacion]"` if `pending_justification`, or `" [RIESGO: sin evidencia]"` if `missing_evidence`, otherwise no note.
8. Footer: `_Generado por Auditor NeurIPS 2026._`

Source: extracted_frontend_01.md § 5.2.2 (audit_results.py:287-316); cross_ref_resolution_cross_ref_root_to_frontend.md § g_006

---

## 7. SOTA Analysis Section

Rendered by `render_sota_analysis(md_text: str) -> None`.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:5); cross_ref_resolution_cross_ref_root_to_frontend.md § g_007

### 7.1 Section Header and Divider

1. `st.markdown("---")` — horizontal divider above the section.
2. `st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")` — exact string.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:5)

### 7.2 Trigger Button

- Widget: `st.button("Ejecutar Análisis de Literatura Reciente")`
- Label (exact): `"Ejecutar Análisis de Literatura Reciente"`
- No explicit `key` parameter.
- The entire analysis block (spinner, results) is rendered conditionally on this button press.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:10)

### 7.3 Spinner During SOTA Fetch

- Widget: `st.spinner("Conectando con Semantic Scholar y validando bibliografía...")`
- Exact spinner text: `"Conectando con Semantic Scholar y validando bibliografía..."`
- Wraps the `st.session_state.sota_analyzer.analyze_sota(md_text)` call.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:12)

### 7.4 Post-Fetch Success Display (when `"error" not in resultado_sota`)

1. `st.success("Análisis completado")` — exact text.
2. Conclusion section:
   - `st.markdown("### 📝 Conclusión")`
   - `st.info(resultado_sota.get('conclusion_sota', ''))` — content from `conclusion_sota` key.
3. Papers dataframe and missing-paper recommendations rendered by `_render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)` — see §7.5.
   - Only called when `not df_papers.empty and papers_omitidos` both true.
   - If `not papers_omitidos`: renders `st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")`.

### 7.5 Missing Papers Recommendations Sub-section

Header: `st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")`  
Caption: `st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")`  

Papers displayed as `st.dataframe` with these columns and column configs:

| Column Name | Config Type | Width |
|-------------|-------------|-------|
| `"Título"` | TextColumn | `"large"` |
| `"Autores"` | TextColumn | `"medium"` |
| `"Año"` | NumberColumn | `"small"` |
| `"Posterior"` (label: `"Posterior al tuyo"`) | TextColumn | `"small"` |
| `"Citas"` | NumberColumn | `"small"` |
| `"Relevancia"` | TextColumn | `"small"` |
| `"Subtema"` | TextColumn | `"medium"` |
| `"Justificación"` | TextColumn | `"large"` |

Source: extracted_frontend_01.md § 5.5.1 (sota_section.py:85-101)

**`"Posterior"` cell values:**
- `"✅ Sí"` — when `año_paper_estudiado AND paper['year'] > año_paper_estudiado`
- `"❌ No"` — when `año_paper_estudiado AND NOT (paper['year'] > año_paper_estudiado)`
- `"?"` — when `not año_paper_estudiado`

**Sort order:** Not explicitly specified in extraction. `[GAP: sort order of the papers dataframe not extracted]`

**Footer captions (conditional):**
- When `año_paper_estudiado` is truthy: `st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")`
- When falsy: `st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")`

If `df_no_citados` is empty: `st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")`

Source: extracted_frontend_01.md § 5.5.1 (sota_section.py:31-108)

### 7.6 Error Display

When `"error" in resultado_sota`:
- `st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")`

Source: extracted_frontend_01.md § 5.5 (sota_section.py:29)

### 7.7 Conditional Visibility

The entire analysis (results, dataframe, recommendations) is only shown after the button is clicked (standard Streamlit button stateless pattern — renders on the same rerun as the button press).

---

## 8. Chatbot Interface

Rendered by `render_chatbot(md_text: str) -> None`.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:4); cross_ref_resolution_cross_ref_root_to_frontend.md § g_007, § g_027

### 8.1 Section Header and Divider

1. `st.markdown("---")` — horizontal divider.
2. `st.header("💬 Pregunta al Revisor")` — exact header string.
3. `st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")` — exact caption string.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:4-9)

### 8.2 Conversation History Display

- Iterates `st.session_state.messages` (a list of `{"role": str, "content": str}` dicts).
- For each message: `st.chat_message(message["role"])` container wrapping `st.markdown(message["content"])`.
- Roles present at runtime: `"user"` and `"assistant"`.
- Message template (how history is built for the chatbot backend, not for display): `f"{m['role']}: {m['content']}"` — applied to the last 4 messages joined with `"\n"` to form `history_str`.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:10-12, 23)

### 8.3 Text Input Widget

| Attribute | Value |
|-----------|-------|
| Widget function | `st.text_input` |
| Label (exact) | `"Escribe tu pregunta:"` |
| `key` | `"chat_input"` |
| `placeholder` (exact) | `"Ej: ¿En qué página falla el paper en su estadística?"` |

Source: extracted_frontend_01.md § 5.3 (chatbot.py:14-18)

### 8.4 Submit Button Widget

| Attribute | Value |
|-----------|-------|
| Widget function | `st.button` |
| Label (exact) | `"Enviar"` |
| `key` | `"send_button"` |

Submit guard rule: the chatbot backend is called only when `st.button("Enviar")` AND `prompt_usuario` is truthy (non-empty input). A button click with empty input is silently ignored.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:20); § 8 RULE: ChatSubmitGuard

### 8.5 On-Submit Spinner

- Widget: `st.spinner("El revisor está analizando tu consulta...")`
- Exact text: `"El revisor está analizando tu consulta..."`
- Wraps the `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` call.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:24-26)

### 8.6 Session State Keys (Link to g_027 — `initialize_session_state`)

The chatbot interface depends on these session state keys:

| Key | Type | Default Value (from `initialize_session_state`) | Set/Modified By | Read By |
|-----|----|---|---|---|
| `messages` | `list` of `{"role": str, "content": str}` dicts | `[]` | `session_state.py:20-21` (init); `file_uploader.py:21` (reset on new file); `chatbot.py:21,28` (appends) | `chatbot.py:10, 23` |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | `session_state.py:14-15` (init only) | `chatbot.py:26` |

Guard condition in `initialize_session_state`: `if "key" not in st.session_state` — idempotent, never overwrites existing values.

Source: cross_ref_resolution_cross_ref_root_to_frontend.md § g_027 (session_state.py:7)

### 8.7 Post-Submit Flow

1. Append `{"role": "user", "content": prompt_usuario}` to `st.session_state.messages`.
2. Build `history_str` from last 4 messages: `"\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])`.
3. Call `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` → `respuesta_ia`.
4. Append `{"role": "assistant", "content": respuesta_ia}` to `st.session_state.messages`.
5. Call `st.rerun()` to refresh conversation display.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:21-29)

---

## 9. Gauge Chart (Quality Tiers and Colors)

Defined in `frontend/components/gauge_chart.py`.

Source: extracted_frontend_01.md § 5.4 and § 2.4 (gauge_chart.py:4-71)

### 9.1 Function Signature

```
create_gauge_chart(score: float) -> plotly.graph_objects.Figure
```

- Parameter: `score` — numeric value in range [0, 100].
- Return type: `plotly.graph_objects.Figure`.
- Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:4)

### 9.2 Plotly Figure Type

- Figure type: `go.Figure(go.Indicator(...))`
- Indicator mode: `"gauge+number"`
- `value`: `score`
- `domain`: `{'x': [0, 1], 'y': [0, 1]}`

Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:33-71)

### 9.3 NeurIPS Quality Tier Thresholds and Colors

The tier determines both `label` (title sub-text) and `color_barra` (gauge bar color).

| Tier Label | Score Min (inclusive) | Score Max (exclusive, except last) | Bar Color (hex) | Color Name |
|-----------|-----------------------|-------------------------------------|-----------------|------------|
| `"Strong Accept"` | 87.5 | 100 (inclusive) | `#00aa00` | Dark green |
| `"Accept"` | 75 | 87.5 | `#00cc44` | Green |
| `"Borderline"` | 62.5 | 75 | `#ffcc00` | Yellow |
| `"Weak Reject"` | 50 | 62.5 | `#ff9900` | Orange |
| `"Reject"` | 25 | 50 | `#ff4b4b` | Red |
| `"Strong Reject"` | 0 | 25 | `#cc0000` | Dark red |

Source: extracted_frontend_01.md § 2.4 (gauge_chart.py:14-31)

### 9.4 Threshold Line

- Value: `62.5` (marks the Borderline boundary)
- Color: `"red"`
- Width: `4`

Source: extracted_frontend_01.md § 2.4 (gauge_chart.py:57-61)

### 9.5 Gauge Axis and Bar Properties

- Gauge axis range: `[0, 100]`
- Tick mode: linear; `tick0=0`; `dtick=25`
- Bar: `color=color_barra`, `thickness=0.8`, line `color="black"`, `width=2`
- Gauge: `bgcolor="white"`, `borderwidth=2`, `bordercolor="black"`
- Background steps: coloured segments matching each of the 6 tiers (exact step color values equal the bar colors in §9.3)

Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:33-71)

### 9.6 Title and Layout Properties

- `title`: `{'text': f"Quality Score<br><sub>{label}</sub>", 'font': {'size': 18}}`
- `number`: `{'suffix': "%", 'font': {'size': 40}}`
- Layout `height`: `300`
- Layout margins: `l=10`, `r=10`, `t=50`, `b=25`
- `paper_bgcolor`: transparent
- Font color: `#E5E7EB`

Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:33-71)

### 9.7 Call Site Gap

> `[GAP: create_gauge_chart is not called from any of the 14 files in the frontend cluster (GAP-ext_frontend_01-001). A caller that passes a numeric score (0-100) and renders the Figure via st.plotly_chart() is expected but not found in the extraction. Likely location: audit_results.py or a caller outside the frontend package.]`

---

## 10. Custom CSS (All Selectors and Property Values)

Defined in `CUSTOM_CSS` constant in `frontend/styles/custom_css.py`.  
Link to g_026 (`apply_custom_styles`): the function `apply_custom_styles()` injects all CSS below by calling `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)`. It takes no parameters and returns None. It is called unconditionally on every page render, as the second statement after `st.set_page_config()` (app.py:21).

Source: extracted_frontend_01.md § 6 (custom_css.py:4-86); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### Selector: `.stApp`

| Property | Value |
|----------|-------|
| `background-color` | `#374151 !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### Selector: `#MainMenu`

| Property | Value |
|----------|-------|
| `visibility` | `hidden` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `footer`

| Property | Value |
|----------|-------|
| `visibility` | `hidden` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `header`

| Property | Value |
|----------|-------|
| `background-color` | `transparent !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"]`

| Property | Value |
|----------|-------|
| `background-color` | `#2d3436 !important` |
| `border-radius` | `15px !important` |
| `padding` | `5px !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### Selector: `[data-testid="stTable"] table`

| Property | Value |
|----------|-------|
| `border-collapse` | `collapse !important` |
| `width` | `100% !important` |
| `border` | `none !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] th`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `font-weight` | `800 !important` |
| `background-color` | `#3d4446 !important` |
| `border` | `1px solid #4a4a4a !important` |
| `padding` | `12px !important` |
| `text-transform` | `capitalize !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] th *`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `font-weight` | `800 !important` |
| `text-decoration` | `none !important` |
| `border` | `none !important` |
| `text-transform` | `capitalize !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] tbody th`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `background-color` | `#2d3436 !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] tbody th *`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `background-color` | `transparent !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] td`

| Property | Value |
|----------|-------|
| `color` | `#E2E8F0 !important` |
| `font-size` | `13.5px !important` |
| `font-weight` | `400 !important` |
| `background-color` | `transparent !important` |
| `border` | `1px solid #4a4a4a !important` |
| `padding` | `12px !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] td *`

| Property | Value |
|----------|-------|
| `color` | `#E2E8F0 !important` |
| `font-size` | `13.5px !important` |
| `font-weight` | `400 !important` |
| `text-decoration` | `none !important` |
| `border` | `none !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stPlotlyChart"]`

| Property | Value |
|----------|-------|
| `background-color` | `#2d3436 !important` |
| `border-radius` | `15px !important` |
| `padding` | `10px !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### CSS Injection Mechanism (`apply_custom_styles`)

```python
def apply_custom_styles() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
```

- The entire `CUSTOM_CSS` string constant is a `<style>...</style>` HTML block.
- Injected via `st.markdown(..., unsafe_allow_html=True)`.
- Called unconditionally at application startup (app.py:21), before any widget rendering.
- No conditions under which it is skipped.

Source: extracted_frontend_01.md § 6 (custom_css.py:85-86); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

## Appendix A: Complete Session State Reference

All session state keys used by the frontend, merged from all components:

| Key | Type | Default Value | Initialised By | Modified By |
|-----|------|---------------|----------------|-------------|
| `resultado` | `dict` or `None` | `None` | `session_state.py:8-9` | `file_uploader.py:49-52, 85` |
| `auditor` | `PaperAuditor` instance | `PaperAuditor()` | `session_state.py:11-12` | Never (stateful object) |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | `session_state.py:14-15` | Never (stateful object) |
| `sota_analyzer` | `SotaAnalyzer` instance | `SotaAnalyzer()` | `session_state.py:17-18` | Never (stateful object) |
| `messages` | `list` of `{"role": str, "content": str}` | `[]` | `session_state.py:20-21` | `file_uploader.py:21` (reset), `chatbot.py:21, 28` (append) |
| `archivo_actual` | `str` | Not pre-initialised | `file_uploader.py:19` | `file_uploader.py:19` |
| `file_hash` | `str` (MD5 hex) | Not pre-initialised | `file_uploader.py:20` | `file_uploader.py:20` |
| `md_text` | `str` | Not pre-initialised | `file_uploader.py:36-39` | `file_uploader.py:36-39` |

Link to g_027: `initialize_session_state()` (session_state.py:7) initialises the first 5 keys only, using `if "key" not in st.session_state` guards.

Source: extracted_frontend_01.md § 3; cross_ref_resolution_cross_ref_root_to_frontend.md § g_027

---

## Appendix B: Full Top-Level Rendering Order

```
1. st.set_page_config(page_title="NeurIPS 2026 Checklist Auditor", layout="wide", page_icon="🔬")
2. apply_custom_styles()                          — injects CUSTOM_CSS
3. initialize_session_state()                    — guards 5 session keys
4. st.title(TITLE)                               — "💻 Auditor de Papers en Ciencias de la Computación"
5. st.markdown("---")                            — horizontal rule
6. st.button("🔄 Limpiar y subir nuevo archivo") — clears all session state + st.rerun()
7. st.file_uploader("Sube el PDF del artículo científico", type=["pdf","txt","md"])
8. [if uploaded_file:]
   8a. process_uploaded_file(uploaded_file)       — extract + audit; manages st.spinner / st.status
   8b. [error branches — see §3.2, §8 Business Rules]
   8c. render_audit_results(resultado, uploaded_file)
   8d. render_sota_analysis(md_text)
   8e. render_chatbot(md_text)
   8f. st.markdown("---") + st.subheader(...) + st.download_button(...)
9. [with st.sidebar:]
   st.image(SIDEBAR_IMAGE, width=150)
   st.markdown("### Sobre el TFG")
   st.write(SIDEBAR_DESCRIPTION)
```

Source: extracted_frontend_01.md § 4.2 (app.py)


### 05_test_scenarios.md (56604 chars)
# 05 — Test Scenario Specifications

This document consolidates all test scenarios extracted from the legacy codebase into a single authoritative reference for the Specs2Code pipeline. Every scenario is traceable to its extraction source. Sections follow the prescribed order. GAP markers are preserved verbatim where the extraction data was absent or incomplete.

---

## LLM Client Retry Logic Tests

### `scratch/test_llm_retry.py` — Overview

**Type:** Unit test with mocks (script-level, not pytest).  
**Framework:** Python `unittest.mock` (`MagicMock`, `patch`).  
**Module under test:** `backend.common.llm_client.LLMClient`  
**Module-level mock setup:** `google`, `google.genai`, and `streamlit` are injected into `sys.modules` before any import of `LLMClient` to prevent real API calls at import time.

> Source: extracted_root_tests_scratch_01.md § 11.10

---

#### `test_retry_logic` — Success Within Retry Budget

```
TEST: test_retry_logic
RULE: RULE-06 — LLMClient succeeds after transient failures (LLM retries — success within retries)
MOCK_SETUP:
  - client = LLMClient(model_name="test-model")
  - mock_gen = MagicMock()
  - client.client.models.generate_content = mock_gen
  - mock_gen.side_effect = [
        Exception("503 UNAVAILABLE: High demand"),   # attempt 0 — fail
        Exception("503 UNAVAILABLE: High demand"),   # attempt 1 — fail
        MagicMock(text="Success response")           # attempt 2 — success
    ]
  - patch('time.sleep') as mock_sleep   (suppresses real sleep)
  - Outer patch context:
      patch('backend.common.config.GOOGLE_API_KEY', "test-key")
      patch('backend.common.config.MODEL_NAME',     "test-model")
TRIGGER: response = client.generate("test prompt")
POSITIVE CASE:
  INPUT: Two transient 503 exceptions followed by a successful response on the 3rd call.
  EXPECTED:
    - No exception raised; function returns the MagicMock with .text == "Success response".
    - mock_gen.call_count == 3   (2 failures + 1 success)
    - mock_sleep.call_count == 2  (one sleep per retry before the success)
NEGATIVE CASE:
  INPUT: N/A — the negative exhaustion path is covered by test_final_failure.
  EXPECTED: N/A
SOURCE: extracted_root_tests_scratch_01.md § 11.10, RULE-06
```

> **Rule Reference:** RULE-06 — LLMClient succeeds after transient failures  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-06), § 11.10

---

#### `test_final_failure` — Full Retry Exhaustion (6-Attempt Scenario)

```
TEST: test_final_failure
RULE: RULE-05 — LLMClient maximum retry attempts
MOCK_SETUP:
  - client = LLMClient(model_name="test-model")
  - mock_gen = MagicMock()
  - mock_gen.side_effect = Exception("503 UNAVAILABLE: High demand")   # always fails
  - patch('time.sleep') as mock_sleep
  - Outer patch context:
      patch('backend.common.config.GOOGLE_API_KEY', "test-key")
      patch('backend.common.config.MODEL_NAME',     "test-model")
TRIGGER: client.generate("test prompt")   — expected to raise
POSITIVE CASE (exhaustion — "positive" that the guard fires):
  INPUT: Every attempt to call generate_content raises the same 503 exception.
  EXPECTED:
    - An exception IS raised from client.generate (test asserts False if no exception raised;
      the except block catches and verifies the exception occurred).
    - mock_gen.call_count == 6  (1 original attempt at index 0 + 5 retries at indices 1–5)
    - mock_sleep.call_count == 5  (one sleep between each consecutive failing attempt)
    - The caught exception is re-raised (the test block reads:
        try:
            client.generate("test prompt")
            assert False, "Should have raised an exception"
        except Exception as e:
            print(f"Caught expected final exception: {e}")
            assert mock_gen.call_count == 6
      )
NEGATIVE CASE:
  INPUT: If client.generate did NOT raise, the assert False sentinel would trigger AssertionError.
  EXPECTED: The sentinel AssertionError ("Should have raised an exception") is the failure signal.
SOURCE: extracted_root_tests_scratch_01.md § 11.10, RULE-05
```

> **Rule Reference:** RULE-05 — LLMClient maximum retry attempts  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-05), § 10.8, § 10.11

---

### LLMClient Business Rules Confirmed by Tests

| Constant | Value | Source |
|----------|-------|--------|
| `max_retries` | `5` | `llm_client.py:39` |
| `base_delay` | `2` seconds | `llm_client.py:40` |
| Total attempts | `6` (= `max_retries + 1`) | `llm_client.py:42` |
| Retryable error codes | `"503"`, `"429"`, `"UNAVAILABLE"`, `"RESOURCE_EXHAUSTED"`, `"DEADLINE_EXCEEDED"` (substring match in uppercased error string) | `llm_client.py:54` |
| Backoff formula | `delay = base_delay * (2 ** attempt) + random.uniform(0, 1)` | `llm_client.py:58` |
| Sleep call count on success at 3rd attempt | `2` | RULE-06 / test_retry_logic |
| Sleep call count on total exhaustion | `5` | RULE-05 / test_final_failure |

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY [g_012]; extracted_backend_core_01.md § 3.1

---

## Information Extraction Skill Tests (section fragmenting, MAP/REDUCE)

### `tests/test_section_splitter.py` — Overview

**Type:** Script with assertions (no pytest or unittest).  
**Module under test:** `backend.skills.auditor_skills.InformationExtractionSkill`  
**Fragmentation method:** Internal MAP-phase section-splitting logic, exposed by a `TestSkill` subclass.

> Source: extracted_root_tests_scratch_01.md § 11.14

---

#### `test_splitting_logic` — Fragment Count from 6-Section Paper

```
TEST: test_splitting_logic
RULE: RULE-09 — Section fragmentation produces at most 4 fragments from a multi-section paper
      BR-TEST-08 — 6 equal-length sections produce exactly 4 fragments
MOCK_SETUP:
  - class MockLLM:
        def generate(self, prompt):
            return type('obj', (object,), {'text': '{}'})()
    (Returns empty JSON object; prevents real LLM calls during fragment testing)
  - skill = InformationExtractionSkill(llm_client=MockLLM())
  - class TestSkill(InformationExtractionSkill):
        def get_fragments(self, paper_text):
            # Exposes internal fragmentation logic of execute():
            paper_text_norm = paper_text.replace('\r\n', '\n')
            sections = re.split(r'\n(?=#+ )', '\n' + paper_text_norm)
            sections = [s.strip() for s in sections if s.strip()]
            if len(sections) > 1:
                total_chars = sum(len(s) for s in sections)
                target = total_chars / 4
                fragments = []
                current_fragment = ""
                for section in sections:
                    if (len(current_fragment) + len(section) > target
                            and len(fragments) < 3):
                        if current_fragment:
                            fragments.append(current_fragment)
                            current_fragment = section
                        else:
                            fragments.append(section)
                    else:
                        current_fragment += ("\n\n" if current_fragment else "") + section
                if current_fragment:
                    fragments.append(current_fragment)
                return fragments
            return []
  - test_skill = TestSkill(llm_client=MockLLM())
TRIGGER: fragments = test_skill.get_fragments(paper_text)
INPUT FIXTURE (paper_text):
  6 equal-length sections:
    "# Section 1\nContent 1.\n"
    "# Section 2\nContent 2.\n"
    "# Section 3\nContent 3.\n"
    "# Section 4\nContent 4.\n"
    "# Section 5\nContent 5.\n"
    "# Section 6\nContent 6.\n"
  (All sections have identical byte length — SOURCE: tests/test_section_splitter.py:11-23)
POSITIVE CASE:
  INPUT: 6 equal-length Markdown-header sections.
  EXPECTED:
    - len(fragments) == 4   (assert message: "Expected 4 fragments, got {len(fragments)}")
    - For each fragment f: len(f) > 0
NEGATIVE CASE:
  INPUT: Paper text with no Markdown headers (no `# ` patterns).
  EXPECTED:
    - len(sections) <= 1 after split on r'\n(?=#+ )'
    - get_fragments returns []   (early-exit guard at len(sections) <= 1)
SOURCE: extracted_root_tests_scratch_01.md § 11.14, RULE-09, BR-TEST-08
```

> **Rule Reference:** RULE-09 — Section fragment count cap; BR-TEST-08  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-09), § 12 (BR-TEST-08)

---

### Fragmentation Algorithm — Confirmed Constants

| Constant | Value | Source |
|----------|-------|--------|
| Section split regex | `r'\n(?=#+ )'` (prepend `'\n'` to paper text first) | `tests/test_section_splitter.py:44` |
| Target fragment size | `total_chars / 4` | `tests/test_section_splitter.py:49` |
| Maximum early fragment boundaries | `3` (i.e., `len(fragments) < 3`) | `tests/test_section_splitter.py:54` |
| Expected output fragment count (6 equal sections) | `4` | `tests/test_section_splitter.py:75` |

> Source: extracted_root_tests_scratch_01.md § 8, § 9.7

---

### MAP/REDUCE Pipeline Rules (from InformationExtractionSkill)

The MAP/REDUCE pipeline is invoked inside `InformationExtractionSkill.execute()`, not directly tested by `test_section_splitter.py`. The test focuses only on the section-fragment boundary computation. The following MAP/REDUCE rules are confirmed by extraction:

| Phase | Rule | Source |
|-------|------|--------|
| MAP | If `len(sections) > 1`, split text into up to 4 fragments using `total_chars / 4` target | `auditor_skills.py:36` |
| MAP fallback | If no headers detected, use `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)`, take first 4 fragments | `auditor_skills.py:77` |
| MAP LLM call | `get_map_extraction_prompt(fragment)` per fragment; result parsed as JSON | `auditor_skills.py:77` (cross-ref `prompts.py:184`) |
| REDUCE | `get_reduce_extraction_prompt(map_results)` with serialized list of MAP results; consolidates into DEFINITIVE MASTER JSON | `prompts.py:228` |

> Source: extracted_backend_skills_01.md § 3.2; extracted_backend_core_01.md § 2.2

---

## RAG Logical Block Splitting Tests

### `tests/test_rag_logical_splitter.py` — Integration Test

**Type:** Script with assertions (no pytest or unittest).  
**Splitting strategy:** Double-newline paragraph split with minimum chunk length filter.

> Source: extracted_root_tests_scratch_01.md § 11.13

---

#### `test_rag_logical_splitter` — Chunk Count and Content Assertions

```
TEST: test_rag_logical_splitter
RULE: RULE-08 — RAG chunk minimum filtering (len > 10 after strip)
      BR-TEST-06 — Second chunk (index 1) must contain Abstract heading
      BR-TEST-07 — Table header and data must remain in same chunk
MOCK_SETUP: None (inline processing, no mocks)
TRIGGER: (inline script execution)
INPUT FIXTURE (paper_text):
  Multi-line string with the following double-newline-separated sections:
    - "Title" section (Title)
    - "Abstract" section
    - "Introduction" section
    - A Markdown table block containing "| Table 1 |" header row and "Data 1" data row
    - "Final word" section
  (SOURCE: tests/test_rag_logical_splitter.py:10-25)
PROCESSING (inline, no helper function):
  1. paper_text_norm = paper_text.replace('\r\n', '\n')
  2. raw_chunks = re.split(r'\n\n+', paper_text_norm)
  3. chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]
POSITIVE CASE:
  INPUT: Well-formed multi-section paper text with all required sections present.
  EXPECTED (4 assertions):
    - len(chunks) >= 4
    - "| Table 1 |" in chunks[3]   (table header retained in chunk at index 3)
    - "Data 1" in chunks[3]        (table data row retained in same chunk as header)
    - "Abstract" in chunks[1]      (Abstract section is second chunk)
NEGATIVE CASE (minimum length filter):
  INPUT: A chunk whose stripped content is <= 10 characters long (e.g., "OK" or "Hi").
  EXPECTED: The chunk is excluded from the output list.
SOURCE: extracted_root_tests_scratch_01.md § 11.13, RULE-08, BR-TEST-06, BR-TEST-07
```

> **Rule References:** RULE-08, BR-TEST-06, BR-TEST-07  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-08), § 12 (BR-TEST-06, BR-TEST-07)

---

### `scratch/test_rag_split.py` — Naive Chunking Scratch Test

**Type:** Exploratory/scratch script. No assertions. Observation-only output.

> Source: extracted_root_tests_scratch_01.md § 11.11

---

#### `get_rag_chunks` — Naive Paragraph Split (no minimum length)

```
TEST: test_rag_split (scratch/exploratory)
RULE: N/A — no business assertions; naive chunking for observation
MOCK_SETUP: None
FUNCTION UNDER TEST:
  def get_rag_chunks(paper_text):
      paper_text_norm = paper_text.replace('\r\n', '\n')   # SOURCE: scratch/test_rag_split.py:5
      raw_chunks = re.split(r'\n\n+', paper_text_norm)     # SOURCE: scratch/test_rag_split.py:22
      return [c.strip() for c in raw_chunks if c.strip()]  # SOURCE: scratch/test_rag_split.py:23
  NOTE: No minimum length filter — differs from tests/test_rag_logical_splitter.py which requires len > 10.
TRIGGER: chunks = get_rag_chunks(test_text)
INPUT FIXTURE (test_text):
  Multi-line string with sections: Title, Abstract, Introduction, Table, Final text sections.
  (SOURCE: scratch/test_rag_split.py:28-43)
POSITIVE CASE:
  INPUT: Well-formed multi-section paper text.
  EXPECTED (observation only — no assertions):
    - Total chunk count printed as "Total chunks: {len(chunks)}"
    - Each chunk printed with a header separator
    - [GAP: chunk schema not extracted — cannot define assertions]
NEGATIVE CASE:
  INPUT: Text with only whitespace-only paragraphs between double newlines.
  EXPECTED: Empty-after-strip chunks are filtered out; non-empty result expected if any real text present.
SOURCE: extracted_root_tests_scratch_01.md § 11.11, § 9.5
```

> Source: extracted_root_tests_scratch_01.md § 9.5 (transformation), § 11.11

---

### Comparison: Naive Chunker vs. Length-Filtered Chunker

| Attribute | `scratch/test_rag_split.py` (`get_rag_chunks`) | `tests/test_rag_logical_splitter.py` |
|-----------|-----------------------------------------------|---------------------------------------|
| Split regex | `r'\n\n+'` | `r'\n\n+'` |
| Filter | Excludes empty (whitespace-only) | Excludes `len <= 10` after strip |
| Assertions | None (observation only) | 4 assertions (len, content, index) |
| Test type | Exploratory scratch | Integration test |

> Source: extracted_root_tests_scratch_01.md § 9.5, § 9.6

---

## Audit Data Model Tests (AuditState, ExtractedInfo, ChecklistItem)

### `tests/test_audit_state.py` — Overview

**Type:** `unittest.TestCase` (standard pytest-discoverable).  
**Import:** `from backend.common.audit_state import AuditState, ExtractedInfo, ChecklistItem`  
**Source:** `tests/test_audit_state.py:2`

> Source: extracted_root_tests_scratch_01.md § 11.12

---

### AuditState — Field Defaults

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `paper_text` | `str` | No | (required constructor arg) | Must be set at construction | `tests/test_audit_state.py:7` |
| `invalid_paper` | `bool` | No | `False` | `assertFalse` | `tests/test_audit_state.py:9` |
| `execution_time` | `float` | No | `0.0` | `assertEqual(0.0)` | `tests/test_audit_state.py:10` |
| `evaluation` | `dict` or `None` | Yes | `None` (optional constructor kwarg) | Used by `to_frontend_dict()` | `tests/test_audit_state.py:13` |

> Source: extracted_root_tests_scratch_01.md § 11.12 (RULE-14, RULE-15)

---

#### `test_initialization` — AuditState Default Values

```
TEST: test_initialization
RULE: RULE-14 — AuditState initializes with correct defaults
MOCK_SETUP: None
TRIGGER: state = AuditState(paper_text="Test content")
POSITIVE CASE:
  INPUT: Single string argument "Test content" passed to constructor.
  EXPECTED:
    - state.paper_text == "Test content"   (assertEqual)
    - state.invalid_paper == False         (assertFalse)
    - state.execution_time == 0.0          (assertEqual)
NEGATIVE CASE:
  INPUT: Constructing AuditState without paper_text (or with a missing required field).
  EXPECTED: [GAP: response schema not extracted — cannot define assertions; AuditState constructor
             signature not fully extracted; test does not cover this path]
SOURCE: extracted_root_tests_scratch_01.md § 11.12, RULE-14
```

> **Rule Reference:** RULE-14  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-14)

---

#### `test_to_frontend_dict` — Output Key Contract

```
TEST: test_to_frontend_dict
RULE: RULE-15 — to_frontend_dict output must contain claims, informacion_extraida, metricas keys
      BR-TEST-05 — to_frontend_dict() always includes informacion_extraida and metricas keys
MOCK_SETUP: None
TRIGGER: d = state.to_frontend_dict()
POSITIVE CASE:
  INPUT: state = AuditState(paper_text="Test", evaluation={"claims": {"answer": "Yes"}})
  EXPECTED:
    - d["claims"]["answer"] == "Yes"        (assertEqual)
    - "informacion_extraida" in d           (assertIn)
    - "metricas" in d                       (assertIn)
NEGATIVE CASE:
  INPUT: AuditState constructed with evaluation=None or evaluation={}.
  EXPECTED: [GAP: response schema not extracted — cannot define assertions for empty/None
             evaluation path in to_frontend_dict()]
SOURCE: extracted_root_tests_scratch_01.md § 11.12, RULE-15, BR-TEST-05
```

> **Rule Reference:** RULE-15; BR-TEST-05  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-15), § 12 (BR-TEST-05)

---

### ExtractedInfo — Nested Sub-Model Defaults

| Sub-model | Field | Type | Nullable | Default | Source |
|-----------|-------|------|----------|---------|--------|
| `code` | `repository_url` | `str` | No | `"NOT FOUND"` | `tests/test_audit_state.py:22` |
| `hyperparameters` | `optimizer` | `str` | No | `"NOT FOUND"` | `tests/test_audit_state.py:23` |

> Source: extracted_root_tests_scratch_01.md § 11.12 (RULE-16, RULE-17)

---

#### `test_extracted_info_nesting` — Sub-Model Default Values

```
TEST: test_extracted_info_nesting
RULE: RULE-16 — ExtractedInfo.code.repository_url defaults to "NOT FOUND"
      RULE-17 — ExtractedInfo.hyperparameters.optimizer defaults to "NOT FOUND"
MOCK_SETUP: None
TRIGGER: info = ExtractedInfo()
POSITIVE CASE:
  INPUT: Default instantiation with no arguments.
  EXPECTED:
    - info.code.repository_url == "NOT FOUND"      (assertEqual)
    - info.hyperparameters.optimizer == "NOT FOUND" (assertEqual)
NEGATIVE CASE:
  INPUT: ExtractedInfo constructed with an explicit repository_url value (e.g., "https://github.com/user/repo").
  EXPECTED: [GAP: response schema not extracted — cannot define assertions for non-default construction paths]
SOURCE: extracted_root_tests_scratch_01.md § 11.12, RULE-16, RULE-17
```

> **Rule Reference:** RULE-16, RULE-17  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-16, RULE-17)

---

### ChecklistItem — Model Specification

[GAP: ChecklistItem field definitions not extracted from `backend/common/audit_state.py` — the source file (`backend/common/audit_state.py`) was confirmed absent from the extraction cluster. The model is imported in `tests/test_audit_state.py:2` but no test scenario exercises ChecklistItem directly. Cannot define field table or test assertions without source.]

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § [g_014] — UNRESOLVED

---

## Audit Pipeline Integration Tests

### `test_auditor_refactor.py` — Overview

**Type:** Script-based integration tests (not pytest). Uses a custom `main()` runner.  
**Error handling:** Every test function is wrapped in `try/except Exception`; returns `True` on pass, `False` on failure. Failures print `"❌ Error …: {e}"`. The `main()` function collects `(name, bool)` tuples and prints a summary.

> Source: extracted_root_tests_scratch_01.md § 11.1

---

#### `test_auditor_initialization` — PaperAuditor Constructor Smoke Test

```
TEST: test_auditor_initialization
RULE: RULE-10 — PaperAuditor must expose exactly 6 skill attributes (verified in test_skills_integration;
      this test verifies the constructor does not raise)
MOCK_SETUP: None (real initialization; requires GOOGLE_API_KEY in environment)
TRIGGER: auditor = PaperAuditor()
POSITIVE CASE:
  INPUT: No arguments (constructor takes none).
  EXPECTED:
    - No exception raised → function returns True.
    - PaperAuditor() creates 5 LLMClient instances and 6 skill instances (confirmed by source).
NEGATIVE CASE:
  INPUT: GOOGLE_API_KEY missing from environment.
  EXPECTED:
    - LLMClient.__init__ raises ValueError("No se encontró la GOOGLE_API_KEY en el .env").
    - The except block catches it → prints "❌ Error al inicializar auditor: {e}" → returns False.
    - main() reports test as FAIL.
SOURCE: extracted_root_tests_scratch_01.md § 11.1
```

> Source: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_009]

---

#### `test_regex_patterns` — REGEX_PATTERNS Import Smoke Test

```
TEST: test_regex_patterns
RULE: REGEX_PATTERNS must have len > 0 when imported from backend.services.auditor
MOCK_SETUP: None
TRIGGER: from backend.services.auditor import REGEX_PATTERNS; assert len(REGEX_PATTERNS) > 0
POSITIVE CASE:
  INPUT: REGEX_PATTERNS is defined at module level in auditor.py with at least 1 entry.
  EXPECTED: assertion passes → returns True.
NEGATIVE CASE (DEPLOYMENT READINESS SIGNAL — EXPECTED TO FAIL):
  INPUT: Current codebase post-refactoring.
  EXPECTED:
    - ImportError raised: `REGEX_PATTERNS` does not exist in `backend/services/auditor.py` in
      the current (post-refactoring) version.
    - The except block catches it → prints "❌ Error en patrones regex: {e}" → returns False.
    - This test is expected to FAIL on the current codebase.
    - The regex patterns that were previously inlined in auditor.py now live as class-level
      PATTERNS attributes on individual skill classes in regex_detection_skills.py.
NOTE: This test signals a pre-refactor/post-refactor API break. The test must be updated
      to reference per-skill PATTERNS class attributes (e.g., HyperparameterDetectionSkill.PATTERNS)
      or retired.
SOURCE: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_011]
```

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § [g_011] — UNRESOLVED

---

#### `test_preprocess_method` — _preprocess_paper Integration Test

```
TEST: test_preprocess_method
RULE: _preprocess_paper(text) must return a dict
MOCK_SETUP: None
TRIGGER: auditor._preprocess_paper("This is a test paper with github.com/test/repo")
POSITIVE CASE:
  INPUT: text = "This is a test paper with github.com/test/repo"
  EXPECTED:
    - isinstance(red_flags, dict) == True   (return type assertion)
    - Side effect: prints count of truthy values in red_flags dict.
NEGATIVE CASE (DEPLOYMENT READINESS SIGNAL — EXPECTED TO FAIL):
  INPUT: Current codebase post-refactoring.
  EXPECTED:
    - AttributeError raised: `PaperAuditor` in the current source has only two methods
      (`__init__` and `audit`). The method `_preprocess_paper` was removed during refactoring.
    - The except block catches it → prints "❌ Error en _preprocess_paper: {e}" → returns False.
    - Expected output: [GAP: method removed in refactoring — expected output undefined]
NOTE: The current `audit` method initialises `context = {'paper_text': paper_text, 'red_flags': {}}`
      with an empty red_flags dict (auditor.py:78), suggesting _preprocess_paper was replaced by
      an empty placeholder. Recovery of the original contract requires pre-refactor commit history.
SOURCE: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_009]
```

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § [g_009] — UNRESOLVED (partial)

---

#### `test_prompts_module` — Prompt Function Smoke Test

```
TEST: test_prompts_module
RULE: get_extraction_prompt and get_evaluation_prompt must return non-empty strings
MOCK_SETUP: None
TRIGGER:
  - extraction_prompt = get_extraction_prompt("Test paper", {"test": True})
  - evaluation_prompt = get_evaluation_prompt({"test": "info"}, {"test": True})
POSITIVE CASE:
  INPUT:
    - test_text = "Test paper"
    - test_flags = {"test": True}
    - test_info = {"test": "info"}
  EXPECTED:
    - len(extraction_prompt) > 0   (non-empty string)
    - len(evaluation_prompt) > 0   (non-empty string)
    - Returns True.
NEGATIVE CASE:
  INPUT: get_extraction_prompt or get_evaluation_prompt raises an exception (e.g., import error,
         template formatting error).
  EXPECTED: except block catches it → prints "❌ Error en módulo prompts: {e}" → returns False.
SOURCE: extracted_root_tests_scratch_01.md § 11.1
```

> Source: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_010]

---

### `main()` Runner — Deployment Readiness Summary

```
FUNCTION: main()
BEHAVIOUR:
  - Runs tests in order: [test_auditor_initialization, test_regex_patterns,
                          test_preprocess_method, test_prompts_module]
  - Collects (name, bool_result) per test.
  - Prints: "✅ PASS" or "❌ FAIL" per test.
  - Prints summary: "{passed}/{total}"
  - If passed == total: "Refactorización completada exitosamente!"
  - Else: "Algunos tests fallaron."
EXPECTED OUTCOME (current codebase):
  - test_auditor_initialization: PASS (if GOOGLE_API_KEY set) / FAIL (if key absent)
  - test_regex_patterns: FAIL (REGEX_PATTERNS removed from auditor.py post-refactoring)
  - test_preprocess_method: FAIL (_preprocess_paper method removed post-refactoring)
  - test_prompts_module: PASS (get_extraction_prompt and get_evaluation_prompt still exist)
SOURCE: extracted_root_tests_scratch_01.md § 11.1
```

> Source: extracted_root_tests_scratch_01.md § 11.1

---

## Import Smoke Tests

### `test_imports.py` — Overview

**Type:** Sequential import checks (no pytest or unittest; script-level).  
**Structure:** 7 `try/except Exception` blocks, each testing one import.  
**Outcome:** Prints `"OK <module>"` on success or `"ERROR <module>: {e}"` on failure.  
**Final line:** `"Todas las importaciones funcionan correctamente!"` (printed after all blocks).

> Source: extracted_root_tests_scratch_01.md § 11.2

---

### Module Import Scenarios

| Block | Module / Import Target | Import Statement | Expected (Pass) | Expected (Fail) |
|-------|------------------------|-----------------|-----------------|-----------------|
| 1 | `frontend.config` | `from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION` | `"OK frontend.config"` | `"ERROR frontend.config: {e}"` |
| 2 | `frontend.styles.custom_css` | `from frontend.styles.custom_css import apply_custom_styles` | `"OK frontend.styles.custom_css"` | `"ERROR frontend.styles.custom_css: {e}"` |
| 3 | `frontend.utils.session_state` | `from frontend.utils.session_state import initialize_session_state` | `"OK frontend.utils.session_state"` | `"ERROR frontend.utils.session_state: {e}"` |
| 4 | `frontend.components.file_uploader` | `from frontend.components.file_uploader import process_uploaded_file` | `"OK frontend.components.file_uploader"` | `"ERROR frontend.components.file_uploader: {e}"` |
| 5 | `frontend.components.audit_results` | `from frontend.components.audit_results import render_audit_results, generate_report` | `"OK frontend.components.audit_results"` | `"ERROR frontend.components.audit_results: {e}"` |
| 6 | `frontend.components.sota_section` | `from frontend.components.sota_section import render_sota_analysis` | `"OK frontend.components.sota_section"` | `"ERROR frontend.components.sota_section: {e}"` |
| 7 | `frontend.components.chatbot` | `from frontend.components.chatbot import render_chatbot` | `"OK frontend.components.chatbot"` | `"ERROR frontend.components.chatbot: {e}"` |

> Source: extracted_root_tests_scratch_01.md § 11.2 (test_imports.py:4-44)

---

#### Scenario Blocks — Detailed

```
TEST: Block 1 — frontend.config
TRIGGER: from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION
POSITIVE CASE:
  EXPECTED: print("OK frontend.config"); ImportError absent
  VERIFIED SYMBOLS: TITLE (str), SIDEBAR_IMAGE (str URL), SIDEBAR_DESCRIPTION (str)
NEGATIVE CASE:
  INPUT: Module not installed or path misconfigured.
  EXPECTED: ImportError caught → print("ERROR frontend.config: {e}")
SOURCE: test_imports.py:4-8; cross_ref_resolution_cross_ref_root_to_frontend.md § g_008
```

```
TEST: Block 2 — frontend.styles.custom_css
TRIGGER: from frontend.styles.custom_css import apply_custom_styles
POSITIVE CASE:
  EXPECTED: print("OK frontend.styles.custom_css"); ImportError absent
NEGATIVE CASE:
  INPUT: Module not found / dependency on streamlit unavailable.
  EXPECTED: ImportError caught → print("ERROR frontend.styles.custom_css: {e}")
SOURCE: test_imports.py:10-14; cross_ref_resolution_cross_ref_root_to_frontend.md § g_026
```

```
TEST: Block 3 — frontend.utils.session_state
TRIGGER: from frontend.utils.session_state import initialize_session_state
POSITIVE CASE:
  EXPECTED: print("OK frontend.utils.session_state"); ImportError absent
NEGATIVE CASE:
  INPUT: Module or its transitive dependencies (PaperAuditor, PaperChatbot, SotaAnalyzer) not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.utils.session_state: {e}")
SOURCE: test_imports.py:16-20; cross_ref_resolution_cross_ref_root_to_frontend.md § g_027
```

```
TEST: Block 4 — frontend.components.file_uploader
TRIGGER: from frontend.components.file_uploader import process_uploaded_file
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.file_uploader"); ImportError absent
NEGATIVE CASE:
  INPUT: hashlib, os, or streamlit not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.components.file_uploader: {e}")
SOURCE: test_imports.py:22-26; cross_ref_resolution_cross_ref_root_to_frontend.md § g_004
```

```
TEST: Block 5 — frontend.components.audit_results
TRIGGER: from frontend.components.audit_results import render_audit_results, generate_report
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.audit_results"); ImportError absent
NEGATIVE CASE:
  INPUT: scoring.py or Streamlit not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.components.audit_results: {e}")
SOURCE: test_imports.py:28-32; cross_ref_resolution_cross_ref_root_to_frontend.md § g_005, g_006
```

```
TEST: Block 6 — frontend.components.sota_section
TRIGGER: from frontend.components.sota_section import render_sota_analysis
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.sota_section"); ImportError absent
NEGATIVE CASE:
  INPUT: Module not found / SotaAnalyzer dependency missing.
  EXPECTED: ImportError caught → print("ERROR frontend.components.sota_section: {e}")
SOURCE: test_imports.py:34-38; cross_ref_resolution_cross_ref_root_to_frontend.md § g_007
```

```
TEST: Block 7 — frontend.components.chatbot
TRIGGER: from frontend.components.chatbot import render_chatbot
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.chatbot"); ImportError absent
NEGATIVE CASE:
  INPUT: Module not found / Streamlit not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.components.chatbot: {e}")
SOURCE: test_imports.py:40-44; cross_ref_resolution_cross_ref_root_to_frontend.md § g_007
```

> Source: extracted_root_tests_scratch_01.md § 11.2

---

## Skills Architecture Integration Tests

### `test_skills_integration.py` — Overview

**Type:** Script (10 numbered tests with `sys.exit(1)` on any failure).  
**Exit behavior:** Any `AssertionError` or uncaught `Exception` triggers `sys.exit(1)`.  
**All 10 tests run sequentially; failure on any one halts the process.**

> Source: extracted_root_tests_scratch_01.md § 11.3

---

#### Test 1 — Module Imports (All 15 Skill Classes)

```
TEST: Test 1 — skill module imports
MOCK_SETUP: None
TRIGGER:
  from backend.skills import (
      BaseSkill, InformationExtractionSkill, ReproducibilityEvaluationSkill,
      MetricsCalculationSkill, MetadataAggregationSkill, ConversationalResponseSkill,
      ContextValidationSkill, ThematicCoverageSkill, QueryGenerationSkill,
      SemanticScholarSearchSkill, CoverageGapAnalysisSkill, CrossValidationSkill
  )
  from backend.skills.regex_detection_skills import (
      LimitationsQualityDetectionSkill, SoftwareVersionDetectionSkill, HardwareDetailDetectionSkill
  )
POSITIVE CASE:
  INPUT: All modules installed and importable.
  EXPECTED: No ImportError or Exception raised.
NEGATIVE CASE:
  INPUT: Any one of the 15 symbols missing from backend.skills or regex_detection_skills.
  EXPECTED: Exception caught → print("   [ERROR] Error en importaciones: {e}") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 1); test_skills_integration.py:9-35
```

> **Note:** `__init__.py` exports exactly 15 symbols; `ChecklistVerificationSkill` and `HybridHyperparameterExtractionSkill` are NOT exported from `__init__.py`.  
> Source: extracted_backend_skills_01.md § 1.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_016]

---

#### Test 2 — Service Imports

```
TEST: Test 2 — service imports
MOCK_SETUP: None
TRIGGER:
  from backend.services.auditor import PaperAuditor
  from backend.services.chatbot import Chatbot
  from backend.services.sota_analyzer import SotaAnalyzer
POSITIVE CASE:
  INPUT: All service modules importable.
  EXPECTED: No Exception raised.
NEGATIVE CASE:
  INPUT: Any service module missing or has import-time errors.
  EXPECTED: print("   [ERROR] Error importando servicios: {e}") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 2); test_skills_integration.py:38-46
```

---

#### Test 3 — Service Initialization

```
TEST: Test 3 — service initialization
MOCK_SETUP: None (real initialization; requires GOOGLE_API_KEY in environment)
TRIGGER:
  auditor = PaperAuditor()
  chatbot = Chatbot()
  sota = SotaAnalyzer()
POSITIVE CASE:
  INPUT: GOOGLE_API_KEY set; all dependencies available.
  EXPECTED: All three instances created without exception.
NEGATIVE CASE:
  INPUT: GOOGLE_API_KEY absent or LLMClient raises ValueError.
  EXPECTED:
    - print("   [ERROR] Error inicializando servicios: {e}")
    - traceback.print_exc()
    - sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 3); test_skills_integration.py:49-63
```

---

#### Test 4 — PaperAuditor Skill Attributes (6 Required)

```
TEST: Test 4 — PaperAuditor skill attributes
RULE: RULE-10 — PaperAuditor must expose exactly 6 skill attributes
MOCK_SETUP: auditor = PaperAuditor() (from Test 3)
TRIGGER: hasattr(auditor, attr) for each of 6 attribute names
REQUIRED ATTRIBUTES (6 total):
  'extraction_skill', 'hybrid_hp_skill', 'evaluation_skill',
  'verification_skill', 'metrics_skill', 'metadata_skill'
POSITIVE CASE:
  INPUT: PaperAuditor properly constructed.
  EXPECTED: All 6 hasattr checks return True.
NEGATIVE CASE:
  INPUT: Any one attribute is missing from the PaperAuditor instance.
  EXPECTED:
    - AssertionError with message "Falta <attr>"
    - print("   [ERROR] Falta <attr>")
    - sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 4); RULE-10; test_skills_integration.py:66-77
```

> **Rule Reference:** RULE-10  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-10)

---

#### Test 5 — Chatbot Skill Attributes (2 Required)

```
TEST: Test 5 — Chatbot skill attributes
RULE: RULE-11 — Chatbot must expose exactly 2 skill attributes
MOCK_SETUP: chatbot = Chatbot() (from Test 3)
TRIGGER: hasattr(chatbot, 'response_skill') AND hasattr(chatbot, 'validation_skill')
REQUIRED ATTRIBUTES (2 total): 'response_skill', 'validation_skill'
POSITIVE CASE:
  INPUT: Chatbot properly constructed.
  EXPECTED: Both hasattr checks return True.
NEGATIVE CASE:
  INPUT: Either attribute missing.
  EXPECTED: AssertionError "Falta <attr>" → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 5); RULE-11; test_skills_integration.py:80-87
```

> **Rule Reference:** RULE-11  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-11)

---

#### Test 6 — SotaAnalyzer Skill Attributes (5 Required)

```
TEST: Test 6 — SotaAnalyzer skill attributes
RULE: RULE-12 — SotaAnalyzer must expose exactly 5 skill attributes
MOCK_SETUP: sota = SotaAnalyzer() (from Test 3)
TRIGGER: hasattr(sota, attr) for each of 5 attribute names
REQUIRED ATTRIBUTES (5 total): 'thematic_skill', 'query_skill', 'search_skill', 'gap_skill', 'validation_skill'
POSITIVE CASE:
  INPUT: SotaAnalyzer properly constructed.
  EXPECTED: All 5 hasattr checks return True.
NEGATIVE CASE:
  INPUT: Any one attribute missing.
  EXPECTED: AssertionError "Falta <attr>" → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 6); RULE-12; test_skills_integration.py:90-100
```

> **Rule Reference:** RULE-12  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-12)

---

#### Test 7 — BaseSkill Inheritance

```
TEST: Test 7 — BaseSkill inheritance
MOCK_SETUP: auditor, chatbot, sota from Test 3
TRIGGER:
  isinstance(auditor.extraction_skill, BaseSkill)
  isinstance(chatbot.response_skill, BaseSkill)
  isinstance(sota.thematic_skill, BaseSkill)
POSITIVE CASE:
  INPUT: All three skills are instances of BaseSkill (or a BaseSkill subclass).
  EXPECTED: All 3 isinstance checks return True.
NEGATIVE CASE:
  INPUT: Any skill is not a BaseSkill subclass.
  EXPECTED: print("   [ERROR] Error en herencia de BaseSkill") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 7); test_skills_integration.py:103-111
```

---

#### Test 8 — BaseSkill Required Methods

```
TEST: Test 8 — BaseSkill required methods
MOCK_SETUP: skill = auditor.extraction_skill (InformationExtractionSkill instance)
TRIGGER:
  hasattr(skill, 'execute')
  hasattr(skill, 'validate_context')
  hasattr(skill, 'log_execution')
  callable(skill.execute)
REQUIRED METHOD PRESENCE AND CALLABILITY:
  - 'execute': present and callable
  - 'validate_context': present
  - 'log_execution': present
POSITIVE CASE:
  INPUT: extraction_skill is a properly constructed BaseSkill subclass.
  EXPECTED: All 4 checks pass; no AssertionError raised.
NEGATIVE CASE:
  INPUT: Any method absent or execute not callable.
  EXPECTED:
    AssertionError messages (per check):
      "Falta método execute"
      "Falta método validate_context"
      "Falta método log_execution"
      "execute no es callable"
    → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 8); test_skills_integration.py:114-124
```

---

#### Test 9 — SemanticScholarSearchSkill Execution with Empty Queries

```
TEST: Test 9 — SemanticScholarSearchSkill execution
RULE: RULE-13 — SemanticScholarSearchSkill with empty search_queries returns dict with 'sota_papers' key
MOCK_SETUP:
  from backend.skills.sota_skills import SemanticScholarSearchSkill
  search_skill = SemanticScholarSearchSkill()   (no llm_client argument)
TRIGGER: result = search_skill.execute({'search_queries': []})
POSITIVE CASE:
  INPUT: context = {'search_queries': []}   (empty queries list)
  EXPECTED: 'sota_papers' in result   (key present in returned dict)
NEGATIVE CASE:
  INPUT: execute raises any exception (network error, missing dependency, etc.).
  EXPECTED:
    - print("   [ERROR] Error ejecutando skill: {e}")
    - traceback.print_exc()
    - sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 9); RULE-13; test_skills_integration.py:127-141
```

> **Rule Reference:** RULE-13  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-13); cross_ref_resolution_cross_ref_root_to_backend.md § [g_018]

---

#### Test 10 — Logging Smoke Test

```
TEST: Test 10 — logging infrastructure
MOCK_SETUP:
  from backend.utils.logger import get_logger
  logger = get_logger("test_skill")
TRIGGER: logger.info("Test de logging")
POSITIVE CASE:
  INPUT: get_logger returns a logger with a working .info() method.
  EXPECTED: No exception raised.
NEGATIVE CASE:
  INPUT: get_logger raises or logger.info raises.
  EXPECTED: print("   [ERROR] Error en logging: {e}") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 10); test_skills_integration.py:144-151
```

---

## Checklist Health Scoring Tests (get_checklist_health)

### `scratch/test_checklist_health.py` — Overview

**Type:** Scratch assertion script.  
**Module under test:** `frontend.utils.scoring.get_checklist_health`  
**Priority:** HIGH (this function gates the checklist risk display in the UI).

> Source: extracted_root_tests_scratch_01.md § 11.9

---

### `get_checklist_health` — Function Specification

```
FUNCTION: get_checklist_health
SIGNATURE: get_checklist_health(evaluation: dict) -> dict
SOURCE: scoring.py:37
PARAMETERS:
  - evaluation: dict — keyed by the 16 CHECKLIST_KEYS.
    Expected structure per key:
      {
        "answer":          str,          # "Yes" / "No" / "N/A" / "" (case-insensitive comparison)
        "justification":   str,
        "evidence":        str,
        "is_no_justified": bool or str   # True/False or "true"/"false"
      }
RETURN: dict with keys:
  - "status":        str  — "valid" if pending_count == 0, else "risk"   SOURCE: scoring.py:122-123
  - "pending_count": int  — count of risk-triggering items              SOURCE: scoring.py:122-126
  - "total":         int  — len(items); always 16 when evaluation non-empty; 0 on early exit  SOURCE: scoring.py:127
  - "items":         list — 16 item dicts (one per CHECKLIST_KEYS key), each containing:
      "key":                  str  — the CHECKLIST_KEYS key string
      "label":                str  — from CHECKLIST_LABELS.get(key, key)
      "answer":               str  — stripped answer if non-empty, else "—"
      "evidence":             str  — evidence if present, else justification if present, else "—"
      "justification":        str  — stripped justification string
      "is_no_justified":      bool — normalised from raw ("true"/"false" or bool)
      "pending_justification":bool — True when "no" in answer AND (not is_no_justified OR not justification)
      "missing_evidence":     bool — True when "yes" in answer AND (not evidence AND not justification)
      "alert_msg":            str  — risk description; "" if no risk;
                                     special suffix for "crowdsourcing_human_subjects":
                                     "⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."
                                     SOURCE: scoring.py:110-120
EARLY_EXIT_GUARD:
  When evaluation is falsy (None, {}, etc.):
    returns {"status": "risk", "items": [], "pending_count": 0, "total": 0}
  SOURCE: scoring.py:56-62
```

> Source: cross_ref_resolution_cross_ref_root_to_frontend.md § g_013; extracted_frontend_01.md § 7.1

---

### 16 Checklist Items (CHECKLIST_KEYS and CHECKLIST_LABELS)

| # | Key | Label |
|---|-----|-------|
| 1 | `claims` | "1. Claims" |
| 2 | `limitations` | "2. Limitations" |
| 3 | `theory_assumptions_proofs` | "3. Theory, Assumptions & Proofs" |
| 4 | `experimental_result_reproducibility` | "4. Experimental Result Reproducibility" |
| 5 | `open_access_data_code` | "5. Open Access to Data and Code" |
| 6 | `experimental_setting_details` | "6. Experimental Setting / Details" |
| 7 | `experiment_statistical_significance` | "7. Experiment Statistical Significance" |
| 8 | `experiments_compute_resource` | "8. Experiments Compute Resource" |
| 9 | `code_of_ethics` | "9. Code of Ethics" |
| 10 | `broader_impacts` | "10. Broader Impacts" |
| 11 | `safeguards` | "11. Safeguards" |
| 12 | `licenses` | "12. Licenses" |
| 13 | `assets` | "13. Assets" |
| 14 | `crowdsourcing_human_subjects` | "14. Crowdsourcing & Human Subjects" |
| 15 | `irb_approvals` | "15. IRB Approvals" |
| 16 | `declaration_llm_usage` | "16. Declaration of LLM Usage" |

> Source: extracted_frontend_01.md § 2.3; scoring.py:8-34

---

### Mock Evaluation Dictionary (16 Items)

The `mock_eval` used by `scratch/test_checklist_health.py` includes one entry per CHECKLIST_KEYS key. The key that triggers the main assertion is:

| Key | answer | evidence | justification | is_no_justified |
|-----|--------|----------|---------------|-----------------|
| `experiment_statistical_significance` | `'No'` | `''` | `''` | `False` |

All other keys in mock_eval have their own answer/evidence/justification values — the full list of 16 keys is: `['claims', 'limitations', 'theory_assumptions_proofs', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiment_statistical_significance', 'experiments_compute_resource', 'code_of_ethics', 'broader_impacts', 'safeguards', 'licenses', 'assets', 'crowdsourcing_human_subjects', 'irb_approvals', 'declaration_llm_usage']`.

> Source: extracted_root_tests_scratch_01.md § 8 (mock_eval key list), § 11.9

---

#### Scenario 1 — 'No' Without Justification Triggers 'risk' Status

```
TEST: get_checklist_health — pending_justification and risk status
RULE: RULE-07 — health['status'] == 'risk' when any item has answer='No' AND is_no_justified=False
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(mock_eval)
POSITIVE CASE (risk correctly detected):
  INPUT: mock_eval['experiment_statistical_significance'] =
           {'answer': 'No', 'evidence': '', 'justification': '', 'is_no_justified': False}
  EXPECTED:
    - stats_item = next(i for i in health['items'] if i['key'] == 'experiment_statistical_significance')
    - stats_item['pending_justification'] == True
        (assert message: "Item 7 should be flagged!")
    - health['status'] == 'risk'
        (assert message: "Should be risk with unjustified No!")
NEGATIVE CASE:
  INPUT: evaluation is falsy (None, {}, etc.).
  EXPECTED (EARLY_EXIT_GUARD):
    - {"status": "risk", "items": [], "pending_count": 0, "total": 0} returned immediately.
SOURCE: extracted_root_tests_scratch_01.md § 11.9; RULE-07; scratch/test_checklist_health.py:33-35
```

> **Rule Reference:** RULE-07  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-07)

---

#### Scenario 2 — All 'Yes' Answers (Valid Status)

```
TEST: get_checklist_health — all Yes answers
RULE: status == 'valid' when pending_count == 0
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(all_yes_eval)
POSITIVE CASE:
  INPUT: All 16 items have answer='Yes' with non-empty evidence.
  EXPECTED:
    - health['status'] == 'valid'
    - health['pending_count'] == 0
    - health['total'] == 16
    - All items have missing_evidence == False and pending_justification == False
NEGATIVE CASE: [GAP: scoring formula not extracted for partial Yes/missing-evidence edge cases]
SOURCE: scoring.py:122-127 (inferred from RETURN spec); cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

#### Scenario 3 — All 'No' Answers (Full Risk)

```
TEST: get_checklist_health — all No answers without justification
RULE: pending_count == 16 when all No items are unjustified
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(all_no_eval)
POSITIVE CASE:
  INPUT: All 16 items have answer='No', justification='', is_no_justified=False.
  EXPECTED:
    - health['status'] == 'risk'
    - health['pending_count'] == 16
    - All items have pending_justification == True
NEGATIVE CASE: [GAP: scoring formula not extracted — exact pending_count calculation
               when some items are 'No' with is_no_justified=True is not tested in extraction]
SOURCE: scoring.py:122-127 (inferred)
```

---

#### Scenario 4 — pending_justification Edge Case

```
TEST: get_checklist_health — pending_justification edge case
RULE: pending_justification == True when "no" in answer AND (not is_no_justified OR not justification)
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(pending_eval)
POSITIVE CASE:
  INPUT: Item with answer='No', is_no_justified=True but justification='' (empty string).
  EXPECTED:
    - pending_justification == True (because not justification is True when justification='')
  INPUT: Item with answer='No', is_no_justified=False but justification='Some text'.
  EXPECTED:
    - pending_justification == True (because not is_no_justified is True)
NEGATIVE CASE:
  INPUT: Item with answer='No', is_no_justified=True, justification='Justified reason'.
  EXPECTED:
    - pending_justification == False
SOURCE: scoring.py:110-120 (item dict definition); cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

#### Scenario 5 — missing_evidence Edge Case

```
TEST: get_checklist_health — missing_evidence edge case
RULE: missing_evidence == True when "yes" in answer AND (not evidence AND not justification)
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(missing_ev_eval)
POSITIVE CASE:
  INPUT: Item with answer='Yes', evidence='', justification=''.
  EXPECTED: missing_evidence == True
NEGATIVE CASE:
  INPUT: Item with answer='Yes', evidence='', justification='Some justification text'.
  EXPECTED: missing_evidence == False (justification counts as substitute evidence)
SOURCE: scoring.py:110-120; cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

#### Scenario 6 — crowdsourcing_human_subjects Special Alert Suffix

```
TEST: get_checklist_health — crowdsourcing ethics suffix
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(crowd_eval)
POSITIVE CASE:
  INPUT: Item 'crowdsourcing_human_subjects' with a risk condition (pending_justification or
         missing_evidence).
  EXPECTED:
    - alert_msg contains "⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."
      appended as special suffix.
NEGATIVE CASE:
  [GAP: exact conditions that trigger the suffix beyond a generic risk condition not fully
        extracted — the special suffix is appended to items triggering risk for key
        'crowdsourcing_human_subjects' specifically; full logic not extracted]
SOURCE: scoring.py:110-120; cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

## Scratch / Exploratory Test Cases

### `scratch/test_rag_split.py` — Naive Chunking (Already Covered in Section 3)

The naive chunking approach, input preconditions, and function definition are documented in full in the **RAG Logical Block Splitting Tests** section above.

Additional notes:

- **Test precondition:** No external file dependency. The `test_text` fixture is a hardcoded multi-line string defined at `scratch/test_rag_split.py:28-43`.
- **No assertions:** This is an observation-only script that prints chunk count and chunk content. It cannot fail unless Python itself crashes.

> Source: extracted_root_tests_scratch_01.md § 11.11

---

### `backend/scratch/test_embed.py` — Google GenAI Embed API Response Structure

**Type:** Scratch script. No assertions. No error handling.  
**Purpose:** Verifies the response structure of `client.models.embed_content` with a 3-element input.

> Source: extracted_root_tests_scratch_01.md § 11.4

```
TEST: test_embed (scratch/exploratory)
MOCK_SETUP: None (real Google GenAI API call)
PRECONDITION: GOOGLE_API_KEY set in .env
TRIGGER:
  client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
  contents = ["hello", "world", "test"]
  res = client.models.embed_content(model="gemini-embedding-2", contents=contents)
OBSERVATION ONLY (no assertions):
  - Prints type(res)
  - If hasattr(res, 'embeddings'):
      Prints type(res.embeddings)
      If isinstance(res.embeddings, list):
          Prints len(res.embeddings)        — expected: 3 (one per input string)
          Prints type(res.embeddings[0])
          Prints type(res.embeddings[0].values)
          Prints len(res.embeddings[0].values)   — embedding vector dimension
      Else: Prints "Embeddings is not a list. It is {type(res.embeddings)}"
  - Else: Prints "No embeddings attribute"
POSITIVE CASE:
  INPUT: Valid API call with 3 text strings.
  EXPECTED (from API contract):
    - res.embeddings is a list of 3 embedding objects
    - res.embeddings[0].values is a list of numeric values (vector)
    - [GAP: API response schema not extracted — cannot define assertions on exact
             embedding dimension or numeric value ranges]
NEGATIVE CASE:
  INPUT: Invalid GOOGLE_API_KEY or API unavailable.
  EXPECTED:
    - No error handling in this script. Exception propagates uncaught to interpreter.
    - [GAP: API response schema not extracted — cannot define assertions]
SOURCE: extracted_root_tests_scratch_01.md § 11.4; § 7.5
```

> Source: extracted_root_tests_scratch_01.md § 7.5, § 11.4

---

### `backend/scratch/test_embed2.py` — Embed API with Error Handling

**Type:** Scratch script. No assertions. Has `try/except` wrapper.

> Source: extracted_root_tests_scratch_01.md § 11.5

```
TEST: test_embed2 (scratch/exploratory)
MOCK_SETUP: None (real API call)
PRECONDITION: GOOGLE_API_KEY set in .env
TRIGGER:
  Block 1:
    try:
        res = client.models.embed_content(model="gemini-embedding-2", contents=["hello","world","test"])
        print embed length or "no attribute"
    except Exception as e:
        print("embed_content error:", e)
  Block 2:
    try: pass
    except Exception: pass   (empty placeholder block)
POSITIVE CASE:
  INPUT: Valid API call.
  EXPECTED (observation only):
    - [GAP: API response schema not extracted — cannot define assertions]
NEGATIVE CASE:
  INPUT: API call fails.
  EXPECTED: print("embed_content error:", e)   (no re-raise; script continues)
SOURCE: extracted_root_tests_scratch_01.md § 11.5
```

---

### `scratch/repro_hyperparams.py` — Hyperparameter Detection Reproduction

**Type:** Scratch script. No assertions. Function `test_hyperparameter_detection()` called at `__main__`.

> TEST PRECONDITION: File `paper_cientifico_3_CON_ERRORES.md` must exist in the current working directory (UTF-8 encoded). This is a **test precondition**, not a deployment constraint. The script silently skips if the file is missing (prints `"File … not found"` and returns).

> **Note:** `*.md` files are in `.gitignore` (`.gitignore:34`). The test file is not version-controlled and must be provided externally before running this script.

```
TEST: test_hyperparameter_detection (scratch/exploratory)
MOCK_SETUP:
  skill = HyperparameterDetectionSkill()
  skill.log_execution = lambda msg, level="info": print(f"[{level.upper()}] {msg}")
  (log_execution overridden to print inline — avoids logging infrastructure dependency)
PRECONDITION: os.path.exists("paper_cientifico_3_CON_ERRORES.md") == True
TRIGGER: results = skill.execute({"paper_text": text})
POSITIVE CASE:
  INPUT: Contents of paper_cientifico_3_CON_ERRORES.md (UTF-8) with hyperparameter-bearing text.
  EXPECTED (observation only):
    - json.dumps(results, indent=2) prints successfully
    - [GAP: response schema not extracted — cannot define assertions on results structure]
NEGATIVE CASE:
  INPUT: File missing from CWD.
  EXPECTED: print("File ... not found") → function returns; no exception.
SOURCE: extracted_root_tests_scratch_01.md § 11.8
```

---

### `scratch/patch_skills.py` — One-Time Maintenance Script

> DEPLOYMENT CONSTRAINT: This is not a test scenario. `patch_skills.py` is a one-time maintenance script that performs an AST-validated in-place rewrite of `backend/skills/regex_detection_skills.py`. It is classified here as a deployment constraint per the prescribed format.

> **DEPLOYMENT CONSTRAINT:**
> `patch_skills.py` requires the following **three class markers** to exist in `backend/skills/regex_detection_skills.py` **in exact order**:
> 1. `'class CrowdsourcingDetectionSkill(BaseSkill):'`
> 2. `'class LicenseDetectionSkill(BaseSkill):'`
> 3. `'class LimitationsQualityDetectionSkill(BaseSkill):'`
>
> If any marker is absent or out of order, the script raises `ValueError` (or `str.index()` raises `ValueError` for the missing substring). The patch is non-idempotent: running it twice will corrupt the file because the original class boundaries will have been replaced. The script calls `ast.parse(new_content)` after writing as a post-write syntax validator.
>
> Source: extracted_root_tests_scratch_01.md § 11.7; extracted_root_tests_scratch_01.md § 8 (patch class boundary markers)

---

### `scratch/check_st.py` — Streamlit API Surface Check

**Type:** Scratch script (6 lines). No assertions.  
**Purpose:** Checks whether `st.html` and `st.iframe` exist as Streamlit attributes.

```
TEST: check_st (scratch/exploratory)
MOCK_SETUP: None
TRIGGER:
  import streamlit as st
  print(f"st.html exists: {hasattr(st, 'html')}")
  print(f"st.iframe exists: {hasattr(st, 'iframe')}")
POSITIVE CASE:
  EXPECTED (observation only): Both hasattr checks complete and print without exception.
NEGATIVE CASE:
  INPUT: Streamlit not installed / import fails.
  EXPECTED: Exception caught → print("Error: {e}")
SOURCE: extracted_root_tests_scratch_01.md § 11.6
```

---

*End of 05_test_scenarios.md*


### 06_glossary.md (42669 chars)
# 06 — Domain Glossary

Specification for the NeurIPS 2026 Reproducibility Audit Application.
Generated from: `extracted_backend_core_01.md`, `extracted_backend_skills_01.md`,
`extracted_frontend_01.md`, `extracted_root_tests_scratch_01.md`,
`cross_ref_resolution_cross_ref_root_to_backend.md`,
`cross_ref_resolution_cross_ref_root_to_frontend.md`.

---

## 1. Domain Concepts

### 1.1 NeurIPS 2026 Reproducibility Checklist

**Definition:** A structured set of 16 transparency and reproducibility criteria that NeurIPS 2026 requires submitted papers to satisfy. The checklist covers claims, limitations, theoretical proofs, experimental reproducibility, open access to data and code, statistical significance reporting, compute resource disclosure, ethical conduct, broader societal impact, safeguards, asset licensing, crowdsourcing practices, IRB approvals, and LLM usage declarations.

**Purpose:** The application automates auditing of submitted papers against all 16 items. For each item, the LLM evaluates the paper text and returns an answer (`"Yes"`, `"No"`, or `"N/A"`) with evidence or justification. Items with missing evidence or unjustified negative answers are flagged as risks that may lead to Desk Reject.

**Programmatic representation:** The 16 items are encoded as Python lists `CHECKLIST_KEYS` (machine-readable key strings) and `CHECKLIST_LABELS` (human-readable display strings), both defined in `frontend/utils/scoring.py`. At evaluation time, the LLM returns a dict keyed by these 16 keys.

(Source: `extracted_frontend_01.md`, §2.3 — scoring.py:8–34; `extracted_backend_core_01.md`, §2.2 — prompts.py:378)

---

### 1.2 paper_type — Valid vs. Invalid Classification Logic

**Definition:** `paper_type` is a string field returned by the LLM during the extraction phase (FASE 1). It classifies whether the submitted paper belongs to the ML/AI domain that the checklist targets.

**Valid/invalid determination:**
- **Invalid:** `extracted_info.get('paper_type', '').startswith('INVALID')` evaluates to `True`.
  - Known invalid value: `"INVALID - Not ML/AI"` — returned when the paper does not involve ML/AI training, research, or experimentation.
  - When invalid, the LLM short-circuits and returns only `{"paper_type": "INVALID - Not ML/AI", "invalid_reason": "<explanation>"}`. No further checklist evaluation is performed.
  - The audit pipeline sets `result['invalid_paper'] = True` and propagates this flag to the frontend result dict.
- **Valid:** Any `paper_type` string that does NOT start with `"INVALID"`. The audit continues through all remaining phases.

**Source of value:** The extraction prompt (`get_extraction_prompt`) instructs the LLM to classify the paper. The guard is inlined at the top of the prompt text. (Source: `extracted_backend_core_01.md`, §2.2 — prompts.py:4; `cross_ref_resolution_cross_ref_root_to_backend.md`, §RESOLUTION SUMMARY [g_010])

---

### 1.3 red_flags — Structure, Keys, and Meaning

**Definition:** `red_flags` is a Python `dict` that accumulates signals detected by the regex-based detection skills before the LLM extraction prompt is assembled. It is initialised as `{}` in `PaperAuditor.audit()` and populated by each detection skill that runs.

**Structure:** Keys are string identifiers. Key naming conventions determine which keys are included in the LLM prompt:
- Keys starting with `'_'` are **internal/private** — filtered OUT of the `flags_section` block injected into the extraction prompt. Example: `_hp_snippets` (a dict of hyperparameter text snippets used to build the RAG query context).
- Keys NOT starting with `'_'` are **rendered** as inline context inside the `flags_section` block in the extraction prompt body.
- Keys prefixed with `tiene_`, `menciona_`, `cantidad_`, `puntos_` are boolean or numeric flags capturing detection results (e.g., `tiene_repositorio`, `menciona_datos_propietarios`). These are NOT counted as "critical" risk indicators by the checklist scoring logic.

**Special key `_hp_snippets`:** A dict mapping hyperparameter names to their extracted text snippets. Built by `HyperparameterDetectionSkill` and consumed by `HybridHyperparameterExtractionSkill` (FASE 1.5) to seed the RAG query context. (Source: `extracted_backend_skills_01.md`, §3.x — regex_detection_skills.py; `extracted_backend_core_01.md`, §2.2 — prompts.py:4)

---

### 1.4 Audit Pipeline Phases

The `PaperAuditor.audit(paper_text, status_callback=None)` method executes the following phases in order:

#### FASE 1 — Information Extraction

**Domain meaning:** The paper text is fragmented into up to 4 balanced sections using Docling markdown header boundaries (`\n(?=#+ )`). Each fragment is sent to the LLM independently (MAP phase). The resulting per-fragment extraction dicts are then consolidated into a single DEFINITIVE MASTER JSON (REDUCE phase). The skill responsible is `InformationExtractionSkill`.

**Output context key:** `extracted_info` — a dict containing all extracted fields from the LLM schema (paper_type, code, data, hyperparameters, hardware, statistics, architecture, baseline_comparison, software_versions, limitations_quality, etc.).

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:60–180; `extracted_backend_skills_01.md`, §3.2 — auditor_skills.py:21; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_015)

#### FASE 1.5 — Hybrid Hyperparameter Extraction

**Domain meaning:** A deep, targeted extraction of numerical hyperparameters that is more accurate than the general MAP/REDUCE extraction. Called "hybrid" because it combines three techniques: (1) regex-based detection (`HyperparameterDetectionSkill`) to locate candidate text snippets, (2) RAG (Retrieval-Augmented Generation) using Google embedding API + ChromaDB in-memory vector store to retrieve the most relevant paper chunks per query, and (3) Pydantic schema-constrained LLM MAP/REDUCE on the retrieved chunks to produce a validated structured output. The responsible skill is `HybridHyperparameterExtractionSkill`.

**Output context key:** `extracted_hyperparameters_hybrid` — a Pydantic-validated dict of hyperparameter values.

(Source: `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py:27; `extracted_backend_core_01.md`, §3.2 — auditor.py:~115–140)

#### FASE 2 — Reproducibility Evaluation

**Domain meaning:** The full `extracted_info` dict and `red_flags` are passed to the LLM acting as a "Senior Area Chair for NeurIPS 2026". The LLM evaluates each of the 16 NeurIPS checklist items and returns structured answers with evidence or justification. The responsible skill is `ReproducibilityEvaluationSkill`.

**Output context key:** `evaluation` — a dict keyed by the 16 CHECKLIST_KEYS, each value being `{"answer": str, "evidence": str, "justification": str, "is_no_justified": bool}`.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~145–160; §2.2 — prompts.py:378)

#### FASE 2.5 — Strict Verification (False-Negative Check)

**Domain meaning:** A second LLM pass acting as "Auditor 2". This phase reviews the FASE 2 evaluation results and checks for false negatives (items incorrectly marked "Yes" without real evidence) and false positives (items incorrectly marked "No" that should be "N/A"). The responsible skill is `ChecklistVerificationSkill`.

**Output:** Updates or supplements the `evaluation` dict with corrected answers.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~162–175; `extracted_backend_skills_01.md`, §3.x — auditor_skills.py:319)

#### FASE 3 — Metrics Calculation

**Domain meaning:** Computes aggregate metrics from the evaluated checklist items: reproducibility score, open access score, statistics score, compute resource score, license score, crowdsourcing compliance score. The responsible skill is `MetricsCalculationSkill` (no LLM client required — pure computation).

**Output context key:** `metricas` — a dict of computed float scores.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~178–185)

#### FASE 4 — Metadata Aggregation

**Domain meaning:** The final assembly phase. `MetadataAggregationSkill` merges all context keys produced by previous phases into a single flat result dict that matches the shape expected by the frontend (`st.session_state.resultado`). This includes flattening the `evaluation` dict keys to top-level keys, and renaming `extracted_info` to `informacion_extraida`. No LLM client required — pure data assembly.

**Output:** The final `resultado` dict returned by `PaperAuditor.audit()`.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~187–200)

---

### 1.5 MAP/REDUCE Extraction Strategy

**Definition:** A divide-and-conquer LLM extraction pattern used in both FASE 1 (`InformationExtractionSkill`) and FASE 1.5 (`HybridHyperparameterExtractionSkill`).

- **MAP phase:** The paper text (or RAG-retrieved chunks) is split into up to 4 balanced fragments. Each fragment is processed independently by the LLM using a map-extraction prompt. This parallelises extraction and avoids exceeding the LLM context window for long papers. Between fragment calls, `time.sleep(2)` is used to avoid rate limiting.
- **REDUCE phase:** All MAP results (a list of per-fragment extraction dicts) are sent together to the LLM with a reduce-consolidation prompt. The LLM merges them into a single DEFINITIVE MASTER JSON, resolving conflicts by preferring the most complete information from any fragment.

**Fragment construction algorithm:**
1. Split paper text on Docling markdown header boundaries: `re.split(r'\n(?=#+ )', '\n' + paper_text_norm)`.
2. Accumulate sections into balanced fragments targeting `total_chars / 4` chars per fragment; at most 3 cut points.
3. Fallback for flat documents (no headers detected): `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)`, first 4 chunks.

(Source: `extracted_backend_skills_01.md`, §3.2 — auditor_skills.py:21; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_015)

---

### 1.6 Hybrid Hyperparameter Extraction — What Makes It "Hybrid"

**Definition:** The term "hybrid" refers to the combination of three distinct extraction techniques within `HybridHyperparameterExtractionSkill`:

1. **Regex detection (pre-processing):** `HyperparameterDetectionSkill` runs regex patterns on the full paper text to detect candidate hyperparameter snippets. These snippets are stored in `red_flags['_hp_snippets']`.
2. **RAG retrieval:** The paper text is chunked and embedded using the Google Generative Language API (`gemini-embedding-2`). Chunks are stored in a ChromaDB in-memory vector store (ephemeral — rebuilt on every call, never persisted). 13 fixed query strings are used to retrieve the top 10 chunks per query. Retrieved chunks are deduplicated by minimum cosine distance.
3. **Schema-constrained LLM MAP/REDUCE:** The deduplicated RAG chunks are used as the MAP fragments. The REDUCE phase produces output validated against a Pydantic schema for hyperparameter fields.

This combination produces higher-precision hyperparameter extraction than FASE 1's general extraction, which processes the whole paper uniformly.

(Source: `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py:27)

---

### 1.7 RAG (Retrieval-Augmented Generation) — Scope and Purpose

**Definition in this application:** RAG is used exclusively in FASE 1.5 (`HybridHyperparameterExtractionSkill`). It is NOT used for the general extraction (FASE 1) or the evaluation/verification phases.

**Scope:**
- **Embedding model:** `gemini-embedding-2` via the Google Generative Language API (`batchEmbedContents` endpoint).
- **Vector store:** ChromaDB, in-memory only. A new ChromaDB instance is created on every call to `HybridHyperparameterExtractionSkill.execute()`. No persistence between audit runs.
- **Query strategy:** 13 fixed domain-specific query strings targeting hyperparameter-related content (learning rate, batch size, optimizer, warmup, etc.).
- **Retrieval:** Top 10 chunks per query; deduplicated by minimum cosine distance across all 13 queries.
- **Output:** The retrieved chunks become the MAP fragments for the subsequent LLM MAP/REDUCE extraction.

**Components that use RAG:** `HybridHyperparameterExtractionSkill` (rag_extraction_skill.py).
**Components that do NOT use RAG:** `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `ChecklistVerificationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `PaperChatbot`, `SotaAnalyzer`.

(Source: `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py:27; `extracted_backend_core_01.md`, §2.1 — config.py:35)

---

## 2. NeurIPS 2026 Checklist Items (all 16 with definitions)

All 16 items are defined in `CHECKLIST_KEYS` and `CHECKLIST_LABELS` in `frontend/utils/scoring.py` and are evaluated by the `ReproducibilityEvaluationSkill` in FASE 2. Keys and labels are reproduced exactly as they appear in the extraction.

| # | Key | Label | Definition | Source |
|---|-----|-------|------------|--------|
| 1 | `claims` | `"1. Claims"` | Verifies that the paper's claims are consistent with its experimental results and limitations. The LLM checks whether the paper clearly states what it claims to demonstrate and whether the evidence matches. | `extracted_frontend_01.md`, §2.3 — scoring.py:8; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 2 | `limitations` | `"2. Limitations"` | Verifies that the paper includes an explicit discussion of its limitations. Checks for a dedicated limitations section or clear statements of scope restrictions. | `extracted_frontend_01.md`, §2.3 — scoring.py:10; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 3 | `theory_assumptions_proofs` | `"3. Theory, Assumptions & Proofs"` | Verifies that theoretical results include stated assumptions and, where applicable, proofs or references to proofs. Checks for appendix references and whether assumptions are enumerated. | `extracted_frontend_01.md`, §2.3 — scoring.py:12; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 4 | `experimental_result_reproducibility` | `"4. Experimental Result Reproducibility"` | Verifies that the paper provides enough information to reproduce its experimental results: code, datasets, hyperparameters, and procedural details. | `extracted_frontend_01.md`, §2.3 — scoring.py:14; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 5 | `open_access_data_code` | `"5. Open Access to Data and Code"` | Verifies that the paper provides open access to its datasets and code, or explains why access is restricted (proprietary data, licensing restrictions, etc.). | `extracted_frontend_01.md`, §2.3 — scoring.py:16; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 6 | `experimental_setting_details` | `"6. Experimental Setting / Details"` | Verifies that the experimental setup is described in sufficient detail: hardware, software versions, hyperparameters, training procedure, evaluation metrics. | `extracted_frontend_01.md`, §2.3 — scoring.py:18; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 7 | `experiment_statistical_significance` | `"7. Experiment Statistical Significance"` | Verifies that results are reported with appropriate statistical analysis: confidence intervals, significance tests, number of experimental runs. | `extracted_frontend_01.md`, §2.3 — scoring.py:20; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 8 | `experiments_compute_resource` | `"8. Experiments Compute Resource"` | Verifies that the paper discloses the compute resources used: GPU/CPU type, count, memory, training time, carbon footprint, energy consumption. | `extracted_frontend_01.md`, §2.3 — scoring.py:22; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 9 | `code_of_ethics` | `"9. Code of Ethics"` | Verifies that the paper acknowledges and complies with the NeurIPS Code of Ethics, particularly when the work involves human participants, data collection, or social impact. | `extracted_frontend_01.md`, §2.3 — scoring.py:24; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 10 | `broader_impacts` | `"10. Broader Impacts"` | Verifies that the paper includes a broader impact statement discussing potential positive and negative societal consequences of the research. | `extracted_frontend_01.md`, §2.3 — scoring.py:26; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 11 | `safeguards` | `"11. Safeguards"` | Verifies that the paper describes safeguards implemented to mitigate potential harms or dual-use risks of the proposed system or dataset. | `extracted_frontend_01.md`, §2.3 — scoring.py:28; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 12 | `licenses` | `"12. Licenses"` | Verifies that all third-party assets (datasets, code, models) used in the paper have their licenses explicitly named and that the paper complies with those licenses. | `extracted_frontend_01.md`, §2.3 — scoring.py:30; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 13 | `assets` | `"13. Assets"` | Verifies that all assets introduced or used by the paper (datasets, models, code) are properly identified and that release or access information is provided. | `extracted_frontend_01.md`, §2.3 — scoring.py:31; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 14 | `crowdsourcing_human_subjects` | `"14. Crowdsourcing & Human Subjects"` | Verifies that any crowdsourcing or human participant study includes: instructions provided to participants, compensation details (with mandatory minimum compensation per NeurIPS ethics rules), and consent information. Note: a special warning `"⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."` is appended to the `alert_msg` for this item when flagged. | `extracted_frontend_01.md`, §2.3 — scoring.py:32; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:110–120 |
| 15 | `irb_approvals` | `"15. IRB Approvals"` | Verifies that the paper documents IRB (Institutional Review Board) approval or equivalent ethical review for studies involving human subjects. | `extracted_frontend_01.md`, §2.3 — scoring.py:33; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 16 | `declaration_llm_usage` | `"16. Declaration of LLM Usage"` | Verifies that the paper includes a declaration of any LLM usage in the research methodology, distinguishing between LLMs used as part of the method vs. LLMs used for writing assistance. | `extracted_frontend_01.md`, §2.3 — scoring.py:34; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |

---

## 3. Status Enums

### 3.1 Checklist Answer Values

Answer values are produced by the LLM in FASE 2 (`ReproducibilityEvaluationSkill`) and FASE 2.5 (`ChecklistVerificationSkill`). They are stored per checklist item in the `evaluation` dict and are consumed by `get_checklist_health()` for scoring.

Comparison in `get_checklist_health()` uses `.lower()` (case-insensitive): `"yes" in answer.lower()` and `"no" in answer.lower()`.

| Value | Display / Internal Meaning | Scoring Impact | Source |
|-------|---------------------------|----------------|--------|
| `'Yes'` | Item is compliant — the paper satisfies this checklist requirement | Risk flagged if `evidence` AND `justification` are both empty (`missing_evidence = True`, `pending_count += 1`) | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:110–120 |
| `'No'` | Item is not compliant — the paper does NOT satisfy this requirement | Risk flagged if `is_no_justified` is `False` OR `justification` is empty (`pending_justification = True`, `pending_count += 1`) | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:110–120 |
| `'N/A'` | Item is not applicable to this paper | No risk flagged. No `pending_count` increment. Item displays without alert. | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |
| `''` (empty string) | Not answered — LLM returned empty or the key is absent from evaluation dict | No risk flagged. Item displays with `answer` shown as `"—"`. | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |

**Evaluation dict per-item schema** (as passed to `get_checklist_health`):
```
{
  "answer":          str,           # "Yes" / "No" / "N/A" / ""
  "justification":   str,
  "evidence":        str,
  "is_no_justified": bool or str    # True/False or "true"/"false"
}
```
(Source: `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:37)

---

### 3.2 Health Status Enum

The health status is the top-level verdict returned by `get_checklist_health(evaluation: dict) -> dict`. The `status` field value determines the displayed audit verdict.

| Value | Meaning | Trigger Condition | Source |
|-------|---------|-------------------|--------|
| `'valid'` | All 16 checklist items have acceptable evidence or justification. The paper passes the reproducibility audit. | `pending_count == 0` (no items with missing evidence or missing justification) | `extracted_frontend_01.md`, §7.1 — scoring.py:122–123; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |
| `'risk'` | One or more checklist items are flagged for missing evidence (for `"Yes"` answers) or missing/unjustified negatives (for `"No"` answers). The paper is at risk of Desk Reject. | `pending_count > 0` | `extracted_frontend_01.md`, §7.1 — scoring.py:122–123; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |

**Early-exit guard:** When `evaluation` is falsy (`None`, `{}`, etc.), `get_checklist_health` returns immediately: `{"status": "risk", "items": [], "pending_count": 0, "total": 0}`. (Source: `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:56–62)

---

### 3.3 paper_type Enum

The `paper_type` field is returned by the LLM during FASE 1 extraction. Its value determines whether the audit proceeds or short-circuits.

| Value | Valid/Invalid | Description | Source |
|-------|---------------|-------------|--------|
| `'INVALID - Not ML/AI'` | **Invalid** | The submitted paper does not belong to the ML/AI research domain that the NeurIPS checklist targets. The audit short-circuits; no checklist evaluation is performed. | `extracted_backend_core_01.md`, §2.2 — prompts.py:4; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_010 |
| Any string not starting with `'INVALID'` | **Valid** | The paper is classified as an ML/AI paper. The audit proceeds through all 6 phases. | `extracted_backend_core_01.md`, §3.2 — auditor.py:~152; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_010 |

**Note:** No other specific valid `paper_type` string values were present in the extraction. The prompt instructs the LLM to classify the paper type in free text, and only the `startswith('INVALID')` guard is programmatically checked. (Source: `extracted_backend_core_01.md`, §2.2 — prompts.py:4)

---

## 4. Named Constants Glossary

### 4.1 CHECKLIST_KEYS

All 16 values in declaration order, exactly as they appear in `scoring.py`.

| Index | Key Value | Source |
|-------|-----------|--------|
| 1 | `"claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:8 |
| 2 | `"limitations"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 3 | `"theory_assumptions_proofs"` | `extracted_frontend_01.md`, §2.3 — scoring.py:10 |
| 4 | `"experimental_result_reproducibility"` | `extracted_frontend_01.md`, §2.3 — scoring.py:11 |
| 5 | `"open_access_data_code"` | `extracted_frontend_01.md`, §2.3 — scoring.py:12 |
| 6 | `"experimental_setting_details"` | `extracted_frontend_01.md`, §2.3 — scoring.py:13 |
| 7 | `"experiment_statistical_significance"` | `extracted_frontend_01.md`, §2.3 — scoring.py:14 |
| 8 | `"experiments_compute_resource"` | `extracted_frontend_01.md`, §2.3 — scoring.py:15 |
| 9 | `"code_of_ethics"` | `extracted_frontend_01.md`, §2.3 — scoring.py:16 |
| 10 | `"broader_impacts"` | `extracted_frontend_01.md`, §2.3 — scoring.py:17 |
| 11 | `"safeguards"` | `extracted_frontend_01.md`, §2.3 — scoring.py:18 |
| 12 | `"licenses"` | `extracted_frontend_01.md`, §2.3 — scoring.py:19 |
| 13 | `"assets"` | `extracted_frontend_01.md`, §2.3 — scoring.py:20 |
| 14 | `"crowdsourcing_human_subjects"` | `extracted_frontend_01.md`, §2.3 — scoring.py:21 |
| 15 | `"irb_approvals"` | `extracted_frontend_01.md`, §2.3 — scoring.py:22 |
| 16 | `"declaration_llm_usage"` | `extracted_frontend_01.md`, §2.3 — scoring.py:23 |

---

### 4.2 CHECKLIST_LABELS

All 16 display labels in declaration order, mapped to their corresponding key. Labels are exactly as they appear in `scoring.py`.

| Index | Key | Label | Source |
|-------|-----|-------|--------|
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:26 |
| 2 | `"limitations"` | `"2. Limitations"` | `extracted_frontend_01.md`, §2.3 — scoring.py:27 |
| 3 | `"theory_assumptions_proofs"` | `"3. Theory, Assumptions & Proofs"` | `extracted_frontend_01.md`, §2.3 — scoring.py:28 |
| 4 | `"experimental_result_reproducibility"` | `"4. Experimental Result Reproducibility"` | `extracted_frontend_01.md`, §2.3 — scoring.py:29 |
| 5 | `"open_access_data_code"` | `"5. Open Access to Data and Code"` | `extracted_frontend_01.md`, §2.3 — scoring.py:30 |
| 6 | `"experimental_setting_details"` | `"6. Experimental Setting / Details"` | `extracted_frontend_01.md`, §2.3 — scoring.py:31 |
| 7 | `"experiment_statistical_significance"` | `"7. Experiment Statistical Significance"` | `extracted_frontend_01.md`, §2.3 — scoring.py:32 |
| 8 | `"experiments_compute_resource"` | `"8. Experiments Compute Resource"` | `extracted_frontend_01.md`, §2.3 — scoring.py:33 |
| 9 | `"code_of_ethics"` | `"9. Code of Ethics"` | `extracted_frontend_01.md`, §2.3 — scoring.py:34 |
| 10 | `"broader_impacts"` | `"10. Broader Impacts"` | `extracted_frontend_01.md`, §2.3 — scoring.py:35 |
| 11 | `"safeguards"` | `"11. Safeguards"` | `extracted_frontend_01.md`, §2.3 — scoring.py:36 |
| 12 | `"licenses"` | `"12. Licenses"` | `extracted_frontend_01.md`, §2.3 — scoring.py:37 |
| 13 | `"assets"` | `"13. Assets"` | `extracted_frontend_01.md`, §2.3 — scoring.py:38 |
| 14 | `"crowdsourcing_human_subjects"` | `"14. Crowdsourcing & Human Subjects"` | `extracted_frontend_01.md`, §2.3 — scoring.py:39 |
| 15 | `"irb_approvals"` | `"15. IRB Approvals"` | `extracted_frontend_01.md`, §2.3 — scoring.py:40 |
| 16 | `"declaration_llm_usage"` | `"16. Declaration of LLM Usage"` | `extracted_frontend_01.md`, §2.3 — scoring.py:41 |

---

[... 145507 chars trimmed (priority 1)]