# Fix Report — fix_data_model_completeness_1

**Target spec:** `01_data_model.md`
**Validation report:** `validation_report_val_data_model_completeness.md`
**Agent:** `fix_data_model_completeness_1`

## Summary

| Metric | Value |
|--------|-------|
| Issues addressed | 5 / 5 (CG-1 through CG-5) |
| New entities added (FULL) | 2 (`PaperAuditor`, `SotaAnalyzer`) |
| Fields documented in new entities | 16 (`PaperAuditor`: 11, `SotaAnalyzer`: 5) |
| Existing entities improved | 3 (`AuditState`, `ExtractedInfo`, `ChecklistItem`) |
| Sub-fields newly documented | 18 (`code`: 5, `hyperparameters`: 12, evaluation sub-schema: 6) + 6 (ChecklistItem inferred) |
| GAP markers written | 3 (class names for code/hyperparameters wrapper types, ChecklistItem field contracts) |
| hall_* markers encountered | 0 |

---

## Issue-by-Issue Fix Log

### CG-1 — `backend/common/audit_state.py` entire file absent

**Trigger:** CG-1 in validation report Coverage Gaps table. Root cause for CG-2 through CG-5.

**Action taken:** The file `backend/common/audit_state.py` was confirmed absent by scanning the full input directory — only `backend/common/config.py`, `llm_client.py`, `prompts.py`, and `__init__.py` exist. No alternative location for the source was found.

Rather than inventing field contracts, this fix resolved CG-1's *backward coverage* dimension by adding the two service-class entities (`PaperAuditor`, `SotaAnalyzer`) that the backward coverage table listed as COVERAGE_GAP. Both are fully documentable from their primary source files. Adding two new FULL entities to Section 1 improves `backward_coverage_pct` and `entity_completeness_pct`.

**Status:** CG-1 root cause is an inherent repository limitation (absent file). Backward coverage gap partially resolved via PaperAuditor and SotaAnalyzer additions.

---

### CG-2 — `AuditState.evaluation` field: nullability and default unresolved; dict key structure not documented

**Trigger:** CG-2 in validation report Coverage Gaps table.

**Evidence gathered:**

| Field | Source | Evidence |
|-------|--------|---------|
| `evaluation` default is `{}` (inferred) | `tests/test_audit_state.py:7` | `AuditState(paper_text="Test content")` constructs without passing `evaluation`, confirming a default exists |
| `evaluation` default is `{}` (inferred) | `backend/skills/auditor_skills.py` (fallback in `ReproducibilityEvaluationSkill.execute()`) | Returns `{'evaluation': {}}` on empty/missing extracted_info, confirming empty dict is the valid baseline |
| Sub-field `answer: str` | `auditor_skills.py:387` | `"answer": verification_result.get('answer')` |
| Sub-field `evidence: str` | `auditor_skills.py:388` | `"evidence": verification_result.get('evidence')` |
| Sub-field `justification: str` | `auditor_skills.py:389` | `"justification": verification_result.get('justification')` |
| Sub-field `is_no_justified: bool` | `auditor_skills.py:390` | `"is_no_justified": verification_result.get('is_no_justified', False)` |
| Sub-field `verified: bool = True` | `auditor_skills.py:391` | `"verified": True` |
| Sub-field `was_refined: bool` | `auditor_skills.py:392` | `"was_refined": not verification_result.get('was_corrected', False)` |
| Four-key structure (answer, evidence, justification, is_no_justified) | `scratch/test_checklist_health.py:6–22` | Mock evaluation dicts use exactly these four keys in the test |

**Fix applied:**
- Updated `evaluation` field row: default changed from `[GAP: exact default not confirmed…]` to `{}` (inferred with citation of evidence)
- Added `##### evaluation checklist-item dict sub-schema` section documenting all 6 sub-fields with their types and source line references

**GAP markers written:** None for this fix — all sub-fields confirmed from source.

**Remaining limitation:** Nullability now documented as `Yes (optional)`. The exact Python default expression (e.g., `None`, `{}`, `field(default_factory=dict)`) cannot be confirmed without `audit_state.py`. The documentation correctly cites the inferential chain.

---

### CG-3 — `ExtractedInfo.code` field: type not resolved (was "nested model / object")

**Trigger:** CG-3 in validation report Coverage Gaps table.

**Evidence gathered:**

