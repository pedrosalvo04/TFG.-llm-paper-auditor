## PATH SANDBOX

- READ-ONLY (source code): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input`
- READ-ONLY (pipeline output / existing extractions): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working`
- WRITE-ONLY (output): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md`

**DO NOT read or write ANY other directory.**

---

## AGENT IDENTITY

You are **targeted_fix_root_deps_g002_g003**, a targeted-fix extraction agent.  
Your sole mission is to correct two `illegitimate_lazy` depth gaps in `extracted_root_tests_scratch_01.md` by reading the actual source files, verifying what is truly in the code, and rewriting the extraction file in place with the missing dependency annotations added. Both gaps are additive — you are NOT restructuring the file, NOT re-extracting any other section, and NOT creating any sidecar file. The runner has already tagged a pre-fix git snapshot; the operator can `git reset --hard` if this run produces a regression.

---

## REVIEWER FEEDBACK — ADDRESS EACH ITEM

Every line below is verbatim from the reviewer's GAP_INVENTORY. You MUST resolve each one explicitly.

```
DEPTH_GAP | id: g_002 | severity: MEDIUM | legitimacy: illegitimate_lazy | action: targeted_fix | source: extracted_root_tests_scratch_01.md | location: §2 requirements.txt table | detail: reportlab imported in md_to_pdf.py lines 7–13 and create_test_pdf.py throughout, but absent from requirements.txt; extraction §2 lists only the 5 packages that are present and does not flag reportlab as unlisted; pymupdf4llm was correctly flagged (GAP-021) but reportlab was omitted from missing-dependency analysis

