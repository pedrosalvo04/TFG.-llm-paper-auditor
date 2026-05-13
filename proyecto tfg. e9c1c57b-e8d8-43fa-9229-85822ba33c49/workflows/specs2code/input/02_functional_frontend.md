# 02 — Frontend Functional Specification

**Writer agent:** functional_writer_frontend  
**Sources consumed:**
- `extracted_frontend_01.md` (primary extraction — cluster_frontend_01)
- `extracted_root_tests_scratch_01.md` (primary extraction — cluster_root_tests_scratch_01)
- `cross_ref_resolution_cross_ref_root_to_frontend.md` (gap resolutions g_004–g_008, g_013, g_026, g_027)

---

## 1. Application Bootstrap Sequence

The application entry point is `frontend/app.py` (76 lines). Steps 1–6 execute in source order (top-to-bottom); the sidebar block at lines 73–76 appears last in source and is documented as Step 7 below.

(Source: extracted_frontend_01.md §4.2 Top-level rendering order)

---

### Step 1 — `st.set_page_config`

```
TRIGGER: Python module load of app.py (executed before any widget statement)
CONDITION: Must be the first Streamlit call; comment in source: "IMPORTANTE: configure_page() debe ser lo primero"
ACTION: st.set_page_config(
    page_title="NeurIPS 2026 Checklist Auditor",
    layout="wide",
    page_icon="🔬"
)
RESULT: Browser tab shows "NeurIPS 2026 Checklist Auditor" with microscope icon; page uses wide layout.
```

Note: `extracted_root_tests_scratch_01.md §3.2` records `page_title="Nature Auditor Pro"` from a later version of `app.py`. The frontend cluster extraction (`extracted_frontend_01.md §2.2`) records `page_title="NeurIPS 2026 Checklist Auditor"`. Both sources agree on `layout="wide"` and `page_icon="🔬"`. The most specific and authoritative value is `"NeurIPS 2026 Checklist Auditor"` (Source: extracted_frontend_01.md §2.2, app.py:6-10).

NOTE: `frontend/app.py` contains no `os.environ` or `warnings.filterwarnings` calls. The following environment variables are set in the **alternate root entry point** `app.py` (88 lines at the repository root), which is a separate file from `frontend/app.py`. They are listed here for reference because the extraction corpus documented them together, but they belong to the root entry point only (SOURCE: root/app.py:13-22):

| Variable | Value set | Purpose |
|----------|-----------|---------|
| `TRANSFORMERS_VERBOSITY` | `"error"` | Suppresses transformers library logs |
| `TOKENIZERS_PARALLELISM` | `"false"` | Suppresses tokenizer parallelism warnings |
| `ANONYMIZED_TELEMETRY` | `"False"` | Disables ChromaDB telemetry |
| `OTEL_SDK_DISABLED` | `"true"` | Disables OpenTelemetry SDK (avoids Streamlit conflicts) |

Also sets three `warnings.filterwarnings("ignore", ...)` calls and `logging.getLogger("transformers").setLevel(logging.ERROR)` (Source: extracted_root_tests_scratch_01.md §3.1, root/app.py:13-22).

---

### Step 2 — `apply_custom_styles`

```
TRIGGER: Immediately after st.set_page_config; SOURCE: app.py:21
CONDITION: None (unconditional call)
ACTION: Calls apply_custom_styles() from frontend.styles.custom_css
RESULT: Injects the CUSTOM_CSS <style> block via st.markdown(CUSTOM_CSS, unsafe_allow_html=True).
        CSS targets: .stApp background, #MainMenu, footer, header, [data-testid="stTable"] family,
        and [data-testid="stPlotlyChart"]. Full CSS detail in Section 2 of this spec is referenced
        here; see also §2.6 of the extraction.
```

(Source: extracted_frontend_01.md §6 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_026)

---

### Step 3 — `initialize_session_state`

```
TRIGGER: Immediately after apply_custom_styles(); SOURCE: app.py:22
CONDITION: None (unconditional call); internally each key is guarded by "if key not in st.session_state"
ACTION: Calls initialize_session_state() from frontend.utils.session_state
RESULT: Ensures 5 session state keys exist with their defaults.
        Full schema documented in Section 2.
```

(Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_027)

---

### Step 4 — Page title and "Limpiar" button

```
TRIGGER: After initialize_session_state(); SOURCE: frontend/app.py:25-32
ACTION:
  st.title(TITLE)        — renders page heading with TITLE constant
  st.markdown("---")     — horizontal rule
  st.button("🔄 Limpiar y subir nuevo archivo", key not specified)
CONDITION (on button): if clicked →
  for key in list(st.session_state.keys()):
      del st.session_state[key]          SOURCE: app.py:32
  st.rerun()                             SOURCE: app.py:33
  All session_state keys are deleted, including service instances:
    auditor (PaperAuditor), chatbot (PaperChatbot), sota_analyzer (SotaAnalyzer),
    resultado, md_text, messages, archivo_actual, file_hash.
  No try/except wraps this block.
  On the next Streamlit rerun, initialize_session_state() recreates all
  service instances fresh (new PaperAuditor(), PaperChatbot(), SotaAnalyzer()).
RESULT: Title constant is "💻 Auditor de Papers en Ciencias de la Computación".
        Clicking the "Limpiar" button resets the entire application state.
ERROR:
  No user-catchable error path exists for this button block.
  - dict key deletion (del st.session_state[key]) does not raise on valid keys;
    no exception handling is present in the source.
  - st.rerun() internally raises Streamlit's RerunException (a subclass of
    BaseException, not Exception), caught exclusively by the Streamlit runtime
    before returning to user code. User code cannot catch or recover from it.
  - No session corruption guard is implemented in the source.
```

(Source: extracted_frontend_01.md §4.2 / §8 RULE:ClearAndReset, app.py:31-33, session_state.py:7-22)

---

### Step 5 — File upload widget

```
TRIGGER: After title+button; SOURCE: app.py:34
ACTION:
  uploaded_file = st.file_uploader(
      "Sube el PDF del artículo científico",
      type=["pdf", "txt", "md"]
  )
RESULT: Widget rendered; uploaded_file is None until user selects a file.
```

(Source: extracted_frontend_01.md §5.1, app.py:34)

---

### Step 6 — Conditional: if uploaded_file is not None

```
TRIGGER: uploaded_file is not None (user has uploaded a file)
CONDITION: `if uploaded_file:`
ACTION sequence (SOURCE: frontend/app.py:36-70):
  6a. md_text, resultado = process_uploaded_file(uploaded_file)   — see Section 3
                                                       SOURCE: frontend/app.py:37
  6b. Branch on resultado content:
      - resultado and "error" in resultado:
          err = resultado["error"]
          If err == "INVALID_PAPER_TYPE"
            → st.error(f"❌ Paper no válido: {resultado.get('message', 'Solo se evalúan papers de ML/AI')}")
          Else
            → st.error(f"❌ Error en la auditoría: {err}")
      - resultado and "evaluation_error" in resultado
            → st.error(f"❌ Error del LLM: {evaluation_error}")
              st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")
              st.info("💡 Tip: Recarga la página o sube el archivo nuevamente.")
      - resultado and resultado.get("claims") is truthy (SUCCESS PATH):
            → Step 6c (render_audit_results)
            → Step 6d (render_sota_analysis)
            → Step 6e (render_chatbot)
            → Step 6f (download button)
      - resultado truthy but no "claims" and no error keys
            → st.error("⚠️ La auditoría no generó resultados válidos.")
              st.info("Posibles causas: respuesta vacía del LLM o JSON inválido.")
      - resultado is falsy/None
            → st.warning("⚠️ No hay resultado disponible.")
```

---

### Step 6c — `render_audit_results`

