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

- `Hyperparameters` is used as the Pydantic response schema for the fallback call in `HybridHyperparameterExtractionSkill`'s REDUCE phase: `config={'response_schema': Hyperparameters}` — SOURCE: `rag_extraction_skill.py:239`.
- After cleaning (`_clean_with_regex`), fields `learning_rate` and `weight_decay` may be converted to `float`; `batch_size`, `epochs`, `random_seed` to `int`; all others remain `str` — SOURCE: `rag_extraction_skill.py:277`.

---

### Entity: `AuditState`

**Inherits From:** `pydantic.BaseModel`

Source: `backend/common/audit_state.py:22`

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `paper_text` | `str` | No | — | Set at construction | `audit_state.py:24` |
| `extracted_info` | `ExtractedInfo` | No | — | Nested technical metadata | `audit_state.py:25` |
| `evaluation` | `Dict[str, ChecklistItem]` | No | `{}` | Keyed by NeurIPS checklist items | `audit_state.py:26` |
| `metrics` | `Dict[str, Any]` | No | `{}` | Audit execution metrics | `audit_state.py:27` |
| `execution_time` | `float` | No | `0.0` | Total execution duration | `audit_state.py:28` |
| `red_flags` | `Dict[str, bool]` | No | `{}` | Regex-detected risk signals | `audit_state.py:29` |

#### Relationships

- `AuditState` is the primary container for the audit results, instantiated by `PaperAuditor.audit()` and consumed by the Streamlit frontend.
- Contains nested `ExtractedInfo` and `ChecklistItem` models.

---

### Entity: `ExtractedInfo`

**Inherits From:** `pydantic.BaseModel`

Source: `backend/common/audit_state.py:12`

| Field | Type | Nullable | Default | Description | Source |
|-------|------|----------|---------|-------------|--------|
| `paper_title` | `str` | No | `"Unknown"` | Title of the paper | `audit_state.py:14` |
| `authors` | `List[str]` | No | `[]` | List of author names | `audit_state.py:15` |
| `paper_type` | `str` | No | `"Unknown"` | E.g., "Computer Science" | `audit_state.py:16` |
| `thought_process` | `str` | No | `""` | LLM reasoning trail | `audit_state.py:17` |
| `hyperparameters` | `Dict[str, Any]` | No | `{}` | Technical HP extraction | `audit_state.py:18` |
| `hardware` | `Any` | No | `{}` | Hardware disclosures | `audit_state.py:19` |
| `context_mapping` | `List[str]` | No | `[]` | Identified sections | `audit_state.py:20` |

---

### Entity: `ChecklistItem`

**Inherits From:** `pydantic.BaseModel`

Source: `backend/common/audit_state.py:4`

| Field | Type | Nullable | Default | Description | Source |
|-------|------|----------|---------|-------------|--------|
| `answer` | `str` | No | — | `"Yes"`, `"No"`, or `"N/A"` | `audit_state.py:6` |
| `evidence` | `Optional[str]` | Yes | `None` | Verbatim cita from paper | `audit_state.py:7` |
| `justification` | `Optional[str]` | Yes | `None` | Reasoning for evaluation | `audit_state.py:8` |
| `verified` | `bool` | No | `False` | Flag for strict verification phase | `audit_state.py:9` |
| `was_corrected` | `bool` | No | `False` | True if verification changed answer | `audit_state.py:10` |

---

### Entity: `BaseSkill`

**Inherits From:** `abc.ABC`

Source: `base_skill.py:10`

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `llm_client` | `Optional[LLMClient]` | Yes | `None` | Stored from constructor param | `base_skill.py:19` |
| `config` | `Dict` | No | `{}` | If `None` passed, set to `{}`; stored from constructor param | `base_skill.py:19` |
| `name` | `str` | No | `self.__class__.__name__` | Set from runtime class name | `base_skill.py:19` |

#### Relationships

- Abstract method `execute(self, context: Dict[str, Any]) -> Dict[str, Any]` must be overridden by all concrete subclasses — SOURCE: `base_skill.py:34`.
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

### Entity: `PaperAuditor`

**Inherits From:** none (plain Python class)

Source: `backend/services/auditor.py:25`

