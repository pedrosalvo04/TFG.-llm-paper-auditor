PATH SANDBOX
============
READ-ONLY (source code): /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input
WRITE-ONLY (output dir): /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working

NEVER use relative paths — ALWAYS use the ABSOLUTE paths above.
NEVER write files to the current working directory (cwd).
NEVER create files outside the WRITE-ONLY path.
Before writing ANY file, verify the target path starts with the WRITE-ONLY path.

---

AGENT ID: ext_backend_core_01
OUTPUT FILE: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_core_01.md

Write your output file DIRECTLY to the WRITE-ONLY path. NEVER create subdirectories. The output path is: WRITE-ONLY/extracted_backend_core_01.md — NOT WRITE-ONLY/subfolder/extracted_backend_core_01.md

---

FILES TO READ
=============
Read each file using EXACTLY these absolute paths — do NOT modify, shorten, or re-base them:

1. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/__init__.py
2. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/common/config.py
3. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/common/llm_client.py
4. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/common/prompts.py
5. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/common/__init__.py
6. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/services/auditor.py
7. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/services/chatbot.py
8. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/services/pdf_parser.py
9. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/services/sota_analyzer.py
10. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/services/__init__.py
11. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/utils/logger.py
12. /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/utils/__init__.py

You MUST NOT access any path outside the READ-ONLY source root. You MUST NOT read from specs/, output/, or any Specs2Code-related paths.

---

SCOPE
=====
You are extracting the core backend infrastructure of a Python application called "LLM Paper Auditor Multimodels". This cluster covers:
- LLM client abstraction layer (multi-model support)
- Configuration management
- Prompt templates for LLM interactions
- Auditor service logic (academic paper auditing)
- Chatbot service
- PDF parsing service
- SOTA (State of the Art) analysis service
- Logging utilities

EXTRACTION CATEGORIES TO COVER (mandatory):
- Category 5: Constants, enums, lookup tables — with ACTUAL VALUES
- Category 8: API/Service contracts — method signatures, parameters, return types, error codes
- Category 10: Batch jobs / processing pipelines — trigger, input, processing steps, output, error handling
- Category 11: Security — roles, permissions, auth method, session handling
- Category 12: Error handling — every error code, message, exception type, recovery action, transaction boundaries

---

FIDELITY RULE (CRITICAL):
EXTRACT ONLY what the source code demonstrates exists. NEVER invent modules, tables, fields, functions, or business rules. If something is referenced but not implemented in this cluster's files, document it as a GAP with the reference location. Every extracted element MUST include a source reference (file:line or file:function).

HONESTY OVER COMPLETENESS (CRITICAL):
If a code unit (method, function, handler) contains NO substantive logic — only delegation, simple getters/setters, or boilerplate — document it as:
  DETAIL: DELEGATION_ONLY — calls <target> with <params>, no local logic.
  or: DETAIL: TRIVIAL — getter/setter for <field>, no business logic.
NEVER invent logic to fill gaps. NEVER describe what a method 'probably does' or 'would typically do'. If you cannot determine the actual behavior from the source code in scope, write:
  DETAIL: UNRESOLVABLE — source logic not available in this cluster's files.
  CROSS-REFERENCE: likely implemented in <file/module> based on <evidence>.
A correct UNRESOLVABLE is infinitely better than an invented description.

SOURCE REFERENCE FORMAT (MANDATORY):
Use this exact format for every source reference: `SOURCE: filename.py:line_number` or `SOURCE: filename.py:method_name`. Do NOT use bare inline references like `(file:line)` or unlabeled line numbers. The `SOURCE:` prefix is mandatory for traceability and automated validation.

---

LARGE FILE STRATEGY (CRITICAL — agents MUST NOT surrender):
Files with >200 LOC or >50KB MUST still be fully documented. Use this strategy:
1. SCAN: Read the full file to identify all code units (classes, methods, functions)
2. INDEX: List every code unit with its line range and one-line purpose
3. DECOMPOSE: For each code unit, extract its full logic using the DEPTH RULE below
4. If context limits approach, prioritize by this order:
   a) Business rules and validation logic — ALWAYS full detail
   b) Data operations (processing, transformations) — ALWAYS full detail
   c) Event handlers and state transitions — ALWAYS full detail
   d) UI layout/styling — structure + bindings, skip cosmetic properties
   e) Boilerplate/framework wiring — DELEGATION_ONLY notation
