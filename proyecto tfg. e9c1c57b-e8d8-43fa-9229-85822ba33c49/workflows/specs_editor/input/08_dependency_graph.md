# Dependency Graph

Source: Synthesized from extracted_backend_core_01.md, extracted_backend_skills_01.md, extracted_frontend_01.md, extracted_root_tests_scratch_01.md, cross_ref_resolution_cross_ref_root_to_backend.md, cross_ref_resolution_cross_ref_root_to_frontend.md

---

## Metadata

| Key | Value |
|---|---|
| node_count | 56 |
| edge_count | 60 |
| schema_version | 1.0 |
| generated | 2026-05-09T14:49:57Z |

---

## Graph Statistics

| Metric | Value |
|---|---|
| Total nodes | 56 |
| Total edges | 60 |
| Cross-module edges | 49 |
| Detected cycles | 1 |
| Modules | backend_core, backend_skills, frontend, root |
| External system nodes | 5 |

**Node breakdown by type:**

| Type | Count |
|---|---|
| service | 37 |
| screen | 6 |
| entity | 3 |
| config | 2 |
| class | 3 |
| external | 5 (module: external) |

**Edge breakdown by type:**

| Type | Count |
|---|---|
| instantiates | 20 |
| calls | 22 |
| reads | 12 |
| writes | 1 |
| import | 2 |
| uses | 1 |
| inherits | 2 |

**Cross-module edge summary:**

| Module Pair | Edge Count |
|---|---|
| backend_core → backend_skills | 13 |
| backend_skills → backend_core | 12 |
| frontend → backend_core | 7 |
| root → frontend | 6 |
| frontend → external | 4 |
| external → backend_core | 3 |
| backend_core → external | 2 |
| backend_skills → external | 2 |

All counts are derived from the JSON `nodes` and `edges` arrays.

---

## Module: backend_core

### Services

#### service:PaperAuditor

- **Node ID**: `service:PaperAuditor`
- **Type**: service
- **Module**: backend_core
- **Description**: 6-phase (1/1.5/2/2.5/3/4) audit pipeline orchestrator. Creates 5 LLMClient instances and 6 skill instances in `__init__`. Entry point: `audit(paper_text, status_callback=None) -> dict`.
- **Source**: `extracted_backend_core_01.md#3.2-Auditor-Service`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `config:config_py` | reads | AUDIT_CONFIG/EXTRACTION_MODEL_NAME/MAP_MODEL_NAME/REDUCE_MODEL_NAME/EVALUATION_MODEL_NAME/VERIFICATION_MODEL_NAME | MEDIUM | extracted_backend_core_01.md#3.2 (auditor.py:31-43) |
| `service:LLMClient` | instantiates | 5 LLMClient instances: extraction_llm/evaluation_llm/rag_map_llm/rag_reduce_llm/verification_llm | CRITICAL | extracted_backend_core_01.md#3.2 (auditor.py:31-43) |
| `service:InformationExtractionSkill` | instantiates | extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm) | CRITICAL | extracted_backend_core_01.md#3.2 (auditor.py:46) |
| `service:HybridHyperparameterExtractionSkill` | instantiates | hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm) | HIGH | extracted_backend_core_01.md#3.2 (auditor.py:47) |
| `service:ReproducibilityEvaluationSkill` | instantiates | evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm) | CRITICAL | extracted_backend_core_01.md#3.2 (auditor.py:48) |
| `service:ChecklistVerificationSkill` | instantiates | verification_skill = ChecklistVerificationSkill(llm_client=self.verification_llm) | HIGH | extracted_backend_core_01.md#3.2 (auditor.py:51) |
| `service:MetricsCalculationSkill` | instantiates | metrics_skill = MetricsCalculationSkill() | MEDIUM | extracted_backend_core_01.md#3.2 (auditor.py:53) |
| `service:MetadataAggregationSkill` | instantiates | metadata_skill = MetadataAggregationSkill() | MEDIUM | extracted_backend_core_01.md#3.2 (auditor.py:54) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:file_uploader` | calls | st.session_state.auditor.audit(md_text, status_callback=update_status) | CRITICAL | extracted_frontend_01.md#5.1 (file_uploader.py:49) |
| `service:session_state` | instantiates | PaperAuditor() stored as st.session_state['auditor'] | HIGH | extracted_frontend_01.md#3 (session_state.py:11-12) |
| `external:st.session_state` | reads | auditor key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |

---

#### service:PaperChatbot

- **Node ID**: `service:PaperChatbot`
- **Type**: service
- **Module**: backend_core
- **Description**: Skill-based Q&A chatbot over audited papers. Creates 1 LLMClient, ConversationalResponseSkill, and ContextValidationSkill. Entry point: `preguntar(paper_text, question, history_text) -> str`. Alias class: `Chatbot(PaperChatbot)`.
- **Source**: `extracted_backend_core_01.md#3.3-Chatbot-Service`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `config:config_py` | reads | CHAT_CONFIG | MEDIUM | extracted_backend_core_01.md#3.3 (chatbot.py:17) |
| `service:LLMClient` | instantiates | LLMClient(generation_config=CHAT_CONFIG) | HIGH | extracted_backend_core_01.md#3.3 (chatbot.py:17) |
| `service:ConversationalResponseSkill` | instantiates | response_skill = ConversationalResponseSkill(llm_client=self.llm_client) | HIGH | extracted_backend_core_01.md#3.3 (chatbot.py:20) |
| `service:ContextValidationSkill` | instantiates | validation_skill = ContextValidationSkill() | MEDIUM | extracted_backend_core_01.md#3.3 (chatbot.py:21) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:chatbot` | calls | st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str) | CRITICAL | extracted_frontend_01.md#5.3 (chatbot.py:26) |
| `service:session_state` | instantiates | PaperChatbot() stored as st.session_state['chatbot'] | HIGH | extracted_frontend_01.md#3 (session_state.py:14-15) |
| `external:st.session_state` | reads | chatbot key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |

---

#### service:Chatbot

