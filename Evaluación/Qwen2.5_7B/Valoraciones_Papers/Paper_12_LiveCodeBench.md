# Paper 12: LiveCodeBench
LiveCodeBench

**Ítem 1. Claims**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper 'LiveCodeBench: A Holistic and Contamination-Free Evaluation of LLMs for Code' does not provide a clear statement in the abstract or introduction regarding its main claims... However, there is no explicit mention of what the paper aims to achieve or contribute.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo por ceguera documental. El modelo dice que no se menciona el objetivo del artículo. Sin embargo, el abstract y la introducción de LiveCodeBench indican claramente la creación de una plataforma de evaluación sin contaminación ("holistic and contamination-free evaluation of LLMs for code"). Ignorar estas afirmaciones metodológicas invalida el dictamen.

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The provided JSON summary lists several potential issues that could affect the robustness of the evaluation, including contamination in older benchmarks, overfitting to HumanEval, ambiguous problem descriptions... According to the NeurIPS 2026 official criteria, if any limitations are stated— even briefly—the answer should be |
- **Mi Valoración:** Correcto
- **Mi Justificación:** El veredicto es correcto ("Sí") y se identifican las limitaciones del paper: sobreajuste a HumanEval y problemas ambiguos.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not contain any specific information about the theoretical results, assumptions, or proofs in the paper... According to the NeurIPS 2026 official criteria for Item 3... Since no such information is provided, this item cannot be evaluated as 'Yes' or 'No', hence the answer is N/A.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El veredicto es correcto: al ser un artículo empírico (la presentación de un benchmark), no tiene que probar teoremas matemáticos puros ("N/A").

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide any URLs, instructions, or other means to reproduce the experimental results. According to the NeurIPS 2026 official criteria... The pre-computed help indicates that no code/model URLs were found, which is a critical requirement.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA marcó un falso negativo al indicar que no se proveen enlaces. En la primera página del artículo, bajo los autores, se encuentra el enlace: "Website: https://livecodebench.github.io/". La herramienta no detectó este enlace y atribuyó el problema a variables ocultas ("The pre-computed help indicates...").

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide any URLs or instructions that grant access to the authors' own original code, model weights, or newly collected datasets... The only mention of code is 'LiveCodeBench', but no URL or further details are provided.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Este punto tiene el mismo problema que el Ítem 4. Al no incluir el enlace matriz del proyecto ("https://livecodebench.github.io/"), que da acceso a los datos, se acusa de falta de transparencia sin motivo.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper lacks detailed information about hyperparameters such as optimizer type, learning rate, batch size, epochs, etc. These are crucial for understanding the model's configuration and training process. According to the NeurIPS 2026 official criteria, it is essential to specify all the training details.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA penaliza el artículo por no incluir "optimizadores, learning rates, epochs y batch sizes". Estos son parámetros de entrenamiento de modelos neuronales. LiveCodeBench evalúa la inferencia, no el entrenamiento de modelos. Los hiperparámetros de inferencia usados (temperatura 0.2, top_p 0.95, vLLM) están descritos en la Sección 4 del original.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide any information about error bars, confidence intervals, or statistical significance tests... The paper fails to meet this requirement as it does not provide any such measures, even though it mentions that the results are accompanied by a time of execution (143.37s) and character count (112564).
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo grave: Ceguera y alucinación telemétrica. Los autores calculan la varianza en la Sección 7, indicando "estimate a 1-1.5% performance variance [...] measured by bootstrapping problem sets". La IA no consideró este método. Además, incluyó metadatos del script Python (143.37s y 112564 caracteres) como si fueran resultados de los modelos evaluados.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper mentions that the type of compute workers used is 'vLLM for execution environment'... Additionally, it specifies the time of execution as 143.37s and the number of characters analyzed (112564), which can be used to estimate the computational load.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Alucinación Absurda y Falso Positivo. Qwen2.5 responde "Sí", basándose en que los autores especifican el tiempo de ejecución y la carga de cómputo. Su "evidencia" es que se tardó "143.37s" y se procesaron "112564 caracteres". El modelo interpretó que a los autores les tomó 2 minutos evaluar 52 modelos (Llama 3 70B, GPT-4, etc.) resolviendo 511 problemas algorítmicos.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper does not explicitly mention an 'Ethics Statement' or a dedicated section on broader impacts. However, the authors have taken several steps to ensure ethical considerations are addressed... implemented strict measures to avoid paywalled content and prohibit training on collected problems to respect intellectual property rights (see code_of_ethics -> prohibit_training_on_collected_problems).
- **Mi Valoración:** Correcto
- **Mi Justificación:** El dictamen es aceptable porque reconoce que los autores cumplen con la propiedad intelectual.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not discuss potential negative societal impacts of its work. While the focus on a contamination-free evaluation is positive, it does not address any potential harms or unintended uses that could arise from the technology.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Qwen2.5 entiende que crear algo útil para la comunidad ("contamination-free evaluation") no exime a los investigadores de discutir los posibles usos maliciosos (unintended uses). En esta prueba, su análisis semántico fue más claro que el de Gemini.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper 'LiveCodeBench: A Holistic and Contamination-Free Evaluation of LLMs for Code' does not present a high-risk artefact that could be misused, such as generating harmful content, enabling surveillance... The primary focus is on evaluating language models for code generation tasks in a controlled manner.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Deducción analítica buena. Entiende que crear un benchmark inerte de evaluación automatizada no es lo mismo que desplegar un modelo generativo tóxico de alto riesgo que necesite restricciones.