NEVER write 'file too complex' or 'too large to analyze'. NEVER skip methods because the file is big. If you genuinely cannot fit everything, document what you extracted AND list the code units you could not reach with their line ranges, marked as:
  INCOMPLETE: <method_name> at lines <range> — not extracted due to context limits.
  This is recoverable. 'Too complex to analyze' is NOT.

---

DEPTH RULE (CRITICAL):
Document EVERY code unit (function, method, class, handler) with its actual logic:
- NOT "processes the PDF" → instead: "reads bytes from <param>, calls <library_function> with <args>, extracts text page by page iterating over <range>, strips whitespace with <method>, returns concatenated string"
- NOT "calls the LLM" → instead: "constructs message list as [{'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': <input_param>}], sends to <model_name> via <client.method> with temperature=<value>, max_tokens=<value>, returns response.choices[0].message.content"
- NOT "validates input" → instead: "checks if <field> is None OR len(<field>) == 0, if true raises <ExceptionType>('<message>'), if false proceeds to <next_step>"
- NOT "has several configuration values" → instead: list EVERY constant: "OPENAI_API_KEY: read from env var 'OPENAI_API_KEY', default=None; MODEL_NAME: 'gpt-4', no default; MAX_TOKENS: 2000, type int"
- NOT "has error handling" → instead: "catches <ExceptionType> at line <N>, logs message '<exact_message_template>' via <logger_call>, returns <return_value_or_raises>"

The agent MUST trace every decision branch in processing logic. If a code unit has >50 lines of logic, the agent MUST still describe every significant branch — not summarize it.

---

SERVICE/DAO METHOD RULE:
For EVERY method in a Service, ServiceImpl, Business, DAO, or Repository class:
- Document the EXACT operations performed (LLM calls, file reads, parsing steps) with all parameters
- Document EVERY parameter received and how it is used
- Document the return type and what data it contains
- Document error/exception handling with specific exception types
- If the method delegates to another service, follow the chain (FOLLOW-THE-CHAIN)
FORBIDDEN descriptions for service methods:
  'handles record processing' — WHAT records? WHAT processing?
  'manages LLM interaction' — WHAT model? WHAT prompt? WHAT parameters?
  'processes the request' — WHAT fields? WHAT validations? WHAT response?
Each of these MUST be replaced with the actual operations from source code.

---

BUSINESS RULE DECOMPOSITION FORMAT:
For every business rule found in the source code, use this exact format:

  RULE: <descriptive name>
  TRIGGER: <when — on function call / on message received / on file upload / scheduled / etc.>
  CONDITION: <exact expression with actual field names, operators, values>
  ACTION IF TRUE: <exact operations with field names>
  ACTION IF FALSE: <exact operations or "no action">
  ERROR: <code + exact message text, or "N/A">
  FIELDS INVOLVED: <list of every field read or written>
  CALLS: <decomposed inline — NOT just the function name>
  SOURCE: <file:line>

This format is mandatory. A business rule described as prose ("validates that the audit is complete") MUST be rejected and rewritten in this structured format.

---

FOLLOW-THE-CHAIN RULE:
When a code unit calls another function/method that contains business logic, the agent MUST NOT stop at the call boundary. It MUST:
1. Follow the call to the target function (even if in another file within the cluster)
2. Decompose the target function's logic inline or as a sub-section
3. Document the parameters passed and return values
4. If the target is OUTSIDE the cluster, document it as:
   "CROSS-REFERENCE: calls <function> in <file> — not in this cluster's scope, should be documented by agent ext_backend_core_01 or the responsible agent"

---

INLINE LOGIC DECOMPOSITION (CRITICAL):
Anonymous inner functions, lambdas, closures, and inline callbacks often contain CORE BUSINESS LOGIC. The agent MUST:
- Extract the FULL logic body of every inline block
- Document every variable read/set, every method call, every conditional
- NOT say "processes the response" — instead list every key accessed in the response dict, every transformation applied, every conditional branch taken

---

STRUCTURED GAP FORMAT (MANDATORY):
Use this EXACT format for every cross-reference or unresolved dependency:

  GAP_ID: GAP-cluster_backend_core_01-<seq_number>
  TYPE: CROSS_REFERENCE | MISSING_SOURCE | EXTERNAL_SYSTEM | CONFIG_DEPENDENCY
  FROM: <file>:<line> — <code_unit_name>
  EXPECTS: <what is needed — function signature, config value, external API schema, etc.>
  LIKELY_LOCATION: <best guess of file/module where this is implemented>
  IMPACT: HIGH | MEDIUM | LOW — <why this gap matters for understanding the logic>
  SOURCE: <file>:<line>

