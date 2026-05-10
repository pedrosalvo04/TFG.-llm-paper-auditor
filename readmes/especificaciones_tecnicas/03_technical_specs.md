# Technical Specifications — 03_technical_specs.md

---

## 1. External API Contracts (Google Gemini, Semantic Scholar)

### 1.1 Google Gemini API

**All 6 model constants** — Source: `backend/common/config.py` [Source: extracted_backend_core_01.md § 2.1]

| Constant | Exact String Value | Purpose | Source File & Line |
|---|---|---|---|
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | RAG embeddings | `config.py:35` |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Triage and Map phase extraction | `config.py:37` |
| `REDUCE_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Orchestration and Consolidation (Reduce phase) | `config.py:39` |
| `EXTRACTION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Initial extraction (General Analysis) | `config.py:41` |
| `EVALUATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Final evaluation (Senior Area Chair) | `config.py:43` |
| `VERIFICATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | Strict verification (Auditor 2) | `config.py:45` |

Note: Lines 48–105 of `config.py` contain a multi-line docstring listing all available Gemini models for reference; not executable code. [Source: extracted_backend_core_01.md § 2.1]

**Generation config dicts associated with model constants:**

`AUDIT_CONFIG` — associated with `EXTRACTION_MODEL_NAME`, `EVALUATION_MODEL_NAME`, `MAP_MODEL_NAME`, `REDUCE_MODEL_NAME`, `VERIFICATION_MODEL_NAME` — [Source: extracted_backend_core_01.md § 2.1, `config.py:116`]:

```python
{
    "response_mime_type": "application/json",
    "temperature": 0.0,       # = AUDIT_TEMPERATURE
    "top_k": 1,
    "top_p": 0.1,
    "max_output_tokens": 16384
}
```

Used by: `PaperAuditor.__init__` for all 5 `LLMClient` instances (`extraction_llm`, `evaluation_llm`, `rag_map_llm`, `rag_reduce_llm`, `verification_llm`). [Source: extracted_backend_core_01.md § 2.1, `config.py:116`]

`CHAT_CONFIG` — associated with the default `MODEL_NAME` (= `EXTRACTION_MODEL_NAME` = `"gemini-3.1-flash-lite-preview"`) — [Source: extracted_backend_core_01.md § 2.1, `config.py:125`]:

```python
{
    "temperature": 0.2        # = CHAT_TEMPERATURE
}
```

Used by: `PaperChatbot.__init__`. [Source: extracted_backend_core_01.md § 2.1, `config.py:125`]

`SOTA_CONFIG` — associated with the default `MODEL_NAME` — [Source: extracted_backend_core_01.md § 2.1, `config.py:130`]:

```python
{
    "response_mime_type": "application/json",
    "temperature": 0.1        # = SOTA_TEMPERATURE
}
```

Used by: `SotaAnalyzer.__init__`. [Source: extracted_backend_core_01.md § 2.1, `config.py:130`]

**Full method call signature used to invoke the API:**

Primary call in `LLMClient.generate` — [Source: extracted_backend_core_01.md § 3.1, `llm_client.py:44–48`]:

```python
self.client.models.generate_content(
    model=self.model_name,
    contents=prompt,
    config=self.generation_config
)
```

Fallback call signature in `InformationExtractionSkill` REDUCE phase — [Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_015, `auditor_skills.py:125`]:

```python
self.llm_client.client.models.generate_content(
    model=REDUCE_MODEL_NAME,
    contents=reduce_prompt,
    config={"response_mime_type": "application/json", "temperature": 0.0}
)
```

---

### 1.2 Semantic Scholar API

[Source: extracted_backend_core_01.md § 2.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_018]

**Base URL (exact string):**

```
https://api.semanticscholar.org/graph/v1/paper/search
```

Constant: `SEMANTIC_SCHOLAR_BASE_URL` — [Source: `config.py:136`]

**Query parameters (exact values):**

| Parameter Name | Value | Source Constant | Source File & Line |
|---|---|---|---|
| `query` | value of each search query string (runtime) | — | `sota_skills.py:202` |
| `year` | `"2023-2026"` | `SEMANTIC_SCHOLAR_YEAR_RANGE` | `config.py:137` |
| `limit` | `5` | `SEMANTIC_SCHOLAR_LIMIT` | `config.py:138` |
| `fields` | `"paperId,title,authors,year,citationCount,abstract,url"` | `SEMANTIC_SCHOLAR_FIELDS` | `config.py:139` |

**Authentication:**

- Header name: `"x-api-key"`
- Value source: `SEMANTIC_SCHOLAR_API_KEY` environment variable (`os.getenv("SEMANTIC_SCHOLAR_API_KEY")`)
- This header is included only when `SEMANTIC_SCHOLAR_API_KEY` is set; the API is still callable (public access, subject to rate limits) without it. [Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_018]

**Full constructed URL pattern:**

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query=<search_query>
  &year=2023-2026
  &limit=5
  &fields=paperId,title,authors,year,citationCount,abstract,url
