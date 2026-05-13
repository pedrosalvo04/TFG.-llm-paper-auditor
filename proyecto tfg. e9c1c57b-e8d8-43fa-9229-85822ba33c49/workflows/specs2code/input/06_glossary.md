# 06 — Domain Glossary

Specification for the NeurIPS 2026 Reproducibility Audit Application.
Generated from: `extracted_backend_core_01.md`, `extracted_backend_skills_01.md`,
`extracted_frontend_01.md`, `extracted_root_tests_scratch_01.md`,
`cross_ref_resolution_cross_ref_root_to_backend.md`,
`cross_ref_resolution_cross_ref_root_to_frontend.md`.

---

## 1. Domain Concepts

### 1.1 NeurIPS 2026 Reproducibility Checklist

**Definition:** A structured set of 16 transparency and reproducibility criteria that NeurIPS 2026 requires submitted papers to satisfy. The checklist covers claims, limitations, theoretical proofs, experimental reproducibility, open access to data and code, statistical significance reporting, compute resource disclosure, ethical conduct, broader societal impact, safeguards, asset licensing, crowdsourcing practices, IRB approvals, and LLM usage declarations.

**Purpose:** The application automates auditing of submitted papers against all 16 items. For each item, the LLM evaluates the paper text and returns an answer (`"Yes"`, `"No"`, or `"N/A"`) with evidence or justification. Items with missing evidence or unjustified negative answers are flagged as risks that may lead to Desk Reject.

**Programmatic representation:** The 16 items are encoded as Python lists `CHECKLIST_KEYS` (machine-readable key strings) and `CHECKLIST_LABELS` (human-readable display strings), both defined in `frontend/utils/scoring.py`. At evaluation time, the LLM returns a dict keyed by these 16 keys.

(Source: `extracted_frontend_01.md`, §2.3 — scoring.py:8–34; `extracted_backend_core_01.md`, §2.2 — prompts.py:378)

---

### 1.2 paper_type — Valid vs. Invalid Classification Logic

**Definition:** `paper_type` is a string field returned by the LLM during the extraction phase (FASE 1). It classifies whether the submitted paper belongs to the ML/AI domain that the checklist targets.

**Valid/invalid determination:**
- **Invalid:** `extracted_info.get('paper_type', '').startswith('INVALID')` evaluates to `True`.
  - Known invalid value: `"INVALID - Not ML/AI"` — returned when the paper does not involve ML/AI training, research, or experimentation.
  - When invalid, the LLM short-circuits and returns only `{"paper_type": "INVALID - Not ML/AI", "invalid_reason": "<explanation>"}`. No further checklist evaluation is performed.
  - The audit pipeline sets `result['invalid_paper'] = True` and propagates this flag to the frontend result dict.
- **Valid:** Any `paper_type` string that does NOT start with `"INVALID"`. The audit continues through all remaining phases.

**Source of value:** The extraction prompt (`get_extraction_prompt`) instructs the LLM to classify the paper. The guard is inlined at the top of the prompt text. (Source: `extracted_backend_core_01.md`, §2.2 — prompts.py:4; `cross_ref_resolution_cross_ref_root_to_backend.md`, §RESOLUTION SUMMARY [g_010])

---

### 1.3 red_flags — Structure, Keys, and Meaning

**Definition:** `red_flags` is a Python `dict` that accumulates signals detected by the regex-based detection skills before the LLM extraction prompt is assembled. It is initialised as `{}` in `PaperAuditor.audit()` and populated by each detection skill that runs.

**Structure:** Keys are string identifiers. Key naming conventions determine which keys are included in the LLM prompt:
- Keys starting with `'_'` are **internal/private** — filtered OUT of the `flags_section` block injected into the extraction prompt. Example: `_hp_snippets` (a dict of hyperparameter text snippets used to build the RAG query context).
- Keys NOT starting with `'_'` are **rendered** as inline context inside the `flags_section` block in the extraction prompt body.
- Keys prefixed with `tiene_`, `menciona_`, `cantidad_`, `puntos_` are boolean or numeric flags capturing detection results (e.g., `tiene_repositorio`, `menciona_datos_propietarios`). These are NOT counted as "critical" risk indicators by the checklist scoring logic.

**Special key `_hp_snippets`:** A dict mapping hyperparameter names to their extracted text snippets. Built by `HyperparameterDetectionSkill` and consumed by `HybridHyperparameterExtractionSkill` (FASE 1.5) to seed the RAG query context. (Source: `extracted_backend_skills_01.md`, §3.x — regex_detection_skills.py; `extracted_backend_core_01.md`, §2.2 — prompts.py:4)

---

### 1.4 Audit Pipeline Phases

The `PaperAuditor.audit(paper_text, status_callback=None)` method executes the following phases in order:

#### FASE 1 — Information Extraction

**Domain meaning:** The paper text is fragmented into up to 4 balanced sections using Docling markdown header boundaries (`\n(?=#+ )`). Each fragment is sent to the LLM independently (MAP phase). The resulting per-fragment extraction dicts are then consolidated into a single DEFINITIVE MASTER JSON (REDUCE phase). The skill responsible is `InformationExtractionSkill`.

**Output context key:** `extracted_info` — a dict containing all extracted fields from the LLM schema (paper_type, code, data, hyperparameters, hardware, statistics, architecture, baseline_comparison, software_versions, limitations_quality, etc.).

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:60–180; `extracted_backend_skills_01.md`, §3.2 — auditor_skills.py:21; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_015)

#### FASE 1.5 — Hybrid Hyperparameter Extraction

