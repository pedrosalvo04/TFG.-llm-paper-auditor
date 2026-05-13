# 04 — Look & Feel Specification
## NeurIPS 2026 Checklist Auditor

**Document type:** Look & Feel Specification  
**Target pipeline:** Specs2Code  
**Source extractions:** extracted_frontend_01.md, extracted_root_tests_scratch_01.md, cross_ref_resolution_cross_ref_root_to_frontend.md  

---

## 1. Page Configuration

The application is a single-page Streamlit app. `st.set_page_config()` is called as the very first Streamlit statement, before any widget-touching imports.

| Parameter | Value |
|-----------|-------|
| `page_title` | `"NeurIPS 2026 Checklist Auditor"` |
| `layout` | `"wide"` |
| `page_icon` | `"🔬"` |

No additional `st.set_page_config` parameters are present beyond the three above.

Source: extracted_frontend_01.md § 2.2 (app.py:6-10)

> **Note on cross-cluster discrepancy:** extracted_root_tests_scratch_01.md § 3.2 (app.py:25-29) documents a root-level entry point with `page_title="Nature Auditor Pro"`. The authoritative frontend module (`frontend/app.py`) uses `page_title="NeurIPS 2026 Checklist Auditor"` (extracted_frontend_01.md § 2.2). The root app.py is a separate, older entry point. The frontend/app.py value is canonical for this specification.

Source: extracted_frontend_01.md § 2.2; cross-noted in extracted_root_tests_scratch_01.md § 3.2

---

## 2. Sidebar Layout

Rendering order inside `with st.sidebar:` (top to bottom):

1. **ACM Logo Image**
   - Widget: `st.image(SIDEBAR_IMAGE, width=150)`
   - `SIDEBAR_IMAGE` constant value (exact):  
     `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"`
   - Width parameter: `150` (integer, pixels)
   - No caption parameter is set.
   - Source: extracted_frontend_01.md § 2.1 (config.py:4); § 4.3 (app.py:73)

2. **Section Header**
   - Widget: `st.markdown("### Sobre el TFG")`
   - Exact string: `"### Sobre el TFG"`
   - Source: extracted_frontend_01.md § 4.3 (app.py:74)

3. **Description Text**
   - Widget: `st.write(SIDEBAR_DESCRIPTION)`
   - `SIDEBAR_DESCRIPTION` constant value (exact):  
     `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."`
   - Source: extracted_frontend_01.md § 2.1 (config.py:5); § 4.3 (app.py:75)

No other sidebar widgets, dividers, or sections are present.

Source: extracted_frontend_01.md § 4.3 (app.py:73-76); cross_ref_resolution_cross_ref_root_to_frontend.md § g_008

---

## 3. File Upload Widget

### 3.1 Widget Definition

| Attribute | Value |
|-----------|-------|
| Widget function | `st.file_uploader` |
| Label text (exact) | `"Sube el PDF del artículo científico"` |
| `type` (accepted extensions) | `["pdf", "txt", "md"]` |
| `accept_multiple_files` | Not set (default `False`) |
| `key` | Not explicitly set — no `key=` argument in source (app.py:34); Streamlit auto-assigns key at runtime |

Source: extracted_frontend_01.md § 5.1 (app.py:34)

### 3.2 Processing Status Widget Sequence

When a new file is detected (deduplication condition is True), the following widget sequence is rendered inside `process_uploaded_file()`:

**Step 1 — Text extraction spinner:**
- Widget: `st.spinner("📂 Extrayendo texto...")`
- Exact spinner label: `"📂 Extrayendo texto..."`
- Active during: PDF-to-Markdown conversion or TXT/MD file read.
- Source: extracted_frontend_01.md § 5.1 (file_uploader.py:34)

**Step 2 — Audit status widget:**
- Widget: `st.status("🧠 Analizando el documento...", expanded=True)`
- Exact initial label: `"🧠 Analizando el documento..."`
- `expanded=True` on creation.
- During analysis: a nested `update_status(msg)` callback calls `st.write(msg)` inside this status block (source: file_uploader.py:46-47).
- Source: extracted_frontend_01.md § 5.1 (file_uploader.py:45)

**Step 3 — Success state:**
- Transitions the status widget: `status.update(label="✅ Análisis completado", state="complete", expanded=False)`
- Then renders: `st.success("✅ Análisis completado")`
- Source: extracted_frontend_01.md § 5.1 (file_uploader.py:90, 92)

**Step 4 — Error states (saturation):**
- `status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)`
- `st.error("### ⚠️ El servicio de IA está saturado")`
- Expander wrapping the detail text: `st.expander("🔍 Detalles técnicos y solución", expanded=True)` (Source: file_uploader.py:66). Inside the expander:
  - `st.write("El modelo Gemini está experimentando una demanda extremadamente alta en este momento y no ha podido completar la tarea tras 5 reintentos automáticos.")`
  - `st.info("Este es un problema temporal de Google. Puedes esperar unos minutos e intentar reanudar, o cancelar la ejecución actual.")`
