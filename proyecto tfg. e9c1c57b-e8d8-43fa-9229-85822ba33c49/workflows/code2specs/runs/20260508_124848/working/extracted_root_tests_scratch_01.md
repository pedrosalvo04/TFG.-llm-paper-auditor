## REFORMAT LOG
Agent: reformat_root_loc_g001
Gap addressed: g_001
Action: Corrected LOC column in §1 File Index table using inventory.json as source of truth.

Changes applied:
| File | Old LOC | New LOC | Source |
|---|---|---|---|
| `.gitignore` | 42 | 34 | inventory.json |
| `app.py` | 89 | 74 | inventory.json |
| `create_test_pdf.py` | 184 | 160 | inventory.json |
| `list_models.py` | 18 | 15 | inventory.json |
| `md_to_pdf.py` | 325 | 264 | inventory.json |
| `pdf_to_md.py` | 159 | 125 | inventory.json |
| `test_auditor_refactor.py` | 101 | 84 | inventory.json |
| `test_imports.py` | 47 | 38 | inventory.json |
| `test_skills_integration.py` | 164 | 148 | inventory.json |
| `backend/scratch/test_embed.py` | 26 | 22 | inventory.json |
| `backend/scratch/test_embed2.py` | 23 | 19 | inventory.json |
| `scratch/check_st.py` | 7 | 6 | inventory.json |
| `scratch/patch_skills.py` | 109 | 84 | inventory.json |
| `scratch/repro_hyperparams.py` | 33 | 23 | inventory.json |
| `scratch/test_checklist_health.py` | 37 | 34 | inventory.json |
| `scratch/test_llm_retry.py` | 64 | 50 | inventory.json |
| `scratch/test_rag_split.py` | 48 | 35 | inventory.json |
| `tests/test_audit_state.py` | 27 | 23 | inventory.json |
| `tests/test_rag_logical_splitter.py` | 44 | 32 | inventory.json |
| `tests/test_section_splitter.py` | 84 | 68 | inventory.json |

Files unchanged (LOC already matched inventory.json):
- `requirements.txt`

Files in §1 table but absent from inventory.json (LOC not changed):
- None

Discovered-during-reformat items needing follow-up (do NOT act on these):
- None

---

## FIX LOG
<!-- Agent: targeted_fix_root_deps_g002_g003 | Run: targeted_fix -->

| gap_id | original gap detail | source consulted (file:line) | what was added / corrected |
|--------|--------------------|-----------------------------|---------------------------|
| g_002  | reportlab imported in md_to_pdf.py:7–13 and create_test_pdf.py throughout but absent from requirements.txt; extraction §2 did not flag it as a missing dependency | md_to_pdf.py:8–13, create_test_pdf.py:2–6 (all reportlab lines), requirements.txt:1–5 | Added missing-dependency annotation (GAP-025) to §2 requirements.txt table identifying reportlab as an undeclared hard dependency required by both md_to_pdf.py (6 sub-package imports at lines 8–13) and create_test_pdf.py (5 sub-package imports at lines 2–6); noted that any environment built from requirements.txt alone cannot run either utility (ModuleNotFoundError at module-load time) |
| g_003  | markdown2 attempted in md_to_pdf.py:15-17 is absent from requirements.txt; §10.5 documented the ImportError handler but did not state markdown2 was unlisted, leaving reader ambiguity | md_to_pdf.py:15–19, requirements.txt:1–5 (absence confirmed) | Added missing-dependency annotation (GAP-026) to §2 noting markdown2 as an optional unlisted dependency; augmented §10.5 RECOVERY block to explicitly state markdown2 is absent from requirements.txt so the ImportError branch is the default execution path in any requirements.txt-only environment, and clarified that HAS_MARKDOWN=False means the markdown-conversion feature is silently unavailable (flag is set but never read downstream — no code path gated on it) |

---

# Extraction Report: cluster_root_tests_scratch_01
## Agent: ext_root_tests_scratch_01

---

## 1. File Index

| # | File | Lines | Purpose |
|---|------|-------|---------|
| 1 | `.gitignore` | 34 | Git ignore rules: excludes pycache, venvs, IDEs, `.env`, PDFs, logs, `*.md`, `*.txt` |
| 2 | `app.py` | 74 | Main Streamlit application entry point: configures page, handles file upload, renders audit results |
| 3 | `create_test_pdf.py` | 160 | CLI script to generate a test PDF paper with known errors using reportlab |
| 4 | `list_models.py` | 15 | CLI script to list available Google GenAI embedding models via API |
| 5 | `md_to_pdf.py` | 264 | CLI tool to convert Markdown/TXT files or folders to PDF using reportlab |
| 6 | `pdf_to_md.py` | 125 | CLI tool to convert PDF files or folders to Markdown using pymupdf4llm |
| 7 | `requirements.txt` | 5 | Python dependency list (no pinned versions) |
| 8 | `test_auditor_refactor.py` | 84 | Integration smoke-test verifying auditor refactoring correctness |
| 9 | `test_imports.py` | 38 | Import smoke-test verifying all frontend modules are importable |
| 10 | `test_skills_integration.py` | 148 | Integration test verifying skills architecture and service initialization |
| 11 | `backend/scratch/test_embed.py` | 22 | Scratch script testing Google GenAI `embed_content` API response structure |
| 12 | `backend/scratch/test_embed2.py` | 19 | Scratch script testing Google GenAI `embed_content` API with error handling |
| 13 | `scratch/check_st.py` | 6 | Scratch script checking for `st.html` and `st.iframe` Streamlit attribute existence |
| 14 | `scratch/patch_skills.py` | 84 | One-time script that rewrites `CrowdsourcingDetectionSkill` and `LicenseDetectionSkill` classes in `backend/skills/regex_detection_skills.py` via AST-validated string replacement |
| 15 | `scratch/repro_hyperparams.py` | 23 | Scratch script reproducing hyperparameter detection on a real paper file |
| 16 | `scratch/test_checklist_health.py` | 34 | Scratch script testing `get_checklist_health()` with a mock evaluation dict |
| 17 | `scratch/test_llm_retry.py` | 50 | Unit test for `LLMClient` retry logic (mock-based, no real LLM) |
| 18 | `scratch/test_rag_split.py` | 35 | Scratch script defining and testing a naive `get_rag_chunks()` split function |
| 19 | `tests/test_audit_state.py` | 23 | Unit test for `AuditState`, `ExtractedInfo`, and `ChecklistItem` datamodels |
| 20 | `tests/test_rag_logical_splitter.py` | 32 | Integration test for RAG logical block splitting strategy |
| 21 | `tests/test_section_splitter.py` | 68 | Integration test for `InformationExtractionSkill` section-fragmenting logic |

---

## 2. Dependencies & Configuration (requirements.txt)

No version pins are present in `requirements.txt`. All packages are installed at latest available version.

| Package | Role in Application |
|---------|---------------------|
| `docling` | Local (free) PDF-to-Markdown conversion for file ingestion in the backend |
| `google-generativeai` | Google Gemini 1.5 Flash API client for LLM calls (extraction, evaluation) and embedding API |
| `python-dotenv` | Loads `GOOGLE_API_KEY` and other secrets from `.env` file |
| `streamlit` | Web UI framework for the main application (`app.py`) |
| `pydantic` | Structured/validated LLM response parsing |

`SOURCE: requirements.txt:1-5`

**Missing dependencies not listed in `requirements.txt`:**

```
GAP_ID: GAP-cluster_root_tests_scratch_01-025
TYPE: MISSING_DEPENDENCY
FROM: md_to_pdf.py:8–13 (all PDF generation logic), create_test_pdf.py:2–6 (all PDF generation logic)
DETAIL: reportlab is a hard dependency imported unconditionally in both utilities but is absent from requirements.txt.
  md_to_pdf.py lines 8–13 imports:
    reportlab.lib.pagesizes  → letter, A4
    reportlab.lib.styles     → getSampleStyleSheet, ParagraphStyle
    reportlab.lib.units      → inch
    reportlab.platypus       → SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
    reportlab.lib            → colors
    reportlab.lib.enums      → TA_CENTER, TA_LEFT, TA_JUSTIFY
  create_test_pdf.py lines 2–6 imports:
    reportlab.lib.pagesizes  → letter
    reportlab.lib.styles     → getSampleStyleSheet, ParagraphStyle
    reportlab.lib.units      → inch
    reportlab.platypus       → SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    reportlab.lib            → colors
IMPACT: HIGH — any environment installed strictly from requirements.txt (pip install -r requirements.txt) fails
  at module-load time with ModuleNotFoundError when either md_to_pdf.py or create_test_pdf.py is executed;
  all PDF generation functionality is unavailable without reportlab
SOURCE: md_to_pdf.py:8–13, create_test_pdf.py:2–6, requirements.txt:1–5 (absence confirmed)
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-026
TYPE: MISSING_DEPENDENCY
FROM: md_to_pdf.py:15–17 — try: import markdown2 / HAS_MARKDOWN = True
DETAIL: markdown2 is attempted via `try: import markdown2` at md_to_pdf.py:15. It is not listed in
  requirements.txt. The except ImportError branch (md_to_pdf.py:18–21) sets HAS_MARKDOWN = False and
  prints: "⚠️ Advertencia: markdown2 no instalado. Solo se soportará conversión básica." /
  "   Instala con: pip install markdown2". The package is characterised as optional: runtime does not
  crash. However, HAS_MARKDOWN is never used to gate any code path in the file — the built-in
  line-by-line parser (parse_markdown_to_elements, md_to_pdf.py:23–101) runs unconditionally
  regardless of markdown2 availability.
IMPACT: LOW — runtime does not crash; markdown2-enhanced conversion path is not implemented in this
  file; markdown2 is an undeclared optional dependency whose absence is the default state in any
  requirements.txt-only environment
SOURCE: md_to_pdf.py:15–17, requirements.txt:1–5 (absence confirmed)
```

---

## 3. Application Entry Point (app.py)

### 3.1 Environment Configuration (executed at module load)

The following environment variables are set unconditionally before any import of transformers/chromadb:

| Variable | Value Set | Purpose |
|----------|-----------|---------|
| `TRANSFORMERS_VERBOSITY` | `"error"` | Suppresses transformers library logs |
| `TOKENIZERS_PARALLELISM` | `"false"` | Suppresses tokenizer parallelism warnings |
| `ANONYMIZED_TELEMETRY` | `"False"` | Disables ChromaDB telemetry |
| `OTEL_SDK_DISABLED` | `"true"` | Disables OpenTelemetry SDK (avoids Streamlit conflicts) |

`SOURCE: app.py:13-14` (TRANSFORMERS_VERBOSITY, TOKENIZERS_PARALLELISM)
`SOURCE: app.py:21-22` (ANONYMIZED_TELEMETRY, OTEL_SDK_DISABLED)

Additionally three `warnings.filterwarnings("ignore", ...)` calls suppress:
- `message=".*Accessing.*__path__.*"` — SOURCE: app.py:15
- `category=FutureWarning` — SOURCE: app.py:16
- `category=UserWarning` — SOURCE: app.py:17

`logging.getLogger("transformers").setLevel(logging.ERROR)` — SOURCE: app.py:18

### 3.2 Streamlit Page Configuration

Called as FIRST Streamlit operation (mandatory):

```
st.set_page_config(
    page_title="Nature Auditor Pro",
    layout="wide",
    page_icon="🔬"
)
```
`SOURCE: app.py:25-29`

### 3.3 Imports (frontend modules)

| Symbol | Module |
|--------|--------|
| `TITLE`, `SIDEBAR_IMAGE`, `SIDEBAR_DESCRIPTION` | `frontend.config` |
| `apply_custom_styles` | `frontend.styles.custom_css` |
| `initialize_session_state` | `frontend.utils.session_state` |
| `process_uploaded_file` | `frontend.components.file_uploader` |
| `render_audit_results`, `generate_report` | `frontend.components.audit_results` |
| `render_sota_analysis` | `frontend.components.sota_section` |
| `render_chatbot` | `frontend.components.chatbot` |

`SOURCE: app.py:31-37`

### 3.4 Initialization Sequence

1. `apply_custom_styles()` — applies CSS — SOURCE: app.py:40
2. `initialize_session_state()` — initializes Streamlit session state — SOURCE: app.py:41
3. `st.title(TITLE)` — renders page title — SOURCE: app.py:44
4. File uploader widget rendered accepting `["pdf", "txt", "md"]` — SOURCE: app.py:48-51

### 3.5 File Upload & Audit Flow (main conditional block)

`SOURCE: app.py:53-88`

**Trigger:** `uploaded_file` is not None (user uploaded a file)

**Step 1:** `process_uploaded_file(uploaded_file)` — delegates file processing to frontend component — SOURCE: app.py:54

**Step 2:** Read from `st.session_state`:
- `resultado = st.session_state.get('resultado')` — SOURCE: app.py:57
- `md_text = st.session_state.get('md_text')` — SOURCE: app.py:58

**Step 3 — Branch on `resultado`:**

| Condition | Action |
|-----------|--------|
| `resultado` is not None AND `"error" in resultado` | `st.error(f"❌ Error en la auditoría: {resultado['error']}")` |
| `resultado` is not None AND `"evaluation_error" in resultado` | `st.error(f"❌ Error del LLM: {resultado['evaluation_error']}")` AND `st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")` |
| `resultado` is not None AND `resultado.get("claims")` is truthy | Call `render_audit_results`, `render_sota_analysis`, `render_chatbot`, offer download button |
| `resultado` is not None but none of above | `st.error("⚠️ La auditoría no generó resultados válidos.")` AND `st.json(resultado)` |

