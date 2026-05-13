# 05 — Test Scenario Specifications

This document defines the test scenarios, validation rules, and business logic assertions extracted from the codebase.

## 1. LLM Client Retry Logic

| Scenario | Trigger | Expected Behavior |
|---|---|---|
| **Transient Failure** | `LLMClient.generate()` receives a 503 or 429 error. | Retries with exponential backoff (2^attempt + jitter). |
| **Max Retries** | `LLMClient.generate()` fails 6 times (1 initial + 5 retries). | Raises the final exception to the caller. |
| **Success on Retry** | Succeeds on the 3rd attempt. | Returns the valid response; total call count = 3. |

## 2. Information Extraction Fragmentation

**Rule**: The `InformationExtractionSkill` must balance the paper text into fragments to avoid LLM context overflow.

| Test Case | Input | Assertion |
|---|---|---|
| **Multi-section Paper** | 6 equal-length Markdown sections. | Produces exactly 4 fragments (`total_chars / 4`). |
| **Flat Document** | Text without Markdown headers (`# `). | Falls back to `RecursiveCharacterTextSplitter` (chunk_size=25000). |
| **RAG Retrieval** | 13 hyperparameter queries. | Deduplicates chunks by cosine distance and takes top 10 unique results. |

## 3. RAG Logical Block Splitting

**Module**: `backend/skills/rag_extraction_skill.py`

| Rule ID | Rule Description | Assertion |
|---|---|---|
| **RULE-08** | Minimum chunk filter. | Chunks with stripped length ≤ 10 characters are discarded. |
| **BR-TEST-06** | Abstract location. | Abstract section must be preserved as a coherent block (usually index 1). |
| **BR-TEST-07** | Table integrity. | Table headers (`| Header |`) and data rows must remain in the same chunk. |

## 4. Audit Data Model Defaults

Verified via `tests/test_audit_state.py`.

| Field | Model | Default Value |
|---|---|---|
| `invalid_paper` | `AuditState` | `False` |
| `execution_time` | `AuditState` | `0.0` |
| `repository_url` | `ExtractedInfo.code` | `"NOT FOUND"` |
| `optimizer` | `ExtractedInfo.hyperparameters` | `"NOT FOUND"` |

## 5. Checklist Health Scoring (Business Rules)

**Module**: `frontend/utils/scoring.py`

| Scenario | Condition | Health Status |
|---|---|---|
| **Unjustified No** | `answer == "No"` AND `is_no_justified == False`. | `risk` |
| **Missing Evidence** | `answer == "Yes"` AND `evidence == ""` AND `justification == ""`. | `risk` |
| **Ethics Alert** | `key == "crowdsourcing_human_subjects"` AND `status == "risk"`. | Appends NeurIPS Code of Ethics warning. |
| **Clean Pass** | All items "Yes" with evidence OR "No" with justification OR "N/A". | `valid` |

## 6. Integration Smoke Tests

| Test Function | Target | Success Condition |
|---|---|---|
| `test_auditor_initialization` | `PaperAuditor()` | Constructor completes without exception; 6 skills instantiated. |
| `test_imports` | `frontend.components.*` | All frontend modules and their dependencies are importable. |
| `test_skills_integration` | `backend.skills.*` | All 15 exported skill classes are importable and inherit from `BaseSkill`. |
| `test_prompts_module` | `prompts.py` | `get_extraction_prompt` and `get_evaluation_prompt` return non-empty strings. |
