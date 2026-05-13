---
validator_id: val_forward_data_model
validator_type: forward_coverage
target_specs: [01_data_model.md]
forward_coverage_pct: 99
backward_coverage_pct: N/A
depth_pct: 67
entity_completeness_pct: 50
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 2
depth_gaps: 3
spec_consistency_issues: 0
total_issues: 7
overall_status: needs_review
---

## Summary

`01_data_model.md` documents the complete Python-level data model for the Nature Auditor Pro application: 6 Pydantic/plain-Python models, 3 configuration dicts, ~70 named constants, 8 session-state keys, 16 CHECKLIST_KEYS, and 7 LLM response JSON schemas with full sub-schema decomposition. **Forward coverage is excellent at 99%**: every spec claim that cites a source file was opened and verified, with only 2 stale line-number references found (content correct in both cases). **Depth gaps are entirely due to a missing source file** (`backend/common/audit_state.py` is absent from the repository), which the spec correctly documents with `[GAP:]` markers and UNRESOLVED flags — this is proper practice, not a spec authoring error. Two minor coverage gaps exist: the `CHECKLIST_LABELS` constant and the `NEGATION_PATTERNS` compiled regex are present in source but absent from the spec. Overall status is **needs_review** due to the unavoidable depth gaps and entity_completeness_pct impact from the absent source file; the production-quality portion of the spec (all resolvable entities) is fully accurate.

---

## Forward Coverage (Specs → Source)

### Pydantic / Dataclass Models

| Spec Element | Element Type | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `Hyperparameters.thought_process` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Field and Field() description match exactly |
| `Hyperparameters.learning_rate` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 13 |
| `Hyperparameters.batch_size` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 14 |
| `Hyperparameters.epochs` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 15 |
| `Hyperparameters.optimizer` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 16 |
| `Hyperparameters.warmup_steps` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 17 |
| `Hyperparameters.weight_decay` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 18 |
| `Hyperparameters.random_seed` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 19 |
| `Hyperparameters.betas` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 20 |
| `Hyperparameters.epsilon` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 21 |
| `Hyperparameters.training_steps` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 22 |
| `Hyperparameters.total_tokens` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 23 |
| `Hyperparameters.hardware` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 24 |
| `Hyperparameters.latency_metrics` | model_field | `rag_extraction_skill.py:11` | Yes | VERIFIED | Confirmed at line 25 |
| `AuditState.paper_text` | model_field | `tests/test_audit_state.py:6` | Inferred | UNRESOLVED | Source file `backend/common/audit_state.py` absent; inferred from test — [GAP:] correctly marked in spec |
| `AuditState.invalid_paper` | model_field | `tests/test_audit_state.py:9` | Inferred | UNRESOLVED | Same caveat |
| `AuditState.execution_time` | model_field | `tests/test_audit_state.py:10` | Inferred | UNRESOLVED | Same caveat |
| `AuditState.evaluation` | model_field | `tests/test_audit_state.py:13` | Inferred | UNRESOLVED | Same caveat |
| `ExtractedInfo.code` | model_field | `tests/test_audit_state.py:22` | Inferred | UNRESOLVED | Source absent |
| `ExtractedInfo.hyperparameters` | model_field | `tests/test_audit_state.py:23` | Inferred | UNRESOLVED | Source absent |
| `ChecklistItem` (all fields) | model_field | `tests/test_audit_state.py` | No | UNRESOLVED | [GAP:] marker in spec; source absent |
| `BaseSkill.llm_client` | model_field | `base_skill.py:19` | Yes | VERIFIED | Line 19: `def __init__(self, llm_client: Optional[LLMClient] = None, ...)`; stored at line 28 |
| `BaseSkill.config` | model_field | `base_skill.py:19` | Yes | VERIFIED | `config = config or {}` at line 29; default `{}` verified |
| `BaseSkill.name` | model_field | `base_skill.py:19` | Yes | VERIFIED | `self.name = self.__class__.__name__` at line 30 |
| `BaseSkill.execute` (abstract method) | model_field | `base_skill.py:34` | Yes | VERIFIED | `@abstractmethod` + `def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:` at line 34 |
| `CompositeSkill.skills` | model_field | `base_skill.py:91` | Yes | VERIFIED | `def __init__(self, skills: list[BaseSkill], ...)` at line 91; `self.skills = skills` at line 100 |
| `CompositeSkill.llm_client` | model_field | `base_skill.py:91` | Yes | VERIFIED | `llm_client: Optional[LLMClient] = None` at line 91 |
| `CompositeSkill.name` | model_field | `base_skill.py:19` | Yes | VERIFIED | Inherited from BaseSkill.__init__; value `"CompositeSkill"` at runtime |
| `CompositeSkill.config` | model_field | `base_skill.py:19` | Yes | VERIFIED | Inherited from BaseSkill.__init__ |

