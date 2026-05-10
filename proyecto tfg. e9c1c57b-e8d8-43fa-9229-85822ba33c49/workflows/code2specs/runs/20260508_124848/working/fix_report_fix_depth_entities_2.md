# Fix Report — fix_depth_entities_2

**Fix Agent ID:** fix_depth_entities_2
**Fix Type:** depth_fix
**Target spec:** `01_data_model.md`
**Validation report:** `validation_report_val_depth_entities.md`
**Issues resolved:** #13, #14, #15 (of 15 total)

---

## Issue #13 — Named Constants: Saturation Error Keywords — missing TYPE and per-row SOURCE

### Description (from validation report)
Depth gap #8: The Saturation Error Keywords constant table was missing an explicit Python type (`list[str]`) and a per-row SOURCE citation. Only a section-header source was provided, not an inline column in the table row.

### Entity / Field
- **Entity:** Named Constants — Saturation Error Keywords
- **Field/constant:** keyword list (inline literal `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]`)

### Evidence
**SOURCE: `frontend/components/file_uploader.py:60`**
```python
is_saturation = any(x in error_msg.upper() for x in ["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"])
```
The literal is a Python `list[str]` passed as the second argument to `any()` via a generator expression. The constant is defined inline at this exact line.

### Change applied (before → after)

**Before:**
```markdown
| Constant Name | Value | Usage Context |
|---|---|---|
| Saturation error keywords (list) | `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` | Checked `in error_msg.upper()` to classify backend error as saturation vs hard failure |
```

**After:**
```markdown
| Constant Name | Value | Type | Usage Context | Source |
|---|---|---|---|---|
| Saturation error keywords (list) | `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` | `list[str]` | Checked `in error_msg.upper()` to classify backend error as saturation vs hard failure | `file_uploader.py:60` |
```

**What changed:** Added `Type` column (`list[str]`) and `Source` column (`file_uploader.py:60`) to the table. No other rows or sections were modified.

---

## Issue #14 — Named Constants: Checklist Priority Items — missing TYPE

### Description (from validation report)
Depth gap #9: The `priority_items` local list in the Checklist Verification Priority Items table was missing an explicit Python type annotation (`list[str]`).

### Entity / Field
- **Entity:** Named Constants — Checklist Verification Priority Items
- **Field/constant:** `priority_items` (local variable in `ChecklistVerificationSkill.execute`)

### Evidence
**SOURCE: `backend/skills/auditor_skills.py:340-344`**
```python
priority_items = [
    'claims', 'experimental_result_reproducibility', 'open_access_data_code',
    'experimental_setting_details', 'experiments_compute_resource',
    'experiment_statistical_significance', 'licenses', 'declaration_llm_usage'
]
```
All elements are string literals, confirming Python type `list[str]`.

### Change applied (before → after)

**Before:**
```markdown
| Constant Name | Value | Source |
|---|---|---|
| `priority_items` (local list in `ChecklistVerificationSkill.execute`) | `['claims', 'experimental_result_reproducibility', ...]` | `auditor_skills.py:340` |
```

**After:**
```markdown
| Constant Name | Value | Type | Source |
|---|---|---|---|
| `priority_items` (local list in `ChecklistVerificationSkill.execute`) | `['claims', 'experimental_result_reproducibility', ...]` | `list[str]` | `auditor_skills.py:340` |
```

**What changed:** Added `Type` column (`list[str]`). No other rows or sections were modified.

---

## Issue #15 — Named Constants: NeurIPS Quality Score Tiers and Compliance Table Row Colors — missing per-row TYPE and SOURCE

### Description (from validation report)
Depth gap #10: Both the NeurIPS Quality Score Tiers table and the Compliance Table Row Colors table lacked per-row TYPE and SOURCE line references. Only a section-level source range was provided.

### Entity / Field
- **Entity 1:** Named Constants — NeurIPS Quality Score Tiers
- **Entity 2:** Named Constants — Compliance Table Row Colors

### Evidence — NeurIPS Quality Score Tiers
**SOURCE: `frontend/components/gauge_chart.py:14-31`**
```python
14    if score >= 87.5:
15        color_barra = "#00aa00"  # Verde oscuro - Strong Accept
16        label = "Strong Accept"
17    elif score >= 75:
18        color_barra = "#00cc44"  # Verde - Accept
19        label = "Accept"
20    elif score >= 62.5:
21        color_barra = "#ffcc00"  # Amarillo - Borderline
22        label = "Borderline"
23    elif score >= 50:
24        color_barra = "#ff9900"  # Naranja - Weak Reject
25        label = "Weak Reject"
26    elif score >= 25:
27        color_barra = "#ff4b4b"  # Rojo - Reject
28        label = "Reject"
29    else:
30        color_barra = "#cc0000"  # Rojo oscuro - Strong Reject
31        label = "Strong Reject"
```
`label` and `color_barra` are both `str`. Each tier maps to a 2-line block at the confirmed line numbers.

