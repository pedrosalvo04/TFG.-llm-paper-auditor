# Paper 14: KAN: Kolmogorov-Arnold Networks
KAN: Kolmogorov-Arnold Networks

**Ítem 1. Claims**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA devuelve "N/A" y deja la justificación en blanco. Los papers científicos, incluido este que se presenta como alternativa a los MLPs, siempre exponen sus aportes. No incluir este punto es un fallo grave en la auditoría.

**Ítem 2. Limitations**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** El ítem está vacío con un "N/A". El documento original de KAN incluye una Sección 6 que detalla sus debilidades ("KANs are currently slower than MLPs..."). No incluir esta información invalida la evaluación.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The research is designed to improve interpretability and accuracy in scientific domains such as partial differential equations, knot theory, and physics." (Broader Impacts Extraction) and the paper provides a detailed explanation of the Kolmogorov-Arnold Representation Theorem. Additionally, the scaling laws are described: "Relationship between grid points, spline order, and approximation error" (Theory and Proofs). These theoretical foundations support the assumptions made in the research.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La extracción técnica es correcta. Identifica la base teórica (el Teorema de Representación de Kolmogorov-Arnold) y las leyes de escalado derivadas.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors have made their implementation publicly available. The repository URL is https://github.com/KindXiaoming/pykan, which contains the full implementation of Kolmogorov-Arnold Networks (KANs), including source code for model architecture, training loops, and specific scripts used to reproduce experiments." (Code)
- **Mi Valoración:** Correcto
- **Mi Justificación:** Usa el repositorio exacto que los autores proporcionaron, lo que asegura la reproducibilidad.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides a GitHub repository URL: https://github.com/KindXiaoming/pykan, which contains the full implementation of Kolmogorov-Arnold Networks (KANs), including source code for model architecture, training loops, and specific scripts used to reproduce experiments. This aligns with the NeurIPS 2026 criteria that require authors to include the code needed to reproduce the main experimental results in the supplemental material or as a URL.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El veredicto y la justificación son buenos. Valida el acceso abierto usando el mismo repositorio de GitHub, sin recurrir a fugas de sistema en la redacción.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides detailed information about hyperparameters such as optimizer (LBFGS, Adam), learning rate (0.001, 0.0001), batch size (4096), and training steps ('200 per grid extension', '5000+5000 for images'). These details are crucial for understanding the experimental setup and can be found in the supplementary materials or within the paper itself.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto extrae los hiperparámetros matemáticos dispersos del paper. Menciona la configuración dual del optimizador (LBFGS, Adam) y la programación de pasos por extensión de grilla ("200 per grid extension").

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper does not provide error bars, confidence intervals, or any other form of statistical significance measures for the experiments. The pre-computed help indicates that 'Significance Tests: yes' but 'Runs: NOT FOUND'. According to the NeurIPS 2026 official criteria, if NO intervals/variance/runs found -> answer 'No' and set is_no_justified: false. Since no statistical measures are present in the paper, this constitutes a transparency risk as it does not allow readers to assess the reliability of the reported results.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El método es correcto (los resultados de ecuaciones y RMSE se dan como estimaciones puntuales sin medidas estadísticas).

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper mentions hardware but does not provide any metrics for total training time, per-sample efficiency, or environmental impact/CO2 emissions. The pre-computed help states that 'DETECTED hardware/cluster: NOT FOUND'. According to the NeurIPS 2026 official criteria, a 'Yes' is warranted if hardware is mentioned AND (total training time OR per-sample efficiency OR environmental impact/CO2 emissions) is provided. Since no such metrics are provided, this also constitutes a transparency risk.
- **Mi Valoración:** Correcto
- **Mi Justificación:** No acepta la falta de tiempos de ejecución y eficiencia, señalando una omisión en los recursos de cómputo.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a GitHub repository with implementation details and scripts for reproducing experiments, aligning with NeurIPS Code of Ethics requirements. The paper does not contain any clear ethical red flags or harmful applications that would require an ethics statement or IRB discussion.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA confunde la publicación de código en GitHub con el cumplimiento del Código de Ética de NeurIPS. Subir código ayuda a la reproducibilidad, pero la ética de NeurIPS exige evaluar impactos sociales y privacidad.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper focuses on improving interpretability and accuracy in scientific domains such as partial differential equations, knot theory, and physics. There is no direct path to negative societal impacts or potential malicious uses of the research. The broader impact discussion is not applicable given the nature of the work.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La deducción es correcta. Una arquitectura matemática de splines para física y teoría de nudos no tiene aplicaciones de riesgo social que requieran evaluar daños.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** El veredicto "N/A" es adecuado porque es un algoritmo matemático, no una API generativa tóxica. Sin embargo, la IA dejó la celda de justificación en blanco.

**Ítem 12. Licenses**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** —
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo doble. La justificación está vacía y el dictamen debería haber sido "Yes" o "No", indicando si el repositorio de PyKAN incluye la licencia comercial/abierta. No puede ser "no aplicable" cuando hay software involucrado.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors are releasing new assets such as datasets, model weights, benchmarks, or software libraries created as part of this work. The paper mentions a GitHub repository with implementation details and scripts for reproducing experiments but does not explicitly state that these are new creations.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA afirma que no se liberan nuevas librerías, pero el documento presenta y libera públicamente el paquete PyKAN. Se basa en el "JSON summary" para su justificación.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The provided JSON summary does not indicate that the authors have hired or compensated human workers to collect or label new data. The paper mentions the use of B-spline parametrization and symbolic regression techniques but does not provide any information about hiring or compensating human subjects for this research.
- **Mi Valoración:** Correcto
- **Mi Justificación:** No aplica. Es regresión simbólica in-silico, no hay anotadores humanos.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper does not involve any direct research with human subjects. It focuses on the implementation and comparison of Kolmogorov-Arnold Networks (KANs) using existing, public datasets for training and testing purposes.
- **Mi Valoración:** Correcto
- **Mi Justificación:** No hay ensayos con pacientes o grupos sociales.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly mentions the use of LLMs for certain components of its methodology, such as B-spline parametrization and symbolic regression techniques. According to the NeurIPS 2026 criteria, a declaration is required if LLMs are an important component of the core methods.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA local calificó con un "Sí" al afirmar que la parametrización por B-splines y las técnicas de regresión simbólica son LLMs. Confundir el modelado clásico de funciones a trozos (B-splines) con Modelos de Lenguaje Masivo (LLMs) indica una falta de conocimiento en Machine Learning por parte de Qwen2.5.


