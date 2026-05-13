### Extraction statistics
Extraction statistics:
  Total extracted files: 4
  Total size: 301,317 bytes
  Average size: 75,329 bytes
  Total clusters in plan: 4


### Sample extractions
### extracted_backend_core_01.md (66,955 bytes)
# Extraction Report — Agent ext_backend_core_01
## Cluster: cluster_backend_core_01
## Scope: Core backend infrastructure (Python)

---

## 1. File Index

| # | File | Lines | Purpose |
|---|------|-------|---------|
| 1 | `backend/__init__.py` | 1 | Package docstring only: `"""Backend modular para el Auditor de Papers"""` |
| 2 | `backend/common/config.py` | 140 | Centralized configuration: API keys, model names, temperature constants, generation config dicts, Semantic Scholar settings |
| 3 | `backend/common/llm_client.py` | 77 | `LLMClient` class — Google Gemini wrapper with retry/backoff logic |
| 4 | `backend/common/prompts.py` | 540 | All LLM prompt templates: extraction, map, reduce, evaluation signals, evaluation, verification |
| 5 | `backend/common/__init__.py` | 1 | Package docstring only: `"""Componentes comunes compartidos"""` |
| 6 | `backend/services/auditor.py` | 205 | `PaperAuditor` class — 4-phase audit pipeline orchestrator |
| 7 | `backend/services/chatbot.py` | 62 | `PaperChatbot` class + `Chatbot` alias — skill-based Q&A chatbot over audited papers |
| 8 | `backend/services/pdf_parser.py` | 86 | `convert_pdf_to_markdown` function — Docling-based chunked PDF→Markdown converter |
| 9 | `backend/services/sota_analyzer.py` | 102 | `SotaAnalyzer` class — 5-step state-of-the-art analysis pipeline |
| 10 | `backend/services/__init__.py` | 1 | Package docstring only: `"""Servicios de lógica de negocio"""` |
| 11 | `backend/utils/logger.py` | 59 | `Colors`, `ColoredFormatter`, `get_logger` — centralized colored logging |
| 12 | `backend/utils/__init__.py` | 1 | Package docstring only: `"""Utilidades del backend"""` |

---

## 2. Constants, Enums, and Configuration Values (Category 5)

### 2.1 config.py — All Configuration Keys

SOURCE file: `backend/common/config.py`

**Environment variable suppression (module-level side effects, lines 8–25):**