- **Node ID**: `service:Chatbot`
- **Type**: service
- **Module**: backend_core
- **Description**: Backward-compatibility alias class inheriting from `PaperChatbot` with no method overrides. Declared for test compatibility: `class Chatbot(PaperChatbot): pass`. Exposes identical `preguntar(paper_text, question, history_text) -> str` interface.
- **Source**: `chatbot.py:56-57`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperChatbot` | inherits | `class Chatbot(PaperChatbot)` — backward-compat alias | LOW | `chatbot.py:56` |

**Inbound Edges:** None found in the extracted corpus (alias is present for tests only).

---

#### service:SotaAnalyzer

- **Node ID**: `service:SotaAnalyzer`
- **Type**: service
- **Module**: backend_core
- **Description**: 5-step SOTA analysis pipeline. Creates 1 LLMClient and 5 SOTA skills. Entry point: `analyze_sota(paper_text) -> Dict[str, Any]`.
- **Source**: `extracted_backend_core_01.md#3.5-SOTA-Analyzer-Service`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `config:config_py` | reads | SOTA_CONFIG/SEMANTIC_SCHOLAR_BASE_URL/SEMANTIC_SCHOLAR_YEAR_RANGE | MEDIUM | extracted_backend_core_01.md#3.5 (sota_analyzer.py:31) |
| `service:LLMClient` | instantiates | LLMClient(generation_config=SOTA_CONFIG) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:31) |
| `service:ThematicCoverageSkill` | instantiates | thematic_skill = ThematicCoverageSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:34) |
| `service:QueryGenerationSkill` | instantiates | query_skill = QueryGenerationSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:35) |
| `service:SemanticScholarSearchSkill` | instantiates | search_skill = SemanticScholarSearchSkill() | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:36) |
| `service:CoverageGapAnalysisSkill` | instantiates | gap_skill = CoverageGapAnalysisSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:37) |
| `service:CrossValidationSkill` | instantiates | validation_skill = CrossValidationSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:38) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:sota_section` | calls | st.session_state.sota_analyzer.analyze_sota(md_text) | HIGH | extracted_frontend_01.md#5.5 (sota_section.py:12) |
| `service:session_state` | instantiates | SotaAnalyzer() stored as st.session_state['sota_analyzer'] | HIGH | extracted_frontend_01.md#3 (session_state.py:17-18) |
| `external:st.session_state` | reads | sota_analyzer key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |

---

#### service:LLMClient

- **Node ID**: `service:LLMClient`
- **Type**: service
- **Module**: backend_core
- **Description**: Google Gemini wrapper. Constructor: `LLMClient(model_name=None, generation_config=None)`. Method `generate(prompt)` with exponential backoff retry (max 5 retries) on HTTP 503/429/UNAVAILABLE. Raises ValueError if GOOGLE_API_KEY absent.
- **Source**: `extracted_backend_core_01.md#3.1-LLM-Client`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `config:config_py` | reads | GOOGLE_API_KEY/MODEL_NAME | CRITICAL | extracted_backend_core_01.md#3.1 (llm_client.py:19,25) |
| `external:GoogleGeminiAPI` | calls | client.models.generate_content(model, contents, config) | CRITICAL | extracted_backend_core_01.md#3.1 (llm_client.py:44-48) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | 5 LLMClient instances (extraction/evaluation/rag_map/rag_reduce/verification) | CRITICAL | extracted_backend_core_01.md#3.2 |
| `service:PaperChatbot` | instantiates | LLMClient(generation_config=CHAT_CONFIG) | HIGH | extracted_backend_core_01.md#3.3 |
| `service:SotaAnalyzer` | instantiates | LLMClient(generation_config=SOTA_CONFIG) | HIGH | extracted_backend_core_01.md#3.5 |
| `service:InformationExtractionSkill` | calls | llm_client.generate(prompt) [MAP and REDUCE phases] | CRITICAL | extracted_backend_skills_01.md#3.2 |
| `service:ReproducibilityEvaluationSkill` | calls | llm_client.generate(evaluation_prompt) | CRITICAL | extracted_backend_skills_01.md#3.2 |
| `service:ChecklistVerificationSkill` | calls | llm_client.generate(verification_prompt) [per priority item] | HIGH | extracted_backend_skills_01.md#3.2 |
| `service:HybridHyperparameterExtractionSkill` | calls | llm_client.generate(prompt) [MAP phase] | HIGH | extracted_backend_skills_01.md#4.3 |
| `service:ThematicCoverageSkill` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 |
| `service:QueryGenerationSkill` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 |
| `service:CoverageGapAnalysisSkill` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 |
| `service:CrossValidationSkill` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 |
| `service:ConversationalResponseSkill` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#7.2 |

---

#### service:convert_pdf_to_markdown

- **Node ID**: `service:convert_pdf_to_markdown`
- **Type**: service
- **Module**: backend_core
- **Description**: Docling-based chunked PDF→Markdown converter. Signature: `convert_pdf_to_markdown(pdf_path) -> str`. Processes PDF in chunks of 5 pages using DocumentConverter with `do_ocr=False`, `do_table_structure=True`.
- **Source**: `extracted_backend_core_01.md#3.4-PDF-Parser-Service`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `external:Docling` | calls | DocumentConverter.convert(tmp_path) -> result.document.export_to_markdown() | HIGH | extracted_backend_core_01.md#4.1 (pdf_parser.py:39-71) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:file_uploader` | calls | convert_pdf_to_markdown(temp_path) | HIGH | extracted_frontend_01.md#5.1 (file_uploader.py:36) |

---

### Config Namespaces

#### config:config_py

- **Node ID**: `config:config_py`
- **Type**: config
- **Module**: backend_core
- **Description**: Centralized configuration: API keys (GOOGLE_API_KEY, SEMANTIC_SCHOLAR_API_KEY), model name constants (EXTRACTION_MODEL_NAME, MAP_MODEL_NAME, etc.), temperature constants (AUDIT_TEMPERATURE=0.0, CHAT_TEMPERATURE=0.2, SOTA_TEMPERATURE=0.1), generation config dicts (AUDIT_CONFIG, CHAT_CONFIG, SOTA_CONFIG), Semantic Scholar settings (BASE_URL, YEAR_RANGE=2023-2026, LIMIT=5, FIELDS).
- **Source**: `extracted_backend_core_01.md#2.1-config.py`

**Outbound Edges:** None (terminal config namespace)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | reads | GOOGLE_API_KEY/MODEL_NAME | CRITICAL | extracted_backend_core_01.md#3.1 |
| `service:PaperAuditor` | reads | AUDIT_CONFIG/model name constants | MEDIUM | extracted_backend_core_01.md#3.2 |
| `service:PaperChatbot` | reads | CHAT_CONFIG | MEDIUM | extracted_backend_core_01.md#3.3 |
| `service:SotaAnalyzer` | reads | SOTA_CONFIG/Semantic Scholar constants | MEDIUM | extracted_backend_core_01.md#3.5 |

---

#### config:prompts_py

- **Node ID**: `config:prompts_py`
- **Type**: config
- **Module**: backend_core
- **Description**: All LLM prompt template functions: `get_extraction_prompt(paper_text, red_flags)`, `get_map_extraction_prompt(fragment_text)`, `get_reduce_extraction_prompt(map_results)`, `get_evaluation_signals(extracted_info)`, `get_evaluation_prompt(extracted_info, red_flags)`, `get_verification_prompt(item_key, item_data, paper_context)`.
- **Source**: `extracted_backend_core_01.md#2.2-prompts.py`

**Outbound Edges:** None (terminal config namespace)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:InformationExtractionSkill` | reads | get_map_extraction_prompt/get_reduce_extraction_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 |
| `service:ReproducibilityEvaluationSkill` | reads | get_evaluation_signals/get_evaluation_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 |
| `service:ChecklistVerificationSkill` | reads | get_verification_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 |

---

### Logging Utility Classes

#### service:CleanNetworkLogs

- **Node ID**: `service:CleanNetworkLogs`
- **Type**: service
- **Module**: backend_core
- **Description**: `logging.Filter` subclass. Applied via `logging.getLogger("httpx").addFilter(CleanNetworkLogs())` in `config.py`. Suppresses verbose HTTP network log records emitted by `httpx` to reduce application log noise.
- **Source**: `config.py:14`

**Outbound Edges:** None

**Inbound Edges:** None (applied as a filter directly to the httpx logger at module load time)

---

#### service:ColoredFormatter

- **Node ID**: `service:ColoredFormatter`
- **Type**: service
- **Module**: backend_core
- **Description**: `logging.Formatter` subclass. `FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"`. Maps log levels to ANSI color codes via `LEVEL_COLORS` dict: `DEBUG→Blue`, `INFO→Green`, `WARNING→Yellow`, `ERROR→Red`, `CRITICAL→Bold+Red`. Special case: messages containing "HTTP Request" receive Cyan color on the message body. Used by `get_logger()` to configure each logger's `StreamHandler`.
- **Source**: `logger.py:10-35`

