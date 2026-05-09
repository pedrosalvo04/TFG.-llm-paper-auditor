import re

spec_path = "/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/02_functional_backend.md"

with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

original = content  # keep for verification

# =========================================================
# F01 — §3.4 Guard Conditions return shape
# SOURCE: rag_extraction_skill.py:31-32
# =========================================================
old = (
    "RULE: guard_hyperparameter_extraction  \n"
    "TRIGGER: `execute()` is called  \n"
    "CONDITION: `context.get(\"paper_text\")` is falsy (empty string or absent)  \n"
    "ACTION: Return `{\"success\": False, \"error\": \"No paper text in context\", \"phase\": \"hyperparameter_extraction\"}`  \n"
    "ERROR: Non-critical; `PaperAuditor.audit()` catches this and continues pipeline"
)
new = (
    "RULE: guard_hyperparameter_extraction  \n"
    "TRIGGER: `execute()` is called  \n"
    "CONDITION: `context.get(\"paper_text\")` is falsy (empty string or absent); checked via `self.validate_context(context, ['paper_text'])`  \n"
    "ACTION: Return `{'extracted_hyperparameters_hybrid': {}}`  \n"
    "ERROR: Non-critical; `PaperAuditor.audit()` catches this and continues pipeline  \n"
    "SOURCE: `rag_extraction_skill.py:31-32`"
)
assert old in content, "F01: old text not found"
content = content.replace(old, new, 1)
print("F01 applied")

# =========================================================
# F02 — §3.5 Step 1 chunking algorithm
# SOURCE: rag_extraction_skill.py:43-47
# =========================================================
old = (
    "```pseudocode\n"
    "FUNCTION chunk_text(paper_text, chunk_size=1000, overlap=200):\n"
    "    chunks = []\n"
    "    start = 0\n"
    "    WHILE start < len(paper_text):\n"
    "        end = min(start + chunk_size, len(paper_text))\n"
    "        chunks.append(paper_text[start:end])\n"
    "        start += chunk_size - overlap\n"
    "    RETURN chunks\n"
    "```"
)
new = (
    "```pseudocode\n"
    "# Normalize line endings\n"
    "paper_text_norm = paper_text.replace('\\r\\n', '\\n')\n"
    "\n"
    "# Split on two or more consecutive newlines (Docling paragraph/block separator)\n"
    "raw_chunks = re.split(r'\\n\\n+', paper_text_norm)\n"
    "\n"
    "# Strip whitespace; discard blocks of 10 characters or fewer (noise filter)\n"
    "chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]\n"
    "```\n"
    "\n"
    "SOURCE: `rag_extraction_skill.py:43-47`"
)
assert old in content, "F02: old text not found"
content = content.replace(old, new, 1)
print("F02 applied")

# =========================================================
# F03 — §3.5 Step 3 ChromaDB collection name + delete-before-create
# SOURCE: rag_extraction_skill.py:85-97
# =========================================================
old = (
    "```pseudocode\n"
    "client = chromadb.Client()   # in-memory (no persistence)\n"
    "collection = client.create_collection(\"hyperparams\")\n"
    "collection.add(\n"
    "    documents=chunks,\n"
    "    embeddings=embeddings,\n"
    "    ids=[f\"chunk_{i}\" for i in range(len(chunks))]\n"
    ")\n"
    "```"
)
new = (
    "```pseudocode\n"
    "chroma_client = chromadb.Client()   # in-memory (no persistence)\n"
    "\n"
    "# Delete stale collection from any previous run (silently ignore if absent)\n"
    "try:\n"
    "    chroma_client.delete_collection(\"paper_chunks\")\n"
    "except:\n"
    "    pass\n"
    "\n"
    "collection = chroma_client.create_collection(name=\"paper_chunks\")\n"
    "collection.add(\n"
    "    embeddings=embeddings,\n"
    "    documents=chunks,\n"
    "    ids=[str(i) for i in range(len(chunks))]\n"
    ")\n"
    "```\n"
    "\n"
    "SOURCE: `rag_extraction_skill.py:85-97`"
)
assert old in content, "F03: old text not found"
content = content.replace(old, new, 1)
print("F03 applied")

