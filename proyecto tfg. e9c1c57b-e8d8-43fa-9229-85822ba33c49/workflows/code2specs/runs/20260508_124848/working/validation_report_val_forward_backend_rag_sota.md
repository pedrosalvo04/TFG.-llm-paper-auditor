---
validator_id: val_forward_backend_rag_sota
validator_type: forward_coverage
target_specs: [02_functional_backend.md]
forward_coverage_pct: 42
backward_coverage_pct: N/A
depth_pct: 55
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 32
coverage_gaps: 0
depth_gaps: 15
spec_consistency_issues: 2
total_issues: 49
overall_status: fail
---

## Summary

Validation was performed against all 8 in-scope components (HybridHyperparameterExtractionSkill, SemanticScholarSearchSkill, CrossValidationSkill, QueryGenerationSkill, CoverageGapAnalysisSkill, LLMClient, PDFParser, and Regex Detection Skills / NegationWindow), verified claim-by-claim against the corresponding source files (`rag_extraction_skill.py`, `sota_skills.py`, `llm_client.py`, `pdf_parser.py`, `regex_detection_skills.py`, `config.py`). The spec provides thorough coverage of all 8 components with detailed pseudocode, tables, and formulas, which is a significant strength. However, 32 fidelity issues were found, including critical discrepancies in the HybridHyperparameterExtractionSkill chunking algorithm, relevance scoring formula, ChromaDB collection name, and query call parameters; the CrossValidationSkill, QueryGenerationSkill, and CoverageGapAnalysisSkill have completely wrong input context keys and guard conditions; and the LLMClient's constructor signature, `generate()` signature, and return type all differ substantially from source. The overall forward coverage is 42% with 49 total issues, which results in a **fail** status.

---

## Forward Coverage (Specs → Source)