- Two buttons rendered in a 2-column layout (`st.columns(2)`):
  - Left column: `st.button("🔄 Reintentar ahora", use_container_width=True)` — no `key=` parameter in source (file_uploader.py:72); triggers `st.rerun()` on click.
  - Right column: `st.button("🚫 Cancelar ejecución", use_container_width=True)` — no `key=` parameter in source (file_uploader.py:75); sets `st.session_state.resultado` to cancellation error dict and calls `st.stop()`.
- Source: file_uploader.py:56-88 (confirmed lines 62-79)

**Step 5 — Error state (non-saturation critical failure):**
- `status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)`
- `st.error(f"❌ Error crítico: {error_msg}")`
- Source: extracted_frontend_01.md § 8 RULE: SaturationErrorDetection (file_uploader.py:56-88)

### 3.3 Dynamic Visibility

The entire audit results section (and all sections below it) is rendered only when `uploaded_file is not None` — i.e., the conditional block `if uploaded_file:` in app.py gates all downstream rendering.

Source: extracted_frontend_01.md § 4.2 (app.py:37)

### 3.4 Post-Processing Error Handling Branches (app.py lines 40–70)

After `process_uploaded_file()` returns `(md_text, resultado)`, `app.py` evaluates three mutually exclusive error branches before rendering audit results. These branches produce user-facing UI elements and must be implemented by any rebuild.

**Branch A — `"error"` key present in resultado (app.py:40–45)**

Condition: `resultado and "error" in resultado`

- Sub-branch A1 — INVALID_PAPER_TYPE:
  - Condition: `err == "INVALID_PAPER_TYPE"` where `err = resultado["error"]`
  - Widget: `st.error(f"❌ Paper no válido: {resultado.get('message', 'Solo se evalúan papers de ML/AI')}")`
  - Exact fallback message string: `'Solo se evalúan papers de ML/AI'`
  - Source: frontend/app.py:42–43

- Sub-branch A2 — Generic error:
  - Condition: `err != "INVALID_PAPER_TYPE"` (else clause)
  - Widget: `st.error(f"❌ Error en la auditoría: {err}")`
  - Source: frontend/app.py:44–45

**Branch B — `"evaluation_error"` key present in resultado (app.py:46–49)**

Condition: `resultado and "evaluation_error" in resultado` (elif, only reached if Branch A was not taken)

Three widgets rendered in sequence:
1. `st.error(f"❌ Error del LLM: {resultado['evaluation_error']}")` — Source: frontend/app.py:47
2. `st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")` — Source: frontend/app.py:48
3. `st.info("💡 Tip: Recarga la página o sube el archivo nuevamente.")` — Source: frontend/app.py:49

**Branch C — resultado present but `resultado.get("claims")` is falsy (app.py:66–70)**

Condition: `resultado` is truthy but does not contain `"claims"` key (elif, reached only if Branches A and B were not taken and the `claims` branch at line 50 was also not taken)

- Sub-branch C1 — resultado is truthy but claims absent:
  - Condition: `elif resultado:` (app.py:66)
  - `st.error("⚠️ La auditoría no generó resultados válidos.")` — Source: frontend/app.py:67
  - `st.info("Posibles causas: respuesta vacía del LLM o JSON inválido.")` — Source: frontend/app.py:68

- Sub-branch C2 — resultado is falsy (None or empty):
  - Condition: `else:` (app.py:69)
  - `st.warning("⚠️ No hay resultado disponible.")` — Source: frontend/app.py:70

**Branch D — Valid result with `claims` (app.py:50–65)**

Condition: `resultado and resultado.get("claims")` — this is the happy path that triggers render_audit_results, render_sota_analysis, render_chatbot, and the download section (see §4, §6, §7, §8).

Source: frontend/app.py:40–70

---

## 4. Audit Results Page Layout

Rendered by `render_audit_results(resultado: dict, uploaded_file) -> health: dict`.

Source: extracted_frontend_01.md § 5.2 (audit_results.py:90)

### 4a. Success Banner

- Widget: `st.success("Auditoria Finalizada")`
- Exact message text: `"Auditoria Finalizada"` (no accent on "Auditoria")
- No additional icon parameter (Streamlit's default success icon is used).
- This is the first widget rendered inside `render_audit_results`.
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:92)

### 4b. Health Verdict Block

- Section header: `st.header("Veredicto del Checklist NeurIPS 2026")`
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:100)

Data field driving verdict: `health["status"]` (string, either `"valid"` or `"risk"`), where `health` is the return value of `get_checklist_health(resultado)`.

**Valid state:**
- Condition: `health["status"] == "valid"` (i.e., `pending_count == 0`)
- Rendered as a dark-green styled `<div>` (HTML injected via st.html or st.markdown with `unsafe_allow_html=True`)
- Primary text: `"Checklist Valido"`
- Sub-text (exact): `"Todas las respuestas tienen evidencia o justificacion documentada. El checklist esta listo para NeurIPS."`
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:102-109)

