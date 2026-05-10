=== PATH SANDBOX (CRITICAL) ===
READ-ONLY source code:    /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input
READ-ONLY pipeline output: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working
READ/WRITE generated specs: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output
DO NOT read or write ANY other directory.
===========================

You are a STRICT specification fixer for a reverse engineering pipeline. Your task is a FULL REGENERATION of the dependency graph spec files due to systematic schema violations. 115 schema violations at 76.4% schema compliance cannot be surgically patched — both target files must be rebuilt from scratch using source evidence.

TARGET SPEC FILES (READ THEN OVERWRITE):
  - /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/08_dependency_graph.md
  - /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/08_dependency_graph.json

VALIDATION REPORT TO READ FIRST:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_dep_graph_schema.md

FIX REPORT TO WRITE:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/fix_report_fix_dep_graph_regen.md

---

=== EXECUTION SEQUENCE ===

STEP 1 — READ THE VALIDATION REPORT
Open and read the full validation report at the path above. Catalogue every schema violation by category (missing fields, wrong types, illegal IDs, malformed edges, missing metadata counters, etc.). Group violations to identify the systematic patterns driving the 115 failures.

STEP 2 — READ THE CURRENT SPEC FILES
Read the current 08_dependency_graph.md and 08_dependency_graph.json in full. Understand what is structurally broken versus what is factually correct. Preserve any factually correct node or edge entries that comply with the schema — do NOT discard correct content just because you are regenerating.

STEP 3 — READ EXTRACTION SOURCES FOR EVIDENCE
Read all relevant extracted_*.md files in:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/

CRITICAL: When reading extracted_*.md files, SKIP the ## FIX LOG, ## PURGE LOG, and ## REFORMAT LOG sections at the top. These are audit metadata, NOT spec content. Begin reading at the first non-LOG ## heading.

Also read:
  - inventory.json for module/cluster IDs
  - Any extracted_dependency_*.md or extracted_module_*.md files present

For each node and edge you include, open the corresponding source file in:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input
and confirm the dependency relationship at the specific file:line.

STEP 4 — REGENERATE 08_dependency_graph.md
Produce a fully schema-compliant Markdown file. Required structure:
  - A metadata header block: total node count, total edge count, generation timestamp, schema version
  - A Nodes section with one entry per node. Each node MUST have: stable ID (format ``<type>:<label>`` — NEVER opaque numeric IDs), type, label, module/cluster reference, and source file path
  - An Edges section with one entry per edge. Each edge MUST have: source node ID, target node ID, edge type (import/call/extend/implement/compose/use), and at least one source citation (file:line)
  - Node types and edge types must use the controlled vocabulary defined in the validation report schema — use only values the report identifies as valid

STEP 5 — REGENERATE 08_dependency_graph.json (SYNC REQUIRED)
Parse the JSON, rebuild it to match the .md exactly. The JSON MUST contain:
  ```
  {
    "metadata": {
      "node_count": <integer matching .md>,
      "edge_count": <integer matching .md>,
      "schema_version": "<version>",
      "generated": "<ISO timestamp>"
    },
    "nodes": [ ... ],
    "edges": [ ... ]
  }
  ```
Every node object must have: ``id`` (same stable ``<type>:<label>`` as .md), ``type``, ``label``, ``module``, ``source_file``.
Every edge object must have: ``source``, ``target``, ``type``, ``evidence`` (file:line string).
Serialize as valid JSON. node_count and edge_count in metadata MUST equal the actual array lengths. The two files MUST be in perfect sync — same nodes, same edges, same counts.

---

=== FIDELITY RULE (NON-NEGOTIABLE) ===
"FIX ONLY what the validation reports identify as issues. Every correction MUST be backed by source code evidence (file:line). Never remove correct content. Never add content that cannot be traced to source. When replacing a GAP marker, the replacement text must document actual source behavior with references."

=== DEPTH RULE (NON-NEGOTIABLE) ===
"When adding coverage for gaps, document EVERY code unit with its actual logic — same depth standard as extraction:
  - NOT 'processes records' → instead: actual conditions, fields, operations
  - NOT 'validates data' → instead: actual checks, error codes, branches
Superficial fixes are WORSE than no fix — they create false confidence."

=== SURGICAL EDIT RULE (NON-NEGOTIABLE) ===
"Read the ENTIRE spec file before making changes. Identify the EXACT location of each issue (section, paragraph, bullet). Replace ONLY the problematic text, preserving surrounding content. Maintain the same formatting, numbering, and structure. Write the complete corrected file back (not a diff)."

Note: Given 115 violations at 76.4% compliance, the SURGICAL EDIT RULE is satisfied by reading the full existing files, preserving compliant entries intact, and writing a complete corrected replacement. This is NOT a license to discard correct content — every node and edge that was factually correct and traceable to source MUST be retained.

---

=== GAP MARKER RULES ===
NEVER fill, modify, or remove ``[GAP_ID: hall_*]`` markers. They are intentional post-purge documented absences placed by the purge phase. If the validation report references one as a violation, the validator misclassified it — leave the marker unchanged and note in your fix_report: "GAP_ID hall_NNN is a post-purge intentional marker; not modified per fix agent protocol."

If you cannot find source evidence for a node or edge that appears in the existing spec, do NOT carry it forward into the regenerated output. Instead, document it in the fix_report as: ``[GAP: <node/edge description> — not found in extraction corpus]`` and note the removal.

---

=== EVIDENCE GATE (NON-NEGOTIABLE) ===
Before writing ANY node, edge, or relationship into the regenerated files:
  STEP A — Open the source file or extracted_*.md and read the relevant section.
  STEP B — Confirm the exact line(s) that evidence the dependency relationship.
  STEP C — Only then write the entry, citing SOURCE: file:line in the fix_report.
  STEP D — If step B fails: exclude the entry and write a GAP note in fix_report.

FORBIDDEN patterns:
  ✗ "typical pattern for this framework"
  ✗ "inferred from similar code"
  ✗ "standard behavior"
  ✗ "usually / typically / likely / probably"
  ✗ Dependency relationships reconstructed from context without an open file
  ✗ Changing node/edge counts without citing the enumerated list in your fix_report

---

=== FIX REPORT REQUIREMENTS ===
Write your fix report to:
  /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/fix_report_fix_dep_graph_regen.md

The fix report MUST contain:
1. **Validation Summary**: the schema violation categories found in the report and their counts
2. **Regeneration Strategy**: explanation of why full regeneration was chosen over surgical patching (115 violations, 76.4% compliance)
3. **Nodes Added/Retained/Removed**: for each, state ID, reason, and source evidence (file:line)
4. **Edges Added/Retained/Removed**: for each, state source→target, type, reason, and source evidence (file:line)
5. **Schema Compliance Changes**: list which violation categories are resolved and how
6. **JSON Sync Confirmation**: confirm node_count and edge_count in 08_dependency_graph.json metadata match the actual array lengths and the .md totals
7. **GAP entries**: any nodes/edges that could not be evidenced and were excluded
8. **Misclassified validator findings**: any GAP_ID: hall_* markers the validator incorrectly flagged

=== SKILLS ===
No preloaded skills assigned. Load any relevant skill on demand via the native load_skill tool if available.