| Spec Element | Component | Source Reference | Verified? | Status | Notes |
|---|---|---|---|---|---|
| batch_size = 15 for embeddings | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:61` | Yes | VERIFIED | `batch_size = 15` confirmed |
| inter_batch_sleep = 15 seconds | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:67` | Yes | VERIFIED | `time.sleep(15)` confirmed |
| ChromaDB in-memory client | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:85` | Yes | VERIFIED | `chromadb.Client()` (no persistence) |
| delete + create collection before use | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:86-90` | Yes | VERIFIED | delete_collection then create_collection |
| 13 fixed queries (count) | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:99-113` | Yes | VERIFIED | Exactly 13 query strings present |
| Inter-chunk LLM sleep = 1 second | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:199` | Yes | VERIFIED | `time.sleep(1)` confirmed |
| Guard condition: falsy paper_text | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:31-32` | Partial | FIDELITY_ISSUE | Guard exists but returns `{'extracted_hyperparameters_hybrid': {}}`, not `{"success": False, "error": "No paper text in context", "phase": "hyperparameter_extraction"}` as spec claims |
| Chunking: chunk_size=1000, overlap=200 while loop | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:43-47` | No | FIDELITY_ISSUE | Spec claims a `chunk_text(chunk_size=1000, overlap=200)` while loop. Actual code: `re.split(r'\n\n+', paper_text_norm)` with filter `len > 10`. No character-based chunking. |
| ChromaDB collection name: "hyperparams" | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:90` | No | FIDELITY_ISSUE | Spec says `"hyperparams"`. Actual: `"paper_chunks"`. |
| Query call: `query_texts=[query]`, `n_results=3` | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:115-124` | No | FIDELITY_ISSUE | Spec says `collection.query(query_texts=[query], n_results=3)` (one query at a time). Actual: all 13 query embeddings sent at once via `query_embeddings=query_embeddings`, `n_results=10`. |
| 13 query strings (§3.5 Step 4 list) | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:99-113` | No | FIDELITY_ISSUE | Spec lists 13 strings starting with "learning rate optimizer training configuration". Actual strings are completely different (e.g., "training details optimization hyperparameters"). All 13 strings differ. |
| Relevance scoring: piecewise linear, thresholds 0.3/0.7/1.2, returns 0.0–1.0 | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:152-157` | No | FIDELITY_ISSUE | Spec claims 4-range formula (≤0.3→1.0, ≤0.7→linear to 0.5, ≤1.2→linear to 0.1, else→0.0). Actual: 3-range formula returning integer 0–100 (distance<0.4→int(95-distance*25); distance<0.7→int(85-(distance-0.4)*180); else→max(5, int(31-(distance-0.7)*50))). Breakpoints and scale are both wrong. |
| Merge strategy: last-write-wins for hyperparameter_results | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:204-261` | No | FIDELITY_ISSUE | Spec §3.5 Step 7 says "last chunks overwrite earlier chunks for the same key". Actual is a full LLM REDUCE phase with a structured prompt consolidating fragments. No last-write-wins logic. |
| Output context key: `hyperparameter_results` | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:268-271` | No | FIDELITY_ISSUE | Spec says output key is `hyperparameter_results`. Actual key is `extracted_hyperparameters_hybrid` (also returns `triage_fragments`). |
| Return shape: `{"success": True, "hyperparameter_results": dict}` | HybridHyperparameterExtractionSkill | `rag_extraction_skill.py:268-271` | No | FIDELITY_ISSUE | Actual: `{'extracted_hyperparameters_hybrid': cleaned_data, 'triage_fragments': extracted_fragments}`. No `success` key. Different structure. |
| Semantic Scholar endpoint URL | SemanticScholarSearchSkill | `config.py:136` | Yes | VERIFIED | `SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"` |
| Fields: `"paperId,title,authors,year,citationCount,abstract,url"` | SemanticScholarSearchSkill | `config.py:139` | Yes | VERIFIED | `SEMANTIC_SCHOLAR_FIELDS` matches spec claim |
| Year range: `"2023-2026"` | SemanticScholarSearchSkill | `config.py:137` | Yes | VERIFIED | `SEMANTIC_SCHOLAR_YEAR_RANGE = "2023-2026"` |
| limit = 5 | SemanticScholarSearchSkill | `config.py:138` | Yes | VERIFIED | `SEMANTIC_SCHOLAR_LIMIT = 5` |
| Deduplication by paperId | SemanticScholarSearchSkill | `sota_skills.py:227` | Yes | VERIFIED | `{p['paperId']: p for p in sota_papers}` |
| Auth: None (public API, unauthenticated) | SemanticScholarSearchSkill | `sota_skills.py:182-185` | No | FIDELITY_ISSUE | Spec says "None (public API, unauthenticated)". Actual: `if SEMANTIC_SCHOLAR_API_KEY: headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY`. API key is optionally injected. GAP marker exists in spec but the surrounding text is still misleading. |
| Rate limiting: no explicit handling; relies on LLMClient retry | SemanticScholarSearchSkill | `sota_skills.py:191, 215-217` | No | FIDELITY_ISSUE | Spec says "No explicit rate limit handling in skill; relies on HTTP 429 retry in LLMClient". Actual: `time.sleep(0.5)` between queries AND `time.sleep(2)` on HTTP 429. Explicit handling exists. |
| Top-N selection (no mention in spec) | SemanticScholarSearchSkill | `sota_skills.py:227-233` | No | FIDELITY_ISSUE | Spec describes dedup by paperId only. Actual also sorts by `citationCount` descending and takes top 10 (`[:10]`). This behavior is not documented in the spec. |
| Required input keys: `sota_papers`, `checklist`, `extracted_info` | CrossValidationSkill | `sota_skills.py:319-321` | No | FIDELITY_ISSUE | Spec §11 says required: `sota_papers`, `checklist`, `extracted_info`. Actual `validate_context` checks: `['paper_text', 'sota_papers', 'thematic_data']`. No `checklist` or `extracted_info` in required keys. |
| Guard: falsy `sota_papers` OR falsy `checklist` | CrossValidationSkill | `sota_skills.py:319-331` | No | FIDELITY_ISSUE | Spec guard checks `sota_papers` and `checklist`. Actual guards on `paper_text`, `sota_papers`, `thematic_data`. No `checklist` guard. |
| Output key: `cross_validation_results` | CrossValidationSkill | `sota_skills.py:422` | No | FIDELITY_ISSUE | Spec says output key `cross_validation_results`. Actual: `{'validation_results': validation_results}`. Different key. |
| Output key: `unsupported_claims_count` (int) | CrossValidationSkill | `sota_skills.py:422` | No | FIDELITY_ISSUE | Spec claims output key `unsupported_claims_count`. Not present in actual output. |
| Required input keys: `themes`, `keywords`, `research_area` | QueryGenerationSkill | `sota_skills.py:107` | No | FIDELITY_ISSUE | Spec §11 says required: `themes`, `keywords`, `research_area`. Actual `validate_context` checks: `['paper_text', 'thematic_data']`. Completely different keys. |
| Guard: falsy `themes` | QueryGenerationSkill | `sota_skills.py:107-112` | No | FIDELITY_ISSUE | Spec says "if `context.get('themes')` is falsy". Actual guards on `paper_text` and `thematic_data`. |
| Output key: `search_queries` (list[str]) | QueryGenerationSkill | `sota_skills.py:148` | Yes | VERIFIED | `return {'search_queries': queries}` |
| 3–5 search queries generated | QueryGenerationSkill | `sota_skills.py:129` | Yes | VERIFIED | Prompt instructs "Genera 3 búsquedas", so 3 queries produced |
| Required input keys: `sota_papers`, `extracted_info`, `paper_text` | CoverageGapAnalysisSkill | `sota_skills.py:256` | No | FIDELITY_ISSUE | Spec says required: `sota_papers`, `extracted_info`, `paper_text`. Actual `validate_context`: `['paper_text', 'thematic_data']`. No `sota_papers` or `extracted_info`. |
| Guard: falsy or empty `sota_papers` | CoverageGapAnalysisSkill | `sota_skills.py:256` | No | FIDELITY_ISSUE | Spec says guard fires on `sota_papers`. Actual guards on `paper_text` and `thematic_data`. |
| Output key: `coverage_gaps` exists | CoverageGapAnalysisSkill | `sota_skills.py:294-295` | Yes | VERIFIED | Output key `coverage_gaps` present |
| Output schema: `{gap_description, severity, related_papers}` | CoverageGapAnalysisSkill | `sota_skills.py:269-288` | No | FIDELITY_ISSUE | Spec says list of `{gap_description: str, severity: str, related_papers: list[str]}`. Actual LLM prompt returns `{"areas_debiles": [{"subtema": ..., "diagnostico": ...}]}`. Completely different schema. |
| Output key: `sota_comparison_summary` (str) | CoverageGapAnalysisSkill | `sota_skills.py:294-295` | No | FIDELITY_ISSUE | `sota_comparison_summary` not present in actual output. Actual only has `coverage_gaps`. |
| Constructor: `max_retries: int = 5`, `base_delay: float = 2.0`, `api_key` as params | LLMClient | `llm_client.py:11` | No | FIDELITY_ISSUE | Spec claims constructor signature `__init__(self, model_name, api_key, max_retries=5, base_delay=2.0)`. Actual: `__init__(self, model_name=None, generation_config=None)`. `max_retries` and `base_delay` are local variables in `generate()`, not constructor params. |
| `genai.configure(api_key)` + `genai.GenerativeModel(model_name)` | LLMClient | `llm_client.py:23` | No | FIDELITY_ISSUE | Spec claims legacy API. Actual uses `genai.Client(api_key=GOOGLE_API_KEY)`. Different genai SDK usage pattern. |
| `generate(prompt, config, history)` signature | LLMClient | `llm_client.py:30` | No | FIDELITY_ISSUE | Spec says 3 params (`prompt`, `config`, `history`). Actual: only `prompt`. Configuration is set at construction via `self.generation_config`. No `history` param. |
| generate() returns str | LLMClient | `llm_client.py:49` | No | FIDELITY_ISSUE | Spec says returns `str`. Actual returns `response` object (full `GenerateContentResponse`). Skills must access `.text` on the returned value. |
| Retry loop: `range(6)` attempts | LLMClient | `llm_client.py:42` | Yes | VERIFIED | `for attempt in range(max_retries + 1)` where `max_retries=5` → `range(6)` |
| Delay formula: `base_delay * (2**attempt) + random.uniform(0,1)` | LLMClient | `llm_client.py:58` | Yes | VERIFIED | Formula confirmed |
| Retryable codes: "503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED" | LLMClient | `llm_client.py:54` | Yes | VERIFIED | All 5 codes confirmed; checked with `error_msg.upper()` |
| Sleep position: before LLM call (`if attempt > 0: sleep`) | LLMClient | `llm_client.py:56-69` | No | FIDELITY_ISSUE | Spec says sleep is at start of loop iteration. Actual: sleep is INSIDE the except block, after a failed attempt, before the loop continues. Functionally equivalent but structurally different from spec description. |
| `convert_pdf_to_markdown(pdf_path, chunk_size: int = 5)` signature | PDFParser | `pdf_parser.py:7` | No | FIDELITY_ISSUE | Spec claims `chunk_size` is a function parameter with default=5. Actual signature: `convert_pdf_to_markdown(pdf_path)`. `chunk_size = 5` is a hardcoded local variable, not a parameter. |
| Library: Docling `DocumentConverter` | PDFParser | `pdf_parser.py:3,39` | Yes | VERIFIED | `from docling.document_converter import DocumentConverter` |
| PdfReader / PdfWriter for page chunking | PDFParser | `pdf_parser.py:23,46,59` | Yes | VERIFIED | `pypdf.PdfReader`, `pypdf.PdfWriter` |
| chunk_size = 5 pages per block | PDFParser | `pdf_parser.py:51` | Yes | VERIFIED | `chunk_size = 5 # Procesar de 5 en 5 páginas` |
| Temp file creation with suffix=".pdf" | PDFParser | `pdf_parser.py:63-65` | Yes | VERIFIED | `tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")` |
| Error notice format: HTML comment `<!-- Error ... -->` | PDFParser | `pdf_parser.py:75` | No | FIDELITY_ISSUE | Spec says HTML comment. Actual: Markdown blockquote `> [!ERROR] Error al procesar páginas ...`. Different format. |
| File-not-found: exception propagates to caller | PDFParser | `pdf_parser.py:83-85` | No | FIDELITY_ISSUE | Spec says exception propagates. Actual outer `except Exception as e` catches ALL errors (including file not found) and returns `f"❌ Error en la extracción del PDF: {str(e)}"` — a string, not an exception. |
| Chunks assembled with `"\n\n".join()` | PDFParser | `pdf_parser.py:71` | Yes | VERIFIED | Equivalent: `full_md_text += block_md + "\n\n"` produces same result (trailing `\n\n` minor difference) |
| NEGATION_WINDOW = 60 | Regex / NegationWindow | `regex_detection_skills.py:8` | Yes | VERIFIED | Exact value confirmed |
| NEGATION_PATTERNS (full regex string) | Regex / NegationWindow | `regex_detection_skills.py:10-18` | Yes | VERIFIED | All 6 alternation branches match spec exactly |
| `_search_with_negation` returns list of all non-negated matches | Regex / NegationWindow | `regex_detection_skills.py:28-35` | No | FIDELITY_ISSUE | Spec describes return type as list (collects all matches). Actual: `Optional[re.Match]` — returns only the FIRST non-negated match, or `None`. Single-match semantics, not list semantics. |
| TableExtractionHelper uses simplified TABLE_PATTERNS list | Regex / NegationWindow | `regex_detection_skills.py:47-69` | No | FIDELITY_ISSUE | Spec §10.0 shows simplified patterns: `r'Table\s+\d+\s*[:\.]'`, `r'^\|.+\|.+\|'`, `r'^\t.+\t'`. Actual patterns are more specific: table_pattern includes 2000-char lookahead, pipe_table requires 3+ rows `(\|[^\n]+\|\n){3,}`, tab_table requires 3+ rows with 2+ tabs. Not equivalent to spec's simplified versions. |
| AUDIT_CONFIG values | LLMClient / Config | `config.py:116-122` | Yes | VERIFIED | `{"response_mime_type": "application/json", "temperature": 0.0, "top_k": 1, "top_p": 0.1, "max_output_tokens": 16384}` |
| CHAT_CONFIG temperature = 0.2 | Config | `config.py:125-127` | Yes | VERIFIED | `CHAT_CONFIG = {"temperature": CHAT_TEMPERATURE}` where `CHAT_TEMPERATURE = 0.2` |
| SOTA_CONFIG = JSON + temperature 0.1 | Config | `config.py:130-133` | Yes | VERIFIED | `SOTA_CONFIG = {"response_mime_type": "application/json", "temperature": SOTA_TEMPERATURE}` where `SOTA_TEMPERATURE = 0.1` |

