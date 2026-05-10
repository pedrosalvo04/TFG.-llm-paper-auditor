# -*- coding: utf-8 -*-
"""
Lógica de estado del checklist NeurIPS 2026.
Reemplaza el antiguo sistema de puntuación numérica.
El auditor ya no pone una nota: valida que cada ítem tenga respuesta + evidencia/justificación.
"""

CHECKLIST_KEYS = [
    "claims", "limitations", "theory_assumptions_proofs",
    "experimental_result_reproducibility", "open_access_data_code",
    "experimental_setting_details", "experiment_statistical_significance",
    "experiments_compute_resource", "code_of_ethics", "broader_impacts",
    "safeguards", "licenses", "assets", "crowdsourcing_human_subjects",
    "irb_approvals", "declaration_llm_usage"
]

CHECKLIST_LABELS = {
    "claims": "1. Claims",
    "limitations": "2. Limitations",
    "theory_assumptions_proofs": "3. Theory, Assumptions & Proofs",
    "experimental_result_reproducibility": "4. Experimental Result Reproducibility",
    "open_access_data_code": "5. Open Access to Data and Code",
    "experimental_setting_details": "6. Experimental Setting / Details",
    "experiment_statistical_significance": "7. Experiment Statistical Significance",
    "experiments_compute_resource": "8. Experiments Compute Resource",
    "code_of_ethics": "9. Code of Ethics",
    "broader_impacts": "10. Broader Impacts",
    "safeguards": "11. Safeguards",
    "licenses": "12. Licenses",
    "assets": "13. Assets",
    "crowdsourcing_human_subjects": "14. Crowdsourcing & Human Subjects",
    "irb_approvals": "15. IRB Approvals",
    "declaration_llm_usage": "16. Declaration of LLM Usage",
}


def get_checklist_health(evaluation: dict) -> dict:
    """
    Analiza el estado del checklist sin calcular ninguna puntuación numérica.

    Para cada ítem valida:
    - ¿Tiene respuesta (Yes/No/N/A)?
    - Si es "Yes" → ¿existe evidencia (sección o fragmento del paper)?
    - Si es "No" o "N/A" → ¿existe justificación del autor?

    Devuelve:
        {
          "status": "valid" | "risk",
          "items": [{ key, label, answer, evidence, justification,
                      needs_justification, pending_justification,
                      alert_msg }],
          "pending_count": int,
          "total": int,
        }
    """
    if not evaluation:
        return {
            "status": "risk",
            "items": [],
            "pending_count": 0,
            "total": 0,
        }

    items = []
    pending_count = 0

    for key in CHECKLIST_KEYS:
        val = evaluation.get(key, {})
        answer_raw = val.get("answer", "").strip()
        answer_norm = answer_raw.lower()
        justification = val.get("justification", "").strip()
        evidence = val.get("evidence", "").strip()
        is_no_justified_raw = val.get("is_no_justified", False)
        if isinstance(is_no_justified_raw, str):
            is_no_justified = is_no_justified_raw.lower() == "true"
        else:
            is_no_justified = bool(is_no_justified_raw)

        # --- Risk detection ---
        pending_justification = False
        missing_evidence = False
        alert_msg = ""

        if "yes" in answer_norm:
            # Yes → necesitamos la sección o evidencia del paper
            if not evidence and not justification:
                missing_evidence = True
                pending_count += 1
                alert_msg = "⚠️ Respuesta 'Yes' sin evidencia de sección del paper."
        elif "no" in answer_norm:
            # No → necesitamos justificación del autor
            if not is_no_justified or not justification:
                pending_justification = True
                pending_count += 1
                alert_msg = "🔴 'No' sin justificación del autor → Riesgo de Desk Reject."

            # Regla especial ítem 14: alerta de Código de Ética NeurIPS
            if key == "crowdsourcing_human_subjects" and not is_no_justified:
                alert_msg += " ⚠️ NeurIPS Code of Ethics: compensación mínima obligatoria."

        elif "n/a" in answer_norm or answer_norm == "":
            # N/A → aceptable si hay un mínimo de contexto
            if not justification and not evidence:
                # N/A sin nada es aceptable solo si el ítem no aplica; no lo marcamos como riesgo
                pass

        # Evidencia final a mostrar (priorizar el campo evidence, sino justification)
        display_evidence = evidence if evidence else justification if justification else "—"

        items.append({
            "key": key,
            "label": CHECKLIST_LABELS.get(key, key),
            "answer": answer_raw if answer_raw else "—",
            "evidence": display_evidence,
            "justification": justification,
            "is_no_justified": is_no_justified,
            "pending_justification": pending_justification,
            "missing_evidence": missing_evidence,
            "alert_msg": alert_msg,
        })

    status = "valid" if pending_count == 0 else "risk"

    return {
        "status": status,
        "items": items,
        "pending_count": pending_count,
        "total": len(items),
    }
