# Fix Report — fix_depth_apis_1

**Target spec:** `03_technical_specs.md`
**Validation report:** `validation_report_val_depth_apis.md`
**Total issues addressed:** 9 (2 fidelity, 7 depth_gaps)

---

## Issue 1 — API-002 / Fidelity: Wrong line reference in §1.1

**Type:** fidelity
**Validation report section:** Fidelity Issues > API-002

**Before:**
```
Fallback call signature in `InformationExtractionSkill` REDUCE phase — [Source: ..., `auditor_skills.py:113`]:
```

**After:**
```
Fallback call signature in `InformationExtractionSkill` REDUCE phase — [Source: ..., `auditor_skills.py:125`]:
```

**Source evidence:** `auditor_skills.py:113` contains a comment `# 2. Fase REDUCE (Consolidación)`. The actual fallback call `self.llm_client.client.models.generate_content(model=REDUCE_MODEL_NAME, contents=reduce_prompt, config={...})` is at `auditor_skills.py:125`.

---

## Issue 2 — API-003 / Fidelity: Wrong line reference in query params table (§1.2)

**Type:** fidelity
**Validation report section:** Fidelity Issues > API-003

**Before:**
```
| `query` | value of each search query string (runtime) | — | `sota_skills.py:162` |
```

**After:**
```
| `query` | value of each search query string (runtime) | — | `sota_skills.py:202` |
```

**Source evidence:** `sota_skills.py:162` is inside the `SemanticScholarSearchSkill` class docstring (not executable code). The `requests.get(SEMANTIC_SCHOLAR_BASE_URL, params=params, headers=headers, timeout=15)` call is at `sota_skills.py:202`.

---

## Issue 3 — API-003 / Fidelity: Wrong line reference in HTTP call summary line (§1.2)

**Type:** fidelity
**Validation report section:** Fidelity Issues > API-003

**Before:**
```
HTTP call via `requests.get(..., timeout=15)`. [Source: ..., `sota_skills.py:162`]
```

**After:**
```
HTTP call via `requests.get(..., timeout=15)`. [Source: ..., `sota_skills.py:202`]
```

**Source evidence:** Same as Issue 2 — actual `requests.get` is at `sota_skills.py:202`.

---

## Issue 4 — API-001 / stream_flag: Synchronous call mode undocumented (§2.2)

**Type:** depth_gap
**Validation report section:** Depth Gaps > API-001 — stream_flag

**Before:**
```
- Return type: Google genai response object; caller accesses `.text` or `.candidates[0].content` etc.
```

**After:**
```
- **Calling mode: synchronous** — the `stream` parameter is NOT passed to `generate_content`; the SDK defaults to a blocking, non-streaming call. [Source: `llm_client.py:44–48`]
- Return type: response object from `genai.Client.models.generate_content`; callers access the text payload via the `.text` attribute directly (e.g., `raw_text = response.text.strip()`). [Source: `llm_client.py:49`, `auditor_skills.py:121`]
```

**Source evidence:**
- `llm_client.py:44–48`: The call `self.client.models.generate_content(model=self.model_name, contents=prompt, config=self.generation_config)` does NOT include a `stream` parameter → synchronous/blocking mode.
- `llm_client.py:49`: `return response`
- `auditor_skills.py:121`: `raw_text = response.text.strip()` — caller uses `.text` directly.

---

## Issue 5 — API-001 / response_type_name: Return type name underspecified (§2.2)

**Type:** depth_gap
**Validation report section:** Depth Gaps > API-001 — response_type_name

**Fix:** Combined with Issue 4 in the same line replacement above. The spec now specifies that `.text` is the concrete accessor used by callers, and notes the source confirming this (`auditor_skills.py:121`). The type name `google.genai.types.GenerateContentResponse` is not explicitly stated in any type annotation in the source; the accessor pattern `.text` is confirmed from source and documented.

**Source evidence:** `auditor_skills.py:121`: `raw_text = response.text.strip()` — confirms `.text` is the correct accessor.

---

## Issue 6 — API-002 / response_schema: Response accessor absent from §2.3

**Type:** depth_gap
**Validation report section:** Depth Gaps > API-002 — response_schema

**Before:** §2.3 ended immediately after the `generate_content` call block and `REDUCE_MODEL_NAME` note. No response accessor was documented.

**After:** Added **Response accessor** section:
```
**Response accessor:**

Immediately after the fallback call, the caller extracts text via:

```python
raw_text = response.text.strip()
```

Source: `auditor_skills.py:130`. The `.text` attribute is the sole accessor used; no other fields are read from the response object in this path.
```

**Source evidence:** `auditor_skills.py:130`: `raw_text = response.text.strip()` — immediately follows the fallback call at line 125.

