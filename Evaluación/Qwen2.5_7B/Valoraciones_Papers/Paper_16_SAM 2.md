# Paper 16: SAM 2


**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper claims to introduce SAM 2, a unified model for promptable visual segmentation in images and videos, which outperforms prior state-of-the-art methods on semi-supervised video object segmentation (VOS) and interactive benchmarks. The abstract states: 'We introduce SAM 2, a foundation model for promptable visual segmentation in images and videos... SAM 2 outperforms prior state-of-the-art methods on a wide range of video segmentation tasks.'"
- **Mi Valoración:** Correcto
- **Mi Justificación:** Recopila y contrasta el objetivo del abstract con la validación empírica en tareas de segmentación. Cita literal del texto original la superioridad en "semi-supervised video object segmentation (VOS) and interactive benchmarks" .

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper includes a dedicated 'C Limitations' section in the appendix, which explicitly lists several failure modes and constraints: 'Ambiguous prompts (single click) may result in multiple masks', 'Model may lose object (occlusion)', 'Failure across shot changes', 'Tracking/confusion in crowded scenes', 'Failure after long occlusions', 'Failure in extended videos', 'Struggles with thin/fine details', 'Struggles with fast-moving objects', 'Struggles with nearby objects of similar appearance', 'No inter-object communication', 'SAM 2 often tends to segment object parts on the first click while DAVIS contains whole objects', 'Estimation of annotation time does not account for model's tracking FPS', 'Manual masklets: Human errors (missed frames)', 'Auto masklets: Model errors (inconsistencies)', 'No parity across all geographic and demographic groups'."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Realiza una pesquisa exhaustiva en el Apéndice C y extrae de forma íntegra los fallos técnicos reales documentados por los creadores del modelo de visión, sin caer en generalizaciones .

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper 'SAM2: Segment Anything in Images and Videos' is an empirical research contribution focused on model architecture, data engineering, and large-scale video segmentation performance. It does not propose or rely on novel theoretical theorems, mathematical proofs, or formal assumptions that require verification under the NeurIPS criteria for theoretical results. The paper's contributions are entirely algorithmic and empirical, rendering the requirement for formal proofs and stated theoretical assumptions not applicable."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Clasifica adecuadamente la naturaleza del artículo. Determina que el modelado de visión por computador es de carácter algorítmico y empírico, carente de teoremas matemáticos formales que exijan demostración pura .

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide a dedicated repository at https://github.com/facebookresearch/sam2 and the SA-V dataset at https://ai.meta.com/datasets/segment-anything-video/. The paper includes extensive documentation in the Appendix, specifically sections D (SAM2 details), E (Data details), and H (Model, data and annotation cards), which detail the architecture, training protocols, and data engine phases."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Recupera de manera factual las URLs corporativas y los repositorios exactos proporcionados para la replicación del modelo y los datos .

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide explicit access to their contributions: 'https://github.com/facebookresearch/sam2' for the source code and 'https://ai.meta.com/datasets/segment-anything-video/' for the SA-V dataset. These URLs point directly to the authors' own implementation and the newly collected dataset used for the main experimental results."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Valida el cumplimiento del acceso abierto respaldándose en la provisión efectiva de los enlaces detectados en el ítem de reproducibilidad .

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper provides extensive documentation in the Appendix, specifically in sections 'D.2 Training', 'E.2 Data engine details', and 'F Details on zero-shot transfer experiments'. For instance, the authors specify the optimizer (AdamW), batch sizes (128 for pre-training, 1 for video tasks), learning rate strategies, and sequence lengths (8 frames default, 16 for fine-tuning)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extrae hiperparámetros precisos de control ocultos en los apéndices técnicos (D.2 y E.2), identificando el optimizador (AdamW) y las longitudes de secuencia de video .

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper fails to meet the NeurIPS 2026 criteria for statistical significance. According to the official criteria, authors must report error bars, confidence intervals, or statistical significance tests for experiments supporting the main claims. While the paper provides extensive benchmarking and performance metrics, it presents these as point estimates without accompanying measures of variability (such as standard deviation or confidence intervals) or statistical tests to validate the robustness of the results across different runs or seeds. As the authors have not provided an explicit scientific or computational justification for this omission, the requirement for transparency regarding the factors of variability remains unfulfilled."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Sanciona normativamente que los resultados de benchmarking se reporten exclusivamente como puntos de estimación plana, constatando la ausencia de métricas de varianza o desvío estocástico sin justificación explícita .

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper focuses on the release of the SAM 2 model and its capabilities in visual segmentation. Specific computational resource requirements for reproducing the experiments are not explicitly detailed as a primary focus.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Error de categorización normativa del modelo. Aunque el artículo sea la presentación de un "foundation model", las normas exigen transparentar de forma obligatoria el gasto de GPU, tiempos de ejecución e infraestructura utilizados durante el entrenamiento. El dictamen debido ante su ausencia en el texto es "No", no "N/A".

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors explicitly address the ethical dimensions of their research through an internal review process, the use of third-party vendors for crowdsourcing with verified consent, and the implementation of safety measures such as face-blurring and content moderation. The paper includes detailed documentation in the appendix (Section H) regarding data annotation cards, maintenance, and distribution, which aligns with the NeurIPS Code of Ethics requirement to communicate data-related concerns, privacy, and consent."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Avala que la descripción detallada de procesos de privacidad (ej. difuminado de rostros) y revisión interna constituyen un cumplimiento material válido de los requisitos éticos, sin forzar la existencia de un apartado con el título literal de "Código de Ética" .

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper includes a dedicated discussion on limitations and broader impacts, specifically addressing fairness evaluations in Section E.1.1 and providing a comprehensive analysis of environmental impact (carbon emissions and energy consumption). The authors acknowledge potential risks such as model failure in crowded scenes or with fast-moving objects and provide a reporting mechanism (segment-anything@meta.com) for misuse."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Verifica que los autores discuten las ramificaciones a gran escala, mapeando el impacto ecológico (emisiones de carbono) y la apertura de canales directos de reporte de mal uso como mitigaciones de impacto ampliado .

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper presents SAM 2, a foundational model for promptable visual segmentation in images and videos. The authors have implemented privacy-preserving measures, such as face blurring in the SA-V dataset, and have established a reporting mechanism (segment-anything@meta.com) for objectionable content. The model is a general-purpose computer vision tool for segmentation and does not inherently generate harmful content, synthesize dangerous information, or facilitate surveillance in a manner that constitutes a high risk for misuse compared to standard foundational vision models."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Diferencia con madurez conceptual que un modelo de visión cuya salida son máscaras de segmentación de píxeles no posee las mismas capacidades de riesgo (ej. generación de desinformación o texto tóxico) que un modelo de lenguaje masivo, eximiéndolo lógicamente de implementar salvaguardas de acceso coercitivas .

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper explicitly states the licensing terms for the released assets in the 'H.3 Data annotation card' and the associated repository documentation: 'SA-V dataset: CC by 4.0' and 'SAM 2 code: Apache 2.0'."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extrae las licencias fácticas reales presentes en los anexos sin alucinaciones. Distingue correctamente la licencia de los datos (CC by 4.0) de la licencia de software (Apache 2.0) .

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The authors provide comprehensive documentation for the newly released SA-V dataset and the SAM 2 model. Specifically, section 'H. Model, data and annotation cards' includes detailed 'Composition', 'Collection Process', 'Preprocessing / Cleaning / Labeling', 'Uses', 'Distribution', and 'Maintenance' sections. Furthermore, 'H.3 Data annotation card' provides structured metadata regarding the dataset's creation. The authors also explicitly state the license for the SA-V dataset (CC by 4.0) and the SAM 2 code (Apache 2.0)."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Verifica y valida formalmente que el artículo cumple con la provisión de las plantillas documentales estructuradas exigidas (Model Cards y Data Cards) en el Apéndice H para los nuevos activos liberados .

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper explicitly details the use of crowdworkers for video capture and annotation in section 'E.2 Data engine details' and 'E.2.1 Annotation protocol'. The authors confirm that workers were compensated with an hourly wage and consented via a third-party vendor. Additionally, the 'human_subjects_extraction' metadata confirms that a separate set of annotators was used for quality verification and that these individuals underwent 1-2 weeks of training."
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El dictamen de cumplimiento y la identificación de las métricas de compensación salarial de los anotadores es correcta. No obstante, en la redacción, el sistema rompe la interfaz de auditoría inyectando una variable interna directa ("the 'human_subjects_extraction' metadata confirms"), provocando una fuga de prompt (prompt leakage) inaceptable en un informe final .

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper states in the 'Human subjects' extraction that 'Crowdworkers used for video capture and annotation; compensated with hourly wage; consented via third-party vendor.' Furthermore, the 'Code of ethics' section notes that the 'Project underwent an internal review process' and that the 'Contracted third-party provided representations regarding notices and consents.'"
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Acepta que los procesos de revisión interna y el uso de proveedores regulados actúan como mecanismo de consentimiento institucional para este tipo de recolección en visión. Sin embargo, vuelve a sufrir de fuga de contexto en su redacción ("states in the 'Human subjects' extraction") .

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The NeurIPS 2026 criteria state that a declaration is only required if an LLM is an important, original, or non-standard component of the core methods. The provided technical documentation for SAM 2 describes a computer vision architecture based on a hierarchical image encoder (Hiera), a memory bank, and a transformer-based mask decoder. There is no evidence that LLMs were utilized as a core component of the methodology (e.g., for synthetic data generation or as part of the model architecture). As the research focuses on visual segmentation rather than language modeling or LLM-based reasoning, this item is not applicable."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Determina de forma deductiva que el marco metodológico pertenece estrictamente a la visión por computador (encoders de imágenes Hiera), sin existir rastro de intervención o asistencia por parte de Modelos de Lenguaje para la generación de datos del estudio .