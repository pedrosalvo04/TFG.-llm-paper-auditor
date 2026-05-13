## PURGE LOG
Agent: purge_backend_skills_g001
Run date: 2026-05-08

| gap_id | original claim | source check performed | correction applied |
|--------|---------------|----------------------|-------------------|
| g_001 | Prose in Section 1.1 stated "exports exactly **14** symbols"; SOURCE annotation pointed to `__init__.py:1` (module docstring line) | Read `backend/skills/__init__.py:36–51`; counted entries in `__all__` literal; confirmed actual count is **15** (BaseSkill + 4 auditor + 2 chatbot + 5 sota + 3 regex); confirmed `__all__` declaration starts at line 36, not line 1 | Changed prose count from `14` to `15`; updated SOURCE from `__init__.py:1` to `__init__.py:36`; table left unchanged (already correct) |

No [GAP] markers inserted: the correct value is confirmed by source and by the existing table — a structured absence placeholder is not appropriate here.

---

# Extracted Specification — cluster_backend_skills_01
## Agent: ext_backend_skills_01

---

## 1. Skill Registry & Package Init (`__init__.py`)

### 1.1 Exported Symbols

`SOURCE: __init__.py:36`

The `__all__` list (lines 36-52) exports exactly **15** symbols:

| Symbol | Origin Module |
|---|---|
| `BaseSkill` | `backend.skills.base_skill` |
| `InformationExtractionSkill` | `backend.skills.auditor_skills` |
| `ReproducibilityEvaluationSkill` | `backend.skills.auditor_skills` |
| `MetricsCalculationSkill` | `backend.skills.auditor_skills` |
| `MetadataAggregationSkill` | `backend.skills.auditor_skills` |
| `ConversationalResponseSkill` | `backend.skills.chatbot_skills` |
| `ContextValidationSkill` | `backend.skills.chatbot_skills` |
| `ThematicCoverageSkill` | `backend.skills.sota_skills` |
| `QueryGenerationSkill` | `backend.skills.sota_skills` |
| `SemanticScholarSearchSkill` | `backend.skills.sota_skills` |
| `CoverageGapAnalysisSkill` | `backend.skills.sota_skills` |
| `CrossValidationSkill` | `backend.skills.sota_skills` |
| `LimitationsQualityDetectionSkill` | `backend.skills.regex_detection_skills` |
| `SoftwareVersionDetectionSkill` | `backend.skills.regex_detection_skills` |
| `HardwareDetailDetectionSkill` | `backend.skills.regex_detection_skills` |

**NOTE — NOT exported but defined in the package:**
- `ChecklistVerificationSkill` (defined in `auditor_skills.py:319`) — absent from `__init__.py`
- `HybridHyperparameterExtractionSkill` (defined in `rag_extraction_skill.py:27`) — absent from `__init__.py`
- All other regex detection skills in `regex_detection_skills.py` (`HyperparameterDetectionSkill`, `DataAvailabilityDetectionSkill`, `CodeAvailabilityDetectionSkill`, `StatisticsDetectionSkill`, `EnvironmentalImpactDetectionSkill`, `ProblematicPhrasesDetectionSkill`, `LlmUsageDetectionSkill`, `CrowdsourcingDetectionSkill`, `LicenseDetectionSkill`) — absent from `__init__.py`

### 1.2 Skill Registration Logic

DETAIL: None — `__init__.py` performs only re-export via `from ... import` statements and defines `__all__`. No registry class, no factory, no dynamic registration logic.

---

## 2. Base Skill Interface (`base_skill.py`)

### 2.1 Class Hierarchy & Abstract Methods

```
BaseSkill (ABC)
└── CompositeSkill(BaseSkill)
```

`SOURCE: base_skill.py:10`

`BaseSkill` is an abstract base class. It declares one abstract method:
- `execute(self, context: Dict[str, Any]) -> Dict[str, Any]` — `SOURCE: base_skill.py:34`

### 2.2 Constructor Parameters and Instance Fields

**`BaseSkill.__init__`** (`SOURCE: base_skill.py:19`):
- Parameter `llm_client: Optional[LLMClient] = None` — stored as `self.llm_client`
- Parameter `config: Optional[Dict] = None` — stored as `self.config`; if `None`, set to `{}`
- `self.name` — set to `self.__class__.__name__` (runtime class name)
- Side effect: calls `logger.debug(f"Skill '{self.name}' inicializado")`

**`CompositeSkill.__init__`** (`SOURCE: base_skill.py:91`):
- Parameter `skills: list[BaseSkill]` — stored as `self.skills`
- Parameter `llm_client: Optional[LLMClient] = None` — passed to `super().__init__(llm_client)`
- Side effect: calls `self.log_execution(f"Skill compuesto con {len(skills)} skills")`

### 2.3 Method-by-Method Decomposition

**`BaseSkill.validate_context(self, context, required_keys)`** (`SOURCE: base_skill.py:47`):
- Computes `missing_keys = [key for key in required_keys if key not in context]`
- If `missing_keys` is non-empty: calls `logger.error(f"Skill '{self.name}': Faltan claves en contexto: {missing_keys}")`, returns `False`
- If all keys present: returns `True`
- Return type: `bool`

**`BaseSkill.log_execution(self, message, level="info")`** (`SOURCE: base_skill.py:64`):
- Prepends `[self.name]` to `message` → `full_message`
- Routes to `logger.info`, `logger.warning`, `logger.error`, or `logger.debug` based on `level` string value
- Exact branches: `level == "info"` → `logger.info`; `level == "warning"` → `logger.warning`; `level == "error"` → `logger.error`; else → `logger.debug`
- No return value

**`CompositeSkill.execute(self, context)`** (`SOURCE: base_skill.py:103`):
- Creates `accumulated_context = context.copy()`
- Iterates `self.skills` with `enumerate(self.skills, 1)`
- For each `(i, skill)`: calls `self.log_execution(f"Ejecutando skill {i}/{len(self.skills)}: {skill.name}")`
- Calls `skill.execute(accumulated_context)` wrapped in `try/except Exception as e`
- On success: calls `accumulated_context.update(result)` to merge returned dict into accumulator
- On exception: calls `self.log_execution(f"Error en skill {skill.name}: {str(e)}", level="error")`, sets `accumulated_context[f"error_{skill.name}"] = str(e)` (key pattern: `"error_" + skill_class_name`)
- Returns `accumulated_context` (all results merged)

### 2.4 Constants / Class-level Attributes

None at class level. `name` is set per-instance from `__class__.__name__`.

---

## 3. Auditor Skills (`auditor_skills.py`)

### 3.1 Class Hierarchy

```
BaseSkill (ABC)
├── InformationExtractionSkill
├── ReproducibilityEvaluationSkill
├── MetricsCalculationSkill
├── MetadataAggregationSkill
└── ChecklistVerificationSkill   ← NOT in __init__.py
```

`SOURCE: auditor_skills.py:18`

### 3.2 Method-by-Method Decomposition

#### `InformationExtractionSkill.execute` (`SOURCE: auditor_skills.py:21`)

**Input context keys required:** `['paper_text']`

**Guard checks:**
1. `self.validate_context(context, ['paper_text'])` → if fails, returns `{'extracted_info': {}}`
2. `if not self.llm_client` → returns `{'extracted_info': {}}`

**Phase MAP — Section-based segmentation** (`SOURCE: auditor_skills.py:36`):
- Reads `context['paper_text']` into `paper_text`
- Normalises line endings: `paper_text.replace('\r\n', '\n')` → `paper_text_norm`
- Splits into sections with `re.split(r'\n(?=#+ )', '\n' + paper_text_norm)` — splits on lines beginning with `#` (Docling markdown headers)
- Strips each section; filters empty sections
- If `len(sections) > 1`:
  - Computes `total_chars = sum(len(s) for s in sections)`
  - Computes `target = total_chars / 4`
  - Builds `fragments` list by iterating sections: if `len(current_fragment) + len(section) > target AND len(fragments) < 3`, appends `current_fragment` and starts new one; edge case: if `current_fragment` is empty and section alone exceeds target, appends it directly; otherwise concatenates with `"\n\n"`; appends any remaining `current_fragment` at the end
- Fallback (no sections detected): uses `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)`, calls `.split_text(paper_text)`, takes first 4 items (`fragments[:4]`)

**Phase MAP — LLM calls per fragment** (`SOURCE: auditor_skills.py:77`):
- Imports `time` inline
- Iterates `fragments` with index `i`
- For each fragment: calls `get_map_extraction_prompt(fragment)` → `prompt` (CROSS-REFERENCE: `backend.common.prompts`)
- Calls `self.llm_client.generate(prompt)` → `response`; reads `response.text.strip()` → `raw_text`
- Balanced JSON extraction loop: finds first `{` in `raw_text`, then walks char-by-char counting `{`/`}` with a stack counter; when stack reaches 0 the first complete JSON object is isolated
- Calls `json.loads(raw_text)` → `fragment_data`; appends to `map_results`
- Between fragments (not on last): calls `time.sleep(2)` to avoid RPM quota exhaustion
- Catches `Exception` per fragment: logs warning with fragment index and error string; continues to next fragment
- If `map_results` is empty after all fragments: returns `{'extracted_info': {}, 'extraction_error': "Map phase produced no results"}`

**Phase REDUCE — consolidation** (`SOURCE: auditor_skills.py:113`):
- Calls `get_reduce_extraction_prompt(map_results)` → `reduce_prompt` (CROSS-REFERENCE: `backend.common.prompts`)
- Primary attempt: `self.llm_client.generate(reduce_prompt)` → `response.text.strip()` → `raw_text`
- Fallback (on any exception): calls `self.llm_client.client.models.generate_content(model=REDUCE_MODEL_NAME, contents=reduce_prompt, config={"response_mime_type": "application/json", "temperature": 0.0})` (CROSS-REFERENCE: `backend.common.config.REDUCE_MODEL_NAME`)
- Applies same balanced JSON extraction loop on `raw_text`
- Primary JSON parse: `json.loads(raw_text)` → `extracted_info`
- JSON repair fallback: applies `re.sub(r',\s*([\]}])', r'\1', raw_text)` (removes trailing commas) then retries `json.loads`

**Post-REDUCE validation** (`SOURCE: auditor_skills.py:152`):
- Checks `extracted_info.get('paper_type', '').startswith('INVALID')` → if True, returns `{'extracted_info': extracted_info, 'invalid_paper': True, 'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')}`
- Ensures `'thought_process'` key exists; if absent sets it to `"Resumen de consolidación no generado por el modelo."`
- Ensures `'context_mapping'` key exists; if absent reconstructs by collecting `context_mapping` lists from all `map_results`, deduplicating with `set()`, defaulting to `["General Context"]` if empty

**Return on success:**
```python
{
  'extracted_info': extracted_info,
  'invalid_paper': False,
  'map_steps': map_results,       # list of per-fragment dicts
  'reduce_step': extracted_info   # same as extracted_info
}
```

**Return on outer exception:**
```python
{'extracted_info': {}, 'extraction_error': str(e)}
```

---

#### `ReproducibilityEvaluationSkill.execute` (`SOURCE: auditor_skills.py:187`)

**Input context keys:** `extracted_info` (optional key, but if missing/empty returns early), `red_flags` (optional, defaults to `{}`)

**Guard checks:**
- Reads `context.get('extracted_info') or {}` — `or {}` means falsy values (empty dict, None) also fall through
- If `not isinstance(extracted_info, dict)`: logs warning, resets to `{}`
- If `not extracted_info` (empty dict): returns `{'evaluation': {}}`
- If `not self.llm_client`: returns `{'evaluation': {}}`

**Execution:**
- Calls `get_evaluation_signals(extracted_info)` → `signals` (CROSS-REFERENCE: `backend.common.prompts`)
- Calls `get_evaluation_prompt(extracted_info, red_flags)` → `evaluation_prompt` (CROSS-REFERENCE: `backend.common.prompts`)
- Calls `self.llm_client.generate(evaluation_prompt)` → `response.text.strip()` → `raw_text`
- Strips markdown code fences: if `raw_text.startswith("```")`, applies `re.sub(r'^```(?:json)?\n?|```$', '', raw_text, flags=re.MULTILINE).strip()`
- Primary JSON parse: `json.loads(raw_text)` → `evaluation`
- JSON repair: applies `re.sub(r',\s*([\]}])', r'\1', raw_text)` then retries; on persistent failure returns `{'evaluation': {}, 'evaluation_error': f'JSON parse error: {str(e)}'}`
- If `evaluation` is a list: takes `evaluation[0]` (or `{}` if empty)
- If `evaluation` is not a dict: resets to `{}`

