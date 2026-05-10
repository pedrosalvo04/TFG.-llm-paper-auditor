# Extracted Specification: cluster_frontend_01
## Agent: ext_frontend_01

---

## 1. File Index

| # | File | Line Count | Role |
|---|------|-----------|------|
| 1 | `frontend/__init__.py` | 1 | Package marker; single docstring: "Frontend modular para el Auditor de Papers" |
| 2 | `frontend/app.py` | 77 | Main Streamlit application entry point; orchestrates page config, styles, session state, upload, audit, results, chatbot, download |
| 3 | `frontend/config.py` | 5 | Application-level constants: TITLE, SIDEBAR_IMAGE URL, SIDEBAR_DESCRIPTION |
| 4 | `frontend/components/audit_results.py` | 317 | Renders the full audit results page (verdict, metrics, RAG ficha, compliance table, expanders); also generates the downloadable Markdown report |
| 5 | `frontend/components/chatbot.py` | 29 | Renders the interactive chat section; reads/writes `st.session_state.messages`; calls `st.session_state.chatbot.preguntar()` |
| 6 | `frontend/components/file_uploader.py` | 101 | Handles file upload (PDF/TXT/MD), MD extraction, and invocation of the backend auditor; manages `st.session_state` caching by file hash |
| 7 | `frontend/components/gauge_chart.py` | 71 | Pure function `create_gauge_chart(score)`: returns a Plotly Figure (gauge indicator) based on NeurIPS quality tiers |
| 8 | `frontend/components/sota_section.py` | 109 | Renders SOTA analysis section; triggers `st.session_state.sota_analyzer.analyze_sota()`; renders missing-papers dataframe |
| 9 | `frontend/components/__init__.py` | 1 | Package marker; single docstring: "Componentes visuales de la aplicación" |
| 10 | `frontend/styles/custom_css.py` | 87 | Defines CUSTOM_CSS string constant; `apply_custom_styles()` injects CSS via `st.markdown` |
| 11 | `frontend/styles/__init__.py` | 1 | Package marker; single docstring: "Estilos CSS para la aplicación" |
| 12 | `frontend/utils/scoring.py` | 130 | Defines CHECKLIST_KEYS list (16 items), CHECKLIST_LABELS dict, and `get_checklist_health()` function |
| 13 | `frontend/utils/session_state.py` | 22 | `initialize_session_state()`: initialises 5 session state keys on app boot |
| 14 | `frontend/utils/__init__.py` | 1 | Package marker; single docstring: "Utilidades para el frontend" |

---

## 2. Configuration & Constants

### 2.1 Application-level constants (`frontend/config.py`)

```
TITLE = "💻 Auditor de Papers en Ciencias de la Computación"
SOURCE: config.py:3

SIDEBAR_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"
SOURCE: config.py:4

SIDEBAR_DESCRIPTION = "Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."
SOURCE: config.py:5
```

### 2.2 Streamlit page configuration (`frontend/app.py`)

```
page_title = "NeurIPS 2026 Checklist Auditor"
layout    = "wide"
page_icon  = "🔬"
SOURCE: app.py:6-10
```

Note: `st.set_page_config()` is called as the very first Streamlit statement, before any imports that touch Streamlit widgets.
SOURCE: app.py:5 (comment: "IMPORTANTE: configure_page() debe ser lo primero")

### 2.3 Checklist keys and labels (`frontend/utils/scoring.py`)

**CHECKLIST_KEYS** (ordered list, 16 elements):
SOURCE: scoring.py:8-15

```
[
    "claims",
    "limitations",
    "theory_assumptions_proofs",
    "experimental_result_reproducibility",
    "open_access_data_code",
    "experimental_setting_details",
    "experiment_statistical_significance",
    "experiments_compute_resource",
    "code_of_ethics",
    "broader_impacts",
    "safeguards",
    "licenses",
    "assets",
    "crowdsourcing_human_subjects",
    "irb_approvals",
    "declaration_llm_usage"
]
```

**CHECKLIST_LABELS** (dict, key → display string):
SOURCE: scoring.py:17-34

```
"claims"                              → "1. Claims"
"limitations"                         → "2. Limitations"
"theory_assumptions_proofs"           → "3. Theory, Assumptions & Proofs"
"experimental_result_reproducibility" → "4. Experimental Result Reproducibility"
"open_access_data_code"               → "5. Open Access to Data and Code"
"experimental_setting_details"        → "6. Experimental Setting / Details"
"experiment_statistical_significance" → "7. Experiment Statistical Significance"
"experiments_compute_resource"        → "8. Experiments Compute Resource"
"code_of_ethics"                      → "9. Code of Ethics"
"broader_impacts"                     → "10. Broader Impacts"
"safeguards"                          → "11. Safeguards"
"licenses"                            → "12. Licenses"
"assets"                              → "13. Assets"
"crowdsourcing_human_subjects"        → "14. Crowdsourcing & Human Subjects"
"irb_approvals"                       → "15. IRB Approvals"
"declaration_llm_usage"               → "16. Declaration of LLM Usage"
```

### 2.4 NeurIPS Quality Score Tiers (`frontend/components/gauge_chart.py`)

```
[87.5, 100] → label="Strong Accept", bar_color="#00aa00" (dark green)
[75, 87.5)  → label="Accept",        bar_color="#00cc44" (green)
[62.5, 75)  → label="Borderline",    bar_color="#ffcc00" (yellow)
[50, 62.5)  → label="Weak Reject",   bar_color="#ff9900" (orange)
[25, 50)    → label="Reject",        bar_color="#ff4b4b" (red)
[0, 25)     → label="Strong Reject", bar_color="#cc0000" (dark red)

Threshold line: value=62.5, color="red", width=4  (marks Borderline boundary)
SOURCE: gauge_chart.py:14-31, 57-61
```

### 2.5 Compliance table row background colours (`frontend/components/audit_results.py`)

```
pending_justification == True     → "#450a0a"  (deep red — Critical risk)
missing_evidence == True OR        → "#452e0a"  (amber/orange — Warning)
  alert_msg non-empty (for others)
"yes" in answer (lower)           → "#064e3b"  (emerald green — OK)
all other cases                   → "#111827"  (neutral dark)
SOURCE: audit_results.py:18-32
```

### 2.6 Badge styles for Yes/No/N/A (`frontend/components/audit_results.py`)

```
"yes" in answer (lower) → background:#065f46; color:#6ee7b7; text:"Yes"
"no"  in answer (lower) → background:#7f1d1d; color:#fca5a5; text:"No"
else (N/A)              → background:#1e3a5f; color:#93c5fd; text:"N/A"
SOURCE: audit_results.py:10-16
```

### 2.7 Saturation error detection keywords (`frontend/components/file_uploader.py`)

The following uppercase strings are checked in the error message to classify a backend error as "saturation":
```
["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]
SOURCE: file_uploader.py:60
```

### 2.8 Supported file extensions (`frontend/components/file_uploader.py`)

```
Accepted by st.file_uploader: ["pdf", "txt", "md"]    SOURCE: app.py:34
PDF processing:  calls convert_pdf_to_markdown()       SOURCE: file_uploader.py:36
TXT/MD:          reads with open(..., 'r', encoding='utf-8')  SOURCE: file_uploader.py:37-39
```

### 2.9 Temporary file directory

```
temp_path = os.path.join("temp", uploaded_file.name)
Directory created if not exists: os.makedirs("temp")
File deleted after processing: os.remove(temp_path)
SOURCE: file_uploader.py:23-24, 26-27, 86-87, 94-95
```

---

## 3. Session State

All 5 session state keys are initialised in `initialize_session_state()`.
SOURCE: session_state.py:7-22

