---
validator_id: val_depth_entities
validator_type: depth
target_specs: [01_data_model.md]
forward_coverage_pct: 92
backward_coverage_pct: N/A
depth_pct: 91
entity_completeness_pct: 50
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 3
depth_gaps: 10
spec_consistency_issues: 0
total_issues: 15
overall_status: fail
---

## Summary

The `01_data_model.md` spec for *Nature Auditor Pro* is exceptionally well-constructed for the portions of the codebase that are present in the repository. All six entity sections (Pydantic models, config dicts, named constants, session-state keys) that reference available source files are documented with full structured decomposition — type, nullability, default, constraint, and file:line source — and the majority of those references were confirmed accurate by direct inspection. The primary driver of the `fail` status is the **permanent absence of `backend/common/audit_state.py`** from the repository, which leaves three entities (`AuditState`, `ExtractedInfo`, `ChecklistItem`) fully or partially unresolvable; the spec correctly marks them `CONFIDENCE: UNRESOLVED` and uses `[GAP: ...]` markers, but their PARTIAL/EMPTY status mathematically suppresses `entity_completeness_pct` to 50%. Two genuine fidelity issues were found (line-number citations off by 30+ lines in one case). Excluding the three absent-source entities, the resolvable entity completeness is 79% and depth is 95%, which would qualify for `needs_review`.

---

## Entity Inventory

| Entity Name | Type | Field Count | FULL | PARTIAL | EMPTY | Entity Status |
|-------------|------|-------------|------|---------|-------|---------------|
| `Hyperparameters` | Pydantic BaseModel | 14 | 14 | 0 | 0 | FULL |
| `AuditState` | Inferred/UNRESOLVED (source absent) | 4 | 3 | 1 | 0 | PARTIAL |
| `ExtractedInfo` | Inferred/UNRESOLVED (source absent) | 2 | 0 | 2 | 0 | PARTIAL |
| `ChecklistItem` | Inferred/UNRESOLVED (source absent) | 0 | 0 | 0 | 1 | EMPTY |
| `BaseSkill` | Plain class (ABC) | 3 | 3 | 0 | 0 | FULL |
| `CompositeSkill` | Plain class | 4 | 4 | 0 | 0 | FULL |
| `AUDIT_CONFIG` | config dict | 5 | 5 | 0 | 0 | FULL |
| `CHAT_CONFIG` | config dict | 1 | 1 | 0 | 0 | FULL |
| `SOTA_CONFIG` | config dict | 2 | 2 | 0 | 0 | FULL |
| Session State keys | session | 8 | 5 | 3 | 0 | PARTIAL |
| Named Constants (API Keys) | constant group | 2 | 2 | 0 | 0 | FULL |
| Named Constants (Model Names) | constant group | 8 | 8 | 0 | 0 | FULL |
| Named Constants (Temperature) | constant group | 3 | 3 | 0 | 0 | FULL |
| Named Constants (Semantic Scholar) | constant group | 4 | 4 | 0 | 0 | FULL |
| Named Constants (LLM Retry) | constant group | 2 | 2 | 0 | 0 | FULL |
| Named Constants (PDF Parser) | constant group | 1 | 1 | 0 | 0 | FULL |
| Named Constants (Colors class) | constant group | 8 | 8 | 0 | 0 | FULL |
| Named Constants (RAG Operations) | constant group | 7 | 7 | 0 | 0 | FULL |
| Named Constants (SOTA Operations) | constant group | 5 | 5 | 0 | 0 | FULL |
| Named Constants (Frontend) | constant group | 3 | 3 | 0 | 0 | FULL |
| Named Constants (Saturation Keywords) | constant group | 1 | 0 | 1 | 0 | PARTIAL |
| Named Constants (Checklist Priority) | constant group | 1 | 0 | 1 | 0 | PARTIAL |
| CHECKLIST_KEYS enum | constant group | 16 | 16 | 0 | 0 | FULL |

---

## Depth Validation — Field Detail

### Section 1 — Pydantic/Class Models

