## FIX LOG
Agent: targeted_fix_backend_core_g002
Run timestamp: 2026-05-08T11:39:51Z

| gap_id | original gap detail                                              | source file:line consulted                              | correction applied                                                         |
|--------|------------------------------------------------------------------|---------------------------------------------------------|----------------------------------------------------------------------------|
| g_002  | File-index table described auditor.py as "4-phase …orchestrator" | backend/services/auditor.py:86 (phase label region) | Changed description to "6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator" |

# Extraction Report — Agent ext_backend_core_01
## Cluster: cluster_backend_core_01
## Scope: Core backend infrastructure (Python)

---

## 1. File Index

| # | File | Lines | Purpose |
|---|------|-------|---------|
| 1 | `backend/__init__.py` | 1 | Package docstring only: `"""Backend modular para el Auditor de Papers"""` |
| 2 | `backend/common/config.py` | 140 | Centralized configuration: API keys, model names, temperature constants, generation config dicts, Semantic Scholar settings |
| 3 | `backend/common/llm_client.py` | 77 | `LLMClient` class — Google Gemini wrapper with retry/backoff logic |
| 4 | `backend/common/prompts.py` | 540 | All LLM prompt templates: extraction, map, reduce, evaluation signals, evaluation, verification |
| 5 | `backend/common/__init__.py` | 1 | Package docstring only: `"""Componentes comunes compartidos"""` |
| 6 | `backend/services/auditor.py` | 205 | `PaperAuditor` class — 6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator |
| 7 | `backend/services/chatbot.py` | 62 | `PaperChatbot` class + `Chatbot` alias — skill-based Q&A chatbot over audited papers |
| 8 | `backend/services/pdf_parser.py` | 86 | `convert_pdf_to_markdown` function — Docling-based chunked PDF→Markdown converter |
| 9 | `backend/services/sota_analyzer.py` | 102 | `SotaAnalyzer` class — 5-step state-of-the-art analysis pipeline |
| 10 | `backend/services/__init__.py` | 1 | Package docstring only: `"""Servicios de lógica de negocio"""` |
| 11 | `backend/utils/logger.py` | 59 | `Colors`, `ColoredFormatter`, `get_logger` — centralized colored logging |
| 12 | `backend/utils/__init__.py` | 1 | Package docstring only: `"""Utilidades del backend"""` |

---

## 2. Constants, Enums, and Configuration Values (Category 5)

### 2.1 config.py — All Configuration Keys

SOURCE file: `backend/common/config.py`

**Environment variable suppression (module-level side effects, lines 8–25):**

| Operation | Value set | SOURCE |
|-----------|-----------|--------|
| `os.environ["TRANSFORMERS_VERBOSITY"]` | `"error"` | `config.py:8` |
| `os.environ["TOKENIZERS_PARALLELISM"]` | `"false"` | `config.py:9` |
| `warnings.filterwarnings("ignore")` | all warnings suppressed | `config.py:10` |
| `logging.getLogger("transformers").setLevel(logging.ERROR)` | ERROR level | `config.py:11` |
| `logging.getLogger("httpx").addFilter(CleanNetworkLogs())` | custom filter | `config.py:22` |
| `logging.getLogger("RapidOCR").setLevel(logging.WARNING)` | WARNING level | `config.py:23` |
| `logging.getLogger("docling").setLevel(logging.WARNING)` | WARNING level | `config.py:24` |
| `logging.getLogger("onnxruntime").setLevel(logging.ERROR)` | ERROR level | `config.py:25` |

**`CleanNetworkLogs` filter (lines 14–20):**
- Class inheriting `logging.Filter`
- `filter(self, record)`: calls `record.getMessage()`, checks if `"huggingface.co"` is in `msg` AND (`"HEAD"` in `msg` OR `"GET"` in `msg`); if true returns `False` (suppresses); otherwise returns `True`
- SOURCE: `config.py:14`

**API Keys (loaded via `load_dotenv()` at line 27):**

| Constant | Type | Environment Variable | Default | SOURCE |
|----------|------|---------------------|---------|--------|
| `GOOGLE_API_KEY` | `str \| None` | `"GOOGLE_API_KEY"` | `None` (no default) | `config.py:30` |
| `SEMANTIC_SCHOLAR_API_KEY` | `str \| None` | `"SEMANTIC_SCHOLAR_API_KEY"` | `None` (no default) | `config.py:31` |

**Model Name Constants (all hardcoded strings, not env-overridable):**

| Constant | Type | Value | Purpose | SOURCE |
|----------|------|-------|---------|--------|
| `EMBEDDING_MODEL_NAME` | `str` | `"gemini-embedding-2"` | RAG embeddings | `config.py:35` |
| `MAP_MODEL_NAME` | `str` | `"gemini-3.1-flash-lite-preview"` | Triage and Map phase extraction | `config.py:37` |
| `REDUCE_MODEL_NAME` | `str` | `"gemini-3.1-flash-lite-preview"` | Orchestration and Consolidation (Reduce phase) | `config.py:39` |
| `EXTRACTION_MODEL_NAME` | `str` | `"gemini-3.1-flash-lite-preview"` | Initial extraction (General Analysis) | `config.py:41` |
| `EVALUATION_MODEL_NAME` | `str` | `"gemini-3.1-flash-lite-preview"` | Final evaluation (Senior Area Chair) | `config.py:43` |
| `VERIFICATION_MODEL_NAME` | `str` | `"gemini-3.1-flash-lite-preview"` | Strict verification (Auditor 2) | `config.py:45` |
| `MODEL_NAME` | `str` | `= EXTRACTION_MODEL_NAME` (alias) | Default model for `LLMClient` | `config.py:107` |
| `RAG_MODEL_NAME` | `str` | `= MAP_MODEL_NAME` (alias) | Default model for RAG | `config.py:108` |

Note: Lines 48–105 contain a multi-line docstring listing all available Gemini models for reference; not executable code.

**Temperature Constants:**

| Constant | Type | Value | Used by | SOURCE |
|----------|------|-------|---------|--------|
| `AUDIT_TEMPERATURE` | `float` | `0.0` | `AUDIT_CONFIG` | `config.py:111` |
| `CHAT_TEMPERATURE` | `float` | `0.2` | `CHAT_CONFIG` | `config.py:112` |
| `SOTA_TEMPERATURE` | `float` | `0.1` | `SOTA_CONFIG` | `config.py:113` |

**Generation Config Dictionaries:**

`AUDIT_CONFIG` — SOURCE: `config.py:116`
```python
{
    "response_mime_type": "application/json",
    "temperature": 0.0,       # AUDIT_TEMPERATURE
    "top_k": 1,
    "top_p": 0.1,
    "max_output_tokens": 16384
}
```
Used by: `PaperAuditor.__init__` for all 5 LLM clients (`extraction_llm`, `evaluation_llm`, `rag_map_llm`, `rag_reduce_llm`, `verification_llm`)

`CHAT_CONFIG` — SOURCE: `config.py:125`
```python
{
    "temperature": 0.2        # CHAT_TEMPERATURE
}
```
Used by: `PaperChatbot.__init__`

`SOTA_CONFIG` — SOURCE: `config.py:130`
```python
{
    "response_mime_type": "application/json",
    "temperature": 0.1        # SOTA_TEMPERATURE
}
```
Used by: `SotaAnalyzer.__init__`

**Semantic Scholar API Constants:**

| Constant | Type | Value | SOURCE |
|----------|------|-------|--------|
| `SEMANTIC_SCHOLAR_BASE_URL` | `str` | `"https://api.semanticscholar.org/graph/v1/paper/search"` | `config.py:136` |
| `SEMANTIC_SCHOLAR_YEAR_RANGE` | `str` | `"2023-2026"` | `config.py:137` |
| `SEMANTIC_SCHOLAR_LIMIT` | `int` | `5` | `config.py:138` |
| `SEMANTIC_SCHOLAR_FIELDS` | `str` | `"paperId,title,authors,year,citationCount,abstract,url"` | `config.py:139` |

---

### 2.2 prompts.py — All Prompt Templates (full text)

SOURCE file: `backend/common/prompts.py`

#### Prompt 1: `get_extraction_prompt(paper_text, red_flags)` — SOURCE: `prompts.py:4`

**Signature:** `def get_extraction_prompt(paper_text: str, red_flags: dict) -> str`

**Parameters:**
- `paper_text`: full paper text injected at end of prompt via `{paper_text}`
- `red_flags`: dict; extracts `red_flags.get('_hp_snippets', {})` to build `snippets_section`; filters keys not starting with `'_'` to build `flags_section`

**Used by:** `InformationExtractionSkill.execute()` (outside cluster)

