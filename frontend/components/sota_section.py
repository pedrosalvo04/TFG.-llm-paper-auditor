"""Componente de análisis del Estado del Arte (SOTA) con clustering semántico"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ---------------------------------------------------------------------------
# Punto de entrada principal
# ---------------------------------------------------------------------------

def render_sota_analysis(md_text: str):
    """Renderiza la sección completa de análisis SOTA."""
    st.markdown("---")
    st.subheader("📚 State of the Art Validation (SOTA)")

    if "sota_results" not in st.session_state:
        st.info("By default, the system selects the top-20 papers based on citation count. You can change this priority after the initial analysis.")
        if st.button("Run Literature Analysis", type="primary"):
            with st.spinner("Connecting to Semantic Scholar and validating bibliography..."):
                resultado_sota = st.session_state.sota_analyzer.analyze_sota(
                    md_text, ranking_criterion="citations"
                )
                st.session_state.sota_results = resultado_sota
            st.rerun()
    else:
        resultado_sota = st.session_state.sota_results
        
        if "error" in resultado_sota:
            st.error(f"Error performing SOTA analysis: {resultado_sota.get('error', 'Unknown error')}")
            if st.button("Retry Analysis"):
                del st.session_state.sota_results
                st.rerun()
            return
            
        st.success("Analysis completed")

        # --- Datos base ---
        papers_omitidos = resultado_sota.get("papers_omitidos", [])
        papers_analizados = resultado_sota.get("papers_analizados", [])
        clustering = resultado_sota.get("clustering", {})
        año_paper_estudiado = resultado_sota.get("metadata", {}).get("año_paper_estudiado")
        meta = resultado_sota.get("metadata", {})

        # --- Sección de clustering (siempre visible si hay datos) ---
        if clustering.get("diversity_score") is not None:
            _render_clustering_section(papers_analizados, clustering)

        # --- Selector de criterio de ranking y filtros (Dentro de los resultados) ---
        st.markdown("#### ⚙️ Top-20 Selection Criterion & Filters")
        st.caption("Change how the top-20 papers are selected and filter by thematic cluster.")
        
        criterion_map = {
            "📈 Citations": "citations",
            "🧬 Cosine Similarity": "similarity",
            "🤖 LLM Relevance": "llm",
        }
        
        current_crit = resultado_sota.get("ranking_criterion", "citations")
        current_cluster = meta.get("target_cluster_id", "all")
        
        idx = 0
        keys = list(criterion_map.keys())
        for i, k in enumerate(keys):
            if criterion_map[k] == current_crit:
                idx = i
                break

        cluster_summary = clustering.get("cluster_summary", {})
        
        cluster_options = ["All Clusters"]
        cluster_map = {"All Clusters": "all"}
        for cid, info in cluster_summary.items():
            label = f"{info.get('emoji', '📁')} {info.get('label', f'Cluster {cid}')}"
            cluster_options.append(label)
            cluster_map[label] = str(cid)

        cluster_idx = 0
        for i, opt in enumerate(cluster_options):
            if cluster_map[opt] == str(current_cluster):
                cluster_idx = i
                break

        col1, col2 = st.columns(2)
        with col1:
            criterion_label = st.selectbox(
                "Ranking strategy:",
                options=keys,
                index=idx,
            )
            selected_crit = criterion_map[criterion_label]

        with col2:
            cluster_label = st.selectbox(
                "Filter by Cluster:",
                options=cluster_options,
                index=cluster_idx,
            )
            selected_cluster = cluster_map[cluster_label]

        # Auto-update logic
        if selected_crit != current_crit or selected_cluster != str(current_cluster):
            with st.spinner(f"Re-analyzing using '{selected_crit}' and cluster filter..."):
                new_resultado = st.session_state.sota_analyzer.update_ranking_and_reanalyze(selected_crit, selected_cluster)
                st.session_state.sota_results = new_resultado
            st.rerun()

        # Tooltip explicativo según criterio seleccionado
        _criterion_tooltips = {
            "citations": "ℹ️ Papers with the highest citation count are prioritised. Fast and deterministic.",
            "similarity": "ℹ️ Papers whose abstract is most semantically similar to yours (cosine similarity on embeddings).",
            "llm": "ℹ️ The LLM scores each paper's relevance to your research (0–10) and picks the top-20. Slower but most contextual.",
        }
        st.caption(_criterion_tooltips[selected_crit])

        st.markdown("<br>", unsafe_allow_html=True)
        
        n_rec = meta.get("total_papers_recuperados", "?")
        n_ana = meta.get("total_papers_analizados", "?")
        
        st.info(
            f"📊 **Analysis Scope:** Retrieved **{n_rec}** candidates from Semantic Scholar. "
            f"Currently displaying in-depth analysis for the top **{n_ana}** papers, "
            f"filtered and ranked by **{selected_crit}**."
        )

        # --- Conclusión ---
        st.markdown("### 📝 Conclusion")
        st.info(resultado_sota.get("conclusion_sota", ""))

        # --- Lista unificada de los papers evaluados (destacando citados y no citados) ---
        df_papers = pd.DataFrame(papers_analizados)
        if not df_papers.empty:
            _render_unified_evaluated_papers(df_papers, papers_omitidos, año_paper_estudiado, clustering)
        else:
            st.warning("No papers available for evaluation.")


# ---------------------------------------------------------------------------
# Sección de clustering
# ---------------------------------------------------------------------------

def _render_clustering_section(papers_analizados: list, clustering: dict):
    """Renderiza la sección de clustering semántico con métricas y gráfico de similitud."""
    st.markdown("---")
    st.markdown("### 🧮 Semantic Clustering Analysis")
    st.caption(
        "Papers grouped into thematic families based on abstract embeddings "
        "(all-MiniLM-L6-v2 + cosine similarity vs your paper)"
    )

    diversity_score = clustering.get("diversity_score")
    cluster_summary = clustering.get("cluster_summary", {})
    user_similarities = clustering.get("user_similarities", [])

    # --- Métricas rápidas ---
    n_clusters = len(cluster_summary)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Retrieved Papers", len(user_similarities))
    with col2:
        st.metric("🗂️ Thematic Clusters", n_clusters)
    with col3:
        div_pct = f"{diversity_score:.1%}" if diversity_score is not None else "N/A"
        diversity_label = _diversity_label(diversity_score)
        st.metric(f"🌈 Diversity Score ({diversity_label})", div_pct)

    # --- Barra de diversidad ---
    if diversity_score is not None:
        _render_diversity_bar(diversity_score)

    # --- Similitud vs paper del usuario ---
    if user_similarities:
        _render_similarity_bars(user_similarities)

    # --- Resumen por cluster ---
    if cluster_summary:
        _render_cluster_summary(cluster_summary)


def _diversity_label(score) -> str:
    if score is None:
        return "N/A"
    if score >= 0.75:
        return "High"
    if score >= 0.45:
        return "Medium"
    return "Low"


def _render_diversity_bar(diversity_score: float):
    """Barra de progreso visual para el score de diversidad."""
    color = "#10b981" if diversity_score >= 0.6 else ("#f59e0b" if diversity_score >= 0.4 else "#ef4444")
    pct = int(diversity_score * 100)
    st.markdown(
        f"""
