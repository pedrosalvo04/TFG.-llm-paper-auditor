# Paper 14: KAN: Kolmogorov-Arnold Networks
KAN: Kolmogorov-Arnold Networks

**Ítem 1. Claims**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo estructural severo. La IA emite un "N/A" y deja la justificación en blanco. Todo paper científico (y este no es la excepción, afirmando ser una alternativa a los MLPs) presenta claims sobre sus aportes. Omitir este ítem es una violación total a la auditoría.

**Ítem 2. Limitations**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo estructural y ceguera documental. Deja el ítem vacío con un "N/A". El documento original de KAN posee una Sección 6 explícita dedicada a sus debilidades ("KANs are currently slower than MLPs..."). Ignorarlo y no emitir texto invalida la evaluación.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The research is designed to improve interpretability and accuracy in scientific domains such as partial differential equations, knot theory, and physics." (Broader Impacts Extraction) and the paper provides a detailed explanation of the Kolmogorov-Arnold Representation Theorem. Additionally, the scaling laws are described: "Relationship between grid points, spline order, and approximation error" (Theory and Proofs). These theoretical foundations support the assumptions made in the research.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La extracción técnica es fáctica y buena. Identifica con rigor la base teórica (el Teorema de Representación de Kolmogorov-Arnold) y las leyes de escalado derivadas.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors have made their implementation publicly available. The repository URL is https://github.com/KindXiaoming/pykan, which contains the full implementation of Kolmogorov-Arnold Networks (KANs), including source code for model architecture, training loops, and specific scripts used to reproduce experiments." (Code)
- **Mi Valoración:** Correcto
- **Mi Justificación:** Acierta al recuperar el repositorio exacto provisto por los autores para garantizar la reproducibilidad.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides a GitHub repository URL: https://github.com/KindXiaoming/pykan, which contains the full implementation of Kolmogorov-Arnold Networks (KANs), including source code for model architecture, training loops, and specific scripts used to reproduce experiments. This aligns with the NeurIPS 2026 criteria that require authors to include the code needed to reproduce the main experimental results in the supplemental material or as a URL.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Veredicto y justificación buenos. Valida el acceso abierto basándose en el mismo repositorio de GitHub, sin recurrir a fugas de sistema en la redacción.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides detailed information about hyperparameters such as optimizer (LBFGS, Adam), learning rate (0.001, 0.0001), batch size (4096), and training steps ('200 per grid extension', '5000+5000 for images'). These details are crucial for understanding the experimental setup and can be found in the supplementary materials or within the paper itself.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extracción excepcional de los hiperparámetros matemáticos dispersos por el paper. Cita la configuración dual del optimizador (LBFGS, Adam) y la programación de pasos por extensión de grilla ("200 per grid extension").

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide error bars, confidence intervals, or any other form of statistical significance measures for the experiments. The pre-computed help indicates that 'Significance Tests: yes' but 'Runs: NOT FOUND'. According to the NeurIPS 2026 official criteria, if NO intervals/variance/runs found -> answer 'No' and set is_no_justified: false. Since no statistical measures are present in the paper, this constitutes a transparency risk as it does not allow readers to assess the reliability of the reported results.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El castigo metodológico es correcto (los resultados de ecuaciones y RMSE se dan como estimaciones puntuales sin medidas estadísticas).

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper mentions hardware but does not provide any metrics for total training time, per-sample efficiency, or environmental impact/CO2 emissions. The pre-computed help states that 'DETECTED hardware/cluster: NOT FOUND'. According to the NeurIPS 2026 official criteria, a 'Yes' is warranted if hardware is mentioned AND (total training time OR per-sample efficiency OR environmental impact/CO2 emissions) is provided. Since no such metrics are provided, this also constitutes a transparency risk.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Deniega la falta de tiempos de ejecución y eficiencia de buena forma, al señalar una omisión en los recursos de cómputo.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a GitHub repository with implementation details and scripts for reproducing experiments, aligning with NeurIPS Code of Ethics requirements. The paper does not contain any clear ethical red flags or harmful applications that would require an ethics statement or IRB discussion.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo Conceptual Lógico. La IA afirma que proveer un repositorio en GitHub es equivalente a "alinearse con el Código de Ética de NeurIPS". Publicar código atañe a la reproducibilidad, pero la ética en NeurIPS demanda evaluación de impactos sociales y privacidad, no subir un script a internet.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper focuses on improving interpretability and accuracy in scientific domains such as partial differential equations, knot theory, and physics. There is no direct path to negative societal impacts or potential malicious uses of the research. The broader impact discussion is not applicable given the nature of the work.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Deducción analítica bueno. Entiende que una arquitectura matemática de splines orientada a resolver física y teoría de nudos ("knot theory") no posee aplicaciones duales de riesgo social que exijan una evaluación de daños masivos.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Aunque el "N/A" es el veredicto idóneo (es un algoritmo matemático, no una API generativa tóxica), la IA vuelve a presentar un fallo estructural, dejando la celda de justificación totalmente en blanco y evadiendo su responsabilidad argumentativa.

**Ítem 12. Licenses**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Doble fallo estructural. Además de dejar la justificación vacía, el dictamen debió ser "Yes" o "No" evaluando si el repositorio de PyKAN proveía o no la licencia comercial/abierta en el documento. No puede ser un ítem no aplicable cuando hay software de por medio.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors are releasing new assets such as datasets, model weights, benchmarks, or software libraries created as part of this work. The paper mentions a GitHub repository with implementation details and scripts for reproducing experiments but does not explicitly state that these are new creations.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo e incomprensión. La IA declara que no se liberan nuevas librerías, ignorando que el propósito principal del documento es la presentación y liberación pública del paquete PyKAN, el cual constituye un activo de software fundacional primario. Reincide en justificar basándose en el "JSON summary".

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors have hired or compensated human workers to collect or label new data. The paper mentions the use of B-spline parametrization and symbolic regression techniques but does not provide any information about hiring or compensating human subjects for this research.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Un 'N/A' certero y lógico (se trata de regresión simbólica in-silico, no de anotadores humanos).

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper does not involve any direct research with human subjects. It focuses on the implementation and comparison of Kolmogorov-Arnold Networks (KANs) using existing, public datasets for training and testing purposes.
- **Mi Valoración:** Correcto
- **Mi Justificación:** "N/A" argumentado con solidez y pureza al constatar la ausencia de ensayos con pacientes o cohortes sociales.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly mentions the use of LLMs for certain components of its methodology, such as B-spline parametrization and symbolic regression techniques. According to the NeurIPS 2026 criteria, a declaration is required if LLMs are an important component of the core methods.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Alucinación Técnica Gravísima. La IA local otorga un "Sí" afirmando que la parametrización por B-splines y las técnicas de regresión simbólica ¡son LLMs! Confundir el modelado clásico de funciones a trozos (B-splines) con Modelos de Lenguaje Masivo (LLMs) revela una falla sistémica en el conocimiento de dominios de Machine Learning por parte de Qwen2.5.


