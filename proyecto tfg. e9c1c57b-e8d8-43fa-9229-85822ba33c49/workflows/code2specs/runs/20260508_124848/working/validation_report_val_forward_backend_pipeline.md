---
validator_id: val_forward_backend_pipeline
validator_type: forward_coverage
target_specs: [02_functional_backend.md]
forward_coverage_pct: 24.4
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 34
coverage_gaps: 0
depth_gaps: 3
spec_consistency_issues: 0
total_issues: 37
overall_status: fail
---

## Summary

Validated `02_functional_backend.md` against the actual source code in
`backend/services/auditor.py`, `backend/skills/auditor_skills.py`,
`backend/skills/base_skill.py`, `backend/skills/chatbot_skills.py`, and
`backend/skills/sota_skills.py`, focusing on: `PaperAuditor` constructor and
`audit()` method; eight concrete skill classes (`InformationExtractionSkill`,
`ReproducibilityEvaluationSkill`, `ChecklistVerificationSkill`,
`ConversationalResponseSkill`, `ContextValidationSkill`,
`ThematicCoverageSkill`, `MetricsCalculationSkill`,
`MetadataAggregationSkill`); `CompositeSkill` execution loop; and `BaseSkill`
abstract contract.

Of 86 enumerated spec claims, only 21 (24.4 %) are fully verified against
source. The spec systematically mis-describes the return shapes of every skill
(wrong key names, missing/spurious `success`/`phase` fields), mis-describes
`PaperAuditor.audit()`'s signature (spec adds `red_flags` parameter that does
not exist), and completely mischaracterises `CompositeSkill` error behaviour
(spec says it halts on sub-skill failure; source continues after catching
exceptions). `ContextValidationSkill` is particularly divergent: the spec
asserts it makes an LLM call and returns a relevance score, but the real
implementation does only local string validation with no LLM. The "Known Bug
(NameError)" described in §1.3 does not exist in the source — the outer
`except` block assigns `end_time` itself, so no `NameError` can occur.
**Overall status: fail.**

---

## Forward Coverage (Specs → Source)

> Legend: VERIFIED = claim confirmed in source | FIDELITY_ISSUE = claim contradicted by
> source | DEPTH_GAP = claim too vague to verify | GAP_INTENTIONAL = intentional [GAP:…]
> marker — skipped per policy.