**Full prompt template (static portions):**
```
CRITICAL: This system ONLY evaluates ML/AI papers (neural networks, deep learning, machine learning).

FIRST: Determine if this paper involves ML/AI training. If NO:
RETURN ONLY: {"paper_type": "INVALID - Not ML/AI", "invalid_reason": "explanation"}

If YES, continue with EXHAUSTIVE extraction below.
    
REASONING INSTRUCTIONS:
- Analyze technical ratios (e.g., if the paper mentions 0.13 million H800 hours, evaluate if that reflects the reported training efficiency).
- Look for hidden hyperparameters in tables or parenthetical remarks.
- Differentiate between pre-training and fine-tuning settings.
- Use the 'thought_process' field to document your reasoning step-by-step before filling the structured fields.

You are an expert information extractor for ML/AI papers. Your job is to extract
SPECIFIC factual information - not opinions - from every section of the paper.

ANALYSIS STRATEGY - Read the paper section by section:
1. Abstract + Introduction -> claims, scope, contributions
2. Methods/Architecture -> model details, design choices
3. Training/Optimization -> hyperparameters, optimizer, schedule
4. Data -> datasets, preprocessing, splits
5. Experiments/Results -> baselines, metrics, tables
6. Implementation -> code, hardware, software versions
7. Appendix -> often contains hyperparameter tables, environmental data
8. Limitations/Broader Impact -> quality and specificity

CRITICAL RULES:
- Search APPENDIX and ALL tables (Table 1 through Table 10+) before marking NOT FOUND
- Look specifically for "Data Availability Statement", "Dataset access", or URLs to model hubs (HuggingFace, etc.)
- If paper says "standard settings" or "not disclosed" -> extract as vague_phrase, NOT as the actual value
- For software, look for any mentions of frameworks (PyTorch, JAX), libraries (Transformers, DeepSpeed), or specific training protocols.
{snippets_section}
{flags_section}

EXTRACT THE FOLLOWING (respond "NOT FOUND" ONLY after exhaustive search):

1. CODE: repository_url, negative_phrase, dependencies, instructions (yes/no), release_mention
2. DATA: dataset_name, access_url, negative_phrase, preprocessing, splits, release_mention
3. HYPERPARAMETERS: optimizer, learning_rate, batch_size, epochs, training_steps, total_tokens, warmup, weight_decay, betas, epsilon, vague_phrase, table_reference
4. HARDWARE: gpu_cpu, num_gpus, memory, time, carbon_footprint, energy_consumption, pue, throughput (tokens/sec), latency_metrics
5. STATISTICS: confidence_intervals (yes/no), significance_tests (yes/no), num_runs
6. ARCHITECTURE: description (layers, dims, heads), weights_available, release_mention
7. BASELINE COMPARISON: compared_models (list), has_comparative_tables (yes/no), same_metrics (yes/no), results_section
8. SOFTWARE: framework_versions, python_version, cuda_version, dependency_file (yes/no)
9. LIMITATIONS: has_section (yes/no), specific_points (list), quantified_issues (yes/no)
10. PROBLEMATIC PHRASES: Extract TEXTUALLY any phrase with "cannot release", "proprietary", "confidential", "not available", "restricted", "competitive concerns". NOTE: Ignore phrases regarding "restricted compute/budget/resources".
11. THEORY_AND_PROOFS: theoretical derivations, mathematical formulations, proof sketches, assumptions.
12. BROADER_IMPACTS: "Impact Statement", "Broader Impacts", "Societal Impact" section (often in APPENDIX).
13. AI_ASSISTANTS_IN_WRITING: declaration regarding AI tools (ChatGPT, Claude, etc.) for writing.
14. LLM_IN_METHODOLOGY: language models used for automated data annotation, filtering, evaluation.
15. HUMAN_SUBJECTS_AND_CROWDSOURCING: human annotators, crowdsourcing, SFT datasets with human labels.
16. LICENSES: explicit licenses (CC-BY, MIT, Apache) for datasets, code, or models used or released.
17. CODE_OF_ETHICS: "Code of Ethics", "Ethics Statement", or "Ethical Considerations" section.
```

**Return JSON schema (fields):**
`thought_process`, `paper_type`, `invalid_reason`, `code` {`repository_url`, `negative_phrase`, `dependencies`, `instructions`, `release_mention`}, `data` {`dataset_name`, `access_url`, `negative_phrase`, `preprocessing`, `splits`, `release_mention`}, `hyperparameters` {`optimizer`, `learning_rate`, `batch_size`, `epochs`, `training_steps`, `total_tokens`, `warmup`, `weight_decay`, `betas`, `epsilon`, `vague_phrase`, `table_reference`}, `hardware` {`gpu_cpu`, `num_gpus`, `memory`, `time`, `carbon_footprint`, `energy_consumption`, `pue`, `throughput`, `latency_metrics`}, `statistics` {`confidence_intervals`, `significance_tests`, `num_runs`}, `architecture` {`description`, `weights_available`, `release_mention`}, `baseline_comparison` {`compared_models`, `has_comparative_tables`, `same_metrics`, `results_section`}, `software_versions` {`framework`, `python_version`, `cuda_version`, `dependency_file`}, `limitations_quality` {`has_section`, `specific_points`, `quantified_issues`}, `problematic_phrases`, `theory_and_proofs` {`has_theoretical_results`, `assumptions_stated`, `proofs_included`, `appendix_reference`}, `broader_impacts_extraction` {`has_impact_statement`, `appendix_reference`, `concerns_discussed`}, `llm_usage_extraction` {`models_used_in_methodology`, `purpose_in_methodology`, `used_for_writing`, `writing_declaration_quote`}, `human_subjects_extraction` {`uses_human_annotation`, `compensation_details`, `instructions_provided`}, `licenses_extraction` {`assets_used`, `licenses_named`, `missing_licenses_for_some_assets`}, `context_mapping`

---

#### Prompt 2: `get_map_extraction_prompt(fragment_text)` — SOURCE: `prompts.py:184`

**Signature:** `def get_map_extraction_prompt(fragment_text: str) -> str`

**Parameters:** `fragment_text` — single fragment of the paper text; injected via `{fragment_text}`

**Used by:** `InformationExtractionSkill` map phase (outside cluster)

**Full prompt template (static portion):**
```
You are a Senior ML Researcher performing a deep technical extraction on a FRAGMENT of a scientific paper.

TASK:
Extract EVERY technical detail, hyperparameter, architectural choice, and experimental result found in this fragment.

REASONING INSTRUCTIONS:
- Identify specific architectural components (e.g., "Gated Attention", "MoE configuration", "Normalization layers").
- Capture ALL hyperparameters even if they seem minor (betas, epsilon, warmup steps, weight decay).
- Note specific benchmarks and their corresponding results if present in tables or text.
- Document your 'thought_process' specifically for this fragment.

FRAGMENT:
{fragment_text}

STRUCTURE:
Return a structured JSON with the following standard keys (add more if needed to preserve detail):
- "paper_title", "authors", "context_mapping", "code", "data",
- "hyperparameters" (optimizer, LR, batch size, and technical variants),
- "hardware", "statistics", "architecture" (layers, gating, MoE, dims),
- "baseline_comparison", "software_versions", "limitations_quality",
- "problematic_phrases", "theory_and_proofs", "broader_impacts_extraction",
- "llm_usage_extraction", "human_subjects_extraction", "licenses_extraction",
- "thought_process"

If a field is not mentioned in this fragment, use "NOT FOUND" or an empty list [].
BE EXHAUSTIVE. Do not summarize; extract verbatim data where possible.
```

---

#### Prompt 3: `get_reduce_extraction_prompt(map_results)` — SOURCE: `prompts.py:228`

**Signature:** `def get_reduce_extraction_prompt(map_results: list) -> str`

**Parameters:** `map_results` — list of dicts from map phase; serialized via `json.dumps(map_results, indent=2)` and injected into `{map_results_serialized}` position

**Used by:** `InformationExtractionSkill` reduce phase (outside cluster)

**Full prompt template (static portion):**
```
You are a Senior AI Researcher and Meta-Reviewer. Your task is to CONSOLIDATE multiple partial extractions (MAP phase) from a scientific paper into a single DEFINITIVE MASTER JSON.

INPUT DATA:
{json.dumps(map_results, indent=2)}

CRITICAL OBJECTIVE: 
ZERO INFORMATION LOSS. You must synthesize a master database that preserves EVERY unique technical detail found across all fragments.

CONSOLIDATION RULES:
1. RESOLVE CONFLICTS: Prioritize the most specific value; explicitly stated 'Hyperparameters' table takes precedence.
2. ARCHITECTURE MERGE: Combine all architectural details from all fragments.
3. HYPERPARAMETER SYNTHESIS: Aggregate all training settings; list per-phase (Pre-training vs SFT) if different.
4. DATA & HARDWARE: Combine token counts, dataset names, GPU types, total compute hours.
5. EXPERIMENTAL RESULTS: Union of all benchmarks and metrics; preserve specific numbers (e.g., MMLU: 70.2, HumanEval: 45.1).
6. CONTEXT MAPPING: Deduplicated, ordered list of ALL sections across all fragments.
7. THOUGHT PROCESS: Final synthesis of the paper's technical rigor and reproducibility.

FINAL STRUCTURE (standard keys, preserving all sub-details):
"paper_title", "authors", "context_mapping", "code", "data", "hyperparameters",
"hardware", "statistics", "architecture", "baseline_comparison", "software_versions",
"limitations_quality", "problematic_phrases", "theory_and_proofs",
"broader_impacts_extraction", "llm_usage_extraction", "human_subjects_extraction",
"licenses_extraction", "thought_process"

RETURN THE CONSOLIDATED MASTER JSON ONLY. Ensure the JSON is perfectly formatted and valid.
```

---

#### Prompt 4: `get_evaluation_signals(extracted_info)` — SOURCE: `prompts.py:273`

**Signature:** `def get_evaluation_signals(extracted_info: dict) -> dict`

**Not a prompt template.** Computes a `signals` dict consumed by `get_evaluation_prompt`. Logic:

- Reads `extracted_info.get('code')` as `code_info` dict; reads `extracted_info.get('data')` as `data_info` dict; reads `extracted_info.get('hardware')` as `hw_info`; reads `extracted_info.get('licenses_extraction')` as `lic_info`; reads `extracted_info.get('human_subjects_extraction')` as `human_info`
- Extracts: `code_url = code_info.get('repository_url', 'NOT FOUND')`, `data_url = data_info.get('access_url', 'NOT FOUND')`, `code_negative = code_info.get('negative_phrase', 'NOT FOUND')`, `code_release = code_info.get('release_mention', 'NOT FOUND')`
- Computes: `has_any_url = (code_url != 'NOT FOUND') or (data_url != 'NOT FOUND')`
- Computes: `has_release_intent = code_release != 'NOT FOUND' and any(word in code_release.lower() for word in ['release', 'open-source', 'available', 'github', 'provide'])`
- Handles `hw_data` polymorphically: if `list` → joins as string; if `str` and non-empty → uses as is; if `dict` → reads `gpu_cpu`, `num_gpus`, `time`, assembles `hw_summary`
- Reads: `total_tokens = extracted_info.get('hyperparameters', {}).get('total_tokens', 'NOT FOUND')`
- Reads: `assets_used = lic_info.get('assets_used', [])`, `licenses_named = lic_info.get('licenses_named', [])`
- Reads: `human_annotation = human_info.get('uses_human_annotation', 'no')`

Returns `signals` dict with keys: `'reproducibility'`, `'open_access'`, `'statistics'`, `'compute_resource'`, `'licenses'`, `'crowdsourcing'` — each a string injected into the evaluation prompt.

---

#### Prompt 5: `get_evaluation_prompt(extracted_info, red_flags)` — SOURCE: `prompts.py:378`

**Signature:** `def get_evaluation_prompt(extracted_info: dict, red_flags: dict) -> str`

**Parameters:**
- `extracted_info`: serialized via `json.dumps(extracted_info, indent=2, ensure_ascii=False)`
- `red_flags`: cleaned (keys not starting with `'_'`) and serialized as JSON

**Used by:** `ReproducibilityEvaluationSkill.execute()` (outside cluster)

**Full prompt template (static portion):**
```
Act as a Senior Area Chair for NeurIPS 2026. Your task is to VALIDATE the transparency of the NeurIPS 2026 Paper Checklist.
DO NOT produce any numeric score. Your output is a transparency audit, not a grade.

EXTRACTED INFORMATION:
{json.dumps(extracted_info, indent=2, ensure_ascii=False)}

{flags_section}

=======================================================
PRE-COMPUTED SIGNALS - USE THESE TO AVOID COMMON ERRORS
=======================================================
[Item 4 - Reproducibility]   {signals['reproducibility']}
[Item 5 - Open Access]       {signals['open_access']}
[Item 7 - Statistics]        {signals['statistics']}
[Item 8 - Compute Resource]  {signals['compute_resource']}
[Item 12 - Licenses]         {signals['licenses']}
[Item 14 - Crowdsourcing]    {signals['crowdsourcing']}

=======================================================
OUTPUT RULES - MANDATORY FOR ALL 16 ITEMS
=======================================================
For every item:
- "answer" MUST be exactly one of: "Yes", "No", or "N/A".
- If "Yes" -> "evidence" MUST contain paper section AND verbatim fragment.
- If "No" -> "justification" MUST explain what is missing and why it constitutes a transparency risk.
- If "N/A" -> "justification" MUST explain why item is not applicable.
- "is_no_justified" MUST be true only if explicit justification exists or pre-computed signals apply.
- LENGTH REQUIREMENT: Every "evidence" and "justification" should be at least 2-3 sentences.

[Per-item rules for items 1, 2, 4, 5, 6, 7, 9, 12, 14, 16 — as documented above in source read]
```

**Return JSON schema keys (16 NeurIPS checklist items):**
`claims`, `limitations`, `theory_assumptions_proofs`, `experimental_result_reproducibility`, `open_access_data_code`, `experimental_setting_details`, `experiment_statistical_significance`, `experiments_compute_resource`, `code_of_ethics`, `broader_impacts`, `safeguards`, `licenses`, `assets`, `crowdsourcing_human_subjects`, `irb_approvals`, `declaration_llm_usage`

Each item has sub-fields: `answer` ("Yes"/"No"/"N/A"), `evidence`, `justification`, `is_no_justified` (bool)

---

#### Prompt 6: `get_verification_prompt(item_key, item_data, paper_context)` — SOURCE: `prompts.py:494`

**Signature:** `def get_verification_prompt(item_key: str, item_data: dict, paper_context: str) -> str`

**Parameters:**
- `item_key`: name of the checklist item being verified (e.g., `"declaration_llm_usage"`)
- `item_data`: dict with `answer`, `justification`, `evidence` keys
- `paper_context`: full paper text or excerpts

**Used by:** `ChecklistVerificationSkill.execute()` (outside cluster)

**Full prompt template (static portion):**
```
You are an OBJECTIVE NEURIPS AUDITOR. Your task is to VERIFY the accuracy of an initial evaluation of a scientific paper.

CRITICAL INSTRUCTIONS:
- If initial answer is 'No' or 'N/A': Search for FALSE NEGATIVES (evidence that was missed).
- If initial answer is 'Yes': Search for FALSE POSITIVES (claiming compliance when evidence is weak, generic, or incorrect).
- Your goal is the TRUTH. Do not change the answer unless you are 100% sure the initial one is wrong.

ITEM TO VERIFY: {item_key}
INITIAL ANSWER: {answer}
INITIAL JUSTIFICATION: {justification}
INITIAL EVIDENCE: {evidence}

PAPER CONTEXT (Excerpts or Full Text):
{paper_context}

INSTRUCTIONS:
1. Review the initial evaluation and the paper context.
2. STRICT SEMANTIC VALIDATION: Verify that 'evidence' quote is actually RELEVANT to the item.
3. Item 16 CRITICAL DISTINCTION: Differentiate between research topic (LLMs in methodology) and AI-assisted writing declaration. Answering "Yes" for Item 16 based on methodology text is a CRITICAL HALLUCINATION.
4. For 'Yes' answers: Verify the verbatim quote actually exists and directly supports the answer.
5. For Item 7 (Statistics): A table of results is NOT statistical significance unless it includes error metrics.
6. Search for explicit section headers that might have been missed.
7. If you change the answer, provide detailed justification.
```

**Return JSON schema:** `answer` ("Yes"/"No"/"N/A"), `evidence`, `justification`, `is_no_justified` (bool), `was_corrected` (bool)

---

### 2.3 Other Constants (per file)

**`backend/utils/logger.py` — ANSI color codes (class `Colors`):**

| Attribute | Type | Value | SOURCE |
|-----------|------|-------|--------|
| `Colors.BLUE` | `str` | `"\033[94m"` | `logger.py:7` |
| `Colors.CYAN` | `str` | `"\033[96m"` | `logger.py:8` |
| `Colors.GREEN` | `str` | `"\033[92m"` | `logger.py:9` |
| `Colors.YELLOW` | `str` | `"\033[93m"` | `logger.py:10` |
| `Colors.RED` | `str` | `"\033[91m"` | `logger.py:11` |
| `Colors.MAGENTA` | `str` | `"\033[95m"` | `logger.py:12` |
| `Colors.BOLD` | `str` | `"\033[1m"` | `logger.py:13` |
| `Colors.RESET` | `str` | `"\033[0m"` | `logger.py:14` |

**`backend/utils/logger.py` — Log level → color mapping:**

| Level | Color constant | SOURCE |
|-------|---------------|--------|
| `logging.DEBUG` | `Colors.BLUE` | `logger.py:22` |
| `logging.INFO` | `Colors.GREEN` | `logger.py:23` |
| `logging.WARNING` | `Colors.YELLOW` | `logger.py:24` |
| `logging.ERROR` | `Colors.RED` | `logger.py:25` |
| `logging.CRITICAL` | `Colors.BOLD + Colors.RED` | `logger.py:26` |

**`backend/services/pdf_parser.py` — Inline constant:**

| Constant | Type | Value | SOURCE |
|----------|------|-------|--------|
| `chunk_size` | `int` | `5` (pages per processing block) | `pdf_parser.py:51` |

**`backend/common/llm_client.py` — Inline constants:**

| Constant | Type | Value | SOURCE |
|----------|------|-------|--------|
| `max_retries` | `int` | `5` | `llm_client.py:39` |
| `base_delay` | `int` | `2` (seconds) | `llm_client.py:40` |

---

## 3. API and Service Contracts (Category 8)

### 3.1 LLM Client (llm_client.py)

**Pattern:** Single class `LLMClient`, not singleton, instantiated per service.

**Supported provider:** Google Gemini exclusively via `google.genai.Client`.

**Class: `LLMClient`** — SOURCE: `llm_client.py:8`
- Parent class: none
- Module-level logger: `logger = get_logger(__name__)` at `llm_client.py:6`

**`LLMClient.__init__(self, model_name=None, generation_config=None)`** — SOURCE: `llm_client.py:11`
- Parameter `model_name`: `str | None`, default `None`; if `None`, uses `MODEL_NAME` from config (`"gemini-3.1-flash-lite-preview"`)
- Parameter `generation_config`: `dict | None`, default `None`; if `None`, uses `{}`
- RULE: checks `if not GOOGLE_API_KEY` → raises `ValueError("No se encontró la GOOGLE_API_KEY en el .env")` and logs `logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")` — SOURCE: `llm_client.py:19-21`
- Creates `self.client = genai.Client(api_key=GOOGLE_API_KEY)` — SOURCE: `llm_client.py:23`
- Sets `self.model_name = model_name or MODEL_NAME` — SOURCE: `llm_client.py:25`
- Sets `self.generation_config = generation_config or {}` — SOURCE: `llm_client.py:26`
- Logs: `logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")` — SOURCE: `llm_client.py:28`
- Returns: `None` (constructor)