Free-text GAP descriptions ("some functionality is defined elsewhere") MUST be rejected and rewritten in this structured format.

---

ANTI-SUMMARY RULES (CRITICAL):

1. NEVER COUNT — ALWAYS LIST:
   NEVER write '45+ services', '220 queries identified', 'several validators', 'multiple endpoints', or any count/approximation. Instead LIST EVERY SINGLE ONE by name. If there are 45 services, list all 45. If there are 220 queries, list all 220 (name + purpose + source). Counting is FORBIDDEN — listing is mandatory.

2. NEVER USE GENERIC SOURCE RANGES:
   NEVER write SOURCE: file:1-1800 or SOURCE: file:6-96 as a range covering a whole file or section. Each extracted element MUST have its OWN specific SOURCE: file:exact_line reference. If documenting a configuration constant, cite the exact line where that constant is defined, not the range of the whole file.

3. NEVER PARAPHRASE CONFIG/PROMPT COMMENTS:
   When extracting configuration values, prompt templates, or rules from Python source, extract the ACTUAL values from the code, not paraphrased descriptions.
   BAD: 'sets up the LLM with appropriate parameters'
   GOOD: 'instantiates OpenAI client with api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4", temperature=0.2, max_tokens=4096'

4. SINGLE OUTPUT DIRECTORY:
   Write your output file DIRECTLY to the WRITE-ONLY path. NEVER create subdirectories. The output path is: WRITE-ONLY/extracted_backend_core_01.md — NOT WRITE-ONLY/subfolder/extracted_backend_core_01.md

---

WHAT TO EXTRACT — DETAILED INSTRUCTIONS PER CATEGORY
=====================================================

### CATEGORY 5 — Constants, Enums, Lookup Tables (with ACTUAL VALUES)

For every constant, enum, configuration value, or lookup structure found in ANY of the 12 files:
- Name of the constant/enum
- Exact Python type (str, int, float, bool, Enum, dict, list, etc.)
- ACTUAL value(s) as written in source — not paraphrased
- Where it is used (which functions reference it)
- Whether it is overridable via environment variable or constructor parameter
- SOURCE: file:line

For `config.py` specifically:
- List EVERY configuration key
- Document the exact source (os.environ.get / os.getenv / hardcoded / class attribute)
- Document the environment variable name (exact string)
- Document the default value (exact value or None)
- Document the type cast if any (int(), float(), bool(), etc.)

For `prompts.py` specifically:
- Extract EVERY prompt template in full — do not truncate, do not summarize
- Document every placeholder/variable inside each template (e.g., {paper_text}, {question})
- Document which service/function uses each prompt template
- SOURCE: prompts.py:line

### CATEGORY 8 — API/Service Contracts

For EVERY class and EVERY method/function in the service files (auditor.py, chatbot.py, pdf_parser.py, sota_analyzer.py) and common files (llm_client.py):
- Class name, parent class (if any), constructor parameters with types and defaults
- Method name
- Parameters: name, type annotation (if present), default value, how the parameter is used inside the method
- Return type annotation (if present), actual returned value/structure
- LLM model name used (exact string value)
- LLM call parameters: temperature, max_tokens, top_p, or any other kwargs passed
- Prompt construction: which prompt template from prompts.py is used, how variables are injected
- Whether the method is synchronous or asynchronous (async def vs def)
- Any decorators present
- SOURCE: file:method_name

For `llm_client.py` specifically:
- Document the abstraction pattern: is it a class, a function factory, a singleton?
- Document every supported LLM provider/model (list each one by name as it appears in code)
- Document the routing logic: how does the client decide which provider/model to call?
- Document the exact API call structure for each provider
- Document retry logic, timeout logic, or fallback logic if present

### CATEGORY 10 — Processing Pipelines / Batch Jobs

For every multi-step processing pipeline (e.g., PDF upload → parse → audit → return result):
- Entry point: function name, file, line
- Step 1 → Step 2 → ... → Step N with:
  - What data is passed between steps (exact variable names and types)
  - What transformation happens at each step (exact operations)
  - What conditions branch the pipeline into alternative paths
  - What is the final output (exact structure)
- Error handling at each step: what exception is caught, what happens on failure
- SOURCE: file:line for each step