| # | Spec Element | Type | Source Reference | Verified? | Status |
|---|---|---|---|---|---|
| 1 | Pipeline order: 1→1.5→2→2.5→3→4 sequential | orchestration | `auditor.py:86-189` | Yes | VERIFIED |
| 2 | Shared mutable context dict passed to each skill | orchestration | `auditor.py:84, 93, 123, 163, 172, 184` | Yes | VERIFIED |
| 3 | `PaperAuditor.audit(paper_text: str, red_flags: list) -> dict` signature | method-signature | `auditor.py:60` | No | FIDELITY_ISSUE |
| 4 | `context["start_time"] = start_time` set in `audit()` | constructor | `auditor.py:80-84` | No | FIDELITY_ISSUE |
| 5 | `context["end_time"] = end_time` set before Phase 3 | orchestration | `auditor.py:176` | No | FIDELITY_ISSUE |
| 6 | Phase 1 critical: on exception returns error and halts | error-handler | `auditor.py:89-91` | Partial | FIDELITY_ISSUE |
| 7 | Phase 1.5 non-critical: on failure logs to `context["error_log"]` | error-handler | `auditor.py:118-123` | No | FIDELITY_ISSUE |
| 8 | Phase 2.5 non-critical: on exception logs to `context["error_log"]` | error-handler | `auditor.py:171-172` | No | FIDELITY_ISSUE |
| 9 | Known Bug (NameError): `end_time` unbound in outer `except` | bug | `auditor.py:201-204` | No | FIDELITY_ISSUE |
| 10 | `PaperAuditor.__init__` initialises single `LLMClient` | constructor | `auditor.py:28-57` | No | FIDELITY_ISSUE |
| 11 | `InformationExtractionSkill.execute()` signature `(self, context: dict) -> dict` | method-signature | `auditor_skills.py:21` | Yes | VERIFIED |
| 12 | Phase 1 always runs unconditionally first | trigger | `auditor.py:88` | Yes | VERIFIED |
| 13 | Fragment split uses `\n(?=#+ )` regex on paper_text | algorithm | `auditor_skills.py:40` | Yes | VERIFIED |
| 14 | `target_size = total_chars / 4` for balanced splitting | algorithm | `auditor_skills.py:45` | Yes | VERIFIED |
| 15 | Fallback to RecursiveCharacterTextSplitter (chunk_size=25000, overlap=2000) limited to 4 | algorithm | `auditor_skills.py:72-74` | Yes | VERIFIED |
| 16 | MAP loop: `time.sleep(2)` between fragments | side-effect | `auditor_skills.py:105` | Yes | VERIFIED |
| 17 | MAP loop: per-fragment errors logged; fragment skipped | error-handler | `auditor_skills.py:106-108` | Yes | VERIFIED |
| 18 | Balanced JSON extraction: string-aware + escape-aware state machine | algorithm | `auditor_skills.py:89-98` | No | FIDELITY_ISSUE |
| 19 | REDUCE calls `get_reduce_extraction_prompt(map_results)` | method-call | `auditor_skills.py:116` | Yes | VERIFIED |
| 20 | REDUCE applies trailing-comma regex repair | algorithm | `auditor_skills.py:148` | Yes | VERIFIED |
| 21 | Output key `map_results` (list of MAP dicts) | output-schema | `auditor_skills.py:173-178` | No | FIDELITY_ISSUE |
| 22 | Output key `reduce_result` (alias of `extracted_info`) | output-schema | `auditor_skills.py:173-178` | No | FIDELITY_ISSUE |
| 23 | Output key `fragment_count` (int) | output-schema | `auditor_skills.py:173-178` | No | FIDELITY_ISSUE |
| 24 | Output key `paper_title` extracted from `extracted_info["title"]` | output-schema | `auditor_skills.py:173-178` | No | FIDELITY_ISSUE |
| 25 | Success return shape: `{"success": True, "extracted_info": …, "map_results": …, "fragment_count": …}` | return-schema | `auditor_skills.py:173-178` | No | FIDELITY_ISSUE |
| 26 | Failure return shape: `{"success": False, "error": str, "phase": "information_extraction"}` | return-schema | `auditor_skills.py:110-111, 179-181` | No | FIDELITY_ISSUE |
| 27 | `ReproducibilityEvaluationSkill.execute()` calls `get_evaluation_signals(extracted_info)` | method-call | `auditor_skills.py:208` | Yes | VERIFIED |
| 28 | `ReproducibilityEvaluationSkill.execute()` calls `get_evaluation_prompt(extracted_info, red_flags)` | method-call | `auditor_skills.py:210-213` | Yes | VERIFIED |
| 29 | Guard: if `extracted_info` falsy → return `{"success": False, "error": …, "phase": "reproducibility_evaluation"}` | guard | `auditor_skills.py:188-196` | No | FIDELITY_ISSUE |
| 30 | Output key `checklist` (16-item NeurIPS evaluation) | output-schema | `auditor_skills.py:239-242` | No | FIDELITY_ISSUE |
| 31 | Output key `evaluation_signals` (6-key dict) | output-schema | `auditor_skills.py:241` | Yes | VERIFIED |
| 32 | Success return shape: `{"success": True, "checklist": dict}` | return-schema | `auditor_skills.py:239-242` | No | FIDELITY_ISSUE |
| 33 | Failure return shape: `{"success": False, "error": str, "phase": "reproducibility_evaluation"}` | return-schema | `auditor_skills.py:243-250` | No | FIDELITY_ISSUE |
| 34 | `ChecklistVerificationSkill` reads `context["checklist"]` as input | input-schema | `auditor_skills.py:326` | No | FIDELITY_ISSUE |
| 35 | Guard: if `checklist` or `paper_text` falsy → error shape | guard | `auditor_skills.py:326-336` | No | FIDELITY_ISSUE |
| 36 | Paper context truncation: `paper_text[:30000] + paper_text[-30000:]` | algorithm | `auditor_skills.py:368` | Yes | VERIFIED |
| 37 | 8 priority checklist items selected for re-verification | algorithm | `auditor_skills.py:340-356` | Yes (partial) | VERIFIED |
| 38 | Output key `checklist` (updated in-place) | output-schema | `auditor_skills.py:399` | No | FIDELITY_ISSUE |
| 39 | Output key `verification_count` | output-schema | `auditor_skills.py:399` | No | FIDELITY_ISSUE |
| 40 | Output key `checklist_summary` | output-schema | `auditor_skills.py:399` | No | FIDELITY_ISSUE |
| 41 | Success return shape: `{"success": True, "verification_count": int, "checklist_summary": dict}` | return-schema | `auditor_skills.py:399` | No | FIDELITY_ISSUE |
| 42 | `MetricsCalculationSkill` guard: if `start_time` absent → error | guard | `auditor_skills.py:257-259` | No | FIDELITY_ISSUE |
| 43 | `MetricsCalculationSkill` reads `context["start_time"]` to compute `tiempo_segundos` | input-schema | `auditor_skills.py:256-279` | No | FIDELITY_ISSUE |
| 44 | `MetricsCalculationSkill` reads `context["extracted_info"]` for red-flag counting | input-schema | `auditor_skills.py:264-276` | No | FIDELITY_ISSUE |
| 45 | Output key `tiempo_segundos` (direct on context) | output-schema | `auditor_skills.py:271-279` | No | FIDELITY_ISSUE |
| 46 | Output key `caracteres_leidos` = `len(paper_text)` | output-schema | `auditor_skills.py:274` | Yes | VERIFIED |
| 47 | Output key `red_flags_detectadas` (filtered from extracted_info) | output-schema | `auditor_skills.py:263-276` | No | FIDELITY_ISSUE |
| 48 | Success return shape: `{"success": True, "tiempo_segundos": …, "caracteres_leidos": …, "red_flags_detectadas": …}` | return-schema | `auditor_skills.py:278` | No | FIDELITY_ISSUE |
| 49 | `MetadataAggregationSkill` reads the 23 context keys listed in §1.2 | input-schema | `auditor_skills.py:285-317` | No | FIDELITY_ISSUE |
| 50 | `MetadataAggregationSkill` adds `audit_complete: True` and `pipeline_version` | aggregation | `auditor_skills.py:285-317` | No | FIDELITY_ISSUE |
| 51 | Output stored under `context["result"]` key | output-schema | `auditor_skills.py:285-317` | No | FIDELITY_ISSUE |
| 52 | Success return shape: `{"success": True, "result": dict}` | return-schema | `auditor_skills.py:317` | No | FIDELITY_ISSUE |
| 53 | `CompositeSkill.__init__(skills, name="CompositeSkill")` signature | constructor | `base_skill.py:91` | No | FIDELITY_ISSUE |
| 54 | `CompositeSkill` stores `self.skills` list | constructor | `base_skill.py:100` | Yes | VERIFIED |
| 55 | Chaining: checks `result.get("success", False)` and stops on failure | algorithm | `base_skill.py:103-124` | No | FIDELITY_ISSUE |
| 56 | Chaining: merges result into context via `context.update(result)` | algorithm | `base_skill.py:119` | Yes | VERIFIED |
| 57 | Success return: `{"success": True, "context": dict}` | return-schema | `base_skill.py:103-124` | No | FIDELITY_ISSUE |
| 58 | Failure return: `{"success": False, "error": …, "failed_skill": …, "phase": …}` | return-schema | `base_skill.py:103-124` | No | FIDELITY_ISSUE |
| 59 | Error isolation: one failure STOPS chain; subsequent skills not executed | error-handler | `base_skill.py:120-123` | No | FIDELITY_ISSUE |
| 60 | `BaseSkill` is ABC with `@abstractmethod execute()` | abstract-contract | `base_skill.py:10-45` | Yes | VERIFIED |
| 61 | `execute(self, context: dict) -> dict` abstract signature | abstract-contract | `base_skill.py:34` | Yes | VERIFIED |
| 62 | `BaseSkill.__init__(llm_client, config)` stores both attributes | constructor | `base_skill.py:19-31` | Yes | VERIFIED |
| 63 | `validate_context()` helper method present | helper | `base_skill.py:47-62` | Yes | VERIFIED |
| 64 | `log_execution()` helper method present | helper | `base_skill.py:64-80` | Yes | VERIFIED |
| 65 | `name` exposed as `@property` returning class name | property | `base_skill.py:30` | No | FIDELITY_ISSUE |
| 66 | BaseSkill return contract: always include `success`, `error`, `phase` | return-contract | `auditor_skills.py` (multiple) | No | FIDELITY_ISSUE |
| 67 | `ConversationalResponseSkill`: required inputs `question`, `paper_text`, `conversation_history` | input-schema | `chatbot_skills.py:24, 34` | No | FIDELITY_ISSUE |
| 68 | `ConversationalResponseSkill`: guard returns `{"success": False, …}` | guard | `chatbot_skills.py:25-26` | No | FIDELITY_ISSUE |
| 69 | `ConversationalResponseSkill`: uses `CHAT_CONFIG = {"temperature": 0.2}` | llm-config | `chatbot_skills.py:59-61` | No | FIDELITY_ISSUE |
| 70 | `ConversationalResponseSkill`: output key `answer` | output-schema | `chatbot_skills.py:62` | No | FIDELITY_ISSUE |
| 71 | `ConversationalResponseSkill`: output key `updated_history` | output-schema | `chatbot_skills.py:62` | No | FIDELITY_ISSUE |
| 72 | `ConversationalResponseSkill`: uses LLM | llm-usage | `chatbot_skills.py:60` | Yes | VERIFIED |
| 73 | `ContextValidationSkill`: validates question answerability via LLM; returns relevance score | purpose | `chatbot_skills.py:68-117` | No | FIDELITY_ISSUE |
| 74 | `ContextValidationSkill`: guard: if `question` falsy → `{"success": False, …}` | guard | `chatbot_skills.py:86-91` | No | FIDELITY_ISSUE |
| 75 | `ContextValidationSkill`: uses LLM with `AUDIT_CONFIG` (JSON output) | llm-usage | `chatbot_skills.py:68-117` | No | FIDELITY_ISSUE |
| 76 | `ContextValidationSkill`: output keys `question_relevant`, `relevance_confidence`, `relevance_reason` | output-schema | `chatbot_skills.py:107-117` | No | FIDELITY_ISSUE |
| 77 | `ThematicCoverageSkill`: guard: if `paper_text` falsy → `{"success": False, "error": …}` | guard | `sota_skills.py:34-35` | No | FIDELITY_ISSUE |
| 78 | `ThematicCoverageSkill`: uses LLM with `SOTA_CONFIG = {"response_mime_type": "application/json", "temperature": 0.1}` | llm-config | `sota_skills.py:73` | No | FIDELITY_ISSUE |
| 79 | `ThematicCoverageSkill`: output keys `themes`, `keywords`, `research_area` | output-schema | `sota_skills.py:83` | No | FIDELITY_ISSUE |
| 80 | `ThematicCoverageSkill`: uses LLM | llm-usage | `sota_skills.py:73` | Yes | VERIFIED |
| 81 | §3: `HybridHyperparameterExtractionSkill` guard: if `paper_text` falsy → returns error | guard | `rag_extraction_skill.py` (unchecked) | DEPTH_GAP | DEPTH_GAP |
| 82 | §3.5 Step 2: batch embeddings with `batch_size=15`, `sleep(15)` between batches | algorithm | `rag_extraction_skill.py` (unchecked) | DEPTH_GAP | DEPTH_GAP |
| 83 | §1.2: 23 context keys for Phase 4, including `paper_title`, `map_results`, `reduce_result`, `fragment_count`, `checklist_summary`, `verification_count` | input-schema | `auditor_skills.py:285-317` | No | FIDELITY_ISSUE |
| 84 | §1.3 time tracking: `start_time` set before Phase 1, `end_time` set after Phase 2.5, both written to context | orchestration | `auditor.py:80-184` | No | FIDELITY_ISSUE |
| 85 | `ChecklistVerificationSkill`: per-item increments `context["verification_count"]` | algorithm | `auditor_skills.py:395-398` | No | FIDELITY_ISSUE |
| 86 | §6.5: `tiempo_segundos = end_time - start_time` inside MetricsCalculationSkill | algorithm | `auditor_skills.py:272-273` | No | FIDELITY_ISSUE |

