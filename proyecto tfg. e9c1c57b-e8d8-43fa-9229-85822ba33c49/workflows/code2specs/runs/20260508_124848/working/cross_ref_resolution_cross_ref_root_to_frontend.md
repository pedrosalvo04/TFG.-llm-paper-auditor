# Cross-Reference Resolution: cluster_root_tests_scratch_01 → cluster_frontend_01

Agent: cross_ref_root_to_frontend
Type: cross_ref_resolution
Date: 2026-05-08
Gaps addressed: 8

## RESOLUTION SUMMARY

| gap_id | entity | resolved_in | source_file:line | confidence |
|--------|--------|-------------|------------------|------------|
| g_004  | process_uploaded_file | § 5.1 File Uploader (`frontend/components/file_uploader.py`) | file_uploader.py:6 | HIGH |
| g_005  | render_audit_results | § 5.2 Audit Results Display (`frontend/components/audit_results.py`) | audit_results.py:90 | HIGH |
| g_006  | generate_report | § 5.2.2 `generate_report` (`frontend/components/audit_results.py`) | audit_results.py:287 | HIGH |
| g_007  | render_sota_analysis, render_chatbot | § 5.5 SOTA Section / § 5.3 Chatbot Interface | sota_section.py:5 / chatbot.py:4 | HIGH |
| g_008  | TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION | § 2.1 Application-level constants (`frontend/config.py`) | config.py:3–5 | HIGH |
| g_013  | get_checklist_health | § 7.1 `get_checklist_health` (`frontend/utils/scoring.py`) | scoring.py:37 | HIGH |
| g_026  | apply_custom_styles | § 6. Custom CSS & Styling (`frontend/styles/custom_css.py`) | custom_css.py:85 | HIGH |
| g_027  | initialize_session_state | § 3. Session State / File Index row 13 (`frontend/utils/session_state.py`) | session_state.py:7 | HIGH |

---

## g_004 — process_uploaded_file

**Original GAP location:** GAP-cluster_root_tests_scratch_01-001
**Resolution source:** extracted_frontend_01.md § 5.1 File Uploader (`frontend/components/file_uploader.py`)
**Source file:line:** file_uploader.py:6

### Resolved Content

FUNCTION: process_uploaded_file
SIGNATURE: process_uploaded_file(uploaded_file)
  — No type annotations in source. Inferred types from extraction: `uploaded_file` is a Streamlit UploadedFile object.
PARAMETERS:
  - uploaded_file: Streamlit UploadedFile object — the file returned by `st.file_uploader`; accepted extensions: pdf, txt, md
RETURN:
  TYPE: tuple (md_text: str, resultado: dict)
  DESCRIPTION: Both values are read from `st.session_state` at the end of the function:
    - md_text  = st.session_state.get('md_text', '')   — the extracted text of the uploaded file (str; '' if not set)
    - resultado = st.session_state.get('resultado', {}) — the audit result dict (dict; {} if not set)
  SOURCE: file_uploader.py:98-100
SESSION_STATE_CONTRACT:
  WRITES (when new file detected — deduplication condition is True):
    - st.session_state.archivo_actual: str — set to `uploaded_file.name`
      SOURCE: file_uploader.py:19
    - st.session_state.file_hash: str (MD5 hex digest) — set to `hashlib.md5(uploaded_file.getvalue()).hexdigest()`
      SOURCE: file_uploader.py:20
    - st.session_state.messages: list — reset to `[]`
      SOURCE: file_uploader.py:21
    - st.session_state.md_text: str — set to extracted text content (via `convert_pdf_to_markdown` for PDF, or `open(...).read()` for TXT/MD)
      SOURCE: file_uploader.py:35-39
    - st.session_state.resultado: dict — set to the return value of `st.session_state.auditor.audit(st.session_state.md_text, status_callback=update_status)`; on error set to `{"error": error_msg}`
      SOURCE: file_uploader.py:49-52, 85
  READS:
    - st.session_state.archivo_actual: compared to `uploaded_file.name` to detect file change
    - st.session_state.file_hash: compared to current MD5 to detect content change
    - st.session_state.md_text: read at end to form return tuple
    - st.session_state.resultado: read at end to form return tuple
SIDE_EFFECTS:
  - Creates `temp/` directory if not present (`os.makedirs("temp")`); writes file to `temp/<filename>`; deletes temp file after processing
  - Renders `st.spinner`, `st.status`, `st.success`, `st.error` widgets during processing
SOURCE: file_uploader.py:6

---

## g_005 — render_audit_results

**Original GAP location:** GAP-cluster_root_tests_scratch_01-002
**Resolution source:** extracted_frontend_01.md § 5.2 Audit Results Display (`frontend/components/audit_results.py`)
**Source file:line:** audit_results.py:90

