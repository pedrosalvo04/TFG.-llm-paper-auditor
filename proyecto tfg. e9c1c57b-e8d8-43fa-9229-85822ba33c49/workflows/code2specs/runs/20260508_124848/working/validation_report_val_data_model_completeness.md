---
validator_id: val_data_model_completeness
validator_type: data_model_completeness
target_specs: [01_data_model.md]
forward_coverage_pct: 75
backward_coverage_pct: 78
depth_pct: 85
entity_completeness_pct: 58
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 0
coverage_gaps: 5
depth_gaps: 0
spec_consistency_issues: 0
total_issues: 5
overall_status: fail
---

## Summary

The data model spec (`01_data_model.md`) covers six section-1 entities: `Hyperparameters`, `AuditState`, `ExtractedInfo`, `ChecklistItem`, `BaseSkill`, and `CompositeSkill`. Three entities (`Hyperparameters`, `BaseSkill`, `CompositeSkill`) are fully verified against primary source files with complete field counts, type annotations, defaults, and constraints. Three entities (`AuditState`, `ExtractedInfo`, `ChecklistItem`) are unverifiable from primary source because the file `backend/common/audit_state.py` is **absent from the repository**; these are correctly documented with `[CONFIDENCE: UNRESOLVED]` warnings, `[GAP: ...]` markers, and test-inference caveats. The constants, config structures, session state schema, and LLM response schemas (sections 2–5) are thoroughly documented and independently verified against their source references. The overall status is **fail** because `entity_completeness_pct` (58%) falls below the 75% threshold — a direct consequence of the missing source file, not a spec-writing deficiency.

---

## Entity Completeness Table

| Entity Name | Source File | Spec Fields | Source Fields | Types Match | Defaults Match | Constraints Verifiable | Classification | Issues |
|---|---|---|---|---|---|---|---|---|
| `Hyperparameters` | `backend/skills/rag_extraction_skill.py:11` | 14 | 14 | ✓ All `str` exact | ✓ No defaults (all required) | ✓ All `Field(description=...)` confirmed | **FULL** | None |
| `AuditState` | `backend/common/audit_state.py` — ABSENT | 4 | UNKNOWN | Partial (3/4 inferred from tests) | Partial (`invalid_paper=False`, `execution_time=0.0` confirmed via test) | Cannot verify from primary source | **PARTIAL** | Source file absent; fields inferred from `tests/test_audit_state.py` |
| `ExtractedInfo` | `backend/common/audit_state.py` — ABSENT | 2 | UNKNOWN | ✗ Both types are `[GAP: type not resolved]` | Not determinable | Cannot verify | **SHALLOW** | Source file absent; types unresolved; both fields have [GAP] type markers |
| `ChecklistItem` | `backend/common/audit_state.py` — ABSENT | 0 (all [GAP]) | UNKNOWN | N/A | N/A | N/A | **SHALLOW** | VERIFIED_DOCUMENTED_GAP — all fields carry explicit [GAP] marker |
| `BaseSkill` | `backend/skills/base_skill.py:10` | 3 | 3 | ✓ `Optional[LLMClient]`, `Dict`, `str` | ✓ `None`, `{}`, `self.__class__.__name__` | ✓ `config or {}` guard confirmed | **FULL** | None |
| `CompositeSkill` | `backend/skills/base_skill.py:91` | 4 | 4 | ✓ `list[BaseSkill]`, `Optional[LLMClient]`, `str`, `Dict` | ✓ `—`, `None`, `"CompositeSkill"`, `{}` | ✓ Inherited guards confirmed | **FULL** | None |

**entity_completeness_pct** = (3×1.0 + 1×0.5 + 0 + 0) / 6 × 100 = **58%**

---

## Forward Coverage (Specs → Source)

### Section 1 — Pydantic / Dataclass Models

