---
validator_id: val_forward_frontend
validator_type: forward_coverage
target_specs: [02_functional_frontend.md]
forward_coverage_pct: 92
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 8
coverage_gaps: 1
depth_gaps: 2
spec_consistency_issues: 0
total_issues: 11
overall_status: needs_review
---

## Summary

`02_functional_frontend.md` is a thorough and well-structured specification of the Streamlit frontend, covering all seven source files (`app.py`, `file_uploader.py`, `audit_results.py`, `audit_results.py/_build_table_html`, `scoring.py`, `sota_section.py`, `chatbot.py`, `gauge_chart.py`, `session_state.py`, `custom_css.py`, `config.py`). The vast majority of claims—widget labels, session-state key names and defaults, branching conditions, color hex codes, threshold values, and function signatures—verify exactly against source code. Eight fidelity issues were found, centered on three root causes: (1) the spec conflates `frontend/app.py` with the root `app.py` in two places (sidebar step ordering and the `process_uploaded_file` call pattern), (2) the download filename in `frontend/app.py` contains an extra `_neurips_` prefix omitted from the spec, and (3) two minor source-line discrepancies in `file_uploader.py`. These issues are correctable without structural revision to the spec. Overall status is **needs_review**.

---

## Forward Coverage (Specs → Source)

