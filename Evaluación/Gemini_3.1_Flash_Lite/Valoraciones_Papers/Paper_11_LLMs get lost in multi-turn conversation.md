# Paper 11: LLMs get lost in multi-turn conversation
LLMs get lost in multi-turn conversation

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The abstract and introduction claim that LLMs suffer from a 'lost in conversation' phenomenon, characterized by performance degradation in multi-turn, underspecified settings. The paper supports these claims through a systematic evaluation across 200,000+ simulated conversations, demonstrating a 39% average performance drop and identifying specific failure modes such as 'answer bloat' and 'loss-of-middle-turns'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta conecta la hipótesis principal con la métrica destructiva probada. Obtiene los datos del resumen original: "evaluating LLMs across 200,000+ simulated conversations... Demonstrating a 39% average performance drop".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 9, titled 'Limitations', explicitly states: 'Simulated conversations are not representative of human-AI conversations', 'Simulation environment is simplistic and idealized', 'Conversations are guaranteed to end with sufficient information', and 'Degradations observed are likely underestimates of real-world scenarios'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La IA extrae las confesiones metodológicas directamente de la Sección 9, sin añadir información.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper focuses on empirical analysis of LLM behavior in multi-turn conversations rather than proposing new mathematical theorems or formal proofs.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Entiende que es un estudio fenomenológico e in-silico sobre el comportamiento de modelos pre-entrenados, por lo que no necesita derivaciones algebraicas ni axiomas formales.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation, which includes the implementation of the simulation pipeline, the sharding process, and the evaluation logic used to generate the reported results.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El repositorio del PDF incluye el pipeline de fragmentación (sharding).

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation. This repository contains the implementation of the simulation framework, the sharding pipeline, and the evaluation logic used to generate the results presented in the paper.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Validado con el Ítem 4. La URL oficial del repositorio confirma el acceso abierto.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides extensive documentation of experimental settings across the main text and appendices. Specifically, Appendix I (Task-specific Implementation details), Appendix K (Gradual Sharding Implementation), Appendix L (Temperature Experiment Implementation)... explicitly lists temperature settings (0.0, 0.5, 1.0), simulation counts (10 to 20 per pair), and performance thresholds (0.8).
- **Mi Valoración:** Correcto
- **Mi Justificación:** La IA extrae información detallada. Revisa los apéndices I, K y L para documentar hiperparámetros específicos como el umbral de rendimiento (thresholds (0.8)) y las temperaturas de los LLM evaluados.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper fails to meet the NeurIPS 2026 criteria for statistical significance. While the authors report performance metrics such as 'average performance drop' and 'multi-turn performance average', they do not provide error bars, confidence intervals, or formal statistical significance tests (e.g., p-values or hypothesis testing) to accompany these results.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El trabajo aplica rigor científico. Aunque presenta muchos experimentos, las métricas (como "Aptitud" o "Falta de confiabilidad") se reportan como promedios absolutos de caída, sin la varianza estocástica que requiere NeurIPS.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide sufficient information regarding the compute resources used for the experiments. According to the NeurIPS 2026 criteria, authors must indicate the type of compute workers (CPU/GPU), memory, and storage, as well as provide an estimate of the total compute required for the experimental runs. The provided text contains no mention of the hardware infrastructure, execution time, or efficiency metrics for the 200,000+ simulated conversations.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Los autores mencionan generar "200,000+ simulated conversations" con modelos de frontera, pero no detallan la infraestructura ni el gasto energético que esto implica.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** No
- **Justificación Auditor:** The authors have failed to include a dedicated 'Code of Ethics' statement or an explicit declaration of adherence to the NeurIPS Code of Ethics. While the paper conducts extensive human-in-the-loop simulations and utilizes human annotators for validation, there is no mention of IRB approval, ethical review processes, or compliance with the NeurIPS requirement regarding fair wages...
- **Mi Valoración:** Correcto
- **Mi Justificación:** Falla al no mencionar declaraciones éticas explícitas ni salarios justos documentados, lo que requiere más transparencia.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 7.1 'Implications for System and Agent Builders', 7.2 'Implications for LLM Builders', 7.3 'Implications for NLP Practitioners', and 7.4 'Implications for Users of Conversational Systems'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La Sección 7 del artículo discute las derivaciones y fallos sistémicos de la tecnología, lo que aborda el impacto en la comunidad.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper presents a diagnostic framework for evaluating LLM performance in multi-turn, underspecified conversations. The research focuses on measuring 'Aptitude' and 'Unreliability' through a simulation pipeline using existing, publicly available models (e.g., GPT-4o, Claude 3.7, Llama 3.1).
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto entiende que un estudio centrado en la evaluación analítica in-silico no es lo mismo que implementar un nuevo modelo fundacional de alto riesgo que requiera filtros o restricciones de acceso para el usuario.

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The repository at https://github.com/Microsoft/lost_in_conversation is associated with the authors' work and is released under the MIT License.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Alucinación fáctica recurrente. La herramienta añade información externa. Asume que por estar en GitHub tiene una "MIT License". La cadena de caracteres "MIT" no aparece en el documento original.

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a comprehensive repository... The paper details the 'Semi-Automatic Sharding Process' in Appendix C and provides specific task-specific implementation details in Appendix I, ensuring that the new simulation assets are documented and accessible for reproduction.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Verifica los metadatos y las instrucciones del pipeline de sharding del Apéndice C.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper relies on a fully automated simulation environment using LLMs as agents, judges, and strategy classifiers. While the 'human_subjects_extraction' section notes manual inspection and validation of shards, these tasks were performed by the authors as part of the research process rather than through crowdsourcing...
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** La deducción lógica es correcta: la validación la realizaron los propios investigadores ("performed by the authors"), no recolectores externos. Sin embargo, hay un problema de exposición técnica. Al redactar "While the 'human_subjects_extraction' section notes", se expone el nombre de una variable interna de extracción del backend al usuario.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The research utilizes established, publicly available datasets such as HumanEval, Spider 1.0, GSM8K... alongside a semi-automated simulation pipeline where LLMs act as both the user and the assistant.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El experimento es in-silico, usando agentes virtuales que simulan humanos. Por lo tanto, valida la exención biomédica o social.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The methodology relies on a semi-automated sharding pipeline and a multi-agent simulation environment.' Furthermore, the 'llm_usage_extraction' section details that LLMs are used as a judge, user simulator, strategy classifier, answer extractor, and for the sharding process itself.
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El texto destaca el uso de LLMs como motor central (jueces, clasificadores, simuladores). Sin embargo, se le asigna "correcto" porque vuelve a mostrar un prompt leakage, filtrando la clave de sistema: "Furthermore, the 'llm_usage_extraction' section details...".