```
TRIGGER: resultado.get("claims") is truthy; SOURCE: frontend/app.py:50,52
CONDITION: SUCCESS PATH only
ACTION: health = render_audit_results(resultado, uploaded_file)
RESULT: Renders full audit results page (verdict, metrics, RAG ficha, compliance table, expanders).
        Returns health dict (stored as health). See Section 4.
```

---

### Step 6d — `render_sota_analysis`

```
TRIGGER: Immediately after render_audit_results; SOURCE: frontend/app.py:53
CONDITION: SUCCESS PATH only
ACTION: render_sota_analysis(md_text)
RESULT: Renders SOTA analysis section with on-demand button trigger. See Section 7.
```

---

### Step 6e — `render_chatbot`

```
TRIGGER: Immediately after render_sota_analysis; SOURCE: frontend/app.py:54
CONDITION: SUCCESS PATH only
ACTION: render_chatbot(md_text)
RESULT: Renders interactive chatbot section. See Section 8.
```

---

### Step 6f — Download report button

```
TRIGGER: After render_chatbot; SOURCE: frontend/app.py:56-65
CONDITION: SUCCESS PATH only
ACTION:
  st.markdown("---")                                           SOURCE: frontend/app.py:57
  st.subheader("📄 Descargar Informe")                         SOURCE: frontend/app.py:58
  reporte = generate_report(resultado, uploaded_file, health)  SOURCE: frontend/app.py:59
  st.download_button(
      label="📥 Descargar Informe Completo (.md)",
      data=reporte,
      file_name=f"auditoria_neurips_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md",
      mime="text/markdown"
  )
RESULT: User can download the Markdown audit report.
```

(Source: extracted_frontend_01.md §4.2 / §10.8, frontend/app.py:56-65)

---

### Step 7 — Sidebar render

```
TRIGGER: Executed after all main content (lines 73–76 of frontend/app.py, after the uploaded_file block)
CONDITION: None (unconditional; sidebar is always rendered on every rerun)
ACTION:
  with st.sidebar:
    st.image(SIDEBAR_IMAGE, width=150)     SOURCE: frontend/app.py:74
    st.markdown("### Sobre el TFG")       SOURCE: frontend/app.py:75
    st.write(SIDEBAR_DESCRIPTION)         SOURCE: frontend/app.py:76
RESULT: Sidebar panel displays ACM logo (150px wide) and a descriptive paragraph.
NOTE: Although the `with st.sidebar:` block is at source lines 73–76 (after all main content),
      Streamlit renders sidebar widgets in the sidebar UI panel independently of their code position.
      The sidebar is always visible regardless of which main-page branch is active.
```

Constants used (Source: extracted_frontend_01.md §2.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_008, frontend/app.py:73-76):
- `SIDEBAR_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"`
- `SIDEBAR_DESCRIPTION = "Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."`

---

## 1b. Alternate Entry Point — Root `app.py` (88 lines)

The repository root contains a second, older application entry point: `TFG.-llm-paper-auditor-multimodels/app.py` (88 lines). This file is **distinct from** `frontend/app.py`. It imports and calls the same frontend components but has several key differences documented below.

**Primary entry point:** `frontend/app.py` — 76 lines; the canonical refactored module.  
**Alternate entry point:** root `app.py` — 88 lines; earlier version with different call patterns.

(Source: root/app.py:1-88; verified by wc -l)

---

### 1b.1 Differences from `frontend/app.py`

| Attribute | `frontend/app.py` (canonical) | root `app.py` (alternate) | Source |
|-----------|-------------------------------|---------------------------|--------|
| Line count | 76 | 88 | wc -l |
| `page_title` | `"NeurIPS 2026 Checklist Auditor"` | `"Nature Auditor Pro"` | root/app.py:26 |
| `page_icon` | `"🔬"` | `"🔬"` | root/app.py:28 |
| `file_uploader` label | `"Sube el PDF del artículo científico"` | `"Sube el artículo científico (PDF, TXT o Markdown)"` | root/app.py:48-51 |
| `process_uploaded_file` capture | Direct: `md_text, resultado = process_uploaded_file(uploaded_file)` | Two-step: call without capture, then read `st.session_state.get('resultado')` / `st.session_state.get('md_text')` | root/app.py:54-58 |
| Return variable for `render_audit_results` | `health` | `puntuacion` | root/app.py:66 |
| Download filename | `f"auditoria_neurips_{...}.md"` | `f"auditoria_{...}.md"` (no `_neurips_`) | root/app.py:77 |
| Sidebar position | Lines 73–76 (after all main content) | Lines 84–88 (after all main content) | root/app.py:84-88 |
| Env var / logging setup | None (not present) | Yes — `TRANSFORMERS_VERBOSITY`, `TOKENIZERS_PARALLELISM`, `ANONYMIZED_TELEMETRY`, `OTEL_SDK_DISABLED`, three `warnings.filterwarnings`, `logging.setLevel` | root/app.py:13-22 |
| Error handling for "error" key | Separate `INVALID_PAPER_TYPE` check + generic fallback | Single `st.error(f"❌ Error en la auditoría: {resultado['error']}")` | root/app.py:60-61 |
| Fallback for invalid result | `st.error(...)` + `st.info(...)` | `st.error(...)` + `st.json(resultado)` | root/app.py:81-82 |

### 1b.2 Env Var Initialization (root `app.py` only)

```
TRIGGER: Module load of root app.py (before any Streamlit import)
ACTION:
  os.environ["TRANSFORMERS_VERBOSITY"] = "error"    SOURCE: root/app.py:13
  os.environ["TOKENIZERS_PARALLELISM"] = "false"    SOURCE: root/app.py:14
  warnings.filterwarnings("ignore", message=".*Accessing.*__path__.*")  SOURCE: root/app.py:15
  warnings.filterwarnings("ignore", category=FutureWarning)             SOURCE: root/app.py:16
  warnings.filterwarnings("ignore", category=UserWarning)               SOURCE: root/app.py:17
  logging.getLogger("transformers").setLevel(logging.ERROR)             SOURCE: root/app.py:18
  os.environ["ANONYMIZED_TELEMETRY"] = "False"      SOURCE: root/app.py:21
  os.environ["OTEL_SDK_DISABLED"] = "true"          SOURCE: root/app.py:22
RESULT: Suppresses noisy logs from transformers, huggingface, ChromaDB, and OpenTelemetry.
NOTE: frontend/app.py does NOT perform this initialization.
```

---

## 2. Session State Schema and Initialization

`initialize_session_state()` is defined in `frontend/utils/session_state.py` (22 lines). It uses the guard `if "key" not in st.session_state` for every key — the function is idempotent and will NOT overwrite keys already set. (Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_027, session_state.py:7)

### 2.1 Keys initialised by `initialize_session_state`

| Key | Type | Default | Guard Condition | Purpose | Source |
|-----|------|---------|-----------------|---------|--------|
| `resultado` | `dict` or `None` | `None` | `if "resultado" not in st.session_state` | Holds the full audit result dict returned by `auditor.audit()`; `None` before first audit; `{"error": ...}` on failure | session_state.py:8-9 |
| `auditor` | `PaperAuditor` instance | `PaperAuditor()` | `if 'auditor' not in st.session_state` | Backend audit engine; exposes `audit(md_text, status_callback)` | session_state.py:11-12 |
| `chatbot` | `PaperChatbot` instance | `PaperChatbot()` | `if 'chatbot' not in st.session_state` | Backend chatbot engine; exposes `preguntar(md_text, question, history_str)` | session_state.py:14-15 |
| `sota_analyzer` | `SotaAnalyzer` instance | `SotaAnalyzer()` | `if 'sota_analyzer' not in st.session_state` | Backend SOTA analysis engine; exposes `analyze_sota(md_text)` | session_state.py:17-18 |
| `messages` | `list` of dicts | `[]` | `if "messages" not in st.session_state` | Chat history; each entry is `{"role": str, "content": str}` | session_state.py:20-21 |