<div style="margin: 8px 0 20px 0;">
  <div style="display:flex; justify-content:space-between; font-size:0.78em; color:#94a3b8; margin-bottom:4px;">
    <span>0 — All identical</span>
    <span>1 — Maximally diverse</span>
  </div>
  <div style="background:rgba(255,255,255,0.08); border-radius:999px; height:10px; overflow:hidden;">
    <div style="width:{pct}%; background:{color}; height:100%; border-radius:999px;
                transition:width 0.6s ease;"></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_cluster_summary(cluster_summary: dict):
    """Tarjetas de resumen por cluster."""
    st.markdown("#### 🗂️ Thematic Clusters (All Retrieved)")

    # Normalizar claves a str
    enriched = {str(k): v for k, v in cluster_summary.items()}

    if not enriched:
        st.info("No cluster information available.")
        return

    n_cols = max(1, min(len(enriched), 3))
    cols = st.columns(n_cols)
    for idx, (cid, info) in enumerate(sorted(enriched.items())):
        titles = info.get("paper_titles", [])
        color = info.get("color", "#6366f1")
        emoji = info.get("emoji", "🔵")
        label = info.get("label", f"Cluster {int(cid)+1}")
        with cols[idx % 3]:
            # Mostrar todos los títulos abreviados
            titles_html = "".join(
                f"<li style='font-size:0.78em; color:#cbd5e1; margin-bottom:3px;'>{t[:55]}{'…' if len(t)>55 else ''}</li>"
                for t in titles
            )
            st.markdown(
                f"""
<div style="background:rgba(255,255,255,0.06); border-radius:12px;
            border:1px solid {color}55; padding:16px; margin-bottom:12px;">
  <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
    <span style="font-size:1.4em;">{emoji}</span>
    <span style="font-weight:700; color:{color}; font-size:1em;">{label}</span>
    <span style="margin-left:auto; background:{color}22; color:{color};
                 font-size:0.75em; padding:2px 8px; border-radius:999px;">
      {len(titles)} papers
    </span>
  </div>
  <ul style="margin:0; padding-left:14px; list-style:disc;">
    {titles_html}
  </ul>
</div>
""",
                unsafe_allow_html=True,
            )