**Domain meaning:** A deep, targeted extraction of numerical hyperparameters that is more accurate than the general MAP/REDUCE extraction. Called "hybrid" because it combines three techniques: (1) regex-based detection (`HyperparameterDetectionSkill`) to locate candidate text snippets, (2) RAG (Retrieval-Augmented Generation) using Google embedding API + ChromaDB in-memory vector store to retrieve the most relevant paper chunks per query, and (3) Pydantic schema-constrained LLM MAP/REDUCE on the retrieved chunks to produce a validated structured output. The responsible skill is `HybridHyperparameterExtractionSkill`.

**Output context key:** `extracted_hyperparameters_hybrid` — a Pydantic-validated dict of hyperparameter values.

(Source: `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py:27; `extracted_backend_core_01.md`, §3.2 — auditor.py:~115–140)

#### FASE 2 — Reproducibility Evaluation

**Domain meaning:** The full `extracted_info` dict and `red_flags` are passed to the LLM acting as a "Senior Area Chair for NeurIPS 2026". The LLM evaluates each of the 16 NeurIPS checklist items and returns structured answers with evidence or justification. The responsible skill is `ReproducibilityEvaluationSkill`.

**Output context key:** `evaluation` — a dict keyed by the 16 CHECKLIST_KEYS, each value being `{"answer": str, "evidence": str, "justification": str, "is_no_justified": bool}`.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~145–160; §2.2 — prompts.py:378)

#### FASE 2.5 — Strict Verification (False-Negative Check)

**Domain meaning:** A second LLM pass acting as "Auditor 2". This phase reviews the FASE 2 evaluation results and checks for false negatives (items incorrectly marked "Yes" without real evidence) and false positives (items incorrectly marked "No" that should be "N/A"). The responsible skill is `ChecklistVerificationSkill`.

**Output:** Updates or supplements the `evaluation` dict with corrected answers.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~162–175; `extracted_backend_skills_01.md`, §3.x — auditor_skills.py:319)

#### FASE 3 — Metrics Calculation

**Domain meaning:** Computes aggregate metrics from the evaluated checklist items: reproducibility score, open access score, statistics score, compute resource score, license score, crowdsourcing compliance score. The responsible skill is `MetricsCalculationSkill` (no LLM client required — pure computation).

**Output context key:** `metricas` — a dict of computed float scores.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~178–185)

#### FASE 4 — Metadata Aggregation

**Domain meaning:** The final assembly phase. `MetadataAggregationSkill` merges all context keys produced by previous phases into a single flat result dict that matches the shape expected by the frontend (`st.session_state.resultado`). This includes flattening the `evaluation` dict keys to top-level keys, and renaming `extracted_info` to `informacion_extraida`. No LLM client required — pure data assembly.

**Output:** The final `resultado` dict returned by `PaperAuditor.audit()`.

(Source: `extracted_backend_core_01.md`, §3.2 — auditor.py:~187–200)

---

### 1.5 MAP/REDUCE Extraction Strategy

**Definition:** A divide-and-conquer LLM extraction pattern used in both FASE 1 (`InformationExtractionSkill`) and FASE 1.5 (`HybridHyperparameterExtractionSkill`).

- **MAP phase:** The paper text (or RAG-retrieved chunks) is split into up to 4 balanced fragments. Each fragment is processed independently by the LLM using a map-extraction prompt. This parallelises extraction and avoids exceeding the LLM context window for long papers. Between fragment calls, `time.sleep(2)` is used to avoid rate limiting.
- **REDUCE phase:** All MAP results (a list of per-fragment extraction dicts) are sent together to the LLM with a reduce-consolidation prompt. The LLM merges them into a single DEFINITIVE MASTER JSON, resolving conflicts by preferring the most complete information from any fragment.

**Fragment construction algorithm:**
1. Split paper text on Docling markdown header boundaries: `re.split(r'\n(?=#+ )', '\n' + paper_text_norm)`.
2. Accumulate sections into balanced fragments targeting `total_chars / 4` chars per fragment; at most 3 cut points.
3. Fallback for flat documents (no headers detected): `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)`, first 4 chunks.

(Source: `extracted_backend_skills_01.md`, §3.2 — auditor_skills.py:21; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_015)

---

### 1.6 Hybrid Hyperparameter Extraction — What Makes It "Hybrid"

**Definition:** The term "hybrid" refers to the combination of three distinct extraction techniques within `HybridHyperparameterExtractionSkill`:

1. **Regex detection (pre-processing):** `HyperparameterDetectionSkill` runs regex patterns on the full paper text to detect candidate hyperparameter snippets. These snippets are stored in `red_flags['_hp_snippets']`.
2. **RAG retrieval:** The paper text is chunked and embedded using the Google Generative Language API (`gemini-embedding-2`). Chunks are stored in a ChromaDB in-memory vector store (ephemeral — rebuilt on every call, never persisted). 13 fixed query strings are used to retrieve the top 10 chunks per query. Retrieved chunks are deduplicated by minimum cosine distance.
3. **Schema-constrained LLM MAP/REDUCE:** The deduplicated RAG chunks are used as the MAP fragments. The REDUCE phase produces output validated against a Pydantic schema for hyperparameter fields.

This combination produces higher-precision hyperparameter extraction than FASE 1's general extraction, which processes the whole paper uniformly.

(Source: `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py:27)

---

### 1.7 RAG (Retrieval-Augmented Generation) — Scope and Purpose

**Definition in this application:** RAG is used exclusively in FASE 1.5 (`HybridHyperparameterExtractionSkill`). It is NOT used for the general extraction (FASE 1) or the evaluation/verification phases.