`SOURCE: app.py:60-82`

**Step 4 — Report download (only when claims present):**
- `puntuacion = render_audit_results(resultado, uploaded_file)` — SOURCE: app.py:66
- `render_sota_analysis(md_text)` — SOURCE: app.py:67
- `render_chatbot(md_text)` — SOURCE: app.py:68
- `reporte = generate_report(resultado, uploaded_file, puntuacion)` — SOURCE: app.py:73
- `st.download_button(label="📥 Descargar Informe Completo (.md)", data=reporte, file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md", mime="text/markdown")` — SOURCE: app.py:74-79

**Step 5 — Sidebar:**
- `st.image(SIDEBAR_IMAGE, width=150)` — SOURCE: app.py:86
- `st.markdown("### Sobre el TFG")` and `st.write(SIDEBAR_DESCRIPTION)` — SOURCE: app.py:87-88

---

## 4. PDF Utility Scripts

### 4.1 md_to_pdf.py

**Purpose:** Convert Markdown or TXT files (single file or folder) to PDF.

#### Function: `parse_markdown_to_elements(md_text, styles)`
`SOURCE: md_to_pdf.py:23`

**Parameters:**
- `md_text` (str): Markdown text to convert
- `styles`: reportlab `getSampleStyleSheet()` dict

**Returns:** List of reportlab flowable elements (Paragraph, Spacer, Preformatted)

**Logic — iterates lines of `md_text.split('\n')` with index `i`:**

| Line pattern | Action |
|-------------|--------|
| Empty string after `.strip()` | Append `Spacer(1, 0.1*inch)`, increment `i` |
| Starts with `'# '` AND NOT `'## '` | Extract `line[2:].strip()`, append `Paragraph(text, styles['Heading1'])` + `Spacer(1, 0.2*inch)` |
| Starts with `'## '` AND NOT `'### '` | Extract `line[3:].strip()`, append `Paragraph(text, styles['Heading2'])` + `Spacer(1, 0.15*inch)` |
| Starts with `'### '` | Extract `line[4:].strip()`, append `Paragraph(text, styles['Heading3'])` + `Spacer(1, 0.1*inch)` |
| Starts with `'- '` OR `'* '` | Prepend `'• '` to `line[2:].strip()`, append `Paragraph(text, styles['Normal'])` |
| `len(line) > 2` AND `line[0].isdigit()` AND `line[1:3] in ['. ', ') ']` | Append `Paragraph(line, styles['Normal'])` (numbered list item) |
| Starts with ` ``` ` | Collect all lines until next ` ``` `, join with `'\n'`, append `Preformatted(code_text, styles['Code'])` + `Spacer(1, 0.1*inch)` |
| Starts with `'---'` OR `'==='` | Append `Spacer(1, 0.1*inch)` + `Paragraph('<hr/>', styles['Normal'])` + `Spacer(1, 0.1*inch)` |
| All other lines | Replace `'**'` pairs with `<b>`/`</b>` and `'*'` pairs with `<i>`/`</i>` (NOTE: naive sequential replacement — both replacements use the same token, resulting in all `**` becoming `<b>` first then any remaining `*` becoming `<i>`), append `Paragraph(text, styles['Normal'])` |

`SOURCE: md_to_pdf.py:38-99`

#### Function: `convert_to_pdf(input_path, output_path=None, page_size='letter')`
`SOURCE: md_to_pdf.py:103`

**Parameters:**
- `input_path` (str): Path to `.md`, `.txt`, or `.markdown` file
- `output_path` (str, optional): Output PDF path; default: same directory, `.pdf` extension
- `page_size` (str): `'letter'` (default) or `'a4'`

**Validation rules (abort and return `None` if violated):**
1. `os.path.exists(input_path)` is False → print error, return `None` — SOURCE: md_to_pdf.py:116-118
2. `ext not in ['md', 'txt', 'markdown']` (where `ext = input_path.lower().split('.')[-1]`) → print error, return `None` — SOURCE: md_to_pdf.py:121-123

**Processing steps:**
1. If `output_path is None`: `output_path = input_path.rsplit('.', 1)[0] + '.pdf'` — SOURCE: md_to_pdf.py:127-128
2. Read file: `open(input_path, 'r', encoding='utf-8').read()` — SOURCE: md_to_pdf.py:135-136
3. Select page size: `A4 if page_size.lower() == 'a4' else letter` — SOURCE: md_to_pdf.py:139
4. Create `SimpleDocTemplate(output_path, pagesize=pagesize, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)` — SOURCE: md_to_pdf.py:142-149
5. Build styles with custom `'Code'` style (font: `Courier`, size: `9`, leftIndent: `20`, rightIndent: `20`, textColor: `#2d2d2d`, backColor: `#f5f5f5`, borderPadding: `5`) — SOURCE: md_to_pdf.py:154-165
6. Override `Normal`: fontSize=11, leading=14, alignment=TA_JUSTIFY — SOURCE: md_to_pdf.py:168-170
7. Override `Heading1`: fontSize=18, textColor=#1a1a1a, spaceAfter=12 — SOURCE: md_to_pdf.py:172-174
8. Override `Heading2`: fontSize=14, textColor=#2d2d2d, spaceAfter=10 — SOURCE: md_to_pdf.py:176-178
9. Override `Heading3`: fontSize=12, textColor=#404040, spaceAfter=8 — SOURCE: md_to_pdf.py:180-182
10. Call `parse_markdown_to_elements(content, styles)` — SOURCE: md_to_pdf.py:185
11. Call `doc.build(elements)` — SOURCE: md_to_pdf.py:188
12. Print stats: file size (`os.path.getsize(output_path)`), estimated page count (`len(elements) // 30`), format — SOURCE: md_to_pdf.py:191-199
13. Return `output_path` — SOURCE: md_to_pdf.py:201

**Error handling:** Catch-all `except Exception as e`: print error message + `traceback.print_exc()`, return `None` — SOURCE: md_to_pdf.py:203-207

#### Function: `convert_folder(folder_path, output_folder=None, page_size='letter')`
`SOURCE: md_to_pdf.py:209`

**Logic:**
1. Validate `os.path.exists(folder_path)` else print error and return — SOURCE: md_to_pdf.py:218-220
2. Glob `*.md` and `*.txt` from `folder_path`, concatenate lists — SOURCE: md_to_pdf.py:223-225
3. If empty, print warning and return — SOURCE: md_to_pdf.py:227-229
4. If `output_folder` specified: `os.makedirs(output_folder, exist_ok=True)` — SOURCE: md_to_pdf.py:235-236
5. Iterate: for each file, build output_path as `os.path.join(output_folder, file.stem + '.pdf')` if output_folder else `None`, call `convert_to_pdf(str(file), output_path, page_size)` — SOURCE: md_to_pdf.py:242-254
6. Track `successful` and `failed` counts, print summary — SOURCE: md_to_pdf.py:239-262

#### Function: `main()` — CLI entry point
`SOURCE: md_to_pdf.py:264`

**CLI arguments (parsed from `sys.argv` manually):**

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `sys.argv[1]` | str | Yes (or print usage) | First positional: file path OR `'--folder'` |
| `sys.argv[2]` | str | Conditional | Output path (file mode) or folder path (folder mode) |
| `--size <value>` | str | No | Page size: `'letter'` (default) or `'a4'` |
| `--folder <path>` | str | Conditional | Source folder (activates folder mode) |
| `--output <path>` | str | No | Output folder (folder mode only) |

**Branching:**
- If `len(sys.argv) < 2`: print usage/examples and return — SOURCE: md_to_pdf.py:270-287
- If `'--size' in sys.argv`: extract `page_size = sys.argv[size_idx + 1]` — SOURCE: md_to_pdf.py:291-294
- If `sys.argv[1] == '--folder'`: folder mode — extract `folder_path`, optionally `output_folder`, call `convert_folder(folder_path, output_folder, page_size)` — SOURCE: md_to_pdf.py:297-310
- Else: single file mode — `input_path = sys.argv[1]`, `output_path = sys.argv[2] if len(sys.argv) >= 3 and not sys.argv[2].startswith('--') else None`, call `convert_to_pdf(input_path, output_path, page_size)` — SOURCE: md_to_pdf.py:313-321

### 4.2 pdf_to_md.py

**Purpose:** Convert PDF files (single file or folder) to Markdown using `pymupdf4llm`.

#### Function: `convert_pdf_to_md(pdf_path, output_path=None)`
`SOURCE: pdf_to_md.py:10`

**Parameters:**
- `pdf_path` (str): Path to PDF file
- `output_path` (str, optional): Output Markdown path; default: same path with `.md` extension

**Validation rules (abort and return `None` if violated):**
1. `not os.path.exists(pdf_path)` → print error, return `None` — SOURCE: pdf_to_md.py:23-25
2. `not pdf_path.lower().endswith('.pdf')` → print error, return `None` — SOURCE: pdf_to_md.py:28-30

**Processing steps:**
1. If `output_path is None`: `output_path = pdf_path.replace('.pdf', '.md')` — SOURCE: pdf_to_md.py:33-34
2. Call `pymupdf4llm.to_markdown(pdf_path)` → assigns to `md_text` — SOURCE: pdf_to_md.py:41
3. Write `md_text` to `output_path` with `open(output_path, 'w', encoding='utf-8')` — SOURCE: pdf_to_md.py:44-45
4. Print stats: `os.path.getsize(output_path)` bytes, `len(md_text)` characters, `md_text.count('\n')` lines — SOURCE: pdf_to_md.py:48-57
5. Return `output_path` — SOURCE: pdf_to_md.py:59

**Error handling:** Catch-all `except Exception as e`: print `"❌ Error durante la conversión: {str(e)}"`, return `None` — SOURCE: pdf_to_md.py:61-63

#### Function: `convert_folder(folder_path, output_folder=None)`
`SOURCE: pdf_to_md.py:65`

**Logic:**
1. Validate `os.path.exists(folder_path)` else print error and return — SOURCE: pdf_to_md.py:73-75
2. Glob `*.pdf` from `folder_path` — SOURCE: pdf_to_md.py:78
3. If empty, print warning and return — SOURCE: pdf_to_md.py:80-81
4. If `output_folder` specified: `os.makedirs(output_folder, exist_ok=True)` — SOURCE: pdf_to_md.py:88-89
5. Iterate PDFs: build output_path as `os.path.join(output_folder, pdf_file.stem + '.md')` if output_folder else `None`, call `convert_pdf_to_md(str(pdf_file), output_path)` — SOURCE: pdf_to_md.py:95-107
6. Track `successful` and `failed`, print summary — SOURCE: pdf_to_md.py:91-115

#### Function: `main()` — CLI entry point
`SOURCE: pdf_to_md.py:117`

**CLI arguments:**

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `sys.argv[1]` | str | Yes (or print usage) | PDF path OR `'--folder'` |
| `sys.argv[2]` | str | Conditional | Output `.md` path (file mode) or folder path (folder mode) |
| `--folder <path>` | str | Conditional | Source folder (activates folder mode) |
| `--output <path>` | str | No | Output folder (folder mode only; detected at `sys.argv[3] == '--output'`, value at `sys.argv[4]`) |

**Branching:**
- If `len(sys.argv) < 2`: print usage/examples and return — SOURCE: pdf_to_md.py:123-134
- If `sys.argv[1] == '--folder'`: folder mode — SOURCE: pdf_to_md.py:137-148
- Else: single file mode — `pdf_path = sys.argv[1]`, `output_path = sys.argv[2] if len(sys.argv) >= 3 else None`, call `convert_pdf_to_md(pdf_path, output_path)` — SOURCE: pdf_to_md.py:151-155

### 4.3 create_test_pdf.py

**Purpose:** Generates the file `paper_test_con_errores.pdf` — a synthetic scientific paper with intentionally vague/low-quality content for testing the auditor.

#### Function: `create_test_paper_pdf()`
`SOURCE: create_test_pdf.py:8`

**Parameters:** None. **Returns:** None. **Side effect:** Creates `paper_test_con_errores.pdf` in the current working directory.

**Document structure written via reportlab:**

| Section | Content |
|---------|---------|
| Title | "Deep Learning for Image Classification: A Novel Approach" |
| Authors | "John Doe, Jane Smith" |
| Affiliation | "University of Example" |
| Year | "2024" |
| Abstract | Vague claims: "outperforms previous approaches by a significant margin", "promising results on standard benchmarks" |
| 1. Introduction | Generic text about deep learning |
| 2. Related Work | References CNNs and ResNets without specifics |
| 3.1 Model Architecture | "convolutional layers followed by fully connected layers", "dropout for regularization" — no hyperparameter values |
| 3.2 Training | "trained on a dataset", "using a GPU", "an optimizer" — intentionally vague |
| 3.3 Hyperparameters | "We tuned the hyperparameters to get good results" — no values |
| 4.1 Dataset | "popular image dataset" — no name |
| 4.2 Results | Table: [Ours: 95.2%, Baseline: 92.1%] |
| 4.3 Ablation | "all components are important" |
| 5. Implementation | "implemented in Python. We used some libraries" |
| 6. Computational Resources | "some time on our hardware" |
| 7. Data Availability | "publicly available" — no URL |
| 8. Code Availability | "upon request" — no URL/repo |
| 9. Conclusion | "novel approach that works well" |
| References | Three placeholder references |