Service orchestrator for the full audit pipeline. Initialised once per session (stored in `st.session_state.auditor` — `frontend/utils/session_state.py:12`). All five LLM clients are created with `AUDIT_CONFIG` (deterministic / JSON-mode settings).

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `extraction_llm` | `LLMClient` | No | — | `LLMClient(model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG)` | `auditor.py:31` |
| `evaluation_llm` | `LLMClient` | No | — | `LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=AUDIT_CONFIG)` | `auditor.py:34` |
| `rag_map_llm` | `LLMClient` | No | — | `LLMClient(model_name=MAP_MODEL_NAME, generation_config=AUDIT_CONFIG)` — MAP phase / triage | `auditor.py:37` |
| `rag_reduce_llm` | `LLMClient` | No | — | `LLMClient(model_name=REDUCE_MODEL_NAME, generation_config=AUDIT_CONFIG)` — REDUCE / consolidation phase | `auditor.py:40` |
| `verification_llm` | `LLMClient` | No | — | `LLMClient(model_name=VERIFICATION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — Auditor 2 strict verification | `auditor.py:43` |
| `extraction_skill` | `InformationExtractionSkill` | No | — | `InformationExtractionSkill(llm_client=self.extraction_llm)` | `auditor.py:46` |
| `hybrid_hp_skill` | `HybridHyperparameterExtractionSkill` | No | — | `HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm)` — RAG + Pydantic hyperparameter extraction | `auditor.py:47` |
| `evaluation_skill` | `ReproducibilityEvaluationSkill` | No | — | `ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm)` | `auditor.py:48` |
| `verification_skill` | `ChecklistVerificationSkill` | No | — | `ChecklistVerificationSkill(llm_client=self.verification_llm)` | `auditor.py:51` |
| `metrics_skill` | `MetricsCalculationSkill` | No | — | `MetricsCalculationSkill()` — no LLM client; deterministic calculation | `auditor.py:53` |
| `metadata_skill` | `MetadataAggregationSkill` | No | — | `MetadataAggregationSkill()` — no LLM client; assembles final result dict | `auditor.py:54` |

#### Relationships

- `audit(paper_text: str, status_callback=None) -> dict` — main orchestration method executing 4 phases + Phase 1.5 (RAG). Returns `resultado` dict on success; error dict on failure — SOURCE: `auditor.py:57`.
- All `*_llm` fields use `AUDIT_CONFIG` (deterministic JSON-mode); model names map to `config.py:41,43,37,39,45` respectively.
- All `*_skill` fields are `BaseSkill` subclasses stored for re-use across calls within a session.

---

### Entity: `SotaAnalyzer`

**Inherits From:** none (plain Python class)

Source: `backend/services/sota_analyzer.py:17`

Service orchestrator for the State-of-the-Art analysis pipeline. Initialised once per session (stored in `st.session_state.sota_analyzer` — `frontend/utils/session_state.py:15`). A single shared `LLMClient` with `SOTA_CONFIG` is used for all LLM-dependent skills.

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `thematic_skill` | `ThematicCoverageSkill` | No | — | `ThematicCoverageSkill(llm_client=llm_client)` — identifies subtopics and technical areas | `sota_analyzer.py:34` |
| `query_skill` | `QueryGenerationSkill` | No | — | `QueryGenerationSkill(llm_client=llm_client)` — generates Semantic Scholar search queries | `sota_analyzer.py:35` |
| `search_skill` | `SemanticScholarSearchSkill` | No | — | `SemanticScholarSearchSkill()` — no LLM; HTTP calls to Semantic Scholar API | `sota_analyzer.py:36` |
| `gap_skill` | `CoverageGapAnalysisSkill` | No | — | `CoverageGapAnalysisSkill(llm_client=llm_client)` — identifies bibliography coverage gaps | `sota_analyzer.py:37` |
| `validation_skill` | `CrossValidationSkill` | No | — | `CrossValidationSkill(llm_client=llm_client)` — detects omissions; selects up to 5 missing papers | `sota_analyzer.py:38` |

#### Relationships

- `analyze_sota(paper_text: str) -> Dict[str, Any]` — main orchestration method executing 5 sequential skill steps. Returns `final_results` dict with `metadata` key added — SOURCE: `sota_analyzer.py:45`.
- `search_skill` has no `llm_client`; it uses `SEMANTIC_SCHOLAR_BASE_URL`, `SEMANTIC_SCHOLAR_FIELDS`, `SEMANTIC_SCHOLAR_LIMIT`, `SEMANTIC_SCHOLAR_YEAR_RANGE` constants from `config.py:136–139`.
- All LLM-dependent skills share a single `LLMClient(generation_config=SOTA_CONFIG)` instance created locally in `__init__` — SOURCE: `sota_analyzer.py:31`.

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
| `logging.ERROR` | `Colors.RED" | `logger.py:25` |
| `logging.CRITICAL` | `Colors.BOLD + Colors.RED` | `logger.py:26` |

---

### Constants: RAG Operations

