# Fix Report — fix_glossary_1
**Target spec:** `06_glossary.md`  
**Validator:** `val_glossary_completeness`  
**Issues addressed:** 5 (2 FIDELITY, 2 COVERAGE_GAP, 1 DEPTH_GAP)

---

### Fix 1 — FIDELITY: §4.2 CHECKLIST_LABELS — source line numbers off by 8

**Validation issue:** FIDELITY-01. All 16 label source references in §4.2 pointed to `scoring.py:26–41`. Actual content at `scoring.py:26` is `"code_of_ethics": "9. Code of Ethics"` (the 9th label), not `"claims": "1. Claims"` (the 1st). Systematic offset of +8 across all 16 entries.

**Source evidence:** `frontend/utils/scoring.py:17–34` — confirmed by direct file read:
- Line 17: `CHECKLIST_LABELS = {`
- Line 18: `"claims": "1. Claims",`
- Line 19: `"limitations": "2. Limitations",`
- Line 26: `"code_of_ethics": "9. Code of Ethics",`  ← was incorrectly cited as label 1
- Line 33: `"declaration_llm_usage": "16. Declaration of LLM Usage",`
- Line 34: `}`

**Change made:** Replaced all 16 `Source` column entries in §4.2 table, correcting the line references from `scoring.py:26–41` to `scoring.py:18–33` (one line per label, matching the actual dict layout). Also updated the table intro sentence to document that the dict starts at line 17 and entries occupy lines 18–33.

**Before (excerpt, rows 1 and 9):**
```
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:26 |
| 9 | `"code_of_ethics"` | `"9. Code of Ethics"` | `extracted_frontend_01.md`, §2.3 — scoring.py:34 |
```

**After (excerpt, rows 1 and 9):**
```
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:18 |
| 9 | `"code_of_ethics"` | `"9. Code of Ethics"` | `extracted_frontend_01.md`, §2.3 — scoring.py:26 |
```

---

### Fix 2 — FIDELITY: §4.1 CHECKLIST_KEYS — per-key line references wrong for keys 3–16

**Validation issue:** FIDELITY-02. The §4.1 table assigned one line number per key incrementing by 1 (lines 8–23), but the actual `CHECKLIST_KEYS` list packs 2–4 keys per line across lines 9–14 only. Keys 3–16 referenced lines that either don't exist in `CHECKLIST_KEYS` context (line 23 is inside `CHECKLIST_LABELS`) or point to the wrong content (line 10 was assigned to key 3 `"theory_assumptions_proofs"`, but line 10 actually contains `"experimental_result_reproducibility", "open_access_data_code"`).

**Source evidence:** `frontend/utils/scoring.py:8–15` — confirmed by direct file read:
- Line 8: `CHECKLIST_KEYS = [`
- Line 9: `"claims", "limitations", "theory_assumptions_proofs",`
- Line 10: `"experimental_result_reproducibility", "open_access_data_code",`
- Line 11: `"experimental_setting_details", "experiment_statistical_significance",`
- Line 12: `"experiments_compute_resource", "code_of_ethics", "broader_impacts",`
- Line 13: `"safeguards", "licenses", "assets", "crowdsourcing_human_subjects",`
- Line 14: `"irb_approvals", "declaration_llm_usage"`
- Line 15: `]`

**Change made:** Replaced the §4.1 table header (3 columns → 4 columns, adding `NeurIPS Item Name`) and all 16 source line references. The corrected assignments: keys 1–3 → line 9; keys 4–5 → line 10; keys 6–7 → line 11; keys 8–10 → line 12; keys 11–14 → line 13; keys 15–16 → line 14. Also updated the introductory sentence to explain the multi-key-per-line packing. (The NeurIPS Item Name column addition is tracked under Fix 5 — DEPTH below.)

**Before (excerpt, rows 1–5):**
```
| Index | Key Value | Source |
|-------|-----------|--------|
| 1 | `"claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:8 |
| 2 | `"limitations"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 3 | `"theory_assumptions_proofs"` | `extracted_frontend_01.md`, §2.3 — scoring.py:10 |
| 4 | `"experimental_result_reproducibility"` | `extracted_frontend_01.md`, §2.3 — scoring.py:11 |
| 5 | `"open_access_data_code"` | `extracted_frontend_01.md`, §2.3 — scoring.py:12 |
```

**After (excerpt, rows 1–5):**
```
| Index | Key Value | NeurIPS Item Name | Source |
|-------|-----------|-------------------|--------|
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 2 | `"limitations"` | `"2. Limitations"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 3 | `"theory_assumptions_proofs"` | `"3. Theory, Assumptions & Proofs"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 4 | `"experimental_result_reproducibility"` | `"4. Experimental Result Reproducibility"` | `extracted_frontend_01.md`, §2.3 — scoring.py:10 |
| 5 | `"open_access_data_code"` | `"5. Open Access to Data and Code"` | `extracted_frontend_01.md`, §2.3 — scoring.py:10 |
```

---

### Fix 3 — COVERAGE_GAP: NeurIPS gauge chart score tier labels completely absent