**Outbound Edges:** None

**Inbound Edges:** None (instantiated inside `get_logger()` as a local formatter)

---

#### service:Colors

- **Node ID**: `service:Colors`
- **Type**: service
- **Module**: backend_core
- **Description**: ANSI escape-code constants class. Constants: `BLUE="\033[94m"`, `CYAN="\033[96m"`, `GREEN="\033[92m"`, `YELLOW="\033[93m"`, `RED="\033[91m"`, `MAGENTA="\033[95m"`, `BOLD="\033[1m"`, `RESET="\033[0m"`. Used by `ColoredFormatter` for terminal log coloring.
- **Source**: `logger.py:5-13`

**Outbound Edges:** None

**Inbound Edges:** None (referenced as constants by `ColoredFormatter`)

---

## Module: backend_skills

### Base Infrastructure

#### class:BaseSkill

- **Node ID**: `class:BaseSkill`
- **Type**: class
- **Module**: backend_skills
- **Description**: Abstract base class (ABC) for all skills. Abstract method: `execute(context: Dict[str, Any]) -> Dict[str, Any]`. Helper methods: `validate_context(context, required_keys) -> bool`, `log_execution(message, level)`. Subclass `CompositeSkill` chains multiple skills sequentially.
- **Source**: `base_skill.py:9-70`

**Outbound Edges:** None (abstract base class)

**Inbound Edges:** All 25 concrete skill classes inherit from BaseSkill (inheritance not shown as individual edges; documented here for completeness). `class:CompositeSkill` explicitly inherits (see edge below).

---

#### class:CompositeSkill

- **Node ID**: `class:CompositeSkill`
- **Type**: class
- **Module**: backend_skills
- **Description**: Concrete subclass of BaseSkill that executes multiple skills sequentially. Constructor: `CompositeSkill(skills: list[BaseSkill], llm_client=None)`. `execute(context)` iterates `self.skills`, calls each `skill.execute(accumulated_context)`, updates the accumulated context with each result, and captures per-skill errors in `context['error_<skill.name>']` without aborting the chain.
- **Source**: `base_skill.py:67-113`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `class:BaseSkill` | inherits | `class CompositeSkill(BaseSkill)` | HIGH | `base_skill.py:67` |

**Inbound Edges:** None found in source. `CompositeSkill` is available as an exported skill but is not instantiated by any service in the extracted corpus.

---

#### class:Hyperparameters

- **Node ID**: `class:Hyperparameters`
- **Type**: class
- **Module**: backend_skills
- **Description**: Pydantic `BaseModel` with 14 required `str` fields representing ML training hyperparameters extracted from a paper: `thought_process`, `learning_rate`, `batch_size`, `epochs`, `optimizer`, `warmup_steps`, `weight_decay`, `random_seed`, `betas`, `epsilon`, `training_steps`, `total_tokens`, `hardware`, `latency_metrics`. All fields use sentinel string `"NOT FOUND"` when absent. Used as `response_schema` in `HybridHyperparameterExtractionSkill`'s REDUCE-phase fallback LLM call.
- **Source**: `rag_extraction_skill.py:11`

**Outbound Edges:** None

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:HybridHyperparameterExtractionSkill` | uses | `response_schema=Hyperparameters` in REDUCE phase fallback LLM call | MEDIUM | `rag_extraction_skill.py:239` |

---

### Auditor Skills

#### service:InformationExtractionSkill

- **Node ID**: `service:InformationExtractionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: MAP-REDUCE LLM extraction of paper metadata. Splits paper into ≤4 fragments, calls `get_map_extraction_prompt` per fragment via `LLMClient.generate()` (2s inter-fragment sleep), then consolidates via `get_reduce_extraction_prompt`. Returns `{extracted_info, invalid_paper, map_steps, reduce_step}`.
- **Source**: `extracted_backend_skills_01.md#3.2-InformationExtractionSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) [MAP and REDUCE phases] | CRITICAL | extracted_backend_skills_01.md#3.2 (auditor_skills.py:77,113) |
| `config:prompts_py` | reads | get_map_extraction_prompt/get_reduce_extraction_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 (auditor_skills.py:36,113) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | extraction_skill = InformationExtractionSkill(...) | CRITICAL | extracted_backend_core_01.md#3.2 |

---

#### service:ReproducibilityEvaluationSkill

- **Node ID**: `service:ReproducibilityEvaluationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: LLM-based evaluation of 16 NeurIPS checklist items. Calls `get_evaluation_signals` then `get_evaluation_prompt` via `LLMClient.generate()`. Returns `{evaluation: dict(16 items), evaluation_signals}`.
- **Source**: `extracted_backend_skills_01.md#3.2-ReproducibilityEvaluationSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(evaluation_prompt) | CRITICAL | extracted_backend_skills_01.md#3.2 (auditor_skills.py:200) |
| `config:prompts_py` | reads | get_evaluation_signals/get_evaluation_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 (auditor_skills.py:198-200) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | evaluation_skill = ReproducibilityEvaluationSkill(...) | CRITICAL | extracted_backend_core_01.md#3.2 |

---

#### service:MetricsCalculationSkill

- **Node ID**: `service:MetricsCalculationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: No-LLM skill. Computes audit metrics from context: `tiempo_segundos` (execution time), `caracteres_leidos` (paper length), `red_flags_detectadas` (count of critical flags). Returns `{metrics: {tiempo_segundos, caracteres_leidos, red_flags_detectadas}}`.
- **Source**: `extracted_backend_skills_01.md#3.2-MetricsCalculationSkill`

**Outbound Edges:** None (pure computation, no external calls)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | metrics_skill = MetricsCalculationSkill() | MEDIUM | extracted_backend_core_01.md#3.2 |

---

#### service:MetadataAggregationSkill

- **Node ID**: `service:MetadataAggregationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: No-LLM skill. Aggregates all 23 result fields from context into flat dict: 16 checklist items + informacion_extraida + red_flags + metricas + general_analysis_map + general_analysis_reduce + hybrid_triage_fragments + evaluation_signals.
- **Source**: `extracted_backend_skills_01.md#3.2-MetadataAggregationSkill`

**Outbound Edges:** None (pure aggregation, no external calls)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | metadata_skill = MetadataAggregationSkill() | MEDIUM | extracted_backend_core_01.md#3.2 |

---

#### service:ChecklistVerificationSkill

- **Node ID**: `service:ChecklistVerificationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT in `__init__.py` exports. Strict verification (Auditor 2) of up to 8 priority checklist items via LLMClient. Calls `get_verification_prompt` per item. Priority items: claims, experimental_result_reproducibility, open_access_data_code, experimental_setting_details, experiments_compute_resource, experiment_statistical_significance, licenses, declaration_llm_usage.
- **Source**: `extracted_backend_skills_01.md#3.2-ChecklistVerificationSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(verification_prompt) [per priority item] | HIGH | extracted_backend_skills_01.md#3.2 (auditor_skills.py:362) |
| `config:prompts_py` | reads | get_verification_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 (auditor_skills.py:362) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | verification_skill = ChecklistVerificationSkill(...) | HIGH | extracted_backend_core_01.md#3.2 |