| Key | Type | Initial Value | Set When | Read When | Cleared When |
|-----|------|---------------|----------|-----------|--------------|
| `resultado` | dict or None | `None` | After `auditor.audit()` completes (file_uploader.py:50); on error, set to `{"error": error_msg}` (file_uploader.py:85) or `{"error": "Ejecución cancelada..."}` (file_uploader.py:76) | app.py:40-68; audit_results.py:90,287 | Cleared implicitly when all session keys are deleted (app.py:30-32) |
| `auditor` | `PaperAuditor` instance | `PaperAuditor()` | On first load (session_state.py:12-13) | file_uploader.py:49 | On "Limpiar" button press (all keys deleted, app.py:30-32) |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | On first load (session_state.py:15-16) | chatbot.py:26 | On "Limpiar" button press |
| `sota_analyzer` | `SotaAnalyzer` instance | `SotaAnalyzer()` | On first load (session_state.py:18-19) | sota_section.py:12 | On "Limpiar" button press |
| `messages` | list of dicts | `[]` | On first load (session_state.py:21-22); reset to `[]` when a new file is detected (file_uploader.py:21) | chatbot.py:10, 23 | On "Limpiar" press; on new file upload |

Additional session state keys set by `file_uploader.py` (not initialised in `initialize_session_state`):

| Key | Type | Initial Value | Set When | Read When |
|-----|------|---------------|----------|-----------|
| `archivo_actual` | str | not set | file_uploader.py:19 — set to `uploaded_file.name` | file_uploader.py:16 — compared to detect file change |
| `file_hash` | str (MD5 hex) | not set | file_uploader.py:20 — set to `hashlib.md5(file_content).hexdigest()` | file_uploader.py:17 — compared to detect content change |
| `md_text` | str | not set | file_uploader.py:36 (PDF) or file_uploader.py:39 (TXT/MD) | chatbot.py:26; sota_section.py:12; app.py:53-54; file_uploader.py:98 |

---

## 4. Page Layout & Navigation

### 4.1 Single-page application

The application is a **single-page Streamlit app** with no `st.switch_page()` calls and no multi-page routing. All content is rendered on one page in top-to-bottom order.
SOURCE: app.py (entire file)

### 4.2 Top-level rendering order (`frontend/app.py`)

```
1. st.set_page_config(...)                             SOURCE: app.py:6-10
2. apply_custom_styles()                               SOURCE: app.py:21
3. initialize_session_state()                          SOURCE: app.py:22
4. st.title(TITLE)                                     SOURCE: app.py:25
5. st.markdown("---")                                  SOURCE: app.py:26
6. "Limpiar y subir nuevo archivo" button              SOURCE: app.py:29-32
7. st.file_uploader(...)                               SOURCE: app.py:34
8. [conditional: if uploaded_file]
   8a. Call process_uploaded_file(uploaded_file)       SOURCE: app.py:37
   8b. Branch on error conditions (see §8 Rules)
   8c. Call render_audit_results(resultado, ...)       SOURCE: app.py:52
   8d. Call render_sota_analysis(md_text)              SOURCE: app.py:53
   8e. Call render_chatbot(md_text)                    SOURCE: app.py:54
   8f. st.markdown("---"), st.subheader, download btn  SOURCE: app.py:57-65
9. st.sidebar block (image + "Sobre el TFG" + description)  SOURCE: app.py:73-76
```

### 4.3 Sidebar

```
st.image(SIDEBAR_IMAGE, width=150)   — ACM logo from Wikipedia CDN
st.markdown("### Sobre el TFG")
st.write(SIDEBAR_DESCRIPTION)
SOURCE: app.py:73-76
```

### 4.4 Navigation — no deep links, no multi-page routing

The application has no `st.navigation`, `st.page_link`, or `st.switch_page` calls. All sections appear on the same page after a file is uploaded.
SOURCE: app.py (confirmed by full read)

---

## 5. UI Components

### 5.1 File Uploader (`frontend/components/file_uploader.py`)

**Function:** `process_uploaded_file(uploaded_file) -> (md_text: str, resultado: dict)`
SOURCE: file_uploader.py:6

**Widget (defined in app.py, consumed here):**
- Type: `st.file_uploader`
- Label: `"Sube el PDF del artículo científico"`
- Accepted types: `["pdf", "txt", "md"]`
- Key: none explicit (Streamlit auto-key)
- Mandatory: implicit — the entire results section is gated on `if uploaded_file:`
SOURCE: app.py:34

**Duplicate-detection logic:**
1. Computes `file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()`.
   SOURCE: file_uploader.py:11-12
2. Checks `("archivo_actual" not in st.session_state) OR (st.session_state.archivo_actual != uploaded_file.name) OR (st.session_state.get('file_hash') != file_hash)`.
   SOURCE: file_uploader.py:15-17
3. If any condition is true → new file detected → process. Otherwise → return cached `(md_text, resultado)` from session_state.
   SOURCE: file_uploader.py:15-101

**Processing steps (when new file detected):**
1. Set `st.session_state.archivo_actual = uploaded_file.name`.
   SOURCE: file_uploader.py:19
2. Set `st.session_state.file_hash = file_hash`.
   SOURCE: file_uploader.py:20
3. Reset `st.session_state.messages = []`.
   SOURCE: file_uploader.py:21
4. Create `temp/` directory if not exists: `os.makedirs("temp")`.
   SOURCE: file_uploader.py:23-24
5. Write file to `temp/<filename>`.
   SOURCE: file_uploader.py:26-28
6. Show `st.spinner("📂 Extrayendo texto...")`.
   SOURCE: file_uploader.py:34
   - If `file_extension == 'pdf'`: call `convert_pdf_to_markdown(temp_path)`, store result in `st.session_state.md_text`.
     SOURCE: file_uploader.py:35-36
   - If `file_extension in ['txt', 'md']`: open file, read as UTF-8, store in `st.session_state.md_text`.
     SOURCE: file_uploader.py:37-39
   - Else: `st.error("❌ Formato no soportado: {file_extension}")`, return `(None, {'error': 'Formato no soportado: ...'})`.
     SOURCE: file_uploader.py:41-42
7. Show `st.status("🧠 Analizando el documento...", expanded=True)`.
   SOURCE: file_uploader.py:45
8. Define `update_status(msg)` callback: calls `st.write(msg)`.
   SOURCE: file_uploader.py:46-47
9. Call `st.session_state.auditor.audit(st.session_state.md_text, status_callback=update_status)`, store in `st.session_state.resultado`.
   SOURCE: file_uploader.py:49-52
10. Error handling on `resultado` (see §8 Rules).
11. On success: `status.update(label="✅ Análisis completado", state="complete", expanded=False)`.
    SOURCE: file_uploader.py:90
12. Show `st.success("✅ Análisis completado")`.
    SOURCE: file_uploader.py:92
13. Delete temp file: `os.remove(temp_path)` if it exists.
    SOURCE: file_uploader.py:94-95

**Return value (always from session_state):**
```python
md_text  = st.session_state.get('md_text', '')
resultado = st.session_state.get('resultado', {})
return md_text, resultado
SOURCE: file_uploader.py:98-100
```

---

### 5.2 Audit Results Display (`frontend/components/audit_results.py`)

**Function:** `render_audit_results(resultado: dict, uploaded_file) -> health: dict`
SOURCE: audit_results.py:90

**Rendering sequence:**

1. `st.success("Auditoria Finalizada")`.
   SOURCE: audit_results.py:92

2. Call `get_checklist_health(resultado)` → `health` dict.
   SOURCE: audit_results.py:94

3. Reads `health["pending_count"]`, `health["total"]`.
   SOURCE: audit_results.py:95-96