---

## Depth Validation

| Spec Element | Component | Has Structured Decomposition | Detail Level | Missing Elements |
|---|---|---|---|---|
| Chunking algorithm (§3.5 Step 1) | HybridHyperparameterExtractionSkill | Yes (pseudocode) | NONE | Algorithm is wholly wrong; the spec describes a character-based while-loop not present in source |
| Embedding batching (§3.5 Step 2) | HybridHyperparameterExtractionSkill | Yes (pseudocode) | PARTIAL | Batch_size and sleep correct; API call abstracted as `batchEmbedContents()` when actual uses `httpx.post()` with JSON body |
| ChromaDB population (§3.5 Step 3) | HybridHyperparameterExtractionSkill | Yes (pseudocode) | PARTIAL | Collection name wrong; missing the delete-before-create step |
| Query call & n_results (§3.5 Step 4) | HybridHyperparameterExtractionSkill | Yes (pseudocode) | NONE | Wrong params (`query_texts` vs `query_embeddings`, `n_results=3` vs `10`), queries single not batched |
| 13 query strings | HybridHyperparameterExtractionSkill | Yes (enumerated list) | NONE | All 13 strings are incorrect |
| Relevance scoring formula (§3.5 Step 5) | HybridHyperparameterExtractionSkill | Yes (pseudocode with formula) | NONE | Formula breakpoints and scale both wrong; returns float 0–1 in spec vs integer 0–100 actual |
| Guard return shape (§3.4) | HybridHyperparameterExtractionSkill | Yes (RULE/TRIGGER/CONDITION/ACTION) | PARTIAL | Condition correct; ACTION return shape wrong |
| Output key and structure (§3.6/3.7) | HybridHyperparameterExtractionSkill | Yes (table + code block) | NONE | Key name and overall shape wrong |
| API authentication (§11) | SemanticScholarSearchSkill | Partial (note + GAP) | PARTIAL | GAP marker present but surrounding text falsely states "unauthenticated" |
| Rate limiting (§11) | SemanticScholarSearchSkill | Prose description | NONE | Describes no handling; actual has sleep(0.5) + sleep(2) on 429 |
| Top-N selection / sort (§11) | SemanticScholarSearchSkill | Not present | NONE | Missing: sorted by citationCount desc, top-10 cap |
| Input context keys (§11) | CrossValidationSkill | Table | NONE | All three required keys are wrong |
| Guard condition (§11) | CrossValidationSkill | RULE form | NONE | Wrong keys specified |
| Output keys + schema (§11) | CrossValidationSkill | Table | NONE | Key name wrong, unsupported_claims_count absent |
| Input context keys (§11) | QueryGenerationSkill | Table | NONE | Uses `themes`, `keywords` instead of `paper_text`, `thematic_data` |
| Input context keys (§11) | CoverageGapAnalysisSkill | Table | NONE | All required keys wrong |
| Output schema (§11) | CoverageGapAnalysisSkill | Table | NONE | Field names and structure wrong |
| sota_comparison_summary (§11) | CoverageGapAnalysisSkill | Table | NONE | Not produced by actual skill |
| LLMClient constructor (§15.2) | LLMClient | Code block | NONE | Wrong parameter names and defaults |
| generate() signature (§15.3) | LLMClient | Code block | NONE | `config` and `history` params not present in actual |
| generate() return type (§15.3) | LLMClient | Documented as `str` | NONE | Actual returns response object |
| Sleep position in retry (§15.4) | LLMClient | Pseudocode | PARTIAL | Timing of sleep described at wrong position in loop |
| Retry logic (§15.4–15.7) | LLMClient | FULL pseudocode | FULL | Delay formula, retry count, retryable codes all correct |
| chunk_size parameter (§14.1) | PDFParser | Function signature | PARTIAL | Documented as parameter; actually a local variable |
| Error notice format (§14.5) | PDFParser | Prose | PARTIAL | Format differs (HTML comment vs Markdown blockquote) |
| File-not-found propagation (§14.5) | PDFParser | Table | NONE | Spec says propagate; actual catches and returns error string |
| NEGATION_WINDOW (§10) | Regex / NegationWindow | Constant with comment | FULL | Exact value and semantics correct |
| NEGATION_PATTERNS (§10) | Regex / NegationWindow | Regex string | FULL | All 6 alternation branches verified |
| _search_with_negation return type (§10) | Regex / NegationWindow | Pseudocode | PARTIAL | Return described as list; actual is Optional[re.Match] |
| TABLE_PATTERNS (§10.0) | Regex / NegationWindow | Code block | PARTIAL | Simplified patterns shown, not actual complex regexes |

