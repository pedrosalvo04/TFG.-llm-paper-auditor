"""Plantillas de prompts para el sistema de auditoria"""
import json

def get_extraction_prompt(paper_text: str, red_flags: dict) -> str:
    """
    Genera el prompt para la fase de extraccion de informacion.
    Incluye snippets detectados por regex para que el LLM los valide.
    """
    hp_snippets = red_flags.get('_hp_snippets', {}) if red_flags else {}
    snippets_section = ""
    if hp_snippets:
        snippets_section = "\nREGEX-DETECTED SNIPPETS (VALIDATE THESE - some may be false positives):\n"
        for k, v in hp_snippets.items():
            snippets_section += f"  - {k}: \"{v}\" -> Is this an actual reported value or a false positive?\n"

    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')} if red_flags else {}
    flags_section = ""
    if clean_flags:
        flags_section = f"\nRED FLAGS DETECTED BY REGEX PRE-PROCESSING:\n{json.dumps(clean_flags, indent=2)}\n"

    return f"""
CRITICAL: This system ONLY evaluates ML/AI papers (neural networks, deep learning, machine learning).

FIRST: Determine if this paper involves ML/AI training. If NO:
RETURN ONLY: {{"paper_type": "INVALID - Not ML/AI", "invalid_reason": "explanation"}}

If YES, continue with EXHAUSTIVE extraction below.
    
REASONING INSTRUCTIONS:
- Analyze technical ratios (e.g., if the paper mentions 0.13 million H800 hours, evaluate if that reflects the reported training efficiency).
- Look for hidden hyperparameters in tables or parenthetical remarks.
- Differentiate between pre-training and fine-tuning settings.
- Use the 'thought_process' field to document your reasoning step-by-step before filling the structured fields.

You are an expert information extractor for ML/AI papers. Your job is to extract
SPECIFIC factual information - not opinions - from every section of the paper.

ANALYSIS STRATEGY - Read the paper section by section:
1. Abstract + Introduction -> claims, scope, contributions
2. Methods/Architecture -> model details, design choices
3. Training/Optimization -> hyperparameters, optimizer, schedule
4. Data -> datasets, preprocessing, splits
5. Experiments/Results -> baselines, metrics, tables
6. Implementation -> code, hardware, software versions
7. Appendix -> often contains hyperparameter tables, environmental data
8. Limitations/Broader Impact -> quality and specificity

CRITICAL RULES:
- Search APPENDIX and ALL tables (Table 1 through Table 10+) before marking NOT FOUND
- Look specifically for "Data Availability Statement", "Dataset access", or URLs to model hubs (HuggingFace, etc.)
- If paper says "standard settings" or "not disclosed" -> extract as vague_phrase, NOT as the actual value
- For software, look for any mentions of frameworks (PyTorch, JAX), libraries (Transformers, DeepSpeed), or specific training protocols.
{snippets_section}
{flags_section}

EXTRACT THE FOLLOWING (respond "NOT FOUND" ONLY after exhaustive search):

1. CODE: repository_url, negative_phrase (quote if code cannot be released), dependencies, instructions (yes/no), release_mention
2. DATA: dataset_name, access_url, negative_phrase, preprocessing, splits, release_mention
3. HYPERPARAMETERS: optimizer, learning_rate, batch_size, epochs, training_steps, total_tokens, warmup, weight_decay, betas, epsilon, vague_phrase (quote if uses "standard settings" etc), table_reference
4. HARDWARE: gpu_cpu (specific model), num_gpus, memory, time, carbon_footprint, energy_consumption, pue, throughput (tokens/sec), latency_metrics
5. STATISTICS: confidence_intervals (yes/no), significance_tests (yes/no), num_runs
6. ARCHITECTURE: description (layers, dims, heads), weights_available, release_mention
7. BASELINE COMPARISON: compared_models (list), has_comparative_tables (yes/no), same_metrics (yes/no), results_section
8. SOFTWARE: framework_versions (e.g. "PyTorch 2.0"), python_version, cuda_version, dependency_file (yes/no)
9. LIMITATIONS: has_section (yes/no), specific_points (list), quantified_issues (yes/no)
10. PROBLEMATIC PHRASES: Extract TEXTUALLY any phrase with "cannot release", "proprietary", "confidential", "not available", "restricted", "competitive concerns". NOTE: Ignore phrases regarding "restricted compute", "restricted budget", or "restricted resources".
11. THEORY_AND_PROOFS: explicitly state if there are theoretical derivations, mathematical formulations, proof sketches, or assumptions detailed in the main text or the APPENDIX. Mention specifically if an appendix contains proofs.
12. BROADER_IMPACTS: explicitly check for an "Impact Statement", "Broader Impacts", or "Societal Impact" section. This is OFTEN in the APPENDIX. Note any discussions about environmental impact, bias, privacy, security, or misuse.
13. AI_ASSISTANTS_IN_WRITING: explicitly check for a declaration regarding the use of AI tools (ChatGPT, Claude, etc.) for writing, editing, or preparing the paper (usually in Appendix or Acknowledgments).
14. LLM_IN_METHODOLOGY: explicitly state if any language models (e.g., BERT, GPT, LLaMA) were used for automated data annotation, filtering, evaluation, or as part of the core methodology.
15. HUMAN_SUBJECTS_AND_CROWDSOURCING: explicitly state if the paper uses human annotators, crowdsourcing, or human-annotated datasets (e.g. SFT datasets with human labels). Look for compensation details or instructions.
16. LICENSES: explicitly extract any mentioned licenses (e.g., CC-BY, MIT, Apache) for datasets, code, or models USED or RELEASED. If external datasets are used, note if their specific licenses are named.
17. CODE_OF_ETHICS: explicitly search for a "Code of Ethics", "Ethics Statement", or "Ethical Considerations" section or mention.

RETURN JSON:
{{
  "thought_process": "Internal reasoning about the technical details found in the paper. Specifically analyze technical ratios (e.g., if the paper mentions 0.13 million H800 hours, evaluate if that reflects the reported training efficiency). Identify hidden hyperparameters in tables or parenthetical remarks. Differentiate between pre-training and fine-tuning settings.",
  "paper_type": "ML/AI or INVALID - Not ML/AI",
  "invalid_reason": "",
  "code": {{
    "repository_url": "URL or NOT FOUND",
    "negative_phrase": "textual quote or NOT FOUND",
    "dependencies": "description or NOT FOUND",
    "instructions": "yes/no",
    "release_mention": "quote or NOT FOUND"
  }},
  "data": {{
    "dataset_name": "name or NOT FOUND",
    "access_url": "URL/DOI or NOT FOUND",
    "negative_phrase": "textual quote or NOT FOUND",
    "preprocessing": "description or NOT FOUND",
    "splits": "description or NOT FOUND",
    "release_mention": "quote or NOT FOUND"
  }},
  "hyperparameters": {{
    "optimizer": "name or NOT FOUND",
    "learning_rate": "value or NOT FOUND",
    "batch_size": "value or NOT FOUND",
    "epochs": "value or NOT FOUND",
    "training_steps": "value or NOT FOUND",
    "total_tokens": "value or NOT FOUND",
    "warmup": "value or NOT FOUND",
    "weight_decay": "value or NOT FOUND",
    "betas": "values or NOT FOUND",
    "epsilon": "value or NOT FOUND",
    "vague_phrase": "textual quote or NOT FOUND",
    "table_reference": "table number or NOT FOUND"
  }},
  "hardware": {{
    "gpu_cpu": "specific model or NOT FOUND",
    "num_gpus": "number or NOT FOUND",
    "memory": "amount or NOT FOUND",
    "time": "duration or NOT FOUND",
    "carbon_footprint": "value or NOT FOUND",
    "energy_consumption": "value or NOT FOUND",
    "pue": "value or NOT FOUND",
    "throughput": "value or NOT FOUND",
    "latency_metrics": "verbatim details or NOT FOUND"
  }},
  "statistics": {{
    "confidence_intervals": "yes/no",
    "significance_tests": "yes/no",
    "num_runs": "number or NOT FOUND"
  }},
  "architecture": {{
    "description": "detailed summary or NOT FOUND",
    "weights_available": "yes/no",
    "release_mention": "quote or NOT FOUND"
  }},
  "baseline_comparison": {{
    "compared_models": ["list"],
    "has_comparative_tables": "yes/no",
    "same_metrics": "yes/no",
    "results_section": "summary or NOT FOUND"
  }},
  "software_versions": {{
    "framework": "name+version or NOT FOUND",
    "python_version": "version or NOT FOUND",
    "cuda_version": "version or NOT FOUND",
    "dependency_file": "yes/no"
  }},
  "limitations_quality": {{
    "has_section": "yes/no",
    "specific_points": ["point1", "point2"],
    "quantified_issues": "yes/no"
  }},
  "problematic_phrases": ["textual quote 1", "textual quote 2"],
  "theory_and_proofs": {{
    "has_theoretical_results": "yes/no/not found",
    "assumptions_stated": "description or NOT FOUND",
    "proofs_included": "yes/no/not found",
    "appendix_reference": "reference to appendix section or NOT FOUND"
  }},
  "broader_impacts_extraction": {{
    "has_impact_statement": "yes/no/not found",
    "appendix_reference": "reference to appendix or NOT FOUND",
    "concerns_discussed": ["list of concerns like bias, environment, etc."]
  }},
  "llm_usage_extraction": {{
    "models_used_in_methodology": ["list"],
    "purpose_in_methodology": "description or NOT FOUND",
    "used_for_writing": "yes/no/not mentioned",
    "writing_declaration_quote": "textual quote or NOT FOUND"
  }},
  "human_subjects_extraction": {{
    "uses_human_annotation": "yes/no",
    "compensation_details": "description or NOT FOUND",
    "instructions_provided": "yes/no"
  }},
  "licenses_extraction": {{
    "assets_used": ["list of datasets/code, including benchmarks like MMLU, GSM8k, etc."],
    "licenses_named": ["list of explicit licenses"],
    "missing_licenses_for_some_assets": "yes/no"
  }},
  "context_mapping": ["Abstract", "Methodology", "Experiments", "Appendix"]
}}

PAPER TEXT:
{paper_text}
"""