### 2.2 Additional session state keys set lazily by `file_uploader.py`

These keys are NOT set by `initialize_session_state`; they are written on first (or new) file upload.

| Key | Type | Initial Value | Set When | Read When | Source |
|-----|------|---------------|----------|-----------|--------|
| `archivo_actual` | `str` | not pre-set | `file_uploader.py:19` — set to `uploaded_file.name` | `file_uploader.py:16` — compared to detect file change | file_uploader.py:19 |
| `file_hash` | `str` (MD5 hex, 32 chars) | not pre-set | `file_uploader.py:20` — set to `hashlib.md5(uploaded_file.getvalue()).hexdigest()` | `file_uploader.py:17` — compared to detect content change | file_uploader.py:20 |
| `md_text` | `str` | not pre-set | `file_uploader.py:36` (PDF) or `file_uploader.py:39` (TXT/MD) | `chatbot.py:26`; `sota_section.py:12`; `app.py:53-54`; `file_uploader.py:98` | file_uploader.py:36,39 |

---

## 3. File Upload Flow (`process_uploaded_file`)

**File:** `frontend/components/file_uploader.py` (101 lines)  
**Function signature:** `process_uploaded_file(uploaded_file)` — no type annotations; `uploaded_file` is a Streamlit `UploadedFile` object.  
**Return value:** `tuple (md_text: str, resultado: dict)` — both values are read from `st.session_state` at the end of the function: `st.session_state.get('md_text', '')` and `st.session_state.get('resultado', {})`.  
(Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_004, file_uploader.py:6,98-100)

---

### 3.1 MD5 Deduplication

```
TRIGGER: process_uploaded_file called with an uploaded file object.
CONDITION:
  1. file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()   (SOURCE: file_uploader.py:11-12)
  2. Check: ("archivo_actual" not in st.session_state)
         OR (st.session_state.archivo_actual != uploaded_file.name)
         OR (st.session_state.get('file_hash') != file_hash)
                                                                    (SOURCE: file_uploader.py:15-17)
ACTION (if condition TRUE — new file detected):
  - Proceed to full processing pipeline (steps 3.2 – 3.4).
ACTION (if condition FALSE — same file already processed):
  - Skip all processing.
  - Return (st.session_state.get('md_text', ''), st.session_state.get('resultado', {})) immediately.
                                                                    (SOURCE: file_uploader.py:15-101)
```

---

### 3.2 File Type Branching

When a new file is detected, the following steps execute in order before audit invocation:

```
STEP 1:
  st.session_state.archivo_actual = uploaded_file.name             SOURCE: file_uploader.py:19
  st.session_state.file_hash      = file_hash                      SOURCE: file_uploader.py:20
  st.session_state.messages       = []                             SOURCE: file_uploader.py:21

STEP 2: Create temp directory and write temp file
  os.makedirs("temp")   (if "temp/" directory does not exist)      SOURCE: file_uploader.py:23-24
  temp_path = os.path.join("temp", uploaded_file.name)
  Write uploaded_file bytes to temp_path                           SOURCE: file_uploader.py:30-31

STEP 3: Determine file type
  CONDITION: file_extension = uploaded_file.name.split('.')[-1].lower()
  DETECTION: by file extension (not MIME type)                     SOURCE: file_uploader.py:27

STEP 4 — Extraction (inside st.spinner("📂 Extrayendo texto...")):
  ACTION (PDF branch):
    if file_extension == 'pdf':
      st.session_state.md_text = convert_pdf_to_markdown(temp_path)
      — convert_pdf_to_markdown is CROSS-REFERENCE: backend/services/pdf_parser.py
                                                                    SOURCE: file_uploader.py:35-36
  ACTION (TXT/MD branch):
    elif file_extension in ['txt', 'md']:
      with open(temp_path, 'r', encoding='utf-8') as f:
        st.session_state.md_text = f.read()
                                                                    SOURCE: file_uploader.py:37-39
  ERROR (unsupported extension):
    else:
      st.error(f"❌ Formato no soportado: {file_extension}")
      return (None, {'error': 'Formato no soportado: {file_extension}'})
                                                                    SOURCE: file_uploader.py:41-42
```

(Source: extracted_frontend_01.md §5.1, §2.8)

---

### 3.3 Auditor Invocation

```
TRIGGER: After successful file parsing (st.session_state.md_text is set).

STEP 1: Open status block
  status = st.status("🧠 Analizando el documento...", expanded=True)
                                                                    SOURCE: file_uploader.py:45
STEP 2: Define status_callback
  def update_status(msg):
      st.write(msg)
  — This callback receives progress messages from the backend and renders them
    as text inside the st.status block during processing.
                                                                    SOURCE: file_uploader.py:46-47
STEP 3: Invoke auditor
  ACTION: st.session_state.resultado = st.session_state.auditor.audit(
              st.session_state.md_text,
              status_callback=update_status
          )
  — Returns a dict with keys: the 16 CHECKLIST_KEYS plus optional keys:
    "metricas", "informacion_extraida", "general_analysis_map",
    "original_extraction_raw", "hybrid_triage_fragments",
    "extracted_hyperparameters_hybrid", "evaluation_signals"
  — On error: returns dict with key "error" (str)
                                                                    SOURCE: file_uploader.py:49-52

STEP 4: Error handling on resultado
  CONDITION: "error" in resultado
    Sub-condition A (SATURATION):
      any(x in str(resultado['error']).upper() for x in
          ["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"])
      ACTION:
        status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)
        st.error("### ⚠️ El servicio de IA está saturado")
        Renders expander with explanation text.
        Renders st.info with retry guidance.
        Renders 2 buttons:
          "🔄 Reintentar ahora" → st.rerun()
          "🚫 Cancelar ejecución" → st.session_state.resultado = {"error": "Ejecución cancelada..."}
                                    → st.stop()
        Calls st.stop() to halt normal flow.
                                                                    SOURCE: file_uploader.py:56-88
    Sub-condition B (non-saturation error):
      ACTION:
        status.update(label="❌ La auditoría ha fallado", state="error", expanded=True)
        st.error(f"❌ Error crítico: {error_msg}")
        st.session_state.resultado = {"error": error_msg}
        Delete temp file if exists.
        st.stop()
                                                                    SOURCE: file_uploader.py:86-88

STEP 5 (SUCCESS):
  status.update(label="✅ Análisis completado", state="complete", expanded=False)
  st.success("✅ Análisis completado")
                                                                    SOURCE: file_uploader.py:90-92
```

(Source: extracted_frontend_01.md §5.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_004)

---

### 3.4 Temp File Lifecycle

```
CREATION:
  Directory: "temp/" (relative to working directory)
  Path: temp_path = os.path.join("temp", uploaded_file.name)
  Creation trigger: os.makedirs("temp") called before writing
                                                                    SOURCE: file_uploader.py:23-24

WRITE:
  File bytes written immediately after directory creation.
                                                                    SOURCE: file_uploader.py:30-31

DELETION:
  os.remove(temp_path) — called if temp file exists after processing (success or non-saturation error)
  Pattern: guarded check (if os.path.exists(temp_path)) before removal
                                                                    SOURCE: file_uploader.py:94-95

NOTE: No try/finally is explicitly documented in extraction data; deletion occurs in the
  error-handling path (non-saturation) and in the success path.
  [GAP: exact try/finally or context-manager structure around temp file lifecycle not confirmed in extraction]

OS CONSIDERATIONS: Requires filesystem write permission for the "temp/" relative directory.
  If unavailable (e.g., read-only container filesystem), processing will fail with an OS error.
                                                                    SOURCE: GAP-ext_frontend_01-006
```

---

## 4. Audit Results Rendering (`render_audit_results`)

