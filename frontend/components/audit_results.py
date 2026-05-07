# -*- coding: utf-8 -*-
"""Componente de resultados de auditoria NeurIPS 2026 - Tabla de Cumplimiento"""
import streamlit as st
from frontend.utils.scoring import get_checklist_health


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
        # 1. Rojo: "No" sin justificación (Riesgo Crítico de Desk Reject)
        if item["pending_justification"]:
            return "#450a0a"
            
        # 2. Ámbar/Naranja: Advertencia (Claim sin evidencia O cualquier ítem con alerta detectada)
        if item["missing_evidence"] or (item.get("alert_msg") and item["alert_msg"].strip()):
            return "#452e0a"
            
        a = item["answer"].strip().lower()
        if "yes" in a:
            return "#064e3b" # Verde Esmeralda (Todo OK)
        
        # Para el resto (No justificado o N/A sin alertas), fondo neutro
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
            alert_html = '<div style="color:#fca5a5;font-size:0.78rem;margin-top:5px;font-style:italic;">&#9888; Sin justificacion del autor &mdash; Riesgo de Desk Reject</div>'
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
            f'<div style="background:#7f1d1d;border-left:6px solid #ef4444;padding:16px 20px;border-radius:8px;">'
            f'<strong style="font-size:1.15rem;color:#fca5a5;">&#x1F534; Riesgo de Desk Reject</strong>'
            f'<p style="color:#fecaca;margin:6px 0 0 0;"><strong>{pending} de {total}</strong> item(s) requieren accion del autor antes del envio.</p>'
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

    # ── FICHA TÉCNICA RAG ───────────────────────────────────────────────────
    rag_data = resultado.get("extracted_hyperparameters_hybrid", {})
    if rag_data:
        st.markdown("---")
        st.subheader("🎯 Ficha Técnica de Entrenamiento (RAG Specialist)")
        st.caption("Estos datos han sido extraídos mediante un escaneo profundo (RAG) de las secciones técnicas y apéndices.")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**🚀 Optimizador**")
            st.code(rag_data.get("optimizer", "N/A"))
            st.markdown("**📈 Learning Rate**")
            st.code(rag_data.get("learning_rate", "N/A"))
        with c2:
            st.markdown("**📦 Batch Size**")
            st.code(rag_data.get("batch_size", "N/A"))
            st.markdown("**🔄 Epochs**")
            st.code(rag_data.get("epochs", "N/A"))
        with c3:
            st.markdown("**🔥 Warmup Steps**")
            st.code(rag_data.get("warmup_steps", "N/A"))
            st.markdown("**⚖️ Weight Decay**")
            st.code(rag_data.get("weight_decay", "N/A"))
        with c4:
            st.markdown("**💻 Hardware**")
            st.info(rag_data.get("hardware", "N/A"))
            if rag_data.get("random_seed") and rag_data.get("random_seed") != "NOT FOUND":
                st.markdown("**🌱 Seed**")
                st.code(rag_data.get("random_seed"))

    # ── TABLA DE CUMPLIMIENTO ────────────────────────────────────────────────
    st.markdown("---")
    st.header("Tabla de Cumplimiento NeurIPS 2026")
    st.caption(
        "🟢 Fila verde: Cumplimiento verificado | "
        "🟠 Fila naranja: Claim sin evidencia (verificar) | "
        "🔴 Fila roja: Omisión sin justificar (riesgo de Desk Reject)"
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

    # ── PIPELINE RAG HÍBRIDO ────────────────────────────────────────────────
    with st.expander("🔍 Pipeline de Extracción Híbrida (RAG Specialist)"):
        st.write("Proceso de recuperación semántica y extracción técnica de precisión para hiperparámetros.")
        
        c_triage, c_reduce = st.columns(2)
        with c_triage:
            st.markdown("### 🛠️ Fase de Triage (MAP)")
            st.caption("Extracción estructurada de fragmentos recuperados por ChromaDB.")
            triage_steps = resultado.get("hybrid_triage_fragments", [])
            if triage_steps:
                for i, fragment in enumerate(triage_steps):
                    relevance = fragment.get("_relevance_score", "N/A")
                    color = "#065f46" if isinstance(relevance, int) and relevance > 70 else "#1e3a5f"
                    with st.expander(f"📄 Fragmento Técnico {i+1} (Relevancia: {relevance}%)"):
                        st.markdown(f'<div style="background:{color};padding:2px 10px;border-radius:10px;font-size:0.7rem;display:inline-block;margin-bottom:10px;">Confianza RAG: {relevance}%</div>', unsafe_allow_html=True)
                        st.markdown("**Texto del Chunk:**")
                        st.caption(fragment.get("_chunk_text", "Texto no disponible"))
                        st.markdown("**Datos Extraídos:**")
                        st.json({k: v for k, v in fragment.items() if not k.startswith('_')})
            else:
                st.warning("No hay datos de triage disponibles.")
                
        with c_reduce:
            st.markdown("### 💎 Fase de Consolidación (REDUCE)")
            st.caption("Fusión de datos técnicos con Gemma 4 31B.")
            st.json(resultado.get("extracted_hyperparameters_hybrid", {}))

    # ── PIPELINE DE EVALUACIÓN ──────────────────────────────────────────────
    with st.expander("🔍 Pipeline de Evaluación (Senior Area Chair + Self-Correction)"):
        st.write("Validación final de cumplimiento basada en señales pre-computadas y auditoría de falsos negativos.")
        
        # 1. Señales Pre-computadas
        st.markdown("### 🚦 Señales de Juicio (Signals)")
        signals = resultado.get("evaluation_signals", {})
        if signals:
            for key, msg in signals.items():
                st.markdown(f"**Item {key.replace('_', ' ').title()}:**")
                st.info(msg)
        else:
            st.warning("No se generaron señales dinámicas para esta evaluación.")
            
        st.markdown("---")
        
        # 2. Detalles de Verificación (Self-Correction / Auditor 2)
        st.markdown("### 🛡️ Auditoría de Falsos Negativos (Self-Correction - Auditor 2)")
        st.caption("Re-evaluación crítica de ítems realizada por Gemini 3.1 Pro para detectar omisiones o errores de interpretación.")
        
        # Filtrar ítems que fueron verificados
        verification_details = {k: v for k, v in resultado.items() if isinstance(v, dict) and v.get('verified')}
        if not verification_details:
             # Si no están directos, buscarlos dentro de las secciones
             for k, v in resultado.items():
                 if isinstance(v, dict) and v.get('answer'):
                     if v.get('verified'):
                         verification_details[k] = v
                         
        if verification_details:
            for item, data in verification_details.items():
                status = "✨ Corregido" if data.get('was_corrected') else "✅ Confirmado"
                with st.expander(f"{status}: {item}"):
                    st.write(f"**Respuesta:** {data.get('answer')}")
                    st.write(f"**Justificación Técnica:** {data.get('justification')}")
                    st.markdown("**Evidencia Verificada:**")
                    st.code(data.get('evidence'))
        else:
            st.warning("La fase de verificación no reportó cambios o no está disponible.")

    return health


def generate_report(resultado, uploaded_file, health=None):
    """Genera el informe descargable en formato Markdown."""
    if health is None:
        health = get_checklist_health(resultado)

    status_label = "Checklist Valido" if health["status"] == "valid" else "Riesgo de Desk Reject"
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
            note = " [RIESGO: sin justificacion]"
        elif item["missing_evidence"]:
            note = " [RIESGO: sin evidencia]"
        reporte += f"| {idx} | {label} | {answer} | {evidence}{note} |\n"

    reporte += "\n---\n_Generado por Auditor NeurIPS 2026._\n"
    return reporte