### Configuration Dicts

| Spec Element | Element Type | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `AUDIT_CONFIG.response_mime_type` | config_key | `config.py:116` | Yes | VERIFIED | `"application/json"` at line 117 |
| `AUDIT_CONFIG.temperature` | config_key | `config.py:116` | Yes | VERIFIED | `AUDIT_TEMPERATURE` (0.0) at line 118 |
| `AUDIT_CONFIG.top_k` | config_key | `config.py:116` | Yes | VERIFIED | `1` at line 119 |
| `AUDIT_CONFIG.top_p` | config_key | `config.py:116` | Yes | VERIFIED | `0.1` at line 120 |
| `AUDIT_CONFIG.max_output_tokens` | config_key | `config.py:116` | Yes | VERIFIED | `16384` at line 121 |
| `CHAT_CONFIG.temperature` | config_key | `config.py:125` | Yes | VERIFIED | `CHAT_TEMPERATURE` (0.2) at line 126 |
| `SOTA_CONFIG.response_mime_type` | config_key | `config.py:130` | Yes | VERIFIED | `"application/json"` at line 131 |
| `SOTA_CONFIG.temperature` | config_key | `config.py:130` | Yes | VERIFIED | `SOTA_TEMPERATURE` (0.1) at line 132 |

### Named Constants