**File:** `frontend/components/audit_results.py` (317 lines)  
**Function signature:** `render_audit_results(resultado: dict, uploaded_file) -> health: dict`  
**Return value:** `dict` returned by `get_checklist_health(resultado)` — keys: `"status"`, `"items"`, `"pending_count"`, `"total"`. (Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_005, audit_results.py:90,284)

Widgets rendered in the following order:

---

### 4.1 Success Banner

```
TRIGGER: Function entry (unconditional).
ACTION: st.success("Auditoria Finalizada")
CONDITION: Always displayed when render_audit_results is called.
```

(Source: extracted_frontend_01.md §5.2 step 1, audit_results.py:92)

---

### 4.2 Health Verdict

```
TRIGGER: After st.success banner.
ACTION:
  health = get_checklist_health(resultado)          SOURCE: audit_results.py:94
  pending = health["pending_count"]
  total   = health["total"]
  st.header("Veredicto del Checklist NeurIPS 2026") SOURCE: audit_results.py:100

CONDITION (health["status"] == "valid"):
  Renders dark-green <div> containing:
    - Text: "Checklist Valido"
    - Sub-text: "Todas las respuestas tienen evidencia o justificacion documentada.
                 El checklist esta listo para NeurIPS."
                                                    SOURCE: audit_results.py:102-109

CONDITION ELSE (health["status"] == "risk"):
  Renders dark-red <div> containing:
    - Text: "Riesgo de Desk Reject"
    - Sub-text: f"{pending} de {total} item(s) requieren accion del autor antes del envio."
                                                    SOURCE: audit_results.py:111-117
```

(Source: extracted_frontend_01.md §5.2 step 4)

---

### 4.3 4-Column Metrics Row

```
TRIGGER: After health verdict block.
ACTION: Creates 4 Streamlit columns; renders one st.metric per column.
                                                    SOURCE: audit_results.py:121-133

Column layout:
  col1: st.metric("Items Yes",  <count of items where "yes" in item["answer"].lower()>)
  col2: st.metric("Items No",   <count of items where "no"  in item["answer"].lower()>)
  col3: st.metric("Items N/A",  <count of items where "n/a" in item["answer"].lower()>)
  col4: st.metric("Tiempo",     f"{tiempo}s")
        where tiempo = resultado.get("metricas", {}).get("tiempo_segundos", "N/A")
```

(Source: extracted_frontend_01.md §5.2 step 5)

---

### 4.4 RAG Ficha Técnica

```
TRIGGER: After metrics row.
CONDITION: rag_data = resultado.get("extracted_hyperparameters_hybrid", {}) — displayed only if truthy.
ACTION:
  st.subheader("🎯 Ficha Técnica de Entrenamiento (RAG Specialist)")
  st.caption("Estos datos han sido extraídos mediante un escaneo profundo (RAG)
              de las secciones técnicas y apéndices.")
  Layout: 4 columns (c1, c2, c3, c4)
  c1: st.code(rag_data.get("optimizer",      "N/A"))
      st.code(rag_data.get("learning_rate",  "N/A"))
  c2: st.code(rag_data.get("batch_size",     "N/A"))
      st.code(rag_data.get("epochs",         "N/A"))
  c3: st.code(rag_data.get("warmup_steps",   "N/A"))
      st.code(rag_data.get("weight_decay",   "N/A"))
  c4: st.info(rag_data.get("hardware",       "N/A"))
      st.code(rag_data.get("random_seed",    "N/A"))
        — shown only if rag_data.get("random_seed") AND rag_data.get("random_seed") != "NOT FOUND"
                                                    SOURCE: audit_results.py:136-163
```

(Source: extracted_frontend_01.md §5.2 step 6)

---

### 4.5 Compliance Table (`_build_table_html`)

```
TRIGGER: After RAG Ficha Técnica.
ACTION:
  st.header("Tabla de Cumplimiento NeurIPS 2026")
  st.caption(...)  — colour legend caption
  table_html = _build_table_html(health["items"])
  st.html(table_html)
                                                    SOURCE: audit_results.py:167-175
```

#### `_build_table_html(items: list) -> str`

(Source: extracted_frontend_01.md §5.2.1, audit_results.py:7-87)

**Parameters:** `items` — list of 16 item dicts from `get_checklist_health()`.  
**Returns:** Complete HTML table string.

**Per-row logic:**

```
For each item dict in items:
  1. Split item["label"] on ". " to get num and name:
       if ". " in item["label"]:
           num, name = item["label"].split(". ", 1)
       else:
           num = str(idx)   # 1-based iteration index
           name = item["label"]
                                                    SOURCE: audit_results.py:39-42

  2. evidence_text:
       item["evidence"] if item["evidence"] and item["evidence"] != "-" else ""
                                                    SOURCE: audit_results.py:44

  3. Row background (from row_bg(item)):
       pending_justification == True       → "#450a0a"  (deep red — Critical risk)
       missing_evidence == True OR         → "#452e0a"  (amber/orange — Warning)
         alert_msg non-empty
       "yes" in answer (lowercased)        → "#064e3b"  (emerald green — OK)
       all other cases                     → "#111827"  (neutral dark)
                                                    SOURCE: audit_results.py:18-32

  4. Badge HTML (for Respuesta column):
       "yes" in answer.lower() → background:#065f46; color:#6ee7b7; text:"Yes"
       "no"  in answer.lower() → background:#7f1d1d; color:#fca5a5; text:"No"
       else  (N/A)             → background:#1e3a5f; color:#93c5fd; text:"N/A"
                                                    SOURCE: audit_results.py:10-16

  5. Evidence cell HTML:
       if evidence_text non-empty → <span style="color:#d1d5db;">{evidence_text}</span>
       else                       → <em style="color:#6b7280;">No disponible</em>
                                                    SOURCE: audit_results.py:48

  6. Alert line HTML:
       if item["pending_justification"]:
           alert HTML = <div style="color:#fca5a5;...">&#9888; Sin justificacion del autor &mdash;
                        Riesgo de Desk Reject</div>
                                                    SOURCE: audit_results.py:52-53
       elif item["missing_evidence"]:
           alert HTML = <div style="color:#fde68a;...">&#9888; Respuesta Yes sin evidencia de
                        seccion del paper</div>
                                                    SOURCE: audit_results.py:54-55
       Additionally: if "compensacion" in item.get("alert_msg","").lower()
                       OR "etica" in item.get("alert_msg","").lower():
           Append: <div style="color:#fde68a;...">&#9888; NeurIPS Code of Ethics:
                   compensacion minima obligatoria</div>
                                                    SOURCE: audit_results.py:57-58

  7. Row HTML: <tr> with 4 <td> cells: number, name, badge HTML, evidence+alert HTML.
```

**Generated HTML table structure:**

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
    <!-- 16 rows, one per CHECKLIST_KEY -->
  </tbody>
