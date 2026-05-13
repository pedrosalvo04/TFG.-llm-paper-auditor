# 05 — Test Scenario Specifications

This document consolidates all test scenarios extracted from the legacy codebase into a single authoritative reference for the Specs2Code pipeline. Every scenario is traceable to its extraction source. Sections follow the prescribed order. GAP markers are preserved verbatim where the extraction data was absent or incomplete.

---

## LLM Client Retry Logic Tests

### `scratch/test_llm_retry.py` — Overview

**Type:** Unit test with mocks (script-level, not pytest).  
**Framework:** Python `unittest.mock` (`MagicMock`, `patch`).  
**Module under test:** `backend.common.llm_client.LLMClient`  
**Module-level mock setup:** `google`, `google.genai`, and `streamlit` are injected into `sys.modules` before any import of `LLMClient` to prevent real API calls at import time.

> Source: extracted_root_tests_scratch_01.md § 11.10

---

#### `test_retry_logic` — Success Within Retry Budget

```
TEST: test_retry_logic
RULE: RULE-06 — LLMClient succeeds after transient failures (LLM retries — success within retries)
MOCK_SETUP:
  - client = LLMClient(model_name="test-model")
  - mock_gen = MagicMock()
  - client.client.models.generate_content = mock_gen
  - mock_gen.side_effect = [
        Exception("503 UNAVAILABLE: High demand"),   # attempt 0 — fail
        Exception("503 UNAVAILABLE: High demand"),   # attempt 1 — fail
        MagicMock(text="Success response")           # attempt 2 — success
    ]
  - patch('time.sleep') as mock_sleep   (suppresses real sleep)
  - Outer patch context:
      patch('backend.common.config.GOOGLE_API_KEY', "test-key")
      patch('backend.common.config.MODEL_NAME',     "test-model")
TRIGGER: response = client.generate("test prompt")
POSITIVE CASE:
  INPUT: Two transient 503 exceptions followed by a successful response on the 3rd call.
  EXPECTED:
    - No exception raised; function returns the MagicMock with .text == "Success response".
    - mock_gen.call_count == 3   (2 failures + 1 success)
    - mock_sleep.call_count == 2  (one sleep per retry before the success)
NEGATIVE CASE:
  INPUT: N/A — the negative exhaustion path is covered by test_final_failure.
  EXPECTED: N/A
SOURCE: extracted_root_tests_scratch_01.md § 11.10, RULE-06
```

> **Rule Reference:** RULE-06 — LLMClient succeeds after transient failures  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-06), § 11.10

---

#### `test_final_failure` — Full Retry Exhaustion (6-Attempt Scenario)

```
TEST: test_final_failure
RULE: RULE-05 — LLMClient maximum retry attempts
MOCK_SETUP:
  - client = LLMClient(model_name="test-model")
  - mock_gen = MagicMock()
  - mock_gen.side_effect = Exception("503 UNAVAILABLE: High demand")   # always fails
  - patch('time.sleep') as mock_sleep
  - Outer patch context:
      patch('backend.common.config.GOOGLE_API_KEY', "test-key")
      patch('backend.common.config.MODEL_NAME',     "test-model")
TRIGGER: client.generate("test prompt")   — expected to raise
POSITIVE CASE (exhaustion — "positive" that the guard fires):
  INPUT: Every attempt to call generate_content raises the same 503 exception.
  EXPECTED:
    - An exception IS raised from client.generate (test asserts False if no exception raised;
      the except block catches and verifies the exception occurred).
    - mock_gen.call_count == 6  (1 original attempt at index 0 + 5 retries at indices 1–5)
    - mock_sleep.call_count == 5  (one sleep between each consecutive failing attempt)
    - The caught exception is re-raised (the test block reads:
        try:
            client.generate("test prompt")
            assert False, "Should have raised an exception"
        except Exception as e:
            print(f"Caught expected final exception: {e}")
            assert mock_gen.call_count == 6
      )
NEGATIVE CASE:
  INPUT: If client.generate did NOT raise, the assert False sentinel would trigger AssertionError.
  EXPECTED: The sentinel AssertionError ("Should have raised an exception") is the failure signal.
SOURCE: extracted_root_tests_scratch_01.md § 11.10, RULE-05
```

> **Rule Reference:** RULE-05 — LLMClient maximum retry attempts  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-05), § 10.8, § 10.11

---

### LLMClient Business Rules Confirmed by Tests

| Constant | Value | Source |
|----------|-------|--------|
| `max_retries` | `5` | `llm_client.py:39` |
| `base_delay` | `2` seconds | `llm_client.py:40` |
| Total attempts | `6` (= `max_retries + 1`) | `llm_client.py:42` |
| Retryable error codes | `"503"`, `"429"`, `"UNAVAILABLE"`, `"RESOURCE_EXHAUSTED"`, `"DEADLINE_EXCEEDED"` (substring match in uppercased error string) | `llm_client.py:54` |
| Backoff formula | `delay = base_delay * (2 ** attempt) + random.uniform(0, 1)` | `llm_client.py:58` |
| Sleep call count on success at 3rd attempt | `2` | RULE-06 / test_retry_logic |
| Sleep call count on total exhaustion | `5` | RULE-05 / test_final_failure |

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § RESOLUTION SUMMARY [g_012]; extracted_backend_core_01.md § 3.1

---

## Information Extraction Skill Tests (section fragmenting, MAP/REDUCE)

### `tests/test_section_splitter.py` — Overview

**Type:** Script with assertions (no pytest or unittest).  
**Module under test:** `backend.skills.auditor_skills.InformationExtractionSkill`  
**Fragmentation method:** Internal MAP-phase section-splitting logic, exposed by a `TestSkill` subclass.

> Source: extracted_root_tests_scratch_01.md § 11.14

---

#### `test_splitting_logic` — Fragment Count from 6-Section Paper

```
TEST: test_splitting_logic
RULE: RULE-09 — Section fragmentation produces at most 4 fragments from a multi-section paper
      BR-TEST-08 — 6 equal-length sections produce exactly 4 fragments
MOCK_SETUP:
  - class MockLLM:
        def generate(self, prompt):
            return type('obj', (object,), {'text': '{}'})()
    (Returns empty JSON object; prevents real LLM calls during fragment testing)
  - skill = InformationExtractionSkill(llm_client=MockLLM())
  - class TestSkill(InformationExtractionSkill):
        def get_fragments(self, paper_text):
            # Exposes internal fragmentation logic of execute():
            paper_text_norm = paper_text.replace('\r\n', '\n')
            sections = re.split(r'\n(?=#+ )', '\n' + paper_text_norm)
            sections = [s.strip() for s in sections if s.strip()]
            if len(sections) > 1:
                total_chars = sum(len(s) for s in sections)
                target = total_chars / 4
                fragments = []
                current_fragment = ""
                for section in sections:
                    if (len(current_fragment) + len(section) > target
                            and len(fragments) < 3):
                        if current_fragment:
                            fragments.append(current_fragment)
                            current_fragment = section
                        else:
                            fragments.append(section)
                    else:
                        current_fragment += ("\n\n" if current_fragment else "") + section
                if current_fragment:
                    fragments.append(current_fragment)
                return fragments
            return []
  - test_skill = TestSkill(llm_client=MockLLM())
TRIGGER: fragments = test_skill.get_fragments(paper_text)
INPUT FIXTURE (paper_text):
  6 equal-length sections:
    "# Section 1\nContent 1.\n"
    "# Section 2\nContent 2.\n"
    "# Section 3\nContent 3.\n"
    "# Section 4\nContent 4.\n"
    "# Section 5\nContent 5.\n"
    "# Section 6\nContent 6.\n"
  (All sections have identical byte length — SOURCE: tests/test_section_splitter.py:11-23)
POSITIVE CASE:
  INPUT: 6 equal-length Markdown-header sections.
  EXPECTED:
    - len(fragments) == 4   (assert message: "Expected 4 fragments, got {len(fragments)}")
    - For each fragment f: len(f) > 0
NEGATIVE CASE:
  INPUT: Paper text with no Markdown headers (no `# ` patterns).
  EXPECTED:
    - len(sections) <= 1 after split on r'\n(?=#+ )'
    - get_fragments returns []   (early-exit guard at len(sections) <= 1)