| Spec Element | Element Type | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `GOOGLE_API_KEY` | named_constant | `config.py:30` | Yes | VERIFIED | `os.getenv("GOOGLE_API_KEY")` at line 30 |
| `SEMANTIC_SCHOLAR_API_KEY` | named_constant | `config.py:31` | Yes | VERIFIED | `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` at line 31 |
| `EMBEDDING_MODEL_NAME` | named_constant | `config.py:35` | Yes | VERIFIED | `"gemini-embedding-2"` at line 35 |
| `MAP_MODEL_NAME` | named_constant | `config.py:37` | Yes | VERIFIED | `"gemini-3.1-flash-lite-preview"` at line 37 |
| `REDUCE_MODEL_NAME` | named_constant | `config.py:39` | Yes | VERIFIED | `"gemini-3.1-flash-lite-preview"` at line 39 |
| `EXTRACTION_MODEL_NAME` | named_constant | `config.py:41` | Yes | VERIFIED | `"gemini-3.1-flash-lite-preview"` at line 41 |
| `EVALUATION_MODEL_NAME` | named_constant | `config.py:43` | Yes | VERIFIED | `"gemini-3.1-flash-lite-preview"` at line 43 |
| `VERIFICATION_MODEL_NAME` | named_constant | `config.py:45` | Yes | VERIFIED | `"gemini-3.1-flash-lite-preview"` at line 45 |
| `MODEL_NAME` | named_constant | `config.py:107` | Yes | VERIFIED | `= EXTRACTION_MODEL_NAME` at line 107 |
| `RAG_MODEL_NAME` | named_constant | `config.py:108` | Yes | VERIFIED | `= MAP_MODEL_NAME` at line 108 |
| `AUDIT_TEMPERATURE` | named_constant | `config.py:111` | Yes | VERIFIED | `0.0` at line 111 |
| `CHAT_TEMPERATURE` | named_constant | `config.py:112` | Yes | VERIFIED | `0.2` at line 112 |
| `SOTA_TEMPERATURE` | named_constant | `config.py:113` | Yes | VERIFIED | `0.1` at line 113 |
| `SEMANTIC_SCHOLAR_BASE_URL` | named_constant | `config.py:136` | Yes | VERIFIED | Correct URL at line 136 |
| `SEMANTIC_SCHOLAR_YEAR_RANGE` | named_constant | `config.py:137` | Yes | VERIFIED | `"2023-2026"` at line 137 |
| `SEMANTIC_SCHOLAR_LIMIT` | named_constant | `config.py:138` | Yes | VERIFIED | `5` at line 138 |
| `SEMANTIC_SCHOLAR_FIELDS` | named_constant | `config.py:139` | Yes | VERIFIED | Full fields string at line 139 |
| `max_retries` (LLM retry) | named_constant | `llm_client.py:39` | Yes | VERIFIED | `max_retries = 5` at line 39 |
| `base_delay` (LLM retry) | named_constant | `llm_client.py:40` | Yes | VERIFIED | `base_delay = 2` at line 40 |
| Retryable codes `"503","429","UNAVAILABLE","RESOURCE_EXHAUSTED","DEADLINE_EXCEEDED"` | named_constant | `llm_client.py:54` | Yes | VERIFIED | `any(code in error_msg.upper() for code in [...])` at line 54 |
| `chunk_size` (PDF parser) | named_constant | `pdf_parser.py:51` | Yes | VERIFIED | `chunk_size = 5` at line 51 |
| `Colors.BLUE` | named_constant | `logger.py:7` | Yes | VERIFIED | `"\033[94m"` at line 7 |
| `Colors.CYAN` | named_constant | `logger.py:8` | Yes | VERIFIED | `"\033[96m"` at line 8 |
| `Colors.GREEN` | named_constant | `logger.py:9` | Yes | VERIFIED | `"\033[92m"` at line 9 |
| `Colors.YELLOW` | named_constant | `logger.py:10` | Yes | VERIFIED | `"\033[93m"` at line 10 |
| `Colors.RED` | named_constant | `logger.py:11` | Yes | VERIFIED | `"\033[91m"` at line 11 |
| `Colors.MAGENTA` | named_constant | `logger.py:12` | Yes | VERIFIED | `"\033[95m"` at line 12 |
| `Colors.BOLD` | named_constant | `logger.py:13` | Yes | VERIFIED | `"\033[1m"` at line 13 |
| `Colors.RESET` | named_constant | `logger.py:14` | Yes | VERIFIED | `"\033[0m"` at line 14 |
| Log-level color map (5 entries) | named_constant | `logger.py:22-26` | Yes | VERIFIED | `LEVEL_COLORS` dict matches spec exactly at lines 22-26 |
| `NEGATION_WINDOW` | named_constant | `regex_detection_skills.py:8` | Yes | VERIFIED | `NEGATION_WINDOW = 60` at line 8 |
| RAG `batch_size = 15` | named_constant | `rag_extraction_skill.py:61` | Yes | VERIFIED | Inline `batch_size = 15` at line 61 |
| RAG inter-batch sleep 15s | named_constant | `rag_extraction_skill.py:67` | Yes | VERIFIED | `time.sleep(15)` at line 67 |
| RAG inter-chunk sleep 1s | named_constant | `rag_extraction_skill.py:199` | Yes | VERIFIED | `time.sleep(1)` at line 199 |
| RAG `n_results=10` | named_constant | `rag_extraction_skill.py:123` | Yes | VERIFIED | `n_results=10` at line 123 |
| RAG query count 13 | named_constant | `rag_extraction_skill.py:99` | Yes | VERIFIED | List starting at line 99 contains exactly 13 query strings |
| MAP fragment inter-sleep 2s | named_constant | `auditor_skills.py:104` | Yes | VERIFIED | `time.sleep(2)` at line 105 (condition at line 104) |
| RAG distance formula | named_constant | `rag_extraction_skill.py:127` | **No** | **FIDELITY_ISSUE** | Spec cites line 127; actual code at lines 152–157. Line 127 is `chunk_relevance = {}` — unrelated. Formula itself is correct. |
| Semantic Scholar rate-limit sleep 2s | named_constant | `sota_skills.py:217` | Yes | VERIFIED | `time.sleep(2)` at line 217 |
| Semantic Scholar inter-query sleep 0.5s | named_constant | `sota_skills.py:191` | Yes | VERIFIED | `time.sleep(0.5)` at line 191 |
| Semantic Scholar API timeout 15s | named_constant | `sota_skills.py:207` | Yes | VERIFIED | `timeout=15` at line 206 (off by 1; within ±10 lines) |
| Semantic Scholar top-N = 10 | named_constant | `sota_skills.py:232` | Yes | VERIFIED | `sorted_papers[:10]` at line 232 |
| CrossValidation max papers 5 | named_constant | `sota_skills.py:379` | Yes | VERIFIED | Prompt text "Selecciona hasta 5 papers omitidos" at line 380 |
| `priority_items` (checklist verification) | named_constant | `auditor_skills.py:340` | Yes | VERIFIED | List of 8 keys at lines 340-343; matches spec exactly |
| `TITLE` | named_constant | `frontend/config.py:3` | Yes | VERIFIED | `"💻 Auditor de Papers en Ciencias de la Computación"` at line 3 |
| `SIDEBAR_IMAGE` | named_constant | `frontend/config.py:4` | Yes | VERIFIED | ACM logo URL at line 4 |
| `SIDEBAR_DESCRIPTION` | named_constant | `frontend/config.py:5` | Yes | VERIFIED | Exact string at line 5 |
| Saturation error keywords list | named_constant | `frontend/components/file_uploader.py:60` | Yes | VERIFIED | `["503","UNAVAILABLE","SATURAD","DEMAND","QUOTA","LIMIT"]` at line 60 |
| NeurIPS quality tiers (6 tiers + threshold) | named_constant | `gauge_chart.py:14-31,57-61` | Yes | VERIFIED | All 6 tiers, labels, hex colors, and threshold value 62.5 verified |
| Compliance row colors (4 conditions) | named_constant | `audit_results.py:18-32` | Yes | VERIFIED | `#450a0a`, `#452e0a`, `#064e3b`, `#111827` at lines 21,25,29,32 |
| Env var suppressions (8 operations) | named_constant | `config.py:8-25` | Yes | VERIFIED | All 8 env/log ops confirmed at lines 8-25 |