**Totals**: 21 VERIFIED | 62 FIDELITY_ISSUE / FIDELITY_ISSUE (partial) | 3 DEPTH_GAP

---

## Depth Validation

| Spec Element | Type | Has Structured Decomposition | Detail Level | Missing |
|---|---|---|---|---|
| §4.5 `get_evaluation_signals()` "computes a dict with 6 keys derived from extracted_info" | helper-function | No | Prose-only | Exact 6 key names, formulas, data-type of each value |
| §6.5–6.6 Red flag detection formula: "filters extracted_info keys by known red-flag prefix" | algorithm | No | Prose-only | Exact prefix strings used to filter (e.g., `tiene_`, `menciona_`, prefix exclusions) |
| §9.4 BaseSkill return contract: "return dict MUST always contain success, error, phase" | contract | Partial | Structural table only | Contract is stated but no invariant enforcement mechanism described; actual implementations violate it |

---

## Fidelity Issues

### FI-01 — `audit()` signature includes `red_flags` parameter
**Spec (§1.3)**: "`PaperAuditor.audit(paper_text: str, red_flags: list) -> dict` is the single entry point."  
**Claimed SOURCE**: `extracted_backend_core_01.md §4.2`  
**Actual source** (`auditor.py:60`): `def audit(self, paper_text, status_callback=None):`  
`red_flags` is NOT a parameter; `context` is initialised with `'red_flags': {}` (hardcoded empty dict, line 84).