| Operation | Value set | SOURCE |
|-----------|-----------|--------|
| `os.environ["TRANSFORMERS_VERBOSITY"]
...

### extracted_backend_skills_01.md (84,192 bytes)
# Extracted Specification — cluster_backend_skills_01
## Agent: ext_backend_skills_01

---

## 1. Skill Registry & Package Init (`__init__.py`)

### 1.1 Exported Symbols

`SOURCE: __init__.py:1`

The `__all__` list (lines 36-52) exports exactly 14 symbols:

| Symbol | Origin Module |
|---|---|
| `BaseSkill` | `backend.skills.base_skill` |
| `InformationExtractionSkill` | `backend.skills.auditor_skills` |
| `ReproducibilityEvaluationSkill` | `backend.skills.auditor_skills` |
| `MetricsCalculationSkill` | `backend.skills.auditor_skills` |
| `MetadataAggregationSkill` | `backend.skills.auditor_skills` |
| `ConversationalResponseSkill` | `backend.skills.chatbot_skills` |
| `ContextValidationSkill` | `backend.skills.chatbot_skills` |
| `ThematicCoverageSkill` | `backend.skills.sota_skills` |
| `QueryGenerationSkill` | `backend.skills.sota_skills` |
| `SemanticScholarSearchSkill` | `backend.skills.sota_skills` |
| `CoverageGapAnalysisSkill` | `backend.skills.sota_skills` |
| `CrossValidationSkill` | `backend.skills.sota_skills` |
| `LimitationsQualityDetectionSkill` | `backend.skills.regex_detection_skills` |
| `SoftwareVersionDetectionSkill` | `backend.skills.regex_detection_skills` |
| `HardwareDetailDetectionSkill` | `backend.skills.regex_detection_skills` |

**NOTE — NOT exported but defined in the package:**
- `ChecklistVerificationSkill` (defined in `auditor_skills.py:319`) — absent from `__init__.py`
- `HybridHyperparameterExtractionSkill` (defined in `rag_extraction_skill.py:27`) — absent from `__init__.py`
- All other regex detection skills in `regex_detection_skills.py` (`HyperparameterDetectionSkill`, `DataAvailabilityDetectionSkill`, `CodeAvailabilityDetectionSkill`, `StatisticsDetectionSkill`, `EnvironmentalImpactDetectionSkill`, `ProblematicPhrasesDetectionSkill`, `LlmUsageDetectionSkill`, `CrowdsourcingDetectionSkill`, `LicenseDetectionSkill`) — absent from `__init__.py`

### 1.2 Skill Registration Logic

DETAIL: None — `__init__.py` performs only re-export
...

### extracted_frontend_01.md (59,211 bytes)
# Extracted Specification: cluster_frontend_01
## Agent: ext_frontend_01

---

## 1. File Index

| # | File | Line Count | Role |
|---|------|-----------|------|
| 1 | `frontend/__init__.py` | 1 | Package marker; single docstring: "Frontend modular para el Auditor de Papers" |
| 2 | `frontend/app.py` | 77 | Main Streamlit application entry point; orchestrates page config, styles, session state, upload, audit, results, chatbot, download |
| 3 | `frontend/config.py` | 5 | Application-level constants: TITLE, SIDEBAR_IMAGE URL, SIDEBAR_DESCRIPTION |
| 4 | `frontend/components/audit_results.py` | 317 | Renders the full audit results page (verdict, metrics, RAG ficha, compliance table, expanders); also generates the downloadable Markdown report |
| 5 | `frontend/components/chatbot.py` | 29 | Renders the interactive chat section; reads/writes `st.session_state.messages`; calls `st.session_state.chatbot.preguntar()` |
| 6 | `frontend/components/file_uploader.py` | 101 | Handles file upload (PDF/TXT/MD), MD extraction, and invocation of the backend auditor; manages `st.session_state` caching by file hash |
| 7 | `frontend/components/gauge_chart.py` | 71 | Pure function `create_gauge_chart(score)`: returns a Plotly Figure (gauge indicator) based on NeurIPS quality tiers |
| 8 | `frontend/components/sota_section.py` | 109 | Renders SOTA analysis section; triggers `st.session_state.sota_analyzer.analyze_sota()`; renders missing-papers dataframe |
| 9 | `frontend/components/__init__.py` | 1 | Package marker; single docstring: "Componentes visuales de la aplicación" |
| 10 | `frontend/styles/custom_css.py` | 87 | Defines CUSTOM_CSS string constant; `apply_custom_styles()` injects CSS via `st.markdown` |
| 11 | `frontend/styles/__init__.py` | 1 | Package marker; single docstring: "Estilos CSS para la aplicación" |
| 12 | `frontend/utils/scoring.py` | 130 | Defines CHECKLIST_KEYS list (16 items), CHECKLIST_LABELS dict, and `get_checklist_health()` function |
| 13 | `frontend/utils/
...

### extracted_root_tests_scratch_01.md (90,959 bytes)
# Extraction Report: cluster_root_tests_scratch_01
## Agent: ext_root_tests_scratch_01

---

## 1. File Index

