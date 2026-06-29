# Paper 11: LLMs get lost in multi-turn conversation


**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The abstract and introduction claim that LLMs suffer from a 'lost in conversation' phenomenon, characterized by performance degradation in multi-turn, underspecified settings. The paper supports these claims through a systematic evaluation across 200,000+ simulated conversations, demonstrating a 39% average performance drop and identifying specific failure modes such as 'answer bloat' and 'loss-of-middle-turns'."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Asocia la hipótesis central con la métrica empírica probada. Extrae los datos del resumen original, señalando una caída promedio del rendimiento del 39% al evaluar más de 200,000 conversaciones simuladas.

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "Section 9, titled 'Limitations', explicitly states: 'Simulated conversations are not representative of human-AI conversations', 'Simulation environment is simplistic and idealized', 'Conversations are guaranteed to end with sufficient information', and 'Degradations observed are likely underestimates of real-world scenarios'."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Localiza directamente la Sección 9 y extrae las debilidades metodológicas literales expresadas por los autores, sin generar limitaciones genéricas.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper focuses on empirical analysis of LLM behavior in multi-turn conversations rather than proposing new mathematical theorems or formal proofs."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Comprende que el estudio analiza el comportamiento de los modelos de forma empírica mediante simulaciones, por lo que no requiere aportar axiomas formales ni derivaciones algebraicas matemáticas.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation, which includes the implementation of the simulation pipeline, the sharding process, and the evaluation logic used to generate the reported results."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Detecta el hipervínculo del repositorio proporcionado en el documento y verifica que contiene el código utilizado para el proceso de fragmentación (sharding).

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation. This repository contains the implementation of the simulation framework, the sharding pipeline, and the evaluation logic used to generate the results presented in the paper."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Valida el acceso abierto apoyándose en la presencia de la misma URL oficial del repositorio identificada en el ítem anterior.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper provides extensive documentation of experimental settings across the main text and appendices. Specifically, Appendix I (Task-specific Implementation details), Appendix K (Gradual Sharding Implementation), Appendix L (Temperature Experiment Implementation)... explicitly lists temperature settings (0.0, 0.5, 1.0), simulation counts (10 to 20 per pair), and performance thresholds (0.8)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Navega por los apéndices I, K y L para extraer hiperparámetros específicos, como el umbral de rendimiento de 0.8 y las temperaturas (0.0, 0.5, 1.0) de los modelos evaluados.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper fails to meet the NeurIPS 2026 criteria for statistical significance. While the authors report performance metrics such as 'average performance drop' and 'multi-turn performance average', they do not provide error bars, confidence intervals, or formal statistical significance tests (e.g., p-values or hypothesis testing) to accompany these results."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Penaliza que las métricas de aptitud o falta de confiabilidad se presenten como promedios absolutos de caída, sin reportar las medidas de varianza estocástica requeridas.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide sufficient information regarding the compute resources used for the experiments. According to the NeurIPS 2026 criteria, authors must indicate the type of compute workers (CPU/GPU), memory, and storage, as well as provide an estimate of the total compute required for the experimental runs. The provided text contains no mention of the hardware infrastructure, execution time, or efficiency metrics for the 200,000+ simulated conversations."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Sanciona la omisión de información sobre la infraestructura de hardware y el tiempo de ejecución absolutos necesarios para procesar las más de 200,000 conversaciones simuladas.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The authors have failed to include a dedicated 'Code of Ethics' statement or an explicit declaration of adherence to the NeurIPS Code of Ethics. While the paper conducts extensive human-in-the-loop simulations and utilizes human annotators for validation, there is no mention of IRB approval, ethical review processes, or compliance with the NeurIPS requirement regarding fair wages..."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Audita la falta de declaraciones éticas explícitas o de confirmación de salarios justos para los anotadores humanos involucrados en la validación manual, aplicando la normativa al pie de la letra.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "Section 7.1 'Implications for System and Agent Builders', 7.2 'Implications for LLM Builders', 7.3 'Implications for NLP Practitioners', and 7.4 'Implications for Users of Conversational Systems'."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Identifica que la extensa discusión en la Sección 7 sobre las implicaciones y fallos sistémicos de la tecnología suple la necesidad de debatir el impacto social o los posibles usos adversos.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper presents a diagnostic framework for evaluating LLM performance in multi-turn, underspecified conversations. The research focuses on measuring 'Aptitude' and 'Unreliability' through a simulation pipeline using existing, publicly available models (e.g., GPT-4o, Claude 3.7, Llama 3.1)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Determina que proponer un entorno de evaluación (benchmark) utilizando modelos públicos existentes no equivale a desplegar un nuevo modelo fundacional de alto riesgo que requiera implementar filtros de acceso.

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The repository at https://github.com/Microsoft/lost_in_conversation is associated with the authors' work and is released under the MIT License."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Alucinación fáctica. La herramienta asume que el repositorio utiliza una licencia MIT simplemente por estar alojado en GitHub. Dicha licencia no se menciona en ninguna parte del documento original.

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a comprehensive repository... The paper details the 'Semi-Automatic Sharding Process' in Appendix C and provides specific task-specific implementation details in Appendix I, ensuring that the new simulation assets are documented and accessible for reproduction."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Corrobora que las instrucciones detalladas del proceso de sharding en el Apéndice C sirven como marco documental estructurado para el nuevo entorno de simulación creado.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper relies on a fully automated simulation environment using LLMs as agents, judges, and strategy classifiers. While the 'human_subjects_extraction' section notes manual inspection and validation of shards, these tasks were performed by the authors as part of the research process rather than through crowdsourcing..."
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** La deducción es acertada al constatar que la inspección manual fue realizada por los propios autores y no mediante recolectores subcontratados. Sin embargo, la herramienta expone el nombre de una variable interna del sistema ("human_subjects_extraction") en su texto de salida, rompiendo el formato de la justificación (prompt leakage).

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The research utilizes established, publicly available datasets such as HumanEval, Spider 1.0, GSM8K... alongside a semi-automated simulation pipeline where LLMs act as both the user and the assistant."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Valida la exención dado que el experimento se ejecuta de forma in-silico con agentes virtuales, sin involucrar ensayos clínicos o sociales con humanos.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The methodology relies on a semi-automated sharding pipeline and a multi-agent simulation environment.' Furthermore, the 'llm_usage_extraction' section details that LLMs are used as a judge, user simulator, strategy classifier, answer extractor, and for the sharding process itself."
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Extrae correctamente los múltiples usos de los modelos de lenguaje como motor metodológico central (jueces, simuladores, clasificadores). No obstante, vuelve a incurrir en una fuga de instrucciones al filtrar una variable interna del sistema ("llm_usage_extraction") en la redacción de su justificación.