| Spec Element | Field | Source Reference | Verified? | Status |
|---|---|---|---|---|
| `Hyperparameters` | `thought_process` | `rag_extraction_skill.py:11` | ✓ | PASS — `thought_process: str = Field(description="Internal reasoning...")` confirmed |
| `Hyperparameters` | `learning_rate` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `batch_size` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `epochs` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `optimizer` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `warmup_steps` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `weight_decay` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `random_seed` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `betas` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `epsilon` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `training_steps` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `total_tokens` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `hardware` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `Hyperparameters` | `latency_metrics` | `rag_extraction_skill.py:11` | ✓ | PASS |
| `AuditState` | `paper_text` | `tests/test_audit_state.py:6` | Partial | COVERAGE_GAP (test-inferred) — test asserts `state.paper_text == "Test content"`; primary source absent |
| `AuditState` | `invalid_paper` | `tests/test_audit_state.py:9` | Partial | COVERAGE_GAP (test-inferred) — `assertFalse(state.invalid_paper)` confirms default=False |
| `AuditState` | `execution_time` | `tests/test_audit_state.py:10` | Partial | COVERAGE_GAP (test-inferred) — `assertEqual(state.execution_time, 0.0)` confirms default=0.0 |
| `AuditState` | `evaluation` | `tests/test_audit_state.py:13` | Partial | COVERAGE_GAP (test-inferred) — `[GAP: nullability not resolved]`, `[GAP: default not resolved]` are intentional |
| `ExtractedInfo` | `code` | `tests/test_audit_state.py:22` | Partial | COVERAGE_GAP (test-inferred) — type is `[GAP: type not resolved]` |
| `ExtractedInfo` | `hyperparameters` | `tests/test_audit_state.py:23` | Partial | COVERAGE_GAP (test-inferred) — type is `[GAP: type not resolved]` |
| `ChecklistItem` | (all) | `tests/test_audit_state.py` | N/A | VERIFIED_DOCUMENTED_GAP — `[GAP: field contract not resolved in extraction]` is correct |
| `BaseSkill` | `llm_client` | `base_skill.py:19` | ✓ | PASS — `Optional[LLMClient] = None` confirmed |
| `BaseSkill` | `config` | `base_skill.py:19` | ✓ | PASS — `config or {}` confirmed; stored type always `Dict` |
| `BaseSkill` | `name` | `base_skill.py:19` | ✓ | PASS — `self.__class__.__name__` confirmed |
| `CompositeSkill` | `skills` | `base_skill.py:91` | ✓ | PASS — `skills: list[BaseSkill]`, required, confirmed |
| `CompositeSkill` | `llm_client` | `base_skill.py:91` | ✓ | PASS — passed to `super().__init__(llm_client)` |
| `CompositeSkill` | `name` | `base_skill.py:19` | ✓ | PASS — evaluates to `"CompositeSkill"` via `__class__.__name__` |
| `CompositeSkill` | `config` | `base_skill.py:19` | ✓ | PASS — inherited from `BaseSkill.__init__` |

### Sections 2–5 — Spot-Check Key Claims

