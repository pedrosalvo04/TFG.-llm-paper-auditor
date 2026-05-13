import sys

spec_path = "/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/output/02_functional_backend.md"

with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

errors = []

def replace_once(tag, old, new, content):
    if old not in content:
        errors.append(f"{tag}: old text NOT FOUND")
        return content
    count = content.count(old)
    if count > 1:
        errors.append(f"{tag}: WARNING: old text found {count} times, replacing first only")
    result = content.replace(old, new, 1)
    print(f"{tag} applied")
    return result

# =========================================================
# F01 — §3.4 Guard ACTION return shape
# SOURCE: rag_extraction_skill.py:31-32
# =========================================================
content = replace_once("F01",
    'CONDITION: `context.get("paper_text")` is falsy (empty string or absent)  \n'
    'ACTION: Return `{"success": False, "error": "No paper text in context", "phase": "hyperparameter_extraction"}`  \n'
    'ERROR: Non-critical; `PaperAuditor.audit()` catches this and continues pipeline',

    'CONDITION: `context.get("paper_text")` is falsy (empty string or absent); checked via `self.validate_context(context, [\'paper_text\'])`  \n'
    "ACTION: Return `{'extracted_hyperparameters_hybrid': {}}`  \n"
    'ERROR: Non-critical; `PaperAuditor.audit()` catches this and continues pipeline  \n'
    'SOURCE: `rag_extraction_skill.py:31-32`',
    content
)

# =========================================================
# F02 — §3.5 Step 1 chunking algorithm
# SOURCE: rag_extraction_skill.py:43-47
# =========================================================
content = replace_once("F02",
    '```pseudocode\n'
    'FUNCTION chunk_text(paper_text, chunk_size=1000, overlap=200):\n'
    '    chunks = []\n'
    '    start = 0\n'
    '    WHILE start < len(paper_text):\n'
    '        end = min(start + chunk_size, len(paper_text))\n'
    '        chunks.append(paper_text[start:end])\n'
    '        start += chunk_size - overlap\n'
    '    RETURN chunks\n'
    '```',

    '```pseudocode\n'
    "# Normalize line endings\n"
    "paper_text_norm = paper_text.replace('\\r\\n', '\\n')\n"
    '\n'
    '# Split on two or more consecutive newlines (Docling paragraph/block separator)\n'
    "raw_chunks = re.split(r'\\n\\n+', paper_text_norm)\n"
    '\n'
    '# Strip whitespace; discard blocks of 10 characters or fewer (noise filter)\n'
    'chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]\n'
    '```\n'
    '\n'
    'SOURCE: `rag_extraction_skill.py:43-47`',
    content
)

# =========================================================
# F03 — §3.5 Step 3 ChromaDB collection name + delete-before-create
# SOURCE: rag_extraction_skill.py:85-97
# =========================================================
content = replace_once("F03",
    '```pseudocode\n'
    'client = chromadb.Client()   # in-memory (no persistence)\n'
    'collection = client.create_collection("hyperparams")\n'
    'collection.add(\n'
    '    documents=chunks,\n'
    '    embeddings=embeddings,\n'
    '    ids=[f"chunk_{i}" for i in range(len(chunks))]\n'
    ')\n'
    '```',

    '```pseudocode\n'
    'chroma_client = chromadb.Client()   # in-memory (no persistence)\n'
    '\n'
    '# Delete stale collection from any previous run (silently ignore if absent)\n'
    'try:\n'
    '    chroma_client.delete_collection("paper_chunks")\n'
    'except:\n'
    '    pass\n'
    '\n'
    'collection = chroma_client.create_collection(name="paper_chunks")\n'
    'collection.add(\n'
    '    embeddings=embeddings,\n'
    '    documents=chunks,\n'
    '    ids=[str(i) for i in range(len(chunks))]\n'
    ')\n'
    '```\n'
    '\n'
    'SOURCE: `rag_extraction_skill.py:85-97`',
    content
)

