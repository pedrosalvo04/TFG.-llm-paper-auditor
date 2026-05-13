# Fix Report — fix_depth_entities_1

**Target spec:** `01_data_model.md`
**Validator:** `val_depth_entities`
**Agent responsible for:** Issues 1–12 of 15
**Issues 13–15:** Assigned to another agent — not touched.

---

## Issue 1 — FIDELITY

**Validation finding:** The `Hyperparameters` Relationships section cites `config={'response_schema': Hyperparameters}` at SOURCE: `rag_extraction_skill.py:204`. Line 204 is actually `self.log_execution("🧠 [Fase REDUCE]...")`. The actual assignment is at line 239 inside the `except` block of the REDUCE phase fallback call.

**Source evidence:** `backend/skills/rag_extraction_skill.py:239` — `'response_schema': Hyperparameters,` (inside the `config={...}` dict of the Gemini `generate_content()` call in the REDUCE except block).

**Action taken:** Changed the source citation in the Relationships bullet under `Entity: Hyperparameters` from `rag_extraction_skill.py:204` to `rag_extraction_skill.py:239`. The substantive claim was correct; only the line number was wrong.

**GAP markers written (if any):** None.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 2 — FIDELITY

**Validation finding:** In the "After `ChecklistVerificationSkill` runs" sub-table, both `verified` and `was_refined` rows cite SOURCE: `auditor_skills.py:325`. Line 325 is `def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:` (the method signature). The actual assignments are at lines 391–392 inside that method.

**Source evidence:**
- `backend/skills/auditor_skills.py:391` — `"verified": True,`
- `backend/skills/auditor_skills.py:392` — `"was_refined": not verification_result.get('was_corrected', False)`

**Action taken:** Updated the Source column of the `verified` row to `auditor_skills.py:391` and the `was_refined` row to `auditor_skills.py:392`. The claims were substantively correct; only the line numbers were wrong.

**GAP markers written (if any):** None.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 3 — COVERAGE_GAP

**Validation finding:** Entity `AuditState` exists in the test import but its source file `backend/common/audit_state.py` is absent from the repository.

**Source evidence:** N/A — source file absent. Validator explicitly notes: "These are correctly flagged by the spec as UNRESOLVED. They are reported here as coverage gaps per validator protocol, not as evidence of spec carelessness."

**Action taken:** No change. The spec already correctly documents `AuditState` with `CONFIDENCE: UNRESOLVED` markers and `[GAP: ...]` entries throughout. The existing documentation accurately conveys the limitation.

**GAP markers written (if any):** Pre-existing `[GAP: base class not extractable — source file backend/common/audit_state.py absent from repository]` preserved as-is.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 4 — COVERAGE_GAP

**Validation finding:** Entity `ExtractedInfo` exists in the test import but its source file `backend/common/audit_state.py` is absent from the repository.

**Source evidence:** N/A — source file absent. Same caveat as Issue 3.

**Action taken:** No change. The spec already correctly documents `ExtractedInfo` with `CONFIDENCE: UNRESOLVED` and `[GAP: ...]` markers. Pre-existing documentation is appropriate.

**GAP markers written (if any):** Pre-existing `[GAP: type not resolved]` (×2) and `[GAP: field contracts not resolved in extraction]` preserved as-is.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 5 — COVERAGE_GAP

**Validation finding:** Entity `ChecklistItem` exists in the test import but its source file `backend/common/audit_state.py` is absent from the repository. No field contracts are derivable from tests.

**Source evidence:** N/A — source file absent. Same caveat as Issues 3–4.

**Action taken:** No change. The spec already correctly documents `ChecklistItem` with `CONFIDENCE: UNRESOLVED` and `[GAP: field contract not resolved in extraction]`. Pre-existing documentation is appropriate.

**GAP markers written (if any):** Pre-existing `[GAP: base class not extractable ...]` and `[GAP: field contract not resolved in extraction]` preserved as-is.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 6 — DEPTH_GAP

**Validation finding:** `ChecklistItem` — all fields: TYPE, NULLABILITY, DEFAULT, CONSTRAINT, SOURCE are missing. Suggested fix requires the absent `backend/common/audit_state.py`.

**Source evidence:** `backend/common/audit_state.py` — ABSENT from repository. No field contracts derivable from test code.

**Action taken:** No change possible. Pre-existing `[GAP: field contract not resolved in extraction]` left exactly as found. Correctly-marked gap is better than invented detail.

**GAP markers written (if any):** Pre-existing marker preserved.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 7 — DEPTH_GAP

**Validation finding:** `ExtractedInfo.code` — TYPE (currently "nested model / object", too vague) and NULLABILITY are missing. Requires the absent source file.

**Source evidence:** `backend/common/audit_state.py` — ABSENT. Type of the `code` sub-model class cannot be confirmed.

**Action taken:** No change possible. Pre-existing `[GAP: type not resolved]` left exactly as found.