</table>
```

(Source: audit_results.py:69-87)

#### 16 CHECKLIST_KEYS and CHECKLIST_LABELS

| # | CHECKLIST_KEY | CHECKLIST_LABEL | Source |
|---|---------------|-----------------|--------|
| 1 | `claims` | `"1. Claims"` | scoring.py:8,17 |
| 2 | `limitations` | `"2. Limitations"` | scoring.py:9,18 |
| 3 | `theory_assumptions_proofs` | `"3. Theory, Assumptions & Proofs"` | scoring.py:10,19 |
| 4 | `experimental_result_reproducibility` | `"4. Experimental Result Reproducibility"` | scoring.py:11,20 |
| 5 | `open_access_data_code` | `"5. Open Access to Data and Code"` | scoring.py:12,21 |
| 6 | `experimental_setting_details` | `"6. Experimental Setting / Details"` | scoring.py:13,22 |
| 7 | `experiment_statistical_significance` | `"7. Experiment Statistical Significance"` | scoring.py:14,23 |
| 8 | `experiments_compute_resource` | `"8. Experiments Compute Resource"` | scoring.py:14,24 |
| 9 | `code_of_ethics` | `"9. Code of Ethics"` | scoring.py:15,25 |
| 10 | `broader_impacts` | `"10. Broader Impacts"` | scoring.py:15,26 |
| 11 | `safeguards` | `"11. Safeguards"` | scoring.py:15,27 |
| 12 | `licenses` | `"12. Licenses"` | scoring.py:15,28 |
| 13 | `assets` | `"13. Assets"` | scoring.py:15,29 |
| 14 | `crowdsourcing_human_subjects` | `"14. Crowdsourcing & Human Subjects"` | scoring.py:15,30 |
| 15 | `irb_approvals` | `"15. IRB Approvals"` | scoring.py:15,31 |
| 16 | `declaration_llm_usage` | `"16. Declaration of LLM Usage"` | scoring.py:15,32 |

(Source: extracted_frontend_01.md §2.3, scoring.py:8-34)

---

### 4.6 Expander Sections

Three expanders are rendered after the compliance table, in order:

#### Expander 1 — "Pipeline de Análisis Profundo (Map-Reduce + CoT + Context Mapping)"

(Source: extracted_frontend_01.md §5.2 step 8, audit_results.py:179-215)

```
CONTENT rendered inside this expander:

Chain-of-Thought:
  cot = resultado.get("informacion_extraida", {}).get("thought_process", "No disponible")
  st.info(cot)

Context Mapping:
  context_map = resultado.get("informacion_extraida", {}).get("context_mapping", [])
  if non-empty:
    Renders in columns (up to 5 per row)
  else:
    st.warning("No se ha podido mapear la estructura de secciones.")

Comparativa Map vs Reduce (2 columns):
  LEFT (MAP):
    map_data = resultado.get("general_analysis_map", [])
    if non-empty:
      Iterates; renders each step in st.expander(f"📦 Fragmento {i+1}") with st.json(step)
    else:
      Renders resultado.get("original_extraction_raw", {}) as JSON
  RIGHT (REDUCE):
    Renders resultado.get("informacion_extraida", {}) as JSON
```

#### Expander 2 — "Pipeline de Extracción Híbrida (RAG Specialist)"

(Source: extracted_frontend_01.md §5.2 step 9, audit_results.py:218-242)

```
CONTENT rendered inside this expander:

LEFT (Triage MAP):
  fragments = resultado.get("hybrid_triage_fragments", [])
  if non-empty:
    For each fragment:
      relevance = fragment.get("_relevance_score", "N/A")
      row_bg_color:
        "#065f46" if isinstance(relevance, int) and relevance > 70
        "#1e3a5f" otherwise
      Renders expander: "📄 Fragmento Técnico {i+1} (Relevancia: {relevance}%)"
      Inside: relevance badge, fragment["_chunk_text"] via st.caption,
              all non-underscore-prefixed fields via st.json

RIGHT (REDUCE):
  Renders resultado.get("extracted_hyperparameters_hybrid", {}) as JSON

NOTE: If hybrid_triage_fragments is empty:
  st.warning("No hay datos de triage disponibles.")
```

#### Expander 3 — "Pipeline de Evaluación (Senior Area Chair + Self-Correction)"

(Source: extracted_frontend_01.md §5.2 step 10, audit_results.py:245-283)

```
CONTENT rendered inside this expander:

Evaluation Signals:
  signals = resultado.get("evaluation_signals", {})
  if truthy:
    For each (k, msg) in signals.items():
      st.markdown(f"**Item {k.replace('_', ' ').title()}:**")
      st.info(msg)
  else:
    st.warning("No se generaron señales dinámicas para esta evaluación.")

Self-Correction Verification Details:
  Collects items from resultado where value is dict with v.get("verified") == True.
  Falls back to second-level scanning if no verified items at top level.
  If verified items found:
    For each item:
      status_label = "✨ Corregido" if data.get("was_corrected") else "✅ Confirmado"
      Renders st.expander with answer, justification (st.write), evidence (st.code)
  else:
    st.warning("La fase de verificación no reportó cambios o no está disponible.")
```

---

### 4.7 Download Button

The download button is rendered in `frontend/app.py`, not inside `render_audit_results`. See Section 1 Step 6f for full specification.

```
LABEL:     "📥 Descargar Informe Completo (.md)"
CONTENT:   reporte = generate_report(resultado, uploaded_file, health)  (str)
FILE NAME: f"auditoria_neurips_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"
MIME:      "text/markdown"
CONDITION: Only shown on SUCCESS PATH (resultado.get("claims") is truthy)
```

(Source: extracted_frontend_01.md §10.8 / §4.2, frontend/app.py:56-65)

---

## 5. Compliance Scoring (`get_checklist_health` + 16 Item Evaluation Rules)

**File:** `frontend/utils/scoring.py` (130 lines)  
(Source: extracted_frontend_01.md §7.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_013)

---

### 5.1 Function Signature

```python
def get_checklist_health(evaluation: dict) -> dict:
```

**Parameters:**
- `evaluation: dict` — keyed by the 16 CHECKLIST_KEYS. Per-key structure:
  ```python
  {
    "answer":          str,          # "Yes" / "No" / "N/A" / "" (case-insensitive)
    "justification":   str,
    "evidence":        str,
    "is_no_justified": bool or str   # True/False or "true"/"false"
  }
  ```

**Return type:** `dict` with keys:
- `"status"`: `str` — `"valid"` if `pending_count == 0`, else `"risk"` (Source: scoring.py:122-123)
- `"pending_count"`: `int` — count of items that triggered a risk rule (Source: scoring.py:122-126)
- `"total"`: `int` — `len(items)`; always 16 when evaluation is non-empty; 0 on early-exit (Source: scoring.py:127)
- `"items"`: `list` — 16 item dicts in CHECKLIST_KEYS order (Source: scoring.py:110-120)

(Source: scoring.py:37)

---

### 5.2 Per-Item Evaluation Algorithm

**Early-exit guard:**

```
CONDITION: evaluation is falsy (None, {}, etc.)
ACTION: return {"status": "risk", "items": [], "pending_count": 0, "total": 0}
SOURCE: scoring.py:56-62
```

**Per-item iteration (for each key in CHECKLIST_KEYS):**

```
1. val             = evaluation.get(key, {})
2. answer_raw      = val.get("answer", "").strip()
3. answer_norm     = answer_raw.lower()
4. justification   = val.get("justification", "").strip()
5. evidence        = val.get("evidence", "").strip()
6. is_no_justified_raw = val.get("is_no_justified", False)
7. Normalise is_no_justified:
     if isinstance(is_no_justified_raw, str):
         is_no_justified = is_no_justified_raw.lower() == "true"
     else:
         is_no_justified = bool(is_no_justified_raw)
                                                        SOURCE: scoring.py:73-77
```

**16 item evaluation rules (CHECKLIST_KEYS in order):**

```
RULE: claims (key 1)
TRIGGER: function iterates over CHECKLIST_KEYS; key = "claims"
CONDITION (missing_evidence): "yes" in answer_norm AND NOT evidence AND NOT justification
  ACTION: missing_evidence = True; pending_count += 1;
          alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."
                                                        SOURCE: scoring.py:84-89
CONDITION (pending_justification): "no" in answer_norm AND (NOT is_no_justified OR NOT justification)
  ACTION: pending_justification = True; pending_count += 1;
          alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."
                                                        SOURCE: scoring.py:90-95
CONDITION (N/A or empty): "n/a" in answer_norm OR answer_norm == ""
  AND NOT justification AND NOT evidence → no risk flagged
                                                        SOURCE: scoring.py:101-105
SPECIAL CASE (crowdsourcing): does NOT apply to key "claims"
SOURCE: scoring.py:84-105