**`LLMClient.generate(self, prompt)`** — SOURCE: `llm_client.py:30`
- Parameter `prompt`: any type accepted by `genai.Client.models.generate_content` (string or structured content)
- Imports `time`, `streamlit as st`, `random` inline at method entry — SOURCE: `llm_client.py:35-37`
- Iterates `for attempt in range(max_retries + 1)` → `range(6)` (attempts 0 through 5) — SOURCE: `llm_client.py:42`
- Each attempt calls: `self.client.models.generate_content(model=self.model_name, contents=prompt, config=self.generation_config)` — SOURCE: `llm_client.py:44-48`
- On success: returns `response` object directly (no post-processing) — SOURCE: `llm_client.py:49`
- On exception: reads `error_msg = str(e)`; checks `is_retryable = any(code in error_msg.upper() for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"])` — SOURCE: `llm_client.py:54`
- If `attempt < max_retries and is_retryable`:
  - Computes delay: `delay = base_delay * (2 ** attempt) + random.uniform(0, 1)` — SOURCE: `llm_client.py:58`
  - Logs: `logger.warning(f"⚠️ Error API Gemini [{self.model_name}]: {error_msg}. Reintento {attempt + 1}/{max_retries} en {delay:.1f}s...")` — SOURCE: `llm_client.py:60`
  - Attempts `st.toast(f"⏳ Gemini saturado (Alta demanda). Reintento {attempt + 1}/{max_retries} en {int(delay)}s...", icon="⏳")` inside `try/except Exception: pass` — SOURCE: `llm_client.py:63-66`
  - Calls `time.sleep(delay)` — SOURCE: `llm_client.py:69`
- Else (not retryable OR exhausted retries):
  - If `attempt >= max_retries`: logs `logger.error(f"❌ Error crítico tras {max_retries} reintentos: {error_msg}")` — SOURCE: `llm_client.py:73`
  - If not retryable: logs `logger.error(f"❌ Error no reintentable detectado: {error_msg}")` — SOURCE: `llm_client.py:75`
  - `raise` (re-raises original exception) — SOURCE: `llm_client.py:76`
- Return type: Google genai response object (caller accesses `.text` or `.candidates[0]` etc.)
- Retry logic: exponential backoff for HTTP 503, 429, UNAVAILABLE, RESOURCE_EXHAUSTED, DEADLINE_EXCEEDED; up to 5 retries

---

### 3.2 Auditor Service (auditor.py)

**Class: `PaperAuditor`** — SOURCE: `auditor.py:25`
- Parent class: none
- Imports: `time`, `LLMClient`, 6 config constants, `get_logger`, `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ChecklistVerificationSkill`, `HybridHyperparameterExtractionSkill`

**`PaperAuditor.__init__(self)`** — SOURCE: `auditor.py:28`
- No parameters
- Creates 5 `LLMClient` instances:
  - `self.extraction_llm = LLMClient(model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:31`
  - `self.evaluation_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:34`
  - `self.rag_map_llm = LLMClient(model_name=MAP_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:37`
  - `self.rag_reduce_llm = LLMClient(model_name=REDUCE_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:40`
  - `self.verification_llm = LLMClient(model_name=VERIFICATION_MODEL_NAME, generation_config=AUDIT_CONFIG)` — SOURCE: `auditor.py:43`
- Creates 6 skill instances (see GAPs for skill details):
  - `self.extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm)` — SOURCE: `auditor.py:46`
  - `self.hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm)` — SOURCE: `auditor.py:47`
  - `self.evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm)` — SOURCE: `auditor.py:48`
  - `self.verification_skill = ChecklistVerificationSkill(llm_client=self.verification_llm)` — SOURCE: `auditor.py:51`
  - `self.metrics_skill = MetricsCalculationSkill()` (no LLM client) — SOURCE: `auditor.py:53`
  - `self.metadata_skill = MetadataAggregationSkill()` (no LLM client) — SOURCE: `auditor.py:54`
- Logs: `logger.info(f"✅ Motor de Embeddings inicializado: {EMBEDDING_MODEL_NAME}")` — SOURCE: `auditor.py:56`
- Logs: `logger.info("✅ Auditor inicializado respetando la configuración técnica.")` — SOURCE: `auditor.py:57`

**`PaperAuditor.audit(self, paper_text, status_callback=None)`** — SOURCE: `auditor.py:60`
- Parameter `paper_text`: `str` — full paper text in markdown format
- Parameter `status_callback`: callable | None, default `None` — called with status message strings
- Return type: `dict` — on success: audit result from `MetadataAggregationSkill`; on failure: `{"error": str(e)}` or `{"error": "INVALID_PAPER_TYPE", "message": ..., "paper_type": ...}`
- Detailed logic: see Section 4.2 (Audit Pipeline)

---

### 3.3 Chatbot Service (chatbot.py)

**Class: `PaperChatbot`** — SOURCE: `chatbot.py:12`
- Parent class: none

**`PaperChatbot.__init__(self)`** — SOURCE: `chatbot.py:15`
- No parameters
- Creates: `self.llm_client = LLMClient(generation_config=CHAT_CONFIG)` (uses default `MODEL_NAME`) — SOURCE: `chatbot.py:17`
- Creates: `self.response_skill = ConversationalResponseSkill(llm_client=self.llm_client)` — SOURCE: `chatbot.py:20`
- Creates: `self.validation_skill = ContextValidationSkill()` (no LLM client) — SOURCE: `chatbot.py:21`
- Logs: `logger.info("✅ Módulo de Chatbot inicializado con arquitectura de skills")` — SOURCE: `chatbot.py:23`

**`PaperChatbot.preguntar(self, paper_text, question, history_text)`** — SOURCE: `chatbot.py:25`
- Parameter `paper_text`: `str` — full paper text
- Parameter `question`: `str` — user question
- Parameter `history_text`: `str` — conversation history
- Return type: `str` — chatbot response or error string
- Logic: see Section 4.4 (Chatbot Pipeline)

**Class: `Chatbot(PaperChatbot)`** — SOURCE: `chatbot.py:59`
- DETAIL: DELEGATION_ONLY — inherits all `PaperChatbot` methods without override; docstring: `"""Alias para compatibilidad con tests"""`

---

### 3.4 PDF Parser Service (pdf_parser.py)

**Function: `convert_pdf_to_markdown(pdf_path)`** — SOURCE: `pdf_parser.py:7`
- Parameter `pdf_path`: path to PDF file (str or path-like)
- Return type: `str` — full Markdown text of the PDF, or error string starting with `"❌ Error en la extracción del PDF: "` on outer exception
- Library used: `docling.document_converter.DocumentConverter`
- Logic: see Section 4.1 (PDF Parse Pipeline)

---

### 3.5 SOTA Analyzer Service (sota_analyzer.py)

**Class: `SotaAnalyzer`** — SOURCE: `sota_analyzer.py:17`
- Type hints imported: `from typing import Dict, Any`

**`SotaAnalyzer.__init__(self)`** — SOURCE: `sota_analyzer.py:29`
- No parameters
- Creates single `LLMClient` instance: `llm_client = LLMClient(generation_config=SOTA_CONFIG)` — SOURCE: `sota_analyzer.py:31`
- Creates 5 skill instances (all receive same `llm_client` except `search_skill`):
  - `self.thematic_skill = ThematicCoverageSkill(llm_client=llm_client)` — SOURCE: `sota_analyzer.py:34`
  - `self.query_skill = QueryGenerationSkill(llm_client=llm_client)` — SOURCE: `sota_analyzer.py:35`
  - `self.search_skill = SemanticScholarSearchSkill()` (no LLM client) — SOURCE: `sota_analyzer.py:36`
  - `self.gap_skill = CoverageGapAnalysisSkill(llm_client=llm_client)` — SOURCE: `sota_analyzer.py:37`
  - `self.validation_skill = CrossValidationSkill(llm_client=llm_client)` — SOURCE: `sota_analyzer.py:38`
- Logs: `logger.info("✅ Analizador SOTA inicializado con skills")` — SOURCE: `sota_analyzer.py:40`

**`SotaAnalyzer.analyze_sota(self, paper_text)`** — SOURCE: `sota_analyzer.py:43`
- Parameter `paper_text`: `str` — full paper text
- Return type: `Dict[str, Any]` — on success: dict with `"metadata"` key plus keys from `CrossValidationSkill`; on error: `{"error": "explanation string"}`
- Logic: see Section 4.3 (SOTA Analysis Pipeline)

---

## 4. Processing Pipelines (Category 10)

### 4.1 PDF Parse Pipeline

**Entry point:** `convert_pdf_to_markdown(pdf_path)` — SOURCE: `pdf_parser.py:7`

**Step 0 — Imports:** Lazily imports `docling.datamodel.base_models.InputFormat`, `docling.document_converter.DocumentConverter`, `docling.document_converter.PdfFormatOption`, `docling.datamodel.pipeline_options.PdfPipelineOptions`, `pypdf.PdfReader`, `pypdf.PdfWriter`, `os`, `tempfile` — SOURCE: `pdf_parser.py:20-25`

