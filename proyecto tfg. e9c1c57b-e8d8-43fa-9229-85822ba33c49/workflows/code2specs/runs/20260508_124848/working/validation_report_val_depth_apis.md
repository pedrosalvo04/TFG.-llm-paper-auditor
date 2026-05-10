---
validator_id: val_depth_apis
validator_type: depth
target_specs: [03_technical_specs.md]
forward_coverage_pct: 91
backward_coverage_pct: N/A
depth_pct: 75
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 0
depth_gaps: 7
spec_consistency_issues: 0
total_issues: 9
overall_status: needs_review
---

## Summary

Validated the API call and LLM generation config depth in `03_technical_specs.md` across 6 identified elements: 2 Gemini SDK calls (primary LLMClient path and REDUCE-phase fallback), 1 Semantic Scholar REST API call, and 3 LLM generation config dicts (AUDIT_CONFIG, CHAT_CONFIG, SOTA_CONFIG). The three config objects are well-documented with exact parameter values and are rated FULL. The three API calls are all rated PARTIAL: the primary Gemini SDK call omits the `stream` flag and response type name; the REDUCE fallback omits response schema, error handling, and authentication context; the Semantic Scholar call omits the response item schema and error-handling paths. Additionally, two source line references are incorrect (off by 12 lines for `auditor_skills.py` and 40 lines for `sota_skills.py`). Two critical external integrations — ChromaDB (used by `rag_extraction_skill.py`) and the Gemini embedding API (both via httpx batchEmbedContents and SDK `embed_content`) — are entirely absent from `03_technical_specs.md`, representing significant undocumented surface area. Overall status: **needs_review**.

---

## Depth Validation — API and LLM Call Elements

| Element ID | Spec Section | Type | SDK/Endpoint | Source Reference | Verified? | Depth Score | Missing Fields |
|------------|-------------|------|--------------|-----------------|-----------|-------------|----------------|
| API-001 | §1.1 "Full method call signature used to invoke the API" / §2.2 "generate() Retry Loop" | gemini_sdk | `genai.Client.models.generate_content` (primary, via `LLMClient.generate`) | `llm_client.py:44–48` | YES | PARTIAL | `stream` flag not explicitly documented; response type (`GenerateContentResponse`) not named |
| API-002 | §2.3 "client.models.generate_content Fallback" | gemini_sdk | `genai.Client.models.generate_content` (direct fallback in REDUCE phase) | `auditor_skills.py:113` ❌ (actual: line 125) | FAIL (wrong line) | PARTIAL | Response schema absent; error handling for fallback path not documented; authentication context not stated |
| API-003 | §1.2 "Semantic Scholar API" | semantic_scholar_rest | `GET https://api.semanticscholar.org/graph/v1/paper/search` | `sota_skills.py:162` ❌ (actual: line 202); `config.py:136–139` ✅ | PARTIAL (content correct, line ref wrong) | PARTIAL | Response data-array item schema (field names + types) not documented; error handling (429 sleep-2s, non-200 warning, inter-query sleep-0.5s, timeout exception) absent |
| CFG-001 | §1.1 "AUDIT_CONFIG" | llm_gen_config | `google.genai.Client` (plain dict) | `config.py:116` | YES | FULL | — |
| CFG-002 | §1.1 "CHAT_CONFIG" | llm_gen_config | `google.genai.Client` (plain dict) | `config.py:125` | YES | FULL | — |
| CFG-003 | §1.1 "SOTA_CONFIG" | llm_gen_config | `google.genai.Client` (plain dict) | `config.py:130` | YES | FULL | — |

**Depth calculation:**
- FULL: 3 elements × 1.0 = 3.0
- PARTIAL: 3 elements × 0.5 = 1.5
- Total: 4.5 / 6 × 100 = **75%**

---

## Forward Coverage (Specs → Source)

