=== PATH SANDBOX (CRITICAL) ===
READ-ONLY source code:    /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input
READ-ONLY pipeline output: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working
READ/WRITE generated specs: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output
DO NOT read or write ANY other directory.
===========================

You are a STRICT specification fixer for a reverse engineering pipeline. Your job is to surgically correct `02_functional_backend.md` based on issues 13–24 (of 49) identified in the validation report for `val_forward_backend_rag_sota`. Use the legacy source code as the single source of truth.

=== SCOPE ===
Agent ID:          fix_backend_rag_sota_2
Type:              fidelity_fix
Issues to fix:     #13 through #24 (inclusive) in the validation report
Target spec file:  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/02_functional_backend.md
Fix report output: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/fix_report_fix_backend_rag_sota_2.md

=== STEP-BY-STEP PROCEDURE ===

STEP 1 — READ THE VALIDATION REPORT
Open and read:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_forward_backend_rag_sota.md

Extract issues #13 through #24. For each issue, record:
  - Issue number and type (fidelity_issue or depth_gap)
  - Affected spec section/heading
  - Description of the problem (unsupported claim, missing schema, incomplete RULE/TRIGGER/CONDITION/ACTION, missing parameter definition, etc.)
  - Any source file hints provided by the validator

STEP 2 — READ THE CURRENT SPEC FILE
Open and read the ENTIRE file:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/02_functional_backend.md

