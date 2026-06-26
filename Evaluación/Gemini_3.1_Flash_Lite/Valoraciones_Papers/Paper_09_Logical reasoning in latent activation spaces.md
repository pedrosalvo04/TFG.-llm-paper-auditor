# Paper 9: Logical reasoning in latent activation spaces
Logical reasoning in latent activation spaces

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The abstract states: 'We introduce ActivationReasoning (AR), a framework for performing logical reasoning within the latent activation space of LLMs... AR enables model steering and improves transparency.' The introduction further claims that AR allows for 'grounding propositions in latent activation space' and 'performing logical inference via forward chaining.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El framework empírico coincide con la afirmación principal del texto. Se cita la mecánica descrita por los autores: "performing logical inference via forward chaining".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 5 (Discussion) and the extracted 'limitations_quality' list explicitly address: 'Polysemy, Contextual instability, Overly low-level features, Lack of compositionality in standard SAEs, Limited control over discovered concepts...'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Identifica correctamente las debilidades del sistema SAE mencionadas en la Sección 5. Señala problemas como "Polysemy, Contextual instability, Overly low-level features".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** Incorrecto
- **Justificación Auditor:** The paper defines the logical framework in Section 3.3 and Appendix D, specifically stating: 'AR computes L ∪ { C ∗ 1 , . . . , C ∗ m }'
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso positivo persistente. Confunde ecuaciones de métrica heurística computacional con pruebas matemáticas y teoremas formales. Vuelve a confundir la formulación matemática de un método empírico con las demostraciones teóricas que pide NeurIPS. Debió ser "N/A".

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides detailed hyperparameter configurations for all models (Llama 3.1 8B, Gemma 2 9B) in Section 4 and Appendices A.1-A.4, and references the AR pipeline implementation. While the paper relies on third-party datasets (PrOntoQA, BeaverTails), it provides the specific steering formulas and architectural components (SAE decoder weights, weighting vectors) necessary to replicate the ActivationReasoning (AR) intervention.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Asegúrate de que se incluyan los pesos del decodificador y los vectores necesarios para replicar la intervención en las arquitecturas evaluadas (Llama 3.1 8B, Gemma 2 9B).

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides a comprehensive framework for ActivationReasoning (AR) and explicitly references the implementation of the pipeline, including the use of Sparse Autoencoders (SAEs) and the integration of datasets like PrOntoQA, Rail2Country, and ProverQA. The authors provide links to the underlying infrastructure and datasets used, such as https://github.com/asaparov/prontoqa/ and the EleutherAI sparsify repository...
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El veredicto de "Yes" es correcto porque los autores mencionan en el Apéndice H que comparten su código y scripts. Sin embargo, la IA justifica el acceso abierto citando enlaces a repositorios de terceros ("PrOntoQA" y "EleutherAI sparsify repository") en lugar de referenciar el código propio de los autores.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides extensive experimental details in Appendix A (Experimental Setup), which includes subsections for each dataset (A.1 PrOntoQA, A.2 Rail2Country, A.3 ProverQA, A.4 Safety). These sections specify the data splits, the specific model backbones (Llama-3.1-8B, Gemma-2-9B), and a granular breakdown of hyperparameters such as 'topk_in', 'topk_multi', 'steering_factor_alpha', and 'soft_threshold_tau' for each model and task.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El modelo muestra una buena capacidad para extraer detalles en los vectores latentes. En el Apéndice A, se mencionan parámetros de control específicos: "topk_multi, steering_factor_alpha, and soft_threshold_tau".

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper reports performance metrics (e.g., 95.0% accuracy on PrOntoQA) as point estimates without accompanying error bars, confidence intervals, or statistical significance tests. According to the NeurIPS 2026 criteria, authors must report error bars or statistical significance tests for experiments supporting the main claims. While the paper utilizes greedy decoding, which is deterministic, the criteria explicitly require information about the factors of variability and the method for calculating error bars.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Entendimiento estadístico avanzado. Se observa que, aunque los autores utilizan decodificación greedy sin semillas aleatorias, reportan un único porcentaje de precisión ("95.0% accuracy on PrOntoQA"). Esto ignora la varianza de los datos, un requisito de NeurIPS, y no hay justificación en el texto.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides detailed hardware specifications in Appendix C, stating: 'All experiments were conducted on a compute node equipped with 8 x NVIDIA A100-SXM4 GPUs (80 GB each), an AMD EPYC 7313 16-core CPU, and 2 TB of RAM.' Furthermore, the paper includes a dedicated section 'B Runtime Efficiency' which provides quantitative metrics on the execution time for different models (e.g., 0.1066s for Llama3.1_8B vs 0.3747s for AR_Llama3.1_8B).
- **Mi Valoración:** Correcto
- **Mi Justificación:** Describe la infraestructura de hardware y el tiempo de ejecución en menos de un segundo. Incluye las citas directas: "8 x NVIDIA A100-SXM4 GPUs" y los tiempos de latencia de "0.1066s for Llama3.1_8B".

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated 'Ethics Statement' (Section G) and explicitly states: 'Adhere to the ICLR Code of Ethics'. Furthermore, the authors demonstrate ethical awareness by conducting safety experiments using the BeaverTails dataset...
- **Mi Valoración:** Correcto
- **Mi Justificación:** El Apéndice G es válido para este ítem. Cita literal del artículo: "Adhere to the ICLR Code of Ethics".

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors address broader impacts in Section G (Ethics Statement) and throughout the discussion of their methodology. They explicitly state: 'Framework enables model steering which could be misused; authors condemn misuse.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Señala las advertencias sobre el riesgo de manipulación de pesos. Cita: "Framework enables model steering which could be misused".