| Spec Element | Component | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| `frontend/app.py` is entry point (76 lines) | app.py | frontend/app.py | PARTIAL | FIDELITY_ISSUE | Spec says 74 lines; actual `wc -l` = 76 |
| `st.set_page_config(page_title="NeurIPS 2026 Checklist Auditor", layout="wide", page_icon="🔬")` | app.py | frontend/app.py:6-10 | YES | VERIFIED | Exact match |
| `IMPORTANTE: configure_page() debe ser lo primero` comment | app.py | frontend/app.py:5 | YES | VERIFIED | Comment present at line 5 |
| Env vars set before Streamlit import (`TRANSFORMERS_VERBOSITY`, `TOKENIZERS_PARALLELISM`, `ANONYMIZED_TELEMETRY`, `OTEL_SDK_DISABLED`) | app.py | root/app.py:13-22 | YES | VERIFIED | These are in root `app.py`, not `frontend/app.py`; spec correctly cites `app.py:13-22` which matches root |
| 3 `warnings.filterwarnings("ignore", ...)` calls | app.py | root/app.py:15-17 | YES | VERIFIED | Present at root/app.py:15-17 |
| `logging.getLogger("transformers").setLevel(logging.ERROR)` | app.py | root/app.py:18 | YES | VERIFIED | Line 18 of root app.py |
| Step 2: `apply_custom_styles()` called unconditionally, SOURCE app.py:21 | app.py | frontend/app.py:21 | YES | VERIFIED | `apply_custom_styles()` at line 21 |
| Step 3: `initialize_session_state()` called unconditionally, SOURCE app.py:22 | app.py | frontend/app.py:22 | YES | VERIFIED | `initialize_session_state()` at line 22 |
| Step 4 sidebar placed as Step 4 (between init and page title) | app.py | frontend/app.py:73 | PARTIAL | FIDELITY_ISSUE | Sidebar code is at line 73, AFTER page title (line 25). Spec claims top-to-bottom order with sidebar at Step 4—impossible given line numbers. Sidebar executes after all main content. Source line 73 is correct, but step ordering is wrong. |
| Sidebar: `st.image(SIDEBAR_IMAGE, width=150)` | app.py | frontend/app.py:74 | YES | VERIFIED | Exact match |
| Sidebar: `st.markdown("### Sobre el TFG")` | app.py | frontend/app.py:75 | YES | VERIFIED | Exact match |
| Sidebar: `st.write(SIDEBAR_DESCRIPTION)` | app.py | frontend/app.py:76 | YES | VERIFIED | Exact match |
| Step 5: `st.title(TITLE)` at app.py:25 | app.py | frontend/app.py:25 | YES | VERIFIED | `st.title(TITLE)` at line 25 |
| Step 5: `st.markdown("---")` at app.py:26 | app.py | frontend/app.py:26 | YES | VERIFIED | Exact match |
| Step 5: `st.button("🔄 Limpiar y subir nuevo archivo")` | app.py | frontend/app.py:29 | YES | VERIFIED | Exact label match |
| Limpiar: deletes ALL session_state keys via `del st.session_state[key]` loop | app.py | frontend/app.py:30-31 | YES | VERIFIED | `for key in list(st.session_state.keys()): del st.session_state[key]` |
| Limpiar: calls `st.rerun()` after deletion | app.py | frontend/app.py:32 | YES | VERIFIED | Exact match |
| Step 6: `st.file_uploader("Sube el PDF del artículo científico", type=["pdf", "txt", "md"])` | app.py | frontend/app.py:34 | YES | VERIFIED | Exact label and types match |
| Steps 7a+7b: `process_uploaded_file(uploaded_file)` then separate `st.session_state.get('resultado')` / `st.session_state.get('md_text')` reads | app.py | frontend/app.py:36 | PARTIAL | FIDELITY_ISSUE | `frontend/app.py` uses `md_text, resultado = process_uploaded_file(uploaded_file)` (direct return capture). The 7a+7b two-step pattern (call with no capture, then session_state reads) is from root `app.py`, not `frontend/app.py`. |
| Step 7c: `"error" == "INVALID_PAPER_TYPE"` → `st.error(f"❌ Paper no válido: ...")` | app.py | frontend/app.py:40-42 | YES | VERIFIED | Exact condition and error message match |
| Step 7c: non-INVALID_PAPER_TYPE error → `st.error(f"❌ Error en la auditoría: {err}")` | app.py | frontend/app.py:43-44 | YES | VERIFIED | Exact match |
| Step 7c: `"evaluation_error" in resultado` → 3-message block (error, warning, info) | app.py | frontend/app.py:45-48 | YES | VERIFIED | All 3 messages match including tip text |
| Step 7d: `render_audit_results(resultado, uploaded_file)` on SUCCESS PATH | app.py | frontend/app.py:50 | YES | VERIFIED | Call is correct |
| Step 7d: return stored as `puntuacion` | app.py | frontend/app.py:50 | PARTIAL | FIDELITY_ISSUE | Variable is named `health` in `frontend/app.py`, not `puntuacion`. `puntuacion` is the variable name used in root `app.py`. |
| Step 7e: `render_sota_analysis(md_text)` after render_audit_results | app.py | frontend/app.py:51 | YES | VERIFIED | Exact match |
| Step 7f: `render_chatbot(md_text)` after render_sota_analysis | app.py | frontend/app.py:52 | YES | VERIFIED | Exact match |
| Step 7g: download button label `"📥 Descargar Informe Completo (.md)"` | app.py | frontend/app.py:62 | YES | VERIFIED | Exact match |
| Step 7g: `generate_report(resultado, uploaded_file, puntuacion)` | app.py | frontend/app.py:60 | YES | VERIFIED | Called as `generate_report(resultado, uploaded_file, health)` — functionally correct |
| Step 7g: `file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"` | app.py | frontend/app.py:63 | PARTIAL | FIDELITY_ISSUE | Actual filename is `f"auditoria_neurips_{...}.md"` — spec omits the `_neurips_` prefix |
| Step 7g: `mime="text/markdown"` | app.py | frontend/app.py:64 | YES | VERIFIED | Exact match |
| Fallback `elif resultado:` → `st.error("⚠️ La auditoría no generó resultados válidos.")` | app.py | frontend/app.py:65-66 | YES | VERIFIED | Exact match |
| Fallback `else:` → `st.warning("⚠️ No hay resultado disponible.")` | app.py | frontend/app.py:67-68 | YES | VERIFIED | Exact match |
| `initialize_session_state` uses `if "key" not in st.session_state` guard | session_state.py | session_state.py:9,12,15,18,21 | YES | VERIFIED | Each key guarded; function is idempotent |
| `resultado` initialized to `None` | session_state.py | session_state.py:9-10 | YES | VERIFIED | `st.session_state.resultado = None` |
| `auditor` initialized to `PaperAuditor()` | session_state.py | session_state.py:12-13 | YES | VERIFIED | Exact match |
| `chatbot` initialized to `PaperChatbot()` | session_state.py | session_state.py:15-16 | YES | VERIFIED | Exact match |
| `sota_analyzer` initialized to `SotaAnalyzer()` | session_state.py | session_state.py:18-19 | YES | VERIFIED | Exact match |
| `messages` initialized to `[]` | session_state.py | session_state.py:21-22 | YES | VERIFIED | Exact match |
| `archivo_actual` set at file_uploader.py:19 (uploaded_file.name) | file_uploader.py | file_uploader.py:19 | YES | VERIFIED | Line 19: `st.session_state.archivo_actual = uploaded_file.name` |
| `file_hash` set at file_uploader.py:20 (MD5 hex) | file_uploader.py | file_uploader.py:20 | YES | VERIFIED | Line 20: `st.session_state.file_hash = file_hash` |
| `md_text` set at file_uploader.py:36 (PDF) or file_uploader.py:39 (TXT/MD) | file_uploader.py | file_uploader.py:36,39 | YES | VERIFIED | Lines 36 and 39 exact |
| MD5 hash computed via `hashlib.md5(file_content).hexdigest()` (lines 11-12) | file_uploader.py | file_uploader.py:11-12 | YES | VERIFIED | `file_content = uploaded_file.getvalue()` at line 11; md5 at line 12 |
| Dedup condition: `archivo_actual` not in state OR name changed OR hash changed (lines 15-17) | file_uploader.py | file_uploader.py:15-17 | YES | VERIFIED | Three-part OR condition matches exactly |
| `messages` reset to `[]` on new file at line 21 | file_uploader.py | file_uploader.py:21 | YES | VERIFIED | `st.session_state.messages = []` at line 21 |
| `os.makedirs("temp")` if `not os.path.exists("temp")` at lines 23-24 | file_uploader.py | file_uploader.py:23-24 | YES | VERIFIED | Exact match |
| `temp_path = os.path.join("temp", uploaded_file.name)` | file_uploader.py | file_uploader.py:26 | YES | VERIFIED | Line 26 |
| Extension detection: spec says `rsplit('.', 1)[-1].lower()` at lines 35-42 | file_uploader.py | file_uploader.py:27 | PARTIAL | FIDELITY_ISSUE | Actual code: `uploaded_file.name.split('.')[-1].lower()` (no `rsplit`, line 27). Functionally equivalent but wrong method name; also the detection happens at line 27 not 35. |
| File bytes written to temp_path; spec says lines 26-28 | file_uploader.py | file_uploader.py:30-31 | PARTIAL | FIDELITY_ISSUE | Write block is `with open(temp_path, "wb") as f: f.write(file_content)` at lines 30-31, not 26-28. Line numbers are off by 4. |
| `st.spinner("📂 Extrayendo texto...")` wrapping PDF/TXT dispatch | file_uploader.py | file_uploader.py:34 | YES | VERIFIED | `with st.spinner(...)` at line 34 |
| PDF branch: `st.session_state.md_text = convert_pdf_to_markdown(temp_path)` | file_uploader.py | file_uploader.py:35-36 | YES | VERIFIED | Exact match |
| TXT/MD branch: open with `'r', encoding='utf-8'` and read | file_uploader.py | file_uploader.py:37-39 | YES | VERIFIED | Exact match |
| Unsupported extension: `st.error(...)` then `return None, {'error': ...}` | file_uploader.py | file_uploader.py:41-42 | YES | VERIFIED | Exact match |
| `st.status("🧠 Analizando el documento...", expanded=True) as status` at line 45 | file_uploader.py | file_uploader.py:45 | YES | VERIFIED | Exact match |
| `update_status(msg)` callback using `st.write(msg)` at lines 46-47 | file_uploader.py | file_uploader.py:46-47 | YES | VERIFIED | Exact match |
| `st.session_state.auditor.audit(st.session_state.md_text, status_callback=update_status)` at lines 49-52 | file_uploader.py | file_uploader.py:49-52 | YES | VERIFIED | Exact match |
| Saturation detection strings: `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` | file_uploader.py | file_uploader.py:58 | YES | VERIFIED | Exact list match |
| Saturation: `status.update(label="⚠️ IA Saturada (Alta demanda)", state="error", expanded=True)` | file_uploader.py | file_uploader.py:60 | YES | VERIFIED | Exact match |
| Saturation: `st.error("### ⚠️ El servicio de IA está saturado")` | file_uploader.py | file_uploader.py:61 | YES | VERIFIED | Exact match |
| Saturation: 2-column layout with "Reintentar ahora" and "Cancelar ejecución" buttons | file_uploader.py | file_uploader.py:66-75 | YES | VERIFIED | Both buttons present with exact labels |
| "Reintentar ahora" → `st.rerun()` | file_uploader.py | file_uploader.py:69 | YES | VERIFIED | Exact match |
| "Cancelar ejecución" → set `resultado = {"error": "Ejecución cancelada..."}` → `st.stop()` | file_uploader.py | file_uploader.py:71-73 | YES | VERIFIED | Exact match |
| Saturation: `st.stop()` to halt normal flow | file_uploader.py | file_uploader.py:75 | YES | VERIFIED | `st.stop()` present |
| Non-saturation error: `status.update(label="❌ La auditoría ha fallado", ...)` | file_uploader.py | file_uploader.py:77 | YES | VERIFIED | Exact match |
| Non-saturation: `st.error(f"❌ Error crítico: {error_msg}")` | file_uploader.py | file_uploader.py:78 | YES | VERIFIED | Exact match |
| Non-saturation: `os.remove(temp_path)` if exists, then `st.stop()` | file_uploader.py | file_uploader.py:80-82 | YES | VERIFIED | Guard check + remove + stop |
| Success: `status.update(label="✅ Análisis completado", state="complete", expanded=False)` | file_uploader.py | file_uploader.py:84 | YES | VERIFIED | Exact match |
| `st.success("✅ Análisis completado")` after status block | file_uploader.py | file_uploader.py:87 | YES | VERIFIED | Exact match |
| Temp file deleted with `os.path.exists` guard after processing | file_uploader.py | file_uploader.py:89-90 | YES | VERIFIED | `if os.path.exists(temp_path): os.remove(temp_path)` |
| Return `(md_text, resultado)` from session_state | file_uploader.py | file_uploader.py:93-96 | YES | VERIFIED | Returns `(st.session_state.get('md_text', ''), st.session_state.get('resultado', {}))` |
| `st.success("Auditoria Finalizada")` at audit_results.py:92 | audit_results.py | audit_results.py:92 | YES | VERIFIED | First line of `render_audit_results` body |
| `health = get_checklist_health(resultado)` at audit_results.py:94 | audit_results.py | audit_results.py:94 | YES | VERIFIED | Exact match |
| `st.header("Veredicto del Checklist NeurIPS 2026")` | audit_results.py | audit_results.py:100 | YES | VERIFIED | Exact match |
| "valid" → `background:#064e3b` div with "Checklist Valido" text | audit_results.py | audit_results.py:102-109 | YES | VERIFIED | Exact background color and text |
| "risk" → `background:#7f1d1d` div with `f"{pending} de {total} item(s)..."` | audit_results.py | audit_results.py:111-117 | YES | VERIFIED | Exact match |
| 4-column metrics: Yes, No, N/A, Tiempo | audit_results.py | audit_results.py:121-133 | YES | VERIFIED | All four `st.metric` calls verified |
| `tiempo = resultado.get("metricas", {}).get("tiempo_segundos", "N/A")` | audit_results.py | audit_results.py:130 | YES | VERIFIED | Exact match |
| RAG Ficha Técnica conditional on `extracted_hyperparameters_hybrid` | audit_results.py | audit_results.py:136 | YES | VERIFIED | `if rag_data:` |
| RAG fields: optimizer, learning_rate, batch_size, epochs, warmup_steps, weight_decay, hardware, random_seed | audit_results.py | audit_results.py:143-163 | YES | VERIFIED | All 8 keys present; random_seed conditional confirmed |
| `st.header("Tabla de Cumplimiento NeurIPS 2026")` | audit_results.py | audit_results.py:167 | YES | VERIFIED | Exact match |
| `st.html(table_html)` render | audit_results.py | audit_results.py:175 | YES | VERIFIED | Exact match |
| `_build_table_html` row_bg: pending_justification → `"#450a0a"` | audit_results.py | audit_results.py:18-20 | YES | VERIFIED | Exact color |
| `_build_table_html` row_bg: missing_evidence OR alert_msg → `"#452e0a"` | audit_results.py | audit_results.py:22-24 | YES | VERIFIED | Exact color |
| `_build_table_html` row_bg: yes → `"#064e3b"` | audit_results.py | audit_results.py:26-27 | YES | VERIFIED | Exact color |
| `_build_table_html` row_bg: other → `"#111827"` | audit_results.py | audit_results.py:29 | YES | VERIFIED | Exact color |
| Badge Yes: `background:#065f46;color:#6ee7b7` | audit_results.py | audit_results.py:10-11 | YES | VERIFIED | Exact colors and text "Yes" |
| Badge No: `background:#7f1d1d;color:#fca5a5` | audit_results.py | audit_results.py:12-13 | YES | VERIFIED | Exact colors and text "No" |
| Badge N/A: `background:#1e3a5f;color:#93c5fd` | audit_results.py | audit_results.py:14-15 | YES | VERIFIED | Exact colors and text "N/A" |
| Evidence text: `"<span ...>{evidence_text}</span>"` vs `"<em ...>No disponible</em>"` | audit_results.py | audit_results.py:48 | YES | VERIFIED | Exact HTML structure |
| Alert pending_justification: `&#9888; Sin justificacion del autor &mdash; Riesgo de Desk Reject` | audit_results.py | audit_results.py:52-53 | YES | VERIFIED | Exact HTML text |
| Alert missing_evidence: `&#9888; Respuesta Yes sin evidencia de seccion del paper` | audit_results.py | audit_results.py:54-55 | YES | VERIFIED | Exact text |
| Crowdsourcing HTML alert trigger: `"compensacion"` or `"etica"` in alert_msg | audit_results.py | audit_results.py:57-58 | YES | VERIFIED | Exact condition |
| Table HTML: 4-column headers (#, Item del Checklist, Respuesta, Evidencia / Justificacion) | audit_results.py | audit_results.py:69-87 | YES | VERIFIED | Exact header labels |
| 16 CHECKLIST_KEYS in correct order | scoring.py | scoring.py:8-23 | YES | VERIFIED | All 16 keys in declared order |
| 16 CHECKLIST_LABELS with exact strings (e.g., "1. Claims", "3. Theory, Assumptions & Proofs") | scoring.py | scoring.py:17-32 | YES | VERIFIED | All 16 labels exact |
| `get_checklist_health` early-exit returns `{"status":"risk","items":[],"pending_count":0,"total":0}` | scoring.py | scoring.py:56-62 | YES | VERIFIED | Matches exactly |
| `is_no_justified` string normalisation: `is_no_justified_raw.lower() == "true"` | scoring.py | scoring.py:73-77 | YES | VERIFIED | Exact pattern |
| missing_evidence: yes + no evidence + no justification → pending_count++ | scoring.py | scoring.py:84-89 | YES | VERIFIED | Exact condition |
| pending_justification: no + (not is_no_justified OR not justification) → pending_count++ | scoring.py | scoring.py:90-95 | YES | VERIFIED | Exact condition |
| N/A: no risk flagged when no justification/evidence | scoring.py | scoring.py:101-105 | YES | VERIFIED | `pass` statement present |
| crowdsourcing special case appends compensation alert when `not is_no_justified` | scoring.py | scoring.py:98-99 | YES | VERIFIED | Inside `elif "no" in answer_norm:` block; condition confirmed |
| `display_evidence = evidence if evidence else (justification if justification else "—")` | scoring.py | scoring.py:108 | YES | VERIFIED | Exact logic |
| `status = "valid" if pending_count == 0 else "risk"` | scoring.py | scoring.py:122-123 | YES | VERIFIED | Exact |
| Return dict keys: status, items, pending_count, total | scoring.py | scoring.py:122-127 | YES | VERIFIED | Exact structure |
| `generate_report` signature and default health=None | audit_results.py | audit_results.py:287 | YES | VERIFIED | `def generate_report(resultado, uploaded_file, health=None)` |
| Report template header: `# NeurIPS 2026 Checklist Audit Report` | audit_results.py | audit_results.py:295 | YES | VERIFIED | Exact match |
| Report rows: 16 items with note logic (`[RIESGO: sin justificacion]` / `[RIESGO: sin evidencia]`) | audit_results.py | audit_results.py:304-313 | YES | VERIFIED | Exact note strings |
| `render_sota_analysis` renders `st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")` | sota_section.py | sota_section.py:5 | YES | VERIFIED | Exact match |
| Button "Ejecutar Análisis de Literatura Reciente" | sota_section.py | sota_section.py:7 | YES | VERIFIED | Exact label |
| `st.spinner("Conectando con Semantic Scholar y validando bibliografía...")` | sota_section.py | sota_section.py:8 | YES | VERIFIED | Exact text |
| `st.session_state.sota_analyzer.analyze_sota(md_text)` | sota_section.py | sota_section.py:9 | YES | VERIFIED | Exact call |
| SOTA success: `st.success("Análisis completado")` + conclusion + papers logic | sota_section.py | sota_section.py:11-27 | YES | VERIFIED | All branches match |
| SOTA error: `st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', ...)}")` | sota_section.py | sota_section.py:29 | YES | VERIFIED | Exact match |
| `_render_missing_papers`: authors_display lambda (x[:2] join + et al. if len > 2) | sota_section.py | sota_section.py:33-36 | YES | VERIFIED | Exact lambda logic |
| Column rename: `titulo→title`, `año→year`, `citas→citationCount` | sota_section.py | sota_section.py:38 | YES | VERIFIED | Exact rename mapping |
| Fuzzy match for `es_omitido` (bidirectional substring) | sota_section.py | sota_section.py:42-47 | YES | VERIFIED | Both `omitido in titulo_lower` and `titulo_lower in omitido` |
| `es_posterior` logic: "✅ Sí" / "❌ No" / "?" | sota_section.py | sota_section.py:58-61 | YES | VERIFIED | Exact strings |
| `st.dataframe` with column_config for all 8 columns | sota_section.py | sota_section.py:70-84 | YES | VERIFIED | All 8 columns and configs present |
| Year caption / no-year warning | sota_section.py | sota_section.py:86-89 | YES | VERIFIED | Exact text |
| `render_chatbot` header: `st.header("💬 Pregunta al Revisor")` | chatbot.py | chatbot.py:6 | YES | VERIFIED | Exact match |
| Messages rendered with `st.chat_message(message["role"])` + `st.markdown(message["content"])` | chatbot.py | chatbot.py:9-11 | YES | VERIFIED | Exact pattern |
| `st.text_input("Escribe tu pregunta:", key="chat_input", placeholder=...)` | chatbot.py | chatbot.py:13-17 | YES | VERIFIED | Exact match including placeholder text |
| `st.button("Enviar", key="send_button")` | chatbot.py | chatbot.py:19 | YES | VERIFIED | Exact match |
| Submit guard: button AND non-empty prompt | chatbot.py | chatbot.py:19 | YES | VERIFIED | `if st.button(...) and prompt_usuario:` |
| Append `{"role": "user", "content": prompt_usuario}` to messages | chatbot.py | chatbot.py:20 | YES | VERIFIED | Exact dict structure |
| `history_str` from `messages[-4:]` with role:content format | chatbot.py | chatbot.py:22 | YES | VERIFIED | Exact slice and format |
| `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)` | chatbot.py | chatbot.py:25 | YES | VERIFIED | Exact call signature |
| Append `{"role": "assistant", "content": respuesta_ia}` | chatbot.py | chatbot.py:27 | YES | VERIFIED | Exact dict structure |
| `st.rerun()` after assistant message appended | chatbot.py | chatbot.py:28 | YES | VERIFIED | Exact match |
| GaugeChart 6 tiers: Strong Accept / Accept / Borderline / Weak Reject / Reject / Strong Reject | gauge_chart.py | gauge_chart.py:14-31 | YES | VERIFIED | All 6 labels exact |
| Tier color #00aa00 (Strong Accept ≥ 87.5) | gauge_chart.py | gauge_chart.py:15 | YES | VERIFIED | Exact hex |
| Tier color #00cc44 (Accept ≥ 75) | gauge_chart.py | gauge_chart.py:18 | YES | VERIFIED | Exact hex |
| Tier color #ffcc00 (Borderline ≥ 62.5) | gauge_chart.py | gauge_chart.py:21 | YES | VERIFIED | Exact hex |
| Tier color #ff9900 (Weak Reject ≥ 50) | gauge_chart.py | gauge_chart.py:24 | YES | VERIFIED | Exact hex |
| Tier color #ff4b4b (Reject ≥ 25) | gauge_chart.py | gauge_chart.py:27 | YES | VERIFIED | Exact hex |
| Tier color #cc0000 (Strong Reject < 25) | gauge_chart.py | gauge_chart.py:30 | YES | VERIFIED | Exact hex |
| Threshold line at value=62.5, color="red", width=4 | gauge_chart.py | gauge_chart.py:57-61 | YES | VERIFIED | `'value': 62.5` and `{'color': "red", 'width': 4}` |
| Gauge layout: height=300, margins l=10/r=10/t=50/b=25, paper_bgcolor transparent, font="#E5E7EB" | gauge_chart.py | gauge_chart.py:63-69 | YES | VERIFIED | All layout params exact |
| Custom CSS: `.stApp { background-color: #374151 !important }` | custom_css.py | custom_css.py:7-9 | YES | VERIFIED | Exact |
| CSS: `#MainMenu { visibility: hidden }` | custom_css.py | custom_css.py:12 | YES | VERIFIED | Exact |
| CSS: `footer { visibility: hidden }` | custom_css.py | custom_css.py:13 | YES | VERIFIED | Exact |
| CSS: `header { background-color: transparent !important }` | custom_css.py | custom_css.py:14 | YES | VERIFIED | Exact |
| CSS: `[data-testid="stTable"]` dark bg + rounded corners | custom_css.py | custom_css.py:16-20 | YES | VERIFIED | `#2d3436`, `15px`, `5px` |
| CSS: `th` styling (white bold text, `#3d4446` bg) | custom_css.py | custom_css.py:28-36 | YES | VERIFIED | All properties match |
| CSS: `tbody th` styling | custom_css.py | custom_css.py:44-49 | YES | VERIFIED | Exact |
| CSS: `td` styling (`#E2E8F0`, 13.5px, transparent bg) | custom_css.py | custom_css.py:55-62 | YES | VERIFIED | All properties match |
| CSS: `[data-testid="stPlotlyChart"]` dark bg + rounded corners | custom_css.py | custom_css.py:68-72 | YES | VERIFIED | `#2d3436`, `15px`, `10px` |
| `apply_custom_styles()` calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)` | custom_css.py | custom_css.py:75-76 | YES | VERIFIED | Exact |
| `TITLE = "💻 Auditor de Papers en Ciencias de la Computación"` | config.py | config.py:3 | YES | VERIFIED | Exact |
| `SIDEBAR_IMAGE` = ACM logo Wikipedia URL | config.py | config.py:4 | YES | VERIFIED | Exact URL |
| `SIDEBAR_DESCRIPTION` text | config.py | config.py:5 | YES | VERIFIED | Exact |

---

## Fidelity Issues

**FI-01 — `frontend/app.py` line count wrong**
- ELEMENT: "The application entry point is `frontend/app.py` (74 lines)"
- SOURCE CITED: extracted_frontend_01.md §4.2 Top-level rendering order
- REASON: `wc -l frontend/app.py` = 76. Spec claims 74. Off by 2.

**FI-02 — Sidebar step ordering contradicts line numbers**
- ELEMENT: "Step 4 — Sidebar render ... TRIGGER: Executed as part of app.py sidebar block; SOURCE: app.py:73-76"
- SOURCE CITED: app.py:73-76
- REASON: Spec explicitly claims "All steps execute on every Streamlit rerun, top-to-bottom, in the order documented below," then places Sidebar as Step 4 between `initialize_session_state` (Step 3, line 22) and page title (Step 5, line 25). But the sidebar block is at lines 73-76 of `frontend/app.py`—well after page title (line 25). The top-to-bottom order is Step 5 → Step 6 → Step 7 → Sidebar (line 73). The source line citation is correct, but the step ordering is wrong.

**FI-03 — Steps 7a+7b call pattern mismatch**
- ELEMENT: "7a. process_uploaded_file(uploaded_file)" then "7b. resultado = st.session_state.get('resultado'); md_text = st.session_state.get('md_text')"
- SOURCE CITED: app.py:37-70
- REASON: In `frontend/app.py` the return value is captured directly: `md_text, resultado = process_uploaded_file(uploaded_file)` (line 36). The two-step pattern described (call without capture, then session_state reads) is from root `app.py`, not `frontend/app.py`. Source lines 37-70 of root `app.py` match this pattern, but the spec's stated entry point is `frontend/app.py`.

**FI-04 — Variable name `puntuacion` vs `health`**
- ELEMENT: "puntuacion = render_audit_results(resultado, uploaded_file)"
- SOURCE CITED: app.py:52 / app.py:66
- REASON: In `frontend/app.py`, `render_audit_results` return value is assigned to variable `health` (line 50), not `puntuacion`. The name `puntuacion` is used in root `app.py`. Downstream references in Step 7g ("generate_report(resultado, uploaded_file, puntuacion)") inherit this wrong name.

**FI-05 — Download filename missing `_neurips_` prefix**
- ELEMENT: `file_name=f"auditoria_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"`
- SOURCE CITED: extracted_frontend_01.md §10.8 / §4.2, app.py:57-65
- REASON: `frontend/app.py` line 63 generates `f"auditoria_neurips_{uploaded_file.name.replace('.pdf', '').replace('.md', '')}.md"`. The spec omits `_neurips_`. Root `app.py` (line ~75) uses `auditoria_` without `_neurips_`. The `frontend/app.py` version, which is the documented entry point, has the `_neurips_` prefix.

**FI-06 — Extension detection method: `rsplit` vs `split`**
- ELEMENT: `file_extension = uploaded_file.name.rsplit('.', 1)[-1].lower()` — SOURCE: file_uploader.py:35-42
- SOURCE CITED: file_uploader.py:35-42
- REASON: Actual code at line 27 uses `uploaded_file.name.split('.')[-1].lower()` (no `rsplit`, no limit). The method name difference is minor (functionally equivalent for single-extension files), but the line number cited (35-42) is wrong—extension detection is at line 27, while lines 35-42 contain the dispatch logic.

**FI-07 — File write line numbers off by 4**
- ELEMENT: "Write uploaded_file bytes to temp_path SOURCE: file_uploader.py:26-28"
- SOURCE CITED: file_uploader.py:26-28
- REASON: The write block (`with open(temp_path, "wb") as f: f.write(file_content)`) is at lines 30-31, not 26-28. Lines 26-28 are `temp_path = os.path.join(...)`, `file_extension = ...`, and a blank line.

**FI-08 — Env var setup attributed to `frontend/app.py` bootstrap but lives in root `app.py`**
- ELEMENT: Step 1 note: "before any Streamlit import, app.py sets the following environment variables … SOURCE: extracted_root_tests_scratch_01.md §3.1, app.py:13-22"
- SOURCE CITED: app.py:13-22
- REASON: `frontend/app.py` contains no `os.environ` or `warnings.filterwarnings` calls. These env vars are in the root `app.py` at lines 13-22. The spec correctly cites `app.py:13-22` (which matches root `app.py`), but describing them as part of `frontend/app.py`'s bootstrap sequence is misleading. The root `app.py` is a separate 88-line file that imports and calls the frontend components; `frontend/app.py` is a self-contained 76-line module.

---

## Coverage Gaps

**CG-01 — Root `app.py` (88 lines) not documented as a distinct module**

Root `TFG.-llm-paper-auditor-multimodels/app.py` (88 lines) is an alternate application entry point that imports from `frontend.*` and has a different structure: it does not use `process_uploaded_file`'s return value directly, uses `puntuacion` variable name, uses `page_title="Nature Auditor Pro"`, and has a different download filename. This file has significant logic (88 LOC) and is listed in `inventory.json` as a top-level file. The spec does not clearly identify it as a separate file, leading to conflation in several descriptions (FI-03, FI-04, FI-05, FI-08). The spec should document both entry points or explicitly state which is canonical.

---

## Depth Gaps

**DG-01 — Step 7g download section missing `st.markdown("---")` and `st.subheader`**

The spec documents Step 7g as just `generate_report(...)` + `st.download_button(...)`. Actual `frontend/app.py` lines 56-58 add `st.markdown("---")` and `st.subheader("📄 Descargar Informe")` before the download button. These are rendered UI elements that are absent from the spec.

**DG-02 — Chatbot section missing `st.caption` after header**

The spec documents `st.header("💬 Pregunta al Revisor")` but does not document the immediately following `st.caption("Usa este chat para debatir los resultados o pedir aclaraciones sobre este artículo.")` (chatbot.py:7). This is a rendered element visible to users.

---

## Spec Consistency Issues

None identified. `02_functional_frontend.md` does not contradict `04_look_and_feel.md`, `02_functional_specs.md`, or any other spec file on the verified claims. The gauge chart tiers documented in Section 9 align with the look-and-feel spec's color palette description.

---

## Quality Assessment

**What is well-specified:**
The spec is exceptionally detailed for a frontend specification. Every major behavioral path in `file_uploader.py` is correctly documented including saturation detection keywords, button labels, status messages, and temp-file lifecycle. The `scoring.py` logic is accurately transcribed—all 16 checklist keys, labels, risk conditions, and the crowdsourcing special case verify perfectly. The `gauge_chart.py` tier definitions (6 tiers, hex colors, threshold at 62.5) are exact. The CSS selector table in Section 10 matches `custom_css.py` completely. Session-state key names and defaults are all correct.

**What needs revision:**
The spec conflates `frontend/app.py` with root `app.py` in a way that introduces four fidelity issues (FI-03, FI-04, FI-05, FI-08). These are easy to fix: identify both files, document `frontend/app.py` as the refactored entry point, and correct the `puntuacion`→`health` variable name, the download filename prefix, and the call pattern for `process_uploaded_file`. The sidebar step ordering (FI-02) needs a note clarifying that while `with st.sidebar:` code is at line 73, Streamlit renders it independently of code position. The line number discrepancies (FI-06, FI-07) should be corrected to point to lines 27 and 30-31 respectively.

**What is acceptable as-is:**
The [GAP] markers (e.g., GAP-ext_frontend_01-001 for gauge chart call site) are correctly placed and honestly represent extraction limits. Section 5 (scoring logic), Section 6 (report generation), Section 7 (SOTA), Section 8 (chatbot), and Section 9 (gauge chart) are complete and accurate enough to implement from without further source inspection. The cross-reference table in Section 12 correctly identifies all backend dependencies.
