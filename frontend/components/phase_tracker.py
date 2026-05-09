import streamlit as st

PHASES = [
    {"id": 1, "name": "Extracción", "skill": "InformationExtraction"},
    {"id": 2, "name": "RAG Híbrido", "skill": "HybridHyperparameter"},
    {"id": 3, "name": "Evaluación", "skill": "ReproducibilityEvaluation"},
    {"id": 4, "name": "Verificación", "skill": "ChecklistVerification"},
    {"id": 5, "name": "Métricas", "skill": "MetricsCalculation"},
    {"id": 6, "name": "Finalizado", "skill": "MetadataAggregation"}
]

def get_phase_tracker_html(current_phase_index=0):
    """
    Genera el HTML para el rastreador de fases visual en una sola línea para evitar errores de Markdown.
    """
    items = []
    for i, phase in enumerate(PHASES):
        phase_id = i + 1
        status_class = "completed" if current_phase_index > phase_id else ("active" if current_phase_index == phase_id else "")
        
        item_html = (
            f'<div class="stepper-item {status_class}">'
            f'<div class="step-counter">{phase_id}</div>'
            f'<div class="step-name">{phase["name"]}</div>'
            f'</div>'
        )
        items.append(item_html)
    
    return f'<div class="stepper-wrapper">{"".join(items)}</div>'

def render_phase_tracker(current_phase_index=0):
    """Renderiza el tracker directamente (legacy support)."""
    st.markdown(get_phase_tracker_html(current_phase_index), unsafe_allow_html=True)