### Resolved Content

FUNCTION: render_audit_results
SIGNATURE: render_audit_results(resultado, uploaded_file)
  — No type annotations in source. Inferred types from extraction: `resultado: dict`, `uploaded_file`: Streamlit UploadedFile object.
PARAMETERS:
  - resultado: dict — the audit result dict produced by `auditor.audit()`; expected keys include the 16 CHECKLIST_KEYS plus optional keys: `"metricas"`, `"informacion_extraida"`, `"general_analysis_map"`, `"original_extraction_raw"`, `"hybrid_triage_fragments"`, `"extracted_hyperparameters_hybrid"`, `"evaluation_signals"`
  - uploaded_file: Streamlit UploadedFile object — used for display purposes (e.g. `uploaded_file.name`) and passed to `generate_report`
RETURN:
  TYPE: dict (named `health` in extraction)
  DESCRIPTION: The dict returned by `get_checklist_health(resultado)`.
  KEYS:
    - "status": str — "valid" if no pending items, else "risk"
    - "items": list — 16 item dicts (see g_013 for full item structure)
    - "pending_count": int — number of items with risk issues
    - "total": int — total items evaluated (16 when evaluation is non-empty)
  SOURCE: audit_results.py:284
SIDE_EFFECTS:
  - Renders the full audit results page via Streamlit widgets: success banner, health verdict block, 4-column metrics row, RAG Ficha Técnica, compliance table (via `_build_table_html`), and three expander sections (Pipeline de Análisis Profundo, Extracción Híbrida, Evaluación)
  - Calls `get_checklist_health(resultado)` internally
  - Renders a download button for the Markdown report via `generate_report(resultado, uploaded_file, health)`
SOURCE: audit_results.py:90

---

## g_006 — generate_report

**Original GAP location:** GAP-cluster_root_tests_scratch_01-003
**Resolution source:** extracted_frontend_01.md § 5.2.2 `generate_report` (`frontend/components/audit_results.py`)
**Source file:line:** audit_results.py:287

### Resolved Content

FUNCTION: generate_report
SIGNATURE: generate_report(resultado, uploaded_file, health=None)
  — No type annotations in source. Inferred types from extraction: `resultado: dict`, `uploaded_file`: Streamlit UploadedFile, `health: dict or None`.
PARAMETERS:
  - resultado: dict — the full audit result dict; used to compute `health` if `health is None`
  - uploaded_file: Streamlit UploadedFile object — `uploaded_file.name` is embedded in the report header line `**Paper:** {uploaded_file.name}`
  - health: dict or None — default `None`; if None, computed internally via `get_checklist_health(resultado)`. If already computed (e.g. by `render_audit_results`), can be passed in to avoid duplicate computation
RETURN:
  TYPE: str
  DESCRIPTION: A Markdown-formatted audit report string. Structure:
    - `# NeurIPS 2026 Checklist Audit Report`
    - `**Paper:** {uploaded_file.name}`
    - `**Veredicto:** {status_label}` — "Checklist Valido" or "Riesgo de Desk Reject"
    - `**Items con problemas:** {pending} de {total}`
    - `---`
    - `## Tabla de Cumplimiento` with Markdown table: `| # | Item | Respuesta | Evidencia / Justificacion |`
    - For each of the 16 items: row with optional note `" [RIESGO: sin justificacion]"` if `pending_justification`, or `" [RIESGO: sin evidencia]"` if `missing_evidence`
    - Footer: `_Generado por Auditor NeurIPS 2026._`
  SOURCE: audit_results.py:295-316 (return is `reporte`, a str)
SIDE_EFFECTS: None (pure function — does not call any Streamlit widgets)
SOURCE: audit_results.py:287

---

## g_007 — render_sota_analysis and render_chatbot

**Original GAP location:** GAP-cluster_root_tests_scratch_01-004
**Resolution source:** extracted_frontend_01.md § 5.5 SOTA Section and § 5.3 Chatbot Interface
**Source file:line:** sota_section.py:5 / chatbot.py:4

### Resolved Content

FUNCTION: render_sota_analysis
SIGNATURE: render_sota_analysis(md_text)
  — No type annotation in source. Inferred type from extraction: `md_text: str`.
PARAMETERS:
  - md_text: str — the full Markdown text of the uploaded paper; passed to `st.session_state.sota_analyzer.analyze_sota(md_text)` on button press
RETURN: None (no return statement; function renders UI only)
SIDE_EFFECTS:
  - Renders `st.markdown("---")` and `st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")`
  - Renders a button `"Ejecutar Análisis de Literatura Reciente"`
  - On button press: shows `st.spinner`, calls `st.session_state.sota_analyzer.analyze_sota(md_text)`, then renders conclusion, papers dataframe, and missing-paper recommendations via `_render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)`
  - Does NOT write to `st.session_state` directly (sota_analyzer is already in session state)