**Page size:** `letter` (8.5 x 11 in) — SOURCE: create_test_pdf.py:13

**Title style:** CustomTitle, `parent=Heading1`, `fontSize=16`, `textColor=HexColor('#000000')`, `spaceAfter=30`, `alignment=1` (CENTER) — SOURCE: create_test_pdf.py:18-25

**Output file name (hardcoded):** `"paper_test_con_errores.pdf"` — SOURCE: create_test_pdf.py:12

**Table style:** header row background `colors.grey`, header text `colors.whitesmoke`, fontName `Helvetica-Bold`, fontSize 12, data row background `colors.beige`, grid `colors.black` — SOURCE: create_test_pdf.py:112-121

---

## 5. Model Listing CLI (list_models.py)

`SOURCE: list_models.py:1-18`

**Purpose:** Lists all Google GenAI models available for the configured API key.

**Initialization:**
1. `load_dotenv()` — loads `.env` file — SOURCE: list_models.py:5
2. `GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")` — SOURCE: list_models.py:6
3. If `not GOOGLE_API_KEY`: print `"No se encontró GOOGLE_API_KEY"` and `exit()` — SOURCE: list_models.py:8-10
4. `client = genai.Client(api_key=GOOGLE_API_KEY)` — SOURCE: list_models.py:12

**Listing logic:**
```
for m in client.models.list():
    print(f"ID: {m.name} | Display Name: {m.display_name}")
```
`SOURCE: list_models.py:14-16`

**Error handling:** `except Exception as e: print(f"Error listando modelos: {e}")` — SOURCE: list_models.py:17-18

---

## 6. Business Rules (Category 5)

### RULE-01: File type validation in md_to_pdf
```
RULE: md_to_pdf input extension validation
TRIGGER: On call to convert_to_pdf(input_path, ...)
CONDITION: ext (= input_path.lower().split('.')[-1]) NOT IN ['md', 'txt', 'markdown']
ACTION IF TRUE: print error "❌ Error: '<input_path>' no es un archivo MD o TXT"; return None
ACTION IF FALSE: proceed with conversion
ERROR: N/A (function returns None, no exception raised)
FIELDS INVOLVED: input_path (read), ext (derived)
CALLS: No further calls on failure path
SOURCE: md_to_pdf.py:121-124
```

### RULE-02: md_to_pdf page size selection
```
RULE: md_to_pdf page size selection
TRIGGER: On call to convert_to_pdf(input_path, output_path, page_size)
CONDITION: page_size.lower() == 'a4'
ACTION IF TRUE: pagesize = A4
ACTION IF FALSE: pagesize = letter
ERROR: N/A
FIELDS INVOLVED: page_size (read), pagesize (written)
CALLS: No further calls
SOURCE: md_to_pdf.py:139
```

### RULE-03: md_to_pdf output path derivation
```
RULE: Output PDF path default derivation
TRIGGER: On call to convert_to_pdf(..., output_path=None, ...)
CONDITION: output_path IS None
ACTION IF TRUE: output_path = input_path.rsplit('.', 1)[0] + '.pdf'
ACTION IF FALSE: use provided output_path unchanged
ERROR: N/A
FIELDS INVOLVED: output_path, input_path
CALLS: str.rsplit('.', 1) on input_path
SOURCE: md_to_pdf.py:127-128
```

### RULE-04: pdf_to_md file extension validation
```
RULE: pdf_to_md input extension validation
TRIGGER: On call to convert_pdf_to_md(pdf_path, ...)
CONDITION: NOT pdf_path.lower().endswith('.pdf')
ACTION IF TRUE: print "❌ Error: '<pdf_path>' no es un archivo PDF"; return None
ACTION IF FALSE: proceed
ERROR: N/A
FIELDS INVOLVED: pdf_path
CALLS: str.endswith('.pdf')
SOURCE: pdf_to_md.py:28-30
```

### RULE-05: Retry count for LLM client (from test encoding)
```
RULE: LLMClient maximum retry attempts
TRIGGER: On each call to client.generate(prompt) when LLM raises Exception
CONDITION: Exception message matches 503 error; retry count < 5
ACTION IF TRUE: retry (up to 5 additional attempts after original = 6 total calls)
ACTION IF FALSE (count == 5): raise final exception
ERROR: Exception raised with last error message
FIELDS INVOLVED: mock_gen.call_count (must equal 6 on exhaustion), mock_sleep.call_count (must equal 5 on exhaustion)
CALLS: client.client.models.generate_content (mocked), time.sleep (mocked)
SOURCE: scratch/test_llm_retry.py:55
```

### RULE-06: LLM retry — success within retries
```
RULE: LLMClient succeeds after transient failures
TRIGGER: On call to client.generate("test prompt") with 2 prior failures then success
CONDITION: mock_gen raises Exception twice, returns MagicMock(text="Success response") on 3rd call
ACTION IF TRUE: response returned without raising; mock_gen.call_count == 3; mock_sleep.call_count == 2
ACTION IF FALSE: N/A (test fails)
ERROR: N/A (success path)
FIELDS INVOLVED: mock_gen.call_count, mock_sleep.call_count
CALLS: time.sleep (mocked via patch)
SOURCE: scratch/test_llm_retry.py:34-35
```

### RULE-07: Checklist health status determination
```
RULE: Checklist health status is 'risk' when any item has answer='No' without justification
TRIGGER: On call to get_checklist_health(mock_eval)
CONDITION: any checklist item has answer='No' AND is_no_justified=False (i.e., pending_justification=True)
ACTION IF TRUE: health['status'] == 'risk'
ACTION IF FALSE: health['status'] is not 'risk' (exact non-risk value: GAP — not defined in this file)
ERROR: AssertionError if status != 'risk'
FIELDS INVOLVED: evaluation dict key 'experiment_statistical_significance' -> answer='No', is_no_justified=False; health['status']; stats_item['pending_justification']
CALLS: get_checklist_health (CROSS-REFERENCE: frontend/utils/scoring.py)
SOURCE: scratch/test_checklist_health.py:33-36
```

### RULE-08: RAG chunk minimum filtering
```
RULE: RAG chunks must have length > 10 characters to be kept
TRIGGER: On execution of get_rag_chunks equivalent in tests/test_rag_logical_splitter.py
CONDITION: len(c.strip()) > 10
ACTION IF TRUE: include chunk in output list
ACTION IF FALSE: discard chunk
ERROR: N/A
FIELDS INVOLVED: raw_chunks (split by r'\n\n+'), c.strip() length
CALLS: re.split(r'\n\n+', paper_text_norm)
SOURCE: tests/test_rag_logical_splitter.py:29
```

### RULE-09: Section fragment count cap
```
RULE: Section fragmentation produces at most 4 fragments from a multi-section paper
TRIGGER: On call to TestSkill.get_fragments(paper_text) in tests/test_section_splitter.py
CONDITION: len(sections) > 1; accumulate sections into current_fragment until len(current_fragment) + len(section) > (total_chars / 4) AND len(fragments) < 3; if condition met AND current_fragment not empty: push current_fragment, start new fragment with section; else append to current_fragment
ACTION IF TRUE: When condition is satisfied AND fragments < 3: fragment boundary is created
ACTION IF FALSE: section is concatenated to current_fragment
POST-CONDITION: assert len(fragments) == 4 with 6 sections of equal content
ERROR: AssertionError: "Expected 4 fragments, got {len(fragments)}"
FIELDS INVOLVED: sections (list), total_chars, target (= total_chars / 4), fragments (list), current_fragment (str)
CALLS: re.split(r'\n(?=#+ )', '\n' + paper_text_norm)
SOURCE: tests/test_section_splitter.py:47-75
```

### RULE-10: PaperAuditor required skill attributes
```
RULE: PaperAuditor must expose exactly 6 skill attributes
TRIGGER: On initialization of PaperAuditor()
CONDITION: hasattr(auditor, attr) for each of: 'extraction_skill', 'hybrid_hp_skill', 'evaluation_skill', 'verification_skill', 'metrics_skill', 'metadata_skill'
ACTION IF TRUE: test passes
ACTION IF FALSE: AssertionError with message "Falta <attr>"
ERROR: sys.exit(1) on AssertionError
FIELDS INVOLVED: auditor object attributes
SOURCE: test_skills_integration.py:68-77
```

### RULE-11: Chatbot required skill attributes
```
RULE: Chatbot must expose exactly 2 skill attributes
TRIGGER: On initialization of Chatbot()
CONDITION: hasattr(chatbot, 'response_skill') AND hasattr(chatbot, 'validation_skill')
ACTION IF TRUE: test passes
ACTION IF FALSE: AssertionError with message "Falta <attr>"
ERROR: sys.exit(1)
FIELDS INVOLVED: chatbot object attributes
SOURCE: test_skills_integration.py:82-87
```

### RULE-12: SotaAnalyzer required skill attributes
```
RULE: SotaAnalyzer must expose exactly 5 skill attributes
TRIGGER: On initialization of SotaAnalyzer()
CONDITION: hasattr(sota, attr) for each of: 'thematic_skill', 'query_skill', 'search_skill', 'gap_skill', 'validation_skill'
ACTION IF TRUE: test passes
ACTION IF FALSE: AssertionError with message "Falta <attr>"
ERROR: sys.exit(1)
FIELDS INVOLVED: sota object attributes
SOURCE: test_skills_integration.py:93-99
```

### RULE-13: SemanticScholarSearchSkill empty-query returns empty sota_papers
```
RULE: SemanticScholarSearchSkill with empty search_queries returns result containing 'sota_papers' key
TRIGGER: On call to search_skill.execute({'search_queries': []})
CONDITION: context['search_queries'] == []
ACTION IF TRUE: result dict contains key 'sota_papers'
ACTION IF FALSE: N/A (test fails)
ERROR: Any exception causes sys.exit(1)
FIELDS INVOLVED: context['search_queries'], result['sota_papers']
SOURCE: test_skills_integration.py:134-136
```

### RULE-14: AuditState default initialization values
```
RULE: AuditState initializes with correct defaults
TRIGGER: On AuditState(paper_text="Test content") construction
CONDITION: always (construction rule)
ACTION IF TRUE: state.paper_text == "Test content"; state.invalid_paper == False; state.execution_time == 0.0
ACTION IF FALSE: N/A
ERROR: AssertionError
FIELDS INVOLVED: paper_text, invalid_paper, execution_time
SOURCE: tests/test_audit_state.py:6-10
```

### RULE-15: AuditState.to_frontend_dict must contain required keys
```
RULE: to_frontend_dict output must contain claims, informacion_extraida, metricas keys
TRIGGER: On state.to_frontend_dict() call with evaluation={"claims": {"answer": "Yes"}}
CONDITION: always (output contract)
ACTION IF TRUE: d["claims"]["answer"] == "Yes"; "informacion_extraida" in d; "metricas" in d
ACTION IF FALSE: AssertionError
ERROR: AssertionError
FIELDS INVOLVED: d["claims"]["answer"], d["informacion_extraida"], d["metricas"]
SOURCE: tests/test_audit_state.py:13-18
```

### RULE-16: ExtractedInfo.code.repository_url default value
```
RULE: ExtractedInfo sub-model code.repository_url defaults to "NOT FOUND"
TRIGGER: On ExtractedInfo() construction
CONDITION: always (default value contract)
ACTION IF TRUE: info.code.repository_url == "NOT FOUND"
ACTION IF FALSE: AssertionError
ERROR: AssertionError
FIELDS INVOLVED: info.code.repository_url
SOURCE: tests/test_audit_state.py:22
```

### RULE-17: ExtractedInfo.hyperparameters.optimizer default value
```
RULE: ExtractedInfo sub-model hyperparameters.optimizer defaults to "NOT FOUND"
TRIGGER: On ExtractedInfo() construction
CONDITION: always (default value contract)
ACTION IF TRUE: info.hyperparameters.optimizer == "NOT FOUND"
ACTION IF FALSE: AssertionError
ERROR: AssertionError
FIELDS INVOLVED: info.hyperparameters.optimizer
SOURCE: tests/test_audit_state.py:23
```

### RULE-18: CrowdsourcingDetectionSkill — negation gate
```
RULE: Crowdsourcing negation pattern suppresses active crowdsourcing detection
TRIGGER: On CrowdsourcingDetectionSkill.execute(context) when negation matches
CONDITION: re.search(NEGATION_CROWD, text, re.IGNORECASE) returns a match
  where NEGATION_CROWD = r"(?:no|not|without|does\s+not\s+use|did\s+not\s+use).{0,20}(?:human\s+subject|human\s+annotator|crowdsourc|human\s+participant)"
ACTION IF TRUE: has_negation=True; skip CROWDSOURCING_ACTIVE scan; has_active_crowd=False
ACTION IF FALSE: proceed with CROWDSOURCING_ACTIVE regex scan
ERROR: N/A
FIELDS INVOLVED: text (paper_text), has_negation, has_active_crowd
SOURCE: scratch/patch_skills.py:41-46
```

### RULE-19: LicenseDetectionSkill — posible_licencia_faltante
```
RULE: Flag possible missing license when a known dataset is used but no explicit license is found
TRIGGER: On LicenseDetectionSkill.execute(context)
CONDITION: uses_known_dataset == True AND found_license == False
ACTION IF TRUE: license_flags['posible_licencia_faltante'] = True
ACTION IF FALSE: license_flags['posible_licencia_faltante'] = False
ERROR: N/A
FIELDS INVOLVED: found_license (bool), uses_known_dataset (bool), license_flags['posible_licencia_faltante']
SOURCE: scratch/patch_skills.py:96
```