---

## Fidelity Issues

**F01 — HybridHP Guard return shape (§3.4)**
Claim: guard returns `{"success": False, "error": "No paper text in context", "phase": "hyperparameter_extraction"}`.
Actual (rag_extraction_skill.py:31-32): `return {'extracted_hyperparameters_hybrid': {}}`. No `success`, `error`, or `phase` keys.
Impact: Callers expecting the error shape documented in the spec will be broken.

**F02 — HybridHP Chunking algorithm (§3.5 Step 1)**
Claim: `FUNCTION chunk_text(paper_text, chunk_size=1000, overlap=200)` with a character-count while loop.
Actual (rag_extraction_skill.py:43-47): `re.split(r'\n\n+', paper_text_norm)` then filter `len > 10`. No character limits, no overlap. A reimplementation following the spec would produce fundamentally different chunking behavior (fixed-size character blocks vs paragraph-level semantic blocks).

**F03 — HybridHP ChromaDB collection name (§3.5 Step 3)**
Claim: collection name is `"hyperparams"`.
Actual (rag_extraction_skill.py:87,90): collection named `"paper_chunks"`. Additionally, spec omits the delete-before-create step (`chroma_client.delete_collection("paper_chunks")`).

**F04 — HybridHP Query call parameters (§3.5 Step 4)**
Claim: `collection.query(query_texts=[query], n_results=3)` — one query at a time, using text strings, returning 3 results.
Actual (rag_extraction_skill.py:115-124): Generates embeddings for all 13 queries simultaneously via `self.llm_client.client.models.embed_content(model=..., contents=queries)`, then `collection.query(query_embeddings=query_embeddings, n_results=10)`. Uses `query_embeddings` (not `query_texts`), batched (not one-at-a-time), and `n_results=10` (not 3).