**Risk state:**
- Condition: `health["status"] == "risk"` (i.e., `pending_count > 0`)
- Rendered as a dark-red styled `<div>`
- Primary text: `"Riesgo de Desk Reject"`
- Sub-text (exact template): `"{pending} de {total} item(s) requieren accion del autor antes del envio."` where `pending = health["pending_count"]` and `total = health["total"]`
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:111-117)

### 4c. 4-Column Metrics Row

Rendered with `st.columns(4)` pattern (4 equal columns). Each column contains one `st.metric` call.

| Column | Metric Label (exact) | Value Source | Format | Source |
|--------|---------------------|--------------|--------|--------|
| col1 | `"Items Yes"` | Count of items in `health["items"]` where `"yes" in item["answer"].lower()` | Integer (count) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |
| col2 | `"Items No"` | Count of items in `health["items"]` where `"no" in item["answer"].lower()` | Integer (count) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |
| col3 | `"Items N/A"` | Count of items in `health["items"]` where `"n/a" in item["answer"].lower()` | Integer (count) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |
| col4 | `"Tiempo"` | `resultado.get("metricas", {}).get("tiempo_segundos", "N/A")` | `f"{tiempo}s"` (string) | extracted_frontend_01.md § 5.2 (audit_results.py:121-133) |

No `delta` or `help` parameters are set on any of the four `st.metric` calls.

> **GAP — `tiempo_segundos`, `caracteres_leidos`, `red_flags_detectadas`, gauge score column:**  
> The extraction documents exactly 4 columns: Items Yes, Items No, Items N/A, Tiempo (from `metricas.tiempo_segundos`). The keys `caracteres_leidos` and `red_flags_detectadas` do not appear in the audit_results.py metrics row extraction. A gauge-based score column is NOT documented as part of the 4-column metrics row — the `create_gauge_chart` function is defined in `gauge_chart.py` but its call site is absent from the 14-file cluster (see GAP-ext_frontend_01-001). `[GAP: call site for create_gauge_chart not found in frontend cluster — gauge may be rendered outside the 4-column metrics row or in a caller not present in the extraction]`

Source: extracted_frontend_01.md § 5.2 (audit_results.py:121-133)

### 4d. RAG Ficha Técnica Section

- Subheader: `st.subheader("🎯 Ficha Técnica de Entrenamiento (RAG Specialist)")`
- Visibility condition: rendered only if `resultado.get("extracted_hyperparameters_hybrid", {})` is truthy.
- Caption (exact): `st.caption("Estos datos han sido extraídos mediante un escaneo profundo (RAG) de las secciones técnicas y apéndices.")`
- Layout: 4 equal columns (c1, c2, c3, c4).

| Column | Fields (in order) | Widget | Value Source | Conditional |
|--------|-------------------|--------|--------------|-------------|
| c1 | `optimizer` | `st.code` | `rag_data.get("optimizer", "N/A")` | Always if section visible |
| c1 | `learning_rate` | `st.code` | `rag_data.get("learning_rate", "N/A")` | Always if section visible |
| c2 | `batch_size` | `st.code` | `rag_data.get("batch_size", "N/A")` | Always if section visible |
| c2 | `epochs` | `st.code` | `rag_data.get("epochs", "N/A")` | Always if section visible |
| c3 | `warmup_steps` | `st.code` | `rag_data.get("warmup_steps", "N/A")` | Always if section visible |
| c3 | `weight_decay` | `st.code` | `rag_data.get("weight_decay", "N/A")` | Always if section visible |
| c4 | `hardware` | `st.info` | `rag_data.get("hardware", "N/A")` | Always if section visible |
| c4 | `random_seed` | `st.code` | `rag_data.get("random_seed", "N/A")` | Only if `rag_data.get("random_seed") and rag_data.get("random_seed") != "NOT FOUND"` |

Where `rag_data = resultado.get("extracted_hyperparameters_hybrid", {})`.

No expander wraps this section; it is rendered inline.

Source: extracted_frontend_01.md § 5.2 (audit_results.py:136-163)

### 4e. Compliance Table

See Section 5 below for full detail.

Section header: `st.header("Tabla de Cumplimiento NeurIPS 2026")`  
Caption with colour legend is shown before the table.  
Table is rendered via `st.html(_build_table_html(health["items"]))`.

Source: extracted_frontend_01.md § 5.2 (audit_results.py:167-175)

### 4f. Three Expander Sections

Rendered in this exact order (1st, 2nd, 3rd):

**1st Expander — Pipeline de Análisis Profundo**
- `st.expander` label (exact): `"🔍 Pipeline de Análisis Profundo (Map-Reduce + CoT + Context Mapping)"`
- Content (in order):
  1. Chain-of-Thought: `cot = resultado.get("informacion_extraida", {}).get("thought_process", "No disponible")`; rendered as `st.info(cot)`.
  2. Context Mapping: reads `resultado.get("informacion_extraida", {}).get("context_mapping", [])`. If non-empty: renders items in columns (up to 5 per row). If empty: `st.warning("No se ha podido mapear la estructura de secciones.")`.
  3. Comparativa Map vs Reduce (2 sub-columns):
     - Left (MAP): reads `resultado.get("general_analysis_map", [])`. If non-empty: iterates and renders each step in nested `st.expander(f"📦 Fragmento {i+1}")` with `st.json(step)`. Else: renders `resultado.get("original_extraction_raw", {})` as `st.json(...)`.
     - Right (REDUCE): renders `resultado.get("informacion_extraida", {})` as `st.json(...)`.
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:179-215)

