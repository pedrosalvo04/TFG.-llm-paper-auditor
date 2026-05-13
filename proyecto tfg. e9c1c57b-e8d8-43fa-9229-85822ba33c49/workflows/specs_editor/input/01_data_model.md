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

**Inherits From:** [GAP: base class not extractable — source file `backend/common/audit_state.py` absent from repository]

Source: `tests/test_audit_state.py` (inferred from test assertions); `backend/common/audit_state.py` — UNRESOLVED (file absent)

> **CONFIDENCE: UNRESOLVED.** The file `backend/common/audit_state.py` does not exist in the repository. The contracts below are INFERRED from test assertions in `tests/test_audit_state.py` and are NOT confirmed from source. See cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY [g_014].

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `paper_text` | `str` | No | — | Set at construction | `tests/test_audit_state.py:6` |
| `invalid_paper` | `bool` | No | `False` | Default from construction rule | `tests/test_audit_state.py:9` |
| `execution_time` | `float` | No | `0.0` | Default from construction rule | `tests/test_audit_state.py:10` |
| `evaluation` | `dict` | Yes (optional) | `{}` (inferred — `AuditState(paper_text=...)` at `test_audit_state.py:7` omits `evaluation` arg and passes; `ReproducibilityEvaluationSkill.execute()` returns `{'evaluation': {}}` for fallback paths, confirming empty dict is the baseline value) | Dict keyed by any of 16 `CHECKLIST_KEYS` strings (`"claims"` … `"declaration_llm_usage"`); each value is a checklist-item dict — see sub-schema below | `tests/test_audit_state.py:13–14`; dict structure: `auditor_skills.py:387–392`; usage pattern: `scratch/test_checklist_health.py:6–22` |

##### `evaluation` checklist-item dict sub-schema

Each value in the `evaluation` dict is a plain Python dict constructed by `ChecklistVerificationSkill.execute()`. The same four-key structure is produced by the LLM evaluation phase (`ReproducibilityEvaluationSkill`) and confirmed by `scratch/test_checklist_health.py:6–22`.

| Sub-field | Type | Required when | Description | Source |
|-----------|------|---------------|-------------|--------|
| `answer` | `str` | Always | Exactly `"Yes"`, `"No"`, or `"N/A"` | `auditor_skills.py:387` |
| `evidence` | `str` | `answer == "Yes"` | Paper section + verbatim fragment | `auditor_skills.py:388` |
| `justification` | `str` | `answer != "Yes"` | Reason for No/N/A — missing element and transparency risk | `auditor_skills.py:389` |
| `is_no_justified` | `bool` | Always | `True` only if explicit justification or pre-computed signal applies | `auditor_skills.py:390` |
| `verified` | `bool` | After verification phase | Always `True` when set by `ChecklistVerificationSkill` | `auditor_skills.py:391` |
| `was_refined` | `bool` | After verification phase | `True` if initial answer unchanged (refined only); `False` if answer was corrected | `auditor_skills.py:392` |

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
| `code` | object (wrapper type; primary source absent) | No (non-None default) — `ExtractedInfo()` constructs with no args and `code.repository_url` equals `"NOT FOUND"`, confirming a default non-None object | object with all sub-fields defaulting to `"NOT FOUND"` (inferred — see sub-field contracts below) | Attribute-access wrapper around the `"code"` sub-dict of the extraction JSON schema; 5 confirmed sub-fields — see sub-field contracts below | `tests/test_audit_state.py:22` (attribute access); `prompts.py:81–86` (sub-field schema) |
| `hyperparameters` | object (wrapper type; primary source absent) | No (non-None default) — same `ExtractedInfo()` no-args construction and `hyperparameters.optimizer` equals `"NOT FOUND"` | object with all sub-fields defaulting to `"NOT FOUND"` (inferred — see sub-field contracts below) | Attribute-access wrapper around the `"hyperparameters"` sub-dict of the extraction JSON schema; 12 confirmed sub-fields — see sub-field contracts below | `tests/test_audit_state.py:23` (attribute access); `prompts.py:97–108` (sub-field schema) |

#### Sub-field contracts

##### `code` object sub-fields

Attribute access confirmed via `tests/test_audit_state.py:22` (`info.code.repository_url == "NOT FOUND"`). Sub-field names confirmed from extraction JSON schema in `prompts.py:81–86`. Actual wrapper class name: `[GAP: not determinable — primary source absent]`.

