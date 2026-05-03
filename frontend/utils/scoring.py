"""Utilidades para cálculo de puntuaciones con sistema híbrido de penalizaciones"""


def calcular_puntuacion(peer_review_scores, red_flags=None, evaluation=None):
    """
    Calcula puntuación basada en los prestigiosos criterios de NeurIPS.
    Prioriza el Overall Score del LLM sobre las penalizaciones por micro-detalles.
    """
    if not peer_review_scores:
        return 0, {"score_base": 0, "penalizaciones": [], "bonificaciones": [], "total_penalizaciones": 0}
    
    # Convertir a int si vienen como string
    def safe_int(value, default=0):
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default
    
    # --- ANCLA NEURIPS: Overall Score (1-10) ---
    overall_score_raw = peer_review_scores.get('overall_score', {})
    overall_val = safe_int(overall_score_raw.get('score', 0))
    
    # El Score Base viene directamente del veredicto del revisor (NeurIPS scale 1-10)
    # 10 -> 100%, 8 -> 80%, 5 -> 50%, etc.
    score_base = overall_val * 10
    
    # Sub-criterios para el desglose visual
    soundness = safe_int(peer_review_scores.get('soundness', {}).get('score', 0))
    presentation = safe_int(peer_review_scores.get('presentation', {}).get('score', 0))
    contribution = safe_int(peer_review_scores.get('contribution', {}).get('score', 0))
    
    penalizaciones = []
    bonificaciones = []
    
    # ===== PENALIZACIONES CRÍTICAS (SOLO LO REALMENTE GRAVE) =====
    if red_flags:
        # Solo penalizamos si NO hay sección de limitaciones (Requisito NeurIPS)
        if not red_flags.get('tiene_seccion_limitaciones', True):
            penalizaciones.append(("Falta sección obligatoria de Limitaciones", -5))
            
        # Solo penalizamos si los datos son propietarios Y además no hay forma de verificarlos
        if red_flags.get('datos_propietarios') and red_flags.get('cannot_release_data'):
            penalizaciones.append(("Datos propietarios sin vía de verificación", -5))

    if evaluation:
        ethics = evaluation.get('ethics_flag', {})
        if isinstance(ethics, dict) and ethics.get('requires_ethics_review', '').strip().lower() == 'yes':
            penalizaciones.append(("Bandera ética activada (Requiere revisión)", -5))

    # ===== BONIFICACIONES POR EXCELENCIA CIENTÍFICA =====
    # Premiar la innovación real
    if contribution >= 4:
        bonificaciones.append(("Contribución excepcional / Paradigm-shifting", +10))
    elif contribution >= 3:
        bonificaciones.append(("Contribución sólida a la comunidad", +5))
    
    # Premiar la robustez técnica
    if soundness >= 4:
        bonificaciones.append(("Metodología técnica impecable", +5))
    
    # Si reporta hardware detallado o impacto ambiental (Buenas prácticas NeurIPS)
    if red_flags:
        if sum(1 for f in ['tiene_carbon_footprint', 'tiene_energy_consumption', 'tiene_pue'] if red_flags.get(f)) >= 1:
            bonificaciones.append(("Transparencia en impacto ambiental", +3))
        
        hw_detail_count = sum(1 for k in ['tiene_gpu_model', 'tiene_gpu_count', 'tiene_gpu_memory', 'tiene_training_time'] if red_flags.get(k))
        if hw_detail_count >= 2:
            bonificaciones.append(("Detalles de hardware completos", +2))

    # ===== CÁLCULO FINAL =====
    total_penalizaciones = sum(p[1] for p in penalizaciones)
    total_bonificaciones = sum(b[1] for b in bonificaciones)
    
    score_final = score_base + total_penalizaciones + total_bonificaciones
    score_final = max(0, min(100, round(score_final, 1)))
    
    desglose = {
        "score_base": round(score_base, 1),
        "penalizaciones": penalizaciones,
        "bonificaciones": bonificaciones,
        "total_penalizaciones": total_penalizaciones,
        "total_bonificaciones": total_bonificaciones,
        "scores_llm": {
            "soundness": soundness,
            "presentation": presentation,
            "contribution": contribution
        }
    }
    
    return score_final, desglose


def _apply_extracted_info_penalties(extracted_info, penalizaciones):
    """
    Aplica penalizaciones reducidas basadas en la información extraída.
    """
    def is_missing(value):
        if not value or not isinstance(value, str): return True
        return value.strip().lower() in ('not found', 'n/a', 'none', '')
    
    def is_problematic(value):
        if not value or not isinstance(value, str): return False
        problematic_terms = ['proprietary', 'confidential', 'cannot release', 'internal']
        return any(term in value.strip().lower() for term in problematic_terms)
    
    hp_info = extracted_info.get('hyperparameters', {})
    if isinstance(hp_info, dict):
        hp_missing = sum(1 for f in ['optimizer', 'learning_rate', 'batch_size', 'epochs', 'warmup', 'weight_decay', 'betas', 'epsilon'] if is_missing(hp_info.get(f, '')))
        if hp_missing >= 6:
            penalizaciones.append((f"Faltan muchos hiperparámetros (LLM)", -2))
    
    data_info = extracted_info.get('data', {})
    if isinstance(data_info, dict):
        if is_problematic(data_info.get('access_url', '')) or is_problematic(data_info.get('negative_phrase', '')):
            penalizaciones.append(("Datos marcados como propietarios (LLM)", -3))
            
    code_info = extracted_info.get('code', {})
    if isinstance(code_info, dict):
        if is_problematic(code_info.get('negative_phrase', '')) or is_problematic(code_info.get('repository_url', '')):
            penalizaciones.append(("Código con restricciones de acceso (LLM)", -3))
            
    problematic = extracted_info.get('problematic_phrases', [])
    if isinstance(problematic, list) and len(problematic) > 0:
        real_problems = [p for p in problematic if isinstance(p, str) and not is_missing(p)]
        if len(real_problems) >= 2:
            penalizaciones.append(("Frases problemáticas (propietario/confidencial)", -2))
