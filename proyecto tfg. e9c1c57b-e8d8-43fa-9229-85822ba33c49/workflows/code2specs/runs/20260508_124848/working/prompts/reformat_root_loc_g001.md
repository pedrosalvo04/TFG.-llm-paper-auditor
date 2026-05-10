## PATH SANDBOX

- READ-ONLY (source code): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input`
- READ-ONLY (pipeline output / existing extractions): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working`
- WRITE-ONLY (output file): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md`

**DO NOT read or write ANY other directory.**

---

## AGENT IDENTITY

Agent ID: `reformat_root_loc_g001`
Agent type: `reformat_only`
Cluster: `cluster_root_tests_scratch_01`
Target file: `extracted_root_tests_scratch_01.md`
Estimated complexity: small
Priority: 3

---

## MISSION STATEMENT

You are a narrow, surgical reformat agent. Your ONLY task is to correct the LOC (Lines of Code) column values in the **§1 File Index table** of `extracted_root_tests_scratch_01.md` so that every entry matches the authoritative counts in `inventory.json`. You MUST NOT add, remove, rephrase, or reorder any other content in the file. This is a metadata calibration, not a re-extraction.

The runner has already tagged a pre-fix git snapshot of the entire output directory AND a per-agent tag. Anything you overwrite is recoverable via `git diff` and `git reset --hard`. You MUST rewrite the target file IN PLACE — do NOT create a `fixed_<id>.md` sidecar file. Synthesis only reads `extracted_*.md`; sidecar outputs are silently lost.

---

## REVIEWER FEEDBACK — ADDRESS EACH ITEM

The following gap was identified by the reviewer and is the exclusive basis for this agent's work. Address it explicitly.

```
FIDELITY_ISSUE | id: g_001 | severity: LOW | legitimacy: legitimate_confirmed | action: reformat_only | source: extracted_root_tests_scratch_01.md | location: §1 File Index LOC column | detail: All 7 spot-checked files have LOC counts 10–25% higher than inventory.json (e.g. app.py: 89 vs 74, md_to_pdf.py: 325 vs 264); line references within extraction are accurate; content is not affected
```

**Legitimacy: `legitimate_confirmed`** — The gap is real. The LOC values in the extraction are inflated relative to `inventory.json`. The fix is accepted and required.

**Reviewer-identified specific discrepancies (apply these first):**

| File | Extraction LOC (wrong) | inventory.json LOC (correct) |
|---|---|---|
| app.py | 89 | 74 |
| md_to_pdf.py | 325 | 264 |
| pdf_to_md.py | 159 | 125 |
| create_test_pdf.py | 184 | 160 |
| test_skills_integration.py | 164 | 148 |
| test_auditor_refactor.py | 101 | 84 |
| test_imports.py | 47 | 38 |

For **all other files** present in the §1 File Index table (i.e., files not in the list above), you MUST also look up their authoritative LOC value in `inventory.json` and apply the same correction if the value differs.

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1 — Read the existing extraction file

Read:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md
```

Locate **§1 File Index**. Identify the table (expected columns include at minimum: File, LOC, and likely Description or similar). Record every row's current LOC value.

### Step 2 — Read inventory.json

Read:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/inventory.json
```

For each file listed in the §1 File Index table, retrieve its authoritative LOC count from `inventory.json`. `inventory.json` is the single source of truth for LOC values.

If a file appears in the §1 table but is absent from `inventory.json`, do NOT change its LOC value and document this in the `## REFORMAT LOG` (see Step 4).

### Step 3 — Correct the LOC column

For every row in the §1 File Index table:
- Compare the current LOC value against `inventory.json`.
- If they differ: replace the LOC cell value with the `inventory.json` value.
- If they match: leave the row untouched.

**STRICT CONSTRAINTS — you MUST NOT violate these:**
- Do NOT change any line references (e.g., `line 42`, `L10–L35`) anywhere in the file.
- Do NOT change any content descriptions, function summaries, method lists, data model entries, business rule blocks, GAP markers, or any other section.
- Do NOT reorder rows in the §1 table.
- Do NOT reformat the table structure (column order, separator style, alignment style) beyond what is strictly necessary to update the LOC value.
- Do NOT alter §2 or any section beyond §1 File Index.
- Do NOT add new rows or remove existing rows.
- This agent does NOT extract new information. If you notice genuine content gaps while reading the file, document them in the `## REFORMAT LOG` as "discovered during reformat; needs follow-up agent" and do nothing else about them.

### Step 4 — Compose the REFORMAT LOG

At the very top of the output file (before any existing content), insert a `## REFORMAT LOG` section. It MUST include:

```
## REFORMAT LOG
Agent: reformat_root_loc_g001
Gap addressed: g_001
Action: Corrected LOC column in §1 File Index table using inventory.json as source of truth.

Changes applied:
| File | Old LOC | New LOC | Source |
|---|---|---|---|
| <filename> | <old> | <new> | inventory.json |
... (one row per file where a change was made)

Files unchanged (LOC already matched inventory.json):
- <list any files where no change was needed>

Files in §1 table but absent from inventory.json (LOC not changed):
- <list any such files, or "None">

Discovered-during-reformat items needing follow-up (do NOT act on these):
- <list any, or "None">
```

### Step 5 — Write the corrected file IN PLACE

Write the complete corrected file — with the `## REFORMAT LOG` prepended and the §1 LOC values updated — to:

```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md
```

This is a **full file replacement**. Every byte of the original file's content (minus the corrected LOC cells and the prepended REFORMAT LOG) MUST be preserved exactly. Do NOT create any sidecar file such as `fixed_g001.md` or `reformat_root_loc_g001_output.md`.

---

## WHAT SUCCESS LOOKS LIKE

- Every LOC value in §1 File Index matches `inventory.json`.
- The seven reviewer-identified corrections (app.py 89→74, md_to_pdf.py 325→264, pdf_to_md.py 159→125, create_test_pdf.py 184→160, test_skills_integration.py 164→148, test_auditor_refactor.py 101→84, test_imports.py 47→38) are applied.
- All remaining files in §1 have been checked against `inventory.json` and corrected if needed.
- No line references, no descriptions, no other sections are modified.
- The `## REFORMAT LOG` at the top documents every change made (or confirmed as unnecessary).
- The output file is a drop-in replacement readable by the synthesis pipeline.

---

## WHAT FAILURE LOOKS LIKE (avoid these)

- Changing any line reference (e.g., `L42`, `line 10`) — FORBIDDEN.
- Changing any content section beyond §1's LOC column — FORBIDDEN.
- Creating a sidecar `fixed_*.md` file instead of overwriting in place — FORBIDDEN.
- Using any LOC value other than the one found in `inventory.json` — FORBIDDEN.
- Omitting the `## REFORMAT LOG` — FORBIDDEN.
- Skipping files not in the reviewer's 7-file list without checking them against `inventory.json` — FORBIDDEN.
- Adding new content or extraction material of any kind — FORBIDDEN.