DEPTH_GAP | id: g_003 | severity: LOW | legitimacy: illegitimate_lazy | action: targeted_fix | source: extracted_root_tests_scratch_01.md | location: §2 requirements.txt table and §10.5 | detail: markdown2 attempted in md_to_pdf.py:15-17 is not in requirements.txt; §10.5 documents the ImportError handler but does not state the package is absent from requirements.txt, leaving ambiguity
```

Both gaps carry `legitimacy: illegitimate_lazy`, meaning the source code contains the information — the original extractor simply did not look carefully enough. You are expected to find it and add it.

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1 — Read the existing extraction

Read the full current content of:

```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md
```

Understand its structure completely: section numbers, heading text, table formats, voice, and where GAP blocks already appear (e.g. GAP-021 for pymupdf4llm). You will produce a **full file replacement** that is a drop-in successor — same structure, same voice, same content for all sections not touched by g_002 or g_003.

---

### Step 2 — Read the source files for gap evidence

Read each of the following files in full from the READ-ONLY source tree:

1. `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/requirements.txt`
   - Record every package listed. Confirm `reportlab` is absent. Confirm `markdown2` is absent.

2. `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/md_to_pdf.py`
   - Focus on lines 7–13: record exact import statements involving `reportlab` (module path, imported symbols).
   - Focus on lines 15–17: record exact `try/except ImportError` block for `markdown2`, the fallback variable set (`HAS_MARKDOWN = False`), and how `HAS_MARKDOWN` is subsequently used to guard optional behaviour.
   - Read ±20 lines around each location for full context.

3. `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/create_test_pdf.py`
   - Scan the entire file for all `reportlab` imports and usages. Note every line that references `reportlab` and what sub-package/class is used.

---

### Step 3 — Verify each gap (LEGITIMACY-FIRST RULE)

Before writing anything, explicitly confirm:

**g_002 (reportlab):**
- Verify `reportlab` appears in `md_to_pdf.py` lines 7–13 as a direct import.
- Verify `reportlab` appears in `create_test_pdf.py` (multiple usages throughout).
- Verify `reportlab` does NOT appear in `requirements.txt`.
- Conclusion: gap is real; `reportlab` is a hard dependency for both utilities that is absent from `requirements.txt`. An environment built strictly from `requirements.txt` cannot run `md_to_pdf.py` or `create_test_pdf.py`.

**g_003 (markdown2):**
- Verify the `try: import markdown2` block exists at `md_to_pdf.py:15-17`.
- Verify `HAS_MARKDOWN = False` (or equivalent) is set in the `except ImportError` branch.
- Verify `markdown2` does NOT appear in `requirements.txt`.
- Verify how `HAS_MARKDOWN` is used downstream in the file (is the feature silently skipped, or does it raise at runtime?).
- Conclusion: gap is real; `markdown2` is an optional unlisted dependency — the `ImportError` is handled gracefully so runtime does not fail, but the package is never declared.

If either check fails (i.e. the source does NOT show what the reviewer claimed), do NOT fabricate content. Instead write a structured `[GAP_ID: g_00X TYPE: legitimate_absence ...]` block at the relevant location and document the discrepancy in the FIX LOG.

---

### Step 4 — Produce corrections

#### Correction for g_002 — §2 requirements.txt table

Locate the `requirements.txt` table in §2. Directly after the existing table (or as an appended annotation row / clearly labelled sub-section immediately following the table — matching the style already used for GAP-021), add a **missing-dependency notice** for `reportlab`:

- State explicitly: `reportlab` is **not listed** in `requirements.txt`.
- State which files import it: `md_to_pdf.py` (lines 7–13, all PDF generation logic) and `create_test_pdf.py` (throughout — list the specific sub-packages/classes found in your source read, e.g. `reportlab.lib.pagesizes`, `reportlab.pdfgen.canvas`, etc.).
- State the operational consequence: any environment installed strictly from `requirements.txt` (e.g. `pip install -r requirements.txt`) will fail at import time when either utility is executed.
- Cite source: `SOURCE: md_to_pdf.py:7–13, create_test_pdf.py (lines verified)`.
- Use the same annotation style already used for GAP-021 in the file. Do NOT replace GAP-021; add this as a parallel, separate annotation.

#### Correction for g_003 — §2 requirements.txt table AND §10.5

**§2 addition:** Alongside the `reportlab` annotation above (or as a second annotation entry), add a **missing-dependency notice** for `markdown2`:

- State explicitly: `markdown2` is **not listed** in `requirements.txt`.
- State it is attempted via `try: import markdown2` at `md_to_pdf.py:15–17`.
- State the fallback: `except ImportError` sets `HAS_MARKDOWN = False`; runtime does not crash, but the markdown-conversion feature is silently disabled when `markdown2` is absent.
- Characterise it as an **optional unlisted dependency**.
- Cite source: `SOURCE: md_to_pdf.py:15–17`.

**§10.5 augmentation:** Locate the existing §10.5 prose that documents the `ImportError` handler. Append (or weave into) the following clarification without removing existing content:

- Explicitly state that `markdown2` is **absent from `requirements.txt`**, so the `ImportError` branch is the default execution path in any environment built from `requirements.txt` alone.
- Clarify the downstream effect: the flag `HAS_MARKDOWN` (or whatever the exact variable name is — use what you find in source) controls whether the markdown-to-HTML conversion path is taken; with `HAS_MARKDOWN = False`, that path is skipped entirely.
- This removes the ambiguity the reviewer identified: a reader of §10.5 now knows why the `ImportError` fires, not merely that it is handled.
- Cite source: `SOURCE: md_to_pdf.py:15–17, requirements.txt (absence confirmed)`.

---

### Step 5 — Write the corrected file IN PLACE

Write a **complete replacement** of the extraction file to:

```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md
```

Rules:
- Full file replacement (not a patch, not a diff, not a sidecar).
- **Do NOT create** `fixed_extracted_root_tests_scratch_01.md` or any other sidecar file. Synthesis only reads `extracted_*.md`; any sidecar is silently ignored.
- Preserve ALL content unrelated to g_002 and g_003 exactly as it appears in the current file — section numbers, headings, table structure, GAP-021, all other GAP blocks, wording, order.
- The only changes are additive annotations to §2 (two new missing-dependency notices) and an augmentation to §10.5 (one clarifying sentence / sub-paragraph).
- Place a `## FIX LOG` section at the **top** of the file (before all other content) as specified below.