4. **Verdict block** (`st.header("Veredicto del Checklist NeurIPS 2026")`):
   SOURCE: audit_results.py:100-117
   - If `health["status"] == "valid"`: renders dark-green div with text "Checklist Valido" and sub-text "Todas las respuestas tienen evidencia o justificacion documentada. El checklist esta listo para NeurIPS."
     SOURCE: audit_results.py:102-109
   - Else (`"risk"`): renders dark-red div with text "Riesgo de Desk Reject" and sub-text showing `{pending} de {total} item(s) requieren accion del autor antes del envio.`
     SOURCE: audit_results.py:111-117

5. **Metrics row** (4 columns):
   SOURCE: audit_results.py:121-133
   - col1: `st.metric("Items Yes", <count of items where "yes" in answer.lower()>)`
   - col2: `st.metric("Items No",  <count of items where "no"  in answer.lower()>)`
   - col3: `st.metric("Items N/A", <count of items where "n/a" in answer.lower()>)`
   - col4: `st.metric("Tiempo",    f"{tiempo}s")` where `tiempo = resultado.get("metricas", {}).get("tiempo_segundos", "N/A")`

6. **RAG Ficha Técnica** (`st.subheader("🎯 Ficha Técnica de Entrenamiento (RAG Specialist)")`):
   SOURCE: audit_results.py:136-163
   - Displayed only if `rag_data = resultado.get("extracted_hyperparameters_hybrid", {})` is truthy.
   - Shows `st.caption("Estos datos han sido extraídos mediante un escaneo profundo (RAG) de las secciones técnicas y apéndices.")`.
   - Layout: 4 columns (c1, c2, c3, c4).
   - c1: `optimizer` (st.code), `learning_rate` (st.code).
   - c2: `batch_size` (st.code), `epochs` (st.code).
   - c3: `warmup_steps` (st.code), `weight_decay` (st.code).
   - c4: `hardware` (st.info); `random_seed` (st.code) — shown only if `rag_data.get("random_seed") and rag_data.get("random_seed") != "NOT FOUND"`.
   - All values obtained via `rag_data.get("<field>", "N/A")`.

7. **Compliance table** (`st.header("Tabla de Cumplimiento NeurIPS 2026")`):
   SOURCE: audit_results.py:167-175
   - Shows caption with colour legend.
   - Calls `_build_table_html(health["items"])` and renders via `st.html(table_html)`.

8. **Expander: Pipeline de Análisis Profundo (Map-Reduce + CoT + Context Mapping)**:
   SOURCE: audit_results.py:179-215
   - Chain-of-Thought: reads `resultado.get("informacion_extraida", {}).get("thought_process", "No disponible")`, shows via `st.info(cot)`.
   - Context Mapping: reads `resultado.get("informacion_extraida", {}).get("context_mapping", [])`. If non-empty, renders in columns (up to 5 per row); else `st.warning("No se ha podido mapear la estructura de secciones.")`.
   - Comparativa Map vs Reduce (2 columns):
     - Left (MAP): reads `resultado.get("general_analysis_map", [])`. If non-empty, iterates and renders each step in `st.expander(f"📦 Fragmento {i+1}")` with `st.json(step)`. Else renders `resultado.get("original_extraction_raw", {})` as JSON.
     - Right (REDUCE): renders `resultado.get("informacion_extraida", {})` as JSON.

9. **Expander: Pipeline de Extracción Híbrida (RAG Specialist)**:
   SOURCE: audit_results.py:218-242
   - Left (Triage MAP): reads `resultado.get("hybrid_triage_fragments", [])`. If non-empty, iterates; for each fragment reads `_relevance_score` (default "N/A"), sets background colour: `"#065f46"` if `isinstance(relevance, int) and relevance > 70`, else `"#1e3a5f"`. Shows expander title `"📄 Fragmento Técnico {i+1} (Relevancia: {relevance}%)"`, renders relevance badge, `_chunk_text` (via `st.caption`), and all non-underscore-prefixed fields (via `st.json`).
   - Right (REDUCE): renders `resultado.get("extracted_hyperparameters_hybrid", {})` as JSON.

10. **Expander: Pipeline de Evaluación (Senior Area Chair + Self-Correction)**:
    SOURCE: audit_results.py:245-283
    - Evaluation Signals: reads `resultado.get("evaluation_signals", {})`. If truthy, iterates dict items: for each key `k`, renders `st.markdown(f"**Item {k.replace('_', ' ').title()}:**")` then `st.info(msg)`. Else `st.warning(...)`.
    - Self-Correction verification details: collects items from `resultado` where value is a dict with `v.get('verified')` true. Falls back to second-level scanning. If found: for each item, status label is `"✨ Corregido"` if `data.get('was_corrected')` else `"✅ Confirmado"`. Shows `st.expander` with answer, justification (via `st.write`), and evidence (via `st.code`).

**Return value:** `health` dict (from `get_checklist_health`).
SOURCE: audit_results.py:284

---

#### 5.2.1 `_build_table_html(items: list) -> str`
SOURCE: audit_results.py:7-87

**Purpose:** Constructs a complete HTML table string for compliance display.

**For each item dict in `items`:**
- Splits `item["label"]` on `". "` to extract `num` and `name` (e.g., `"1. Claims"` → `num="1"`, `name="Claims"`). If no `". "` present, uses `str(idx)` as num and full label as name.
  SOURCE: audit_results.py:39-42
- `evidence_text`: uses `item["evidence"]` if it exists and is not `"-"`, else `""`.
  SOURCE: audit_results.py:44
- Row background: from `row_bg(item)` (see §2.5 constants).
- Evidence cell HTML: if `evidence_text` non-empty → `<span style="color:#d1d5db;">...</span>`; else `<em style="color:#6b7280;">No disponible</em>`.
  SOURCE: audit_results.py:48
- Alert line logic:
  - If `item["pending_justification"]`: alert HTML = `<div style="color:#fca5a5;...">&#9888; Sin justificacion del autor &mdash; Riesgo de Desk Reject</div>`.
    SOURCE: audit_results.py:52-53
  - Elif `item["missing_evidence"]`: alert HTML = `<div style="color:#fde68a;...">&#9888; Respuesta Yes sin evidencia de seccion del paper</div>`.
    SOURCE: audit_results.py:54-55
  - Additionally, if `"compensacion" in item.get("alert_msg", "").lower() or "etica" in item.get("alert_msg", "").lower()`: appends `<div style="color:#fde68a;...">&#9888; NeurIPS Code of Ethics: compensacion minima obligatoria</div>`.
    SOURCE: audit_results.py:57-58
- Each row is a `<tr>` with 4 `<td>` cells: number, name, badge HTML, evidence+alert HTML.

**Table structure:**
```html
<table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
  <thead>
    <tr>  -- headers: "#", "Item del Checklist", "Respuesta", "Evidencia / Justificacion"
    </tr>
  </thead>
  <tbody> ... rows ... </tbody>
</table>
```
SOURCE: audit_results.py:69-87

---

#### 5.2.2 `generate_report(resultado: dict, uploaded_file, health=None) -> str`
SOURCE: audit_results.py:287-316

**Purpose:** Produces a downloadable Markdown audit report string.

**Logic:**
1. If `health is None`: calls `get_checklist_health(resultado)`.
   SOURCE: audit_results.py:289-290
2. `status_label = "Checklist Valido"` if `health["status"] == "valid"` else `"Riesgo de Desk Reject"`.
   SOURCE: audit_results.py:292
3. Builds Markdown string:
   - Header: `# NeurIPS 2026 Checklist Audit Report`
   - `**Paper:** {uploaded_file.name}`
   - `**Veredicto:** {status_label}`
   - `**Items con problemas:** {pending} de {total}`
   - Separator `---`
   - `## Tabla de Cumplimiento` with Markdown table header `| # | Item | Respuesta | Evidencia / Justificacion |`
   - For each item: row with `note` appended — `" [RIESGO: sin justificacion]"` if `pending_justification`, `" [RIESGO: sin evidencia]"` if `missing_evidence`, else empty string.
     SOURCE: audit_results.py:304-313