SOURCE: extracted_root_tests_scratch_01.md § 11.14, RULE-09, BR-TEST-08
```

> **Rule Reference:** RULE-09 — Section fragment count cap; BR-TEST-08  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-09), § 12 (BR-TEST-08)

---

### Fragmentation Algorithm — Confirmed Constants

| Constant | Value | Source |
|----------|-------|--------|
| Section split regex | `r'\n(?=#+ )'` (prepend `'\n'` to paper text first) | `tests/test_section_splitter.py:44` |
| Target fragment size | `total_chars / 4` | `tests/test_section_splitter.py:49` |
| Maximum early fragment boundaries | `3` (i.e., `len(fragments) < 3`) | `tests/test_section_splitter.py:54` |
| Expected output fragment count (6 equal sections) | `4` | `tests/test_section_splitter.py:75` |

> Source: extracted_root_tests_scratch_01.md § 8, § 9.7

---

### MAP/REDUCE Pipeline Rules (from InformationExtractionSkill)

The MAP/REDUCE pipeline is invoked inside `InformationExtractionSkill.execute()`, not directly tested by `test_section_splitter.py`. The test focuses only on the section-fragment boundary computation. The following MAP/REDUCE rules are confirmed by extraction:

| Phase | Rule | Source |
|-------|------|--------|
| MAP | If `len(sections) > 1`, split text into up to 4 fragments using `total_chars / 4` target | `auditor_skills.py:36` |
| MAP fallback | If no headers detected, use `RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)`, take first 4 fragments | `auditor_skills.py:77` |
| MAP LLM call | `get_map_extraction_prompt(fragment)` per fragment; result parsed as JSON | `auditor_skills.py:77` (cross-ref `prompts.py:184`) |
| REDUCE | `get_reduce_extraction_prompt(map_results)` with serialized list of MAP results; consolidates into DEFINITIVE MASTER JSON | `prompts.py:228` |

> Source: extracted_backend_skills_01.md § 3.2; extracted_backend_core_01.md § 2.2

---

## RAG Logical Block Splitting Tests

### `tests/test_rag_logical_splitter.py` — Integration Test

**Type:** Script with assertions (no pytest or unittest).  
**Splitting strategy:** Double-newline paragraph split with minimum chunk length filter.

> Source: extracted_root_tests_scratch_01.md § 11.13

---

#### `test_rag_logical_splitter` — Chunk Count and Content Assertions

```
TEST: test_rag_logical_splitter
RULE: RULE-08 — RAG chunk minimum filtering (len > 10 after strip)
      BR-TEST-06 — Second chunk (index 1) must contain Abstract heading
      BR-TEST-07 — Table header and data must remain in same chunk
MOCK_SETUP: None (inline processing, no mocks)
TRIGGER: (inline script execution)
INPUT FIXTURE (paper_text):
  Multi-line string with the following double-newline-separated sections:
    - "Title" section (Title)
    - "Abstract" section
    - "Introduction" section
    - A Markdown table block containing "| Table 1 |" header row and "Data 1" data row
    - "Final word" section
  (SOURCE: tests/test_rag_logical_splitter.py:10-25)
PROCESSING (inline, no helper function):
  1. paper_text_norm = paper_text.replace('\r\n', '\n')
  2. raw_chunks = re.split(r'\n\n+', paper_text_norm)
  3. chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]
POSITIVE CASE:
  INPUT: Well-formed multi-section paper text with all required sections present.
  EXPECTED (4 assertions):
    - len(chunks) >= 4
    - "| Table 1 |" in chunks[3]   (table header retained in chunk at index 3)
    - "Data 1" in chunks[3]        (table data row retained in same chunk as header)
    - "Abstract" in chunks[1]      (Abstract section is second chunk)
NEGATIVE CASE (minimum length filter):
  INPUT: A chunk whose stripped content is <= 10 characters long (e.g., "OK" or "Hi").
  EXPECTED: The chunk is excluded from the output list.
SOURCE: extracted_root_tests_scratch_01.md § 11.13, RULE-08, BR-TEST-06, BR-TEST-07
```

> **Rule References:** RULE-08, BR-TEST-06, BR-TEST-07  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-08), § 12 (BR-TEST-06, BR-TEST-07)

---

### `scratch/test_rag_split.py` — Naive Chunking Scratch Test

**Type:** Exploratory/scratch script. No assertions. Observation-only output.

> Source: extracted_root_tests_scratch_01.md § 11.11

---

#### `get_rag_chunks` — Naive Paragraph Split (no minimum length)

```
TEST: test_rag_split (scratch/exploratory)
RULE: N/A — no business assertions; naive chunking for observation
MOCK_SETUP: None
FUNCTION UNDER TEST:
  def get_rag_chunks(paper_text):
      paper_text_norm = paper_text.replace('\r\n', '\n')   # SOURCE: scratch/test_rag_split.py:5
      raw_chunks = re.split(r'\n\n+', paper_text_norm)     # SOURCE: scratch/test_rag_split.py:22
      return [c.strip() for c in raw_chunks if c.strip()]  # SOURCE: scratch/test_rag_split.py:23
  NOTE: No minimum length filter — differs from tests/test_rag_logical_splitter.py which requires len > 10.
TRIGGER: chunks = get_rag_chunks(test_text)
INPUT FIXTURE (test_text):
  Multi-line string with sections: Title, Abstract, Introduction, Table, Final text sections.
  (SOURCE: scratch/test_rag_split.py:28-43)
POSITIVE CASE:
  INPUT: Well-formed multi-section paper text.
  EXPECTED (observation only — no assertions):
    - Total chunk count printed as "Total chunks: {len(chunks)}"
    - Each chunk printed with a header separator
    - [GAP: chunk schema not extracted — cannot define assertions]
NEGATIVE CASE:
  INPUT: Text with only whitespace-only paragraphs between double newlines.
  EXPECTED: Empty-after-strip chunks are filtered out; non-empty result expected if any real text present.