# =========================================================
# F04 + F05 — §3.5 Step 4 query strings + query call parameters
# SOURCE: rag_extraction_skill.py:99-113 (strings), 115-124 (query call)
# =========================================================
old = (
    "The 13 fixed queries are:\n"
    "\n"
    "1. `\"learning rate optimizer training configuration\"`\n"
    "2. `\"batch size training epochs iterations\"`\n"
    "3. `\"model architecture layers parameters\"`\n"
    "4. `\"regularization dropout weight decay\"`\n"
    "5. `\"dataset size training test split\"`\n"
    "6. `\"hardware GPU TPU computational resources\"`\n"
    "7. `\"software framework library version\"`\n"
    "8. `\"hyperparameter search tuning optimization\"`\n"
    "9. `\"loss function objective metric evaluation\"`\n"
    "10. `\"preprocessing normalization augmentation\"`\n"
    "11. `\"random seed initialization reproducibility\"`\n"
    "12. `\"inference deployment serving configuration\"`\n"
    "13. `\"ablation study baseline comparison\"`\n"
    "\n"
    "Source: `extracted_backend_skills_01.md §4 (fixed query list)`\n"
    "\n"
    "For each query:\n"
    "\n"
    "```pseudocode\n"
    "results = collection.query(\n"
    "    query_texts=[query],\n"
    "    n_results=3\n"
    ")\n"
    "```"
)
new = (
    "The 13 fixed queries are (SOURCE: `rag_extraction_skill.py:99-113`):\n"
    "\n"
    "1. `\"training details optimization hyperparameters\"`\n"
    "2. `\"learning rate schedule step size warmup decay learning rate\"`\n"
    "3. `\"batch size mini-batch micro-batch optimization global batch size\"`\n"
    "4. `\"epochs training steps iterations convergence training duration\"`\n"
    "5. `\"optimizer Adam SGD AdamW RMSprop momentum betas optimizer settings\"`\n"
    "6. `\"weight decay L2 regularization weight decay\"`\n"
    "7. `\"random seed reproducibility seed fixed seed initialization\"`\n"
    "8. `\"hardware GPU TPU NVIDIA AMD cluster infrastructure hardware setup\"`\n"
    "9. `\"hyperparameters configuration settings parameters appendix details\"`\n"
    "10. `\"experimental setup implementation details training configuration\"`\n"
    "11. `\"SFT Supervised Fine-tuning instruction tuning training schedule\"`\n"
    "12. `\"pre-training pretraining phase training protocols\"`\n"
    "13. `\"hyperparameter tuning iterations schedule iterations iterations\"`\n"
    "\n"
    "All 13 query embeddings are generated **in one batched call** using\n"
    "`self.llm_client.client.models.embed_content(model=EMBEDDING_MODEL_NAME, contents=queries)`,\n"
    "then queried against ChromaDB as a single batch (SOURCE: `rag_extraction_skill.py:115-124`):\n"
    "\n"
    "```pseudocode\n"
    "# Generate embeddings for all 13 queries at once\n"
    "q_emb_res = llm_client.client.models.embed_content(\n"
    "    model=EMBEDDING_MODEL_NAME,\n"
    "    contents=queries          # list of 13 strings\n"
    ")\n"
    "query_embeddings = [e.values for e in q_emb_res.embeddings]\n"
    "\n"
    "# Single batched query — not one-at-a-time\n"
    "results = collection.query(\n"
    "    query_embeddings=query_embeddings,   # NOT query_texts\n"
    "    n_results=10                          # NOT 3\n"
    ")\n"
    "```"
)
assert old in content, "F04+F05: old text not found"
content = content.replace(old, new, 1)
print("F04+F05 applied")