**Ítem 11. Safeguards**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors explicitly address safety in Section 4 and Appendix A.4, stating: 'We evaluate our approach on the BeaverTails dataset, which contains 14 safety dimensions... The framework enables model steering which could be misused; authors condemn misuse.'
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** La IA confunde la realización de un benchmark sobre toxicidad evaluativa (medir con BeaverTails) con la implementación de un despliegue restrictivo con salvaguardas para el usuario final. Al tratarse de investigación algorítmica fundacional, debería haber indicado "N/A".

**Ítem 12. Licenses**
- **Valoración Auditor:** No
- **Justificación Auditor:** While the authors mention using BeaverTails and provide links to Llama 3.1 and EleutherAI repositories, they fail to explicitly state the license types (e.g., MIT, Apache 2.0, CC-BY) for the assets used or confirm compliance with the specific terms of use for each.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Se penaliza que los autores usen dependencias de terceros (como Llama o BeaverTails) sin declarar el tipo de licencia en el texto.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper utilizes existing datasets (PrOntoQA, Rail2Country, ProverQA, and BeaverTails) and pre-trained models... The authors do not introduce or release new datasets, model weights, or novel software libraries as primary contributions.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo. La IA no identificó que "our newly introduced synthetic dataset Rail2Country" era una aportación nueva, como se indica en la Sección A.4 y el Apéndice G del documento.

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The methodology relies on algorithmic intervention in latent activation spaces using pre-existing datasets (PrOntoQA, Rail2Country, ProverQA, and BeaverTails). There is no mention of human participant studies, crowdsourced data collection...
- **Mi Valoración:** Correcto
- **Mi Justificación:** "N/A" es una justificación sólida. No se utilizan contratistas humanos ni etiquetado masivo primario (crowdsourcing).

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The research utilizes established, publicly available datasets such as PrOntoQA, Rail2Country, ProverQA, and BeaverTails for the purpose of evaluating logical reasoning and safety in latent activation spaces.
- **Mi Valoración:** Correcto
- **Mi Justificación:** No aplica, ya que no hay experimentos directos ni ensayos clínicos con humanos.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly states in Section I (LLM Usage): 'Large language models (LLMs) are used as backbones for our ActivationReasoning framework. LLMs were also used to aid in polishing and rephrasing the manuscript; they were not used for generating ideas, designing methods, running experiments, or analyzing results.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Entiende bien el contexto. Identifica que los LLM son tanto la base del método (backbones) como una herramienta secundaria de escritura, citando la Sección I: "LLMs were also used to aid in polishing and rephrasing the manuscript".


