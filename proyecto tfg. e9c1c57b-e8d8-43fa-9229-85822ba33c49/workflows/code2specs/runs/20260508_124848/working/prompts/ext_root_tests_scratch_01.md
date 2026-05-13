PATH SANDBOX
============
READ-ONLY (source code): /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input
WRITE-ONLY (output dir): /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working

NEVER use relative paths — ALWAYS use the ABSOLUTE paths above.
NEVER write files to the current working directory (cwd).
NEVER create files outside the WRITE-ONLY path.
Before writing ANY file, verify the target path starts with the WRITE-ONLY path.

---

AGENT ID: ext_root_tests_scratch_01
OUTPUT FILE: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md

Write your output file DIRECTLY to the WRITE-ONLY path. NEVER create subdirectories. The output path is: WRITE-ONLY/extracted_root_tests_scratch_01.md — NOT WRITE-ONLY/subfolder/extracted_root_tests_scratch_01.md

---

SCOPE
=====
You are a reverse-engineering extraction agent. Your task is to read the source files listed below and produce a complete, structured Markdown specification document covering the following extraction categories:

- Category 5: Business Rules
- Category 8: API / Service Contracts and Batch Jobs
- Category 9: Constants, Enums, Lookup Tables (with ACTUAL VALUES)
- Category 10: Transformations (source→target, field-by-field conversion logic)
- Category 12: Error Handling (every error code, message, exception type, recovery action, transaction boundaries)

The cluster covers: Application entry point, PDF conversion utilities (md→pdf, pdf→md), model listing CLI, dependency configuration (requirements.txt), integration and unit test suites covering auditor refactoring, skill integration, RAG splitting, section splitting, and embedding experiments.

---

FILES TO READ
=============
Read EVERY file listed below using its EXACT absolute path. Do NOT invent paths. Do NOT shorten or re-base them.

1. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/.gitignore
2. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/app.py
3. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/create_test_pdf.py
4. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/list_models.py
5. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/md_to_pdf.py
6. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/pdf_to_md.py
7. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/requirements.txt
8. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/test_auditor_refactor.py
9. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/test_imports.py
10. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/test_skills_integration.py
11. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/scratch/test_embed.py
12. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/scratch/test_embed2.py
13. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/scratch/check_st.py
14. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/scratch/patch_skills.py
15. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/scratch/repro_hyperparams.py
16. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/scratch/test_checklist_health.py
17. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/scratch/test_llm_retry.py
18. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/scratch/test_rag_split.py
19. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/tests/test_audit_state.py
20. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/tests/test_rag_logical_splitter.py
21. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/tests/test_section_splitter.py

---

FIDELITY RULE (CRITICAL)
=========================
EXTRACT ONLY what the source code demonstrates exists. NEVER invent modules, tables, fields, functions, or business rules. If something is referenced but not implemented in this cluster's files, document it as a GAP with the reference location. Every extracted element MUST include a source reference (file:line or file:function).

HONESTY OVER COMPLETENESS (CRITICAL)
=====================================
If a code unit (method, function, handler) contains NO substantive logic — only delegation, simple getters/setters, or boilerplate — document it as:
  DETAIL: DELEGATION_ONLY — calls <target> with <params>, no local logic.
  or: DETAIL: TRIVIAL — getter/setter for <field>, no business logic.
NEVER invent logic to fill gaps. NEVER describe what a method 'probably does' or 'would typically do'. If you cannot determine the actual behavior from the source code in scope, write:
  DETAIL: UNRESOLVABLE — source logic not available in this cluster's files.
  CROSS-REFERENCE: likely implemented in <file/module> based on <evidence>.
A correct UNRESOLVABLE is infinitely better than an invented description.

---

SOURCE REFERENCE FORMAT (MANDATORY)
=====================================
Every extracted element MUST use this exact format for source references:
  `SOURCE: filename.py:line_number`  or  `SOURCE: filename.py:function_name`
The `SOURCE:` prefix is mandatory for traceability and automated validation. Do NOT use bare inline references like `(file:line)` or unlabeled line numbers.

---