### RULE-20: CrowdsourcingDetectionSkill — sin_compensacion_mencionada
```
RULE: Flag missing compensation when crowdsourcing is active but no compensation mention found
TRIGGER: On CrowdsourcingDetectionSkill.execute(context)
CONDITION: has_active_crowd == True AND re.search(COMPENSATION, text, re.IGNORECASE) returns no match
ACTION IF TRUE: crowdsourcing_flags['sin_compensacion_mencionada'] = True
ACTION IF FALSE: crowdsourcing_flags['sin_compensacion_mencionada'] = False
ERROR: N/A
FIELDS INVOLVED: has_active_crowd, has_comp, crowdsourcing_flags['sin_compensacion_mencionada']
SOURCE: scratch/patch_skills.py:59
```

---

## 7. API / Service Contracts & Batch Jobs (Category 8)

### 7.1 CLI — `md_to_pdf.py`

**Entry point:** `if __name__ == "__main__": main()` — SOURCE: md_to_pdf.py:323-324

**Arguments (parsed manually from `sys.argv`):**

| Argument | Required | Default | Accepted Values |
|----------|----------|---------|-----------------|
| positional `sys.argv[1]` | Yes | — | File path (`.md`/`.txt`) or `'--folder'` |
| positional `sys.argv[2]` | No | None | Output PDF path OR folder path (depends on mode) |
| `--size <value>` | No | `'letter'` | `'letter'` or `'a4'` |
| `--output <path>` | No | None | Output folder (folder mode) |

**Output:** PDF file(s) at derived or specified paths.

### 7.2 CLI — `pdf_to_md.py`

**Entry point:** `if __name__ == "__main__": main()` — SOURCE: pdf_to_md.py:157-158

**Arguments:**

| Argument | Required | Default | Accepted Values |
|----------|----------|---------|-----------------|
| positional `sys.argv[1]` | Yes | — | PDF path or `'--folder'` |
| positional `sys.argv[2]` | No | None | Output `.md` path |
| `--output <path>` (at `sys.argv[3]`/`sys.argv[4]`) | No | None | Output folder (folder mode) |

**Output:** `.md` file(s) at derived or specified paths.

### 7.3 CLI — `create_test_pdf.py`

**Entry point:** `if __name__ == "__main__": create_test_paper_pdf()` — SOURCE: create_test_pdf.py:182-183

**Arguments:** None.

**Output:** `paper_test_con_errores.pdf` in current working directory.

### 7.4 CLI — `list_models.py`

**Entry point:** Script-level execution (no `if __name__` guard) — SOURCE: list_models.py:1-18

**Arguments:** None (reads `GOOGLE_API_KEY` from environment).

**External API call:**
- **Service:** Google GenAI API via `google.genai.Client`
- **Method:** `client.models.list()`
- **Auth:** `api_key=GOOGLE_API_KEY` (from `os.getenv("GOOGLE_API_KEY")`)
- **Request payload:** None (no body parameters documented in this file)
- **Response fields accessed:** `m.name` (model ID), `m.display_name` (human-readable name)
- **Error handling:** `except Exception as e: print(f"Error listando modelos: {e}")` — SOURCE: list_models.py:17-18

### 7.5 External API — Google GenAI `embed_content` (backend/scratch/test_embed.py)

- **Service:** Google GenAI API via `google.genai.Client`
- **Method:** `client.models.embed_content`
- **Model:** `"gemini-embedding-2"` — SOURCE: backend/scratch/test_embed.py:11
- **Auth:** `api_key=os.getenv("GOOGLE_API_KEY")` — SOURCE: backend/scratch/test_embed.py:6
- **Request payload:**
  - `model`: `"gemini-embedding-2"` (str)
  - `contents`: list of strings — e.g., `["hello", "world", "test"]` — SOURCE: backend/scratch/test_embed.py:8
- **Response fields accessed:**
  - `res.embeddings` (list): list of embedding objects — SOURCE: backend/scratch/test_embed.py:16
  - `res.embeddings[0].values` (list): numeric embedding vector — SOURCE: backend/scratch/test_embed.py:21

### 7.6 External API — Google GenAI `embed_content` (backend/scratch/test_embed2.py)

Same as 7.5. Additional error handling:
- **Error path:** `except Exception as e: print("embed_content error:", e)` — SOURCE: backend/scratch/test_embed2.py:16

### 7.7 Streamlit Web Application (app.py)

- **Type:** Interactive web application (not REST API)
- **File input widget:** accepts `["pdf", "txt", "md"]` — SOURCE: app.py:50-51
- **Processing trigger:** non-None `uploaded_file`
- **Report download:** provides `.md` report via `st.download_button`, `mime="text/markdown"`, filename pattern `"auditoria_{uploaded_file.name.replace('.pdf', '')}.md"` — SOURCE: app.py:74-79

### 7.8 Batch Job — `convert_folder` in md_to_pdf.py

- **Input source:** `Path(folder_path).glob('*.md')` + `Path(folder_path).glob('*.txt')` — SOURCE: md_to_pdf.py:223-225
- **Iteration:** for each file in `all_files`, numbered 1..N — SOURCE: md_to_pdf.py:242
- **Per-item processing:** call `convert_to_pdf(str(file), output_path, page_size)` — SOURCE: md_to_pdf.py:250
- **Error handling per item:** function returns `None` on failure; `failed += 1` counter incremented — SOURCE: md_to_pdf.py:253-255
- **Output destination:** `output_folder` (if specified) or same directory as source file

### 7.9 Batch Job — `convert_folder` in pdf_to_md.py

- **Input source:** `Path(folder_path).glob('*.pdf')` — SOURCE: pdf_to_md.py:78
- **Iteration:** for each `pdf_file` in `pdf_files`, numbered 1..N — SOURCE: pdf_to_md.py:95
- **Per-item processing:** call `convert_pdf_to_md(str(pdf_file), output_path)` — SOURCE: pdf_to_md.py:103
- **Error handling per item:** function returns `None` on failure; `failed += 1` — SOURCE: pdf_to_md.py:107

---

## 8. Constants, Enums, and Lookup Tables (Category 9)

| Name | Value | File | Line | Purpose |
|------|-------|------|------|---------|
| `TRANSFORMERS_VERBOSITY` (env var value) | `"error"` | app.py | 13 | Suppress transformer log output |
| `TOKENIZERS_PARALLELISM` (env var value) | `"false"` | app.py | 14 | Suppress tokenizer warnings |
| `ANONYMIZED_TELEMETRY` (env var value) | `"False"` | app.py | 21 | Disable ChromaDB telemetry |
| `OTEL_SDK_DISABLED` (env var value) | `"true"` | app.py | 22 | Disable OpenTelemetry SDK |
| `page_title` (st.set_page_config) | `"Nature Auditor Pro"` | app.py | 26 | Browser tab title |
| `layout` (st.set_page_config) | `"wide"` | app.py | 27 | Streamlit layout mode |
| `page_icon` (st.set_page_config) | `"🔬"` | app.py | 28 | Browser tab icon |
| accepted file types (file_uploader) | `["pdf", "txt", "md"]` | app.py | 50 | Allowed upload formats |
| download mime type | `"text/markdown"` | app.py | 78 | MIME type for report download |
| sidebar image width | `150` | app.py | 86 | Streamlit sidebar image width in pixels |
| output PDF filename (create_test_pdf) | `"paper_test_con_errores.pdf"` | create_test_pdf.py | 12 | Hardcoded output filename |
| title fontSize (create_test_pdf) | `16` | create_test_pdf.py | 19 | PDF title font size |
| title textColor (create_test_pdf) | `'#000000'` | create_test_pdf.py | 20 | Title text color |
| title spaceAfter (create_test_pdf) | `30` | create_test_pdf.py | 21 | Title space after in points |
| title alignment (create_test_pdf) | `1` (CENTER) | create_test_pdf.py | 22 | Reportlab alignment constant |
| spacer height (create_test_pdf, after title) | `0.2*inch` | create_test_pdf.py | 29 | Post-title spacer |
| table data | `[['Model', 'Accuracy'], ['Ours', '95.2%'], ['Baseline', '92.1%']]` | create_test_pdf.py | 106-110 | Results table content |
| tableStyle header background | `colors.grey` | create_test_pdf.py | 113 | Header row background color |
| tableStyle header text | `colors.whitesmoke` | create_test_pdf.py | 114 | Header text color |
| tableStyle font | `'Helvetica-Bold'` | create_test_pdf.py | 116 | Header font name |
| tableStyle fontSize | `12` | create_test_pdf.py | 117 | Header font size |
| tableStyle bottomPadding | `12` | create_test_pdf.py | 118 | Header bottom padding |
| tableStyle data background | `colors.beige` | create_test_pdf.py | 119 | Data row background |
| Code style fontName | `'Courier'` | md_to_pdf.py | 158 | Monospace font for code blocks |
| Code style fontSize | `9` | md_to_pdf.py | 159 | Font size for code blocks |
| Code style leftIndent | `20` | md_to_pdf.py | 160 | Code block left margin |
| Code style rightIndent | `20` | md_to_pdf.py | 161 | Code block right margin |
| Code style textColor | `HexColor('#2d2d2d')` | md_to_pdf.py | 162 | Code text color |
| Code style backColor | `HexColor('#f5f5f5')` | md_to_pdf.py | 163 | Code background color |
| Code style borderPadding | `5` | md_to_pdf.py | 164 | Code border padding |
| Normal fontSize | `11` | md_to_pdf.py | 168 | Body text font size |
| Normal leading | `14` | md_to_pdf.py | 169 | Body text line height |
| Normal alignment | `TA_JUSTIFY` | md_to_pdf.py | 170 | Body text alignment |
| Heading1 fontSize | `18` | md_to_pdf.py | 172 | H1 font size |
| Heading1 textColor | `HexColor('#1a1a1a')` | md_to_pdf.py | 173 | H1 color |
| Heading1 spaceAfter | `12` | md_to_pdf.py | 174 | H1 space after |
| Heading2 fontSize | `14` | md_to_pdf.py | 176 | H2 font size |
| Heading2 textColor | `HexColor('#2d2d2d')` | md_to_pdf.py | 177 | H2 color |
| Heading2 spaceAfter | `10` | md_to_pdf.py | 178 | H2 space after |
| Heading3 fontSize | `12` | md_to_pdf.py | 180 | H3 font size |
| Heading3 textColor | `HexColor('#404040')` | md_to_pdf.py | 181 | H3 color |
| Heading3 spaceAfter | `8` | md_to_pdf.py | 182 | H3 space after |
| PDF margins (right, left, top, bottom) | `72, 72, 72, 18` (points) | md_to_pdf.py | 145-148 | Document margins |
| page_count estimator divisor | `30` | md_to_pdf.py | 192 | Approx elements per page |
| default page_size | `'letter'` | md_to_pdf.py | 290 | CLI default page size |
| embed model name | `"gemini-embedding-2"` | backend/scratch/test_embed.py | 11 | Google GenAI embedding model |
| embed model name | `"gemini-embedding-2"` | backend/scratch/test_embed2.py | 11 | Google GenAI embedding model (duplicate) |
| LLMClient model_name (test) | `"test-model"` | scratch/test_llm_retry.py | 17 | Test model name |
| Exception message trigger | `"503 UNAVAILABLE: High demand"` | scratch/test_llm_retry.py | 25-26 | Simulated 503 error |
| expected total LLM calls on exhaustion | `6` | scratch/test_llm_retry.py | 55 | 1 original + 5 retries |
| expected sleep calls on exhaustion | `5` | scratch/test_llm_retry.py | 55 | One sleep per retry |
| expected sleep calls on partial retry | `2` | scratch/test_llm_retry.py | 35 | Sleeps before third success |
| expected call count on partial retry | `3` | scratch/test_llm_retry.py | 34 | 2 failures + 1 success |
| RAG split pattern | `r'\n\n+'` | scratch/test_rag_split.py | 22 | Regex pattern to split paragraphs |
| RAG chunk minimum length | `> 10` (characters) | tests/test_rag_logical_splitter.py | 29 | Minimum chunk size after strip |
| Section split pattern | `r'\n(?=#+ )'` | tests/test_section_splitter.py | 44 | Regex pattern to split on headers |
| Fragment target divisor | `4` (total_chars / 4) | tests/test_section_splitter.py | 49 | Target size per fragment |
| Maximum fragments before last | `3` | tests/test_section_splitter.py | 54 | Cap on early fragment creation |
| Expected fragment count (6-section paper) | `4` | tests/test_section_splitter.py | 75 | Expected output |
| REGEX_PATTERNS minimum count | `> 0` | test_auditor_refactor.py | 19 | Must define at least one regex pattern |
| test_text for preprocess | `"This is a test paper with github.com/test/repo"` | test_auditor_refactor.py | 31 | Input with GitHub URL for red flag detection |
| test_text for prompts | `"Test paper"` | test_auditor_refactor.py | 43 | Minimal prompt text |
| test_info for prompts | `{"test": "info"}` | test_auditor_refactor.py | 50 | Minimal info dict |
| test_flags | `{"test": True}` | test_auditor_refactor.py | 44 | Minimal red flags dict |
| AuditState default invalid_paper | `False` | tests/test_audit_state.py | 9 | Default boolean state |
| AuditState default execution_time | `0.0` | tests/test_audit_state.py | 10 | Default timing value |
| ExtractedInfo code.repository_url default | `"NOT FOUND"` | tests/test_audit_state.py | 22 | Default string for missing repo |
| ExtractedInfo hyperparameters.optimizer default | `"NOT FOUND"` | tests/test_audit_state.py | 23 | Default string for missing optimizer |
| LLMClient model constructor param | `model_name="test-model"` | scratch/test_llm_retry.py | 17 | LLMClient constructor parameter name |
| embed contents (test) | `["hello", "world", "test"]` | backend/scratch/test_embed.py | 8 | Test batch for embedding API |
| mock_eval key list (checklist) | `['claims', 'limitations', 'theory_assumptions_proofs', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiment_statistical_significance', 'experiments_compute_resource', 'code_of_ethics', 'broader_impacts', 'safeguards', 'licenses', 'assets', 'crowdsourcing_human_subjects', 'irb_approvals', 'declaration_llm_usage']` | scratch/test_checklist_health.py | 7-23 | 16 checklist item keys |
| CROWDSOURCING_ACTIVE regex[0] | `r"(?<!no\s)(?<!without\s)(?<!not\s)\b(crowdsourc|Mechanical\s+Turk|MTurk|Prolific|Scale\s+AI)\b"` | scratch/patch_skills.py | 19 | Active crowdsourcing pattern 1 |
| CROWDSOURCING_ACTIVE regex[1] | `r"\b(we\s+(?:hired|recruited|employed|paid)\s+.{0,30}(?:annotator|worker|participant))"` | scratch/patch_skills.py | 20 | Active crowdsourcing pattern 2 |
| CROWDSOURCING_ACTIVE regex[2] | `r"\b(human\s+annotators?\s+(?:were|are|were\s+asked|labeled|annotated))"` | scratch/patch_skills.py | 21 | Active crowdsourcing pattern 3 |
| CROWDSOURCING_ACTIVE regex[3] | `r"\b(participants?\s+(?:were\s+)?(?:recruited|compensated|paid))"` | scratch/patch_skills.py | 22 | Active crowdsourcing pattern 4 |
| HUMAN_DATASET_USE regex[0] | `r"\b(human[\s-]?label(?:ed|ing)|human[\s-]?annotat(?:ed|ion))\b"` | scratch/patch_skills.py | 26 | Human-labeled dataset pattern 1 |
| HUMAN_DATASET_USE regex[1] | `r"\b(SFT|RLHF|human\s+feedback|preference\s+data).{0,40}(?:dataset|data|corpus)"` | scratch/patch_skills.py | 27 | Human-labeled dataset pattern 2 |
| COMPENSATION regex | `r"\b(compensation|wage|paid\s+(?:at|\$)|minimum\s+wage|hourly\s+rate|instructions\s+provided|consent\s+form)\b"` | scratch/patch_skills.py | 29 | Worker compensation mention pattern |
| NEGATION_CROWD regex | `r"(?:no|not|without|does\s+not\s+use|did\s+not\s+use).{0,20}(?:human\s+subject|human\s+annotator|crowdsourc|human\s+participant)"` | scratch/patch_skills.py | 31 | Crowdsourcing negation pattern |
| EXPLICIT_LICENSE regex | `r"(CC[\s-]BY(?:[\s-]\d\.\d)?(?:[\s-](?:SA|NC|ND))*|MIT\s+[Ll]icense|Apache\s+2\.0|GPL(?:[\s-]\d)?|BSD(?:[\s-]\d[\s-][Cc]lause)?|Creative\s+Commons|\bCC0\b)"` | scratch/patch_skills.py | 68 | Explicit license pattern |
| KNOWN_DATASETS regex | `r"\b(ImageNet|COCO|CIFAR|MNIST|WikiText|RedPajama|OpenWebText|Alpaca|ShareGPT|LAION|WMT\d+|SQuAD|GLUE|SuperGLUE|HumanEval|GSM8K|MMLU|CommonCrawl|BookCorpus|The\s+Pile)\b"` | scratch/patch_skills.py | 70 | Known dataset name pattern |
| patch target filepath | `'backend/skills/regex_detection_skills.py'` | scratch/patch_skills.py | 6 | File to patch |
| patch class boundary markers | `'class CrowdsourcingDetectionSkill(BaseSkill):'`, `'class LicenseDetectionSkill(BaseSkill):'`, `'class LimitationsQualityDetectionSkill(BaseSkill):'` | scratch/patch_skills.py | 9-11 | String anchors for in-place replacement |
| spacer height (md_to_pdf empty line) | `0.1*inch` | md_to_pdf.py | 43 | Empty line spacer |
| spacer height (md_to_pdf H1) | `0.2*inch` | md_to_pdf.py | 51 | H1 post spacer |
| spacer height (md_to_pdf H2) | `0.15*inch` | md_to_pdf.py | 57 | H2 post spacer |
| spacer height (md_to_pdf H3) | `0.1*inch` | md_to_pdf.py | 63 | H3 post spacer |
| bullet prefix | `'• '` | md_to_pdf.py | 67 | Unicode bullet character prepended to list items |

