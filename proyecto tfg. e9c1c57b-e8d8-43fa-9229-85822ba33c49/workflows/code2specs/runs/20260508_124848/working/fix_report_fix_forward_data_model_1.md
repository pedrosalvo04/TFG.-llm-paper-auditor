# Fix Report — fix_forward_data_model_1

**Agent:** fix_forward_data_model_1  
**Type:** depth_fix  
**Target spec:** `01_data_model.md`  
**Validation report:** `validation_report_val_forward_data_model.md`  
**Total issues:** 7 (2 FIDELITY, 2 COVERAGE_GAP, 3 DEPTH_GAP)

---

## Fix 1 — FIDELITY: RAG Distance Formula — Stale Line Reference

**Validation issue (report section):** "Issue 1: RAG Distance Formula — Stale Line Reference. Spec cites `rag_extraction_skill.py:127`; actual code at lines 152–157. Line 127 is `chunk_relevance = {}` — unrelated. Formula itself is correct."

**Location in spec:** Section 3 → Constants: RAG Operations → "RAG distance → relevance score formula" caption line: `Source: rag_extraction_skill.py:127`

**Source evidence:** Opened `backend/skills/rag_extraction_skill.py`. Confirmed:
- Line 127: `chunk_relevance = {}` — start of chunk-deduplication dict; unrelated to formula
- Lines 152–157: the actual `if distance < 0.4: / elif distance < 0.7: / else:` block with the exact formula values cited in the spec (`int(95 - (distance * 25))`, `int(85 - ((distance - 0.4) * 180))`, `max(5, int(31 - ((distance - 0.7) * 50)))`). SOURCE: `rag_extraction_skill.py:152-157`.

**Action taken:** Changed `Source: rag_extraction_skill.py:127` → `Source: rag_extraction_skill.py:152`

**Rationale:** The formula content in the spec is correct; only the line citation was stale. The correct anchor line is 152, where the `if distance < 0.4:` branch begins.

---

## Fix 2 — FIDELITY: `verified` / `was_refined` Fields — Stale Line Reference

**Validation issue (report section):** "Issue 2: `verified` / `was_refined` Fields — Stale Line Reference. Spec cites `auditor_skills.py:325` (method signature); actual assignments at lines 391–392."

**Location in spec:** Section 4 → Checklist Answer Values → "After `ChecklistVerificationSkill` runs, items also gain:" table — both `verified` and `was_refined` rows cited `auditor_skills.py:325`.

**Source evidence:** Opened `backend/skills/auditor_skills.py`. Confirmed:
- Line 325: `def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:` — `ChecklistVerificationSkill.execute` method signature; not the field assignments.
- Line 391: `"verified": True,` — explicit assignment. SOURCE: `auditor_skills.py:391`.
- Line 392: `"was_refined": not verification_result.get('was_corrected', False)` — explicit assignment. SOURCE: `auditor_skills.py:392`.
- The logic described in spec ("always True"; "True if NOT corrected") matches the source exactly.

**Action taken:** Updated `verified` row source from `auditor_skills.py:325` → `auditor_skills.py:391`; updated `was_refined` row source from `auditor_skills.py:325` → `auditor_skills.py:392`.

**Rationale:** Content meaning is correct; line citations now point to the actual assignment lines rather than the method signature.

---

## Fix 3 — COVERAGE_GAP: `CHECKLIST_LABELS` Dict Missing

**Validation issue (report section):** "Coverage Gaps — `frontend/utils/scoring.py` — `CHECKLIST_LABELS` dict. 16-entry dict mapping checklist keys to display strings. Present at line 17. Used in UI rendering via `CHECKLIST_LABELS.get(key, key)` at line 112."

**Location in spec:** Section 4 → After "CHECKLIST_KEYS Enum Set" (new sub-section inserted before "Checklist Answer Values").

