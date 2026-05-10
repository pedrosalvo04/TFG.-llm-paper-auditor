---
validator_id: val_dep_graph_schema
validator_type: dependency_graph_schema
target_specs: [08_dependency_graph.json, 08_dependency_graph.md]
forward_coverage_pct: N/A
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: 76.4
consolidator_preservation_pct: N/A
fidelity_issues: 0
coverage_gaps: 0
depth_gaps: 0
spec_consistency_issues: 0
total_issues: 115
overall_status: fail
---

## Summary

The dependency graph was validated against its JSON schema requirements, the companion markdown file, and spot-checked against source code. The JSON is well-formed and parses cleanly. Node identification, typing, module assignment, and ID format are all fully compliant (50/50 nodes, zero violations). However, a systemic schema deviation affects all 57 edges: the spec requires `source` and `target` as connectivity fields, but the JSON uses `from` and `to` instead — the `source` field present on edges is a provenance reference (file:line), not a node identifier, and `target` is absent entirely. Additionally, the top-level `metadata` key is missing. These two issues account for all 115 SCHEMA_ISSUEs. Graph connectivity is functionally sound (zero dangling references using the actual `from`/`to` fields). JSON/MD consistency is perfect and all 10 spot-checked nodes are verified against source code.

---

## Schema Compliance

| Schema Check | Scope | Result | Deviation |
|---|---|---|---|
| Top-level key: `nodes` | 1 check | PASS | — |
| Top-level key: `edges` | 1 check | PASS | — |
| Top-level key: `modules` | 1 check | PASS | — |
| Top-level key: `cycles` | 1 check | PASS | — |
| Top-level key: `cross_module_summary` | 1 check | PASS | — |
| Top-level key: `metadata` | 1 check | **FAIL** | Key absent entirely |
| `modules` array non-empty | 1 check | PASS | 4 modules present |
| `cross_module_summary` non-empty | 1 check | PASS | 8 cross-module pairs documented |
| `node.id` present | 50 checks | PASS | All 50 nodes have id |
| `node.label` present | 50 checks | PASS | All 50 nodes have label |
| `node.type` present | 50 checks | PASS | All 50 nodes have type |
| `node.module` present | 50 checks | PASS | All 50 nodes have module |
| Node ID format (`type:label`) | 50 checks | PASS | All 50 follow stable `type:label` pattern; no opaque IDs |
| Edge `type` field present | 57 checks | PASS | All 57 edges have `type` |
| Edge `source` field (connectivity) | 57 checks | **FAIL** | Edges use `from` for source node ID; `source` field exists but contains provenance string, not a node reference |
| Edge `target` field (connectivity) | 57 checks | **FAIL** | Edges use `to` for target node ID; `target` field is absent |
| Edge wrong field name (`relationship`) | 57 checks | PASS | No edges use deprecated `relationship` field |
| Referential integrity (`from`/`to` → node_ids) | 57 checks | PASS | 0 dangling references using actual connectivity fields |
| JSON/MD node count consistency | 1 check | PASS | JSON=50, MD=50, delta=0% |
| Module list JSON/MD consistency | 1 check | PASS | Both have [backend_core, backend_skills, frontend, root] |

**Totals:** 487 checks | 372 pass | 115 fail | **schema_compliance_pct = 76.4%**

---

## Node Spot-Check Results

| Node ID | Claimed Type | Source File Found | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `service:PaperAuditor` | service | `backend/services/auditor.py` | Yes | VERIFIED | `class PaperAuditor` found at file root |
| `service:LLMClient` | service | `backend/common/llm_client.py` | Yes | VERIFIED | `class LLMClient` found; uses `google.genai` |
| `service:InformationExtractionSkill` | service | `backend/skills/auditor_skills.py` | Yes | VERIFIED | `class InformationExtractionSkill` found |
| `service:BaseSkill` | service | `backend/skills/base_skill.py` | Yes | VERIFIED | `class BaseSkill` found |
| `service:HybridHyperparameterExtractionSkill` | service | `backend/skills/rag_extraction_skill.py` | Yes | VERIFIED | `class HybridHyperparameterExtractionSkill` found |
| `config:config_py` | config | `backend/common/config.py` | Yes | VERIFIED | File confirmed present in extraction cluster |
| `config:prompts_py` | config | `backend/common/prompts.py` | Yes | VERIFIED | File confirmed present in extraction cluster |
| `screen:file_uploader` | screen | `frontend/components/file_uploader.py` | Yes | VERIFIED | File confirmed; screen classification appropriate for Streamlit component |
| `entity:AuditState` | entity | `backend/common/audit_state.py` (absent) | N/A | VERIFIED | `[GAP:]` description correctly documents that `audit_state.py` does not exist in codebase; referenced via `tests/test_audit_state.py` import. Intentional documented absence — not flagged. |
| `external:GoogleGeminiAPI` | external | N/A (external system) | Yes | VERIFIED | Concept confirmed: `from google import genai` in `backend/common/llm_client.py`; external system classification is correct |

---

## JSON/MD Consistency