| Element ID | Source Reference | File Exists? | Lines Support Claim? | Status |
|------------|-----------------|--------------|----------------------|--------|
| API-001 | `llm_client.py:44–48` | YES | YES — `self.client.models.generate_content(model=self.model_name, contents=prompt, config=self.generation_config)` exactly at lines 44–48 | PASS |
| API-001 | `llm_client.py:39` (max_retries=5) | YES | YES — line 39: `max_retries = 5` | PASS |
| API-001 | `llm_client.py:40` (base_delay=2) | YES | YES — line 40: `base_delay = 2` | PASS |
| API-001 | `llm_client.py:42` (loop) | YES | YES — line 42: `for attempt in range(max_retries + 1):` | PASS |
| API-001 | `llm_client.py:35–37` (imports) | YES | YES — lines 35–37: `import time`, `import streamlit as st`, `import random` | PASS |
| API-001 | `llm_client.py:8–28` (constructor) | YES | YES — class definition starts at line 8; constructor logic at lines 19–28 | PASS |
| API-002 | `auditor_skills.py:113` | YES | NO — line 113 is a comment (`# 2. Fase REDUCE (Consolidación)`). The fallback `self.llm_client.client.models.generate_content(...)` is at line 125. Spec code content is correct but line reference is wrong. | FAIL |
| API-003 | `config.py:136` (SEMANTIC_SCHOLAR_BASE_URL) | YES | YES — line 136: `SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"` | PASS |
| API-003 | `config.py:137` (YEAR_RANGE) | YES | YES — line 137: `SEMANTIC_SCHOLAR_YEAR_RANGE = "2023-2026"` | PASS |
| API-003 | `config.py:138` (LIMIT) | YES | YES — line 138: `SEMANTIC_SCHOLAR_LIMIT = 5` | PASS |
| API-003 | `config.py:139` (FIELDS) | YES | YES — line 139: `SEMANTIC_SCHOLAR_FIELDS = "paperId,title,authors,year,citationCount,abstract,url"` | PASS |
| API-003 | `sota_skills.py:162` (requests.get) | YES | NO — line 162 is in the class docstring. The `requests.get(...)` call is at line 202. Content claim is factually correct; line reference is wrong. | FAIL |
| CFG-001 | `config.py:116` (AUDIT_CONFIG) | YES | YES — line 116: `AUDIT_CONFIG = {` with all 5 documented parameters matching source | PASS |
| CFG-002 | `config.py:125` (CHAT_CONFIG) | YES | YES — line 125: `CHAT_CONFIG = {"temperature": CHAT_TEMPERATURE}` — single parameter matches spec | PASS |
| CFG-003 | `config.py:130` (SOTA_CONFIG) | YES | YES — line 130: `SOTA_CONFIG = {"response_mime_type": "application/json", "temperature": SOTA_TEMPERATURE}` — both parameters match spec | PASS |

---

## Fidelity Issues

- **[API-002]** — `§2.3 "client.models.generate_content Fallback"`: Source reference `auditor_skills.py:113` is incorrect. Line 113 contains a comment `# 2. Fase REDUCE (Consolidación)`. The actual fallback `self.llm_client.client.models.generate_content(model=REDUCE_MODEL_NAME, contents=reduce_prompt, config={...})` is at **line 125**. The code content reproduced in the spec is factually accurate; only the cited line number is wrong.

- **[API-003]** — `§1.2 "Semantic Scholar API"`: Source reference `sota_skills.py:162` is incorrect in two places (query params table and HTTP call summary line). Line 162 is inside the `SemanticScholarSearchSkill` docstring. The actual `requests.get(SEMANTIC_SCHOLAR_BASE_URL, params=params, headers=headers, timeout=15)` is at **line 202**. Content claims about query parameters and timeout are factually accurate; only the line number is wrong.

---

## Depth Gaps

### API-001 — Primary Gemini SDK call (`LLMClient.generate`)