**F05 — HybridHP Query strings (§3.5 Step 4)**
Claim: Lists 13 query strings starting with `"learning rate optimizer training configuration"`, `"batch size training epochs iterations"`, etc.
Actual (rag_extraction_skill.py:99-113): All 13 strings are different (e.g., `"training details optimization hyperparameters"`, `"learning rate schedule step size warmup decay learning rate"`, etc.).

**F06 — HybridHP Relevance scoring formula (§3.5 Step 5)**
Claim: Piecewise function with thresholds 0.3, 0.7, 1.2 returning float 0.0–1.0. Formula: `1.0 - (distance - 0.3)/(0.7 - 0.3) * 0.5` for middle range.
Actual (rag_extraction_skill.py:152-157): 3-range formula: `distance < 0.4` → `int(95 - distance*25)`, `distance < 0.7` → `int(85 - (distance-0.4)*180)`, else → `max(5, int(31-(distance-0.7)*50))`. Returns integer 0–100, not float 0–1. Thresholds differ (0.4 vs 0.3). Only chunks with relevance_score > 0 included — spec says `score > 0.0` but actual uses the integer scale making this threshold always 5+ (never 0 in practice).

**F07 — HybridHP Merge strategy (§3.5 Step 7)**
Claim: "All per-chunk extraction results are merged ... Merge strategy: later chunks overwrite earlier chunks for the same key (last-write-wins)."
Actual (rag_extraction_skill.py:204-261): A full LLM REDUCE phase with a structured prompt that instructs the LLM to consolidate all fragments. No deterministic last-write-wins logic.

