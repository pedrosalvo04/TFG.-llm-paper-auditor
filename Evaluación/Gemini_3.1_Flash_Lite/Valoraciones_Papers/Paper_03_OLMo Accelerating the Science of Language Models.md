# Paper 3: OLMo: Accelerating the Science of Language Models
OLMo: Accelerating the Science of Language Models

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The abstract states: 'We release the full training corpus, Dolma, as well as the training code, logs, and intermediate checkpoints.' The introduction further claims: 'OLMo is a state-of-the-art open language model... designed to enable the scientific study of language models.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta identifica las afirmaciones empíricas clave en el abstract y la introducción sobre la liberación del corpus de entrenamiento y código. Comprueba que estas afirmaciones coinciden con el alcance del paper. Por ejemplo, extrae la cita: "We release the full training corpus, Dolma".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated 'Limitations' section which states: 'Pretraining data is focused on English... models exhibit bias, toxicity, and hallucinations... downstream tasks are not fully representative of chatbot interaction... emissions estimates are lower bounds.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta identifica debilidades en la sección "Limitations", como el sesgo, la toxicidad y el enfoque exclusivo en inglés. Esto se alinea con el criterio. Cita literal: "models exhibit bias, toxicity, and hallucinations".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper focuses on the empirical development, training, and evaluation of the OLMo language model framework. It does not propose new theoretical models, mathematical proofs, or novel algorithmic assumptions that require formal verification.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Dictamen "N/A". Es un reporte técnico empírico y arquitectónico sobre pre-entrenamiento a gran escala, sin teoremas o demostraciones matemáticas.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 5, 'Artifacts Released', states: 'We release the full OLMo framework, including training code, training data (Dolma), training logs, and model weights.' The paper provides comprehensive access to the authors' own implementation, including the Dolma dataset, the training framework built on PyTorch/FSDP, and the resulting model checkpoints.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Sí, la Sección 5 (Artifacts Released) confirma el acceso al marco de trabajo de entrenamiento y evaluación de los autores. Cita literal: "We release the full OLMo framework".

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly states in Section 5, 'Artifacts Released', that the authors are releasing the full pretraining corpus (Dolma), the training code, and the model weights. The authors provide a comprehensive framework for open science, ensuring that the code, data, and instructions needed to reproduce the main experimental results are accessible. This aligns with the NeurIPS 2026 criteria, which encourages the release of code and data to facilitate reproducibility and scientific understanding.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta evalúa este punto basándose en la liberación de los activos propios de los autores (el dataset Dolma, los pesos del modelo y el código nativo), cumpliendo con las directrices de apertura de NeurIPS.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides extensive documentation regarding experimental settings. Section 3 ('Training OLMo') and Appendix A ('Training Settings') detail the training framework, optimizer configurations (AdamW), learning rate schedules (peak and min values), batch sizes (4M tokens), and hardware specifications (LUMI and MosaicML clusters). Furthermore, hyperparameter selection and training details for adaptation (instruction tuning and DPO) are provided in Appendices D and E. This satisfies the NeurIPS 2026 criteria requiring the specification of all training details, including data splits, hyperparameters, and the methodology for their selection.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Identifica datos clave del experimento, como el optimizador AdamW, los calendarios de learning rate y los volúmenes de paralelización. Incluye la cita: "batch sizes (4M tokens)".

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper provides extensive evaluation results across various benchmarks (e.g., MMLU, downstream tasks) but fails to report error bars, confidence intervals, or statistical significance tests for these results. According to the NeurIPS 2026 criteria, authors must provide such information for experiments supporting the main claims. While the authors acknowledge that evaluation is 'noisy' in the limitations section, they do not provide the required statistical measures, nor do they explicitly state that the omission is due to prohibitive computational costs. Therefore, the requirement for statistical transparency is not met, and the omission is not justified by the authors.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta penaliza la ausencia de barras de error en los benchmarks. Los autores admiten que sus resultados son "ruidosos" (noisy). El artículo no justifica la omisión por costes computacionales prohibitivos. No se hacen excepciones injustificadas para LLMs masivos.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 3.4 and Appendix B provide detailed hardware specifications: 'LUMI: 256 nodes, AMD MI250X, 64GB per logical device, 800Gbps interconnect' and 'MosaicML: 27 nodes, NVIDIA A100, 40GB, 800Gbps interconnect'. Furthermore, Appendix B explicitly reports environmental impact: 'carbon_emissions_lumi: 69.78 tCO2eq' and 'energy_consumption_7b: 239 MWh'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Recupera la topología de la granja de servidores (LUMI, MosaicML) y genera la trazabilidad del consumo energético y de carbono que pide NeurIPS. La cita es: "carbon_emissions_lumi: 69.78 tCO2eq".

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated 'Ethics Statement' section which explicitly addresses the authors' commitment to open science and the ethical implications of releasing large-scale language models. The authors state: 'We believe that increased openness is essential for scientific understanding and broad participation in the field of AI.' Furthermore, the paper provides a comprehensive 'Limitations' section that discusses the presence of toxic language, personal information, and copyrighted text within the training data, demonstrating a proactive approach to identifying and communicating potential ethical risks associated with the dataset and model.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Valida la sección "Ethics Statement" del paper. Reconoce la discusión de los autores sobre la apertura científica y los riesgos éticos de los datos, sin penalizar la falta de fórmulas burocráticas exactas.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly discusses the broader societal impacts of their work in the 'Ethics Statement' and 'Limitations' sections. The authors note: 'Our work focuses on the scientific study of biases, risks, and strengths of language models... Increased openness is essential for scientific understanding and reduces duplicated, costly efforts.' Additionally, the authors provide a detailed analysis of the environmental impact, including carbon footprint estimation and operational emissions reporting, which directly addresses the NeurIPS criteria regarding environmental impact and the promotion of sustainable AI practices.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Relaciona la discusión de impacto ambiental y social con los sesgos del modelo, cumpliendo así las directrices de NeurIPS sobre Broader Impacts.