LARGE FILE STRATEGY (CRITICAL — agents MUST NOT surrender)
===========================================================
Files with >200 LOC or >50KB MUST still be fully documented. Use this strategy:
1. SCAN: Read the full file to identify all code units (classes, functions, handlers, test cases).
2. INDEX: List every code unit with its line range and one-line purpose.
3. DECOMPOSE: For each code unit, extract its full logic using the DEPTH RULE below.
4. If context limits approach, prioritize by this order:
   a) Business rules and validation logic — ALWAYS full detail
   b) Data operations (CRUD, transformations) — ALWAYS full detail
   c) Event handlers and state transitions — ALWAYS full detail
   d) Test assertions and their setup/teardown — structure + assertions, skip boilerplate
   e) Boilerplate/framework wiring — DELEGATION_ONLY notation
NEVER write 'file too complex' or 'too large to analyze'. NEVER skip methods because the file is big. If you genuinely cannot fit everything, document what you extracted AND list the code units you could not reach with their line ranges, marked as:
  INCOMPLETE: <function_name> at lines <range> — not extracted due to context limits.
  This is recoverable. 'Too complex to analyze' is NOT.

---

DEPTH RULE (CRITICAL)
======================
Document EVERY code unit (function, method, test case, script block) with its actual logic:
- NOT "processes records" → instead: "reads record from FILE-A, compares FIELD-X with FIELD-Y, if equal writes to FILE-B with FIELD-Z mapped from FIELD-W"
- NOT "validates data" → instead: "checks if FIELD-X > 0 AND FIELD-Y = 'A', if false sets ERROR-CODE to 'E01' and calls ERROR-HANDLER"
- NOT "calls validateOrder()" → instead: decompose what validateOrder does inline
- NOT "has several status values" → instead: list every constant/enum value with its meaning
- NOT "tests the embedding" → instead: "calls embed_text(input='Hello world'), asserts result is a list of floats with length == 384, asserts result[0] is of type float"

Trace every decision branch. If a code unit has >50 lines of logic, STILL describe every significant branch — do NOT summarize.

---

ANTI-SUMMARY RULES (CRITICAL — follow these verbatim)
======================================================

1. NEVER COUNT — ALWAYS LIST:
   NEVER write '45+ services', '220 queries identified', 'several validators', 'multiple endpoints', or any count/approximation. Instead LIST EVERY SINGLE ONE by name. If there are 45 services, list all 45. If there are 220 queries, list all 220 (name + purpose + source). Counting is FORBIDDEN — listing is mandatory.

2. NEVER USE GENERIC SOURCE RANGES:
   NEVER write SOURCE: file:1-1800 or SOURCE: file:6-96 as a range covering a whole file or section. Each extracted element MUST have its OWN specific SOURCE: file:exact_line reference. If documenting a constant, cite the exact line where that constant is defined, not the range of the whole file.

3. NEVER PARAPHRASE CONFIG/COMMENT TEXT:
   When extracting conditions, thresholds, or rules from config or code comments, extract the ACTUAL values from the code, not paraphrased natural language. BAD: 'validates that the model response is acceptable'. GOOD: 'asserts response is not None AND len(response) > 0 AND response != "ERROR"' (or mark as GAP if the actual assertion logic is in another file).

4. SINGLE OUTPUT DIRECTORY:
   Write your output file DIRECTLY to the WRITE-ONLY path. NEVER create subdirectories. The output path is: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_root_tests_scratch_01.md

---

BUSINESS RULE DECOMPOSITION FORMAT (MANDATORY)
===============================================
For every business rule found in the source code, use this exact structured format:

  RULE: <descriptive name>
  TRIGGER: <when — on function call / on script execution / on test run / scheduled / etc.>
  CONDITION: <exact expression with actual field names, operators, values>
  ACTION IF TRUE: <exact operations with field names>
  ACTION IF FALSE: <exact operations or "no action">
  ERROR: <code + exact message text, or "N/A">
  FIELDS INVOLVED: <list of every field read or written>
  CALLS: <decomposed inline — NOT just the function name>
  SOURCE: <file:line>

A business rule described only as prose MUST be rejected and rewritten in this structured format.

---

STRUCTURED GAP FORMAT (MANDATORY)
===================================
For every cross-reference or unresolved dependency, use this EXACT format:

  GAP_ID: GAP-cluster_root_tests_scratch_01-<seq_number>
  TYPE: CROSS_REFERENCE | MISSING_SOURCE | EXTERNAL_SYSTEM | CONFIG_DEPENDENCY
  FROM: <file>:<line> — <code_unit_name>
  EXPECTS: <what is needed — function signature, module interface, config value, etc.>
  LIKELY_LOCATION: <best guess of file/module where this is implemented>
  IMPACT: HIGH | MEDIUM | LOW — <why this gap matters for understanding the logic>
  SOURCE: <file>:<line>

