"""
Sistema de gestión de prompts modular (Prompt Engine).
Carga las plantillas desde archivos .md en backend/prompts/
"""
import os
import json

def load_prompt(category: str, filename: str) -> str:
    """
    Carga un prompt desde un archivo .md.
    
    Args:
        category: Subcarpeta (auditor, chatbot, rag, sota)
        filename: Nombre del archivo (sin .md)
    """
    # Ruta absoluta al directorio de prompts (backend/prompts)
    # asumiendo que este script está en backend/common/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", category, f"{filename}.md")
    
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback o log error
        raise FileNotFoundError(f"Prompt no encontrado en: {prompt_path}")

def render_prompt(template: str, **kwargs) -> str:
    """
    Interpola variables en el template usando .replace() en lugar de .format()
    para evitar conflictos con llaves literales en JSON/Markdown.
    """
    for key, value in kwargs.items():
        placeholder = f"{{{key}}}"
        template = template.replace(placeholder, str(value))
    return template

# =======================================================
# AUDITOR PROMPTS
# =======================================================

def get_extraction_prompt(paper_text: str, red_flags: dict) -> str:
    """Prompt monolítico (legacy/fallback)."""
    template = load_prompt("auditor", "extraction")
    
    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')} if red_flags else {}
    flags_section = ""
    if clean_flags:
        flags_section = f"\nRED FLAGS DETECTED BY REGEX PRE-PROCESSING:\n{json.dumps(clean_flags, indent=2)}\n"
        
    return render_prompt(template,
        snippets_section="", 
        flags_section=flags_section,
        paper_text=paper_text
    )

def get_map_extraction_prompt(fragment_text: str) -> str:
    """Prompt para la fase MAP del analisis general."""
    template = load_prompt("auditor", "map_extraction")
    return render_prompt(template, fragment_text=fragment_text)

def get_reduce_extraction_prompt(map_results: list) -> str:
    """Prompt para la fase REDUCE del analisis general."""
    template = load_prompt("auditor", "reduce_extraction")
    return render_prompt(template, map_results=json.dumps(map_results, indent=2))

def get_evaluation_signals(info: dict) -> dict:
    """
    Lógica de señales de cumplimiento para el auditor.
    Esta función NO es un prompt, sino lógica auxiliar que se queda en Python.
    """
    signals = {}
    
    # Aseguramos que info sea un diccionario
    if not isinstance(info, dict):
        info = {}

    def safe_get(obj, key, default_val=None):
        """Helper para obtener valores de forma segura si obj no es un dict."""
        if not isinstance(obj, dict):
            return default_val
        return obj.get(key, default_val)

    # 1. REPRODUCIBILIDAD (ITEM 4)
    code_data = safe_get(info, 'code', {})
    code_url = safe_get(code_data, 'repository_url', 'NOT FOUND')
    
    arch_data = safe_get(info, 'architecture', {})
    weights = safe_get(arch_data, 'weights_available', 'no')
    
    signals['reproducibility'] = (
        f"CODE FOUND: {code_url}. WEIGHTS: {weights}. "
        "NeurIPS Rule: If ANY code/model URL is present, answer 'Yes'. "
        "If NO code/URL is found, answer 'No' and set is_no_justified: false."
    )
    
    # 2. OPEN ACCESS (ITEM 5)
    data_info = safe_get(info, 'data', {})
    data_url = safe_get(data_info, 'access_url', 'NOT FOUND')
    signals['open_access'] = (
        f"DATA URL: {data_url}. "
        "If ANY public URL (project, demo, HF, github) exists -> 'Yes'. "
        "If only private/proprietary mentioned -> 'No' and set is_no_justified: true ONLY if they explain why."
    )
    
    # 3. ESTADÍSTICA (ITEM 7)
    stats = safe_get(info, 'statistics', {})
    ci = safe_get(stats, 'confidence_intervals', 'no')
    st = safe_get(stats, 'significance_tests', 'no')
    runs = safe_get(stats, 'num_runs', 'NOT FOUND')
    signals['statistics'] = (
        f"CI: {ci}, TESTS: {st}, RUNS: {runs}. "
        "Rule: If NO intervals/variance/runs found -> answer 'No' and set is_no_justified: false."
    )
    
    # 4. RECURSOS (ITEM 8)
    hw = safe_get(info, 'hardware', {})
    hw_summary = f"{safe_get(hw, 'gpu_cpu', 'NOT FOUND')} x {safe_get(hw, 'num_gpus', 'NOT FOUND')}"
    time = safe_get(hw, 'time', 'NOT FOUND')
    signals['compute_resource'] = (
        f"DETECTED hardware/cluster: {hw_summary}. "
        "CRITICAL RULE FOR ITEM 8: "
        "If ANY hardware, internal cluster (e.g., 'Compute Canada', 'Calcul Québec'), or cloud provider is mentioned -> answer 'Yes' for the resource part. "
        "If total training time is ALSO mentioned -> 'Yes' with full evidence. "
        "If ONLY cluster/hardware is mentioned but NOT time -> answer 'No' but set is_no_justified: false, "
        "and EXPLICITLY MENTION the cluster found in the justification so the user knows it was detected but is insufficient."
    )
    
    # 5. LICENCIAS (ITEM 12)
    lic = safe_get(info, 'licenses_extraction', {})
    lic_found = safe_get(lic, 'licenses_named', [])
    signals['licenses'] = (
        f"LICENSES FOUND: {lic_found}. "
        "Rule: If NO specific license (MIT, Apache, CC) is named -> answer 'No' and set is_no_justified: false."
    )
    
    # 6. CROWDSOURCING (ITEM 14)
    crowd = safe_get(info, 'human_subjects_extraction', {})
    uses_human = safe_get(crowd, 'uses_human_annotation', 'no')
    comp = safe_get(crowd, 'compensation_details', 'NOT FOUND')
    signals['crowdsourcing'] = (
        f"USES HUMAN: {uses_human}, COMP: {comp}. "
        "Rule: If NOT using humans/crowds -> 'N/A'. "
        "If using humans but NO compensation mentioned -> 'No' and set is_no_justified: false."
    )
    
    return signals