**Source evidence:** Opened `frontend/utils/scoring.py`. Confirmed:
- Line 17: `CHECKLIST_LABELS = {` — dict definition starts.
- Lines 18–33: all 16 key→label entries, e.g. `"claims": "1. Claims"`, `"declaration_llm_usage": "16. Declaration of LLM Usage"`, etc. SOURCE: `scoring.py:17-34`.
- Line 112: `"label": CHECKLIST_LABELS.get(key, key),` — usage in `get_checklist_health()` function. SOURCE: `scoring.py:112`.

**Action taken:** Added new sub-section "### CHECKLIST_LABELS Display Strings" immediately after the CHECKLIST_KEYS table, with a 16-row table documenting each key→label mapping with per-row source citations (`scoring.py:18` through `scoring.py:33`).

**Rationale:** Satisfies the coverage gap: all 16 entries are now documented with exact string literals and per-line source citations.

---

## Fix 4 — COVERAGE_GAP: `NEGATION_PATTERNS` Compiled Regex Missing

**Validation issue (report section):** "Coverage Gaps — `backend/skills/regex_detection_skills.py` — `NEGATION_PATTERNS` compiled regex. Module-level `re.compile(...)` at line 10. Used alongside `NEGATION_WINDOW` in all regex detection skill classes."

**Location in spec:** Section 3 → Constants: RAG Operations — added block after the NEGATION_WINDOW/batch_size table rows, before the existing inline table for inter-batch sleep and other RAG constants.

**Source evidence:** Opened `backend/skills/regex_detection_skills.py`. Confirmed:
- Lines 10–18: `NEGATION_PATTERNS = re.compile(r"...", re.IGNORECASE)` with 6 alternation branches. SOURCE: `regex_detection_skills.py:10-18`.
- Lines 21–25: `_is_negated(text, match_start)` uses `NEGATION_PATTERNS.search(preceding)` where `preceding` is the `NEGATION_WINDOW`-char slice before the match. SOURCE: `regex_detection_skills.py:21-25`.
- Exact branch patterns extracted verbatim from source lines 11–16.

**Action taken:** Added sub-block "#### Negation Detection Pattern (`NEGATION_PATTERNS`)" with a 6-row table documenting each alternation branch, its pattern text, and the language it targets. Includes usage context and source citations.

**Rationale:** Satisfies the coverage gap. All 6 branches documented with exact pattern text from source. Type (`re.Pattern`), flags (`re.IGNORECASE`), and usage in `_is_negated()` are documented.

---

## Fix 5 — DEPTH_GAP: `AuditState` — Underspecified `evaluation` Field

**Validation issue (report section):** "Depth Gaps — AuditState — PARTIAL — 4 fields inferred from test assertions | Missing: Full type annotations, nullability for `evaluation`, default value for `evaluation`, all other fields beyond the 4 tested (source file `backend/common/audit_state.py` is absent)."

**Location in spec:** Section 1 → Entity: `AuditState` — `evaluation` row in the field table.

**Source evidence (test file):**
- Line 7: `state = AuditState(paper_text="Test content")` — no `evaluation` argument; construction succeeds. This confirms `evaluation` has a default (is optional). SOURCE: `tests/test_audit_state.py:7`.
- Line 14: `state = AuditState(paper_text="Test", evaluation={"claims": {"answer": "Yes"}})` — `evaluation` accepts a dict. SOURCE: `tests/test_audit_state.py:14`.
- `backend/common/audit_state.py` is absent from the repository; exact default value (e.g., `{}` or `None`) cannot be confirmed.

**Action taken:** Updated `evaluation` row:
- Nullable column: `[GAP: nullability not resolved]` → `Yes (optional — test at test_audit_state.py:7 constructs without evaluation arg, confirming a default exists)`
- Default column: `[GAP: default not resolved]` → `[GAP: exact default not confirmed — source absent; test line 7 omits evaluation arg, implying a default (likely {}) exists; test line 14 passes {"claims": {"answer": "Yes"}} and it is accepted as a dict]`
- Source column: `tests/test_audit_state.py:13` → `tests/test_audit_state.py:13-14`

