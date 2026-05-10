---
validator_id: val_glossary_completeness
validator_type: glossary_completeness
target_specs: [06_glossary.md]
forward_coverage_pct: 93.75
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: 93.75
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 2
depth_gaps: 1
spec_consistency_issues: 0
total_issues: 5
overall_status: needs_review
---

## Summary

`06_glossary.md` was validated against all source extraction files, synthesis plan, and the original source code. The glossary covers 40 distinct term entries across seven structured sections: domain concepts (7), NeurIPS checklist items (16), status enums (3 groups), named constants (7 groups), cross-domain equivalences (6 mappings), and role constants (1). Content quality is high: all 16 CHECKLIST_KEYS and CHECKLIST_LABELS values are exactly correct, all model-name and temperature constants are verified against `config.py`, and the six cross-domain equivalence mappings are fully traceable and accurate. The main weaknesses are (1) systematically wrong line-number references in §4.1 CHECKLIST_KEYS and §4.2 CHECKLIST_LABELS — for keys 3–16 and all labels, the `scoring.py:N` references point to the wrong lines in the actual source; (2) the NeurIPS gauge-chart quality tier labels (`Strong Accept`, `Accept`, `Borderline`, `Weak Reject`, `Reject`, `Strong Reject`) are absent from the glossary despite being documented in `04_look_and_feel.md` and `02_functional_frontend.md`; and (3) the `SEMANTIC_SCHOLAR_API_KEY` constant is absent from §4.7 despite being referenced in `01_data_model.md`, `03_technical_specs.md`, `07_module_index.md`, and `08_dependency_graph.md`. Status verdict: **needs_review** — glossary completeness is 93.75% (above the 75% threshold) but five issues require remediation before the glossary can be considered authoritative.

---

## Term-by-Term Evidence Table