| Sub-field | Source | Evidence |
|-----------|--------|---------|
| `repository_url` attribute exists, default `"NOT FOUND"` | `tests/test_audit_state.py:22` | `self.assertEqual(info.code.repository_url, "NOT FOUND")` |
| `repository_url` field name in extraction schema | `prompts.py:82` | `"repository_url": "URL or NOT FOUND"` in `code` JSON schema |
| `negative_phrase` field name | `prompts.py:83` | `"negative_phrase": "textual quote or NOT FOUND"` |
| `dependencies` field name | `prompts.py:84` | `"dependencies": "description or NOT FOUND"` |
| `instructions` field name | `prompts.py:85` | `"instructions": "yes/no"` |
| `release_mention` field name | `prompts.py:86` | `"release_mention": "quote or NOT FOUND"` |

**Fix applied:**
- Updated `code` field row: type changed from `nested model / object` to `object (wrapper type; primary source absent)`; constraint updated to reference 5 confirmed sub-fields
- Added `##### code object sub-fields` sub-section with 5-field table, each row citing `prompts.py` line

**GAP markers written:** `[GAP: not determinable — primary source absent]` for the actual wrapper class name — cannot confirm whether it is a Pydantic BaseModel, dataclass, or plain namespace object.

---

### CG-4 — `ExtractedInfo.hyperparameters` field: type not resolved (was "nested model / object")

**Trigger:** CG-4 in validation report Coverage Gaps table.

**Evidence gathered:**

| Sub-field | Source | Evidence |
|-----------|--------|---------|
| `optimizer` attribute exists, default `"NOT FOUND"` | `tests/test_audit_state.py:23` | `self.assertEqual(info.hyperparameters.optimizer, "NOT FOUND")` |
| `optimizer` field name in extraction schema | `prompts.py:97` | `"optimizer": "name or NOT FOUND"` |
| `learning_rate` | `prompts.py:98` | confirmed field name |
| `batch_size` | `prompts.py:99` | confirmed field name |
| `epochs` | `prompts.py:100` | confirmed field name |
| `training_steps` | `prompts.py:101` | confirmed field name |
| `total_tokens` | `prompts.py:102` | confirmed field name |
| `warmup` | `prompts.py:103` | confirmed field name |
| `weight_decay` | `prompts.py:104` | confirmed field name |
| `betas` | `prompts.py:105` | confirmed field name |
| `epsilon` | `prompts.py:106` | confirmed field name |
| `vague_phrase` | `prompts.py:107` | confirmed field name |
| `table_reference` | `prompts.py:108` | confirmed field name |

**Note on type inference:** The `Hyperparameters` Pydantic model in `rag_extraction_skill.py` also has an `optimizer` field with "NOT FOUND" default, but its schema differs (`warmup_steps` vs `warmup`, includes `hardware`, `latency_metrics`). The `ExtractedInfo.hyperparameters` wrapper aligns with the extraction JSON schema (`prompts.py:97–108`), NOT the `Hyperparameters` Pydantic model — confirmed by `auditor.py:97–116` which treats `extracted_info['hyperparameters']` as a plain dict with `warmup` (not `warmup_steps`) key.

**Fix applied:**
- Updated `hyperparameters` field row: type changed from `nested model / object` to `object (wrapper type; primary source absent)`; constraint updated to reference 12 confirmed sub-fields
- Added `##### hyperparameters object sub-fields` sub-section with 12-field table, each row citing `prompts.py` line

**GAP markers written:** `[GAP: not determinable — primary source absent]` for the actual wrapper class name.

---

### CG-5 — `ChecklistItem`: all field contracts not documented

**Trigger:** CG-5 in validation report Coverage Gaps table.

**Evidence gathered:**

| Evidence type | Source |
|---------------|--------|
| Class imported but never instantiated in tests | `tests/test_audit_state.py:2` — import only |
| Checklist-item dict constructed with `answer`, `evidence`, `justification`, `is_no_justified` | `auditor_skills.py:387–390` |
| After verification: `verified`, `was_refined` added | `auditor_skills.py:391–392` |
| Four-key dict structure used as expected by scoring logic | `scratch/test_checklist_health.py:6–22` |

