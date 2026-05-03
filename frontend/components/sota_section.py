"""Componente de análisis del Estado del Arte (SOTA)"""
import streamlit as st
import pandas as pd

def render_sota_analysis(md_text):
    """Renderiza la sección de análisis SOTA"""
    st.markdown("---")
    st.subheader("📚 Validación del Estado del Arte (SOTA 2023-2026)")
    
    if st.button("Ejecutar Análisis de Literatura Reciente"):
        with st.spinner("Conectando con Semantic Scholar y validando bibliografía..."):
            resultado_sota = st.session_state.sota_analyzer.analyze_sota(md_text)
            
            if "error" not in resultado_sota:
                st.success("Análisis completado")
                
                st.markdown("### 📝 Conclusión")
                st.info(resultado_sota.get('conclusion_sota', ''))
                
                papers_omitidos = resultado_sota.get("papers_omitidos", [])
                df_papers = pd.DataFrame(resultado_sota.get("papers_analizados", []))
                año_paper_estudiado = resultado_sota.get("metadata", {}).get("año_paper_estudiado")
                
                if not df_papers.empty and papers_omitidos:
                    _render_missing_papers(df_papers, papers_omitidos, año_paper_estudiado)
                elif not papers_omitidos:
                    st.success("✅ No se detectaron omisiones significativas en tu bibliografía.")
            else:
                st.error(f"Hubo un error al realizar el análisis SOTA: {resultado_sota.get('error', 'Error desconocido')}")

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
        st.markdown("### 💡 Artículos Relevantes NO Citados en tu Manuscrito")
        st.caption(f"Se encontraron {len(df_no_citados)} artículos recientes que deberías considerar citar")
        
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
        
        st.dataframe(
            df_recomendaciones,
            hide_index=True,
            width='stretch',
            column_config={
                "Título": st.column_config.TextColumn("Título", width="large"),
                "Autores": st.column_config.TextColumn("Autores", width="medium"),
                "Año": st.column_config.NumberColumn("Año", width="small"),
                "Posterior": st.column_config.TextColumn("Posterior al tuyo", width="small"),
                "Citas": st.column_config.NumberColumn("Citas", width="small"),
                "Relevancia": st.column_config.TextColumn("Relevancia", width="small"),
                "Subtema": st.column_config.TextColumn("Subtema", width="medium"),
                "Justificación": st.column_config.TextColumn("Justificación", width="large")
            }
        )
        
        if año_paper_estudiado:
            st.caption(f"📅 Tu artículo es de {año_paper_estudiado}. Los marcados con ✅ son posteriores.")
        else:
            st.warning("⚠️ No se pudo detectar el año de tu artículo. La columna 'Posterior' muestra '?' para todos los artículos.")
    else:
        st.success("✅ Tu manuscrito cita adecuadamente la literatura reciente relevante.")