Source: `backend/skills/rag_extraction_skill.py`, `backend/skills/auditor_skills.py`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
| `NEGATION_WINDOW` | `60` | `int` | Chars before a regex match to inspect for negation context | `regex_detection_skills.py:8` |
| RAG `batch_size` | `15` | `int` | Chunks per embedding API batch | `rag_extraction_skill.py:61` |

#### Negation Detection Pattern (`NEGATION_PATTERNS`)

Source: `backend/skills/regex_detection_skills.py:10`

Module-level compiled regex (`re.Pattern`, flags `re.IGNORECASE`). Used by `_is_negated(text, match_start)` to search the `NEGATION_WINDOW` characters preceding a regex match; returns `True` if a negation context is found — SOURCE: `regex_detection_skills.py:21-25`.

| Branch | Pattern text | Language |
|--------|-------------|----------|
| 1 | `no\s+se\s+(?:especifica|menciona|indica|reporta|incluye|proporciona|detalla)` | Spanish |
| 2 | `falta(?:n)?(?:\s+informaci[oó]n)?` | Spanish |
| 3 | `sin\s+(?:especificar|detallar|mencionar|incluir|reportar|proporcionar)` | Spanish |
| 4 | `not\s+(?:specified|mentioned|reported|provided|included|disclosed|found)` | English |
| 5 | `missing|absent|omitted|lacks?|without` | English |
| 6 | `ERROR\s*\d*\s*:` | Error marker |

Source: `regex_detection_skills.py:10-18`

| Constant Name | Value | Type | Usage Context | Source |
|---------------|-------|------|---------------|--------|
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

Source: `rag_extraction_skill.py:152`

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

| Constant Name | Value | Type | Source |
|---|---|---|---|
| `priority_items` (local list in `ChecklistVerificationSkill.execute`) | `['claims', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiments_compute_resource', 'experiment_statistical_significance', 'licenses', 'declaration_llm_usage']` | `list[str]` | `auditor_skills.py:340` |

---

### Constants: Application-Level (Frontend)

Source: `frontend/config.py`

| Constant Name | Value | Type | Usage Context | Source |
|---|---|---|---|---|
| `TITLE` | `"💻 Auditor de Papers en Ciencias de la Computación"` | `str` | Page title (`st.title`) | `frontend/config.py:3` |
| `SIDEBAR_IMAGE` | `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"` | `str` | Sidebar ACM logo URL | `frontend/config.py:4` |
| `SIDEBAR_DESCRIPTION" | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` | `str` | Sidebar description | `frontend/config.py:5` |

---

### Constants: Saturation Error Keywords

Source: `frontend/components/file_uploader.py:60`

| Constant Name | Value | Type | Usage Context | Source |
|---|---|---|---|---|
| Saturation error keywords (list) | `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` | `list[str]` | Checked `in error_msg.upper()` to classify backend error as saturation vs hard failure | `file_uploader.py:60` |

---

### Constants: NeurIPS Quality Score Tiers

Source: `frontend/components/gauge_chart.py:14-31, 57-61`

| Score Range | Label | Bar Color | Type (Label / Color) | Source |
|---|---|---|---|---|
| `[87.5, 100]` | `"Strong Accept"` | `"#00aa00"` | `str` / `str` | `gauge_chart.py:14-16` |
| `[75, 87.5)` | `"Accept"` | `"#00cc44"` | `str` / `str` | `gauge_chart.py:17-19` |
| `[62.5, 75)` | `"Borderline"` | `"#ffcc00"` | `str` / `str` | `gauge_chart.py:20-22` |
| `[50, 62.5)` | `"Weak Reject"` | `"#ff9900"` | `str" / `str` | `gauge_chart.py:23-25` |
| `[25, 50)` | `"Reject"` | `"#ff4b4b"` | `str` / `str` | `gauge_chart.py:26-28` |
| `[0, 25)` | `"Strong Reject"` | `"#cc0000"` | `str" / `str` | `gauge_chart.py:29-31` |

Threshold line: `value=62.5`, `color="red"`, `width=4`. Source: `gauge_chart.py:57-61`.

---

### Constants: Compliance Table Row Colors

Source: `frontend/components/audit_results.py:18-32`