**Step 1 — Configure Docling pipeline:**
- Creates `pipeline_options = PdfPipelineOptions()` — SOURCE: `pdf_parser.py:28`
- Sets `pipeline_options.do_ocr = False` (OCR disabled for speed) — SOURCE: `pdf_parser.py:29`
- Sets `pipeline_options.do_table_structure = True` (table detection enabled) — SOURCE: `pdf_parser.py:30`
- Imports `torch`; checks `torch.cuda.is_available()` — SOURCE: `pdf_parser.py:33-37`
  - If CUDA available: logs `"🚀 GPU detectada. Docling usará aceleración CUDA automáticamente."`
  - If not: logs `"ℹ️ No se detectó GPU compatible. Usando CPU para Docling."`
  - Note: GPU detection is informational only; Docling auto-detects via torch
- Creates `converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)})` — SOURCE: `pdf_parser.py:39-43`

**Step 2 — Read PDF metadata:**
- Creates `reader = PdfReader(pdf_path)` — SOURCE: `pdf_parser.py:46`
- Reads `total_pages = len(reader.pages)` — SOURCE: `pdf_parser.py:47`
- Logs: `f"📄 Total de páginas detectadas: {total_pages}"`
- Initializes `full_md_text = ""` — SOURCE: `pdf_parser.py:50`

**Step 3 — Chunked conversion loop:**
- Iterates `for i in range(0, total_pages, chunk_size)` where `chunk_size = 5` — SOURCE: `pdf_parser.py:53`
- Each iteration:
  - Computes `start_page = i`, `end_page = min(i + chunk_size, total_pages)` — SOURCE: `pdf_parser.py:54-55`
  - Logs: `f"⏳ Procesando bloque de páginas: {start_page+1} a {end_page}..."`
  - Creates `writer = PdfWriter()` — SOURCE: `pdf_parser.py:59`
  - Iterates `for page_num in range(start_page, end_page)`: calls `writer.add_page(reader.pages[page_num])` — SOURCE: `pdf_parser.py:60-61`
  - Creates temp file: `with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file: tmp_path = tmp_file.name; writer.write(tmp_path)` — SOURCE: `pdf_parser.py:63-65`
  - Inner try: `result = converter.convert(tmp_path)` → `block_md = result.document.export_to_markdown()` → `full_md_text += block_md + "\n\n"` — SOURCE: `pdf_parser.py:69-71`
  - Logs success: `f"✅ Bloque {start_page+1}-{end_page} completado."`
  - Inner except: catches any `Exception as block_error`; logs `f"❌ Error en bloque {start_page+1}-{end_page}: {str(block_error)}"`; appends error notice to `full_md_text`: `f"\n\n> [!ERROR] Error al procesar páginas {start_page+1}-{end_page}: {str(block_error)}\n\n"` — SOURCE: `pdf_parser.py:73-75`
  - Finally: if `os.path.exists(tmp_path)`: calls `os.remove(tmp_path)` (temp cleanup) — SOURCE: `pdf_parser.py:78-79`

**Step 4 — Return result:**
- Logs: `f"🚀 Conversión total completada ({len(full_md_text)} caracteres)"`
- Returns `full_md_text` — SOURCE: `pdf_parser.py:82`

**Outer exception handler:** Catches any `Exception as e`; logs `f"❌ Error en la extracción del PDF: {str(e)}"`; returns `f"❌ Error en la extracción del PDF: {str(e)}"` — SOURCE: `pdf_parser.py:83-85`

**Error handling:**
- Per-block errors: caught, error text appended to output, processing continues — SOURCE: `pdf_parser.py:73-75`
- Empty PDFs: `total_pages = 0` → loop does not execute → returns empty string
- Corrupted/unreadable PDFs: `PdfReader(pdf_path)` raises; caught by outer handler; returns error string
- Password-protected PDFs: `PdfReader` would raise; caught by outer handler; returns error string
- Temp file cleanup: always runs in `finally` block regardless of block conversion success or failure

---

### 4.2 Audit Pipeline

**Entry point:** `PaperAuditor.audit(self, paper_text, status_callback=None)` — SOURCE: `auditor.py:60`

**Local helper:** `log_status(msg)` defined inline at `auditor.py:72`: calls `logger.info(msg)`; if `status_callback` is not None, calls `status_callback(msg)`

**Pre-processing:**
- Computes `caracteres = len(paper_text)` — SOURCE: `auditor.py:77`
- Calls `log_status(f"🚀 Iniciando auditoría con skills. Tamaño: {caracteres} caracteres")`
- Records `start_time = time.time()` — SOURCE: `auditor.py:80`
- Initializes `context = {'paper_text': paper_text, 'red_flags': {}}` — SOURCE: `auditor.py:84`

**PHASE 1 — Information Extraction:**
- Calls `log_status("🔍 Fase 1: Extracción inicial de información clave...")`
- Calls `extraction_result = self.extraction_skill.execute(context)` — SOURCE: `auditor.py:88`
- RULE: if `'extraction_error' in extraction_result`: logs error, returns `{'error': extraction_result['extraction_error']}` — SOURCE: `auditor.py:89-91`
- Calls `context.update(extraction_result)` — SOURCE: `auditor.py:93`
- If `'map_steps' in extraction_result`: sets `context['general_analysis_map'] = extraction_result['map_steps']` — SOURCE: `auditor.py:96-97`
- If `'reduce_step' in extraction_result`: sets `context['general_analysis_reduce'] = extraction_result['reduce_step']` — SOURCE: `auditor.py:98-99`
- If `'extracted_info' in extraction_result`: deep-copies it to `context['original_extraction_raw']` via `copy.deepcopy` — SOURCE: `auditor.py:102-104`
- RULE: if `extraction_result.get('invalid_paper', False)` is True: logs warning, returns `{'error': 'INVALID_PAPER_TYPE', 'message': extraction_result.get('invalid_reason', ...), 'paper_type': extraction_result.get('extracted_info', {}).get('paper_type', 'Unknown')}` — SOURCE: `auditor.py:107-113`

**PHASE 1.5 — Hybrid Hyperparameter Extraction (RAG + Pydantic):**
- Calls `log_status("🧠 Fase 1.5: Profundización técnica con RAG y Pydantic...")`
- Calls `hybrid_hp_result = self.hybrid_hp_skill.execute(context)` — SOURCE: `auditor.py:117`
- RULE: if `'error' in hybrid_hp_result and not hybrid_hp_result.get('extracted_hyperparameters_hybrid')`: logs warning (non-critical, continues) — SOURCE: `auditor.py:120-121`
- Calls `context.update(hybrid_hp_result)` — SOURCE: `auditor.py:123`
- If `'triage_fragments' in hybrid_hp_result`: sets `context['hybrid_triage_fragments'] = hybrid_hp_result['triage_fragments']` — SOURCE: `auditor.py:126-127`
- Hyperparameter merge: if `'extracted_hyperparameters_hybrid' in context and 'extracted_info' in context` and `hybrid_hps` is truthy:
  - Ensures `context['extracted_info']['hyperparameters']` dict exists
  - Maps keys: for each of `['optimizer', 'learning_rate', 'batch_size', 'epochs', 'warmup', 'weight_decay', 'betas', 'epsilon']`: maps `'warmup'` to `'warmup_steps'`, all others identity; if mapped key exists in `hybrid_hps` AND value is non-empty AND value != `'NOT FOUND'`: sets `context['extracted_info']['hyperparameters'][key] = hybrid_hps[mapped_key]` — SOURCE: `auditor.py:136-141`
  - Hardware merge: reads `hybrid_hw = hybrid_hps.get('hardware')`; if truthy and not `'NOT FOUND'`: ensures `context['extracted_info']['hardware']` is a dict (if was list/str: moves to `'original_info'` key); sets `context['extracted_info']['hardware']['gpu_cpu'] = hybrid_hw` — SOURCE: `auditor.py:144-154`

**PHASE 2 — Reproducibility Evaluation:**
- Calls `log_status("⚖️ Fase 2: Evaluación de criterios de reproducibilidad...")`
- Calls `evaluation_result = self.evaluation_skill.execute(context)` — SOURCE: `auditor.py:158`
- RULE: if `'evaluation_error' in evaluation_result`: logs error, returns `{'error': evaluation_result['evaluation_error']}` — SOURCE: `auditor.py:159-161`
- Calls `context.update(evaluation_result)` — SOURCE: `auditor.py:163`
- If `'evaluation_signals' in evaluation_result`: sets `context['evaluation_signals'] = evaluation_result['evaluation_signals']` — SOURCE: `auditor.py:166-167`

**PHASE 2.5 — Strict Verification (Auditor 2 / False-Negative Check):**
- Calls `log_status("🛡️ Fase 2.5: Verificación estricta de cumplimiento (Auditor 2)...")`
- Calls `verification_result = self.verification_skill.execute(context)` — SOURCE: `auditor.py:171`
- Calls `context.update(verification_result)` — SOURCE: `auditor.py:172`

**PHASE 3 — Metrics Calculation:**
- Calls `log_status("📊 Fase 3: Consolidación de métricas y puntuaciones...")`
- Records `end_time = time.time(); execution_time = round(end_time - start_time, 2)` — SOURCE: `auditor.py:176-177`
- Builds `metrics_context = {**context, 'execution_time': execution_time, 'caracteres': caracteres}` — SOURCE: `auditor.py:179-182`
- Calls `metrics_result = self.metrics_skill.execute(metrics_context)` — SOURCE: `auditor.py:184`
- Calls `context.update(metrics_result)` — SOURCE: `auditor.py:185`