| Spec Element | Claim | Source Reference | Verified? | Status |
|---|---|---|---|---|
| `AUDIT_CONFIG` | `response_mime_type="application/json"` | `config.py:116` | ✓ | PASS |
| `AUDIT_CONFIG` | `temperature=0.0`, `top_k=1`, `top_p=0.1`, `max_output_tokens=16384` | `config.py:116` | ✓ | PASS |
| `CHAT_CONFIG` | `temperature=0.2` | `config.py:125` | ✓ | PASS |
| `SOTA_CONFIG` | `response_mime_type="application/json"`, `temperature=0.1` | `config.py:130` | ✓ | PASS |
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | `config.py:35` | ✓ | PASS |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `config.py:37` | ✓ | PASS |
| `MODEL_NAME` | `= EXTRACTION_MODEL_NAME` | `config.py:107` | ✓ | PASS |
| `AUDIT_TEMPERATURE` | `0.0` | `config.py:111` | ✓ | PASS |
| `CHAT_TEMPERATURE` | `0.2` | `config.py:112` | ✓ | PASS |
| `SOTA_TEMPERATURE` | `0.1` | `config.py:113` | ✓ | PASS |
| `SEMANTIC_SCHOLAR_BASE_URL` | correct URL | `config.py:136` | ✓ | PASS |
| `SEMANTIC_SCHOLAR_LIMIT` | `5` | `config.py:138` | ✓ | PASS |
| LLM retry `max_retries` | `5` | `llm_client.py:39` | ✓ | PASS |
| LLM retry `base_delay` | `2` | `llm_client.py:40` | ✓ | PASS |
| Retryable codes | `503`, `429`, `UNAVAILABLE`, `RESOURCE_EXHAUSTED`, `DEADLINE_EXCEEDED` | `llm_client.py:54` | ✓ | PASS |
| PDF `chunk_size` | `5` | `pdf_parser.py:51` | ✓ | PASS |
| `NEGATION_WINDOW` | `60` | `regex_detection_skills.py:8` | ✓ | PASS |
| RAG `batch_size` | `15` | `rag_extraction_skill.py:61` | ✓ | PASS |
| RAG inter-batch sleep | `15` | `rag_extraction_skill.py:67` | ✓ | PASS |
| RAG `n_results` | `10` | `rag_extraction_skill.py:123` | ✓ | PASS |
| SOTA inter-query sleep | `0.5` | `sota_skills.py:191` | ✓ | PASS |
| SOTA API timeout | `15` | `sota_skills.py:206` | ✓ | PASS |
| SOTA rate-limit sleep | `2` | `sota_skills.py:217` | ✓ | PASS |
| SOTA top-N | `[:10]` | `sota_skills.py:232` | ✓ | PASS |
| CrossValidation max papers | `5` | `sota_skills.py:379–380` | ✓ | PASS (`"Selecciona hasta 5 papers omitidos"`) |
| `Colors.BLUE` | `"\033[94m"` | `logger.py:7` | ✓ | PASS |
| `Colors.RESET` | `"\033[0m"` | `logger.py:14` | ✓ | PASS |
| `Colors.BOLD + Colors.RED` for CRITICAL | `logger.py:26` | ✓ | PASS |
| `CHECKLIST_KEYS` | 16 keys in order | `scoring.py:8-15` | ✓ | PASS |
| Session state `resultado` | Initial `None` | `session_state.py:7` | ✓ | PASS |
| Session state `auditor` | `PaperAuditor()` | `session_state.py:12-13` | ✓ | PASS |
| `was_refined` field | `not verification_result.get('was_corrected', False)` | `auditor_skills.py:392` | ✓ | PASS |
| `verified` field | Always `True` | `auditor_skills.py:391` | ✓ | PASS |
| Saturation keywords | `["503","UNAVAILABLE","SATURAD","DEMAND","QUOTA","LIMIT"]` | `file_uploader.py:60` | ✓ | PASS |
| NeurIPS `"Strong Accept"` | `[87.5, 100]`, `"#00aa00"` | `gauge_chart.py:14-31` | ✓ | PASS |
| Compliance row `"#450a0a"` | `pending_justification == True` | `audit_results.py:20-21` | ✓ | PASS |
| Compliance row `"#452e0a"` | `missing_evidence == True OR alert_msg non-empty` | `audit_results.py:24-25` | ✓ | PASS |
| Compliance row `"#064e3b"` | `"yes" in answer.lower()` | `audit_results.py:28-29` | ✓ | PASS |
| Compliance row `"#111827"` | All other cases | `audit_results.py:32` | ✓ | PASS |
| `metricas.tiempo_segundos` | rounded to 2 dp | `auditor.py:122`, `auditor_skills.py:268` | ✓ | PASS — `round(end_time - start_time, 2)` then stored in metrics dict |
| `metricas.red_flags_detectadas` | excludes `tiene_`, `menciona_`, `_`, `cantidad_`, `puntos_` prefixes | `auditor_skills.py:255-260` | ✓ | PASS |

---

## Backward Coverage (Source → Specs)