**2nd Expander — Pipeline de Extracción Híbrida**
- `st.expander` label (exact): `"🔍 Pipeline de Extracción Híbrida (RAG Specialist)"`
- Content (in order):
  1. Left (Triage MAP): reads `resultado.get("hybrid_triage_fragments", [])`. If non-empty: iterates; for each fragment:
     - Reads `_relevance_score` (default `"N/A"`).
     - Background colour: `"#065f46"` if `isinstance(relevance, int) and relevance > 70`; else `"#1e3a5f"`.
     - Expander title: `f"📄 Fragmento Técnico {i+1} (Relevancia: {relevance}%)"`.
     - Inside: relevance badge, `_chunk_text` via `st.caption(...)`, then all non-underscore-prefixed fields via `st.json(...)`.
  2. Right (REDUCE): renders `resultado.get("extracted_hyperparameters_hybrid", {})` as `st.json(...)`.
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:218-242)

**3rd Expander — Pipeline de Evaluación**
- `st.expander` label (exact): `"🔍 Pipeline de Evaluación (Senior Area Chair + Self-Correction)"`
- Content (in order):
  1. Evaluation Signals: reads `resultado.get("evaluation_signals", {})`. If truthy: iterates dict items; for each key `k`, renders `st.markdown(f"**Item {k.replace('_', ' ').title()}:**")` then `st.info(msg)`. If falsy: `st.warning(...)` (exact text not extracted).
  2. Self-Correction verification details: collects items from `resultado` where value is a dict with `v.get('verified')` True. Falls back to second-level scanning. For each verified item:
     - Status label: `"✨ Corregido"` if `data.get('was_corrected')`, else `"✅ Confirmado"`.
     - Shown in `st.expander(...)` with answer, justification (`st.write`), and evidence (`st.code`).
- Source: extracted_frontend_01.md § 5.2 (audit_results.py:245-283)

---

## 5. Compliance Table (Columns, Risk Annotations)

Produced by `_build_table_html(items: list) -> str`.  
Source: extracted_frontend_01.md § 5.2.1 (audit_results.py:7-87)

### 5.1 Column Definition

| Column # | Header Text (exact) | Data Field | HTML Element |
|----------|---------------------|------------|--------------|
| 1 | `"#"` | `item["label"].split(". ")[0]` (numeric part, e.g. `"1"`) | `<th>` then `<td>` |
| 2 | `"Item del Checklist"` | `item["label"].split(". ")[1]` (name part, e.g. `"Claims"`) | `<td>` |
| 3 | `"Respuesta"` | Badge HTML derived from `item["answer"]` (see §5.2) | `<td>` |
| 4 | `"Evidencia / Justificacion"` | Evidence + alert HTML (see §5.3) | `<td>` |

Label splitting logic: `item["label"]` is split on `". "`. If `". "` is not present, `str(idx)` is used as `num` and the full label as `name`. Source: audit_results.py:39-42.

### 5.2 Badge Styles (Column 3 — Respuesta)

Applied based on `item["answer"].lower()`:

| Condition | Background Color | Text Color | Displayed Text |
|-----------|-----------------|------------|----------------|
| `"yes" in answer.lower()` | `#065f46` | `#6ee7b7` | `"Yes"` |
| `"no" in answer.lower()` | `#7f1d1d` | `#fca5a5` | `"No"` |
| all other (N/A or empty) | `#1e3a5f` | `#93c5fd` | `"N/A"` |

Source: extracted_frontend_01.md § 2.6 (audit_results.py:10-16)

### 5.3 Row Background Colors (Conditional Formatting)

Applied to each `<tr>` based on risk flags in the item dict:

| Priority | Condition | Background Color | Semantic Meaning |
|----------|-----------|-----------------|-----------------|
| 1 (highest) | `item["pending_justification"] == True` | `#450a0a` | Deep red — Critical risk (No without justification) |
| 2 | `item["missing_evidence"] == True` OR `item["alert_msg"]` is non-empty (for other alert types) | `#452e0a` | Amber/orange — Warning |
| 3 | `"yes" in item["answer"].lower()` | `#064e3b` | Emerald green — OK |
| 4 (default) | All other cases | `#111827` | Neutral dark |

Source: extracted_frontend_01.md § 2.5 (audit_results.py:18-32)

### 5.4 Evidence Cell (Column 4) HTML

**When `evidence_text` is non-empty** (i.e., `item["evidence"]` exists and is not `"-"`):
```html
<span style="color:#d1d5db;">{evidence_text}</span>
```