---

#### service:HybridHyperparameterExtractionSkill

- **Node ID**: `service:HybridHyperparameterExtractionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT in `__init__.py` exports. RAG+Pydantic hyperparameter extraction: chunk→embed (Google Generative Language API via httpx, batch=15)→ChromaDB→13 RAG queries→MAP LLM per relevant chunk→REDUCE LLM with Pydantic schema→regex cleaning. Returns `{extracted_hyperparameters_hybrid, triage_fragments}`.
- **Source**: `extracted_backend_skills_01.md#4-RAG-Extraction-Skill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) [MAP phase] + llm_client.client.models.embed_content [RAG queries] | HIGH | extracted_backend_skills_01.md#4.3 (rag_extraction_skill.py:143,459) |
| `external:GoogleGeminiAPI` | calls | httpx.post batchEmbedContents API (batch=15 chunks, 15s inter-batch sleep) | HIGH | extracted_backend_skills_01.md#4.3 (rag_extraction_skill.py:56-82) |
| `class:Hyperparameters` | uses | `response_schema=Hyperparameters` in REDUCE phase fallback LLM call | MEDIUM | rag_extraction_skill.py:239 |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm) | HIGH | extracted_backend_core_01.md#3.2 |

---

### SOTA Skills

#### service:ThematicCoverageSkill

- **Node ID**: `service:ThematicCoverageSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: SOTA Step 1. Calls `LLMClient.generate()` to identify 3-5 subtemas, areas_tecnicas, and año_paper from the paper. Returns `{thematic_data: {subtemas, areas_tecnicas, año_paper}}`.
- **Source**: `extracted_backend_skills_01.md#6.2-ThematicCoverageSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:24) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:SotaAnalyzer` | instantiates | thematic_skill = ThematicCoverageSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 |

---

#### service:QueryGenerationSkill

- **Node ID**: `service:QueryGenerationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: SOTA Step 2. Generates 3 English search queries from thematic_data via `LLMClient.generate()`. Returns `{search_queries: ['query1', 'query2', 'query3']}`.
- **Source**: `extracted_backend_skills_01.md#6.2-QueryGenerationSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:97) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:SotaAnalyzer` | instantiates | query_skill = QueryGenerationSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 |

---

#### service:SemanticScholarSearchSkill

- **Node ID**: `service:SemanticScholarSearchSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: SOTA Step 3. No LLMClient. Calls Semantic Scholar API via `requests.get(SEMANTIC_SCHOLAR_BASE_URL, ...)` for each query, 0.5s inter-query sleep, 15s timeout, deduplicates and returns top 10 papers by citationCount. Returns `{sota_papers: list}`.
- **Source**: `extracted_backend_skills_01.md#6.2-SemanticScholarSearchSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `external:SemanticScholarAPI` | calls | GET /graph/v1/paper/search?query=...&year=2023-2026&limit=5 | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:162) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:SotaAnalyzer` | instantiates | search_skill = SemanticScholarSearchSkill() | HIGH | extracted_backend_core_01.md#3.5 |

---

#### service:CoverageGapAnalysisSkill

- **Node ID**: `service:CoverageGapAnalysisSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: SOTA Step 4. Calls `LLMClient.generate()` to identify subtemas with low bibliographic coverage. Returns `{coverage_gaps: {areas_debiles: list}}`.
- **Source**: `extracted_backend_skills_01.md#6.2-CoverageGapAnalysisSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:246) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:SotaAnalyzer` | instantiates | gap_skill = CoverageGapAnalysisSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 |

---

#### service:CrossValidationSkill

- **Node ID**: `service:CrossValidationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: SOTA Step 5. Calls `LLMClient.generate()` to identify up to 5 omitted SOTA papers via LLM comparison of paper references vs sota_papers. Returns `{validation_results: {papers_omitidos, conclusion_sota, cobertura_tematica, papers_analizados}}`.
- **Source**: `extracted_backend_skills_01.md#6.2-CrossValidationSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:309) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:SotaAnalyzer` | instantiates | validation_skill = CrossValidationSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 |

---

### Chatbot Skills

#### service:ConversationalResponseSkill

- **Node ID**: `service:ConversationalResponseSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: Chatbot skill. Calls `LLMClient.generate()` with NeurIPS Senior Area Chair persona prompt using paper_text, question, and history_text context. Returns `{response: str}` (raw LLM text, no JSON parsing).
- **Source**: `extracted_backend_skills_01.md#7.2-ConversationalResponseSkill`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#7.2 (chatbot_skills.py:14) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperChatbot` | instantiates | response_skill = ConversationalResponseSkill(llm_client=self.llm_client) | HIGH | extracted_backend_core_01.md#3.3 |

---

#### service:ContextValidationSkill

- **Node ID**: `service:ContextValidationSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: Chatbot validation skill. No LLMClient. Validates paper_text and question are non-empty strings. Returns `{is_valid: bool, paper_text: str, question: str, history_text: str, paper_length: int, question_length: int}`.
- **Source**: `extracted_backend_skills_01.md#7.2-ContextValidationSkill`