**Return on success:**
```python
{'evaluation': evaluation, 'evaluation_signals': signals}
```

**Error handling (outer exception):**
- If `'503'` or `'UNAVAILABLE'` in error message: returns `{'evaluation': {}, 'evaluation_error': 'El modelo LLM está experimentando alta demanda. Intenta nuevamente en unos momentos.'}`
- Otherwise: returns `{'evaluation': {}, 'evaluation_error': error_msg}`

---

#### `MetricsCalculationSkill.execute` (`SOURCE: auditor_skills.py:256`)

**Input context keys required:** `['paper_text']`

**Execution:**
- Reads `context['paper_text']` → `paper_text`
- Reads `context.get('red_flags', {})` → `red_flags`
- Computes `critical_flags`: list of keys from `red_flags` where the value is truthy AND the key does NOT start with `"tiene_"`, `"menciona_"`, `"_"`, `"cantidad_"`, or `"puntos_"`
- Builds `metrics` dict:
  - `"tiempo_segundos"`: `context.get('execution_time', 0)`
  - `"caracteres_leidos"`: `len(paper_text)`
  - `"red_flags_detectadas"`: `len(critical_flags)`

**Return:**
```python
{'metrics': {'tiempo_segundos': int, 'caracteres_leidos': int, 'red_flags_detectadas': int}}
```

---

#### `MetadataAggregationSkill.execute` (`SOURCE: auditor_skills.py:285`)

**Input context keys:** none required (all are read with `.get()`)

**Execution — field mapping (source context key → result key):**
All fields are read from `evaluation = context.get('evaluation', {})` unless noted:

| Result Key | Source | Access Pattern |
|---|---|---|
| `claims` | `evaluation` | `evaluation.get('claims', {})` |
| `limitations` | `evaluation` | `evaluation.get('limitations', {})` |
| `theory_assumptions_proofs` | `evaluation` | `evaluation.get('theory_assumptions_proofs', {})` |
| `experimental_result_reproducibility` | `evaluation` | `evaluation.get('experimental_result_reproducibility', {})` |
| `open_access_data_code` | `evaluation` | `evaluation.get('open_access_data_code', {})` |
| `experimental_setting_details` | `evaluation` | `evaluation.get('experimental_setting_details', {})` |
| `experiment_statistical_significance` | `evaluation` | `evaluation.get('experiment_statistical_significance', {})` |
| `experiments_compute_resource` | `evaluation` | `evaluation.get('experiments_compute_resource', {})` |
| `code_of_ethics` | `evaluation` | `evaluation.get('code_of_ethics', {})` |
| `broader_impacts` | `evaluation` | `evaluation.get('broader_impacts', {})` |
| `safeguards` | `evaluation` | `evaluation.get('safeguards', {})` |
| `licenses` | `evaluation` | `evaluation.get('licenses', {})` |
| `assets` | `evaluation` | `evaluation.get('assets', {})` |
| `crowdsourcing_human_subjects` | `evaluation` | `evaluation.get('crowdsourcing_human_subjects', {})` |
| `irb_approvals` | `evaluation` | `evaluation.get('irb_approvals', {})` |
| `declaration_llm_usage` | `evaluation` | `evaluation.get('declaration_llm_usage', {})` |
| `informacion_extraida` | `context` | `context.get('extracted_info', {})` |
| `red_flags` | `context` | `context.get('red_flags', {})` |
| `metricas` | `context` | `context.get('metrics', {})` |
| `general_analysis_map` | `context` | `context.get('general_analysis_map', [])` |
| `general_analysis_reduce` | `context` | `context.get('general_analysis_reduce', {})` |
| `hybrid_triage_fragments` | `context` | `context.get('hybrid_triage_fragments', [])` |
| `evaluation_signals` | `context` | `context.get('evaluation_signals', {})` |

**Return:** the assembled `result` dict (all 23 fields above, returned directly — not wrapped under a key).

---

#### `ChecklistVerificationSkill.execute` (`SOURCE: auditor_skills.py:325`) ← NOT exported

**Input context keys:** `evaluation` (optional), `paper_text` (optional)

**Guard checks:**
- Reads `context.get('evaluation') or {}` and `context.get('paper_text') or ''`
- If `not isinstance(evaluation, dict)`: resets to `{}`
- If `not evaluation`: returns `{'evaluation': {}}`

**Item selection** (`SOURCE: auditor_skills.py:340`):
- `priority_items` = `['claims', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiments_compute_resource', 'experiment_statistical_significance', 'licenses', 'declaration_llm_usage']`
- Filters `priority_items` to those that: (a) exist as a key in `evaluation`, AND (b) the value is a `dict`
- If `len(to_check) < 8`: collects other keys from `evaluation` where value is a dict AND `value.get('answer') in ['No', 'N/A']`, appends up to `(8 - len(to_check))` of them

**Verification loop** (`SOURCE: auditor_skills.py:362`):
For each `item_key` in `to_check`:
- Reads `item_data = evaluation[item_key]`
- Builds `context_snippet = paper_text[:30000] + "\n[...]\n" + paper_text[-30000:]` (60k chars total)
- Calls `get_verification_prompt(item_key, item_data, context_snippet)` → `prompt` (CROSS-REFERENCE: `backend.common.prompts`)
- Calls `self.llm_client.generate(prompt)` → `response.text.strip()` → `raw_text`
- Strips markdown code fences with `re.sub(r'^```(?:json)?\n?|```$', '', raw_text, flags=re.MULTILINE).strip()`
- Parses `json.loads(raw_text)` → `verification_result`
- If `verification_result.get('was_corrected', False)`: increments `corrections_made`, logs the change
- Always overwrites `evaluation[item_key]` with:
  ```python
  {
    "answer": verification_result.get('answer'),
    "evidence": verification_result.get('evidence'),
    "justification": verification_result.get('justification'),
    "is_no_justified": verification_result.get('is_no_justified', False),
    "verified": True,
    "was_refined": not verification_result.get('was_corrected', False)
  }
  ```
- On exception: logs warning with item key and error string; continues loop

**Return:**
```python
{'evaluation': evaluation}  # mutated in-place
```

### 3.3 Business Rules

RULE: INVALID_PAPER_GATE
TRIGGER: After REDUCE phase of `InformationExtractionSkill.execute`
CONDITION: `extracted_info.get('paper_type', '').startswith('INVALID')`
ACTION IF TRUE: Return `{'extracted_info': extracted_info, 'invalid_paper': True, 'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')}` — halts further processing
ACTION IF FALSE: Continue to post-REDUCE field validation
ERROR: N/A
FIELDS INVOLVED: `paper_type` (from extracted_info), `invalid_reason` (from extracted_info)
CALLS: No sub-calls; pure dict inspection
SOURCE: auditor_skills.py:152

RULE: METRICS_RED_FLAG_FILTER
TRIGGER: `MetricsCalculationSkill.execute` call
CONDITION: For each key `k` in `red_flags`: `value is truthy AND k does not start with ("tiene_", "menciona_", "_", "cantidad_", "puntos_")`
ACTION IF TRUE: Key is counted as a critical red flag
ACTION IF FALSE: Key is excluded from the count
ERROR: N/A
FIELDS INVOLVED: all keys in `red_flags` context dict
CALLS: No sub-calls; pure dict comprehension
SOURCE: auditor_skills.py:265

RULE: CHECKLIST_ITEM_SELECTION
TRIGGER: `ChecklistVerificationSkill.execute` call
CONDITION: Item is in `priority_items` list AND exists in `evaluation` dict AND its value is a dict
ACTION IF TRUE: Item added to `to_check`
ACTION IF FALSE: Fill remaining slots (to reach 8) with evaluation items having `answer in ['No', 'N/A']`
ERROR: N/A
FIELDS INVOLVED: keys of `evaluation`, `answer` field within each item dict
CALLS: No sub-calls
SOURCE: auditor_skills.py:340

### 3.4 LLM Prompt Templates (exact strings)

CROSS-REFERENCE: All prompt templates (`get_map_extraction_prompt`, `get_reduce_extraction_prompt`, `get_evaluation_prompt`, `get_evaluation_signals`, `get_verification_prompt`) are imported from `backend.common.prompts`. Exact strings are NOT available in `auditor_skills.py`. See GAP-cluster_backend_skills_01-001.

### 3.5 Error Handling

| Location | Exception Type | Condition | Recovery | Return |
|---|---|---|---|---|
| `InformationExtractionSkill.execute` MAP loop | `Exception` (broad) | Any error calling `llm_client.generate` or `json.loads` on a fragment | Log warning with fragment index; continue to next fragment | fragment skipped |
| `InformationExtractionSkill.execute` MAP result | implicit (empty check) | `map_results` is empty | Log error | `{'extracted_info': {}, 'extraction_error': "Map phase produced no results"}` |
| `InformationExtractionSkill.execute` REDUCE | `Exception` (broad) | Primary `llm_client.generate` fails | Fallback to `llm_client.client.models.generate_content` with JSON mime type | continues with fallback response |
| `InformationExtractionSkill.execute` REDUCE JSON | `json.JSONDecodeError` | REDUCE response is not valid JSON | Apply trailing-comma regex fix, retry `json.loads` | continues or propagates |
| `InformationExtractionSkill.execute` outer | `Exception` (broad) | Any uncaught error | Log error | `{'extracted_info': {}, 'extraction_error': str(e)}` |
| `ReproducibilityEvaluationSkill.execute` JSON | `json.JSONDecodeError` | Evaluation response not valid JSON | Apply trailing-comma fix, retry; on failure return error dict | `{'evaluation': {}, 'evaluation_error': 'JSON parse error: ...'}` |
| `ReproducibilityEvaluationSkill.execute` 503 | `Exception` where `'503'` or `'UNAVAILABLE'` in message | LLM overload | Return specific user-facing message | `{'evaluation': {}, 'evaluation_error': 'El modelo LLM está experimentando alta demanda...'}` |
| `ChecklistVerificationSkill.execute` per-item | `Exception` (broad) | Any error on individual item verification | Log warning; skip item, continue loop | item left as-is in evaluation |

### 3.6 Return Structures

See method decompositions above. Summary:
- `InformationExtractionSkill`: `{'extracted_info', 'invalid_paper', 'map_steps', 'reduce_step'}` on success
- `ReproducibilityEvaluationSkill`: `{'evaluation', 'evaluation_signals'}` on success
- `MetricsCalculationSkill`: `{'metrics': {'tiempo_segundos', 'caracteres_leidos', 'red_flags_detectadas'}}`
- `MetadataAggregationSkill`: flat dict with 23 keys (see mapping table above)
- `ChecklistVerificationSkill`: `{'evaluation': <mutated dict>}`

---

## 4. RAG Extraction Skill (`rag_extraction_skill.py`)

### 4.1 Class Hierarchy

```
BaseModel (Pydantic)
└── Hyperparameters

BaseSkill (ABC)
└── HybridHyperparameterExtractionSkill   ← NOT in __init__.py
```

`SOURCE: rag_extraction_skill.py:11`

### 4.2 Constructor and Configuration

`HybridHyperparameterExtractionSkill` uses the inherited `BaseSkill.__init__` — no additional constructor.

**Pydantic model `Hyperparameters`** (`SOURCE: rag_extraction_skill.py:11`):