---

## 9. Transformations (Category 10)

### 9.1 PDF → Markdown (`pdf_to_md.py`)

**Input:** Any valid `.pdf` file at `pdf_path`
**Processing:** Calls `pymupdf4llm.to_markdown(pdf_path)` (CROSS-REFERENCE: pymupdf4llm library, not in cluster)
**Output:** String `md_text` written verbatim to `output_path` (`.md` file) in UTF-8 encoding
**No field-by-field mapping available in this cluster** — `pymupdf4llm.to_markdown` is a third-party black box
**Output statistics computed:** `os.path.getsize(output_path)` bytes, `len(md_text)` chars, `md_text.count('\n')` lines

`SOURCE: pdf_to_md.py:41-45`

### 9.2 Markdown/TXT → PDF (`md_to_pdf.py`)

**Input:** UTF-8 text from `.md`/`.txt`/`.markdown` file, read via `open(input_path, 'r', encoding='utf-8').read()`
**Processing:** `parse_markdown_to_elements(content, styles)` → list of reportlab elements

**Transformation mapping per Markdown element:**

| Source (Markdown) | Target (reportlab) |
|-------------------|-------------------|
| Line starting with `# ` (not `## `) | `Paragraph(line[2:].strip(), styles['Heading1'])` + `Spacer(0.2*inch)` |
| Line starting with `## ` (not `### `) | `Paragraph(line[3:].strip(), styles['Heading2'])` + `Spacer(0.15*inch)` |
| Line starting with `### ` | `Paragraph(line[4:].strip(), styles['Heading3'])` + `Spacer(0.1*inch)` |
| Line starting with `- ` or `* ` | `Paragraph('• ' + line[2:].strip(), styles['Normal'])` |
| Line where `line[0].isdigit()` and `line[1:3] in ['. ', ') ']` | `Paragraph(line, styles['Normal'])` |
| Lines between ` ``` ` fences | Collected, joined with `\n`, → `Preformatted(code_text, styles['Code'])` + `Spacer(0.1*inch)` |
| Lines starting with `---` or `===` | `Spacer(0.1*inch)` + `Paragraph('<hr/>', styles['Normal'])` + `Spacer(0.1*inch)` |
| Empty line | `Spacer(1, 0.1*inch)` |
| All other lines | `**text**` → `<b>text<b>` (note: naive sequential double-replace), `*text*` → `<i>text<i>`, → `Paragraph(text, styles['Normal'])` |

**Page estimate:** `len(elements) // 30` (approximate, used only for output statistics)

`SOURCE: md_to_pdf.py:38-101`

### 9.3 Markdown → PDF from Scratch (create_test_pdf.py)

**Input:** Hardcoded string content (no file read)
**Output:** `paper_test_con_errores.pdf` with `pagesize=letter`
**Transformation:** Uses reportlab `Paragraph`, `Spacer`, `Table` elements directly — no Markdown parsing

`SOURCE: create_test_pdf.py:8-180`

### 9.4 Text → Embedding vector (backend/scratch/test_embed.py)

**Input:** `contents = ["hello", "world", "test"]` — list of strings
**API call:** `client.models.embed_content(model="gemini-embedding-2", contents=contents)`
**Output:** `res.embeddings` — list of embedding objects, one per input string
**Vector access:** `res.embeddings[0].values` — list of numeric values (embedding vector for first input)
**Length of values:** printed as `len(res.embeddings[0].values)` but no assertion on specific dimension in this file

`SOURCE: backend/scratch/test_embed.py:8-23`

### 9.5 Paper Text → RAG Chunks (scratch/test_rag_split.py)

**Function:** `get_rag_chunks(paper_text)`
**Input:** Raw paper text string (may contain `\r\n`)
**Transform steps:**
1. Normalize: `paper_text.replace('\r\n', '\n')` — SOURCE: scratch/test_rag_split.py:5
2. Split: `re.split(r'\n\n+', paper_text)` — SOURCE: scratch/test_rag_split.py:22
3. Filter+strip: `[c.strip() for c in raw_chunks if c.strip()]` — SOURCE: scratch/test_rag_split.py:23
**Output:** List of non-empty stripped strings (chunk list)
**No minimum length filter** (strips whitespace but does not enforce minimum length)

`SOURCE: scratch/test_rag_split.py:3-24`

### 9.6 Paper Text → RAG Chunks with length filter (tests/test_rag_logical_splitter.py)

**Same split strategy as 9.5 but with minimum length filter:**
1. Normalize: `paper_text.replace('\r\n', '\n')` — SOURCE: tests/test_rag_logical_splitter.py:27
2. Split: `re.split(r'\n\n+', paper_text_norm)` — SOURCE: tests/test_rag_logical_splitter.py:28
3. Filter: `[c.strip() for c in raw_chunks if len(c.strip()) > 10]` — SOURCE: tests/test_rag_logical_splitter.py:29
**Output:** List of strings where each has `len > 10` after stripping

### 9.7 Paper Text → Section Fragments (tests/test_section_splitter.py)

**Function:** `TestSkill.get_fragments(paper_text)` (defined inline in test)
**Input:** Paper text with Markdown headers
**Transform steps:**
1. Normalize: `paper_text.replace('\r\n', '\n')` — SOURCE: tests/test_section_splitter.py:43
2. Prepend newline and split on header starts: `re.split(r'\n(?=#+ )', '\n' + paper_text_norm)` — SOURCE: tests/test_section_splitter.py:44
3. Strip and filter empty: `[s.strip() for s in sections if s.strip()]` — SOURCE: tests/test_section_splitter.py:45
4. If `len(sections) > 1`:
   - Compute `total_chars = sum(len(s) for s in sections)` — SOURCE: tests/test_section_splitter.py:48
   - Compute `target = total_chars / 4` — SOURCE: tests/test_section_splitter.py:49
   - Accumulate sections into `current_fragment`; create fragment boundary when `len(current_fragment) + len(section) > target AND len(fragments) < 3` — SOURCE: tests/test_section_splitter.py:54
   - Append final `current_fragment` after loop — SOURCE: tests/test_section_splitter.py:66
5. If `len(sections) <= 1`: return `[]` — SOURCE: tests/test_section_splitter.py:69
**Output:** List of 4 fragments from 6 equal-length sections

---

## 10. Error Handling (Category 12)

### 10.1 `convert_to_pdf` — general exception catch
```
LOCATION: md_to_pdf.py:203-207
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"❌ Error durante la conversión: {str(e)}")
  import traceback
  traceback.print_exc()
  return None
RECOVERY: caller receives None as return value; no re-raise
```

### 10.2 `convert_pdf_to_md` — general exception catch
```
LOCATION: pdf_to_md.py:61-63
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"❌ Error durante la conversión: {str(e)}")
  return None
RECOVERY: caller receives None; no traceback printed; no re-raise
```

### 10.3 `list_models.py` — API listing error
```
LOCATION: list_models.py:17-18
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"Error listando modelos: {e}")
RECOVERY: program continues past try/except (no exit); no re-raise
```

### 10.4 `list_models.py` — missing API key guard
```
LOCATION: list_models.py:8-10
CONDITION: GOOGLE_API_KEY is None or empty string (falsy)
BLOCK:
  print("No se encontró GOOGLE_API_KEY")
  exit()
RECOVERY: none — program exits; not a try/except, a conditional guard
```

### 10.5 `md_to_pdf.py` — markdown2 import failure
```
LOCATION: md_to_pdf.py:15-20
EXCEPTION TYPES: ImportError
BLOCK:
  HAS_MARKDOWN = False
  print("⚠️ Advertencia: markdown2 no instalado. Solo se soportará conversión básica.")
  print("   Instala con: pip install markdown2")
RECOVERY: HAS_MARKDOWN flag set to False; program continues with basic conversion (note: HAS_MARKDOWN is never checked in parse_markdown_to_elements — it appears the flag is set but not used to gate any code path in the files in this cluster)
DEPENDENCY_NOTE: markdown2 is absent from requirements.txt (requirements.txt:1–5 lists only docling,
  google-generativeai, python-dotenv, streamlit, pydantic). In any environment installed strictly from
  requirements.txt, the except ImportError branch is the default and only execution path — the try block
  always fails. HAS_MARKDOWN is therefore always False in a standard install, meaning the markdown-conversion
  feature is permanently and silently disabled. No code path downstream reads HAS_MARKDOWN to gate behaviour,
  so there is no runtime failure beyond the warning print; however, the package is undeclared and the
  ImportError on every startup is the expected (not exceptional) outcome in the reference environment.
SOURCE: md_to_pdf.py:15–17, requirements.txt:1–5 (absence confirmed)
```