**Outbound Edges:** None (pure validation, no external calls)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperChatbot` | instantiates | validation_skill = ContextValidationSkill() | MEDIUM | extracted_backend_core_01.md#3.3 |

---

### Regex Detection Skills (Exported)

#### service:LimitationsQualityDetectionSkill

- **Node ID**: `service:LimitationsQualityDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: Exported. Regex skill detecting limitations section quality. `SPECIFIC_PATTERNS` (3 patterns for quantified limitations), `SECTION_PATTERN` (section header regex). Returns `{limitations_flags: {tiene_seccion_limitaciones, limitaciones_vagas, puntos_especificos_limitaciones}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-LimitationsQualityDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction — skill is exported but call site not documented in extracted cluster files]

---

#### service:SoftwareVersionDetectionSkill

- **Node ID**: `service:SoftwareVersionDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: Exported. Regex skill detecting software version mentions (PyTorch, Python, CUDA etc.). 4 patterns. Returns `{software_flags: {tiene_versiones_software, cantidad_versiones}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-SoftwareVersionDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction — skill is exported but call site not documented in extracted cluster files]

---

#### service:HardwareDetailDetectionSkill

- **Node ID**: `service:HardwareDetailDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: Exported. Regex skill detecting hardware details. `PATTERNS`: `{gpu_model: 2 patterns, gpu_count: 2, gpu_memory: 2, training_time: 2}`. Returns `{hardware_detail_flags: {tiene_gpu_model, tiene_gpu_count, tiene_gpu_memory, tiene_training_time}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-HardwareDetailDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction — skill is exported but call site not documented in extracted cluster files]

---

### Regex Detection Skills (Internal)

#### service:HyperparameterDetectionSkill

- **Node ID**: `service:HyperparameterDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting hyperparameter presence. `PATTERNS`: `{optimizer, learning_rate, batch_size, epochs, warmup, weight_decay, betas, epsilon, vague}`. Searches tables first (without negation), then full text (with negation). Returns `{hyperparameter_flags}`.
- **Source**: `extracted_backend_skills_01.md#5.2-HyperparameterDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction — used by HybridHyperparameterExtractionSkill or auditor but call site not explicitly documented]

---

#### service:DataAvailabilityDetectionSkill

- **Node ID**: `service:DataAvailabilityDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting data availability signals. `PATTERNS`: `{proprietary, available, doi, cannot_release}`. Returns `{data_flags: {datos_propietarios, datos_sin_acceso, tiene_doi_datos, cannot_release_data}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-DataAvailabilityDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:CodeAvailabilityDetectionSkill

- **Node ID**: `service:CodeAvailabilityDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting code availability signals. `PATTERNS`: `{proprietary, repository (6 patterns), github, cannot_release}`. Returns `{code_flags: {codigo_propietario, sin_repositorio, tiene_github, cannot_release_code}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-CodeAvailabilityDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:StatisticsDetectionSkill

- **Node ID**: `service:StatisticsDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting statistical rigor signals. `PATTERNS`: `{confidence_intervals (6 patterns), significance (5 patterns), multiple_runs (5 patterns)}`. Returns `{statistics_flags: {sin_intervalos_confianza, sin_significancia, sin_multiple_runs}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-StatisticsDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:EnvironmentalImpactDetectionSkill

- **Node ID**: `service:EnvironmentalImpactDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting environmental impact disclosures. `PATTERNS`: `{carbon_footprint (5 patterns), energy_consumption (4 patterns), pue (3 patterns)}`. Returns `{environmental_flags: {tiene_carbon_footprint, tiene_energy_consumption, tiene_pue}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-EnvironmentalImpactDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:ProblematicPhrasesDetectionSkill

- **Node ID**: `service:ProblematicPhrasesDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting problematic NDA-like phrases. `PATTERNS`: `{competitive_concerns, cannot_release, remain_confidential}`. Returns `{problematic_flags: {competitive_concerns, cannot_release, remain_confidential}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-ProblematicPhrasesDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:LlmUsageDetectionSkill

- **Node ID**: `service:LlmUsageDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting LLM usage in methodology. Single pattern combining model names with action verbs. Returns `{llm_usage_flags: {usa_llm_como_herramienta: bool}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-LlmUsageDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:CrowdsourcingDetectionSkill

- **Node ID**: `service:CrowdsourcingDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting crowdsourcing/human subjects. Uses `CROWDSOURCING_ACTIVE` (4 patterns), `HUMAN_DATASET_USE` (2 patterns), `COMPENSATION` (1 pattern), `NEGATION_CROWD` (1 pattern). `NEGATION_CROWD` gates all other patterns. Returns `{crowdsourcing_flags}`.
- **Source**: `extracted_backend_skills_01.md#5.2-CrowdsourcingDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

#### service:LicenseDetectionSkill

- **Node ID**: `service:LicenseDetectionSkill`
- **Type**: service
- **Module**: backend_skills
- **Description**: NOT exported. Regex skill detecting license mentions. `EXPLICIT_LICENSE` pattern, `KNOWN_DATASETS` pattern (20 dataset names). Returns `{license_flags: {menciona_licencia, usa_datasets_conocidos, posible_licencia_faltante}}`.
- **Source**: `extracted_backend_skills_01.md#5.2-LicenseDetectionSkill`

**Outbound Edges:** None (pure regex, no external calls)

**Inbound Edges:** [GAP: direct caller not identified in extraction]

---

## Module: frontend

### UI Screens

#### screen:file_uploader

- **Node ID**: `screen:file_uploader`
- **Type**: screen
- **Module**: frontend
- **Description**: Handles file upload (PDF/TXT/MD). Function: `process_uploaded_file(uploaded_file) -> (md_text: str, resultado: dict)`. MD5 deduplication via `session_state.file_hash`. Calls `convert_pdf_to_markdown` for PDFs or reads directly for TXT/MD. Calls `auditor.audit()` and stores resultado in session_state.
- **Source**: `extracted_frontend_01.md#5.1-File-Uploader`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `external:st.session_state` | writes | resultado/md_text/file_hash/archivo_actual/messages | HIGH | extracted_frontend_01.md#5.1 (file_uploader.py:19-52) |
| `service:PaperAuditor` | calls | st.session_state.auditor.audit(md_text, status_callback=update_status) | CRITICAL | extracted_frontend_01.md#5.1 (file_uploader.py:49) |
| `service:convert_pdf_to_markdown` | calls | convert_pdf_to_markdown(temp_path) | HIGH | extracted_frontend_01.md#5.1 (file_uploader.py:36) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:app` | calls | process_uploaded_file(uploaded_file) | CRITICAL | extracted_root_tests_scratch_01.md#3.5 (app.py:54) |

---

#### screen:audit_results

- **Node ID**: `screen:audit_results`
- **Type**: screen
- **Module**: frontend
- **Description**: Renders full audit results page. Function: `render_audit_results(resultado, uploaded_file) -> health: dict`. Calls `get_checklist_health(resultado)`. Renders verdict block, 4-column metrics row, RAG Ficha Técnica, compliance table (`_build_table_html`), and 3 expanders. Contains `generate_report()` and `_build_table_html()` helpers.
- **Source**: `extracted_frontend_01.md#5.2-Audit-Results-Display`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `external:st.session_state` | reads | resultado | MEDIUM | extracted_frontend_01.md#5.2 (audit_results.py:90) |
| `service:scoring` | calls | get_checklist_health(resultado) | HIGH | extracted_frontend_01.md#5.2 (audit_results.py:94) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:app` | calls | render_audit_results(resultado, uploaded_file) | CRITICAL | extracted_root_tests_scratch_01.md#3.5 (app.py:66) |

---

#### screen:chatbot

- **Node ID**: `screen:chatbot`
- **Type**: screen
- **Module**: frontend
- **Description**: Interactive chat section. Function: `render_chatbot(md_text: str) -> None`. Reads/writes `st.session_state.messages`. On submit calls `st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str)`. Calls `st.rerun()` after each response.
- **Source**: `extracted_frontend_01.md#5.3-Chatbot-Interface`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `external:st.session_state` | reads | chatbot/messages | HIGH | extracted_frontend_01.md#5.3 (chatbot.py:10,26) |
| `service:PaperChatbot` | calls | st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str) | CRITICAL | extracted_frontend_01.md#5.3 (chatbot.py:26) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:app` | calls | render_chatbot(md_text) | HIGH | extracted_root_tests_scratch_01.md#3.5 (app.py:68) |

---

#### screen:gauge_chart

- **Node ID**: `screen:gauge_chart`
- **Type**: screen
- **Module**: frontend
- **Description**: Pure function: `create_gauge_chart(score: float) -> plotly.graph_objects.Figure`. NeurIPS quality score gauge with 6 tiers (Strong Accept/Accept/Borderline/Weak Reject/Reject/Strong Reject). Threshold line at 62.5. [GAP: caller not identified in extracted cluster files — call site not documented in extracted_frontend_01.md or extracted_root_tests_scratch_01.md]
- **Source**: `extracted_frontend_01.md#5.4-Gauge-Chart`

**Outbound Edges:** None (returns a Plotly Figure object, no service calls)

**Inbound Edges:** [GAP: caller not identified in extracted cluster files]

---

#### screen:sota_section