**GAP markers written (if any):** Pre-existing marker preserved.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 8 — DEPTH_GAP

**Validation finding:** `ExtractedInfo.hyperparameters` — TYPE (precise) and NULLABILITY missing. Requires the absent source file.

**Source evidence:** `backend/common/audit_state.py` — ABSENT.

**Action taken:** No change possible. Pre-existing `[GAP: type not resolved]` left exactly as found.

**GAP markers written (if any):** Pre-existing marker preserved.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 9 — DEPTH_GAP

**Validation finding:** `AuditState.evaluation` — NULLABILITY and DEFAULT are missing. Requires the absent source file.

**Source evidence:** `backend/common/audit_state.py` — ABSENT. Test assertions show the key exists in `to_frontend_dict()` output but do not reveal the Python type's nullability or default at construction.

**Action taken:** No change possible. Pre-existing `[GAP: nullability not resolved]` and `[GAP: default not resolved]` left exactly as found.

**GAP markers written (if any):** Pre-existing markers preserved.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 10 — DEPTH_GAP

**Validation finding:** Session State key `archivo_actual` documents SET and READ lifecycle but omits the CLEARED lifecycle (on "Limpiar" button press).

**Source evidence:** `frontend/app.py:29-31` — 
```python
if st.button("🔄 Limpiar y subir nuevo archivo"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
```
All session state keys (including `archivo_actual`) are deleted via `del st.session_state[key]` in this loop.

**Action taken:** Added `**Cleared:** on "Limpiar" button press (\`frontend/app.py:29-31\`, all session keys deleted via \`del st.session_state[key]\` loop).` to the Lifecycle column of the `archivo_actual` row in the Session State Schema table.

**GAP markers written (if any):** None.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 11 — DEPTH_GAP

**Validation finding:** Session State key `file_hash` documents SET and READ lifecycle but omits the CLEARED lifecycle.

**Source evidence:** Same as Issue 10 — `frontend/app.py:29-31` — `del st.session_state[key]` loop clears all session keys including `file_hash`.

**Action taken:** Added `**Cleared:** on "Limpiar" button press (\`frontend/app.py:29-31\`, all session keys deleted via \`del st.session_state[key]\` loop).` to the Lifecycle column of the `file_hash` row.

**GAP markers written (if any):** None.
**Post-purge hall_* marker encountered:** NO.

---

## Issue 12 — DEPTH_GAP

**Validation finding:** Session State key `md_text` documents SET and READ lifecycle but omits the CLEARED lifecycle.

**Source evidence:** Same as Issues 10–11 — `frontend/app.py:29-31` — `del st.session_state[key]` loop clears all session keys including `md_text`.

**Action taken:** Added `**Cleared:** on "Limpiar" button press (\`frontend/app.py:29-31\`, all session keys deleted via \`del st.session_state[key]\` loop).` to the Lifecycle column of the `md_text` row.

**GAP markers written (if any):** None.
**Post-purge hall_* marker encountered:** NO.

---

## Summary Table

| Issue # | Category | Entity/Field | Action | Evidence |
|---------|----------|-------------|--------|----------|
| 1 | FIDELITY | `Hyperparameters` / `response_schema` relationship | Corrected source line from `:204` to `:239` | `rag_extraction_skill.py:239` |
| 2 | FIDELITY | Checklist item dict / `verified` and `was_refined` | Corrected source lines from `:325` to `:391` and `:392` | `auditor_skills.py:391-392` |
| 3 | COVERAGE_GAP | `AuditState` | No change — already correctly marked UNRESOLVED with GAP markers | Source file absent |
| 4 | COVERAGE_GAP | `ExtractedInfo` | No change — already correctly marked UNRESOLVED with GAP markers | Source file absent |
| 5 | COVERAGE_GAP | `ChecklistItem` | No change — already correctly marked UNRESOLVED with GAP markers | Source file absent |
| 6 | DEPTH_GAP | `ChecklistItem` / all fields | No change possible — pre-existing GAP marker preserved | Source file absent |
| 7 | DEPTH_GAP | `ExtractedInfo` / `code` type+nullability | No change possible — pre-existing GAP marker preserved | Source file absent |
| 8 | DEPTH_GAP | `ExtractedInfo` / `hyperparameters` type+nullability | No change possible — pre-existing GAP marker preserved | Source file absent |
| 9 | DEPTH_GAP | `AuditState` / `evaluation` nullability+default | No change possible — pre-existing GAP markers preserved | Source file absent |
| 10 | DEPTH_GAP | Session State / `archivo_actual` CLEARED lifecycle | Added CLEARED lifecycle note to row | `frontend/app.py:29-31` |
| 11 | DEPTH_GAP | Session State / `file_hash` CLEARED lifecycle | Added CLEARED lifecycle note to row | `frontend/app.py:29-31` |
| 12 | DEPTH_GAP | Session State / `md_text` CLEARED lifecycle | Added CLEARED lifecycle note to row | `frontend/app.py:29-31` |
