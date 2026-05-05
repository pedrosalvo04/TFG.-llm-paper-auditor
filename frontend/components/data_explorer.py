# -*- coding: utf-8 -*-
"""Componente para explorar todos los datos extraídos por el auditor"""
import streamlit as st
import pandas as pd

def render_data_explorer(resultado):
    """
    Renderiza un explorador detallado de todos los datos extraídos.
    """
    st.markdown("---")
    st.header("🔍 Explorador de Datos Extraídos")
    st.caption("Esta sección contiene la información técnica detallada que el auditor ha identificado en el paper.")

    extracted = resultado.get("informacion_extraida", {})
    hybrid_hp = resultado.get("extracted_hyperparameters_hybrid", {})
    
    if not extracted and not hybrid_hp:
        st.warning("No hay datos detallados disponibles para este análisis.")
        return

    # Categorías en pestañas para no saturar
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚙️ Hiperparámetros", 
        "💻 Código y Datos", 
        "🔌 Hardware e Impacto", 
        "🧠 Arquitectura y Teoría",
        "⚖️ Ética y Humanos"
    ])

    # --- PESTAÑA 1: HIPERPARÁMETROS ---
    with tab1:
        st.subheader("Configuración de Entrenamiento")
        
        # Combinar datos de extracción básica y extracción híbrida
        hp_basic = extracted.get("hyperparameters", {})
        
        hp_data = {
            "Parámetro": [
                "Optimizer", "Learning Rate", "Batch Size", "Epochs / Steps", 
                "Warmup", "Weight Decay", "Betas", "Epsilon", "Random Seed"
            ],
            "Extracción RAG (Pesada)": [
                str(hybrid_hp.get("optimizer", "N/A")),
                str(hybrid_hp.get("learning_rate", "N/A")),
                str(hybrid_hp.get("batch_size", "N/A")),
                str(hybrid_hp.get("epochs", "N/A")),
                str(hybrid_hp.get("warmup_steps", "N/A")),
                str(hybrid_hp.get("weight_decay", "N/A")),
                str(hybrid_hp.get("betas", "N/A")),
                str(hybrid_hp.get("epsilon", "N/A")),
                str(hybrid_hp.get("random_seed", "N/A"))
            ],
            "Extracción General": [
                str(hp_basic.get("optimizer", "N/A")),
                str(hp_basic.get("learning_rate", "N/A")),
                str(hp_basic.get("batch_size", "N/A")),
                str(hp_basic.get("epochs", "N/A")),
                str(hp_basic.get("warmup", "N/A")),
                str(hp_basic.get("weight_decay", "N/A")),
                str(hp_basic.get("betas", "N/A")),
                str(hp_basic.get("epsilon", "N/A")),
                "N/A"
            ]
        }
        
        df_hp = pd.DataFrame(hp_data)
        st.table(df_hp)
        
        if hp_basic.get("vague_phrase") and hp_basic.get("vague_phrase") != "NOT FOUND":
            st.info(f"**Nota del autor:** \"{hp_basic['vague_phrase']}\"")

    # --- PESTAÑA 2: CÓDIGO Y DATOS ---
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Repositorio de Código")
            code = extracted.get("code", {})
            st.write(f"**URL:** {code.get('repository_url', 'NOT FOUND')}")
            st.write(f"**Dependencias:** {code.get('dependencies', 'NOT FOUND')}")
            st.write(f"**Instrucciones:** {'✅ Sí' if code.get('instructions') == 'yes' else '❌ No'}")
            if code.get("negative_phrase") and code.get("negative_phrase") != "NOT FOUND":
                st.warning(f"**Justificación No-Release:** {code['negative_phrase']}")
        
        with col2:
            st.subheader("Datasets")
            data = extracted.get("data", {})
            st.write(f"**Nombre:** {data.get('dataset_name', 'NOT FOUND')}")
            st.write(f"**Acceso/URL:** {data.get('access_url', 'NOT FOUND')}")
            st.write(f"**Preprocesamiento:** {data.get('preprocessing', 'NOT FOUND')}")
            st.write(f"**Particiones (Splits):** {data.get('splits', 'NOT FOUND')}")

        st.markdown("---")
        st.subheader("Licencias Identificadas")
        lic = extracted.get("licenses_extraction", {})
        st.write(f"**Activos detectados:** {', '.join(lic.get('assets_used', ['Ninguno']))}")
        st.write(f"**Licencias nombradas:** {', '.join(lic.get('licenses_named', ['Ninguna']))}")

    # --- PESTAÑA 3: HARDWARE E IMPACTO ---
    with tab3:
        hw = extracted.get("hardware", {})
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Recursos de Cómputo")
            st.write(f"**Hardware:** {hw.get('gpu_cpu', 'NOT FOUND')}")
            st.write(f"**Cantidad:** {hw.get('num_gpus', 'NOT FOUND')}")
            st.write(f"**Memoria:** {hw.get('memory', 'NOT FOUND')}")
            st.write(f"**Tiempo de entrenamiento:** {hw.get('time', 'NOT FOUND')}")
        
        with col2:
            st.subheader("Impacto Ambiental")
            st.write(f"**Huella de Carbono:** {hw.get('carbon_footprint', 'NOT FOUND')}")
            st.write(f"**Consumo Energético:** {hw.get('energy_consumption', 'NOT FOUND')}")
            st.write(f"**PUE:** {hw.get('pue', 'NOT FOUND')}")

    # --- PESTAÑA 4: ARQUITECTURA Y TEORÍA ---
    with tab4:
        arch = extracted.get("architecture", {})
        st.subheader("Detalles del Modelo")
        st.write(f"**Descripción:** {arch.get('description', 'NOT FOUND')}")
        st.write(f"**Pesos Disponibles:** {'✅ Sí' if arch.get('weights_available') == 'yes' else '❌ No'}")
        
        st.markdown("---")
        theory = extracted.get("theory_and_proofs", {})
        st.subheader("Fundamentos Teóricos")
        st.write(f"**Resultados Teóricos:** {theory.get('has_theoretical_results', 'N/A')}")
        st.write(f"**Supuestos (Assumptions):** {theory.get('assumptions_stated', 'NOT FOUND')}")
        st.write(f"**Pruebas Incluidas:** {theory.get('proofs_included', 'N/A')}")
        if theory.get("appendix_reference") and theory.get("appendix_reference") != "NOT FOUND":
            st.info(f"**Referencia Apéndice:** {theory['appendix_reference']}")

    # --- PESTAÑA 5: ÉTICA Y HUMANOS ---
    with tab5:
        llm = extracted.get("llm_usage_extraction", {})
        st.subheader("Uso de LLMs")
        st.write(f"**Modelos utilizados:** {', '.join(llm.get('models_used', ['Ninguno']))}")
        st.write(f"**Propósito:** {llm.get('purpose', 'NOT FOUND')}")
        
        st.markdown("---")
        human = extracted.get("human_subjects_extraction", {})
        st.subheader("Sujetos Humanos y Crowdsourcing")
        st.write(f"**Uso de humanos:** {'✅ Sí' if human.get('uses_human_annotation') == 'yes' else '❌ No'}")
        st.write(f"**Compensación:** {human.get('compensation_details', 'NOT FOUND')}")
        st.write(f"**Instrucciones provistas:** {'✅ Sí' if human.get('instructions_provided') == 'yes' else '❌ No'}")

        impact = extracted.get("broader_impacts_extraction", {})
        st.markdown("---")
        st.subheader("Impacto Social")
        st.write(f"**Sección de impacto:** {'✅ Sí' if impact.get('has_impact_statement') == 'yes' else '❌ No'}")
        st.write(f"**Temas discutidos:** {', '.join(impact.get('concerns_discussed', ['Ninguno']))}")
