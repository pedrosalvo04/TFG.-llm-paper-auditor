# 🤖 NeurIPS 2026 Paper Auditor: Arquitectura y Flujo de Trabajo

Este documento describe detalladamente el funcionamiento interno del auditor de artículos científicos, desde la ingesta del documento hasta la generación del informe de cumplimiento final. El sistema utiliza una arquitectura de **Skills** (habilidades) coordinadas en un pipeline secuencial de **6 fases** (recientemente optimizado para evaluación contextual).

## 🌟 Descripción General
El **NeurIPS 2026 Paper Auditor** evalúa la transparencia y reproducibilidad de papers de IA/ML siguiendo los criterios oficiales de **NeurIPS 2026**. Su motor combina razonamiento Chain-of-Thought (CoT), arquitectura Map-Reduce para documentos extensos y una evaluación exhaustiva mediante mapeo inteligente de secciones.

## 🏗️ Arquitectura del Sistema
El sistema se basa en una arquitectura modular de servicios y habilidades:

- **Frontend (Streamlit)**: Orquesta la carga, visualización de fases en tiempo real y el dashboard final.
- **Auditor Service (`PaperAuditor`)**: El orquestador principal que gestiona el contexto y la ejecución secuencial de las fases.
- **Skills Layer**: Habilidades especializadas que ejecutan tareas atómicas de IA o cálculo determinista.
- **Prompt Engine**: Sistema centralizado de plantillas Markdown para garantizar respuestas estructuradas en JSON.

## 📊 Diagrama de Flujo del Agente

A continuación se detalla el flujo de datos y la lógica de decisión del agente auditor, desde la ingesta del documento hasta la generación del informe final.

```mermaid
graph TD
    subgraph "0. Motores Globales"
        PE["📄 Prompt Engine (Templates .md)"]
        PY["🐍 Lógica Python (Ayudas/Helps)"]
    end

    subgraph "1. Ingesta y Preprocesamiento"
        A["📄 PDF del Artículo"] --> B["🛠️ Docling Parser"]
        B --> C{"¿Markdown Generado?"}
        C -- "Sí" --> D["📝 Texto Estructurado"]
        C -- "No" --> E["❌ Error de Carga"]
    end

    subgraph "2. Fase de Extracción (InformationExtractionSkill)"
        D --> F["🧠 Segmentador de Secciones"]
        F --> G["📦 Fragmentos de Paper"]
        PE -. "map_extraction.md" .-> H
        G --> H["⚙️ Fase MAP (Extracciones Atómicas)"]
        PE -. "reduce_extraction.md" .-> I
        H --> I["⚙️ Fase REDUCE (Consolidación JSON)"]
        I --> J{"¿Es ML/AI?"}
        J -- "No" --> K["🛑 Abortar: INVALID_PAPER"]
        J -- "Sí" --> L["📋 Información Extraída Master"]
        D -- "Indexación" --> LS["🗂️ Diccionario de Secciones (Título/Texto)"]
    end

    subgraph "2.5. Mapeo Inteligente (SectionMappingSkill)"
        LS --> M1["🗺️ Router: Mapeo Items <-> Secciones"]
        PE -. "section_mapping.md" .-> M1
        M1 --> M2["📍 Mapa de Contexto (JSON)"]
    end

    subgraph "3. Fase de Evaluación (NeurIPSComplianceSkill)"
        PY -. "get_extraction_assistance_helps" .-> N1
        L --> N1["📡 Cálculo de Ayudas/Helps (Python)"]
        
        M2 & LS --> N3["📊 8 Pares High Context (Inyección de Texto Crudo)"]
        PE -. "evaluation_high_context.md" .-> N3
        
        N1 & N3 --> O["📄 Evaluación Consolidada Final"]
    end

    subgraph "4. Consolidación y Veredicto"
        O --> V["📊 Cálculo de Métricas"]
        V --> W["🧠 Lógica de Salud (Health Scoring)"]
        W --> X{"¿No's Justificados?"}
        X -- "Sí" --> Y["🟢 Veredicto: Válido"]
        X -- "No" --> Z["🔴 Veredicto: Desk Reject Risk"]
        Y & Z --> AA["🏁 JSON Maestro Final"]
    end

    AA --> AB["🎨 Dashboard Streamlit"]
```

