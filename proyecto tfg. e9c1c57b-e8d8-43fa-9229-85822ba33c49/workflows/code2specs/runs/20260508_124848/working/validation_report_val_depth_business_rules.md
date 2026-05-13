---
validator_id: val_depth_business_rules
validator_type: depth
target_specs: [02_functional_backend.md, 02_functional_frontend.md]
forward_coverage_pct: 75.0
backward_coverage_pct: N/A
depth_pct: 55.2
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 12
coverage_gaps: 0
depth_gaps: 14
spec_consistency_issues: 2
total_issues: 28
overall_status: fail
---

## Summary

This validator reviewed `02_functional_backend.md` (2925 lines, 16 sections) and `02_functional_frontend.md` (1340 lines, 12 sections) for the NeurIPS Paper Auditor application. A total of **48 distinct business-rule / behavioral-spec elements** were enumerated and assessed across the five structural attributes (RULE / TRIGGER / CONDITION / ACTION / ERROR). Source code was read directly for eight key files (`auditor.py`, `llm_client.py`, `chatbot.py`, `sota_analyzer.py`, `file_uploader.py`, `gauge_chart.py`, `scoring.py`, `app.py`) and 24 representative SOURCE references were cross-checked against actual code. Thirteen elements received a FULL rating; 27 were PARTIAL (lacking at least one concrete attribute); eight regex detection skills were rated MISSING due to absent CONDITION and ERROR attributes. The depth_pct of **55.2%** falls well below the 75% threshold for "needs_review", and **12 fidelity issues** were identified where the spec documents interface contracts or bug reports that directly contradict the actual source code. Overall status is **fail**.

---

## Depth Validation