def get_map_extraction_prompt(fragment_text: str) -> str:
    """Prompt para la fase MAP del analisis general."""
    return f"""
    You are a Senior ML Researcher performing a deep technical extraction on a FRAGMENT of a scientific paper.
    
    TASK:
    Extract EVERY technical detail, hyperparameter, architectural choice, and experimental result found in this fragment.
    
    REASONING INSTRUCTIONS:
    - Identify specific architectural components (e.g., "Gated Attention", "MoE configuration", "Normalization layers").
    - Capture ALL hyperparameters even if they seem minor (betas, epsilon, warmup steps, weight decay).
    - Note specific benchmarks and their corresponding results if present in tables or text.
    - Document your 'thought_process' specifically for this fragment.
    
    FRAGMENT:
    {fragment_text}
    
    STRUCTURE:
    Return a structured JSON with the following standard keys (add more if needed to preserve detail):
    - "paper_title"
    - "authors"
    - "context_mapping" (list of sections in this fragment)
    - "code"
    - "data"
    - "hyperparameters" (optimizer, LR, batch size, and technical variants)
    - "hardware"
    - "statistics"
    - "architecture" (layers, gating, MoE, dims)
    - "baseline_comparison"
    - "software_versions"
    - "limitations_quality"
    - "problematic_phrases"
    - "theory_and_proofs"
    - "broader_impacts_extraction"
    - "llm_usage_extraction"
    - "human_subjects_extraction"
    - "licenses_extraction"
    - "thought_process"
    
    If a field is not mentioned in this fragment, use "NOT FOUND" or an empty list [].
    BE EXHAUSTIVE. Do not summarize; extract verbatim data where possible.
    """