- **[API-001 / stream_flag]** — `§1.1 / §2.2`: Missing explicit `stream` flag documentation. The Google genai SDK supports streaming via a `stream=True` parameter. The spec does not state that `stream=False` (or that the parameter is omitted, meaning synchronous mode). A developer implementing against the spec cannot determine whether the call is synchronous or streaming without inspecting the source. (Source code confirms: no streaming — `stream` is not passed; but the spec doesn't say this.)

- **[API-001 / response_type_name]** — `§2.2 generate() Retry Loop`: Missing response type name. Spec states "Google genai response object; caller accesses `.text` or `.candidates[0].content` etc." The word "etc." is insufficiently specific. The return type `google.genai.types.GenerateContentResponse` is not named, and the exact accessor path (`.candidates[0].content.parts[0].text` vs `.text`) is not unambiguously specified for non-JSON modes. This leaves response deserialization underspecified for a developer.

### API-002 — REDUCE fallback call (`InformationExtractionSkill`)

- **[API-002 / response_schema]** — `§2.3`: Missing response schema. The spec documents the call signature but does not state what the response object is, how `.text` is accessed, or what the caller does with the result. The source shows `raw_text = response.text.strip()` immediately after the call, but this is absent from the spec. A developer cannot implement the fallback consumer without knowing the accessor.

- **[API-002 / error_handling]** — `§2.3`: Missing error handling for the fallback path. The spec makes no mention of what happens if this fallback call itself fails (raises an exception). The source code shows the fallback is inside an `except Exception` block — if the fallback also raises, the exception propagates uncaught to the caller. This behavior is not documented.

- **[API-002 / authentication]** — `§2.3`: Missing authentication documentation. The spec documents authentication for the primary call (API-001 via `genai.Client(api_key=GOOGLE_API_KEY)`), but §2.3 does not state that the fallback uses the same `GOOGLE_API_KEY` via the pre-constructed `self.llm_client.client`. Without this, a developer unfamiliar with the codebase might not know how credentials flow to this call.

### API-003 — Semantic Scholar REST API

- **[API-003 / response_schema]** — `§1.2`: Missing response data-array item schema. The spec documents `"data"` as the top-level key to extract from the JSON response, but does not document the structure of each item in the `data` array. The requested fields (`paperId: str`, `title: str`, `authors: list`, `year: int`, `citationCount: int`, `abstract: str`, `url: str`) are named only as query parameters — not as documented response fields with types. A developer cannot write the response parser or downstream consumer without this.

- **[API-003 / error_handling]** — `§1.2`: Missing error handling paths. The spec states only "HTTP call via `requests.get(..., timeout=15)`" with no documentation of: (a) HTTP 429 → `time.sleep(2)` then continue; (b) other non-200 status codes → log warning and continue (no retry); (c) inter-query throttling of `time.sleep(0.5)` between successive queries; (d) `except Exception as e` → log error and continue to next query. All four behaviors are present in `sota_skills.py:215–222` but absent from the spec.

---

## Quality Assessment

### Well-documented elements

The three LLM generation config objects (`AUDIT_CONFIG`, `CHAT_CONFIG`, `SOTA_CONFIG`) are **exemplary**: each parameter is listed with its exact literal value, the config is cross-referenced to its source constant and source line, and the consumer (which service/class uses each config) is explicitly named. A developer can reconstruct all three dicts verbatim from the spec with zero ambiguity.

The `LLMClient` retry loop (§2.2) is also well-documented: 6 total attempts (`range(max_retries+1)`), 5 distinct sleep durations with the exponential backoff formula (`2 * 2^attempt + jitter`), the exact 5 retryable error-code substrings, and the non-retryable immediate-raise path. This is production-grade specification.

### Underspecified elements

**API-001 (primary Gemini call):** The spec omits stating `stream=False` (synchronous call) and does not name the return type `GenerateContentResponse`. These are low-risk omissions because the retry loop context implies synchronous behavior, but they are technically missing from the depth checklist.

**API-002 (REDUCE fallback):** This is the weakest element. A developer reading §2.3 learns only the call signature — they cannot determine what the response contains, how to extract text from it, what to do if the fallback itself fails, or why `GOOGLE_API_KEY` is not re-passed. The fallback is described as if it is a complete standalone specification, but it is missing three of the six required depth fields.

**API-003 (Semantic Scholar):** The response schema gap is the most operationally dangerous omission. The spec lists `fields=paperId,title,authors,year,citationCount,abstract,url` as a query parameter, but never documents those as response fields with types. A developer implementing the response handler would not know `authors` is a `list[dict]` or that `citationCount` can be `None`. The error handling paths (429 sleep, non-200 warning, inter-query 0.5s throttle) are all silently absent.

### Critical undocumented integrations (outside scope but reported for completeness)

Two major external integrations are **entirely absent** from `03_technical_specs.md`:

1. **ChromaDB** (`backend/skills/rag_extraction_skill.py`): The spec mentions ChromaDB only in §6 (the `ANONYMIZED_TELEMETRY` env var). It does not document `chromadb.Client()` (in-memory, no path), `create_collection(name="paper_chunks")` (no metadata dict, no hnsw:space setting, no embedding_function), `collection.add(embeddings=embeddings, documents=chunks, ids=ids)`, or `collection.query(query_embeddings=query_embeddings, n_results=10)` — including the distance metric used (L2 by default with precomputed embeddings), the response structure (`ids`, `distances`, `documents` nested lists), or error handling. A developer cannot implement the RAG pipeline from this spec.

2. **Gemini Embedding API** (`rag_extraction_skill.py`): The spec lists `EMBEDDING_MODEL_NAME = "gemini-embedding-2"` as a constant but does not document: (a) the direct httpx call to `https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL_NAME}:batchEmbedContents?key={api_key}` with a `{"requests": [...]}` body; (b) the batch size of 15 with 15-second inter-batch sleep; (c) the SDK call `self.llm_client.client.models.embed_content(model=EMBEDDING_MODEL_NAME, contents=queries)` used for query embedding; (d) the response schema (`data.embeddings[].values` for the httpx path; `.embeddings[].values` for the SDK path). Both call paths are undocumented.

These omissions mean that `03_technical_specs.md` is sufficient to implement the text-generation and SOTA-search surface of the application, but **not** the RAG hyperparameter extraction pipeline, which is a core feature of the system.
