"""Componente de visualización de resultados de auditoría"""
import streamlit as st
import pandas as pd
from frontend.components.gauge_chart import create_gauge_chart
from frontend.utils.scoring import calcular_puntuacion

def render_audit_results(resultado, uploaded_file):
    """Renderiza los resultados de la auditoría con criterios NeurIPS 2025"""
    st.success("✅ Auditoría Finalizada")
    
    # Calcular puntuación híbrida: scores LLM + penalizaciones red flags
    scores = resultado.get('peer_review_scores', {})
    red_flags = resultado.get('red_flags', {})
    evaluation = resultado  # El resultado completo contiene la evaluación
    
    puntuacion, desglose = calcular_puntuacion(scores, red_flags, evaluation)
    
    # === SECCIÓN 1: RESUMEN EJECUTIVO ===
    st.markdown("---")
    st.header("📊 Resumen Ejecutivo")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Overall Score", f"{puntuacion}%")
        st.plotly_chart(create_gauge_chart(puntuacion), width='stretch')
    
    with col2:
        st.metric("Recommendation", resultado.get("recommendation", "N/A"))
        confidence = resultado.get('confidence', 'N/A')
        st.metric("Reviewer Confidence", f"{confidence}/5")
    
    with col3:
        tiempo = resultado.get('metricas', {}).get('tiempo_segundos', 'N/A')
        st.metric("Analysis Time", f"{tiempo}s")
        red_flags_count = resultado.get('metricas', {}).get('red_flags_detectadas', 0)
        st.metric("Red Flags Detected", red_flags_count)
    
    # === SECCIÓN 1.5: DESGLOSE DE PUNTUACIÓN ===
    if desglose.get('penalizaciones') or desglose.get('bonificaciones'):
        with st.expander("📐 Ver Desglose de Puntuación", expanded=True):
            st.markdown(f"**Score Base (LLM):** {desglose['score_base']}%")
            st.caption(
                f"Soundness: {desglose['scores_llm']['soundness']}/4 · "
                f"Contribution: {desglose['scores_llm']['contribution']}/4 · "
                f"Presentation: {desglose['scores_llm']['presentation']}/4"
            )
            
            if desglose['penalizaciones']:
                st.markdown("**🔻 Penalizaciones:**")
                for motivo, valor in desglose['penalizaciones']:
                    st.markdown(f"- {motivo}: **{valor}%**")
                st.markdown(f"**Total penalizaciones: {desglose['total_penalizaciones']}%**")
            
            if desglose['bonificaciones']:
                st.markdown("**🔺 Bonificaciones:**")
                for motivo, valor in desglose['bonificaciones']:
                    st.markdown(f"- {motivo}: **+{valor}%**")
                st.markdown(f"**Total bonificaciones: +{desglose['total_bonificaciones']}%**")
            
            st.markdown(f"---\n**Score Final: {puntuacion}%**")
    
    # === SECCIÓN 2: REVIEWER'S SUMMARY ===
    if resultado.get('self_written_summary'):
        st.markdown("---")
        st.subheader("✍️ Reviewer's Summary (Own Words)")
        st.info(resultado['self_written_summary'])
        
    # === SECCIÓN 2.5: HYBRID HYPERPARAMETER EXTRACTION ===
    hybrid_hps = resultado.get('extracted_hyperparameters_hybrid')
    if hybrid_hps:
        st.markdown("---")
        st.subheader("⚙️ Extracted Hyperparameters (Hybrid RAG Pipeline)")
        
        # Convertir a DataFrame
        import pandas as pd
        
        # Crear un dataframe amigable
        hp_records = []
        for key, value in hybrid_hps.items():
            if str(value).strip() and value != 'NOT FOUND':
                hp_records.append({
                    "Hyperparameter": key.replace('_', ' ').title(),
                    "Extracted Value": str(value)
                })
                
        if hp_records:
            df_hps = pd.DataFrame(hp_records)
            st.table(df_hps)
        else:
            st.info("No explicit hyperparameters found via hybrid extraction.")
    
    # === SECCIÓN 3: PEER REVIEW SCORES ===
    st.markdown("---")
    st.subheader("🎯 Peer Review Scores")
    
    soundness = scores.get('soundness', {}).get('score', 0)
    presentation = scores.get('presentation', {}).get('score', 0)
    contribution = scores.get('contribution', {}).get('score', 0)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("Soundness", f"{soundness}/4")
        st.caption(scores.get('soundness', {}).get('justification', ''))
    with col_s2:
        st.metric("Presentation", f"{presentation}/4")
        st.caption(scores.get('presentation', {}).get('justification', ''))
    with col_s3:
        st.metric("Contribution", f"{contribution}/4")
        st.caption(scores.get('contribution', {}).get('justification', ''))
    
    # === SECCIÓN 4: ORIGINALITY VS SIGNIFICANCE ===
    if resultado.get('originality_significance'):
        st.markdown("---")
        st.subheader("🌟 Originality vs Significance (NeurIPS 2025)")
        orig_sig = resultado['originality_significance']
        
        col_os1, col_os2 = st.columns(2)
        with col_os1:
            st.metric("💡 Originality (Conceptual Novelty)", f"{orig_sig.get('originality_score', 'N/A')}/4")
            st.caption(orig_sig.get('originality_justification', ''))
        with col_os2:
            st.metric("🎯 Significance (Practical Impact)", f"{orig_sig.get('significance_score', 'N/A')}/4")
            st.caption(orig_sig.get('significance_justification', ''))
    
    # === SECCIÓN 5: CLAIMS & SCOPE AUDIT ===
    st.markdown("---")
    st.subheader("🔍 Claims and Scope Audit")
    claims = resultado.get('claims_scope_audit', {})
    
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.metric("Abstract Reflects Results", claims.get('abstract_reflects_results', 'N/A'))
    with col_c2:
        st.metric("Overselling Detected", claims.get('overselling_detected', 'N/A'))
    with col_c3:
        st.metric("Scope Exceeds Evidence", claims.get('scope_exceeds_evidence', 'N/A'))
    with col_c4:
        st.metric("Settings Acknowledged", claims.get('specific_settings_acknowledged', 'N/A'))
    
    if claims.get('overselling_examples'):
        with st.expander("⚠️ View Overselling Examples"):
            for ex in claims['overselling_examples']:
                st.text(f"- {ex}")
    
    if claims.get('suggestions'):
        st.info(f"💡 **Suggestions:** {claims['suggestions']}")
    
    # === SECCIÓN 6: REPRODUCIBILITY ===
    st.markdown("---")
    st.subheader("🔄 Reproducibility Check")
    repro = resultado.get('reproducibility', {})
    
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.metric("Error Bars Method", repro.get('error_bars_method', 'N/A'))
        st.metric("Computational Resources", repro.get('computational_resources', 'N/A'))
    with col_r2:
        st.metric("Dependencies/Versions", repro.get('dependencies_versions', 'N/A'))
        st.metric("Dataset Licensing", repro.get('dataset_licensing', 'N/A'))
    with col_r3:
        st.metric("Path to Verification", repro.get('path_to_verification', 'N/A'))
        highly_repro = repro.get('highly_reproducible', 'No')
        color = "normal" if highly_repro == "Yes" else "inverse"
        st.metric("Highly Reproducible", highly_repro)
    
    if repro.get('blocking_issues'):
        with st.expander("❌ View Blocking Issues"):
            for issue in repro['blocking_issues']:
                st.text(f"- {issue}")
    
    # === SECCIÓN 7: LIMITATIONS & IMPACT ===
    st.markdown("---")
    st.subheader("🚨 Limitations and Impact")
    limits = resultado.get('limitations_impact', {})
    
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        st.metric("Limitations Section", limits.get('limitations_section_present', 'N/A'))
    with col_l2:
        st.metric("Failure Modes Discussed", limits.get('failure_modes_discussed', 'N/A'))
    with col_l3:
        st.metric("Representativeness/Consent", limits.get('representativeness_consent', 'N/A'))
    
    if limits.get('three_specific_limitations'):
        with st.expander("📝 View Required Limitations"):
            for lim in limits['three_specific_limitations']:
                st.text(f"- {lim}")
    
    if limits.get('negative_consequences_identified'):
        st.warning(f"⚠️ **Negative Consequences:** {', '.join(limits['negative_consequences_identified'])}")
    
    # === SECCIÓN 8: THEORETICAL RIGOR ===
    st.markdown("---")
    st.subheader("🧮 Theoretical Rigor")
    theory = resultado.get('theoretical_rigor', {})
    
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.metric("Assumptions Explicit", theory.get('assumptions_explicit', 'N/A'))
    with col_t2:
        st.metric("Proof Sketch Clarity", theory.get('proof_sketch_clarity', 'N/A'))
    with col_t3:
        st.metric("External Theorems Cited", theory.get('external_theorems_cited', 'N/A'))
    with col_t4:
        st.metric("Informal Proofs", theory.get('informal_proofs_without_formal', 'N/A'))
    
    if theory.get('assessment'):
        st.info(f"📊 **Assessment:** {theory['assessment']}")
    
    # === SECCIÓN 9: ETHICS FLAG ===
    st.markdown("---")
    if resultado.get('ethics_flag'):
        ethics = resultado['ethics_flag']
        if ethics.get('requires_ethics_review') == 'Yes':
            st.subheader("⚠️ Ethics Committee Review Required")
            st.error(f"**Concerns:** {', '.join(ethics.get('concerns', []))}")
            st.warning(f"**Justification:** {ethics.get('justification', '')}")
        else:
            st.subheader("✅ Ethics Review")
            st.success("No ethics concerns detected")
            if ethics.get('justification'):
                st.caption(ethics['justification'])
    
    # === SECCIÓN 10: QUESTIONS FOR AUTHORS ===
    st.markdown("---")
    st.subheader("❓ Questions for Authors")
    questions = resultado.get('questions_for_authors', [])
    if questions:
        for i, q in enumerate(questions, 1):
            st.text(f"{i}. {q}")
    else:
        st.info("No questions raised")
    
    return puntuacion