# =========================================================
# F06 — §3.5 Step 5 relevance scoring formula
# SOURCE: rag_extraction_skill.py:152-157
# =========================================================
old = (
    "```pseudocode\n"
    "FUNCTION score_relevance(distance: float) -> float:\n"
    "    # ChromaDB distance: 0.0 = identical, 2.0 = completely dissimilar\n"
    "    IF distance <= 0.3:\n"
    "        RETURN 1.0\n"
    "    ELIF distance <= 0.7:\n"
    "        RETURN 1.0 - (distance - 0.3) / (0.7 - 0.3) * 0.5   # 1.0 → 0.5\n"
    "    ELIF distance <= 1.2:\n"
    "        RETURN 0.5 - (distance - 0.7) / (1.2 - 0.7) * 0.4   # 0.5 → 0.1\n"
    "    ELSE:\n"
    "        RETURN 0.0\n"
    "```\n"
    "\n"
    "Source: `extracted_backend_skills_01.md §4 (relevance scoring formula)`\n"
    "\n"
    "Only chunks with relevance score > 0.0 are included in the LLM context."
)
new = (
    "```pseudocode\n"
    "FUNCTION score_relevance(distance: float) -> int:\n"
    "    # Returns integer 0–100; lower ChromaDB distance = higher relevance\n"
    "    # Recalibrated scale: distance < 0.4 excellent (85%+), distance > 0.7 noise (<31%)\n"
    "    IF distance < 0.4:\n"
    "        RETURN int(95 - distance * 25)              # 0.0 → 95, 0.4 → 85\n"
    "    ELIF distance < 0.7:\n"
    "        RETURN int(85 - (distance - 0.4) * 180)    # 0.4 → 85, 0.7 → 31\n"
    "    ELSE:\n"
    "        RETURN max(5, int(31 - (distance - 0.7) * 50))  # > 0.7: slow decay, floor 5\n"
    "```\n"
    "\n"
    "SOURCE: `rag_extraction_skill.py:152-157`\n"
    "\n"
    "Only chunks with relevance_score > 0 (integer) are included in the LLM context.\n"
    "In practice the floor is 5 for any distance ≥ 0.7, so chunks are always included\n"
    "unless entirely filtered by the `chunk_relevance` min-distance deduplication step."
)
assert old in content, "F06: old text not found"
content = content.replace(old, new, 1)
print("F06 applied")

# =========================================================
# F07 — §3.5 Step 7 merge strategy (LLM REDUCE, not last-write-wins)
# SOURCE: rag_extraction_skill.py:204-261
# =========================================================
old = (
    "#### Step 7: Merge results\n"
    "\n"
    "All per-chunk extraction results are merged into a single `hyperparameter_results` dict.\n"
    "Merge strategy: later chunks overwrite earlier chunks for the same key (last-write-wins).\n"
    "[GAP: exact merge deduplication strategy for hyperparameter_results is not fully specified in extraction]"
)
new = (
    "#### Step 7: REDUCE phase — LLM consolidation\n"
    "\n"
    "After all MAP extractions are collected into `extracted_fragments`, a dedicated LLM REDUCE\n"
    "call consolidates all fragments into a single canonical result (SOURCE: `rag_extraction_skill.py:204-261`).\n"
    "There is **no** deterministic last-write-wins merge; the LLM decides.\n"
    "\n"
    "The REDUCE prompt instructs the model to:\n"
    "- Resolve conflicts between fragments; prefer SFT/fine-tuning values over pre-training\n"
    "  where the distinction is obvious, otherwise pick the most representative value.\n"
    "- Ignore `\"NOT FOUND\"` values from one fragment if another fragment found a valid value.\n"
    "- Use `thought_process` from each fragment to build a final synthesis.\n"
    "- Differentiate between table types when multiple fragments cite different table headers\n"
    "  (e.g., distinguish a 'Model Architecture' table from a 'Training Hyperparameters' table).\n"
    "- Never guess or hallucinate.\n"
    "\n"
    "The raw REDUCE response is JSON-parsed using Balanced JSON Extraction (§2.8).\n"
    "On JSON parse failure, trailing-comma repair via `re.sub(r',\\s*([\\]}])', r'\\1', ...)` is attempted.\n"
    "The parsed dict is then cleaned by `_clean_with_regex()` which normalises scientific notation,\n"
    "extracts first integers, and maps empty/N/A values to `'NOT FOUND'`."
)
assert old in content, "F07: old text not found"
content = content.replace(old, new, 1)
print("F07 applied")

# =========================================================
# F08a — §3.6 Output Context Keys
# SOURCE: rag_extraction_skill.py:268-271
# =========================================================
old = (
    "### 3.6 Output Context Keys\n"
    "\n"
    "| Key | Type | Description |\n"
    "|---|---|---|\n"
    "| `hyperparameter_results` | dict | Merged hyperparameter extraction from all relevant chunks |"
)
new = (
    "### 3.6 Output Context Keys\n"
    "\n"
    "SOURCE: `rag_extraction_skill.py:268-271`\n"
    "\n"
    "| Key | Type | Description |\n"
    "|---|---|---|\n"
    "| `extracted_hyperparameters_hybrid` | dict | Consolidated hyperparameter data from REDUCE phase, cleaned by `_clean_with_regex()` |\n"
    "| `triage_fragments` | list[dict] | Per-chunk MAP extraction results for frontend visualization; each element includes `_relevance_score` (int) and `_chunk_text` (str) |"
)
assert old in content, "F08a: old text not found"
content = content.replace(old, new, 1)
print("F08a applied")

