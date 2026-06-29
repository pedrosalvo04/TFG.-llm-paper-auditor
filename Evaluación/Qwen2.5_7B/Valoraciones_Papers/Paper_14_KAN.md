# Paper 14: KAN


**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The abstract states: 'We propose Kolmogorov-Arnold Networks (KANs) as promising alternatives to MLPs... KANs have learnable activation functions on the edges... KANs are much more efficient than MLPs in terms of parameter count and accuracy.' Section 3 and 4 provide empirical validation through toy datasets, special functions, Feynman datasets, and PDE solving, demonstrating that KANs achieve higher accuracy with fewer parameters compared to MLPs."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Asocia la afirmación principal del abstract sobre la superioridad de las redes KAN frente a los MLPs con sus validaciones empíricas, citando la eficiencia en parámetros y precisión.

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper includes a dedicated 'Discussion' section (Section 6) which explicitly addresses limitations: 'KANs are currently slower than MLPs... Splines suffer from the curse of dimensionality if not used in compositional structures... The original Kolmogorov-Arnold representation (depth-2) can be non-smooth/fractal... Unclear if continual learning method generalizes to high-dimensional cases.'"
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extrae de forma literal las debilidades metodológicas y computacionales documentadas en la sección de discusión, como la lentitud actual de las redes y la maldición de la dimensionalidad.

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper explicitly states the Kolmogorov-Arnold Representation Theorem in Section 2.1, which serves as the theoretical foundation for the KAN architecture. Furthermore, Section 2.3 and Appendix E provide the theoretical derivation for scaling laws, specifically stating the relationship between grid points, spline order, and approximation error. The authors define the assumptions regarding the function space (e.g., smoothness requirements for B-splines) and provide the mathematical derivation for the parameter count formula O(N^2 * L * G)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Identifica que este documento posee una base teórica matemática estructurada, reconociendo el teorema principal de representación y las derivaciones de las leyes de escalado indicadas en el apéndice.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a dedicated GitHub repository at https://github.com/KindXiaoming/pykan, which contains the full implementation of the Kolmogorov-Arnold Networks (KANs). The repository includes the source code for the model architecture, training loops, and the specific scripts used to reproduce the experiments mentioned in the paper, such as the toy datasets, Feynman datasets, and PDE solving tasks. The paper also details the hyperparameters (e.g., learning rates, grid point schedules, and regularization constants) in Appendix C and throughout the experimental sections."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extrae la URL del repositorio oficial de GitHub proporcionado para la reproducibilidad de la arquitectura propuesta.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a dedicated repository at https://github.com/KindXiaoming/pykan, which includes the implementation of the Kolmogorov-Arnold Network (KAN) architecture, training scripts, and reproduction code for the experiments described in the paper (e.g., model.train(dataset), model.prune(), and model.auto_symbolic())."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Valida el acceso abierto a los recursos apoyándose en el enlace al repositorio mencionado en el ítem anterior.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper provides extensive documentation of experimental settings in the main text and Appendix C (Dependence on hyperparameters). Specifically, the authors detail the optimizer (LBFGS, Adam), learning rates (10^-3, 10^-4), batch sizes (4096), grid point schedules (3 to 1000), and specific architecture shapes (e.g., , ) used across different tasks."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Rescata datos granulares sobre la configuración técnica situados en los apéndices, incluyendo optimizadores específicos y tamaños de lote.

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper fails to meet the NeurIPS 2026 criteria for statistical significance. While the authors report performance metrics across various tasks (e.g., knot signature accuracy, MSE for PDEs), they do not provide error bars, confidence intervals, or statistical significance tests to account for variability across different random seeds or data splits. The NeurIPS criteria explicitly require that results be accompanied by these measures to support the main claims. As the authors have not provided an explicit scientific or computational justification for the omission of these statistical measures, the transparency requirement remains unfulfilled."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Penaliza al detectar que las métricas de rendimiento reportadas carecen de barras de error o medidas de varianza estadística y evalúa que no se ofrece justificación textual para la omisión.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper states: 'KANs are usually 10x slower than MLPs to train' and provides specific training step counts such as '200 per grid extension' and '5000+5000 for images'. Additionally, the hardware context is identified as 'personal laptops'."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Da por válido el uso del término coloquial e inespecífico "personal laptops". Las normativas exigen documentar el hardware de manera cuantificable (modelo de CPU/GPU, especificaciones de memoria) y proveer el tiempo total de ejecución del experimento, lo cual el sistema ha ignorado.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a comprehensive 'Discussion' section (Section 6) and an 'Acknowledgement' section, and the research methodology is grounded in transparent scientific inquiry. The paper focuses on foundational machine learning architecture (Kolmogorov-Arnold Networks) applied to mathematical and physical sciences. The authors have made their code publicly available via a GitHub repository (https://github.com/KindXiaoming/pykan), which aligns with the NeurIPS Code of Ethics requirement to 'Ensure legal compliance' and 'Allowing access to research artifacts' to enable external scrutiny and auditing."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Alucinación lógica de equivalencias. Asume que la publicación de código en un repositorio público sirve como prueba de cumplimiento formal del Código de Ética de NeurIPS, mezclando la normativa de acceso a datos (Ítem 5) con la declaración de impacto ético de la investigación (Ítem 9).

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper presents a foundational architectural innovation in neural networks (KANs) designed to improve interpretability and accuracy in scientific domains such as partial differential equations, knot theory, and physics. The authors explicitly frame the technology as a tool for scientific collaboration ('AI-Scientist-Collaboration') and mathematical discovery."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Determina que la naturaleza del estudio se centra en una innovación matemática enfocada en la física teórica y las ecuaciones, careciendo de aplicaciones directas generativas que presenten un riesgo dual para la sociedad.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper introduces Kolmogorov-Arnold Networks (KANs), a novel neural network architecture based on the Kolmogorov-Arnold representation theorem, which replaces fixed activation functions on nodes with learnable activation functions on edges. The research is foundational in nature, focusing on mathematical approximation, interpretability, and scientific discovery (e.g., solving PDEs, knot theory, and physics simulations)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Establece que el trabajo describe una arquitectura algorítmica de cálculo y no un sistema de IA generativa desplegado hacia usuarios, por lo que no es aplicable requerir filtros de seguridad restrictivos.

**Ítem 12. Licenses**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The authors failed to explicitly state the license under which their code (pykan) or the utilized datasets are released. The NeurIPS 2026 criteria for Item 12 mandate that authors must cite the creators of existing assets and respect the license and terms of use. While the authors provide a GitHub repository URL (https://github.com/KindXiaoming/pykan), the paper text itself does not contain a declaration of the license (e.g., MIT, Apache 2.0, or CC-BY). Without an explicit license statement, it is impossible for the community to verify if the authors are respecting the terms of use for the assets they have integrated or if they are providing their own contributions under a clear legal framework, which constitutes a transparency risk."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Detecta que, aunque existe un enlace hacia el software, el manuscrito omite documentar por escrito bajo qué tipo de licencia legal se libera el código o los datos empleados.

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors released the 'pykan' library (https://github.com/KindXiaoming/pykan) as a core contribution of the paper. The repository provides the implementation of the Kolmogorov-Arnold Network architecture, including methods such as model.train(dataset), model.plot(), model.prune(), and model.symbolic_formula()."
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Aprueba el ítem basándose exclusivamente en la existencia de la librería. Pasa por alto que el requerimiento normativo establece que los nuevos activos deben ir acompañados de plantillas estructuradas de documentación formal (como las Model Cards) detallando su arquitectura, proceso y restricciones.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper focuses on the development of a new neural network architecture (KANs) and its application to mathematical, physical, and synthetic datasets (e.g., Feynman datasets, PDE solving, Knot theory). The research does not involve crowdsourcing, human subject experiments, or the collection of human-derived data. As the work is purely algorithmic and mathematical in nature, the requirements regarding participant instructions, compensation, and ethical labor practices for human subjects are not applicable."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Constata que el estudio es estrictamente matemático e in-silico, fundamentando la ausencia de recopilación de encuestas humanas o plataformas de trabajadores.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The research focuses on Kolmogorov-Arnold Networks (KANs) applied to mathematical, physical, and synthetic datasets such as the Feynman datasets, knot theory signatures, and partial differential equations (PDEs)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Confirma que el uso de datos en entornos computacionales, sin experimentación biomédica ni interacción social directa con sujetos de prueba, no requiere autorización institucional clínica.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The methodology relies on B-spline parametrization, LBFGS/Adam optimization, and symbolic regression techniques (e.g., PySR, GPLearn) for mathematical discovery."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Diferencia los métodos matemáticos y paramétricos convencionales de las arquitecturas generativas, indicando que no se utilizaron modelos de lenguaje a gran escala para asistir en el desarrollo metodológico o diseño sintético del experimento.