---

## Issue 7 — API-002 / authentication: Credential flow undocumented in §2.3

**Type:** depth_gap
**Validation report section:** Depth Gaps > API-002 — authentication

**Before:** No authentication documentation in §2.3.

**After:** Added **Authentication** section:
```
`self.llm_client.client` is the `genai.Client(api_key=GOOGLE_API_KEY)` instance constructed in `LLMClient.__init__` [Source: `llm_client.py:23`]. The fallback call reuses this pre-constructed client and therefore authenticates via the same `GOOGLE_API_KEY` environment variable — no separate credential configuration is applied at the fallback call site. [Source: `auditor_skills.py:125`, `llm_client.py:23`]
```

**Source evidence:**
- `llm_client.py:23`: `self.client = genai.Client(api_key=GOOGLE_API_KEY)` — confirms the client is constructed once with `GOOGLE_API_KEY`.
- `auditor_skills.py:125`: `self.llm_client.client.models.generate_content(...)` — the fallback reuses the pre-built `self.llm_client.client`.

---

## Issue 8 — API-002 / error_handling: Fallback exception propagation undocumented (§2.3)

**Type:** depth_gap
**Validation report section:** Depth Gaps > API-002 — error_handling

**Before:** No error handling documented for the fallback call.

**After:** Added **Error handling** section:
```
The fallback call is inside the `except Exception` handler for the primary `self.llm_client.generate(reduce_prompt)` call [Source: `auditor_skills.py:122–130`]. There is no additional `try/except` wrapping the fallback call itself: if `self.llm_client.client.models.generate_content(...)` raises, the exception propagates uncaught to the caller of `InformationExtractionSkill.execute`. [Source: `auditor_skills.py:118–130`]
```

**Source evidence:** `auditor_skills.py:118–130`:
- Line 118: `try:` (primary call block)
- Line 122: `except Exception as e:` (catches primary failure, initiates fallback)
- Line 125: `response = self.llm_client.client.models.generate_content(...)` — no inner try/except
- Line 130: `raw_text = response.text.strip()` — if line 125 raises, this propagates uncaught.

---

## Issue 9 — API-003 / response_schema + error_handling: Response structure and error paths absent (§1.2)

**Type:** depth_gap (two sub-gaps: response_schema and error_handling)
**Validation report section:** Depth Gaps > API-003 — response_schema and error_handling

**Before:** §1.2 ended with the HTTP call summary line. No response structure or error handling was documented.

**After:** Added two new sub-sections immediately after the HTTP call summary line:

**Response structure** — documents:
- `response.json().get("data", [])` as the top-level data extraction (SOURCE: `sota_skills.py:210`)
- Table of each field in the response item: `paperId` (accessed as dict key, str), `citationCount` (accessed with default 0, int|None), and other fields from `SEMANTIC_SCHOLAR_FIELDS` (SOURCE: `sota_skills.py:227`, `sota_skills.py:231`, `config.py:139`)
- Post-processing: dedup by `paperId`, sort by `citationCount` descending, top 10 returned (SOURCE: `sota_skills.py:227–232`)

**Error handling** — documents all four behaviors:
- Inter-query throttle: `time.sleep(0.5)` when `i > 0` (SOURCE: `sota_skills.py:190–191`)
- HTTP 200: extract `data` list (SOURCE: `sota_skills.py:209–214`)
- HTTP 429: log warning + `time.sleep(2)` + continue to next query (SOURCE: `sota_skills.py:215–217`)
- Other non-200: log warning + continue (SOURCE: `sota_skills.py:218–222`)
- `except Exception as e`: log error + continue to next query (SOURCE: `sota_skills.py:223–224`)

**Source evidence:**
- `sota_skills.py:190–191`: `if i > 0: time.sleep(0.5)`
- `sota_skills.py:202–207`: `requests.get(SEMANTIC_SCHOLAR_BASE_URL, params=params, headers=headers, timeout=15)`
- `sota_skills.py:209–214`: HTTP 200 path
- `sota_skills.py:210`: `data = response.json().get("data", [])`
- `sota_skills.py:215–217`: HTTP 429 → `time.sleep(2)`
- `sota_skills.py:218–222`: non-200 → log warning
- `sota_skills.py:223–224`: `except Exception as e` → log error
- `sota_skills.py:227`: `{p['paperId']: p for p in sota_papers if p.get('paperId')}.values()`
- `sota_skills.py:231`: `key=lambda x: x.get('citationCount', 0)`
- `config.py:139`: `SEMANTIC_SCHOLAR_FIELDS = "paperId,title,authors,year,citationCount,abstract,url"`