Free-text GAP descriptions are FORBIDDEN. Every gap MUST use the structured format above.

---

FOLLOW-THE-CHAIN RULE
======================
When a code unit calls another function/method/class that contains business logic, the agent MUST NOT stop at the call boundary. It MUST:
1. Follow the call to the target function (even if in another file within the cluster).
2. Decompose the target function's logic inline or as a sub-section.
3. Document the parameters passed and return values.
4. If the target is OUTSIDE the cluster, document it as:
   "CROSS-REFERENCE: calls <function> in <file> — not in this cluster's scope, should be documented by another agent."

---

INLINE LOGIC DECOMPOSITION (CRITICAL)
======================================
Anonymous inner classes, lambdas, decorators, and inline callables often contain CORE BUSINESS LOGIC. The agent MUST:
- Extract the FULL logic body of every inline block (e.g., pytest fixtures, parametrize decorators, lambda transforms).
- Document every variable read/set, every method call, every conditional inside these blocks.
- NOT say "processes the exchange" or "runs the test" — instead list every assertion, every mocked call, every setup step, and every conditional branch.

---

SERVICE/FUNCTION METHOD RULE
=============================
For EVERY function, method, or script-level block in any utility, script, or test file:
- Document the EXACT operations performed (file I/O, API calls, model calls, PDF operations, etc.)
- Document EVERY parameter received and how it is used
- Document the return type and what data it contains
- Document error/exception handling with specific exception types
- If the function delegates to another function, follow the chain (FOLLOW-THE-CHAIN)

FORBIDDEN descriptions:
  'handles record processing' — WHAT records? WHAT processing?
  'manages model data' — WHAT operations?
  'processes the request' — WHAT fields? WHAT validations? WHAT response?
Each of these MUST be replaced with the actual operations from source code.

---

EXTRACTION INSTRUCTIONS BY CATEGORY
=====================================

### Category 5 — Business Rules
For each business rule embedded in the source files (including test assertions that encode expected system behavior, validation logic in utility scripts, conversion rules in PDF tools, model selection logic in list_models.py, and retry/fallback logic in scratch scripts):
- Use the BUSINESS RULE DECOMPOSITION FORMAT above for every rule.
- Pay special attention to: retry conditions (test_llm_retry.py), checklist health conditions (test_checklist_health.py), hyperparameter constraints (repro_hyperparams.py), RAG split thresholds (test_rag_split.py), section splitting conditions (test_section_splitter.py, tests/test_rag_logical_splitter.py), audit state transitions (tests/test_audit_state.py), and any validation in app.py or pdf_to_md.py / md_to_pdf.py.
- For test files: extract the IMPLICIT business rules encoded in each assertion (what the system MUST do, as proven by the test).

### Category 8 — API/Service Contracts and Batch Jobs
- Document every external API call (LLM APIs, embedding APIs, any HTTP calls): method, endpoint/model name, request payload fields with types, response fields with types, error codes, auth requirements.
- Document every CLI entry point (app.py, list_models.py, create_test_pdf.py, md_to_pdf.py, pdf_to_md.py): command-line arguments (name, type, required/optional, default), processing steps, output produced.
- Document any batch-like processing loops: input source, iteration logic, per-item processing steps, output destination, error handling per item.

### Category 9 — Constants, Enums, Lookup Tables (ACTUAL VALUES MANDATORY)
- List EVERY constant, enum value, magic string, magic number, and configuration literal found in ALL files.
- For each: constant name, actual value (e.g., `CHUNK_SIZE = 512`, `MODEL_NAME = "gpt-4o"`, `EMBED_DIM = 384`), purpose/usage context.
- SOURCE: file:exact_line for each constant.
- Do NOT write "has various constants" — list every single one by name and value.