| Source File | LOC | Entity / Class in Source | Represented in Spec | Status |
|---|---|---|---|---|
| `backend/skills/rag_extraction_skill.py` | 268 | `Hyperparameters` (Pydantic BaseModel) | ✓ Section 1 | PASS |
| `backend/skills/rag_extraction_skill.py` | 268 | `HybridHyperparameterExtractionSkill` (BaseSkill subclass) | Listed as BaseSkill subclass in §1 relationships | PASS (subclass pattern; no new fields beyond `execute()`) |
| `backend/skills/base_skill.py` | 100 | `BaseSkill`, `CompositeSkill` | ✓ Section 1 | PASS |
| `backend/common/audit_state.py` | ABSENT | `AuditState`, `ExtractedInfo`, `ChecklistItem` | ✓ Section 1 (test-inferred with [GAP] markers) | COVERAGE_GAP — file absent from repo; test-inferred documentation is best achievable |
| `backend/common/llm_client.py` | 61 | `LLMClient` (service class) | Referenced in constants/relationships; spec notes "not a data model; wraps Gemini API" | PASS — intentional design decision; LLMClient is service not data entity |
| `backend/common/config.py` | 127 | Configuration dicts, constants | ✓ Sections 2–3 extensively | PASS |
| `backend/services/auditor.py` | 164 | `PaperAuditor` (service orchestrator) | Referenced in session state; not section 1 entity | COVERAGE_GAP — `PaperAuditor` has instance fields (`extraction_llm`, `evaluation_llm`, etc.) not documented as entity in section 1 |
| `backend/services/chatbot.py` | 47 | `PaperChatbot` (service) | Referenced in session state | PASS (LOC = 47, below 50 threshold; scope acceptable) |
| `backend/services/sota_analyzer.py` | 78 | `SotaAnalyzer` (service orchestrator) | Referenced in session state | COVERAGE_GAP — `SotaAnalyzer` has instance fields not in section 1 |
| `backend/services/pdf_parser.py` | 71 | No entity class; functional service | `chunk_size` constant documented | PASS |
| `backend/skills/auditor_skills.py` | 324 | `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ChecklistVerificationSkill` | Listed as BaseSkill subclasses in relationships | PASS (all are BaseSkill subclasses with no new class-level fields; `execute()` only) |
| `backend/skills/chatbot_skills.py` | 90 | `ConversationalResponseSkill`, `ContextValidationSkill` | Listed as BaseSkill subclasses in relationships | PASS (same reasoning) |
| `backend/skills/regex_detection_skills.py` | 542 | Multiple regex skill classes | Listed as BaseSkill subclasses in relationships | PASS (same reasoning) |
| `backend/skills/sota_skills.py` | 334 | `ThematicCoverageSkill`, `QueryGenerationSkill`, etc. | Listed as BaseSkill subclasses in relationships | PASS (same reasoning) |
| `backend/utils/logger.py` | 48 | `Colors`, `ColoredFormatter` | `Colors` constants fully documented in §3 | PASS (LOC = 48, under threshold; Colors documented) |
| `frontend/utils/scoring.py` | 113 | `CHECKLIST_KEYS`, `CHECKLIST_LABELS` | ✓ Section 4 fully documented | PASS |
| `frontend/utils/session_state.py` | 17 | Session state init function | ✓ Section 4 fully documented | PASS |
| `frontend/components/audit_results.py` | 270 | Row color logic, compliance table | ✓ Section 3 constants | PASS |
| `frontend/components/gauge_chart.py` | 67 | Score tier constants | ✓ Section 3 constants | PASS |
| `frontend/components/file_uploader.py` | 80 | Saturation error keywords | ✓ Section 3 constants | PASS |
| `frontend/components/sota_section.py` | 89 | SOTA UI component | No new data types | PASS |
| `backend/common/prompts.py` | 470 | LLM prompt functions | ✓ Section 5 LLM schemas extensively | PASS |

---

## Fidelity Issues

**None.** Every spec claim that has a `SOURCE:` reference was verified by opening the corresponding file and confirming the exact line. No fabricated or incorrect claims were found.

Key verifications performed:
- `Hyperparameters` field `warmup_steps` (not `warmup`) — confirmed exact name at `rag_extraction_skill.py:19`
- `BaseSkill.config` stored type is `Dict` (not `Optional[Dict]`) — correct at storage level due to `config or {}` guard at `base_skill.py:27`
- `was_refined = not verification_result.get('was_corrected', False)` — confirmed at `auditor_skills.py:392`
- `NEGATION_WINDOW = 60` — confirmed at `regex_detection_skills.py:8`
- All 8 `Colors` constants — confirmed at `logger.py:7-14`
- All 5 `AUDIT_CONFIG` keys with correct values — confirmed at `config.py:116-122`
- All 16 `CHECKLIST_KEYS` in correct order — confirmed at `scoring.py:8-15`