def get_reduce_extraction_prompt(map_results: list) -> str:
    """Prompt para la fase REDUCE del analisis general."""
    return f"""
    You are a Senior AI Researcher and Meta-Reviewer. Your task is to CONSOLIDATE multiple partial extractions (MAP phase) from a scientific paper into a single DEFINITIVE MASTER JSON.
    
    INPUT DATA:
    {json.dumps(map_results, indent=2)}
    
    CRITICAL OBJECTIVE: 
    ZERO INFORMATION LOSS. You must synthesize a master database that preserves EVERY unique technical detail found across all fragments.
    
    CONSOLIDATION RULES:
    1. RESOLVE CONFLICTS: If fragments conflict (e.g., different LR values), prioritize the most specific one or the one explicitly stated in a 'Hyperparameters' table.
    2. ARCHITECTURE MERGE: Combine all architectural details (layers, heads, gating mechanisms, MoE configs). If Fragment A describes the gating mechanism and Fragment B describes the MoE expert count, the final 'model_architecture' MUST contain both.
    3. HYPERPARAMETER SYNTHESIS: Aggregate all training settings. If different phases (Pre-training vs SFT) have different parameters, list them clearly or provide them as lists/objects.
    4. DATA & HARDWARE: Combine token counts, dataset names, GPU types, and total compute hours.
    5. EXPERIMENTAL RESULTS: Perform a union of all benchmarks and metrics. Preserve specific numbers from tables (e.g., MMLU: 70.2, HumanEval: 45.1).
    6. CONTEXT MAPPING: Create a deduplicated, ordered list of ALL sections identified across all fragments.
    7. THOUGHT PROCESS: Build a final synthesis of the paper's technical rigor and reproducibility based on the consolidated evidence.
    
    FINAL STRUCTURE (Consolidate into these standard keys, preserving all sub-details):
    - "paper_title"
    - "authors"
    - "context_mapping"
    - "code" (repository_url, release_mention, etc.)
    - "data" (dataset_name, access_url, preprocessing, etc.)
    - "hyperparameters" (optimizer, learning_rate, batch_size, training_steps, total_tokens, and ALL technical variants)
    - "hardware" (gpu_cpu, num_gpus, time, energy, latency, throughput, etc.)
    - "statistics" (runs, intervals)
    - "architecture" (detailed description of layers, gating, MoE, etc.)
    - "baseline_comparison" (compared_models, tables)
    - "software_versions"
    - "limitations_quality"
    - "problematic_phrases"
    - "theory_and_proofs"
    - "broader_impacts_extraction"
    - "llm_usage_extraction"
    - "human_subjects_extraction"
    - "licenses_extraction"
    - "thought_process"
    
    RETURN THE CONSOLIDATED MASTER JSON ONLY. Ensure the JSON is perfectly formatted and valid.
    """