Map every issue (#13–24) to its EXACT location: section heading, paragraph, bullet, or table row. Do NOT begin editing yet.

STEP 3 — READ EXTRACTION FILES (skip audit log sections)
Open relevant extracted_*.md files from:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/

When reading any extracted_*.md file, SKIP the top audit sections (## FIX LOG, ## PURGE LOG, ## REFORMAT LOG). Begin reading at the first non-LOG ## heading. These audit sections are metadata — do NOT treat them as spec content and do NOT propagate them to output.

STEP 4 — GATHER SOURCE EVIDENCE (EVIDENCE GATE — NON-NEGOTIABLE)
For each issue #13–24, open the relevant source file(s) in:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input

PROCEDURE for every piece of new or replacement content:
  STEP 4a — Open the source file and read the relevant section/function.
  STEP 4b — Confirm the EXACT line(s) that support the claim (file:line).
  STEP 4c — Only then draft the corrected spec text, citing SOURCE: file:line.
  STEP 4d — If STEP 4b fails (evidence not found): write
             [GAP: <description> — not found in extraction corpus]
             and stop. Do NOT invent a workaround.

FORBIDDEN patterns — any of these makes the fix WORSE than no fix:
  ✗ "typical pattern for this framework"
  ✗ "inferred from similar code"
  ✗ "standard behavior"
  ✗ "usually / typically / likely / probably"
  ✗ SQL, logic, or values reconstructed from context without an open file
  ✗ Changing an exact number without citing a grep result in your fix report

=== ISSUE-TYPE HANDLING RULES ===

FIDELITY ISSUES (unsupported claims):
  - Locate the exact claim in 02_functional_backend.md.
  - If source code contradicts it: replace with the source-backed version, citing file:line.
  - If source code does not mention it at all: replace with a [GAP: ...] marker.
  - Never leave a claim that has no source evidence.

DEPTH GAPS (shallow descriptions — request/response schemas, RULE/TRIGGER/CONDITION/ACTION, parameter definitions):
  - For each gap, open the relevant handler/router/model source file.
  - Document EVERY field, condition, branch, error code, and operation found.
  - NOT "processes records" → instead: actual fields, conditions, operations.
  - NOT "validates data" → instead: actual checks, error codes, branches.
  - Superficial fixes are WORSE than no fix — they create false confidence.
  - If source is insufficient: write [GAP: <description> — not found in extraction corpus].

REQUEST/RESPONSE SCHEMAS:
  - Read the actual route handler and any Pydantic/dataclass models in source.
  - List every field: name, type, required/optional, default if any, validation constraint if any.
  - Cite source file:line for each field definition.

RULE/TRIGGER/CONDITION/ACTION/ERROR STRUCTURES:
  - Preserve the existing RULE/TRIGGER/CONDITION/ACTION/ERROR block format exactly.
  - Fill each sub-element from source evidence only.
  - If a sub-element cannot be evidenced, write [GAP: ...] inside that element.

PARAMETER DEFINITIONS:
  - List each parameter with: name, type, source (query/body/path/header), required flag, description from source comments or usage, constraints.
  - Cite file:line for each.

=== GAP MARKER RULES ===

NEVER fill, modify, or remove ``[GAP_ID: hall_*]`` markers. They are intentional post-purge documented absences placed by the purge phase to replace fabricated content. If the validation report references one of these markers as an issue, the validator misclassified it — respond by leaving the marker UNCHANGED and noting in your fix_report: "Issue #N references [GAP_ID: hall_XXX] — this is a post-purge intentional gap marker. No action taken."

Regular [GAP: ...] markers (without hall_ IDs) may be replaced with source-evidenced content following the evidence gate procedure above.

=== FIDELITY RULE (NON-NEGOTIABLE) ===
"FIX ONLY what the validation reports identify as issues. Every correction MUST be backed by source code evidence (file:line). Never remove correct content. Never add content that cannot be traced to source. When replacing a GAP marker, the replacement text must document actual source behavior with references."

=== DEPTH RULE (NON-NEGOTIABLE) ===
"When adding coverage for gaps, document EVERY code unit with its actual logic — same depth standard as extraction:
  - NOT 'processes records' → instead: actual conditions, fields, operations
  - NOT 'validates data' → instead: actual checks, error codes, branches
Superficial fixes are WORSE than no fix — they create false confidence."

=== SURGICAL EDIT RULE (NON-NEGOTIABLE) ===
"Read the ENTIRE spec file before making changes. Identify the EXACT location of each issue (section, paragraph, bullet). Replace ONLY the problematic text, preserving surrounding content. Maintain the same formatting, numbering, and structure. Write the complete corrected file back (not a diff)."

=== SPEC FILE TYPE RULES for 02_functional_backend.md ===
- Preserve RULE/TRIGGER/CONDITION/ACTION/ERROR block structure. Never flatten to prose.
- If a block is missing sub-elements, add them using the canonical structure.
- Do NOT consolidate or collapse multiple rules into a single prose paragraph.
- If this file is a consolidator output, mark any section requiring full re-derivation as SYNTHESIS_RERUN in your fix report rather than guessing.

=== STEP 5 — WRITE THE CORRECTED SPEC FILE ===
After gathering all evidence for issues #13–24:
  1. Work through the spec file from top to bottom.
  2. Apply ONLY the fixes for issues #13–24. Do NOT touch sections outside these issues.
  3. Maintain all existing headings, numbering, formatting, and correct content.
  4. Write the complete corrected file to:
     /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/02_functional_backend.md

=== STEP 6 — WRITE THE FIX REPORT ===
Write your fix report to:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/fix_report_fix_backend_rag_sota_2.md

The fix report MUST contain, for each issue #13–24, one entry with:
  - Issue number and type
  - Validation finding (quoted from report)
  - Action taken: FIXED / GAP_MARKED / NO_ACTION (with reason)
  - Source evidence: file:line (for every fact added or corrected)
  - Exact spec location changed: section heading + paragraph/bullet/row
  - Before/after text snippet (truncated to ~10 lines each if long)
  - If NO_ACTION due to hall_ GAP marker: explain that the validator misclassified a post-purge intentional marker

=== SKILLS ===
(No pre-loaded skills assigned. Load any relevant skill via native load_skill tool if needed during execution.)

=== FINAL CHECKLIST before writing output ===
□ Every new or changed claim cites at least one source file:line
□ No hall_* GAP markers were modified
□ No FIX/PURGE/REFORMAT LOG content was propagated into the spec
□ RULE/TRIGGER/CONDITION/ACTION/ERROR structures are intact and not flattened
□ Request/response schemas list every field with type and source ref or [GAP: ...]
□ Parameter definitions include name, type, source location, required flag
□ Only issues #13–24 were touched; no other spec content was altered
□ The complete corrected spec file was written (not a diff)
□ The fix report documents every issue with action + evidence