| # | File | Lines | Purpose |
|---|------|-------|---------|
| 1 | `.gitignore` | 42 | Git ignore rules: excludes pycache, venvs, IDEs, `.env`, PDFs, logs, `*.md`, `*.txt` |
| 2 | `app.py` | 89 | Main Streamlit application entry point: configures page, handles file upload, renders audit results |
| 3 | `create_test_pdf.py` | 184 | CLI script to generate a test PDF paper with known errors using reportlab |
| 4 | `list_models.py` | 18 | CLI script to list available Google GenAI embedding models via API |
| 5 | `md_to_pdf.py` | 325 | CLI tool to convert Markdown/TXT files or folders to PDF using reportlab |
| 6 | `pdf_to_md.py` | 159 | CLI tool to convert PDF files or folders to Markdown using pymupdf4llm |
| 7 | `requirements.txt` | 5 | Python dependency list (no pinned versions) |
| 8 | `test_auditor_refactor.py` | 101 | Integration smoke-test verifying auditor refactoring correctness |
| 9 | `test_imports.py` | 47 | Import smoke-test verifying all frontend modules are importable |
| 10 | `test_skills_integration.py` | 164 | Integration test verifying skills architecture and service initialization |
| 11 | `backend/scratch/test_embed.py` | 26 | Scratch script testing Google GenAI `embed_content` API response structure |
| 12 | `backend/scratch/test_embed2.py` | 23 | Scratch script testing Google GenAI `embed_content` API with error handling |
| 13 | `scratch/check_st.py` | 7 | Scratch script checking for `st.html` and `st.iframe` Streamlit attribute existence |
| 14 | `scratch/patch_skills.py` | 109 | One-time script that rewrites `CrowdsourcingDetectionSkill` and `LicenseDetectionSkill` classes in `backend/skills/regex_detection_skills.py` via AST-validated string replacement |
| 15 | `scratch/repro_hyperparams.py` | 33 | Scratch script reproducing hyperparameter detection on a real paper file |
| 16 | `scratch/test_checklist_health.py` | 37 | Scratch scri
...