**Validation issue:** COVERAGE-01. The six quality tier labels (`Strong Accept`, `Accept`, `Borderline`, `Weak Reject`, `Reject`, `Strong Reject`) used by the gauge chart were entirely absent from the glossary despite being the primary domain-facing verdict vocabulary. The validator recommended adding §3.4 to the Status Enums section.

**Source evidence:** `frontend/components/gauge_chart.py:14–31` — confirmed by direct file read:
```python
if score >= 87.5:
    color_barra = "#00aa00"  # Verde oscuro - Strong Accept
    label = "Strong Accept"
elif score >= 75:
    color_barra = "#00cc44"  # Verde - Accept
    label = "Accept"
elif score >= 62.5:
    color_barra = "#ffcc00"  # Amarillo - Borderline
    label = "Borderline"
elif score >= 50:
    color_barra = "#ff9900"  # Naranja - Weak Reject
    label = "Weak Reject"
elif score >= 25:
    color_barra = "#ff4b4b"  # Rojo - Reject
    label = "Reject"
else:
    color_barra = "#cc0000"  # Rojo oscuro - Strong Reject
    label = "Strong Reject"
```
Chart title injection confirmed at line 37: `title={'text': f"Quality Score<br><sub>{label}</sub>"}`.

**Change made:** Added new §3.4 "NeurIPS Quality Tier Labels" immediately after §3.3 (before the `---` separator that precedes `## 4. Named Constants Glossary`). The new section lists all 6 tiers with score boundaries, display labels, hex colors, and per-tier source line references, plus a usage note explaining how the label is rendered in the Plotly chart.

**Before:** §3.3 ended, then `---`, then `## 4. Named Constants Glossary`.

**After:** §3.3 ends, then `---`, then new §3.4 with the full 6-tier table, then `## 4. Named Constants Glossary`.

---

### Fix 4 — COVERAGE_GAP: SEMANTIC_SCHOLAR_API_KEY constant absent from §4.7

**Validation issue:** COVERAGE-02. The `SEMANTIC_SCHOLAR_API_KEY` constant was absent from §4.7, despite its peer `GOOGLE_API_KEY` being documented there and despite the constant being referenced in 4 other spec files. The validator noted it is optional (rate-limiting context) which is important operational information.

**Source evidence:** `backend/common/config.py:31` — confirmed by direct grep:
```
30: GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
31: SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
```
Line 31 is a direct neighbour of `GOOGLE_API_KEY` at line 30. Cross-references in other specs confirmed by validation report: `01_data_model.md:200`, `03_technical_specs.md:107,269,521,530`, `07_module_index.md:128,181`, `08_dependency_graph.md:210`.

**Change made:** Added a new row for `SEMANTIC_SCHOLAR_API_KEY` immediately after the `GOOGLE_API_KEY` row in the §4.7 table. The entry documents: value expression (`os.getenv(...)`), optional nature (rate-limiting without key, `"x-api-key"` header when set), and cross-spec references.

**Before:**
```
| `GOOGLE_API_KEY` | `os.getenv("GOOGLE_API_KEY")` — runtime value from environment | Google Gemini API key. ... | `extracted_backend_core_01.md`, §2.1 — config.py:30; ... |
| `AUDIT_CONFIG` | ...
```

**After:**
```
| `GOOGLE_API_KEY` | `os.getenv("GOOGLE_API_KEY")` — runtime value from environment | Google Gemini API key. ... | `extracted_backend_core_01.md`, §2.1 — config.py:30; ... |
| `SEMANTIC_SCHOLAR_API_KEY` | `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` — runtime value from environment | Semantic Scholar API key. **Optional** — ... injected as `"x-api-key"` HTTP header ... | `backend/common/config.py:31` |
| `AUDIT_CONFIG` | ...
```

---

### Fix 5 — DEPTH_GAP: §4.1 CHECKLIST_KEYS missing NeurIPS item name column

**Validation issue:** DEPTH-01 (CHECK 4a). The §4.1 table had only `Index | Key Value | Source` columns. CHECK 4a requires each key to include its corresponding NeurIPS checklist item name (e.g., `"1. Claims"` for key `"claims"`), which was missing from §4.1 and required readers to cross-reference §2 or §4.2.

**Source evidence:** `frontend/utils/scoring.py:18–33` — the `CHECKLIST_LABELS` dict provides the exact NeurIPS item name for each key. All 16 name strings taken directly from that dict:
- `"claims"` → `"1. Claims"` (scoring.py:18)
- `"limitations"` → `"2. Limitations"` (scoring.py:19)
- ... (16 entries total through scoring.py:33)

**Change made:** Added `NeurIPS Item Name` column to the §4.1 table (between `Key Value` and `Source`). Values are the exact label strings from `CHECKLIST_LABELS` in `scoring.py:18–33`. This fix was applied as part of the same table rewrite as Fix 2 (FIDELITY-02), since both targeted the same §4.1 table.

**Before (header):**
```
| Index | Key Value | Source |
|-------|-----------|--------|
```

**After (header):**
```
| Index | Key Value | NeurIPS Item Name | Source |
|-------|-----------|-------------------|--------|
```

Example data row before:
```
| 1 | `"claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:8 |
```

Example data row after:
```
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
```