### Category 10 — Transformations
- Document every data transformation: source field/format → target field/format, conversion logic step by step.
- Cover: PDF→Markdown conversion logic in pdf_to_md.py (what is extracted, how it is structured, what is discarded), Markdown→PDF conversion logic in md_to_pdf.py (what renderer/library is used, page settings, font settings, any filters applied), embedding transformations in test_embed.py / test_embed2.py (input text → vector, model used, output dimensionality), any text chunking/splitting transformations in RAG-related test files (input document → chunk list, splitting strategy, chunk size, overlap).

### Category 12 — Error Handling
- Document EVERY try/except block: exception type(s) caught, the exact code inside the except block (logging call with message text, fallback value assigned, re-raise, sys.exit code, etc.).
- Document every assertion failure scenario in test files: what condition triggers the failure, what AssertionError message is produced.
- Document retry logic: number of retries, wait interval (if any), condition to retry vs. give up, final action on exhaustion.
- Document any graceful degradation paths: what the system does when an external call fails.

---

OUTPUT STRUCTURE
================
Produce a single Markdown file with the following top-level sections. Include ALL subsections that apply based on what is actually found in the source code. Target 200–400 lines of structured Markdown, expanding as needed to achieve full fidelity — do NOT truncate to fit the line target.

```
# Extraction Report: cluster_root_tests_scratch_01
## Agent: ext_root_tests_scratch_01

## 1. File Index
(List every file read, with line count and one-line description of its purpose)

## 2. Dependencies & Configuration (requirements.txt)
(List every package with its pinned version and its role in the application)

## 3. Application Entry Point (app.py)
(CLI arguments, initialization steps, routing to sub-functions, exit codes)

## 4. PDF Utility Scripts
### 4.1 md_to_pdf.py
### 4.2 pdf_to_md.py
### 4.3 create_test_pdf.py

## 5. Model Listing CLI (list_models.py)

## 6. Business Rules (Category 5)
(One subsection per rule, using BUSINESS RULE DECOMPOSITION FORMAT)

## 7. API / Service Contracts & Batch Jobs (Category 8)
(One subsection per CLI entry point and per external API integration)

## 8. Constants, Enums, and Lookup Tables (Category 9)
(Full table: Name | Value | File | Line | Purpose)

## 9. Transformations (Category 10)
(One subsection per transformation pipeline)

## 10. Error Handling (Category 12)
(One subsection per try/except block or retry mechanism)

## 11. Test Suite Specifications
### 11.1 test_auditor_refactor.py (root)
### 11.2 test_imports.py (root)
### 11.3 test_skills_integration.py (root)
### 11.4 backend/scratch/test_embed.py
### 11.5 backend/scratch/test_embed2.py
### 11.6 scratch/check_st.py
### 11.7 scratch/patch_skills.py
### 11.8 scratch/repro_hyperparams.py
### 11.9 scratch/test_checklist_health.py
### 11.10 scratch/test_llm_retry.py
### 11.11 scratch/test_rag_split.py
### 11.12 tests/test_audit_state.py
### 11.13 tests/test_rag_logical_splitter.py
### 11.14 tests/test_section_splitter.py

## 12. Implicit Business Rules Encoded in Tests
(Every assertion that encodes a system requirement, in BUSINESS RULE DECOMPOSITION FORMAT)

## 13. Gaps & Cross-References
(Every GAP in STRUCTURED GAP FORMAT)
```

For each test file subsection (Section 11), document:
- Every test function/method: name, setup (fixtures used, mocks applied with exact mock targets), input values passed, assertion(s) checked (exact condition and expected value), teardown.
- Every pytest fixture: name, scope, what it creates/provides, exact return value or yield value.
- Every parametrize decorator: list ALL parameter sets with their actual values.

Do NOT collapse multiple test functions into a summary. Each test function gets its own documented entry.

---

FINAL CHECKLIST BEFORE WRITING OUTPUT
======================================
Before writing the output file, verify:
- [ ] Every extracted element has a `SOURCE: filename.py:line_number` reference.
- [ ] No invented functions, constants, or rules appear anywhere.
- [ ] Every cross-reference uses the STRUCTURED GAP FORMAT.
- [ ] Every business rule uses the BUSINESS RULE DECOMPOSITION FORMAT.
- [ ] No count approximations ("several", "multiple", "various") appear — only lists.
- [ ] The output file path starts with `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/`.
- [ ] No subdirectories were created.
- [ ] The output filename is exactly `extracted_root_tests_scratch_01.md`.