4. Footer: `_Generado por Auditor NeurIPS 2026._`
5. Returns assembled string.

---

### 5.3 Chatbot Interface (`frontend/components/chatbot.py`)

**Function:** `render_chatbot(md_text: str) -> None`
SOURCE: chatbot.py:4

**Rendering:**
1. `st.markdown("---")`, `st.header("💬 Pregunta al Revisor")`.
2. `st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")`.
3. Renders conversation history: iterates `st.session_state.messages` (list of `{"role": str, "content": str}` dicts); for each, shows `st.chat_message(message["role"])` with `st.markdown(message["content"])`.
   SOURCE: chatbot.py:10-12
4. Input widget: `st.text_input("Escribe tu pregunta:", key="chat_input", placeholder="Ej: ¿En qué página falla el paper en su estadística?")`.
   SOURCE: chatbot.py:14-18
5. Submit button: `st.button("Enviar", key="send_button")`.
   SOURCE: chatbot.py:20

**On submit (button pressed AND `prompt_usuario` non-empty):**
1. Appends `{"role": "user", "content": prompt_usuario}` to `st.session_state.messages`.
   SOURCE: chatbot.py:21
2. Builds `history_str` from the last 4 messages: `"\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])`.
   SOURCE: chatbot.py:23
3. Shows `st.spinner("El revisor está analizando tu consulta...")`.
4. Calls `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` → `respuesta_ia`.
   SOURCE: chatbot.py:26 (CROSS-REFERENCE: `preguntar()` is in `backend/services/chatbot.py` — not in this cluster)
5. Appends `{"role": "assistant", "content": respuesta_ia}` to `st.session_state.messages`.
   SOURCE: chatbot.py:28
6. Calls `st.rerun()` to refresh the conversation display.
   SOURCE: chatbot.py:29

---

### 5.4 Gauge Chart Visualisation (`frontend/components/gauge_chart.py`)

**Function:** `create_gauge_chart(score: float) -> plotly.graph_objects.Figure`
SOURCE: gauge_chart.py:4

**Note:** This function is defined here but its call site is NOT present in any of the 14 files in this cluster. It is exported for use by code outside this cluster.

**Logic:**
1. Determines `color_barra` and `label` based on `score` thresholds (see §2.4).
2. Creates `go.Figure(go.Indicator(...))` with:
   - `mode="gauge+number"`
   - `value=score`
   - `domain={'x': [0,1], 'y': [0,1]}`
   - `title={'text': f"Quality Score<br><sub>{label}</sub>", 'font': {'size': 18}}`
   - `number={'suffix': "%", 'font': {'size': 40}}`
   - Gauge axis: range [0, 100], tickmode linear, tick0=0, dtick=25.
   - Bar: `color=color_barra`, thickness=0.8, line color black width 2.
   - Gauge bgcolor white, borderwidth 2, bordercolor black.
   - Coloured background steps matching the 6 tiers (see §2.4 step colours).
   - Threshold line at value 62.5 (Borderline boundary).
3. Layout: height=300, margins l=10/r=10/t=50/b=25, paper_bgcolor transparent, font color `#E5E7EB`.
4. Returns the Figure object.
SOURCE: gauge_chart.py:33-71

GAP — `create_gauge_chart` is not called from any of the 14 files in this cluster.
```
GAP_ID: GAP-ext_frontend_01-001
TYPE: CROSS_REFERENCE
FROM: gauge_chart.py:4 — create_gauge_chart
EXPECTS: A caller that passes a numeric score (0-100) and renders the returned Plotly Figure via st.plotly_chart()
LIKELY_LOCATION: Possibly audit_results.py or a caller outside the frontend package (could be a page not in this cluster)
IMPACT: LOW — the function is fully self-contained; its logic is documented above; the caller pattern is missing
SOURCE: gauge_chart.py:4
```

---

### 5.5 SOTA Section (`frontend/components/sota_section.py`)

**Function:** `render_sota_analysis(md_text: str) -> None`
SOURCE: sota_section.py:5

**Rendering:**
1. `st.markdown("---")`, `st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")`.
2. Button: `"Ejecutar Análisis de Literatura Reciente"` (no explicit key).
   SOURCE: sota_section.py:10

**On button press:**
1. Shows `st.spinner("Conectando con Semantic Scholar y validando bibliografía...")`.
2. Calls `st.session_state.sota_analyzer.analyze_sota(md_text)` → `resultado_sota`.
   SOURCE: sota_section.py:12 (CROSS-REFERENCE: `analyze_sota()` is in `backend/services/sota_analyzer.py` — not in this cluster)
3. If `"error" not in resultado_sota`:
   - `st.success("Análisis completado")`
   - Renders conclusion: `st.markdown("### 📝 Conclusión")`, `st.info(resultado_sota.get('conclusion_sota', ''))`.
   - Reads `papers_omitidos = resultado_sota.get("papers_omitidos", [])`.
   - Builds `df_papers = pd.DataFrame(resultado_sota.get("papers_analizados", []))`.
   - Reads `año_paper_estudiado = resultado_sota.get("metadata", {}).get("año_paper_estudiado")`.
   - If `not df_papers.empty and papers_omitidos`: calls `_render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)`.
   - Elif `not papers_omitidos`: `st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")`.
4. Else: `st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")`.
   SOURCE: sota_section.py:29

---

#### 5.5.1 `_render_missing_papers(df_papers: DataFrame, papers_omitidos: list, año_paper_estudiado) -> None`
SOURCE: sota_section.py:31

**Logic:**
1. Adds `authors_display` column to `df_papers`:
   - Lambda applied to `autores` column: takes up to 2 author dicts, joins `a.get('name', '')` with `', '`; appends `' et al.'` if `len(x) > 2`; else returns joined string; if not a list returns `'N/A'`.
   SOURCE: sota_section.py:33-35
2. Renames columns: `'titulo'→'title'`, `'año'→'year'`, `'citas'→'citationCount'`.
   SOURCE: sota_section.py:37
3. Builds `titulos_omitidos` set: `{p['titulo'].lower().strip() for p in papers_omitidos}`.
   SOURCE: sota_section.py:39
4. Defines `es_omitido(titulo: str) -> bool`:
   - `titulo_lower = titulo.lower().strip()`
   - Iterates `titulos_omitidos`; returns True if `omitido in titulo_lower OR titulo_lower in omitido`.
   - Returns False if no match.
   SOURCE: sota_section.py:41-46
5. Adds `es_omitido` boolean column to `df_papers` by applying `es_omitido` to `'title'` column.
   SOURCE: sota_section.py:48
6. Filters: `df_no_citados = df_papers[df_papers['es_omitido'] == True]`.
   SOURCE: sota_section.py:49
7. If `df_no_citados` is not empty:
   - Header: `st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")`.
   - Caption: `st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")`.
   - Builds `tabla_recomendaciones` list: for each row in `df_no_citados`:
     - Looks up `papers_omitidos` by title fuzzy match (`titulo_omitido in titulo_paper OR titulo_paper in titulo_omitido`).
     - Gets `justificacion`, `relevancia`, `subtema_relacionado` from matching omitted paper entry.
     - Computes `es_posterior`:
       - `"✅ Sí"` if `año_paper_estudiado AND paper['year'] > año_paper_estudiado`.
       - `"❌ No"` if `año_paper_estudiado AND NOT (paper['year'] > año_paper_estudiado)`.
       - `"?"` if `not año_paper_estudiado`.
     - Appends dict with keys: `"Título"`, `"Autores"`, `"Año"`, `"Posterior"`, `"Citas"`, `"Relevancia"`, `"Subtema"`, `"Justificación"`.
     SOURCE: sota_section.py:55-83
   - Converts to DataFrame, renders with `st.dataframe` with custom column configs:
     - "Título": TextColumn width "large"
     - "Autores": TextColumn width "medium"
     - "Año": NumberColumn width "small"
     - "Posterior": TextColumn "Posterior al tuyo" width "small"
     - "Citas": NumberColumn width "small"
     - "Relevancia": TextColumn width "small"
     - "Subtema": TextColumn width "medium"
     - "Justificación": TextColumn width "large"
     SOURCE: sota_section.py:85-101
   - If `año_paper_estudiado`: `st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")`.
   - Else: `st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")`.
