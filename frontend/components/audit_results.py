# -*- coding: utf-8 -*-
"""Componente de resultados de auditoria NeurIPS 2026 - Tabla de Cumplimiento"""
import streamlit as st
from frontend.utils.scoring import get_checklist_health
from frontend.components.gauge_chart import create_gauge_chart


def _build_table_html(items):
    """Construye la tabla HTML completa de cumplimiento."""

    def badge(answer):
        a = answer.strip().lower()
        if "yes" in a:
            return '<span style="background:#065f46;color:#6ee7b7;padding:4px 14px;border-radius:20px;font-weight:700;font-size:0.82rem;white-space:nowrap;">Yes</span>'
        elif "no" in a:
            return '<span style="background:#7f1d1d;color:#fca5a5;padding:4px 14px;border-radius:20px;font-weight:700;font-size:0.82rem;white-space:nowrap;">No</span>'
        return '<span style="background:#1e3a5f;color:#93c5fd;padding:4px 14px;border-radius:20px;font-weight:700;font-size:0.82rem;white-space:nowrap;">N/A</span>'

    def row_bg(item):
        a = item["answer"].strip().lower()
        
        # 1. Rojo: "No" sin justificación
        if item["pending_justification"]:
            return "#450a0a" # Rojo oscuro
            
        # 2. Ámbar/Amarillo: "No" justificado O "Yes" sin evidencia O alertas detectadas
        if ("no" in a) or item["missing_evidence"] or (item.get("alert_msg") and item["alert_msg"].strip()):
            return "#452e0a" # Ámbar/Naranja (Atención)
            
        # 3. Verde: "Yes" con evidencia (Todo OK)
        if "yes" in a:
            return "#064e3b" # Verde Esmeralda
            
        # 4. Azul: "N/A"
        if "n/a" in a:
            return "#1e3a5f" # Navy Blue
        
        # Para el resto, fondo neutro
        return "#111827"

    rows = ""
    for idx, item in enumerate(items, start=1):
        answer = item["answer"]
        label_full = item["label"]
        # Split "1. Claims" -> num="1", name="Claims"
        if ". " in label_full:
            num, name = label_full.split(". ", 1)
        else:
            num, name = str(idx), label_full

        evidence_text = item["evidence"] if item["evidence"] and item["evidence"] != "-" else ""
        bg = row_bg(item)

        # Evidence cell content
        ev_html = f'<span style="color:#d1d5db;">{evidence_text}</span>' if evidence_text else '<em style="color:#6b7280;">No disponible</em>'

        # Alert line
        alert_html = ""
        if item["pending_justification"]:
            alert_html = '<div style="color:#fca5a5;font-size:0.78rem;margin-top:5px;font-style:italic;">&#9888; Falta justificación explícita del autor</div>'
        elif item["missing_evidence"]:
            alert_html = '<div style="color:#fde68a;font-size:0.78rem;margin-top:5px;font-style:italic;">&#9888; Respuesta Yes sin evidencia de seccion del paper</div>'

        if "compensacion" in item.get("alert_msg", "").lower() or "etica" in item.get("alert_msg", "").lower():
            alert_html += '<div style="color:#fde68a;font-size:0.78rem;margin-top:3px;font-style:italic;">&#9888; NeurIPS Code of Ethics: compensacion minima obligatoria</div>'

        rows += f"""
        <tr style="background:{bg};border-bottom:1px solid #1f2937;">
          <td style="padding:10px 12px;color:#6b7280;font-weight:700;text-align:center;vertical-align:top;white-space:nowrap;">{num}</td>
          <td style="padding:10px 12px;color:#e5e7eb;font-weight:500;vertical-align:top;">{name}</td>
          <td style="padding:10px 12px;text-align:center;vertical-align:top;">{badge(answer)}</td>
          <td style="padding:10px 12px;vertical-align:top;">{ev_html}{alert_html}</td>
        </tr>
        """

    return f"""
    <html>
    <body style="margin:0;padding:0;background:transparent;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
    <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
      <thead>
        <tr style="background:#111827;">
          <th style="padding:12px;width:40px;color:#9ca3af;text-align:center;border-bottom:2px solid #374151;">#</th>
          <th style="padding:12px;color:#9ca3af;text-align:left;border-bottom:2px solid #374151;">Item del Checklist</th>
          <th style="padding:12px;width:100px;color:#9ca3af;text-align:center;border-bottom:2px solid #374151;">Respuesta</th>
          <th style="padding:12px;color:#9ca3af;text-align:left;border-bottom:2px solid #374151;">Evidencia / Justificacion</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
    </body>
    </html>
    """