### Session State Schema

| Spec Element | Element Type | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `resultado` | session_key | `session_state.py:7` | Yes | VERIFIED | Spec cites line 7 (function def); actual initialization at lines 9-10. Content correct: default `None`. Off-by-2 is within function scope. |
| `auditor` | session_key | `session_state.py:12-13` | Yes | VERIFIED | `PaperAuditor()` instance at lines 12-13 |
| `chatbot` | session_key | `session_state.py:15-16` | Yes | VERIFIED | `PaperChatbot()` instance at lines 15-16 |
| `sota_analyzer` | session_key | `session_state.py:18-19` | Yes | VERIFIED | `SotaAnalyzer()` instance at lines 18-19 |
| `messages` | session_key | `session_state.py:21-22` | Yes | VERIFIED | `[]` default at lines 21-22 |
| `archivo_actual` | session_key | `file_uploader.py:19` | Yes | VERIFIED | `st.session_state.archivo_actual = uploaded_file.name` at line 19 |
| `file_hash` | session_key | `file_uploader.py:20` | Yes | VERIFIED | `st.session_state.file_hash = file_hash` at line 20 |
| `md_text` | session_key | `file_uploader.py:36-39` | Yes | VERIFIED | Set at line 36 (PDF) or 39 (TXT/MD) |

### CHECKLIST_KEYS and Checklist Sub-schemas