**F08 — HybridHP Output key (§3.6/3.7)**
Claim: Output context key is `hyperparameter_results`; return shape `{"success": True, "hyperparameter_results": dict}`.
Actual (rag_extraction_skill.py:268-271): Return is `{'extracted_hyperparameters_hybrid': cleaned_data, 'triage_fragments': extracted_fragments}`. No `success` key, different field names.

**F09 — SS Auth claim (§11)**
Claim: "Auth: None (public API, unauthenticated)".
Actual (sota_skills.py:182-185, config.py:31): `if SEMANTIC_SCHOLAR_API_KEY: headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY`. The skill optionally authenticates with an API key from environment. Although a GAP marker exists, the surrounding prose is still false.

**F10 — SS Rate limiting (§11)**
Claim: "No explicit rate limit handling in skill; relies on HTTP 429 retry in LLMClient."
Actual (sota_skills.py:191,215-217): `time.sleep(0.5)` between all queries, plus a dedicated `elif response.status_code == 429: time.sleep(2)` handler. Explicit rate-limit handling exists independently of LLMClient.

**F11 — SS Top-N selection absent from spec (§11)**
Claim: Results deduplicated by paperId, no sort mentioned, no limit beyond API `limit=5`.
Actual (sota_skills.py:227-232): After dedup, results are sorted by `citationCount` descending and capped at 10 (`[:10]`). This data-selection step (top-10 by citation count, across all queries) is absent from the spec entirely.

**F12 — CrossValidation Required input keys (§11)**
Claim: Required: `sota_papers`, `checklist`, `extracted_info`.
Actual (sota_skills.py:319): `validate_context(context, ['paper_text', 'sota_papers', 'thematic_data'])`. No `checklist`, no `extracted_info`. `paper_text` and `thematic_data` not in spec's list.

**F13 — CrossValidation Guard condition (§11)**
Claim: Guard fires if `sota_papers` or `checklist` is falsy.
Actual (sota_skills.py:319-331): Guard fires on `paper_text`, `sota_papers`, `thematic_data`. No `checklist` check.

**F14 — CrossValidation Output key (§11)**
Claim: Output key `cross_validation_results`.
Actual (sota_skills.py:422): Output key is `validation_results`. Different name.

**F15 — CrossValidation `unsupported_claims_count` (§11)**
Claim: Output includes `unsupported_claims_count: int`.
Actual: No such key in `validation_results`. The structure contains `papers_omitidos`, `conclusion_sota`, `cobertura_tematica`, `papers_analizados`.

**F16 — QueryGeneration Required input keys (§11)**
Claim: Required: `themes`, `keywords`, optional `research_area`.
Actual (sota_skills.py:107): `validate_context(context, ['paper_text', 'thematic_data'])`. Input is `thematic_data` dict (contains `subtemas`, `areas_tecnicas`, `año_paper`), not the split `themes`/`keywords` context keys.

**F17 — QueryGeneration Guard condition (§11)**
Claim: Guard on `context.get("themes")` falsy.
Actual (sota_skills.py:107-112): Guard on `paper_text` and `thematic_data`. No `themes` guard.

**F18 — CoverageGap Required input keys (§11)**
Claim: Required: `sota_papers`, `extracted_info`, optional `paper_text`.
Actual (sota_skills.py:256): `validate_context(context, ['paper_text', 'thematic_data'])`. No `sota_papers` or `extracted_info`. `paper_text` is required (not optional).

**F19 — CoverageGap Guard condition (§11)**
Claim: Guard fires if `sota_papers` is falsy or empty.
Actual (sota_skills.py:256): Guard on `paper_text` and `thematic_data`. `sota_papers` not checked at all.

**F20 — CoverageGap Output schema (§11)**
Claim: `coverage_gaps` is a `list[dict]` where each dict has `{gap_description: str, severity: str, related_papers: list[str]}`.
Actual (sota_skills.py:269-288,294): LLM prompt returns `{"areas_debiles": [{"subtema": ..., "diagnostico": ...}]}`. Different field names and schema.

**F21 — CoverageGap `sota_comparison_summary` absent (§11)**
Claim: Output key `sota_comparison_summary: str` produced by this skill.
Actual: No such key in the actual output. Not produced.

**F22 — LLMClient Constructor params (§15.2)**
Claim: Constructor takes `model_name`, `api_key`, `max_retries: int = 5`, `base_delay: float = 2.0` and stores `self.max_retries`, `self.base_delay`.
Actual (llm_client.py:11,39-40): Constructor takes `model_name=None`, `generation_config=None` only. `max_retries = 5` and `base_delay = 2` are local variables inside `generate()`, not stored as instance attributes.