def render_audit_results(resultado, uploaded_file):
    """Renderiza los resultados de la auditoria NeurIPS 2026."""
    st.success("Auditoria Finalizada")

    health = get_checklist_health(resultado)
    pending = health["pending_count"]
    total = health["total"]
    
    # ── VEREDICTO PRINCIPAL ──────────────────────────────────────────────────
    st.markdown("---")
    
    st.header("Veredicto del Checklist NeurIPS 2026")
    if health["status"] == "valid":
        st.markdown(
            '<div style="background:#064e3b;border-left:6px solid #10b981;padding:16px 20px;border-radius:8px;">'
            '<strong style="font-size:1.15rem;color:#6ee7b7;">&#x1F7E2; Checklist Valido</strong>'
            '<p style="color:#a7f3d0;margin:6px 0 0 0;">Todas las respuestas tienen evidencia o justificacion documentada. El checklist esta listo para NeurIPS.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="background:#452e0a;border-left:6px solid #fbbf24;padding:16px 20px;border-radius:8px;">'
            f'<strong style="font-size:1.15rem;color:#fde68a;">&#x1F7E0; Atención Requerida</strong>'
            f'<p style="color:#fef3c7;margin:6px 0 0 0;"><strong>{pending} de {total}</strong> item(s) requieren atención o justificación adicional antes del envío.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── METRICAS ─────────────────────────────────────────────────────────────
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        yes_count = sum(1 for i in health["items"] if "yes" in i["answer"].lower())
        st.metric("Items Yes", yes_count)
    with col2:
        no_count = sum(1 for i in health["items"] if "no" in i["answer"].lower())
        st.metric("Items No", no_count)
    with col3:
        na_count = sum(1 for i in health["items"] if "n/a" in i["answer"].lower())
        st.metric("Items N/A", na_count)
    with col4:
        tiempo = resultado.get("metricas", {}).get("tiempo_segundos", "N/A")
        st.metric("Tiempo", f"{tiempo}s")


    # ── DATOS DEL ANÁLISIS EXHAUSTIVO (DINÁMICO DESDE REDUCE JSON) ───────────
    st.markdown("---")
    with st.expander("📊 Datos Extraídos (Análisis Exhaustivo)", expanded=False):
        st.write("Consulta la base de datos técnica consolidada durante la fase REDUCE.")
        
        info = resultado.get("informacion_extraida", {})
        
        # 1. Metadatos del Paper (Título y Autores si existen)
        if info.get("paper_title") or info.get("authors"):
            st.markdown(f"### 📄 {info.get('paper_title', 'Sin título detectado')}")
            if info.get("authors"):
                st.caption(f"Autores: {', '.join(info.get('authors')) if isinstance(info.get('authors'), list) else info.get('authors')}")
            st.markdown("---")

        # 2. Iterar por las "secciones" (claves) del JSON de Reduce
        # Definimos el orden y los iconos para las secciones principales
        section_config = {
            "hyperparameters": {"icon": "⚙️", "label": "Hiperparámetros"},
            "hardware": {"icon": "💻", "label": "Hardware & Compute"},
            "architecture": {"icon": "🏗️", "label": "Arquitectura del Modelo"},
            "data": {"icon": "📂", "label": "Dataset & Datos"},
            "code": {"icon": "💻", "label": "Código & Repositorio"},
            "statistics": {"icon": "📊", "label": "Estadística & Rigor"},
            "baseline_comparison": {"icon": "⚖️", "label": "Comparativa con Baselines"},
            "theory_and_proofs": {"icon": "📐", "label": "Teoría & Demostraciones"},
            "software_versions": {"icon": "🛠️", "label": "Software & Versiones"},
            "limitations_quality": {"icon": "⚠️", "label": "Análisis de Limitaciones"},
            "problematic_phrases": {"icon": "🚩", "label": "Frases Problemáticas"},
            "licenses_extraction": {"icon": "📜", "label": "Licencias detectadas"},
            "broader_impacts_extraction": {"icon": "🌍", "label": "Impacto Social (Broader Impacts)"},
            "llm_usage_extraction": {"icon": "🤖", "label": "Declaración de uso de LLMs"},
            "human_subjects_extraction": {"icon": "👥", "label": "Sujetos Humanos & Crowdsourcing"}
        }

        for key, config in section_config.items():
            data = info.get(key)
            if data and data != "NOT FOUND":
                with st.expander(f"{config['icon']} {config['label']}", expanded=False):
                    if isinstance(data, dict):
                        # Formatear como lista clave-valor con estilo mejorado
                        for k, v in data.items():
                            if v and v != "NOT FOUND":
                                label = k.replace('_', ' ').title()
                                st.markdown(
                                    f'<div style="margin-bottom:8px;">'
                                    f'<span style="color:#60a5fa;font-weight:700;font-size:0.9rem;">{label}:</span> '
                                    f'<span style="color:#e5e7eb;font-size:0.9rem;">{v}</span>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )
                    elif isinstance(data, list):
                        for item in data:
                            st.markdown(
                                f'<div style="margin-bottom:6px;color:#e5e7eb;font-size:0.9rem;">• {item}</div>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(f'<div style="color:#e5e7eb;font-size:0.9rem;">{data}</div>', unsafe_allow_html=True)

        # 3. Razonamiento y Mapeo de Secciones (Siempre al final)
        st.markdown("---")
        col_cot, col_map = st.columns(2)
        with col_cot:
            with st.expander("🧠 Razonamiento de Consolidación (CoT)", expanded=False):
                st.info(info.get("thought_process", "No disponible"))
        with col_map:
            with st.expander("📍 Secciones Identificadas", expanded=False):
                mapping = info.get("context_mapping", [])
                if mapping:
                    for section in mapping:
                        st.markdown(f"✅ `{section}`")
                else:
                    st.write("No disponible")

    # ── TABLA DE CUMPLIMIENTO ────────────────────────────────────────────────
    st.markdown("---")
    st.header("Tabla de Cumplimiento NeurIPS 2026")
    st.caption(
        "🟢 Fila verde: Cumplimiento verificado | "
        "🟠 Fila naranja: 'No' justificado o falta evidencia | "
        "🔴 Fila roja: 'No' sin justificar"
    )

    table_html = _build_table_html(health["items"])
    st.html(table_html)

    # ── EXPLORADOR DE DATOS TÉCNICOS ──────────────────────────────────────────
    st.markdown("---")
    with st.expander("🔍 Pipeline de Análisis Profundo (Map-Reduce + CoT + Context Mapping)"):
        st.write("Visualiza el razonamiento interno y la reconstrucción del paper por parte de la IA.")
        
        # 1. Chain of Thought Final
        st.markdown("### 🧠 Chain-of-Thought (Razonamiento de Consolidación)")
        cot = resultado.get("informacion_extraida", {}).get("thought_process", "No disponible")
        st.info(cot)
        
        # 2. Context Mapping
        st.markdown("### 📍 Context Mapping (Secciones Identificadas)")
        mapping = resultado.get("informacion_extraida", {}).get("context_mapping", [])
        if mapping:
            cols = st.columns(len(mapping) if len(mapping) < 5 else 5)
            for i, section in enumerate(mapping):
                cols[i % 5].markdown(f"✅ `{section}`")
        else:
            st.warning("No se ha podido mapear la estructura de secciones.")
            
        st.markdown("---")
        
        # 3. Comparativa Map vs Reduce
        col_map, col_rag = st.columns(2)
        with col_map:
            st.markdown("### 🗺️ Fase MAP (Extracción Segmentada)")
            st.caption("Extracción en paralelo de fragmentos del paper.")
            map_steps = resultado.get("general_analysis_map", [])
            if map_steps:
                for i, step in enumerate(map_steps):
                    with st.expander(f"📦 Fragmento {i+1}"):
                        st.json(step)
            else:
                st.json(resultado.get("original_extraction_raw", {}))
                
        with col_rag:
            st.markdown("### 🎯 Fase REDUCE (Consolidación Final)")
            st.caption("Datos finales refinados y validados.")
            st.json(resultado.get("informacion_extraida", {}))


    # ── PIPELINE DE EVALUACIÓN ──────────────────────────────────────────────
    with st.expander("🔍 Pipeline de Evaluación (Senior Area Chair)"):
        st.write("Validación final de cumplimiento basada en señales pre-computadas e inyección de contexto profundo.")
        
        # 1. Ayudas del Extractor (Extraction Helps)
        st.markdown("### 🚦 Ayudas del Extractor (Extraction Helps)")
        helps = resultado.get("evaluation_helps", {})
        if helps:
            for key, msg in helps.items():
                st.markdown(f"**Item {key.replace('_', ' ').title()}:**")
                st.info(msg)
        else:
            st.warning("No se generaron ayudas dinámicas para esta evaluación.")
            
        st.markdown("---")
        


    return health


def generate_report(resultado, uploaded_file, health=None):
    """Genera el informe descargable en formato Markdown."""
    if health is None:
        health = get_checklist_health(resultado)

    status_label = "Checklist Valido" if health["status"] == "valid" else "Requiere Atencion (Faltan justificaciones)"
    pending = health["pending_count"]
    total = health["total"]

    reporte = f"# NeurIPS 2026 Checklist Audit Report\n\n"
    reporte += f"**Paper:** {uploaded_file.name}\n\n"
    reporte += f"**Veredicto:** {status_label}\n"
    reporte += f"**Items con problemas:** {pending} de {total}\n\n"
    reporte += "---\n\n## Tabla de Cumplimiento\n\n"
    reporte += "| # | Item | Respuesta | Evidencia / Justificacion |\n"
    reporte += "|---|------|-----------|---------------------------|\n"

    for idx, item in enumerate(health["items"], start=1):
        label = item["label"]
        answer = item["answer"]
        evidence = item["evidence"] if item["evidence"] and item["evidence"] != "-" else "-"
        note = ""
        if item["pending_justification"]:
            note = " [ATENCIÓN: sin justificacion clara]"
        elif item["missing_evidence"]:
            note = " [ATENCIÓN: sin evidencia]"
        reporte += f"| {idx} | {label} | {answer} | {evidence}{note} |\n"

    reporte += "\n---\n_Generado por Auditor NeurIPS 2026._\n"
    return reporte