**When `evidence_text` is empty:**
```html
<em style="color:#6b7280;">No disponible</em>
```

Source: extracted_frontend_01.md § 5.2.1 (audit_results.py:44, 48)

### 5.5 Alert Lines (Appended to Column 4 Cell)

**Alert line 1 — `pending_justification` is True:**
```html
<div style="color:#fca5a5;">&#9888; Sin justificacion del autor &mdash; Riesgo de Desk Reject</div>
```
(Full inline style extracted as: `color:#fca5a5;` with additional styling not fully detailed in extraction.)  
Source: audit_results.py:52-53

**Alert line 2 — `missing_evidence` is True:**
```html
<div style="color:#fde68a;">&#9888; Respuesta Yes sin evidencia de seccion del paper</div>
```
Source: audit_results.py:54-55

**Alert line 3 — Ethics alert (additionally appended when `"compensacion" in item["alert_msg"].lower()` OR `"etica" in item["alert_msg"].lower()`):**
```html
<div style="color:#fde68a;">&#9888; NeurIPS Code of Ethics: compensacion minima obligatoria</div>
```
Source: audit_results.py:57-58

### 5.6 Full HTML Table Structure

```html
<table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
  <thead>
    <tr>
      <th>#</th>
      <th>Item del Checklist</th>
      <th>Respuesta</th>
      <th>Evidencia / Justificacion</th>
    </tr>
  </thead>
  <tbody>
    <!-- One <tr> per item in health["items"] (16 rows total) -->
    <tr style="background-color:{row_bg};">
      <td>{num}</td>
      <td>{name}</td>
      <td>{badge_html}</td>
      <td>{evidence_html}{alert_html}</td>
    </tr>
    ...
  </tbody>
</table>
```

Source: extracted_frontend_01.md § 5.2.1 (audit_results.py:69-87)

---

## 6. Download Report Button

| Attribute | Value |
|-----------|-------|
| Widget function | `st.download_button` |
| Label text (exact) | `"📥 Descargar Informe Completo (.md)"` |
| `file_name` format (exact) | `f"auditoria_neurips_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"` |
| `mime` type | `"text/markdown"` |
| `data` (file content) | The string returned by `generate_report(resultado, uploaded_file, puntuacion)` — a Markdown-formatted audit report |
| `key` parameter | Not explicitly set — no `key=` argument in source (app.py:60–64); Streamlit auto-assigns key at runtime |

**Placement in layout:** Rendered after `render_chatbot(md_text)` call, inside the `if uploaded_file:` block, only when `resultado.get("claims")` is truthy. Preceded by `st.markdown("---")` and `st.subheader("📄 Descargar Informe")` (Source: frontend/app.py:57–58).

Source: extracted_frontend_01.md § 4.2 (app.py:57-65); extracted_root_tests_scratch_01.md § 3.5 (app.py:73-79); cross_ref_resolution_cross_ref_root_to_frontend.md § g_006

**File content source:** `generate_report(resultado, uploaded_file, health=None)` produces a Markdown string with this structure:
1. `# NeurIPS 2026 Checklist Audit Report`
2. `**Paper:** {uploaded_file.name}`
3. `**Veredicto:** {status_label}` — either `"Checklist Valido"` or `"Riesgo de Desk Reject"`
4. `**Items con problemas:** {pending} de {total}`
5. `---`
6. `## Tabla de Cumplimiento` — Markdown table with header `| # | Item | Respuesta | Evidencia / Justificacion |`
7. 16 data rows — each row appends a risk note: `" [RIESGO: sin justificacion]"` if `pending_justification`, or `" [RIESGO: sin evidencia]"` if `missing_evidence`, otherwise no note.
8. Footer: `_Generado por Auditor NeurIPS 2026._`

Source: extracted_frontend_01.md § 5.2.2 (audit_results.py:287-316); cross_ref_resolution_cross_ref_root_to_frontend.md § g_006

---

## 7. SOTA Analysis Section

Rendered by `render_sota_analysis(md_text: str) -> None`.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:5); cross_ref_resolution_cross_ref_root_to_frontend.md § g_007

### 7.1 Section Header and Divider

1. `st.markdown("---")` — horizontal divider above the section.
2. `st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")` — exact string.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:5)

### 7.2 Trigger Button

- Widget: `st.button("Ejecutar Análisis de Literatura Reciente")`
- Label (exact): `"Ejecutar Análisis de Literatura Reciente"`
- No `key=` parameter in source (sota_section.py:10); Streamlit auto-assigns key at runtime.
- The entire analysis block (spinner, results) is rendered conditionally on this button press.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:10)

### 7.3 Spinner During SOTA Fetch

- Widget: `st.spinner("Conectando con Semantic Scholar y validando bibliografía...")`
- Exact spinner text: `"Conectando con Semantic Scholar y validando bibliografía..."`
- Wraps the `st.session_state.sota_analyzer.analyze_sota(md_text)` call.

Source: extracted_frontend_01.md § 5.5 (sota_section.py:12)