### 10.6 `test_auditor_refactor.py` — each test function wraps in try/except
```
LOCATION: test_auditor_refactor.py:7-13 (test_auditor_initialization)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"❌ Error al inicializar auditor: {e}")
  return False
RECOVERY: caller collects (name, False) in results list; counted in failed total
```

```
LOCATION: test_auditor_refactor.py:17-24 (test_regex_patterns)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"❌ Error en patrones regex: {e}")
  return False
```

```
LOCATION: test_auditor_refactor.py:27-38 (test_preprocess_method)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"❌ Error en _preprocess_paper: {e}")
  return False
```

```
LOCATION: test_auditor_refactor.py:41-58 (test_prompts_module)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"❌ Error en módulo prompts: {e}")
  return False
```

### 10.7 `test_skills_integration.py` — try/except with sys.exit(1)
```
LOCATION: test_skills_integration.py:11-35 (import test)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"   [ERROR] Error en importaciones: {e}")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:39-46 (services import test)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"   [ERROR] Error importando servicios: {e}")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:49-63 (services initialization)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"   [ERROR] Error inicializando servicios: {e}")
  import traceback; traceback.print_exc()
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:75-77 (PaperAuditor skill check)
EXCEPTION TYPES: AssertionError
BLOCK:
  print(f"   [ERROR] {e}")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:85-87 (Chatbot skill check)
EXCEPTION TYPES: AssertionError
BLOCK:
  print(f"   [ERROR] {e}")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:97-100 (SotaAnalyzer skill check)
EXCEPTION TYPES: AssertionError
BLOCK:
  print(f"   [ERROR] {e}")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:109-111 (BaseSkill inheritance)
EXCEPTION TYPES: AssertionError
BLOCK:
  print("   [ERROR] Error en herencia de BaseSkill")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:119-124 (BaseSkill methods)
EXCEPTION TYPES: AssertionError
BLOCK:
  print(f"   [ERROR] {e}")
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:137-141 (SemanticScholarSearchSkill execution)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"   [ERROR] Error ejecutando skill: {e}")
  import traceback; traceback.print_exc()
  sys.exit(1)
```

```
LOCATION: test_skills_integration.py:148-150 (logging check)
EXCEPTION TYPES: Exception (any)
BLOCK:
  print(f"   [ERROR] Error en logging: {e}")
  sys.exit(1)
```

### 10.8 `scratch/test_llm_retry.py` — test_final_failure expected exception
```
LOCATION: scratch/test_llm_retry.py:51-56
EXCEPTION TYPES: Exception (any) expected to be raised
BLOCK:
  try:
      client.generate("test prompt")
      assert False, "Should have raised an exception"
  except Exception as e:
      print(f"Caught expected final exception: {e}")
      assert mock_gen.call_count == 6  # 1 original + 5 retries
RECOVERY: verifies that exception WAS raised; test passes if exception occurs
```

### 10.9 `backend/scratch/test_embed2.py` — embed_content error
```
LOCATION: backend/scratch/test_embed2.py:9-16
EXCEPTION TYPES: Exception (any)
BLOCK:
  print("embed_content error:", e)
RECOVERY: script continues; no re-raise
```

### 10.10 `scratch/patch_skills.py` — no error handling
The script performs `open(...).read()`, string index operations, and `open(...).write()` without any try/except. It calls `ast.parse(new_content)` at the end as a post-write syntax validation. If any step fails, the exception propagates uncaught to the interpreter.
`SOURCE: scratch/patch_skills.py:6-108`

### 10.11 Retry mechanism (LLMClient — from test_llm_retry.py evidence)

**Total attempts:** 6 (1 original + 5 retries)
**Triggering condition:** Exception raised by `client.client.models.generate_content` (specifically `"503 UNAVAILABLE"` message in test)
**Sleep calls:** `time.sleep` called once per retry (5 times on exhaustion, 2 times when success on 3rd attempt)
**Sleep interval:** Not determinable from test file (mocked with `patch('time.sleep')`)
**Final action on exhaustion:** Exception re-raised (caught in `test_final_failure` as expected)

`SOURCE: scratch/test_llm_retry.py:24-56`

---

## 11. Test Suite Specifications

### 11.1 test_auditor_refactor.py (root)

**Type:** Script-based integration tests (not pytest — uses `main()` runner)

**Function: `test_auditor_initialization()`** — SOURCE: test_auditor_refactor.py:5
- Setup: None
- Input: None (calls `PaperAuditor()` with no arguments)
- Action: Constructs `PaperAuditor()` instance
- Assertion: If no exception raised → `return True`; if any `Exception` raised → `return False`
- No `assert` statement — pass/fail determined by exception absence

**Function: `test_regex_patterns()`** — SOURCE: test_auditor_refactor.py:15
- Setup: Imports `REGEX_PATTERNS` from `backend.services.auditor`
- Assertion: `assert len(REGEX_PATTERNS) > 0` — at least 1 pattern must be defined

**Function: `test_preprocess_method()`** — SOURCE: test_auditor_refactor.py:26
- Setup: Constructs `PaperAuditor()`
- Input: `text = "This is a test paper with github.com/test/repo"`
- Action: Calls `auditor._preprocess_paper(text)`
- Assertions:
  1. `assert isinstance(red_flags, dict)` — return type must be dict
- Side effect: Prints count of truthy values in red_flags dict

**Function: `test_prompts_module()`** — SOURCE: test_auditor_refactor.py:40
- Setup: Imports `get_extraction_prompt`, `get_evaluation_prompt` from `backend.common.prompts`
- Input for extraction: `test_text = "Test paper"`, `test_flags = {"test": True}`
- Input for evaluation: `test_info = {"test": "info"}`, `test_flags = {"test": True}`
- Assertions:
  1. `assert len(extraction_prompt) > 0`
  2. `assert len(evaluation_prompt) > 0`

**Function: `main()`** — SOURCE: test_auditor_refactor.py:60
- Runs all 4 tests in order: Auditor initialization, Regex patterns, Preprocess method, Prompts module
- Collects `(name, bool_result)` tuples
- Prints summary: `"✅ PASS"` or `"❌ FAIL"` per test
- Prints `passed/total` count
- If `passed == total`: prints "Refactorización completada exitosamente!"
- Else: prints "Algunos tests fallaron."

### 11.2 test_imports.py (root)

**Type:** Script (sequential import checks, no pytest)

**Structure:** 7 sequential `try/except Exception` blocks each attempting one import:

| Block | Import target | Success output | Failure output |
|-------|---------------|----------------|----------------|
| 1 | `from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION` | `"OK frontend.config"` | `"ERROR frontend.config: {e}"` |
| 2 | `from frontend.styles.custom_css import apply_custom_styles` | `"OK frontend.styles.custom_css"` | `"ERROR frontend.styles.custom_css: {e}"` |
| 3 | `from frontend.utils.session_state import initialize_session_state` | `"OK frontend.utils.session_state"` | `"ERROR frontend.utils.session_state: {e}"` |
| 4 | `from frontend.components.file_uploader import process_uploaded_file` | `"OK frontend.components.file_uploader"` | `"ERROR frontend.components.file_uploader: {e}"` |
| 5 | `from frontend.components.audit_results import render_audit_results, generate_report` | `"OK frontend.components.audit_results"` | `"ERROR frontend.components.audit_results: {e}"` |
| 6 | `from frontend.components.sota_section import render_sota_analysis` | `"OK frontend.components.sota_section"` | `"ERROR frontend.components.sota_section: {e}"` |
| 7 | `from frontend.components.chatbot import render_chatbot` | `"OK frontend.components.chatbot"` | `"ERROR frontend.components.chatbot: {e}"` |

`SOURCE: test_imports.py:4-44`

Final print: `"Todas las importaciones funcionan correctamente!"` — SOURCE: test_imports.py:46

### 11.3 test_skills_integration.py (root)

**Type:** Script (10 numbered tests with sys.exit(1) on failure)

**Test 1 — Module imports** — SOURCE: test_skills_integration.py:9-35
- Imports all 12 skill classes from `backend.skills` and 3 from `backend.skills.regex_detection_skills`
- Imported symbols: `BaseSkill`, `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ConversationalResponseSkill`, `ContextValidationSkill`, `ThematicCoverageSkill`, `QueryGenerationSkill`, `SemanticScholarSearchSkill`, `CoverageGapAnalysisSkill`, `CrossValidationSkill`, `LimitationsQualityDetectionSkill`, `SoftwareVersionDetectionSkill`, `HardwareDetailDetectionSkill`
- Assertion: no exception

**Test 2 — Service imports** — SOURCE: test_skills_integration.py:38-46
- Imports: `PaperAuditor` from `backend.services.auditor`, `Chatbot` from `backend.services.chatbot`, `SotaAnalyzer` from `backend.services.sota_analyzer`
- Assertion: no exception

**Test 3 — Service initialization** — SOURCE: test_skills_integration.py:49-63
- Constructs: `PaperAuditor()`, `Chatbot()`, `SotaAnalyzer()`
- Assertion: no exception

**Test 4 — PaperAuditor skill attributes** — SOURCE: test_skills_integration.py:66-77
- Checks `hasattr(auditor, attr)` for: `'extraction_skill'`, `'hybrid_hp_skill'`, `'evaluation_skill'`, `'verification_skill'`, `'metrics_skill'`, `'metadata_skill'`
- AssertionError message: `"Falta <attr>"` for each missing attribute

**Test 5 — Chatbot skill attributes** — SOURCE: test_skills_integration.py:80-87
- Checks: `'response_skill'`, `'validation_skill'`
- AssertionError message: `"Falta <attr>"`

**Test 6 — SotaAnalyzer skill attributes** — SOURCE: test_skills_integration.py:90-100
- Checks: `'thematic_skill'`, `'query_skill'`, `'search_skill'`, `'gap_skill'`, `'validation_skill'`
- AssertionError message: `"Falta <attr>"`

**Test 7 — BaseSkill inheritance** — SOURCE: test_skills_integration.py:103-111
- Assertions:
  1. `isinstance(auditor.extraction_skill, BaseSkill)`
  2. `isinstance(chatbot.response_skill, BaseSkill)`
  3. `isinstance(sota.thematic_skill, BaseSkill)`

**Test 8 — BaseSkill required methods** — SOURCE: test_skills_integration.py:114-124
- `skill = auditor.extraction_skill`
- Checks: `hasattr(skill, 'execute')`, `hasattr(skill, 'validate_context')`, `hasattr(skill, 'log_execution')`, `callable(skill.execute)`
- AssertionError messages: `"Falta método execute"`, `"Falta método validate_context"`, `"Falta método log_execution"`, `"execute no es callable"`

**Test 9 — SemanticScholarSearchSkill execution** — SOURCE: test_skills_integration.py:127-141
- Setup: `from backend.skills.sota_skills import SemanticScholarSearchSkill`; `search_skill = SemanticScholarSearchSkill()`
- Input: `context = {'search_queries': []}`
- Action: `result = search_skill.execute(context)`
- Assertion: `assert 'sota_papers' in result`

**Test 10 — Logging** — SOURCE: test_skills_integration.py:144-151
- Setup: `from backend.utils.logger import get_logger`; `logger = get_logger("test_skill")`
- Action: `logger.info("Test de logging")`
- Assertion: no exception

### 11.4 backend/scratch/test_embed.py

**Type:** Scratch script (no assertions; only prints)

**Script-level execution:**
1. `load_dotenv()` — SOURCE: backend/scratch/test_embed.py:5
2. `client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))` — SOURCE: backend/scratch/test_embed.py:6
3. `contents = ["hello", "world", "test"]` — SOURCE: backend/scratch/test_embed.py:8
4. `res = client.models.embed_content(model="gemini-embedding-2", contents=contents)` — SOURCE: backend/scratch/test_embed.py:9-12
5. Print `type(res)` — SOURCE: backend/scratch/test_embed.py:14
6. If `hasattr(res, 'embeddings')`:
   - Print `type(res.embeddings)`
   - If `isinstance(res.embeddings, list)`:
     - Print `len(res.embeddings)`
     - Print `type(res.embeddings[0])`
     - Print `type(res.embeddings[0].values)`
     - Print `len(res.embeddings[0].values)`
   - Else: Print `"Embeddings is not a list. It is {type(res.embeddings)}"`
7. Else: Print `"No embeddings attribute"`

No assertions. No error handling.

### 11.5 backend/scratch/test_embed2.py

**Type:** Scratch script with error handling

**Script-level execution:**
1. `load_dotenv()`, `client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))` — SOURCE: backend/scratch/test_embed2.py:5-6
2. `contents = ["hello", "world", "test"]` — SOURCE: backend/scratch/test_embed2.py:8
3. **Block 1:** try: `res = client.models.embed_content(model="gemini-embedding-2", contents=contents)`; print embed length or `"no attribute"`; except Exception: print `"embed_content error: {e}"` — SOURCE: backend/scratch/test_embed2.py:9-16
4. **Block 2:** try: `pass`; except Exception: `pass` — SOURCE: backend/scratch/test_embed2.py:18-22 (empty block; placeholder for alternative call method)

No assertions.

### 11.6 scratch/check_st.py

**Type:** Scratch script

**Script-level execution:**
1. `import streamlit as st`
2. try:
   - `print(f"st.html exists: {hasattr(st, 'html')}")` — SOURCE: scratch/check_st.py:3
   - `print(f"st.iframe exists: {hasattr(st, 'iframe')}")` — SOURCE: scratch/check_st.py:4