RULE: limitations (key 2)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: theory_assumptions_proofs (key 3)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: experimental_result_reproducibility (key 4)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: open_access_data_code (key 5)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: experimental_setting_details (key 6)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: experiment_statistical_significance (key 7)
[Same risk detection logic as "claims"; no special case]
NOTE: Test data in scratch/test_checklist_health.py uses this key with answer="No",
      is_no_justified=False to verify health["status"] == "risk"
SOURCE: scoring.py:84-105 / scratch/test_checklist_health.py:33-36

RULE: experiments_compute_resource (key 8)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: code_of_ethics (key 9)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: broader_impacts (key 10)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: safeguards (key 11)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: licenses (key 12)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: assets (key 13)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: crowdsourcing_human_subjects (key 14)
TRIGGER: function iterates over CHECKLIST_KEYS; key = "crowdsourcing_human_subjects"
CONDITION (missing_evidence): "yes" in answer_norm AND NOT evidence AND NOT justification
  ACTION: missing_evidence = True; pending_count += 1;
          alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."
CONDITION (pending_justification): "no" in answer_norm AND (NOT is_no_justified OR NOT justification)
  ACTION: pending_justification = True; pending_count += 1;
          alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."
SPECIAL CASE (crowdsourcing): if "no" in answer_norm AND NOT is_no_justified:
  ADDITIONALLY appends to alert_msg:
    " ⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."
  ALSO TRIGGERS: secondary HTML alert in _build_table_html when
    "compensacion" in alert_msg.lower() OR "etica" in alert_msg.lower()
SOURCE: scoring.py:98-99 / audit_results.py:57-58

RULE: irb_approvals (key 15)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105

RULE: declaration_llm_usage (key 16)
[Same risk detection logic as "claims"; no special case]
SOURCE: scoring.py:84-105
```

**Display evidence selection (applied to every item after risk detection):**

```
display_evidence = evidence if evidence else (justification if justification else "—")
SOURCE: scoring.py:108
```

**Item dict structure appended to items list (for every key):**

```python
{
    "key":                 key,                                  # str: CHECKLIST_KEY
    "label":               CHECKLIST_LABELS.get(key, key),       # str: human-readable label
    "answer":              answer_raw if answer_raw else "—",    # str
    "evidence":            display_evidence,                     # str
    "justification":       justification,                        # str (may be empty)
    "is_no_justified":     is_no_justified,                      # bool (normalised)
    "pending_justification": pending_justification,              # bool
    "missing_evidence":    missing_evidence,                     # bool
    "alert_msg":           alert_msg,                            # str (empty if no risk)
}
SOURCE: scoring.py:110-120
```

---

### 5.3 Aggregate Health Score Computation

```
pending_count = sum of items where missing_evidence==True OR pending_justification==True
total         = len(items)  (always 16 when evaluation is non-empty)

Return value:
  {
      "status":        "valid" if pending_count == 0 else "risk",
      "items":         items,
      "pending_count": pending_count,
      "total":         total,
  }
SOURCE: scoring.py:122-127
```

No numeric score percentage is computed by this function. The function validates completeness (evidence/justification presence), not a numeric quality score. The gauge chart (`create_gauge_chart`) consumes a separate numeric score whose computation source is [GAP: numeric score computation feeding create_gauge_chart not found in extracted frontend files — gauge_chart.py caller not identified within this cluster; see GAP-ext_frontend_01-001].

---

## 6. Report Generation (`generate_report`)

**File:** `frontend/components/audit_results.py`  
(Source: extracted_frontend_01.md §5.2.2 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_006, audit_results.py:287)

---

### 6.1 Function Signature

```python
def generate_report(resultado: dict, uploaded_file, health=None) -> str:
```

**Parameters:**
- `resultado: dict` — full audit result dict; used to compute `health` if `health is None`
- `uploaded_file`: Streamlit UploadedFile — `uploaded_file.name` embedded in report header
- `health: dict or None` — default `None`; if `None`, computed via `get_checklist_health(resultado)`; if already computed (e.g. by `render_audit_results`), can be passed to avoid duplicate computation

**Return type:** `str` — complete Markdown report string.  
**Side effects:** None (pure function — no Streamlit widget calls).

(Source: audit_results.py:287)

---

### 6.2 Report Template Structure

The returned Markdown string follows this exact structure (SOURCE: audit_results.py:295-316):

```
# NeurIPS 2026 Checklist Audit Report

**Paper:** {uploaded_file.name}
**Veredicto:** {status_label}
**Items con problemas:** {pending} de {total}

---

## Tabla de Cumplimiento

| # | Item | Respuesta | Evidencia / Justificacion |
|---|------|-----------|---------------------------|
| {num} | {label} | {answer} | {evidence_or_justification}{note} |
... (16 rows total)

_Generado por Auditor NeurIPS 2026._
```

Where:
- `status_label = "Checklist Valido"` if `health["status"] == "valid"` else `"Riesgo de Desk Reject"` (Source: audit_results.py:292)
- `pending = health["pending_count"]`, `total = health["total"]`
- Per-row `note` (Source: audit_results.py:304-313):

```
CONDITION: item["pending_justification"] == True
  note = " [RIESGO: sin justificacion]"

CONDITION: item["missing_evidence"] == True  (and not pending_justification)
  note = " [RIESGO: sin evidencia]"

CONDITION: neither risk flag
  note = ""  (empty string)
```

**All 16 row formats** (note appended to evidence cell):

| Row | Key | label | Possible note suffix |
|-----|-----|-------|----------------------|
| 1 | `claims` | `1. Claims` | `" [RIESGO: sin justificacion]"` or `" [RIESGO: sin evidencia]"` or `""` |
| 2 | `limitations` | `2. Limitations` | same pattern |
| 3 | `theory_assumptions_proofs` | `3. Theory, Assumptions & Proofs` | same |
| 4 | `experimental_result_reproducibility` | `4. Experimental Result Reproducibility` | same |
| 5 | `open_access_data_code` | `5. Open Access to Data and Code` | same |
| 6 | `experimental_setting_details` | `6. Experimental Setting / Details` | same |
| 7 | `experiment_statistical_significance` | `7. Experiment Statistical Significance` | same |
| 8 | `experiments_compute_resource` | `8. Experiments Compute Resource` | same |
| 9 | `code_of_ethics` | `9. Code of Ethics` | same |
| 10 | `broader_impacts` | `10. Broader Impacts` | same |
| 11 | `safeguards` | `11. Safeguards` | same |
| 12 | `licenses` | `12. Licenses` | same |
| 13 | `assets` | `13. Assets` | same |
| 14 | `crowdsourcing_human_subjects` | `14. Crowdsourcing & Human Subjects` | same |
| 15 | `irb_approvals` | `15. IRB Approvals` | same |
| 16 | `declaration_llm_usage` | `16. Declaration of LLM Usage` | same |

(Source: extracted_frontend_01.md §5.2.2 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_006, audit_results.py:304-313)

---

### 6.3 Risk Annotation Logic

```
CONDITION: item["pending_justification"] == True
  FORMAT: " [RIESGO: sin justificacion]"
  TRIGGER: "no" in answer_norm AND (NOT is_no_justified OR NOT justification)
  SOURCE: audit_results.py:304-313

CONDITION: item["missing_evidence"] == True
  FORMAT: " [RIESGO: sin evidencia]"
  TRIGGER: "yes" in answer_norm AND NOT evidence AND NOT justification
  SOURCE: audit_results.py:304-313

CONDITION: No risk flags
  FORMAT: "" (empty string — no annotation appended)
```

Note: The HTML compliance table (Section 4.5) uses emoji markers `&#9888;` (⚠) and `🔴` in alert messages. The downloadable Markdown report uses text markers `[RIESGO: ...]` (no emoji) in the note field. (Source: cross_ref_resolution_cross_ref_root_to_frontend.md §g_006,g_013,g_026,g_027 combined)

---