def get_evaluation_signals(extracted_info: dict) -> dict:
    """Calcula las señales explícitas para guiar al LLM y para visualización."""
    if not extracted_info:
        return {}
        
    code_info = extracted_info.get('code') if isinstance(extracted_info.get('code'), dict) else {}
    data_info = extracted_info.get('data') if isinstance(extracted_info.get('data'), dict) else {}
    hw_info = extracted_info.get('hardware') if isinstance(extracted_info.get('hardware'), dict) else {}
    lic_info = extracted_info.get('licenses_extraction') if isinstance(extracted_info.get('licenses_extraction'), dict) else {}
    human_info = extracted_info.get('human_subjects_extraction') if isinstance(extracted_info.get('human_subjects_extraction'), dict) else {}

    code_url = code_info.get('repository_url', 'NOT FOUND')
    data_url = data_info.get('access_url', 'NOT FOUND')
    code_negative = code_info.get('negative_phrase', 'NOT FOUND')
    code_release = code_info.get('release_mention', 'NOT FOUND')
    has_any_url = (code_url != 'NOT FOUND') or (data_url != 'NOT FOUND')
    has_release_intent = code_release != 'NOT FOUND' and any(word in code_release.lower() for word in ['release', 'open-source', 'available', 'github', 'provide'])

    signals = {}
    
    signals['reproducibility'] = (
        f"DETECTED URLS -> code_repo: {code_url}, data_access: {data_url}. "
        "Any public URL (demo page, model checkpoint, GitHub repo, HuggingFace) "
        "counts as a valid reproducibility mechanism per NeurIPS guidelines. "
        "Only answer No if the paper explicitly states code/data/model are restricted AND no alternative is offered."
    )

    signals['open_access'] = (
        f"DETECTED -> code_url: {code_url}, data_url: {data_url}, "
        f"negative_phrase: {code_negative}, release_intent: {code_release}. "
        "RULE FOR ITEM 5: "
        "- If a public URL (demo page, project page, GitHub, HuggingFace) is present -> answer 'Yes'. "
        "- If NO URL is found but there is a CLEAR intent to release (e.g., 'we will release our code', 'code will be made available') -> answer 'Yes' and cite the intent as evidence. "
        "  Do NOT penalize as 'No' if the authors explicitly commit to a future release. "
        "- If negative_phrase is present (e.g., 'code is proprietary', 'cannot release') AND no URL exists -> answer 'No'. "
        "- If no URL and no release intent and no negative phrase -> answer 'No' with is_no_justified: false."
    )

    gpu_hours = hw_info.get('time', 'NOT FOUND')
    num_gpus = hw_info.get('num_gpus', 'NOT FOUND')
    total_tokens = extracted_info.get('hyperparameters', {}).get('total_tokens', 'NOT FOUND')
    model_params = extracted_info.get('architecture', {}).get('description', '')
    
    signals['statistics'] = (
        f"DETECTED compute -> training_time: {gpu_hours}, num_gpus: {num_gpus}, total_tokens: {total_tokens}. "
        "LARGE SCALE JUSTIFICATION: "
        "If the paper involves Large Language Models (LLMs) trained on billions/trillions of tokens or with billions of parameters (e.g., 15B+), "
        "performing multiple statistical runs is computationally prohibitive. "
        "In these cases, answer 'No' but set is_no_justified: true, stating that the massive scale of training justifies the lack of multiple runs."
    )

    assets_used = lic_info.get('assets_used', [])
    licenses_named = lic_info.get('licenses_named', [])
    # Check if common benchmarks are mentioned in assets_used even if lic_info missed them
    has_external_assets = bool(assets_used and assets_used not in [[], ['NOT FOUND'], ['list of datasets/code']])
    
    signals['licenses'] = (
        f"DETECTED -> assets_used: {assets_used}, licenses_named: {licenses_named}. "
        "CRITICAL RULE FOR ITEM 12/13: "
        "- If the paper mentions standard benchmarks (e.g., MMLU, GSM8k, Hellaswag, HumanEval, C-Eval) in any section -> HAS_EXTERNAL_ASSETS is TRUE. "
        "- If external assets are used but their specific licenses (e.g., MIT, Apache 2.0, CC-BY) are NOT mentioned -> answer 'No' (NOT N/A). "
        "- Only answer 'N/A' if the paper is purely theoretical or uses ONLY new, proprietary data that they created themselves."
    )

    human_annotation = human_info.get('uses_human_annotation', 'no')
    signals['crowdsourcing'] = (
        f"DETECTED -> uses_human_annotation: {human_annotation}. "
        "STRICT RULE: If this is false/no, the paper does NOT involve human subjects -> answer MUST be N/A. "
        "Do NOT answer No just because compensation is unmentioned when there is no crowdsourcing at all. "
        "Only answer No/Yes if crowdsourcing or human annotation is CONFIRMED present."
    )
    
    return signals