| Field | Type | Description / Default String |
|---|---|---|
| `thought_process` | `str` | "Internal reasoning about the technical details found in this fragment..." |
| `learning_rate` | `str` | "Learning rate value, e.g., '1e-4'... or 'NOT FOUND'" |
| `batch_size` | `str` | "Batch size value, e.g., '32'... or 'NOT FOUND'" |
| `epochs` | `str` | "Number of epochs, e.g., '100'... or 'NOT FOUND'" |
| `optimizer` | `str` | "Optimizer name, e.g., 'AdamW', 'SGD', or 'NOT FOUND'" |
| `warmup_steps` | `str` | "Warmup steps or ratio, e.g., '1000', '0.1', or 'NOT FOUND'" |
| `weight_decay` | `str` | "Weight decay value, e.g., '0.01', '1e-5', or 'NOT FOUND'" |
| `random_seed` | `str` | "Random seed value, e.g., '42', or 'NOT FOUND'" |
| `betas` | `str` | "Adam betas, e.g., '(0.9, 0.999)', or 'NOT FOUND'" |
| `epsilon` | `str` | "Adam epsilon, e.g., '1e-8', or 'NOT FOUND'" |
| `training_steps` | `str` | "Total optimization steps, e.g., '100k', '50000', or 'NOT FOUND'" |
| `total_tokens` | `str` | "Total tokens trained on, e.g., '3T', '100B', or 'NOT FOUND'" |
| `hardware` | `str` | "Hardware details, e.g., '8x NVIDIA A100', '1 TPU v4', or 'NOT FOUND'" |
| `latency_metrics` | `str` | "Performance metrics like latency or throughput, e.g., '2% increase', or 'NOT FOUND'" |

All fields use `pydantic.Field(description=...)` annotations. No default values (all are required).

### 4.3 Method-by-Method Decomposition

#### `HybridHyperparameterExtractionSkill.execute` (`SOURCE: rag_extraction_skill.py:30`)

**Input context keys required:** `['paper_text']`

**Step 1 — Logical chunking** (`SOURCE: rag_extraction_skill.py:38`):
- Reads `context['paper_text']` → `paper_text`
- Normalises: `paper_text.replace('\r\n', '\n')` → `paper_text_norm`
- Splits with `re.split(r'\n\n+', paper_text_norm)` — on double newlines (Docling paragraph separators)
- Filters: `[c.strip() for c in raw_chunks if len(c.strip()) > 10]` → `chunks`

**Step 2 — Embedding generation via Google Generative Language API** (`SOURCE: rag_extraction_skill.py:56`):
- `batch_size = 15`
- `api_key = os.getenv("GOOGLE_API_KEY")`
- `url = f"https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL_NAME}:batchEmbedContents?key={api_key}"` (CROSS-REFERENCE: `EMBEDDING_MODEL_NAME` from `backend.common.config`)
- Iterates chunks in batches of 15, with `time.sleep(15)` between batches (except first)
- Per batch: builds `requests` list as `[{"model": f"models/{EMBEDDING_MODEL_NAME}", "content": {"parts": [{"text": c}]}} for c in batch]`
- POSTs to URL with `httpx.post(url, json={"requests": requests})` — bypasses SDK to avoid vector merging issue
- On status != 200: raises `Exception(f"Error embeddings API: {response.text}")`
- Collects `emb["values"]` from `data["embeddings"]` for each response item → appends to `embeddings` list

**Step 3 — ChromaDB population** (`SOURCE: rag_extraction_skill.py:85`):
- Creates in-memory `chromadb.Client()`
- Deletes collection `"paper_chunks"` if it exists (try/except with bare `except: pass`)
- Creates collection `"paper_chunks"`
- Adds: `ids=[str(i) for i in range(len(chunks))]`, `embeddings=embeddings`, `documents=chunks`

**Step 4 — RAG query** (`SOURCE: rag_extraction_skill.py:99`):
- 13 fixed query strings (exact strings `SOURCE: rag_extraction_skill.py:99-113`):
  1. `"training details optimization hyperparameters"`
  2. `"learning rate schedule step size warmup decay learning rate"`
  3. `"batch size mini-batch micro-batch optimization global batch size"`
  4. `"epochs training steps iterations convergence training duration"`
  5. `"optimizer Adam SGD AdamW RMSprop momentum betas optimizer settings"`
  6. `"weight decay L2 regularization weight decay"`
  7. `"random seed reproducibility seed fixed seed initialization"`
  8. `"hardware GPU TPU NVIDIA AMD cluster infrastructure hardware setup"`
  9. `"hyperparameters configuration settings parameters appendix details"`
  10. `"experimental setup implementation details training configuration"`
  11. `"SFT Supervised Fine-tuning instruction tuning training schedule"`
  12. `"pre-training pretraining phase training protocols"`
  13. `"hyperparameter tuning iterations schedule iterations iterations"`
- Generates query embeddings via `self.llm_client.client.models.embed_content(model=EMBEDDING_MODEL_NAME, contents=queries)` → `[e.values for e in q_emb_res.embeddings]`
- Calls `collection.query(query_embeddings=query_embeddings, n_results=10)` → `results`

**Step 5 — Relevance scoring** (`SOURCE: rag_extraction_skill.py:127`):
- Merges all query results, keeping minimum distance per unique doc: `chunk_relevance[doc] = min(existing, dist)` for each document
- Sorts by ascending distance → `sorted_chunks`
- Converts distance to relevance score (0-100):
  - `distance < 0.4`: `score = int(95 - (distance * 25))` (range: 85–95)
  - `0.4 ≤ distance < 0.7`: `score = int(85 - ((distance - 0.4) * 180))` (range: 31–85)
  - `distance ≥ 0.7`: `score = max(5, int(31 - ((distance - 0.7) * 50)))` (min 5)

**Step 6 — MAP Phase: per-chunk LLM extraction** (`SOURCE: rag_extraction_skill.py:143`):
- For each `(idx, chunk)` in `relevant_chunks`:
- Builds inline prompt (exact template `SOURCE: rag_extraction_skill.py:159-175`):
  ```
  You are a rigorous NeurIPS reviewer performing technical triage on a paper fragment.
  Extract all hyperparameters, scale metrics, and performance data found in this text.
  
  FIELDS TO EXTRACT:
  - learning_rate, batch_size, epochs, training_steps, total_tokens, optimizer, warmup_steps, weight_decay, hardware, latency_metrics.
  
  REASONING INSTRUCTIONS:
  - If the fragment contains optimization steps (e.g. "100k steps") or total tokens (e.g. "2 trillion tokens"), extract them as training_steps and total_tokens.
  - Capture any performance data like "latency was less than 2%" or "throughput of 500 tokens/s" under latency_metrics.
  - Be smart about noisy table text (e.g., if columns are misaligned, try to reconstruct the key-value pair logically).
  
  TEXT FRAGMENT:
  {chunk}
  
  RETURN ONLY A VALID JSON OBJECT WITH THE FIELDS ABOVE. Use "NOT FOUND" if missing.
  ```
- Calls `self.llm_client.generate(prompt)`, applies balanced JSON extraction loop, calls `json.loads`
- Adds `fragment_data['_relevance_score'] = relevance_score` and `fragment_data['_chunk_text'] = chunk`
- Appends to `extracted_fragments`; sleeps 1s between chunks
- On exception per chunk: logs warning, continues

**Step 7 — REDUCE Phase** (`SOURCE: rag_extraction_skill.py:204`):
- Builds inline reduce prompt (exact template `SOURCE: rag_extraction_skill.py:206-221`):
  ```
  You are a senior AI researcher reviewing a paper's hyperparameter extraction.
  Below is a list of independent extractions from various parts of the paper (e.g., Pre-training, SFT, RLHF).
  Your job is to consolidate them into a single definitive set of hyperparameters.
  
  RULES:
  - If there are conflicts (e.g. SFT batch size is 256, Pre-training is 1280), prefer the final fine-tuning/SFT parameters if obvious, or pick the most representative one.
  - If an extraction says 'NOT FOUND', ignore it if another extraction found a valid value.
  - If no valid value is found across all fragments for a field, output 'NOT FOUND'.
  - Use the 'thought_process' from each fragment to build a final synthesis.
  - TABLE VALIDATION: If multiple fragments cite different tables for the same value, verify which table title and headers match the target hyperparameter (e.g., differentiate between a 'Model Architecture' table and a 'Training Hyperparameters' table).
  - DO NOT guess or hallucinate.
  
  EXTRACTIONS:
  {json.dumps(extracted_fragments, indent=2)}
  ```
- Primary: `self.llm_client.generate(reduce_prompt)`
- Fallback (on any exception): `self.llm_client.client.models.generate_content(model=EVALUATION_MODEL_NAME, contents=reduce_prompt, config={'response_mime_type': 'application/json', 'response_schema': Hyperparameters, 'temperature': 0.0})`  (CROSS-REFERENCE: `EVALUATION_MODEL_NAME` from `backend.common.config`)
- Applies balanced JSON extraction loop; JSON repair with trailing-comma regex on `JSONDecodeError`

**Step 8 — Regex cleaning** (`SOURCE: rag_extraction_skill.py:265`):
- Calls `self._clean_with_regex(extracted_json)` → `cleaned_data`

**Return on success:**
```python
{'extracted_hyperparameters_hybrid': cleaned_data, 'triage_fragments': extracted_fragments}
```

**Return on outer exception:**
```python
{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str(e)}
```

---

#### `HybridHyperparameterExtractionSkill._clean_with_regex` (`SOURCE: rag_extraction_skill.py:277`)

**Input:** `data: Dict[str, str]` — extracted hyperparameter dict from REDUCE phase

**For each `(key, value)` in data:**
- Converts to `str_val = str(value).strip()`
- If `str_val.upper() in ['NOT FOUND', 'N/A', 'NONE', 'MISSING']` or `str_val == ''`: sets `cleaned[key] = 'NOT FOUND'`, continues

**Key-specific cleaning:**
- `key in ['learning_rate', 'weight_decay']`:
  - Tries `re.search(r'(\d+(?:\.\d+)?)\s*(?:[x*]\s*10\s*\^?\s*\(?\s*(-\d+)\s*\)?|e(-\d+))', str_val, re.IGNORECASE)`
  - On match: `base = float(group1)`, `exp = int(group2 or group3)`, `cleaned[key] = float(f"{base * (10 ** exp):.8f}")`
  - On no match: tries `re.search(r'0\.\d+', str_val)` → `float(match.group())` if found; else `str_val`
- `key == 'epsilon'`:
  - Tries `re.search(r'1e-\d+', str_val, re.IGNORECASE)` — if match or not, always sets `cleaned[key] = str_val` (no numeric conversion)
- `key in ['batch_size', 'epochs', 'random_seed']`:
  - Tries `re.search(r'\b\d+\b', str_val)` → `int(match.group())` if found; else `str_val`
- All other keys: `cleaned[key] = str_val`

**Return:** `cleaned` dict with values as `float`, `int`, or `str`

### 4.4 Vector Store / Embedding Operations

- **Client:** `chromadb.Client()` (in-memory, ephemeral per execution)
- **Collection name:** `"paper_chunks"` (deleted and recreated on each call)
- **Embedding model:** `EMBEDDING_MODEL_NAME` (CROSS-REFERENCE: `backend.common.config`)
- **Embedding API endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL_NAME}:batchEmbedContents`
- **Batch size for embedding:** 15 chunks, 15 seconds sleep between batches
- **Query transport:** `self.llm_client.client.models.embed_content` (SDK) for query embeddings

### 4.5 Retrieval Logic

- `n_results=10` per query
- 13 queries in parallel (single `collection.query` call with all 13 query embeddings)
- Deduplication: minimum-distance-wins per unique document text
- Ranking: ascending distance (lower = more relevant)
- Score formula: piecewise linear function of ChromaDB L2/cosine distance

### 4.6 Business Rules

RULE: RAG_CONFLICT_RESOLUTION
TRIGGER: REDUCE phase prompt instruction
CONDITION: Two fragments report different values for the same hyperparameter field
ACTION IF TRUE: Prefer final fine-tuning/SFT parameters if identifiable; otherwise pick most representative value
ACTION IF FALSE: Use the single found value
ERROR: N/A
FIELDS INVOLVED: Any hyperparameter field with multiple found values across fragments
CALLS: LLM decision — no deterministic code enforces this; it is a prompt instruction
SOURCE: rag_extraction_skill.py:206

### 4.7 Error Handling

| Location | Exception | Recovery |
|---|---|---|
| Embedding API call | `httpx.post` returns non-200 | Raises `Exception(f"Error embeddings API: {response.text}")` — propagates to outer handler |
| ChromaDB delete | Any | `except: pass` — silently ignored |
| MAP per-chunk | `Exception` | Log warning, continue to next chunk |
| REDUCE primary | `Exception` | Fallback to `models.generate_content` with Pydantic schema |
| REDUCE JSON parse | `json.JSONDecodeError` | Trailing-comma regex fix, retry |
| Outer | `Exception` | Returns `{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str(e)}` |

### 4.8 Return Structures

```python
# Success
{'extracted_hyperparameters_hybrid': Dict[str, Any], 'triage_fragments': List[Dict]}
# Each triage_fragment contains: all hyperparameter fields + '_relevance_score': int + '_chunk_text': str