## 7. SOTA Analysis UI Flow (`render_sota_analysis`)

**File:** `frontend/components/sota_section.py` (109 lines)  
**Function signature:** `render_sota_analysis(md_text: str) -> None`  
(Source: extracted_frontend_01.md §5.5 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_007, sota_section.py:5)

---

**Trigger condition:** Called from `app.py` on the SUCCESS PATH, after `render_audit_results` and before `render_chatbot`. (Source: app.py:53/67)

**Input data source:** `md_text: str` — the full Markdown text of the uploaded paper, read from `st.session_state.md_text` by the caller in `app.py` and passed as a parameter.

**Render sequence:**

```
STEP 1: st.markdown("---")
STEP 2: st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")
STEP 3: Render button "Ejecutar Análisis de Literatura Reciente" (no explicit key)
                                                    SOURCE: sota_section.py:5-10
```

**On button press:**

```
STEP 4: st.spinner("Conectando con Semantic Scholar y validando bibliografía...")
STEP 5: resultado_sota = st.session_state.sota_analyzer.analyze_sota(md_text)
        — CROSS-REFERENCE: analyze_sota() is in backend/services/sota_analyzer.py
                                                    SOURCE: sota_section.py:12

STEP 6 — Branch on resultado_sota:
  CONDITION: "error" NOT in resultado_sota (success):
    st.success("Análisis completado")
    st.markdown("### 📝 Conclusión")
    st.info(resultado_sota.get("conclusion_sota", ""))
    papers_omitidos      = resultado_sota.get("papers_omitidos", [])
    df_papers            = pd.DataFrame(resultado_sota.get("papers_analizados", []))
    año_paper_estudiado  = resultado_sota.get("metadata", {}).get("año_paper_estudiado")
    if NOT df_papers.empty AND papers_omitidos:
        _render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)
    elif NOT papers_omitidos:
        st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")
                                                    SOURCE: sota_section.py:13-27
  CONDITION: "error" in resultado_sota:
    st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")
                                                    SOURCE: sota_section.py:29
```

**`_render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)` sub-function:**

(Source: extracted_frontend_01.md §5.5.1, sota_section.py:31)

```
STEP 1: Add authors_display column:
  lambda on autores column:
    if isinstance(x, list):
      base = ', '.join([a.get('name', '') for a in x[:2]])
      suffix = ' et al.' if len(x) > 2 else ''
      return base + suffix
    else: return 'N/A'

STEP 2: Rename columns:
  'titulo' → 'title', 'año' → 'year', 'citas' → 'citationCount'

STEP 3: Build titulos_omitidos = {p['titulo'].lower().strip() for p in papers_omitidos}

STEP 4: Define es_omitido(titulo) -> bool:
  titulo_lower = titulo.lower().strip()
  iterate titulos_omitidos: return True if omitido in titulo_lower OR titulo_lower in omitido
  return False

STEP 5: Add 'es_omitido' boolean column to df_papers

STEP 6: df_no_citados = df_papers[df_papers['es_omitido'] == True]

STEP 7: If df_no_citados is not empty:
  st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")
  st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")
  Build tabla_recomendaciones list (one dict per row):
    For each row in df_no_citados:
      Fuzzy-match against papers_omitidos by title
      Get justificacion, relevancia, subtema_relacionado from matched entry
      Compute es_posterior:
        "✅ Sí" if año_paper_estudiado AND paper['year'] > año_paper_estudiado
        "❌ No" if año_paper_estudiado AND NOT (paper['year'] > año_paper_estudiado)
        "?"    if not año_paper_estudiado
      Append dict: {
        "Título", "Autores", "Año", "Posterior", "Citas",
        "Relevancia", "Subtema", "Justificación"
      }
  Convert to DataFrame, render with st.dataframe with column configs:
    "Título":     TextColumn, width="large"
    "Autores":    TextColumn, width="medium"
    "Año":        NumberColumn, width="small"
    "Posterior":  TextColumn "Posterior al tuyo", width="small"
    "Citas":      NumberColumn, width="small"
    "Relevancia": TextColumn, width="small"
    "Subtema":    TextColumn, width="medium"
    "Justificación": TextColumn, width="large"
  If año_paper_estudiado:
    st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")
  Else:
    st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")

STEP 8: If df_no_citados is empty:
  st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")
```

**Async/spinner patterns:** Synchronous `st.spinner` context manager used; no async patterns. (Source: sota_section.py:11)

---

## 8. Chatbot UI Flow (`render_chatbot`)

**File:** `frontend/components/chatbot.py` (29 lines)  
**Function signature:** `render_chatbot(md_text: str) -> None`  
(Source: extracted_frontend_01.md §5.3 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_007, chatbot.py:4)

---

### 8.1 Message History Display

```
TRIGGER: Function entry (unconditional).
ACTION:
  st.markdown("---")
  st.header("💬 Pregunta al Revisor")
  st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")
  Reads: st.session_state.messages  (list of {"role": str, "content": str} dicts)
  For each message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
FORMAT: Role-based rendering using Streamlit's st.chat_message context manager;
        content rendered as Markdown.
                                                    SOURCE: chatbot.py:4-12
```

---

### 8.2 User Input and Submit Action

```
WIDGET: st.text_input(
    "Escribe tu pregunta:",
    key="chat_input",
    placeholder="Ej: ¿En qué página falla el paper en su estadística?"
)
                                                    SOURCE: chatbot.py:14-18

SUBMIT BUTTON: st.button("Enviar", key="send_button")
                                                    SOURCE: chatbot.py:20

TRIGGER: st.button("Enviar") returns True AND prompt_usuario (text_input value) is non-empty
CONDITION (ChatSubmitGuard): BOTH conditions must be True; silent ignore if prompt_usuario is empty.
                                                    SOURCE: chatbot.py:20-29

ACTION on submit:
  1. Append {"role": "user", "content": prompt_usuario} to st.session_state.messages
                                                    SOURCE: chatbot.py:21
  2. Build history_str:
       history_str = "\n".join([
           f"{m['role']}: {m['content']}"
           for m in st.session_state.messages[-4:]
       ])
                                                    SOURCE: chatbot.py:23
  3. st.spinner("El revisor está analizando tu consulta...")
  4. Backend call:
       respuesta_ia = st.session_state.chatbot.preguntar(
           md_text,
           prompt_usuario,
           history_str
       )
       — CROSS-REFERENCE: preguntar() is in backend/services/chatbot.py
                                                    SOURCE: chatbot.py:26
  5. Append {"role": "assistant", "content": respuesta_ia} to st.session_state.messages
                                                    SOURCE: chatbot.py:28
```

---

### 8.3 Rerun

```
CONDITION: After assistant response has been appended to st.session_state.messages
ACTION: st.rerun()
PURPOSE: Forces Streamlit to re-render the conversation display with the new user and
         assistant messages visible. Without rerun, the newly appended messages would
         not appear until the next user interaction.
                                                    SOURCE: chatbot.py:29
```

---

## 9. Gauge Chart (`create_gauge_chart` — NeurIPS Quality Tiers)

**File:** `frontend/components/gauge_chart.py` (71 lines)  
(Source: extracted_frontend_01.md §5.4 / §2.4, gauge_chart.py:4)

---

**Function signature:** `create_gauge_chart(score: float) -> plotly.graph_objects.Figure`

**Parameters:**
- `score: float` — quality score in range [0, 100]

**Return value:** `plotly.graph_objects.Figure` — a Plotly gauge indicator figure.

**Chart library:** Plotly (`plotly.graph_objects.go`).

---

### NeurIPS Quality Tier Definitions

