# Paper 12: LiveCodeBench


**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper's claims in the abstract and introduction accurately reflect the paper's contributions and scope. The authors state that LiveCodeBench is a holistic and contamination-free benchmark for evaluating code capabilities, which aligns with their empirical findings presented in the results section (Section 5). Specifically, they claim to address issues of data contamination by using live updates and time-segmented evaluations, as evidenced by Figure 1. The paper also claims that current benchmarks like HumanEval may be subject to overfitting due to insufficient tests and ambiguous problem descriptions, which is supported by their findings in Section 5 (e.g., Figure 5)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Conecta la afirmación principal del abstract sobre la contaminación de datos con las caídas de rendimiento documentadas empíricamente. Cita de forma acertada la propuesta de los autores ("holistic and contamination-free benchmark") y lo respalda con la evidencia de las Figuras 1 y 5.

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper explicitly includes a 'Limitations' section (Section 7) that discusses several limitations, including benchmark size, focus on Python, robustness to prompts, and problem domain. For example, the authors mention that LiveCodeBench currently only focuses on Python, which might not provide enough signal about model capabilities in other languages (Section 7)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extrae la lista de debilidades técnicas descritas por los autores en la Sección 7, identificando barreras reales como el enfoque único en Python ("focus on Python") y la falta de ajuste de prompts.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper does not contain any theoretical results, proofs, or assumptions. The focus of the work is on empirical evaluation and benchmarking of large language models for code generation tasks. Since there are no theoretical contributions in this paper, the criteria related to theory, assumptions, and proofs do not apply. This is consistent with the official NeurIPS 2026 criteria which state that items should be evaluated only if relevant."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Clasifica la naturaleza del artículo basándose en los hechos, entendiendo que presentar un conjunto de evaluación empírico y un benchmark de programación no implica el desarrollo ni la demostración formal de ecuaciones teóricas.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any code or model URLs, and the authors have not made their own implementation or data publicly accessible. The only information provided is that the dataset was scraped from public websites (LeetCode, AtCoder, CodeForces) under certain conditions. However, this does not meet the requirement for making experimental results reproducible as stated in the NeurIPS 2026 criteria. Specifically, the authors should have either released their own code or provided detailed instructions on how to replicate the experiments."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo por omisión de lectura. La herramienta afirma que no se provee un enlace directo al repositorio. Sin embargo, en la primera página del PDF original, justo debajo de los autores, consta textualmente: "Website: https://livecodebench.github.io/". La IA no detectó la URL principal de reproducibilidad del proyecto.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any URLs or instructions for accessing the authors' own original code, model weights, or newly collected datasets used for the main experiments. The experimental setup section mentions evaluating various models across different sizes and classes, but it does not include links to the authors' repositories or detailed instructions on how to access their data and code. This omission poses a transparency risk as it makes it difficult for other researchers to reproduce the results. While the paper cites third-party dependencies such as LeetCode, AtCoder, and CodeForces for problem sources, these are insufficient to meet the criteria for open access to data and code."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Arrastra de forma directa el fallo técnico del Ítem 4. Al ignorar la URL pública del proyecto que da acceso a la plataforma, emite una penalización apoyada en una premisa falsa.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "We describe the experimental setup in this section. First, we provide the common setup across the scenarios, followed by the scenario-specific setups in Section 4.1. Models. We evaluate 52 models across various sizes, ranging from 1 . 3B to 70B, including base models, instruction models, and both open and closed models. Our experiments include models from different classes... Evaluation Metrics. We use the Pass@ 1 (Kulal et al., 2019; Chen et al., 2021) metric for our evaluations. Specifically, we generate 10 candidate answers for each problem either using API or using vLLM (Kwon et al., 2023). We use nucleus sampling with temperature 0 . 2 and top p 0 . 95 and calculate the fraction of programs or answers that are correct..."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Rastrea y extrae los parámetros de inferencia. Localiza el esquema de muestreo utilizado ("nucleus sampling with temperature 0.2, top p 0.95") y la métrica de evaluación principal (Pass@1), aunque pega el texto en crudo sin sintetizar la explicación.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any error bars, confidence intervals, or statistical significance tests for the experiments. The results are reported as averages without any indication of variability or uncertainty. This lack of statistical measures makes it difficult to assess the robustness and reliability of the experimental findings. According to the official criteria, this is a requirement for reporting experiment results in NeurIPS 2026. <br><br> ⚠️ Falta justificación explícita del autor para la respuesta 'No'"
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo. Acusa a los autores de ocultar la variabilidad y no aportar pruebas de significancia, ignorando la Sección 7, donde el artículo especifica de forma textual: "We currently estimate a 1-1.5% performance variance [...] measured by bootstrapping problem sets". El bootstrapping es un método de re-muestreo válido para calcular la varianza estadística según los estándares de NeurIPS.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments. While it mentions the models evaluated and some evaluation metrics, there is no detail provided about the hardware or computational requirements for running these experiments. This omission makes it challenging for other researchers to replicate the results, which is a critical aspect of scientific transparency in machine learning research."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Penaliza con base empírica que, a pesar de evaluar la inferencia de 52 modelos de lenguaje masivos, los autores omitieron por completo reportar la infraestructura de hardware empleada (ej. número de GPUs) y las métricas de consumo temporal necesarias para dichas ejecuciones.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper does not explicitly mention an 'Ethics Statement' or a dedicated section on broader impacts. However, the authors have demonstrated awareness of ethical considerations by addressing potential harms and limitations in their work. Specifically, they discuss issues such as problem set contamination, overfitting to existing benchmarks, and the need for more comprehensive evaluation scenarios (e.g., different programming languages, real-world usage). These discussions align with the NeurIPS Code of Ethics, particularly under 'Societal Impact and Potential Harmful Consequences' and 'Impact Mitigation Measures'. The authors have shown a commitment to transparency and ethical research practices by acknowledging these limitations and proposing solutions."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Confusión conceptual. La IA asume que discutir el "sobreajuste a benchmarks" (overfitting) y la "contaminación de datos" demuestra consciencia sobre el Código de Ética de NeurIPS. Estos son problemas técnicos de metodología del aprendizaje automático, no riesgos morales sobre sujetos humanos, privacidad o impacto dañino a la sociedad que es lo que regula el código de ética.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper discusses potential negative societal impacts, such as overfitting to existing benchmarks (which could lead to misuse) and the need for more comprehensive evaluation scenarios. The authors also highlight the importance of evaluating LLMs on a broader range of capabilities beyond just code generation, which is crucial for understanding their real-world applicability and limitations."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso positivo por sesgo léxico. Vuelve a confundir un problema puramente académico (la limitación y contaminación de un benchmark de código) con el requerimiento estricto del comité, que exige transparentar riesgos de impacto social negativo a nivel civil o de seguridad (ej. usos duales maliciosos). El artículo no aborda este tipo de repercusiones sociales.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper focuses on the evaluation of large language models for code generation and does not involve releasing a model with high risk for misuse. The work is primarily theoretical and foundational, aiming to evaluate LLMs across various scenarios such as code generation, self-repair, and test case output prediction. Given that the primary objective is academic research rather than practical deployment, there is no need for explicit access restrictions or usage guidelines. Therefore, answering 'N/A' aligns with the official criteria which state that safeguards are not required for theoretical or low-risk work."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Distingue la creación de un entorno de evaluación automatizado (benchmark inerte) del entrenamiento y publicación de un modelo fundacional de alto riesgo, eximiendo lógicamente al documento de implementar barreras de acceso (salvaguardas).

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper states: 'We scrape only the problem statements, ground-truth solutions, and test cases from competition websites LeetCode , AtCoder , and CodeForces . Further, we only scrape publicly visible portions of websites, avoiding any data collection that might be paywalled or require login or interaction with the website. Following, Hendrycks et al. (2021) we abide by Fair Use § 107: 'the fair use of a copyrighted work, including such use by ... scholarship, or research, is not an infringement of copyright', where fair use is determined by 'the purpose and character of the use, including whether such use is of a commercial nature or is for nonprofit educational purposes', 'the amount and substantiality of the portion used in relation to the copyrighted work as a whole', and 'the effect of the use upon the potential market for or value of the copyrighted work.' Finally, we use the collected problems for academic purposes only and in addition, do not train on the collected problems.'"
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo jurídico y conceptual. La IA otorga un "Sí" usando como justificación un párrafo donde los autores se amparan en el "Fair Use § 107" (Uso Justo) de Estados Unidos para poder hacer scraping de las webs. El Uso Justo es una defensa contra infracciones de copyright, no una licencia de software libre u open-source explícita (como MIT, Apache o CC-BY) adjuntada al activo final que los autores distribuyen en su repositorio.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper does not appear to introduce any new datasets, models, benchmarks, or software libraries. The assets mentioned (problems collected from LeetCode, AtCoder, and CodeForces) are reusing existing public resources without creating new ones. Therefore, this item is N/A as per the official criteria."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo. La IA asume que recolectar y reutilizar problemas de sitios públicos anula la existencia de un activo nuevo. LiveCodeBench es, por definición en el artículo, un nuevo benchmark dinámico curado de 511 problemas. Al liberar esta plataforma a la comunidad, la normativa exige que vaya acompañada de documentación estructurada.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not mention hiring or compensating human workers to collect or label new data. The datasets used are scraped from publicly available websites, and no new human-derived data was created for this research. Hence, the authors did not engage in crowdsourcing activities as defined by the NeurIPS criteria. <br><br> ⚠️ Falta justificación explícita del autor para la respuesta 'No'"
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Verifica con la evidencia del artículo que los datos se extrajeron automáticamente (scraping) sin utilizar trabajadores humanos subcontratados. Sin embargo, la asignación final falla: si el estudio no está diseñado con encuestas humanas, la regla no aplica y el dictamen correcto en la checklist debía ser "N/A", no un "No" penalizador.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper does not involve any direct research with human subjects. It primarily focuses on evaluating large language models (LLMs) using curated code problems from public platforms such as LeetCode, AtCoder, and CodeForces. The data used is publicly available and scraped for academic purposes only, adhering to the Fair Use guidelines. Therefore, no new IRB approval is required according to NeurIPS 2026 criteria."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Dictamen argumentado con base en la ausencia de interacción médica, clínica o social con humanos a lo largo de los experimentos.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper extensively uses LLMs as a core component of the methodology, particularly in generating synthetic code problems and self-repair scenarios. For instance, the paper mentions 'self-repair' as one of the key evaluation scenarios (see context mapping). This indicates that LLMs are not merely used for writing or editing but are integral to the research methods."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Búsqueda precisa de la dependencia instrumental en el desarrollo de la investigación. Señala que los LLM se usaron para estructurar escenarios fundamentales de evaluación ("self-repair scenarios").