- **Node ID**: `screen:sota_section`
- **Type**: screen
- **Module**: frontend
- **Description**: SOTA analysis section. Function: `render_sota_analysis(md_text: str) -> None`. On button press calls `st.session_state.sota_analyzer.analyze_sota(md_text)`. Renders conclusion, papers dataframe, and `_render_missing_papers()` for uncited papers.
- **Source**: `extracted_frontend_01.md#5.5-SOTA-Section`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `external:st.session_state` | reads | sota_analyzer | HIGH | extracted_frontend_01.md#5.5 (sota_section.py:12) |
| `service:SotaAnalyzer` | calls | st.session_state.sota_analyzer.analyze_sota(md_text) | HIGH | extracted_frontend_01.md#5.5 (sota_section.py:12) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:app` | calls | render_sota_analysis(md_text) | HIGH | extracted_root_tests_scratch_01.md#3.5 (app.py:67) |

---

### Frontend Services

#### service:custom_css

- **Node ID**: `service:custom_css`
- **Type**: service
- **Module**: frontend
- **Description**: Defines `CUSTOM_CSS` string constant with dark-theme style block. Function: `apply_custom_styles() -> None` calls `st.markdown(CUSTOM_CSS, unsafe_allow_html=True)`. Targets: `.stApp` (dark grey bg), `#MainMenu` (hidden), `footer` (hidden), `stTable` (dark rounded bg), `stPlotlyChart` (dark rounded bg).
- **Source**: `extracted_frontend_01.md#6-Custom-CSS`

**Outbound Edges:** None (injects static CSS into Streamlit page)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:app` | calls | apply_custom_styles() | LOW | extracted_root_tests_scratch_01.md#3.4 (app.py:40) |

---

#### service:scoring

- **Node ID**: `service:scoring`
- **Type**: service
- **Module**: frontend
- **Description**: Defines `CHECKLIST_KEYS` (16-item list), `CHECKLIST_LABELS` (dict), and `get_checklist_health(evaluation: dict) -> dict`. Risk detection: missing_evidence for Yes answers, pending_justification for No answers. Special crowdsourcing_human_subjects rule. Returns `{status, items(16), pending_count, total}`.
- **Source**: `extracted_frontend_01.md#7-Scoring-Logic`

**Outbound Edges:** None (pure computation)

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:audit_results` | calls | get_checklist_health(resultado) | HIGH | extracted_frontend_01.md#5.2 (audit_results.py:94) |

---

#### service:session_state

- **Node ID**: `service:session_state`
- **Type**: service
- **Module**: frontend
- **Description**: Function: `initialize_session_state() -> None`. Initialises 5 session state keys with idempotent guards: resultado (None), auditor (PaperAuditor()), chatbot (PaperChatbot()), sota_analyzer (SotaAnalyzer()), messages ([]). Instantiates all three backend services into Streamlit session state.
- **Source**: `extracted_frontend_01.md#3-Session-State`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | instantiates | PaperAuditor() stored as st.session_state['auditor'] | HIGH | extracted_frontend_01.md#3 (session_state.py:11-12) |
| `service:PaperChatbot` | instantiates | PaperChatbot() stored as st.session_state['chatbot'] | HIGH | extracted_frontend_01.md#3 (session_state.py:14-15) |
| `service:SotaAnalyzer` | instantiates | SotaAnalyzer() stored as st.session_state['sota_analyzer'] | HIGH | extracted_frontend_01.md#3 (session_state.py:17-18) |

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:app` | calls | initialize_session_state() | HIGH | extracted_root_tests_scratch_01.md#3.4 (app.py:41) |

---

## Module: root

### Entry Point

#### screen:app

- **Node ID**: `screen:app`
- **Type**: screen
- **Module**: root
- **Description**: Main Streamlit application entry point (root `app.py`, 74 lines). Imports and orchestrates all frontend components. Initialization: `apply_custom_styles()`, `initialize_session_state()`, `st.title()`, `st.file_uploader()`. On upload: `process_uploaded_file()` then `render_audit_results()`, `render_sota_analysis()`, `render_chatbot()`, `generate_report()`. Page config: title='Nature Auditor Pro', layout='wide', page_icon='🔬'.
- **Source**: `extracted_root_tests_scratch_01.md#3-Application-Entry-Point`

**Outbound Edges:**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:file_uploader` | calls | process_uploaded_file(uploaded_file) | CRITICAL | extracted_root_tests_scratch_01.md#3.5 (app.py:54) |
| `screen:audit_results` | calls | render_audit_results(resultado, uploaded_file) | CRITICAL | extracted_root_tests_scratch_01.md#3.5 (app.py:66) |
| `screen:chatbot` | calls | render_chatbot(md_text) | HIGH | extracted_root_tests_scratch_01.md#3.5 (app.py:68) |
| `screen:sota_section` | calls | render_sota_analysis(md_text) | HIGH | extracted_root_tests_scratch_01.md#3.5 (app.py:67) |
| `service:custom_css` | calls | apply_custom_styles() | LOW | extracted_root_tests_scratch_01.md#3.4 (app.py:40) |
| `service:session_state` | calls | initialize_session_state() | HIGH | extracted_root_tests_scratch_01.md#3.4 (app.py:41) |

**Inbound Edges:** None (root entry point; invoked directly by Streamlit runtime)

---

### Entity Nodes (Unresolved)

#### entity:AuditState

- **Node ID**: `entity:AuditState`
- **Type**: entity
- **Module**: root
- **Description**: [GAP: entity definition not found in extraction — `test_audit_state.py` imports `AuditState` from `backend.common.audit_state` which does not exist in the current codebase. The class was removed during the skills-architecture refactoring. Source file `backend/common/audit_state.py` is absent.]
- **Source**: `cross_ref_resolution_cross_ref_root_to_backend.md#g_014`

**Outbound Edges:** [GAP: entity does not exist in current codebase — no edges resolvable]

**Inbound Edges:** [GAP: entity does not exist in current codebase — no edges resolvable]

---

#### entity:ExtractedInfo

- **Node ID**: `entity:ExtractedInfo`
- **Type**: entity
- **Module**: root
- **Description**: [GAP: entity definition not found in extraction — `test_audit_state.py` imports `ExtractedInfo` from `backend.common.audit_state` which does not exist in the current codebase. Source file `backend/common/audit_state.py` is absent.]
- **Source**: `cross_ref_resolution_cross_ref_root_to_backend.md#g_014`

**Outbound Edges:** [GAP: entity does not exist in current codebase — no edges resolvable]

**Inbound Edges:** [GAP: entity does not exist in current codebase — no edges resolvable]

---

#### entity:ChecklistItem

- **Node ID**: `entity:ChecklistItem`
- **Type**: entity
- **Module**: root
- **Description**: [GAP: entity definition not found in extraction — `test_audit_state.py` imports `ChecklistItem` from `backend.common.audit_state` which does not exist in the current codebase. Source file `backend/common/audit_state.py` is absent.]
- **Source**: `cross_ref_resolution_cross_ref_root_to_backend.md#g_014`

**Outbound Edges:** [GAP: entity does not exist in current codebase — no edges resolvable]

**Inbound Edges:** [GAP: entity does not exist in current codebase — no edges resolvable]

---

## Cross-Module Edges

All edges where the source node's module differs from the target node's module. Sorted by severity (CRITICAL first).

