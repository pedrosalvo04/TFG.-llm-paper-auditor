# Flujo de Trabajo: Auditoría con Criterios Personalizados (Modo Libre)

Este documento detalla el ciclo de vida de una auditoría cuando el usuario selecciona el **Modo de Criterios Libres** en la aplicación. La arquitectura está diseñada para ser completamente agnóstica a los criterios, adaptando todas las fases del pipeline dinámicamente.

---

## 1. Entrada de Datos (Frontend)
El proceso comienza en la interfaz de usuario (`app.py` y `file_uploader.py`).
1. **Selección de Modo:** El usuario marca la opción "Criterios Libres".
2. **Carga de Criterios:** Se habilita un *uploader* secundario donde el usuario sube un archivo (PDF, TXT, o Markdown) que contiene las directrices a evaluar (ej. `criterios_prueba.md`).
3. **Carga del Paper:** El usuario sube el artículo científico a auditar.
4. **Inyección al Contexto:** Ambos documentos se extraen como texto plano y se pasan al método `audit` del orquestador (`PaperAuditor`) junto con la bandera `criteria_mode="free"`.

---

## 2. Fase 0: Estructuración de Criterios (`CriteriaExtractionSkill`)
Dado que el texto de los criterios es completamente libre e inestructurado, la primera tarea del LLM es darle sentido.
- **Acción:** Se envía el texto crudo al LLM mediante el prompt `0. criteria_extraction.md`.
- **Salida:** El LLM devuelve un diccionario JSON donde cada clave es un identificador corto (ej. `objective_clarity`) y el valor es la descripción técnica de la regla proporcionada por el usuario.
- **Contexto:** Este diccionario se guarda en la variable `custom_criteria` del contexto global.

---

## 3. Fase 1: Análisis General y Contexto (`InformationExtractionSkill`)
Esta fase escanea el paper en su totalidad para extraer su estructura base y contexto fundamental.
- **Map-Reduce:** El paper se trocea en grandes fragmentos (Map) y luego se consolida (Reduce) para extraer información general como el tipo de paper, URLs, metadatos, hardware detectado, etc.
- **Extracción de Secciones:** Se almacena un índice con todas las secciones estructurales del paper identificadas por Docling (o expresiones regulares), dejando los textos de cada sección listos para fases posteriores.

---

## 4. Fase 1.5: Mapeo de Secciones (`SectionMappingSkill`)
Aquí ocurre la magia del **High Context** (Alto Contexto).
- **Acción:** El sistema envía al LLM la lista de títulos de las secciones del paper y la lista de los `custom_criteria` generados en la Fase 0 (usando el prompt dinámico `3a. section_mapping.md`).
- **Objetivo:** Para cada criterio, el LLM decide qué secciones del paper contienen probablemente la respuesta a esa métrica.
- **Salida:** Un JSON que vincula cada criterio con un máximo de 3 títulos de secciones relevantes del paper.

---

## 5. Fase 2: Evaluación Dinámica (`NeurIPSComplianceSkill`)
En esta fase se genera el veredicto para cada métrica ("Yes", "No", o "N/A"), iterando de forma paralela y fragmentada para evitar la saturación del contexto del LLM.
- **Procesamiento en Lotes:** El orquestador toma todos los `custom_criteria` y los divide en **grupos de 2 en 2**.
- **Inyección de Alto Contexto:** Para los 2 ítems en curso, el sistema consulta el mapeo de la Fase 1.5. A continuación, extrae el texto exacto y literal de esas secciones específicas del paper y lo inyecta en el prompt.
- **Generación de Prompt Genérico:** Utiliza el template `3c. evaluation_high_context.md`. Como estamos en modo libre, las instrucciones estrictas de NeurIPS se eliminan de la petición y el LLM adopta el rol de `"Senior AI Auditor"`, guiándose **exclusivamente** por las descripciones de los criterios que extrajimos en la Fase 0.
- **Salida:** Para cada métrica, el modelo devuelve un veredicto, una justificación detallada y evidencia extraída del texto inyectado.

---

## 6. Fase 3 y 4: Métricas y Agregación Final
- **Métricas (`MetricsCalculationSkill`):** Se calcula el tiempo de ejecución y el volumen de datos procesados.
- **Consolidación (`MetadataAggregationSkill`):** El sistema recopila los resultados generados en las diferentes fases. **Nota importante:** En modo libre, esta skill no depende de claves fijas (como las 16 reglas de NeurIPS); por el contrario, itera dinámicamente sobre todas las claves encontradas en la evaluación, asegurando que ningún criterio personalizado se pierda en el reporte final.

---

## 7. Salida y Renderizado (Frontend)
El diccionario global enriquecido vuelve al frontend (`audit_results.py`).
- **Veredicto:** El componente de la UI itera sobre todas las respuestas obtenidas. Si encuentra un "No" que no esté justificado (`is_no_justified: false`), marcará el estado global como "Atención Requerida".
- **Generación de Reportes:** Se compilan dinámicamente tanto el HTML que ves en pantalla como el PDF descargable, pintando los nombres de tus propios criterios como filas de la tabla principal y obviando cualquier "alert warning" específico de NeurIPS.