3. except Exception as e: `print(f"Error: {e}")` — SOURCE: scratch/check_st.py:5-6

No assertions.

### 11.7 scratch/patch_skills.py

**Type:** One-time maintenance script (not a test)

**Script-level execution:**
1. Opens `'backend/skills/regex_detection_skills.py'` and reads its content — SOURCE: scratch/patch_skills.py:6-7
2. Finds string index of `'class CrowdsourcingDetectionSkill(BaseSkill):'` — SOURCE: scratch/patch_skills.py:9
3. Finds string index of `'class LicenseDetectionSkill(BaseSkill):'` — SOURCE: scratch/patch_skills.py:10
4. Finds string index of `'class LimitationsQualityDetectionSkill(BaseSkill):'` — SOURCE: scratch/patch_skills.py:11
5. Constructs `new_content = before_crowd + new_crowd + new_license + after_license`
   - `before_crowd = content[:crowd_start]`
   - `after_license = content[limitations_start:]` (everything FROM LimitationsQualityDetectionSkill onward is preserved)
   - The region between `CrowdsourcingDetectionSkill` and `LimitationsQualityDetectionSkill` is replaced with new implementations of both `CrowdsourcingDetectionSkill` and `LicenseDetectionSkill`
6. Writes `new_content` back to file — SOURCE: scratch/patch_skills.py:104
7. Calls `ast.parse(new_content)` to validate syntax — SOURCE: scratch/patch_skills.py:107
8. Prints `"Done. Syntax OK. Chars: {len(new_content)}"` — SOURCE: scratch/patch_skills.py:108

### 11.8 scratch/repro_hyperparams.py

**Type:** Scratch script for reproducing hyperparameter detection

**Function: `test_hyperparameter_detection()`** — SOURCE: scratch/repro_hyperparams.py:9
- Checks `os.path.exists("paper_cientifico_3_CON_ERRORES.md")`; if False: print `"File ... not found"` and return — SOURCE: scratch/repro_hyperparams.py:11-13
- Reads file with `open(paper_path, "r", encoding="utf-8").read()` — SOURCE: scratch/repro_hyperparams.py:15-16
- Constructs `HyperparameterDetectionSkill()` — SOURCE: scratch/repro_hyperparams.py:18
- Overrides `skill.log_execution` with lambda: `lambda msg, level="info": print(f"[{level.upper()}] {msg}")` — SOURCE: scratch/repro_hyperparams.py:22
- Calls `skill.execute({"paper_text": text})` — SOURCE: scratch/repro_hyperparams.py:25
- Prints JSON-serialized results with `json.dumps(results, indent=2)` — SOURCE: scratch/repro_hyperparams.py:29

No assertions.

**`if __name__ == "__main__"`: calls `test_hyperparameter_detection()`** — SOURCE: scratch/repro_hyperparams.py:31-32

### 11.9 scratch/test_checklist_health.py

**Type:** Scratch assertion script

**Script-level execution:**
1. `from frontend.utils.scoring import get_checklist_health` — SOURCE: scratch/test_checklist_health.py:4
2. Constructs `mock_eval` dict with 16 checklist item keys and their answer/evidence/justification/is_no_justified values — SOURCE: scratch/test_checklist_health.py:6-23
3. Calls `health = get_checklist_health(mock_eval)` — SOURCE: scratch/test_checklist_health.py:25
4. Prints `health["status"]`, `health["pending_count"]`, `health["total"]` — SOURCE: scratch/test_checklist_health.py:26-27
5. Prints items where `item['alert_msg']` is truthy — SOURCE: scratch/test_checklist_health.py:28-30
6. Retrieves `stats_item = next(i for i in health['items'] if i['key'] == 'experiment_statistical_significance')` — SOURCE: scratch/test_checklist_health.py:33
7. Assertions:
   - `assert stats_item['pending_justification'] == True, "Item 7 should be flagged!"` — SOURCE: scratch/test_checklist_health.py:34
   - `assert health['status'] == 'risk', "Should be risk with unjustified No!"` — SOURCE: scratch/test_checklist_health.py:35

**Mock eval — key `experiment_statistical_significance`:** `{'answer': 'No', 'evidence': '', 'justification': '', 'is_no_justified': False}` — SOURCE: scratch/test_checklist_health.py:13

### 11.10 scratch/test_llm_retry.py

**Type:** Unit test with mocks (script-level)

**Setup:** Mocks `google`, `google.genai`, and `streamlit` modules via `sys.modules` — SOURCE: scratch/test_llm_retry.py:7-9

**Function: `test_retry_logic()`** — SOURCE: scratch/test_llm_retry.py:16
- Setup:
  - `client = LLMClient(model_name="test-model")`
  - `mock_gen = MagicMock()`
  - `client.client.models.generate_content = mock_gen`
  - `mock_gen.side_effect = [Exception("503 UNAVAILABLE: High demand"), Exception("503 UNAVAILABLE: High demand"), MagicMock(text="Success response")]`
  - `patch('time.sleep')` as `mock_sleep`
- Action: `response = client.generate("test prompt")`
- Assertions:
  1. `assert mock_gen.call_count == 3`
  2. `assert mock_sleep.call_count == 2`

**Function: `test_final_failure()`** — SOURCE: scratch/test_llm_retry.py:38
- Setup:
  - `client = LLMClient(model_name="test-model")`
  - `mock_gen.side_effect = Exception("503 UNAVAILABLE: High demand")` (always fails)
  - `patch('time.sleep')` as `mock_sleep`
- Action: `client.generate("test prompt")` — expected to raise
- Assertions:
  1. `assert mock_gen.call_count == 6` (1 original + 5 retries)
  2. Exception is raised (assert False if not raised)

**`__main__` block:**
```python
with patch('backend.common.config.GOOGLE_API_KEY', "test-key"):
    with patch('backend.common.config.MODEL_NAME', "test-model"):
        test_retry_logic()
        test_final_failure()
```
`SOURCE: scratch/test_llm_retry.py:59-63`

### 11.11 scratch/test_rag_split.py

**Type:** Scratch script with inline function definition and direct execution

**Function: `get_rag_chunks(paper_text)`** — SOURCE: scratch/test_rag_split.py:3
- DETAIL: described fully in Section 9.5

**Script-level test:**
- Input text `test_text` (multiline string with Title, Abstract, Introduction, Table, Final text sections) — SOURCE: scratch/test_rag_split.py:28-43
- Calls `chunks = get_rag_chunks(test_text)` — SOURCE: scratch/test_rag_split.py:45
- Prints `"Total chunks: {len(chunks)}"` — SOURCE: scratch/test_rag_split.py:46
- Prints each chunk with header — SOURCE: scratch/test_rag_split.py:47-48

No assertions (observation-only script).

### 11.12 tests/test_audit_state.py

**Type:** `unittest.TestCase`

**Imports:** `AuditState`, `ExtractedInfo`, `ChecklistItem` from `backend.common.audit_state` — SOURCE: tests/test_audit_state.py:2

**Test: `test_initialization()`** — SOURCE: tests/test_audit_state.py:5
- Setup: `state = AuditState(paper_text="Test content")`
- Assertions:
  1. `self.assertEqual(state.paper_text, "Test content")`
  2. `self.assertFalse(state.invalid_paper)`
  3. `self.assertEqual(state.execution_time, 0.0)`

**Test: `test_to_frontend_dict()`** — SOURCE: tests/test_audit_state.py:12
- Setup: `state = AuditState(paper_text="Test", evaluation={"claims": {"answer": "Yes"}})`
- Action: `d = state.to_frontend_dict()`
- Assertions:
  1. `self.assertEqual(d["claims"]["answer"], "Yes")`
  2. `self.assertIn("informacion_extraida", d)`
  3. `self.assertIn("metricas", d)`

**Test: `test_extracted_info_nesting()`** — SOURCE: tests/test_audit_state.py:19
- Setup: `info = ExtractedInfo()`
- Assertions:
  1. `self.assertEqual(info.code.repository_url, "NOT FOUND")`
  2. `self.assertEqual(info.hyperparameters.optimizer, "NOT FOUND")`

### 11.13 tests/test_rag_logical_splitter.py

**Type:** Script with assertions (no pytest or unittest)

**Function: `test_rag_logical_splitter()`** — SOURCE: tests/test_rag_logical_splitter.py:7
- Input: `paper_text` (multiline string with Title, Abstract, Introduction, Table, Final word sections) — SOURCE: tests/test_rag_logical_splitter.py:10-25
- Processing (inline, no helper function called):
  1. `paper_text_norm = paper_text.replace('\r\n', '\n')` — SOURCE: tests/test_rag_logical_splitter.py:27
  2. `raw_chunks = re.split(r'\n\n+', paper_text_norm)` — SOURCE: tests/test_rag_logical_splitter.py:28
  3. `chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]` — SOURCE: tests/test_rag_logical_splitter.py:29
- Assertions:
  1. `assert len(chunks) >= 4` — SOURCE: tests/test_rag_logical_splitter.py:36
  2. `assert "| Table 1 |" in chunks[3]` — chunk at index 3 must contain table header — SOURCE: tests/test_rag_logical_splitter.py:37
  3. `assert "Data 1" in chunks[3]` — chunk at index 3 must contain table data — SOURCE: tests/test_rag_logical_splitter.py:38
  4. `assert "Abstract" in chunks[1]` — chunk at index 1 must contain "Abstract" — SOURCE: tests/test_rag_logical_splitter.py:39

### 11.14 tests/test_section_splitter.py

**Type:** Script with assertions

**Function: `test_splitting_logic()`** — SOURCE: tests/test_section_splitter.py:7
- Input: `paper_text` (6 sections, each `# Section N\nContent N.\n`) — SOURCE: tests/test_section_splitter.py:11-23
- Setup:
  - `class MockLLM`: provides `generate(self, prompt)` returning `type('obj', (object,), {'text': '{}'})` — SOURCE: tests/test_section_splitter.py:32-33
  - `skill = InformationExtractionSkill(llm_client=MockLLM())` — SOURCE: tests/test_section_splitter.py:35
  - `class TestSkill(InformationExtractionSkill)`: adds `get_fragments(self, paper_text)` method exposing internal fragment logic — SOURCE: tests/test_section_splitter.py:40-68
  - `test_skill = TestSkill(llm_client=MockLLM())` — SOURCE: tests/test_section_splitter.py:71
- Action: `fragments = test_skill.get_fragments(paper_text)` — SOURCE: tests/test_section_splitter.py:72
- Assertions:
  1. `assert len(fragments) == 4, f"Expected 4 fragments, got {len(fragments)}"` — SOURCE: tests/test_section_splitter.py:75
  2. For each fragment: `assert len(f) > 0` — SOURCE: tests/test_section_splitter.py:79

---

## 12. Implicit Business Rules Encoded in Tests

### BR-TEST-01: Audit result must contain 'claims' key when successful
```
RULE: Successful audit result contains 'claims' key
TRIGGER: When result is returned from audit pipeline and rendered in app.py
CONDITION: resultado.get("claims") is truthy
ACTION IF TRUE: render full UI (audit results, sota, chatbot, download)
ACTION IF FALSE: show "auditoría no generó resultados válidos" error
ERROR: st.error("⚠️ La auditoría no generó resultados válidos."); st.json(resultado)
FIELDS INVOLVED: resultado['claims']
CALLS: render_audit_results, render_sota_analysis, render_chatbot, generate_report
SOURCE: app.py:65-68
```

### BR-TEST-02: Audit result 'error' key triggers error display
```
RULE: If resultado has 'error' key, display audit error message
TRIGGER: After process_uploaded_file completes and sets st.session_state['resultado']
CONDITION: "error" in resultado
ACTION IF TRUE: st.error(f"❌ Error en la auditoría: {resultado['error']}")
ACTION IF FALSE: proceed to next condition check
ERROR: Displayed via st.error
FIELDS INVOLVED: resultado['error']
SOURCE: app.py:60-61
```

### BR-TEST-03: LLM evaluation_error triggers retry advisory
```
RULE: If resultado has 'evaluation_error' key, show LLM error + retry advisory
TRIGGER: After process_uploaded_file completes
CONDITION: "evaluation_error" in resultado
ACTION IF TRUE: st.error("❌ Error del LLM: {resultado['evaluation_error']}"); st.warning("🔄 El modelo está experimentando alta demanda. Intenta nuevamente.")
ACTION IF FALSE: proceed to next condition
ERROR: N/A (displayed in UI)
FIELDS INVOLVED: resultado['evaluation_error']
SOURCE: app.py:62-64
```

### BR-TEST-04: Report filename uses original uploaded file name
```
RULE: Downloaded report filename is derived from uploaded file name with .pdf stripped
TRIGGER: When st.download_button is rendered
CONDITION: always (when claims are present)
ACTION: file_name = f"auditoria_{uploaded_file.name.replace('.pdf', '')}.md"
ERROR: N/A
FIELDS INVOLVED: uploaded_file.name
SOURCE: app.py:77
```

### BR-TEST-05: AuditState frontend dict must expose 'informacion_extraida' and 'metricas'
```
RULE: to_frontend_dict() output always includes informacion_extraida and metricas keys
TRIGGER: On call to AuditState.to_frontend_dict()
CONDITION: always (structural contract)
ACTION IF TRUE: d contains both keys
ACTION IF FALSE: AssertionError in test
ERROR: unittest.AssertionError
FIELDS INVOLVED: d["informacion_extraida"], d["metricas"]
CALLS: AuditState.to_frontend_dict() (CROSS-REFERENCE: backend/common/audit_state.py)
SOURCE: tests/test_audit_state.py:16-18
```

