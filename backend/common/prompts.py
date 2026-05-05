"""Plantillas de prompts para el sistema de auditoria"""
import json

def get_extraction_prompt(context_mapping: dict, red_flags: dict) -> str:
    """
    Genera el prompt para la fase de extraccion de informacion.
    Utiliza 'Context Mapping' para inyectar solo fragmentos relevantes por sección.
    Incluye snippets detectados por regex para que el LLM los valide.
    """
    hp_snippets = red_flags.get('_hp_snippets', {})
    snippets_section = ""
    if hp_snippets:
        snippets_section = "\nREGEX-DETECTED SNIPPETS (VALIDATE THESE - some may be false positives):\n"
        for k, v in hp_snippets.items():
            snippets_section += f"  - {k}: \"{v}\" -> Is this an actual reported value or a false positive?\n"

    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')}

    return f"""
CRITICAL: This system ONLY evaluates ML/AI papers (neural networks, deep learning, machine learning).

FIRST: Determine if this paper involves ML/AI training. If NO:
RETURN ONLY: {{"paper_type": "INVALID - Not ML/AI", "invalid_reason": "explanation"}}

If YES, continue with EXHAUSTIVE extraction below.

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
- If paper says "standard settings", "default parameters", or "following [Previous Work]" -> extract these as the values for hyperparameters.
- Training duration can be optimization steps (e.g. 100k) or total tokens (e.g. 3.5T). Extract these in the 'epochs' field if epochs are not present.
- For software, look for any mentions of frameworks (PyTorch, JAX), libraries (Transformers, DeepSpeed), or specific training protocols.
{snippets_section}
RED FLAGS DETECTED BY REGEX PRE-PROCESSING:
{json.dumps(clean_flags, indent=2)}

EXTRACT THE FOLLOWING (respond "NOT FOUND" ONLY after exhaustive search):

1. CODE: repository_url, negative_phrase (quote if code cannot be released), dependencies, instructions (yes/no), release_mention
2. DATA: dataset_name, access_url, negative_phrase, preprocessing, splits, release_mention
3. HYPERPARAMETERS: optimizer, learning_rate, batch_size, epochs, warmup, weight_decay, betas, epsilon, vague_phrase (quote if uses "standard settings" etc), table_reference
4. HARDWARE: gpu_cpu (specific model), num_gpus, memory, time, carbon_footprint, energy_consumption, pue
5. STATISTICS: confidence_intervals (yes/no), significance_tests (yes/no), num_runs
6. ARCHITECTURE: description (layers, dims, heads), weights_available, release_mention
7. BASELINE COMPARISON: compared_models (list), has_comparative_tables (yes/no), same_metrics (yes/no), results_section
8. SOFTWARE: framework_versions (e.g. "PyTorch 2.0"), python_version, cuda_version, dependency_file (yes/no)
9. LIMITATIONS: has_section (yes/no), specific_points (list), quantified_issues (yes/no)
10. PROBLEMATIC PHRASES: Extract TEXTUALLY any phrase with "cannot release", "proprietary", "confidential", "not available", "restricted", "competitive concerns". NOTE: Ignore phrases regarding "restricted compute", "restricted budget", or "restricted resources".
11. THEORY_AND_PROOFS: explicitly state if there are theoretical derivations, mathematical formulations, proof sketches, or assumptions detailed in the main text or the APPENDIX. Mention specifically if an appendix contains proofs.
12. BROADER_IMPACTS: explicitly check for an "Impact Statement", "Broader Impacts", or "Societal Impact" section. This is OFTEN in the APPENDIX. Note any discussions about environmental impact, bias, privacy, security, or misuse.
13. LLM_USAGE: explicitly state if any language models (e.g., BERT, GPT, LLaMA) were used for automated data annotation, filtering, evaluation, or as part of the core methodology.
14. HUMAN_SUBJECTS_AND_CROWDSOURCING: explicitly state if the paper uses human annotators, crowdsourcing, or human-annotated datasets (e.g. SFT datasets with human labels). Look for compensation details or instructions.
15. LICENSES: explicitly extract any mentioned licenses (e.g., CC-BY, MIT, Apache) for datasets, code, or models USED or RELEASED. If external datasets are used, note if their specific licenses are named.

RETURN JSON:
{{
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
    "pue": "value or NOT FOUND"
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
    "models_used": ["list"],
    "purpose": "description or NOT FOUND"
  }},
  "human_subjects_extraction": {{
    "uses_human_annotation": "yes/no",
    "compensation_details": "description or NOT FOUND",
    "instructions_provided": "yes/no"
  }},
  "licenses_extraction": {{
    "assets_used": ["list of datasets/code"],
    "licenses_named": ["list of explicit licenses"],
    "missing_licenses_for_some_assets": "yes/no"
  }}
}}

CONTEXT MAPPING (Read the specific section for each topic):

--- 1. CODE ---
{context_mapping.get('code', 'NOT FOUND')}

--- 2. DATA ---
{context_mapping.get('data', 'NOT FOUND')}

--- 3. HYPERPARAMETERS ---
{context_mapping.get('hyperparameters', 'NOT FOUND')}

--- 4. HARDWARE ---
{context_mapping.get('hardware', 'NOT FOUND')}

--- 5. STATISTICS ---
{context_mapping.get('statistics', 'NOT FOUND')}

--- 6. ARCHITECTURE ---
{context_mapping.get('architecture', 'NOT FOUND')}

--- 7. BASELINE COMPARISON ---
{context_mapping.get('baseline_comparison', 'NOT FOUND')}

--- 8. SOFTWARE ---
{context_mapping.get('software', 'NOT FOUND')}

--- 9. LIMITATIONS ---
{context_mapping.get('limitations', 'NOT FOUND')}

--- 10. PROBLEMATIC PHRASES ---
{context_mapping.get('problematic_phrases', 'NOT FOUND')}

--- 11. THEORY AND PROOFS ---
{context_mapping.get('theory_and_proofs', 'NOT FOUND')}

--- 12. BROADER IMPACTS ---
{context_mapping.get('broader_impacts', 'NOT FOUND')}

--- 13. LLM USAGE ---
{context_mapping.get('llm_usage', 'NOT FOUND')}

--- 14. HUMAN SUBJECTS ---
{context_mapping.get('human_subjects', 'NOT FOUND')}

--- 15. LICENSES ---
{context_mapping.get('licenses', 'NOT FOUND')}
"""


