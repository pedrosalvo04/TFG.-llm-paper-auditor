# Paper 11: LLMs get lost in multi-turn conversation
LLMs get lost in multi-turn conversation

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "In this paper, we investigate the performance of large language models (LLMs) in multi-turn conversations and find that they often get lost in such scenarios. This work highlights the challenges faced by LLMs when handling complex conversational contexts." The abstract accurately reflects the main claim made in the introduction, which is supported by the experimental results presented in the paper.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta identifica la idea principal del abstract: los modelos se desorientan en conversaciones largas ("lost in conversation"). Confirma que los resultados experimentales respaldan esta afirmación.

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "Simulated conversations are not representative of human-AI conversations", "Simulation environment is simplistic and idealized", and "Conversations are guaranteed to end with sufficient information". These statements are explicitly mentioned in the 'Limitations' section.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La IA extrae las restricciones y limitaciones metodológicas que los autores mencionan en el manuscrito.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper focuses on empirical analysis of LLM behavior in multi-turn conversations rather than proposing new mathematical theorems or formal proofs. Therefore, there are no theoretical results to state assumptions and provide proofs for. According to the NeurIPS 2026 official criteria, Item 3 states: 'If you are including theoretical results, did you state the full set of assumptions of all theoretical results, and did you include complete proofs of all theoretical results?' Since there are no such results in this paper, it is not applicable to evaluate whether these items were met.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El veredicto ("N/A") es adecuado porque es un análisis empírico.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation. This repository contains the implementation of the simulation framework, the sharding pipeline, and the evaluation logic used to generate the results presented in the paper.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto menciona el repositorio oficial de Microsoft para reproducir el entorno simulado de sharding.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides a dedicated repository at https://github.com/Microsoft/lost_in_conversation. This repository contains the implementation of the simulation framework, the sharding pipeline, and the evaluation logic used to generate the results presented in the paper. According to the NeurIPS 2026 official criteria for Item 5 (Open Access to Data and Code), if any code/model URL is present, the answer should be 'Yes'. The provided URL grants access to the authors' own original code, which meets the requirement.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Valida el repositorio.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide sufficient details regarding the training and experimental settings. Specifically, important hyperparameters such as optimizer, learning rate, batch size, epochs, and iterations are missing. According to the NeurIPS 2026 official criteria for Item 6 (Experimental Setting/Details), it is required that all training details be specified in the main paper or supplementary materials. The lack of these critical details poses a transparency risk as it makes it difficult for other researchers to reproduce and verify the experiments.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo. La IA penaliza el artículo por no especificar el "optimizador, tasa de aprendizaje o epochs". Sin embargo, los autores no entrenan ningún modelo. Realizan una evaluación de modelos existentes (Llama, GPT-4o, etc.) mediante inferencia en simulaciones. Pedir hiperparámetros de entrenamiento a un trabajo que analiza el comportamiento de modelos ya entrenados es un error de contexto.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide error bars, confidence intervals, or any other form of statistical significance measures for the experiments. The pre-computed help indicates that 'Runs: NOT FOUND', and there is no explicit justification provided by the authors for omitting these statistics. According to the NeurIPS 2026 official criteria, if the paper only provides averages without error bars, p-values, or confidence intervals, the answer must be 'No'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El castigo es correcto: el paper presenta estimaciones puntuales sin varianza estocástica para sus modelos.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide sufficient information on the computer resources needed for each experimental run. The pre-computed help indicates that 'hardware/cluster: NOT FOUND' and 'time of execution: 136.65s, Characters analyzed: 156326'. However, there is no mention of the type of compute workers (CPU or GPU), internal cluster, or cloud provider, including relevant memory and storage.
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Alucinación Telemétrica. Como con OLMo 2, la penalización al paper es correcta (los autores no informan de su infraestructura de simulación). Sin embargo, la herramienta cita "time of execution: 136.65s, Characters analyzed: 156326" como datos faltantes del experimento científico. Estos números son, en realidad, metadatos de telemetría del propio script evaluador en Python al procesar el PDF.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper fails to include a dedicated 'Code of Ethics' statement or an explicit declaration of adherence to the NeurIPS Code of Ethics. According to the official criteria, this is required for all submissions as it ensures that authors have considered and adhered to ethical standards in their research.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El documento no incluye esta declaración.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper does not provide a direct path to negative societal impacts that would require a discussion of broader impacts. However, the research focuses on LLMs in multi-turn conversations, which could have implications for privacy and fairness if misused or deployed improperly. Given the nature of the work, it is still advisable for authors to consider potential harms and benefits, even if not explicitly required by the criteria.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA indica "N/A" porque "no hay camino directo a impactos negativos", pero luego menciona que el trabajo "podría tener implicaciones de privacidad y equidad si se usa mal". Si la IA sugiere que es "advisable" discutir esto, el ítem no debería ser "N/A". Debería ser "No" por no abordar los riesgos potenciales.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper does not present a high-risk artefact that could be misused for generating harmful content, enabling surveillance, synthesising dangerous information, or being weaponised. The research focuses on the behavior of large language models (LLMs) in multi-turn conversations and does not involve any direct path to misuse as defined by NeurIPS 2026 criteria.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El razonamiento es bueno. Se crea un entorno in-silico y un protocolo de prueba (sharding) para diagnosticar la amnesia conversacional de los LLMs, sin liberar una API generativa tóxica que requiera "salvaguardas".

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides a URL for the code repository: https://github.com/Microsoft/lost_in_conversation. The license type is explicitly stated as MIT, which is one of the specific licenses (MIT, Apache, CC) mentioned in the NeurIPS 2026 criteria. Therefore, the answer is 'Yes' and no further justification is required based on the pre-computed help provided.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA inventa que el repositorio se liberó con una "Licencia MIT", aunque esa sigla no está en el paper. Además, se excusa diciendo "based on the pre-computed help provided".

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors have created any new assets as part of this work. The paper focuses on using established, publicly available datasets and a semi-automated simulation pipeline. According to the NeurIPS 2026 official criteria for Item 13, if no new assets are created, the item is N/A.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo por incomprensión lectora. El modelo afirma que no se crean nuevos activos, pero el Apéndice C del artículo describe la creación del proceso "Semi-Automatic Sharding Process" y la generación de colecciones de pruebas que requieren documentación formal (Data/Model Cards). Esto debería haber sido un "No". La respuesta comienza con "The provided JSON summary".

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors have hired or compensated human workers to collect or label new data. The paper mentions the use of established, publicly available datasets and a semi-automated simulation pipeline where LLMs act as both users and assistants.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La deducción deductiva es válida: los agentes simulados extraen información de datasets públicos (Spider, GSM8K), sin usar crowdsourcing humano.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper does not involve any direct research with human subjects. It utilizes established, publicly available datasets such as HumanEval, Spider 1.0, GSM8K, ToTTo, and WMT 2019, alongside a semi-automated simulation pipeline where LLMs act as both the user and the assistant.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto identifica los benchmarks estandarizados y señala que la experimentación no incluye seres humanos.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper describes the usage of LLMs as an important component of the core methods in this research. Specifically, LLMs are used to simulate multi-turn conversations where they act both as users and assistants. This usage is critical for generating synthetic data and evaluating the behavior of LLMs in such scenarios.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Entiende que los LLMs evaluados funcionaron como usuarios simulados e interfaces, y las simulaciones in-silico justifican su uso en el estudio.