---

### FI-02 — `context["start_time"]` and `context["end_time"]` claimed to be written by audit()
**Spec (§1.3 code block)**: Shows `context["start_time"] = start_time` and `context["end_time"] = end_time` as explicit assignments.  
**Actual source** (`auditor.py:80–184`): Neither key is ever written into `context`. `start_time` is a local variable; `execution_time` (the delta) is passed via a separate `metrics_context` dict at line 179–183. `context["start_time"]` is never set.

---

### FI-03 — Known Bug (NameError) does not exist
**Spec (§1.3)**: "In the outer `except` block of `audit()`, the code references `end_time`… If an exception is raised before that line (Phase 1, 1.5, or 2), `end_time` is unbound and the outer `except` block itself raises `NameError`."  
**Actual source** (`auditor.py:201–204`): The outer `except Exception as e:` block is `end_time = time.time()` as its first statement. `end_time` is always assigned inside the except block itself. There is no `NameError` risk; the described bug does not exist in this code.

---

### FI-04 — `PaperAuditor.__init__` initialises multiple LLM clients, not one
**Spec (§1.2 constructor bullet)**: Implies a single `llm_client` dependency.  
**Actual source** (`auditor.py:31–54`): Creates five separate `LLMClient` instances:
`extraction_llm`, `evaluation_llm`, `rag_map_llm`, `rag_reduce_llm`, `verification_llm`. Each skill receives its own specialised client.