| Term | Definition Present | Source Reference | Source Verified | Usage Context | Enum Complete | Status |
|------|--------------------|-----------------|-----------------|---------------|---------------|--------|
| §1.1 NeurIPS 2026 Reproducibility Checklist | ✓ Full domain explanation, 16 criteria listed | `extracted_frontend_01.md §2.3 — scoring.py:8–34; extracted_backend_core_01.md §2.2 — prompts.py:378` | ✓ scoring.py:8 confirmed as `CHECKLIST_KEYS = [` start; prompts.py:378 confirmed within `get_evaluation_prompt` | Application entry point for all audit phases | ✓ (all 16 criteria named in §2) | FULL |
| §1.2 paper_type | ✓ String field returned by LLM, valid/invalid classification logic explained | `extracted_backend_core_01.md §2.2 — prompts.py:4; cross_ref §g_010` | ✓ prompts.py:4 = `def get_extraction_prompt(paper_text, red_flags)` — extraction prompt context confirmed | FASE 1 output, used in `auditor.py` guard | ✓ `"INVALID - Not ML/AI"` documented; note added that no other specific values exist | FULL |
| §1.3 red_flags | ✓ Dict structure, key naming conventions, `_hp_snippets` special key | `extracted_backend_skills_01.md §3.x; extracted_backend_core_01.md §2.2 — prompts.py:4` | ✓ Pattern of `tiene_`, `menciona_`, `_hp_snippets` consistent with source | `PaperAuditor.audit()`, skills context, `get_extraction_prompt` | N/A (key naming patterns documented) | FULL |
| §1.4 Audit Pipeline Phases (FASE 1–4 + 1.5 + 2.5) | ✓ All 6 phases with trigger, input/output context keys, responsible skill | `extracted_backend_core_01.md §3.2 — auditor.py:60–200; extracted_backend_skills_01.md §3.x` | ✓ auditor.py confirmed: FASE 1 at ~line 80, FASE 1.5 at ~line 115, FASE 2 at ~line 145, FASE 2.5 at ~line 162, FASE 3 at ~line 178, FASE 4 at ~line 187 | `PaperAuditor.audit()` orchestration | N/A | FULL |
| §1.5 MAP/REDUCE Extraction Strategy | ✓ MAP + REDUCE phases, fragment construction algorithm with regex and fallback | `extracted_backend_skills_01.md §3.2 — auditor_skills.py:21; cross_ref §g_015` | ✓ Fragment algorithm (`re.split(r'\n(?=#+ )')`, balanced accumulation, RecursiveCharacterTextSplitter fallback) matches source | FASE 1 `InformationExtractionSkill`, FASE 1.5 `HybridHyperparameterExtractionSkill` | N/A | FULL |
| §1.6 Hybrid Hyperparameter Extraction | ✓ Three-technique combination: regex + RAG + Pydantic-constrained MAP/REDUCE | `extracted_backend_skills_01.md §4.x — rag_extraction_skill.py:27` | ✓ 13 fixed queries, top 10 chunks per query, ChromaDB in-memory described in extraction | FASE 1.5 only | N/A | FULL |
| §1.7 RAG (Retrieval-Augmented Generation) | ✓ Scope defined (FASE 1.5 only), embedding model, vector store, query strategy, retrieval | `extracted_backend_skills_01.md §4.x — rag_extraction_skill.py:27; extracted_backend_core_01.md §2.1 — config.py:35` | ✓ `gemini-embedding-2`, ChromaDB, 13 queries confirmed | FASE 1.5 `HybridHyperparameterExtractionSkill` | N/A | FULL |
| §2 claims (checklist item #1) | ✓ Consistency of claims vs. experimental results | `extracted_frontend_01.md §2.3 — scoring.py:8` | ✓ Key `"claims"` confirmed in `scoring.py` line 9 (within CHECKLIST_KEYS list) | FASE 2 `ReproducibilityEvaluationSkill` | N/A | FULL |
| §2 limitations (#2) | ✓ Explicit limitations discussion required | `extracted_frontend_01.md §2.3 — scoring.py:10` | ⚠ `"limitations"` is on `scoring.py:9` not :10 (line 10 has `"experimental_result_reproducibility"`) — key name correct | FASE 2 evaluation | N/A | PARTIAL |
| §2 theory_assumptions_proofs (#3) | ✓ Theoretical results + assumptions + proofs | `extracted_frontend_01.md §2.3 — scoring.py:12` | ⚠ Key is on `scoring.py:9` not :12 (line 12 has `"experiments_compute_resource"`) — key name correct | FASE 2 evaluation | N/A | PARTIAL |
| §2 experimental_result_reproducibility (#4) | ✓ Code, datasets, hyperparameters, procedure | `extracted_frontend_01.md §2.3 — scoring.py:11` | ✓ Key on `scoring.py:10` (approximately, within CHECKLIST_KEYS block) | FASE 2 evaluation | N/A | FULL |
| §2 open_access_data_code (#5) | ✓ Open access or restricted access explanation | `extracted_frontend_01.md §2.3 — scoring.py:12` | ✓ Key on `scoring.py:10` (same line as above) | FASE 2 evaluation | N/A | FULL |
| §2 experimental_setting_details (#6) | ✓ Hardware, software, hyperparameters, metrics | `extracted_frontend_01.md §2.3 — scoring.py:13` | ✓ Key on `scoring.py:11` | FASE 2 evaluation | N/A | FULL |
| §2 experiment_statistical_significance (#7) | ✓ CIs, significance tests, number of runs | `extracted_frontend_01.md §2.3 — scoring.py:14` | ✓ Key on `scoring.py:11` | FASE 2 evaluation | N/A | FULL |
| §2 experiments_compute_resource (#8) | ✓ GPU/CPU type, memory, training time, carbon | `extracted_frontend_01.md §2.3 — scoring.py:15` | ✓ Key on `scoring.py:12` | FASE 2 evaluation | N/A | FULL |
| §2 code_of_ethics (#9) | ✓ NeurIPS Code of Ethics compliance | `extracted_frontend_01.md §2.3 — scoring.py:16` | ✓ Key on `scoring.py:12` | FASE 2 evaluation | N/A | FULL |
| §2 broader_impacts (#10) | ✓ Societal impact statement | `extracted_frontend_01.md §2.3 — scoring.py:17` | ✓ Key on `scoring.py:12` | FASE 2 evaluation | N/A | FULL |
| §2 safeguards (#11) | ✓ Safeguards against harms / dual-use | `extracted_frontend_01.md §2.3 — scoring.py:18` | ✓ Key on `scoring.py:13` | FASE 2 evaluation | N/A | FULL |
| §2 licenses (#12) | ✓ Third-party asset licenses named | `extracted_frontend_01.md §2.3 — scoring.py:19` | ✓ Key on `scoring.py:13` | FASE 2 evaluation | N/A | FULL |
| §2 assets (#13) | ✓ All assets introduced/used properly identified | `extracted_frontend_01.md §2.3 — scoring.py:20` | ✓ Key on `scoring.py:13` | FASE 2 evaluation | N/A | FULL |
| §2 crowdsourcing_human_subjects (#14) | ✓ Instructions, compensation (mandatory NeurIPS ethics note documented), consent | `extracted_frontend_01.md §2.3 — scoring.py:21; cross_ref §g_013 — scoring.py:110–120` | ✓ Special `alert_msg` for item 14 confirmed at `scoring.py:49–50` | FASE 2 evaluation, special alert handling | N/A | FULL |
| §2 irb_approvals (#15) | ✓ IRB / ethical review documentation | `extracted_frontend_01.md §2.3 — scoring.py:22` | ✓ Key on `scoring.py:14` | FASE 2 evaluation | N/A | FULL |
| §2 declaration_llm_usage (#16) | ✓ LLM usage declaration, method vs. writing distinction | `extracted_frontend_01.md §2.3 — scoring.py:23` | ⚠ `scoring.py:23` is actually `"experimental_setting_details": "6. Experimental Setting / Details"` in CHECKLIST_LABELS. `"declaration_llm_usage"` is at `scoring.py:14`. Line reference is wrong. Key value is correct. | FASE 2 evaluation | N/A | PARTIAL |
| §3.1 Checklist Answer Values (Yes/No/N/A/empty) | ✓ All 4 values with scoring impact and evidence requirements | `extracted_frontend_01.md §7.1 — scoring.py:37; cross_ref §g_013 — scoring.py:110–120` | ✓ `get_checklist_health` logic confirmed: `"yes" in answer.lower()` → missing_evidence check; `"no" in answer.lower()` → is_no_justified check; N/A/empty → no risk | `get_checklist_health()` in scoring.py | ✓ All 4 values, semantics, evidence requirements documented | FULL |
| §3.2 Health Status Enum (valid/risk) | ✓ `valid` and `risk` with exact trigger conditions | `extracted_frontend_01.md §7.1 — scoring.py:122–123; cross_ref §g_013` | ✓ `scoring.py:122` = `status = "valid" if pending_count == 0 else "risk"` — exact match | `get_checklist_health()` return value, consumed by frontend | ✓ Both values with trigger conditions | FULL |
| §3.3 paper_type Enum | ✓ `"INVALID - Not ML/AI"` documented; valid = any non-INVALID string | `extracted_backend_core_01.md §2.2 — prompts.py:4; cross_ref §g_010` | ✓ Guard `startswith('INVALID')` confirmed in auditor.py context | FASE 1 extraction, pipeline short-circuit | ⚠ Only one named invalid value; no exhaustive enumeration of valid values (none exist — correct) | PARTIAL |
| §4.1 CHECKLIST_KEYS (16 values) | ✓ All 16 key strings listed with ordinal positions | `extracted_frontend_01.md §2.3 — scoring.py:8–23` | ✓ All 16 key values confirmed correct in `scoring.py:8–15` (FIDELITY: per-key line refs wrong for keys 3–16; see Fidelity Issues section) | `scoring.py`, FASE 2 LLM prompt, `get_checklist_health()` | ⚠ Missing "NeurIPS checklist item name" column per CHECK 4a (item names available in §2 and §4.2 but not co-located in §4.1) | PARTIAL |
| §4.2 CHECKLIST_LABELS (16 values) | ✓ All 16 display labels with key mapping | `extracted_frontend_01.md §2.3 — scoring.py:26–41` | ✗ FIDELITY_ISSUE: `scoring.py:26` is `"code_of_ethics": "9. Code of Ethics"`, not `"claims": "1. Claims"`. All label source refs are off by 8 (actual: scoring.py:18–34). Label STRING VALUES are correct. | Frontend display, audit results rendering | ✓ All 16 labels present with exact string values | PARTIAL |
| §4.3 Model Name Constants (8) | ✓ 8 constants with exact string values, alias relationships, usage context | `extracted_backend_core_01.md §2.1 — config.py:35–108` | ✓ All verified: EMBEDDING_MODEL_NAME="gemini-embedding-2" (line 35), MAP_MODEL_NAME="gemini-3.1-flash-lite-preview" (line 37), REDUCE_MODEL_NAME (39), EXTRACTION_MODEL_NAME (41), EVALUATION_MODEL_NAME (43), VERIFICATION_MODEL_NAME (45), MODEL_NAME=EXTRACTION_MODEL_NAME (107), RAG_MODEL_NAME=MAP_MODEL_NAME (108) | `LLMClient` instantiation, `PaperAuditor.__init__` | ✓ 6 primary + 2 alias, all with values and use-case context | FULL |
| §4.4 Temperature Constants (3) | ✓ 3 constants with values and caller context | `extracted_backend_core_01.md §2.1 — config.py:111–113` | ✓ AUDIT_TEMPERATURE=0.0 (line 111), CHAT_TEMPERATURE=0.2 (line 112), SOTA_TEMPERATURE=0.1 (line 113) — exact match | `AUDIT_CONFIG`, `CHAT_CONFIG`, `SOTA_CONFIG` dicts | ✓ All 3 with values and use-case context | FULL |
| §4.5 API Endpoint Strings | ✓ SEMANTIC_SCHOLAR_BASE_URL and Google Generative Language inline endpoint | `extracted_backend_core_01.md §2.1 — config.py:136; extracted_backend_skills_01.md §4.x — rag_extraction_skill.py` | ✓ SEMANTIC_SCHOLAR_BASE_URL = `"https://api.semanticscholar.org/graph/v1/paper/search"` at config.py:136. Google endpoint documented inline in extraction. | `SemanticScholarSearchSkill`, `HybridHyperparameterExtractionSkill` | ✓ | FULL |
| §4.6 SEMANTIC_SCHOLAR_* Constants (4) | ✓ BASE_URL, YEAR_RANGE, LIMIT, FIELDS with values and purpose | `extracted_backend_core_01.md §2.1 — config.py:136–139` | ✓ All 4 verified: BASE_URL (line 136), YEAR_RANGE="2023-2026" (137), LIMIT=5 (138), FIELDS="paperId,title,authors,year,citationCount,abstract,url" (139) | `SemanticScholarSearchSkill.execute()` | ✓ | FULL |
| §4.7 Other Named Constants | ✓ GOOGLE_API_KEY, AUDIT_CONFIG, CHAT_CONFIG, SOTA_CONFIG, TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION | `extracted_backend_core_01.md §2.1; cross_ref §g_023; cross_ref §g_008` | ✓ All verified: GOOGLE_API_KEY (config.py:30), AUDIT_CONFIG (config.py:116–122 — additional fields top_k/top_p/max_output_tokens documented). TITLE/SIDEBAR_IMAGE/SIDEBAR_DESCRIPTION at frontend/config.py:3–5 ✓ | Various — API auth, generation configs, UI constants | ⚠ `SEMANTIC_SCHOLAR_API_KEY` (config.py:31) is missing from this section | PARTIAL |
| §5.1 resultado ↔ evaluation | ✓ Full back-to-front renaming documented with transformation path | `extracted_backend_core_01.md §3.2 — auditor.py:78,~187–200; cross_ref §g_005` | ✓ `context['evaluation']` → flattened to `resultado` top-level keys by `MetadataAggregationSkill` | Frontend `st.session_state.resultado`, backend skill context | N/A | FULL |
| §5.2 extracted_info ↔ informacion_extraida | ✓ Rename path via MetadataAggregationSkill documented | `extracted_backend_skills_01.md §3.2; cross_ref §g_005; extracted_backend_core_01.md §3.2` | ✓ `context['extracted_info']` → `resultado['informacion_extraida']` via MetadataAggregationSkill | Frontend audit results RAG Ficha Técnica section | N/A | FULL |
| §5.3 puntuacion ↔ health / score | ✓ Three-name mapping with [GAP] for gauge call site | `extracted_frontend_01.md §5.2; cross_ref §g_005, §g_006` | ✓ `puntuacion` = return of `render_audit_results()` = `health` dict; `create_gauge_chart(score)` documented in gauge_chart.py. [GAP: call site connecting `health.pending_count` to numeric gauge score — unresolved] | `app.py`, `audit_results.py`, `gauge_chart.py` | N/A | PARTIAL |
| §5.4 md_text ↔ paper_text | ✓ Frontend session state key → backend skill context key fully documented | `cross_ref §g_004 — file_uploader.py:35–39,98–100; cross_ref §g_027; extracted_backend_core_01.md §3.2 — auditor.py:78` | ✓ `st.session_state['md_text']` → `auditor.audit(md_text)` → `context={'paper_text': paper_text, ...}` | `file_uploader.py`, `PaperAuditor.audit()`, `context['paper_text']` | N/A | FULL |
| §5.5 archivo_actual / file_hash | ✓ File deduplication logic, lazy initialization, MD5 hash | `cross_ref §g_004 — file_uploader.py:19–20; cross_ref §g_027` | ✓ `archivo_actual` stores filename, `file_hash` stores MD5 hex digest. File_uploader.py deduplication logic confirmed | `file_uploader.py` | N/A | FULL |
| §5.6 metricas ↔ computed scores | ✓ FASE 3 output → frontend result dict passthrough | `extracted_backend_core_01.md §3.2 — auditor.py:~178–185; cross_ref §g_005` | ✓ `MetricsCalculationSkill` → context `'metricas'` → verbatim copy to `resultado['metricas']` by MetadataAggregationSkill | Frontend 4-column metrics row in `audit_results.py` | N/A | FULL |
| Role Constants (N/A) | ✓ Explicitly documented as not applicable; single-user app confirmed | `extracted_backend_core_01.md §5 — Security` | ✓ Backend security section confirms "No HTTP authentication, session handling, or role-based access control" | N/A | N/A | FULL |

**Totals:** FULL: 35 | PARTIAL: 5 | MISSING: 0 | FIDELITY_ISSUE (within PARTIAL): 1 (§4.2)

---

## Enum / Constant Depth Detail

### CHECK 4a — CHECKLIST_KEYS enum

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| CHECKLIST_KEYS (§4.1) | 16 keys with: (a) key identifier, (b) ordinal position 1–16, (c) NeurIPS checklist item name | 16 keys with identifier + position. NeurIPS item names available via §2 table and §4.2 labels but NOT in §4.1 itself | NeurIPS human-readable item name column within §4.1 | DEPTH_GAP |

**Detail:** §4.1 provides `Index | Key Value | Source` columns. CHECK 4a requires each row to also include "the corresponding NeurIPS checklist item name." That name is the CHECKLIST_LABELS value (e.g., `"1. Claims"` for key `"claims"`). The information exists across §2 and §4.2 but is not co-located in §4.1, requiring the reader to cross-reference two other sections. The section header also claims source lines "scoring.py:8–23" but CHECKLIST_KEYS only spans lines 8–15 (16 keys total last at line 14), making individual per-key line references (scoring.py:8 through scoring.py:23) systematically inaccurate for keys 3–16.

### CHECK 4b — Checklist answer values

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| Answer values (§3.1) | Yes, No, N/A, empty — with semantic meaning + scoring impact + evidence/justification requirements | All 4 values documented with scoring impact, evidence requirements, and condition logic | None | COMPLETE |

### CHECK 4c — NeurIPS score tier labels (gauge chart)

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| Gauge quality tiers | 6 tiers with numeric boundaries and labels | 0 in glossary | Strong Accept (≥87.5), Accept (≥75), Borderline (≥62.5), Weak Reject (≥50), Reject (≥25), Strong Reject (<25) — all with hex colors | COVERAGE_GAP |

**Detail:** `frontend/components/gauge_chart.py:4–31` defines six quality tier labels and score boundaries used by `create_gauge_chart(score: float)`. These are NeurIPS-specific review decision labels that appear in `04_look_and_feel.md` (§5.4, lines 542–611) and `02_functional_frontend.md` (§9, lines 1218–1280) but are completely absent from `06_glossary.md`. These tiers are key domain terminology for the "Quality Score" displayed to reviewers.

### CHECK 4d — LLM model name constants

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| Model name constants (§4.3) | 8 constants with exact string values | 8 constants (EMBEDDING_MODEL_NAME, MAP_MODEL_NAME, REDUCE_MODEL_NAME, EXTRACTION_MODEL_NAME, EVALUATION_MODEL_NAME, VERIFICATION_MODEL_NAME, MODEL_NAME, RAG_MODEL_NAME) | None | COMPLETE |

**Note:** All 8 Gemini-based model name constants are documented with exact string values. 6 primary constants + 2 alias assignments confirmed against `config.py:35–108`.

### CHECK 4e — Temperature constants

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| Temperature constants (§4.4) | All temperature constants with numeric values and use-case context | 3 constants: AUDIT_TEMPERATURE=0.0, CHAT_TEMPERATURE=0.2, SOTA_TEMPERATURE=0.1 | None | COMPLETE |

### CHECK 4f — Semantic Scholar API constants

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| SEMANTIC_SCHOLAR_* constants (§4.6) | BASE_URL, rate-limit constants, field parameters, retry/timeout values | 4 constants: BASE_URL, YEAR_RANGE, LIMIT, FIELDS | SEMANTIC_SCHOLAR_API_KEY (config.py:31 — auth key constant); no explicit retry/timeout constants exist in source for this API | PARTIAL |

**Note:** No retry/timeout constants for the Semantic Scholar API exist in `config.py` (not a gap — they simply don't exist). `SEMANTIC_SCHOLAR_API_KEY` is in `config.py:31` and is missing from §4.7 Other Named Constants (it controls authentication to the API and is therefore a Semantic Scholar constant).

### CHECK 4g — Domain-specific terms

| Category | Expected Items | Found Items | Missing Items | Status |
|----------|---------------|-------------|---------------|--------|
| Domain concepts | NeurIPS checklist, compliance score, audit result, paper metadata, semantic similarity | NeurIPS checklist (§1.1, §2), audit result structure documented (§1.4, §5.1), paper_type classification (§1.2) | "compliance score" as explicit term (application uses valid/risk binary, not numeric compliance score — N/A); "semantic similarity" (ChromaDB cosine distance — documented within §1.7 but not as a standalone term) | MOSTLY COMPLETE |

---

## Forward Coverage (Specs → Source)

| Term | Source Reference | File Opened | Lines Read | Claim Confirmed | Status |
|------|-----------------|-------------|-----------|-----------------|--------|
| CHECKLIST_KEYS all 16 values | `scoring.py:8–15` | `frontend/utils/scoring.py` | 8–15 | ✓ All 16 keys match exactly | VERIFIED |
| CHECKLIST_LABELS all 16 labels | `scoring.py:26–41` (claimed) | `frontend/utils/scoring.py` | 17–34 (actual) | ✓ Label values correct; line refs wrong by 8 | CONTENT VERIFIED / LINE FIDELITY ISSUE |
| EMBEDDING_MODEL_NAME = "gemini-embedding-2" | `config.py:35` | `backend/common/config.py` | 35 | ✓ Exact match | VERIFIED |
| MAP_MODEL_NAME = "gemini-3.1-flash-lite-preview" | `config.py:37` | `backend/common/config.py` | 37 | ✓ Exact match | VERIFIED |
| REDUCE_MODEL_NAME = "gemini-3.1-flash-lite-preview" | `config.py:39` | `backend/common/config.py` | 39 | ✓ Exact match | VERIFIED |
| EXTRACTION_MODEL_NAME = "gemini-3.1-flash-lite-preview" | `config.py:41` | `backend/common/config.py` | 41 | ✓ Exact match | VERIFIED |
| EVALUATION_MODEL_NAME = "gemini-3.1-flash-lite-preview" | `config.py:43` | `backend/common/config.py` | 43 | ✓ Exact match | VERIFIED |
| VERIFICATION_MODEL_NAME = "gemini-3.1-flash-lite-preview" | `config.py:45` | `backend/common/config.py` | 45 | ✓ Exact match | VERIFIED |
| MODEL_NAME = EXTRACTION_MODEL_NAME | `config.py:107` | `backend/common/config.py` | 107 | ✓ `MODEL_NAME = EXTRACTION_MODEL_NAME` exact match | VERIFIED |
| RAG_MODEL_NAME = MAP_MODEL_NAME | `config.py:108` | `backend/common/config.py` | 108 | ✓ `RAG_MODEL_NAME = MAP_MODEL_NAME` exact match | VERIFIED |
| AUDIT_TEMPERATURE = 0.0 | `config.py:111` | `backend/common/config.py` | 111 | ✓ Exact match | VERIFIED |
| CHAT_TEMPERATURE = 0.2 | `config.py:112` | `backend/common/config.py` | 112 | ✓ Exact match | VERIFIED |
| SOTA_TEMPERATURE = 0.1 | `config.py:113` | `backend/common/config.py` | 113 | ✓ Exact match | VERIFIED |
| GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") | `config.py:30` | `backend/common/config.py` | 30 | ✓ Exact match | VERIFIED |
| SEMANTIC_SCHOLAR_BASE_URL (value string) | `config.py:136` | `backend/common/config.py` | 136 | ✓ `"https://api.semanticscholar.org/graph/v1/paper/search"` exact match | VERIFIED |
| SEMANTIC_SCHOLAR_YEAR_RANGE = "2023-2026" | `config.py:137` | `backend/common/config.py` | 137 | ✓ Exact match | VERIFIED |
| SEMANTIC_SCHOLAR_LIMIT = 5 | `config.py:138` | `backend/common/config.py` | 138 | ✓ Exact match | VERIFIED |
| SEMANTIC_SCHOLAR_FIELDS (value string) | `config.py:139` | `backend/common/config.py` | 139 | ✓ `"paperId,title,authors,year,citationCount,abstract,url"` exact match | VERIFIED |
| health status "valid" trigger: `pending_count == 0` | `scoring.py:122–123` | `frontend/utils/scoring.py` | 122 | ✓ `status = "valid" if pending_count == 0 else "risk"` | VERIFIED |
| health status "risk" trigger: `pending_count > 0` | `scoring.py:122–123` | `frontend/utils/scoring.py` | 122 | ✓ Same line, `else "risk"` | VERIFIED |
| AUDIT_CONFIG additional fields (top_k=1, top_p=0.1, max_output_tokens=16384) | `config.py:~115–122` | `backend/common/config.py` | 115–122 | ✓ `"response_mime_type": "application/json", "temperature": AUDIT_TEMPERATURE, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384` confirmed | VERIFIED (glossary notes these exist as dict but does not enumerate all fields — minor omission) |
| crowdsourcing_human_subjects special alert | `scoring.py:110–120` (cross_ref §g_013) | `frontend/utils/scoring.py` | 49–50 | ✓ `if key == "crowdsourcing_human_subjects" and not is_no_justified: alert_msg += " ⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."` | VERIFIED |
| paper_type INVALID guard: `startswith('INVALID')` | `auditor.py:~152` | `backend/services/auditor.py` | ~107–114 | ✓ `if extraction_result.get('invalid_paper', False)` confirmed | VERIFIED |
| TITLE = "💻 Auditor de Papers en Ciencias de la Computación" | `frontend/config.py:3` | `frontend/config.py` | 3 | ✓ Exact match | VERIFIED |

---

## Fidelity Issues

### FIDELITY-01: §4.2 CHECKLIST_LABELS — source line numbers off by 8

**Term:** §4.2 CHECKLIST_LABELS (all 16 entries)  
**Claimed source:** e.g., `"claims"` → `scoring.py:26`  
**File opened:** `frontend/utils/scoring.py`  
**Lines read:** 17–34  
**Actual content at scoring.py:26:** `"code_of_ethics": "9. Code of Ethics",` (the 9th label entry)  
**Claimed content:** "claims" → `"1. Claims"` label (which is actually at `scoring.py:18`)  
**Systematic offset:** All 16 label source references are off by 8 (claimed lines 26–41, actual lines 18–34).  
**Impact:** LOW for understanding (label values are correct); MEDIUM for tooling (any automated tool following the line reference would retrieve the wrong label).  
**Note:** The `[GAP_ID: hall_*]` exemption does NOT apply here — this is a line-numbering error, not a purged hallucination.

### FIDELITY-02: §4.1 CHECKLIST_KEYS — per-key line references wrong for keys 3–16

**Term:** §4.1 CHECKLIST_KEYS table, rows 3–16  
**Claimed source examples:** `"theory_assumptions_proofs"` → `scoring.py:10`; `"declaration_llm_usage"` → `scoring.py:23`  
**File opened:** `frontend/utils/scoring.py`  
**Lines read:** 8–15  
**Actual content at scoring.py:10:** `"experimental_result_reproducibility", "open_access_data_code",` (not `theory_assumptions_proofs`)  
**Actual content at scoring.py:23:** `"experimental_setting_details": "6. Experimental Setting / Details",` (inside CHECKLIST_LABELS, not CHECKLIST_KEYS)  
**Key values are correct:** All 16 key strings verified present in `scoring.py:9–14`.  
**Root cause:** The writer assigned one line number per key incrementing by 1, but the source packs 3–5 keys per line (lines 9–14).  
**Impact:** LOW for understanding; MEDIUM for source traceability.

---

## Coverage Gaps

### COVERAGE-01: NeurIPS gauge chart score tier labels completely absent

**Missing term:** NeurIPS quality tier vocabulary: `"Strong Accept"` (≥87.5%), `"Accept"` (≥75%), `"Borderline"` (≥62.5%), `"Weak Reject"` (≥50%), `"Reject"` (≥25%), `"Strong Reject"` (<25%)  
**Source:** `frontend/components/gauge_chart.py:14–31`  
**Used in:** `04_look_and_feel.md` (§5.4, table at ~line 571), `02_functional_frontend.md` (§9, table at ~line 1240)  
**Impact:** HIGH — these are the primary domain-facing quality verdict labels presented to users. A reader of the glossary cannot understand what "Strong Accept" or "Borderline" means without consulting the look-and-feel spec. These terms should appear in the glossary's §3 (Status Enums) as a fourth enum group with the 6 values, their score boundaries, and associated colors.  
**Remediation:** Add §3.4 "NeurIPS Quality Tier Labels" to the glossary, listing all 6 tiers with score boundaries (e.g., `Strong Accept: score ≥ 87.5`), display label, and hex color.

### COVERAGE-02: SEMANTIC_SCHOLAR_API_KEY constant absent from §4.7

**Missing constant:** `SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")`  
**Source:** `backend/common/config.py:31`  
**Used in:** `01_data_model.md` (line 200), `03_technical_specs.md` (lines 107, 269, 521, 530), `07_module_index.md` (lines 128, 181), `08_dependency_graph.md` (line 210)  
**Impact:** MEDIUM — the glossary §4.7 lists `GOOGLE_API_KEY` (the peer API key constant) but omits `SEMANTIC_SCHOLAR_API_KEY`. The constant is optional (Semantic Scholar API is callable without it, but rate-limited), which is important context for operators.  
**Remediation:** Add `SEMANTIC_SCHOLAR_API_KEY` to the §4.7 table alongside `GOOGLE_API_KEY`, noting that it is optional and controls `"x-api-key"` header in `SemanticScholarSearchSkill.execute`.

---

## Depth Gaps

### DEPTH-01: §4.1 CHECKLIST_KEYS missing NeurIPS item name column (CHECK 4a)

**Term:** §4.1 CHECKLIST_KEYS  
**Required by CHECK 4a:** Each key must include (a) key identifier, (b) ordinal position 1–16, (c) corresponding NeurIPS checklist item name.  
**Found:** Columns `Index | Key Value | Source` — items (a) and (b) are present.  
**Missing in §4.1:** Item (c) — the human-readable NeurIPS checklist item name (e.g., `"1. Claims"` for key `"claims"`).  
**Mitigation:** The NeurIPS item names ARE accessible via §2 (full table) and §4.2 (CHECKLIST_LABELS), but they are not co-located in §4.1, requiring the reader to cross-reference two other sections.  
**Remediation:** Add a `NeurIPS Item Name` column to the §4.1 table (values taken directly from CHECKLIST_LABELS).

---

## Orphan Terms (Warning)

All 40 glossary terms were cross-checked against the other seven output spec files. **No orphan terms were found.** Every term defined in `06_glossary.md` is directly referenced or used in at least one of: `01_data_model.md`, `02_functional_backend.md`, `02_functional_frontend.md`, `03_technical_specs.md`, `04_look_and_feel.md`, `05_test_scenarios.md`, `07_module_index.md`, or `08_dependency_graph.md`.

Notable high-frequency terms across all specs: `CHECKLIST_KEYS`, `CHECKLIST_LABELS`, `paper_type`, `red_flags`, `resultado`, `extracted_info`, `metricas`, `SEMANTIC_SCHOLAR_*`, `MAP_MODEL_NAME`, `AUDIT_TEMPERATURE`.

The "Role Constants — Not Applicable" entry is unique to the glossary but serves a useful negative-specification purpose and cannot be considered orphaned.

---

## Undocumented Terms (Warning)

The following domain terms appear in other spec files but are **absent from `06_glossary.md`**:

| Undocumented Term | Appears In | Significance |
|-------------------|-----------|--------------|
| `SEMANTIC_SCHOLAR_API_KEY` | `01_data_model.md:200`, `03_technical_specs.md:107,269,521`, `07_module_index.md:128,181`, `08_dependency_graph.md:210` | High — API authentication constant, optional but operationally significant |
| NeurIPS quality tiers (`Strong Accept`, `Accept`, `Borderline`, `Weak Reject`, `Reject`, `Strong Reject`) | `04_look_and_feel.md:571–578`, `02_functional_frontend.md:1240–1247` | High — primary user-facing quality verdict vocabulary |
| `LLMClient` | `03_technical_specs.md` (multiple sections), `01_data_model.md`, `07_module_index.md` | Medium — central infrastructure class; absent from glossary but well-covered in technical specs |
| `time.sleep(2)` inter-fragment delay | `02_functional_backend.md` (MAP phase rate-limit mitigation) | Low — implementation detail, not domain terminology |
| `AUDIT_CONFIG` field members (`top_k`, `top_p`, `max_output_tokens`, `response_mime_type`) | `01_data_model.md`, `03_technical_specs.md` | Low — glossary mentions the dict but does not enumerate all fields; other specs do |

---

## Quality Assessment

The `06_glossary.md` is a comprehensive and well-structured domain glossary that substantially fulfills its purpose. Its principal strengths are: (1) complete and verified enumeration of all 16 CHECKLIST_KEYS and CHECKLIST_LABELS with exact string values from source; (2) thorough documentation of all 8 model-name constants, 3 temperature constants, 4 Semantic Scholar API constants, and cross-application constants (AUDIT_CONFIG, CHAT_CONFIG, SOTA_CONFIG); (3) the six cross-domain equivalence mappings (especially `resultado↔evaluation` and `extracted_info↔informacion_extraida`) which are critical for frontend–backend bridge understanding and not documented anywhere else; (4) accurate characterization of the audit pipeline phases with correct skill names, context keys, and phase ordering; and (5) domain-accurate definitions for all enumerated checklist answer values (Yes/No/N/A/empty) with complete scoring semantics.

The remediation priority order is: **HIGH** — add §3.4 NeurIPS Quality Tier Labels (6 tiers with boundaries, currently absent despite being primary user-facing vocabulary); **MEDIUM** — add `SEMANTIC_SCHOLAR_API_KEY` to §4.7 (constant referenced in 4 other spec files, conspicuously absent given `GOOGLE_API_KEY` is present); **LOW** — correct source line references in §4.1 and §4.2 (content is correct, only line numbers are wrong); **LOW** — add NeurIPS item name column to §4.1 CHECKLIST_KEYS table. None of these gaps undermine the accuracy of the content already present; the glossary provides a reliable reference for all enumerated terms. The overall verdict of **needs_review** reflects these specific actionable gaps rather than any systemic quality failure.