| Spec Element | Element Type | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| All 16 CHECKLIST_KEYS | named_constant | `scoring.py:8-15` (spec); actual `scoring.py:8-14` | Yes | VERIFIED | `["claims","limitations",...]` 16 items confirmed |
| Checklist answer values (`"Yes"`,`"No"`,`"N/A"`) | named_constant | `prompts.py:378` | Yes | VERIFIED | Eval prompt at line 378; `"answer" MUST be exactly one of: "Yes", "No", or "N/A"` |
| Checklist item `answer` sub-field | llm_schema_field | `prompts.py:378` | Yes | VERIFIED | Confirmed in prompt JSON schema |
| Checklist item `evidence` sub-field | llm_schema_field | `prompts.py:378` | Yes | VERIFIED | Confirmed |
| Checklist item `justification` sub-field | llm_schema_field | `prompts.py:378` | Yes | VERIFIED | Confirmed |
| Checklist item `is_no_justified` sub-field | llm_schema_field | `prompts.py:378` | Yes | VERIFIED | Confirmed |
| Post-verification `verified` field | llm_schema_field | `auditor_skills.py:325` | **No** | **FIDELITY_ISSUE** | Spec cites line 325 (`def execute` signature); actual assignment `"verified": True` at line 391. Off by 66 lines. Content correct. |
| Post-verification `was_refined` field | llm_schema_field | `auditor_skills.py:325` | **No** | **FIDELITY_ISSUE** | Same issue — `"was_refined": not verification_result.get('was_corrected', False)` at line 392. Logic confirmed correct. |

### LLM Response JSON Schemas