def get_evaluation_prompt(extracted_info: dict, red_flags: dict) -> str:
    """
    Genera el prompt para evaluacion segun criterios NeurIPS 2026.
    Nuevo paradigma: validacion de transparencia, sin puntuacion numerica.
    """
    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')} if red_flags else {}
    flags_section = ""
    if clean_flags:
        flags_section = f"\nRED FLAGS (automated regex pre-processing):\n{json.dumps(clean_flags, indent=2)}\n"

    signals = get_evaluation_signals(extracted_info)

    return f"""
Act as a Senior Area Chair for NeurIPS 2026. Your task is to VALIDATE the transparency of the NeurIPS 2026 Paper Checklist.
DO NOT produce any numeric score. Your output is a transparency audit, not a grade.

EXTRACTED INFORMATION:
{json.dumps(extracted_info, indent=2, ensure_ascii=False)}

{flags_section}

=======================================================
PRE-COMPUTED SIGNALS - USE THESE TO AVOID COMMON ERRORS
=======================================================
[Item 4 - Reproducibility]   {signals['reproducibility']}
[Item 5 - Open Access]       {signals['open_access']}
[Item 7 - Statistics]        {signals['statistics']}
[Item 12 - Licenses]         {signals['licenses']}
[Item 14 - Crowdsourcing]    {signals['crowdsourcing']}

=======================================================
OUTPUT RULES - MANDATORY FOR ALL 16 ITEMS
=======================================================
For every item:
- "answer" MUST be exactly one of: "Yes", "No", or "N/A".
- If "Yes" -> "evidence" MUST contain the paper section AND a significant verbatim fragment (e.g. "Section 4.1: 'We use the AdamW optimizer with...'"). 
  - PROVIDE AS MUCH CONTEXT AS POSSIBLE in the evidence.
- If "No" -> "justification" MUST explain exactly what is missing and why it constitutes a transparency risk (e.g., "The authors mention training on H100s but provide no total training time or energy consumption details, which is required by Item 8.").
- If "N/A" -> "justification" MUST explain clearly why the item is not applicable to this specific paper.
- "is_no_justified" MUST be true only if explicit justification exists or pre-computed signals apply.
- BE VERBOSE and TECHNICAL. Do not use generic phrases. Provide specific details found (or not found) in the provided information.
- LENGTH REQUIREMENT: Every "evidence" and "justification" field should be at least 2-3 sentences long if possible, citing specific data points, section names, and verbatim quotes. Do not truncate information for brevity. We value depth over conciseness here.

=======================================================
CRITICAL PER-ITEM RULES
=======================================================
Item 1 (Claims):
  STRICT VALIDATION: You MUST verify if the claims in the Abstract/Introduction (e.g., "our model outperforms SOTA", "competitiveness with LLaMA") are actually supported by the extracted results and baseline comparisons. 
  - Cross-reference the "claims" found in the intro with the "baseline_comparison" results.
  - DO NOT just cite the section. Explain IF the claim is supported by the data (e.g., "The claim of competitiveness with LLaMA3-8B is supported by Table 1, which shows LLaDA-8B achieving 65.2 vs 64.8 in MMLU").
  - If a claim is unsupported or only partially supported, mark "No" or explain the nuance in the justification.

Item 2 (Limitations):
  NeurIPS EXPLICITLY INSTRUCTS reviewers NOT to penalize honesty about limitations.
  If ANY limitations are stated -- even briefly -- answer "Yes". Only "No" if LITERALLY NO limitations section exists.

Item 4 (Experimental Result Reproducibility):
  NeurIPS accepts MULTIPLE reproducibility forms. Any of these count as "Yes":
  demo page, hosted model, GitHub repo, model checkpoint, HuggingFace model, detailed architecture description.
  Use the [Item 4] pre-computed signal. If any public URL is present, answer "Yes" unless paper explicitly restricts all access.

Item 5 (Open Access to Data and Code):
  Use the [Item 5 - Open Access] pre-computed signal EXACTLY.
  If ANY public URL exists (project page, demo, HuggingFace, GitHub) -> answer "Yes" with that URL as evidence.
  NeurIPS considers a demo page or model card a valid form of open access.

Item 6 (Experimental Setting/Details):
  Do NOT penalize for missing minor optimizer internals (betas, epsilon) when primary hyperparameters (LR, batch size, weight decay) are present.

Item 7 (Statistical Significance):
  Search for error bars, +/-values, confidence intervals in results. If none found, answer "No".
  Use the [Item 7] pre-computed signal for is_no_justified decision.

Item 9 (Code of Ethics):
  NeurIPS 2026 REQUIRES a Code of Ethics statement. 
  - If a dedicated "Code of Ethics", "Ethics Statement", or "Ethical Considerations" section exists, OR if the authors provide a technical and serious discussion of ethical implications (e.g., bias mitigation, safety protocols, dual-use concerns) -> answer "Yes".
  - CRITICAL: Superficial or unrelated mentions (e.g., "we care about the environment" or "we followed local laws") are NOT sufficient for a "Yes". If the statement is too vague or lacks technical depth, answer "No" and justify.
  - If LITERALLY NOTHING is found -> answer "No".
  - NEVER answer "N/A" for this item. A lack of a serious statement is a "No" (missing transparency).

Item 12 (Licenses):
  Use the [Item 12] pre-computed signal EXACTLY as instructed.

Item 14 (Crowdsourcing and Human Subjects):
  Use the [Item 14] pre-computed signal EXACTLY as instructed. When in doubt, N/A is correct for non-human-subject papers.

Item 16 (Declaration of LLM Usage):
  NeurIPS 2026 requires a declaration if AI assistants (like ChatGPT, Claude, etc.) were used for writing, editing, or preparing the paper.
  - If the authors explicitly state they used AI for writing/editing -> "Yes".
  - If there is NO mention of AI usage for paper preparation -> "N/A" (standard practice for papers not using AI for writing).
  - CRITICAL: DO NOT confuse the paper's topic (e.g., "Gated Attention for LLMs" or "Training LLMs") with the authors' usage of AI tools for WRITING. A paper ABOUT Large Language Models does NOT count as using AI to WRITE the paper. Only answer "Yes" if the authors explicitly declare using tools like ChatGPT/Claude for the MANUSCRIPT preparation.

=======================================================
RETURN JSON ONLY. NO OTHER TEXT.
=======================================================
{{
  "claims": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "limitations": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "theory_assumptions_proofs": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "experimental_result_reproducibility": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "open_access_data_code": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "experimental_setting_details": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "experiment_statistical_significance": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "experiments_compute_resource": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "code_of_ethics": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "broader_impacts": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "safeguards": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "licenses": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "assets": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "crowdsourcing_human_subjects": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "irb_approvals": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }},
  "declaration_llm_usage": {{ "answer": "Yes/No/N/A", "evidence": "Section/fragment if Yes", "justification": "...", "is_no_justified": false }}
}}
"""