**F23 — LLMClient `genai.GenerativeModel` (§15.2)**
Claim: Uses `genai.configure(api_key=api_key)` and `self.model = genai.GenerativeModel(model_name)`.
Actual (llm_client.py:23): Uses `self.client = genai.Client(api_key=GOOGLE_API_KEY)` — newer SDK pattern. No `genai.configure()` call, no `GenerativeModel`.

**F24 — LLMClient generate() signature (§15.3)**
Claim: `generate(self, prompt: str, config: dict = None, history: list[dict] = None) -> str`.
Actual (llm_client.py:30): `generate(self, prompt)`. No `config` or `history` parameters. Configuration is fixed at construction time via `self.generation_config`.

**F25 — LLMClient return type (§15.3, §15.9)**
Claim: `generate()` returns `str` (raw LLM response text).
Actual (llm_client.py:49): Returns `response` (the full `GenerateContentResponse` object). Skills call `.text` on the returned value (e.g., `rag_extraction_skill.py:179: raw_text = response.text.strip()`). The spec's type is wrong.

**F26 — LLMClient sleep position (§15.4)**
Claim: Sleep occurs at start of each iteration using `if attempt > 0: time.sleep(delay)` before the LLM call.
Actual (llm_client.py:56-69): Sleep occurs inside the `except` block, after a failed attempt, as part of the retry-decision code. Same practical effect but the loop structure is different from the spec's pseudocode.

**F27 — PDFParser chunk_size as parameter (§14.1)**
Claim: `convert_pdf_to_markdown(pdf_path: str, chunk_size: int = 5) -> str` — `chunk_size` is a configurable parameter.
Actual (pdf_parser.py:7,51): `convert_pdf_to_markdown(pdf_path)` — `chunk_size = 5` is hardcoded as a local variable. Cannot be overridden by callers.

**F28 — PDFParser error notice format (§14.5)**
Claim: On block failure, appends `<!-- Error processing pages N–M: {error} -->` (HTML comment).
Actual (pdf_parser.py:75): Appends `> [!ERROR] Error al procesar páginas N-M: {error}` — Markdown blockquote, not HTML comment. Different syntax.

**F29 — PDFParser file-not-found behavior (§14.5)**
Claim: "PDF file not found → Exception from `open_pdf()` propagates to caller."
Actual (pdf_parser.py:83-85): The outer `except Exception as e` catches ALL exceptions at the function level and returns `f"❌ Error en la extracción del PDF: {str(e)}"` — a string. No exception propagates.

**F30 — Regex `_search_with_negation` return type (§10)**
Claim: Returns a list of all non-negated matches.
Actual (regex_detection_skills.py:28-35): `Optional[re.Match]` — returns the FIRST non-negated match, or `None`. A reimplementation collecting all matches from the list would behave differently.

**F31 — Regex TABLE_PATTERNS oversimplified (§10.0)**
Claim: Spec shows three simple patterns: `r'Table\s+\d+\s*[:\.]'`, `r'^\|.+\|.+\|'`, `r'^\t.+\t'`.
Actual (regex_detection_skills.py:47-69): `table_pattern = r"(Table|Tab\.)\s+\d+[:\.]?[^\n]*\n([\s\S]{0,2000}?)(?=\n\s*\n|Table|Tab\.|\Z)"`, `pipe_table_pattern = r"(\|[^\n]+\|\n){3,}"`, `tab_table_pattern = r"([^\n]+\t[^\n]+\t[^\n]+\n){3,}"`. The actual patterns have 2000-char capture groups, lookaheads, and multi-row requirements not present in spec.

**F32 — HyperparameterDetectionSkill output keys (§10, Skill section)**
Claim: Output keys are `hyperparameter_matches` (list[str]) and `hyperparameter_count` (int).
Actual (regex_detection_skills.py:177-180,185): Returns `{'hyperparameter_flags': results}` where `results` contains `has_{key}` (bool), `{key}_value` (str), `{key}_location` (str) per hyperparameter key. Completely different structure.

---

## Coverage Gaps

No in-scope components are entirely absent from `02_functional_backend.md`. All 8 components (HybridHyperparameterExtractionSkill, SemanticScholarSearchSkill, CrossValidationSkill, QueryGenerationSkill, CoverageGapAnalysisSkill, LLMClient, PDFParser, Regex Detection Skills / NegationWindow) have dedicated sections with behavioral and algorithmic claims documented.

---

## Depth Gaps

The following spec elements have PARTIAL or NONE structured decomposition (missing actual field names, operators, values, or correct algorithm):

**DG01 — HybridHP Chunking (§3.5 Step 1) — NONE**
The pseudocode describes a completely wrong algorithm. Missing: actual split pattern `\n\n+`, filter threshold `len > 10`.

**DG02 — HybridHP Query call parameters (§3.5 Step 4) — NONE**
Missing: `query_embeddings` parameter, batch mode (all 13 at once), actual `n_results=10`. The spec's pseudocode cannot be used to reimplement this step.