# =========================================================
# F04 + F05 — §3.5 Step 4 query strings + call params
# SOURCE: rag_extraction_skill.py:99-113 (strings), 115-124 (call)
# =========================================================
content = replace_once("F04+F05",
    'The 13 fixed queries are:\n'
    '\n'
    '1. `"learning rate optimizer training configuration"`\n'
    '2. `"batch size training epochs iterations"`\n'
    '3. `"model architecture layers parameters"`\n'
    '4. `"regularization dropout weight decay"`\n'
    '5. `"dataset size training test split"`\n'
    '6. `"hardware GPU TPU computational resources"`\n'
    '7. `"software framework library version"`\n'
    '8. `"hyperparameter search tuning optimization"`\n'
    '9. `"loss function objective metric evaluation"`\n'
    '10. `"preprocessing normalization augmentation"`\n'
    '11. `"random seed initialization reproducibility"`\n'
    '12. `"inference deployment serving configuration"`\n'
    '13. `"ablation study baseline comparison"`\n'
    '\n'
    'Source: `extracted_backend_skills_01.md §4 (fixed query list)`\n'
    '\n'
    'For each query:\n'
    '\n'
    '```pseudocode\n'
    'results = collection.query(\n'
    '    query_texts=[query],\n'
    '    n_results=3\n'
    ')\n'
    '```',

    'The 13 fixed queries are (SOURCE: `rag_extraction_skill.py:99-113`):\n'
    '\n'
    '1. `"training details optimization hyperparameters"`\n'
    '2. `"learning rate schedule step size warmup decay learning rate"`\n'
    '3. `"batch size mini-batch micro-batch optimization global batch size"`\n'
    '4. `"epochs training steps iterations convergence training duration"`\n'
    '5. `"optimizer Adam SGD AdamW RMSprop momentum betas optimizer settings"`\n'
    '6. `"weight decay L2 regularization weight decay"`\n'
    '7. `"random seed reproducibility seed fixed seed initialization"`\n'
    '8. `"hardware GPU TPU NVIDIA AMD cluster infrastructure hardware setup"`\n'
    '9. `"hyperparameters configuration settings parameters appendix details"`\n'
    '10. `"experimental setup implementation details training configuration"`\n'
    '11. `"SFT Supervised Fine-tuning instruction tuning training schedule"`\n'
    '12. `"pre-training pretraining phase training protocols"`\n'
    '13. `"hyperparameter tuning iterations schedule iterations iterations"`\n'
    '\n'
    'All 13 query embeddings are generated in **one batched call** using\n'
    '`self.llm_client.client.models.embed_content(model=EMBEDDING_MODEL_NAME, contents=queries)`,\n'
    'then queried against ChromaDB as a single batch (SOURCE: `rag_extraction_skill.py:115-124`):\n'
    '\n'
    '```pseudocode\n'
    '# Generate embeddings for all 13 queries at once\n'
    'q_emb_res = llm_client.client.models.embed_content(\n'
    '    model=EMBEDDING_MODEL_NAME,\n'
    '    contents=queries          # list of 13 strings\n'
    ')\n'
    'query_embeddings = [e.values for e in q_emb_res.embeddings]\n'
    '\n'
    '# Single batched query — NOT one-at-a-time, NOT query_texts\n'
    'results = collection.query(\n'
    '    query_embeddings=query_embeddings,   # NOT query_texts=[query]\n'
    '    n_results=10                          # NOT 3\n'
    ')\n'
    '```',
    content
)

# =========================================================
# F06 — §3.5 Step 5 relevance scoring formula
# SOURCE: rag_extraction_skill.py:152-157
# =========================================================
content = replace_once("F06",
    '```pseudocode\n'
    'FUNCTION score_relevance(distance: float) -> float:\n'
    '    # ChromaDB distance: 0.0 = identical, 2.0 = completely dissimilar\n'
    '    IF distance <= 0.3:\n'
    '        RETURN 1.0\n'
    '    ELIF distance <= 0.7:\n'
    '        RETURN 1.0 - (distance - 0.3) / (0.7 - 0.3) * 0.5   # 1.0 → 0.5\n'
    '    ELIF distance <= 1.2:\n'
    '        RETURN 0.5 - (distance - 0.7) / (1.2 - 0.7) * 0.4   # 0.5 → 0.1\n'
    '    ELSE:\n'
    '        RETURN 0.0\n'
    '```\n'
    '\n'
    'Source: `extracted_backend_skills_01.md §4 (relevance scoring formula)`\n'
    '\n'
    'Only chunks with relevance score > 0.0 are included in the LLM context.',

    '```pseudocode\n'
    'FUNCTION score_relevance(distance: float) -> int:\n'
    '    # Returns integer 0–100 (NOT float 0–1)\n'
    '    # Breakpoints: <0.4 excellent (85–95), <0.7 moderate (31–85), >=0.7 noise (floor 5)\n'
    '    IF distance < 0.4:\n'
    '        RETURN int(95 - distance * 25)              # 0.0 → 95, 0.4 → 85\n'
    '    ELIF distance < 0.7:\n'
    '        RETURN int(85 - (distance - 0.4) * 180)    # 0.4 → 85, 0.7 → 31\n'
    '    ELSE:\n'
    '        RETURN max(5, int(31 - (distance - 0.7) * 50))  # >0.7: slow decay, floor 5\n'
    '```\n'
    '\n'
    'SOURCE: `rag_extraction_skill.py:152-157`\n'
    '\n'
    'Only chunks with relevance_score > 0 (integer) are included in the LLM context.\n'
    'In practice the floor is 5 for any distance >= 0.7, so exclusion only occurs when\n'
    'the chunk_relevance dict deduplication retains a chunk with score exactly 0 (not possible\n'
    'given the floor). All retrieved chunks are included.',
    content
)