**PHASE 4 — Metadata Aggregation:**
- Calls `log_status("🏁 Fase 4: Generación de informe final y metadatos...")`
- Calls `final_result = self.metadata_skill.execute(context)` — SOURCE: `auditor.py:189`
- If `'extracted_hyperparameters_hybrid' in context`: sets `final_result['extracted_hyperparameters_hybrid'] = context['extracted_hyperparameters_hybrid']` — SOURCE: `auditor.py:192-193`
- If `'original_extraction_raw' in context`: sets `final_result['original_extraction_raw'] = context['original_extraction_raw']` — SOURCE: `auditor.py:194-195`
- Calls `log_status(f"✅ Auditoría completada en {execution_time} segundos")`
- Returns `final_result` — SOURCE: `auditor.py:198`

**Outer exception handler:** `except Exception as e` at `auditor.py:201`; logs `f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}"`; returns `{"error": str(e)}`

---

### 4.3 SOTA Analysis Pipeline

**Entry point:** `SotaAnalyzer.analyze_sota(self, paper_text)` — SOURCE: `sota_analyzer.py:43`

**Step 1 — Thematic Coverage Analysis:**
- Initializes `context = {'paper_text': paper_text}` — SOURCE: `sota_analyzer.py:59`
- Calls `thematic_result = self.thematic_skill.execute(context)` — SOURCE: `sota_analyzer.py:62`
- Calls `context.update(thematic_result)` — SOURCE: `sota_analyzer.py:63`
- RULE: if `not context.get('thematic_data')`: returns `{"error": "No se pudo extraer información temática del paper."}` — SOURCE: `sota_analyzer.py:65-66`

**Step 2 — Search Query Generation:**
- Calls `query_result = self.query_skill.execute(context)` — SOURCE: `sota_analyzer.py:69`
- Calls `context.update(query_result)` — SOURCE: `sota_analyzer.py:70`
- RULE: if `not context.get('search_queries')`: returns `{"error": "No se pudieron generar queries de búsqueda."}` — SOURCE: `sota_analyzer.py:72-73`

**Step 3 — Semantic Scholar Search:**
- Calls `search_result = self.search_skill.execute(context)` — SOURCE: `sota_analyzer.py:76`
- Calls `context.update(search_result)` — SOURCE: `sota_analyzer.py:77`
- No early-exit rule; errors from search are tolerated

**Step 4 — Coverage Gap Analysis:**
- Calls `gap_result = self.gap_skill.execute(context)` — SOURCE: `sota_analyzer.py:80`
- Calls `context.update(gap_result)` — SOURCE: `sota_analyzer.py:81`

**Step 5 — Cross-Validation:**
- Calls `validation_result = self.validation_skill.execute(context)` — SOURCE: `sota_analyzer.py:84`
- Reads `final_results = validation_result.get('validation_results', {})` — SOURCE: `sota_analyzer.py:85`

**Metadata assembly:**
- Reads: `thematic_data = context.get('thematic_data', {})`, `sota_papers = context.get('sota_papers', [])`, `search_queries = context.get('search_queries', [])` — SOURCE: `sota_analyzer.py:88-90`
- Sets `final_results["metadata"] = {"subtemas_identificados": thematic_data.get("subtemas", []), "areas_tecnicas": thematic_data.get("areas_tecnicas", []), "año_paper_estudiado": thematic_data.get("año_paper"), "total_papers_analizados": len(sota_papers), "queries_ejecutadas": len(search_queries)}` — SOURCE: `sota_analyzer.py:92-98`
- Returns `final_results` — SOURCE: `sota_analyzer.py:101`

---

### 4.4 Chatbot Conversation Pipeline

**Entry point:** `PaperChatbot.preguntar(self, paper_text, question, history_text)` — SOURCE: `chatbot.py:25`

**Step 1 — Build context dict:**
- Creates `context = {'paper_text': paper_text, 'question': question, 'history_text': history_text}` — SOURCE: `chatbot.py:39-43`

**Step 2 — Context validation (Skill 1):**
- Calls `validation_result = self.validation_skill.execute(context)` — SOURCE: `chatbot.py:46`
- RULE: if `not validation_result.get('is_valid', False)`:
  - Reads `error_msg = validation_result.get('error', 'Error desconocido')` — SOURCE: `chatbot.py:49`
  - Logs: `logger.error(f"❌ Validación fallida: {error_msg}")` — SOURCE: `chatbot.py:50`
  - Returns `f"❌ Error de validación: {error_msg}"` — SOURCE: `chatbot.py:51`

**Step 3 — Response generation (Skill 2):**
- Calls `response_result = self.response_skill.execute(context)` — SOURCE: `chatbot.py:54`
- Returns `response_result.get('response', '❌ Error generando respuesta')` — SOURCE: `chatbot.py:56`

---

## 5. Security (Category 11)

**API key handling:**
- `GOOGLE_API_KEY` is read from environment via `os.getenv("GOOGLE_API_KEY")` at `config.py:30`; stored in module-level variable; passed to `genai.Client(api_key=GOOGLE_API_KEY)` at `llm_client.py:23`
- `SEMANTIC_SCHOLAR_API_KEY` is read from environment via `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` at `config.py:31`; available as module-level variable; actual usage is in SOTA skills (outside this cluster)
- Both keys are loaded via `load_dotenv()` at `config.py:27` (reads from `.env` file)
- Keys stored in memory as plain strings; no secure storage, no encryption
- `LLMClient.__init__` checks `if not GOOGLE_API_KEY` and raises `ValueError` before making any network call — SOURCE: `llm_client.py:19-21`

**Logging of secrets:**
- `logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")` logs only the model name, not the API key — SOURCE: `llm_client.py:28`
- No API key value is logged in any file in this cluster

**Input sanitization:**
- No input sanitization is performed on `paper_text`, `question`, or `history_text` before passing to LLM in this cluster; raw user/upload content flows directly into prompts

**Authentication/Authorization:**
- No HTTP authentication, session handling, or role-based access control exists in this cluster
- All files contain only business logic and infrastructure; access control is UNRESOLVABLE from this cluster's files

**Rate limiting/quota:**
- `LLMClient.generate` implements client-side retry with exponential backoff on HTTP 429 (quota exceeded), but no proactive quota tracking or rate limiting — SOURCE: `llm_client.py:54`

SOURCE FILES CHECKED FOR SECURITY LOGIC: `backend/__init__.py`, `backend/common/config.py`, `backend/common/llm_client.py`, `backend/common/prompts.py`, `backend/common/__init__.py`, `backend/services/auditor.py`, `backend/services/chatbot.py`, `backend/services/pdf_parser.py`, `backend/services/sota_analyzer.py`, `backend/services/__init__.py`, `backend/utils/logger.py`, `backend/utils/__init__.py`

---

## 6. Error Handling (Category 12)

### 6.1 Logger Configuration

**Source:** `backend/utils/logger.py`

**Logger name:** Caller passes `__name__`; `get_logger` calls `logging.getLogger(name)` — SOURCE: `logger.py:45`

**Log level configured:** `logging.INFO` — SOURCE: `logger.py:53`

**Handler:** `logging.StreamHandler(sys.stdout)` — SOURCE: `logger.py:49-50`; output goes to **stdout**

**Formatter:** `ColoredFormatter` instance — SOURCE: `logger.py:50`

**Log format string:** `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` — SOURCE: `logger.py:19`

**Date format:** `'%H:%M:%S'` (hours:minutes:seconds only) — SOURCE: `logger.py:41`

**No log rotation configured.**

**Propagation:** `logger.propagate = False` (no duplication with root logger) — SOURCE: `logger.py:47`

**Handler deduplication:** `if not logger.handlers:` guard prevents adding multiple handlers on repeated `get_logger` calls — SOURCE: `logger.py:49`

**Side effects in `get_logger`:**
- `logging.getLogger("google_genai").setLevel(logging.WARNING)` — SOURCE: `logger.py:56`
- `logging.getLogger("httpx").setLevel(logging.INFO)` — SOURCE: `logger.py:57`

**`ColoredFormatter.format(self, record)` logic** — SOURCE: `logger.py:29`:
- If `"HTTP Request"` in `record.msg`: sets `color = Colors.CYAN`; mutates `record.msg = f"{Colors.CYAN}{record.msg}{Colors.RESET}"` — SOURCE: `logger.py:33-35`
- Else: reads `color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)`; mutates `record.levelname = f"{color}{record.levelname}{Colors.RESET}"` — SOURCE: `logger.py:37-39`
- Creates new `logging.Formatter(log_fmt, datefmt='%H:%M:%S')` on every call (no caching)
- Returns `formatter.format(record)` — SOURCE: `logger.py:42`

---

### 6.2 Exception Handling per File

#### `backend/common/llm_client.py`

**Try/except in `LLMClient.generate`** — SOURCE: `llm_client.py:43-76`
- Try block: `self.client.models.generate_content(model=..., contents=..., config=...)`
- Except: `Exception as e` (catches all)
- In except: computes `is_retryable`; if retryable and attempts remain: logs warning, shows Streamlit toast, sleeps, loops; else: logs error and `raise` (re-raises original exception)
- Inner try/except for `st.toast(...)` — SOURCE: `llm_client.py:63-66`: catches `Exception`, body is `pass` (swallowed silently; for non-Streamlit environments)
- No `finally` block