**Ítem 12. Licenses**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not explicitly provide a specific open-source license such as MIT, Apache, or CC. Instead, it mentions 'Fair Use § 107' and states that no standard open-source license is provided. According to the NeurIPS official criteria for licenses, if no specific license (MIT, Apache, CC) is named, the answer should be 'No'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto penaliza que los autores no especificaran una licencia de software estructurada (MIT, Apache) para el benchmark que liberan, a pesar de identificar el uso de la excusa legal "Fair Use § 107" del copyright de EE. UU. para el escrapeo web.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors are releasing new assets such as datasets, models, or benchmarks. The paper focuses on evaluating existing LLMs for code generation and execution tasks using a newly created benchmark called LiveCodeBench. Since no new assets are being released as part of this work, Item 13 (Assets) does not apply.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA afirma que los autores usan "a newly created benchmark called LiveCodeBench" y luego dice que "ningún activo nuevo está siendo liberado". El benchmark es un activo clave de la investigación y requería documentación (Data Cards). Este error, junto con la mención inicial de "The provided JSON summary", invalida la revisión.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary indicates that the paper does not involve hiring or compensating human workers to collect or label new data. The authors mention using existing, public datasets and do not provide any information about conducting new human research or paying workers.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La deducción es correcta. El uso de scraping automatizado en plataformas públicas de algoritmia y la asistencia de LLMs sintéticos evita la normativa de subcontratación humana (crowdsourcing).

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper 'LiveCodeBench: A Holistic and Contamination-Free Evaluation of LLMs for Code' does not involve any direct research with human subjects. The authors are reusing existing, public datasets such as AtCoder, LeetCode, and CodeForces to evaluate the performance of language models...
- **Mi Valoración:** Correcto
- **Mi Justificación:** No hay ensayos clínicos y el procesamiento se hizo con repositorios virtuales.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper 'LiveCodeBench: A Holistic and Contamination-Free Evaluation of LLMs for Code' uses language models, specifically GPT-4-Turbo, in a significant way. The authors mention that these models were used to generate tests for problems where platform tests were unavailable (llm_usage_extraction -> GPT-4-Turbo: Used to generate tests...)
- **Mi Valoración:** Correcto
- **Mi Justificación:** GPT-4-Turbo fue muy útil para generar casos de prueba en la investigación.