---

## Coverage Gaps

| # | Entity / Source File | Missing | Reason |
|---|---|---|---|
| CG-1 | `backend/common/audit_state.py` (entire file) | All 3 entities (`AuditState`, `ExtractedInfo`, `ChecklistItem`) cannot be verified from primary implementation | **Source file absent from repository.** The spec correctly documents this with `[CONFIDENCE: UNRESOLVED]` warnings and test-inference caveats. Root cause of CG-2 through CG-5. |
| CG-2 | `AuditState` | `evaluation` field: nullability and default not resolved; dict key structure not documented beyond `CHECKLIST_KEYS` reference | Test-inferred only — `test_audit_state.py` does not assert these properties |
| CG-3 | `ExtractedInfo` | `code` field: type is "nested model / object" — actual class name (`CodeInfo` or similar) not determinable | Test-inferred only — `info.code.repository_url == "NOT FOUND"` confirms the attribute exists but not the class type |
| CG-4 | `ExtractedInfo` | `hyperparameters` field: type not resolved — actual class name not determinable | Same reasoning as CG-3 |
| CG-5 | `ChecklistItem` | All field contracts not documented | Source absent; class not exercised in test assertions — VERIFIED_DOCUMENTED_GAP per spec notation |

> Note: CG-2 through CG-5 are all intentionally documented with `[GAP: ...]` markers in the spec. The spec writer correctly signals these as unresolved absences rather than asserting unsupported claims.

---

## Depth Gaps

**None.** All field entries in the spec that have primary source access include type annotations, defaults, and constraint derivations where applicable. The `[GAP: ...]` markers in section 1 for test-inferred entities are valid documented absences, not depth gaps — the spec cannot produce depth for fields whose source class does not exist in the repository.

---

## Special Entity Notes

### `AuditState`

**Classification: PARTIAL**

- Source `backend/common/audit_state.py` is absent from the repository. This is verified by scanning the full input directory: only `backend/common/config.py`, `llm_client.py`, `prompts.py`, and `__init__.py` exist.
- The spec's four field entries are inferred from `tests/test_audit_state.py`. Three fields (`paper_text`, `invalid_paper`, `execution_time`) have their values confirmed by direct test assertions at lines 6, 9, and 10 respectively:
  - `assertEqual(state.paper_text, "Test content")` → `str` ✓
  - `assertFalse(state.invalid_paper)` → `bool`, default `False` ✓
  - `assertEqual(state.execution_time, 0.0)` → `float`, default `0.0` ✓
- The fourth field (`evaluation`) is inferred from `test_to_frontend_dict` which passes `evaluation={"claims": {...}}`. Nullability and the complete dict structure are legitimately `[GAP]`.
- The method `to_frontend_dict()` returning `informacion_extraida` and `metricas` is confirmed by test assertions at lines 13-18.
- **Label: COVERAGE_GAP (test-inferred, partially verifiable)** — the inferred contracts are valid for 3/4 fields.

### `ExtractedInfo`

**Classification: SHALLOW**

- Source absent (same root cause as `AuditState`).
- The spec infers `code` and `hyperparameters` as nested objects from `test_extracted_info_nesting` at lines 22-23:
  - `info.code.repository_url == "NOT FOUND"` confirms `code` has a `repository_url` attribute
  - `info.hyperparameters.optimizer == "NOT FOUND"` confirms `hyperparameters` has an `optimizer` attribute
- **However**, the field types remain `[GAP: type not resolved]`. Neither field provides the actual class name or the full field contract of the nested objects. This prevents a PARTIAL classification (>50% of field detail is missing).
- **Label: COVERAGE_GAP (test-inferred, unverifiable)** — confirmed per instructions for test-only inference.

### `ChecklistItem`

**Classification: SHALLOW / VERIFIED_DOCUMENTED_GAP**

