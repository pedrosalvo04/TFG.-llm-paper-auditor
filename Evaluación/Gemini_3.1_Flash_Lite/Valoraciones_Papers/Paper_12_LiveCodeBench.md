# Paper 12: LiveCodeBench
LiveCodeBench

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The abstract states: 'We introduce LiveCodeBench, a holistic and contamination-free evaluation of LLMs for code... We show that existing benchmarks are heavily contaminated... and that LiveCodeBench provides a more robust evaluation.' Section 5 (Results) and Section 5.1 (Avoiding Contamination) provide empirical evidence comparing model performance on LiveCodeBench versus traditional benchmarks like HumanEval, demonstrating that models which perform well on static benchmarks often show significant performance drops on LiveCodeBench, thereby supporting the claim of contamination in existing datasets.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta relaciona la afirmación del abstract sobre la contaminación de datos con las caídas de rendimiento. El artículo lo confirma con los resultados empíricos: "We show that existing benchmarks are heavily contaminated... And that LiveCodeBench provides a more robust evaluation".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 7, titled 'Limitations', explicitly addresses several constraints: 'Potential contamination in older benchmarks', 'Overfitting to HumanEval', 'Ambiguous problem descriptions in existing benchmarks', 'Insufficient tests in existing benchmarks', 'CodeForces problems are considerably more difficult than AtCoder and LeetCode', 'Long tests on CodeForces are truncated', 'Benchmark size (noise in small problem sets)', 'Focus on Python only', 'Robustness to prompts (lack of prompt tuning)', 'Problem domain (competition programming vs real-world)', 'GPT-4 (gpt-4-1106-preview) struggles with specific code execution tasks even with CoT', and 'Live nature of benchmark causes size to increase over time'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La IA extrae información clave. No solo resume, sino que enumera las debilidades técnicas del estudio, mencionadas por los autores en la Sección 7, como "Focus on Python only" y la advertencia de que "CodeForces problems are considerably more difficult than AtCoder".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper presents an empirical benchmark and evaluation framework for Large Language Models (LLMs) in code generation and execution tasks.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta clasifica correctamente la naturaleza del artículo. Un conjunto de evaluación (benchmark) empírico no implica el desarrollo ni la demostración formal de ecuaciones teóricas o teoremas matemáticos.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper describes the methodology for LiveCodeBench, including scraping, filtering, and evaluation, but does not provide a direct link to the authors' own implementation, code repository, or dataset release.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA identificó un falso negativo al afirmar que no se proporcionaba un enlace directo al repositorio. Sin embargo, en la primera página del PDF original, debajo de las afiliaciones de los autores, se encuentra la dirección "Website: https://livecodebench.github.io/". La herramienta no extrajo esta URL principal de reproducibilidad.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** No
- **Justificación Auditor:** The authors failed to provide a URL or explicit instructions for accessing the 'LiveCodeBench' codebase, the scraping scripts, or the curated dataset used for the experiments. According to the NeurIPS 2026 criteria, authors are expected to include the code, data, and instructions needed to reproduce the main experimental results either in the supplemental material or via a URL. While the paper describes the methodology for data collection and evaluation in detail, the absence of a repository link or a data release mechanism prevents independent verification of the benchmark's construction and the reported model performance, which is central to the paper's contribution.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** El Ítem 4 tiene un error técnico. Se penaliza injustificadamente al ignorar la URL corporativa del proyecto ("https://livecodebench.github.io/"), lo que lleva a una falsa acusación de opacidad en el acceso abierto.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides comprehensive experimental details in sections '4 Experiment Setup' and 'C Experimental Setup'. Specifically, the authors define the sampling strategy (nucleus sampling with temperature 0.2, top_p 0.95), the number of candidates per problem (10), and the specific filtering criteria for code execution (e.g., bytecode limit of 1000, runtime limit of 2 seconds, and constraints on integer/string operations). Furthermore, the authors specify the use of vLLM for the execution environment and provide a clear breakdown of the model classes and sizes evaluated (1.3B to 70B parameters).
- **Mi Valoración:** Correcto
- **Mi Justificación:** La IA identifica los parámetros de inferencia y la configuración del entorno en los apéndices. Las citas directas, como "nucleus sampling with temperature 0.2, top_p 0.95" y el uso de "vLLM", confirman la extracción.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper fails to report error bars, confidence intervals, or formal statistical significance tests for the reported performance metrics (Pass@1). According to the NeurIPS 2026 criteria, authors must provide information about the statistical significance of experiments supporting the main claims. While the paper presents extensive comparative results across 52 models, it lacks the necessary variance analysis or statistical rigor required to account for factors of variability in LLM evaluation. As the authors did not provide an explicit scientific or computational justification for this omission, the transparency requirement remains unmet.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo crítico por omisión de lectura. La herramienta acusa a los autores de ocultar la variabilidad y no justificarla. Sin embargo, el artículo especifica en la Sección 7: "We currently estimate a 1-1.5% performance variance [...] measured by bootstrapping problem sets". El bootstrapping es un método estadístico para estimar varianza, aceptado en NeurIPS.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide sufficient information regarding the computer resources used for the experiments. The NeurIPS 2026 criteria explicitly require the disclosure of the type of compute workers (CPU/GPU), memory, time of execution, and an estimate of the total compute required. Although the paper mentions the use of vLLM for execution, it fails to specify the underlying hardware infrastructure (e.g., specific GPU models, cluster configuration) or the total compute time/resources consumed for the evaluation of the 511 problems across 52 models. Consequently, the reproducibility of the experimental setup is compromised.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto aplica la normativa de NeurIPS. Señala que, a pesar de evaluar 52 modelos masivos, los autores no reportaron la infraestructura de hardware (tipo/cantidad de GPUs) ni las métricas de consumo temporal requeridas para las ejecuciones.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors explicitly state in the 'Data Collection' and 'Usage Policy' sections that the benchmark is intended for 'Academic purposes only' and that they have implemented strict measures to avoid paywalled or login-required content. Furthermore, they explicitly prohibit training on the collected problems to respect the intellectual property of the source platforms.
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El veredicto es positivo por el cumplimiento de los derechos de propiedad intelectual, lo cual es parcialmente correcto. Sin embargo, el razonamiento confunde la protección legal del copyright (evitar barreras de pago/paywalls) con las declaraciones de ética de investigación y riesgo humano del Código de Ética de NeurIPS.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper discusses the broader impact of the work in the context of 'Holistic Evaluation' and 'Contamination', stating: 'The benchmark aims to guide future research in code LLMs and mitigate contamination issues.'
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso positivo por sesgo léxico. La herramienta confunde el impacto académico positivo ("guide future research") con el requisito de NeurIPS de transparentar riesgos de impacto social negativo (usos maliciosos, doble uso, discriminación). El texto no menciona riesgos sociales, por lo que la respuesta correcta era "No".

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper introduces 'LiveCodeBench', a benchmark framework for evaluating Large Language Models on code generation, self-repair, and execution tasks. The research is foundational in nature, focusing on the methodology of contamination-free evaluation rather than the release of a high-risk generative model or a system capable of dual-use harm.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta diferencia la creación de un paquete evaluador (un benchmark inerte) de la publicación de un modelo fundacional generativo. Esto exime al artículo de necesitar salvaguardas de uso o restricciones de acceso.