SOURCE: extracted_root_tests_scratch_01.md § 11.11, § 9.5
```

> Source: extracted_root_tests_scratch_01.md § 9.5 (transformation), § 11.11

---

### Comparison: Naive Chunker vs. Length-Filtered Chunker

| Attribute | `scratch/test_rag_split.py` (`get_rag_chunks`) | `tests/test_rag_logical_splitter.py` |
|-----------|-----------------------------------------------|---------------------------------------|
| Split regex | `r'\n\n+'` | `r'\n\n+'` |
| Filter | Excludes empty (whitespace-only) | Excludes `len <= 10` after strip |
| Assertions | None (observation only) | 4 assertions (len, content, index) |
| Test type | Exploratory scratch | Integration test |

> Source: extracted_root_tests_scratch_01.md § 9.5, § 9.6

---

## Audit Data Model Tests (AuditState, ExtractedInfo, ChecklistItem)

### `tests/test_audit_state.py` — Overview

**Type:** `unittest.TestCase` (standard pytest-discoverable).  
**Import:** `from backend.common.audit_state import AuditState, ExtractedInfo, ChecklistItem`  
**Source:** `tests/test_audit_state.py:2`

> Source: extracted_root_tests_scratch_01.md § 11.12

---

### AuditState — Field Defaults

| Field | Type | Nullable | Default | Constraint | Source |
|-------|------|----------|---------|------------|--------|
| `paper_text` | `str` | No | (required constructor arg) | Must be set at construction | `tests/test_audit_state.py:7` |
| `invalid_paper` | `bool` | No | `False` | `assertFalse` | `tests/test_audit_state.py:9` |
| `execution_time` | `float` | No | `0.0` | `assertEqual(0.0)` | `tests/test_audit_state.py:10` |
| `evaluation` | `dict` or `None` | Yes | `None` (optional constructor kwarg) | Used by `to_frontend_dict()` | `tests/test_audit_state.py:13` |

> Source: extracted_root_tests_scratch_01.md § 11.12 (RULE-14, RULE-15)

---

#### `test_initialization` — AuditState Default Values

```
TEST: test_initialization
RULE: RULE-14 — AuditState initializes with correct defaults
MOCK_SETUP: None
TRIGGER: state = AuditState(paper_text="Test content")
POSITIVE CASE:
  INPUT: Single string argument "Test content" passed to constructor.
  EXPECTED:
    - state.paper_text == "Test content"   (assertEqual)
    - state.invalid_paper == False         (assertFalse)
    - state.execution_time == 0.0          (assertEqual)
NEGATIVE CASE:
  INPUT: Constructing AuditState without paper_text (or with a missing required field).
  EXPECTED: [GAP: response schema not extracted — cannot define assertions; AuditState constructor
             signature not fully extracted; test does not cover this path]
SOURCE: extracted_root_tests_scratch_01.md § 11.12, RULE-14
```

> **Rule Reference:** RULE-14  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-14)

---

#### `test_to_frontend_dict` — Output Key Contract

```
TEST: test_to_frontend_dict
RULE: RULE-15 — to_frontend_dict output must contain claims, informacion_extraida, metricas keys
      BR-TEST-05 — to_frontend_dict() always includes informacion_extraida and metricas keys
MOCK_SETUP: None
TRIGGER: d = state.to_frontend_dict()
POSITIVE CASE:
  INPUT: state = AuditState(paper_text="Test", evaluation={"claims": {"answer": "Yes"}})
  EXPECTED:
    - d["claims"]["answer"] == "Yes"        (assertEqual)
    - "informacion_extraida" in d           (assertIn)
    - "metricas" in d                       (assertIn)
NEGATIVE CASE:
  INPUT: AuditState constructed with evaluation=None or evaluation={}.
  EXPECTED: [GAP: response schema not extracted — cannot define assertions for empty/None
             evaluation path in to_frontend_dict()]
SOURCE: extracted_root_tests_scratch_01.md § 11.12, RULE-15, BR-TEST-05
```

> **Rule Reference:** RULE-15; BR-TEST-05  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-15), § 12 (BR-TEST-05)

---

### ExtractedInfo — Nested Sub-Model Defaults

| Sub-model | Field | Type | Nullable | Default | Source |
|-----------|-------|------|----------|---------|--------|
| `code` | `repository_url` | `str` | No | `"NOT FOUND"` | `tests/test_audit_state.py:22` |
| `hyperparameters` | `optimizer` | `str` | No | `"NOT FOUND"` | `tests/test_audit_state.py:23` |

> Source: extracted_root_tests_scratch_01.md § 11.12 (RULE-16, RULE-17)

---

#### `test_extracted_info_nesting` — Sub-Model Default Values

```
TEST: test_extracted_info_nesting
RULE: RULE-16 — ExtractedInfo.code.repository_url defaults to "NOT FOUND"
      RULE-17 — ExtractedInfo.hyperparameters.optimizer defaults to "NOT FOUND"
MOCK_SETUP: None
TRIGGER: info = ExtractedInfo()
POSITIVE CASE:
  INPUT: Default instantiation with no arguments.
  EXPECTED:
    - info.code.repository_url == "NOT FOUND"      (assertEqual)
    - info.hyperparameters.optimizer == "NOT FOUND" (assertEqual)
NEGATIVE CASE:
  INPUT: ExtractedInfo constructed with an explicit repository_url value (e.g., "https://github.com/user/repo").
  EXPECTED: [GAP: response schema not extracted — cannot define assertions for non-default construction paths]
SOURCE: extracted_root_tests_scratch_01.md § 11.12, RULE-16, RULE-17
```

> **Rule Reference:** RULE-16, RULE-17  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-16, RULE-17)

---

### ChecklistItem — Model Specification

[GAP: ChecklistItem field definitions not extracted from `backend/common/audit_state.py` — the source file (`backend/common/audit_state.py`) was confirmed absent from the extraction cluster. The model is imported in `tests/test_audit_state.py:2` but no test scenario exercises ChecklistItem directly. Cannot define field table or test assertions without source.]

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § [g_014] — UNRESOLVED

---

## Audit Pipeline Integration Tests

### `test_auditor_refactor.py` — Overview

**Type:** Script-based integration tests (not pytest). Uses a custom `main()` runner.  
**Error handling:** Every test function is wrapped in `try/except Exception`; returns `True` on pass, `False` on failure. Failures print `"❌ Error …: {e}"`. The `main()` function collects `(name, bool)` tuples and prints a summary.

> Source: extracted_root_tests_scratch_01.md § 11.1

---

#### `test_auditor_initialization` — PaperAuditor Constructor Smoke Test

```
TEST: test_auditor_initialization
RULE: RULE-10 — PaperAuditor must expose exactly 6 skill attributes (verified in test_skills_integration;
      this test verifies the constructor does not raise)
MOCK_SETUP: None (real initialization; requires GOOGLE_API_KEY in environment)
TRIGGER: auditor = PaperAuditor()
POSITIVE CASE:
  INPUT: No arguments (constructor takes none).
  EXPECTED:
    - No exception raised → function returns True.
    - PaperAuditor() creates 5 LLMClient instances and 6 skill instances (confirmed by source).
NEGATIVE CASE:
  INPUT: GOOGLE_API_KEY missing from environment.
  EXPECTED:
    - LLMClient.__init__ raises ValueError("No se encontró la GOOGLE_API_KEY en el .env").
    - The except block catches it → prints "❌ Error al inicializar auditor: {e}" → returns False.
    - main() reports test as FAIL.
SOURCE: extracted_root_tests_scratch_01.md § 11.1
```

> Source: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_009]

---

#### `test_regex_patterns` — REGEX_PATTERNS Import Smoke Test

```
TEST: test_regex_patterns
RULE: REGEX_PATTERNS must have len > 0 when imported from backend.services.auditor
MOCK_SETUP: None
TRIGGER: from backend.services.auditor import REGEX_PATTERNS; assert len(REGEX_PATTERNS) > 0
POSITIVE CASE:
  INPUT: REGEX_PATTERNS is defined at module level in auditor.py with at least 1 entry.
  EXPECTED: assertion passes → returns True.