**DG03 — HybridHP 13 query strings — NONE**
All 13 strings are wrong. The correct strings must be read from the source file.

**DG04 — HybridHP Relevance scoring formula (§3.5 Step 5) — NONE**
Wrong thresholds, wrong scale (0–1 vs 0–100), wrong number of ranges. Cannot reimplement from spec.

**DG05 — HybridHP Guard return shape (§3.4) — PARTIAL**
Trigger/condition correct. ACTION/ERROR return structure is wrong.

**DG06 — SS Rate limiting behavior — NONE**
Missing: `time.sleep(0.5)` between queries, `time.sleep(2)` on 429. No structured RULE/TRIGGER/CONDITION/ACTION for this behavior.

**DG07 — SS Top-N selection — NONE**
Entire sort-by-citation and top-10 cap behavior absent from spec. No structured description.

**DG08 — CrossValidation input keys and guard — NONE**
All required keys and the guard condition are wrong. No correct structured decomposition.

**DG09 — CrossValidation output keys — NONE**
Both `cross_validation_results` and `unsupported_claims_count` are wrong. The actual `validation_results` structure (with `papers_omitidos`, `conclusion_sota`) is not documented.

**DG10 — QueryGeneration input keys and guard — NONE**
`themes` and `keywords` are not context keys in the actual implementation. Missing: `paper_text`, `thematic_data`.

**DG11 — CoverageGap input keys, guard, output schema — NONE**
All three are wrong. No correct structured decomposition.

**DG12 — LLMClient constructor and generate() signature — NONE**
Constructor parameter list and `generate()` parameter list are both wrong. Cannot reimplement from spec.

**DG13 — LLMClient return type — PARTIAL**
Return documented as `str`. Actual is response object. Skills that access `.text` on the return value would work correctly only if this detail is inferred externally.

**DG14 — PDFParser chunk_size as parameter — PARTIAL**
The value 5 is documented correctly; the fact that it's hardcoded (not configurable) is missing.

**DG15 — Regex `_search_with_negation` return type — PARTIAL**
Algorithm logic is correct but return type (list vs Optional[Match]) is wrong. A caller returning or iterating over the result would behave incorrectly.

---

## Spec Consistency Issues

**SC01 — `_search_with_negation` return type vs usage**
Section 10.0 pseudocode describes `_search_with_negation` as returning a `matches` list ("RETURN matches"). However, in the same section, the usage context implies a single-match check ("IF any negation phrase in prefix ... CONTINUE"). The list-return pseudocode is internally inconsistent with how HyperparameterDetectionSkill uses it (`for i, pattern in enumerate(self.PATTERNS[key]):` then `break` on first found match — consistent with single-return, not list-return).

**SC02 — HybridHP Section 3 vs Section 11 context key naming**
Section 3 (HybridHP) uses `hyperparameter_results` as the output context key (§3.6 table and §3.7 return shapes). Section 11 (Exported Skills / pipeline overview) does not separately list HybridHP (it is non-exported), but §1.2's context key table and §1.1's phase table also use `hyperparameter_results` (§1.2: `hyperparameter_results | dict | Phase 1.5`). The actual key is `extracted_hyperparameters_hybrid`. This inconsistency is systematic across all spec references to this component.

---

## Quality Assessment

The spec `02_functional_backend.md` provides commendably detailed coverage for all 8 in-scope components, with pseudocode blocks, RULE/TRIGGER/CONDITION/ACTION structures, and parameter tables for nearly every component. The NEGATION_WINDOW constant, NEGATION_PATTERNS regex, LLMClient retry loop arithmetic, and Semantic Scholar configuration constants are all accurately specified and constitute the strongest portions of the document.

However, the spec has critical accuracy failures in several areas. For the HybridHyperparameterExtractionSkill, the chunking algorithm, the 13 query strings, the ChromaDB call parameters (n_results=3 vs 10, query_texts vs query_embeddings), and the relevance scoring formula are all substantially wrong — a reimplementation following only the spec would produce a qualitatively different RAG pipeline. For the SOTA skills pipeline (CrossValidationSkill, QueryGenerationSkill, CoverageGapAnalysisSkill), the input context key sets and guard conditions are completely wrong, indicating that the spec was synthesized from incorrect intermediate data rather than verified against the source.

The LLMClient section is particularly problematic: the constructor signature, the `generate()` method signature, and the return type are all wrong, suggesting the spec modeled a hypothetical "designed" API rather than the actual implementation. These errors would cause a developer to write incompatible caller code.

Remediation priorities are: (1) correct HybridHP chunking (split on `\n\n+`, not char-based), query call parameters (`query_embeddings`, `n_results=10`), query strings, and scoring formula; (2) correct CrossValidationSkill, QueryGenerationSkill, CoverageGapAnalysisSkill input context keys and output schemas against `sota_skills.py`; (3) correct LLMClient constructor, `generate()` signature, and return type; (4) correct `_search_with_negation` return type documentation.