---

### FI-05 — InformationExtractionSkill output keys: `map_results`/`reduce_result`/`fragment_count`/`paper_title` absent
**Spec (§2.5)**: Output keys include `extracted_info`, `map_results`, `reduce_result`, `fragment_count`, `paper_title`.  
**Actual source** (`auditor_skills.py:173–178`): Returns `{'extracted_info': …, 'invalid_paper': …, 'map_steps': …, 'reduce_step': …}`. Keys `map_results`, `reduce_result`, `fragment_count`, and `paper_title` do not exist in any return path.

---

### FI-06 — InformationExtractionSkill success and failure return shapes do not include `success`/`phase`
**Spec (§2.12)**: Success: `{"success": True, "extracted_info": dict, "map_results": list, "fragment_count": int}`. Failure: `{"success": False, "error": str, "phase": "information_extraction"}`.  
**Actual source** (`auditor_skills.py:110–111, 154–158, 173–178, 179–181`): None of the return paths include a `success` key. Failure paths return `{'extracted_info': {}, 'extraction_error': str(e)}`. The `phase` identifier is never included.

---

### FI-07 — Balanced JSON extraction is a simplified brace-counter, not a string-aware state machine
**Spec (§2.8)**: Describes a full in-string / escape-next state machine tracking `in_string` and `escape_next` flags so braces inside string literals are not counted.  
**Actual source** (`auditor_skills.py:89–98`): Implements a simple `stack` counter that increments on `{` and decrements on `}` with NO string or escape tracking. A JSON value like `"key": "value with {braces}"` would corrupt the balance count.

---

### FI-08 — ReproducibilityEvaluationSkill output key is `evaluation`, not `checklist`
**Spec (§4.9)**: Output key `checklist` (16-item NeurIPS checklist); success shape `{"success": True, "checklist": dict}`.  
**Actual source** (`auditor_skills.py:239–242`): Returns `{'evaluation': evaluation, 'evaluation_signals': signals}`. The key is `evaluation`, not `checklist`. No `success` key is present in any return path.

---

### FI-09 — ReproducibilityEvaluationSkill guard returns `{'evaluation': {}}`, not error shape
**Spec (§4.4)**: Guard returns `{"success": False, "error": "No extracted_info in context", "phase": "reproducibility_evaluation"}`.  
**Actual source** (`auditor_skills.py:188–196`): When `extracted_info` is absent or not a dict, returns `{'evaluation': {}}` (no `success`, no `error`, no `phase`).

---

### FI-10 — ChecklistVerificationSkill reads `evaluation`, not `checklist`
**Spec (§5.3)**: Input context key is `checklist` (16-item NeurIPS evaluation dict).  
**Actual source** (`auditor_skills.py:326`): Reads `context.get('evaluation')`. The key consumed is `evaluation`, matching the actual output of `ReproducibilityEvaluationSkill`.