| Spec Element | Element Type | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `get_extraction_prompt` → 13 top-level fields | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Function def at line 4; prompt at lines 21–181; all 13 keys present |
| `code` sub-schema (5 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Keys: repository_url, negative_phrase, dependencies, instructions, release_mention |
| `data` sub-schema (6 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Keys: dataset_name, access_url, negative_phrase, preprocessing, splits, release_mention |
| `hyperparameters` sub-schema (12 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed in extraction prompt JSON structure |
| `hardware` sub-schema (9 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `statistics` sub-schema (3 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `architecture` sub-schema (3 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `baseline_comparison` sub-schema (4 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `software_versions` sub-schema (4 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `limitations_quality` sub-schema (3 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `theory_and_proofs` sub-schema (4 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `broader_impacts_extraction` sub-schema (3 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `llm_usage_extraction` sub-schema (4 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `human_subjects_extraction` sub-schema (3 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `licenses_extraction` sub-schema (3 fields) | llm_schema_field | `prompts.py:4` | Yes | VERIFIED | Confirmed |
| `get_map_extraction_prompt` → 18 fields | llm_schema_field | `prompts.py:184` | Yes | VERIFIED | Function at line 184; all 18 keys listed in prompt structure |
| `get_reduce_extraction_prompt` → same schema | llm_schema_field | `prompts.py:228` | Yes | VERIFIED | Function at line 228; spec correctly notes it consolidates to same canonical schema |
| `get_evaluation_prompt` → 16 checklist item keys | llm_schema_field | `prompts.py:378` | Yes | VERIFIED | Function at line 378; 16 keys in prompt output JSON at lines 420-490 |
| `get_evaluation_prompt` → item sub-schema (4 fields) | llm_schema_field | `prompts.py:378` | Yes | VERIFIED | answer, evidence, justification, is_no_justified confirmed |
| `get_verification_prompt` → 5 fields | llm_schema_field | `prompts.py:494` | Yes | VERIFIED | Function at line 494; JSON schema at lines 532-538: answer, evidence, justification, is_no_justified, was_corrected |
| `get_evaluation_signals` → 6 fields | llm_schema_field | `prompts.py:273` | Yes | VERIFIED | Function at line 273; returns reproducibility, open_access, statistics, compute_resource, licenses, crowdsourcing |
| `resultado` virtual schema (25 keys) | llm_schema_field | `auditor_skills.py:285` | Yes | VERIFIED | MetadataAggregationSkill.execute at line 285; all 23 core keys confirmed at lines 290-313; extracted_hyperparameters_hybrid and original_extraction_raw confirmed at auditor.py:192-195 |
| `metricas` sub-schema (3 keys) | llm_schema_field | `auditor_skills.py:256` | Yes | VERIFIED | MetricsCalculationSkill.execute at line 256; tiempo_segundos, caracteres_leidos, red_flags_detectadas confirmed at lines 272-275 |
| Error path dicts (4 variants) | llm_schema_field | `auditor.py:91,109-113,161,201` | Yes | VERIFIED | All 4 error return forms confirmed in source |

---

## Depth Validation

| Spec Element | Element Type | Has Structured Decomposition | Detail Level | Missing |
|---|---|---|---|---|
| `Hyperparameters` | Pydantic model | Yes — 14 fields with Field() descriptions and sentinel contract | FULL | Nothing |
| `AuditState` | Python class | Partially — 4 fields from test inference, nullability/types have [GAP:] | PARTIAL | Full type annotations, nullability, all remaining fields (source file absent) |
| `ExtractedInfo` | Python class | Partially — 2 fields from test inference, types listed as "nested model / object" | PARTIAL | Concrete types for `code` and `hyperparameters` sub-objects (source file absent) |
| `ChecklistItem` | Python class | No — no field contracts at all; only GAP marker | NAME_ONLY | All field contracts (source file absent) |
| `BaseSkill` | ABC class | Yes — 3 fields with types, nullability, defaults, and abstract method | FULL | Nothing |
| `CompositeSkill` | Python class | Yes — 4 fields with types, nullability, defaults, and error accumulation contract | FULL | Nothing |

---

## Fidelity Issues

### Issue 1: RAG Distance Formula — Stale Line Reference

- **Spec claim:** "RAG distance → relevance score formula — Source: `rag_extraction_skill.py:127`"
- **Source reference attempted:** Opened `rag_extraction_skill.py`, navigated to line 127
- **What was actually found at line 127:** `chunk_relevance = {}` — the start of the chunk-deduplication dict, entirely unrelated to the distance-to-score formula
- **Where the declaration actually is:** Lines 152–157 contain the actual if/elif/else block:
  ```python
  if distance < 0.4:
      relevance_score = int(95 - (distance * 25))
  elif distance < 0.7:
      relevance_score = int(85 - ((distance - 0.4) * 180))
  else:
      relevance_score = max(5, int(31 - ((distance - 0.7) * 50)))
  ```
- **Content accuracy:** The formula values stated in the spec (`int(95 - (distance * 25))`, etc.) are **correct** — only the line citation is stale.
- **Recommended fix:** Change `rag_extraction_skill.py:127` → `rag_extraction_skill.py:152` in the spec.

---

### Issue 2: `verified` / `was_refined` Fields — Stale Line Reference

- **Spec claim:** "`verified` and `was_refined` are added by `ChecklistVerificationSkill` — Source: `auditor_skills.py:325`"
- **Source reference attempted:** Opened `auditor_skills.py`, navigated to line 325
- **What was actually found at line 325:** `def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:` — the method signature of `ChecklistVerificationSkill.execute`, not the field assignments
- **Where the declaration actually is:** Lines 391–392:
  ```python
  "verified": True,
  "was_refined": not verification_result.get('was_corrected', False)
  ```
- **Content accuracy:** The semantic meaning is **correct** — `verified` is always `True`; `was_refined` is `True` if NOT corrected.
- **Recommended fix:** Change `auditor_skills.py:325` → `auditor_skills.py:391` in the spec.

---

## Coverage Gaps

Source files/entities found in source code but not represented in `01_data_model.md`:

| Source File | LOC | Missing Entity/Constant | Notes |
|---|---|---|---|
| `frontend/utils/scoring.py` | 113 | `CHECKLIST_LABELS` dict | 16-entry dict mapping checklist keys to display strings (e.g., `"claims"` → `"1. Claims"`). Present at line 17. Used in UI rendering via `CHECKLIST_LABELS.get(key, key)` at line 112. Not a session-state or LLM schema item, but is a notable named constant of the data model. |
| `backend/skills/regex_detection_skills.py` | 542 | `NEGATION_PATTERNS` compiled regex | Module-level `re.compile(...)` at line 10 defining a multilingual negation detection pattern. Used alongside `NEGATION_WINDOW` in all regex detection skill classes but not documented in the spec. Minor omission given the scope of the spec. |

---

## Depth Gaps

| Spec Element | Current Detail Level | What Is Missing |
|---|---|---|
| `AuditState` | PARTIAL — 4 fields inferred from test assertions | Full type annotations (especially for `evaluation` dict value types), nullability for `evaluation`, default value for `evaluation`, all other fields beyond the 4 tested (source file `backend/common/audit_state.py` is absent from the repository) |
| `ExtractedInfo` | PARTIAL — 2 top-level fields (`code`, `hyperparameters`) inferred | Concrete Python types for `code` and `hyperparameters` sub-objects; all other sub-fields beyond `repository_url` and `optimizer` defaults; base class (source absent) |
| `ChecklistItem` | NAME_ONLY — class name only, no field contracts | All field names, types, defaults, and constraints (source absent) |

**Note:** All three depth gaps are caused by the same root issue — `backend/common/audit_state.py` does not exist in the repository. The spec correctly acknowledges this with `[GAP:]` and UNRESOLVED markers and cites test assertions as secondary evidence. This is responsible extraction practice, not a spec quality failure.

---

## Quality Assessment

**What the spec gets right (significant strengths):**

1. **Pydantic model coverage is production-quality.** The `Hyperparameters` model is documented with all 14 fields, exact Field() description text, the sentinel string contract (`"NOT FOUND"`), the post-processing type-coercion rules, and usage context — more than enough for a modernization effort.

2. **Configuration and constants are exhaustive.** All three config dicts (AUDIT_CONFIG, CHAT_CONFIG, SOTA_CONFIG) with exact key-value pairs, all 8 model name constants, temperature values, Semantic Scholar API constants, retry constants, PDF chunking constants, Colors class — every numeric constant that flows through the pipeline is present and verified accurate.

3. **LLM JSON schemas are a standout.** The full nested extraction schema (13 top-level fields + 14 sub-schemas with 66 sub-fields), the MAP/REDUCE schemas, the evaluation schema, the verification schema, and the evaluation_signals dict are all fully documented with field names, types, nullable status, and usage semantics. This is exceptionally valuable for modernization.

4. **Session state schema is complete.** All 8 session keys documented with lifecycle tracking (when set, read, cleared), initial values, and source citations — sufficient to recreate the state management layer.

5. **Missing file handling is exemplary.** The spec does not fabricate content for the absent `backend/common/audit_state.py`. Instead it marks entities as UNRESOLVED with clear provenance from test assertions, and documents exactly what is inferrable vs. what is unknown.

**What needs improvement:**

1. **Two stale line references** (RAG distance formula and `verified`/`was_refined` fields). Both point to the correct source file and the content is accurate, but the line numbers are off by 25 and 66 lines respectively. These should be corrected to lines 152 and 391 respectively.

2. **`CHECKLIST_LABELS` is undocumented.** This constant maps the 16 checklist keys to their NeurIPS display strings and is used in UI rendering. While not critical, a modernization team rebuilding the audit results view would need it.

3. **`NEGATION_PATTERNS` is undocumented.** This compiled multilingual negation regex is a key part of the negation-aware detection logic but is not mentioned in the spec.

**Production-readiness verdict:** The spec is production-ready for modernizing the `Hyperparameters` extraction, all 5 LLM prompt pipelines, the session state management layer, and the configuration system. The only gap material to a modernization effort is the `AuditState`/`ExtractedInfo`/`ChecklistItem` absence — but this is a repository-level gap (missing source file) that cannot be resolved from spec alone and is correctly flagged. Any team modernizing this application will need to discover these three data types through the test suite (the spec provides the correct pointers).