| Sub-field | Type | Default | Source |
|-----------|------|---------|--------|
| `repository_url` | `str` | `"NOT FOUND"` | `tests/test_audit_state.py:22` (access confirmed); `prompts.py:82` (field name confirmed) |
| `negative_phrase` | `str` | `"NOT FOUND"` | `prompts.py:83` |
| `dependencies` | `str` | `"NOT FOUND"` | `prompts.py:84` |
| `instructions` | `str` | `"yes"` or `"no"` or `"NOT FOUND"` | `prompts.py:85` |
| `release_mention` | `str` | `"NOT FOUND"` | `prompts.py:86` |

##### `hyperparameters` object sub-fields

Attribute access confirmed via `tests/test_audit_state.py:23` (`info.hyperparameters.optimizer == "NOT FOUND"`). Sub-field names confirmed from extraction JSON schema in `prompts.py:97–108`. Actual wrapper class name: `[GAP: not determinable — primary source absent]`.

| Sub-field | Type | Default | Source |
|-----------|------|---------|--------|
| `optimizer` | `str` | `"NOT FOUND"` | `tests/test_audit_state.py:23` (access confirmed); `prompts.py:97` (field name confirmed) |
| `learning_rate` | `str` | `"NOT FOUND"` | `prompts.py:98` |
| `batch_size` | `str` | `"NOT FOUND"` | `prompts.py:99` |
| `epochs` | `str` | `"NOT FOUND"` | `prompts.py:100` |
| `training_steps` | `str` | `"NOT FOUND"` | `prompts.py:101` |
| `total_tokens` | `str` | `"NOT FOUND"` | `prompts.py:102` |
| `warmup` | `str` | `"NOT FOUND"` | `prompts.py:103` |
| `weight_decay` | `str` | `"NOT FOUND"` | `prompts.py:104` |
| `betas` | `str` | `"NOT FOUND"` | `prompts.py:105` |
| `epsilon` | `str` | `"NOT FOUND"` | `prompts.py:106` |
| `vague_phrase` | `str` | `"NOT FOUND"` | `prompts.py:107` |
| `table_reference` | `str` | `"NOT FOUND"` | `prompts.py:108` |

---

### Entity: `ChecklistItem`

**Inherits From:** [GAP: base class not extractable — source file `backend/common/audit_state.py` absent]

Source: `tests/test_audit_state.py` — UNRESOLVED (class present but not exercised in tests)

> **CONFIDENCE: UNRESOLVED.** No field contracts are derivable from test code. The class is defined in `backend/common/audit_state.py` which is absent from the repository.

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| [GAP: field contract not resolved in extraction — class not instantiated in any test; primary source `backend/common/audit_state.py` absent] | | | | | `tests/test_audit_state.py:2` |