---

### FI-11 — ChecklistVerificationSkill output keys `verification_count` and `checklist_summary` absent
**Spec (§5.9)**: Output keys: `checklist` (updated), `verification_count` (int), `checklist_summary` (dict).  
**Actual source** (`auditor_skills.py:399`): Returns only `{'evaluation': evaluation}`. No `checklist`, no `verification_count`, no `checklist_summary`.

---

### FI-12 — MetricsCalculationSkill guard checks `paper_text`, not `start_time`
**Spec (§6.4)**: Guard: if `start_time` absent → return error.  
**Actual source** (`auditor_skills.py:257–259`): `if not self.validate_context(context, ['paper_text'])`. Checks for `paper_text`, not `start_time`.

---

### FI-13 — MetricsCalculationSkill reads `execution_time`/`red_flags`, not `start_time`/`extracted_info`
**Spec (§6.3, §6.5)**: Reads `start_time` to compute elapsed time; reads `extracted_info` to count red flags.  
**Actual source** (`auditor_skills.py:262–276`): Reads `context.get('execution_time', 0)` (pre-computed by orchestrator) for `tiempo_segundos` and reads `context.get('red_flags', {})` (not `extracted_info`) for red-flag counting.

---

### FI-14 — MetricsCalculationSkill output is wrapped under `metrics` key
**Spec (§6.7, §6.8)**: Output keys `tiempo_segundos`, `caracteres_leidos`, `red_flags_detectadas` returned at top level; success shape `{"success": True, "tiempo_segundos": …}`.  
**Actual source** (`auditor_skills.py:272–279`): Returns `{'metrics': {'tiempo_segundos': …, 'caracteres_leidos': …, 'red_flags_detectadas': …}}`. All values are nested under `metrics`; no `success` key.

---

### FI-15 — MetadataAggregationSkill reads from `evaluation` dict, not 23 direct context keys
**Spec (§7.3–7.4, §1.2)**: Reads all 23 context keys (including `paper_title`, `map_results`, `reduce_result`, `fragment_count`, `tiempo_segundos`, `checklist_summary`, `verification_count`, etc.) and flattens them.  
**Actual source** (`auditor_skills.py:285–317`): Reads `context.get('evaluation', {})` and extracts its sub-keys, plus `informacion_extraida`, `red_flags`, `metricas`, `general_analysis_map`, `general_analysis_reduce`, `hybrid_triage_fragments`, `evaluation_signals`. Many keys listed in §1.2 (`paper_title`, `map_results`, `reduce_result`, `fragment_count`, `start_time`, `checklist_summary`, `verification_count`) are not read.

---

### FI-16 — MetadataAggregationSkill does not add `audit_complete` or `pipeline_version`; returns dict directly
**Spec (§7.4–7.5)**: Adds `result["audit_complete"] = True` and `result["pipeline_version"] = config.AUDIT_VERSION`; wraps output under `context["result"]`; success shape `{"success": True, "result": dict}`.  
**Actual source** (`auditor_skills.py:285–317`): Returns the `result` dict directly (no wrapping, no `audit_complete`, no `pipeline_version`, no `success` key).

---

### FI-17 — CompositeSkill constructor takes `llm_client`, not `name`
**Spec (§8.2)**: `def __init__(self, skills: list[BaseSkill], name: str = "CompositeSkill"):`  
**Actual source** (`base_skill.py:91`): `def __init__(self, skills: list[BaseSkill], llm_client: Optional[LLMClient] = None):`. No `name` parameter; takes `llm_client` instead.

---

### FI-18 — CompositeSkill does NOT halt on sub-skill failure; continues to next skill
**Spec (§8.4)**: "If `NOT result.get('success', False)` → immediately return failure shape. Subsequent skills NOT executed."  
**Actual source** (`base_skill.py:117–123`): Only catches `Exception`; on exception stores `accumulated_context[f"error_{skill.name}"] = str(e)` and **continues to the next skill**. Does not inspect `result.get("success")` at all.

---

### FI-19 — CompositeSkill returns `accumulated_context` directly, not `{"success": True, "context": dict}`
**Spec (§8.6)**: Success return `{"success": True, "context": dict}`. Failure return `{"success": False, "error": str, "failed_skill": str, "phase": str}`.  
**Actual source** (`base_skill.py:103–124`): Returns `accumulated_context` (a plain dict of all accumulated keys). No `success`, `context`, `failed_skill`, or `phase` wrappers.