---

### ⏱️ Cronología de Ejecución de Prompts
Para entender el flujo temporal del agente:
1.  **`map_extraction.md`** (Múltiple): Una vez por cada sección del paper.
2.  **`reduce_extraction.md`** (1 vez): Para consolidar los hechos.
3.  **`section_mapping.md`** (1 vez): Fase 1.5 para enrutar contexto a los 16 ítems.
4.  **`evaluation_high_context.md`** (8 veces): Evaluación profunda de los ítems agrupados en pares.

---

## 🚀 Pipeline de Auditoría: Detalle de las 5 Fases

### 1. Extracción General (`InformationExtractionSkill`)
Es la base del análisis. Utiliza un enfoque de **Map-Reduce** para procesar papers de cualquier longitud sin pérdida de contexto.

- **Inputs**: 
    - `paper_text` (Texto completo extraído por Docling).
- **Proceso**:
    - **Fase MAP (Extracción Segmentada)**: El paper se divide en secciones lógicas. Cada segmento se envía a un LLM para extraer entidades y contexto técnico.
    - **Indexación de Secciones**: Además de la extracción, esta fase ahora construye un **Diccionario de Secciones** (`paper_sections`) que vincula cada título (`# Heading`) con su texto crudo íntegro.
    - **Fase REDUCE (Consolidación)**: Unifica las extracciones y genera el objeto maestro `extracted_info`.
- **Outputs**: `extracted_info` (JSON global), `paper_sections` (Diccionario de texto crudo).

### 1.5. Mapeo de Contexto (`SectionMappingSkill`) [NUEVA FASE]
Actúa como un **Enrutador Inteligente** para dirigir el contexto adecuado a cada ítem del checklist.

- **Inputs**: 
    - Lista de títulos de secciones extraídos.
    - Criterios literales de NeurIPS 2026 para los 8 ítems de alto contexto.
- **Proceso**:
    - El LLM analiza los títulos y los mapea a los ítems (ej: asociar "4.1 Data Collection" al ítem de "Crowdsourcing").
    - **Regla de Granularidad**: El sistema prioriza automáticamente subsecciones específicas (4.1) sobre títulos genéricos (4) para evitar ruido.
- **Outputs**: `section_mapping` (JSON con el mapeo ítem -> [títulos]).

### 2. Evaluación NeurIPS Contextual (`NeurIPSComplianceSkill`)
Refactorizada para realizar un análisis profundo mediante inyección dinámica de fragmentos para TODOS los ítems.

- **Inputs**: 
    - `extracted_info` (JSON maestro y ayudas pre-calculadas).
    - `section_mapping` y `paper_sections`.
- **Proceso**:
    - **Pares High Context**: Los 16 ítems se agrupan en llamadas de 2 en 2. Para cada par, se busca el texto crudo en `paper_sections` según el mapeo y **se inyecta directamente en el prompt**.
    - **Análisis de Evidencia**: El evaluador lee el texto crudo del paper y las ayudas computadas para emitir su juicio "Yes/No".
- **Outputs**: `evaluation` (Checklist consolidado), `evaluation_helps`.

### 3. Consolidación de Métricas (`MetricsCalculationSkill`)
Fase de cálculo determinista para medir la eficiencia del proceso.

- **Inputs**: `paper_text`, `execution_time`.
- **Proceso**:
    - Calcula estadísticas de rendimiento: tiempo total, velocidad de procesamiento (tokens/segundo) y volumen de datos analizados.
- **Outputs**: `metrics` (Metadatos de rendimiento).

### 4. Generación de Informe Final (`MetadataAggregationSkill`)
Fase de cierre que consolida el conocimiento para el dashboard.

- **Inputs**: Todo el contexto acumulado de las fases 1-4.
- **Proceso**:
    - **Lógica de Veredicto (Health Score)**:
        - **🟢 Checklist Válido**: Si todos los "No" tienen una justificación válida extraída del paper (`is_no_justified: true`).
        - **🔴 Riesgo de Desk Reject**: Si hay ítems en "No" sin justificación del autor.
    - **Empaquetado**: Agrega metadatos finales y estructura el JSON final.
