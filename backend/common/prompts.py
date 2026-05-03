"""Plantillas de prompts para el sistema de auditoría"""
import json

def get_extraction_prompt(paper_text: str, red_flags: dict) -> str:
    """
    Genera el prompt para la fase de extracción de información.
    Incluye snippets detectados por regex para que el LLM los valide.
    """
    # Extraer snippets de hiperparámetros para validación
    hp_snippets = red_flags.get('_hp_snippets', {})
    snippets_section = ""
    if hp_snippets:
        snippets_section = "\nREGEX-DETECTED SNIPPETS (VALIDATE THESE - some may be false positives):\n"
        for k, v in hp_snippets.items():
            snippets_section += f"  - {k}: \"{v}\" → Is this an actual reported value or a false positive?\n"

    # Filtrar claves internas del red_flags para el prompt
    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')}

    return f"""
CRITICAL: This system ONLY evaluates ML/AI papers (neural networks, deep learning, machine learning).

FIRST: Determine if this paper involves ML/AI training. If NO:
RETURN ONLY: {{"paper_type": "INVALID - Not ML/AI", "invalid_reason": "explanation"}}

If YES, continue with EXHAUSTIVE extraction below.

You are an expert information extractor for ML/AI papers. Your job is to extract
SPECIFIC factual information — not opinions — from every section of the paper.

ANALYSIS STRATEGY — Read the paper section by section:
1. Abstract + Introduction → claims, scope, contributions
2. Methods/Architecture → model details, design choices
3. Training/Optimization → hyperparameters, optimizer, schedule
4. Data → datasets, preprocessing, splits
5. Experiments/Results → baselines, metrics, tables
6. Implementation → code, hardware, software versions
7. Appendix → often contains hyperparameter tables, environmental data
8. Limitations/Broader Impact → quality and specificity

CRITICAL RULES:
- Search APPENDIX and ALL tables (Table 1 through Table 10+) before marking NOT FOUND
- Look specifically for "Data Availability Statement", "Dataset access", or URLs to model hubs (HuggingFace, etc.)
- If paper says "standard settings" or "not disclosed" → extract as vague_phrase, NOT as the actual value
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
  "problematic_phrases": ["textual quote 1", "textual quote 2"]
}}

PAPER TEXT:
{paper_text}
"""