NEGATIVE CASE (DEPLOYMENT READINESS SIGNAL — EXPECTED TO FAIL):
  INPUT: Current codebase post-refactoring.
  EXPECTED:
    - ImportError raised: `REGEX_PATTERNS` does not exist in `backend/services/auditor.py` in
      the current (post-refactoring) version.
    - The except block catches it → prints "❌ Error en patrones regex: {e}" → returns False.
    - This test is expected to FAIL on the current codebase.
    - The regex patterns that were previously inlined in auditor.py now live as class-level
      PATTERNS attributes on individual skill classes in regex_detection_skills.py.
NOTE: This test signals a pre-refactor/post-refactor API break. The test must be updated
      to reference per-skill PATTERNS class attributes (e.g., HyperparameterDetectionSkill.PATTERNS)
      or retired.
SOURCE: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_011]
```

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § [g_011] — UNRESOLVED

---

#### `test_preprocess_method` — _preprocess_paper Integration Test

```
TEST: test_preprocess_method
RULE: _preprocess_paper(text) must return a dict
MOCK_SETUP: None
TRIGGER: auditor._preprocess_paper("This is a test paper with github.com/test/repo")
POSITIVE CASE:
  INPUT: text = "This is a test paper with github.com/test/repo"
  EXPECTED:
    - isinstance(red_flags, dict) == True   (return type assertion)
    - Side effect: prints count of truthy values in red_flags dict.
NEGATIVE CASE (DEPLOYMENT READINESS SIGNAL — EXPECTED TO FAIL):
  INPUT: Current codebase post-refactoring.
  EXPECTED:
    - AttributeError raised: `PaperAuditor` in the current source has only two methods
      (`__init__` and `audit`). The method `_preprocess_paper` was removed during refactoring.
    - The except block catches it → prints "❌ Error en _preprocess_paper: {e}" → returns False.
    - Expected output: [GAP: method removed in refactoring — expected output undefined]
NOTE: The current `audit` method initialises `context = {'paper_text': paper_text, 'red_flags': {}}`
      with an empty red_flags dict (auditor.py:78), suggesting _preprocess_paper was replaced by
      an empty placeholder. Recovery of the original contract requires pre-refactor commit history.
SOURCE: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_009]
```

> Source: cross_ref_resolution_cross_ref_root_to_backend.md § [g_009] — UNRESOLVED (partial)

---

#### `test_prompts_module` — Prompt Function Smoke Test

```
TEST: test_prompts_module
RULE: get_extraction_prompt and get_evaluation_prompt must return non-empty strings
MOCK_SETUP: None
TRIGGER:
  - extraction_prompt = get_extraction_prompt("Test paper", {"test": True})
  - evaluation_prompt = get_evaluation_prompt({"test": "info"}, {"test": True})
POSITIVE CASE:
  INPUT:
    - test_text = "Test paper"
    - test_flags = {"test": True}
    - test_info = {"test": "info"}
  EXPECTED:
    - len(extraction_prompt) > 0   (non-empty string)
    - len(evaluation_prompt) > 0   (non-empty string)
    - Returns True.
NEGATIVE CASE:
  INPUT: get_extraction_prompt or get_evaluation_prompt raises an exception (e.g., import error,
         template formatting error).
  EXPECTED: except block catches it → prints "❌ Error en módulo prompts: {e}" → returns False.
SOURCE: extracted_root_tests_scratch_01.md § 11.1
```

> Source: extracted_root_tests_scratch_01.md § 11.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_010]

---

### `main()` Runner — Deployment Readiness Summary

```
FUNCTION: main()
BEHAVIOUR:
  - Runs tests in order: [test_auditor_initialization, test_regex_patterns,
                          test_preprocess_method, test_prompts_module]
  - Collects (name, bool_result) per test.
  - Prints: "✅ PASS" or "❌ FAIL" per test.
  - Prints summary: "{passed}/{total}"
  - If passed == total: "Refactorización completada exitosamente!"
  - Else: "Algunos tests fallaron."
EXPECTED OUTCOME (current codebase):
  - test_auditor_initialization: PASS (if GOOGLE_API_KEY set) / FAIL (if key absent)
  - test_regex_patterns: FAIL (REGEX_PATTERNS removed from auditor.py post-refactoring)
  - test_preprocess_method: FAIL (_preprocess_paper method removed post-refactoring)
  - test_prompts_module: PASS (get_extraction_prompt and get_evaluation_prompt still exist)
SOURCE: extracted_root_tests_scratch_01.md § 11.1
```

> Source: extracted_root_tests_scratch_01.md § 11.1

---

## Import Smoke Tests

### `test_imports.py` — Overview

**Type:** Sequential import checks (no pytest or unittest; script-level).  
**Structure:** 7 `try/except Exception` blocks, each testing one import.  
**Outcome:** Prints `"OK <module>"` on success or `"ERROR <module>: {e}"` on failure.  
**Final line:** `"Todas las importaciones funcionan correctamente!"` (printed after all blocks).

> Source: extracted_root_tests_scratch_01.md § 11.2

---

### Module Import Scenarios

| Block | Module / Import Target | Import Statement | Expected (Pass) | Expected (Fail) |
|-------|------------------------|-----------------|-----------------|-----------------|
| 1 | `frontend.config` | `from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION` | `"OK frontend.config"` | `"ERROR frontend.config: {e}"` |
| 2 | `frontend.styles.custom_css` | `from frontend.styles.custom_css import apply_custom_styles` | `"OK frontend.styles.custom_css"` | `"ERROR frontend.styles.custom_css: {e}"` |
| 3 | `frontend.utils.session_state` | `from frontend.utils.session_state import initialize_session_state` | `"OK frontend.utils.session_state"` | `"ERROR frontend.utils.session_state: {e}"` |
| 4 | `frontend.components.file_uploader` | `from frontend.components.file_uploader import process_uploaded_file` | `"OK frontend.components.file_uploader"` | `"ERROR frontend.components.file_uploader: {e}"` |
| 5 | `frontend.components.audit_results` | `from frontend.components.audit_results import render_audit_results, generate_report` | `"OK frontend.components.audit_results"` | `"ERROR frontend.components.audit_results: {e}"` |
| 6 | `frontend.components.sota_section` | `from frontend.components.sota_section import render_sota_analysis` | `"OK frontend.components.sota_section"` | `"ERROR frontend.components.sota_section: {e}"` |
| 7 | `frontend.components.chatbot` | `from frontend.components.chatbot import render_chatbot` | `"OK frontend.components.chatbot"` | `"ERROR frontend.components.chatbot: {e}"` |

> Source: extracted_root_tests_scratch_01.md § 11.2 (test_imports.py:4-44)

---

#### Scenario Blocks — Detailed

```
TEST: Block 1 — frontend.config
TRIGGER: from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION
POSITIVE CASE:
  EXPECTED: print("OK frontend.config"); ImportError absent
  VERIFIED SYMBOLS: TITLE (str), SIDEBAR_IMAGE (str URL), SIDEBAR_DESCRIPTION (str)
NEGATIVE CASE:
  INPUT: Module not installed or path misconfigured.
  EXPECTED: ImportError caught → print("ERROR frontend.config: {e}")