**Ítem 11. Safeguards**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper presents OLMo as a foundational research artifact, explicitly stating in the 'Ethics Statement' and 'Limitations' sections that the model is intended for scientific study of language models, biases, and risks. The authors acknowledge that the model may exhibit toxic language or hallucinations, but it is released as a base model for research purposes rather than a deployed, high-risk application with direct potential for weaponization or surveillance.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta dictamina "N/A" porque OLMo es un "artefacto de investigación fundacional" (un modelo base de pesos abiertos) para estudio científico, no una aplicación final de alto riesgo para usuarios vía API.

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly states in the 'Artifacts Released' section and the associated repository documentation that the OLMo framework and the Dolma dataset are released under the Apache 2.0 license. The authors provide links to the repositories (e.g., https://github.com/allenai/OLMo) where these terms are clearly defined.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El artículo menciona la licencia Apache 2.0 para el framework y el dataset. Cita textual: "released under the Apache 2.0 license".

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 5, 'Artifacts Released', states: 'We release the full pretraining corpus (Dolma), the training code, the evaluation code, and the model weights for all sizes.' The paper provides a comprehensive framework for these assets, including detailed documentation on the data composition (Section 2.2), training infrastructure (Section 3), and licensing (Apache 2.0).
- **Mi Valoración:** Correcto
- **Mi Justificación:** Los autores incluyen la documentación necesaria (licencias, composición de datos y arquitectura) que NeurIPS pide para nuevos activos.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper utilizes existing, publicly available human-derived datasets for instruction tuning and alignment, such as TÜLU, UltraFeedback, and ShareGPT-Vicuna. The authors did not conduct new primary research involving human subjects, nor did they hire or compensate new crowdsourced workers for data collection or annotation as part of this specific submission. As the work relies on third-party datasets rather than original human-subject research, the requirements for documenting participant instructions, screenshots, and compensation are not applicable.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El dictamen "N/A" se basa en que los autores usaron datos humanos públicos existentes (TÜLU, ShareGPT) para el alineamiento, sin realizar una campaña de crowdsourcing propia que requiera regulación.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The research presented in the paper focuses on the development and evaluation of the OLMo language model using existing, publicly available datasets (such as Dolma, C4, and various instruction-tuning datasets like Alpaca and ShareGPT). According to the NeurIPS 2026 criteria, IRB approval is required for research involving direct human subjects. As the authors did not conduct new human-subject experiments or collect primary data from human participants, but rather utilized established, open-source datasets for training and evaluation, the requirement for IRB approval is not applicable to this study.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Entiende las reglas de experimentación, marcando "N/A" porque los investigadores no hicieron experimentos clínicos, sociales primarios o intervenciones con personas vivas que necesitaran aprobación de comités éticos institucionales (IRB).

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly states the use of LLMs as a core component of the methodology, specifically in the context of data distillation and evaluation: 'We use gpt-3.5-turbo for data distillation' and 'GPT-4 for AlpacaEval annotation'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto menciona el uso de modelos comerciales de terceros para la destilación de datos y la automatización de métricas de evaluación (LLM-as-a-judge). Se cita: "GPT-4 for AlpacaEval annotation".


