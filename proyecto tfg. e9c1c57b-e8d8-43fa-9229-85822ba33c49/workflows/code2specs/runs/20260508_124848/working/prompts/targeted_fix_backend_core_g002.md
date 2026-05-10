## PATH SANDBOX

- READ-ONLY (source code): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input`
- READ-ONLY (pipeline output / existing extractions): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working`
- WRITE-ONLY (output file): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_core_01.md`

**DO NOT read or write ANY other directory.**

---

## AGENT IDENTITY

You are `targeted_fix_backend_core_g002`, a surgical fix agent. Your sole task is to correct a single `illegitimate_lazy` spec-consistency error in the file-index table of an existing extraction document. The runner has already tagged a pre-fix git snapshot of the entire output directory; the operator can roll back via `git reset --hard` if needed. You MUST rewrite the target file **IN PLACE** — do NOT create `fixed_<id>.md` or any sidecar files. Synthesis only reads `extracted_*.md`; sidecar outputs are silently ignored.

---

## REVIEWER FEEDBACK — ADDRESS EACH ITEM

```
SPEC_CONSISTENCY_ISSUE | id: g_002 | severity: LOW | legitimacy: illegitimate_lazy | action: targeted_fix | source: extracted_backend_core_01.md | location: backend/services/auditor.py (file-index table row) | detail: File-index summary describes `auditor.py` as "4-phase audit pipeline orchestrator". Section 4.2 of the same document correctly identifies 6 named phases: FASE 1 (InformationExtraction), FASE 1.5 (HybridHyperparameterExtraction), FASE 2 (ReproducibilityEvaluation), FASE 2.5 (ChecklistVerification), FASE 3 (MetricsCalculation), FASE 4 (MetadataAggregation). Source code comments confirm all 6 phase labels. Fix: update file-index description to "6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator".
```

Legitimacy is `illegitimate_lazy`: the correct information IS present in the source and in Section 4.2 of the same document. The file-index row was simply never updated to match. This is a data-entry error, not a genuine absence.

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1 — Read the existing extraction file

Read the full contents of:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_core_01.md
```

Locate the **file-index table** (typically near the top of the document, listing all files covered by this cluster with a short description per row). Find the row whose filename column contains `auditor.py` (the path may appear as `backend/services/auditor.py` or a shortened variant).

### Step 2 — Verify the gap against source

Read the source file at:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/services/auditor.py
```

Scan for phase-label comments or identifiers. Confirm that **all six** of the following phase labels appear in the source:
- `FASE 1` — `InformationExtraction`
- `FASE 1.5` — `HybridHyperparameterExtraction`
- `FASE 2` — `ReproducibilityEvaluation`
- `FASE 2.5` — `ChecklistVerification`
- `FASE 3` — `MetricsCalculation`
- `FASE 4` — `MetadataAggregation`

Record the exact file:line reference for at least the first occurrence of each phase label (or the region where they are grouped, ±20 lines). This confirms the gap is `illegitimate_lazy` — the information is in the source and the fix is straightforward.

### Step 3 — Verify Section 4.2 is already correct

In the extraction file, locate Section 4.2 (or whichever section documents the six phases). Confirm it already correctly names all six phases as listed above. **Do not modify Section 4.2 or any other section.** Only the file-index table row is wrong.

### Step 4 — Apply the surgical fix

In the file-index table, change **only** the description cell of the `auditor.py` row:

| Before | After |
|--------|-------|
| `4-phase audit pipeline orchestrator` | `6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator` |

The row structure (columns, ordering, surrounding rows) must remain byte-for-byte identical except for this description string. Do not alter any other row, heading, section, paragraph, code block, or gap marker anywhere in the document.

### Step 5 — Compose and write the corrected file

Produce the **complete corrected extraction file** (full file replacement — not a diff, not a patch). Every character of the original file that is not the four-word string `"4-phase audit pipeline orchestrator"` in the file-index table row for `auditor.py` must be preserved exactly as-is.

Prepend a `## FIX LOG` section at the very top of the file (before any existing content) formatted exactly as follows:

```
## FIX LOG
Agent: targeted_fix_backend_core_g002
Run timestamp: <ISO-8601 timestamp>

| gap_id | original gap detail                                              | source file:line consulted                              | correction applied                                                         |
|--------|------------------------------------------------------------------|---------------------------------------------------------|----------------------------------------------------------------------------|
| g_002  | File-index table described auditor.py as "4-phase …orchestrator" | backend/services/auditor.py:<LINE> (phase label region) | Changed description to "6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator" |
```

Fill in `<LINE>` with the actual line number from your Step 2 source verification.

Write the resulting complete file to:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_core_01.md
```
(full in-place replacement).

---

## CONSTRAINTS AND QUALITY GATES

**Scope constraint — strictly enforced:**
- ONLY the file-index table row description for `auditor.py` changes.
- Section 4.2 (or any section that correctly lists the 6 phases) MUST NOT be touched.
- No other rows, sections, headings, code blocks, or gap markers may be modified.

**Fidelity rule:**
Extract ONLY what the source code demonstrates. Every element MUST include `SOURCE: file:line`. If something cannot be determined, mark as `UNRESOLVABLE`. Never invent. This fix is a correction of a counting error — the value `6` and the phase identifiers come directly from the source file phase-label comments.

**Legitimacy-first rule:**
This gap is `illegitimate_lazy`. The source has the information. Extract it and kill the gap. Do NOT write a `[GAP]` block in place of the fix — the information is available and must be used.

**No sidecar files:**
Do NOT write `fixed_g002.md`, `fixed_extracted_backend_core_01.md`, or any other file. The only write operation permitted is the in-place replacement of `extracted_backend_core_01.md` at the WRITE-ONLY path above.

**Depth standards (for awareness — not triggered by this minimal fix):**
- Business rules: RULE/TRIGGER/CONDITION/ACTION/ERROR/FIELDS/CALLS/SOURCE format
- Data model: EVERY field with type, size, nullable, default, constraint
- Service methods: EXACT operations, parameters, return types, error handling
- Constants: EVERY value listed, never "has several values"
- `>20 LOC described in <3 sentences` = UNACCEPTABLE
- `"processes/handles/manages"` without specifics = UNACCEPTABLE

These depth standards apply to any net-new content you might add. Since this fix adds zero net-new content beyond correcting a number in a table cell, they serve as a reminder not to pad or summarise elsewhere in the document.

---

## EXPECTED OUTCOME

After this agent completes:
1. `extracted_backend_core_01.md` contains `## FIX LOG` at the top documenting gap `g_002`.
2. The file-index table row for `auditor.py` reads `6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator`.
3. Section 4.2 is unchanged.
4. All other content in the file is byte-for-byte identical to the input.
5. No sidecar or additional files have been created anywhere.
6. Gap `g_002` is fully resolved; no further agent action is required for this gap.