For `pdf_parser.py` specifically:
- Document the exact library used for PDF parsing (PyPDF2, pdfplumber, pymupdf, etc.)
- Document how the parsed text is cleaned/preprocessed (exact string operations)
- Document what is returned: raw text, structured dict, list of pages, etc.
- Document handling of: empty PDFs, corrupted files, password-protected PDFs, multi-page docs

For `auditor.py` specifically:
- Document the full audit pipeline step by step
- Document every criterion or dimension that is audited (list each one by name as it appears in code)
- Document how audit results are structured (fields, scores, labels)
- Document how the final audit report is assembled

For `sota_analyzer.py` specifically:
- Document what "SOTA analysis" means operationally in this codebase
- Document every step: what input is taken, what LLM calls are made, what is compared/evaluated
- Document the output structure of the SOTA analysis result

For `chatbot.py` specifically:
- Document conversation history management: how is history stored, what is its structure, max length if any
- Document the exact message format sent to the LLM on each turn
- Document how context (e.g., the paper content) is injected into the conversation

### CATEGORY 11 — Security

- Document any authentication or authorization logic present in these files
- Document any API key handling: where keys are loaded, how they are stored in memory, whether they are logged
- Document any input sanitization before passing user content to LLM calls
- Document any rate limiting, quota checking, or usage throttling
- If NO security logic is present in this cluster, state explicitly: "No authentication/authorization logic found in this cluster. SOURCE: [list files checked]"

### CATEGORY 12 — Error Handling

For EVERY try/except block in ALL 12 files:
- The exact exception type(s) caught
- The exact operations in the try block
- The exact operations in the except block (log call with message template, re-raise, return value)
- Whether the exception is re-raised, swallowed, or transformed into another exception
- Any finally block operations
- SOURCE: file:line

For EVERY raise statement:
- The exception type raised
- The exact message string (including any f-string template with variable names)
- The condition that triggers the raise
- SOURCE: file:line

For `logger.py` specifically:
- Document the logger name(s) configured
- Document the log level(s) configured
- Document the log format string (exact format)
- Document the handler(s) configured (StreamHandler, FileHandler, etc.)
- Document whether log output goes to stdout, stderr, or a file
- Document any log rotation configuration
- SOURCE: logger.py:line

---

OUTPUT FORMAT REQUIREMENTS
===========================

Produce a single structured Markdown file with the following top-level sections (use ## for sections, ### for subsections, #### for individual items):

```
# Extraction Report — Agent ext_backend_core_01
## Cluster: cluster_backend_core_01
## Scope: Core backend infrastructure (Python)

## 1. File Index
## 2. Constants, Enums, and Configuration Values (Category 5)
   ### 2.1 config.py — All Configuration Keys
   ### 2.2 prompts.py — All Prompt Templates (full text)
   ### 2.3 Other Constants (per file)
## 3. API and Service Contracts (Category 8)
   ### 3.1 LLM Client (llm_client.py)
   ### 3.2 Auditor Service (auditor.py)
   ### 3.3 Chatbot Service (chatbot.py)
   ### 3.4 PDF Parser Service (pdf_parser.py)
   ### 3.5 SOTA Analyzer Service (sota_analyzer.py)
## 4. Processing Pipelines (Category 10)
   ### 4.1 PDF Parse Pipeline
   ### 4.2 Audit Pipeline
   ### 4.3 SOTA Analysis Pipeline
   ### 4.4 Chatbot Conversation Pipeline
## 5. Security (Category 11)
## 6. Error Handling (Category 12)
   ### 6.1 Logger Configuration
   ### 6.2 Exception Handling per File
## 7. Business Rules
## 8. Gaps and Cross-References
## 9. Incomplete Extractions (if any)
```

Target output size: 200–400 lines of structured Markdown. If the source code warrants more detail, exceed this limit rather than omit logic. Never pad with summaries to reach the minimum.

---

EXECUTION INSTRUCTIONS
======================

1. Read ALL 12 files listed under FILES TO READ using their exact absolute paths.
2. For each file, perform a full SCAN → INDEX → DECOMPOSE pass as described in LARGE FILE STRATEGY.
3. Extract all elements relevant to Categories 5, 8, 10, 11, and 12 plus any business rules found.
4. Apply ALL formatting rules: BUSINESS RULE DECOMPOSITION FORMAT, STRUCTURED GAP FORMAT, SOURCE: prefix on every element.
5. Apply ALL anti-summary rules: list every item, never count, never use range source references, never paraphrase prompt text.
6. Write the final output as a single Markdown file to:
   /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_core_01.md
7. Verify before writing that the output path starts with:
   /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working