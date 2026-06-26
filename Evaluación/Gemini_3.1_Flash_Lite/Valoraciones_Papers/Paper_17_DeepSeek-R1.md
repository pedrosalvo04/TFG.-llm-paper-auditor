# Paper 17: DeepSeek-R1
DeepSeek-R1

**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The abstract claims: 'Here we show that the reasoning abilities of LLMs can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories.' This is supported by the results in Section 4 and Appendix D, which demonstrate that DeepSeek-R1-Zero achieves superior performance on verifiable tasks like AIME and coding competitions compared to supervised learning counterparts.
- **Mi Valoración:** Correcto
- **Mi Justificación:** Relaciona el aprendizaje por refuerzo con la mejora del razonamiento. El texto dice: "Here we show that the reasoning abilities of LLMs can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 6, titled 'Conclusion, Limitation, and Future Work', provides a comprehensive discussion of the model's limitations. The authors state: 'Even if DeepSeek-R1 achieves frontier results on reasoning benchmarks, it still faces several capability limitations, as outlined below: Structure Output and Tool Use... Token efficiency... Language Mixing... Prompting Engineering... Software Engineering Tasks.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El documento menciona debilidades como la mezcla de idiomas y el "reward hacking". Cita literal: "it still faces several capability limitations, as outlined below: Structure Output and Tool Use... Language Mixing... Reward Hacking".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** In Section 2.1, the authors define the GRPO objective: 'For each question q, GRPO samples a group of outputs {o1, o2, · · · , oG} from the old policy πθold and then optimizes the policy model πθ by maximizing the following objective: [formula] where πref is a reference policy, ε and β are hyper-parameters, and Ai is the advantage, computed using a group of rewards {r1, r2, . . . , rG}'.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto menciona el esquema teórico GRPO y sus parámetros matemáticos. Cita: "GRPO samples a group of outputs {o1, o2, · · ·, oG} from the old policy πθold and then optimizes the policy model".

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section I, 'Open Weights, Code, and Data', states: 'To promote the development of the open-source community and industry ecosystem, we have made the model weights of DeepSeek-R1 and DeepSeek-R1-Zero publicly available on HuggingFace... Furthermore, we have released the fundamental model inference code (https://github.com/deepseek-ai/DeepSeek-V3) and provided detailed usage guidelines (https://github.com/deepseek-ai/DeepSeek-R1) on GitHub.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Las URLs proporcionadas dirigen a repositorios funcionales. Cita literal: "we have released the fundamental model inference code (https://github.com/deepseek-ai/DeepSeek-V3)".

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section I, 'Open Weights, Code, and Data', explicitly states: 'To promote the development of the open-source community and industry ecosystem, we have made the model weights of DeepSeek-R1 and DeepSeek-R1-Zero publicly available on HuggingFace... Furthermore, we have released the fundamental model inference code.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Apoya el acceso abierto al indicar que los pesos del modelo están publicados. Cita: "we have made the model weights of DeepSeek-R1 and DeepSeek-R1-Zero publicly available on HuggingFace".

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper provides extensive documentation of training details across multiple sections. Section 3.2.1 details the first RL stage (learning rate 3e-6, KL coefficient 0.001, GRPO clip ratio 10, sampling temperature 1, batch size 512). Section 3.2.2 details the second RL stage (learning rate 2e-6, temperature 0.7, 1,700 training steps).
- **Mi Valoración:** Correcto
- **Mi Justificación:** Extrae métricas de entrenamiento de las secciones de arquitectura. Por ejemplo: "learning rate 3e-6, KL coefficient 0.001, GRPO clip ratio 10, sampling temperature 1, batch size 512".

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** The paper fails to meet the NeurIPS 2026 criteria for statistical significance. While the authors include a note in Table 3 and Table 8 stating that 'Numbers in bold denote the performance is statistically significant (t-test with p < 0.01)', they do not provide the actual error bars, confidence intervals, or the specific variance data for the experiments.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo crítico. La IA penaliza el artículo por no usar barras de error, aunque los autores reportaron la significancia con un t-test, un método aceptado en NeurIPS. La IA no reconoce la validez de la cita: "Numbers in bold denote the performance is statistically significant (t-test with p < 0.01)".

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** In section B.4.4. Training Cost, the authors state: 'For the training of DeepSeek-R1-Zero, we employed 64 8 H800 GPUs, and the process required approximately 198 hours. Additionally, during the training phase of DeepSeek-R1, we utilized the same 64 8 H800 GPUs, completing the process in about 4 days, or roughly 80 hours. To create the SFT datasets, we use 5K GPU hours.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El hardware utilizado fue 64 * 8 H800 GPUs, y el proceso duró unas 198 horas.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper includes a dedicated '5. Ethics and Safety Statement' and a comprehensive 'D.3. DeepSeek-R1 Safety Report'. The authors explicitly state: 'With the advancement in the reasoning capabilities of DeepSeek-R1, we deeply recognize the potential ethical risks... In Supplementary D.3, we present a comprehensive safety report from multiple perspectives.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El cumplimiento ético se valida con el informe de seguridad, sin requerir títulos burocráticos exactos. Cita literal: "In Supplementary D.3, we present a comprehensive safety report from multiple perspectives".

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The paper explicitly discusses potential negative societal impacts in Section 5 and Appendix D.3, noting: 'For example, R1 can be subject to jailbreak attacks, leading to the generation of dangerous content such as explosive manufacturing plans... Besides, a public model is also vulnerable to further fine-tuning that could compromise inherent safety protections.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Se identifica la discusión sobre el uso malicioso del modelo, específicamente la creación de bombas/CBRN. Se cita textualmente: "leading to the generation of dangerous content such as explosive manufacturing plans".