# =========================================================
# F07 — §3.5 Step 7 merge strategy (LLM REDUCE, not last-write-wins)
# SOURCE: rag_extraction_skill.py:204-261
# =========================================================
content = replace_once("F07",
    '#### Step 7: Merge results\n'
    '\n'
    'All per-chunk extraction results are merged into a single `extracted_hyperparameters_hybrid` dict.\n'
    'Merge strategy: later chunks overwrite earlier chunks for the same key (last-write-wins).\n'
    '[GAP: exact merge deduplication strategy for extracted_hyperparameters_hybrid is not fully specified in extraction]',

    '#### Step 7: REDUCE phase — LLM consolidation\n'
    '\n'
    'SOURCE: `rag_extraction_skill.py:204-261`\n'
    '\n'
    'After all MAP extractions are collected into `extracted_fragments`, a dedicated LLM REDUCE\n'
    'call consolidates all fragments into a single canonical result. There is **no** deterministic\n'
    'last-write-wins merge; the LLM decides based on a structured prompt.\n'
    '\n'
    'The REDUCE prompt instructs the model to:\n'
    '- Resolve conflicts between fragments; prefer SFT/fine-tuning values over pre-training\n'
    '  where the distinction is obvious, otherwise pick the most representative value.\n'
    '- Ignore `"NOT FOUND"` values from one fragment if another fragment found a valid value.\n'
    '- Use `thought_process` from each fragment to build a final synthesis.\n'
    '- When multiple fragments cite different tables, verify which table title and headers\n'
    '  match the target hyperparameter (e.g., distinguish "Model Architecture" from "Training\n'
    '  Hyperparameters" tables).\n'
    '- Never guess or hallucinate.\n'
    '\n'
    'The raw REDUCE response is JSON-parsed using Balanced JSON Extraction (§2.8).\n'
    'On JSON parse failure, trailing-comma repair via `re.sub(r\',\\s*([\\]}])\', r\'\\1\', ...)` is\n'
    'attempted. The parsed dict is then cleaned by `_clean_with_regex()` which normalises\n'
    'scientific notation, extracts first integers, and maps empty/N/A values to `"NOT FOUND"`.',
    content
)

# =========================================================
# F09 + F10 — §11 SS Auth + Rate limiting
# SOURCE: sota_skills.py:182-185, 190-191, 215-217
# =========================================================
content = replace_once("F09+F10",
    '**Auth**: None (public API, unauthenticated)  \n'
    '**Rate limiting**: No explicit rate limit handling in skill; relies on HTTP 429 retry in LLMClient  \n'
    '[GAP: whether API key is optionally injected via config is not confirmed in extraction]',

    '**Auth**: Optional API key injection (SOURCE: `sota_skills.py:182-185`).  \n'
    'If `SEMANTIC_SCHOLAR_API_KEY` is set (non-falsy), the header `x-api-key` is added to every\n'
    'request; otherwise requests are sent without authentication (public endpoint).  \n'
    '**Rate limiting**: Explicit in-skill handling, independent of LLMClient (SOURCE: `sota_skills.py:190-191, 215-217`):  \n'
    '- `time.sleep(0.5)` before every query after the first (between-query throttle).  \n'
    '- On HTTP 429 response: `time.sleep(2)` then log warning and continue to next query.',
    content
)

# =========================================================
# F12 — §11 CrossValidationSkill Input Context Keys
# SOURCE: sota_skills.py:319-331
# =========================================================
content = replace_once("F12",
    '| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill |\n'
    '| `checklist` | dict | Yes | Phase 2/2.5 output |\n'
    '| `extracted_info` | dict | Yes | Phase 1 output |\n'
    '\n'
    '#### Guard Conditions\n'
    '\n'
    'RULE: guard_cross_validation  \n'
    'CONDITION: `context.get("sota_papers")` is falsy or `context.get("checklist")` is falsy  \n'
    'ACTION: Return `{"success": False, "error": "Missing sota_papers or checklist", "phase": "cross_validation"}`',

    '| `paper_text` | str | Yes | Full paper text |\n'
    '| `sota_papers` | list[dict] | Yes | From SemanticScholarSearchSkill |\n'
    '| `thematic_data` | dict | Yes | Thematic analysis dict (keys: `subtemas`, `areas_tecnicas`, `año_paper`) |\n'
    '\n'
    'Note: `checklist` and `extracted_info` are **not** required inputs. `paper_text` and\n'
    '`thematic_data` are required but were missing from the previous version of this spec.\n'
    '\n'
    'SOURCE: `sota_skills.py:319`\n'
    '\n'
    '#### Guard Conditions\n'
    '\n'
    'SOURCE: `sota_skills.py:319-331`\n'
    '\n'
    'RULE: guard_cross_validation  \n'
    'CONDITION: any of `paper_text`, `sota_papers`, or `thematic_data` is falsy; checked via\n'
    '`self.validate_context(context, [\'paper_text\', \'sota_papers\', \'thematic_data\'])`  \n'
    "ACTION: Return `{'validation_results': {}}`\n"
    '\n'
    'Additional guard: if `sota_papers` list is empty, return immediately with a default result:\n'
    '\n'
    '```python\n'
    "{'validation_results': {\n"
    "    'papers_omitidos': [],\n"
    "    'cobertura_tematica': {'areas_debiles': []},\n"
    "    'conclusion_sota': 'No se encontraron artículos recientes (2023-2026) en Semantic Scholar.'\n"
    '}}\n'
    '```',
    content
)

if errors:
    print("\nERRORS:")
    for e in errors:
        print(" ", e)
    sys.exit(1)
else:
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("\nAll fixes applied successfully. File written.")