### BR-TEST-06: RAG chunk at index 1 must contain section heading text
```
RULE: Second chunk (index 1) from a paper split by double-newline must contain the Abstract heading
TRIGGER: On RAG split of structured paper
CONDITION: chunks[1] contains string "Abstract"
ACTION IF TRUE: test passes
ACTION IF FALSE: AssertionError
ERROR: AssertionError
FIELDS INVOLVED: chunks[1]
SOURCE: tests/test_rag_logical_splitter.py:39
```

### BR-TEST-07: RAG table rows must remain in same chunk as table header
```
RULE: Markdown table header and data rows separated by single newlines must be in the same chunk
TRIGGER: On RAG split by double-newline
CONDITION: "| Table 1 |" in chunks[3] AND "Data 1" in chunks[3]
ACTION IF TRUE: test passes
ACTION IF FALSE: AssertionError (table was split across chunks)
ERROR: AssertionError
FIELDS INVOLVED: chunks[3]
SOURCE: tests/test_rag_logical_splitter.py:37-38
```

### BR-TEST-08: Section fragmenter must produce 4 fragments from 6 equal sections
```
RULE: 6 equal-length sections produce exactly 4 fragments when fragmented at total_chars/4 target
TRIGGER: On TestSkill.get_fragments(paper_text) with 6 equal-length sections
CONDITION: len(fragments) == 4
ACTION IF TRUE: test passes
ACTION IF FALSE: AssertionError "Expected 4 fragments, got {len(fragments)}"
ERROR: AssertionError
FIELDS INVOLVED: fragments list length
SOURCE: tests/test_section_splitter.py:75
```

---

## 13. Gaps & Cross-References

```
GAP_ID: GAP-cluster_root_tests_scratch_01-001
TYPE: CROSS_REFERENCE
FROM: app.py:34 — process_uploaded_file import
EXPECTS: function process_uploaded_file(uploaded_file: UploadedFile) -> None; must set st.session_state['resultado'] and st.session_state['md_text']
LIKELY_LOCATION: frontend/components/file_uploader.py
IMPACT: HIGH — central processing function; determines all downstream display behavior
SOURCE: app.py:34
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-002
TYPE: CROSS_REFERENCE
FROM: app.py:35 — render_audit_results import
EXPECTS: function render_audit_results(resultado: dict, uploaded_file) -> Any (returns puntuacion used in generate_report)
LIKELY_LOCATION: frontend/components/audit_results.py
IMPACT: HIGH — renders audit output and returns score used for report generation
SOURCE: app.py:35
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-003
TYPE: CROSS_REFERENCE
FROM: app.py:35 — generate_report import
EXPECTS: function generate_report(resultado: dict, uploaded_file, puntuacion: Any) -> bytes or str; returned value is used as data for st.download_button
LIKELY_LOCATION: frontend/components/audit_results.py
IMPACT: HIGH — produces the downloadable audit report
SOURCE: app.py:73
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-004
TYPE: CROSS_REFERENCE
FROM: app.py:36-37 — render_sota_analysis, render_chatbot imports
EXPECTS: render_sota_analysis(md_text: str) -> None; render_chatbot(md_text: str) -> None
LIKELY_LOCATION: frontend/components/sota_section.py, frontend/components/chatbot.py
IMPACT: MEDIUM — secondary display components
SOURCE: app.py:36-37
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-005
TYPE: CROSS_REFERENCE
FROM: app.py:31 — frontend.config imports
EXPECTS: constants TITLE: str, SIDEBAR_IMAGE: str (path or URL), SIDEBAR_DESCRIPTION: str
LIKELY_LOCATION: frontend/config.py
IMPACT: LOW — display constants only
SOURCE: app.py:31
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-006
TYPE: CROSS_REFERENCE
FROM: test_auditor_refactor.py:2 — PaperAuditor import
EXPECTS: class PaperAuditor with methods: __init__(), _preprocess_paper(text: str) -> dict
LIKELY_LOCATION: backend/services/auditor.py
IMPACT: HIGH — core audit service
SOURCE: test_auditor_refactor.py:2
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-007
TYPE: CROSS_REFERENCE
FROM: test_auditor_refactor.py:3 — prompts imports
EXPECTS: functions get_extraction_prompt(text: str, flags: dict) -> str (len > 0); get_evaluation_prompt(info: dict, flags: dict) -> str (len > 0)
LIKELY_LOCATION: backend/common/prompts.py
IMPACT: HIGH — prompt construction for LLM calls
SOURCE: test_auditor_refactor.py:3
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-008
TYPE: CROSS_REFERENCE
FROM: test_auditor_refactor.py:18 — REGEX_PATTERNS import
EXPECTS: module-level variable REGEX_PATTERNS: list or dict with len > 0
LIKELY_LOCATION: backend/services/auditor.py
IMPACT: MEDIUM — regex-based pre-processing patterns
SOURCE: test_auditor_refactor.py:18
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-009
TYPE: CROSS_REFERENCE
FROM: scratch/test_llm_retry.py:14 — LLMClient import
EXPECTS: class LLMClient with constructor LLMClient(model_name: str); method generate(prompt: str) -> object with .text attribute; internal attribute client.models.generate_content (callable); retry logic: max 6 total calls (1 + 5 retries), sleep between retries
LIKELY_LOCATION: backend/common/llm_client.py
IMPACT: HIGH — all LLM calls go through this client; retry count and sleep interval not visible in tests
SOURCE: scratch/test_llm_retry.py:14
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-010
TYPE: CROSS_REFERENCE
FROM: scratch/test_checklist_health.py:4 — get_checklist_health import
EXPECTS: function get_checklist_health(evaluation: dict) -> dict with keys: 'status' (str: 'risk' when any No is unjustified), 'pending_count' (int), 'total' (int), 'items' (list of dicts with keys: 'key', 'label', 'alert_msg', 'pending_justification')
LIKELY_LOCATION: frontend/utils/scoring.py
IMPACT: HIGH — determines checklist risk status displayed in UI
SOURCE: scratch/test_checklist_health.py:4
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-011
TYPE: CROSS_REFERENCE
FROM: tests/test_audit_state.py:2 — AuditState, ExtractedInfo, ChecklistItem imports
EXPECTS: class AuditState(paper_text: str, evaluation: dict = None, invalid_paper: bool = False, execution_time: float = 0.0); method to_frontend_dict() -> dict with keys: evaluation keys, 'informacion_extraida', 'metricas'; class ExtractedInfo with sub-models code (has repository_url defaulting to "NOT FOUND") and hyperparameters (has optimizer defaulting to "NOT FOUND")
LIKELY_LOCATION: backend/common/audit_state.py
IMPACT: HIGH — core data model for audit results
SOURCE: tests/test_audit_state.py:2
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-012
TYPE: CROSS_REFERENCE
FROM: tests/test_section_splitter.py:5 — InformationExtractionSkill import
EXPECTS: class InformationExtractionSkill(llm_client: Any) with internal section-fragmenting logic using re.split(r'\n(?=#+ )', ...) and target = total_chars / 4 with max 3 early fragment boundaries; execute() method
LIKELY_LOCATION: backend/skills/auditor_skills.py
IMPACT: HIGH — core extraction skill; fragmentation algorithm is embedded in execute()
SOURCE: tests/test_section_splitter.py:5
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-013
TYPE: CROSS_REFERENCE
FROM: test_skills_integration.py:12-25 — 12 skill class imports from backend.skills
EXPECTS: module backend/skills/__init__.py exporting: BaseSkill, InformationExtractionSkill, ReproducibilityEvaluationSkill, MetricsCalculationSkill, MetadataAggregationSkill, ConversationalResponseSkill, ContextValidationSkill, ThematicCoverageSkill, QueryGenerationSkill, SemanticScholarSearchSkill, CoverageGapAnalysisSkill, CrossValidationSkill
LIKELY_LOCATION: backend/skills/__init__.py and sub-modules
IMPACT: HIGH — skills architecture foundation
SOURCE: test_skills_integration.py:12-25
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-014
TYPE: CROSS_REFERENCE
FROM: test_skills_integration.py:27-31 — regex detection skill imports
EXPECTS: classes LimitationsQualityDetectionSkill, SoftwareVersionDetectionSkill, HardwareDetailDetectionSkill in backend/skills/regex_detection_skills.py
LIKELY_LOCATION: backend/skills/regex_detection_skills.py
IMPACT: MEDIUM — specialized regex-based detection skills
SOURCE: test_skills_integration.py:27-31
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-015
TYPE: CROSS_REFERENCE
FROM: test_skills_integration.py:130 — SemanticScholarSearchSkill import from sota_skills
EXPECTS: class SemanticScholarSearchSkill in backend/skills/sota_skills.py; execute({'search_queries': []}) returns dict with 'sota_papers' key (value presumably empty list when queries empty)
LIKELY_LOCATION: backend/skills/sota_skills.py
IMPACT: MEDIUM — Semantic Scholar API integration
SOURCE: test_skills_integration.py:130
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-016
TYPE: CROSS_REFERENCE
FROM: test_skills_integration.py:146 — get_logger import
EXPECTS: function get_logger(name: str) -> logger object with .info(msg: str) method
LIKELY_LOCATION: backend/utils/logger.py
IMPACT: LOW — logging utility
SOURCE: test_skills_integration.py:146
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-017
TYPE: CROSS_REFERENCE
FROM: scratch/repro_hyperparams.py:7 — HyperparameterDetectionSkill import
EXPECTS: class HyperparameterDetectionSkill with execute(context: {'paper_text': str}) -> dict; attribute log_execution (callable, replaceable); results serializable as JSON
LIKELY_LOCATION: backend/skills/regex_detection_skills.py
IMPACT: MEDIUM — hyperparameter detection logic not visible in cluster
SOURCE: scratch/repro_hyperparams.py:7
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-018
TYPE: MISSING_SOURCE
FROM: scratch/patch_skills.py:6 — patch target
EXPECTS: file backend/skills/regex_detection_skills.py to contain class strings 'class CrowdsourcingDetectionSkill(BaseSkill):', 'class LicenseDetectionSkill(BaseSkill):', 'class LimitationsQualityDetectionSkill(BaseSkill):' in that order
LIKELY_LOCATION: backend/skills/regex_detection_skills.py
IMPACT: HIGH — patch_skills.py will raise ValueError if these class markers are not found; post-patch state of file is the authoritative version
SOURCE: scratch/patch_skills.py:9-11
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-019
TYPE: MISSING_SOURCE
FROM: scratch/repro_hyperparams.py:11 — file dependency
EXPECTS: file "paper_cientifico_3_CON_ERRORES.md" to exist in current working directory; UTF-8 encoded
LIKELY_LOCATION: Project root or data directory — not tracked in .gitignore? (*.md is in .gitignore)
IMPACT: MEDIUM — script silently skips if file missing
SOURCE: scratch/repro_hyperparams.py:11-13
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-020
TYPE: CONFIG_DEPENDENCY
FROM: scratch/test_llm_retry.py:60-61 — patched config
EXPECTS: backend/common/config.py module with attributes GOOGLE_API_KEY: str and MODEL_NAME: str (patchable with unittest.mock.patch)
LIKELY_LOCATION: backend/common/config.py
IMPACT: HIGH — LLMClient initialization depends on these config values
SOURCE: scratch/test_llm_retry.py:60-61
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-021
TYPE: EXTERNAL_SYSTEM
FROM: pdf_to_md.py:41 — pymupdf4llm.to_markdown call
EXPECTS: function pymupdf4llm.to_markdown(pdf_path: str) -> str (Markdown text); handles all PDF parsing internally
LIKELY_LOCATION: pymupdf4llm third-party library (not in requirements.txt — gap: missing from requirements.txt)
IMPACT: HIGH — entire pdf_to_md.py depends on this library
SOURCE: pdf_to_md.py:41
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-022
TYPE: MISSING_SOURCE
FROM: md_to_pdf.py:16 — HAS_MARKDOWN flag
EXPECTS: HAS_MARKDOWN=True branch: markdown2 library usage in parse_markdown_to_elements; actual usage of HAS_MARKDOWN flag to select parsing strategy
LIKELY_LOCATION: md_to_pdf.py (same file) — HAS_MARKDOWN is set but never read in parse_markdown_to_elements; the enhanced parsing via markdown2 is apparently not implemented
IMPACT: MEDIUM — all Markdown parsing uses the basic line-by-line parser regardless of markdown2 availability
SOURCE: md_to_pdf.py:16-20
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-023
TYPE: CROSS_REFERENCE
FROM: app.py:32 — apply_custom_styles import
EXPECTS: function apply_custom_styles() -> None (injects CSS via st.markdown)
LIKELY_LOCATION: frontend/styles/custom_css.py
IMPACT: LOW — styling only
SOURCE: app.py:32
```

```
GAP_ID: GAP-cluster_root_tests_scratch_01-024
TYPE: CROSS_REFERENCE
FROM: app.py:33 — initialize_session_state import
EXPECTS: function initialize_session_state() -> None (sets default values in st.session_state including 'resultado' and 'md_text')
LIKELY_LOCATION: frontend/utils/session_state.py
IMPACT: MEDIUM — ensures session_state keys exist before access
SOURCE: app.py:33
```