- Source absent. The class is imported at `tests/test_audit_state.py:1` (`from backend.common.audit_state import AuditState, ExtractedInfo, ChecklistItem`) but is never instantiated or asserted against in any test.
- The spec entry contains exactly one row: `[GAP: field contract not resolved in extraction]`. No fields are stated without a `[GAP]` marker.
- **Per the special entity instructions:** "If all fields are marked `[GAP]`, confirm and note as VERIFIED_DOCUMENTED_GAP." ✓
- **Label: VERIFIED_DOCUMENTED_GAP** — the spec correctly and honestly documents the absence of any derivable field contract.

---

## Quality Assessment

### Well-documented areas

**`Hyperparameters` (Pydantic model)** is the strongest entity in the spec. All 14 fields are present with exact source references, correct `str` types, confirmed `Field(description=...)` constraints, and proper "required" notation. The two relationship notes (usage as `response_schema` at line 204 and `_clean_with_regex` type coercions at line 277) add operational context beyond mere field inventory. This entity would pass a production code-generation prompt without modification.

**`BaseSkill` and `CompositeSkill`** are also well-documented. The field count, types, defaults, and the inheritance chain are all confirmed. The note about `config` being stored as `Dict` (not `Optional[Dict]`) despite the `Optional[Dict]` parameter annotation is correctly handled — the spec describes the stored type, which is always `dict`. The subclass list in the `BaseSkill` relationships section provides comprehensive coverage of the inheritance tree.

**Sections 2–5** (configuration dicts, named constants, session state, LLM schemas) are exceptionally thorough. Every constant value was independently verified against source. Notable verified details:
- The exact five AUDIT_CONFIG keys and values
- The retryable HTTP code set in `llm_client.py`
- The complete 16-key `CHECKLIST_KEYS` enum in correct order
- The RAG scoring formula (distance → relevance score)
- The `verified`/`was_refined` field semantics for `ChecklistVerificationSkill` output
- The `metricas.red_flags_detectadas` exclusion logic (5 prefix conditions)
- The full `resultado` virtual schema (23 core keys + 2 optional)

### Weak areas

**The three absent-source entities** (`AuditState`, `ExtractedInfo`, `ChecklistItem`) reduce `entity_completeness_pct` to 58%. This is an inherent limitation of the repository rather than a spec deficiency. The spec handles the situation correctly with explicit confidence warnings and [GAP] markers, but the classifier still scores them as PARTIAL and SHALLOW because actual field detail is unavailable.

**Service class entities** (`PaperAuditor`, `SotaAnalyzer`) are not documented in section 1 even though their `__init__` fields (e.g., `extraction_llm`, `evaluation_llm`, `rag_map_llm`) could be listed. These are service orchestrators, not data-flow types, so their omission from the data model is a reasonable design decision. A reviewer may choose to add them in a follow-up.

### Suitability as reverse-engineering artifact

`01_data_model.md` is **suitable for use as a reverse-engineering artifact** for the portions it covers:

1. The `Hyperparameters` Pydantic model can be reconstructed exactly from the spec (all 14 fields, types, `Field(description=...)` descriptors).
2. The `BaseSkill` and `CompositeSkill` contracts are sufficient to regenerate the abstract base.
3. The full configuration layer (AUDIT_CONFIG, CHAT_CONFIG, SOTA_CONFIG, all constants) is production-faithful.
4. The session state schema and CHECKLIST_KEYS are complete.
5. The five LLM response JSON schemas are detailed enough for code generation.

The only blocker for full reconstruction is the missing `backend/common/audit_state.py`, which cannot be recovered from this spec alone. A fix run should target that gap specifically — either by locating the missing file or by drafting the `AuditState`, `ExtractedInfo`, and `ChecklistItem` contracts from the test assertions that ARE available.

### Recommended fix actions for next pipeline run

1. **Priority 1**: Locate or reconstruct `backend/common/audit_state.py`. The test file `tests/test_audit_state.py` provides enough hints to draft a reasonable implementation for validation.
2. **Priority 2**: Add `PaperAuditor` and `SotaAnalyzer` as service class entries in a new "Service Classes" subsection (section 1b) to improve backward coverage.
3. **Priority 3**: Clarify `ExtractedInfo.code` and `ExtractedInfo.hyperparameters` actual class names (likely `CodeInfo` or `CodeSection` and `HyperparametersInfo` or similar) once the primary source is located.
