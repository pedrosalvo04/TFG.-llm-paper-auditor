"""Componente de análisis del Estado del Arte (SOTA)"""
import streamlit as st
import pandas as pd

def render_sota_analysis(md_text):
    """Renderiza la sección de análisis SOTA"""
    st.markdown("---")
    st.subheader("📚 State of the Art Validation (SOTA)")
    
    if st.button("Run Literature Analysis"):
        with st.spinner("Connecting to Semantic Scholar and validating bibliography..."):
            resultado_sota = st.session_state.sota_analyzer.analyze_sota(md_text)
            
            if "error" not in resultado_sota:
                st.success("Analysis completed")
                
                st.markdown("### 📝 Conclusion")
                st.info(resultado_sota.get('conclusion_sota', ''))
                
                papers_omitidos = resultado_sota.get("papers_omitidos", [])
                df_papers = pd.DataFrame(resultado_sota.get("papers_analizados", []))
                año_paper_estudiado = resultado_sota.get("metadata", {}).get("año_paper_estudiado")
                
                if not df_papers.empty and papers_omitidos:
                    _render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)
                elif not papers_omitidos:
                    st.success("✅ No significant omissions detected in your bibliography.")
            else:
                st.error(f"Error performing SOTA analysis: {resultado_sota.get('error', 'Unknown error')}")

def _render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado):
    """Renderiza la tabla de papers no citados"""
    df_papers['authors_display'] = df_papers['autores'].apply(
        lambda x: ', '.join([a.get('name', '') for a in x[:2]]) + (' et al.' if len(x) > 2 else '') if isinstance(x, list) else 'N/A'
    )
    
    df_papers.rename(columns={'titulo': 'title', 'año': 'year', 'citas': 'citationCount'}, inplace=True)
    
    titulos_omitidos = {p['titulo'].lower().strip() for p in papers_omitidos}
    
    def es_omitido(titulo):
        titulo_lower = titulo.lower().strip()
        for omitido in titulos_omitidos:
            if omitido in titulo_lower or titulo_lower in omitido:
                return True
        return False
    
    df_papers['es_omitido'] = df_papers['title'].apply(es_omitido)
    df_no_citados = df_papers[df_papers['es_omitido'] == True]
    
    if not df_no_citados.empty:
        st.markdown("### 💡 Relevant Articles NOT Cited in Your Manuscript")
        st.caption(f"Found {len(df_no_citados)} articles you should consider citing")
        
        tabla_recomendaciones = []
        for _, paper in df_no_citados.iterrows():
            justificacion = ""
            relevancia = ""
            subtema = ""
            titulo_paper = paper['title'].lower().strip()
            
            for omitido in papers_omitidos:
                titulo_omitido = omitido['titulo'].lower().strip()
                if titulo_omitido in titulo_paper or titulo_paper in titulo_omitido:
                    justificacion = omitido.get('justificacion', '')
                    relevancia = omitido.get('relevancia', '')
                    subtema = omitido.get('subtema_relacionado', '')
                    break
            
            es_posterior = "✅ Sí" if año_paper_estudiado and paper['year'] > año_paper_estudiado else "❌ No"
            if not año_paper_estudiado:
                es_posterior = "?"
            
            tabla_recomendaciones.append({
                "Título": paper['title'],
                "Autores": paper['authors_display'],
                "Año": paper['year'],
                "Posterior": es_posterior,
                "Citas": paper['citationCount'],
                "Relevancia": relevancia,
                "Subtema": subtema,
                "Justificación": justificacion
            })
        
        df_recomendaciones = pd.DataFrame(tabla_recomendaciones)
        
        # Diseño de tarjetas PREMIUM con HTML/CSS para máximo contraste y estética
        for _, paper in df_recomendaciones.iterrows():
            st.markdown(f"""
<div style="background-color: rgba(255, 255, 255, 0.12); padding: 24px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); backdrop-filter: blur(15px);">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
<span style="font-size: 1.5em;">📄</span>
<h4 style="margin: 0; color: #FFFFFF; font-weight: 700; letter-spacing: 0.5px;">{paper['Título']}</h4>
</div>
<p style="color: #cbd5e1; font-size: 0.95em; margin-bottom: 16px; font-weight: 400;">
👤 {paper['Autores']} | 📅 Year: {paper['Año']}
</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px;">
<div style="background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
<span style="font-size: 0.75em; color: #94a3b8; display: block; font-weight: 600; text-transform: uppercase;">Relevance</span>
<span style="font-weight: 700; color: #f8fafc; font-size: 1.1em;">⭐ {paper['Relevancia']}</span>
</div>
<div style="background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
<span style="font-size: 0.75em; color: #94a3b8; display: block; font-weight: 600; text-transform: uppercase;">Citations</span>
<span style="font-weight: 700; color: #f8fafc; font-size: 1.1em;">📈 {paper['Citas']}</span>
</div>
<div style="background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
<span style="font-size: 0.75em; color: #94a3b8; display: block; font-weight: 600; text-transform: uppercase;">Later Than Yours</span>
<span style="font-weight: 700; color: #f8fafc; font-size: 1.1em;">📅 {paper['Posterior']}</span>
</div>
<div style="background: rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
<span style="font-size: 0.75em; color: #94a3b8; display: block; font-weight: 600; text-transform: uppercase;">Subtopic</span>
<span style="font-weight: 700; color: #f8fafc; font-size: 1.1em;">🏷️ {paper['Subtema']}</span>
</div>
</div>
<div style="background: rgba(14, 165, 233, 0.15); padding: 18px; border-radius: 8px; border-left: 5px solid #0ea5e9;">
<p style="margin: 0; font-size: 1em; line-height: 1.6;">
<b style="color: #38bdf8; font-size: 1.1em;">💡 Why cite it:</b><br>
<span style="color: #e2e8f0;">{paper['Justificación']}</span>
</p>
</div>
</div>
""", unsafe_allow_html=True)
        
        if año_paper_estudiado:
            st.caption(f"📅 Your article is from {año_paper_estudiado}. Those marked with ✅ are published later.")
        else:
            st.warning("⚠️ Could not detect your article's year. The 'Later than yours' column shows '?' for all articles.")
    else:
        st.success("✅ Your manuscript adequately cites the relevant literature.")