| Score Range | Label | Bar Color (hex) | Source |
|-------------|-------|----------------|--------|
| [87.5, 100] | `"Strong Accept"` | `"#00aa00"` (dark green) | gauge_chart.py:14-31 |
| [75, 87.5)  | `"Accept"` | `"#00cc44"` (green) | gauge_chart.py:14-31 |
| [62.5, 75)  | `"Borderline"` | `"#ffcc00"` (yellow) | gauge_chart.py:14-31 |
| [50, 62.5)  | `"Weak Reject"` | `"#ff9900"` (orange) | gauge_chart.py:14-31 |
| [25, 50)    | `"Reject"` | `"#ff4b4b"` (red) | gauge_chart.py:14-31 |
| [0, 25)     | `"Strong Reject"` | `"#cc0000"` (dark red) | gauge_chart.py:14-31 |

Threshold line: value=62.5, color="red", width=4 (marks the Borderline boundary). (Source: gauge_chart.py:57-61)

---

### Chart Configuration Options

```python
go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': f"Quality Score<br><sub>{label}</sub>", 'font': {'size': 18}},
    number={'suffix': "%", 'font': {'size': 40}},
    gauge={
        'axis': {'range': [0, 100], 'tickmode': 'linear', 'tick0': 0, 'dtick': 25},
        'bar':  {'color': color_barra, 'thickness': 0.8, 'line': {'color': 'black', 'width': 2}},
        'bgcolor':     'white',
        'borderwidth': 2,
        'bordercolor': 'black',
        'steps': [coloured background steps matching the 6 tiers],
        'threshold': {'line': {'color': 'red', 'width': 4}, 'value': 62.5}
    }
))

layout: height=300, margins l=10/r=10/t=50/b=25, paper_bgcolor=transparent, font color="#E5E7EB"
```

(Source: gauge_chart.py:33-71)

---

### Render Site

[GAP: call site for create_gauge_chart(score) not found within the 14 files of the frontend cluster. The function is defined in gauge_chart.py and exported; its caller is expected to pass a float score (0–100) and render the returned Figure via `st.plotly_chart()`. Likely location: audit_results.py or a page/component not included in this extraction cluster. Impact: LOW — function logic is fully documented; only the caller is missing. Source: GAP-ext_frontend_01-001]

---

## 10. Custom CSS & Styling (`apply_custom_styles`)

**File:** `frontend/styles/custom_css.py` (87 lines)  
(Source: extracted_frontend_01.md §6 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_026)

**Function signature:** `apply_custom_styles() -> None`

**Mechanism:** Calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)` where `CUSTOM_CSS` is a module-level constant defined at `custom_css.py:4-83`. (Source: custom_css.py:85-86)

**CSS scope — complete selector table:**

| Selector | Properties applied | Purpose |
|----------|--------------------|---------|
| `.stApp` | `background-color: #374151 !important` | Dark grey app background |
| `#MainMenu` | `visibility: hidden` | Hides Streamlit hamburger menu |
| `footer` | `visibility: hidden` | Hides Streamlit footer |
| `header` | `background-color: transparent !important` | Transparent header |
| `[data-testid="stTable"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 5px !important` | Table container dark bg with rounded corners |
| `[data-testid="stTable"] table` | `border-collapse: collapse !important; width: 100% !important; border: none !important` | Eliminates duplicate border lines |
| `[data-testid="stTable"] th` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; background-color: #3d4446 !important; border: 1px solid #4a4a4a !important; padding: 12px !important; text-transform: capitalize !important` | Header cells: white bold text |
| `[data-testid="stTable"] th *` | `color: #FFFFFF !important; font-size: 16px !important; font-weight: 800 !important; text-decoration: none !important; border: none !important; text-transform: capitalize !important` | All children of header cells |
| `[data-testid="stTable"] tbody th` | `color: #FFFFFF !important; font-size: 16px !important; background-color: #2d3436 !important` | Body row header cells |
| `[data-testid="stTable"] tbody th *` | `color: #FFFFFF !important; font-size: 16px !important; background-color: transparent !important` | Children of body row headers |
| `[data-testid="stTable"] td` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; background-color: transparent !important; border: 1px solid #4a4a4a !important; padding: 12px !important` | Table data cells |
| `[data-testid="stTable"] td *` | `color: #E2E8F0 !important; font-size: 13.5px !important; font-weight: 400 !important; text-decoration: none !important; border: none !important` | Children of data cells |
| `[data-testid="stPlotlyChart"]` | `background-color: #2d3436 !important; border-radius: 15px !important; padding: 10px !important` | Plotly chart container |

(Source: custom_css.py:4-83)

---

## 11. Application-Level Constants

(Source: extracted_frontend_01.md §2.1 / cross_ref_resolution_cross_ref_root_to_frontend.md §g_008, config.py:3-5)

| Constant | Value | Type | Usage |
|----------|-------|------|-------|
| `TITLE` | `"💻 Auditor de Papers en Ciencias de la Computación"` | `str` | `st.title(TITLE)` in `app.py:25`; page heading |
| `SIDEBAR_IMAGE` | `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"` | `str` | `st.image(SIDEBAR_IMAGE, width=150)` in sidebar |
| `SIDEBAR_DESCRIPTION` | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` | `str` | `st.write(SIDEBAR_DESCRIPTION)` in sidebar |

---

## 12. Cross-References and GAPs

The following are all cross-references and gaps identified in the extraction data that are relevant to rebuilding the frontend:

| GAP_ID | Type | From | Expects | Impact | Source |
|--------|------|------|---------|--------|--------|
| GAP-ext_frontend_01-001 | CROSS_REFERENCE | `gauge_chart.py:4` — `create_gauge_chart(score)` | Caller passing numeric score (0-100) and rendering Figure via `st.plotly_chart()` | LOW | gauge_chart.py:4 |
| GAP-ext_frontend_01-002 | CROSS_REFERENCE | `file_uploader.py:36` — `convert_pdf_to_markdown(temp_path)` | `function(path: str) -> str` converting PDF to Markdown; likely in `backend/services/pdf_parser.py` | HIGH | file_uploader.py:4-5 |
| GAP-ext_frontend_01-003 | CROSS_REFERENCE | `session_state.py:13` — `PaperAuditor()` | Class with `audit(md_text: str, status_callback: callable) -> dict`; expected keys include all 16 CHECKLIST_KEYS plus optional: "error", "evaluation_error", "metricas", "informacion_extraida", "general_analysis_map", "original_extraction_raw", "hybrid_triage_fragments", "extracted_hyperparameters_hybrid", "evaluation_signals" | HIGH | session_state.py:3 |
| GAP-ext_frontend_01-004 | CROSS_REFERENCE | `session_state.py:16` — `PaperChatbot()` | Class with `preguntar(md_text: str, question: str, history_str: str) -> str` | MEDIUM | session_state.py:4 |
| GAP-ext_frontend_01-005 | CROSS_REFERENCE | `session_state.py:19` — `SotaAnalyzer()` | Class with `analyze_sota(md_text: str) -> dict`; keys: "conclusion_sota", "papers_omitidos" (list), "papers_analizados" (list of dicts with 'titulo', 'año', 'citas', 'autores'), "metadata" (dict with 'año_paper_estudiado'), optionally "error" | MEDIUM | session_state.py:5 |
| GAP-ext_frontend_01-006 | CONFIG_DEPENDENCY | `file_uploader.py:23` — `os.makedirs("temp")` | Filesystem write permission in working directory to create `temp/` subdirectory | HIGH | file_uploader.py:23-24 |
| GAP-ext_frontend_01-007 | EXTERNAL_SYSTEM | `sota_section.py:12` — `sota_analyzer.analyze_sota()` | Connectivity to Semantic Scholar API (mentioned in spinner text) | MEDIUM | sota_section.py:11 |
| GAP-ext_frontend_01-008 | MISSING_SOURCE | `audit_results.py:241` — `st.caption("Fusión de datos técnicos con Gemma 4 31B.")` | Knowledge of which LLM model is used in RAG REDUCE phase | LOW | audit_results.py:241 |