| From | To | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|---|
| `screen:file_uploader` | `service:PaperAuditor` | calls | st.session_state.auditor.audit(md_text, status_callback=update_status) | CRITICAL | extracted_frontend_01.md#5.1 (file_uploader.py:49) |
| `screen:app` | `screen:file_uploader` | calls | process_uploaded_file(uploaded_file) | CRITICAL | extracted_root_tests_scratch_01.md#3.5 (app.py:54) |
| `screen:app` | `screen:audit_results` | calls | render_audit_results(resultado, uploaded_file) | CRITICAL | extracted_root_tests_scratch_01.md#3.5 (app.py:66) |
| `service:PaperAuditor` | `service:InformationExtractionSkill` | instantiates | extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm) | CRITICAL | extracted_backend_core_01.md#3.2 (auditor.py:46) |
| `service:PaperAuditor` | `service:ReproducibilityEvaluationSkill` | instantiates | evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm) | CRITICAL | extracted_backend_core_01.md#3.2 (auditor.py:48) |
| `service:InformationExtractionSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) [MAP and REDUCE phases] | CRITICAL | extracted_backend_skills_01.md#3.2 (auditor_skills.py:77,113) |
| `service:ReproducibilityEvaluationSkill` | `service:LLMClient` | calls | llm_client.generate(evaluation_prompt) | CRITICAL | extracted_backend_skills_01.md#3.2 (auditor_skills.py:200) |
| `service:LLMClient` | `config:config_py` | reads | GOOGLE_API_KEY/MODEL_NAME | CRITICAL | extracted_backend_core_01.md#3.1 (llm_client.py:19,25) |
| `service:LLMClient` | `external:GoogleGeminiAPI` | calls | client.models.generate_content(model, contents, config) | CRITICAL | extracted_backend_core_01.md#3.1 (llm_client.py:44-48) |
| `screen:chatbot` | `service:PaperChatbot` | calls | st.session_state.chatbot.preguntar(md_text, prompt_usuario, history_str) | CRITICAL | extracted_frontend_01.md#5.3 (chatbot.py:26) |
| `service:convert_pdf_to_markdown` | `external:Docling` | calls | DocumentConverter.convert(tmp_path) -> result.document.export_to_markdown() | HIGH | extracted_backend_core_01.md#4.1 (pdf_parser.py:39-71) |
| `service:PaperAuditor` | `service:HybridHyperparameterExtractionSkill` | instantiates | hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm) | HIGH | extracted_backend_core_01.md#3.2 (auditor.py:47) |
| `service:PaperAuditor` | `service:ChecklistVerificationSkill` | instantiates | verification_skill = ChecklistVerificationSkill(llm_client=self.verification_llm) | HIGH | extracted_backend_core_01.md#3.2 (auditor.py:51) |
| `service:PaperAuditor` | `service:MetricsCalculationSkill` | instantiates | metrics_skill = MetricsCalculationSkill() | MEDIUM | extracted_backend_core_01.md#3.2 (auditor.py:53) |
| `service:PaperAuditor` | `service:MetadataAggregationSkill` | instantiates | metadata_skill = MetadataAggregationSkill() | MEDIUM | extracted_backend_core_01.md#3.2 (auditor.py:54) |
| `service:PaperChatbot` | `service:LLMClient` | instantiates | LLMClient(generation_config=CHAT_CONFIG) | HIGH | extracted_backend_core_01.md#3.3 (chatbot.py:17) |
| `service:PaperChatbot` | `service:ConversationalResponseSkill` | instantiates | response_skill = ConversationalResponseSkill(llm_client=self.llm_client) | HIGH | extracted_backend_core_01.md#3.3 (chatbot.py:20) |
| `service:PaperChatbot` | `service:ContextValidationSkill` | instantiates | validation_skill = ContextValidationSkill() | MEDIUM | extracted_backend_core_01.md#3.3 (chatbot.py:21) |
| `service:SotaAnalyzer` | `service:LLMClient` | instantiates | LLMClient(generation_config=SOTA_CONFIG) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:31) |
| `service:SotaAnalyzer` | `service:ThematicCoverageSkill` | instantiates | thematic_skill = ThematicCoverageSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:34) |
| `service:SotaAnalyzer` | `service:QueryGenerationSkill` | instantiates | query_skill = QueryGenerationSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:35) |
| `service:SotaAnalyzer` | `service:SemanticScholarSearchSkill` | instantiates | search_skill = SemanticScholarSearchSkill() | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:36) |
| `service:SotaAnalyzer` | `service:CoverageGapAnalysisSkill` | instantiates | gap_skill = CoverageGapAnalysisSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:37) |
| `service:SotaAnalyzer` | `service:CrossValidationSkill` | instantiates | validation_skill = CrossValidationSkill(llm_client=llm_client) | HIGH | extracted_backend_core_01.md#3.5 (sota_analyzer.py:38) |
| `service:ChecklistVerificationSkill` | `service:LLMClient` | calls | llm_client.generate(verification_prompt) [per priority item] | HIGH | extracted_backend_skills_01.md#3.2 (auditor_skills.py:362) |
| `service:ChecklistVerificationSkill` | `config:prompts_py` | reads | get_verification_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 (auditor_skills.py:362) |
| `service:HybridHyperparameterExtractionSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) [MAP phase] | HIGH | extracted_backend_skills_01.md#4.3 (rag_extraction_skill.py:143) |
| `service:HybridHyperparameterExtractionSkill` | `external:GoogleGeminiAPI` | calls | httpx.post batchEmbedContents API (batch=15, 15s sleep) | HIGH | extracted_backend_skills_01.md#4.3 (rag_extraction_skill.py:56-82) |
| `service:ThematicCoverageSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:24) |
| `service:QueryGenerationSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:97) |
| `service:SemanticScholarSearchSkill` | `external:SemanticScholarAPI` | calls | GET /graph/v1/paper/search?query=...&year=2023-2026&limit=5 | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:162) |
| `service:CoverageGapAnalysisSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:246) |
| `service:CrossValidationSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#6.2 (sota_skills.py:309) |
| `service:ConversationalResponseSkill` | `service:LLMClient` | calls | llm_client.generate(prompt) | HIGH | extracted_backend_skills_01.md#7.2 (chatbot_skills.py:14) |
| `service:InformationExtractionSkill` | `config:prompts_py` | reads | get_map_extraction_prompt/get_reduce_extraction_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 (auditor_skills.py:36,113) |
| `service:ReproducibilityEvaluationSkill` | `config:prompts_py` | reads | get_evaluation_signals/get_evaluation_prompt | MEDIUM | extracted_backend_skills_01.md#3.2 (auditor_skills.py:198-200) |
| `service:session_state` | `service:PaperAuditor` | instantiates | PaperAuditor() stored as st.session_state['auditor'] | HIGH | extracted_frontend_01.md#3 (session_state.py:11-12) |
| `service:session_state` | `service:PaperChatbot` | instantiates | PaperChatbot() stored as st.session_state['chatbot'] | HIGH | extracted_frontend_01.md#3 (session_state.py:14-15) |
| `service:session_state` | `service:SotaAnalyzer` | instantiates | SotaAnalyzer() stored as st.session_state['sota_analyzer'] | HIGH | extracted_frontend_01.md#3 (session_state.py:17-18) |
| `screen:file_uploader` | `external:st.session_state` | writes | resultado/md_text/file_hash/archivo_actual/messages | HIGH | extracted_frontend_01.md#5.1 (file_uploader.py:19-52) |
| `screen:audit_results` | `external:st.session_state` | reads | resultado | MEDIUM | extracted_frontend_01.md#5.2 (audit_results.py:90) |
| `screen:chatbot` | `external:st.session_state` | reads | chatbot/messages | HIGH | extracted_frontend_01.md#5.3 (chatbot.py:10,26) |
| `screen:sota_section` | `external:st.session_state` | reads | sota_analyzer | HIGH | extracted_frontend_01.md#5.5 (sota_section.py:12) |
| `external:st.session_state` | `service:PaperAuditor` | reads | auditor key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |
| `external:st.session_state` | `service:PaperChatbot` | reads | chatbot key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |
| `external:st.session_state` | `service:SotaAnalyzer` | reads | sota_analyzer key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |
| `screen:file_uploader` | `service:convert_pdf_to_markdown` | calls | convert_pdf_to_markdown(temp_path) | HIGH | extracted_frontend_01.md#5.1 (file_uploader.py:36) |
| `screen:app` | `screen:chatbot` | calls | render_chatbot(md_text) | HIGH | extracted_root_tests_scratch_01.md#3.5 (app.py:68) |
| `screen:app` | `screen:sota_section` | calls | render_sota_analysis(md_text) | HIGH | extracted_root_tests_scratch_01.md#3.5 (app.py:67) |
| `screen:app` | `service:session_state` | calls | initialize_session_state() | HIGH | extracted_root_tests_scratch_01.md#3.4 (app.py:41) |
| `screen:app` | `service:custom_css` | calls | apply_custom_styles() | LOW | extracted_root_tests_scratch_01.md#3.4 (app.py:40) |

