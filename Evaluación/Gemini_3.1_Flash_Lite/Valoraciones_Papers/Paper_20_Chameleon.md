# Paper 20: Chameleon
Chameleon

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper claims to introduce 'Chameleon', a family of mixed-modal early-fusion foundation models that unify text and images in a single Transformer architecture. The introduction states: 'We present Chameleon, a family of token-based mixed-modal foundation models capable of understanding and generating images and text in an interleaved fashion.' This is supported by the results in Tables 9-14, which demonstrate competitive performance against state-of-the-art baselines like GPT-4V and Gemini-Pro across various benchmarks (e.g., PIQA, MMLU, MATH) and human evaluation preference metrics.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La afirmación principal se conecta con los resultados en las tablas de evaluación. El texto dice: "We present Chameleon, a family of token-based mixed-modal foundation models capable of understanding and generating images and text in an interleaved fashion".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly discusses limitations in the 'Conclusion' and throughout the technical sections, noting: 'Tokenizer weakness in reconstructing images with large amounts of text (OCR-related tasks)', 'Instability when scaling above 8B parameters and 1T tokens', 'Uncontrolled growth of output norms as a predictor of divergence', and 'Early-fusion approach has challenges in representation learning and alignment'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto menciona dos debilidades: "Tokenizer weakness in reconstructing images with large amounts of text (OCR-related tasks)" y el "uncontrolled growth of output norms as a predictor of divergence".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper is an empirical study focused on the architecture and training of a large-scale multimodal foundation model. While the authors discuss the 'softmax translation invariant property' as a conceptual motivation for modality competition, the paper does not present formal theoretical results, theorems, or proofs that require a set of assumptions. As per the NeurIPS 2026 criteria, this item applies only if the authors include theoretical results; since this work is purely empirical and architectural, the item is not applicable.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Diferencia una motivación conceptual de un teorema. Comprende que la "softmax translation invariant property" no necesita una demostración algebraica formal en un estudio arquitectónico empírico.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** No
- **Justificación Auditor:** The authors failed to provide access to their own original implementation code, model weights, or the specific datasets used for the main experiments. While the paper references third-party libraries such as 'xformers' and 'pycocoevalcap', these are external dependencies and do not constitute the authors' own research artifacts. According to the NeurIPS 2026 criteria, reproducibility for a model contribution requires making it possible for others to replicate the model or providing access to the model itself (e.g., via checkpoints or hosted access). The absence of the Chameleon model weights or the training/inference code prevents independent verification of the reported results, which constitutes a significant transparency risk.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Falta el código y los pesos originales. Citar librerías de terceros no reemplaza la ausencia de los artefactos principales. Se aplica el dictamen: "The absence of the Chameleon model weights or the training/inference code prevents independent verification of the reported results".

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** No
- **Justificación Auditor:** The NeurIPS 2026 criteria for Open Access to Data and Code require that authors include the code, data, and instructions needed to reproduce the main experimental results. While the paper provides links to third-party dependencies such as 'pycocoevalcap' and 'xformers', it fails to provide the authors' own implementation code, the specific training data processing pipelines, or the model weights for the Chameleon foundation models. As per the official criteria, links to third-party libraries are insufficient; the paper must provide access to the contribution's core implementation. Since the authors have not released their proprietary training code or model weights, and have not provided a justification for this omission, the transparency requirement is not met.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La penalización se mantiene por la misma razón que en el ítem 4. Mencionar herramientas externas como pycocoevalcap o xformers no cumple con el acceso abierto al modelo.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides comprehensive training details in the 'Pre-Training' and 'Hyperparameters' sections, including: 'optimizer: AdamW', 'betas: [0.9, 0.95]', 'learning_rate: 1.0 x 10^-4', 'warmup_steps: 4000', 'weight_decay: 0.1', 'gradient_clipping: 1.0', and 'global_batch_size: 2^23 (~8M tokens) for 7B'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El documento menciona una configuración técnica específica: "global_batch_size: 2^23 (~8M tokens) for 7B".

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper fails to meet the NeurIPS 2026 criteria for statistical significance. According to the official criteria, authors must report error bars, confidence intervals, or statistical significance tests for experiments supporting the main claims. While the paper presents extensive benchmark results (e.g., Tables 9-14), it provides only point-estimate averages for performance metrics without any accompanying measures of variability, such as standard deviations or confidence intervals. Furthermore, the authors do not provide an explicit justification for the omission of these statistical measures, such as citing prohibitive computational costs for multiple runs. Consequently, the transparency regarding the reliability and reproducibility of the reported performance gains is insufficient.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo por ceguera documental. Se penaliza por asumir una omisión total de variabilidad, pero los autores incluyen el cálculo estadístico en la Sección 4.3 para la evaluación humana. Se ignoró la cita: "Krippendorff's Alpha... Confidence interval is [0.319, 0.356] based on bootstrap sampling".

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides detailed hardware specifications and usage metrics in the 'Pre-Training Hardware' section. Specifically, it states: 'Chameleon-7B: 1024 concurrent GPUs, 856,481 GPU hours; Chameleon-34B: 3072 concurrent GPUs, 4,282,407 GPU hours' using 'NVIDIA A100 80 GB' GPUs on 'Meta's Research Super Cluster (RSC)'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Recupera los datos de hardware y horas de uso reportados. Cita literal: "Chameleon-7B: 1024 concurrent GPUs, 856,481 GPU hours... On Meta's Research Super Cluster (RSC)".

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated 'Contributors' section and acknowledges the use of human evaluation experiments. Furthermore, the authors explicitly mention 'Safety tuning efforts' and 'Safety and red teaming efforts' in the context of their foundation model development. The methodology involves rigorous data curation, including the use of licensed images for the image tokenizer and adherence to standard machine learning research practices for large-scale model training.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Considera los apartados "Safety tuning efforts" y "Safety and red teaming efforts" como la declaración de ética de la empresa.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly identifies 'Safety tuning efforts' and 'Safety and red teaming efforts' as part of the development lifecycle of the Chameleon model. Additionally, the authors discuss the limitations of their model, such as tokenizer weaknesses in OCR-related tasks and instability at scale, which are critical for understanding the reliability and potential misuse of the technology.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La discusión conecta los fallos del modelo, como los problemas de OCR, con los riesgos de inestabilidad y uso malicioso.

