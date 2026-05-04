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

    def row_bg(answer, pending):
        if pending:
            return "#3b0a0a"
        a = answer.strip().lower()
        if "yes" in a:
            return "#052e1a"
        elif "no" in a:
            return "#1c1200"
        return "#0a1628"

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
        pending = item["pending_justification"] or item["missing_evidence"]
        bg = row_bg(answer, pending)

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

    # ── TABLA DE CUMPLIMIENTO ────────────────────────────────────────────────
    st.markdown("---")
    st.header("Tabla de Cumplimiento NeurIPS 2026")
    st.caption(
        "Fila verde = Yes con evidencia | "
        "Fila ambar = No justificado por el autor | "
        "Fila roja = No sin justificacion (requiere accion)"
    )

    table_html = _build_table_html(health["items"])
    # Altura: 16 filas x 58px + cabecera + margen
    row_height = max(900, len(health["items"]) * 58 + 60)
    st.iframe(table_html, height=row_height)

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