def _render_similarity_bars(user_similarities: list):
    """Gráfico de barras horizontal: similitud coseno de cada SOTA paper vs el paper del usuario."""
    with st.expander("📊 Cosine Similarity vs Your Paper (expand)", expanded=True):
        st.caption(
            "How semantically close is each SOTA paper to **your paper** "
            "(abstract embedding cosine similarity, 0 = unrelated, 1 = identical)"
        )

        # Ordenados de mayor a menor similitud (ya vienen ordenados de la skill)
        titles = [e["title"][:55] + ("…" if len(e["title"]) > 55 else "") for e in user_similarities]
        sims = [e["similarity"] for e in user_similarities]
        colors = [e["cluster_color"] for e in user_similarities]
        labels_hover = [
            f"{e['cluster_emoji']} {e['cluster_label']} — {e['similarity']:.3f}"
            for e in user_similarities
        ]

        fig = go.Figure(
            go.Bar(
                x=sims,
                y=titles,
                orientation="h",
                marker=dict(
                    color=colors,
                    opacity=0.85,
                    line=dict(color="rgba(255,255,255,0.15)", width=0.5),
                ),
                text=[f"{s:.2f}" for s in sims],
                textposition="outside",
                textfont=dict(color="#cbd5e1", size=10),
                hovertext=labels_hover,
                hovertemplate="<b>%{y}</b><br>Similarity: <b>%{x:.3f}</b><br>%{hovertext}<extra></extra>",
            )
        )

        height = max(350, len(user_similarities) * 42)
        fig.update_layout(
            title=dict(
                text="Semantic Similarity to Your Paper — SOTA Papers",
                font=dict(size=14, color="#e2e8f0"),
            ),
            paper_bgcolor="rgba(15,23,42,0)",
            plot_bgcolor="rgba(15,23,42,0)",
            font=dict(color="#cbd5e1", size=12),
            xaxis=dict(
                range=[0, min(max(sims) * 1.15, 1.0)],
                showgrid=True,
                gridcolor="rgba(255,255,255,0.07)",
                tickformat=".2f",
                title=dict(text="Cosine Similarity", font=dict(size=12, color="#94a3b8")),
            ),
            yaxis=dict(
                autorange="reversed",
                showgrid=False,
                tickfont=dict(size=15),
            ),
            height=height,
            margin=dict(l=20, r=60, t=45, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Sección de papers omitidos (existente, enriquecida con badges de cluster)
# ---------------------------------------------------------------------------

def _render_unified_evaluated_papers(df_papers, papers_omitidos, año_paper_estudiado, clustering: dict):
    """Renderiza la lista completa de los 20 papers evaluados, destacando visualmente los omitidos/no citados."""
    df_papers["authors_display"] = df_papers["autores"].apply(
        lambda x: (
            ", ".join([a.get("name", "") for a in x[:2]]) + (" et al." if len(x) > 2 else "")
            if isinstance(x, list)
            else "N/A"
        )
    )

    df_papers.rename(
        columns={"titulo": "title", "año": "year", "citas": "citationCount"}, inplace=True
    )

    titulos_omitidos = {p["titulo"].lower().strip() for p in papers_omitidos}

    def es_omitido(titulo):
        titulo_lower = str(titulo).lower().strip()
        for omitido in titulos_omitidos:
            if omitido in titulo_lower or titulo_lower in omitido:
                return True
        return False

    df_papers["es_omitido"] = df_papers["title"].apply(es_omitido)
    num_omitidos = df_papers["es_omitido"].sum()

    st.markdown("### 📚 Complete Evaluated Literature")
    st.caption(
        f"Displaying all **{len(df_papers)} top evaluated papers**. "
        f"🔴 **{num_omitidos} missing citations** flagged for recommended inclusion."
    )

    # Lookup cluster por título
    cluster_by_title = {}
    for paper in clustering.get("cluster_summary", {}).values():
        for t in paper.get("paper_titles", []):
            cluster_by_title[t.lower().strip()] = paper

    for _, paper in df_papers.iterrows():
        titulo_paper = str(paper["title"]).lower().strip()
        es_om = paper["es_omitido"]

        justificacion = relevancia = subtema = ""
        if es_om:
            for omitido in papers_omitidos:
                titulo_omitido = str(omitido["titulo"]).lower().strip()
                if titulo_omitido in titulo_paper or titulo_paper in titulo_omitido:
                    justificacion = omitido.get("justificacion", "")
                    relevancia = omitido.get("relevancia", "High")
                    subtema = omitido.get("subtema_relacionado", "")
                    break

        es_posterior = (
            "✅ Sí"
            if año_paper_estudiado and paper["year"] > año_paper_estudiado
            else "❌ No"
        )
        if not año_paper_estudiado:
            es_posterior = "?"

        cluster_info = cluster_by_title.get(titulo_paper, {})
        cluster_color = cluster_info.get("color", "#6366f1")
        cluster_emoji = cluster_info.get("emoji", "📄")
        cluster_label = cluster_info.get("label", "")

        cluster_badge = ""
        if cluster_label:
            cluster_badge = (
                f'<span style="background:{cluster_color}22; '
                f'color:{cluster_color}; font-size:0.72em; '
                f'padding:2px 10px; border-radius:999px; font-weight:600; '
                f'border:1px solid {cluster_color}55;">'
                f'{cluster_emoji} {cluster_label}</span>'
            )

        if es_om:
            status_badge = (
                '<span style="background:rgba(239,68,68,0.2); color:#fca5a5; font-size:0.72em; '
                'padding:3px 12px; border-radius:999px; font-weight:700; border:1px solid rgba(239,68,68,0.5);">'
                '🔴 NOT CITED — Recommended Gap</span>'
            )
            card_border = f"1px solid {cluster_color}55"
        else:
            status_badge = (
                '<span style="background:rgba(16,185,129,0.2); color:#6ee7b7; font-size:0.72em; '
                'padding:3px 12px; border-radius:999px; font-weight:700; border:1px solid rgba(16,185,129,0.5);">'
                '🟢 CITED IN MANUSCRIPT</span>'
            )
            card_border = "1px solid rgba(255,255,255,0.1)"

        metrics_html = f"""
        <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:10px; margin-bottom:12px; margin-top:12px;">
            <div style="background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
              <span style="font-size:0.70em; color:#94a3b8; display:block; font-weight:600; text-transform:uppercase;">Citations</span>
              <span style="font-weight:700; color:#f8fafc; font-size:1.0em;">📈 {paper['citationCount']}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
              <span style="font-size:0.70em; color:#94a3b8; display:block; font-weight:600; text-transform:uppercase;">Year</span>
              <span style="font-weight:700; color:#f8fafc; font-size:1.0em;">📅 {paper['year']}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
              <span style="font-size:0.70em; color:#94a3b8; display:block; font-weight:600; text-transform:uppercase;">Later Than Yours</span>
              <span style="font-weight:700; color:#f8fafc; font-size:1.0em;">📅 {es_posterior}</span>
            </div>
        """

        if es_om:
            metrics_html += f"""
            <div style="background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
              <span style="font-size:0.70em; color:#94a3b8; display:block; font-weight:600; text-transform:uppercase;">Relevance</span>
              <span style="font-weight:700; color:#f8fafc; font-size:1.0em;">⭐ {relevancia or 'High'}</span>
            </div>
            """
            if subtema:
                metrics_html += f"""
                <div style="background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
                  <span style="font-size:0.70em; color:#94a3b8; display:block; font-weight:600; text-transform:uppercase;">Subtopic</span>
                  <span style="font-weight:700; color:#f8fafc; font-size:1.0em;">🏷️ {subtema}</span>
                </div>
                """

        metrics_html += "</div>"

        box_html = ""
        if es_om and justificacion:
            box_html = f"""
            <div style="background:rgba(14,165,233,0.15); padding:16px; border-radius:8px; border-left:5px solid #0ea5e9;">
              <p style="margin:0; font-size:0.95em; line-height:1.6;">
                <b style="color:#38bdf8; font-size:1.02em;">💡 Why cite it:</b><br>
                <span style="color:#e2e8f0;">{justificacion}</span>
              </p>
            </div>
            """
        elif not es_om:
            box_html = """
            <div style="background:rgba(16,185,129,0.1); padding:10px 14px; border-radius:8px; border-left:4px solid #10b981;">
              <p style="margin:0; font-size:0.90em; color:#a7f3d0;">
                <b>✅ Citation Verified:</b> This paper is already cited in your manuscript's reference section.
              </p>
            </div>
            """

        st.markdown(
            f"""
<div style="background-color: rgba(255,255,255,0.06); padding:20px; border-radius:12px;
            border:{card_border}; margin-bottom:16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2); backdrop-filter:blur(15px);">
  <div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:6px;">
    <span style="font-size:1.3em;">{'🔴' if es_om else '🟢'}</span>
    <div style="flex:1;">
      <h4 style="margin:0 0 6px 0; color:#FFFFFF; font-weight:700;">{paper['title']}</h4>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        {status_badge}
        {cluster_badge}
      </div>
    </div>
  </div>
  <p style="color:#cbd5e1; font-size:0.92em; margin-bottom:8px; margin-top:8px;">
    👤 {paper['authors_display']} &nbsp;|&nbsp; 📅 Year: {paper['year']}
  </p>
  {metrics_html}
  {box_html}
</div>
""",
            unsafe_allow_html=True,
        )

    if año_paper_estudiado:
        st.caption(
            f"📅 Your article is from {año_paper_estudiado}. "
            "Those marked with ✅ are published later."
        )