### Extraction plan
{
  "project_name": "llm-paper-auditor-multimodels",
  "source_type": "python_web_app",
  "clusters": [
    {
      "id": "cluster_backend_core_01",
      "description": "Backend common infrastructure: configuration, LLM client, prompts, core services (auditor, chatbot, PDF parser, SOTA analyzer), and utilities",
      "files": [
        "TFG.-llm-paper-auditor-multimodels/backend/__init__.py",
        "TFG.-llm-paper-auditor-multimodels/backend/common/config.py",
        "TFG.-llm-paper-auditor-multimodels/backend/common/llm_client.py",
        "TFG.-llm-paper-auditor-multimodels/backend/common/prompts.py",
        "TFG.-llm-paper-auditor-multimodels/backend/common/__init__.py",
        "TFG.-llm-paper-auditor-multimodels/backend/services/auditor.py",
        "TFG.-llm-paper-auditor-multimodels/backend/services/chatbot.py",
        "TFG.-llm-paper-auditor-multimodels/backend/services/pdf_parser.py",
        "TFG.-llm-paper-auditor-multimodels/backend/services/sota_analyzer.py",
        "TFG.-llm-paper-auditor-multimodels/backend/services/__init__.py",
        "TFG.-llm-paper-auditor-multimodels/backend/utils/logger.py",
        "TFG.-llm-paper-auditor-multimodels/backend/utils/__init__.py"
      ],
      "file_count": 12,
      "estimated_loc": 1071,
      "tech": [
        "python"
      ],
      "categories_covered": [
        5,
        8,
        10,
        11,
        12
      ],
      "scope": "Core backend infrastructure: LLM client abstraction, configuration management, prompt templates, auditor service logic, chatbot service, PDF parsing service, SOTA analysis service, and logging utilities"
    },
    {
      "id": "cluster_backend_skills_01",
      "description": "Backend skill modules: auditor skills, base skill abstraction, chatbot skills, RAG extraction skill, regex detection skills, SOTA skills, and skills package init",
      "files": [
        "TFG.-llm-paper-auditor-multimodels/backend/skills/auditor_skills.py",
        "TFG.-llm-paper-auditor-multimodels/backend/skills/base_skill.py",
        "TFG.-llm-paper-auditor-multimodels/backend/skills/chatbot_skills.py",
        "TFG.-llm-paper-auditor-multimodels/backend/skills/rag_extraction_skill.py",
        "TFG.-llm-paper-auditor-multimodels/backend/skills/regex_detection_skills.py",
        "TFG.-llm-paper-auditor-multimodels/backend/skills/sota_skills.py",
        "TFG.-llm-paper-auditor-multimodels/backend/skills/__init__.py"
      ],
      "file_count": 7,
      "estimated_loc": 1704,
      "tech": [
        "python"
      ],
      "categories_covered": [
        5,
        8,
        10,
        11,
        12
      ],
      "scope": "Skill plugin system: base skill interface, auditor evaluation skills, RAG extraction logic, regex-based detection patterns, SOTA comparison skills, chatbot interaction skills, and skill registry"
    },
    {
      "id": "cluster_frontend_01",
      "description": "Frontend Streamlit application: app entry point, configuration, UI components (audit results, chatbot, file uploader, gauge chart, SOTA section), styles, and frontend utilities",
      "files": [
        "TFG.-llm-paper-auditor-multimodels/frontend/__init__.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/app.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/config.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/components/audit_results.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/components/chatbot.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/components/file_uploader.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/components/gauge_chart.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/components/sota_section.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/components/__init__.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/styles/custom_css.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/styles/__init__.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/utils/scoring.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/utils/session_state.py",
        "TFG.-llm-paper-auditor-multimodels/frontend/utils/__init__.py"
      ],
      "file_count": 14,
      "estimated_loc": 810,
      "tech": [
        "python",
        "streamlit"
      ],
      "categories_covered": [
        2,
        3,
        4,
        5,
        10,
        11
      ],
      "scope": "Streamlit-based UI: page layout and navigation, file upload flow, audit results display, chatbot interface, gauge chart visualisation, SOTA section, custom CSS styling, scoring logic, and session state management"
    },
    {
      "id": "cluster_root_tests_scratch_01",
      "description": "Root-level scripts (app entry, PDF tools, model listing), test suites (root + tests/ + backend/scratch + scratch/), and configuration files",
      "files": [
        "TFG.-llm-paper-auditor-multimodels/.gitignore",
        "TFG.-llm-paper-auditor-multimodels/app.py",
        "TFG.-llm-paper-auditor-multimodels/create_test_pdf.py",
        "TFG.-llm-paper-auditor-multimodels/list_models.py",
        "TFG.-llm-paper-auditor-multimodels/md_to_pdf.py",
        "TFG.-llm-paper-auditor-multimodels/pdf_to_md.py",
        "TFG.-llm-paper-auditor-multimodels/requirements.txt",
        "TFG.-llm-paper-auditor-multimodels/test_auditor_refactor.py",
        "TFG.-llm-paper-auditor-multimodels/test_imports.py",
        "TFG.-llm-paper-auditor-multimodels/test_skills_integration.py",
        "TFG.-llm-paper-auditor-multimodels/backend/scratch/test_embed.py",
        "TFG.-llm-paper-auditor-multimodels/backend/scratch/test_embed2.py",
        "TFG.-llm-paper-auditor-multimodels/scratch/check_st.py",
        "TFG.-llm-paper-auditor-multimodels/scratch/patch_skills.py",
        "TFG.-llm-paper-auditor-multimodels/scratch/repro_hyperparams.py",
        "TFG.-llm-paper-auditor-multimodels/scratch/test_checklist_health.py",
        "TFG.-llm-paper-auditor-multimodels/scratch/test_llm_retry.py",
        "TFG.-llm-paper-auditor-multimodels/scratch/test_rag_split.py",
        "TFG.-llm-paper-auditor-multimodels/tests/test_audit_state.py",
        "TFG.-llm-paper-auditor-multimodels/tests/test_rag_logical_splitter.py",
        "TFG.-llm-paper-auditor-multimodels/tests/test_section_splitter.py"
      ],
      "file_count": 21,
      "estimated_loc": 1342,
      "tech": [
        "python"
      ],
      "categories_covered": [
        5,
        8,
        9,
        10,
        12
      ],
      "scope": "Application entry point, PDF conversion utilities (md\u2192pdf, pdf\u2192md), model listing CLI, dependency configuration (requirements.txt), integration and unit test suites covering auditor refactoring, skill integration, RAG splitting, section splitting, and embedding experiments"
    }
  ],
  "extraction_agents": [
    {
      "id": "ext_backend_core_01",
      "cluster": "cluster_backend_core_01",
      "engine": "cli",
      "parallel_group": 0,
      "skills": [
        "re-generic"
      ],
      "output_file": "extracted_backend_core_01.md",
      "synthesis_categories": [
        "business_rules",
        "technical"
      ],
      "depends_on": [],
      "categories": [
        5,
        8,
        10,
        11,
        12
      ],
      "estimated_loc": 1071
    },
    {
      "id": "ext_backend_skills_01",
      "cluster": "cluster_backend_skills_01",
      "engine": "cli",
      "parallel_group": 0,
      "skills": [
        "re-generic"
      ],
      "output_file": "extracted_backend_skills_01.md",
      "synthesis_categories": [
        "business_rules",
        "technical"
      ],
      "depends_on": [],
      "categories": [
        5,
        8,
        10,
        11,
        12
      ],
      "estimated_loc": 1704
    },
    {
      "id": "ext_frontend_01",
      "cluster": "cluster_frontend_01",
      "engine": "cli",
      "parallel_group": 0,
      "skills": [
        "re-generic"
      ],
      "output_file": "extracted_frontend_01.md",
      "synthesis_categories": [
        "user_flows_ui",
        "lookfeel_ui",
        "business_rules"
      ],
      "depends_on": [],
      "categories": [
        2,
        3,
        4,
        5,
        10,
        11
      ],
      "estimated_loc": 810
    },
    {
      "id": "ext_root_tests_scratch_01",
      "cluster": "cluster_root_tests_scratch_01",
      "engine": "cli",
      "parallel_group": 0,
      "skills": [
        "re-generic"
      ],
      "output_file": "extracted_root_tests_scratch_01.md",
      "synthesis_categories": [
        "business_rules",
        "technical",
        "test_scenarios"
      ],
      "depends_on": [],
      "categories": [
        5,
        8,
        9,
        10,
        12
      ],
      "estimated_loc": 1342
    }
  ],
  "parallel_config": {
    "max_concurrent": 4,
    "groups": [
      {
        "group": 0,
        "agents": [
          "ext_backend_core_01",
          "ext_backend_skills_01",
          "ext_frontend_01",
          "ext_root_tests_scratch_01"
        ]
      }
    ]
  },
  "category_coverage": {
    "1_data_entities": "N/A: No relational database or ORM models found; the codebase is a Python LLM application that processes PDF documents without a persistent data store",
    "2_screens_ui": [
      "ext_frontend_01"
    ],
    "3_navigation": [
      "ext_frontend_01"
    ],
    "4_user_flows": [
      "ext_frontend_01"
    ],
    "5_business_rules": [
      "ext_backend_core_01",
      "ext_backend_skills_01",
      "ext_frontend_01",
      "ext_root_tests_scratch_01"
    ],
    "6_rbac_security": "N/A: No authentication, authorization or RBAC mechanism found; the application is a local/single-user Streamlit tool with no login system",
    "7_reports": [
      "ext_frontend_01"
    ],
    "8_integrations": [
      "ext_backend_core_01",
      "ext_backend_skills_01",
      "ext_root_tests_scratch_01"
    ],
    "9_batch_jobs": [
      "ext_root_tests_scratch_01"
    ],
    "10_configurations": [
      "ext_backend_core_01",
      "ext_root_tests_scratch_01"
    ],
    "11_transformations": [
      "ext_backend_core_01",
      "ext_backend_skills_01"
    ],
    "12_error_handling": [
      "ext_backend_core_01",
      "ext_backend_skills_01",
      "ext_root_tests_scratch_01"
    ]
  }
}

### Codebase inventory
{
  "summary": {
    "total_files": 54,
    "total_loc": 4927,
    "total_size_bytes": 256409,
    "project_types": [],
    "tech_distribution": {
      "unknown": 54
    },
    "group_distribution": {
      "other": 54
    },
    "directory_count": 13
  }
}