> **Inferred field structure (NOT confirmed from primary source):** Based on `auditor_skills.py:387–392` which constructs plain dicts used as checklist-item values in `AuditState.evaluation`, the `ChecklistItem` class likely corresponds to an object or dataclass with the following fields: `answer` (`str`), `evidence` (`str`), `justification` (`str`), `is_no_justified` (`bool`), and after `ChecklistVerificationSkill` processing: additionally `verified` (`bool`) and `was_refined` (`bool`). These field names are confirmed as dict keys at `auditor_skills.py:387–392` and as expected dict keys at `scratch/test_checklist_health.py:6–22`. Whether `ChecklistItem` is a dataclass with these exact field names: `[GAP: unconfirmable without primary source]`.

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
| `logging.ERROR` | `Colors.RED` | `logger.py:25` |
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
| 1 | `no\s+se\s+(?:especifica\|menciona\|indica\|reporta\|incluye\|proporciona\|detalla)` | Spanish |
| 2 | `falta(?:n)?(?:\s+informaci[oó]n)?` | Spanish |
| 3 | `sin\s+(?:especificar\|detallar\|mencionar\|incluir\|reportar\|proporcionar)` | Spanish |
| 4 | `not\s+(?:specified\|mentioned\|reported\|provided\|included\|disclosed\|found)` | English |
| 5 | `missing\|absent\|omitted\|lacks?\|without` | English |
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
| `SIDEBAR_DESCRIPTION` | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` | `str` | Sidebar description | `frontend/config.py:5` |

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
| `[50, 62.5)` | `"Weak Reject"` | `"#ff9900"` | `str` / `str` | `gauge_chart.py:23-25` |
| `[25, 50)` | `"Reject"` | `"#ff4b4b"` | `str` / `str` | `gauge_chart.py:26-28` |
| `[0, 25)` | `"Strong Reject"` | `"#cc0000"` | `str` / `str` | `gauge_chart.py:29-31` |

Threshold line: `value=62.5`, `color="red"`, `width=4`. Source: `gauge_chart.py:57-61`.

---

### Constants: Compliance Table Row Colors

Source: `frontend/components/audit_results.py:18-32`

| Condition | Background Color | Meaning | Type | Source |
|---|---|---|---|---|
| `pending_justification == True` | `"#450a0a"` | Critical risk (deep red) | `str` | `audit_results.py:20-21` |
| `missing_evidence == True` OR `alert_msg` non-empty | `"#452e0a"` | Warning (amber/orange) | `str` | `audit_results.py:24-25` |
| `"yes" in answer.lower()` | `"#064e3b"` | OK (emerald green) | `str` | `audit_results.py:28-29` |
| All other cases | `"#111827"` | Neutral (dark) | `str` | `audit_results.py:32` |

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
| `archivo_actual` | `str` | not initialised | **Set:** `file_uploader.py:19` to `uploaded_file.name`. **Read:** `file_uploader.py:16` to detect file change. **Cleared:** on "Limpiar" button press (`frontend/app.py:29-31`, all session keys deleted via `del st.session_state[key]` loop). | `file_uploader.py:19` |
| `file_hash` | `str` (MD5 hex digest) | not initialised | **Set:** `file_uploader.py:20` to `hashlib.md5(file_content).hexdigest()`. **Read:** `file_uploader.py:17` to detect content change. **Cleared:** on "Limpiar" button press (`frontend/app.py:29-31`, all session keys deleted via `del st.session_state[key]` loop). | `file_uploader.py:20` |
| `md_text` | `str` | not initialised | **Set:** `file_uploader.py:36` (PDF path) or `file_uploader.py:39` (TXT/MD path) to full paper text. **Read:** `chatbot.py:26`, `sota_section.py:12`, `app.py:53-54`, `file_uploader.py:98`. **Cleared:** on "Limpiar" button press (`frontend/app.py:29-31`, all session keys deleted via `del st.session_state[key]` loop). | `file_uploader.py:36-39` |

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

### CHECKLIST_LABELS Display Strings

Source: `frontend/utils/scoring.py:17`

Maps each of the 16 checklist keys to its NeurIPS display label. Used in UI rendering via `CHECKLIST_LABELS.get(key, key)` — SOURCE: `scoring.py:112`.

| Checklist Key | Display Label | Source |
|---|---|---|
| `"claims"` | `"1. Claims"` | `scoring.py:18` |
| `"limitations"` | `"2. Limitations"` | `scoring.py:19` |
| `"theory_assumptions_proofs"` | `"3. Theory, Assumptions & Proofs"` | `scoring.py:20` |
| `"experimental_result_reproducibility"` | `"4. Experimental Result Reproducibility"` | `scoring.py:21` |
| `"open_access_data_code"` | `"5. Open Access to Data and Code"` | `scoring.py:22` |
| `"experimental_setting_details"` | `"6. Experimental Setting / Details"` | `scoring.py:23` |
| `"experiment_statistical_significance"` | `"7. Experiment Statistical Significance"` | `scoring.py:24` |
| `"experiments_compute_resource"` | `"8. Experiments Compute Resource"` | `scoring.py:25` |
| `"code_of_ethics"` | `"9. Code of Ethics"` | `scoring.py:26` |
| `"broader_impacts"` | `"10. Broader Impacts"` | `scoring.py:27` |
| `"safeguards"` | `"11. Safeguards"` | `scoring.py:28` |
| `"licenses"` | `"12. Licenses"` | `scoring.py:29` |
| `"assets"` | `"13. Assets"` | `scoring.py:30` |
| `"crowdsourcing_human_subjects"` | `"14. Crowdsourcing & Human Subjects"` | `scoring.py:31` |
| `"irb_approvals"` | `"15. IRB Approvals"` | `scoring.py:32` |
| `"declaration_llm_usage"` | `"16. Declaration of LLM Usage"` | `scoring.py:33` |

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
| `verified` | `bool` | Always `True` after verification | `auditor_skills.py:391` |
| `was_refined` | `bool` | `True` if NOT corrected (answer unchanged); `False` if answer was overwritten | `auditor_skills.py:392` |

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