# Failure
{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str}
```

---

## 5. Regex Detection Skills (`regex_detection_skills.py`)

### 5.1 Class Hierarchy

```
(module-level helpers)
├── NEGATION_WINDOW: int = 60
├── NEGATION_PATTERNS: re.Pattern
├── _is_negated(text, match_start) -> bool
├── _search_with_negation(pattern, text, flags) -> Optional[re.Match]
└── TableExtractionHelper (plain class, not BaseSkill)

BaseSkill (ABC)
├── HyperparameterDetectionSkill    ← NOT exported via __init__.py
├── DataAvailabilityDetectionSkill  ← NOT exported
├── CodeAvailabilityDetectionSkill  ← NOT exported
├── StatisticsDetectionSkill        ← NOT exported
├── EnvironmentalImpactDetectionSkill ← NOT exported
├── ProblematicPhrasesDetectionSkill  ← NOT exported
├── LlmUsageDetectionSkill            ← NOT exported
├── CrowdsourcingDetectionSkill       ← NOT exported
├── LicenseDetectionSkill             ← NOT exported
├── LimitationsQualityDetectionSkill  ← exported
├── SoftwareVersionDetectionSkill     ← exported
└── HardwareDetailDetectionSkill      ← exported
```

`SOURCE: regex_detection_skills.py:1`

### 5.2 ALL Regex Patterns

#### Module-level: NEGATION_PATTERNS (`SOURCE: regex_detection_skills.py:10`)

**Pattern string (compiled with `re.IGNORECASE`):**
```
(?:no\s+se\s+(?:especifica|menciona|indica|reporta|incluye|proporciona|detalla))
|(?:falta(?:n)?(?:\s+informaci[oó]n)?)
|(?:sin\s+(?:especificar|detallar|mencionar|incluir|reportar|proporcionar))
|(?:not\s+(?:specified|mentioned|reported|provided|included|disclosed|found))
|(?:missing|absent|omitted|lacks?|without)
|(?:ERROR\s*\d*\s*:)
```
**Purpose:** Detects negation phrases in the 60-character window preceding a regex match.

---

#### `TableExtractionHelper.extract_tables` patterns (`SOURCE: regex_detection_skills.py:47`):

| Pattern Name | Pattern String | Flags | Purpose |
|---|---|---|---|
| table_pattern | `r"(Table\|Tab\.)\s+\d+[:\.]?[^\n]*\n([\s\S]{0,2000}?)(?=\n\s*\n\|Table\|Tab\\.|\Z)"` | `re.IGNORECASE` | Extracts "Table N:" or "Tab. N." prefixed blocks (up to 2000 chars) |
| pipe_table_pattern | `r"(\|[^\n]+\|\n){3,}"` | none | Extracts markdown/LaTeX pipe tables (3+ consecutive pipe-delimited rows) |
| tab_table_pattern | `r"([^\n]+\t[^\n]+\t[^\n]+\n){3,}"` | none | Extracts tab-separated tables (3+ consecutive rows with 2+ tabs) |

`extract_tables` also applies `re.sub(r'<br\s*/?>', ' ', raw)` to normalize HTML `<br>` tags in matched table text.

---

#### `HyperparameterDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:89`):

| Key | Pattern Strings | Flags |
|---|---|---|
| `optimizer` | `r"(?:we\s+use\|using\|with)\s+(?:the\s+)?(AdamW\|Adam\|SGD\|RMSprop\|Adagrad\|LAMB\|LARS)\s*(?:optimizer)?"` | IGNORECASE |
| | `r"optimizer[:\s=]+\s*(AdamW\|Adam\|SGD\|RMSprop\|LAMB)"` | IGNORECASE |
| | `r"(AdamW\|Adam\|SGD\|RMSprop\|LAMB)\s+optimizer"` | IGNORECASE |
| `learning_rate` | `r"learning\s+rate.{0,20}(?:is\|of\|at)?\s*([\d\.e\-×\^]+)"` | IGNORECASE |
| | `r"(?:LR\|lr)\s*[:=]\s*([\d\.e\-×\^]+)"` | IGNORECASE |
| | `r"learning\s+rate\s+is\s+linearly\s+increased\s+from\s+0\s+to\s+([\d\.e\-×\^]+)"` | IGNORECASE |
| | `r"rate\s+of\s+([\d\.e\-]+)"` | IGNORECASE |
| `batch_size` | `r"(?:batch[\s_-]size\|global[\s_-]batch\|micro[\s-]?batch)[\s:=]+.{0,20}(\d{2,})"` | IGNORECASE |
| | `r"(\d{2,})\s*(?:samples?\|examples?)\s*per\s*(?:batch\|GPU)"` | IGNORECASE |
| `epochs` | `r"(?:trained?\s+for\|over)\s+(\d+)\s*(?:epochs?\|steps?\|iterations?)"` | IGNORECASE |
| | `r"(?:epochs?\|training[\s_-]steps?)[\s:=]+(\d+)"` | IGNORECASE |
| | `r"(\d+)\s*(?:epochs?\|training\s+steps)"` | IGNORECASE |
| `warmup` | `r"warmup[\s:=]+(\d+)"` | IGNORECASE |
| | `r"(\d+)\s*warmup\s*steps?"` | IGNORECASE |
| | `r"warm[\s-]?up.{0,20}(?:of\|for\|=\|:)\s*(\d+)"` | IGNORECASE |
| | `r"Warmup-Stable-Decay"` | IGNORECASE |
| `weight_decay` | `r"(?:weight[\s_-]decay\|\$\\lambda\$\|L2[\s_-]regularization)[\s:=,]+.{0,30}(\d+\.\d+)"` | IGNORECASE |
| | `r"(?:decay\|wd)\s*[=:]\s*(\d+\.\d+)"` | IGNORECASE |
| | `r"(?:weight.decay\|regularization)\s+(?:of\|is\|coefficient)\s+(\d+\.\d+)"` | IGNORECASE |
| `betas` | `r"(?:\$\\beta_[12]\$\|beta[\s_-]?[12]\|betas?)[\s:=,]+.{0,30}\d+\.\d+"` | IGNORECASE |
| | `r"\(\s*(?:β\|beta)?\s*0\.9\d*\s*,\s*0\.9\d*\s*\)"` | IGNORECASE |
| | `r"(?:momentum\|beta)\s+(?:coefficients?\|parameters?).{0,40}\d+\.\d+"` | IGNORECASE |
| `epsilon` | `r"(?:epsilon\|\$\\epsilon\$\|eps)[\s:=]+(\d+\.?\d*[eE][-+]?\d+)"` | IGNORECASE |
| | `r"(\d+\.\d+[eE][-+]?\d+).{0,20}(?:epsilon\|numerical[\s_-]stability)"` | IGNORECASE |
| `vague` | `r"(?:standard\s+settings\|default\s+parameters\|typical\s+configuration\|not\s+disclosed\|internal\s+experimentation\|cannot\s+be\s+disclosed\|hyperparameters?\s+(?:were\s+)?(?:not\s+)?tuned)"` | IGNORECASE |

---

#### `DataAvailabilityDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:191`):

| Key | Pattern String | Flags |
|---|---|---|
| `proprietary` | `r"(our\|the\|this)\s+(proprietary\|confidential\|internal\|restricted)\s+.{0,50}(data\|dataset)\|cannot\s+(disclose\|release\|share)\s+.{0,30}(data\|dataset)\|data.{0,30}(not\s+(publicly\s+)?available\|remain\s+confidential)"` | IGNORECASE |
| `available` | `r"(available\s+at\|download\|DOI\|zenodo\|figshare\|huggingface\.co/datasets\|github\.com/.+/data\|data\s+is\s+released)"` | IGNORECASE |
| `doi` | `r"DOI[\s:]+.{0,20}(dataset\|data)"` | IGNORECASE |
| `cannot_release` | `r"cannot\s+(release\|disclose\|share)\s+.{0,30}(data\|dataset)"` | IGNORECASE |

---

#### `CodeAvailabilityDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:237`):

| Key | Pattern String(s) | Flags |
|---|---|---|
| `proprietary` | `r"(proprietary\|confidential\|cannot\s+(disclose\|release\|share)\|not\s+(publicly\s+)?available\|internal\|competitive\s+concerns?)\s+.{0,80}(code\|implementation\|source\|repository\|training\s+code)\|restricted\s+(?!to\s+a\s+(computational\|budget)).{0,50}(code\|implementation\|source\|repository)"` | IGNORECASE |
| `repository` | `r"(?:https?://)?(?:www\.)?(github\|gitlab\|bitbucket\|sourceforge)\.(?:com\|org)/[\w.-]+/[\w.-]+"` | IGNORECASE |
| | `r"github\.com/[\w.-]+"` | IGNORECASE |
| | `r"[\w.-]+\.github\.io"` | IGNORECASE |
| | `r"(?:huggingface\.co\|hf\.co)/[\w.-]+/"` | IGNORECASE |
| | `r"project\s+page\s+at\s+(https?://\S+)"` | IGNORECASE |
| | `r"code\s+(?:available\|released)\s+at\s+(https?://\S+)"` | IGNORECASE |
| `github` | `r"github\.com/[\w.-]+"` | IGNORECASE |
| `cannot_release` | `r"cannot\s+(release\|disclose\|share)\s+.{0,30}(code\|implementation)"` | IGNORECASE |

---

#### `StatisticsDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:290`):

| Key | Pattern Strings | Flags |
|---|---|---|
| `confidence_intervals` | `r"(confidence\s+interval\|standard\s+deviation\|std\.?\s+dev\|error\s+bar\|±\|\+/-\|variance\|std\s+err)"` | IGNORECASE |
| | `r"CI\s*=\s*\d+"` | IGNORECASE |
| | `r"\d+\.\d+\s*±\s*\d+\.\d+"` | IGNORECASE |
| | `r"error\s+bars?"` | IGNORECASE |
| | `r"standard\s+errors?"` | IGNORECASE |
| | `r"confidence\s+level"` | IGNORECASE |
| `significance` | `r"(p-value\|p\s*<\|statistical\s+significance\|t-test\|ANOVA\|Mann-Whitney\|Wilcoxon\|chi-square)"` | IGNORECASE |
| | `r"p\s*=\s*\d+\.\d+"` | IGNORECASE |
| | `r"statistically\s+significant"` | IGNORECASE |
| | `r"significance\s+test"` | IGNORECASE |
| | `r"benchmarks?\s+(?:evaluation\|results\|performance).{0,50}(?:MMLU\|GSM8K\|HumanEval\|ImageNet\|COCO\|Cityscapes\|Atari\|Gym\|standard\s+benchmarks)"` | IGNORECASE |
| `multiple_runs` | `r"(multiple\s+runs?\|\d+\s+seeds?\|random\s+seeds?\|\d+\s+executions?\|\d+\s+trials?)"` | IGNORECASE |
| | `r"repeated\s+\d+\s+times"` | IGNORECASE |
| | `r"average\s+(of\|over)\s+\d+\s+(runs?\|experiments?)"` | IGNORECASE |
| | `r"\d+\s+independent\s+(runs?\|experiments?)"` | IGNORECASE |
| | `r"seed\s*=\s*\d+"` | IGNORECASE |

---

#### `EnvironmentalImpactDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:357`):

| Key | Pattern Strings | Flags |
|---|---|---|
| `carbon_footprint` | `r"(\d+\.\d+\s*tCO2eq\|carbon\s+footprint\|CO2\s+emissions\|environmental\s+impact\|Table\s+6)"` | IGNORECASE |
| | `r"carbon.{0,30}emissions?"` | IGNORECASE |
| | `r"greenhouse\s+gas"` | IGNORECASE |
| | `r"CO2.{0,30}(footprint\|impact\|emissions?)"` | IGNORECASE |
| | `r"environmental.{0,30}(cost\|impact\|footprint)"` | IGNORECASE |
| `energy_consumption` | `r"(\d+\s*MWh\|\d+\s*kWh\|energy\s+consumption\|power\s+consumption)"` | IGNORECASE |
| | `r"energy.{0,30}(usage\|used\|consumption)"` | IGNORECASE |
| | `r"power.{0,30}(usage\|consumption\|draw)"` | IGNORECASE |
| | `r"\d+.{0,20}(kilowatt\|megawatt).{0,20}hours?"` | IGNORECASE |
| `pue` | `r"(PUE\|Power\s+Usage\s+Effectiveness)[\s:=]+.{0,20}(1\.\d+\|\d+\.\d+)"` | IGNORECASE |
| | `r"efficiency.{0,30}(of\|is\|=\|:).{0,30}\d+\.\d+"` | IGNORECASE |
| | `r"PUE\s*=\s*\d+\.\d+"` | IGNORECASE |

---

#### `ProblematicPhrasesDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:422`):

| Key | Pattern String | Flags |
|---|---|---|
| `competitive_concerns` | `r"(competitive\s+concerns?\|intellectual\s+property\|legal\s+constraints?\|business\s+reasons?)"` | IGNORECASE |
| `cannot_release` | `r"(cannot\s+(release\|disclose\|share)\|unable\s+to\s+(release\|disclose\|share)\|not\s+permitted\s+to)"` | IGNORECASE |
| `remain_confidential` | `r"(data\|code\|implementation).{0,30}(remain\s+confidential\|kept\s+confidential\|undisclosed)"` | IGNORECASE |

---

#### `LlmUsageDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:458`):

| Key | Pattern String | Flags |
|---|---|---|
| `llm_usage` | `r"(ChatGPT\|GPT-4\|GPT-3\|Claude\|LLaMA\|BERT\|RoBERTa\|T5\|LLM\|Large\s+Language\s+Model).{0,60}(annotat\|filter\|evaluat\|generat\|process\|label)"` | IGNORECASE |

---

#### `CrowdsourcingDetectionSkill` patterns (`SOURCE: regex_detection_skills.py:483`):

**`CROWDSOURCING_ACTIVE` patterns (list):**
1. `r"(?<!no\s)(?<!without\s)(?<!not\s)\b(crowdsourc|Mechanical\s+Turk|MTurk|Prolific|Scale\s+AI)\b"` — negative lookbehind for "no ", "without ", "not "
2. `r"\b(we\s+(?:hired|recruited|employed|paid)\s+.{0,30}(?:annotator|worker|participant))"`
3. `r"\b(human\s+annotators?\s+(?:were|are|were\s+asked|labeled|annotated))"`
4. `r"\b(participants?\s+(?:were\s+)?(?:recruited|compensated|paid))"`

**`HUMAN_DATASET_USE` patterns (list):**
1. `r"\b(human[\s-]?label(?:ed|ing)|human[\s-]?annotat(?:ed|ion))\b"`
2. `r"\b(SFT|RLHF|human\s+feedback|preference\s+data).{0,40}(?:dataset|data|corpus)"`

**`COMPENSATION`:** `r"\b(compensation|wage|paid\s+(?:at|\$)|minimum\s+wage|hourly\s+rate|instructions\s+provided|consent\s+form)\b"`

**`NEGATION_CROWD`:** `r"(?:no|not|without|does\s+not\s+use|did\s+not\s+use).{0,20}(?:human\s+subject|human\s+annotator|crowdsourc|human\s+participant)"`

---

#### `LicenseDetectionSkill` patterns (`SOURCE: regex_detection_skills.py:531`):

| Name | Pattern String | Flags |
|---|---|---|
| `EXPLICIT_LICENSE` | `r"(CC[\s-]BY(?:[\s-]\d\.\d)?(?:[\s-](?:SA\|NC\|ND))*\|MIT\s+[Ll]icense\|Apache\s+2\.0\|GPL(?:[\s-]\d)?\|BSD(?:[\s-]\d[\s-][Cc]lause)?\|Creative\s+Commons\|\bCC0\b)"` | IGNORECASE |
| `KNOWN_DATASETS` | `r"\b(ImageNet\|COCO\|CIFAR\|MNIST\|WikiText\|RedPajama\|OpenWebText\|Alpaca\|ShareGPT\|LAION\|WMT\d+\|SQuAD\|GLUE\|SuperGLUE\|HumanEval\|GSM8K\|MMLU\|CommonCrawl\|BookCorpus\|The\s+Pile)\b"` | IGNORECASE |

---

#### `LimitationsQualityDetectionSkill` patterns (`SOURCE: regex_detection_skills.py:564`):

**`SPECIFIC_PATTERNS` (list, used with `_search_with_negation`):**
1. `r"(?:limitation|weakness).{0,60}(?:\d+|specific|quantif|measur|metric)"`
2. `r"(?:bias|toxicity|fairness).{0,40}(?:evaluat|measur|test|audit|analyz)"`
3. `r"(?:fail|error|degrad).{0,40}(?:when|if|under|specific|certain)"`

**`SECTION_PATTERN`:** `r"(?:^|\n)\s*(?:#+\s*[\*_]{0,2}(?:Limitation|Broader\s+Impact|Conclusion|Discussion|Social\s+Impact)[\*_]{0,2}|(?:\*\*|__)Limitations?[\.\s:]|Limitations?[\.\s:])"`

---

#### `SoftwareVersionDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:595`):

1. `r"(?:PyTorch|TensorFlow|JAX|Keras|Transformers)\s*(?:v|version)?\s*\d+\.\d+"`
2. `r"(?:Python|CUDA|cuDNN)\s*(?:v|version)?\s*\d+\.\d+"`
3. `r"(?:numpy|scipy|pandas|scikit)\S*\s*(?:v|version)?\s*\d+\.\d+"`
4. `r"requirements\.txt|environment\.yml|setup\.py|pyproject\.toml"`

All used with `_search_with_negation` (i.e., negation-aware).

---

#### `HardwareDetailDetectionSkill.PATTERNS` (`SOURCE: regex_detection_skills.py:625`):

| Key | Pattern Strings | Flags |
|---|---|---|
| `gpu_model` | `r"(?:A100\|V100\|H100\|A6000\|RTX\s*\d{4}\|MI\d{3}\|TPU\s*v\d)"` | (via `_search_with_negation` → IGNORECASE) |
| | `r"(?:NVIDIA\|AMD\|Google)\s+(?:GPU\|TPU)\s*\S+"` | |
| `gpu_count` | `r"(\d+)\s*(?:x\s*)?(?:GPU\|TPU\|A100\|V100\|H100)"` | |
| | `r"(?:GPU\|TPU)s?\s*(?:x\s*)?(\d+)"` | |
| `gpu_memory` | `r"(\d+)\s*GB\s*(?:GPU\|VRAM\|HBM\|memory)"` | |
| | `r"(?:GPU\|VRAM\|HBM)\s*(?:memory)?\s*(?:of)?\s*(\d+)\s*GB"` | |
| `training_time` | `r"(?:train\|took\|required)\S*\s+(?:for\s+)?(?:approximately\s+)?\d+\s*(?:hours?\|days?\|weeks?\|GPU[\s-]hours?)"` | |
| | `r"\d+\s*(?:GPU[\s-]hours?\|GPU[\s-]days?\|node[\s-]hours?)"` | |

### 5.3 Detection Logic Per Pattern

**General pattern for all regex detection skills:**
1. Call `self.validate_context(context, ['paper_text'])` — if fails, return `{}`
2. Read `text = context['paper_text']`
3. For each category key in `PATTERNS`:
   - Iterate over pattern list; for each pattern:
     - (Where implemented) Search tables first without negation filtering: `re.search(pattern, table_text, re.IGNORECASE)`
     - Search full text with negation filtering: `_search_with_negation(pattern, text)`
   - Stop on first match; set `found = True` and record snippet
4. Build and return results dict based on match/no-match for each category

**Action if match:** Set `found = True`; log snippet; may store `{key}_value` and `{key}_location`
**Action if no match:** Set `found = False`; log `NOT FOUND`

**`HyperparameterDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:177`):
- `has_{key}`: bool for each of: `optimizer`, `learning_rate`, `batch_size`, `epochs`, `warmup`, `weight_decay`, `betas`, `epsilon`, `vague`
- `{key}_value`: matched snippet (if `found and key != 'vague'`)
- `{key}_location`: `"TABLE"` or `"TEXT"`
- Return: `{'hyperparameter_flags': results}`

**`DataAvailabilityDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:223`):
- `datos_propietarios`: found `proprietary`
- `datos_sin_acceso`: NOT found `available`
- `tiene_doi_datos`: found `doi`
- `cannot_release_data`: found `cannot_release`
- Return: `{'data_flags': results}`

**`CodeAvailabilityDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:276`):
- `codigo_propietario`: found `proprietary`
- `sin_repositorio`: NOT found `repository`
- `tiene_github`: found `github`
- `cannot_release_code`: found `cannot_release`
- Return: `{'code_flags': results}`

**`StatisticsDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:344`):
- `sin_intervalos_confianza`: NOT found `confidence_intervals`
- `sin_significancia`: NOT found `significance`
- `sin_multiple_runs`: NOT found `multiple_runs`
- Return: `{'statistics_flags': results}`

**`EnvironmentalImpactDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:409`):
- `tiene_carbon_footprint`: found `carbon_footprint`
- `tiene_energy_consumption`: found `energy_consumption`
- `tiene_pue`: found `pue`
- Return: `{'environmental_flags': results}`

**`ProblematicPhrasesDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:443`):
- `competitive_concerns`: bool
- `cannot_release`: bool
- `remain_confidential`: bool
- Return: `{'problematic_flags': results}`

**`LlmUsageDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:475`):
- `usa_llm_como_herramienta`: bool
- Return: `{'llm_usage_flags': {'usa_llm_como_herramienta': bool}}`

**`CrowdsourcingDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:520`):
- `usa_crowdsourcing`: `has_active_crowd` (False if `has_negation` is True)
- `usa_datasets_humanos`: any `HUMAN_DATASET_USE` match
- `sin_compensacion_mencionada`: `has_active_crowd AND NOT has_comp`
- Return: `{'crowdsourcing_flags': results}`

**`LicenseDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:555`):
- `menciona_licencia`: found `EXPLICIT_LICENSE`
- `usa_datasets_conocidos`: found `KNOWN_DATASETS`
- `posible_licencia_faltante`: `usa_datasets_conocidos AND NOT menciona_licencia`
- Return: `{'license_flags': results}`

**`LimitationsQualityDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:585`):
- `tiene_seccion_limitaciones`: found `SECTION_PATTERN`
- `limitaciones_vagas`: `has_section AND specific_count == 0`
- `puntos_especificos_limitaciones`: count (0–3) of `SPECIFIC_PATTERNS` matched
- Return: `{'limitations_flags': results}`

**`SoftwareVersionDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:615`):
- `tiene_versiones_software`: `found_count > 0`
- `cantidad_versiones`: count of matched patterns (0–4)
- Return: `{'software_flags': results}`

**`HardwareDetailDetectionSkill` result keys** (`SOURCE: regex_detection_skills.py:660`):
- `tiene_gpu_model`: bool
- `tiene_gpu_count`: bool
- `tiene_gpu_memory`: bool
- `tiene_training_time`: bool
- Return: `{'hardware_detail_flags': results}`

### 5.4 Business Rules

RULE: NEGATION_CONTEXT_FILTER
TRIGGER: Every call to `_search_with_negation` within any detection skill
CONDITION: Characters at positions `[max(0, match_start-60) : match_start]` match `NEGATION_PATTERNS`
ACTION IF TRUE: Match is discarded; search continues to next match candidate
ACTION IF FALSE: Match is accepted and returned
ERROR: N/A
FIELDS INVOLVED: `text` (full paper text), `match_start` (position of regex match)
CALLS: `_is_negated(text, match_start)` → `NEGATION_PATTERNS.search(preceding_60_chars)`
SOURCE: regex_detection_skills.py:21

RULE: TABLE_SEARCH_PRIORITY
TRIGGER: `HyperparameterDetectionSkill.execute` and `StatisticsDetectionSkill.execute`
CONDITION: `table_text` (extracted table content) is non-empty
ACTION IF TRUE: Search tables first WITHOUT negation filtering (numeric table values assumed literal); if table match found, skip full-text search; set `search_location = "TABLE"`
ACTION IF FALSE: Proceed directly to full-text negation-aware search
ERROR: N/A
FIELDS INVOLVED: `table_text`, `found`, `matched_snippet`, `search_location`
CALLS: `TableExtractionHelper.extract_tables(text)`
SOURCE: regex_detection_skills.py:155

RULE: CROWDSOURCING_NEGATION_GATE
TRIGGER: `CrowdsourcingDetectionSkill.execute`
CONDITION: `NEGATION_CROWD` pattern found anywhere in `text`
ACTION IF TRUE: Sets `has_active_crowd = False` without running `CROWDSOURCING_ACTIVE` patterns
ACTION IF FALSE: Runs all `CROWDSOURCING_ACTIVE` patterns
ERROR: N/A
FIELDS INVOLVED: `has_negation`, `has_active_crowd`
CALLS: `re.search(self.NEGATION_CROWD, text, re.IGNORECASE)`
SOURCE: regex_detection_skills.py:506

RULE: LICENSE_GAP_DETECTION
TRIGGER: `LicenseDetectionSkill.execute`
CONDITION: `usa_datasets_conocidos == True AND menciona_licencia == False`
ACTION IF TRUE: Sets `posible_licencia_faltante = True`
ACTION IF FALSE: Sets `posible_licencia_faltante = False`
ERROR: N/A
FIELDS INVOLVED: `menciona_licencia`, `usa_datasets_conocidos`
CALLS: No sub-calls; pure boolean logic
SOURCE: regex_detection_skills.py:557

### 5.5 Return Structures

See section 5.3 above for each skill's return dict structure.

---

## 6. SOTA Comparison Skills (`sota_skills.py`)

### 6.1 Class Hierarchy

```
BaseSkill (ABC)
├── ThematicCoverageSkill
├── QueryGenerationSkill
├── SemanticScholarSearchSkill
├── CoverageGapAnalysisSkill
└── CrossValidationSkill
```

`SOURCE: sota_skills.py:16`

### 6.2 Method-by-Method Decomposition

#### `ThematicCoverageSkill.execute` (`SOURCE: sota_skills.py:24`)

**Input context keys required:** `['paper_text']`

**Guard checks:** `validate_context`, `llm_client` present

**Execution:**
- Reads `context['paper_text']`
- Builds inline prompt (exact template `SOURCE: sota_skills.py:45-70`):
  ```
  Analiza este manuscrito científico e identifica:
  1. Los 3-5 subtemas principales que aborda
  2. Las áreas técnicas específicas que cubre
  3. El año de publicación o envío (busca en: encabezado, pie de página, sección de metadata, fecha de envío/aceptación, copyright)
  
  IMPORTANTE para el año:
  - Busca patrones como "2024", "Published: 2023", "Submitted: 2022", "Copyright © 2024"
  - Si encuentras múltiples fechas (envío, revisión, aceptación), usa la más reciente
  - Si no encuentras ninguna fecha clara, devuelve null
  - NO inventes el año, debe estar explícitamente en el texto
  
  Devuelve EXCLUSIVAMENTE un JSON:
  {
      "subtemas": ["subtema 1", "subtema 2", ...],
      "areas_tecnicas": ["área 1", "área 2", ...],
      "año_paper": 2024
  }
  
  TEXTO (primeras páginas y últimas páginas donde suelen estar las fechas):
  INICIO:
  {paper_text[:15000]}
  
  FINAL:
  {paper_text[-5000:]}
  ```
- Calls `self.llm_client.generate(prompt)` → `response.text` → `json.loads` → `thematic_data`
- Checks `thematic_data.get("año_paper")` — logs year if found, warning if absent

**Return on success:** `{'thematic_data': {'subtemas': list, 'areas_tecnicas': list, 'año_paper': int|null}}`

**Return on exception:** `{'thematic_data': {"subtemas": [], "areas_tecnicas": [], "año_paper": None}}`

---

#### `QueryGenerationSkill.execute` (`SOURCE: sota_skills.py:97`)

**Input context keys required:** `['paper_text', 'thematic_data']`

**Execution:**
- Reads `context['paper_text'][:8000]` (first 8000 chars only)
- Reads `context['thematic_data']`
- Joins `subtemas` as `subtemas_str` and `areas_tecnicas` as `areas_str`
- Builds inline prompt (exact template `SOURCE: sota_skills.py:122-142`):
  ```
  Actúa como un investigador senior en Ciencias de la Computación.
  Analiza el siguiente manuscrito científico.
  
  SUBTEMAS IDENTIFICADOS: {subtemas_str}
  ÁREAS TÉCNICAS: {areas_str}
  
  Genera 3 búsquedas especializadas EN INGLÉS para encontrar SOTA reciente:
  - 2 queries generales sobre el tema principal (amplias)
  - 1 query específica sobre el subtema más relevante
  
  IMPORTANTE: Usa términos amplios y comunes, evita ser demasiado específico.
  
  Devuelve EXCLUSIVAMENTE un JSON:
  {
      "queries": ["query 1", "query 2", "query 3"]
  }
  
  TEXTO DEL MANUSCRITO:
  {paper_text[:8000]}
  ```
- Calls `self.llm_client.generate(prompt)` → `json.loads(response.text).get("queries", [])` → `queries`

**Return on success:** `{'search_queries': ['query 1', 'query 2', 'query 3']}`

**Return on exception:** `{'search_queries': []}`

---

#### `SemanticScholarSearchSkill.execute` (`SOURCE: sota_skills.py:162`)

**Input context keys required:** `['search_queries']`

**Guard checks:**
- `validate_context`
- `if not queries` (empty list): returns `{'sota_papers': []}`

**Execution:**
- Reads `SEMANTIC_SCHOLAR_API_KEY` from config — if set, adds header `"x-api-key": SEMANTIC_SCHOLAR_API_KEY`
- Iterates queries with index `i`; sleeps `0.5` seconds between queries (not before first)
- Per query: calls `requests.get(SEMANTIC_SCHOLAR_BASE_URL, params={'query': q, 'year': SEMANTIC_SCHOLAR_YEAR_RANGE, 'limit': SEMANTIC_SCHOLAR_LIMIT, 'fields': SEMANTIC_SCHOLAR_FIELDS}, headers=headers, timeout=15)`
- On HTTP 200: extends `sota_papers` with `response.json().get("data", [])`; logs count; logs warning if count == 0
- On HTTP 429: logs rate limit warning, sleeps 2 seconds
- On other status: logs warning with status code
- On exception: logs error and continues to next query
- Post-loop deduplication: `{p['paperId']: p for p in sota_papers if p.get('paperId')}.values()`
- Sorts by `citationCount` descending, takes top 10: `sorted_papers[:10]`

**Return:** `{'sota_papers': list}` (max 10 items, deduplicated, sorted by citations descending)

---

#### `CoverageGapAnalysisSkill.execute` (`SOURCE: sota_skills.py:246`)

**Input context keys required:** `['paper_text', 'thematic_data']`

**Execution:**
- Reads `paper_text[:5000]` (intro) and `paper_text[-10000:]` (references section)
- Reads `subtemas` from `thematic_data`, joins as string
- Builds inline prompt (exact template `SOURCE: sota_skills.py:269-288`):
  ```
  Analiza la cobertura bibliográfica de este manuscrito.
  
  SUBTEMAS IDENTIFICADOS: {subtemas_str}
  
  TEXTO (inicio y referencias):
  INICIO: {paper_text[:5000]}
  REFERENCIAS: {paper_text[-10000:]}
  
  Identifica qué subtemas tienen POCA o NULA cobertura bibliográfica.
  
  Devuelve JSON:
  {
      "areas_debiles": [
          {
              "subtema": "nombre del subtema",
              "diagnostico": "por qué tiene baja cobertura"
          }
      ]
  }
  ```
- Calls LLM, parses JSON response

**Return on success:** `{'coverage_gaps': {'areas_debiles': list}}`

**Return on exception:** `{'coverage_gaps': {"areas_debiles": []}}`

---

#### `CrossValidationSkill.execute` (`SOURCE: sota_skills.py:309`)

**Input context keys required:** `['paper_text', 'sota_papers', 'thematic_data']`

**Guard checks:**
- `validate_context`
- If `sota_papers` is empty: returns pre-built result with `"papers_omitidos": [], "cobertura_tematica": {"areas_debiles": []}, "conclusion_sota": "No se encontraron artículos recientes (2023-2026) en Semantic Scholar."`
- `if not self.llm_client`

**Execution:**
- Reads `sota_papers`, `thematic_data`, `coverage_gaps = context.get('coverage_gaps', {"areas_debiles": []})`
- Logs first 3 papers for debugging (title, year, citationCount)
- Builds `sota_context` string: for each paper `[i]`: `f"[{i+1}] Título: {p['title']}\nAño: {p['year']}\nCitas: {p['citationCount']}\nURL: {p.get('url', 'N/A')}\nAbstract: {(p.get('abstract') or 'No abstract')[:400]}"`
- Reads `paper_text[:5000]` (intro) and `paper_text[-15000:]` (references)
- Builds inline prompt (exact template `SOURCE: sota_skills.py:357-396`):
  ```
  Actúa como Revisor Editorial Experto.
  
  MANUSCRITO ORIGINAL:
  INICIO: {paper_text[:5000]}
  REFERENCIAS: {paper_text[-15000:]}
  
  SUBTEMAS DEL MANUSCRITO: {subtemas_str}
  
  PAPERS SOTA CANDIDATOS (2023-2026):
  {sota_context}
  
  TAREA:
  Identifica papers OMITIDOS (no citados) que sean RELEVANTES para el manuscrito.
  
  CRITERIOS:
  - Descartar si el título es similar al manuscrito (es el propio paper)
  - Descartar si ya está citado en referencias
  - Incluir si aporta valor al tema tratado
  - Justificar por qué debería citarse
  - Indicar qué subtema fortalece
  
  IMPORTANTE: Si encuentras papers relevantes, inclúyelos. No seas demasiado restrictivo.
  Selecciona hasta 5 papers omitidos más relevantes, ordenados por importancia.
  
  Devuelve JSON:
  {
      "papers_omitidos": [
          {
              "titulo": "título exacto",
              "año": 2024,
              "citas": 150,
              "url": "url",
              "relevancia": "Alta/Media",
              "subtema_relacionado": "subtema que fortalece",
              "justificacion": "Por qué es crucial citarlo y dónde encajaría (sección específica)"
          }
      ],
      "conclusion_sota": "Evaluación de la frescura bibliográfica y cobertura actual"
  }
  ```
- Calls LLM, parses JSON
- Adds `validation_results["cobertura_tematica"] = coverage_gaps`
- Adds `validation_results["papers_analizados"]` = list of first 10 `sota_papers` as `{'titulo', 'año', 'citas', 'url', 'autores'}`

**Return on success:**
```python
{'validation_results': {'papers_omitidos': list, 'conclusion_sota': str, 'cobertura_tematica': dict, 'papers_analizados': list}}
```

**Return on exception:** `{'validation_results': {"error": str(e)}}`

### 6.3 Comparison Logic

- Source of SOTA candidates: Semantic Scholar API (`SEMANTIC_SCHOLAR_BASE_URL`) filtered by `SEMANTIC_SCHOLAR_YEAR_RANGE` (CROSS-REFERENCE: `backend.common.config`)
- Candidate ranking: by `citationCount` descending, top 10
- Omission check: delegated to LLM with criteria in prompt (not deterministic regex)
- Maximum omitted papers reported: 5 (prompt instruction)
- Relevance labels: `"Alta"` or `"Media"` (prompt schema)

### 6.4 Business Rules

RULE: SOTA_EMPTY_RESULT
TRIGGER: `SemanticScholarSearchSkill.execute` when no queries or `CrossValidationSkill.execute` when `sota_papers` is empty
CONDITION: `not sota_papers` or `not queries`
ACTION IF TRUE: Return fixed result with `"No se encontraron artículos recientes (2023-2026)"` conclusion; skip LLM call
ACTION IF FALSE: Proceed with LLM cross-validation
ERROR: N/A
FIELDS INVOLVED: `sota_papers`, `queries`
CALLS: No sub-calls
SOURCE: sota_skills.py:178, sota_skills.py:323

### 6.5 LLM Prompt Templates (exact strings)

Documented inline in section 6.2 above.

### 6.6 Error Handling

| Skill | Exception | Recovery | Return |
|---|---|---|---|
| `ThematicCoverageSkill` | `Exception` | Log error | `{'thematic_data': {"subtemas": [], "areas_tecnicas": [], "año_paper": None}}` |
| `QueryGenerationSkill` | `Exception` | Log error | `{'search_queries': []}` |
| `SemanticScholarSearchSkill` | HTTP 429 | `time.sleep(2)`, continue | skip query |
| `SemanticScholarSearchSkill` | other HTTP error | Log warning, continue | skip query |
| `SemanticScholarSearchSkill` | `Exception` | Log error, continue | skip query |
| `CoverageGapAnalysisSkill` | `Exception` | Log error | `{'coverage_gaps': {"areas_debiles": []}}` |
| `CrossValidationSkill` | `Exception` | Log error | `{'validation_results': {"error": str(e)}}` |

### 6.7 Return Structures

Documented inline in section 6.2 above.

---

## 7. Chatbot Skills (`chatbot_skills.py`)

### 7.1 Class Hierarchy

```
BaseSkill (ABC)
├── ConversationalResponseSkill
└── ContextValidationSkill
```

`SOURCE: chatbot_skills.py:6`

### 7.2 Method-by-Method Decomposition

#### `ConversationalResponseSkill.execute` (`SOURCE: chatbot_skills.py:14`)

**Input context keys required:** `['paper_text', 'question']`

**Guard checks:**
- `validate_context(context, ['paper_text', 'question'])` → if fails, returns `{'response': '❌ Error: Faltan datos para generar respuesta'}`
- `if not self.llm_client` → returns `{'response': '❌ Error: Cliente LLM no disponible'}`

**Execution:**
- Reads `context['paper_text']` (FULL text — no truncation applied here)
- Reads `context['question']`
- Reads `context.get('history_text', 'Sin historial previo.')` → `history_text`
- Builds inline prompt (exact template `SOURCE: chatbot_skills.py:38-57`):
  ```
  You are a Senior Area Chair for NeurIPS 2024 who just audited this paper.
  The author has a question about your review or the paper content.
  
  YOUR STRICT RULES:
  1. Answer professionally, clearly, and based ONLY on the provided text.
  2. If asked about something NOT in the paper, say so directly. Don't invent.
  3. If asked to justify a finding, cite relevant sections from the text.
  4. Focus on reproducibility, code, data, and computational experimentation aspects.
  5. Reference NeurIPS 2024 criteria when relevant (Claims Audit, Limitations, Theoretical Rigor, Reproducibility, Peer Review).
  
  PAPER CONTENT:
  {paper_text}
  
  CONVERSATION HISTORY:
  {history_text}
  
  USER QUESTION:
  {question}
  ```
- Calls `self.llm_client.generate(prompt)` → returns `response.text` directly (no JSON parsing)

**Return on success:** `{'response': response.text}` (raw LLM text)

**Return on exception:** `{'response': f"❌ Hubo un error de conexión con el revisor: {str(e)}"}`

---

#### `ContextValidationSkill.execute` (`SOURCE: chatbot_skills.py:76`)

**Input context keys required:** `['paper_text', 'question']`

**Guard checks:**
- `validate_context` → if fails, returns `{'is_valid': False, 'error': 'Faltan datos requeridos (paper_text o question)'}`

**Validations:**
- `if not paper_text.strip()`: returns `{'is_valid': False, 'error': 'El texto del paper está vacío'}`
- `if not question.strip()`: returns `{'is_valid': False, 'error': 'La pregunta está vacía'}`

**Success path:**
- Strips all three inputs: `paper_text`, `question`, `history_text`
- Sets `history_text = 'Sin historial previo.'` if original value was falsy

**Return on success:**
```python
{
  'is_valid': True,
  'paper_text': str,         # stripped
  'question': str,           # stripped
  'history_text': str,       # stripped or 'Sin historial previo.'
  'paper_length': int,       # len(paper_text)
  'question_length': int     # len(question)
}
```

### 7.3 Conversation State Management

No persistent state — both skills are stateless. `history_text` is passed as a pre-formatted string in the `context` dict from the caller; neither skill stores or updates conversation history internally.

### 7.4 Business Rules

RULE: CHATBOT_GROUNDING
TRIGGER: `ConversationalResponseSkill.execute` — injected as prompt instruction
CONDITION: LLM's knowledge of paper is limited to `paper_text` provided in context
ACTION IF TRUE: LLM instructed to cite relevant text sections
ACTION IF FALSE (question not in paper): LLM instructed to say so directly; no invention
ERROR: N/A
FIELDS INVOLVED: `paper_text`, `question`, `history_text`
CALLS: Pure LLM prompt instruction — not enforced deterministically
SOURCE: chatbot_skills.py:38

### 7.5 LLM Prompt Templates (exact strings)

See section 7.2.

### 7.6 Error Handling

| Skill | Exception | Recovery | Return |
|---|---|---|---|
| `ConversationalResponseSkill` | `Exception` (broad) | Log error | `{'response': '❌ Hubo un error de conexión con el revisor: {str(e)}'}` |
| `ContextValidationSkill` | No exception handling | Validations are pure string checks with early returns | N/A |

### 7.7 Return Structures

See section 7.2.

---

## 8. Constants, Enums, and Lookup Tables

| Constant | Value | Location |
|---|---|---|
| `NEGATION_WINDOW` | `60` (int) | `SOURCE: regex_detection_skills.py:8` — chars before match to inspect for negation |
| `NEGATION_PATTERNS` | Compiled `re.Pattern` with `re.IGNORECASE` — see section 5.2 for full pattern string | `SOURCE: regex_detection_skills.py:10` |
| `HyperparameterDetectionSkill.PATTERNS` | Dict of 8 keys each mapping to list of regex strings — see section 5.2 | `SOURCE: regex_detection_skills.py:89` |
| `DataAvailabilityDetectionSkill.PATTERNS` | Dict of 4 keys | `SOURCE: regex_detection_skills.py:191` |
| `CodeAvailabilityDetectionSkill.PATTERNS` | Dict of 4 keys | `SOURCE: regex_detection_skills.py:237` |
| `StatisticsDetectionSkill.PATTERNS` | Dict of 3 keys | `SOURCE: regex_detection_skills.py:290` |
| `EnvironmentalImpactDetectionSkill.PATTERNS` | Dict of 3 keys | `SOURCE: regex_detection_skills.py:357` |
| `ProblematicPhrasesDetectionSkill.PATTERNS` | Dict of 3 keys | `SOURCE: regex_detection_skills.py:422` |
| `LlmUsageDetectionSkill.PATTERNS` | Dict of 1 key | `SOURCE: regex_detection_skills.py:457` |
| `CrowdsourcingDetectionSkill.CROWDSOURCING_ACTIVE` | List of 4 patterns | `SOURCE: regex_detection_skills.py:483` |
| `CrowdsourcingDetectionSkill.HUMAN_DATASET_USE` | List of 2 patterns | `SOURCE: regex_detection_skills.py:490` |
| `CrowdsourcingDetectionSkill.COMPENSATION` | Single pattern string | `SOURCE: regex_detection_skills.py:494` |
| `CrowdsourcingDetectionSkill.NEGATION_CROWD` | Single pattern string | `SOURCE: regex_detection_skills.py:496` |
| `LicenseDetectionSkill.EXPLICIT_LICENSE` | Single pattern string | `SOURCE: regex_detection_skills.py:531` |
| `LicenseDetectionSkill.KNOWN_DATASETS` | Single pattern string (20 dataset names) | `SOURCE: regex_detection_skills.py:533` |
| `LimitationsQualityDetectionSkill.SPECIFIC_PATTERNS` | List of 3 patterns | `SOURCE: regex_detection_skills.py:564` |
| `LimitationsQualityDetectionSkill.SECTION_PATTERN` | Single pattern string | `SOURCE: regex_detection_skills.py:569` |
| `SoftwareVersionDetectionSkill.PATTERNS` | List of 4 patterns | `SOURCE: regex_detection_skills.py:595` |
| `HardwareDetailDetectionSkill.PATTERNS` | Dict of 4 keys, each list of 2 patterns | `SOURCE: regex_detection_skills.py:625` |
| `ChecklistVerificationSkill.priority_items` | `['claims', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiments_compute_resource', 'experiment_statistical_significance', 'licenses', 'declaration_llm_usage']` | `SOURCE: auditor_skills.py:340` |
| RAG batch_size | `15` (int) | `SOURCE: rag_extraction_skill.py:61` |
| RAG inter-batch sleep | `15` (seconds) | `SOURCE: rag_extraction_skill.py:67` |
| RAG inter-chunk sleep | `1` (second, MAP phase) | `SOURCE: rag_extraction_skill.py:199` |
| RAG n_results per query | `10` | `SOURCE: rag_extraction_skill.py:123` |
| RAG query count | `13` | `SOURCE: rag_extraction_skill.py:99` |
| RAG relevance thresholds | `distance < 0.4`, `0.4–0.7`, `≥0.7` | `SOURCE: rag_extraction_skill.py:152` |
| Semantic Scholar rate-limit sleep | `2` (seconds, on HTTP 429) | `SOURCE: sota_skills.py:217` |
| Semantic Scholar inter-query sleep | `0.5` (seconds) | `SOURCE: sota_skills.py:191` |
| Semantic Scholar timeout | `15` (seconds) | `SOURCE: sota_skills.py:207` |
| Semantic Scholar top-N results | `10` | `SOURCE: sota_skills.py:232` |
| CrossValidation max papers to report | `5` (prompt instruction) | `SOURCE: sota_skills.py:379` |
| MAP fragment sleep | `2` (seconds, between fragments) | `SOURCE: auditor_skills.py:104` |

---

## 9. API / Service Contracts

### `BaseSkill.execute` (abstract)
- **Signature:** `execute(self, context: Dict[str, Any]) -> Dict[str, Any]`
- **Parameters:** `context` — dict with arbitrary string keys; required keys vary per subclass
- **Returns:** dict with arbitrary string keys (results); empty dict or partial dict on failure
- **Exceptions:** No declared exceptions; subclasses typically catch all and return error keys
- `SOURCE: base_skill.py:34`

### `BaseSkill.validate_context`
- **Signature:** `validate_context(self, context: Dict[str, Any], required_keys: list) -> bool`
- **Returns:** `True` if all keys present, `False` otherwise
- `SOURCE: base_skill.py:47`

### `BaseSkill.log_execution`
- **Signature:** `log_execution(self, message: str, level: str = "info") -> None`
- **Parameters:** `level` ∈ `{"info", "warning", "error", "debug"}` (default `"info"`)
- `SOURCE: base_skill.py:64`

### `CompositeSkill.execute`
- **Signature:** `execute(self, context: Dict[str, Any]) -> Dict[str, Any]`
- **Returns:** merged context dict; adds `"error_{skill_name}"` key on per-skill failure
- `SOURCE: base_skill.py:103`

### `HybridHyperparameterExtractionSkill._clean_with_regex`
- **Signature:** `_clean_with_regex(self, data: Dict[str, str]) -> Dict[str, Any]`
- **Returns:** dict with same keys; values converted to `float`, `int`, or `str`; `"NOT FOUND"` for missing values
- `SOURCE: rag_extraction_skill.py:277`

### `TableExtractionHelper.extract_tables` (static)
- **Signature:** `extract_tables(text: str) -> List[str]`
- `SOURCE: regex_detection_skills.py:42`

### `TableExtractionHelper.extract_table_rows` (static)
- **Signature:** `extract_table_rows(table_text: str) -> List[str]`
- **Returns:** list of non-empty, non-separator lines
- `SOURCE: regex_detection_skills.py:72`

### `_is_negated` (module function)
- **Signature:** `_is_negated(text: str, match_start: int) -> bool`
- `SOURCE: regex_detection_skills.py:21`

### `_search_with_negation` (module function)
- **Signature:** `_search_with_negation(pattern: str, text: str, flags: int = re.IGNORECASE) -> Optional[re.Match]`
- **Returns:** first `re.Match` not in negation context, or `None`
- `SOURCE: regex_detection_skills.py:28`

---

## 10. Transformations

| Transformation | Source Field | Target Field | Logic | Source |
|---|---|---|---|---|
| Paper segmentation by sections | `paper_text` (string) | `fragments` (list of strings) | Split on `\n(?=#+ )` (Docling headers); group into ≤4 balanced chunks by `total_chars / 4` target | `auditor_skills.py:40` |
| Paper fallback segmentation | `paper_text` (string) | `fragments` (list, max 4) | `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000).split_text(paper_text)[:4]` | `auditor_skills.py:72` |
| JSON fence stripping | `raw_text` (string with ```json...``` wrapper) | `raw_text` (clean JSON string) | `re.sub(r'^```(?:json)?\n?\|```$', '', raw_text, flags=re.MULTILINE).strip()` | `auditor_skills.py:217` |
| Balanced JSON extraction | `raw_text` (string containing JSON + surrounding text) | `raw_text` (first complete JSON object) | Find first `{`, walk char-by-char counting braces (stack), stop when stack == 0 | `auditor_skills.py:89` |
| JSON trailing-comma repair | `raw_text` (malformed JSON) | `fixed_text` (valid JSON) | `re.sub(r',\s*([\]}])', r'\1', raw_text)` | `auditor_skills.py:148` |
| Scientific notation → float | `str_val` (e.g., `"3 x 10^-4"`) | `float` | `base * (10 ** exp)` with regex capture groups; formatted to 8 decimal places | `rag_extraction_skill.py:289` |
| RAG distance → relevance score | `distance` (float, ChromaDB L2) | `relevance_score` (int 5-95) | Piecewise linear — see section 4.5 | `rag_extraction_skill.py:152` |
| chunk text → embedding | raw paragraph text | `[float, ...]` vector | `httpx.POST` to Google Generative Language `batchEmbedContents` endpoint | `rag_extraction_skill.py:74` |
| paper_type validity check | `extracted_info['paper_type']` (string) | `invalid_paper` (bool) | `paper_type.startswith('INVALID')` | `auditor_skills.py:152` |
| MetadataAggregation flatten | `context` (nested dict) | flat result dict | Direct `.get()` of 23 fields from `evaluation` and `context` sub-dicts | `auditor_skills.py:285` |
| context_mapping reconstruction | `map_results` list | `extracted_info['context_mapping']` (list of strings) | Collect all `context_mapping` lists from MAP results, `set()` deduplication, fallback `["General Context"]` | `auditor_skills.py:165` |

---

## 11. Error Handling Catalog

| ID | Skill / Location | Exception Type | Condition / Trigger | Recovery Action | Return / Impact |
|---|---|---|---|---|---|
| EH-01 | `InformationExtractionSkill` MAP fragment | `Exception` (broad) | Any per-fragment LLM or JSON error | Log warning with fragment index and error string; continue loop | Fragment skipped; other fragments still processed |
| EH-02 | `InformationExtractionSkill` MAP empty | implicit (empty list check) | `not map_results` | Log error | `{'extracted_info': {}, 'extraction_error': "Map phase produced no results"}` |
| EH-03 | `InformationExtractionSkill` REDUCE primary | `Exception` (broad) | `llm_client.generate` failure | Fallback to `llm_client.client.models.generate_content` with `response_mime_type: "application/json"`, `temperature: 0.0` | Continue with fallback response |
| EH-04 | `InformationExtractionSkill` REDUCE JSON | `json.JSONDecodeError` | Invalid JSON from LLM | `re.sub(r',\s*([\]}])', r'\1', raw_text)` then retry `json.loads` | Raises if repair fails; caught by EH-05 |
| EH-05 | `InformationExtractionSkill` outer | `Exception` (broad) | Any uncaught exception | Log error | `{'extracted_info': {}, 'extraction_error': str(e)}` |
| EH-06 | `ReproducibilityEvaluationSkill` JSON | `json.JSONDecodeError` | Invalid evaluation JSON | Trailing-comma repair + retry; on persistent failure: return error dict | `{'evaluation': {}, 'evaluation_error': 'JSON parse error: ...'}` |
| EH-07 | `ReproducibilityEvaluationSkill` 503/overload | `Exception` where `'503'` or `'UNAVAILABLE'` in message | LLM service overload | Return user-facing message | `{'evaluation': {}, 'evaluation_error': 'El modelo LLM está experimentando alta demanda...'}` |
| EH-08 | `ReproducibilityEvaluationSkill` outer | `Exception` (broad) | General error | Log error | `{'evaluation': {}, 'evaluation_error': error_msg}` |
| EH-09 | `ChecklistVerificationSkill` per-item | `Exception` (broad) | Error verifying individual checklist item | Log warning; continue to next item | Item left unchanged in evaluation dict |
| EH-10 | `HybridHyperparameterExtractionSkill` embedding API | `httpx.post` non-200 response | HTTP error from Google Generative Language API | Raises `Exception(f"Error embeddings API: {response.text}")` | Propagates to EH-12 |
| EH-11 | `HybridHyperparameterExtractionSkill` ChromaDB delete | Any | Collection doesn't exist | `except: pass` — silently ignored | Normal execution continues |
| EH-12 | `HybridHyperparameterExtractionSkill` per-chunk MAP | `Exception` (broad) | Per-chunk LLM or JSON error | Log warning, continue to next chunk | Chunk skipped |
| EH-13 | `HybridHyperparameterExtractionSkill` REDUCE primary | `Exception` (broad) | REDUCE LLM failure | Fallback to `models.generate_content` with `Hyperparameters` Pydantic schema | Continue with fallback |
| EH-14 | `HybridHyperparameterExtractionSkill` REDUCE JSON | `json.JSONDecodeError` | Invalid REDUCE JSON | Trailing-comma repair + retry | Raises if repair fails; caught by EH-15 |
| EH-15 | `HybridHyperparameterExtractionSkill` outer | `Exception` (broad) | Any uncaught exception | Log error | `{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str(e)}` |
| EH-16 | `SemanticScholarSearchSkill` HTTP 429 | No exception — status code check | Rate limit exceeded | `time.sleep(2)`; continue to next query | Current query skipped |
| EH-17 | `SemanticScholarSearchSkill` other HTTP error | No exception — status code check | Any non-200, non-429 status | Log warning; continue | Query skipped |
| EH-18 | `SemanticScholarSearchSkill` per-query | `Exception` (broad) | Network/parsing error | Log error; continue | Query skipped |
| EH-19 | `ThematicCoverageSkill` outer | `Exception` (broad) | Any error | Log error | `{'thematic_data': {"subtemas": [], "areas_tecnicas": [], "año_paper": None}}` |
| EH-20 | `QueryGenerationSkill` outer | `Exception` (broad) | Any error | Log error | `{'search_queries': []}` |
| EH-21 | `CoverageGapAnalysisSkill` outer | `Exception` (broad) | Any error | Log error | `{'coverage_gaps': {"areas_debiles": []}}` |
| EH-22 | `CrossValidationSkill` outer | `Exception` (broad) | Any error | Log error | `{'validation_results': {"error": str(e)}}` |
| EH-23 | `ConversationalResponseSkill` outer | `Exception` (broad) | Any LLM error | Log error | `{'response': '❌ Hubo un error de conexión con el revisor: {str(e)}'}` |
| EH-24 | `CompositeSkill.execute` per-skill | `Exception` (broad) | Any sub-skill error | Log error; set `accumulated_context["error_{skill_name}"] = str(e)`; continue | Other skills still run |

---

## 12. Cross-References and Gaps

GAP_ID: GAP-cluster_backend_skills_01-001
TYPE: CROSS_REFERENCE
FROM: auditor_skills.py:7 — `InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `ChecklistVerificationSkill`
EXPECTS: Functions `get_extraction_prompt`, `get_evaluation_prompt`, `get_verification_prompt`, `get_map_extraction_prompt`, `get_reduce_extraction_prompt`, `get_evaluation_signals` — exact prompt template strings and parameter schemas
LIKELY_LOCATION: `backend/common/prompts.py`
IMPACT: HIGH — these functions contain all LLM prompt templates used by the core auditor pipeline; without them the exact prompts are unknown
SOURCE: auditor_skills.py:6

GAP_ID: GAP-cluster_backend_skills_01-002
TYPE: CROSS_REFERENCE
FROM: auditor_skills.py:6 — `InformationExtractionSkill.execute` REDUCE phase
EXPECTS: Value of `REDUCE_MODEL_NAME` constant (model identifier string)
LIKELY_LOCATION: `backend/common/config.py`
IMPACT: HIGH — determines which LLM model runs REDUCE consolidation
SOURCE: auditor_skills.py:114

GAP_ID: GAP-cluster_backend_skills_01-003
TYPE: CROSS_REFERENCE
FROM: rag_extraction_skill.py:9 — `HybridHyperparameterExtractionSkill.execute`
EXPECTS: Values of `MAP_MODEL_NAME`, `REDUCE_MODEL_NAME`, `EMBEDDING_MODEL_NAME`, `EVALUATION_MODEL_NAME` constants
LIKELY_LOCATION: `backend/common/config.py`
IMPACT: HIGH — these four model identifiers determine which Google models are used at each pipeline phase
SOURCE: rag_extraction_skill.py:9

GAP_ID: GAP-cluster_backend_skills_01-004
TYPE: CROSS_REFERENCE
FROM: sota_skills.py:7 — `SemanticScholarSearchSkill.execute`
EXPECTS: Values of `SEMANTIC_SCHOLAR_API_KEY` (string or None), `SEMANTIC_SCHOLAR_BASE_URL` (URL string), `SEMANTIC_SCHOLAR_YEAR_RANGE` (string e.g. `"2023-2026"`), `SEMANTIC_SCHOLAR_LIMIT` (int), `SEMANTIC_SCHOLAR_FIELDS` (comma-separated field names string)
LIKELY_LOCATION: `backend/common/config.py`
IMPACT: HIGH — these 5 constants fully define the Semantic Scholar API search behaviour
SOURCE: sota_skills.py:7

GAP_ID: GAP-cluster_backend_skills_01-005
TYPE: CROSS_REFERENCE
FROM: base_skill.py:4 — all skills via inheritance
EXPECTS: `LLMClient` class interface — specifically the `.generate(prompt) -> response` method signature, `.client.models.generate_content(...)` interface, `.client.models.embed_content(model, contents)` interface, and how `response.text` is structured
LIKELY_LOCATION: `backend/common/llm_client.py`
IMPACT: HIGH — all LLM calls in every skill depend on this interface
SOURCE: base_skill.py:4

GAP_ID: GAP-cluster_backend_skills_01-006
TYPE: CROSS_REFERENCE
FROM: base_skill.py:5 — all skills via `log_execution`
EXPECTS: `get_logger` function signature and logger configuration
LIKELY_LOCATION: `backend/utils/logger.py`
IMPACT: LOW — logging infrastructure; does not affect business logic
SOURCE: base_skill.py:5

GAP_ID: GAP-cluster_backend_skills_01-007
TYPE: MISSING_SOURCE
FROM: __init__.py:36 — package `__all__`
EXPECTS: `ChecklistVerificationSkill` is defined in `auditor_skills.py:319` but not listed in `__init__.py.__all__` and not imported; similarly `HybridHyperparameterExtractionSkill` is defined in `rag_extraction_skill.py:27` but not in `__init__.py`
LIKELY_LOCATION: These symbols exist but are intentionally or accidentally excluded from the public API
IMPACT: MEDIUM — callers importing from `backend.skills` cannot access these two skills by default
SOURCE: __init__.py:36

GAP_ID: GAP-cluster_backend_skills_01-008
TYPE: CROSS_REFERENCE
FROM: rag_extraction_skill.py:63 — `HybridHyperparameterExtractionSkill.execute`
EXPECTS: `GOOGLE_API_KEY` env var — read via `os.getenv("GOOGLE_API_KEY")`; must be set at runtime for embedding API calls
LIKELY_LOCATION: environment / `config/.env`
IMPACT: HIGH — without this key, all `httpx.post` embedding calls fail with non-200 response and the RAG skill raises an exception
SOURCE: rag_extraction_skill.py:63