SOURCE: test_imports.py:4-8; cross_ref_resolution_cross_ref_root_to_frontend.md § g_008
```

```
TEST: Block 2 — frontend.styles.custom_css
TRIGGER: from frontend.styles.custom_css import apply_custom_styles
POSITIVE CASE:
  EXPECTED: print("OK frontend.styles.custom_css"); ImportError absent
NEGATIVE CASE:
  INPUT: Module not found / dependency on streamlit unavailable.
  EXPECTED: ImportError caught → print("ERROR frontend.styles.custom_css: {e}")
SOURCE: test_imports.py:10-14; cross_ref_resolution_cross_ref_root_to_frontend.md § g_026
```

```
TEST: Block 3 — frontend.utils.session_state
TRIGGER: from frontend.utils.session_state import initialize_session_state
POSITIVE CASE:
  EXPECTED: print("OK frontend.utils.session_state"); ImportError absent
NEGATIVE CASE:
  INPUT: Module or its transitive dependencies (PaperAuditor, PaperChatbot, SotaAnalyzer) not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.utils.session_state: {e}")
SOURCE: test_imports.py:16-20; cross_ref_resolution_cross_ref_root_to_frontend.md § g_027
```

```
TEST: Block 4 — frontend.components.file_uploader
TRIGGER: from frontend.components.file_uploader import process_uploaded_file
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.file_uploader"); ImportError absent
NEGATIVE CASE:
  INPUT: hashlib, os, or streamlit not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.components.file_uploader: {e}")
SOURCE: test_imports.py:22-26; cross_ref_resolution_cross_ref_root_to_frontend.md § g_004
```

```
TEST: Block 5 — frontend.components.audit_results
TRIGGER: from frontend.components.audit_results import render_audit_results, generate_report
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.audit_results"); ImportError absent
NEGATIVE CASE:
  INPUT: scoring.py or Streamlit not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.components.audit_results: {e}")
SOURCE: test_imports.py:28-32; cross_ref_resolution_cross_ref_root_to_frontend.md § g_005, g_006
```

```
TEST: Block 6 — frontend.components.sota_section
TRIGGER: from frontend.components.sota_section import render_sota_analysis
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.sota_section"); ImportError absent
NEGATIVE CASE:
  INPUT: Module not found / SotaAnalyzer dependency missing.
  EXPECTED: ImportError caught → print("ERROR frontend.components.sota_section: {e}")
SOURCE: test_imports.py:34-38; cross_ref_resolution_cross_ref_root_to_frontend.md § g_007
```

```
TEST: Block 7 — frontend.components.chatbot
TRIGGER: from frontend.components.chatbot import render_chatbot
POSITIVE CASE:
  EXPECTED: print("OK frontend.components.chatbot"); ImportError absent
NEGATIVE CASE:
  INPUT: Module not found / Streamlit not importable.
  EXPECTED: ImportError caught → print("ERROR frontend.components.chatbot: {e}")
SOURCE: test_imports.py:40-44; cross_ref_resolution_cross_ref_root_to_frontend.md § g_007
```

> Source: extracted_root_tests_scratch_01.md § 11.2

---

## Skills Architecture Integration Tests

### `test_skills_integration.py` — Overview

**Type:** Script (10 numbered tests with `sys.exit(1)` on any failure).  
**Exit behavior:** Any `AssertionError` or uncaught `Exception` triggers `sys.exit(1)`.  
**All 10 tests run sequentially; failure on any one halts the process.**

> Source: extracted_root_tests_scratch_01.md § 11.3

---

#### Test 1 — Module Imports (All 15 Skill Classes)

```
TEST: Test 1 — skill module imports
MOCK_SETUP: None
TRIGGER:
  from backend.skills import (
      BaseSkill, InformationExtractionSkill, ReproducibilityEvaluationSkill,
      MetricsCalculationSkill, MetadataAggregationSkill, ConversationalResponseSkill,
      ContextValidationSkill, ThematicCoverageSkill, QueryGenerationSkill,
      SemanticScholarSearchSkill, CoverageGapAnalysisSkill, CrossValidationSkill
  )
  from backend.skills.regex_detection_skills import (
      LimitationsQualityDetectionSkill, SoftwareVersionDetectionSkill, HardwareDetailDetectionSkill
  )
POSITIVE CASE:
  INPUT: All modules installed and importable.
  EXPECTED: No ImportError or Exception raised.
NEGATIVE CASE:
  INPUT: Any one of the 15 symbols missing from backend.skills or regex_detection_skills.
  EXPECTED: Exception caught → print("   [ERROR] Error en importaciones: {e}") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 1); test_skills_integration.py:9-35
```

> **Note:** `__init__.py` exports exactly 15 symbols; `ChecklistVerificationSkill` and `HybridHyperparameterExtractionSkill` are NOT exported from `__init__.py`.  
> Source: extracted_backend_skills_01.md § 1.1; cross_ref_resolution_cross_ref_root_to_backend.md § [g_016]

---

#### Test 2 — Service Imports

```
TEST: Test 2 — service imports
MOCK_SETUP: None
TRIGGER:
  from backend.services.auditor import PaperAuditor
  from backend.services.chatbot import Chatbot
  from backend.services.sota_analyzer import SotaAnalyzer
POSITIVE CASE:
  INPUT: All service modules importable.
  EXPECTED: No Exception raised.
NEGATIVE CASE:
  INPUT: Any service module missing or has import-time errors.
  EXPECTED: print("   [ERROR] Error importando servicios: {e}") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 2); test_skills_integration.py:38-46
```

---

#### Test 3 — Service Initialization

```
TEST: Test 3 — service initialization
MOCK_SETUP: None (real initialization; requires GOOGLE_API_KEY in environment)
TRIGGER:
  auditor = PaperAuditor()
  chatbot = Chatbot()
  sota = SotaAnalyzer()
POSITIVE CASE:
  INPUT: GOOGLE_API_KEY set; all dependencies available.
  EXPECTED: All three instances created without exception.
NEGATIVE CASE:
  INPUT: GOOGLE_API_KEY absent or LLMClient raises ValueError.
  EXPECTED:
    - print("   [ERROR] Error inicializando servicios: {e}")
    - traceback.print_exc()
    - sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 3); test_skills_integration.py:49-63
```

---

#### Test 4 — PaperAuditor Skill Attributes (6 Required)

```
TEST: Test 4 — PaperAuditor skill attributes
RULE: RULE-10 — PaperAuditor must expose exactly 6 skill attributes
MOCK_SETUP: auditor = PaperAuditor() (from Test 3)
TRIGGER: hasattr(auditor, attr) for each of 6 attribute names
REQUIRED ATTRIBUTES (6 total):
  'extraction_skill', 'hybrid_hp_skill', 'evaluation_skill',
  'verification_skill', 'metrics_skill', 'metadata_skill'
POSITIVE CASE:
  INPUT: PaperAuditor properly constructed.
  EXPECTED: All 6 hasattr checks return True.
NEGATIVE CASE:
  INPUT: Any one attribute is missing from the PaperAuditor instance.
  EXPECTED:
    - AssertionError with message "Falta <attr>"
    - print("   [ERROR] Falta <attr>")
    - sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 4); RULE-10; test_skills_integration.py:66-77