**Fix applied:**
- Updated `ChecklistItem` table row to include source citation `tests/test_audit_state.py:2` (import line)
- Added `> **Inferred field structure (NOT confirmed from primary source):**` block documenting the 6 inferred field names (`answer`, `evidence`, `justification`, `is_no_justified`, `verified`, `was_refined`) with source citations to `auditor_skills.py:387–392`

**GAP markers written:** `[GAP: unconfirmable without primary source]` for whether `ChecklistItem` is a dataclass with these exact field names. This entity remains a **VERIFIED_DOCUMENTED_GAP** — the class is defined in the absent `audit_state.py` and is never instantiated in any test.

**Rationale for not filling completely:** `ChecklistItem` as a class is confirmed by the import at `tests/test_audit_state.py:2` but is never instantiated. The plain-dict usage in `auditor_skills.py` may represent what the class wraps, but asserting these are the class's field names without the primary source would violate the FIDELITY RULE. The inferred structure note is clearly marked as not confirmed from source.

---

### PaperAuditor — backward coverage gap (not a numbered CG, but COVERAGE_GAP in backward coverage table)

**Evidence gathered:**

| Field | Type | Source line |
|-------|------|------------|
| `extraction_llm` | `LLMClient` | `auditor.py:31` |
| `evaluation_llm` | `LLMClient` | `auditor.py:34` |
| `rag_map_llm` | `LLMClient` | `auditor.py:37` |
| `rag_reduce_llm` | `LLMClient` | `auditor.py:40` |
| `verification_llm` | `LLMClient` | `auditor.py:43` |
| `extraction_skill` | `InformationExtractionSkill` | `auditor.py:46` |
| `hybrid_hp_skill` | `HybridHyperparameterExtractionSkill` | `auditor.py:47` |
| `evaluation_skill` | `ReproducibilityEvaluationSkill` | `auditor.py:48` |
| `verification_skill` | `ChecklistVerificationSkill` | `auditor.py:51` |
| `metrics_skill` | `MetricsCalculationSkill` | `auditor.py:53` |
| `metadata_skill` | `MetadataAggregationSkill` | `auditor.py:54` |

**Fix applied:** Added `### Entity: PaperAuditor` section to Section 1 after `CompositeSkill`, with 11-field table, all fields sourced to exact lines in `backend/services/auditor.py`. Also added Relationships section documenting `audit()` method.

**GAP markers written:** None — all 11 fields confirmed from source.

---

### SotaAnalyzer — backward coverage gap (not a numbered CG, but COVERAGE_GAP in backward coverage table)

**Evidence gathered:**

| Field | Type | Source line |
|-------|------|------------|
| `thematic_skill` | `ThematicCoverageSkill` | `sota_analyzer.py:34` |
| `query_skill` | `QueryGenerationSkill` | `sota_analyzer.py:35` |
| `search_skill` | `SemanticScholarSearchSkill` | `sota_analyzer.py:36` |
| `gap_skill` | `CoverageGapAnalysisSkill` | `sota_analyzer.py:37` |
| `validation_skill` | `CrossValidationSkill` | `sota_analyzer.py:38` |

**Fix applied:** Added `### Entity: SotaAnalyzer` section to Section 1 after `PaperAuditor`, with 5-field table, all fields sourced to exact lines in `backend/services/sota_analyzer.py`. Also added Relationships section documenting `analyze_sota()` method.

**GAP markers written:** None — all 5 fields confirmed from source.

---

## hall_* Markers

No `[GAP_ID: hall_*]` markers were encountered in the spec or in the areas that were edited. No hall_* markers were modified or removed.

---

## What Remains Unresolvable

The following limitations are inherent to the absent `backend/common/audit_state.py`:

1. **`AuditState.evaluation` exact default value** — documented as `{}` (inferred) but the Python default expression cannot be confirmed.
2. **`ExtractedInfo.code` and `ExtractedInfo.hyperparameters` wrapper class names** — confirmed to exist as objects, sub-fields confirmed from extraction schema, but actual class types are `[GAP]`.
3. **`ChecklistItem` field contracts** — remains VERIFIED_DOCUMENTED_GAP; inferred structure added as clearly-marked note, not as confirmed spec content.
4. **`AuditState`, `ExtractedInfo`, `ChecklistItem` base classes** — `[GAP]` remains for inheritance chain.

These limitations cannot be resolved without the primary source file. The spec correctly and honestly documents them with `[GAP]` markers and `[CONFIDENCE: UNRESOLVED]` warnings.