def get_evaluation_prompt(extracted_info: dict, red_flags: dict) -> str:
    """Genera el prompt para evaluacion segun criterios NeurIPS 2026."""
    template = load_prompt("auditor", "evaluation")
    
    clean_flags = {k: v for k, v in red_flags.items() if not k.startswith('_')} if red_flags else {}
    flags_section = ""
    if clean_flags:
        flags_section = f"\nRED FLAGS (automated regex pre-processing):\n{json.dumps(clean_flags, indent=2)}\n"

    signals = get_evaluation_signals(extracted_info)

    return render_prompt(template,
        extracted_info_json=json.dumps(extracted_info, indent=2, ensure_ascii=False),
        flags_section=flags_section,
        reproducibility_signal=signals['reproducibility'],
        open_access_signal=signals['open_access'],
        statistics_signal=signals['statistics'],
        compute_resource_signal=signals['compute_resource'],
        licenses_signal=signals['licenses'],
        crowdsourcing_signal=signals['crowdsourcing']
    )

def get_verification_prompt(item_key: str, item_data: dict, paper_context: str) -> str:
    """Prompt para la fase de 'Auditor Estricto' (Self-Correction)."""
    template = load_prompt("auditor", "verification")
    
    answer = item_data.get('answer', 'N/A')
    justification = item_data.get('justification', '')
    evidence = item_data.get('evidence', '')
    
    return render_prompt(template,
        item_key=item_key,
        answer=answer,
        justification=justification,
        evidence=evidence,
        paper_context=paper_context
    )

# =======================================================
# CHATBOT PROMPTS
# =======================================================

def get_chatbot_response_prompt(paper_text: str, question: str, history_text: str) -> str:
    """Genera el prompt para la respuesta del chatbot."""
    template = load_prompt("chatbot", "conversational")
    return render_prompt(template,
        paper_text=paper_text,
        history_text=history_text,
        question=question
    )

# =======================================================
# RAG PROMPTS
# =======================================================

def get_rag_map_extraction_prompt(chunk: str) -> str:
    """Prompt para la fase MAP de extracción híbrida RAG."""
    template = load_prompt("rag", "map_triage")
    return render_prompt(template, chunk=chunk)

def get_rag_reduce_extraction_prompt(extracted_fragments: list) -> str:
    """Prompt para la fase REDUCE de extracción híbrida RAG."""
    template = load_prompt("rag", "reduce_triage")
    return render_prompt(template, extracted_fragments=json.dumps(extracted_fragments, indent=2))

# =======================================================
# SOTA PROMPTS
# =======================================================

def get_thematic_coverage_prompt(paper_text: str) -> str:
    """Prompt para identificar subtemas, áreas técnicas y año del paper."""
    template = load_prompt("sota", "thematic")
    return render_prompt(template,
        paper_text_start=paper_text[:15000],
        paper_text_end=paper_text[-5000:]
    )

def get_query_generation_prompt(subtemas_str: str, areas_str: str, paper_text: str) -> str:
    """Prompt para generar queries de búsqueda especializadas."""
    template = load_prompt("sota", "query_generation")
    return render_prompt(template,
        subtemas_str=subtemas_str,
        areas_str=areas_str,
        paper_text_snippet=paper_text[:8000]
    )

def get_coverage_gap_prompt(paper_text: str, subtemas_str: str) -> str:
    """Prompt para analizar gaps de cobertura bibliográfica."""
    template = load_prompt("sota", "gap_analysis")
    return render_prompt(template,
        subtemas_str=subtemas_str,
        paper_text_start=paper_text[:5000],
        paper_text_refs=paper_text[-10000:]
    )

def get_cross_validation_prompt(paper_text: str, sota_context: str, subtemas_str: str) -> str:
    """Prompt para validación cruzada y detección de omisiones."""
    template = load_prompt("sota", "cross_validation")
    return render_prompt(template,
        paper_text_start=paper_text[:5000],
        paper_text_refs=paper_text[-15000:],
        subtemas_str=subtemas_str,
        sota_context=sota_context
    )
