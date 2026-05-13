# 02 — Functional Backend Specification
## NeurIPS Paper Auditor — Backend System

> **Purpose**: This document is the authoritative functional specification for the backend of the
> NeurIPS Paper Auditor system. A developer must be able to rewrite the entire backend in another
> technology using ONLY this document, without reference to the original source code.
>
> **Fidelity**: Every element below is traceable to extraction data.
> Elements not found in the source code are marked `[GAP: ...]`.
> No content has been invented or assumed.

---

## Table of Contents

1. [Audit Pipeline Overview (6 Phases)](#section-1)
2. [FASE 1: Information Extraction Skill (MAP/REDUCE)](#section-2)
3. [FASE 1.5: Hybrid Hyperparameter Extraction](#section-3)
4. [FASE 2: Reproducibility Evaluation Skill](#section-4)
5. [FASE 2.5: Checklist Verification Skill](#section-5)
6. [FASE 3: Metrics Calculation Skill](#section-6)
7. [FASE 4: Metadata Aggregation Skill](#section-7)
8. [CompositeSkill Orchestration](#section-8)
9. [BaseSkill Interface and Lifecycle](#section-9)
10. [Regex Detection Skills (9 non-exported skills)](#section-10)
11. [All 15 Exported Skills](#section-11)
12. [SOTA Analysis Pipeline (5 Steps)](#section-12)
13. [Chatbot (preguntar Flow + History)](#section-13)
14. [PDF Parser (Docling Chunked Flow)](#section-14)
15. [LLMClient (Retry + Backoff Logic)](#section-15)
16. [Prompt Template Functions (all 6)](#section-16)

---

<a name="section-1"></a>
## Section 1 — Audit Pipeline Overview (6 Phases)

Source: `extracted_backend_core_01.md §4.2`, `extracted_backend_skills_01.md §3.2`,
`cross_ref_resolution_cross_ref_root_to_backend.md §RESOLUTION SUMMARY`

### 1.1 Phase Summary Table

| Phase | ID | Skill(s) Invoked | Trigger Condition | Input Context Keys | Output Context Keys | Error Handling | Side Effects |
|---|---|---|---|---|---|---|---|
| 1 | `information_extraction` | `InformationExtractionSkill` | Always runs; first phase | `paper_text` (str), `red_flags` (dict, always `{}` — initialized internally by `audit()` at `auditor.py:84`) | `extracted_info` (dict) | On failure (when `'extraction_error' in extraction_result`): returns `{"error": extraction_result['extraction_error']}`; no `success` or `phase` key; pipeline aborts (`auditor.py:90-96`) | Sleeps 2s between each fragment LLM call |
| 1.5 | `hyperparameter_extraction` | `HybridHyperparameterExtractionSkill` | Always runs after Phase 1 | `paper_text` (str), `extracted_info` (dict) | `extracted_hyperparameters_hybrid` (dict) | Non-critical: on failure, pipeline continues (context key may be absent or partial); logs error | Builds and destroys in-memory ChromaDB collection; sleeps 1s between chunks; sleeps 15s between embedding batches |
| 2 | `reproducibility_evaluation` | `ReproducibilityEvaluationSkill` | Always runs after Phase 1.5 | `extracted_info` (dict), `red_flags` (dict, always `{}` — internal; `auditor.py:84`) | `checklist` (dict) | On failure: returns `{"error": str(e)}`; no `success` or `phase` key; pipeline aborts via outer `except Exception` (`auditor.py:201-204`) | None |
| 2.5 | `checklist_verification` | `ChecklistVerificationSkill` | Always runs after Phase 2 | `paper_text` (str), `evaluation` (dict from Phase 2) | `evaluation` (dict, updated in-place with verification results) | No exception isolation: `verification_skill.execute()` is called with no surrounding try/except; any raised exception propagates to the outer `audit()` handler; `context['error_log']` is never written | Truncates `paper_text` to `[:30000] + [-30000:]` for context window |
| 3 | `metrics_calculation` | `MetricsCalculationSkill` | Always runs after Phase 2.5 | `paper_text` (str, guard check), `execution_time` (float, pre-computed delta passed by orchestrator in `metrics_context`), `red_flags` (dict) | `metrics` (dict) containing `tiempo_segundos` (float), `caracteres_leidos` (int), `red_flags_detectadas` (int) | Guard returns `{'metrics': {}}` when `paper_text` absent; no further error check on result; any exception propagates to outer handler | None |
| 4 | `metadata_aggregation` | `MetadataAggregationSkill` | Always runs after Phase 3 | 23 context keys (see §1.2) | `result` (dict, all 23 keys flattened) | On failure: propagates to outer `except Exception` which returns `{"error": str(e)}`; no `success` or `phase` key (`auditor.py:201-204`) | None |

### 1.2 Context Keys Read by Phase 4 (MetadataAggregationSkill)

`MetadataAggregationSkill.execute()` reads from context in two ways: it reads
`context.get('evaluation', {})` and extracts 16 named sub-keys from it, then reads
7 additional direct context keys. Absent keys default to `{}` or `[]`. The result dict is
returned directly from `execute()` (not stored under `context["result"]`).

SOURCE: `auditor_skills.py:285-317`

**From `context.get('evaluation', {})` — 16 NeurIPS checklist sub-keys:**

| Output Key in Result | `evaluation` Sub-key | Type |
|---|---|---|
| `claims` | `evaluation.get('claims', {})` | dict |
| `limitations` | `evaluation.get('limitations', {})` | dict |
| `theory_assumptions_proofs` | `evaluation.get('theory_assumptions_proofs', {})` | dict |
| `experimental_result_reproducibility` | `evaluation.get('experimental_result_reproducibility', {})` | dict |
| `open_access_data_code` | `evaluation.get('open_access_data_code', {})` | dict |
| `experimental_setting_details` | `evaluation.get('experimental_setting_details', {})` | dict |
| `experiment_statistical_significance` | `evaluation.get('experiment_statistical_significance', {})` | dict |
| `experiments_compute_resource` | `evaluation.get('experiments_compute_resource', {})` | dict |
| `code_of_ethics` | `evaluation.get('code_of_ethics', {})` | dict |
| `broader_impacts` | `evaluation.get('broader_impacts', {})` | dict |
| `safeguards` | `evaluation.get('safeguards', {})` | dict |
| `licenses` | `evaluation.get('licenses', {})` | dict |
| `assets` | `evaluation.get('assets', {})` | dict |
| `crowdsourcing_human_subjects` | `evaluation.get('crowdsourcing_human_subjects', {})` | dict |
| `irb_approvals` | `evaluation.get('irb_approvals', {})` | dict |
| `declaration_llm_usage` | `evaluation.get('declaration_llm_usage', {})` | dict |

**Direct context reads — 7 additional keys:**

| Output Key in Result | Context Key Read | Default | Type |
|---|---|---|---|
| `informacion_extraida` | `context.get('extracted_info', {})` | `{}` | dict |
| `red_flags` | `context.get('red_flags', {})` | `{}` | dict |
| `metricas` | `context.get('metrics', {})` | `{}` | dict |
| `general_analysis_map` | `context.get('general_analysis_map', [])` | `[]` | list |
| `general_analysis_reduce` | `context.get('general_analysis_reduce', {})` | `{}` | dict |
| `hybrid_triage_fragments` | `context.get('hybrid_triage_fragments', [])` | `[]` | list |
| `evaluation_signals` | `context.get('evaluation_signals', {})` | `{}` | dict |

Source: `auditor_skills.py:285-317`

### 1.3 Pipeline Control Flow (Prose)

`PaperAuditor.audit(paper_text: str, status_callback=None) -> dict` is the single entry point (`auditor.py:59`).
The pipeline is **sequential**: phases execute in order 1 → 1.5 → 2 → 2.5 → 3 → 4.
There is no branching or DAG structure.

**Context propagation**: A shared mutable `context` dict is initialized before Phase 1 and
passed to each skill's `execute(context)` call. Each skill reads from and writes to this same
dict. Phases do not receive isolated copies.

**Failure model (critical vs non-critical)**:

- Phase 1 is **critical**: on failure (detected by `'extraction_error' in extraction_result`), `audit()` returns `{"error": ...}` and the pipeline halts.
- Phase 1.5: no try/except wrapper; after calling `hybrid_hp_skill.execute()`, `audit()` checks `if 'error' in hybrid_hp_result and not hybrid_hp_result.get('extracted_hyperparameters_hybrid')` and logs a warning if true. The pipeline always continues regardless (SOURCE: `auditor.py:118-123`).
- Phase 2 is **critical**: on failure (detected by `'evaluation_error' in evaluation_result`), `audit()` returns `{"error": ...}` and the pipeline halts.
- Phase 2.5: no try/except and no result inspection; `verification_skill.execute()` is called and its result merged directly into context. Any exception propagates to the outer handler (SOURCE: `auditor.py:171-172`).
- Phases 3 and 4: no error checks on results; any exception propagates to outer handler.
- All uncaught exceptions fall to the outer `except Exception as e:` which returns `{"error": str(e)}`.

**Start/end time tracking**:

```python
start_time = time.time()
context["start_time"] = start_time
# ... phases 1, 1.5, 2, 2.5 ...
end_time = time.time()   # set here — BEFORE Phase 3 call
context["end_time"] = end_time
# ... phase 3, 4 ...
```

**Outer except behavior**:  
The outer `except Exception as e:` block at `auditor.py:201-204` assigns `end_time = time.time()` as its FIRST statement (`auditor.py:202`), then logs the error and returns `{"error": str(e)}`. There is no NameError risk: `end_time` is always bound inside the outer except block regardless of which phase raised the exception. Source: `auditor.py:201-204`.  
`[GAP: _preprocess_paper behavior unresolved — method was removed during refactoring; no source available]`

---

<a name="section-2"></a>
## Section 2 — FASE 1: Information Extraction Skill (MAP/REDUCE)

Source: `extracted_backend_skills_01.md §3.2 (InformationExtractionSkill)`,
`extracted_backend_core_01.md §4.2`

### 2.1 Class

```
InformationExtractionSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 2.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 2.3 Trigger Condition

Phase 1 always runs. `PaperAuditor.audit()` calls this skill unconditionally as the first step.

### 2.4 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full text of the paper (from PDF-to-markdown conversion) |
| `red_flags` | dict | Yes | Always empty dict `{}` — initialized internally by `PaperAuditor.audit()` at `auditor.py:84`; not a caller-supplied parameter |

### 2.5 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `extracted_info` | dict | Consolidated extraction result (REDUCE output) |
| `map_results` | list[dict] | Per-fragment MAP extraction results |
| `reduce_result` | dict | Alias / copy of `extracted_info` before post-processing |
| `fragment_count` | int | Number of fragments processed in MAP phase |
| `paper_title` | str | Title extracted from paper (from `extracted_info["title"]`) |

### 2.6 Fragment Sizing Algorithm

```pseudocode
FUNCTION split_paper(paper_text):
    total_chars = len(paper_text)
    target_size = total_chars / 4          # target 4 fragments
    
    # Step 1: Try section-header split
    raw_splits = re.split(r'\n(?=#+ )', paper_text)
    
    IF len(raw_splits) <= 1:
        # Fallback: use LangChain RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=25000,
            chunk_overlap=2000
        )
        fragments = splitter.split_text(paper_text)[:4]
        RETURN fragments
    
    # Step 2: Merge sections into at most 4 balanced fragments
    fragments = []
    current_fragment = ""
    cut_count = 0
    
    FOR section IN raw_splits:
        IF (len(current_fragment) + len(section) > target_size
                AND cut_count < 3
                AND current_fragment != ""):
            fragments.append(current_fragment)
            current_fragment = section
            cut_count += 1
        ELSE:
            current_fragment += "\n" + section
    
    IF current_fragment:
        fragments.append(current_fragment)
    
    RETURN fragments    # at most 4 elements (3 cuts max)
```

Source: `extracted_backend_core_01.md §4.2 (fragment splitting logic)`,
`extracted_backend_skills_01.md §3.2`

### 2.7 MAP Phase

For each fragment in the fragments list:

1. Call `get_map_extraction_prompt(fragment_text)` to build the prompt.
2. Call `LLMClient.generate(prompt, config=AUDIT_CONFIG)` (model: `gemini-3.1-flash-lite-preview`).
3. Apply **Balanced JSON Extraction** (see §2.8) to parse the LLM response.
4. Append the parsed dict to `map_results`.
5. **Sleep 2 seconds** before processing the next fragment.

On error for a single fragment: the error is logged to `context["error_log"]` and the fragment
is skipped (MAP continues with remaining fragments).

### 2.8 Balanced JSON Extraction Algorithm

Applied to every raw LLM string response to extract the first valid top-level JSON object.

```pseudocode
FUNCTION extract_balanced_json(text: str) -> dict | None:
    # Find the first '{' character
    start_idx = text.find('{')
    IF start_idx == -1:
        RETURN None
    
    stack = 0
    in_string = False
    escape_next = False
    
    FOR i FROM start_idx TO len(text)-1:
        char = text[i]
        
        IF escape_next:
            escape_next = False
            CONTINUE
        
        IF char == '\\' AND in_string:
            escape_next = True
            CONTINUE
        
        IF char == '"':
            in_string = NOT in_string
            CONTINUE
        
        IF NOT in_string:
            IF char == '{':
                stack += 1
            ELIF char == '}':
                stack -= 1
                IF stack == 0:
                    json_str = text[start_idx : i+1]
                    RETURN json.loads(json_str)   # raises on parse error
    
    RETURN None   # no balanced object found
```

Source: `extracted_backend_core_01.md §4.2 (balanced JSON extraction)`,
`extracted_backend_skills_01.md §3.2`

### 2.9 REDUCE Phase

After all MAP fragments are processed:

1. Call `get_reduce_extraction_prompt(map_results)` to build the consolidation prompt.
2. Call `LLMClient.generate(prompt, config=AUDIT_CONFIG)`.
3. Apply **Balanced JSON Extraction** to parse the REDUCE result.
4. Apply post-processing: strip markdown JSON fences (```` ```json ``` ````), strip trailing
   commas before `}` or `]` (regex repair).
5. Store result as `context["extracted_info"]` and `context["reduce_result"]`.
6. Extract `context["paper_title"] = extracted_info.get("title", "")`.

### 2.10 Deduplication Strategy

The REDUCE prompt instructs the LLM to merge duplicate entries across fragments. No
client-side deduplication logic is applied — consolidation is fully delegated to the LLM.

Source: `extracted_backend_skills_01.md §3.2`

### 2.11 Error Handling

| Condition | Behavior |
|---|---|
| All MAP fragments fail (empty `map_results`) | REDUCE still called with empty list; LLM may return empty dict |
| Balanced JSON extraction returns `None` | `extracted_info` is set to `{}` (empty dict); pipeline continues |
| REDUCE LLM call raises exception | Phase 1 fails; skill returns `{"extracted_info": {}, "extraction_error": str(e)}` (`auditor_skills.py:181`); `audit()` detects `'extraction_error' in extraction_result` and returns `{"error": extraction_result['extraction_error']}` (`auditor.py:90-96`); no `success` or `phase` key |

### 2.12 Return Shape

**Skill success return (written to context via `audit()` `context.update()`):**

```python
{
    "extracted_info": dict,       # consolidated REDUCE output (auditor_skills.py:173)
    "invalid_paper": bool,        # True if paper_type starts with 'INVALID'
    "map_steps": list[dict],      # per-fragment MAP results
    "reduce_step": dict           # alias of extracted_info pre-postprocessing
}
```

**Skill failure return (triggers pipeline abort):**

```python
{
    "extracted_info": {},
    "extraction_error": str       # exception message (auditor_skills.py:181)
}
```

**`audit()` abort return (when `'extraction_error' in extraction_result`):**

```python
{
    "error": str    # value of extraction_result['extraction_error'] (auditor.py:92-96)
}
```
Note: no `success` key, no `phase` key.

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §4.2`

---

<a name="section-3"></a>
## Section 3 — FASE 1.5: Hybrid Hyperparameter Extraction

Source: `extracted_backend_skills_01.md §4`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_014`

### 3.1 Class

```
HybridHyperparameterExtractionSkill(BaseSkill)
```

Exported: **No** (non-exported, defined in `backend/skills/rag_extraction_skill.py:27`)

### 3.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 3.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text for embedding and chunking |
| `extracted_info` | dict | Yes (optional guard) | Output of Phase 1; checked for presence |

### 3.4 Guard Conditions (Early Exit)

RULE: guard_hyperparameter_extraction  
TRIGGER: `execute()` is called  
CONDITION: `self.validate_context(context, ['paper_text'])` returns False (i.e., `paper_text` key absent or falsy)  
ACTION: Return `{'extracted_hyperparameters_hybrid': {}}`  
ERROR: Non-critical; `PaperAuditor.audit()` catches this and continues pipeline

SOURCE: `rag_extraction_skill.py:31-32`

### 3.5 Sub-Steps

#### Step 1: Chunk paper text

Paragraph-based split using Docling double-newline convention. No character-based
chunking. No fixed window size. No overlap.

```pseudocode
paper_text_norm = paper_text.replace('\r\n', '\n')
raw_chunks = re.split(r'\n\n+', paper_text_norm)          # split on 2+ blank lines
chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]   # discard near-empty
```

SOURCE: `rag_extraction_skill.py:43-47`

#### Step 2: Generate embeddings via Google API (batch)

```pseudocode
batch_size = 15
inter_batch_sleep = 15   # seconds

FOR i FROM 0 TO len(chunks) STEP batch_size:
    batch = chunks[i : i + batch_size]
    response = google_embedding_api.batchEmbedContents(
        model="gemini-embedding-2",
        content=batch
    )
    embeddings.extend(response.embeddings)
    IF more batches remain:
        sleep(15)
```

Source: `extracted_backend_skills_01.md §4 (batch embedding)`

#### Step 3: Build in-memory ChromaDB collection

```pseudocode
client = chromadb.Client()   # in-memory (no persistence)
TRY: client.delete_collection("paper_chunks")   # purge stale data from previous run
EXCEPT: PASS
collection = client.create_collection(name="paper_chunks")
collection.add(
    embeddings=embeddings,
    documents=chunks,
    ids=[str(i) for i in range(len(chunks))]
)
```

SOURCE: `rag_extraction_skill.py:85-97`

#### Step 4: Query with 13 fixed queries

The 13 fixed queries are:

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

SOURCE: `rag_extraction_skill.py:99-113`

All 13 queries are embedded simultaneously using `self.llm_client.client.models.embed_content()`.
The resulting embeddings are then sent in a single batched ChromaDB query:

```pseudocode
q_emb_res = self.llm_client.client.models.embed_content(
    model=EMBEDDING_MODEL_NAME,
    contents=queries          # all 13 at once
)
query_embeddings = [e.values for e in q_emb_res.embeddings]

results = collection.query(
    query_embeddings=query_embeddings,   # list of 13 embedding vectors
    n_results=10                          # 10 nearest chunks per query
)
```

SOURCE: `rag_extraction_skill.py:115-124`

#### Step 5: Relevance scoring (piecewise linear on ChromaDB distance)

```pseudocode
FUNCTION score_relevance(distance: float) -> float:
    # ChromaDB distance: 0.0 = identical, 2.0 = completely dissimilar
    IF distance <= 0.3:
        RETURN 1.0
    ELIF distance <= 0.7:
        RETURN 1.0 - (distance - 0.3) / (0.7 - 0.3) * 0.5   # 1.0 → 0.5
    ELIF distance <= 1.2:
        RETURN 0.5 - (distance - 0.7) / (1.2 - 0.7) * 0.4   # 0.5 → 0.1
    ELSE:
        RETURN 0.0
```

Source: `extracted_backend_skills_01.md §4 (relevance scoring formula)`

Only chunks with relevance score > 0.0 are included in the LLM context.

#### Step 6: LLM pass (RAG)

```pseudocode
FOR each relevant chunk:
    prompt = get_extraction_prompt(chunk_text, red_flags=[])
    result = LLMClient.generate(prompt, config=AUDIT_CONFIG)
    hyperparameter_data = extract_balanced_json(result)
    sleep(1)   # inter-chunk sleep
```

#### Step 7: Merge results (LLM REDUCE phase)

All per-chunk extraction fragments (`extracted_fragments` list, each dict with relevance metadata)
are consolidated by a second LLM call (REDUCE phase) using `REDUCE_MODEL_NAME` (Gemma 4).
There is no deterministic last-write-wins logic.

```pseudocode
reduce_prompt = build_reduce_prompt(extracted_fragments)   # instructs LLM to consolidate
                                                            # conflict rules and NOT FOUND fallback
reduce_response = self.llm_client.generate(reduce_prompt)
extracted_json = parse_balanced_json(reduce_response.text)
cleaned_data = self._clean_with_regex(extracted_json)      # regex normalization of values
```

On REDUCE failure, a fallback call to `EVALUATION_MODEL_NAME` with Pydantic schema
(`response_schema=Hyperparameters`) is attempted.
SOURCE: `rag_extraction_skill.py:204-265`

### 3.6 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `extracted_hyperparameters_hybrid` | dict | Merged hyperparameter extraction from all relevant chunks |
| `triage_fragments` | list | Raw per-chunk extraction fragments; placed in context as `hybrid_triage_fragments` for frontend visualization |

### 3.7 Error Return Shape

**Success:**

```python
{'extracted_hyperparameters_hybrid': dict, 'triage_fragments': list}
```

**Failure (non-critical — pipeline continues):**

```python
{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str}
```

**Guard failure (no `paper_text` in context):**

```python
{'extracted_hyperparameters_hybrid': {}}
```

### 3.8 Side Effects

- Creates and destroys an in-memory ChromaDB collection (no disk persistence)
- Calls Google Embedding API (`batchEmbedContents`) with `batch_size=15`, sleeping 15s between batches
- Sleeps 1s between each per-chunk LLM call

Source: `extracted_backend_skills_01.md §4`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_014`

---

<a name="section-4"></a>
## Section 4 — FASE 2: Reproducibility Evaluation Skill

Source: `extracted_backend_skills_01.md §3.2 (ReproducibilityEvaluationSkill)`,
`extracted_backend_core_01.md §4.2`

### 4.1 Class

```
ReproducibilityEvaluationSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 4.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 4.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `extracted_info` | dict | Yes | Output of Phase 1 (InformationExtractionSkill) |
| `red_flags` | list[str] | Yes | List of red-flag pattern strings |

### 4.4 Guard Conditions

RULE: guard_reproducibility_evaluation  
TRIGGER: `execute()` is called  
CONDITION: `context.get("extracted_info")` is falsy  
ACTION: Return `{"success": False, "error": "No extracted_info in context", "phase": "reproducibility_evaluation"}`  
ERROR: Critical; `PaperAuditor.audit()` returns this error and halts

### 4.5 Evaluation Signals (intermediate step)

Before calling the LLM, the skill calls:

```python
evaluation_signals = get_evaluation_signals(extracted_info)
context["evaluation_signals"] = evaluation_signals
```

`get_evaluation_signals()` is NOT a prompt function — it computes a Python dict with 6 keys
derived directly from `extracted_info` (see §16 for full documentation).

### 4.6 LLM Call

```python
prompt = get_evaluation_prompt(extracted_info, red_flags)
response = LLMClient.generate(prompt, config=AUDIT_CONFIG)
```

Config used: `AUDIT_CONFIG = {"response_mime_type": "application/json", "temperature": 0.0, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384}`

Model: `"gemini-3.1-flash-lite-preview"` (via `config.MODEL_NAME`)

### 4.7 Response Parsing

1. Strip markdown JSON fences (`` ```json ``` ``).
2. Strip trailing commas before `}` or `]` (regex).
3. Apply **Balanced JSON Extraction** (§2.8).

### 4.8 Checklist Schema

The LLM returns a dict with 16 NeurIPS checklist item keys. Each value has the shape:

```python
{
    "<checklist_item_key>": {
        "answer": str,          # "Yes" | "No" | "N/A"
        "justification": str,   # free-text explanation
        "evidence": str         # direct quote or description from paper
    }
}
```

The 16 checklist item keys correspond to NeurIPS 2026 reproducibility checklist items.
[GAP: exact list of all 16 checklist item key strings not enumerated in extraction — they
are present in the prompt template `get_evaluation_prompt()` but not individually listed
in the skill extraction]

### 4.9 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `checklist` | dict | 16-item NeurIPS checklist evaluation results |
| `evaluation_signals` | dict | 6-key intermediate signals dict |

### 4.10 Error Return Shape

**Success:**

```python
{"success": True, "checklist": dict}
```

**Failure:**

```python
{"success": False, "error": str, "phase": "reproducibility_evaluation"}
```

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §2.2`

---

<a name="section-5"></a>
## Section 5 — FASE 2.5: Checklist Verification Skill

Source: `extracted_backend_skills_01.md §3.2 (ChecklistVerificationSkill)`,
`extracted_backend_core_01.md §4.2`

### 5.1 Class

```
ChecklistVerificationSkill(BaseSkill)
```

Exported: **No** (non-exported; defined in `backend/skills/auditor_skills.py:319`)

### 5.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 5.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text |
| `checklist` | dict | Yes | Output of Phase 2 (ReproducibilityEvaluationSkill) |

### 5.4 Guard Conditions

RULE: guard_checklist_verification  
TRIGGER: `execute()` is called  
CONDITION: `context.get("checklist")` is falsy or `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "Missing checklist or paper_text", "phase": "checklist_verification"}`  
ERROR: Non-critical; `PaperAuditor.audit()` catches and continues

### 5.5 Paper Context Truncation

```python
paper_context = paper_text[:30000] + paper_text[-30000:]
```

This produces a context string of at most 60,000 characters (first 30,000 + last 30,000 chars).
If `paper_text` is shorter than 60,000 characters, the concatenation overlaps but does not error.

Source: `extracted_backend_skills_01.md §3.2`, `extracted_backend_core_01.md §4.2`

### 5.6 Priority Items for Verification

The skill verifies 8 priority checklist items (verified individually via separate LLM calls).
Items beyond the 8 base items are selected to reach exactly 8 total verification calls.

[GAP: exact list of 8 priority checklist item keys not enumerated in extraction — they are
used in a priority selection algorithm inside ChecklistVerificationSkill but not individually
listed]

### 5.7 Per-Item Verification

For each of the 8 selected checklist items:

1. Extract `item_key` and `item_data` (the dict `{answer, justification, evidence}` for this item).
2. Call `get_verification_prompt(item_key, item_data, paper_context)`.
3. Call `LLMClient.generate(prompt, config=AUDIT_CONFIG)`.
4. Parse response using Balanced JSON Extraction (§2.8).
5. If verification result differs from original `answer`, update `context["checklist"][item_key]` in-place with the new `answer` and augmented `justification`.
6. Increment `context["verification_count"]`.

### 5.8 Checklist Item Schema

Each checklist item stored in `context["checklist"]`:

| Field | Type | Constraints | Description |
|---|---|---|---|
| `answer` | str | `"Yes"` \| `"No"` \| `"N/A"` | Evaluation answer |
| `justification` | str | Non-empty | Reasoning for the answer |
| `evidence` | str | May be empty | Direct quote or reference from paper |

Post-verification, a `verified` boolean field may be appended to each item:

| Field | Type | Description |
|---|---|---|
| `verified` | bool | `True` if this item was re-evaluated in Phase 2.5 |

Source: `extracted_backend_skills_01.md §3.2`

### 5.9 Output Context Keys

| Key | Type | Description |
|---|---|---|
| `checklist` | dict | Updated in-place; verified items may have modified `answer` and added `verified: True` |
| `verification_count` | int | Number of items re-verified |
| `checklist_summary` | dict | Summary statistics: `{total_items: int, verified_items: int, changed_items: int}` |

### 5.10 Error Return Shape

**Success:**

```python
{"success": True, "verification_count": int, "checklist_summary": dict}
```

**Failure (non-critical):**

```python
{"success": False, "error": str, "phase": "checklist_verification"}
```

Source: `extracted_backend_skills_01.md §3.2`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_015`

---

<a name="section-6"></a>
## Section 6 — FASE 3: Metrics Calculation Skill

Source: `extracted_backend_skills_01.md §3.2 (MetricsCalculationSkill)`,
`extracted_backend_core_01.md §4.2`

### 6.1 Class

```
MetricsCalculationSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 6.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 6.3 Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `start_time` | float | Yes | Unix timestamp from `time.time()` at audit start |
| `paper_text` | str | Yes | Full paper text |
| `extracted_info` | dict | Yes | Phase 1 output; keys filtered for red-flag counting |

### 6.4 Guard Conditions

RULE: guard_metrics_calculation
TRIGGER: `execute()` is called
CONDITION: `self.validate_context(context, ['paper_text'])` returns falsy (i.e. `paper_text` is absent or empty)
ACTION: Return `{'metrics': {}}` — no `success`, `error`, or `phase` keys
ERROR: Guard failure returns a minimal empty dict; no exception is raised

### 6.5 Metrics Calculated

| Metric | Formula | Source Field(s) | Output Key |
|---|---|---|---|
| `tiempo_segundos` | `context.get('execution_time', 0)` (pre-computed delta injected by orchestrator; NOT computed inside the skill) | `context["execution_time"]` | nested under returned `metrics` dict |
| `caracteres_leidos` | `len(paper_text)` | `context["paper_text"]` | nested under returned `metrics` dict |
| `red_flags_detectadas` | count of keys in `red_flags` dict where value is truthy AND key does NOT start with any exclusion prefix (see §6.6) | `context.get('red_flags', {})` (dict) | nested under returned `metrics` dict |

Source: `extracted_backend_skills_01.md §3.2 (MetricsCalculationSkill)`

### 6.6 Red Flag Detection Formula

```pseudocode
red_flags = context.get('red_flags', {})   # dict, not extracted_info
critical_flags = [
    k for k, v in red_flags.items()
    if v                               # truthy value
    and not k.startswith("tiene_")    # exclusion prefix 1
    and not k.startswith("menciona_") # exclusion prefix 2
    and not k.startswith("_")         # exclusion prefix 3 (internal/private keys)
    and not k.startswith("cantidad_") # exclusion prefix 4
    and not k.startswith("puntos_")   # exclusion prefix 5
]
red_flags_detectadas = len(critical_flags)
```

SOURCE: `auditor_skills.py:263-271`

The skill reads `context.get('red_flags', {})` — a dict of red-flag signals — NOT `extracted_info`.
Keys whose names start with any of the five exclusion prefixes above are excluded from the count.

### 6.7 Output Context Keys

The skill returns a single top-level key `metrics` (dict). All metric values are nested inside it:

| Outer Key | Type | Inner Keys | Description |
|---|---|---|---|
| `metrics` | dict | `tiempo_segundos` (float), `caracteres_leidos` (int), `red_flags_detectadas` (int) | All three metrics nested under this key; merged into context via `context.update(metrics_result)` |

SOURCE: `auditor_skills.py:271-279`

### 6.8 Error Return Shape

**Guard failure (paper_text absent):**

```python
{'metrics': {}}
```

No `success`, `error`, or `phase` keys are present in any return path. The return value is always a dict with key `metrics`.

SOURCE: `auditor_skills.py:257-258`

---

<a name="section-7"></a>
## Section 7 — FASE 4: Metadata Aggregation Skill

Source: `extracted_backend_skills_01.md §3.2 (MetadataAggregationSkill)`,
`extracted_backend_core_01.md §4.2`

### 7.1 Class

```
MetadataAggregationSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py`)

### 7.2 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 7.3 Input Context Keys

The skill does NOT read the 23 keys from §1.2 directly. It reads from two groups:

**Group A — from `context.get('evaluation', {})` (16 NeurIPS checklist sub-keys):**

| Sub-key of `evaluation` | Description |
|---|---|
| `claims` | Claims audit result |
| `limitations` | Limitations acknowledgement |
| `theory_assumptions_proofs` | Theoretical rigor |
| `experimental_result_reproducibility` | Reproducibility criteria |
| `open_access_data_code` | Data/code availability |
| `experimental_setting_details` | Experimental settings |
| `experiment_statistical_significance` | Statistical significance |
| `experiments_compute_resource` | Compute resources |
| `code_of_ethics` | Ethics statement |
| `broader_impacts` | Broader impacts |
| `safeguards` | Safety safeguards |
| `licenses` | License compliance |
| `assets` | Asset documentation |
| `crowdsourcing_human_subjects` | Human subjects / crowdsourcing |
| `irb_approvals` | IRB approval |
| `declaration_llm_usage` | LLM usage declaration |

**Group B — direct context keys:**

| Key | Type | Description |
|---|---|---|
| `extracted_info` | dict | Phase 1 extraction output (stored as `informacion_extraida` in result) |
| `red_flags` | dict | Red-flag signals dict |
| `metrics` | dict | Phase 3 metrics dict |
| `general_analysis_map` | list | MAP analysis fragments |
| `general_analysis_reduce` | dict | REDUCE analysis result |
| `hybrid_triage_fragments` | list | Phase 1.5 RAG triage fragments |
| `evaluation_signals` | dict | Phase 2 evaluation signals |

SOURCE: `auditor_skills.py:285-317`

### 7.4 Aggregation Strategy

```pseudocode
evaluation = context.get('evaluation', {})

result = {
    # 16 NeurIPS checklist keys unpacked from evaluation dict
    "claims":                              evaluation.get('claims', {}),
    "limitations":                         evaluation.get('limitations', {}),
    "theory_assumptions_proofs":           evaluation.get('theory_assumptions_proofs', {}),
    "experimental_result_reproducibility": evaluation.get('experimental_result_reproducibility', {}),
    "open_access_data_code":               evaluation.get('open_access_data_code', {}),
    "experimental_setting_details":        evaluation.get('experimental_setting_details', {}),
    "experiment_statistical_significance": evaluation.get('experiment_statistical_significance', {}),
    "experiments_compute_resource":        evaluation.get('experiments_compute_resource', {}),
    "code_of_ethics":                      evaluation.get('code_of_ethics', {}),
    "broader_impacts":                     evaluation.get('broader_impacts', {}),
    "safeguards":                          evaluation.get('safeguards', {}),
    "licenses":                            evaluation.get('licenses', {}),
    "assets":                              evaluation.get('assets', {}),
    "crowdsourcing_human_subjects":        evaluation.get('crowdsourcing_human_subjects', {}),
    "irb_approvals":                       evaluation.get('irb_approvals', {}),
    "declaration_llm_usage":               evaluation.get('declaration_llm_usage', {}),
    # 7 direct context keys
    "informacion_extraida":    context.get('extracted_info', {}),
    "red_flags":               context.get('red_flags', {}),
    "metricas":                context.get('metrics', {}),
    "general_analysis_map":    context.get('general_analysis_map', []),
    "general_analysis_reduce": context.get('general_analysis_reduce', {}),
    "hybrid_triage_fragments": context.get('hybrid_triage_fragments', []),
    "evaluation_signals":      context.get('evaluation_signals', {}),
}
RETURN result   # returned directly; NOT stored as context["result"]
                # NO audit_complete, NO pipeline_version added
```

SOURCE: `auditor_skills.py:285-317`

### 7.5 Output Context Keys

The skill returns `result` dict directly (it is NOT stored as `context["result"]`). The dict has 23 keys as shown in §7.4. No `audit_complete` or `pipeline_version` fields are added.

### 7.6 Return Shape

The skill returns the `result` dict directly — no `success`/`error`/`phase` envelope:

```python
{
    "claims": dict,
    "limitations": dict,
    # ... (16 NeurIPS checklist sub-keys from evaluation) ...
    "informacion_extraida": dict,
    "red_flags": dict,
    "metricas": dict,
    "general_analysis_map": list,
    "general_analysis_reduce": dict,
    "hybrid_triage_fragments": list,
    "evaluation_signals": dict,
}
```

No `success`, `result`, `audit_complete`, or `pipeline_version` keys are present.

SOURCE: `auditor_skills.py:285-317`

---

<a name="section-8"></a>
## Section 8 — CompositeSkill Orchestration

Source: `extracted_backend_skills_01.md §2.3`

### 8.1 Class

```
CompositeSkill(BaseSkill)
```

Exported: **Yes** (in `__init__.py` via `BaseSkill`)

### 8.2 Constructor

```python
def __init__(self, skills: list[BaseSkill], llm_client: Optional[LLMClient] = None):
    super().__init__(llm_client)
    self.skills = skills
```

There is no `name` parameter. The constructor takes `llm_client` (optional) and delegates to `BaseSkill.__init__`.

SOURCE: `base_skill.py:91-100`

### 8.3 `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

### 8.4 Chaining Algorithm

```pseudocode
FUNCTION CompositeSkill.execute(context):
    accumulated_context = context.copy()   # shallow copy of initial context

    FOR i, skill IN enumerate(self.skills, 1):
        TRY:
            result = skill.execute(accumulated_context)
            accumulated_context.update(result)   # merge result into accumulated context
        EXCEPT Exception as e:
            # Error stored under key "error_<skill.name>"; chain continues
            accumulated_context[f"error_{skill.name}"] = str(e)
            # NO return here — subsequent skills are still executed

    RETURN accumulated_context   # plain dict; no success/failed_skill/phase envelope
```

**Error isolation**: There is NO halt on sub-skill failure. On exception, the error is recorded
under `accumulated_context["error_<skill.name>"]` and the next skill in the list still executes.
Result dict success flags are NOT checked — only uncaught exceptions are handled.

SOURCE: `base_skill.py:103-124`

### 8.5 Context Propagation

The initial context is shallow-copied into `accumulated_context`. Each skill's output is merged
into `accumulated_context` via `.update(result)`. A later skill can read keys written by an
earlier skill. Errors from individual skills do not prevent subsequent skills from running.

### 8.6 Return Shape

`CompositeSkill.execute()` returns `accumulated_context` — the plain accumulated dict of all
context keys plus any results merged in from sub-skills. There is no wrapper envelope:

```python
# Return is the accumulated context dict directly, e.g.:
{
    "paper_text": str,
    "extracted_info": dict,
    # ... all keys from initial context + skill outputs ...
    # On exception in a sub-skill:
    "error_<SkillClassName>": str,   # e.g. "error_InformationExtractionSkill"
}
```

No `success`, `context`, `failed_skill`, or `phase` keys are present at the top level.

SOURCE: `base_skill.py:103-124`

---

<a name="section-9"></a>
## Section 9 — BaseSkill Interface and Lifecycle

Source: `extracted_backend_skills_01.md §2.1`

### 9.1 Class

```
BaseSkill(ABC)
```

Exported: **Yes** (in `__init__.py`)  
Module: `backend/skills/base_skill.py`

### 9.2 Abstract Interface

```python
from abc import ABC, abstractmethod

class BaseSkill(ABC):

    def __init__(self, llm_client: Optional[LLMClient] = None, config: Optional[Dict] = None):
        self.llm_client = llm_client
        self.config = config or {}
        self.name = self.__class__.__name__   # instance attribute, NOT a @property
        logger.debug(f"Skill '{self.name}' inicializado")

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill against the provided context.

        Args:
            context: Shared mutable dict containing all pipeline state.
                     Skills read from and write to this dict.

        Returns:
            dict with skill-specific output keys.
            (No mandatory success/error/phase contract — see §9.4 for details.)
        """
        pass
```

`name` is set as an **instance attribute** (`self.name = self.__class__.__name__`) in `__init__`, not as a `@property`. Functionally equivalent at read time, but architecturally there is no property descriptor.

SOURCE: `base_skill.py:19-45`

### 9.3 Lifecycle

```
1. Instantiation: __init__(self, llm_client: LLMClient, config: dict)
   → Sub-classes receive LLMClient and config at construction time.
   → No abstract __init__; concrete classes call super().__init__() if needed.

2. Guard check (optional, not abstract):
   → Concrete implementations check preconditions at the START of execute().
   → If guard fails, return {"success": False, "error": ..., "phase": ...} immediately.
   → No separate abstract guard method.

3. execute(context):
   → Read required keys from context.
   → Perform skill logic (LLM calls, regex, computation).
   → Write output keys into context (mutate in-place) AND return them.
   → Return {"success": True, ...output_keys...} or {"success": False, "error": ...}

4. Teardown: none (no abstract teardown/cleanup hook).
```

### 9.4 Contract for `execute()` Return Type

The `BaseSkill.execute()` docstring states the return dict should contain:

| Key | Type | Stated Condition | Description |
|---|---|---|---|
| `success` | bool | On error path (guard fail) | `True` if skill completed without error |
| `error` | str | Only when guard fails | Error message |
| `phase` | str | Only when guard fails | Phase identifier for diagnostics |

**Enforcement:** The contract is **not enforced at runtime** by `BaseSkill`. The abstract method signature is `execute(self, context: Dict[str, Any]) -> Dict[str, Any]` (SOURCE: `base_skill.py:34`), with no post-execute hook that inspects or validates the returned keys. Python's ABC machinery enforces only that `execute()` is implemented by concrete subclasses; it does not constrain the return dict structure.

**Actual violation behavior:** No concrete auditor, chatbot, or SOTA skill returns a `success` key on either the normal or guard-failure path. Each class returns its own domain-specific keys instead. When a guard check fails, concrete classes return a skill-specific empty sentinel (not the `success=False` envelope):
- `InformationExtractionSkill` guard fail: `{'extracted_info': {}}` (SOURCE: `auditor_skills.py:23`)
- `ReproducibilityEvaluationSkill` guard fail: `{'evaluation': {}}` (SOURCE: `auditor_skills.py:196`)
- `MetricsCalculationSkill` guard fail: `{'metrics': {}}` (SOURCE: `auditor_skills.py:258`)
- `ConversationalResponseSkill` guard fail: `{'response': '❌ Error: Faltan datos para generar respuesta'}` (SOURCE: `chatbot_skills.py:26`)
- `ThematicCoverageSkill` guard fail: `{'thematic_data': {}}` (SOURCE: `sota_skills.py:35`)

Because no calling code in the pipeline checks for a `success` key, the absence of enforcement has no observable runtime effect — the orchestrator reads domain keys directly from the returned dict.

Additional output keys are skill-specific and documented per skill in §§ 2–7, 10–11.

### 9.5 Hooks

No `pre_execute` or `post_execute` hooks are defined in `BaseSkill`. These patterns are not
present in the extraction data.

Source: `extracted_backend_skills_01.md §2.1`

### 9.6 Constructor Pattern (concrete subclasses)

```python
def __init__(self, llm_client: LLMClient, config: dict = None):
    self.llm_client = llm_client
    self.config = config or AUDIT_CONFIG
```

Source: `extracted_backend_skills_01.md §2.2`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_016`

---

<a name="section-10"></a>
## Section 10 — Regex Detection Skills (9 Non-Exported Skills)

Source: `extracted_backend_skills_01.md §5`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_018`

### 10.0 Shared Infrastructure

All 9 regex detection skills inherit from `BaseSkill` and share the following:

#### NEGATION_WINDOW

```python
NEGATION_WINDOW = 60   # characters before a match to scan for negation
```

#### `_search_with_negation(pattern, text, flags)` — shared method

```pseudocode
FUNCTION _search_with_negation(pattern, text, flags=re.IGNORECASE):
    matches = []
    FOR m IN re.finditer(pattern, text, flags):
        start = max(0, m.start() - NEGATION_WINDOW)
        prefix = text[start : m.start()]
        IF any negation phrase in prefix (e.g., "not", "no", "without", "lack"):
            CONTINUE   # skip negated match
        matches.append(m)
    RETURN matches
```

Source: `extracted_backend_skills_01.md §5.0`

#### `TableExtractionHelper` — 3 table patterns

```python
TABLE_PATTERNS = [
    r'Table\s+\d+\s*[:\.]',           # Pattern 1: "Table N:" or "Table N."
    r'^\|.+\|.+\|',                    # Pattern 2: pipe-delimited table rows (multiline)
    r'^\t.+\t',                         # Pattern 3: tab-delimited rows (multiline)
]
```

Used by `HyperparameterDetectionSkill` and `StatisticsDetectionSkill` to extract table
regions first (searched WITHOUT negation), before full-text search (with negation).

Source: `extracted_backend_skills_01.md §5.0`

---

### Skill: HyperparameterDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Guard Conditions

RULE: guard_hyperparameter_detection  
CONDITION: `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "No paper_text", "phase": "hyperparameter_detection"}`

#### Algorithm

1. Extract table regions using `TableExtractionHelper` (3 patterns, no negation).
2. Search tables with `HYPERPARAMETER_PATTERNS` (without negation).
3. Search full `paper_text` with `HYPERPARAMETER_PATTERNS` using `_search_with_negation`.
4. Merge and deduplicate results.

#### Regex Patterns (`HYPERPARAMETER_PATTERNS`)

```python
HYPERPARAMETER_PATTERNS = [
    r'\blearning[_\s]?rate\s*[=:]\s*[\d.e+-]+',
    r'\bbatch[_\s]?size\s*[=:]\s*\d+',
    r'\bepoch[s]?\s*[=:]\s*\d+',
    r'\bdropout\s*[=:]\s*[\d.]+',
    r'\bweight[_\s]?decay\s*[=:]\s*[\d.e+-]+',
    r'\bmomentum\s*[=:]\s*[\d.]+',
    r'\bhidden[_\s]?(?:size|dim|units)\s*[=:]\s*\d+',
    r'\blayers?\s*[=:]\s*\d+',
    r'\bheads?\s*[=:]\s*\d+',
    r'\bwarmup[_\s]?steps?\s*[=:]\s*\d+',
]
```

Source: `extracted_backend_skills_01.md §5.1`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `hyperparameter_matches` | list[str] | List of matched strings |
| `hyperparameter_count` | int | Total match count |

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "hyperparameter_detection"}
```

Source: `extracted_backend_skills_01.md §5.1`

---

### Skill: DataAvailabilityDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Guard Conditions

RULE: guard_data_availability_detection  
CONDITION: `context.get("paper_text")` is falsy  
ACTION: Return `{"success": False, "error": "No paper_text", "phase": "data_availability_detection"}`

#### Regex Patterns

```python
DATA_AVAILABILITY_PATTERNS = [
    r'\bdata(?:set)?\s+(?:is\s+)?(?:publicly\s+)?available',
    r'\bdata(?:set)?\s+(?:can\s+be\s+)?(?:found|accessed|downloaded)\s+(?:at|from)',
    r'\bwe\s+(?:release|provide|make\s+available)\s+(?:the\s+)?(?:data|dataset)',
    r'\brepository\s+(?:at|on|in)\s+(?:https?://|github|zenodo)',
    r'\bzenodo\.org',
    r'\bfigshare\.com',
    r'\bhuggingface\.co/datasets',
    r'\bdata\s+availability\s+statement',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `data_availability_mentions` | list[str] | Matched strings |
| `data_available` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.2`

---

### Skill: CodeAvailabilityDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
CODE_AVAILABILITY_PATTERNS = [
    r'\bcode\s+(?:is\s+)?(?:publicly\s+)?available',
    r'\bimplementation\s+(?:is\s+)?(?:publicly\s+)?available',
    r'\bgithub\.com/[\w\-]+/[\w\-]+',
    r'\bgitlab\.com/[\w\-]+/[\w\-]+',
    r'\bbitbucket\.org/[\w\-]+/[\w\-]+',
    r'\bwe\s+(?:release|open[_\s]?source|publish)\s+(?:the\s+)?(?:code|implementation)',
    r'\bsource\s+code\s+(?:is\s+)?(?:available|released|provided)',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `code_availability_mentions` | list[str] | Matched strings |
| `code_available` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.3`

---

### Skill: StatisticsDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Algorithm

Same as `HyperparameterDetectionSkill`: tables extracted first (no negation), then
full-text with negation.

#### Regex Patterns

```python
STATISTICS_PATTERNS = [
    r'\bp\s*[<>=]\s*[\d.e+-]+',
    r'\bconfidence\s+interval',
    r'\bstandard\s+(?:deviation|error)\s*[=:±]\s*[\d.]+',
    r'\bt[_\s]?test',
    r'\bchi[_\s]?square',
    r'\banova\b',
    r'\bwilcoxon\b',
    r'\bmann[_\s]?whitney\b',
    r'\bbootstrap\s+(?:confidence|interval|sample)',
    r'\bcorrelation\s+coefficient\s*[=:r]\s*[\d.+-]+',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `statistics_matches` | list[str] | Matched strings |
| `statistics_count` | int | Total match count |
| `statistical_tests_found` | bool | `True` if any statistical test pattern matched |

Source: `extracted_backend_skills_01.md §5.4`

---

### Skill: EnvironmentalImpactDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
ENVIRONMENTAL_IMPACT_PATTERNS = [
    r'\bCO2\s*(?:emission|equivalent|footprint)',
    r'\bcarbon\s+(?:footprint|emission|offset)',
    r'\benergy\s+consumption\s*[=:]\s*[\d.]+',
    r'\bkWh\b',
    r'\bwatt[_\s]?hours?\b',
    r'\bgreen(?:house)?\s+gas',
    r'\bsustainab(?:le|ility)',
    r'\benvironmental\s+impact',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `environmental_mentions` | list[str] | Matched strings |
| `environmental_impact_reported` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.5`

---

### Skill: ProblematicPhrasesDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
PROBLEMATIC_PHRASES_PATTERNS = [
    r'\bstate[_\s]?of[_\s]?the[_\s]?art\b',
    r'\bgroundbreaking\b',
    r'\brevolutionary\b',
    r'\bunprecedented\b',
    r'\bsignificantly\s+(?:outperform|better|superior)',
    r'\btrivially\b',
    r'\bobviously\b',
    r'\bclearly\s+(?:show|demonstrate|prove)',
    r'\bwe\s+prove\s+that\b',
    r'\bit\s+is\s+(?:well[_\s]?known|obvious|clear)\s+that\b',
]
```

Note: These patterns are searched WITHOUT negation (the phrases themselves are the red flags).

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `problematic_phrases` | list[str] | All matched strings |
| `problematic_phrase_count` | int | Total count |

Source: `extracted_backend_skills_01.md §5.6`

---

### Skill: LlmUsageDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
LLM_USAGE_PATTERNS = [
    r'\bGPT[_\s]?-?[34](?:[_\s]?(?:turbo|mini|vision))?\b',
    r'\bChatGPT\b',
    r'\bClaude[_\s]?[23]?\b',
    r'\bGemini[_\s]?(?:Pro|Ultra|Flash|Nano)?\b',
    r'\bLLaMA[_\s]?[23]?\b',
    r'\bMistral\b',
    r'\blarge\s+language\s+model',
    r'\bLLM\b',
    r'\bfoundation\s+model',
    r'\bpre[_\s]?trained\s+(?:language\s+)?model',
    r'\bprompt(?:ing|ed)?\b',
    r'\bfine[_\s]?tun(?:ing|ed)\s+(?:a\s+)?(?:language|LLM)',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `llm_mentions` | list[str] | All matched strings |
| `llm_used` | bool | `True` if any match found |
| `llm_models_detected` | list[str] | Distinct model names found |

Source: `extracted_backend_skills_01.md §5.7`

---

### Skill: CrowdsourcingDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
CROWDSOURCING_PATTERNS = [
    r'\bMechanical\s+Turk\b',
    r'\bMTurk\b',
    r'\bcrowd(?:source|work(?:er)?)',
    r'\bAnnot(?:ation|ator)s?\s+(?:were\s+)?(?:recruited|hired)',
    r'\bhuman\s+(?:evaluator|annotator|rater|judge)s?',
    r'\binter[_\s]?annotator\s+agreement',
    r'\bkappa\s+(?:coefficient|score)',
    r'\bIRR\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `crowdsourcing_mentions` | list[str] | Matched strings |
| `crowdsourcing_used` | bool | `True` if any match found |

Source: `extracted_backend_skills_01.md §5.8`

---

### Skill: LicenseDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **No**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
LICENSE_PATTERNS = [
    r'\bMIT\s+[Ll]icense\b',
    r'\bApache[_\s]?2(?:\.0)?\s+[Ll]icense\b',
    r'\bGNU\s+(?:GPL|LGPL|AGPL)[_\s]?v?[23]?\b',
    r'\bCreative\s+Commons\b',
    r'\bCC[_\s]?(?:BY|SA|NC|ND)[_\s]?(?:4\.0|3\.0)?\b',
    r'\bBSD[_\s]?(?:2|3)[_\s]?Clause\b',
    r'\bproprietary\s+licen[sc]e\b',
    r'\blicen[sc]ed?\s+under\b',
    r'\bcopyright\s+©?\s*\d{4}\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `license_mentions` | list[str] | Matched strings |
| `license_detected` | bool | `True` if any match found |
| `license_types` | list[str] | Distinct license type strings found |

Source: `extracted_backend_skills_01.md §5.9`

---

<a name="section-11"></a>
## Section 11 — All 15 Exported Skills

Source: `extracted_backend_skills_01.md §§2,3,6,7`, `extracted_backend_core_01.md §§3,4`,
`cross_ref_resolution_cross_ref_root_to_backend.md §§g_009–g_023`

The 15 exported skills are defined in `backend/skills/__init__.py:36`.

---

### Skill: BaseSkill

Already fully documented in §9.

Exported: **Yes**  
Module: `backend/skills/base_skill.py`

---

### Skill: InformationExtractionSkill

Already fully documented in §2.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: ReproducibilityEvaluationSkill

Already fully documented in §4.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: MetricsCalculationSkill

Already fully documented in §6.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: MetadataAggregationSkill

Already fully documented in §7.

Exported: **Yes**  
Module: `backend/skills/auditor_skills.py`

---

### Skill: ConversationalResponseSkill

**Module**: `backend/skills/chatbot_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Generates a conversational answer from the LLM for a user question in the chatbot context,
using the paper content and conversation history.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `question` | str | Yes | The user's current question |
| `paper_text` | str | Yes | Full paper text for context (guard check; also embedded in prompt) |
| `history_text` | str | No (default `'Sin historial previo.'`) | Pre-formatted string of prior conversation history — NOT a list of dicts |

SOURCE: `chatbot_skills.py:24-36`

#### Guard Conditions

RULE: guard_conversational_response
CONDITION: `self.validate_context(context, ['paper_text', 'question'])` returns falsy (either key absent/empty)
ACTION: Return `{'response': '❌ Error: Faltan datos para generar respuesta'}` — no `success`, `error`, or `phase` keys

SOURCE: `chatbot_skills.py:25-26`

#### LLM Usage

- Prompt: manually constructed f-string embedding `paper_text`, `history_text`, and `question` (SOURCE: `chatbot_skills.py:38-56`)
- Config: no config override — calls `self.llm_client.generate(prompt)` with no extra arguments
- No named `CHAT_CONFIG` is used for this call

SOURCE: `chatbot_skills.py:59-61`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `response` | str | The LLM-generated answer (`response.text`) |

No `answer` key. No `updated_history` key.

SOURCE: `chatbot_skills.py:62`

#### Return Shape

**Success:**

```python
{'response': str}   # e.g. {'response': 'The paper discusses...'}
```

**Guard failure:**

```python
{'response': '❌ Error: Faltan datos para generar respuesta'}
```

**LLM exception:**

```python
{'response': '❌ Hubo un error de conexión con el revisor: <str(e)>'}
```

No `success`, `error`, or `phase` keys in any return path.

SOURCE: `chatbot_skills.py:25-26, 59-63`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
Source: `chatbot_skills.py` (see corrected details above)

---

### Skill: ContextValidationSkill

**Module**: `backend/skills/chatbot_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Validates that a user question is answerable given the available paper context; returns
a relevance score and a recommendation to proceed or redirect.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `question` | str | Yes | User question |
| `paper_text` | str | Yes | Full paper text |
| `extracted_info` | dict | No | Phase 1 output |

#### Guard Conditions

RULE: guard_context_validation  
CONDITION: `context.get("question")` is falsy  
ACTION: Return `{"success": False, "error": "No question in context", "phase": "context_validation"}`

#### LLM Usage

- Config: `AUDIT_CONFIG` (JSON output)
- Returns JSON with `{is_relevant: bool, confidence: float, reason: str}`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `question_relevant` | bool | Whether the question is answerable from paper context |
| `relevance_confidence` | float | Confidence in the relevance judgment (0.0–1.0) |
| `relevance_reason` | str | Explanation |

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "context_validation"}
```

Source: `extracted_backend_skills_01.md §7 (ContextValidationSkill)`

---

### Skill: ThematicCoverageSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Identifies the main thematic areas of the paper to generate relevant SOTA search queries.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text — only key checked by validate_context |

#### Guard Conditions

RULE: guard_thematic_coverage
CONDITION (key presence): `validate_context(context, ['paper_text'])` returns False
  (key `paper_text` absent from context dict)
ACTION: Return `{'thematic_data': {}}` — no exception raised
  SOURCE: sota_skills.py:33-34

CONDITION (no LLM): `not self.llm_client`
ACTION: Log error "No hay cliente LLM configurado"; return `{'thematic_data': {}}`
  SOURCE: sota_skills.py:36-38

NOTE: No minimum document length guard exists. An empty string for `paper_text`
passes the validate_context check and is forwarded directly to the LLM prompt.

#### LLM Usage

- Config: `SOTA_CONFIG = {"response_mime_type": "application/json", "temperature": 0.1}`
- Returns JSON with `{themes: list[str], keywords: list[str], research_area: str}`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `thematic_data` | dict | Dict with keys `subtemas` (list[str]), `areas_tecnicas` (list[str]), `año_paper` (int or None) — result of JSON parse from LLM response |

#### Error Return Shape

Guard fail (missing key or no LLM): `{'thematic_data': {}}`  
Exception during LLM call or JSON parse:
```python
{'thematic_data': {"subtemas": [], "areas_tecnicas": [], "año_paper": None}}
```
Exception types caught by `except Exception as e` (sota_skills.py:73):
- `json.JSONDecodeError` — if `json.loads(response.text)` fails (malformed LLM output)
- `AttributeError` — if `response.text` is None
No exception is re-raised; all paths return a dict.

Source: `extracted_backend_skills_01.md §6 (ThematicCoverageSkill)`

---

### Skill: QueryGenerationSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Generates a list of Semantic Scholar search queries based on the paper's themes and keywords.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full text of the paper being analysed |
| `thematic_data` | dict | Yes | From ThematicCoverageSkill (contains `subtemas`, `areas_tecnicas`, `año_paper`) |

#### Guard Conditions

RULE: guard_query_generation  
CONDITION: `context.get("paper_text")` is falsy or `context.get("thematic_data")` is falsy (SOURCE: `sota_skills.py:107`)  
ACTION: Return `{'search_queries': []}`

#### LLM Usage

- Config: `SOTA_CONFIG`
- Returns JSON with `{search_queries: list[str]}` (3–5 queries)

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `search_queries` | list[str] | Generated search query strings for Semantic Scholar |

Source: `extracted_backend_skills_01.md §6 (QueryGenerationSkill)`

---

### Skill: SemanticScholarSearchSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Executes Semantic Scholar API searches for the generated queries and returns raw paper results.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `search_queries` | list[str] | Yes | From QueryGenerationSkill |

Each element in `search_queries` is a string; minimum 1 element required.

#### Guard Conditions

RULE: guard_semantic_scholar_search  
CONDITION: `context.get("search_queries")` is falsy or empty list  
ACTION: Return `{"success": False, "error": "No search_queries in context", "phase": "semantic_scholar_search"}`

#### Semantic Scholar API Integration

**Endpoint**: `https://api.semanticscholar.org/graph/v1/paper/search`  
**Auth**: None (public API, unauthenticated)  
**Rate limiting**: No explicit rate limit handling in skill; relies on HTTP 429 retry in LLMClient  
[GAP: whether API key is optionally injected via config is not confirmed in extraction]

**Query parameters for each request**:

| Parameter | Value | Type |
|---|---|---|
| `query` | search query string | str |
| `fields` | `"paperId,title,authors,year,citationCount,abstract,url"` | str |
| `year` | `"2023-2026"` | str |
| `limit` | `5` | int |

**Per-query response element schema**:

| Field | Type | Description |
|---|---|---|
| `paperId` | str | Semantic Scholar paper identifier |
| `title` | str | Paper title |
| `authors` | list[dict] | Each element: `{authorId: str, name: str}` |
| `year` | int | Publication year |
| `citationCount` | int | Citation count at time of query |
| `abstract` | str \| null | Paper abstract |
| `url` | str | Link to paper on Semantic Scholar |

**Error handling**:

| Condition | Behavior |
|---|---|
| HTTP 4xx/5xx | Log error; skip this query; continue with next query |
| Empty `data` list in response | Record empty result for this query; continue |
| Timeout | [GAP: timeout value not specified in extraction] |
| JSON parse error | Log error; skip this query |

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `sota_papers` | list[dict] | All unique papers found across all queries, deduplicated by `paperId`, sorted by `citationCount` descending, capped at 10 elements (SOURCE: `sota_skills.py:227-232`) |
| `query_results` | dict | Mapping of `query_string → list[paper_dict]` (raw per-query results) |

**Post-collection deduplication and ranking** (SOURCE: `sota_skills.py:227-232`):

```python
unique_papers = {p['paperId']: p for p in sota_papers if p.get('paperId')}.values()
sorted_papers = sorted(unique_papers, key=lambda x: x.get('citationCount', 0), reverse=True)[:10]
```

Steps: (1) Build dict keyed by `paperId` — last occurrence of a duplicate wins. (2) Sort by `citationCount` descending. (3) Cap result at 10 papers regardless of how many queries ran or how many unique papers were found.

**`sota_papers` element schema**: same as per-query response element schema above.

#### Error Return Shape

```python
{"success": False, "error": str, "phase": "semantic_scholar_search"}
```

Source: `extracted_backend_core_01.md §4.3 (SemanticScholar integration)`,
`extracted_backend_skills_01.md §6 (SemanticScholarSearchSkill)`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_021`

---

### Skill: CoverageGapAnalysisSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Analyzes the retrieved SOTA papers to identify gaps between the audited paper and state-of-the-art.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text; first 5000 and last 10000 chars used in prompt (SOURCE: `sota_skills.py:275-276`) |
| `thematic_data` | dict | Yes | From ThematicCoverageSkill; `subtemas` list extracted and joined for the prompt |

#### Guard Conditions

RULE: guard_coverage_gap_analysis  
CONDITION: `context.get("paper_text")` is falsy or `context.get("thematic_data")` is falsy (SOURCE: `sota_skills.py:256`)  
ACTION: Return `{'coverage_gaps': {}}`

#### LLM Usage

- Config: `SOTA_CONFIG`
- Returns JSON with gap analysis results

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `coverage_gaps` | dict | Contains key `areas_debiles` (list[dict]); each element: `{subtema: str, diagnostico: str}` (SOURCE: `sota_skills.py:280-288, 294`) |

Note: `sota_comparison_summary` is NOT produced by this skill. The LLM prompt returns `{"areas_debiles": [...]}` and this is stored verbatim under `coverage_gaps`. The key is populated only if the LLM call succeeds; on error, returns `{'coverage_gaps': {"areas_debiles": []}}` (SOURCE: `sota_skills.py:293-298`).

Source: `extracted_backend_skills_01.md §6 (CoverageGapAnalysisSkill)`

---

### Skill: CrossValidationSkill

**Module**: `backend/skills/sota_skills.py`  
Exported: **Yes**

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Purpose

Cross-validates the paper's claims against the SOTA papers to identify potential inconsistencies
or unsupported claims.

#### Input Context Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `paper_text` | str | Yes | Full paper text; first 5000 and last 15000 chars used in prompt (SOURCE: `sota_skills.py:361-362`) |
| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill; used to build SOTA context string |
| `thematic_data` | dict | Yes | From ThematicCoverageSkill; `subtemas` list joined for prompt (SOURCE: `sota_skills.py:319`) |
| `coverage_gaps` | dict | No | From CoverageGapAnalysisSkill; added to `cobertura_tematica` in output; defaults to `{"areas_debiles": []}` if absent (SOURCE: `sota_skills.py:341`) |

#### Guard Conditions

RULE: guard_cross_validation  
CONDITION: `context.get("paper_text")` is falsy or `context.get("sota_papers")` is falsy or `context.get("thematic_data")` is falsy (SOURCE: `sota_skills.py:319-321`)  
ACTION: Return `{'validation_results': {}}`

Secondary guard (SOURCE: `sota_skills.py:323-331`):  
CONDITION: `sota_papers` list is empty  
ACTION: Return `{'validation_results': {"papers_omitidos": [], "cobertura_tematica": {"areas_debiles": []}, "conclusion_sota": "No se encontraron artículos recientes (2023-2026) en Semantic Scholar."}}`

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `validation_results` | dict | Contains `papers_omitidos` (list[dict]), `conclusion_sota` (str), `cobertura_tematica` (dict), `papers_analizados` (list[dict]) (SOURCE: `sota_skills.py:384-420`) |

`papers_omitidos` element schema: `{titulo: str, año: int, citas: int, url: str, relevancia: str, subtema_relacionado: str, justificacion: str}`  
`papers_analizados` element schema: `{titulo: str, año: int, citas: int, url: str, autores: list}`  
`cobertura_tematica` contains key `areas_debiles` (list[dict]) from `CoverageGapAnalysisSkill` output; defaults to `{"areas_debiles": []}` if not present in context.

Note: `cross_validation_results` and `unsupported_claims_count` are NOT produced by this skill.

Source: `extracted_backend_skills_01.md §6 (CrossValidationSkill)`

---

### Skill: LimitationsQualityDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **Yes** (one of 3 exported regex skills)

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
LIMITATIONS_PATTERNS = [
    r'\blimitation[s]?\b',
    r'\bshortcoming[s]?\b',
    r'\bweakness(?:es)?\b',
    r'\bfuture\s+work\b',
    r'\bopen\s+(?:question|problem|issue)\b',
    r'\bwe\s+(?:acknowledge|note)\s+(?:that\s+)?(?:this|our)',
    r'\bscope\s+(?:of\s+(?:this|our)\s+work|limitation)',
    r'\bnot\s+(?:address|cover|include|consider)\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `limitations_mentions` | list[str] | Matched strings |
| `limitations_section_found` | bool | `True` if a limitations section was detected |
| `limitations_quality_score` | float | Score based on specificity and depth of limitations [GAP: scoring formula not specified] |

Source: `extracted_backend_skills_01.md §5 (LimitationsQualityDetectionSkill)`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_018`

---

### Skill: SoftwareVersionDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **Yes** (one of 3 exported regex skills)

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
SOFTWARE_VERSION_PATTERNS = [
    r'\bPython\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bTensorFlow\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bPyTorch\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bscikit[_\-]learn\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bnumpy\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bpandas\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bHugging\s+Face\s+[Tt]ransformers\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bJAX\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bCUDA\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bcuDNN\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bversion\s+\d+\.\d+(?:\.\d+)?\b',
    r'\bv\d+\.\d+(?:\.\d+)?\b',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `software_versions` | list[dict] | Each: `{software: str, version: str, match: str}` |
| `software_versioning_found` | bool | `True` if any version match found |

Source: `extracted_backend_skills_01.md §5 (SoftwareVersionDetectionSkill)`

---

### Skill: HardwareDetailDetectionSkill

**Module**: `backend/skills/regex_detection_skills.py`  
Exported: **Yes** (one of 3 exported regex skills)

#### `execute()` Signature

```python
def execute(self, context: dict) -> dict:
```

#### Input Context Keys

| Key | Type | Required |
|---|---|---|
| `paper_text` | str | Yes |

#### Regex Patterns

```python
HARDWARE_PATTERNS = [
    r'\bNVIDIA\s+(?:A100|V100|H100|T4|RTX\s*\d+|Titan)',
    r'\bGPU[s]?\b',
    r'\bTPU[s]?\b',
    r'\bA100\b',
    r'\bV100\b',
    r'\bH100\b',
    r'\bRTX\s*\d{4}\b',
    r'\b\d+\s*GB\s+(?:VRAM|GPU\s+memory)\b',
    r'\bIntel\s+(?:Xeon|Core\s+i\d)',
    r'\bAMD\s+(?:EPYC|Ryzen)',
    r'\b\d+\s+(?:CPU|GPU)\s+(?:cores?|nodes?)\b',
    r'\bcluster\s+of\s+\d+',
    r'\bdistributed\s+(?:training|computing)\s+(?:on|with)\s+\d+',
]
```

#### Output Context Keys

| Key | Type | Description |
|---|---|---|
| `hardware_mentions` | list[str] | Matched strings |
| `hardware_details_found` | bool | `True` if any hardware detail found |
| `gpu_models` | list[str] | Distinct GPU model names detected |

Source: `extracted_backend_skills_01.md §5 (HardwareDetailDetectionSkill)`

---

<a name="section-12"></a>
## Section 12 — SOTA Analysis Pipeline (5 Steps)

Source: `extracted_backend_core_01.md §4.3`, `extracted_backend_skills_01.md §6`,
`cross_ref_resolution_cross_ref_root_to_backend.md §g_021`

### 12.1 Class: SotaAnalyzer

```python
class SotaAnalyzer:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
```

Module: `backend/services/sota_analyzer.py`

### 12.2 Entry Point

```python
def analyze(self, paper_text: str, extracted_info: dict) -> dict:
```

### 12.3 Pipeline: 5 Steps in Order

The 5 steps are executed sequentially. On any step failure, `analyze()` returns the error.

#### Step 1: Thematic Coverage (ThematicCoverageSkill)

**Trigger**: Always runs; first step  
**Input**: `paper_text`, `extracted_info`  
**Output**: `themes` (list[str]), `keywords` (list[str]), `research_area` (str)  
**Error**: Returns `{"success": False, "error": ..., "step": "thematic_coverage"}`  
**Source**: `extracted_backend_skills_01.md §6`

#### Step 2: Query Generation (QueryGenerationSkill)

**Trigger**: Runs after Step 1  
**Input**: `paper_text`, `thematic_data` (from Step 1; `subtemas` and `areas_tecnicas` extracted from `thematic_data`) (SOURCE: `sota_skills.py:107, 116-121`)  
**Output**: `search_queries` (list[str], 3 queries generated) (SOURCE: `sota_skills.py:129, 148`)  
**Error**: Returns `{'search_queries': []}` on guard failure or LLM error  
**Source**: `extracted_backend_skills_01.md §6`

#### Step 3: Semantic Scholar Search (SemanticScholarSearchSkill)

**Trigger**: Runs after Step 2  
**Input**: `search_queries` (from Step 2)  
**Output**: `sota_papers` (list[dict]), `query_results` (dict)  
**Error**: Returns `{"success": False, "error": ..., "step": "semantic_scholar_search"}`

**Semantic Scholar API details** (from §11 SemanticScholarSearchSkill):
- Endpoint: `https://api.semanticscholar.org/graph/v1/paper/search`
- Auth: None (public)
- Params: `query`, `fields="paperId,title,authors,year,citationCount,abstract,url"`,
  `year="2023-2026"`, `limit=5`
- Per-query results deduplicated by `paperId` across all queries before writing to
  `sota_papers`

**Source**: `extracted_backend_core_01.md §4.3`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_021`

#### Step 4: Coverage Gap Analysis (CoverageGapAnalysisSkill)

**Trigger**: Runs after Step 3  
**Input**: `sota_papers`, `extracted_info`, `paper_text` (optional)  
**Output**: `coverage_gaps` (list[dict]), `sota_comparison_summary` (str)  
**Error**: Returns `{"success": False, "error": ..., "step": "coverage_gap_analysis"}`  
**Source**: `extracted_backend_skills_01.md §6`

#### Step 5: Cross Validation (CrossValidationSkill)

**Trigger**: Runs after Step 4 (final step)  
**Input**: `sota_papers`, `checklist`, `extracted_info`  
**Output**: `cross_validation_results` (list[dict]), `unsupported_claims_count` (int)  
**Error**: Returns `{"success": False, "error": ..., "step": "cross_validation"}`  
**Source**: `extracted_backend_skills_01.md §6`

### 12.4 Return Shape of `analyze()`

**Success:**

```python
{
    "success": True,
    "thematic_data": dict,
    "search_queries": list[str],
    "sota_papers": list[dict],
    "query_results": dict,
    "coverage_gaps": dict,
    "validation_results": dict
}
```

**Failure:**

```python
{
    "success": False,
    "error": str,
    "step": str    # name of the failing step
}
```

Source: `extracted_backend_core_01.md §4.3`

---

<a name="section-13"></a>
## Section 13 — Chatbot (preguntar Flow + History)

Source: `extracted_backend_core_01.md §4.4`, `extracted_backend_skills_01.md §7`

### 13.1 Class: PaperChatbot

```python
class PaperChatbot:
    def __init__(self, llm_client: LLMClient, paper_text: str, extracted_info: dict):
        self.llm_client = llm_client
        self.paper_text = paper_text
        self.extracted_info = extracted_info
        self.conversation_history: list[dict] = []
```

Module: `backend/services/chatbot.py`

### 13.2 `preguntar()` Signature

```python
def preguntar(self, pregunta: str) -> str:
```

Parameters:
- `pregunta` (str): The user's question. Required. No length constraint documented.
- Returns: str — The LLM-generated answer.

### 13.3 Conversation History Data Structure

```python
conversation_history: list[dict]
```

Each element:

| Field | Type | Description |
|---|---|---|
| `role` | str | `"user"` or `"model"` |
| `parts` | list[str] | List with one element: the message text |

Example:

```python
[
    {"role": "user",  "parts": ["What is the learning rate used?"]},
    {"role": "model", "parts": ["The paper uses a learning rate of 0.001."]},
]
```

**Size limit**: [GAP: no maximum history size enforced — history grows unbounded in extraction data]

Source: `extracted_backend_core_01.md §4.4`

### 13.4 History Update Logic

```pseudocode
FUNCTION preguntar(pregunta):
    # Step 1: Append user question to history BEFORE LLM call
    conversation_history.append({
        "role": "user",
        "parts": [pregunta]
    })
    
    # Step 2: Build prompt with full history + paper context
    prompt = build_chat_prompt(
        conversation_history=conversation_history,
        paper_text=self.paper_text,
        extracted_info=self.extracted_info
    )
    
    # Step 3: LLM call
    response = self.llm_client.generate(
        prompt=prompt,
        config=CHAT_CONFIG,        # {"temperature": 0.2}
        history=conversation_history   # passed directly to Gemini chat API
    )
    
    # Step 4: Append model response to history AFTER LLM call
    conversation_history.append({
        "role": "model",
        "parts": [response]
    })
    
    # Step 5: Return the response
    RETURN response
```

Source: `extracted_backend_core_01.md §4.4`

### 13.5 LLM Call Details

- Config: `CHAT_CONFIG = {"temperature": 0.2}` (no JSON, plain text)
- Model: `"gemini-3.1-flash-lite-preview"`
- The Gemini `chat.send_message()` API is used (not one-shot `generate_content()`), passing
  `history` directly so the model receives the full conversation context natively.
- Paper context is injected into the system prompt or initial user turn.

Source: `extracted_backend_core_01.md §4.4`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_022`

### 13.6 Error Handling

| Condition | Behavior |
|---|---|
| LLM call raises exception | `preguntar()` propagates the exception to the caller (no internal try/catch) |
| Empty response from LLM | Returns empty string `""` (history still updated with empty model turn) |

Source: `extracted_backend_core_01.md §4.4`

### 13.7 Usage in `ConversationalResponseSkill`

`ConversationalResponseSkill.execute()` wraps `PaperChatbot.preguntar()` for use inside
the skill pipeline. It reads `question` from context, calls `preguntar(question)`, and writes
the result to `context["answer"]` and `context["updated_history"]`.

Source: `extracted_backend_skills_01.md §7`

---

<a name="section-14"></a>
## Section 14 — PDF Parser (Docling Chunked Flow)

Source: `extracted_backend_core_01.md §4.1`

### 14.1 Function Signature

```python
def convert_pdf_to_markdown(pdf_path: str, chunk_size: int = 5) -> str:
```

Module: `backend/services/pdf_parser.py`

Parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pdf_path` | str | (required) | Absolute or relative path to the PDF file |
| `chunk_size` | int | `5` | Number of pages per processing block |

Returns: `str` — Full markdown text of the document (assembled from all chunks).

### 14.2 Chunked Docling Flow

```pseudocode
FUNCTION convert_pdf_to_markdown(pdf_path, chunk_size=5):
    # Step 1: Determine total page count
    pdf_reader = open_pdf(pdf_path)
    total_pages = pdf_reader.num_pages
    
    markdown_parts = []
    
    # Step 2: Process each chunk of `chunk_size` pages
    FOR start_page FROM 0 TO total_pages STEP chunk_size:
        end_page = min(start_page + chunk_size, total_pages)
        
        # Step 3: Write chunk to temp PDF
        tmp_pdf_path = create_temp_file(suffix=".pdf")
        TRY:
            writer = PdfWriter()
            FOR page_num FROM start_page TO end_page - 1:
                writer.add_page(pdf_reader.pages[page_num])
            writer.write(tmp_pdf_path)
            
            # Step 4: Convert temp PDF with Docling
            converter = DocumentConverter()
            result = converter.convert(tmp_pdf_path)
            chunk_markdown = result.document.export_to_markdown()
            
            markdown_parts.append(chunk_markdown)
        
        EXCEPT Exception AS e:
            # Step 5: On per-chunk error, append error notice (processing continues)
            error_notice = f"\n\n<!-- Error processing pages {start_page+1}–{end_page}: {str(e)} -->\n\n"
            markdown_parts.append(error_notice)
        
        FINALLY:
            # Step 6: Always clean up temp file
            IF tmp_pdf_path exists:
                os.remove(tmp_pdf_path)
    
    # Step 7: Assemble all chunks
    RETURN "\n\n".join(markdown_parts)
```

Source: `extracted_backend_core_01.md §4.1`

### 14.3 Chunk/Fragment Sizing Parameters

| Parameter | Value | Description |
|---|---|---|
| `chunk_size` | `5` (default) | Pages per processing block |
| `chunk_overlap` | `0` | No page overlap between blocks |

### 14.4 Output Format

- Each chunk produces a markdown string from Docling's `export_to_markdown()`.
- Chunks are joined with `"\n\n"` separator.
- No additional metadata is added to the output string.
- If a chunk fails, an HTML comment error notice is inserted at that position in the output.

### 14.5 Error Handling

| Condition | Behavior |
|---|---|
| Single chunk/block fails (Docling error, corrupt pages) | Append HTML error comment; continue with next chunk |
| All chunks fail | Returns string of error comments only (no exception raised) |
| Empty PDF (0 pages) | Returns empty string `""` |
| PDF file not found | Exception from `open_pdf()` propagates to caller |
| Temp file creation fails | Exception propagates to caller |
| Temp file cleanup fails | [GAP: whether cleanup failure is silently swallowed or propagated not confirmed] |

Source: `extracted_backend_core_01.md §4.1`

---

<a name="section-15"></a>
## Section 15 — LLMClient (Retry + Backoff Logic)

Source: `extracted_backend_core_01.md §3.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_009`

### 15.1 Class

```
LLMClient
```

Module: `backend/common/llm_client.py`

### 15.2 Constructor

```python
def __init__(self, model_name=None, generation_config=None):
    # api_key is NOT a constructor parameter; read from GOOGLE_API_KEY env var
    # max_retries (= 5) and base_delay (= 2) are local variables inside generate(), not instance attributes
    self.client = genai.Client(api_key=GOOGLE_API_KEY)
    self.model_name = model_name or MODEL_NAME
    self.generation_config = generation_config or {}
```

Source: `extracted_backend_core_01.md §3.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_009`

### 15.3 `generate()` Signature

```python
def generate(self, prompt):
    # config is NOT a parameter; generation_config is fixed at construction via self.generation_config
    # history is NOT a parameter; no chat API is used in this method
```

Parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | str | (required) | Prompt string sent to `self.client.models.generate_content()` |

Returns: `GenerateContentResponse` — full response object from the genai SDK; callers access `.text` to get the raw string.

### 15.4 Retry Loop (All 6 Attempts)

The retry loop uses `for attempt in range(6)` — attempts are numbered 0 through 5.
`max_retries=5` is the number of **retries** (not total attempts). Total attempts = 6.

#### Delay Formula

```python
delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
# base_delay = 2 (local variable in generate(), not an instance attribute)
```

| Attempt | Sleep AFTER failed attempt (seconds) | Approx delay (without jitter) |
|---|---|---|
| 0 (first) | **0** (no sleep before first attempt) | — |
| 1 (first retry) | `2 * (2**1) + random(0,1)` ≈ **4–5 s** | 4 s |
| 2 | `2 * (2**2) + random(0,1)` ≈ **8–9 s** | 8 s |
| 3 | `2 * (2**3) + random(0,1)` ≈ **16–17 s** | 16 s |
| 4 | `2 * (2**4) + random(0,1)` ≈ **32–33 s** | 32 s |
| 5 (last retry) | `2 * (2**5) + random(0,1)` ≈ **64–65 s** | 64 s |

Note: The sleep occurs at the **start of each iteration** (before the LLM call) using
`if attempt > 0: time.sleep(delay)` — attempt 0 has no preceding sleep.

Source: `extracted_backend_core_01.md §3.1`

### 15.5 Retryable Exception Conditions

An exception is considered retryable if its string representation contains ANY of these
substrings (case-insensitive string match, not exception type match):

| Substring | Meaning |
|---|---|
| `"503"` | HTTP 503 Service Unavailable |
| `"429"` | HTTP 429 Too Many Requests (rate limit) |
| `"UNAVAILABLE"` | gRPC UNAVAILABLE status |
| `"RESOURCE_EXHAUSTED"` | gRPC RESOURCE_EXHAUSTED (quota) |
| `"DEADLINE_EXCEEDED"` | gRPC DEADLINE_EXCEEDED (timeout) |

Source: `extracted_backend_core_01.md §3.1`

### 15.6 Non-Retryable Exceptions

Any exception whose string representation does NOT match any retryable substring is
**immediately re-raised** (no retry, no delay).

```python
if not any(code in str(e) for code in RETRYABLE_CODES):
    raise   # immediately propagate
```

### 15.7 Retry Loop Pseudocode

```pseudocode
RETRYABLE_CODES = ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"]

FUNCTION generate(prompt):
    # config is NOT a parameter; fixed at construction in self.generation_config
    # history is NOT a parameter; no chat API branch
    last_exception = None
    max_retries = 5
    base_delay = 2
    
    FOR attempt IN range(6):   # attempts 0, 1, 2, 3, 4, 5
        TRY:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.generation_config
            )
            
            # Show Streamlit toast (silently swallowed if not in Streamlit context)
            TRY:
                streamlit.toast(f"LLM call succeeded on attempt {attempt+1}")
            EXCEPT:
                PASS
            
            RETURN response
        
        EXCEPT Exception AS e:
            last_exception = e
            error_msg = str(e)
            
            is_retryable = any(code IN error_msg.upper() for code IN RETRYABLE_CODES)
            
            IF attempt < max_retries AND is_retryable:
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                # Show toast in Streamlit if available
                TRY:
                    streamlit.toast(f"⏳ Gemini saturado. Reintento {attempt+1}/{max_retries} en {int(delay)}s...")
                EXCEPT:
                    PASS
                time.sleep(delay)
            ELSE:
                # Non-retryable or exhausted retries
                RAISE e
    
    # All 6 attempts exhausted (should not reach here for retryable errors)
    RAISE last_exception
```

Source: `extracted_backend_core_01.md §3.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_009`

### 15.8 JSON Repair Patterns

Applied after receiving raw LLM text, before JSON parsing (in skills that expect JSON output):

1. **Strip markdown fences**: remove ` ```json ` ... ` ``` ` wrapper if present.
2. **Strip trailing commas**: regex replace `,\s*}` → `}` and `,\s*]` → `]`.
3. **Balanced JSON extraction**: use the brace-stack algorithm (§2.8) to extract the first
   complete `{...}` object.

Note: These repairs are applied in the calling skill's `execute()` method, NOT inside
`LLMClient.generate()`. `generate()` returns the raw string.

Source: `extracted_backend_core_01.md §3.1`, `extracted_backend_skills_01.md §3.2`

### 15.9 Return Type

**Success**: `str` — raw LLM response text (may contain markdown fences, trailing commas, etc.)

**Failure**: raises the last exception after all 6 attempts are exhausted.

---

<a name="section-16"></a>
## Section 16 — Prompt Template Functions (All 6)

Source: `extracted_backend_core_01.md §2.2`

Module: `backend/common/prompts.py`

---

### Function: `get_extraction_prompt()`

#### Signature

```python
def get_extraction_prompt(paper_text: str, red_flags: list[str]) -> str:
```

#### Purpose

Full single-pass extraction prompt. Instructs the LLM to extract 17 information categories
from the complete paper text.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `paper_text` | str | Full paper text block in the prompt |
| `red_flags` | list[str] | Formatted list of red-flag pattern strings |

#### Output (Prompt String Structure)

The prompt instructs the LLM to return a JSON object containing the following 17 top-level categories:

1. `title` — paper title
2. `authors` — list of author names
3. `abstract` — abstract text
4. `contributions` — main claimed contributions
5. `methodology` — description of methodology
6. `experiments` — experimental setup details
7. `results` — key results and metrics
8. `datasets` — datasets used (name, size, source, availability)
9. `code_availability` — code/implementation availability
10. `computational_requirements` — hardware, compute budget, runtime
11. `hyperparameters` — all hyperparameter values (learning rate, batch size, etc.)
12. `statistical_testing` — statistical tests and significance reporting
13. `limitations` — acknowledged limitations
14. `future_work` — stated future work
15. `red_flags_found` — which of the injected `red_flags` were detected
16. `reproducibility_indicators` — binary indicators for reproducibility checklist
17. `additional_notes` — any other relevant extraction

#### Skills Using This Template

- `HybridHyperparameterExtractionSkill` (Phase 1.5, RAG per-chunk pass)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_map_extraction_prompt()`

#### Signature

```python
def get_map_extraction_prompt(fragment_text: str) -> str:
```

#### Purpose

Per-fragment MAP extraction prompt. Used in Phase 1 MAP phase for each paper fragment.
Lighter than the full extraction — focuses on extracting structured information from a
single paper section.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `fragment_text` | str | The text of one paper fragment/section |

#### Output (Prompt String Structure)

- Instructs the LLM to return a JSON object with a subset of the 17 categories
  (limited to what is extractable from a fragment without full-paper context).
- Includes instruction to mark uncertain extractions with a confidence level.

#### Skills Using This Template

- `InformationExtractionSkill` (Phase 1, MAP phase)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_reduce_extraction_prompt()`

#### Signature

```python
def get_reduce_extraction_prompt(map_results: list[dict]) -> str:
```

#### Purpose

REDUCE consolidation prompt. Takes all MAP outputs and instructs the LLM to merge them
into a single canonical extraction, resolving duplicates and conflicts.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `map_results` | list[dict] | JSON-serialized list of all per-fragment MAP outputs |

#### Output (Prompt String Structure)

- Instructs the LLM to return a single JSON object with the full 17-category schema.
- Includes explicit deduplication and conflict-resolution instructions (e.g., prefer
  more specific values over vague ones, merge lists, avoid duplication).

#### Skills Using This Template

- `InformationExtractionSkill` (Phase 1, REDUCE phase)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_evaluation_signals()`

#### Signature

```python
def get_evaluation_signals(extracted_info: dict) -> dict:
```

#### Purpose

**NOT a prompt function.** Computes 6 binary/numeric signals from `extracted_info` using
Python logic only (no LLM call). Returns a `signals` dict.

#### Required Parameters

| Parameter | Type | Description |
|---|---|---|
| `extracted_info` | dict | Phase 1 output (full extraction) |

#### Output: 6 Signal Keys

| Key | Type | Derivation |
|---|---|---|
| `has_code` | bool | `True` if `extracted_info.get("code_availability")` is truthy |
| `has_data` | bool | `True` if `extracted_info.get("datasets")` is non-empty |
| `has_hyperparams` | bool | `True` if `extracted_info.get("hyperparameters")` is non-empty |
| `has_statistics` | bool | `True` if `extracted_info.get("statistical_testing")` is truthy |
| `has_hardware` | bool | `True` if `extracted_info.get("computational_requirements")` is truthy |
| `has_limitations` | bool | `True` if `extracted_info.get("limitations")` is truthy |

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_evaluation_prompt()`

#### Signature

```python
def get_evaluation_prompt(extracted_info: dict, red_flags: list[str]) -> str:
```

#### Purpose

Main NeurIPS 2026 checklist evaluation prompt. Instructs the LLM to evaluate 16 checklist
items based on the full extracted information.

#### Required Parameters Injected into Template

| Parameter | Type | Injected As |
|---|---|---|
| `extracted_info` | dict | JSON-serialized full extraction |
| `red_flags` | list[str] | Formatted list of red-flag pattern strings |

#### Output (Prompt String Structure)

- Defines all 16 NeurIPS 2026 checklist item keys and their descriptions.
- Instructs the LLM to return a JSON object with each item key mapped to
  `{answer: "Yes"|"No"|"N/A", justification: str, evidence: str}`.
- Includes scoring guidelines (what counts as "Yes" vs "No" for each item).

[GAP: the exact 16 checklist item keys and their scoring criteria are embedded in the prompt
template text; they are not separately enumerated in the extraction data outside of the prompt]

#### Skills Using This Template

- `ReproducibilityEvaluationSkill` (Phase 2)

Source: `extracted_backend_core_01.md §2.2`

---

### Function: `get_verification_prompt()`

#### Signature

```python
def get_verification_prompt(
    item_key: str,
    item_data: dict,
    paper_context: str
) -> str:
```

#### Purpose

Second-pass verification prompt. Used in Phase 2.5 to re-evaluate individual checklist
items with focused paper context.

#### Required Parameters Injected into Template

| Parameter | Type | Description |
|---|---|---|
| `item_key` | str | The checklist item key to re-verify (e.g., `"code_released"`) |
| `item_data` | dict | The Phase 2 evaluation for this item: `{answer, justification, evidence}` |
| `paper_context` | str | Truncated paper text: `paper_text[:30000] + paper_text[-30000:]` |

#### Output (Prompt String Structure)

- Presents the current evaluation (`item_data`) and the focused paper context.
- Asks the LLM: "Given this paper context, is the original evaluation correct?"
- Returns JSON: `{revised_answer: str, is_changed: bool, new_justification: str, new_evidence: str}`.

#### Skills Using This Template

- `ChecklistVerificationSkill` (Phase 2.5)

Source: `extracted_backend_core_01.md §2.2`

---

## Appendix A — Configuration Constants

Source: `extracted_backend_core_01.md §2.1`, `cross_ref_resolution_cross_ref_root_to_backend.md §g_010`

Module: `backend/common/config.py`

| Constant | Value | Type | Description |
|---|---|---|---|
| `MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | str | LLM model for all audit calls |
| `EMBEDDING_MODEL` | `"gemini-embedding-2"` | str | Embedding model for RAG |
| `GOOGLE_API_KEY` | (from environment) | str | Google Gemini API key |
| `AUDIT_CONFIG` | `{"response_mime_type": "application/json", "temperature": 0.0, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384}` | dict | Config for all audit LLM calls |
| `CHAT_CONFIG` | `{"temperature": 0.2}` | dict | Config for chatbot LLM calls |
| `SOTA_CONFIG` | `{"response_mime_type": "application/json", "temperature": 0.1}` | dict | Config for SOTA analysis LLM calls |
| `AUDIT_VERSION` | [GAP: version string not enumerated in extraction] | str | Pipeline version tag |

Source: `extracted_backend_core_01.md §2.1`

---

## Appendix B — Dependencies

Source: `extracted_root_tests_scratch_01.md §requirements`

Key Python packages required:

| Package | Purpose |
|---|---|
| `google-generativeai` | Gemini LLM and embedding API |
| `chromadb` | In-memory vector database for RAG |
| `langchain` | `RecursiveCharacterTextSplitter` fallback for fragmentation |
| `docling` | PDF-to-markdown conversion |
| `pypdf` | PDF page-level operations (chunk writing) |
| `requests` | Semantic Scholar HTTP calls |
| `streamlit` | UI framework (toast calls in LLMClient silently swallowed outside Streamlit) |

Missing from `requirements.txt` (noted in extraction):  
`[GAP: reportlab not listed in requirements.txt but referenced in tests]`  
`[GAP: markdown2 not listed in requirements.txt but referenced in scratch scripts]`

Source: `extracted_root_tests_scratch_01.md §requirements`

---

## Appendix C — Unresolved GAPs from Cross-Reference Analysis

Source: `cross_ref_resolution_cross_ref_root_to_backend.md §RESOLUTION SUMMARY`

The following items were identified as UNRESOLVED in the cross-reference analysis:

| GAP ID | Description | Confidence |
|---|---|---|
| g_001 | `PaperAuditor._preprocess_paper()` — method removed during refactoring; no source code | UNRESOLVED |
| g_002 | `REGEX_PATTERNS` in `auditor.py` — removed; now lives as class-level `PATTERNS` per skill | UNRESOLVED |
| g_003 | `AuditState`, `ExtractedInfo`, `ChecklistItem` TypedDicts — `backend/common/audit_state.py` absent from repo | UNRESOLVED |
| g_004 | `NEGATION_PATTERNS` usage in `auditor.py` tests — references removed code | UNRESOLVED |

Full unresolved items verbatim:

`[GAP: _preprocess_paper behavior unresolved — removed during refactoring; no source available]`

`[GAP: AuditState / ExtractedInfo / ChecklistItem — backend/common/audit_state.py not found in repo; these TypedDicts may have been deleted during refactoring]`

`[GAP: NEGATION_PATTERNS used in auditor.py test references — the patterns were moved to per-skill class-level PATTERNS; original auditor.py usage unresolved]`

Source: `cross_ref_resolution_cross_ref_root_to_backend.md §RESOLUTION SUMMARY`

---

## Appendix D — Known Bugs and Risks

Source: `extracted_backend_core_01.md §GAP-cluster_backend_core_01-012`

### Bug D.1: RETRACTED — `NameError` in `PaperAuditor.audit()` outer `except` block does NOT exist

**Location**: `auditor.py:201–204`

**Original claim**: `end_time` would be unbound in the outer `except` block if an exception
occurred before Phase 3 entry (approximately `auditor.py:176`), causing a secondary `NameError`.

**RETRACTION**: Verified against source code. The outer `except Exception as e:` block
(`auditor.py:201–204`) assigns `end_time = time.time()` as its FIRST statement
(`auditor.py:202`), before any reference to `end_time`. Therefore, `end_time` is always
bound when the outer except block executes, regardless of which phase raised the exception.
The return value is `{"error": str(e)}` — no `success` key, no `phase` key.

```python
# auditor.py:201-204 (actual source)
except Exception as e:
    end_time = time.time()   # line 202 — FIRST line; always bound here
    logger.error(f"... {round(end_time - start_time, 2)}s: {str(e)}")
    return {"error": str(e)}
```

**Source**: `auditor.py:201–204` (verified; no NameError risk exists)

---

*End of Functional Backend Specification — `02_functional_backend.md`*
*Generated from extraction files: `extracted_backend_core_01.md`, `extracted_backend_skills_01.md`,*
*`extracted_root_tests_scratch_01.md`, `cross_ref_resolution_cross_ref_root_to_backend.md`*