```

> **Rule Reference:** RULE-10  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-10)

---

#### Test 5 — Chatbot Skill Attributes (2 Required)

```
TEST: Test 5 — Chatbot skill attributes
RULE: RULE-11 — Chatbot must expose exactly 2 skill attributes
MOCK_SETUP: chatbot = Chatbot() (from Test 3)
TRIGGER: hasattr(chatbot, 'response_skill') AND hasattr(chatbot, 'validation_skill')
REQUIRED ATTRIBUTES (2 total): 'response_skill', 'validation_skill'
POSITIVE CASE:
  INPUT: Chatbot properly constructed.
  EXPECTED: Both hasattr checks return True.
NEGATIVE CASE:
  INPUT: Either attribute missing.
  EXPECTED: AssertionError "Falta <attr>" → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 5); RULE-11; test_skills_integration.py:80-87
```

> **Rule Reference:** RULE-11  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-11)

---

#### Test 6 — SotaAnalyzer Skill Attributes (5 Required)

```
TEST: Test 6 — SotaAnalyzer skill attributes
RULE: RULE-12 — SotaAnalyzer must expose exactly 5 skill attributes
MOCK_SETUP: sota = SotaAnalyzer() (from Test 3)
TRIGGER: hasattr(sota, attr) for each of 5 attribute names
REQUIRED ATTRIBUTES (5 total): 'thematic_skill', 'query_skill', 'search_skill', 'gap_skill', 'validation_skill'
POSITIVE CASE:
  INPUT: SotaAnalyzer properly constructed.
  EXPECTED: All 5 hasattr checks return True.
NEGATIVE CASE:
  INPUT: Any one attribute missing.
  EXPECTED: AssertionError "Falta <attr>" → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 6); RULE-12; test_skills_integration.py:90-100
```

> **Rule Reference:** RULE-12  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-12)

---

#### Test 7 — BaseSkill Inheritance

```
TEST: Test 7 — BaseSkill inheritance
MOCK_SETUP: auditor, chatbot, sota from Test 3
TRIGGER:
  isinstance(auditor.extraction_skill, BaseSkill)
  isinstance(chatbot.response_skill, BaseSkill)
  isinstance(sota.thematic_skill, BaseSkill)
POSITIVE CASE:
  INPUT: All three skills are instances of BaseSkill (or a BaseSkill subclass).
  EXPECTED: All 3 isinstance checks return True.
NEGATIVE CASE:
  INPUT: Any skill is not a BaseSkill subclass.
  EXPECTED: print("   [ERROR] Error en herencia de BaseSkill") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 7); test_skills_integration.py:103-111
```

---

#### Test 8 — BaseSkill Required Methods

```
TEST: Test 8 — BaseSkill required methods
MOCK_SETUP: skill = auditor.extraction_skill (InformationExtractionSkill instance)
TRIGGER:
  hasattr(skill, 'execute')
  hasattr(skill, 'validate_context')
  hasattr(skill, 'log_execution')
  callable(skill.execute)
REQUIRED METHOD PRESENCE AND CALLABILITY:
  - 'execute': present and callable
  - 'validate_context': present
  - 'log_execution': present
POSITIVE CASE:
  INPUT: extraction_skill is a properly constructed BaseSkill subclass.
  EXPECTED: All 4 checks pass; no AssertionError raised.
NEGATIVE CASE:
  INPUT: Any method absent or execute not callable.
  EXPECTED:
    AssertionError messages (per check):
      "Falta método execute"
      "Falta método validate_context"
      "Falta método log_execution"
      "execute no es callable"
    → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 8); test_skills_integration.py:114-124
```

---

#### Test 9 — SemanticScholarSearchSkill Execution with Empty Queries

```
TEST: Test 9 — SemanticScholarSearchSkill execution
RULE: RULE-13 — SemanticScholarSearchSkill with empty search_queries returns dict with 'sota_papers' key
MOCK_SETUP:
  from backend.skills.sota_skills import SemanticScholarSearchSkill
  search_skill = SemanticScholarSearchSkill()   (no llm_client argument)
TRIGGER: result = search_skill.execute({'search_queries': []})
POSITIVE CASE:
  INPUT: context = {'search_queries': []}   (empty queries list)
  EXPECTED: 'sota_papers' in result   (key present in returned dict)
NEGATIVE CASE:
  INPUT: execute raises any exception (network error, missing dependency, etc.).
  EXPECTED:
    - print("   [ERROR] Error ejecutando skill: {e}")
    - traceback.print_exc()
    - sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 9); RULE-13; test_skills_integration.py:127-141
```

> **Rule Reference:** RULE-13  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-13); cross_ref_resolution_cross_ref_root_to_backend.md § [g_018]

---

#### Test 10 — Logging Smoke Test

```
TEST: Test 10 — logging infrastructure
MOCK_SETUP:
  from backend.utils.logger import get_logger
  logger = get_logger("test_skill")
TRIGGER: logger.info("Test de logging")
POSITIVE CASE:
  INPUT: get_logger returns a logger with a working .info() method.
  EXPECTED: No exception raised.
NEGATIVE CASE:
  INPUT: get_logger raises or logger.info raises.
  EXPECTED: print("   [ERROR] Error en logging: {e}") → sys.exit(1)
SOURCE: extracted_root_tests_scratch_01.md § 11.3 (Test 10); test_skills_integration.py:144-151
```

---

## Checklist Health Scoring Tests (get_checklist_health)

### `scratch/test_checklist_health.py` — Overview

**Type:** Scratch assertion script.  
**Module under test:** `frontend.utils.scoring.get_checklist_health`  
**Priority:** HIGH (this function gates the checklist risk display in the UI).

> Source: extracted_root_tests_scratch_01.md § 11.9

---

### `get_checklist_health` — Function Specification

```
FUNCTION: get_checklist_health
SIGNATURE: get_checklist_health(evaluation: dict) -> dict
SOURCE: scoring.py:37
PARAMETERS:
  - evaluation: dict — keyed by the 16 CHECKLIST_KEYS.
    Expected structure per key:
      {
        "answer":          str,          # "Yes" / "No" / "N/A" / "" (case-insensitive comparison)
        "justification":   str,
        "evidence":        str,
        "is_no_justified": bool or str   # True/False or "true"/"false"
      }
RETURN: dict with keys:
  - "status":        str  — "valid" if pending_count == 0, else "risk"   SOURCE: scoring.py:122-123
  - "pending_count": int  — count of risk-triggering items              SOURCE: scoring.py:122-126
  - "total":         int  — len(items); always 16 when evaluation non-empty; 0 on early exit  SOURCE: scoring.py:127
  - "items":         list — 16 item dicts (one per CHECKLIST_KEYS key), each containing:
      "key":                  str  — the CHECKLIST_KEYS key string
      "label":                str  — from CHECKLIST_LABELS.get(key, key)
      "answer":               str  — stripped answer if non-empty, else "—"
      "evidence":             str  — evidence if present, else justification if present, else "—"
      "justification":        str  — stripped justification string
      "is_no_justified":      bool — normalised from raw ("true"/"false" or bool)
      "pending_justification":bool — True when "no" in answer AND (not is_no_justified OR not justification)
      "missing_evidence":     bool — True when "yes" in answer AND (not evidence AND not justification)
      "alert_msg":            str  — risk description; "" if no risk;
                                     special suffix for "crowdsourcing_human_subjects":
                                     "⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."
                                     SOURCE: scoring.py:110-120