---

## Detected Cycles

### Cycle 001 — Data-Flow Session State Cycle

- **ID**: `cycle_001`
- **Path**: `screen:file_uploader` → `external:st.session_state` → `screen:audit_results`
- **Classification**: `informational`
- **Description**: Data-flow cycle via shared state. `screen:file_uploader` writes `session_state.resultado` after calling `auditor.audit()`; `screen:audit_results` reads `session_state.resultado` to render the results. There is no execution loop — `screen:app` invokes both components in sequence (file_uploader first, then audit_results) on each Streamlit run. The data flows unidirectionally through shared state; the cycle is an artefact of the read/write representation, not a true execution loop.
- **Source**: `cross_ref_resolution_cross_ref_root_to_frontend.md` and `extracted_frontend_01.md#5.1,5.2`

---

## External System Nodes

#### external:GoogleGeminiAPI

- **Node ID**: `external:GoogleGeminiAPI`
- **Type**: external
- **Module**: external
- **Description**: Google Gemini generative AI API. Two call protocols: (1) `google.genai.Client` SDK for `generate_content` calls from `LLMClient.generate()`; (2) direct `httpx.post` to `https://generativelanguage.googleapis.com/v1beta/models/{model}:batchEmbedContents` for embedding batches from `HybridHyperparameterExtractionSkill`. Auth: GOOGLE_API_KEY env var.
- **Source**: `extracted_backend_core_01.md#3.1-LLM-Client`

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:LLMClient` | calls | client.models.generate_content(model, contents, config) | CRITICAL | extracted_backend_core_01.md#3.1 |
| `service:HybridHyperparameterExtractionSkill` | calls | httpx.post batchEmbedContents API (batch=15) | HIGH | extracted_backend_skills_01.md#4.3 |

---

#### external:SemanticScholarAPI

- **Node ID**: `external:SemanticScholarAPI`
- **Type**: external
- **Module**: external
- **Description**: Semantic Scholar paper search API. Endpoint: `GET https://api.semanticscholar.org/graph/v1/paper/search`. Params: `query`, `year=2023-2026`, `limit=5`, `fields=paperId/title/authors/year/citationCount/abstract/url`. Optional header: `x-api-key`. Timeout: 15s. Rate limit: sleep 2s on HTTP 429. Inter-query sleep: 0.5s. Returns top-10 deduplicated results by citationCount.
- **Source**: `extracted_backend_core_01.md#2.1-config.py`

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:SemanticScholarSearchSkill` | calls | GET /graph/v1/paper/search?query=...&year=2023-2026&limit=5 | HIGH | extracted_backend_skills_01.md#6.2 |

---

#### external:Docling

- **Node ID**: `external:Docling`
- **Type**: external
- **Module**: external
- **Description**: Local PDF-to-Markdown conversion library. Classes used: `DocumentConverter`, `PdfFormatOption`, `PdfPipelineOptions` (`do_ocr=False`, `do_table_structure=True`). Method: `converter.convert(tmp_path) -> result.document.export_to_markdown()`. GPU auto-detected via `torch.cuda.is_available()`. Processes in 5-page chunks.
- **Source**: `extracted_backend_core_01.md#4.1-PDF-Parse-Pipeline`

**Inbound Edges:**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:convert_pdf_to_markdown` | calls | DocumentConverter.convert(tmp_path) -> result.document.export_to_markdown() | HIGH | extracted_backend_core_01.md#4.1 |

---

#### external:Streamlit

- **Node ID**: `external:Streamlit`
- **Type**: external
- **Module**: external
- **Description**: Web UI framework used throughout frontend and root app. Key calls: `st.set_page_config`, `st.title`, `st.file_uploader`, `st.spinner`, `st.status`, `st.success`, `st.error`, `st.warning`, `st.info`, `st.markdown`, `st.header`, `st.subheader`, `st.metric`, `st.expander`, `st.download_button`, `st.rerun`, `st.sidebar`, `st.image`, `st.chat_message`, `st.html`, `st.dataframe`, `st.plotly_chart`.
- **Source**: `extracted_frontend_01.md#1-File-Index`

**Inbound Edges:** Implicit — all frontend screen nodes and `screen:app` use Streamlit widgets throughout their rendering logic. No single explicit edge documented; usage is pervasive and co-located with all screen nodes.

---

#### external:st.session_state

- **Node ID**: `external:st.session_state`
- **Type**: external
- **Module**: external
- **Description**: Streamlit in-process key-value store shared across all reruns. Keys managed: `resultado` (dict|None), `auditor` (PaperAuditor), `chatbot` (PaperChatbot), `sota_analyzer` (SotaAnalyzer), `messages` (list), `archivo_actual` (str), `file_hash` (str MD5), `md_text` (str). Initialized by `initialize_session_state()`; written by `file_uploader`; read by `audit_results`, `chatbot`, `sota_section`.
- **Source**: `extracted_frontend_01.md#3-Session-State`

**Inbound Edges (writes to session_state):**

| From Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `screen:file_uploader` | writes | resultado/md_text/file_hash/archivo_actual/messages | HIGH | extracted_frontend_01.md#5.1 |
| `service:session_state` | instantiates | PaperAuditor()/PaperChatbot()/SotaAnalyzer() initial values | HIGH | extracted_frontend_01.md#3 |

**Outbound Edges (reads from session_state):**

| To Node | Edge Type | Label | Severity | Evidence |
|---|---|---|---|---|
| `service:PaperAuditor` | reads | auditor key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |
| `service:PaperChatbot` | reads | chatbot key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |
| `service:SotaAnalyzer` | reads | sota_analyzer key | HIGH | cross_ref_resolution_cross_ref_root_to_frontend.md#g_027 |
| `screen:audit_results` | reads | resultado | MEDIUM | extracted_frontend_01.md#5.2 |
| `screen:chatbot` | reads | chatbot/messages | HIGH | extracted_frontend_01.md#5.3 |
| `screen:sota_section` | reads | sota_analyzer | HIGH | extracted_frontend_01.md#5.5 |
