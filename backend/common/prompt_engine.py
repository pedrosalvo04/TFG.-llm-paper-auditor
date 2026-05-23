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

def get_extraction_prompt(paper_text: str) -> str:
    """Prompt monolítico (legacy/fallback)."""
    template = load_prompt("auditor", "extraction")
    
    return render_prompt(template,
        snippets_section="", 
        flags_section="",
        paper_text=paper_text
    )

def get_map_extraction_prompt(fragment_text: str) -> str:
    """Prompt para la fase MAP del analisis general."""
    template = load_prompt("auditor", "1. map_extraction")
    return render_prompt(template, fragment_text=fragment_text)

def get_reduce_extraction_prompt(map_results: list) -> str:
    """Prompt para la fase REDUCE del analisis general."""
    template = load_prompt("auditor", "2. reduce_extraction")
    return render_prompt(template, map_results=json.dumps(map_results, indent=2))

def get_extraction_assistance_helps(info: dict) -> dict:
    """
    Convierte el JSON de extracción de la Fase 1 en pequeñas ayudas (helps)
    para el evaluador de la Fase 2. No es un prompt final, sino fragmentos inyectables.
    """
    helps = {}
    
    # Aseguramos que info sea un diccionario
    if not isinstance(info, dict):
        info = {}

    def safe_get(obj, key, default_val=None):
        if not isinstance(obj, dict):
            return default_val
        return obj.get(key, default_val)

    def find_urls(obj):
        urls = []
        if isinstance(obj, str):
            import re
            # Regex robusto que incluye URLs con y sin protocolo (comunes en papers)
            found = re.findall(r'(?:https?://|www\.)(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:\S+)?', obj)
            # Casos especiales de dominios de investigación comunes si no tienen protocolo
            found.extend(re.findall(r'\b(?:github\.com|huggingface\.co|arxiv\.org|gitlab\.com)/\S+', obj))
            
            # Limpiar URLs de caracteres de puntuación final
            urls.extend([u.rstrip('.,;)]') for u in found])
        elif isinstance(obj, list):
            for item in obj:
                urls.extend(find_urls(item))
        elif isinstance(obj, dict):
            for value in obj.values():
                urls.extend(find_urls(value))
        return list(set(urls))

    def search_globally(obj, keywords):
        content = str(obj).lower()
        return any(k.lower() in content for k in keywords)

    # Búsqueda global de URLs y señales críticas
    all_urls = find_urls(info)
    url_str = ", ".join(all_urls) if all_urls else "NOT FOUND"
    info_str_lower = str(info).lower()
    
    # 1. REPRODUCIBILIDAD (ITEM 4)
    # Búsqueda global de pesos/checkpoints (no solo en architecture)
    weights_keywords = ['weights', 'checkpoint', 'huggingface', 'download', 'checkpoints', 'model card', 'available at']
    weights = 'yes' if search_globally(info, weights_keywords) else 'no'
    
    helps['reproducibility'] = (
        f"CODE/MODEL URLS: {url_str}. WEIGHTS: {weights}. "
        "NeurIPS Rule: If ANY code/model URL is present, answer 'Yes'. "
        "If NO code/URL is found, answer 'No' and set is_no_justified: false."
    )
    
    # 2. OPEN ACCESS (ITEM 5)
    helps['open_access'] = (
        f"DATA/RESOURCE URLS: {url_str}. "
        "If ANY public URL (project, demo, HF, github) exists -> 'Yes'. "
        "If only private/proprietary mentioned -> 'No' and set is_no_justified: true ONLY if they explain why."
    )
    
    # 3. ESTADÍSTICA (ITEM 7)
    # Búsqueda más agresiva de símbolos estadísticos
    ci_keywords = ['confidence interval', '±', 'std dev', 'standard deviation', 'error bars', 'variance', 'uncertainty']
    st_keywords = ['p-value', 'significant', 't-test', 'wilcoxon', 'statistical significance', 'p <', 'p=']
    
    ci = 'yes' if any(x in info_str_lower for x in ci_keywords) else 'no'
    st = 'yes' if any(x in info_str_lower for x in st_keywords) else 'no'
    
    stats_data = safe_get(info, 'statistics', {})
    runs = safe_get(stats_data, 'num_runs', 'NOT FOUND')
    
    hyperparams = safe_get(info, 'hyperparameters', {})
    is_greedy = search_globally(hyperparams, ['greedy']) or search_globally(info_str_lower, ['deterministic decoding', 'greedy search'])
    
    greedy_note = " (DETERMINISTIC: Greedy decoding detected. Results are likely deterministic zero-shot benchmarks.)" if is_greedy else ""
    
    helps['statistics'] = (
        f"CI/Variance: {ci}, Significance Tests: {st}, Runs: {runs}.{greedy_note} "
        "Rule: If NO intervals/variance/runs found -> answer 'No' and set is_no_justified: false. "
        "EXCEPTIONAL RULE: For deterministic LLM benchmarks, 'Yes' is acceptable if greedy decoding is used."
    )
    
    # 4. RECURSOS (ITEM 8)
    hw = safe_get(info, 'hardware', {})
    hw_str = str(hw) if hw else "NOT FOUND"
    co2_keywords = ['co2', 'carbon', 'emission', 'tco2eq', 'power consumption', 'energy usage', 'watt']
    co2_found = search_globally(info, co2_keywords)
    co2_note = " (ENVIRONMENTAL DATA DETECTED: CO2 emissions or carbon footprint mentioned.)" if co2_found else ""
    
    efficiency_keywords = ['efficiency', 'latency', 'throughput', 'samples per second', 'ms/token', 'tokens/sec', 'runtime']
    efficiency_found = search_globally(info, efficiency_keywords)
    efficiency_note = " (EFFICIENCY METRIC DETECTED: Per-sample runtime or latency found.)" if efficiency_found else ""

    helps['compute_resource'] = (
        f"DETECTED hardware/cluster: {hw_str}.{co2_note}{efficiency_note} "
        "CRITICAL RULE FOR ITEM 8: If ANY hardware, cluster, or CO2 emissions are mentioned -> answer 'Yes'. "
        "If hardware is mentioned but BOTH time and efficiency/CO2 are missing -> 'No'."
    )
    
    # 5. LICENSES (ITEM 12)
    lic_found = []
    lic_keywords = {
        'mit': 'MIT', 'apache': 'Apache', 'creative commons': 'CC', 'cc-by': 'CC', 
        'openrail': 'OpenRAIL', 'bsd': 'BSD', 'gpl': 'GPL', 'allenai': 'AllenAI License'
    }
    
    for k, v in lic_keywords.items():
        if k in info_str_lower:
            lic_found.append(v)
    lic_found = list(set(lic_found))

    helps['licenses'] = (
        f"LICENSES FOUND: {lic_found}. "
        "Rule: If NO specific license (MIT, Apache, CC) is named -> answer 'No' and set is_no_justified: false."
    )
    
    # 6. CROWDSOURCING (ITEM 14)
    human_datasets = [
        'ultrafeedback', 'wildchat', 'preference data', 'rlhf', 'human feedback', 
        'crowdsourcing', 'mturk', 'prolific', 'annotators', 'human evaluators'
    ]
    uses_human_data = search_globally(info, human_datasets)
    
    crowd = safe_get(info, 'human_subjects_extraction', {})
    # Unificar detección
    detected_human = (safe_get(crowd, 'uses_human_annotation') == 'yes') or uses_human_data
    uses_human_flag = 'yes' if detected_human else 'no'
    comp = safe_get(crowd, 'compensation_details', 'NOT FOUND')
    
    helps['crowdsourcing'] = (
        f"USES HUMAN/PREFERENCE DATA: {uses_human_flag}, COMP: {comp}. "
        "Rule: If human-derived data (RLHF, Ultrafeedback) is used, Items 14/15 MUST be addressed (Yes/No). "
        "N/A is ONLY for purely algorithmic papers with NO human data interaction."
    )
    
    return helps