8. Else (df_no_citados is empty): `st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")`.
   SOURCE: sota_section.py:108

---

## 6. Custom CSS & Styling (`frontend/styles/custom_css.py`)

**Constant:** `CUSTOM_CSS` — a multi-line HTML string with `<style>` block.
SOURCE: custom_css.py:4-83

**Function:** `apply_custom_styles() -> None`
- Calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)`.
SOURCE: custom_css.py:85-86

**CSS rules defined:**

| Selector | Properties | Purpose |
|----------|-----------|---------|
| `.stApp` | `background-color: #374151 !important` | Dark grey app background |
| `#MainMenu` | `visibility: hidden` | Hides Streamlit hamburger menu |
| `footer` | `visibility: hidden` | Hides Streamlit footer |
| `header` | `background-color: transparent !important` | Transparent header |
| `[data-testid="stTable"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 5px !important` | Table container dark background with rounded corners |
| `[data-testid="stTable"] table` | `border-collapse: collapse !important; width: 100% !important; border: none !important` | Eliminates duplicate border lines |
| `[data-testid="stTable"] th` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; background-color: #3d4446 !important; border: 1px solid #4a4a4a !important; padding: 12px !important; text-transform: capitalize !important` | Header cells: white bold text, dark header BG |
| `[data-testid="stTable"] th *` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; text-decoration: none !important; border: none !important; text-transform: capitalize !important` | All children of header cells |
| `[data-testid="stTable"] tbody th` | `color: #FFFFFF !important; font-size: 16px !important; background-color: #2d3436 !important` | Body row header cells |
| `[data-testid="stTable"] tbody th *` | `color: #FFFFFF !important; font-size: 16px !important; background-color: transparent !important` | Children of body row headers |
| `[data-testid="stTable"] td` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; background-color: transparent !important; border: 1px solid #4a4a4a !important; padding: 12px !important` | Table data cells |
| `[data-testid="stTable"] td *` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; text-decoration: none !important; border: none !important` | Children of data cells |
| `[data-testid="stPlotlyChart"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 10px !important` | Plotly chart container |

SOURCE: custom_css.py:7-82 (line-by-line)

---

## 7. Scoring Logic (`frontend/utils/scoring.py`)

### 7.1 `get_checklist_health(evaluation: dict) -> dict`
SOURCE: scoring.py:37

**Purpose:** Analyses the audit result dict and produces a health report for the 16-item NeurIPS 2026 checklist. No numeric score is computed; the function validates completeness (evidence/justification presence).

**Parameters:**
- `evaluation`: dict keyed by checklist item keys (see §2.3). Expected structure per key:
  ```python
  {
    "answer":         str,   # "Yes" / "No" / "N/A" / ""
    "justification":  str,
    "evidence":       str,
    "is_no_justified": bool or str  # "true"/"false" or True/False
  }
  ```

**Early-exit guard:**
- If `evaluation` is falsy → returns `{"status": "risk", "items": [], "pending_count": 0, "total": 0}`.
  SOURCE: scoring.py:56-62

**Per-item processing (iterates CHECKLIST_KEYS in order):**
1. Reads `val = evaluation.get(key, {})`.
2. `answer_raw = val.get("answer", "").strip()`; `answer_norm = answer_raw.lower()`.
3. `justification = val.get("justification", "").strip()`.
4. `evidence = val.get("evidence", "").strip()`.
5. Normalises `is_no_justified`: if `isinstance(is_no_justified_raw, str)` → compare to `"true"` (case-insensitive); else `bool(is_no_justified_raw)`.
   SOURCE: scoring.py:73-77

**Risk detection rules (in order):**

- **If `"yes" in answer_norm`:**
  - If `not evidence AND not justification`: `missing_evidence = True`, `pending_count += 1`, `alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."`.
  SOURCE: scoring.py:84-89

- **Elif `"no" in answer_norm`:**
  - If `not is_no_justified OR not justification`: `pending_justification = True`, `pending_count += 1`, `alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."`.
  SOURCE: scoring.py:90-95
  - **Special rule for item `"crowdsourcing_human_subjects"` (key 14):** If `not is_no_justified`: appends `" ⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."` to `alert_msg`.
  SOURCE: scoring.py:98-99

- **Elif `"n/a" in answer_norm OR answer_norm == ""`:**
  - If `not justification AND not evidence`: no risk flagged (pass).
  SOURCE: scoring.py:101-105

**Display evidence selection:**
```python
display_evidence = evidence if evidence else (justification if justification else "—")
SOURCE: scoring.py:108
```

**Item dict appended to items list:**
```python
{
    "key":                key,
    "label":              CHECKLIST_LABELS.get(key, key),
    "answer":             answer_raw if answer_raw else "—",
    "evidence":           display_evidence,
    "justification":      justification,
    "is_no_justified":    is_no_justified,
    "pending_justification": pending_justification,
    "missing_evidence":   missing_evidence,
    "alert_msg":          alert_msg,
}
SOURCE: scoring.py:110-120
```

**Return value:**
```python
{
    "status":        "valid" if pending_count == 0 else "risk",
    "items":         items,       # list of 16 dicts
    "pending_count": pending_count,
    "total":         len(items),  # always 16 when evaluation is non-empty
}
SOURCE: scoring.py:122-127
```

---

## 8. Business Rules

---

**RULE: ClearAndReset**
TRIGGER: User clicks "🔄 Limpiar y subir nuevo archivo" button
CONDITION: Button is clicked (Streamlit evaluates `st.button()` as True)
ACTION IF TRUE: Iterates `list(st.session_state.keys())`, deletes every key from `st.session_state`, then calls `st.rerun()`
ACTION IF FALSE: No action
ERROR: N/A
FIELDS INVOLVED: All keys in `st.session_state`
CALLS: `del st.session_state[key]` for each key, then `st.rerun()`
SOURCE: app.py:29-32

---

**RULE: FileDeduplication**
TRIGGER: `st.file_uploader` widget returns a file
CONDITION: `"archivo_actual" not in st.session_state` OR `st.session_state.archivo_actual != uploaded_file.name` OR `st.session_state.get('file_hash') != hashlib.md5(uploaded_file.getvalue()).hexdigest()`
ACTION IF TRUE: Process new file (extract text + audit)
ACTION IF FALSE: Return cached `(st.session_state.md_text, st.session_state.resultado)` without re-processing
ERROR: N/A
FIELDS INVOLVED: `st.session_state.archivo_actual`, `st.session_state.file_hash`
CALLS: `hashlib.md5(file_content).hexdigest()`
SOURCE: file_uploader.py:15-17

---

**RULE: UnsupportedFileFormat**
TRIGGER: Uploaded file extension is not in ['pdf', 'txt', 'md']
CONDITION: `file_extension not in ['pdf', 'txt', 'md']`  (note: the file_uploader widget itself restricts to these types, so this is a secondary guard)
ACTION IF TRUE: `st.error(f"❌ Formato no soportado: {file_extension}")`, return `(None, {'error': 'Formato no soportado: {file_extension}'})`
ACTION IF FALSE: Continue processing
ERROR: Display text: `"❌ Formato no soportado: {file_extension}"`
FIELDS INVOLVED: `uploaded_file.name`
CALLS: `st.error(...)`; returns early
SOURCE: file_uploader.py:41-42

---

**RULE: SaturationErrorDetection**
TRIGGER: `auditor.audit()` returns a dict with key `"error"`, AND error message is checked for saturation keywords
CONDITION: `any(x in str(resultado['error']).upper() for x in ["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"])`
ACTION IF TRUE:
  - `status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)`
  - `st.error("### ⚠️ El servicio de IA está saturado")`
  - Shows expander with explanation text: "El modelo Gemini está experimentando una demanda extremadamente alta en este momento y no ha podido completar la tarea tras 5 reintentos automáticos."
  - Shows info: "Este es un problema temporal de Google. Puedes esperar unos minutos e intentar reanudar, o cancelar la ejecución actual."
  - Renders 2 buttons: "🔄 Reintentar ahora" (calls `st.rerun()`) and "🚫 Cancelar ejecución" (sets `st.session_state.resultado = {"error": "Ejecución cancelada por el usuario debido a saturación de API."}` and calls `st.stop()`)
  - Calls `st.stop()` to halt normal flow
ACTION IF FALSE (non-saturation error):
  - `status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)`
  - `st.error(f"❌ Error crítico: {error_msg}")`
  - `st.session_state.resultado = {"error": error_msg}`
  - Deletes temp file if exists
  - Calls `st.stop()`
ERROR: Varies — see action descriptions
FIELDS INVOLVED: `st.session_state.resultado`, temp file path
CALLS: `st.error`, `st.stop`, `st.rerun`, `os.remove`
SOURCE: file_uploader.py:56-88

---

**RULE: InvalidPaperTypeError**
TRIGGER: `process_uploaded_file` returns a `resultado` dict AND `"error" in resultado`
CONDITION: `resultado["error"] == "INVALID_PAPER_TYPE"`
ACTION IF TRUE: `st.error(f"❌ Paper no válido: {resultado.get('message', 'Solo se evalúan papers de ML/AI')}")`
ACTION IF FALSE: Falls through to next error check
ERROR: Display text: `"❌ Paper no válido: {message}"` — default message: `"Solo se evalúan papers de ML/AI"`
FIELDS INVOLVED: `resultado["error"]`, `resultado["message"]`
CALLS: `st.error(...)`
SOURCE: app.py:42-43

---

**RULE: GenericAuditError**
TRIGGER: `"error" in resultado` AND `resultado["error"] != "INVALID_PAPER_TYPE"`
CONDITION: `resultado["error"]` is present and not "INVALID_PAPER_TYPE"
ACTION IF TRUE: `st.error(f"❌ Error en la auditoría: {err}")`
ACTION IF FALSE: No action
ERROR: Display text: `"❌ Error en la auditoría: {err}"`
FIELDS INVOLVED: `resultado["error"]`
CALLS: `st.error(...)`
SOURCE: app.py:45

---

**RULE: LLMEvaluationError**
TRIGGER: `resultado` dict has key `"evaluation_error"`
CONDITION: `"evaluation_error" in resultado`
ACTION IF TRUE:
  - `st.error(f"❌ Error del LLM: {resultado['evaluation_error']}")`
  - `st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")`
  - `st.info("💡 Tip: Recarga la página o sube el archivo nuevamente.")`
ACTION IF FALSE: No action
ERROR: Multiple display widgets shown
FIELDS INVOLVED: `resultado["evaluation_error"]`
CALLS: `st.error`, `st.warning`, `st.info`
SOURCE: app.py:46-49

---

**RULE: EmptyAuditResult**
TRIGGER: `resultado` is truthy but `resultado.get("claims")` is falsy (AND no error keys present)
CONDITION: `resultado` is not None, `"error" not in resultado`, `"evaluation_error" not in resultado`, `not resultado.get("claims")`
ACTION IF TRUE: `st.error("⚠️ La auditoría no generó resultados válidos.")`; `st.info("Posibles causas: respuesta vacía del LLM o JSON inválido.")`
ACTION IF FALSE: Proceeds to render full results
ERROR: `"⚠️ La auditoría no generó resultados válidos."`
FIELDS INVOLVED: `resultado.get("claims")`
CALLS: `st.error(...)`, `st.info(...)`
SOURCE: app.py:66-68

---

**RULE: NoResultAvailable**
TRIGGER: `resultado` is falsy (None or empty dict)
CONDITION: `not resultado` (i.e., `resultado` evaluates to False)
ACTION IF TRUE: `st.warning("⚠️ No hay resultado disponible.")`
ACTION IF FALSE: No action
ERROR: `"⚠️ No hay resultado disponible."`
FIELDS INVOLVED: `resultado` (session_state)
CALLS: `st.warning(...)`
SOURCE: app.py:69-70

---

**RULE: ChecklistItemYesRisk**
TRIGGER: `get_checklist_health()` processes each item with answer containing "yes"
CONDITION: `"yes" in answer_norm AND not evidence AND not justification`
ACTION IF TRUE: `missing_evidence = True`, `pending_count += 1`, `alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."`
ACTION IF FALSE: No risk flagged for this item
ERROR: N/A (risk flag, not user-facing error)
FIELDS INVOLVED: `val["answer"]`, `val["evidence"]`, `val["justification"]`
CALLS: None — pure state computation
SOURCE: scoring.py:84-89

---

**RULE: ChecklistItemNoRisk**
TRIGGER: `get_checklist_health()` processes each item with answer containing "no"
CONDITION: `"no" in answer_norm AND (not is_no_justified OR not justification)`
ACTION IF TRUE: `pending_justification = True`, `pending_count += 1`, `alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."`
ACTION IF FALSE: No risk flagged
ERROR: N/A
FIELDS INVOLVED: `val["answer"]`, `val["is_no_justified"]`, `val["justification"]`
CALLS: None — pure state computation
SOURCE: scoring.py:90-95

---

**RULE: CrowdsourcingEthicsAlert**
TRIGGER: Item key `"crowdsourcing_human_subjects"` processed in `get_checklist_health()` with "no" answer and no justification
CONDITION: `key == "crowdsourcing_human_subjects" AND "no" in answer_norm AND not is_no_justified`
ACTION IF TRUE: Appends `" ⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."` to `alert_msg`; also triggers display of NeurIPS Code of Ethics alert line in HTML table (via check `"compensacion" in alert_msg.lower() or "etica" in alert_msg.lower()`)
ACTION IF FALSE: No extra alert
ERROR: N/A
FIELDS INVOLVED: `val["is_no_justified"]`
CALLS: `audit_results.py:57-58` — triggers secondary HTML alert in `_build_table_html`
SOURCE: scoring.py:98-99

---

**RULE: ChecklistValidVerdict**
TRIGGER: `get_checklist_health()` finishes iterating all 16 items
CONDITION: `pending_count == 0`
ACTION IF TRUE: `status = "valid"`
ACTION IF FALSE: `status = "risk"`
ERROR: N/A
FIELDS INVOLVED: `pending_count`, `status`
CALLS: None
SOURCE: scoring.py:122

---

**RULE: ChatSubmitGuard**
TRIGGER: User clicks "Enviar" button in chatbot section
CONDITION: `st.button("Enviar") AND prompt_usuario` (both must be truthy)
ACTION IF TRUE: Add user message to history, call chatbot backend, add response, rerun
ACTION IF FALSE: No action (button click without text is silently ignored)
ERROR: N/A
FIELDS INVOLVED: `st.session_state.messages`, `prompt_usuario` (text_input value)
CALLS: `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` — CROSS-REFERENCE to backend
SOURCE: chatbot.py:20-29

---

## 9. User Flows & State Transitions

### 9.1 Main user flow: File upload → Audit → Results

```
START
  │
  ▼
[Page loads]
  │  initialize_session_state() called
  │  apply_custom_styles() called
  │
  ▼
[User sees: title, "Limpiar" button, file_uploader]
  │
  ├─ User clicks "🔄 Limpiar y subir nuevo archivo"
  │    → ALL session_state keys deleted
  │    → st.rerun() → page reloads from START
  │
  └─ User uploads PDF/TXT/MD file
       │
       ▼
       [process_uploaded_file(uploaded_file)]
       │
       ├─ Duplicate check (hash + filename)
       │    Same file? → return cached (md_text, resultado) → skip to DISPLAY
       │
       └─ New file detected:
            │  - Set archivo_actual, file_hash
            │  - Reset messages=[]
            │  - Write to temp/<filename>
            │  - st.spinner: extract text
            │      PDF → convert_pdf_to_markdown()
            │      TXT/MD → open+read UTF-8
            │  - st.status "🧠 Analizando...": call auditor.audit()
            │
            ├─ Error: unsupported format → show st.error → return (None, error_dict)
            │
            ├─ Error: saturation (503/QUOTA/etc.)
            │    → show error UI with Reintentar/Cancelar buttons
            │    → st.stop()
            │
            ├─ Error: general → show st.error → st.session_state.resultado = error_dict → st.stop()
            │
            └─ Success:
                 status.update("✅ Análisis completado")
                 st.success("✅ Análisis completado")
                 delete temp file
                 return (md_text, resultado)
       │
       ▼
       DISPLAY BLOCK (app.py:40-70):
       │
       ├─ resultado["error"] == "INVALID_PAPER_TYPE" → st.error("❌ Paper no válido: ...")
       │
       ├─ "error" in resultado (other) → st.error("❌ Error en la auditoría: ...")
       │
       ├─ "evaluation_error" in resultado → st.error + st.warning + st.info
       │
       ├─ resultado.get("claims") truthy → FULL RESULTS PATH:
       │    │
       │    ├─ render_audit_results(resultado, uploaded_file) → health dict
       │    │    (verdict, metrics, RAG ficha, compliance table, expanders)
       │    │
       │    ├─ render_sota_analysis(md_text)
       │    │    (user must click button to trigger SOTA)
       │    │
       │    ├─ render_chatbot(md_text)
       │    │    (interactive Q&A)
       │    │
       │    └─ Download report section
       │         st.download_button(label="📥 Descargar Informe Completo (.md)", ...)
       │         filename: auditoria_neurips_{name_without_ext}.md
       │
       ├─ resultado truthy but no "claims" → st.error("⚠️ La auditoría no generó resultados válidos.")
       │
       └─ resultado falsy → st.warning("⚠️ No hay resultado disponible.")
```

### 9.2 SOTA analysis sub-flow

```
[render_sota_analysis(md_text)]
  │
  ├─ "Ejecutar Análisis de Literatura Reciente" button NOT clicked → show button only
  │
  └─ Button clicked:
       │
       ▼
       sota_analyzer.analyze_sota(md_text) [backend call]
       │
       ├─ "error" in result → st.error("Hubo un error al realizar el análisis SOTA: ...")
       │
       └─ Success:
            st.success("Análisis completado")
            st.info(conclusion_sota)
            │
            ├─ papers_omitidos is empty → st.success("No se detectaron omisiones significativas...")
            │
            └─ df_papers non-empty AND papers_omitidos non-empty
                 → _render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)
                   → renders filtered dataframe of uncited papers
```

### 9.3 Chatbot sub-flow

```
[render_chatbot(md_text)]
  │
  ├─ Renders existing messages from st.session_state.messages
  ├─ Renders text_input "Escribe tu pregunta:" (key="chat_input")
  ├─ Renders "Enviar" button (key="send_button")
  │
  └─ "Enviar" clicked AND prompt_usuario non-empty:
       │
       ├─ Append {"role": "user", "content": prompt_usuario} to messages
       ├─ Build history_str from last 4 messages
       ├─ st.spinner: call chatbot.preguntar(md_text, prompt_usuario, history_str)
       ├─ Append {"role": "assistant", "content": respuesta_ia} to messages
       └─ st.rerun() → re-renders conversation with new message
```

---

## 10. Transformations

### 10.1 File hash computation

```
INPUT:  uploaded_file.getvalue()  → bytes
OUTPUT: hexadecimal MD5 digest string (32 chars)
FORMULA: hashlib.md5(file_content).hexdigest()
STORED IN: st.session_state.file_hash
SOURCE: file_uploader.py:11-12
```

### 10.2 Text extraction from uploaded file

```
INPUT:  temp_path (str), file_extension (str)
OUTPUT: st.session_state.md_text (str — Markdown text)

BRANCH 1: file_extension == 'pdf'
  → calls convert_pdf_to_markdown(temp_path)
  → CROSS-REFERENCE: implemented in backend/services/pdf_parser.py

BRANCH 2: file_extension in ['txt', 'md']
  → open(temp_path, 'r', encoding='utf-8').read()
  → stored directly as Markdown text

SOURCE: file_uploader.py:35-39
```

### 10.3 Checklist item label splitting

```
INPUT:  label_full (str) — e.g., "1. Claims"
OUTPUT: num (str), name (str) — e.g., "1", "Claims"
FORMULA:
  if ". " in label_full:
      num, name = label_full.split(". ", 1)
  else:
      num = str(idx)   # 1-based index
      name = label_full
SOURCE: audit_results.py:39-42
```

### 10.4 `display_evidence` selection

```
INPUT:  evidence (str), justification (str)
OUTPUT: display_evidence (str)
FORMULA: evidence if evidence else (justification if justification else "—")
SOURCE: scoring.py:108
```

### 10.5 Chat history string construction

```
INPUT:  st.session_state.messages (list of dicts), last 4 elements
OUTPUT: history_str (str)
FORMULA: "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
SOURCE: chatbot.py:23
```

### 10.6 Authors display name

```
INPUT:  autores (list of dicts with key 'name', or non-list)
OUTPUT: str — formatted author string
FORMULA:
  if isinstance(x, list):
    base = ', '.join([a.get('name', '') for a in x[:2]])
    suffix = ' et al.' if len(x) > 2 else ''
    return base + suffix
  else:
    return 'N/A'
SOURCE: sota_section.py:33-35
```

### 10.7 SOTA paper column rename

```
INPUT:  df_papers (DataFrame) with columns 'titulo', 'año', 'citas'
OUTPUT: same DataFrame with renamed columns 'title', 'year', 'citationCount'
FORMULA: df_papers.rename(columns={'titulo': 'title', 'año': 'year', 'citas': 'citationCount'}, inplace=True)
SOURCE: sota_section.py:37
```

### 10.8 Report filename transformation

```
INPUT:  uploaded_file.name (str) — e.g., "paper.pdf" or "paper.md"
OUTPUT: filename for download button (str)
FORMULA: f"auditoria_neurips_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"
Example: "paper.pdf" → "auditoria_neurips_paper.md"
SOURCE: app.py:63
```

### 10.9 Gauge score to label/colour

```
INPUT:  score (float, range [0, 100])
OUTPUT: (label: str, color_barra: str)

score >= 87.5 → ("Strong Accept", "#00aa00")
score >= 75   → ("Accept",        "#00cc44")
score >= 62.5 → ("Borderline",    "#ffcc00")
score >= 50   → ("Weak Reject",   "#ff9900")
score >= 25   → ("Reject",        "#ff4b4b")
score <  25   → ("Strong Reject", "#cc0000")
SOURCE: gauge_chart.py:14-31
```

### 10.10 `is_no_justified` normalisation

```
INPUT:  is_no_justified_raw (bool or str)
OUTPUT: is_no_justified (bool)
FORMULA:
  if isinstance(is_no_justified_raw, str):
    is_no_justified = is_no_justified_raw.lower() == "true"
  else:
    is_no_justified = bool(is_no_justified_raw)
SOURCE: scoring.py:73-77
```

---

## 11. Error Handling

| Error Condition | Display Widget | Exact Message Text | Recovery Path |
|----------------|---------------|--------------------|---------------|
| File format not supported | `st.error` | `"❌ Formato no soportado: {file_extension}"` | Return `(None, error_dict)` — no audit attempted |
| Backend saturation (503/QUOTA/etc.) | `st.error` + `st.info` | `"### ⚠️ El servicio de IA está saturado"` | Show "Reintentar ahora" (`st.rerun()`) or "Cancelar ejecución" (`st.stop()`) |
| General audit error | `st.error` | `"❌ Error crítico: {error_msg}"` | Delete temp file, `st.stop()` |
| `INVALID_PAPER_TYPE` error key | `st.error` | `"❌ Paper no válido: {message}"` (default: "Solo se evalúan papers de ML/AI") | No recovery — page stays with error shown |
| Generic error key in resultado | `st.error` | `"❌ Error en la auditoría: {err}"` | No recovery |
| LLM evaluation error | `st.error` + `st.warning` + `st.info` | Error: `"❌ Error del LLM: {evaluation_error}"`; Warning: `"🔄 El modelo está experimentando alta demanda. Intenta nuevamente."`; Info: `"💡 Tip: Recarga la página o sube el archivo nuevamente."` | Manual page reload |
| Valid result but no `claims` field | `st.error` + `st.info` | Error: `"⚠️ La auditoría no generó resultados válidos."`; Info: `"Posibles causas: respuesta vacía del LLM o JSON inválido."` | No recovery |
| `resultado` is falsy/None | `st.warning` | `"⚠️ No hay resultado disponible."` | No recovery shown |
| SOTA analysis error | `st.error` | `"Hubo un error al realizar el análisis SOTA: {error}"` | No recovery (button can be clicked again) |
| Context Mapping empty | `st.warning` | `"No se ha podido mapear la estructura de secciones."` | Informational only |
| Evaluation signals absent | `st.warning` | `"No se generaron señales dinámicas para esta evaluación."` | Informational only |
| Self-correction not available | `st.warning` | `"La fase de verificación no reportó cambios o no está disponible."` | Informational only |
| No SOTA triage data | `st.warning` | `"No hay datos de triage disponibles."` | Informational only |
| Uncited papers table empty | `st.success` | `"✅ Tu manuscrito cita adecuadamente la literatura reciente relevante."` | Success state — no action needed |
| `año_paper_estudiado` not detected | `st.warning` | `"⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos."` | Informational only |

---

## 12. Gaps & Cross-References

```
GAP_ID: GAP-ext_frontend_01-001
TYPE: CROSS_REFERENCE
FROM: gauge_chart.py:4 — create_gauge_chart(score)
EXPECTS: A caller that passes a numeric score (float, 0–100) and renders the returned go.Figure via st.plotly_chart()
LIKELY_LOCATION: Possibly audit_results.py (not found in current version) or an older version of the same file; or a page not included in this cluster
IMPACT: LOW — function is fully documented above; gap is only the call site
SOURCE: gauge_chart.py:4

GAP_ID: GAP-ext_frontend_01-002
TYPE: CROSS_REFERENCE
FROM: file_uploader.py:36 — convert_pdf_to_markdown(temp_path)
EXPECTS: function(path: str) -> str — converts a PDF file at `path` to a Markdown string
LIKELY_LOCATION: backend/services/pdf_parser.py (import: `from backend.services.pdf_parser import convert_pdf_to_markdown`)
IMPACT: HIGH — PDF is the primary supported format; if this function is absent or changes signature, PDF auditing breaks entirely
SOURCE: file_uploader.py:4-5

GAP_ID: GAP-ext_frontend_01-003
TYPE: CROSS_REFERENCE
FROM: session_state.py:13 — PaperAuditor()
EXPECTS: Class with method `audit(md_text: str, status_callback: callable) -> dict` where dict contains keys: "claims" (and 15 other CHECKLIST_KEYS), optionally "error", "evaluation_error", "metricas", "informacion_extraida", "general_analysis_map", "original_extraction_raw", "hybrid_triage_fragments", "extracted_hyperparameters_hybrid", "evaluation_signals"
LIKELY_LOCATION: backend/services/auditor.py (import: `from backend.services.auditor import PaperAuditor`)
IMPACT: HIGH — central backend dependency; the entire audit pipeline and result structure depends on this class
SOURCE: session_state.py:3

GAP_ID: GAP-ext_frontend_01-004
TYPE: CROSS_REFERENCE
FROM: session_state.py:16 — PaperChatbot()
EXPECTS: Class with method `preguntar(md_text: str, question: str, history_str: str) -> str` returning a text response
LIKELY_LOCATION: backend/services/chatbot.py (import: `from backend.services.chatbot import PaperChatbot`)
IMPACT: MEDIUM — chatbot section is non-functional without this; core audit flow is unaffected
SOURCE: session_state.py:4

GAP_ID: GAP-ext_frontend_01-005
TYPE: CROSS_REFERENCE
FROM: session_state.py:19 — SotaAnalyzer()
EXPECTS: Class with method `analyze_sota(md_text: str) -> dict` where dict contains keys: "conclusion_sota", "papers_omitidos" (list), "papers_analizados" (list of dicts with 'titulo', 'año', 'citas', 'autores'), "metadata" (dict with 'año_paper_estudiado'), optionally "error"
LIKELY_LOCATION: backend/services/sota_analyzer.py (import: `from backend.services.sota_analyzer import SotaAnalyzer`)
IMPACT: MEDIUM — SOTA section is non-functional without this; core audit flow is unaffected
SOURCE: session_state.py:5

GAP_ID: GAP-ext_frontend_01-006
TYPE: CONFIG_DEPENDENCY
FROM: file_uploader.py:23 — os.makedirs("temp")
EXPECTS: Filesystem write permission in the working directory to create a `temp/` subdirectory
LIKELY_LOCATION: Application working directory / container filesystem
IMPACT: HIGH — if `temp/` cannot be created (permissions, read-only filesystem), file upload processing will fail with an OS error
SOURCE: file_uploader.py:23-24

GAP_ID: GAP-ext_frontend_01-007
TYPE: EXTERNAL_SYSTEM
FROM: sota_section.py:12 — st.session_state.sota_analyzer.analyze_sota(md_text)
EXPECTS: Connectivity to Semantic Scholar API (mentioned in spinner text: "Conectando con Semantic Scholar y validando bibliografía...")
LIKELY_LOCATION: backend/services/sota_analyzer.py — external HTTP call
IMPACT: MEDIUM — SOTA analysis will fail if Semantic Scholar API is unreachable; error is handled gracefully in the UI
SOURCE: sota_section.py:11

GAP_ID: GAP-ext_frontend_01-008
TYPE: MISSING_SOURCE
FROM: audit_results.py:241 — st.caption("Fusión de datos técnicos con Gemma 4 31B.")
EXPECTS: Knowledge of which LLM model is used in the RAG REDUCE phase (Gemma 4 31B is mentioned inline in UI text)
LIKELY_LOCATION: backend/services/auditor.py or a config file
IMPACT: LOW — informational label only; does not affect functional behaviour
SOURCE: audit_results.py:241

GAP_ID: GAP-ext_frontend_01-009
TYPE: MISSING_SOURCE
FROM: audit_results.py:262 — st.caption("Re-evaluación crítica de ítems realizada por Gemini 3.1 Pro para detectar omisiones o errores de interpretación.")
EXPECTS: Knowledge that "Gemini 3.1 Pro" is the Self-Correction (Auditor 2) model
LIKELY_LOCATION: backend/services/auditor.py
IMPACT: LOW — informational label only
SOURCE: audit_results.py:262
```