| Condition | Background Color | Meaning | Type | Source |
|---|---|---|---|---|
| `pending_justification == True` | `"#450a0a"` | Critical risk (deep red) | `str` | `audit_results.py:20-21` |
| `missing_evidence == True` OR `alert_msg` non-empty | `"#452e0a"` | Warning (amber/orange) | `str" | `audit_results.py:24-25` |
| `"yes" in answer.lower()` | `"#064e3b"` | OK (emerald green) | `str" | `audit_results.py:28-29` |
| All other cases | `"#111827"` | Neutral (dark) | `str" | `audit_results.py:32` |

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
| `resultado` | `AuditState | None` | `None` | **Set:** `file_uploader.py:50` after `auditor.audit()` completes. **Read:** `app.py:40-68`. **Cleared:** on "Limpiar" button press. | `session_state.py:7` |
| `auditor` | `PaperAuditor` | `PaperAuditor()` | **Set:** on first app load. **Read:** `file_uploader.py:49`. **Cleared:** on "Limpiar". | `session_state.py:12-13` |
| `chatbot` | `PaperChatbot` | `PaperChatbot()` | **Set:** on first app load. **Read:** `chatbot.py:26`. **Cleared:** on "Limpiar". | `session_state.py:15-16` |
| `sota_analyzer` | `SotaAnalyzer` | `SotaAnalyzer()` | **Set:** on first app load. **Read:** `sota_section.py:12`. **Cleared:** on "Limpiar". | `session_state.py:18-19` |
| `messages` | `list[dict]` | `[]` | **Set:** on first app load. **Mutated:** chatbot appends user/assistant messages. **Cleared:** on "Limpiar". | `session_state.py:21-22` |
| `md_text` | `str` | not initialised | **Set:** `file_uploader.py:36-39`. **Read:** chatbot, sota, app. **Cleared:** on "Limpiar". | `file_uploader.py:36-39` |

---

### CHECKLIST_KEYS Enum Set

Source: `frontend/utils/scoring.py:8-15`

| Key String | Position / Index | Meaning | Source |
|---|---|---|---|
| `"claims"` | 0 | NeurIPS item 1 — Claims | `scoring.py:9` |
| `"limitations"` | 1 | NeurIPS item 2 — Limitations | `scoring.py:10` |
| `"theory_assumptions_proofs"` | 2 | NeurIPS item 3 | `scoring.py:11` |
| `"experimental_result_reproducibility"` | 3 | NeurIPS item 4 | `scoring.py:12` |
| `"open_access_data_code"` | 4 | NeurIPS item 5 | `scoring.py:13` |
| `"experimental_setting_details"` | 5 | NeurIPS item 6 | `scoring.py:14` |
| `"experiment_statistical_significance"` | 6 | NeurIPS item 7 | `scoring.py:15` |
| `"experiments_compute_resource"` | 7 | NeurIPS item 8 | `scoring.py:16` |
| `"code_of_ethics"` | 8 | NeurIPS item 9 | `scoring.py:17` |
| `"broader_impacts"` | 9 | NeurIPS item 10 | `scoring.py:18` |
| `"safeguards"` | 10 | NeurIPS item 11 | `scoring.py:19` |
| `"licenses"` | 11 | NeurIPS item 12 | `scoring.py:20` |
| `"assets"` | 12 | NeurIPS item 13 | `scoring.py:21` |
| `"crowdsourcing_human_subjects"` | 13 | NeurIPS item 14 | `scoring.py:22` |
| `"irb_approvals"` | 14 | NeurIPS item 15 | `scoring.py:23` |
| `"declaration_llm_usage"` | 15 | NeurIPS item 16 | `scoring.py:24` |

---

### CHECKLIST_LABELS Display Strings

Source: `frontend/utils/scoring.py:17`

Maps each of the 16 checklist keys to its NeurIPS display label.

---

### Checklist Answer Values

Source: `extracted_backend_core_01.md § 2.2`

| Answer String | Semantics | Source |
|---|---|---|
| `"Yes"` | Item criterion is met | `prompts.py:378` |
| `"No"` | Item criterion is not met | `prompts.py:378` |
| `"N/A"` | Item is not applicable | `prompts.py:378` |

---

## 5. LLM Response JSON Schemas

### LLM Schema: `get_extraction_prompt` → extraction result

Source: `backend/common/prompts.py:4`

[The detailed extraction sub-schemas follow here, mirroring the canonical extraction result structure...]

---

### LLM Schema: `get_map_extraction_prompt` → map fragment result

Source: `backend/common/prompts.py:184`

---

### LLM Schema: `get_reduce_extraction_prompt` → consolidated master result

Source: `backend/common/prompts.py:228`

---

### LLM Schema: `get_evaluation_prompt` → evaluation result

Source: `backend/common/prompts.py:378`

---

### LLM Schema: `get_verification_prompt` → verification result

Source: `backend/common/prompts.py:494`

---

### LLM Schema: `get_evaluation_signals` → signals dict (deterministic function)

Source: `backend/common/prompts.py:273`

---

### Virtual Schema: `resultado` (audit result dict)

Source: `auditor_skills.py:285`

The final output dict produced by `MetadataAggregationSkill`.

---

*End of Data Model Specification.*