---

### FI-20 — BaseSkill `name` is an instance attribute, not a `@property`
**Spec (§9.2)**: Shows `@property def name(self) -> str: return self.__class__.__name__`.  
**Actual source** (`base_skill.py:30`): `self.name = self.__class__.__name__` — assigned as an instance attribute in `__init__`. No property descriptor. Functionally equivalent but architecturally different.

---

### FI-21 — Phase 1.5 error handling: spec says "non-critical, pipeline continues"; source has conditional
**Spec (§1.1, Phase 1.5 row)**: "Non-critical: on failure, pipeline continues."  
**Actual source** (`auditor.py:118–123`): Continues only when `'error' in hybrid_hp_result and not hybrid_hp_result.get('extracted_hyperparameters_hybrid')`. This is a weaker guard than a blanket "on exception, continue" — it checks a specific dict key pattern, not a try/except.

---

### FI-22 — Phase 2.5 non-critical error handling missing from source
**Spec (§1.1, Phase 2.5 row, §1.3)**: "Non-critical: on exception, logged to `context['error_log']`, pipeline continues."  
**Actual source** (`auditor.py:171–172`): `verification_result = self.verification_skill.execute(context); context.update(verification_result)`. No try/except. Any exception raised by `verification_skill.execute()` propagates to the outer handler. `context["error_log"]` is never written.

---

### FI-23 — Phase 3 error criticality: spec says Phase 3 is critical; source has no check
**Spec (§1.1)**: Phase 3 is critical; on failure returns error dict and halts.  
**Actual source** (`auditor.py:176–185`): `metrics_result = self.metrics_skill.execute(metrics_context); context.update(metrics_result)`. No error check on `metrics_result`. Any failure silently continues to Phase 4.

---

### FI-24 — ConversationalResponseSkill reads `history_text`, not `conversation_history`; returns `response`, not `answer`/`updated_history`
**Spec (§11, ConversationalResponseSkill)**: Input: `conversation_history` (list[dict]). Output: `answer` (str), `updated_history` (list[dict]).  
**Actual source** (`chatbot_skills.py:34, 62`): Reads `context.get('history_text', 'Sin historial previo.')` (a pre-formatted string, not a list). Returns `{'response': response.text}`. No `answer` key; no `updated_history` key.

---

### FI-25 — ContextValidationSkill performs only local validation; no LLM; output completely different
**Spec (§11, ContextValidationSkill)**: Uses LLM with `AUDIT_CONFIG` to assess question relevance; returns `question_relevant` (bool), `relevance_confidence` (float), `relevance_reason` (str).  
**Actual source** (`chatbot_skills.py:68–117`): No `llm_client` call anywhere. Validates that `paper_text` is non-empty and `question` is non-empty, then returns a prepared context dict with keys `is_valid`, `paper_text`, `question`, `history_text`, `paper_length`, `question_length`. Completely different purpose, no LLM, completely different output schema.

---

### FI-26 — ThematicCoverageSkill output keys are `thematic_data.subtemas`/`areas_tecnicas`/`año_paper`, not `themes`/`keywords`/`research_area`
**Spec (§11, ThematicCoverageSkill)**: Output: `themes` (list[str]), `keywords` (list[str]), `research_area` (str). LLM config: `SOTA_CONFIG = {"response_mime_type": "application/json", "temperature": 0.1}`.  
**Actual source** (`sota_skills.py:83`): Returns `{'thematic_data': {...}}` where the inner dict has keys `subtemas`, `areas_tecnicas`, `año_paper`. No named `SOTA_CONFIG`; calls `self.llm_client.generate(prompt)` with no config override.

---

### FI-27 — §1.2 Phase 4 input key list includes keys that do not exist in context
**Spec (§1.2)**: Lists 23 keys read by Phase 4, including `paper_title`, `map_results`, `reduce_result`, `fragment_count`, `checklist`, `checklist_summary`, `verification_count`, `audit_version`.  
**Actual source** (`auditor_skills.py:285–317` + `auditor.py`): None of `paper_title`, `map_results`, `reduce_result`, `fragment_count`, `checklist`, `checklist_summary`, `verification_count`, or `audit_version` exist in the actual context dict at the time Phase 4 runs. They were described under wrong key names in earlier phases, so they never accumulate in context.

---