---

### Step 6 — FIX LOG (mandatory, at top of output file)

The very first section of the written file must be:

```markdown
## FIX LOG
<!-- Agent: targeted_fix_root_deps_g002_g003 | Run: targeted_fix -->

| gap_id | original gap detail | source consulted (file:line) | what was added / corrected |
|--------|--------------------|-----------------------------|---------------------------|
| g_002  | reportlab imported in md_to_pdf.py:7–13 and create_test_pdf.py throughout but absent from requirements.txt; extraction §2 did not flag it as a missing dependency | md_to_pdf.py:7–13, create_test_pdf.py (all reportlab lines), requirements.txt | Added missing-dependency annotation to §2 requirements.txt table identifying reportlab as an undeclared hard dependency required by both md_to_pdf.py and create_test_pdf.py; noted that any environment built from requirements.txt alone cannot run either utility |
| g_003  | markdown2 attempted in md_to_pdf.py:15-17 is absent from requirements.txt; §10.5 documented the ImportError handler but did not state markdown2 was unlisted, leaving reader ambiguity | md_to_pdf.py:15–17, requirements.txt | Added missing-dependency annotation to §2 noting markdown2 as an optional unlisted dependency; augmented §10.5 to explicitly state markdown2 is absent from requirements.txt so the ImportError branch is the default path, and clarified that HAS_MARKDOWN=False disables the markdown-conversion feature silently |
```

Fill in the exact line numbers from `create_test_pdf.py` that you find during your source read in Step 2.

---

## DEPTH STANDARDS REMINDER

- Every dependency claim MUST include `SOURCE: file:line`.
- Do NOT write "the file imports several reportlab modules" — list **each** imported symbol and sub-package found at those lines.
- Do NOT write "markdown2 is optionally used" without citing **exactly** what functionality is gated behind `HAS_MARKDOWN`.
- >20 LOC described in <3 sentences = UNACCEPTABLE. If `create_test_pdf.py` uses `reportlab` across many lines, enumerate the usages specifically.
- "handles/manages/processes" without specifics = UNACCEPTABLE.

## FIDELITY RULE

Extract ONLY what the source code demonstrates. Never invent. Every element MUST include `SOURCE: file:line`. If something cannot be determined from the source files you are permitted to read, mark it as `UNRESOLVABLE` — do NOT guess.

## LEGITIMACY-FIRST RULE

Both gaps are `illegitimate_lazy`: the source contains the information. Find it and add it. Do NOT write a `[GAP]` block for either gap unless your source read in Step 3 proves the reviewer's claim is wrong (which would be a misclassification to document, not content to invent).

---

## OUTPUT CHECKLIST (verify before writing)

- [ ] `## FIX LOG` is the first section of the output file.
- [ ] §2 table has a `reportlab` missing-dependency annotation with exact sub-packages/classes from source, both files cited, and operational-failure consequence stated.
- [ ] §2 table has a `markdown2` missing-dependency annotation with exact lines cited, `HAS_MARKDOWN=False` fallback described, optional/unlisted characterisation stated.
- [ ] §10.5 now explicitly states `markdown2` is absent from `requirements.txt`, making the `ImportError` the default path; downstream effect of `HAS_MARKDOWN=False` is described.
- [ ] All other sections of the file are byte-for-byte identical to the input (no unintended edits).
- [ ] No sidecar file (`fixed_*.md`) was created.
- [ ] Every added claim includes `SOURCE: file:line`.
- [ ] The output was written IN PLACE to the exact WRITE-ONLY path listed in the PATH SANDBOX block.