**Scope:**
- **Embedding model:** `gemini-embedding-2` via the Google Generative Language API (`batchEmbedContents` endpoint).
- **Vector store:** ChromaDB, in-memory only. A new ChromaDB instance is created on every call to `HybridHyperparameterExtractionSkill.execute()`. No persistence between audit runs.
- **Query strategy:** 13 fixed domain-specific query strings targeting hyperparameter-related content (learning rate, batch size, optimizer, warmup, etc.).
- **Retrieval:** Top 10 chunks per query; deduplicated by minimum cosine distance across all 13 queries.
- **Output:** The retrieved chunks become the MAP fragments for the subsequent LLM MAP/REDUCE extraction.

**Components that use RAG:** `HybridHyperparameterExtractionSkill` (rag_extraction_skill.py).
**Components that do NOT use RAG:** `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `ChecklistVerificationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `PaperChatbot`, `SotaAnalyzer`.

(Source: `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py:27; `extracted_backend_core_01.md`, §2.1 — config.py:35)

---

## 2. NeurIPS 2026 Checklist Items (all 16 with definitions)

All 16 items are defined in `CHECKLIST_KEYS` and `CHECKLIST_LABELS` in `frontend/utils/scoring.py` and are evaluated by the `ReproducibilityEvaluationSkill` in FASE 2. Keys and labels are reproduced exactly as they appear in the extraction.

| # | Key | Label | Definition | Source |
|---|-----|-------|------------|--------|
| 1 | `claims` | `"1. Claims"` | Verifies that the paper's claims are consistent with its experimental results and limitations. The LLM checks whether the paper clearly states what it claims to demonstrate and whether the evidence matches. | `extracted_frontend_01.md`, §2.3 — scoring.py:8; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 2 | `limitations` | `"2. Limitations"` | Verifies that the paper includes an explicit discussion of its limitations. Checks for a dedicated limitations section or clear statements of scope restrictions. | `extracted_frontend_01.md`, §2.3 — scoring.py:10; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 3 | `theory_assumptions_proofs` | `"3. Theory, Assumptions & Proofs"` | Verifies that theoretical results include stated assumptions and, where applicable, proofs or references to proofs. Checks for appendix references and whether assumptions are enumerated. | `extracted_frontend_01.md`, §2.3 — scoring.py:12; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 4 | `experimental_result_reproducibility` | `"4. Experimental Result Reproducibility"` | Verifies that the paper provides enough information to reproduce its experimental results: code, datasets, hyperparameters, and procedural details. | `extracted_frontend_01.md`, §2.3 — scoring.py:14; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 5 | `open_access_data_code` | `"5. Open Access to Data and Code"` | Verifies that the paper provides open access to its datasets and code, or explains why access is restricted (proprietary data, licensing restrictions, etc.). | `extracted_frontend_01.md`, §2.3 — scoring.py:16; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 6 | `experimental_setting_details` | `"6. Experimental Setting / Details"` | Verifies that the experimental setup is described in sufficient detail: hardware, software versions, hyperparameters, training procedure, evaluation metrics. | `extracted_frontend_01.md`, §2.3 — scoring.py:18; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 7 | `experiment_statistical_significance` | `"7. Experiment Statistical Significance"` | Verifies that results are reported with appropriate statistical analysis: confidence intervals, significance tests, number of experimental runs. | `extracted_frontend_01.md`, §2.3 — scoring.py:20; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 8 | `experiments_compute_resource` | `"8. Experiments Compute Resource"` | Verifies that the paper discloses the compute resources used: GPU/CPU type, count, memory, training time, carbon footprint, energy consumption. | `extracted_frontend_01.md`, §2.3 — scoring.py:22; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 9 | `code_of_ethics` | `"9. Code of Ethics"` | Verifies that the paper acknowledges and complies with the NeurIPS Code of Ethics, particularly when the work involves human participants, data collection, or social impact. | `extracted_frontend_01.md`, §2.3 — scoring.py:24; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 10 | `broader_impacts` | `"10. Broader Impacts"` | Verifies that the paper includes a broader impact statement discussing potential positive and negative societal consequences of the research. | `extracted_frontend_01.md`, §2.3 — scoring.py:26; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 11 | `safeguards` | `"11. Safeguards"` | Verifies that the paper describes safeguards implemented to mitigate potential harms or dual-use risks of the proposed system or dataset. | `extracted_frontend_01.md`, §2.3 — scoring.py:28; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 12 | `licenses` | `"12. Licenses"` | Verifies that all third-party assets (datasets, code, models) used in the paper have their licenses explicitly named and that the paper complies with those licenses. | `extracted_frontend_01.md`, §2.3 — scoring.py:30; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 13 | `assets` | `"13. Assets"` | Verifies that all assets introduced or used by the paper (datasets, models, code) are properly identified and that release or access information is provided. | `extracted_frontend_01.md`, §2.3 — scoring.py:31; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 14 | `crowdsourcing_human_subjects` | `"14. Crowdsourcing & Human Subjects"` | Verifies that any crowdsourcing or human participant study includes: instructions provided to participants, compensation details (with mandatory minimum compensation per NeurIPS ethics rules), and consent information. Note: a special warning `"⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."` is appended to the `alert_msg` for this item when flagged. | `extracted_frontend_01.md`, §2.3 — scoring.py:32; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:110–120 |
| 15 | `irb_approvals` | `"15. IRB Approvals"` | Verifies that the paper documents IRB (Institutional Review Board) approval or equivalent ethical review for studies involving human subjects. | `extracted_frontend_01.md`, §2.3 — scoring.py:33; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |
| 16 | `declaration_llm_usage` | `"16. Declaration of LLM Usage"` | Verifies that the paper includes a declaration of any LLM usage in the research methodology, distinguishing between LLMs used as part of the method vs. LLMs used for writing assistance. | `extracted_frontend_01.md`, §2.3 — scoring.py:34; `extracted_backend_core_01.md`, §2.2 — prompts.py:378 |

---

## 3. Status Enums

### 3.1 Checklist Answer Values

Answer values are produced by the LLM in FASE 2 (`ReproducibilityEvaluationSkill`) and FASE 2.5 (`ChecklistVerificationSkill`). They are stored per checklist item in the `evaluation` dict and are consumed by `get_checklist_health()` for scoring.

Comparison in `get_checklist_health()` uses `.lower()` (case-insensitive): `"yes" in answer.lower()` and `"no" in answer.lower()`.

| Value | Display / Internal Meaning | Scoring Impact | Source |
|-------|---------------------------|----------------|--------|
| `'Yes'` | Item is compliant — the paper satisfies this checklist requirement | Risk flagged if `evidence` AND `justification` are both empty (`missing_evidence = True`, `pending_count += 1`) | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:110–120 |
| `'No'` | Item is not compliant — the paper does NOT satisfy this requirement | Risk flagged if `is_no_justified` is `False` OR `justification` is empty (`pending_justification = True`, `pending_count += 1`) | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:110–120 |
| `'N/A'` | Item is not applicable to this paper | No risk flagged. No `pending_count` increment. Item displays without alert. | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |
| `''` (empty string) | Not answered — LLM returned empty or the key is absent from evaluation dict | No risk flagged. Item displays with `answer` shown as `"—"`. | `extracted_frontend_01.md`, §7.1 — scoring.py:37; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |

**Evaluation dict per-item schema** (as passed to `get_checklist_health`):
```
{
  "answer":          str,           # "Yes" / "No" / "N/A" / ""
  "justification":   str,
  "evidence":        str,
  "is_no_justified": bool or str    # True/False or "true"/"false"
}
```
(Source: `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:37)