### FI-28 — ConversationalResponseSkill guard returns non-structured error response
**Spec (§11)**: Guard returns `{"success": False, "error": "Missing question or paper_text", "phase": "conversational_response"}`.  
**Actual source** (`chatbot_skills.py:25–26`): Returns `{'response': '❌ Error: Faltan datos para generar respuesta'}`. No `success`, `error`, or `phase` keys.

---

## Coverage Gaps

No source files in the auditing pipeline domain with LOC > 50 were found to be entirely absent from spec coverage. All major modules (`auditor.py`, `auditor_skills.py`, `base_skill.py`, `chatbot_skills.py`, `sota_skills.py`, `rag_extraction_skill.py`, `regex_detection_skills.py`) have at least some coverage in `02_functional_backend.md`. Coverage of `rag_extraction_skill.py` was not directly verified against source in this validation run (marked as DEPTH_GAP for two of its algorithm claims), but the class is described at length in §3.

---

## Depth Gaps

### DG-01 — `get_evaluation_signals()` key set undocumented
**Spec (§4.5)**: "Computes a Python dict with 6 keys derived directly from `extracted_info`." No keys, formulas, or data types are specified.  
**Why it matters**: A developer reimplementing the backend cannot reproduce this function without knowing the 6 keys. The spec refers to "§16 for full documentation" but that reference is to prompt template functions in a later section, not to the evaluation signals dict structure.

### DG-02 — Red flag prefix set not specified
**Spec (§6.6)**: "Filters extracted_info keys by prefix." Lists the filtering logic but marks the prefix strings as `[GAP: the exact set of red-flag key prefixes used for filtering is not enumerated in extraction]`.  
**Why it matters**: The actual implementation filters `red_flags` (not `extracted_info`) by key-name patterns that exclude `tiene_`, `menciona_`, `_`, `cantidad_`, `puntos_` prefixes. None of this is in the spec.

### DG-03 — BaseSkill return contract stated but not enforced
**Spec (§9.4)**: States the return dict MUST always contain `success`, `error`, `phase`. No description of how this is enforced or what happens when concrete classes violate it.  
**Why it matters**: Multiple concrete skills (`InformationExtractionSkill`, `ReproducibilityEvaluationSkill`, `ChecklistVerificationSkill`, `MetricsCalculationSkill`, `MetadataAggregationSkill`, `ConversationalResponseSkill`, `ThematicCoverageSkill`) do NOT include a `success` key in their returns, making the contract effectively a dead letter.

---

## Quality Assessment

The forward coverage analysis reveals systematic and pervasive specification drift from the actual source code. Structural elements — class hierarchy, phase ordering, use of an LLM client, section-header-based fragmentation — are correctly described. However, the interface contracts (return shapes, input/output key names, guard behaviour) are wrong for nearly every skill.

**Well-specified elements**: The six-phase pipeline ordering, the MAP/REDUCE structure of `InformationExtractionSkill`, the paper-text truncation in `ChecklistVerificationSkill`, the abstract `BaseSkill` contract (ABC + `execute()`), and the presence of `validate_context()` / `log_execution()` helpers.

**Under-specified or incorrectly specified**:
- *Every skill's return shape* omits or misnames keys. The spec consistently adds a `success`/`phase` envelope that no actual skill uses.
- `ContextValidationSkill` is the most severe divergence: the spec describes an LLM-driven relevance assessor; the implementation is a simple local validator with no LLM call.
- `CompositeSkill` error behaviour is inverted: spec says halt-on-failure; implementation continues silently.
- The "Known Bug (NameError)" is entirely fabricated — no such bug exists in the outer `except` block.
- The `audit()` signature adds a `red_flags` parameter that does not exist.
- `MetadataAggregationSkill` description of 23 aggregated keys is fictional — the actual keys differ substantially.

**Recommendations**:
1. Rewrite all skill return-shape tables to match actual returns (drop `success`/`phase` envelope where absent).
2. Correct `audit()` signature to `(paper_text, status_callback=None)` and update §1.2 context-init description.
3. Replace the `ContextValidationSkill` description with the actual local-validation behavior.
4. Correct `CompositeSkill` error-handling description: it continues after exceptions, not halts.
5. Remove the NameError bug description in §1.3.
6. Fix output key names for `InformationExtractionSkill` (`map_steps`, `reduce_step`) and `ChecklistVerificationSkill`/`ReproducibilityEvaluationSkill` (`evaluation` key).
7. Document the actual `MetricsCalculationSkill` inputs (`execution_time` from orchestrator, `red_flags` dict) and output wrapper (`metrics` key).