def get_verification_prompt(item_key: str, item_data: dict, paper_context: str) -> str:
    """
    Prompt para la fase de 'Auditor Estricto' (Self-Correction).
    Realiza una verificacion OBJETIVA para confirmar si la evaluacion inicial es correcta,
    detectando tanto Falsos Negativos como Falsos Positivos.
    """
    answer = item_data.get('answer', 'N/A')
    justification = item_data.get('justification', '')
    evidence = item_data.get('evidence', '')
    
    return f"""
    You are an OBJECTIVE NEURIPS AUDITOR. Your task is to VERIFY the accuracy of an initial evaluation of a scientific paper.
    
    CRITICAL INSTRUCTIONS:
    - If initial answer is 'No' or 'N/A': Search for FALSE NEGATIVES (evidence that was missed).
    - If initial answer is 'Yes': Search for FALSE POSITIVES (claiming compliance when evidence is weak, generic, or incorrect).
    - Your goal is the TRUTH. Do not change the answer unless you are 100% sure the initial one is wrong.

    ITEM TO VERIFY: {item_key}
    INITIAL ANSWER: {answer}
    INITIAL JUSTIFICATION: {justification}
    INITIAL EVIDENCE: {evidence}

    PAPER CONTEXT (Excerpts or Full Text):
    {paper_context}

    INSTRUCTIONS:
    1. Review the initial evaluation and the paper context.
    2. STRICT SEMANTIC VALIDATION: You MUST verify that the 'evidence' quote is actually RELEVANT to the item. Hallucination check: sometimes the initial auditor picks a random technical quote from the correct section that has NOTHING to do with the checklist item (e.g., citing latency numbers for an LLM Usage declaration). If the evidence is irrelevant, mark it as a FALSE POSITIVE.
    3. Item 16 (AI Usage for Writing) CRITICAL DISTINCTION: You MUST differentiate between the "Object of Study" (e.g., a paper researching Gated Attention for LLMs) and the "Tool for Preparation" (e.g., using ChatGPT to write the abstract). 
       - Mentions of "LLM", "GPT", or "LLaMA" in the methodology or architecture are research topics, NOT declarations of AI-assisted writing. 
       - Answering "Yes" for Item 16 based on methodology text is a CRITICAL HALLUCINATION. Only "Yes" if there is an explicit statement about using AI to assist in the manuscript preparation.
    4. For 'Yes' answers: Verify the verbatim quote in 'evidence' actually exists and directly supports the 'Yes' answer.
    5. For Item 7 (Statistics): Beware of tables that show performance results but NO variance (std dev, intervals). A table of results is NOT statistical significance unless it includes error metrics.
    6. Search for explicit section headers like "Data Availability", "Ethical Statement", or "Limitations" that might have been missed.
    7. If you change the answer, provide a detailed 'justification' explaining exactly why the initial reference was incorrect (e.g., "The cited quote discusses model latency, which is irrelevant to the declaration of LLM usage for writing").

    RETURN JSON ONLY:
    {{
      "answer": "Yes/No/N/A",
      "evidence": "Detailed verbatim quote and section",
      "justification": "Technical explanation of why the answer is correct or why it was corrected",
      "is_no_justified": true/false,
      "was_corrected": true/false
    }}
    """