**Raise in `LLMClient.__init__`** — SOURCE: `llm_client.py:21`
- Exception type: `ValueError`
- Message: `"No se encontró la GOOGLE_API_KEY en el .env"`
- Condition: `if not GOOGLE_API_KEY` (None or empty string)

---

#### `backend/services/auditor.py`

**Outer try/except in `PaperAuditor.audit`** — SOURCE: `auditor.py:82-204`
- Try block: all 4 phases and returns
- Except: `Exception as e` (catches all)
- In except: logs `f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}"`
- Returns `{"error": str(e)}`
- No `finally` block
- Note: `end_time` may be unbound if exception occurs before Phase 3; this would cause `NameError` — GAP: potential `NameError` if exception raised before `end_time = time.time()` at line 176

**Conditional early returns (not raise):**
- Returns `{'error': extraction_result['extraction_error']}` if Phase 1 fails — SOURCE: `auditor.py:91`
- Returns `{'error': 'INVALID_PAPER_TYPE', ...}` if paper is not ML/AI — SOURCE: `auditor.py:109-113`
- Returns `{'error': evaluation_result['evaluation_error']}` if Phase 2 fails — SOURCE: `auditor.py:161`

---

#### `backend/services/pdf_parser.py`

**Inner try/except/finally per block** — SOURCE: `pdf_parser.py:67-79`
- Try block: `converter.convert(tmp_path)`, `result.document.export_to_markdown()`, `full_md_text += block_md + "\n\n"`
- Except: `Exception as block_error`
- In except: logs `f"❌ Error en bloque {start_page+1}-{end_page}: {str(block_error)}"`; appends error text to `full_md_text`; processing continues to next block (exception not re-raised)
- Finally: `if os.path.exists(tmp_path): os.remove(tmp_path)` — always executed, cleans up temp file

**Outer try/except** — SOURCE: `pdf_parser.py:18-85`
- Try block: all logic including imports and loop
- Except: `Exception as e`
- In except: logs `f"❌ Error en la extracción del PDF: {str(e)}"`; returns `f"❌ Error en la extracción del PDF: {str(e)}"` (error string, not raise)

---

#### `backend/services/chatbot.py`

No try/except blocks. Error signaling done via return values:
- Returns `f"❌ Error de validación: {error_msg}"` if validation fails — SOURCE: `chatbot.py:51`
- Returns `'❌ Error generando respuesta'` if `response_result` dict has no `'response'` key — SOURCE: `chatbot.py:56`

---

#### `backend/services/sota_analyzer.py`

No try/except blocks. Error signaling done via dict returns:
- Returns `{"error": "No se pudo extraer información temática del paper."}` if thematic_data missing — SOURCE: `sota_analyzer.py:66`
- Returns `{"error": "No se pudieron generar queries de búsqueda."}` if search_queries missing — SOURCE: `sota_analyzer.py:73`

---

#### `backend/common/config.py`

No try/except blocks. No raise statements. Missing API keys silently resolve to `None`.

---

#### `backend/common/prompts.py`

No try/except blocks. No raise statements. All error paths are left to callers.

---

#### `backend/utils/logger.py`

No try/except blocks. No raise statements.

---

## 7. Business Rules

RULE: GOOGLE_API_KEY_REQUIRED
TRIGGER: On `LLMClient.__init__` invocation
CONDITION: `not GOOGLE_API_KEY` (evaluates to True if `None` or empty string)
ACTION IF TRUE: `logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")`; raises `ValueError("No se encontró la GOOGLE_API_KEY en el .env")`; LLM client not created
ACTION IF FALSE: proceeds to create `genai.Client(api_key=GOOGLE_API_KEY)`
ERROR: `ValueError` with message `"No se encontró la GOOGLE_API_KEY en el .env"`
FIELDS INVOLVED: `GOOGLE_API_KEY` (from `config.py`)
CALLS: `logger.error(...)`, `raise ValueError(...)`
SOURCE: `llm_client.py:19-21`

---

RULE: INVALID_PAPER_TYPE_REJECTION
TRIGGER: During `PaperAuditor.audit` after Phase 1 extraction completes
CONDITION: `extraction_result.get('invalid_paper', False)` is True
ACTION IF TRUE: logs `f"❌ Paper rechazado: {extraction_result.get('invalid_reason')}"`; returns `{'error': 'INVALID_PAPER_TYPE', 'message': extraction_result.get('invalid_reason', 'Este sistema solo evalúa papers de ML/AI'), 'paper_type': extraction_result.get('extracted_info', {}).get('paper_type', 'Unknown')}`; pipeline aborted
ACTION IF FALSE: continues to Phase 1.5
ERROR: `'INVALID_PAPER_TYPE'` key in return dict
FIELDS INVOLVED: `invalid_paper`, `invalid_reason`, `extracted_info.paper_type`
CALLS: `log_status(...)`, return early
SOURCE: `auditor.py:107-113`

---

RULE: HYBRID_HP_NON_CRITICAL_FAILURE
TRIGGER: During `PaperAuditor.audit` after Phase 1.5 (hybrid extraction)
CONDITION: `'error' in hybrid_hp_result and not hybrid_hp_result.get('extracted_hyperparameters_hybrid')`
ACTION IF TRUE: logs `f"⚠️ Error en extracción híbrida RAG: {hybrid_hp_result['error']}"`; continues pipeline (non-blocking)
ACTION IF FALSE: proceeds normally
ERROR: warning logged; no error returned to caller
FIELDS INVOLVED: `hybrid_hp_result['error']`, `hybrid_hp_result['extracted_hyperparameters_hybrid']`
SOURCE: `auditor.py:120-121`

---

RULE: HYPERPARAMETER_KEY_MERGE
TRIGGER: During `PaperAuditor.audit` Phase 1.5 post-processing
CONDITION: `'extracted_hyperparameters_hybrid' in context and 'extracted_info' in context and hybrid_hps` is truthy
ACTION IF TRUE: for each of `['optimizer', 'learning_rate', 'batch_size', 'epochs', 'warmup', 'weight_decay', 'betas', 'epsilon']`: maps `'warmup'`→`'warmup_steps'`; if source value non-empty and not `'NOT FOUND'`: overwrites `context['extracted_info']['hyperparameters'][key]` with hybrid value
ACTION IF FALSE: `extracted_info.hyperparameters` left unchanged
ERROR: N/A
FIELDS INVOLVED: `extracted_hyperparameters_hybrid.*`, `extracted_info.hyperparameters.*`
SOURCE: `auditor.py:130-141`

---

RULE: HARDWARE_DICT_NORMALIZATION
TRIGGER: During `PaperAuditor.audit` Phase 1.5 post-processing when hardware merge needed
CONDITION: `context['extracted_info']['hardware']` is not a dict (is list or string) AND hybrid hardware value is available
ACTION IF TRUE: saves old value to `context['extracted_info']['hardware']['original_info']`; resets `context['extracted_info']['hardware']` to `{}`; then sets `['gpu_cpu'] = hybrid_hw`
ACTION IF FALSE: directly sets `context['extracted_info']['hardware']['gpu_cpu'] = hybrid_hw`
ERROR: N/A
FIELDS INVOLVED: `extracted_info.hardware`, `extracted_hyperparameters_hybrid.hardware`
SOURCE: `auditor.py:147-154`

---

RULE: THEMATIC_DATA_REQUIRED_FOR_SOTA
TRIGGER: During `SotaAnalyzer.analyze_sota` after Step 1
CONDITION: `not context.get('thematic_data')`
ACTION IF TRUE: returns `{"error": "No se pudo extraer información temática del paper."}`; pipeline aborted
ACTION IF FALSE: continues to Step 2
ERROR: `"error"` key in return dict
FIELDS INVOLVED: `context['thematic_data']`
SOURCE: `sota_analyzer.py:65-66`

---

RULE: SEARCH_QUERIES_REQUIRED_FOR_SOTA
TRIGGER: During `SotaAnalyzer.analyze_sota` after Step 2
CONDITION: `not context.get('search_queries')`
ACTION IF TRUE: returns `{"error": "No se pudieron generar queries de búsqueda."}`; pipeline aborted
ACTION IF FALSE: continues to Step 3
ERROR: `"error"` key in return dict
FIELDS INVOLVED: `context['search_queries']`
SOURCE: `sota_analyzer.py:72-73`

---

RULE: LLM_RETRY_RETRYABLE_ERRORS
TRIGGER: On exception from `self.client.models.generate_content(...)` within `LLMClient.generate`
CONDITION: `any(code in error_msg.upper() for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"])` AND `attempt < max_retries` (i.e., attempt < 5)
ACTION IF TRUE: computes `delay = 2 * (2 ** attempt) + random.uniform(0, 1)` seconds; logs warning; shows Streamlit toast; sleeps `delay` seconds; retries
ACTION IF FALSE: if `attempt >= 5`: logs critical error and re-raises; if non-retryable error: logs error and re-raises
ERROR: re-raises original exception after 5 failed retries or on non-retryable error
FIELDS INVOLVED: `attempt`, `max_retries=5`, `base_delay=2`, `error_msg`
SOURCE: `llm_client.py:42-76`

---