def generate_report(resultado, uploaded_file, puntuacion):
    """Genera el informe descargable en formato Markdown con criterios NeurIPS 2025"""
    
    # Recalcular desglose para incluirlo en el informe
    scores = resultado.get('peer_review_scores', {})
    red_flags = resultado.get('red_flags', {})
    evaluation = resultado
    _, desglose = calcular_puntuacion(scores, red_flags, evaluation)
    
    reporte = f"# NeurIPS 2025 Review Report: {uploaded_file.name}\n\n"
    reporte += f"**Overall Score:** {puntuacion:.1f}%\n"
    reporte += f"**Recommendation:** {resultado.get('recommendation', '')}\n"
    reporte += f"**Confidence:** {resultado.get('confidence', '')}/5\n\n"
    
    # Desglose de puntuación
    reporte += "## Score Breakdown\n\n"
    reporte += f"- **Score Base (LLM):** {desglose['score_base']}%\n"
    reporte += f"  - Soundness: {desglose['scores_llm']['soundness']}/4\n"
    reporte += f"  - Contribution: {desglose['scores_llm']['contribution']}/4\n"
    reporte += f"  - Presentation: {desglose['scores_llm']['presentation']}/4\n\n"
    
    if desglose['penalizaciones']:
        reporte += "### Penalizaciones\n\n"
        for motivo, valor in desglose['penalizaciones']:
            reporte += f"- {motivo}: **{valor}%**\n"
        reporte += f"\n**Total penalizaciones: {desglose['total_penalizaciones']}%**\n\n"
    
    if desglose['bonificaciones']:
        reporte += "### Bonificaciones\n\n"
        for motivo, valor in desglose['bonificaciones']:
            reporte += f"- {motivo}: **+{valor}%**\n"
        reporte += f"\n**Total bonificaciones: +{desglose['total_bonificaciones']}%**\n\n"
    
    # Self-Written Summary
    if resultado.get('self_written_summary'):
        reporte += "## Reviewer's Summary (Own Words)\n\n"
        reporte += f"{resultado['self_written_summary']}\n\n"
    
    reporte += "## Peer Review Scores\n\n"
    for criterion in ['soundness', 'presentation', 'contribution']:
        data = scores.get(criterion, {})
        reporte += f"### {criterion.title()}\n"
        reporte += f"- **Score:** {data.get('score', 'N/A')}/4\n"
        reporte += f"- **Justification:** {data.get('justification', '')}\n\n"
    
    # Originality vs Significance
    if resultado.get('originality_significance'):
        reporte += "## Originality vs Significance (NeurIPS 2025)\n\n"
        orig_sig = resultado['originality_significance']
        reporte += f"### Originality (Conceptual Novelty)\n"
        reporte += f"- **Score:** {orig_sig.get('originality_score', 'N/A')}/4\n"
        reporte += f"- **Justification:** {orig_sig.get('originality_justification', '')}\n\n"
        reporte += f"### Significance (Practical Impact)\n"
        reporte += f"- **Score:** {orig_sig.get('significance_score', 'N/A')}/4\n"
        reporte += f"- **Justification:** {orig_sig.get('significance_justification', '')}\n\n"
    
    # Ethics Flag
    if resultado.get('ethics_flag'):
        reporte += "## Ethics Review\n\n"
        ethics = resultado['ethics_flag']
        reporte += f"- **Requires Ethics Committee Review:** {ethics.get('requires_ethics_review', 'N/A')}\n"
        if ethics.get('concerns'):
            reporte += f"- **Concerns:** {', '.join(ethics['concerns'])}\n"
        reporte += f"- **Justification:** {ethics.get('justification', '')}\n\n"
    
    reporte += "## Claims and Scope Audit\n"
    claims = resultado.get('claims_scope_audit', {})
    for k, v in claims.items():
        reporte += f"- **{k}:** {v}\n"
    reporte += "\n"
    
    reporte += "## Limitations and Impact\n"
    limits = resultado.get('limitations_impact', {})
    for k, v in limits.items():
        reporte += f"- **{k}:** {v}\n"
    reporte += "\n"
    
    reporte += "## Reproducibility\n"
    repro = resultado.get('reproducibility', {})
    for k, v in repro.items():
        reporte += f"- **{k}:** {v}\n"
    reporte += "\n"
    
    reporte += "## Questions for Authors\n"
    for i, q in enumerate(resultado.get('questions_for_authors', []), 1):
        reporte += f"{i}. {q}\n"
    
    return reporte