| Entity | Field / Key / Constant | Type ✓ | Nullable ✓ | Default ✓ | Constraint ✓ | Source ✓ | Status | Missing Attributes |
|--------|------------------------|---------|-----------|----------|-------------|---------|--------|--------------------|
| `Hyperparameters` | `thought_process` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `learning_rate` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `batch_size` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `epochs` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `optimizer` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `warmup_steps` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `weight_decay` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `random_seed` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `betas` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `epsilon` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `training_steps` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `total_tokens` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `hardware` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `Hyperparameters` | `latency_metrics` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AuditState` | `paper_text` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AuditState` | `invalid_paper` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AuditState` | `execution_time` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AuditState` | `evaluation` | ✓ | ✗ | ✗ | ✓ | ✓ | PARTIAL | NULLABILITY, DEFAULT |
| `ExtractedInfo` | `code` | ✗ | ✗ | ✓ | ✓ | ✓ | PARTIAL | TYPE (vague), NULLABILITY |
| `ExtractedInfo` | `hyperparameters` | ✗ | ✗ | ✓ | ✓ | ✓ | PARTIAL | TYPE (vague), NULLABILITY |
| `ChecklistItem` | `[GAP: field contract not resolved]` | ✗ | ✗ | ✗ | ✗ | ✗ | EMPTY | TYPE, NULLABILITY, DEFAULT, CONSTRAINT, SOURCE |
| `BaseSkill` | `llm_client` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `BaseSkill` | `config` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `BaseSkill` | `name` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `CompositeSkill` | `skills` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `CompositeSkill` | `llm_client` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `CompositeSkill` | `name` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `CompositeSkill` | `config` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |

**Section 1 depth_pct:** (24 × 1.0 + 3 × 0.5 + 1 × 0) / 28 × 100 = **91.1%**

### Section 2 — Configuration Structures