def get_section_mapping_prompt(section_titles: list) -> str:
    """Genera el prompt para mapear títulos de secciones a items de alto contexto."""
    template = load_prompt("auditor", "3a. section_mapping")
    return render_prompt(template, section_titles="\n".join(f"- {title}" for title in section_titles))


def load_item_rule(item_key: str) -> str:
    """
    Carga la regla de un item desde su archivo .md individual en item_rules/.
    Devuelve string vacío si el archivo no existe (item sin regla específica).
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rule_path = os.path.join(base_dir, "prompts", "auditor", "item_rules", f"{item_key}.md")
    try:
        with open(rule_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def get_evaluation_high_context_prompt(extracted_info: dict, items_to_evaluate: list, mapped_sections_text: str, criteria_literal_text: str = "") -> str:
    """Genera el prompt para items de alto contexto.
    Inyecta dinámicamente SOLO las reglas de los items del batch actual,
    cargadas desde backend/prompts/auditor/item_rules/<item>.md."""
    template = load_prompt("auditor", "3c. evaluation_high_context")

    helps = get_extraction_assistance_helps(extracted_info)

    # Cargar y concatenar SOLO las reglas de los 2 items de este batch
    per_item_rules = "\n\n".join(
        rule for item in items_to_evaluate
        if (rule := load_item_rule(item))
    )

    return render_prompt(template,
        items_to_evaluate=json.dumps(items_to_evaluate, indent=2),
        extracted_info_json=json.dumps(extracted_info, indent=2, ensure_ascii=False),
        mapped_sections_text=mapped_sections_text,
        criteria_literal_text=criteria_literal_text,
        per_item_rules=per_item_rules,
        reproducibility_help=helps.get('reproducibility', ''),
        open_access_help=helps.get('open_access', ''),
        statistics_help=helps.get('statistics', ''),
        compute_resource_help=helps.get('compute_resource', ''),
        licenses_help=helps.get('licenses', ''),
        crowdsourcing_help=helps.get('crowdsourcing', '')
    )



# =======================================================
# SOTA PROMPTS
# =======================================================

def get_thematic_coverage_prompt(paper_text: str) -> str:
    """Prompt para identificar subtemas, áreas técnicas y año del paper."""
    template = load_prompt("sota", "1. thematic")
    return render_prompt(template,
        paper_text_start=paper_text[:15000],
        paper_text_end=paper_text[-5000:]
    )

def get_query_generation_prompt(subtemas_str: str, areas_str: str, paper_text: str) -> str:
    """Prompt para generar queries de búsqueda especializadas."""
    template = load_prompt("sota", "2. query_generation")
    return render_prompt(template,
        subtemas_str=subtemas_str,
        areas_str=areas_str,
        paper_text_snippet=paper_text[:8000]
    )

def get_coverage_gap_prompt(paper_text: str, subtemas_str: str) -> str:
    """Prompt para analizar gaps de cobertura bibliográfica."""
    template = load_prompt("sota", "3. gap_analysis")
    return render_prompt(template,
        subtemas_str=subtemas_str,
        paper_text_start=paper_text[:5000],
        paper_text_refs=paper_text[-10000:]
    )

def get_cross_validation_prompt(paper_text: str, sota_context: str, subtemas_str: str) -> str:
    """Prompt para validación cruzada y detección de omisiones."""
    template = load_prompt("sota", "4. cross_validation")
    return render_prompt(template,
        paper_text_start=paper_text[:5000],
        paper_text_refs=paper_text[-15000:],
        subtemas_str=subtemas_str,
        sota_context=sota_context
    )