**Rationale:** Cannot fully resolve this depth gap — source file is absent. The improvement replaces blank [GAP:] markers with specific, test-backed evidence about optionality and the dict type acceptance. The remaining unknown (exact default value and all other fields beyond the 4 tested) is properly [GAP:]'ed with source explanation.

---

## Fix 6 — DEPTH_GAP: `ExtractedInfo` — Misplaced Column Values and Unresolved Nullable/Default

**Validation issue (report section):** "Depth Gaps — ExtractedInfo — PARTIAL — 2 top-level fields (code, hyperparameters) inferred | Missing: Concrete Python types for code and hyperparameters sub-objects; all other sub-fields beyond repository_url and optimizer defaults."

**Location in spec:** Section 1 → Entity: `ExtractedInfo` — `code` and `hyperparameters` rows in the field table. Both rows had `[GAP: type not resolved]` incorrectly placed in the **Nullable** column (not the Type column), and `—` in the Default column.

**Source evidence (test file):**
- Line 22: `info = ExtractedInfo()` — no-argument construction succeeds. SOURCE: `tests/test_audit_state.py:22`.
- Line 23: `self.assertEqual(info.code.repository_url, "NOT FOUND")` — `code` field is a non-None object with attribute `repository_url == "NOT FOUND"`. SOURCE: `tests/test_audit_state.py:23`.
- Line 24: `self.assertEqual(info.hyperparameters.optimizer, "NOT FOUND")` — `hyperparameters` field is a non-None object with attribute `optimizer == "NOT FOUND"`. SOURCE: `tests/test_audit_state.py:22-23` (test method `test_extracted_info_nesting`).
- `backend/common/audit_state.py` is absent; concrete class names for the default objects cannot be confirmed.

**Action taken:** Updated both rows:
- `code` Nullable: `[GAP: type not resolved]` (misplaced) → `No (non-None default) — ExtractedInfo() constructs with no args and code.repository_url equals "NOT FOUND", confirming a default non-None object`
- `code` Default: `—` → `[GAP: concrete default class not confirmed — source absent; test line 22 confirms non-None default object with repository_url == "NOT FOUND"]`
- `hyperparameters` Nullable: `[GAP: type not resolved]` (misplaced) → `No (non-None default) — same ExtractedInfo() no-args construction and hyperparameters.optimizer equals "NOT FOUND"`
- `hyperparameters` Default: `—` → `[GAP: concrete default class not confirmed — source absent; test line 22 confirms non-None default object with optimizer == "NOT FOUND"]`
- `hyperparameters` Source: `tests/test_audit_state.py:23` → `tests/test_audit_state.py:22-23`

**Rationale:** Corrects the column misplacement (type text was in the Nullable column). Replaces uninformative dashes with test-backed evidence that both fields have non-None defaults. The concrete class types remain [GAP:] because the source file is absent. All other sub-fields remain [GAP:] in the sub-field table below.

---

## Fix 7 — DEPTH_GAP: `ChecklistItem` — No Field Contracts

**Validation issue (report section):** "Depth Gaps — ChecklistItem — NAME_ONLY — class name only, no field contracts | Missing: All field names, types, defaults, and constraints (source absent)."

**Location in spec:** Section 1 → Entity: `ChecklistItem` — single-row table with `[GAP: field contract not resolved in extraction]`.

**Source evidence attempt:**
- `backend/common/audit_state.py` is absent from the repository — primary source unavailable.
- Opened `tests/test_audit_state.py`: `ChecklistItem` is imported at line 2 but never instantiated or field-accessed in any test method. No field contracts can be derived from the test file. SOURCE: `tests/test_audit_state.py:2` (import only).
- Evidence gate failed: no field contracts found in any available source file.

**Action taken:** NO CHANGE

**Rationale:** Evidence gate failed (Step B). The test file imports `ChecklistItem` but does not construct or assert on any field. The source definition file (`backend/common/audit_state.py`) is absent. Adding field contracts based on the LLM response schema (prompts.py) or the auditor_skills.py dict assignments would constitute "inferred from similar code" — a forbidden pattern. The existing `[GAP: field contract not resolved in extraction]` marker is the correct and only permissible representation.