SOURCE: sota_section.py:5

FUNCTION: render_chatbot
SIGNATURE: render_chatbot(md_text)
  — No type annotation in source. Inferred type from extraction: `md_text: str`.
PARAMETERS:
  - md_text: str — the full Markdown text of the uploaded paper; passed to `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` on submit
RETURN: None (no return statement; function renders UI only)
SIDE_EFFECTS:
  - Renders `st.markdown("---")`, `st.header("💬 Pregunta al Revisor")`, caption, conversation history, text input (`key="chat_input"`), and submit button (`key="send_button"`)
  - On submit: appends `{"role": "user", "content": prompt_usuario}` to `st.session_state.messages`; calls `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` → appends assistant response to `st.session_state.messages`; calls `st.rerun()`
  - READS: `st.session_state.messages`
  - WRITES: `st.session_state.messages` (appends two entries: user message and assistant response)
SOURCE: chatbot.py:4

---

## g_008 — TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION

**Original GAP location:** GAP-cluster_root_tests_scratch_01-005
**Resolution source:** extracted_frontend_01.md § 2.1 Application-level constants (`frontend/config.py`)
**Source file:line:** config.py:3–5

### Resolved Content

CONSTANT: TITLE
  VALUE: "💻 Auditor de Papers en Ciencias de la Computación"
  TYPE: str
  PURPOSE: Page title displayed via `st.title(TITLE)` in `app.py:25`; also used as page heading
  SOURCE: config.py:3

CONSTANT: SIDEBAR_IMAGE
  VALUE: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"
  TYPE: str
  PURPOSE: URL of the ACM logo (Wikipedia CDN); displayed in the sidebar via `st.image(SIDEBAR_IMAGE, width=150)`
  SOURCE: config.py:4

CONSTANT: SIDEBAR_DESCRIPTION
  VALUE: "Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."
  TYPE: str
  PURPOSE: Descriptive text displayed in the sidebar via `st.write(SIDEBAR_DESCRIPTION)`
  SOURCE: config.py:5

---

## g_013 — get_checklist_health

**Original GAP location:** GAP-cluster_root_tests_scratch_01-010
**Resolution source:** extracted_frontend_01.md § 7.1 `get_checklist_health` (`frontend/utils/scoring.py`)
**Source file:line:** scoring.py:37

### Resolved Content

FUNCTION: get_checklist_health
SIGNATURE: get_checklist_health(evaluation: dict) -> dict
  — Type annotations confirmed present in source: `def get_checklist_health(evaluation: dict) -> dict:`
PARAMETERS:
  - evaluation: dict — keyed by the 16 CHECKLIST_KEYS. Expected structure per key:
      {
        "answer":          str,          # "Yes" / "No" / "N/A" / "" (case-insensitive comparison used)
        "justification":   str,
        "evidence":        str,
        "is_no_justified": bool or str   # True/False or "true"/"false"
      }
RETURN:
  TYPE: dict
  KEYS:
    - status: str — "valid" if pending_count == 0, else "risk"
      SOURCE: scoring.py:122-123
    - pending_count: int — count of items that triggered a risk rule (missing evidence for "Yes" answers, or missing justification for "No" answers)
      SOURCE: scoring.py:122-126
    - total: int — len(items); always 16 when evaluation is non-empty; 0 when evaluation is falsy (early-exit path)
      SOURCE: scoring.py:127
    - items: list of dicts — one dict per checklist key in CHECKLIST_KEYS order. Each item dict has these keys:
        - "key":                  str  — the CHECKLIST_KEYS key string
        - "label":                str  — human-readable label from CHECKLIST_LABELS.get(key, key)
        - "answer":               str  — answer_raw (the stripped answer string) if non-empty, else "—"
        - "evidence":             str  — display_evidence: evidence if evidence else (justification if justification else "—")
        - "justification":        str  — the stripped justification string (may be empty str)
        - "is_no_justified":      bool — normalised from raw value (str "true"/"false" or bool)
        - "pending_justification": bool — True when "no" in answer and (not is_no_justified OR not justification)
        - "missing_evidence":     bool — True when "yes" in answer and (not evidence AND not justification)
        - "alert_msg":            str  — describes the risk; empty str if no risk; may include special suffix "⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria." for key "crowdsourcing_human_subjects"
      SOURCE: scoring.py:110-120
EARLY_EXIT_GUARD:
  When evaluation is falsy (None, {}, etc.): returns immediately with
  {"status": "risk", "items": [], "pending_count": 0, "total": 0}
  SOURCE: scoring.py:56-62