```

HTTP call via `requests.get(..., timeout=15)`. [Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_018, `sota_skills.py:202`]

**Response structure:**

The JSON response is parsed with `response.json()`. The top-level key `"data"` holds a list of paper objects. [Source: `sota_skills.py:210`]

```python
data = response.json().get("data", [])
```

Each item in `data` contains the fields listed in `SEMANTIC_SCHOLAR_FIELDS`. Confirmed access patterns from source:

| Field | Python Access | Notes | Source |
|---|---|---|---|
| `paperId` | `p['paperId']` or `p.get('paperId')` | Used as dedup dict key; str type | `sota_skills.py:227` |
| `citationCount` | `x.get('citationCount', 0)` | Default 0 when absent; int or None from API | `sota_skills.py:231` |
| `title` | present in item dict | str; requested in FIELDS | `config.py:139` |
| `authors` | present in item dict | list; requested in FIELDS | `config.py:139` |
| `year` | present in item dict | int; requested in FIELDS | `config.py:139` |
| `abstract` | present in item dict | str; requested in FIELDS | `config.py:139` |
| `url` | present in item dict | str; requested in FIELDS | `config.py:139` |

After collecting all results, duplicates are removed by `paperId` and sorted by `citationCount` descending, top 10 returned. [Source: `sota_skills.py:227–232`]

**Error handling:**

| Condition | Behaviour | Source |
|---|---|---|
| Inter-query throttle (between successive queries, `i > 0`) | `time.sleep(0.5)` before constructing params for the next query | `sota_skills.py:190–191` |
| HTTP 200 | `response.json().get("data", [])` appended to results | `sota_skills.py:209–214` |
| HTTP 429 (rate limit) | Log warning `"⚠️ Rate limit alcanzado, esperando..."` then `time.sleep(2)` and continue to next query (no retry for this query) | `sota_skills.py:215–217` |
| Other non-200 status codes | Log warning `f"⚠️ Error {response.status_code} para query: {q}"` and continue to next query (no retry) | `sota_skills.py:218–222` |
| `except Exception as e` (network error, timeout, etc.) | Log error `f"❌ Error en API: {str(e)}"` and continue to next query | `sota_skills.py:223–224` |

---

## 2. LLM Client Configuration and Retry Policy

### 2.1 LLMClient Constructor

[Source: extracted_backend_core_01.md § 3.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_012, `llm_client.py:8–28`]

**Class:** `LLMClient` — `backend/common/llm_client.py:8`

- Parent class: none
- Module-level logger: `logger = get_logger(__name__)` at `llm_client.py:6`
- Supported provider: Google Gemini exclusively via `google.genai.Client`
- Not a singleton; a new instance is created per service

**Signature:**

```python
def __init__(self, model_name=None, generation_config=None)
```

| Parameter | Type | Default | Behaviour |
|---|---|---|---|
| `model_name` | `str \| None` | `None` | If `None`, resolved to `MODEL_NAME` from config (`"gemini-3.1-flash-lite-preview"`) |
| `generation_config` | `dict \| None` | `None` | If `None`, resolved to `{}` |

**Execution sequence:**

1. Checks `if not GOOGLE_API_KEY` (evaluates `True` if `None` or empty string) — `llm_client.py:19`
   - If true: calls `logger.error("ERROR: No se encontró la GOOGLE_API_KEY en el .env")`  — `llm_client.py:20`
   - Then: raises `ValueError("No se encontró la GOOGLE_API_KEY en el .env")` — `llm_client.py:21`
   - Construction aborted; no attributes set
2. Creates `self.client = genai.Client(api_key=GOOGLE_API_KEY)` — `llm_client.py:23`
3. Sets `self.model_name = model_name or MODEL_NAME` — `llm_client.py:25`
4. Sets `self.generation_config = generation_config or {}` — `llm_client.py:26`
5. Logs `logger.info(f"✅ Cliente LLM inicializado: {self.model_name}")` — `llm_client.py:28`

**Return:** `None` (constructor)

**Instance attributes after successful construction:** `self.client` (genai.Client), `self.model_name` (str), `self.generation_config` (dict)

---

### 2.2 generate() Retry Loop

[Source: extracted_backend_core_01.md § 3.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_012, `llm_client.py:30–76`]

**Signature:**

```python
def generate(self, prompt)
```

- Parameter `prompt`: any type accepted by `genai.Client.models.generate_content` (string or structured content)
- **Calling mode: synchronous** — the `stream` parameter is NOT passed to `generate_content`; the SDK defaults to a blocking, non-streaming call. [Source: `llm_client.py:44–48`]
- Return type: response object from `genai.Client.models.generate_content`; callers access the text payload via the `.text` attribute directly (e.g., `raw_text = response.text.strip()`). [Source: `llm_client.py:49`, `auditor_skills.py:121`]
- Inline imports at method entry: `time`, `streamlit as st`, `random` — `llm_client.py:35–37`

**Retry constants:**

| Constant | Value | Source |
|---|---|---|
| `max_retries` | `5` | `llm_client.py:39` |
| `base_delay` | `2` (seconds) | `llm_client.py:40` |

**Loop:**

```python
for attempt in range(max_retries + 1):   # range(6): attempts 0 through 5 = 6 TOTAL ATTEMPTS
```

Source: `llm_client.py:42`

**Per-attempt logic:**

1. Calls `self.client.models.generate_content(model=self.model_name, contents=prompt, config=self.generation_config)` — `llm_client.py:44–48`
2. On success: returns `response` immediately — `llm_client.py:49`

**Exception handling — on any `Exception as e`:**

- Computes `error_msg = str(e)` — `llm_client.py:52`
- Computes `is_retryable = any(code in error_msg.upper() for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"])` — `llm_client.py:54`

**Retryable error codes (matched by substring in uppercased `error_msg`):**

- `"503"`
- `"429"`
- `"UNAVAILABLE"`
- `"RESOURCE_EXHAUSTED"`
- `"DEADLINE_EXCEEDED"`

**If `attempt < max_retries AND is_retryable` (retryable, attempts remaining):**

- Computes delay: `delay = base_delay * (2 ** attempt) + random.uniform(0, 1)` — `llm_client.py:58`
- Sleep durations per attempt (deterministic portion only; add up to 1s of jitter):
  - Attempt 0: `2 * (2 ** 0)` = `2` seconds + jitter → ≈ 2–3 s
  - Attempt 1: `2 * (2 ** 1)` = `4` seconds + jitter → ≈ 4–5 s
  - Attempt 2: `2 * (2 ** 2)` = `8` seconds + jitter → ≈ 8–9 s
  - Attempt 3: `2 * (2 ** 3)` = `16` seconds + jitter → ≈ 16–17 s
  - Attempt 4: `2 * (2 ** 4)` = `32` seconds + jitter → ≈ 32–33 s
- Logs `logger.warning(f"⚠️ Error API Gemini [{self.model_name}]: {error_msg}. Reintento {attempt + 1}/{max_retries} en {delay:.1f}s...")` — `llm_client.py:60`
- Attempts `st.toast(f"⏳ Gemini saturado (Alta demanda). Reintento {attempt + 1}/{max_retries} en {int(delay)}s...", icon="⏳")` inside `try/except Exception: pass` (silently ignored if Streamlit not active) — `llm_client.py:63–66`
- Calls `time.sleep(delay)` — `llm_client.py:69`
- Continues to next attempt

**If `attempt >= max_retries` (all 5 retry attempts exhausted):**

- Logs `logger.error(f"❌ Error crítico tras {max_retries} reintentos: {error_msg}")` — `llm_client.py:73`
- `raise` (re-raises original exception) — `llm_client.py:76`

**If NOT `is_retryable` (non-retryable error on any attempt, regardless of attempt number):**

- Logs `logger.error(f"❌ Error no reintentable detectado: {error_msg}")` — `llm_client.py:75`
- `raise` (re-raises original exception) — `llm_client.py:76`

**Summary:**

- Total possible calls: 6 (1 original + up to 5 retries). [Source: extracted_root_tests_scratch_01.md § RULE-05, `scratch/test_llm_retry.py:55`]
- Total possible `time.sleep` calls: 5 (one per retry). [Source: `scratch/test_llm_retry.py:55`]
- Non-retryable errors: immediately re-raised on first occurrence, no sleep.

---

### 2.3 client.models.generate_content Fallback

[Source: cross_ref_resolution_cross_ref_root_to_backend.md § g_015, `auditor_skills.py:125`]

Used by `InformationExtractionSkill` REDUCE phase when primary call fails. Full fallback signature:

```python
self.llm_client.client.models.generate_content(
    model=REDUCE_MODEL_NAME,
    contents=reduce_prompt,
    config={"response_mime_type": "application/json", "temperature": 0.0}
)
```

Where `REDUCE_MODEL_NAME = "gemini-3.1-flash-lite-preview"` [Source: `config.py:39`].

**Response accessor:**

Immediately after the fallback call, the caller extracts text via:

```python
raw_text = response.text.strip()
```

Source: `auditor_skills.py:130`. The `.text` attribute is the sole accessor used; no other fields are read from the response object in this path.

**Authentication:**

`self.llm_client.client` is the `genai.Client(api_key=GOOGLE_API_KEY)` instance constructed in `LLMClient.__init__` [Source: `llm_client.py:23`]. The fallback call reuses this pre-constructed client and therefore authenticates via the same `GOOGLE_API_KEY` environment variable — no separate credential configuration is applied at the fallback call site. [Source: `auditor_skills.py:125`, `llm_client.py:23`]

**Error handling:**

The fallback call is inside the `except Exception` handler for the primary `self.llm_client.generate(reduce_prompt)` call [Source: `auditor_skills.py:122–130`]. There is no additional `try/except` wrapping the fallback call itself: if `self.llm_client.client.models.generate_content(...)` raises, the exception propagates uncaught to the caller of `InformationExtractionSkill.execute`. [Source: `auditor_skills.py:118–130`]

---

## 3. Configuration Parameters (all constants with values)

[Source: extracted_backend_core_01.md § 2.1, `backend/common/config.py`]

| Constant / Key | Value | Type | Source (env var or hardcoded) | Description | Source File & Section |
|---|---|---|---|---|---|
| `GOOGLE_API_KEY` | — (no default) | `str \| None` | Env var `"GOOGLE_API_KEY"` | Google Gemini API key; `None` if not set | `config.py:30` |
| `SEMANTIC_SCHOLAR_API_KEY` | — (no default) | `str \| None` | Env var `"SEMANTIC_SCHOLAR_API_KEY"` | Semantic Scholar API key; `None` if not set | `config.py:31` |
| `EMBEDDING_MODEL_NAME` | `"gemini-embedding-2"` | `str` | Hardcoded | RAG embeddings model | `config.py:35` |
| `MAP_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Triage and Map phase extraction model | `config.py:37` |
| `REDUCE_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Reduce phase / consolidation model | `config.py:39` |
| `EXTRACTION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Initial extraction model | `config.py:41` |
| `EVALUATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Final evaluation model | `config.py:43` |
| `VERIFICATION_MODEL_NAME` | `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded | Strict verification model (Auditor 2) | `config.py:45` |
| `MODEL_NAME` | `= EXTRACTION_MODEL_NAME` → `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded (alias assignment) | Default model for `LLMClient`; NOT env-overridable | `config.py:107` |
| `RAG_MODEL_NAME` | `= MAP_MODEL_NAME` → `"gemini-3.1-flash-lite-preview"` | `str` | Hardcoded (alias assignment) | Default model for RAG | `config.py:108` |
| `AUDIT_TEMPERATURE` | `0.0` | `float` | Hardcoded | Temperature for `AUDIT_CONFIG` | `config.py:111` |
| `CHAT_TEMPERATURE` | `0.2` | `float` | Hardcoded | Temperature for `CHAT_CONFIG` | `config.py:112` |
| `SOTA_TEMPERATURE` | `0.1` | `float` | Hardcoded | Temperature for `SOTA_CONFIG` | `config.py:113` |
| `AUDIT_CONFIG` | See § 1.1 | `dict` | Hardcoded | generation_config for all audit LLM calls | `config.py:116` |
| `CHAT_CONFIG` | See § 1.1 | `dict` | Hardcoded | generation_config for chatbot LLM calls | `config.py:125` |
| `SOTA_CONFIG` | See § 1.1 | `dict` | Hardcoded | generation_config for SOTA analysis LLM calls | `config.py:130` |
| `SEMANTIC_SCHOLAR_BASE_URL` | `"https://api.semanticscholar.org/graph/v1/paper/search"` | `str` | Hardcoded | Semantic Scholar API endpoint | `config.py:136` |
| `SEMANTIC_SCHOLAR_YEAR_RANGE` | `"2023-2026"` | `str` | Hardcoded | Year filter for Semantic Scholar queries | `config.py:137` |
| `SEMANTIC_SCHOLAR_LIMIT` | `5` | `int` | Hardcoded | Max results per Semantic Scholar query | `config.py:138` |
| `SEMANTIC_SCHOLAR_FIELDS` | `"paperId,title,authors,year,citationCount,abstract,url"` | `str` | Hardcoded | Fields requested from Semantic Scholar API | `config.py:139` |
| `max_retries` (inline, `LLMClient.generate`) | `5` | `int` | Hardcoded (local var) | Maximum retry attempts (loop is `range(6)`) | `llm_client.py:39` |
| `base_delay` (inline, `LLMClient.generate`) | `2` (seconds) | `int` | Hardcoded (local var) | Base delay for exponential backoff | `llm_client.py:40` |
| `chunk_size` (inline, `pdf_parser.py`) | `5` (pages per block) | `int` | Hardcoded (local var) | Pages per Docling processing chunk | `pdf_parser.py:51` |

---

## 4. Dependency Declarations and Missing Dependencies

### 4.1 Declared Dependencies (requirements.txt)

[Source: extracted_root_tests_scratch_01.md § 2, `requirements.txt:1–13`]

All packages are installed at latest available version.

| Package | Version Specifier | Role | Source |
|---|---|---|---|
| `docling` | (none — latest) | Local (free) PDF-to-Markdown conversion for file ingestion in the backend | `requirements.txt:1` |
| `google-generativeai` | (none — latest) | Google Gemini API client for LLM calls (extraction, evaluation) and embedding API | `requirements.txt:2` |
| `python-dotenv` | (none — latest) | Loads `GOOGLE_API_KEY` and other secrets from `.env` file | `requirements.txt:3` |
| `streamlit` | (none — latest) | Web UI framework for the main application (`app.py`) | `requirements.txt:4` |
| `pydantic` | (none — latest) | Structured/validated LLM response parsing | `requirements.txt:5` |
| `reportlab` | (none — latest) | PDF generation support | `requirements.txt:6` |
| `chromadb` | (none — latest) | Vector database for RAG operations | `requirements.txt:7` |
| `httpx` | (none — latest) | Async HTTP calls for embedding API | `requirements.txt:8` |
| `pypdf` | (none — latest) | PDF page operations and chunking | `requirements.txt:9` |
| `requests` | (none — latest) | HTTP client for Semantic Scholar API | `requirements.txt:10` |
| `torch` | (none — latest) | GPU detection for Docling | `requirements.txt:11` |
| `pymupdf4llm` | (none — latest) | Alternative PDF conversion mechanism | `requirements.txt:12` |
| `langchain-text-splitters` | (none — latest) | Text segmentation utilities | `requirements.txt:13` |

---

### 4.2 Undeclared / Missing Dependencies

[Source: extracted_root_tests_scratch_01.md § 2, cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY]

#### markdown2 — GAP-026

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
SOURCE: md_to_pdf.py:15–17, requirements.txt:1–13 (absence confirmed)
```

---

## 5. Logging Infrastructure

### 5.1 get_logger Function

[Source: extracted_backend_core_01.md § 6.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_019, `backend/utils/logger.py:44`]

**Signature:**

```python
def get_logger(name)
```

Note: The source function has **no type annotations** on either the parameter or the return value. SOURCE: `backend/utils/logger.py:44` — actual source line reads `def get_logger(name):` with no type hints.

**Parameters:**

- `name` (no annotation): Logger name; callers pass `__name__` (module name) — `logger.py:44`

**Return type:** `logging.Logger` (unannotated — inferred from `return logger` at `logger.py:58`)

**Behaviour (execution sequence):**

1. Calls `logging.getLogger(name)` → `logger` — `logger.py:45`
2. Sets `logger.propagate = False` (prevents duplication with root logger) — `logger.py:47`
3. Guard: `if not logger.handlers:` — `logger.py:49` (prevents adding duplicate handlers on repeated calls)
   - Creates `logging.StreamHandler(sys.stdout)` — `logger.py:49–50`; output directed to **stdout**
   - Creates `ColoredFormatter` instance with format string `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` and date format `'%H:%M:%S'` — `logger.py:19, 41`
   - Attaches formatter to handler; adds handler to logger
   - Sets `logger.setLevel(logging.INFO)` — `logger.py:53`
4. Side effects (always executed, regardless of handler guard):
   - `logging.getLogger("google_genai").setLevel(logging.WARNING)` — `logger.py:56`
   - `logging.getLogger("httpx").setLevel(logging.INFO)` — `logger.py:57`
5. Returns `logger`

**Available logger methods (standard `logging.Logger`):** `.info(msg)`, `.debug(msg)`, `.warning(msg)`, `.error(msg)`, `.critical(msg)`

**Log format:** `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` with date format `'%H:%M:%S'` — `logger.py:19, 41`

**No log rotation configured.**

---

### 5.2 ColoredFormatter Class

[Source: extracted_backend_core_01.md § 6.1, cross_ref_resolution_cross_ref_root_to_backend.md § g_019, `backend/utils/logger.py`]

**Class definition:**

```python
class ColoredFormatter(logging.Formatter):
    ...
```

Inherits from `logging.Formatter`. [Source: `logger.py`]

**Constructor parameters:** None specified (uses inherited `logging.Formatter.__init__`). The formatter is instantiated as `ColoredFormatter()` without arguments.

**`format(self, record)` method behaviour** — [Source: `logger.py:29`]:

1. Checks `if "HTTP Request" in record.msg`:
   - If true: sets `color = Colors.CYAN`; mutates `record.msg = f"{Colors.CYAN}{record.msg}{Colors.RESET}"` — `logger.py:33–35`
   - Colors the entire message body in cyan
2. Else:
   - Reads `color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)` — `logger.py:37`
   - Mutates `record.levelname = f"{color}{record.levelname}{Colors.RESET}"` — `logger.py:39`
   - Colors the level name prefix
3. Creates a new `logging.Formatter(log_fmt, datefmt='%H:%M:%S')` on every call (no caching) — `logger.py:41`
4. Returns `formatter.format(record)` — `logger.py:42`

**`LEVEL_COLORS` mapping (class-level dict):**

| Level | Color constant used | Source |
|---|---|---|
| `logging.DEBUG` | `Colors.BLUE` (`"\033[94m"`) | `logger.py:22` |
| `logging.INFO` | `Colors.GREEN` (`"\033[92m"`) | `logger.py:23` |
| `logging.WARNING` | `Colors.YELLOW` (`"\033[93m"`) | `logger.py:24` |
| `logging.ERROR` | `Colors.RED` (`"\033[91m"`) | `logger.py:25` |
| `logging.CRITICAL` | `Colors.BOLD + Colors.RED` (`"\033[1m" + "\033[91m"`) | `logger.py:26` |

---

### 5.3 Colors Class

[Source: extracted_backend_core_01.md § 2.3, `backend/utils/logger.py:7–14`]

```python
class Colors:
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"
```

| Attribute | Value (ANSI escape code) | Source |
|---|---|---|
| `Colors.BLUE` | `"\033[94m"` | `logger.py:7` |
| `Colors.CYAN` | `"\033[96m"` | `logger.py:8` |
| `Colors.GREEN` | `"\033[92m"` | `logger.py:9` |
| `Colors.YELLOW` | `"\033[93m"` | `logger.py:10` |
| `Colors.RED` | `"\033[91m"` | `logger.py:11` |
| `Colors.MAGENTA` | `"\033[95m"` | `logger.py:12` |
| `Colors.BOLD` | `"\033[1m"` | `logger.py:13` |
| `Colors.RESET` | `"\033[0m"` | `logger.py:14` |

---

### 5.4 CleanNetworkLogs Filter

[Source: extracted_backend_core_01.md § 2.1, `config.py:14–20`]

**Class definition:**

```python
class CleanNetworkLogs(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "huggingface.co" in msg and ("HEAD" in msg or "GET" in msg):
            return False
        return True
```

**Filter algorithm — precise description:**

- Inherits `logging.Filter`
- `filter(self, record)` method:
  1. Calls `record.getMessage()` → assigns result to `msg`
  2. Checks compound condition: `"huggingface.co" in msg` AND (`"HEAD" in msg` OR `"GET" in msg`)
     - If **true**: returns `False` — the log record is **suppressed** (filtered out)
     - If **false**: returns `True` — the log record **passes** (is emitted)
- **Exact URL pattern matched:** the literal substring `"huggingface.co"` must be present in the message
- **Exact HTTP methods matched:** literal substrings `"HEAD"` or `"GET"` must be present in the message
- All matching is **case-sensitive** (no `re.IGNORECASE` — plain `in` operator on strings)
- **Effect:** Suppresses logging of HuggingFace HEAD and GET HTTP request log lines emitted by the `httpx` library when models are loaded or checked
- **Applied to:** `logging.getLogger("httpx")` via `.addFilter(CleanNetworkLogs())` at `config.py:22`

[Source: extracted_backend_core_01.md § 2.1, `config.py:14–22`]

---

## 6. Environment Variable Schema

[Source: extracted_backend_core_01.md § 2.1, § 5; extracted_root_tests_scratch_01.md § 3.1]

| Variable Name | Required / Optional | Loaded Via | Default | Used By | Source |
|---|---|---|---|---|---|
| `GOOGLE_API_KEY` | Required (for any LLM operation) | `load_dotenv()` in `config.py:27`; `os.getenv("GOOGLE_API_KEY")` at `config.py:30` | `None` (raises `ValueError` in `LLMClient.__init__` if not set) | `LLMClient.__init__`, all LLM-dependent services | `config.py:30` |
| `SEMANTIC_SCHOLAR_API_KEY` | Optional | `load_dotenv()` in `config.py:27`; `os.getenv("SEMANTIC_SCHOLAR_API_KEY")` at `config.py:31` | `None` (API still accessible without it, subject to rate limits) | `SemanticScholarSearchSkill.execute` (sent as `"x-api-key"` header) | `config.py:31` |
| `TRANSFORMERS_VERBOSITY` | N/A (set by code, not read) | Set by `config.py:8` and `app.py:13` at module import | `"error"` (hardcoded, overrides any preexisting value) | Suppresses `transformers` library logs | `config.py:8`, `app.py:13` |
| `TOKENIZERS_PARALLELISM` | N/A (set by code, not read) | Set by `config.py:9` and `app.py:14` at module import | `"false"` (hardcoded) | Suppresses tokenizer parallelism warnings | `config.py:9`, `app.py:14` |
| `ANONYMIZED_TELEMETRY` | N/A (set by code, not read) | Set by `app.py:21` at module import | `"False"` (hardcoded) | Disables ChromaDB telemetry | `app.py:21` |
| `OTEL_SDK_DISABLED` | N/A (set by code, not read) | Set by `app.py:22` at module import | `"true"` (hardcoded) | Disables OpenTelemetry SDK (avoids Streamlit conflicts) | `app.py:22` |

**How `.env` loading works:**

- `python-dotenv` is used via `load_dotenv()`.
- `load_dotenv()` is called at module level in `backend/common/config.py:27` (before reading `GOOGLE_API_KEY` and `SEMANTIC_SCHOLAR_API_KEY`).
- `load_dotenv()` is also called at module level in `list_models.py:5`.
- All modules that import from `backend.common.config` (or `backend.common.llm_client`) trigger this `load_dotenv()` call at import time. [Source: extracted_backend_core_01.md § 2.1, `config.py:27`]

---

## 7. Module-Level Side Effects

[Source: extracted_backend_core_01.md § 2.1, extracted_root_tests_scratch_01.md § 3.1]

The following side effects occur at module import time:

### `backend/common/config.py`

| Side Effect | Exact Mechanism | Source |
|---|---|---|
| Sets `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` | `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` (direct dict assignment) | `config.py:8` |
| Sets `os.environ["TOKENIZERS_PARALLELISM"] = "false"` | `os.environ["TOKENIZERS_PARALLELISM"] = "false"` (direct dict assignment) | `config.py:9` |
| Suppresses all Python warnings | `warnings.filterwarnings("ignore")` | `config.py:10` |
| Sets `transformers` logger level to ERROR | `logging.getLogger("transformers").setLevel(logging.ERROR)` | `config.py:11` |
| Loads `.env` file into environment | `load_dotenv()` (from `python-dotenv`) | `config.py:27` |
| Applies `CleanNetworkLogs` filter to `httpx` logger | `logging.getLogger("httpx").addFilter(CleanNetworkLogs())` | `config.py:22` |
| Sets `RapidOCR` logger level to WARNING | `logging.getLogger("RapidOCR").setLevel(logging.WARNING)` | `config.py:23` |
| Sets `docling` logger level to WARNING | `logging.getLogger("docling").setLevel(logging.WARNING)` | `config.py:24` |
| Sets `onnxruntime` logger level to ERROR | `logging.getLogger("onnxruntime").setLevel(logging.ERROR)` | `config.py:25` |

### `app.py`

| Side Effect | Exact Mechanism | Source |
|---|---|---|
| Sets `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` | `os.environ["TRANSFORMERS_VERBOSITY"] = "error"` | `app.py:13` |
| Sets `os.environ["TOKENIZERS_PARALLELISM"] = "false"` | `os.environ["TOKENIZERS_PARALLELISM"] = "false"` | `app.py:14` |
| Suppresses `__path__` access warnings | `warnings.filterwarnings("ignore", message=".*Accessing.*__path__.*")` | `app.py:15` |
| Suppresses all `FutureWarning` | `warnings.filterwarnings("ignore", category=FutureWarning)` | `app.py:16` |
| Suppresses all `UserWarning` | `warnings.filterwarnings("ignore", category=UserWarning)` | `app.py:17` |
| Sets `transformers` logger level to ERROR | `logging.getLogger("transformers").setLevel(logging.ERROR)` | `app.py:18` |
| Sets `os.environ["ANONYMIZED_TELEMETRY"] = "False"` | `os.environ["ANONYMIZED_TELEMETRY"] = "False"` | `app.py:21` |
| Sets `os.environ["OTEL_SDK_DISABLED"] = "true"` | `os.environ["OTEL_SDK_DISABLED"] = "true"` | `app.py:22` |

Note: `TRANSFORMERS_VERBOSITY` and `TOKENIZERS_PARALLELISM` are set in **both** `config.py` and `app.py`. Because `config.py` is imported before `app.py` sets its own values, the final values are the same. The duplication ensures the suppression applies even if `config.py` is not imported first. [Source: extracted_root_tests_scratch_01.md § 3.1]

---

## 8. PDF Conversion Technical Details

### 8.1 Docling-Based PDF Conversion Pipeline (`backend/services/pdf_parser.py`)

[Source: extracted_backend_core_01.md § 4.1, `backend/services/pdf_parser.py`]

**Entry point function:**

```python
def convert_pdf_to_markdown(pdf_path) -> str
```

- Parameter `pdf_path`: path to PDF file (str or path-like)
- Return type: `str` — full Markdown text of the PDF; or error string starting with `"❌ Error en la extracción del PDF: "` on outer exception
- Library used: `docling.document_converter.DocumentConverter`

**Chunked processing approach:**

- Chunk size: `chunk_size = 5` pages per processing block — `pdf_parser.py:51`
- No overlap between chunks
- Iteration pattern: `for i in range(0, total_pages, chunk_size)` — `pdf_parser.py:53`

**Full call chain (input PDF → Markdown output):**

**Step 0 — Lazy imports at function entry** (`pdf_parser.py:20–25`):

```python
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from pypdf import PdfReader
from pypdf import PdfWriter
import os
import tempfile
```

**Step 1 — Configure Docling pipeline** (`pdf_parser.py:28–43`):

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False              # OCR disabled for speed
pipeline_options.do_table_structure = True   # table detection enabled
```

GPU detection (informational only — Docling auto-detects via torch):

```python
import torch
if torch.cuda.is_available():
    logger.info("🚀 GPU detectada. Docling usará aceleración CUDA automáticamente.")
else:
    logger.info("ℹ️ No se detectó GPU compatible. Usando CPU para Docling.")
```

```python
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
```

**Step 2 — Read PDF metadata** (`pdf_parser.py:46–50`):

```python
reader = PdfReader(pdf_path)
total_pages = len(reader.pages)
full_md_text = ""
```

**Step 3 — Chunked conversion loop** (`pdf_parser.py:53–79`):

Per chunk iteration:

```python
start_page = i
end_page = min(i + chunk_size, total_pages)   # chunk_size = 5

writer = PdfWriter()
for page_num in range(start_page, end_page):
    writer.add_page(reader.pages[page_num])

with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    tmp_path = tmp_file.name
    writer.write(tmp_path)

try:
    result = converter.convert(tmp_path)
    block_md = result.document.export_to_markdown()
    full_md_text += block_md + "\n\n"
except Exception as block_error:
    # error text appended, processing continues to next block
    full_md_text += f"\n\n> [!ERROR] Error al procesar páginas {start_page+1}-{end_page}: {str(block_error)}\n\n"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)    # temp file always cleaned up
```

**Step 4 — Return result** (`pdf_parser.py:82`):

```python
return full_md_text
```

**Intermediate formats:**

1. PDF file (original)
2. Per-chunk temporary PDF files (written to `tempfile.NamedTemporaryFile`, suffix `.pdf`; deleted in `finally`)
3. Docling `ConversionResult` object (`result`)
4. Markdown string per chunk (`block_md` = `result.document.export_to_markdown()`)
5. Concatenated full Markdown string (`full_md_text`)

**Configuration passed to Docling:**

- `PdfPipelineOptions.do_ocr = False` — OCR disabled
- `PdfPipelineOptions.do_table_structure = True` — table detection enabled
- GPU acceleration: Docling auto-detects via `torch`; no explicit CUDA config passed

**Error handling:**

| Error scenario | Handling |
|---|---|
| Per-block conversion error | Caught (`Exception as block_error`); error text appended to `full_md_text`; processing continues to next block; temp file cleaned in `finally` |
| Empty PDF (`total_pages = 0`) | Loop does not execute; returns empty string `""` |
| Corrupted/unreadable PDF (`PdfReader` raises) | Caught by outer `except Exception as e`; returns `f"❌ Error en la extracción del PDF: {str(e)}"` |
| Password-protected PDF (`PdfReader` raises) | Same as corrupted PDF — outer handler; returns error string |
| Temp file always cleaned | `finally` block: `if os.path.exists(tmp_path): os.remove(tmp_path)` |

**Outer exception handler** (`pdf_parser.py:83–85`):

```python
except Exception as e:
    logger.error(f"❌ Error en la extracción del PDF: {str(e)}")
    return f"❌ Error en la extracción del PDF: {str(e)}"
```

---

### 8.2 pymupdf4llm Alternative Path (`pdf_to_md.py`)

[Source: extracted_root_tests_scratch_01.md § 4.2, `pdf_to_md.py:41`]

**Entry point function:**

```python
def convert_pdf_to_md(pdf_path, output_path=None) -> str | None
```

- This is a **separate CLI utility** (`pdf_to_md.py`), not the backend's primary PDF conversion pipeline (which uses Docling in `pdf_parser.py`).

**Call signature:**

```python
md_text = pymupdf4llm.to_markdown(pdf_path)
```

Source: `pdf_to_md.py:41`

- Input: `pdf_path` (str) — path to PDF file
- Output: `md_text` (str) — Markdown text of the entire PDF (single call, no chunking)
- No chunking, no intermediate formats, no configuration parameters passed
- Result written verbatim to `output_path` with `open(output_path, 'w', encoding='utf-8')` — `pdf_to_md.py:44–45`

**Output statistics printed:**

```python
os.path.getsize(output_path)   # bytes written
len(md_text)                   # characters
md_text.count('\n')            # lines
```

Source: `pdf_to_md.py:48–57`

**Error handling:**

```python
except Exception as e:
    print(f"❌ Error durante la conversión: {str(e)}")
    return None
```

Source: `pdf_to_md.py:61–63` — no traceback printed; no re-raise; caller receives `None`.

**Validation rules (abort and return `None` before calling pymupdf4llm):**

1. `not os.path.exists(pdf_path)` → print error, return `None` — `pdf_to_md.py:23–25`
2. `not pdf_path.lower().endswith('.pdf')` → print error, return `None` — `pdf_to_md.py:28–30`

**Default output path derivation (if `output_path is None`):**

```python
output_path = pdf_path.replace('.pdf', '.md')
```

Source: `pdf_to_md.py:33–34`

---

## 9. ChromaDB Integration and Gemini Embedding Pipeline (`backend/skills/rag_extraction_skill.py`)

[Source: `backend/skills/rag_extraction_skill.py` — 317 LOC; only location in the codebase where vector embeddings are stored, retrieved, and queried]

This section documents the complete RAG embedding and vector search pipeline implemented in `HybridHyperparameterExtractionSkill.execute()`.

---

### 9.1 batchEmbedContents REST Embedding Pipeline (document chunks)

[Source: `rag_extraction_skill.py:54–81`]

**Rationale for bypassing the SDK (source comment at line 71):**

> "Bypasseamos el SDK usando httpx directo porque 'embed_content' fusionaba la lista en un único vector"

The SDK's `embed_content` call fuses the entire batch into a single vector. Direct REST via `httpx` is used to preserve per-chunk individual vectors.

**Embedding batch size constant:**

| Constant | Value | Type | Source |
|---|---|---|---|
| `batch_size` | `15` (chunks per REST request) | `int` (hardcoded local var) | `rag_extraction_skill.py:61` |

**Throttling rationale (source comment at line 61):**

> "Reducido a 15 para apuntar a 60 RPM (margen muy seguro frente al límite de 100)"

**REST endpoint URL:**

```
POST https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL_NAME}:batchEmbedContents?key={api_key}
```

- `{EMBEDDING_MODEL_NAME}` = `"gemini-embedding-2"` (from `config.py:35`)
- `{api_key}` = runtime value of `os.getenv("GOOGLE_API_KEY")` — `rag_extraction_skill.py:62–63`

SOURCE: `rag_extraction_skill.py:63`

**HTTP call:**

```python
response = httpx.post(url, json={"requests": requests})
```

SOURCE: `rag_extraction_skill.py:74`

**Request body structure (per batch):**

```python
requests = [
    {
        "model": f"models/{EMBEDDING_MODEL_NAME}",   # e.g. "models/gemini-embedding-2"
        "content": {
            "parts": [{"text": c}]
        }
    }
    for c in batch   # batch = chunks[i : i + batch_size]
]
```

SOURCE: `rag_extraction_skill.py:72`

**Inter-batch throttle:**

```python
if i > 0:
    time.sleep(15)   # 15 chunks / 15s = 60 requests/min, 60% of 100 RPM limit
```

SOURCE: `rag_extraction_skill.py:66–67`

**Response parsing:**

```python
data = response.json()
for emb in data.get("embeddings", []):
    embeddings.append(emb["values"])
```

SOURCE: `rag_extraction_skill.py:79–81`

**Error handling:**

```python
if response.status_code != 200:
    self.log_execution(f"❌ Error en API Embeddings: {response.text}", level="error")
    raise Exception(f"Error embeddings API: {response.text}")
```

SOURCE: `rag_extraction_skill.py:75–77`

- Non-200 responses raise `Exception`, propagating to the outer `try/except` in `execute()`.
- No partial-batch retry logic; the entire `execute()` method is aborted.

---

### 9.2 ChromaDB In-Memory Collection Management

[Source: `rag_extraction_skill.py:85–97`]

**Client type:**

```python
chroma_client = chromadb.Client()
```

SOURCE: `rag_extraction_skill.py:85`

- Uses the in-memory `chromadb.Client()` (no persistence path configured; data is lost when the process exits or the method returns).

**Idempotent reset before each run:**

```python
try:
    chroma_client.delete_collection("paper_chunks")
except:
    pass
```

SOURCE: `rag_extraction_skill.py:86–89`

- Deletes the collection if it already exists (e.g., from a prior call in the same process); silently swallows any exception (e.g., collection not found).

**Collection creation:**

```python
collection = chroma_client.create_collection(name="paper_chunks")
```

SOURCE: `rag_extraction_skill.py:90`

- Collection name: `"paper_chunks"` (hardcoded).
- No embedding function parameter is passed; embeddings are pre-computed externally and passed explicitly to `collection.add()`.

**Inserting document embeddings:**

```python
ids = [str(i) for i in range(len(chunks))]
collection.add(
    embeddings=embeddings,
    documents=chunks,
    ids=ids
)
```

SOURCE: `rag_extraction_skill.py:92–97`

- `embeddings`: list of float vectors, one per chunk, generated by the batchEmbedContents pipeline (§ 9.1).
- `documents`: list of text strings (the raw chunk text).
- `ids`: list of stringified integer indices (e.g., `["0", "1", "2", ...]`).

---

### 9.3 Gemini SDK `embed_content` for Query Embeddings

[Source: `rag_extraction_skill.py:115–119`]

Query embeddings are generated via the SDK (not REST), using the same `EMBEDDING_MODEL_NAME`:

```python
q_emb_res = self.llm_client.client.models.embed_content(
    model=EMBEDDING_MODEL_NAME,
    contents=queries
)
query_embeddings = [e.values for e in q_emb_res.embeddings]
```

SOURCE: `rag_extraction_skill.py:115–119`

- `queries`: list of 13 hardcoded natural language query strings (e.g., `"training details optimization hyperparameters"`, `"learning rate schedule step size warmup decay learning rate"`, etc.) — `rag_extraction_skill.py:99–113`.
- `q_emb_res.embeddings`: list of embedding objects; each has a `.values` attribute (list of floats).
- Uses SDK path (not REST) because the SDK call here returns one vector per query string correctly.

---

### 9.4 ChromaDB Vector Query and Result Deduplication

[Source: `rag_extraction_skill.py:121–138`]

**Query call:**

```python
results = collection.query(
    query_embeddings=query_embeddings,
    n_results=10
)
```

SOURCE: `rag_extraction_skill.py:121–124`

- `query_embeddings`: list of float vectors (one per query string, from § 9.3).
- `n_results=10`: returns up to 10 nearest neighbours per query.
- Return structure: `results['documents']` (list of lists of chunk text), `results['distances']` (list of lists of float distances).

**Deduplication using distances (keep best/lowest distance per chunk):**

```python
chunk_relevance = {}
for i in range(len(results['documents'])):
    docs = results['documents'][i]
    dists = results['distances'][i]
    for doc, dist in zip(docs, dists):
        if doc not in chunk_relevance or dist < chunk_relevance[doc]:
            chunk_relevance[doc] = dist

sorted_chunks = sorted(chunk_relevance.items(), key=lambda x: x[1])
relevant_chunks = [c[0] for c in sorted_chunks]
```

SOURCE: `rag_extraction_skill.py:127–137`

- Merges results from all 13 queries into a single dict keyed by chunk text.
- For duplicate chunks across queries, keeps the lowest (best) distance score.
- Final `relevant_chunks` list is ordered ascending by distance (most relevant first).
- Distance metric: ChromaDB default (L2 or cosine depending on collection configuration; no explicit metric specified at `create_collection`).