RULE: CHATBOT_VALIDATION_GATE
TRIGGER: During `PaperChatbot.preguntar` before LLM call
CONDITION: `not validation_result.get('is_valid', False)`
ACTION IF TRUE: logs `f"❌ Validación fallida: {error_msg}"`; returns `f"❌ Error de validación: {error_msg}"` (no LLM call made)
ACTION IF FALSE: proceeds to `ConversationalResponseSkill.execute(context)`
ERROR: N/A (returns string, not raises)
FIELDS INVOLVED: `validation_result['is_valid']`, `validation_result['error']`
CALLS: `ContextValidationSkill.execute(context)` — CROSS-REFERENCE: outside cluster
SOURCE: `chatbot.py:46-51`

---

RULE: PDF_BLOCK_ERROR_CONTINUATION
TRIGGER: On exception from `converter.convert(tmp_path)` or `result.document.export_to_markdown()` within PDF chunked loop
CONDITION: any `Exception` raised during block processing
ACTION IF TRUE: logs `f"❌ Error en bloque {start_page+1}-{end_page}: {str(block_error)}"`; appends markdown error notice to `full_md_text`; `finally` cleans temp file; loop continues to next block
ACTION IF FALSE: normal block processing
ERROR: N/A (returns partial text, not raises)
FIELDS INVOLVED: `full_md_text`, `tmp_path`, `start_page`, `end_page`
SOURCE: `pdf_parser.py:73-79`

---

## 8. Gaps and Cross-References

GAP_ID: GAP-cluster_backend_core_01-001
TYPE: CROSS_REFERENCE
FROM: `auditor.py:14` — `PaperAuditor.__init__`
EXPECTS: `InformationExtractionSkill` class with `execute(context: dict) -> dict` method; should place `'extraction_error'`, `'extracted_info'`, `'invalid_paper'`, `'invalid_reason'`, `'map_steps'`, `'reduce_step'` keys in returned dict
LIKELY_LOCATION: `backend/skills/auditor_skills.py`
IMPACT: HIGH — Phase 1 of audit pipeline; if this skill fails or returns unexpected structure, entire audit aborts
SOURCE: `auditor.py:14`

GAP_ID: GAP-cluster_backend_core_01-002
TYPE: CROSS_REFERENCE
FROM: `auditor.py:21` — `PaperAuditor.__init__`
EXPECTS: `HybridHyperparameterExtractionSkill` class with `execute(context: dict) -> dict`; returns keys `'extracted_hyperparameters_hybrid'`, `'triage_fragments'`, and optionally `'error'`; `extracted_hyperparameters_hybrid` should be a dict with `'optimizer'`, `'learning_rate'`, `'batch_size'`, `'epochs'`, `'warmup_steps'`, `'weight_decay'`, `'betas'`, `'epsilon'`, `'hardware'` keys
LIKELY_LOCATION: `backend/skills/rag_extraction_skill.py`
IMPACT: HIGH — Phase 1.5 of audit; overrides hyperparameter and hardware data extracted in Phase 1
SOURCE: `auditor.py:21`

GAP_ID: GAP-cluster_backend_core_01-003
TYPE: CROSS_REFERENCE
FROM: `auditor.py:16` — `PaperAuditor.__init__`
EXPECTS: `ReproducibilityEvaluationSkill` class with `execute(context: dict) -> dict`; should return `'evaluation_error'` key on failure, or result dict with `'evaluation_signals'` on success
LIKELY_LOCATION: `backend/skills/auditor_skills.py`
IMPACT: HIGH — Phase 2 of audit; evaluates all 16 NeurIPS checklist items
SOURCE: `auditor.py:16`

GAP_ID: GAP-cluster_backend_core_01-004
TYPE: CROSS_REFERENCE
FROM: `auditor.py:17` — `PaperAuditor.__init__`
EXPECTS: `MetricsCalculationSkill` class with `execute(context: dict) -> dict`; receives context with `execution_time` and `caracteres`; returns computed metrics dict
LIKELY_LOCATION: `backend/skills/auditor_skills.py`
IMPACT: MEDIUM — Phase 3 of audit; calculates aggregate scores
SOURCE: `auditor.py:17`

GAP_ID: GAP-cluster_backend_core_01-005
TYPE: CROSS_REFERENCE
FROM: `auditor.py:18` — `PaperAuditor.__init__`
EXPECTS: `MetadataAggregationSkill` class with `execute(context: dict) -> dict`; returns final audit report dict that becomes the return value of `PaperAuditor.audit`
LIKELY_LOCATION: `backend/skills/auditor_skills.py`
IMPACT: HIGH — Phase 4; final report structure determines what frontend receives
SOURCE: `auditor.py:18`

GAP_ID: GAP-cluster_backend_core_01-006
TYPE: CROSS_REFERENCE
FROM: `auditor.py:19` — `PaperAuditor.__init__`
EXPECTS: `ChecklistVerificationSkill` class with `execute(context: dict) -> dict`; uses `get_verification_prompt` from `prompts.py`; returns verified/corrected checklist items
LIKELY_LOCATION: `backend/skills/auditor_skills.py`
IMPACT: HIGH — Phase 2.5; second-pass verification detects false negatives/positives in evaluation
SOURCE: `auditor.py:19`

GAP_ID: GAP-cluster_backend_core_01-007
TYPE: CROSS_REFERENCE
FROM: `chatbot.py:5-6` — `PaperChatbot.__init__`
EXPECTS: `ConversationalResponseSkill` class with `execute(context: dict) -> dict`; context has `'paper_text'`, `'question'`, `'history_text'`; returns dict with `'response'` key containing chatbot answer string
LIKELY_LOCATION: `backend/skills/chatbot_skills.py`
IMPACT: HIGH — sole response generation mechanism for chatbot
SOURCE: `chatbot.py:5`

GAP_ID: GAP-cluster_backend_core_01-008
TYPE: CROSS_REFERENCE
FROM: `chatbot.py:5-7` — `PaperChatbot.__init__`
EXPECTS: `ContextValidationSkill` class with `execute(context: dict) -> dict`; should return dict with `'is_valid'` (bool) and optionally `'error'` (str) keys
LIKELY_LOCATION: `backend/skills/chatbot_skills.py`
IMPACT: MEDIUM — validation gate before LLM call; determines whether chatbot responds or returns error
SOURCE: `chatbot.py:7`

GAP_ID: GAP-cluster_backend_core_01-009
TYPE: CROSS_REFERENCE
FROM: `sota_analyzer.py:7-11` — `SotaAnalyzer.__init__`
EXPECTS: `ThematicCoverageSkill`, `QueryGenerationSkill`, `CoverageGapAnalysisSkill`, `CrossValidationSkill` classes each with `execute(context: dict) -> dict`; `SemanticScholarSearchSkill` with `execute(context: dict) -> dict`; `CrossValidationSkill` returns dict with `'validation_results'` key; `SemanticScholarSearchSkill` uses `SEMANTIC_SCHOLAR_BASE_URL`, `SEMANTIC_SCHOLAR_YEAR_RANGE`, `SEMANTIC_SCHOLAR_LIMIT`, `SEMANTIC_SCHOLAR_FIELDS` from config
LIKELY_LOCATION: `backend/skills/sota_skills.py`
IMPACT: HIGH — entire SOTA analysis pipeline depends on these skills
SOURCE: `sota_analyzer.py:7`

GAP_ID: GAP-cluster_backend_core_01-010
TYPE: CONFIG_DEPENDENCY
FROM: `config.py:30` — `GOOGLE_API_KEY`
EXPECTS: environment variable `"GOOGLE_API_KEY"` set in `.env` file; required for any LLM operation; if absent, all services fail at `LLMClient.__init__`
LIKELY_LOCATION: `.env` file (runtime environment)
IMPACT: HIGH — system-wide blocking dependency; all LLM features non-functional without it
SOURCE: `config.py:30`

GAP_ID: GAP-cluster_backend_core_01-011
TYPE: EXTERNAL_SYSTEM
FROM: `llm_client.py:44` — `LLMClient.generate`
EXPECTS: Google Gemini API (`google.generativeai` / `google.genai`) at `api.generativeai.googleapis.com`; model `"gemini-3.1-flash-lite-preview"` must be available; responds to `generate_content` with a response object having a `.text` or `.candidates` attribute
LIKELY_LOCATION: Google Cloud / Gemini API (external)
IMPACT: HIGH — all LLM functionality depends on this external API
SOURCE: `llm_client.py:44`

GAP_ID: GAP-cluster_backend_core_01-012
TYPE: MISSING_SOURCE
FROM: `auditor.py:201-204` — `PaperAuditor.audit` outer except block
EXPECTS: `end_time` variable to be defined; if exception is raised BEFORE line 176 (e.g., during Phase 1 or Phase 1.5), `end_time` is unbound → `NameError: name 'end_time' is not defined` would occur in the except handler at `round(end_time - start_time, 2)`
LIKELY_LOCATION: `auditor.py:201`
IMPACT: MEDIUM — masking exception with `NameError` in error path; would prevent clean error reporting for early-phase failures
SOURCE: `auditor.py:201`

---

## 9. Incomplete Extractions (if any)

All 12 files in this cluster have been fully extracted. No code units were skipped.

The following files contained only a single docstring and no executable code:
- `backend/__init__.py` — `"""Backend modular para el Auditor de Papers"""`
- `backend/common/__init__.py` — `"""Componentes comunes compartidos"""`
- `backend/services/__init__.py` — `"""Servicios de lógica de negocio"""`
- `backend/utils/__init__.py` — `"""Utilidades del backend"""`

The implementation of all skills referenced by services (`auditor_skills.py`, `rag_extraction_skill.py`, `chatbot_skills.py`, `sota_skills.py`) is outside this cluster and documented as GAPs 001–009.