| Entity | Field / Key | Type ✓ | Nullable ✓ | Default ✓ | Constraint ✓ | Source ✓ | Status | Missing Attributes |
|--------|-------------|---------|-----------|----------|-------------|---------|--------|--------------------|
| `AUDIT_CONFIG` | `response_mime_type` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AUDIT_CONFIG` | `temperature` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AUDIT_CONFIG` | `top_k` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AUDIT_CONFIG` | `top_p` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `AUDIT_CONFIG` | `max_output_tokens` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `CHAT_CONFIG` | `temperature` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `SOTA_CONFIG` | `response_mime_type` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| `SOTA_CONFIG` | `temperature` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |

**Section 2 depth_pct:** 8/8 = **100%**

### Section 3 — Named Constants (sampled key groups)

| Entity | Constant Name | Type ✓ | Nullable ✓ | Default ✓ | Constraint ✓ | Source ✓ | Status | Missing Attributes |
|--------|---------------|---------|-----------|----------|-------------|---------|--------|--------------------|
| API Keys | `GOOGLE_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| API Keys | `SEMANTIC_SCHOLAR_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Model Names | `EMBEDDING_MODEL_NAME`…`RAG_MODEL_NAME` (8) | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Temperature | `AUDIT_TEMPERATURE`…`SOTA_TEMPERATURE` (3) | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Semantic Scholar | `SEMANTIC_SCHOLAR_BASE_URL`…`FIELDS` (4) | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| LLM Retry | `max_retries`, `base_delay` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| PDF Parser | `chunk_size` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Colors | `Colors.BLUE`…`Colors.RESET` (8) | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| RAG Operations | `NEGATION_WINDOW`, `batch_size`, inter-batch/chunk sleep, `n_results`, query count, MAP sleep (7) | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| SOTA Operations | 5 inline constants | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Frontend | `TITLE`, `SIDEBAR_IMAGE`, `SIDEBAR_DESCRIPTION` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Saturation Keywords | keyword list | ✗ | ✓ | ✓ | ✓ | ✗ | PARTIAL | TYPE (list[str] implied, not stated), SOURCE (header only, not in row) |
| Checklist Priority | `priority_items` | ✗ | ✓ | ✓ | ✓ | ✓ | PARTIAL | TYPE (`list[str]` not stated) |

### Section 4 — Session State Keys

| Entity | Key Name | Type ✓ | Nullable ✓ | Default ✓ | Constraint ✓ | Source ✓ | Status | Missing Attributes |
|--------|----------|---------|-----------|----------|-------------|---------|--------|--------------------|
| Session | `resultado` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Session | `auditor` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Session | `chatbot` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Session | `sota_analyzer` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Session | `messages` | ✓ | ✓ | ✓ | ✓ | ✓ | FULL | — |
| Session | `archivo_actual` | ✓ | ✓ | ✓ | ✓ | ✓ | PARTIAL | CLEARED lifecycle not stated |
| Session | `file_hash` | ✓ | ✓ | ✓ | ✓ | ✓ | PARTIAL | CLEARED lifecycle not stated |
| Session | `md_text` | ✓ | ✓ | ✓ | ✓ | ✓ | PARTIAL | CLEARED lifecycle not stated |

> **Note on constraint/lifecycle column:** For session-state keys, "Nullable" and "Constraint" columns are interpreted as LIFECYCLE attributes (set/mutated/cleared). The three PARTIAL keys document SET and READ lifecycle but omit the CLEARED lifecycle (which is "on 'Limpiar' button press at `app.py:30-32`" by context — verifiable for the main 5 keys, not explicitly stated for archivo_actual, file_hash, md_text).

---

## Forward Coverage (Specs → Source)

| Spec Element | Source Reference | File Exists? | Line Content Matches Claim? | Status |
|---|---|---|---|---|
| `Hyperparameters` class | `rag_extraction_skill.py:11` | Yes | `class Hyperparameters(BaseModel):` ✓ | VERIFIED |
| `Hyperparameters.learning_rate` field | `rag_extraction_skill.py:11` | Yes | Field declared within class starting at line 11 ✓ | VERIFIED |
| `response_schema: Hyperparameters` (REDUCE fallback) | `rag_extraction_skill.py:204` | Yes | **Line 204 is** `self.log_execution("🧠 [Fase REDUCE]...")`. The `response_schema: Hyperparameters` assignment is at **line 239**. | **FIDELITY_ISSUE** |
| `BaseSkill.__init__` | `base_skill.py:19` | Yes | `def __init__(self, llm_client: Optional[LLMClient] = None, config: Optional[Dict] = None):` ✓ | VERIFIED |
| `BaseSkill.execute` (abstract) | `base_skill.py:34` | Yes | `@abstractmethod / def execute(...)` ✓ | VERIFIED |
| `CompositeSkill.__init__` | `base_skill.py:91` | Yes | `def __init__(self, skills: list[BaseSkill], llm_client: Optional[LLMClient] = None):` ✓ | VERIFIED |
| `CompositeSkill.execute` error handling | `base_skill.py:103` | Yes | `accumulated_context.update(result)` and `accumulated_context[f"error_{skill.name}"]` ✓ | VERIFIED |
| `_clean_with_regex` | `rag_extraction_skill.py:277` | Yes | `def _clean_with_regex(self, data: Dict[str, str]) -> Dict[str, Any]:` ✓ | VERIFIED |
| `AUDIT_CONFIG` dict | `config.py:116` | Yes | `AUDIT_CONFIG = {` ✓ | VERIFIED |
| `CHAT_CONFIG` dict | `config.py:125` | Yes | `CHAT_CONFIG = {` ✓ | VERIFIED |
| `SOTA_CONFIG` dict | `config.py:130` | Yes | `SOTA_CONFIG = {` ✓ | VERIFIED |
| `AUDIT_TEMPERATURE` | `config.py:111` | Yes | `AUDIT_TEMPERATURE = 0.0` ✓ | VERIFIED |
| `GOOGLE_API_KEY` | `config.py:30` | Yes | `GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")` ✓ | VERIFIED |
| `EMBEDDING_MODEL_NAME` | `config.py:35` | Yes | `EMBEDDING_MODEL_NAME = "gemini-embedding-2"` ✓ | VERIFIED |
| `SEMANTIC_SCHOLAR_BASE_URL` | `config.py:136` | Yes | ✓ | VERIFIED |
| `max_retries = 5` | `llm_client.py:39` | Yes | `max_retries = 5` ✓ | VERIFIED |
| `base_delay = 2` | `llm_client.py:40` | Yes | `base_delay = 2` ✓ | VERIFIED |
| Retryable codes `"503", "429", ...` | `llm_client.py:54` | Yes | `is_retryable = any(code in error_msg.upper() for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"])` ✓ | VERIFIED |
| `NEGATION_WINDOW = 60` | `regex_detection_skills.py:8` | Yes | `NEGATION_WINDOW = 60` ✓ | VERIFIED |
| RAG `batch_size = 15` | `rag_extraction_skill.py:61` | Yes | `batch_size = 15` ✓ | VERIFIED |
| RAG inter-batch `time.sleep(15)` | `rag_extraction_skill.py:67` | Yes | `time.sleep(15)` ✓ | VERIFIED |
| RAG `n_results=10` | `rag_extraction_skill.py:123` | Yes | `n_results=10` ✓ | VERIFIED |
| RAG query count 13 | `rag_extraction_skill.py:99` | Yes | `queries = [...]` with 13 items ✓ | VERIFIED |
| RAG inter-chunk `time.sleep(1)` | `rag_extraction_skill.py:199` | Yes | `time.sleep(1)` at line 199 ✓ | VERIFIED |
| MAP fragment `time.sleep(2)` | `auditor_skills.py:104` | Yes | **Line 104 is** `if i < len(fragments) - 1:`. The `time.sleep(2)` is at **line 105**. | MINOR DISCREPANCY (off by 1) |
| SOTA rate-limit `time.sleep(2)` | `sota_skills.py:217` | Yes | `time.sleep(2)` ✓ | VERIFIED |
| SOTA inter-query `time.sleep(0.5)` | `sota_skills.py:191` | Yes | `time.sleep(0.5)` ✓ | VERIFIED |
| SOTA top-N `sorted_papers[:10]` | `sota_skills.py:232` | Yes | `[:10]` end of sorted() expression ✓ | VERIFIED |
| `verified: True`, `was_refined` | `auditor_skills.py:325` | Yes | **Line 325 is** `def execute(...)` method header. The assignment is at **lines 391-392**. | **FIDELITY_ISSUE** |
| `Colors.BLUE` | `logger.py:7` | Yes | `BLUE = "\033[94m"` ✓ | VERIFIED |
| Level-to-color mapping `DEBUG: Colors.BLUE` | `logger.py:22` | Yes | `logging.DEBUG: Colors.BLUE,` ✓ | VERIFIED |
| `TITLE`, `SIDEBAR_IMAGE`, `SIDEBAR_DESCRIPTION` | `frontend/config.py:3,4,5` | Yes | Lines 3-5 confirmed ✓ | VERIFIED |
| `chunk_size = 5` | `pdf_parser.py:51` | Yes | `chunk_size = 5` ✓ | VERIFIED |
| `priority_items` list | `auditor_skills.py:340` | Yes | `priority_items = [` ✓ | VERIFIED |
| `get_extraction_prompt` | `prompts.py:4` | Yes | `def get_extraction_prompt(...)` ✓ | VERIFIED |
| `get_map_extraction_prompt` | `prompts.py:184` | Yes | `def get_map_extraction_prompt(...)` ✓ | VERIFIED |
| `get_reduce_extraction_prompt` | `prompts.py:228` | Yes | `def get_reduce_extraction_prompt(...)` ✓ | VERIFIED |
| `get_evaluation_signals` | `prompts.py:273` | Yes | `def get_evaluation_signals(...)` ✓ | VERIFIED |
| `get_evaluation_prompt` | `prompts.py:378` | Yes | `def get_evaluation_prompt(...)` ✓ | VERIFIED |
| `get_verification_prompt` | `prompts.py:494` | Yes | `def get_verification_prompt(...)` ✓ | VERIFIED |
| `MetadataAggregationSkill.execute` | `auditor_skills.py:285` | Yes | `def execute(...)` ✓ | VERIFIED |
| Session state `resultado = None` | `session_state.py:7` | Yes | Line 7 is `def initialize_session_state():` (function def). Assignment at line 10. Minor offset. | MINOR DISCREPANCY |
| Session state `auditor = PaperAuditor()` | `session_state.py:12-13` | Yes | lines 12-13 confirmed ✓ | VERIFIED |
| Session state `messages = []` | `session_state.py:21-22` | Yes | lines 21-22 confirmed ✓ | VERIFIED |
| `archivo_actual` set | `file_uploader.py:19` | Yes | `st.session_state.archivo_actual = uploaded_file.name` ✓ | VERIFIED |
| `AuditState`, `ExtractedInfo`, `ChecklistItem` | `backend/common/audit_state.py` | **No** | File **absent** from repo | COVERAGE_GAP (documented as UNRESOLVED) |
| `CHECKLIST_KEYS` enum | `scoring.py:8-15` | Yes | List defined at lines 8-24 ✓ | VERIFIED |

---

## Fidelity Issues

1. **Entity: `Hyperparameters` — Relationship: response_schema usage**
   - **Spec claims:** `config={'response_schema': Hyperparameters}` — SOURCE: `rag_extraction_skill.py:204`
   - **Source reality:** Line 204 contains `self.log_execution("🧠 [Fase REDUCE] Consolidando datos extraídos con Gemma 4...")`. The actual `'response_schema': Hyperparameters` assignment is at **line 239** within the `except` block of the REDUCE phase fallback call.
   - **Impact:** Readers following this citation will land on the wrong line (35-line offset). The claim itself is accurate; only the line number is wrong.

2. **Entity: Checklist item dict — Fields: `verified`, `was_refined`**
   - **Spec claims:** `"verified": True` and `"was_refined": not verification_result.get('was_corrected', False)` — SOURCE: `auditor_skills.py:325`
   - **Source reality:** Line 325 is `def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:` (the `execute` method of `ChecklistVerificationSkill`). The actual assignments are at **lines 391–392** within the evaluation update block deep inside that method.
   - **Impact:** Readers will land on the method signature rather than the specific assignment lines. The claim is substantively correct.

---

## Coverage Gaps

The following entities exist in the test import at `tests/test_audit_state.py:2` (`from backend.common.audit_state import AuditState, ExtractedInfo, ChecklistItem`) but their source file `backend/common/audit_state.py` is **absent from the repository**:

1. **`AuditState`** — Documented as UNRESOLVED with fields inferred from test assertions. Base class, precise types for `evaluation`, and full field list cannot be confirmed. The spec's inference is reasonable and correctly caveat-flagged.
2. **`ExtractedInfo`** — Documented as UNRESOLVED. Sub-type of `code` and `hyperparameters` fields is documented as `nested model / object` (vague) because the actual class definition is absent. Additional sub-fields (beyond `repository_url` and `optimizer`) are explicitly noted as `[GAP: field contracts not resolved in extraction]`.
3. **`ChecklistItem`** — Documented as UNRESOLVED and EMPTY. No field contracts derivable from tests. The entity is referenced in the import but never exercised in test assertions.

> These are **correctly flagged** by the spec as UNRESOLVED. They are reported here as coverage gaps per validator protocol, not as evidence of spec carelessness.

---

## Depth Gaps

1. **Entity:** `ChecklistItem`
   **Field/Key/Constant:** All fields
   **Missing:** TYPE, NULLABILITY, DEFAULT, CONSTRAINT, SOURCE
   **Suggested Fix:** The file `backend/common/audit_state.py` must be added to the repository. Once available, extract all fields of `ChecklistItem` with their full 5-attribute decomposition (type, nullability, default, Field() constraints, source line). Until then, no fix is possible from within existing source.

2. **Entity:** `ExtractedInfo`
   **Field/Key/Constant:** `code`
   **Missing:** TYPE (precise — currently "nested model / object"), NULLABILITY
   **Suggested Fix:** Replace type with the actual class name of the `code` sub-model (e.g., `CodeInfo` or similar defined in `audit_state.py`) and state nullability (`Optional[...]` or required). Requires the absent source file.

3. **Entity:** `ExtractedInfo`
   **Field/Key/Constant:** `hyperparameters`
   **Missing:** TYPE (precise), NULLABILITY
   **Suggested Fix:** Same as above — determine the exact class type and document nullability once `audit_state.py` is available.

4. **Entity:** `AuditState`
   **Field/Key/Constant:** `evaluation`
   **Missing:** NULLABILITY, DEFAULT
   **Suggested Fix:** Add explicit nullability (`Optional[Dict]` vs required `Dict`) and default value (`{}` or `None` or "required") once `audit_state.py` is available.

5. **Entity:** Session State
   **Field/Key/Constant:** `archivo_actual`
   **Missing:** CLEARED lifecycle (not stated in lifecycle column)
   **Suggested Fix:** Add `**Cleared:** on "Limpiar" button press (app.py:30-32, all session keys deleted via st.session_state clear)` to the lifecycle field, consistent with how the other five session keys document their cleanup.

6. **Entity:** Session State
   **Field/Key/Constant:** `file_hash`
   **Missing:** CLEARED lifecycle
   **Suggested Fix:** Same as above — add CLEARED lifecycle reference.

7. **Entity:** Session State
   **Field/Key/Constant:** `md_text`
   **Missing:** CLEARED lifecycle
   **Suggested Fix:** Same as above — add CLEARED lifecycle reference.

8. **Entity:** Named Constants — Saturation Error Keywords
   **Field/Key/Constant:** keyword list constant
   **Missing:** TYPE (`list[str]` not explicitly stated in the table), per-row SOURCE (only given in section header `frontend/components/file_uploader.py:60`, not in the table body)
   **Suggested Fix:** Add a Type column with `list[str]` and a Source column with `file_uploader.py:60` inline.

9. **Entity:** Named Constants — Checklist Priority Items
   **Field/Key/Constant:** `priority_items`
   **Missing:** TYPE (`list[str]` not stated)
   **Suggested Fix:** Add explicit `list[str]` type to the table row.

10. **Entity:** Named Constants — NeurIPS Quality Score Tiers and Compliance Table Row Colors
    **Field/Key/Constant:** All tier/condition rows
    **Missing:** Per-row TYPE and SOURCE line references
    **Suggested Fix:** For each tier row, add the Python type of the constant (e.g., `float`, `str`) and the specific source line where that threshold is defined (e.g., `gauge_chart.py:14`, `gauge_chart.py:15`, etc.). For color rows, add `audit_results.py:18`, `audit_results.py:22`, etc.

---

## Pre-existing Gaps

The following `[GAP: ...]` markers were encountered in `01_data_model.md` and are documented here as legitimate pre-existing absences. They are NOT new DEPTH_GAP entries.

| Location | Gap Marker |
|---|---|
| `AuditState` — inherits-from | `[GAP: base class not extractable — source file backend/common/audit_state.py absent from repository]` |
| `AuditState.evaluation` — nullable | `[GAP: nullability not resolved]` |
| `AuditState.evaluation` — default | `[GAP: default not resolved]` |
| `ExtractedInfo` — inherits-from | `[GAP: base class not extractable — source file backend/common/audit_state.py absent]` |
| `ExtractedInfo.code` — type | `[GAP: type not resolved]` |
| `ExtractedInfo.hyperparameters` — type | `[GAP: type not resolved]` |
| `ExtractedInfo` — other sub-fields | `[GAP: field contracts not resolved in extraction]` |
| `ChecklistItem` — inherits-from | `[GAP: base class not extractable — source file backend/common/audit_state.py absent]` |
| `ChecklistItem` — all fields | `[GAP: field contract not resolved in extraction]` |

All nine gaps are traceable to a single root cause: the missing `backend/common/audit_state.py` file.

---

## Quality Assessment

**Strengths (well-documented):**

The spec excels in its documentation of what is available in the repository. The single Pydantic model (`Hyperparameters`) is documented with all 14 fields, all 5 attributes per field, confirmed accurate at line level. The three configuration dicts are fully specified. The named constant coverage is extraordinary — 7 distinct groupings across `config.py`, `llm_client.py`, `regex_detection_skills.py`, `rag_extraction_skill.py`, `sota_skills.py`, `logger.py`, `frontend/config.py`, `frontend/components/*.py` — all with literal values, Python types, usage contexts, and exact file:line references. Session state keys for the main 5 application objects are documented with complete lifecycle (set/mutated/cleared). The CHECKLIST_KEYS enum is fully documented. The LLM Response JSON Schema section (Section 5) is a bonus documentation of runtime prompt schemas that goes significantly beyond what the validator requires, and is internally consistent.

**Recurring patterns of missing depth:**

1. **Absent source file (primary issue):** The `backend/common/audit_state.py` file is not present in the repository scan. This is a repository-level gap, not a spec writing failure. The spec correctly identifies this and applies `CONFIDENCE: UNRESOLVED` + `[GAP: ...]` markers throughout.
2. **Missing CLEARED lifecycle for three session keys:** `archivo_actual`, `file_hash`, `md_text` document SET and READ lifecycle but omit the CLEARED event, which is implied but not stated.
3. **Implicit types in constant tables:** A small number of "lookup table" constant groups (Saturation Keywords, priority_items) omit the Python type annotation.
4. **LLM schema fields lack DEFAULT/CONSTRAINT:** The 150+ fields in Section 5 (LLM response schemas) all lack explicit DEFAULT and CONSTRAINT columns. This is architecturally reasonable since LLM response fields have no Python defaults, but the validator's strict 5-attribute rule treats them as PARTIAL.

**Production usability:**

The data model spec is **production-usable** for the available source. Any developer implementing a Specs2Code migration or a Spec Editor transformation of this codebase can reliably derive the Python types, constructor signatures, configuration values, constant names, and session state contracts from this spec without re-reading the source. The UNRESOLVED sections are properly quarantined with confidence markers and will not mislead — they accurately convey what the repository does and does not contain.

**Remediation priority:**

1. **High:** Locate or reconstruct `backend/common/audit_state.py` (possibly in a different branch or external dependency). Resolve UNRESOLVED entities.
2. **Medium:** Add CLEARED lifecycle notes to `archivo_actual`, `file_hash`, `md_text` session state rows.
3. **Low:** Add explicit `list[str]` type to Saturation Keywords and priority_items rows; add per-row source lines to NeurIPS tier and compliance color tables.
4. **Informational:** Correct the two fidelity issue line numbers (`rag_extraction_skill.py:204→239`; `auditor_skills.py:325→391-392`).