def get_evaluation_prompt(extracted_info: dict, red_flags: dict) -> str:
    """
    Genera el prompt para evaluación según criterios NeurIPS 2025
    """
    # Filtrar claves internas
    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')}
    
    return f"""
Act as a Senior Area Chair for NeurIPS 2025. Apply official conference criteria with STRICT rigor.

EXTRACTED INFORMATION:
{json.dumps(extracted_info, indent=2, ensure_ascii=False)}

RED FLAGS (from automated regex pre-processing):
{json.dumps(clean_flags, indent=2)}

═══════════════════════════════════════════════════════
GUIDING SCORING PRINCIPLES (APPLY WITH CONTEXTUAL FAIRNESS)
═══════════════════════════════════════════════════════

BEFORE assigning ANY score, review the EXTRACTED INFORMATION above. 
Keep in mind that highly influential or foundational papers (like "Attention is All You Need", "ResNet", etc.) were written before modern 2024+ NeurIPS reproducibility checklists existed. DO NOT overly penalize older or clearly paradigm-shifting papers for missing GitHub links, specific hardware versions, or carbon footprints.

SOUNDNESS (1-4):
- Penalize if there is explicit overselling without evidence.
- Penalize if the methodology is fundamentally flawed.
- If data is proprietary, evaluate if there is a valid reason (e.g., medical data) before penalizing.

PRESENTATION (1-4):
- Consider missing CORE hyperparameters (LR, Optimizer, Batch, Epochs) as a weakness.
- Do NOT penalize for missing SECONDARY details like Random Seed, Betas, or Epsilon if the core setup is clear.
- Specifically for DISCRETE DIFFUSION / MASK-PREDICT (MDM) architectures, the lack of "betas" is expected and should NOT be considered a flaw.
- Do NOT penalize presentation if the paper mentions standard protocols/frameworks (e.g., "standard SFT protocols", "HuggingFace Transformers") even if specific version numbers are missing.
- Missing hardware specifics or software versions are minor omissions, not fatal flaws.
- Vague phrases ("standard settings") should reduce the score slightly, but not drastically if the architecture is clear.

CONTRIBUTION (1-4):
- For FOUNDATIONAL papers introducing new paradigms (e.g., new architectures, novel theoretical frameworks), focus on theoretical soundness over missing minor experimental details.
- Lack of open code/data reduces contribution slightly but does not invalidate a major conceptual breakthrough.

OVERALL_SCORE (1-10):
- 8-10: Excellent/Foundational papers. Can have minor omissions (e.g., no hardware details, some missing hyperparameters) if the core contribution is massive.
- 6-7: Strong papers, solid methodology, mostly reproducible.
- 5: Borderline, significant reproducibility gaps but decent ideas.
- 1-4: Reject, flawed methodology or entirely irreproducible without merit.
- DO NOT blindly cap the overall score just because `highly_reproducible` is "No". A paradigm-shifting paper can score 8-10 even if it lacks open code or exhaustive hyperparameters.

REPRODUCIBILITY evaluation:
- Code/Data "NOT FOUND" is negative, but evaluate the complexity of replicating from the math/architecture description.
- CORE hyperparameters (LR, Batch Size, Optimizer, Epochs) are MANDATORY for "highly_reproducible" = Yes.
- SECONDARY hyperparameters (Seed, Betas, Epsilon) are OPTIONAL and should NOT block a positive reproducibility evaluation.

LIMITATIONS QUALITY:
- Missing a dedicated "Limitations" section is a weakness, but check if limitations are discussed in the conclusion or experiments.

RECOMMENDATION:
- overall_score 8-10 → "Strong Accept" or "Accept"
- overall_score 6-7 → "Weak Accept"
- overall_score 5 → "Borderline"
- overall_score 4 → "Weak Reject"
- overall_score 1-3 → "Reject"

═══════════════════════════════════════════════════════
NEURIPS 2025 EVALUATION CRITERIA
═══════════════════════════════════════════════════════

1. CLAIMS AND SCOPE AUDIT:
   - Compare Abstract/Introduction claims with Experiments results and Appendix proofs
   - Does paper accurately reflect actual contributions?
   - Identify overselling: aspirational goals presented as achieved milestones
   - Check if scope exceeds experimental evidence or theoretical assumptions
   - Verify claims acknowledge specific settings (dataset constraints, hyperparameters)
   - CRITICAL: If paper claims to be "truly open" but data/code is proprietary → overselling_detected = "Yes"

2. LIMITATIONS AND SOCIAL IMPACT:
   - Assess 'Limitations' and 'Broader Impact' sections per NeurIPS 2025 Ethics Guidelines
   - Identify overlooked negative societal consequences: data privacy, algorithmic bias, security vulnerabilities
   - Evaluate upfront disclosure of failure modes
   - For facial recognition/medical data: check representativeness and consent protocols
   - Require 3 specific limitation points for soundness and transparency

3. THEORETICAL RIGOR AND ASSUMPTIONS:
   - Analyze mathematical formulations, theorems, lemmas in Section 3 and Technical Appendix
   - Verify all assumptions (convexity, Lipschitz constants, distribution types) explicitly stated
   - Assess proof sketch clarity for non-specialist readers
   - Ensure external theorems properly cited
   - Identify informal proofs lacking formal derivation in supplemental material

4. EXPERIMENTAL REPRODUCIBILITY:
   - Check NeurIPS Code and Data Submission Policy compliance
   - Verify: (1) error bar calculation methods (std dev vs std error); (2) computational resources and training time; (3) complete dependency list with versions
   - For new datasets: verify licensing and preservation plan (DOI, persistent URL)
   - If data is proprietary, check "Path to Verification": surrogate dataset or anonymous verification method
   - CRITICAL: If hyperparameters are in appendix (Table 5+), do NOT mark as missing
   - CRITICAL: If environmental data is in appendix (Table 6+), PRAISE transparency instead of requesting it
   - Assess if work is 'highly reproducible' per NeurIPS standards

5. ORIGINALITY VS SIGNIFICANCE (NeurIPS 2025 NEW):
   - Originality: Is the approach conceptually novel? New algorithm/architecture/theory?
   - Significance: Does it have practical/social impact? Unique datasets? Real-world applications?
   - A paper can be low originality but high significance (e.g., comprehensive benchmark with new data)
   - A paper can be high originality but low significance (e.g., theoretical result with no applications)

6. PEER REVIEW SIMULATION:
   - Apply the MANDATORY SCORE CEILINGS above
   - Evaluate: Soundness (1-4), Presentation (1-4), Contribution (1-4), Originality (1-4), Significance (1-4)
   - Check novelty vs concurrent work (>2 months ago)
   - Verify sufficient baseline comparisons
   - Assess figure/table clarity
   - Determine value to broader NeurIPS community

7. ETHICS FLAG (NeurIPS 2025 MANDATORY):
   - Data without consent or proper licensing?
   - Unmitigated algorithmic bias?
   - Dual-use concerns (military, surveillance)?
   - Environmental impact not disclosed?
   - CRITICAL: If carbon footprint + energy + PUE are reported → PRAISE transparency, do NOT flag
   - CRITICAL: If environmental data is in appendix (Table 6) → this is EXCELLENT, mention it positively
   - If YES to any concern, flag for Ethics Committee review

SCORING SCALE:
- 4: Excellent (ONLY if ALL information is complete, transparent, and highly reproducible)
- 3: Good (minor omissions, mostly complete)
- 2: Fair (significant omissions or transparency issues)
- 1: Poor (critical information missing, not reproducible)

CONFIDENCE SCALE (1-5):
- 5: Absolutely certain (expert in this exact subfield)
- 4: Quite sure (familiar with related work)
- 3: Moderately confident (general ML knowledge)
- 2: Somewhat uncertain (outside main expertise)
- 1: Pure guess (unfamiliar area)

CRITICAL RULES:
- If CORE hyperparameters (LR, Batch, Optimizer, Epochs) are present in either text or appendix, do NOT penalize presentation.
- FOUNDATIONAL papers should prioritize Contribution and Originality scores (aim for 4/4 if paradigm-shifting).
- "Restricted compute/budget" is NOT a reason to penalize code or ethics.
- A score of 4 in any category is reserved for truly excellent work, but 3 is solid and 2 should only be used for significant flaws.

RETURN JSON:
{{
  "self_written_summary": "Write a 3-sentence summary of the paper IN YOUR OWN WORDS. Do NOT copy the abstract. Explain: (1) What problem? (2) What solution? (3) What results?",
  "claims_scope_audit": {{
    "abstract_reflects_results": "Yes/No",
    "overselling_detected": "Yes/No",
    "overselling_examples": ["textual quote 1", "textual quote 2"],
    "scope_exceeds_evidence": "Yes/No",
    "specific_settings_acknowledged": "Yes/No",
    "suggestions": "Precise language improvements"
  }},
  "limitations_impact": {{
    "limitations_section_present": "Yes/No",
    "failure_modes_discussed": "Yes/No",
    "negative_consequences_identified": ["privacy risks", "bias", "security"],
    "representativeness_consent": "Yes/No/NA",
    "three_specific_limitations": ["limitation 1", "limitation 2", "limitation 3"]
  }},
  "theoretical_rigor": {{
    "assumptions_explicit": "Yes/No/NA",
    "proof_sketch_clarity": "1-4 or NA",
    "external_theorems_cited": "Yes/No/NA",
    "informal_proofs_without_formal": "Yes/No/NA",
    "assessment": "Technical soundness evaluation"
  }},
  "reproducibility": {{
    "error_bars_method": "Yes/No",
    "computational_resources": "Yes/No",
    "dependencies_versions": "Yes/No",
    "dataset_licensing": "Yes/No/NA",
    "path_to_verification": "Yes/No/NA (surrogate dataset or anonymous verification if proprietary)",
    "highly_reproducible": "Yes/No",
    "blocking_issues": ["issue 1", "issue 2"]
  }},
  "originality_significance": {{
    "originality_score": "1-4 (conceptual novelty)",
    "originality_justification": "Is the approach/algorithm/theory new?",
    "significance_score": "1-4 (practical/social impact)",
    "significance_justification": "Does it matter? Unique data? Real-world use?"
  }},
  "ethics_flag": {{
    "requires_ethics_review": "Yes/No",
    "concerns": ["data consent", "bias", "dual-use", "environmental"],
    "justification": "Why flagged or why not"
  }},
  "peer_review_scores": {{
    "soundness": {{
      "score": "1-4",
      "justification": "Technical quality, claims support, limitations honesty"
    }},
    "presentation": {{
      "score": "1-4",
      "justification": "Organization, reproducibility information, appendix completeness"
    }},
    "contribution": {{
      "score": "1-4",
      "justification": "Overall contribution (originality + significance)"
    }},
    "overall_score": {{
      "score": "1-10 (NeurIPS 2024 scale: 8=clear accept, 6=weak accept, 5=borderline, 3=reject)",
      "justification": "Aggregate score based on soundness, presentation, contribution, reproducibility"
    }}
  }},
  "summary_contributions": "Brief summary of paper contributions",
  "questions_for_authors": ["Actionable question 1 for rebuttal", "Actionable question 2 for rebuttal", "Actionable question 3 for rebuttal"],
  "recommendation": "Strong Accept/Accept/Weak Accept/Borderline/Weak Reject/Reject",
  "confidence": "1-5 (1=guess, 2=uncertain, 3=moderate, 4=sure, 5=expert)"
}}

⚠️ FINAL CHECKLIST (verify before responding):
1. Did I count NOT FOUND fields in extracted_info? 
2. Did I apply ALL mandatory score ceilings?
3. Did I check problematic_phrases for "cannot"/"proprietary"/"confidential"?
4. Is overall_score consistent with individual scores and reproducibility?
5. Is recommendation consistent with overall_score?
6. self_written_summary is in my own words, NOT copied from abstract?
7. A score of 4 is reserved ONLY for truly excellent, fully transparent papers?
8. questions_for_authors are actionable for rebuttal period?
- DO NOT ask for information that is already in appendix (Table 5, Table 6)
"""