---

### 3.2 Health Status Enum

The health status is the top-level verdict returned by `get_checklist_health(evaluation: dict) -> dict`. The `status` field value determines the displayed audit verdict.

| Value | Meaning | Trigger Condition | Source |
|-------|---------|-------------------|--------|
| `'valid'` | All 16 checklist items have acceptable evidence or justification. The paper passes the reproducibility audit. | `pending_count == 0` (no items with missing evidence or missing justification) | `extracted_frontend_01.md`, §7.1 — scoring.py:122–123; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |
| `'risk'` | One or more checklist items are flagged for missing evidence (for `"Yes"` answers) or missing/unjustified negatives (for `"No"` answers). The paper is at risk of Desk Reject. | `pending_count > 0` | `extracted_frontend_01.md`, §7.1 — scoring.py:122–123; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 |

**Early-exit guard:** When `evaluation` is falsy (`None`, `{}`, etc.), `get_checklist_health` returns immediately: `{"status": "risk", "items": [], "pending_count": 0, "total": 0}`. (Source: `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_013 — scoring.py:56–62)

---

### 3.3 paper_type Enum

The `paper_type` field is returned by the LLM during FASE 1 extraction. Its value determines whether the audit proceeds or short-circuits.

| Value | Valid/Invalid | Description | Source |
|-------|---------------|-------------|--------|
| `'INVALID - Not ML/AI'` | **Invalid** | The submitted paper does not belong to the ML/AI research domain that the NeurIPS checklist targets. The audit short-circuits; no checklist evaluation is performed. | `extracted_backend_core_01.md`, §2.2 — prompts.py:4; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_010 |
| Any string not starting with `'INVALID'` | **Valid** | The paper is classified as an ML/AI paper. The audit proceeds through all 6 phases. | `extracted_backend_core_01.md`, §3.2 — auditor.py:~152; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_010 |

**Note:** No other specific valid `paper_type` string values were present in the extraction. The prompt instructs the LLM to classify the paper type in free text, and only the `startswith('INVALID')` guard is programmatically checked. (Source: `extracted_backend_core_01.md`, §2.2 — prompts.py:4)

---

### 3.4 NeurIPS Quality Tier Labels

These are the six quality verdict labels presented to users in the gauge chart. They represent the primary domain-facing assessment of a paper's reproducibility quality score as rendered by `create_gauge_chart(score)` in `frontend/components/gauge_chart.py`. Each tier has a score boundary, display label, and associated hex color used for the bar element of the Plotly gauge indicator.

| Tier | Display Label | Score Boundary | Hex Color | Color Name | Source |
|------|--------------|----------------|-----------|------------|--------|
| 1 (highest) | `"Strong Accept"` | score ≥ 87.5 | `#00aa00` | dark green | `frontend/components/gauge_chart.py:14–16` |
| 2 | `"Accept"` | 75 ≤ score < 87.5 | `#00cc44` | green | `frontend/components/gauge_chart.py:17–19` |
| 3 | `"Borderline"` | 62.5 ≤ score < 75 | `#ffcc00` | yellow | `frontend/components/gauge_chart.py:20–22` |
| 4 | `"Weak Reject"` | 50 ≤ score < 62.5 | `#ff9900` | orange | `frontend/components/gauge_chart.py:23–25` |
| 5 | `"Reject"` | 25 ≤ score < 50 | `#ff4b4b` | red | `frontend/components/gauge_chart.py:26–28` |
| 6 (lowest) | `"Strong Reject"` | score < 25 | `#cc0000` | dark red | `frontend/components/gauge_chart.py:29–31` |

**Usage:** The tier label is injected into the Plotly chart title as `f"Quality Score<br><sub>{label}</sub>"` and the hex color is applied to the gauge bar. The same tier vocabulary is used in `04_look_and_feel.md` (§5.4 gauge chart description) and `02_functional_frontend.md` (§9 audit results rendering). (Source: `frontend/components/gauge_chart.py:4–37`)

---

## 4. Named Constants Glossary

### 4.1 CHECKLIST_KEYS

All 16 values in declaration order, exactly as they appear in `scoring.py`. Multiple keys are packed per source line (lines 9–14 of `scoring.py`); the `Source` column reflects the actual line where each key string appears.

| Index | Key Value | NeurIPS Item Name | Source |
|-------|-----------|-------------------|--------|
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 2 | `"limitations"` | `"2. Limitations"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 3 | `"theory_assumptions_proofs"` | `"3. Theory, Assumptions & Proofs"` | `extracted_frontend_01.md`, §2.3 — scoring.py:9 |
| 4 | `"experimental_result_reproducibility"` | `"4. Experimental Result Reproducibility"` | `extracted_frontend_01.md`, §2.3 — scoring.py:10 |
| 5 | `"open_access_data_code"` | `"5. Open Access to Data and Code"` | `extracted_frontend_01.md`, §2.3 — scoring.py:10 |
| 6 | `"experimental_setting_details"` | `"6. Experimental Setting / Details"` | `extracted_frontend_01.md`, §2.3 — scoring.py:11 |
| 7 | `"experiment_statistical_significance"` | `"7. Experiment Statistical Significance"` | `extracted_frontend_01.md`, §2.3 — scoring.py:11 |
| 8 | `"experiments_compute_resource"` | `"8. Experiments Compute Resource"` | `extracted_frontend_01.md`, §2.3 — scoring.py:12 |
| 9 | `"code_of_ethics"` | `"9. Code of Ethics"` | `extracted_frontend_01.md`, §2.3 — scoring.py:12 |
| 10 | `"broader_impacts"` | `"10. Broader Impacts"` | `extracted_frontend_01.md`, §2.3 — scoring.py:12 |
| 11 | `"safeguards"` | `"11. Safeguards"` | `extracted_frontend_01.md`, §2.3 — scoring.py:13 |
| 12 | `"licenses"` | `"12. Licenses"` | `extracted_frontend_01.md`, §2.3 — scoring.py:13 |
| 13 | `"assets"` | `"13. Assets"` | `extracted_frontend_01.md`, §2.3 — scoring.py:13 |
| 14 | `"crowdsourcing_human_subjects"` | `"14. Crowdsourcing & Human Subjects"` | `extracted_frontend_01.md`, §2.3 — scoring.py:13 |
| 15 | `"irb_approvals"` | `"15. IRB Approvals"` | `extracted_frontend_01.md`, §2.3 — scoring.py:14 |
| 16 | `"declaration_llm_usage"` | `"16. Declaration of LLM Usage"` | `extracted_frontend_01.md`, §2.3 — scoring.py:14 |

---

### 4.2 CHECKLIST_LABELS

All 16 display labels in declaration order, mapped to their corresponding key. Labels are exactly as they appear in `scoring.py`. The `CHECKLIST_LABELS` dict is declared at `scoring.py:17`; each key-value entry occupies one line (lines 18–33).

| Index | Key | Label | Source |
|-------|-----|-------|--------|
| 1 | `"claims"` | `"1. Claims"` | `extracted_frontend_01.md`, §2.3 — scoring.py:18 |
| 2 | `"limitations"` | `"2. Limitations"` | `extracted_frontend_01.md`, §2.3 — scoring.py:19 |
| 3 | `"theory_assumptions_proofs"` | `"3. Theory, Assumptions & Proofs"` | `extracted_frontend_01.md`, §2.3 — scoring.py:20 |
| 4 | `"experimental_result_reproducibility"` | `"4. Experimental Result Reproducibility"` | `extracted_frontend_01.md`, §2.3 — scoring.py:21 |
| 5 | `"open_access_data_code"` | `"5. Open Access to Data and Code"` | `extracted_frontend_01.md`, §2.3 — scoring.py:22 |
| 6 | `"experimental_setting_details"` | `"6. Experimental Setting / Details"` | `extracted_frontend_01.md`, §2.3 — scoring.py:23 |
| 7 | `"experiment_statistical_significance"` | `"7. Experiment Statistical Significance"` | `extracted_frontend_01.md`, §2.3 — scoring.py:24 |
| 8 | `"experiments_compute_resource"` | `"8. Experiments Compute Resource"` | `extracted_frontend_01.md`, §2.3 — scoring.py:25 |
| 9 | `"code_of_ethics"` | `"9. Code of Ethics"` | `extracted_frontend_01.md`, §2.3 — scoring.py:26 |
| 10 | `"broader_impacts"` | `"10. Broader Impacts"` | `extracted_frontend_01.md`, §2.3 — scoring.py:27 |
| 11 | `"safeguards"` | `"11. Safeguards"` | `extracted_frontend_01.md`, §2.3 — scoring.py:28 |
| 12 | `"licenses"` | `"12. Licenses"` | `extracted_frontend_01.md`, §2.3 — scoring.py:29 |
| 13 | `"assets"` | `"13. Assets"` | `extracted_frontend_01.md`, §2.3 — scoring.py:30 |
| 14 | `"crowdsourcing_human_subjects"` | `"14. Crowdsourcing & Human Subjects"` | `extracted_frontend_01.md`, §2.3 — scoring.py:31 |
| 15 | `"irb_approvals"` | `"15. IRB Approvals"` | `extracted_frontend_01.md`, §2.3 — scoring.py:32 |
| 16 | `"declaration_llm_usage"` | `"16. Declaration of LLM Usage"` | `extracted_frontend_01.md`, §2.3 — scoring.py:33 |

---

### 4.3 Model Name Constants

All 6 distinct model name constants plus the 2 alias assignments, as defined in `backend/common/config.py`.

| Constant Name | Value (string) | Is Alias Of | Purpose / Usage Context | Source |
|---------------|---------------|-------------|------------------------|--------|
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | — (primary) | Google embedding model used by `HybridHyperparameterExtractionSkill` for RAG chunk embedding via the Google Generative Language API. Referenced in `PaperAuditor.__init__` log message. | `extracted_backend_core_01.md`, §2.1 — config.py:35 |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | — (primary) | LLM for the MAP phase of extraction (both general and RAG-based). Assigned to `self.rag_map_llm` in `PaperAuditor.__init__`. | `extracted_backend_core_01.md`, §2.1 — config.py:37 |
| `REDUCE_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | — (primary) | LLM for the REDUCE (consolidation) phase. Assigned to `self.rag_reduce_llm` in `PaperAuditor.__init__`. Also used as direct fallback model in `InformationExtractionSkill` REDUCE step. | `extracted_backend_core_01.md`, §2.1 — config.py:39; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_015 |
| `EXTRACTION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | — (primary) | LLM for general information extraction (FASE 1). Assigned to `self.extraction_llm` in `PaperAuditor.__init__`. | `extracted_backend_core_01.md`, §2.1 — config.py:41 |
| `EVALUATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | — (primary) | LLM for reproducibility evaluation (FASE 2 — Senior Area Chair role). Assigned to `self.evaluation_llm` in `PaperAuditor.__init__`. | `extracted_backend_core_01.md`, §2.1 — config.py:43 |
| `VERIFICATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | — (primary) | LLM for strict verification (FASE 2.5 — Auditor 2 role). Assigned to `self.verification_llm` in `PaperAuditor.__init__`. | `extracted_backend_core_01.md`, §2.1 — config.py:45 |
| `MODEL_NAME` | `EXTRACTION_MODEL_NAME` (resolves to `"gemini-3.1-flash-lite-preview"`) | Alias of `EXTRACTION_MODEL_NAME` | Default model name for `LLMClient.__init__` when `model_name=None`. Also used as fallback in `InformationExtractionSkill` REDUCE step. | `extracted_backend_core_01.md`, §2.1 — config.py:107; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_023 |
| `RAG_MODEL_NAME` | `MAP_MODEL_NAME` (resolves to `"gemini-3.1-flash-lite-preview"`) | Alias of `MAP_MODEL_NAME` | Default model name for RAG-based LLM calls in `HybridHyperparameterExtractionSkill`. | `extracted_backend_core_01.md`, §2.1 — config.py:108; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_023 |

---

### 4.4 Temperature Constants

All 3 temperature constants, as defined in `backend/common/config.py`.

| Constant Name | Value | Used In (context) | Source |
|---------------|-------|-------------------|--------|
| `AUDIT_TEMPERATURE` | `0.0` | `AUDIT_CONFIG` generation config dict, used for all LLM calls in `PaperAuditor` (extraction, evaluation, verification, RAG map/reduce). Value `0.0` ensures deterministic, reproducible LLM outputs for the audit pipeline. | `extracted_backend_core_01.md`, §2.1 — config.py:111 |
| `CHAT_TEMPERATURE` | `0.2` | `CHAT_CONFIG` generation config dict, used by `PaperChatbot` conversational responses (`ConversationalResponseSkill`). Higher temperature produces more natural-sounding chat responses. | `extracted_backend_core_01.md`, §2.1 — config.py:112 |
| `SOTA_TEMPERATURE` | `0.1` | `SOTA_CONFIG` generation config dict, used by `SotaAnalyzer` for literature analysis queries (`ThematicCoverageSkill`, `QueryGenerationSkill`, `CoverageGapAnalysisSkill`). | `extracted_backend_core_01.md`, §2.1 — config.py:113 |

---

### 4.5 API Endpoint Strings

All API endpoint string constants found in the extraction.

| Constant Name | Value | Protocol / Service | Source |
|---------------|-------|-------------------|--------|
| `SEMANTIC_SCHOLAR_BASE_URL` | `"https://api.semanticscholar.org/graph/v1/paper/search"` | HTTPS / Semantic Scholar Graph API v1 — used by `SemanticScholarSearchSkill` for SOTA literature search | `extracted_backend_core_01.md`, §2.1 — config.py:136 |
| *(inline constant — no named module-level variable)* | `"https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL_NAME}:batchEmbedContents"` | HTTPS / Google Generative Language API — used by `HybridHyperparameterExtractionSkill` to batch-embed paper chunks for RAG retrieval. The `{EMBEDDING_MODEL_NAME}` is substituted at call time with the value `"gemini-embedding-2"`. | `extracted_backend_skills_01.md`, §4.x — rag_extraction_skill.py |

---

### 4.6 SEMANTIC_SCHOLAR_* Constants

All `SEMANTIC_SCHOLAR_*` constants found in the extraction.

| Constant Name | Value | Purpose | Source |
|---------------|-------|---------|--------|
| `SEMANTIC_SCHOLAR_BASE_URL` | `"https://api.semanticscholar.org/graph/v1/paper/search"` | Base URL for Semantic Scholar paper search API requests in `SemanticScholarSearchSkill.execute()` | `extracted_backend_core_01.md`, §2.1 — config.py:136 |
| `SEMANTIC_SCHOLAR_YEAR_RANGE` | `"2023-2026"` | Year filter applied to Semantic Scholar queries to restrict results to recent papers for SOTA analysis | `extracted_backend_core_01.md`, §2.1 — config.py:137 |
| `SEMANTIC_SCHOLAR_LIMIT` | `5` | Maximum number of papers returned per Semantic Scholar query | `extracted_backend_core_01.md`, §2.1 — config.py:138 |
| `SEMANTIC_SCHOLAR_FIELDS` | `"paperId,title,authors,year,citationCount,abstract,url"` | Comma-separated list of fields requested from the Semantic Scholar API per result; used as the `fields` query parameter | `extracted_backend_core_01.md`, §2.1 — config.py:139 |

---

### 4.7 Other Named Constants

Additional named constants from the extraction that do not fit the above sub-sections.

| Constant Name | Value | Purpose | Source |
|---------------|-------|---------|--------|
| `GOOGLE_API_KEY` | `os.getenv("GOOGLE_API_KEY")` — runtime value from environment | Google Gemini API key. Required for all LLM calls via `LLMClient` and for the embedding API in RAG. If `None` or empty, `LLMClient.__init__` raises `ValueError`. | `extracted_backend_core_01.md`, §2.1 — config.py:30; `cross_ref_resolution_cross_ref_root_to_backend.md`, §g_023 |
| `SEMANTIC_SCHOLAR_API_KEY` | `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` — runtime value from environment | Semantic Scholar API key. **Optional** — the Semantic Scholar API is callable without it, but unauthenticated requests are rate-limited. When set, it is injected as the `"x-api-key"` HTTP header in `SemanticScholarSearchSkill.execute()`. Referenced in `01_data_model.md` (line 200), `03_technical_specs.md` (lines 107, 269, 521, 530), `07_module_index.md` (lines 128, 181), and `08_dependency_graph.md` (line 210). | `backend/common/config.py:31` |
| `AUDIT_CONFIG` | `{"temperature": 0.0, ...}` (generation config dict) | Generation configuration dict passed to `LLMClient` instances for the audit pipeline (extraction, evaluation, verification, RAG). Uses `AUDIT_TEMPERATURE = 0.0`. | `extracted_backend_core_01.md`, §2.1 — config.py:~115 |
| `CHAT_CONFIG` | `{"temperature": 0.2, ...}` (generation config dict) | Generation configuration dict for chatbot LLM calls. Uses `CHAT_TEMPERATURE = 0.2`. | `extracted_backend_core_01.md`, §2.1 — config.py:~116 |
| `SOTA_CONFIG` | `{"temperature": 0.1, ...}` (generation config dict) | Generation configuration dict for SOTA analysis LLM calls. Uses `SOTA_TEMPERATURE = 0.1`. | `extracted_backend_core_01.md`, §2.1 — config.py:~117 |
| `TITLE` | `"💻 Auditor de Papers en Ciencias de la Computación"` | Page title displayed via `st.title(TITLE)` in `app.py:25`. | `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_008 — config.py:3 |
| `SIDEBAR_IMAGE` | `"https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Association_for_Computing_Machinery_%28ACM%29_logo.svg/1200px-Association_for_Computing_Machinery_%28ACM%29_logo.svg.png"` | URL of ACM logo (Wikipedia CDN) displayed in sidebar via `st.image(SIDEBAR_IMAGE, width=150)`. | `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_008 — config.py:4 |
| `SIDEBAR_DESCRIPTION` | `"Herramienta desarrollada para automatizar la auditoría de reproducibilidad en artículos de Ciencias de la Computación usando LLMs."` | Descriptive text shown in the sidebar via `st.write(SIDEBAR_DESCRIPTION)`. | `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_008 — config.py:5 |

---

## 5. Cross-Domain Equivalences

This section documents cases where the same data object, field, or concept is referred to by different names in different parts of the codebase (frontend vs. backend, session state vs. skill context, Spanish vs. English naming). Cross-reference files are the primary source for this section.

---

**1. `resultado` ↔ `evaluation`**

**Term A:** `resultado` (Context: `frontend/app.py`, `frontend/utils/session_state.py`, `frontend/components/audit_results.py`, `frontend/components/file_uploader.py`)

**Term B:** `evaluation` (Context: `backend/skills/auditor_skills.py` skill context dict key; `get_evaluation_prompt` return schema)

**Description:** The full audit result dict (produced by `PaperAuditor.audit()`) is stored in `st.session_state.resultado` on the frontend. Within the backend skill pipeline, the dict containing the 16 checklist item evaluations is stored under the context key `'evaluation'` (populated by `ReproducibilityEvaluationSkill` and `ChecklistVerificationSkill`). `MetadataAggregationSkill` merges the `evaluation` sub-dict into the top-level `resultado` by flattening the 16 checklist item keys to the top level of the result dict. Thus `resultado['claims']` corresponds to `context['evaluation']['claims']` in the skill pipeline.

**Source:** `extracted_backend_core_01.md`, §3.2 — auditor.py:78,~187–200; `extracted_backend_skills_01.md`, §3.x — auditor_skills.py:319; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_005 — audit_results.py:90

---

**2. `extracted_info` ↔ `informacion_extraida`**

**Term A:** `extracted_info` (Context: `backend/skills/auditor_skills.py` skill context key — `InformationExtractionSkill` return dict; also used as parameter name in `get_evaluation_prompt(extracted_info, ...)`)

**Term B:** `informacion_extraida` (Context: `frontend` — key in `st.session_state.resultado`; key in the audit result dict passed to `render_audit_results`)

**Description:** `InformationExtractionSkill.execute()` returns `{'extracted_info': {...}, ...}`. The skill pipeline propagates this as `context['extracted_info']`. `MetadataAggregationSkill.execute()` renames this to `informacion_extraida` in the final result dict. On the frontend, `resultado['informacion_extraida']` is used to render the RAG Ficha Técnica section in `audit_results.py`.

**Source:** `extracted_backend_skills_01.md`, §3.2 — auditor_skills.py:21; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_005 — audit_results.py:78; `extracted_backend_core_01.md`, §3.2 — auditor.py:~187

---

**3. `puntuacion` ↔ `health` / `score`**

**Term A:** `puntuacion` (Context: `frontend/app.py:66` — local variable name for the return value of `render_audit_results(resultado, uploaded_file)`)

**Term B:** `health` (Context: `frontend/components/audit_results.py:284` — variable name for the return value of `get_checklist_health(resultado)` within `render_audit_results`)

**Term C:** `score` (Context: `frontend/components/audit_results.py` — parameter name of `create_gauge_chart(score)` — the numeric gauge value)

**Description:** In `app.py`, the variable `puntuacion` is assigned the return value of `render_audit_results()`, which is the `health` dict (`{"status": str, "pending_count": int, "total": int, "items": list}`). The `health` dict is then passed as the third argument to `generate_report(resultado, uploaded_file, puntuacion)`. The function `create_gauge_chart(score)` takes a numeric value 0–100; [GAP: the call site for `create_gauge_chart` was not found in any extraction file — the connection between `puntuacion`/`health` and the numeric `score` input to the gauge chart is unresolved].

**Source:** `extracted_frontend_01.md`, §5.2 — audit_results.py:284; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_005 — audit_results.py:90; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_006 — audit_results.py:287

---

**4. `md_text` ↔ `paper_text`**

**Term A:** `md_text` (Context: `st.session_state['md_text']` — Streamlit session state key in `frontend/components/file_uploader.py` and `frontend/utils/session_state.py`)

**Term B:** `paper_text` (Context: `backend/skills/auditor_skills.py` skill context dict key; `backend/services/auditor.py` — parameter name of `PaperAuditor.audit(paper_text, ...)` and `context['paper_text']`)

**Description:** When the user uploads a file, `file_uploader.py` extracts the text content and stores it as `st.session_state['md_text']`. This string is then passed to `st.session_state.auditor.audit(st.session_state.md_text)`. Inside `PaperAuditor.audit()`, it is stored as `context = {'paper_text': paper_text, 'red_flags': {}}`. All backend skills that consume the paper text read it from `context['paper_text']`. When the same text is passed to the chatbot (`render_chatbot(md_text)`) and SOTA analyzer (`render_sota_analysis(md_text)`), the function parameter is also named `md_text` in the frontend but passed as `paper_text` in the backend skill context.

**Source:** `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_004 — file_uploader.py:35–39,98–100; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_027 — session_state.py:7; `extracted_backend_core_01.md`, §3.2 — auditor.py:78

---

**5. `archivo_actual` / `file_hash` — deduplication keys (additional equivalence)**

**Term A:** `archivo_actual` (Context: `st.session_state['archivo_actual']` — stores the filename of the currently processed file)

**Term B:** `file_hash` (Context: `st.session_state['file_hash']` — stores the MD5 hex digest of the currently processed file's byte content)

**Description:** These two session state keys together implement file deduplication in `file_uploader.py`. A new audit is only triggered if either the filename (`uploaded_file.name != archivo_actual`) or the content hash (`hashlib.md5(uploaded_file.getvalue()).hexdigest() != file_hash`) differs from the last processed file. This prevents re-running the expensive 6-phase audit pipeline when the user re-selects the same file. These keys are NOT initialised by `initialize_session_state()`; they are set lazily on first upload.

**Source:** `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_004 — file_uploader.py:19–20; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_027 — session_state.py:7

---

**6. `metricas` (resultado key) ↔ computed scores (FASE 3 output)**

**Term A:** `metricas` (Context: key in `st.session_state.resultado` / `render_audit_results` — used to render the 4-column metrics row in the audit results UI)

**Term B:** Computed score fields from `MetricsCalculationSkill.execute()` (Context: `backend/skills/auditor_skills.py` — FASE 3 output under context key `'metricas'`)

**Description:** `MetricsCalculationSkill` (no LLM client, pure computation) calculates aggregate reproducibility scores from the `evaluation` dict and stores them in the skill context as `metricas`. `MetadataAggregationSkill` copies this dict verbatim to the final `resultado` dict as the key `metricas`. The frontend reads `resultado['metricas']` to render the summary metrics row (4 columns) in `audit_results.py`.

**Source:** `extracted_backend_core_01.md`, §3.2 — auditor.py:~178–185; `cross_ref_resolution_cross_ref_root_to_frontend.md`, §g_005 — audit_results.py:90

---

## Role Constants

**Not applicable — this application has no user roles or role-based access control.**

The application is a single-user tool accessible without authentication. There is no login, session-based identity management, or permission system. All Streamlit session state keys are scoped to the browser session automatically by Streamlit, not to any user identity.

This is confirmed by the backend security section, which explicitly states: "No HTTP authentication, session handling, or role-based access control exists in this cluster." (Source: `extracted_backend_core_01.md`, §5 — Security)

[GAP: no extraction explicitly confirms absence of roles in the frontend layer — inferred from absence of any role/auth logic in all 6 extraction files and confirmed by the backend security section]