EARLY_EXIT_GUARD:
  When evaluation is falsy (None, {}, etc.):
    returns {"status": "risk", "items": [], "pending_count": 0, "total": 0}
  SOURCE: scoring.py:56-62
```

> Source: cross_ref_resolution_cross_ref_root_to_frontend.md § g_013; extracted_frontend_01.md § 7.1

---

### 16 Checklist Items (CHECKLIST_KEYS and CHECKLIST_LABELS)

| # | Key | Label |
|---|-----|-------|
| 1 | `claims` | "1. Claims" |
| 2 | `limitations` | "2. Limitations" |
| 3 | `theory_assumptions_proofs` | "3. Theory, Assumptions & Proofs" |
| 4 | `experimental_result_reproducibility` | "4. Experimental Result Reproducibility" |
| 5 | `open_access_data_code` | "5. Open Access to Data and Code" |
| 6 | `experimental_setting_details` | "6. Experimental Setting / Details" |
| 7 | `experiment_statistical_significance` | "7. Experiment Statistical Significance" |
| 8 | `experiments_compute_resource` | "8. Experiments Compute Resource" |
| 9 | `code_of_ethics` | "9. Code of Ethics" |
| 10 | `broader_impacts` | "10. Broader Impacts" |
| 11 | `safeguards` | "11. Safeguards" |
| 12 | `licenses` | "12. Licenses" |
| 13 | `assets` | "13. Assets" |
| 14 | `crowdsourcing_human_subjects` | "14. Crowdsourcing & Human Subjects" |
| 15 | `irb_approvals` | "15. IRB Approvals" |
| 16 | `declaration_llm_usage` | "16. Declaration of LLM Usage" |

> Source: extracted_frontend_01.md § 2.3; scoring.py:8-34

---

### Mock Evaluation Dictionary (16 Items)

The `mock_eval` used by `scratch/test_checklist_health.py` includes one entry per CHECKLIST_KEYS key. The key that triggers the main assertion is:

| Key | answer | evidence | justification | is_no_justified |
|-----|--------|----------|---------------|-----------------|
| `experiment_statistical_significance` | `'No'` | `''` | `''` | `False` |

All other keys in mock_eval have their own answer/evidence/justification values — the full list of 16 keys is: `['claims', 'limitations', 'theory_assumptions_proofs', 'experimental_result_reproducibility', 'open_access_data_code', 'experimental_setting_details', 'experiment_statistical_significance', 'experiments_compute_resource', 'code_of_ethics', 'broader_impacts', 'safeguards', 'licenses', 'assets', 'crowdsourcing_human_subjects', 'irb_approvals', 'declaration_llm_usage']`.

> Source: extracted_root_tests_scratch_01.md § 8 (mock_eval key list), § 11.9

---

#### Scenario 1 — 'No' Without Justification Triggers 'risk' Status

```
TEST: get_checklist_health — pending_justification and risk status
RULE: RULE-07 — health['status'] == 'risk' when any item has answer='No' AND is_no_justified=False
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(mock_eval)
POSITIVE CASE (risk correctly detected):
  INPUT: mock_eval['experiment_statistical_significance'] =
           {'answer': 'No', 'evidence': '', 'justification': '', 'is_no_justified': False}
  EXPECTED:
    - stats_item = next(i for i in health['items'] if i['key'] == 'experiment_statistical_significance')
    - stats_item['pending_justification'] == True
        (assert message: "Item 7 should be flagged!")
    - health['status'] == 'risk'
        (assert message: "Should be risk with unjustified No!")
NEGATIVE CASE:
  INPUT: evaluation is falsy (None, {}, etc.).
  EXPECTED (EARLY_EXIT_GUARD):
    - {"status": "risk", "items": [], "pending_count": 0, "total": 0} returned immediately.
SOURCE: extracted_root_tests_scratch_01.md § 11.9; RULE-07; scratch/test_checklist_health.py:33-35
```

> **Rule Reference:** RULE-07  
> Source: extracted_root_tests_scratch_01.md § 6 (RULE-07)

---

#### Scenario 2 — All 'Yes' Answers (Valid Status)

```
TEST: get_checklist_health — all Yes answers
RULE: status == 'valid' when pending_count == 0
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(all_yes_eval)
POSITIVE CASE:
  INPUT: All 16 items have answer='Yes' with non-empty evidence.
  EXPECTED:
    - health['status'] == 'valid'
    - health['pending_count'] == 0
    - health['total'] == 16
    - All items have missing_evidence == False and pending_justification == False
NEGATIVE CASE: [GAP: scoring formula not extracted for partial Yes/missing-evidence edge cases]
SOURCE: scoring.py:122-127 (inferred from RETURN spec); cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

#### Scenario 3 — All 'No' Answers (Full Risk)

```
TEST: get_checklist_health — all No answers without justification
RULE: pending_count == 16 when all No items are unjustified
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(all_no_eval)
POSITIVE CASE:
  INPUT: All 16 items have answer='No', justification='', is_no_justified=False.
  EXPECTED:
    - health['status'] == 'risk'
    - health['pending_count'] == 16
    - All items have pending_justification == True
NEGATIVE CASE: [GAP: scoring formula not extracted — exact pending_count calculation
               when some items are 'No' with is_no_justified=True is not tested in extraction]
SOURCE: scoring.py:122-127 (inferred)
```

---

#### Scenario 4 — pending_justification Edge Case

```
TEST: get_checklist_health — pending_justification edge case
RULE: pending_justification == True when "no" in answer AND (not is_no_justified OR not justification)
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(pending_eval)
POSITIVE CASE:
  INPUT: Item with answer='No', is_no_justified=True but justification='' (empty string).
  EXPECTED:
    - pending_justification == True (because not justification is True when justification='')
  INPUT: Item with answer='No', is_no_justified=False but justification='Some text'.
  EXPECTED:
    - pending_justification == True (because not is_no_justified is True)
NEGATIVE CASE:
  INPUT: Item with answer='No', is_no_justified=True, justification='Justified reason'.
  EXPECTED:
    - pending_justification == False
SOURCE: scoring.py:110-120 (item dict definition); cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

#### Scenario 5 — missing_evidence Edge Case

```
TEST: get_checklist_health — missing_evidence edge case
RULE: missing_evidence == True when "yes" in answer AND (not evidence AND not justification)
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(missing_ev_eval)
POSITIVE CASE:
  INPUT: Item with answer='Yes', evidence='', justification=''.
  EXPECTED: missing_evidence == True
NEGATIVE CASE:
  INPUT: Item with answer='Yes', evidence='', justification='Some justification text'.
  EXPECTED: missing_evidence == False (justification counts as substitute evidence)
SOURCE: scoring.py:110-120; cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

#### Scenario 6 — crowdsourcing_human_subjects Special Alert Suffix

```
TEST: get_checklist_health — crowdsourcing ethics suffix
MOCK_SETUP: None
TRIGGER: health = get_checklist_health(crowd_eval)
POSITIVE CASE:
  INPUT: Item 'crowdsourcing_human_subjects' with a risk condition (pending_justification or
         missing_evidence).
  EXPECTED:
    - alert_msg contains "⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."
      appended as special suffix.
NEGATIVE CASE:
  [GAP: exact conditions that trigger the suffix beyond a generic risk condition not fully
        extracted — the special suffix is appended to items triggering risk for key
        'crowdsourcing_human_subjects' specifically; full logic not extracted]
SOURCE: scoring.py:110-120; cross_ref_resolution_cross_ref_root_to_frontend.md § g_013
```