### 7.4 Post-Fetch Success Display (when `"error" not in resultado_sota`)

1. `st.success("Análisis completado")` — exact text.
2. Conclusion section:
   - `st.markdown("### 📝 Conclusión")`
   - `st.info(resultado_sota.get('conclusion_sota', ''))` — content from `conclusion_sota` key.
3. Papers dataframe and missing-paper recommendations rendered by `_render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)` — see §7.5.
   - Only called when `not df_papers.empty and papers_omitidos` both true.
   - If `not papers_omitidos`: renders `st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")`.

### 7.5 Missing Papers Recommendations Sub-section

Header: `st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")`  
Caption: `st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")`  

Papers displayed as `st.dataframe` with these columns and column configs:

| Column Name | Config Type | Width |
|-------------|-------------|-------|
| `"Título"` | TextColumn | `"large"` |
| `"Autores"` | TextColumn | `"medium"` |
| `"Año"` | NumberColumn | `"small"` |
| `"Posterior"` (label: `"Posterior al tuyo"`) | TextColumn | `"small"` |
| `"Citas"` | NumberColumn | `"small"` |
| `"Relevancia"` | TextColumn | `"small"` |
| `"Subtema"` | TextColumn | `"medium"` |
| `"Justificación"` | TextColumn | `"large"` |

Source: extracted_frontend_01.md § 5.5.1 (sota_section.py:85-101)

**`"Posterior"` cell values:**
- `"✅ Sí"` — when `año_paper_estudiado AND paper['year'] > año_paper_estudiado`
- `"❌ No"` — when `año_paper_estudiado AND NOT (paper['year'] > año_paper_estudiado)`
- `"?"` — when `not año_paper_estudiado`

**Sort order:** Not explicitly specified in extraction. `[GAP: sort order of the papers dataframe not extracted]`

**Footer captions (conditional):**
- When `año_paper_estudiado` is truthy: `st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")`
- When falsy: `st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")`

If `df_no_citados` is empty: `st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")`

Source: extracted_frontend_01.md § 5.5.1 (sota_section.py:31-108)

### 7.6 Error Display

When `"error" in resultado_sota`:
- `st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")`

Source: extracted_frontend_01.md § 5.5 (sota_section.py:29)

### 7.7 Conditional Visibility

The entire analysis (results, dataframe, recommendations) is only shown after the button is clicked (standard Streamlit button stateless pattern — renders on the same rerun as the button press).

---

## 8. Chatbot Interface

Rendered by `render_chatbot(md_text: str) -> None`.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:4); cross_ref_resolution_cross_ref_root_to_frontend.md § g_007, § g_027

### 8.1 Section Header and Divider

1. `st.markdown("---")` — horizontal divider.
2. `st.header("💬 Pregunta al Revisor")` — exact header string.
3. `st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")` — exact caption string.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:4-9)

### 8.2 Conversation History Display

- Iterates `st.session_state.messages` (a list of `{"role": str, "content": str}` dicts).
- For each message: `st.chat_message(message["role"])` container wrapping `st.markdown(message["content"])`.
- Roles present at runtime: `"user"` and `"assistant"`.
- Message template (how history is built for the chatbot backend, not for display): `f"{m['role']}: {m['content']}"` — applied to the last 4 messages joined with `"\n"` to form `history_str`.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:10-12, 23)

### 8.3 Text Input Widget

| Attribute | Value |
|-----------|-------|
| Widget function | `st.text_input` |
| Label (exact) | `"Escribe tu pregunta:"` |
| `key` | `"chat_input"` |
| `placeholder` (exact) | `"Ej: ¿En qué página falla el paper en su estadística?"` |

Source: extracted_frontend_01.md § 5.3 (chatbot.py:14-18)

### 8.4 Submit Button Widget

| Attribute | Value |
|-----------|-------|
| Widget function | `st.button` |
| Label (exact) | `"Enviar"` |
| `key` | `"send_button"` |

Submit guard rule: the chatbot backend is called only when `st.button("Enviar")` AND `prompt_usuario` is truthy (non-empty input). A button click with empty input is silently ignored.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:20); § 8 RULE: ChatSubmitGuard

### 8.5 On-Submit Spinner

- Widget: `st.spinner("El revisor está analizando tu consulta...")`
- Exact text: `"El revisor está analizando tu consulta..."`
- Wraps the `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` call.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:24-26)

### 8.6 Session State Keys (Link to g_027 — `initialize_session_state`)

The chatbot interface depends on these session state keys:

| Key | Type | Default Value (from `initialize_session_state`) | Set/Modified By | Read By |
|-----|----|---|---|---|
| `messages` | `list` of `{"role": str, "content": str}` dicts | `[]` | `session_state.py:20-21` (init); `file_uploader.py:21` (reset on new file); `chatbot.py:21,28` (appends) | `chatbot.py:10, 23` |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | `session_state.py:14-15` (init only) | `chatbot.py:26` |

Guard condition in `initialize_session_state`: `if "key" not in st.session_state` — idempotent, never overwrites existing values.