| Metric | JSON Value | MD Value | Delta % | Status |
|---|---|---|---|---|
| Node count | 50 | 50 (unique `####` headings) | 0% | PASS |
| Module count | 4 | 4 (`## Module:` sections) | 0% | PASS |

**Note:** The MD has 50 unique node headings matching the 50 JSON nodes exactly. A minor observation: one node appears to be missing the `**Node ID**` bullet (49 vs 50 instances), but all 50 nodes have a dedicated `####` heading — this is a formatting inconsistency within the MD, not a node count discrepancy. The 5 nodes with `module=external` in JSON are not listed in the `modules` array (which has 4 entries) nor in an MD `## Module:` section; this is consistent between JSON and MD and thus not a CONSISTENCY_ISSUE.

---

## Fidelity Issues

None. All 10 spot-checked nodes are verified against source code. The three entity nodes (`entity:AuditState`, `entity:ExtractedInfo`, `entity:ChecklistItem`) carry `[GAP: ...]` markers in their descriptions explicitly documenting that `backend/common/audit_state.py` is absent from the codebase. Per validation rules, plain `[GAP: ...]` markers are intentional documented absences and are not flagged as fidelity issues.

---

## Spec Consistency Issues

None. JSON node count (50) and MD node reference count (50) are identical (0% delta, within the 10% threshold). The JSON `modules` array and the MD `## Module:` sections both enumerate the same four modules: `backend_core`, `backend_skills`, `frontend`, `root`.

---

## Schema Violations Detail

### Violation 1 — Missing top-level `metadata` key (1 SCHEMA_ISSUE)

| Location | Field | Violation |
|---|---|---|
| Top-level JSON | `metadata` | Key absent. The spec requires `metadata` as a top-level key. No metadata object is present in the JSON. |

### Violation 2 — Edge connectivity field names (114 SCHEMA_ISSUEs across 57 edges)

All 57 edges use `from` and `to` as connectivity fields instead of the required `source` and `target`. The `source` field does exist on every edge but contains a provenance reference (e.g., `"extracted_backend_core_01.md#3.1-LLM-Client (llm_client.py:19,25)"`) — a documentation string, not a node ID. The `target` field is entirely absent.

**Representative violations (first 5 edges):**

| Edge (from → to) | Field | Violation |
|---|---|---|
| `service:LLMClient` → `config:config_py` | `source` | Field absent as node ref; uses `from` instead. `source` contains provenance string. |
| `service:LLMClient` → `config:config_py` | `target` | Field absent; uses `to` instead. |
| `service:PaperAuditor` → `config:config_py` | `source` | Same pattern. |
| `service:PaperAuditor` → `config:config_py` | `target` | Same pattern. |
| `service:PaperChatbot` → `config:config_py` | `source` | Same pattern. |

**Scope:** This pattern is uniform across **all 57 edges** — it is a single systemic naming convention deviation, not 57 independent errors. The underlying connectivity data is correct (zero dangling references when using the actual `from`/`to` fields). A mechanical rename of `from`→`source` and `to`→`target` in the JSON would resolve all 114 violations.

---

## Quality Assessment

**What is structurally sound:**
- **Node quality is excellent.** All 50 nodes have valid `id`, `label`, `type`, and `module` fields. All node IDs follow the stable `type:label` naming convention (e.g., `service:PaperAuditor`, `screen:file_uploader`). No opaque IDs (`node_N` style) are present.
- **Graph topology is accurate.** The 57 edges represent real dependencies verified through spot-checks. The `from`/`to` fields correctly reference existing node IDs — zero dangling references. The detected cycle (`file_uploader → st.session_state → audit_results`) is correctly classified as informational (data-flow through shared Streamlit session state, not an execution loop).
- **Module coverage is complete.** All 4 modules (backend_core, backend_skills, frontend, root) are populated in `modules` and `cross_module_summary`. Cross-module edge counts are documented (8 direction pairs, 49 cross-module edges of 57 total).
- **JSON/MD consistency is perfect.** Both files document 50 nodes across 4 modules with zero discrepancy.
- **Fidelity is high.** All 10 spot-checked nodes trace to real source constructs. The 3 entity [GAP:] nodes correctly document a missing file (`audit_state.py` absent from codebase), which is accurate.

**What deviates from expected schema:**
- **Edge field naming (systemic, requires fix):** The entire edge array uses `from`/`to` for connectivity instead of the spec-required `source`/`target`. This is the sole root cause of 114 of the 115 SCHEMA_ISSUEs and drives the `fail` status. Remediation is mechanical: a single find-and-replace `"from":` → `"source":` and `"to":` → `"target":` throughout the `edges` array. The `source` provenance field must be renamed to avoid collision — e.g., `"provenance"` or `"evidence"`.
- **Missing `metadata` key (minor):** The top-level `metadata` object is absent. Recommend adding at minimum `{"generated_at": "<timestamp>", "source_files": [...], "graph_version": "1.0"}`.

**Risk assessment:**
- The field naming issue is a **high-priority structural fix** that blocks any downstream consumer expecting `source`/`target` in edges (e.g., graph visualization tools, Specs2Code pipeline readers).
- All other aspects of the graph (coverage, accuracy, depth) are high quality and do not require rework.