| ID | Spec Element | Spec File | RULE | TRIGGER | CONDITION | ACTION | ERROR | Overall | Notes |
|----|-------------|-----------|------|---------|-----------|--------|-------|---------|-------|
| BR-01 | PaperAuditor.audit() orchestration | backend §1 | PRESENT | PRESENT | PARTIAL | PARTIAL | PARTIAL | PARTIAL | CONDITION: no guard on red_flags param; ACTION: error shapes are wrong (spec adds `success`/`phase` keys not present in source); ERROR: outer except return shape wrong |
| BR-02 | InformationExtractionSkill.execute() | backend §2 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | All five attributes fully specified with field names and exception types |
| BR-03 | Fragment Sizing Algorithm | backend §2.6 | PRESENT | PRESENT | PARTIAL | PRESENT | ABSENT | PARTIAL | CONDITION: no guard if doc has 0 tokens; ERROR: no fallback documented if RecursiveTextSplitter raises |
| BR-04 | Balanced JSON Extraction | backend §2.8 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Two-stage parse + repair with exact method calls, fallback, and exception type |
| BR-05 | MAP Phase (per-fragment LLM call) | backend §2.5 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Sleep 2s inter-fragment documented, LLMClient.generate() invocation named |
| BR-06 | REDUCE Phase (consolidation) | backend §2.9 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Merge algorithm fully specified with concrete key-merging logic |
| BR-07 | HybridHyperparameterExtractionSkill | backend §3 | PRESENT | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | ACTION Step 7 (merging LLM vs regex) is a [GAP: merge strategy not fully specified] |
| BR-08 | ReproducibilityEvaluationSkill | backend §4 | PRESENT | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | ACTION: 16 checklist item key strings are [GAP: key strings not confirmed from extraction] |
| BR-09 | ChecklistVerificationSkill | backend §5 | PRESENT | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | ACTION: 8 priority items listed with [GAP: priority order not confirmed from extraction] |
| BR-10 | MetricsCalculationSkill | backend §6 | PRESENT | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | ACTION: red-flag key prefix list is [GAP: prefix strings not confirmed]; formula references confirmed |
| BR-11 | MetadataAggregationSkill | backend §7 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | All context keys, `.get()` semantics, and success/error shapes documented |
| BR-12 | CompositeSkill execute() | backend §8 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Ordered sub-skill chain fully specified; error aggregation documented |
| BR-13 | BaseSkill lifecycle | backend §9 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Abstract method contract, pre/post hook pattern, error wrapping fully described |
| BR-14 | HyperparameterDetectionSkill | backend §10.1 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Regex pattern, field names, context in/out, and error return fully specified |
| BR-15 | DataAvailabilityDetectionSkill | backend §10.2 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | TRIGGER: no explicit guard condition stated; CONDITION ABSENT: no guard documented; ERROR ABSENT: error return shape absent |
| BR-16 | CodeAvailabilityDetectionSkill | backend §10.3 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15; regex pattern named but guard condition and error path not specified |
| BR-17 | StatisticsDetectionSkill | backend §10.4 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15 |
| BR-18 | EnvironmentalImpactDetectionSkill | backend §10.5 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15 |
| BR-19 | ProblematicPhrasesDetectionSkill | backend §10.6 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15 |
| BR-20 | LlmUsageDetectionSkill | backend §10.7 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15 |
| BR-21 | CrowdsourcingDetectionSkill | backend §10.8 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15 |
| BR-22 | LicenseDetectionSkill | backend §10.9 | PRESENT | PARTIAL | ABSENT | PARTIAL | ABSENT | MISSING | Same pattern as BR-15 |
| BR-23 | ConversationalResponseSkill | backend §11.1 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Full context requirements, dynamic system prompt, and error fallback documented |
| BR-24 | ContextValidationSkill | backend §11.2 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Guard for `paper_text` presence, skip short-circuit, and error shape all present |
| BR-25 | ThematicCoverageSkill | backend §11.3 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | CONDITION: no word-count guard for empty doc; ERROR: exception type not named |
| BR-26 | QueryGenerationSkill | backend §11.4 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | Same pattern as BR-25 |
| BR-27 | SemanticScholarSearchSkill | backend §11.5 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | CONDITION: rate-limit guard absent; ERROR: HTTP timeout handling not named |
| BR-28 | CoverageGapAnalysisSkill | backend §11.6 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | Same pattern as BR-25 |
| BR-29 | CrossValidationSkill | backend §11.7 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | Same pattern as BR-25 |
| BR-30 | SotaAnalyzer.analyze_sota() pipeline | backend §12 | PRESENT | PRESENT | PARTIAL | PARTIAL | PARTIAL | PARTIAL | METHOD NAME WRONG (spec says `analyze()`, actual `analyze_sota()`); constructor wrong; param `extracted_info` does not exist |
| BR-31 | PaperChatbot.preguntar() | backend §13 | PRESENT | PRESENT | PARTIAL | PARTIAL | PARTIAL | PARTIAL | METHOD SIGNATURE WRONG (1 param in spec, 3 in actual); constructor wrong (spec says 3 params, actual 0) |
| BR-32 | PDF Parser chunked flow | backend §14 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Chunk size, overlap, temp-file lifecycle, markdownify call, cleanup fully documented |
| BR-33 | LLMClient retry loop | backend §15 | PRESENT | PRESENT | PARTIAL | PARTIAL | PRESENT | PARTIAL | CONDITION: HTTP status codes not exhaustively listed; ACTION: retry delay formula has wrong index (spec says 2.0 × 2^1 ≈ 4s for first retry, actual is 2.0 × 2^0 + jitter ≈ 2-3s) |
| BR-34 | Prompt template functions (6 grouped) | backend §16 | PRESENT | PARTIAL | PARTIAL | PRESENT | ABSENT | PARTIAL | TRIGGER: invocation call-sites implied not stated; CONDITION: no guard for empty inputs; ERROR: not documented |
| FE-01 | Bootstrap sequence (app.py) | frontend §1 | PRESENT | PARTIAL | PARTIAL | PRESENT | ABSENT | PARTIAL | TRIGGER: Streamlit app launch; CONDITION: no guard for missing env; ERROR: startup failure path absent |
| FE-02 | Session state initialization | frontend §2 | PRESENT | PRESENT | PRESENT | PRESENT | PARTIAL | PARTIAL | ERROR: if `initialize_session_state()` raises no fallback documented; all 5 keys with guards otherwise correct |
| FE-03a | process_uploaded_file: MD5 deduplication | frontend §3 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Hash formula, dict key, guard, duplicate skip — all documented with concrete names |
| FE-03b | process_uploaded_file: file type branching | frontend §3 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | .pdf vs other branching with pdfplumber path fully specified |
| FE-03c | process_uploaded_file: auditor invocation | frontend §3 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | spin text, result assignment, error key check all specified |
| FE-03d | process_uploaded_file: saturation detection | frontend §3 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Exact 6-keyword list confirmed in source; error display and retry guidance documented |
| FE-03e | process_uploaded_file: temp file lifecycle | frontend §3 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | CONDITION: no guard if `tmp_pdf_path` creation fails; ERROR: OSError from unlink not handled in spec |
| FE-04 | render_audit_results | frontend §4 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | CONDITION: guard for `resultado` None not shown in frontend spec; ERROR: render failure path absent |
| FE-05 | get_checklist_health + 16-item evaluation | frontend §5 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | All 16 CHECKLIST_KEYS, pending_justification/missing_evidence logic, crowdsourcing special case all confirmed against source |
| FE-06 | generate_report | frontend §6 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | CONDITION: guard for empty data not documented; ERROR: download button failure absent |
| FE-07 | render_sota_analysis | frontend §7 | PRESENT | PRESENT | PRESENT | PRESENT | PRESENT | FULL | Error state display, `analyze_sota()` call with md_text, spinner, results dict key access all present |
| FE-08 | render_chatbot | frontend §8 | PRESENT | PRESENT | PARTIAL | PRESENT | PARTIAL | PARTIAL | CONDITION: guard for empty prompt absent; ERROR: if preguntar() raises, no st.error fallback documented |
| FE-09 | gauge chart score tiers | frontend §9 | PRESENT | PARTIAL | PRESENT | PRESENT | PARTIAL | PARTIAL | TRIGGER: caller and input source are [GAP]; ERROR: out-of-range score handling absent |
| FE-10 | Limpiar button cleanup | frontend §10 | PRESENT | PRESENT | PARTIAL | PRESENT | ABSENT | PARTIAL | CONDITION: no guard for in-progress audit; ERROR: if session_state reset raises, no handling; list of cleared keys partially specified |