Source: cross_ref_resolution_cross_ref_root_to_frontend.md § g_027 (session_state.py:7)

### 8.7 Post-Submit Flow

1. Append `{"role": "user", "content": prompt_usuario}` to `st.session_state.messages`.
2. Build `history_str` from last 4 messages: `"\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])`.
3. Call `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` → `respuesta_ia`.
4. Append `{"role": "assistant", "content": respuesta_ia}` to `st.session_state.messages`.
5. Call `st.rerun()` to refresh conversation display.

Source: extracted_frontend_01.md § 5.3 (chatbot.py:21-29)

---

## 9. Gauge Chart (Quality Tiers and Colors)

Defined in `frontend/components/gauge_chart.py`.

Source: extracted_frontend_01.md § 5.4 and § 2.4 (gauge_chart.py:4-71)

### 9.1 Function Signature

```
create_gauge_chart(score: float) -> plotly.graph_objects.Figure
```

- Parameter: `score` — numeric value in range [0, 100].
- Return type: `plotly.graph_objects.Figure`.
- Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:4)

### 9.2 Plotly Figure Type

- Figure type: `go.Figure(go.Indicator(...))`
- Indicator mode: `"gauge+number"`
- `value`: `score`
- `domain`: `{'x': [0, 1], 'y': [0, 1]}`

Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:33-71)

### 9.3 NeurIPS Quality Tier Thresholds and Colors

The tier determines both `label` (title sub-text) and `color_barra` (gauge bar color).

| Tier Label | Score Min (inclusive) | Score Max (exclusive, except last) | Bar Color (hex) | Color Name |
|-----------|-----------------------|-------------------------------------|-----------------|------------|
| `"Strong Accept"` | 87.5 | 100 (inclusive) | `#00aa00` | Dark green |
| `"Accept"` | 75 | 87.5 | `#00cc44` | Green |
| `"Borderline"` | 62.5 | 75 | `#ffcc00` | Yellow |
| `"Weak Reject"` | 50 | 62.5 | `#ff9900` | Orange |
| `"Reject"` | 25 | 50 | `#ff4b4b` | Red |
| `"Strong Reject"` | 0 | 25 | `#cc0000` | Dark red |

Source: extracted_frontend_01.md § 2.4 (gauge_chart.py:14-31)

### 9.4 Threshold Line

- Value: `62.5` (marks the Borderline boundary)
- Color: `"red"`
- Width: `4`

Source: extracted_frontend_01.md § 2.4 (gauge_chart.py:57-61)

### 9.5 Gauge Axis and Bar Properties

- Gauge axis range: `[0, 100]`
- Tick mode: linear; `tick0=0`; `dtick=25`
- Bar: `color=color_barra`, `thickness=0.8`, line `color="black"`, `width=2`
- Gauge: `bgcolor="white"`, `borderwidth=2`, `bordercolor="black"`
- Background steps: coloured segments matching each of the 6 tiers (exact step color values equal the bar colors in §9.3)

Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:33-71)

### 9.6 Title and Layout Properties

- `title`: `{'text': f"Quality Score<br><sub>{label}</sub>", 'font': {'size': 18}}`
- `number`: `{'suffix': "%", 'font': {'size': 40}}`
- Layout `height`: `300`
- Layout margins: `l=10`, `r=10`, `t=50`, `b=25`
- `paper_bgcolor`: transparent
- Font color: `#E5E7EB`

Source: extracted_frontend_01.md § 5.4 (gauge_chart.py:33-71)

### 9.7 Call Site Gap

> `[GAP: create_gauge_chart is not called from any of the 14 files in the frontend cluster (GAP-ext_frontend_01-001). A caller that passes a numeric score (0-100) and renders the Figure via st.plotly_chart() is expected but not found in the extraction. Likely location: audit_results.py or a caller outside the frontend package.]`

---

## 10. Custom CSS (All Selectors and Property Values)

Defined in `CUSTOM_CSS` constant in `frontend/styles/custom_css.py`.  
Link to g_026 (`apply_custom_styles`): the function `apply_custom_styles()` injects all CSS below by calling `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)`. It takes no parameters and returns None. It is called unconditionally on every page render, as the second statement after `st.set_page_config()` (app.py:21).

Source: extracted_frontend_01.md § 6 (custom_css.py:4-86); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### Selector: `.stApp`

| Property | Value |
|----------|-------|
| `background-color` | `#374151 !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### Selector: `#MainMenu`

| Property | Value |
|----------|-------|
| `visibility` | `hidden` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `footer`

| Property | Value |
|----------|-------|
| `visibility` | `hidden` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `header`

| Property | Value |
|----------|-------|
| `background-color` | `transparent !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"]`