- **Outputs**: Objeto JSON final con veredicto, métricas, helps y checklist verificado.

---

## 🧠 Desarrollo Técnico de las Skills

A continuación se detalla la lógica interna de "bajo nivel" de cada componente del agente:

### 🔍 Skill de Extracción (Map-Reduce + Domain Triage)
Esta skill es la más compleja debido a la variabilidad de tamaño de los papers.
1.  **Segmentación Inteligente**: En lugar de usar trozos por caracteres, detecta los encabezados de Docling (`#`, `##`) para agrupar fragmentos por secciones reales (Abstract, Intro, Method, etc.).
2.  **Fase MAP**: Ejecuta llamadas paralelas al LLM (`Gemini 1.5 Flash`) para cada fragmento, extrayendo una mini-estructura JSON con contexto local.
3.  **Fase REDUCE**: Unifica las extracciones locales. Si hay discrepancias (ej. la Intro dice una cosa y los Apéndices otra), el prompt de REDUCE prioriza la evidencia técnica de las secciones de "Experimentación".
4.  **Triage de Dominio**: Realiza una clasificación tipo "zero-shot" para asegurar que el contenido es científico-técnico de IA.

### ⚖️ Skill de Cumplimiento (Evaluación Normativa)
Transforma hechos técnicos en cumplimiento de reglas NeurIPS.
1.  **Ayudas del Extractor (Helps)**: Antes de la evaluación profunda, un puente de Python lee el JSON de la Fase 1 y genera pistas de ayuda (`evaluation_helps`) sobre la presencia de palabras clave (ej. "MIT License", "GitHub", "p < 0.05") para pre-calentar al evaluador.
2.  **Chain-of-Thought (CoT)**: Obliga al LLM a generar un campo `thought_process` antes de decidir el estado `Yes/No`. Esto mejora drásticamente la precisión en criterios abstractos como "Broader Impacts".

### 🛡️ Skill de Verificación (Auditor 2 / Self-Correction)
Actúa como un filtro de calidad crítico.
1.  **Selección de Items**: No verifica todo el checklist para optimizar costes. Selecciona los 8 ítems más propensos al error o aquellos marcados como "No".
2.  **Ventana de Contexto Amplia**: A diferencia de la extracción, esta fase envía el ítem específico junto con una ventana de 60,000 caracteres (aprox. 15-20 páginas) para una búsqueda exhaustiva.
3.  **Lógica de Corrección**: Si el Auditor 2 encuentra evidencia que contradice la Fase 2, sobrescribe el estado y añade un flag `verified: true` y `was_corrected: true`, lo que se visualiza con un icono especial en el dashboard.

### 📊 Skills de Soporte (Métricas y Metadatos)
- **Métricas**: Calcula el rendimiento en tiempo total y volumen de datos, permitiendo auditar la eficiencia del sistema.
- **Metadatos**: Mapea las respuestas técnicas al esquema Pydantic `AuditState` para garantizar estabilidad en el frontend.
- **Veredicto**: Aplica la heurística de "Transparencia NeurIPS": un "No" solo es aceptable si el paper explica explícitamente la omisión (ej. "No proporcionamos código por razones de privacidad comercial").

---

## 🛠️ Tecnologías y Stack Técnico

- **LLM Core**: Familia **Gemini 3.1 Flash Lite** (optimizado para latencia y razonamiento técnico en JSON).
- **Context Handling**: Ventanas de hasta 1M tokens con técnicas de Map-Reduce y Ventanas Deslizantes.
- **PDF Intelligence**: **Docling (IBM)** para preservación de semántica y estructura Markdown.
- **Prompting**: Arquitectura **Markdown-to-JSON** con validación estricta de esquemas.
- **Frontend**: Streamlit 2026 con componentes personalizados en HTML/CSS para visualización de "signals".

## 📊 Ciclo de Vida del Contexto
1. **Raw Text**: 100% del documento (Docling).
2. **Context Mapping**: Identificación de anclas (Fase 1.5).
3. **Structured Context**: Extracción consolidada (Fase 2).
4. **Insights**: Dashboard visual final (Fase 4).