### Evidence — Compliance Table Row Colors
**SOURCE: `frontend/components/audit_results.py:18-32`**
```python
18    def row_bg(item):
19        # 1. Rojo: "No" sin justificación (Riesgo Crítico de Desk Reject)
20        if item["pending_justification"]:
21            return "#450a0a"
22
23        # 2. Ámbar/Naranja: Advertencia
24        if item["missing_evidence"] or (item.get("alert_msg") and item["alert_msg"].strip()):
25            return "#452e0a"
26
27        a = item["answer"].strip().lower()
28        if "yes" in a:
29            return "#064e3b"  # Verde Esmeralda (Todo OK)
30
31        # Para el resto (No justificado o N/A sin alertas), fondo neutro
32        return "#111827"
```
All return values are `str` (hex color strings). Each condition maps to the confirmed line numbers.

### Changes applied (before → after)

**NeurIPS Quality Score Tiers — Before:**
```markdown
| Score Range | Label | Bar Color |
|---|---|---|
| `[87.5, 100]` | `"Strong Accept"` | `"#00aa00"` |
| `[75, 87.5)` | `"Accept"` | `"#00cc44"` |
| `[62.5, 75)` | `"Borderline"` | `"#ffcc00"` |
| `[50, 62.5)` | `"Weak Reject"` | `"#ff9900"` |
| `[25, 50)` | `"Reject"` | `"#ff4b4b"` |
| `[0, 25)` | `"Strong Reject"` | `"#cc0000"` |
```

**NeurIPS Quality Score Tiers — After:**
```markdown
| Score Range | Label | Bar Color | Type (Label / Color) | Source |
|---|---|---|---|---|
| `[87.5, 100]` | `"Strong Accept"` | `"#00aa00"` | `str` / `str` | `gauge_chart.py:14-16` |
| `[75, 87.5)` | `"Accept"` | `"#00cc44"` | `str` / `str` | `gauge_chart.py:17-19` |
| `[62.5, 75)` | `"Borderline"` | `"#ffcc00"` | `str` / `str` | `gauge_chart.py:20-22` |
| `[50, 62.5)` | `"Weak Reject"` | `"#ff9900"` | `str` / `str` | `gauge_chart.py:23-25` |
| `[25, 50)` | `"Reject"` | `"#ff4b4b"` | `str` / `str` | `gauge_chart.py:26-28` |
| `[0, 25)` | `"Strong Reject"` | `"#cc0000"` | `str` / `str` | `gauge_chart.py:29-31` |
```

**Compliance Table Row Colors — Before:**
```markdown
| Condition | Background Color | Meaning |
|---|---|---|
| `pending_justification == True` | `"#450a0a"` | Critical risk (deep red) |
| `missing_evidence == True` OR `alert_msg` non-empty | `"#452e0a"` | Warning (amber/orange) |
| `"yes" in answer.lower()` | `"#064e3b"` | OK (emerald green) |
| All other cases | `"#111827"` | Neutral (dark) |
```

**Compliance Table Row Colors — After:**
```markdown
| Condition | Background Color | Meaning | Type | Source |
|---|---|---|---|---|
| `pending_justification == True` | `"#450a0a"` | Critical risk (deep red) | `str` | `audit_results.py:20-21` |
| `missing_evidence == True` OR `alert_msg` non-empty | `"#452e0a"` | Warning (amber/orange) | `str` | `audit_results.py:24-25` |
| `"yes" in answer.lower()` | `"#064e3b"` | OK (emerald green) | `str` | `audit_results.py:28-29` |
| All other cases | `"#111827"` | Neutral (dark) | `str` | `audit_results.py:32` |
```

**What changed:** Added `Type (Label / Color)` and `Source` columns to the NeurIPS tiers table; added `Type` and `Source` columns to the Compliance colors table. No other rows, sections, or surrounding content were modified.

---

## Summary

| Issue | Entity | Field | Fix Applied | Evidence |
|---|---|---|---|---|
| #13 | Named Constants — Saturation Error Keywords | keyword list | Added `Type` (`list[str]`) and `Source` (`file_uploader.py:60`) columns | `file_uploader.py:60` confirmed in context |
| #14 | Named Constants — Checklist Priority Items | `priority_items` | Added `Type` (`list[str]`) column | `auditor_skills.py:340-344` confirmed in context |
| #15 | Named Constants — NeurIPS Quality Score Tiers | all 6 tier rows | Added `Type (Label / Color)` and `Source` per-row columns | `gauge_chart.py:14-31` confirmed in context |
| #15 | Named Constants — Compliance Table Row Colors | all 4 condition rows | Added `Type` and `Source` per-row columns | `audit_results.py:18-32` confirmed in context |

All evidence gates passed. No `[GAP_ID: hall_*]` markers were touched. No other sections modified.