| Property | Value |
|----------|-------|
| `background-color` | `#2d3436 !important` |
| `border-radius` | `15px !important` |
| `padding` | `5px !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### Selector: `[data-testid="stTable"] table`

| Property | Value |
|----------|-------|
| `border-collapse` | `collapse !important` |
| `width` | `100% !important` |
| `border` | `none !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] th`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `font-weight` | `800 !important` |
| `background-color` | `#3d4446 !important` |
| `border` | `1px solid #4a4a4a !important` |
| `padding` | `12px !important` |
| `text-transform` | `capitalize !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] th *`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `font-weight` | `800 !important` |
| `text-decoration` | `none !important` |
| `border` | `none !important` |
| `text-transform` | `capitalize !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] tbody th`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `background-color` | `#2d3436 !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] tbody th *`

| Property | Value |
|----------|-------|
| `color` | `#FFFFFF !important` |
| `font-size` | `16px !important` |
| `background-color` | `transparent !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] td`

| Property | Value |
|----------|-------|
| `color` | `#E2E8F0 !important` |
| `font-size` | `13.5px !important` |
| `font-weight` | `400 !important` |
| `background-color` | `transparent !important` |
| `border` | `1px solid #4a4a4a !important` |
| `padding` | `12px !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stTable"] td *`

| Property | Value |
|----------|-------|
| `color` | `#E2E8F0 !important` |
| `font-size` | `13.5px !important` |
| `font-weight` | `400 !important` |
| `text-decoration` | `none !important` |
| `border` | `none !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82)

---

### Selector: `[data-testid="stPlotlyChart"]`

| Property | Value |
|----------|-------|
| `background-color` | `#2d3436 !important` |
| `border-radius` | `15px !important` |
| `padding` | `10px !important` |

Source: extracted_frontend_01.md § 6 (custom_css.py:7-82); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

### CSS Injection Mechanism (`apply_custom_styles`)

```python
def apply_custom_styles() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
```

- The entire `CUSTOM_CSS` string constant is a `<style>...</style>` HTML block.
- Injected via `st.markdown(..., unsafe_allow_html=True)`.
- Called unconditionally at application startup (app.py:21), before any widget rendering.
- No conditions under which it is skipped.

Source: extracted_frontend_01.md § 6 (custom_css.py:85-86); cross_ref_resolution_cross_ref_root_to_frontend.md § g_026

---

## Appendix A: Complete Session State Reference

All session state keys used by the frontend, merged from all components:

| Key | Type | Default Value | Initialised By | Modified By |
|-----|------|---------------|----------------|-------------|
| `resultado` | `dict` or `None` | `None` | `session_state.py:8-9` | `file_uploader.py:49-52, 85` |
| `auditor` | `PaperAuditor` instance | `PaperAuditor()` | `session_state.py:11-12` | Never (stateful object) |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | `session_state.py:14-15` | Never (stateful object) |
| `sota_analyzer` | `SotaAnalyzer` instance | `SotaAnalyzer()` | `session_state.py:17-18` | Never (stateful object) |
| `messages` | `list` of `{"role": str, "content": str}` | `[]` | `session_state.py:20-21` | `file_uploader.py:21` (reset), `chatbot.py:21, 28` (append) |
| `archivo_actual` | `str` | Not pre-initialised | `file_uploader.py:19` | `file_uploader.py:19` |
| `file_hash` | `str` (MD5 hex) | Not pre-initialised | `file_uploader.py:20` | `file_uploader.py:20` |
| `md_text` | `str` | Not pre-initialised | `file_uploader.py:36-39` | `file_uploader.py:36-39` |

Link to g_027: `initialize_session_state()` (session_state.py:7) initialises the first 5 keys only, using `if "key" not in st.session_state` guards.

Source: extracted_frontend_01.md § 3; cross_ref_resolution_cross_ref_root_to_frontend.md § g_027

---

## Appendix B: Full Top-Level Rendering Order

```
1. st.set_page_config(page_title="NeurIPS 2026 Checklist Auditor", layout="wide", page_icon="🔬")
2. apply_custom_styles()                          — injects CUSTOM_CSS
3. initialize_session_state()                    — guards 5 session keys
4. st.title(TITLE)                               — "💻 Auditor de Papers en Ciencias de la Computación"
5. st.markdown("---")                            — horizontal rule
6. st.button("🔄 Limpiar y subir nuevo archivo") — clears all session state + st.rerun()
7. st.file_uploader("Sube el PDF del artículo científico", type=["pdf","txt","md"])
8. [if uploaded_file:]
   8a. process_uploaded_file(uploaded_file)       — extract + audit; manages st.spinner / st.status
   8b. [error branches — see §3.4: Branch A (INVALID_PAPER_TYPE / generic error), Branch B (evaluation_error: 3 widgets), Branch C (no valid claims: st.error+st.info or st.warning)]
   8c. render_audit_results(resultado, uploaded_file)
   8d. render_sota_analysis(md_text)
   8e. render_chatbot(md_text)
   8f. st.markdown("---") + st.subheader(...) + st.download_button(...)
9. [with st.sidebar:]
   st.image(SIDEBAR_IMAGE, width=150)
   st.markdown("### Sobre el TFG")
   st.write(SIDEBAR_DESCRIPTION)
```

Source: extracted_frontend_01.md § 4.2 (app.py)