---

## Scratch / Exploratory Test Cases

### `scratch/test_rag_split.py` — Naive Chunking (Already Covered in Section 3)

The naive chunking approach, input preconditions, and function definition are documented in full in the **RAG Logical Block Splitting Tests** section above.

Additional notes:

- **Test precondition:** No external file dependency. The `test_text` fixture is a hardcoded multi-line string defined at `scratch/test_rag_split.py:28-43`.
- **No assertions:** This is an observation-only script that prints chunk count and chunk content. It cannot fail unless Python itself crashes.

> Source: extracted_root_tests_scratch_01.md § 11.11

---

### `backend/scratch/test_embed.py` — Google GenAI Embed API Response Structure

**Type:** Scratch script. No assertions. No error handling.  
**Purpose:** Verifies the response structure of `client.models.embed_content` with a 3-element input.

> Source: extracted_root_tests_scratch_01.md § 11.4

```
TEST: test_embed (scratch/exploratory)
MOCK_SETUP: None (real Google GenAI API call)
PRECONDITION: GOOGLE_API_KEY set in .env
TRIGGER:
  client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
  contents = ["hello", "world", "test"]
  res = client.models.embed_content(model="gemini-embedding-2", contents=contents)
OBSERVATION ONLY (no assertions):
  - Prints type(res)
  - If hasattr(res, 'embeddings'):
      Prints type(res.embeddings)
      If isinstance(res.embeddings, list):
          Prints len(res.embeddings)        — expected: 3 (one per input string)
          Prints type(res.embeddings[0])
          Prints type(res.embeddings[0].values)
          Prints len(res.embeddings[0].values)   — embedding vector dimension
      Else: Prints "Embeddings is not a list. It is {type(res.embeddings)}"
  - Else: Prints "No embeddings attribute"
POSITIVE CASE:
  INPUT: Valid API call with 3 text strings.
  EXPECTED (from API contract):
    - res.embeddings is a list of 3 embedding objects
    - res.embeddings[0].values is a list of numeric values (vector)
    - [GAP: API response schema not extracted — cannot define assertions on exact
             embedding dimension or numeric value ranges]
NEGATIVE CASE:
  INPUT: Invalid GOOGLE_API_KEY or API unavailable.
  EXPECTED:
    - No error handling in this script. Exception propagates uncaught to interpreter.
    - [GAP: API response schema not extracted — cannot define assertions]
SOURCE: extracted_root_tests_scratch_01.md § 11.4; § 7.5
```

> Source: extracted_root_tests_scratch_01.md § 7.5, § 11.4

---

### `backend/scratch/test_embed2.py` — Embed API with Error Handling

**Type:** Scratch script. No assertions. Has `try/except` wrapper.

> Source: extracted_root_tests_scratch_01.md § 11.5

```
TEST: test_embed2 (scratch/exploratory)
MOCK_SETUP: None (real API call)
PRECONDITION: GOOGLE_API_KEY set in .env
TRIGGER:
  Block 1:
    try:
        res = client.models.embed_content(model="gemini-embedding-2", contents=["hello","world","test"])
        print embed length or "no attribute"
    except Exception as e:
        print("embed_content error:", e)
  Block 2:
    try: pass
    except Exception: pass   (empty placeholder block)
POSITIVE CASE:
  INPUT: Valid API call.
  EXPECTED (observation only):
    - [GAP: API response schema not extracted — cannot define assertions]
NEGATIVE CASE:
  INPUT: API call fails.
  EXPECTED: print("embed_content error:", e)   (no re-raise; script continues)
SOURCE: extracted_root_tests_scratch_01.md § 11.5
```

---

### `scratch/repro_hyperparams.py` — Hyperparameter Detection Reproduction

**Type:** Scratch script. No assertions. Function `test_hyperparameter_detection()` called at `__main__`.

> TEST PRECONDITION: File `paper_cientifico_3_CON_ERRORES.md` must exist in the current working directory (UTF-8 encoded). This is a **test precondition**, not a deployment constraint. The script silently skips if the file is missing (prints `"File … not found"` and returns).

> **Note:** `*.md` files are in `.gitignore` (`.gitignore:34`). The test file is not version-controlled and must be provided externally before running this script.

```
TEST: test_hyperparameter_detection (scratch/exploratory)
MOCK_SETUP:
  skill = HyperparameterDetectionSkill()
  skill.log_execution = lambda msg, level="info": print(f"[{level.upper()}] {msg}")
  (log_execution overridden to print inline — avoids logging infrastructure dependency)
PRECONDITION: os.path.exists("paper_cientifico_3_CON_ERRORES.md") == True
TRIGGER: results = skill.execute({"paper_text": text})
POSITIVE CASE:
  INPUT: Contents of paper_cientifico_3_CON_ERRORES.md (UTF-8) with hyperparameter-bearing text.
  EXPECTED (observation only):
    - json.dumps(results, indent=2) prints successfully
    - [GAP: response schema not extracted — cannot define assertions on results structure]
NEGATIVE CASE:
  INPUT: File missing from CWD.
  EXPECTED: print("File ... not found") → function returns; no exception.
SOURCE: extracted_root_tests_scratch_01.md § 11.8
```

---

### `scratch/patch_skills.py` — One-Time Maintenance Script

> DEPLOYMENT CONSTRAINT: This is not a test scenario. `patch_skills.py` is a one-time maintenance script that performs an AST-validated in-place rewrite of `backend/skills/regex_detection_skills.py`. It is classified here as a deployment constraint per the prescribed format.

> **DEPLOYMENT CONSTRAINT:**
> `patch_skills.py` requires the following **three class markers** to exist in `backend/skills/regex_detection_skills.py` **in exact order**:
> 1. `'class CrowdsourcingDetectionSkill(BaseSkill):'`
> 2. `'class LicenseDetectionSkill(BaseSkill):'`
> 3. `'class LimitationsQualityDetectionSkill(BaseSkill):'`
>
> If any marker is absent or out of order, the script raises `ValueError` (or `str.index()` raises `ValueError` for the missing substring). The patch is non-idempotent: running it twice will corrupt the file because the original class boundaries will have been replaced. The script calls `ast.parse(new_content)` after writing as a post-write syntax validator.
>
> Source: extracted_root_tests_scratch_01.md § 11.7; extracted_root_tests_scratch_01.md § 8 (patch class boundary markers)

---

### `scratch/check_st.py` — Streamlit API Surface Check

**Type:** Scratch script (6 lines). No assertions.  
**Purpose:** Checks whether `st.html` and `st.iframe` exist as Streamlit attributes.

```
TEST: check_st (scratch/exploratory)
MOCK_SETUP: None
TRIGGER:
  import streamlit as st
  print(f"st.html exists: {hasattr(st, 'html')}")
  print(f"st.iframe exists: {hasattr(st, 'iframe')}")
POSITIVE CASE:
  EXPECTED (observation only): Both hasattr checks complete and print without exception.
NEGATIVE CASE:
  INPUT: Streamlit not installed / import fails.
  EXPECTED: Exception caught → print("Error: {e}")
SOURCE: extracted_root_tests_scratch_01.md § 11.6
```

---

*End of 05_test_scenarios.md*