# =========================================================
# F08b — §3.7 Error Return Shape
# SOURCE: rag_extraction_skill.py:31-32, 268-271, 274-275
# =========================================================
old = (
    "### 3.7 Error Return Shape\n"
    "\n"
    "**Success:**\n"
    "\n"
    "```python\n"
    "{\"success\": True, \"hyperparameter_results\": dict}\n"
    "```\n"
    "\n"
    "**Failure (non-critical — pipeline continues):**\n"
    "\n"
    "```python\n"
    "{\"success\": False, \"error\": str, \"phase\": \"hyperparameter_extraction\"}\n"
    "```"
)
new = (
    "### 3.7 Return Shapes\n"
    "\n"
    "SOURCE: `rag_extraction_skill.py:31-32, 268-271, 274-275`\n"
    "\n"
    "**Early exit (guard — `paper_text` absent):**\n"
    "\n"
    "```python\n"
    "{'extracted_hyperparameters_hybrid': {}}\n"
    "```\n"
    "\n"
    "**Success (full pipeline completes):**\n"
    "\n"
    "```python\n"
    "{\n"
    "    'extracted_hyperparameters_hybrid': dict,   # cleaned REDUCE output\n"
    "    'triage_fragments': list[dict]               # per-chunk MAP results\n"
    "}\n"
    "```\n"
    "\n"
    "**Failure (outer exception caught — non-critical, pipeline continues):**\n"
    "\n"
    "```python\n"
    "{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str}\n"
    "```\n"
    "\n"
    "Note: there is **no** `success` key in any return shape. Callers must check for the\n"
    "presence and non-emptiness of `extracted_hyperparameters_hybrid`."
)
assert old in content, "F08b: old text not found"
content = content.replace(old, new, 1)
print("F08b applied")

# =========================================================
# F08c — §1.1 Phase table Phase 1.5 output key
# SOURCE: rag_extraction_skill.py:268-271
# =========================================================
old = (
    "| 1.5 | `hyperparameter_extraction` | `HybridHyperparameterExtractionSkill` | Always runs after Phase 1 | `paper_text` (str), `extracted_info` (dict) | `hyperparameter_results` (dict) | Non-critical: on failure, pipeline continues (context key may be absent or partial); logs error | Builds and destroys in-memory ChromaDB collection; sleeps 1s between chunks; sleeps 15s between embedding batches |"
)
new = (
    "| 1.5 | `hyperparameter_extraction` | `HybridHyperparameterExtractionSkill` | Always runs after Phase 1 | `paper_text` (str) | `extracted_hyperparameters_hybrid` (dict), `triage_fragments` (list[dict]) | Non-critical: on failure, pipeline continues (context key may be absent or partial); no `success` key returned | Builds and destroys in-memory ChromaDB collection; sleeps 1s between MAP LLM calls; sleeps 15s between embedding batches |"
)
assert old in content, "F08c: old text not found"
content = content.replace(old, new, 1)
print("F08c applied")

# =========================================================
# F08d — §1.2 Context Keys Table row for hyperparameter_results
# SOURCE: rag_extraction_skill.py:268-271
# =========================================================
old = "| `hyperparameter_results` | dict | Phase 1.5 |"
new = "| `extracted_hyperparameters_hybrid` | dict | Phase 1.5 |"
assert old in content, "F08d: old text not found"
content = content.replace(old, new, 1)
print("F08d applied")

# =========================================================
# F09 — §11 SS Auth description
# SOURCE: sota_skills.py:182-185
# =========================================================
old = (
    "**Auth**: None (public API, unauthenticated)  \n"
    "**Rate limiting**: No explicit rate limit handling in skill; relies on HTTP 429 retry in LLMClient  \n"
    "[GAP: whether API key is optionally injected via config is not confirmed in extraction]"
)
new = (
    "**Auth**: Optional API key injection (SOURCE: `sota_skills.py:182-185`).  \n"
    "If `SEMANTIC_SCHOLAR_API_KEY` is set (non-falsy), the header `x-api-key` is added to every request;\n"
    "otherwise requests are sent without authentication (public endpoint).  \n"
    "**Rate limiting**: Explicit in-skill handling independent of LLMClient (SOURCE: `sota_skills.py:190-191, 215-217`):  \n"
    "- `time.sleep(0.5)` is inserted **before** every query except the first (between-query throttle).  \n"
    "- On HTTP 429 response: `time.sleep(2)` then log warning and continue to next query."
)
assert old in content, "F09+F10: old text not found"
content = content.replace(old, new, 1)
print("F09+F10 applied")