**Ítem 12. Licenses**
- **Valoración Auditor:** No
- **Justificación Auditor:** The authors cite 'Fair Use § 107' as a legal justification for their data collection practices, but they fail to provide a specific, standard open-source license (such as MIT, Apache 2.0, or CC-BY) for the LiveCodeBench dataset or the associated code repository. The NeurIPS 2026 criteria explicitly require that authors cite the creators and respect the license and terms of use of existing assets. By failing to provide a clear, machine-readable, or standard license for their own released benchmark, the authors do not meet the transparency requirements for asset management and legal compliance.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto identifica la justificación legal del artículo ("Fair Use § 107 of the US Copyright Law" para la recolección). Sin embargo, señala que los autores no incluyeron una licencia estructurada explícita (ej. Apache, MIT) para el activo resultante.

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper introduces 'LiveCodeBench' as a new, dynamic benchmark for evaluating LLMs on code. In Appendix A (Dataset), the authors provide documentation regarding the collection methodology, the specific platforms scraped (LeetCode, AtCoder, CodeForces), the total number of problems (511), and the usage policy. Furthermore, the authors explicitly state in Appendix A.1 that the dataset is intended for 'Academic purposes only' and provide a justification based on Fair Use § 107 of the US Copyright Law.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El Apéndice A sirve como plantilla documental del nuevo activo, aportando los metadatos numéricos y operativos exigidos.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The research methodology for LiveCodeBench relies on automated scraping of publicly available competitive programming platforms and the use of GPT-4-Turbo for synthetic test case generation. There is no evidence of human subjects being recruited, compensated, or involved in the data collection or labeling process. As the study does not involve human labor or crowdsourcing, the requirements for documenting participant instructions, screenshots, or compensation are not applicable.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El marco no requiere validación. Se basa en el uso de scraping automatizado y generación de código in-silico, lo que elimina la necesidad de regulaciones laborales de crowdsourcing.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The research methodology involves the automated scraping of publicly available competitive programming platforms (LeetCode, AtCoder, CodeForces) and the use of LLMs for test case generation and evaluation. No human subjects were recruited, surveyed, or experimented upon during the course of this study.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Dictamen "N/A" porque el experimento no involucra intervención clínica o social con humanos.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly states in the methodology: 'GPT-4-Turbo used to generate tests for problems where platform tests were unavailable' and 'One-shot prompt templates used for synthesizing random and adversarial input generators.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto menciona que GPT-4-Turbo se usó para generar casos de prueba, lo que indica su dependencia instrumental en el paper.