**Ítem 11. Safeguards**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** As detailed in Section D.3.1 ('Risk Control System for DeepSeek-R1') and Section D.3.5 ('Robustness against Jailbreaking'), the authors explicitly state: 'Generally, beyond the intrinsic safety of models, model-based services typically implement an external risk control system to enhance system-level security.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** Diferencia un sistema de control de riesgo externo de un alineamiento interno. Cita: "model-based services typically implement an external risk control system to enhance system-level security".

**Ítem 12. Licenses**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** In Section I ('Open Weights, Code, and Data'), the authors state: 'we have made the model weights of DeepSeek-R1 and DeepSeek-R1-Zero publicly available on HuggingFace' and provide links to their GitHub repositories (https://github.com/deepseek-ai/DeepSeek-V3 and https://github.com/deepseek-ai/DeepSeek-R1). The project utilizes the MIT License, which is a standard open-source license.
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Alucinación legal. La IA dice que usa la "MIT License", pero esa licencia no aparece en el documento original de DeepSeek-R1.

**Ítem 13. Assets**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** The authors explicitly state in Appendix I, 'Open Weights, Code, and Data', that they are releasing the model weights, training code, and inference code. Furthermore, the paper provides extensive documentation regarding the model architecture (671B MoE), training methodology (GRPO), and detailed hyperparameter configurations in Appendix B. The model card for DeepSeek-R1 is referenced.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El documento menciona que se ha proporcionado documentación estructurada y acceso al modelo. Se cita: "we have made the model weights of DeepSeek-R1 and DeepSeek-R1-Zero publicly available on HuggingFace".

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The authors utilized existing datasets and automated reinforcement learning pipelines (GRPO) to train the model. While the paper mentions human-aligned thinking process examples and SFT data, these are described as part of the cold-start and supervised fine-tuning pipeline, which relies on existing data curation practices rather than the authors conducting new, primary research involving human subjects or direct crowdsourcing labor.
- **Mi Valoración:** Correcto
- **Mi Justificación:** El texto indica que se usaron datos de recopilación secundaria y aprendizaje por refuerzo automatizado. Menciona: "The prompts used in this dataset... Are sourced either from publicly available open-source datasets or from users who have explicitly consented".

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** The paper utilizes publicly available datasets (e.g., AIME, Codeforces, Arena-Hard) and crowdsourced preference data from ChatbotArena. Section 3.1 states: 'The prompts used in this dataset are all non-reasoning questions and are sourced either from publicly available open-source datasets or from users who have explicitly consented to share their data for the purpose of model improvement.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** El "N/A" es válido porque son datos secundarios sin experimentación humana en un entorno clínico o de riesgo directo.

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** Section 3.1, 'Model-based Rewards', explicitly states: 'We build upon the DeepSeek-V3 pipeline... For each preference pair, we query DeepSeek-V3 four times... The architecture of our reward model is consistent with that of DeepSeek-R1, with the addition of a reward head designed to predict scalar preference scores.'
- **Mi Valoración:** Correcto
- **Mi Justificación:** DeepSeek-V3 se usa como juez metodológico para los rewards. Se le consulta cuatro veces por cada par de preferencias.