# =========================================================
# F11 — §11 SS Output Context Keys — add top-10 sort note
# SOURCE: sota_skills.py:227-232
# =========================================================
old = (
    "#### Output Context Keys\n"
    "\n"
    "| Key | Type | Description |\n"
    "|---|---|---|\n"
    "| `sota_papers` | list[dict] | All unique papers found across all queries (deduplicated by `paperId`) |\n"
    "| `query_results` | dict | Mapping of `query_string → list[paper_dict]` (raw per-query results) |"
)
new = (
    "#### Post-processing: deduplication and top-N selection\n"
    "\n"
    "After all queries are complete, results are processed as follows (SOURCE: `sota_skills.py:227-232`):\n"
    "\n"
    "```pseudocode\n"
    "# Deduplicate by paperId (last occurrence wins for duplicates)\n"
    "unique_papers = {p['paperId']: p for p in sota_papers if p.get('paperId')}.values()\n"
    "\n"
    "# Sort by citationCount descending; cap at 10 results\n"
    "sorted_papers = sorted(unique_papers, key=lambda x: x.get('citationCount', 0), reverse=True)[:10]\n"
    "```\n"
    "\n"
    "The final `sota_papers` list contains **at most 10 papers**, ordered by citation count descending.\n"
    "\n"
    "#### Output Context Keys\n"
    "\n"
    "| Key | Type | Description |\n"
    "|---|---|---|\n"
    "| `sota_papers` | list[dict] | Unique papers across all queries, deduplicated by `paperId`, sorted by `citationCount` descending, capped at 10 |\n"
    "| `query_results` | dict | Mapping of `query_string → list[paper_dict]` (raw per-query results) |"
)
assert old in content, "F11: old text not found"
content = content.replace(old, new, 1)
print("F11 applied")

# =========================================================
# F12 — §11 CrossValidationSkill Input Context Keys
# SOURCE: sota_skills.py:319
# =========================================================
old = (
    "#### Input Context Keys\n"
    "\n"
    "| Key | Type | Required | Description |\n"
    "|---|---|---|---|\n"
    "| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill |\n"
    "| `checklist` | dict | Yes | Phase 2/2.5 output |\n"
    "| `extracted_info` | dict | Yes | Phase 1 output |\n"
    "\n"
    "#### Guard Conditions\n"
    "\n"
    "RULE: guard_cross_validation  \n"
    "CONDITION: `context.get(\"sota_papers\")` is falsy or `context.get(\"checklist\")` is falsy  \n"
    "ACTION: Return `{\"success\": False, \"error\": \"Missing sota_papers or checklist\", \"phase\": \"cross_validation\"}`"
)
new = (
    "#### Input Context Keys\n"
    "\n"
    "SOURCE: `sota_skills.py:319`\n"
    "\n"
    "| Key | Type | Required | Description |\n"
    "|---|---|---|---|\n"
    "| `paper_text` | str | Yes | Full paper text |\n"
    "| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill |\n"
    "| `thematic_data` | dict | Yes | Thematic analysis dict (contains `subtemas`, `areas_tecnicas`, `año_paper`) |\n"
    "\n"
    "Note: `checklist` and `extracted_info` are **not** required inputs; `paper_text` and\n"
    "`thematic_data` are required but were absent from the previous version of this spec.\n"
    "\n"
    "#### Guard Conditions\n"
    "\n"
    "SOURCE: `sota_skills.py:319-331`\n"
    "\n"
    "RULE: guard_cross_validation  \n"
    "CONDITION: any of `paper_text`, `sota_papers`, `thematic_data` is falsy; checked via\n"
    "`self.validate_context(context, ['paper_text', 'sota_papers', 'thematic_data'])`  \n"
    "ACTION: Return `{'validation_results': {}}`\n"
    "\n"
    "Additional guard: if `sota_papers` is an empty list, return immediately with a default result:\n"
    "\n"
    "```python\n"
    "{'validation_results': {\n"
    "    'papers_omitidos': [],\n"
    "    'cobertura_tematica': {'areas_debiles': []},\n"
    "    'conclusion_sota': 'No se encontraron artículos recientes (2023-2026) en Semantic Scholar.'\n"
    "}}\n"
    "```"
)
assert old in content, "F12: old text not found"
content = content.replace(old, new, 1)
print("F12 applied")

# Write back
with open(spec_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\nAll fixes applied successfully. File written.")
print(f"Original length: {len(original)} chars | New length: {len(content)} chars")