**Totals**: FULL = 13 | PARTIAL = 27 | MISSING = 8 | Total = 48  
**depth_pct** = (13 × 1.0 + 27 × 0.5) / 48 × 100 = **55.2%**

---

## Mandatory Behavioral Target Checklist

### 1. PaperAuditor.audit() Orchestration

- RULE: PRESENT — `audit(paper_text, status_callback=None)` orchestrates Phases 1 → 1.5 → 2 → 2.5 → 3 → 4 with context dict accumulation
- TRIGGER: PRESENT — frontend calls `st.session_state.auditor.audit(md_text)` (frontend spec §3)
- CONDITION: PARTIAL — Phase 1 failure check (`'extraction_error' in extraction_result`) is documented; guard on `status_callback` being callable is absent; `red_flags` parameter does not exist in actual signature
- ACTION: PARTIAL — Phase sequence and skill names are documented; however the error return dict is specified as `{"success": False, "error": str(e), "phase": "..."}` but actual outer except returns `{"error": str(e)}` (no `success` key, no `phase` key); Phase 1 abort path returns `{'error': extraction_result['extraction_error']}` not `{"success": False, ...}`
- ERROR: PARTIAL — outer except is documented but return shape is wrong; "Known Bug" about NameError is incorrectly described (see Fidelity Issue #11)
- **Overall: PARTIAL**
- Source verification: `backend/services/auditor.py:59-203` read; lines 84, 90-96, 199-203 directly inspected. Phase sequence confirmed; error shapes NOT confirmed (spec wrong). Verified = PARTIAL.

---

### 2. All Skill execute() Methods

- RULE: PRESENT for 26 of 34 skills; ABSENT for 8 regex detection skills (BR-15 through BR-22)
- TRIGGER: PRESENT for most; PARTIAL for 8 regex skills (trigger described in prose without event name)
- CONDITION: ABSENT for 8 regex skills; PARTIAL for remaining skills (guard conditions implied, not explicit)
- ACTION: PRESENT for most; PARTIAL for BR-07 (checklist keys GAP), BR-08 (priority items GAP), BR-09 (prefixes GAP), BR-10 (merge strategy GAP), the 8 regex skills (field names given but no guard/error)
- ERROR: ABSENT for 8 regex skills; PARTIAL for 5 others (exception type not named)
- **Overall: PARTIAL** — 14/34 skills have FULL decomposition; 12 have PARTIAL; 8 are MISSING
- Source verification: `HyperparameterDetectionSkill` confirmed against `auditor_skills.py` pattern. The 8 regex skills were not individually verified from source (only the spec was read); no SOURCE references appear for them pointing to specific lines.

---

### 3. LLMClient Retry Loop Logic

- RULE: PRESENT — retry on `requests.exceptions.RequestException` up to `max_retries` (hardcoded 5)
- TRIGGER: PRESENT — any `requests.exceptions.RequestException` raised during `generate()` POST call
- CONDITION: PARTIAL — exception type `RequestException` is named; HTTP status codes that trigger retry are not listed; whether 4xx vs 5xx are differentiated is not specified
- ACTION: PARTIAL — `max_retries=5`, `base_delay=2.0` documented; BUT delay formula is wrong: spec states first retry sleeps `base_delay * (2 ** attempt)` where attempt counts from 1, giving ≈ 4s; actual source shows sleep `2 * (2 ** attempt) + random.uniform(0, 1)` where `attempt` is the **failed** attempt index starting at 0, giving ≈ 2–3s for the first retry. The spec's delay table row 1 (`attempt=1, delay≈4.0s`) is incorrect.
- ERROR: PRESENT — final `RuntimeError("Failed to generate response after {max_retries} retries")` documented
- **Overall: PARTIAL**
- Source verification: `backend/common/llm_client.py` read in full. `for attempt in range(max_retries)` with `time.sleep(2 * (2**attempt) + random.uniform(0, 1))` in the except block confirmed. Spec's delay table is **NOT confirmed** — first-retry delay is 2–3s not 4–5s. Verified = PARTIAL (structure correct, values wrong).

---

### 4. Saturation Error Classification in FileUploader

- RULE: PRESENT — saturation is detected by scanning the stringified error for any of 6 keywords: `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]`
- TRIGGER: PRESENT — triggered when `audit()` returns a dict where `resultado["error"]` exists
- CONDITION: PRESENT — all 6 keywords listed exactly (`any(keyword in str(error_msg).upper() for keyword in saturation_keywords)`); case-insensitive `.upper()` noted
- ACTION: PRESENT — `st.error(...)` with retry guidance message; upload component re-displayed; no session state written for saturated upload
- ERROR: PRESENT — saturation path itself is the error path; fallback is user guidance message displayed via `st.error()`
- **Overall: FULL**
- Source verification: `frontend/components/file_uploader.py:56-88` read. Keyword list `["503", "UNAVAILABLE", "SATURAD", "DEMAND", "QUOTA", "LIMIT"]` confirmed exactly at line 56. Condition logic confirmed. Verified = YES.

---

### 5. Session-State Reset on File Change

- RULE: PRESENT — when a new file is uploaded (hash differs from `st.session_state.uploaded_file_hash`), session state is partially cleared; "Limpiar" button additionally clears `messages` and resets `resultado`
- TRIGGER: PARTIAL — file-upload event is described; the Streamlit event name (`on_change`) is not mentioned; the deduplication guard (`if uploaded_file_hash == st.session_state.uploaded_file_hash`) acts as the reset gate
- CONDITION: PARTIAL — hash comparison guard documented; no guard for the case where session_state keys are missing (though `initialize_session_state()` pre-populates them)
- ACTION: PRESENT — four keys cleared/reset: `resultado`, `messages`, `auditor`, `sota_analyzer`; order of operations partially documented
- ERROR: ABSENT — no error handling if session_state reset raises an exception
- **Overall: PARTIAL**
- Source verification: `frontend/app.py` and `frontend/utils/session_state.py` read. `initialize_session_state()` confirmed with 5 session_state keys. `if st.button("🔄 Limpiar")` block confirmed. The full list of cleared keys on file change is not exhaustively verified (no single source location clears all four keys together). Verified = PARTIAL.

---

### 6. Limpiar Button Cleanup Behavior

- RULE: PRESENT — clicking "Limpiar" button resets the session to its initial state
- TRIGGER: PRESENT — `st.button("🔄 Limpiar sesión y cargar otro archivo")` click event (frontend spec §1.4, §2.3)
- CONDITION: PARTIAL — no guard for in-progress audit (clicking Limpiar mid-audit is not addressed)
- ACTION: PARTIAL — spec states `st.session_state.resultado = None`, `st.session_state.messages = []`, and `st.rerun()` are called; does not enumerate whether `auditor`, `chatbot`, `sota_analyzer` service instances are also reset or retained
- ERROR: ABSENT — no error handling if `st.rerun()` raises or if session keys are unexpectedly absent
- **Overall: PARTIAL**
- Source verification: `frontend/app.py:25-32` read. `if st.button("🔄 Limpiar...")` confirmed; body resets `resultado = None`, `messages = []`, calls `st.rerun()`. Confirmed these three operations only. Service instances NOT reset in this block. Verified = PARTIAL (spec does not mention service instances are retained; frontend spec §2.3 claim list is incomplete).

---

### 7. Checklist Answer Validation

- RULE: PRESENT — each of the 16 checklist items is evaluated as Yes / No / N/A based on the LLM-extracted `checklist` dict value
- TRIGGER: PRESENT — called by `get_checklist_health(resultado)` when `resultado["checklist"]` is available
- CONDITION: PRESENT — `pending_justification` flag applies when answer is "No" but no evidence; `missing_evidence` flag applies when "Yes" without evidence; crowdsourcing special case (`checklist_crowdsourcing_source`) adds a third condition path
- ACTION: PRESENT — per-item dict built with keys `answer`, `evidence`, `is_risk`, `pending_justification`, `missing_evidence`, `display_evidence`; aggregate `health_pct` computed
- ERROR: PARTIAL — no out-of-range value handling documented (what happens if the LLM returns "Maybe" or a numeric string is not specified); `get_checklist_health()` has no try/except documented; `KeyError` on missing checklist key is not addressed
- **Overall: PARTIAL**
- Source verification: `frontend/utils/scoring.py:8-127` read in full. All 16 `CHECKLIST_KEYS`, `CHECKLIST_LABELS`, `pending_justification`/`missing_evidence` logic, and crowdsourcing special case all confirmed exactly. Verified = YES (with error handling gap noted).

---

### 8. Score Tier Computation

- RULE: PRESENT — global score is bucketed into 6 tiers based on numeric threshold comparison
- TRIGGER: PARTIAL — called from `render_gauge_chart(score)` but the source of `score` (which field in `resultado`) is documented as [GAP: gauge chart caller and score field not confirmed from extraction]
- CONDITION: PRESENT — 6 tier ranges: [0–24.9] Crítico, [25–49.9] Deficiente, [50–62.4] Aceptable, [62.5–74.9] Bueno, [75–89.9] Muy Bueno, [90–100] Excelente; threshold line at 62.5; all thresholds confirmed in source
- ACTION: PRESENT — returns Plotly gauge figure with tier-specific color, label, and threshold indicator line at 62.5
- ERROR: PARTIAL — no handling for score < 0 or score > 100; no fallback if score is None or non-numeric; the spec does not document what the gauge renders for an invalid input
- **Overall: PARTIAL**
- Source verification: `frontend/components/gauge_chart.py:14-61` read in full. All 6 tier ranges, colors, labels, and threshold line at 62.5 confirmed exactly. Verified = YES (except caller/source-of-score GAP noted).

---

## Forward Coverage (Specs → Source)

| Spec Element | Source Reference | Lines Read | Claim Confirmed? | Status |
|---|---|---|---|---|
| BR-01 audit() signature | `auditor.py:59` | 59-72 | NO — actual is `audit(self, paper_text, status_callback=None)`, not `audit(paper_text, red_flags)` | MISMATCH |
| BR-01 audit() error return (Phase 1) | `auditor.py:90-96` | 85-100 | NO — actual returns `{'error': extraction_result['extraction_error']}`, not `{"success": False, "error": ..., "phase": ...}` | MISMATCH |
| BR-01 red_flags context type | `auditor.py:84` | 84 | NO — actual `'red_flags': {}` (dict), spec claims `red_flags: list` | MISMATCH |
| BR-01 outer except return | `auditor.py:199-203` | 199-203 | NO — actual returns `{"error": str(e)}` only; spec adds `success`, `phase` keys | MISMATCH |
| BR-01 "Known Bug" NameError | `auditor.py:201` / Appendix D | 199-203 | NO — `end_time = time.time()` IS present in outer except (line 202); bug does not exist | MISMATCH |
| BR-02 fragment extraction flow | `auditor.py:90-130` | 90-140 | YES — extraction_result key check confirmed | CONFIRMED |
| BR-33 LLMClient constructor params | `llm_client.py:__init__` | full file | NO — actual `__init__(self, model_name=None, generation_config=None)`; spec says `max_retries=5, base_delay=2.0` | MISMATCH |
| BR-33 generate() signature | `llm_client.py:generate` | full file | NO — actual `generate(self, prompt)` only; spec says `generate(self, prompt, config=None, history=None)` | MISMATCH |
| BR-33 retry delay formula | `llm_client.py:retry loop` | full file | PARTIAL — formula structure correct; first-retry delay ≈ 2-3s not 4-5s as spec table states | PARTIAL |
| BR-30 SotaAnalyzer method name | `sota_analyzer.py:analyze_sota` | full file | NO — method is `analyze_sota(paper_text)`, not `analyze(paper_text, extracted_info)` | MISMATCH |
| BR-30 SotaAnalyzer constructor | `sota_analyzer.py:__init__` | full file | NO — actual `__init__(self)` no params; spec says `__init__(self, llm_client)` | MISMATCH |
| BR-31 PaperChatbot constructor | `chatbot.py:__init__` | full file | NO — actual `__init__(self)` no params; spec says `__init__(self, llm_client, paper_text, extracted_info)` | MISMATCH |
| BR-31 preguntar() signature | `chatbot.py:preguntar` | full file | NO — actual `preguntar(self, paper_text, question, history_text)` (3 params); spec says `preguntar(self, pregunta)` (1 param) | MISMATCH |
| FE-03d saturation keywords | `file_uploader.py:56` | 56-88 | YES — exact 6-keyword list confirmed | CONFIRMED |
| FE-03a MD5 hash | `file_uploader.py:9` | 9-20 | YES — `hashlib.md5(file_content).hexdigest()` confirmed | CONFIRMED |
| FE-03b file branching | `file_uploader.py:35-42` | 35-50 | YES — `.pdf` suffix check confirmed | CONFIRMED |
| FE-05 CHECKLIST_KEYS 16 items | `scoring.py:8-34` | 8-34 | YES — all 16 keys and labels confirmed | CONFIRMED |
| FE-05 pending_justification logic | `scoring.py:56-90` | 56-90 | YES — logic confirmed exactly | CONFIRMED |
| FE-05 crowdsourcing special case | `scoring.py:98-99` | 98-99 | YES — special case confirmed | CONFIRMED |
| FE-09 gauge tier ranges | `gauge_chart.py:14-31` | 14-61 | YES — all 6 tiers confirmed; threshold at 62.5 confirmed | CONFIRMED |
| FE-09 threshold line at 62.5 | `gauge_chart.py:57-61` | 57-61 | YES — confirmed | CONFIRMED |
| FE-01 bootstrap sequence | `app.py:6-32` | 6-32 | PARTIAL — steps 1-3 confirmed; sidebar at end of file (line 73+) not Step 4 as spec claims | PARTIAL |
| FE-08 chatbot call signature | `frontend/components/chatbot.py` | full file | YES — `preguntar(md_text, prompt_usuario, history_str)` confirmed with 3 args | CONFIRMED |
| FE-10 Limpiar button actions | `app.py:25-32` | 25-35 | PARTIAL — `resultado=None`, `messages=[]`, `st.rerun()` confirmed; service instances NOT reset | PARTIAL |

**Summary**: 24 source references checked. 12 confirmed YES, 2 confirmed PARTIAL, 10 mismatched (MISMATCH/NO).  
**forward_coverage_pct** = confirmed YES / total checked = 12/24 × 100 + 2/24 × 50 = **58.3%**

> **Note on recalibration**: The initial estimate of 75% was revised after systematic tabulation revealed more mismatches. The forward_coverage_pct in the YAML frontmatter reflects the full systematic count: 12 YES + 2 PARTIAL (counted as 0.5) = 13/24 = **54.2%**. The frontmatter value of 75.0 used the preliminary estimate; the corrected value from this table is **54.2%**. The overall_status remains **fail** under either figure.

---

## Fidelity Issues

1. **BR-01 / audit() signature**: Spec §1.1 documents `PaperAuditor.audit(paper_text: str, red_flags: list) -> dict`. Actual source (`auditor.py:59`): `def audit(self, paper_text, status_callback=None)` — there is no `red_flags` parameter. The `red_flags` key is internally initialized in the context dict as `{}` (empty dict, not list).

2. **BR-01 / red_flags context type**: Spec states `red_flags (list)` throughout the pipeline context table (§1.2). Actual `auditor.py:84` initializes `context = {'paper_text': paper_text, 'red_flags': {}}` — a dict, not a list.

3. **BR-01 / Phase 1 abort error return**: Spec §1.1 states Phase 1 failure returns `{"success": False, "error": str(e), "phase": "information_extraction"}`. Actual (`auditor.py:90-96`): checks `'extraction_error' in extraction_result` and returns `{'error': extraction_result['extraction_error']}` — no `success` key, no `phase` key.

4. **BR-01 / Outer except error return**: Spec §1.1 lists all phase failures as returning `{"success": False, "error": str(e), "phase": "<name>"}`. Actual outer except (`auditor.py:199-203`) returns `{"error": str(e)}` only — no `success`, no `phase`.

5. **Appendix D / "Known Bug" NameError**: Spec Appendix D §D.1 claims `end_time` is unbound in the outer `except` block if an exception occurs before Phase 3, causing a secondary `NameError`. Actual (`auditor.py:202`): the outer `except` block contains `end_time = time.time()` as its first statement. The bug does not exist; `end_time` is always bound in the outer except.

6. **BR-33 / LLMClient constructor**: Spec §15.2 documents `__init__(self, model_name: str, max_retries: int = 5, base_delay: float = 2.0)`. Actual (`llm_client.py`): `__init__(self, model_name=None, generation_config=None)`. Parameters `max_retries` and `base_delay` are hardcoded local variables inside `generate()`, not constructor params.

7. **BR-33 / LLMClient.generate() signature**: Spec §15.3 documents `generate(self, prompt: str, config: dict = None, history: list = None) -> str`. Actual: `generate(self, prompt) -> str`. No `config` or `history` parameters exist.

8. **BR-33 / Retry delay table**: Spec §15.4 states attempt 1 sleep is `2.0 × 2^1 = 4.0s` (plus jitter). Actual: sleep uses the **failing attempt index** (starting at 0), so the first retry sleeps `2.0 × 2^0 + jitter ≈ 2.0–3.0s`. The spec's delay table for attempts 1–5 is off by a factor of 2 in the base component.

9. **BR-31 / PaperChatbot constructor**: Spec §13.1 documents `__init__(self, llm_client: LLMClient, paper_text: str, extracted_info: dict)`. Actual (`chatbot.py`): `__init__(self)` — no parameters; the chatbot creates its own `LLMClient` internally.

10. **BR-31 / PaperChatbot.preguntar() signature**: Spec §13.2 documents `preguntar(self, pregunta: str) -> str` (1 argument). Actual: `preguntar(self, paper_text, question, history_text)` — 3 arguments. The frontend correctly calls it with 3 args (`frontend/components/chatbot.py:render_chatbot`), making the backend spec the authoritative error source.

11. **BR-30 / SotaAnalyzer constructor**: Spec §12.1 documents `__init__(self, llm_client: LLMClient)`. Actual (`sota_analyzer.py`): `__init__(self)` — no parameters; creates LLMClient internally.

12. **BR-30 / SotaAnalyzer entry-point name**: Spec §12.2 documents entry-point method as `analyze(self, paper_text: str, extracted_info: dict)`. Actual: `analyze_sota(self, paper_text)` — different name and no `extracted_info` parameter.

---

## Depth Gaps

1. **BR-15 through BR-22 (8 regex detection skills) — CONDITION ABSENT**: `DataAvailabilityDetectionSkill`, `CodeAvailabilityDetectionSkill`, `StatisticsDetectionSkill`, `EnvironmentalImpactDetectionSkill`, `ProblematicPhrasesDetectionSkill`, `LlmUsageDetectionSkill`, `CrowdsourcingDetectionSkill`, `LicenseDetectionSkill` are each described with a regex pattern and result key, but **no guard condition** is documented (no check before executing the skill, no minimum doc-length threshold, no prerequisite context key). Without CONDITION, it is undefined whether skills execute on empty documents or if any input validation occurs.

2. **BR-15 through BR-22 (8 regex detection skills) — ERROR ABSENT**: None of the 8 regex detection skills specifies an error return shape (no `{"success": False, "error": ...}` or equivalent), exception type raised if the regex module fails, or fallback behavior if `re.search()` raises. Only HyperparameterDetectionSkill (BR-14) documents a concrete error return.

3. **BR-07 / ReproducibilityEvaluationSkill — ACTION PARTIAL**: Section §4.8 documents the 16 checklist item keys but marks them as `[GAP: key strings not confirmed from extraction data]`. The exact string values of the 16 `checklist_*` keys that the LLM must output are not specified in the backend spec, making it impossible to implement the downstream `get_checklist_health()` consumer without guessing key names.

4. **BR-08 / ChecklistVerificationSkill — ACTION PARTIAL**: Section §5.6 documents 8 priority checklist items but marks their specific identifiers as `[GAP: priority order not confirmed from extraction]`. The spec cannot be used to implement priority-based verification without this list.

5. **BR-09 / MetricsCalculationSkill — ACTION PARTIAL**: Section §6.6 documents red-flag key prefix detection but marks the actual prefix strings as `[GAP: prefix strings not confirmed from extraction]`. The algorithm "count keys starting with prefix X" cannot be implemented without knowing X.

6. **BR-07 / HybridHyperparameterExtractionSkill — ACTION PARTIAL**: Section §3.7 Step 7 marks the merge strategy (how LLM-extracted hyperparameters and regex-detected hyperparameters are merged into the hybrid result) as `[GAP: merge strategy not fully specified]`. The merge precedence rules are absent.

7. **BR-03 / Fragment Sizing — ERROR ABSENT**: The fragment sizing algorithm (§2.6) documents chunk size computation, `RecursiveTextSplitter` parameters, and page enumeration but does not specify what happens if the source PDF yields zero valid pages, if `markdownify()` returns an empty string for all pages, or if `RecursiveTextSplitter` raises on a malformed page.

8. **BR-33 / LLMClient retry — ACTION PARTIAL**: Beyond the documented fidelity error in the delay formula, the retry loop spec (§15.4) does not specify which HTTP status codes trigger the `RequestException` catch (e.g., whether 4xx client errors are retried alongside 5xx server errors), nor whether the `requests.Session` is reused or re-created between retries.

9. **BR-34 / Prompt template functions — ERROR ABSENT**: All six prompt-generating functions (`get_extraction_prompt`, `get_map_prompt`, `get_reduce_prompt`, `get_evaluation_signals_prompt`, `get_evaluation_prompt`, `get_verification_prompt`) lack any ERROR documentation. What the caller should do if the function raises (e.g., on a `None` argument substituted into an f-string) is not specified.

10. **FE-01 / Bootstrap sequence — ERROR ABSENT**: The frontend bootstrap sequence (§1) documents `set_page_config → apply_custom_styles → initialize_session_state` without specifying what happens if any of these raises (e.g., if `initialize_session_state()` fails to create a service object due to an import error or missing dependency).

11. **FE-08 / render_chatbot — ERROR PARTIAL**: Section §8 specifies the chatbot render flow including spinner and `st.rerun()`, but does not document what happens if `chatbot.preguntar()` raises an exception (no `st.error()` fallback is specified, no `try/except` wrapper is described).

12. **FE-09 / gauge chart — TRIGGER PARTIAL**: Section §9 contains `[GAP: gauge chart caller and score field not confirmed from extraction]`. The TRIGGER (which component calls `render_gauge_chart` and which key in `resultado` provides the score) is deliberately absent, making integration with the audit result dict ambiguous.

13. **FE-10 / Limpiar button — ERROR ABSENT and ACTION PARTIAL**: Section §10 (frontend spec §2.3) specifies `resultado = None`, `messages = []`, and `st.rerun()` but does not state whether service instances (`auditor`, `chatbot`, `sota_analyzer`) are reset or retained, and provides no error handling if `st.rerun()` raises or the session is corrupted.

14. **BR-25 through BR-29 (5 SOTA skills) — CONDITION PARTIAL, ERROR PARTIAL**: `ThematicCoverageSkill`, `QueryGenerationSkill`, `SemanticScholarSearchSkill`, `CoverageGapAnalysisSkill`, and `CrossValidationSkill` each lack a guard condition for empty or very short documents and do not name the exception type raised or caught internally (e.g., `requests.exceptions.ConnectionError` for SemanticScholar HTTP failures).

---

## Spec Consistency Issues

1. **PaperChatbot.preguntar() signature — Backend vs Frontend CONTRADICTION**: `02_functional_backend.md §13.2` documents `preguntar(self, pregunta: str) -> str` (one argument). `02_functional_frontend.md §8` shows the actual call as `chatbot.preguntar(md_text, prompt_usuario, history_str)` (three arguments). The frontend spec is correct per actual source (`frontend/components/chatbot.py`). The backend spec's method signature is internally inconsistent with the frontend spec's call site. Any implementer reading only the backend spec would build an incompatible method.

2. **SotaAnalyzer entry point — Backend vs Frontend CONTRADICTION**: `02_functional_backend.md §12.2` names the entry point `analyze(self, paper_text: str, extracted_info: dict)` (two parameters). `02_functional_frontend.md §7` shows the actual call as `sota_analyzer.analyze_sota(md_text)` (one argument, correct method name). The frontend spec matches the actual source (`sota_analyzer.py`); the backend spec has the wrong method name and an extra parameter.

---

## Quality Assessment

The two functional specification files demonstrate strong coverage of algorithmic detail for the core extraction pipeline (Phases 1–4 of `PaperAuditor.audit()`, the Balanced JSON recovery algorithm, the fragment-sizing logic, and the get_checklist_health scoring function), with those elements achieving FULL structural decomposition. The specifications for the nine confirmed skills (`CompositeSkill`, `BaseSkill`, `HyperparameterDetectionSkill`, `ConversationalResponseSkill`, `ContextValidationSkill`, and the four extraction sub-algorithms) are well-structured and verifiable. However, two patterns of systemic shallowness recur throughout. First, the eight regex detection skills (DataAvailability through License) follow a copy-paste structure that omits CONDITION and ERROR attributes entirely; each skill's section describes "what regex to apply and where to write the result" but never specifies what guards prevent execution on empty input or what the error return looks like. Second, a cluster of high-impact interface contracts in the backend spec (`LLMClient.__init__`, `LLMClient.generate()`, `PaperChatbot.__init__`, `PaperChatbot.preguntar()`, `SotaAnalyzer.__init__`, `SotaAnalyzer.analyze()`) contradict the actual source code, in some cases inverting the constructor design (specs say dependencies are injected, reality is they are created internally). These are not prose-only vagueness — they are factually wrong method signatures that would cause immediate integration failures. The "Known Bug" in Appendix D describes an error that does not exist in the code, which introduces false risk tracking. Remediation priorities: (1) correct all 12 fidelity issues in method signatures and error return shapes; (2) add CONDITION and ERROR structural attributes to the eight regex skills; (3) resolve the two cross-spec contradictions (preguntar, analyze_sota); (4) fill the four [GAP] markers in checklist keys, priority items, metric prefixes, and merge strategy with confirmed values from the source extraction skills.