SOURCE: scoring.py:37

---

## g_026 — apply_custom_styles

**Original GAP location:** GAP-cluster_root_tests_scratch_01-023
**Resolution source:** extracted_frontend_01.md § 6. Custom CSS & Styling (`frontend/styles/custom_css.py`)
**Source file:line:** custom_css.py:85

### Resolved Content

FUNCTION: apply_custom_styles
SIGNATURE: apply_custom_styles() -> None
  — No return type annotation in source; returns implicitly None.
PARAMETERS: none
RETURN: None
MECHANISM: Calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)` where CUSTOM_CSS is the module-level constant defined at custom_css.py:4-83
SOURCE: custom_css.py:85-86

CSS_SCOPE: The CUSTOM_CSS string constant defines a `<style>` block targeting the following selectors:

| Selector | Properties applied |
|----------|--------------------|
| `.stApp` | `background-color: #374151 !important` — dark grey app background |
| `#MainMenu` | `visibility: hidden` — hides Streamlit hamburger menu |
| `footer` | `visibility: hidden` — hides Streamlit footer |
| `header` | `background-color: transparent !important` — transparent header |
| `[data-testid="stTable"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 5px !important` — table container dark bg with rounded corners |
| `[data-testid="stTable"] table` | `border-collapse: collapse !important; width: 100% !important; border: none !important` — eliminates duplicate border lines |
| `[data-testid="stTable"] th` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; background-color: #3d4446 !important; border: 1px solid #4a4a4a !important; padding: 12px !important; text-transform: capitalize !important` |
| `[data-testid="stTable"] th *` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; text-decoration: none !important; border: none !important; text-transform: capitalize !important` |
| `[data-testid="stTable"] tbody th` | `color: #FFFFFF !important; font-size: 16px !important; background-color: #2d3436 !important` |
| `[data-testid="stTable"] tbody th *` | `color: #FFFFFF !important; font-size: 16px !important; background-color: transparent !important` |
| `[data-testid="stTable"] td` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; background-color: transparent !important; border: 1px solid #4a4a4a !important; padding: 12px !important` |
| `[data-testid="stTable"] td *` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; text-decoration: none !important; border: none !important` |
| `[data-testid="stPlotlyChart"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 10px !important` — Plotly chart container |

SOURCE: custom_css.py:4-83 (CUSTOM_CSS constant), custom_css.py:85-86 (apply_custom_styles function)

---

## g_027 — initialize_session_state

**Original GAP location:** GAP-cluster_root_tests_scratch_01-024
**Resolution source:** extracted_frontend_01.md § 3. Session State (table) and File Index row 13 (`frontend/utils/session_state.py`)
**Source file:line:** session_state.py:7

### Resolved Content

FUNCTION: initialize_session_state
SIGNATURE: initialize_session_state() -> None
  — No return type annotation in source; returns implicitly None.
PARAMETERS: none
RETURN: None
SESSION_STATE_WRITES:
  All 5 keys are written with the guard `if "key" not in st.session_state` (conditional, not unconditional assignment).
  - st.session_state['resultado']:      default value None  (type: NoneType initially; becomes dict after audit)
    SOURCE: session_state.py:8-9
  - st.session_state['auditor']:        default value PaperAuditor()  (type: PaperAuditor instance)
    SOURCE: session_state.py:11-12 (guard: `if 'auditor' not in st.session_state`)
  - st.session_state['chatbot']:        default value PaperChatbot()  (type: PaperChatbot instance)
    SOURCE: session_state.py:14-15 (guard: `if 'chatbot' not in st.session_state`)
  - st.session_state['sota_analyzer']:  default value SotaAnalyzer()  (type: SotaAnalyzer instance)
    SOURCE: session_state.py:17-18 (guard: `if 'sota_analyzer' not in st.session_state`)
  - st.session_state['messages']:       default value []  (type: list of dicts)
    SOURCE: session_state.py:20-21 (guard: `if "messages" not in st.session_state`)
GUARD_CONDITION: All 5 keys use `if "key" not in st.session_state` guard — idempotent; already-set keys are NOT overwritten on subsequent calls. Confirmed from source: each block is `if "key" not in st.session_state: st.session_state.key = <default>`.
NOTE: The following additional session-state keys exist at runtime but are NOT initialised by `initialize_session_state`; they are set lazily by `file_uploader.py`:
  - `archivo_actual` (str): set to `uploaded_file.name` on first upload
  - `file_hash` (str, MD5 hex): set to file content hash on first upload
  - `md_text` (str): set to extracted text on first upload
  SOURCE: extracted_frontend_01.md § 3 (additional session state table) / file_uploader.py:19-20,36-39
SOURCE: session_state.py:7