def get_evaluation_prompt(extracted_info: dict, red_flags: dict) -> str:
    """
    Genera el prompt para evaluacion segun criterios NeurIPS 2026.
    Nuevo paradigma: validacion de transparencia, sin puntuacion numerica.
    """
    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')}

    # --- Pre-compute explicit signals to guide the LLM and avoid common errors ---

    # Signals for Items 4 and 5: URL detection
    code_url = extracted_info.get('code', {}).get('repository_url', 'NOT FOUND')
    data_url = extracted_info.get('data', {}).get('access_url', 'NOT FOUND')
    code_negative = extracted_info.get('code', {}).get('negative_phrase', 'NOT FOUND')
    has_any_url = (code_url != 'NOT FOUND') or (data_url != 'NOT FOUND')

    reproducibility_signal = (
        f"DETECTED URLS -> code_repo: {code_url}, data_access: {data_url}. "
        "Any public URL (demo page, model checkpoint, GitHub repo, HuggingFace) "
        "counts as a valid reproducibility mechanism per NeurIPS guidelines. "
        "Only answer No if the paper explicitly states code/data/model are restricted AND no alternative is offered."
    )

    # Item 5 signal: distinguish 'demo only' from 'code not released'
    open_access_signal = (
        f"DETECTED -> code_url: {code_url}, data_url: {data_url}, "
        f"negative_phrase: {code_negative}, has_any_public_url: {has_any_url}. "
        "RULE FOR ITEM 5: "
        "- If a public URL (demo page, project page, GitHub, HuggingFace) is present -> answer 'Yes'. "
        "  NeurIPS accepts demo pages and model cards as forms of open access. "
        "  Use the URL as the evidence. "
        "- If negative_phrase is present (e.g., 'code is proprietary', 'cannot release') AND no URL exists -> answer 'No'. "
        "- If no URL and no negative phrase -> answer 'No' with is_no_justified: false."
    )

    # Signal for Item 7: large-scale training implicitly justifies no multiple runs
    gpu_hours = extracted_info.get('hardware', {}).get('time', 'NOT FOUND')
    num_gpus = extracted_info.get('hardware', {}).get('num_gpus', 'NOT FOUND')
    has_compute_base = clean_flags.get('tiene_compute_base', False)
    stats_signal = (
        f"DETECTED compute -> training_time: {gpu_hours}, num_gpus: {num_gpus}, has_compute_base: {has_compute_base}. "
        "If training required significant compute (100+ GPU-hours, or 8+ GPUs for long runs, or mentions 1B+ parameters / 1T+ tokens), "
        "the absence of multiple statistical runs is IMPLICITLY JUSTIFIED -> set is_no_justified: true "
        "and explain in justification field."
    )

    # Signal for Item 3: Theory and Proofs (Empirical papers)
    has_theory = extracted_info.get('theory_and_proofs', {}).get('has_theoretical_results', 'no')
    theory_signal = (
        f"DETECTED theory -> {has_theory}. "
        "If the paper is primarily empirical (proposing an architecture, benchmark, or system) and does NOT "
        "claim new theorems, answer 'N/A' or 'No' with is_no_justified: true. "
        "NeurIPS does NOT require proofs for purely empirical contributions."
    )

    # Signal for Item 8: Compute Resources
    compute_signal = (
        f"DETECTED -> compute_time: {gpu_hours}, has_compute_base: {has_compute_base}. "
        "If the author provides the model size (e.g., 7B, 70B parameters) and dataset size (e.g., 2T tokens), "
        "this counts as providing the base for compute estimation -> answer 'Yes'."
    )

    # Signal for Item 12: whether external assets were used and if licenses were named
    assets_used = extracted_info.get('licenses_extraction', {}).get('assets_used', [])
    licenses_named = extracted_info.get('licenses_extraction', {}).get('licenses_named', [])
    has_external_assets = bool(assets_used and assets_used not in [[], ['NOT FOUND'], ['list of datasets/code']])
    licenses_signal = (
        f"DETECTED -> assets_used: {assets_used}, licenses_named: {licenses_named}, "
        f"has_external_assets (computed): {has_external_assets}. "
        "RULE: If has_external_assets is False -> answer N/A. "
        "If has_external_assets is True but specific licenses (e.g., MIT, CC-BY) are NOT explicitly named -> answer 'No' and set justification to: 'Falta de transparencia: Se usan activos externos pero no se especifican sus licencias.'. "
        "If license names are explicitly stated -> answer Yes with evidence."
    )

    # Signal for Item 14: was crowdsourcing/human subjects actually used?
    uses_crowd = clean_flags.get('usa_crowdsourcing', False)
    human_annotation = extracted_info.get('human_subjects_extraction', {}).get('uses_human_annotation', 'no')
    compensation_details = extracted_info.get('human_subjects_extraction', {}).get('compensation_details', 'NOT FOUND')
    crowdsourcing_signal = (
        f"DETECTED -> regex_crowdsourcing_flag: {uses_crowd}, uses_human_annotation: {human_annotation}, compensation_details: {compensation_details}. "
        "STRICT RULE: If both flags are false/no, the paper does NOT involve human subjects -> answer MUST be N/A. "
        "If human annotation or crowdsourcing is detected, you MUST look for compensation terms (wage, paid, salary, compensation). "
        "If compensation is missing or 'NOT FOUND', answer 'No' and set justification EXACTLY to: 'Riesgo Ético: Has declarado uso de humanos pero no has detallado su compensación económica según el Código de Ética de NeurIPS'."
    )

    # Signal for Item 15: IRB Approvals
    irb_signal = (
        f"DETECTED -> uses_human_annotation: {human_annotation}. "
        "STRICT RULE: If human annotators or crowdsourcing are used, the system MUST require a mention of an 'Institutional Review Board' (IRB) or ethics committee. "
        "If there is no trace of IRB approval, you MUST answer 'No' and state 'Riesgo de Desk Reject: Faltan aprobaciones del comité de ética (IRB).' in the justification."
    )

    # Signal for Item 6: Hyperparameters (Inference)
    hyper_vague = extracted_info.get('hyperparameters', {}).get('vague_phrase', 'NOT FOUND')
    hyper_signal = (
        f"DETECTED vague_phrase: {hyper_vague}. "
        "IMPORTANT: If the author states that hyperparameters follow 'default values', 'standard settings', "
        "or 'previous work (e.g. Qwen2)', this counts as a valid justification for Item 6. "
        "Also, total tokens (e.g. 3.5T) or optimization steps (e.g. 100k steps) count as valid training duration (Item 6)."
    )

    # Signal for Item 16: Declaration of LLM Usage (The Negative Declaration Rule)
    has_llm_section = clean_flags.get('tiene_seccion_declaracion', False)
    has_llm_negative = clean_flags.get('tiene_declaracion_negativa', False)
    has_llm_positive = bool(extracted_info.get('llm_usage_extraction', {}).get('models_used', []))
    llm_signal = (
        f"DETECTED -> has_explicit_section: {has_llm_section}, has_negative_declaration: {has_llm_negative}, has_positive_usage: {has_llm_positive}. "
        "RULE: Authors MUST include a 'Declaration of LLM Usage' (either positive or negative). "
        "If NO traces of such declaration are found (neither section nor explicit sentence) -> answer 'No' "
        "and use justification: 'El documento no contiene la sección obligatoria de declaración de uso de LLMs, lo cual es un incumplimiento de las guías de autor de NeurIPS.'."
    )

    return f"""
Act as a Senior Area Chair for NeurIPS 2026. Your task is to VALIDATE the transparency of the NeurIPS 2026 Paper Checklist.
DO NOT produce any numeric score. Your output is a transparency audit, not a grade.

EXTRACTED INFORMATION:
{json.dumps(extracted_info, indent=2, ensure_ascii=False)}

RED FLAGS (automated regex pre-processing):
{json.dumps(clean_flags, indent=2)}

=======================================================
PRE-COMPUTED SIGNALS - USE THESE TO AVOID COMMON ERRORS
=======================================================
[Item 3 - Theory]           {theory_signal}
[Item 4 - Reproducibility]   {reproducibility_signal}
[Item 5 - Open Access]       {open_access_signal}
[Item 7 - Statistics]        {stats_signal}
[Item 8 - Compute]           {compute_signal}
[Item 12 - Licenses]         {licenses_signal}
[Item 14 - Crowdsourcing]    {crowdsourcing_signal}
[Item 15 - IRB Approvals]    {irb_signal}
[Item 6 - Hyperparameters]   {hyper_signal}
[Item 16 - LLM Declaration]  {llm_signal}

=======================================================
OUTPUT RULES - MANDATORY FOR ALL 16 ITEMS
=======================================================
For every item:
- "answer" MUST be exactly one of: "Yes", "No", or "N/A" (never anything else).
- If "Yes" -> "evidence" MUST contain the paper section or a verbatim fragment (e.g. "See Section 3.2"). NEVER leave evidence blank for a Yes.
- If "No"  -> set "is_no_justified": true ONLY if the authors explicitly justified it OR the pre-computed signal above grants implicit justification.
- If "N/A" -> "justification" must briefly state why it does not apply.

=======================================================
CRITICAL PER-ITEM RULES
=======================================================
Item 2 (Limitations):
  NeurIPS EXPLICITLY INSTRUCTS reviewers NOT to penalize honesty about limitations.
  If ANY limitations are stated -- even briefly -- answer "Yes". Only "No" if LITERALLY NO limitations section exists.

Item 3 (Theory, Assumptions & Proofs):
  Use the [Item 3 - Theory] pre-computed signal. If the work is empirical, do not penalize the absence of proofs.
  Answer "N/A" or "No" with is_no_justified: true.

Item 4 (Experimental Result Reproducibility):
  NeurIPS accepts MULTIPLE reproducibility forms. Any of these count as "Yes":
  demo page, hosted model, GitHub repo, model checkpoint, HuggingFace model, detailed architecture description.
  Use the [Item 4] pre-computed signal. If any public URL is present, answer "Yes" unless paper explicitly restricts all access.

Item 5 (Open Access to Data and Code):
  Use the [Item 5 - Open Access] pre-computed signal EXACTLY.
  If ANY public URL exists (project page, demo, HuggingFace, GitHub) OR the author explicitly promises future release (e.g., "we will release code") -> answer "Yes" with that evidence.
  NeurIPS considers a demo page, model card, or a commitment to release as valid forms of transparency.

Item 8 (Experiments Compute Resource):
  Use the [Item 8 - Compute] pre-computed signal.
  Providing model size and token counts is sufficient for compute estimation. Answer "Yes" if these are present.

Item 6 (Experimental Setting / Details):
  Use the [Item 6 - Hyperparameters] pre-computed signal.
  Do NOT penalize for missing specific values if the author states they use "default values" of a known optimizer (like AdamW) or follow a cited previous work.
  Training duration can be expressed in epochs, optimization steps, or total tokens. Any of these count as "Yes".

Item 7 (Statistical Significance):
  Search for error bars, +/-values, confidence intervals in results. If none found, answer "No".
  Use the [Item 7] pre-computed signal for is_no_justified decision.

Item 12 (Licenses):
  Use the [Item 12 - Licenses] pre-computed signal EXACTLY as instructed.

Item 14 (Crowdsourcing and Human Subjects):
  Use the [Item 14 - Crowdsourcing] pre-computed signal EXACTLY as instructed. 

Item 15 (IRB Approvals):
  Use the [Item 15 - IRB Approvals] pre-computed signal EXACTLY as instructed.

Item 16 (Declaration of LLM Usage):
  Use the [Item 16 - LLM Declaration] pre-computed signal EXACTLY.
  It is NOT enough to assume No usage if not mentioned. A declaration (positive or negative) MUST be present.
  If missing -> answer "No" with the administrative justification provided in the signal.

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
