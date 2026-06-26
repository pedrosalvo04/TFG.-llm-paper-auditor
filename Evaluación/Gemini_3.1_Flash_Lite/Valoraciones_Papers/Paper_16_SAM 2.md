# Paper 16: SAM 2
SAM 2

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper claims to introduce SAM 2, a unified model for promptable visual segmentation in images and videos, which outperforms prior state-of-the-art methods on semi-supervised video object segmentation (VOS) and interactive benchmarks. The abstract states: 'We introduce SAM 2, a foundation model for promptable visual segmentation in images and videos... SAM 2 outperforms prior state-of-the-art methods on a wide range of video segmentation tasks.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El abstract menciona que SAM 2 es un modelo fundacional para segmentación visual en imágenes y videos, y que supera a métodos anteriores en tareas de segmentación de video.

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated 'C Limitations' section in the appendix, which explicitly lists several failure modes and constraints: 'Ambiguous prompts (single click) may result in multiple masks', 'Model may lose object (occlusion)', 'Failure across shot changes', 'Tracking/confusion in crowded scenes', 'Failure after long occlusions', 'Failure in extended videos', 'Struggles with thin/fine details', 'Struggles with fast-moving objects', 'Struggles with nearby objects of similar appearance', 'No inter-object communication', 'SAM 2 often tends to segment object parts on the first click while DAVIS contains whole objects', 'Estimation of annotation time does not account for model's tracking FPS', 'Manual masklets: Human errors (missed frames)', 'Auto masklets: Model errors (inconsistencies)', 'No parity across all geographic and demographic groups'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La investigación en el Apéndice C es exhaustiva. Identifica fallos del modelo de visión, como se indica en las citas: "Ambiguous prompts (single click) may result in multiple masks" y "Failure after long occlusions".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper 'SAM2: Segment Anything in Images and Videos' is an empirical research contribution focused on model architecture, data engineering, and large-scale video segmentation performance. It does not propose or rely on novel theoretical theorems, mathematical proofs, or formal assumptions that require verification under the NeurIPS criteria for theoretical results. The paper's contributions are entirely algorithmic and empirical, rendering the requirement for formal proofs and stated theoretical assumptions not applicable.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Exención confirmada. El modelado de visión industrial es algorítmico y empírico, no requiere demostraciones de teoremas matemáticos puros.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide a dedicated repository at https://github.com/facebookresearch/sam2 and the SA-V dataset at https://ai.meta.com/datasets/segment-anything-video/. The paper includes extensive documentation in the Appendix, specifically sections D (SAM2 details), E (Data details), and H (Model, data and annotation cards), which detail the architecture, training protocols, and data engine phases.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Se verificaron las URL corporativas proporcionadas: "https://github.com/facebookresearch/sam2" y "https://ai.meta.com/datasets/segment-anything-video/".

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide explicit access to their contributions: 'https://github.com/facebookresearch/sam2' for the source code and 'https://ai.meta.com/datasets/segment-anything-video/' for the SA-V dataset. These URLs point directly to the authors' own implementation and the newly collected dataset used for the main experimental results.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Confirma el hallazgo del ítem 4, validando el acceso abierto a la implementación y al dataset.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides extensive documentation in the Appendix, specifically in sections 'D.2 Training', 'E.2 Data engine details', and 'F Details on zero-shot transfer experiments'. For instance, the authors specify the optimizer (AdamW), batch sizes (128 for pre-training, 1 for video tasks), learning rate strategies, and sequence lengths (8 frames default, 16 for fine-tuning).
- **Mi Valoración:** Correcto
- **Mi Justificación:** Encuentra los hiperparámetros en los apéndices D y E. Se mencionan: "AdamW", "batch sizes", "sequence lengths (8 frames default, 16 for fine-tuning)".

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper fails to meet the NeurIPS 2026 criteria for statistical significance. According to the official criteria, authors must report error bars, confidence intervals, or statistical significance tests for experiments supporting the main claims. While the paper provides extensive benchmarking and performance metrics, it presents these as point estimates without accompanying measures of variability (such as standard deviation or confidence intervals) or statistical tests to validate the robustness of the results across different runs or seeds. As the authors have not provided an explicit scientific or computational justification for this omission, the requirement for transparency regarding the factors of variability remains unfulfilled.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Pide medidas de varianza. Señala que las tablas (como J&F) son estimaciones sin intervalos de confianza.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides detailed information regarding the computational infrastructure and environmental impact: 'training_infrastructure: 256 A100 GPUs', 'training_duration: 108 hours', 'inference_device: Single A100 GPU (80GB)', 'energy_consumption: 12165.12 kWH', and 'carbon_emissions: 3.89 metric tons of CO2e'.
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El contenido extraído (256 A100s, 108 horas) es correcto, pero la IA muestra una fuga de formato. Expone las claves de su diccionario JSON interno en la respuesta pública. Cita del fallo: "training_infrastructure: 256 A100 GPUs", "training_duration: 108 hours".

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors explicitly address the ethical dimensions of their research through an internal review process, the use of third-party vendors for crowdsourcing with verified consent, and the implementation of safety measures such as face-blurring and content moderation. The paper includes detailed documentation in the appendix (Section H) regarding data annotation cards, maintenance, and distribution, which aligns with the NeurIPS Code of Ethics requirement to communicate data-related concerns, privacy, and consent.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Aprueba los procesos de privacidad de Meta en los apéndices como mitigación equivalente a la declaración. Cita literal: "safety measures such as face-blurring and content moderation".

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated discussion on limitations and broader impacts, specifically addressing fairness evaluations in Section E.1.1 and providing a comprehensive analysis of environmental impact (carbon emissions and energy consumption). The authors acknowledge potential risks such as model failure in crowded scenes or with fast-moving objects and provide a reporting mechanism (segment-anything@meta.com) for misuse.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Relaciona las emisiones de CO2 y los riesgos de fallos físicos en la vía pública (escenas rápidas) como "Broader Impact" negativo.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper presents SAM 2, a foundational model for promptable visual segmentation in images and videos. The authors have implemented privacy-preserving measures, such as face blurring in the SA-V dataset, and have established a reporting mechanism (segment-anything@meta.com) for objectionable content. The model is a general-purpose computer vision tool for segmentation and does not inherently generate harmful content, synthesize dangerous information, or facilitate surveillance in a manner that constitutes a high risk for misuse compared to standard foundational vision models.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La deducción es correcta. Un modelo generador de máscaras visuales no necesita los mismos filtros de acceso que un LLM que puede generar desinformación o texto tóxico.

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly states the licensing terms for the released assets in the 'H.3 Data annotation card' and the associated repository documentation: 'SA-V dataset: CC by 4.0' and 'SAM 2 code: Apache 2.0'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** No hay alucinaciones (cero menciones MIT aleatorias). Extrae las licencias de los anexos. Cita literal: "SA-V dataset: CC by 4.0" y "SAM 2 code: Apache 2.0".

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors provide comprehensive documentation for the newly released SA-V dataset and the SAM 2 model. Specifically, section 'H. Model, data and annotation cards' includes detailed 'Composition', 'Collection Process', 'Preprocessing / Cleaning / Labeling', 'Uses', 'Distribution', and 'Maintenance' sections. Furthermore, 'H.3 Data annotation card' provides structured metadata regarding the dataset's creation. The authors also explicitly state the license for the SA-V dataset (CC by 4.0) and the SAM 2 code (Apache 2.0).
- **Mi Valoración:** Correcto
- **Mi Justificación:** El trabajo cumple con el formato y las plantillas de NeurIPS. Se incluye la cita literal: "H. Model, data and annotation cards".

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly details the use of crowdworkers for video capture and annotation in section 'E.2 Data engine details' and 'E.2.1 Annotation protocol'. The authors confirm that workers were compensated with an hourly wage and consented via a third-party vendor. Additionally, the 'human_subjects_extraction' metadata confirms that a separate set of annotators was used for quality verification and that these individuals underwent 1-2 weeks of training.
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El dictamen es correcto y verifica a los trabajadores remunerados. Sin embargo, rompe la interfaz del reporte al inyectar su variable local del backend (prompt leakage). El error de formato indica: "the 'human_subjects_extraction' metadata confirms".

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper states in the 'Human subjects' extraction that 'Crowdworkers used for video capture and annotation; compensated with hourly wage; consented via third-party vendor.' Furthermore, the 'Code of ethics' section notes that the 'Project underwent an internal review process' and that the 'Contracted third-party provided representations regarding notices and consents.'
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Acepta a los proveedores de anotación como mitigación válida, pero mantiene el error de redacción sobre la fuga de instrucciones. El error se encuentra en la cita: "The paper states in the 'Human subjects' extraction".

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The NeurIPS 2026 criteria state that a declaration is only required if an LLM is an important, original, or non-standard component of the core methods. The provided technical documentation for SAM 2 describes a computer vision architecture based on a hierarchical image encoder (Hiera), a memory bank, and a transformer-based mask decoder. There is no evidence that LLMs were utilized as a core component of the methodology (e.g., for synthetic data generation or as part of the model architecture). As the research focuses on visual segmentation rather than language modeling or LLM-based reasoning, this item is not applicable.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El modelo es de visión computacional, sin usar LLMs. Su arquitectura es un "hierarchical image encoder (Hiera)".