**Ítem 11. Safeguards**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly mentions in the 'Broader Impacts' and 'Safety' sections that the authors conducted 'Safety tuning efforts' and 'Safety and red teaming efforts' to mitigate risks associated with the model's deployment. Furthermore, the model is presented as a foundation model where the authors acknowledge the necessity of responsible release practices.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Identifica que los "Safety tuning efforts" funcionan como controles para reducir riesgos antes de implementar el modelo.

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly references the use of licensed assets, stating: 'Image tokenizer trained using only licensed images' and citing various Creative Commons licenses including 'CC-BY-SA 2.0', 'CC-BY-SA 3.0', and 'CC-BY-SA 4.0'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El documento indica que el tokenizador de imágenes se entrenó con imágenes bajo licencias CC-BY-SA 2.0, CC-BY-SA 3.0 y CC-BY-SA 4.0.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper utilizes established datasets such as Llama-2 pre-training data, MS-COCO, Flickr30k, VQA-v2, ShareGPT, GQA, Laion-5b, and various academic benchmarks (PIQA, SIQA, HellaSwag, etc.).
- **Mi Valoración:** Correcto
- **Mi Justificación:** Los ítems 4 y 5 no aplican. El modelo no tiene pesos ni código liberados, por lo que no se exige una "Model Card" de activos.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Appendix B, 'Additional Information of Human Evaluations', details the methodology for human preference evaluation against baselines like Gemini-Pro and GPT-4V. The authors describe the task categories (e.g., Advice, Article, Brainstorming, Comparison, Explanation) and the evaluation protocol used to measure the quality of mixed-modal long-form responses.
- **Mi Valoración:** Correcto
- **Mi Justificación:** La metodología de evaluación con humanos se encuentra en el Apéndice B, "Additional Information of Human Evaluations", donde se detalla cómo se evaluaron las preferencias humanas frente a modelos como Gemini-Pro y GPT-4V.

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Appendix B: 'Additional Information of Human Evaluations' describes the methodology for human preference data collection. The authors state: 'Human evaluation experiment measuring quality of mixed-modal long-form responses to open-ended prompts.'
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso positivo. El texto asume que mencionar un "Human evaluation experiment measuring quality" implica la aprobación de un comité ético institucional (IRB). Las evaluaciones manuales en internet no aseguran una revisión ética clínica.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper utilizes 'Llama-2 pre-training data' and 'ShareGPT' as core components of the training pipeline. Furthermore, the methodology involves comparing the model against 'GPT-4V' and 'Gemini' as primary benchmarks for performance validation.
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El veredicto es aceptable porque usa datos de ShareGPT. Sin embargo, la justificación tiene un error: usar "GPT-4V" y "Gemini" como rivales en un benchmark no es lo mismo que usar LLMs para el desarrollo metodológico del paper.