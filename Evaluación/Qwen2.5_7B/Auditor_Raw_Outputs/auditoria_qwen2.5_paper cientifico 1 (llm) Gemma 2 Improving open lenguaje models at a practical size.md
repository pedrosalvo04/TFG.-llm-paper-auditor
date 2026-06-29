# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 1 (llm) Gemma 2 Improving open lenguaje models at a practical size.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-28 10:21:28 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 718.67s |
| 📊 **Caracteres Analizados** | 73,466 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **2 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 8
- **No Cumple (No):** 5
- **No Aplica (N/A):** 3
- **Ítems con Alerta:** 2

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | "Overall, Gemma 2 significantly advances state-of-the-art performance relative to comparable-scale open models and are even competitive with some models more than twice their size (AI@Meta, 2024; Almazrouei et al., 2023; Jiang et al., 2023; xAI, 2024), across a variety of automated benchmarks and human evaluations. Example domains include question answering (Clark et al., 2019; Kwiatkowski et al., 2019), commonsense reasoning (Sakaguchi et al., 2019; Suzgun et al., 2022), mathematics and science (Cobbe et al., 2021; Hendrycks et al., 2020), and coding (Austin et al., 2021; Chen et al., 2021)." |
| 2 | Limitations | 🟢 Yes | "While thorough testing of our models has been conducted, these tests cannot cover all applications and scenarios in which Gemma 2 may be used. With this in mind, all Gemma 2 users should conduct rigorous safety testing specific to their use case before deployment or use." |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper does not contain any theoretical results, proofs, or assumptions. The official criteria for Theory, Assumptions and Proofs (Item 3) require that if the paper includes theoretical results, all assumptions should be clearly stated or referenced in the statement of any theorems, and complete proofs should be included either in the main paper or supplemental material. Since no such content is present in this paper, it does not meet the criteria for transparency in theory, assumptions, and proofs. |
| 4 | Experimental Result Reproducibility | 🔴 No | The paper lacks explicit URLs or instructions that grant access to the authors' own original code, model weights, or newly collected datasets used for the main experiments. The official criteria (Item 4) require steps taken by the authors to make their results reproducible or verifiable. While the paper mentions a tokenizer and some hyperparameters, these details alone are insufficient to ensure experimental result reproducibility. Therefore, this paper does not meet the transparency requirements for experimental result reproducibility. |
| 5 | Open Access to Data and Code | 🔴 No | The paper does not provide any open access to the authors' own original code, model weights, or newly collected datasets used for the main experiments. The relevant sections of the paper do not mention any URLs or instructions that grant access to these elements. Instead, it mentions third-party dependencies such as SentencePiece tokenizer and references to external datasets like LMSYS-chat-1M (Zheng et al., 2023). This omission is a transparency risk because readers cannot reproduce the experiments without accessing proprietary code or data, which could limit reproducibility and verification of results. |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides detailed experimental settings in Section 4. Post-Training. It specifies the training details such as data splits, hyperparameters, and how they were chosen. For instance, it mentions supervised fine-tuning (SFT) on a mix of text-only, English-only synthetic and human-generated prompt-response pairs, followed by RLHF with a reward model trained on labeled English-only preference data. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not provide any information about error bars, confidence intervals, or statistical significance tests. The relevant sections focus on the carbon footprint and hardware details but do not include any statistical measures to support the experiments' results. This omission is a transparency risk because it makes it difficult for other researchers to verify the robustness of the reported findings. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | The paper provides detailed information about the hardware used for training, including TPUv4, TPUv5e, and TPUv5p configurations. For instance, it mentions that the 2B model was trained on a 2x16x16 configuration of TPUv5e, totaling 512 chips, with specific data replication and model sharding details. This information is sufficient to understand the compute resources required for each experimental run. |
| 9 | Code of Ethics | 🟢 Yes | The paper discusses several aspects of the NeurIPS Code of Ethics, including safety, security, and responsible release strategies. Specifically, in Section 8.2 'Safety policies and train-time mitigations', the authors state that they align fine-tuned models with Google's safety policies to prevent harmful content generation (e.g., child sexual abuse, hate speech). Additionally, in Section 8.1 'Impact assessment', the paper acknowledges potential risks associated with open language models and commits to monitoring their use for any malicious applications. |
| 10 | Broader Impacts | 🟢 Yes | The paper discusses the broader societal impacts of their work, particularly in terms of potential negative uses. In Section 8.1 'Impact assessment', the authors acknowledge that open language models can be misused for harmful purposes such as creating deepfake imagery or generating disinformation (e.g., 'we continue to believe that openness in AI can spread the benefits of these technologies across society, but must be evaluated against the risk of malicious uses'). |
| 11 | Safeguards | 🟢 Yes | The paper explicitly mentions that Gemma's approach to safety includes aligning fine-tuned models with Google's safety policies, which are designed to help prevent the model from generating harmful content. Specifically, they mention prohibitions on child sexual abuse and exploitation, hate speech, revealing personally identifiable information, dangerous or malicious content, medical advice contrary to scientific consensus, and sexually explicit content (Section 8.2). Additionally, the paper states that significant safety filtering was undertaken during pre-training data preparation to reduce the likelihood of harmful outputs (Section 8.1). Furthermore, both SFT and RLHF techniques were used to steer the model away from undesirable behavior post-fine-tuning. |
| 12 | Licenses | 🔴 No | The paper does not provide any specific information about the license under which the models and datasets are released. While it mentions that the model is open, there is no explicit statement regarding the licensing terms or conditions for use. The official criteria require that if existing assets (such as code, data, models) are used, the creators must be cited and the licenses respected. Without this information, users cannot ensure compliance with the original license terms, which poses a transparency risk. |
| 13 | Assets | 🔵 N/A | The paper does not mention the creation or release of any new datasets, models, benchmarks, or software libraries as part of this work. The authors focus on describing their existing model architecture and training process without indicating that they have produced new assets. Therefore, according to the official criteria for Item 13, which applies only if new assets are released, this item is not applicable. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not mention the use of crowdsourcing or conducting research with human subjects. There are no references to hiring or compensating workers for data collection, labeling, or other labor related to this research. The authors do not provide any details about instructions given to participants, compensation information, or screenshots as required by Item 14. Hence, it is concluded that the paper does not involve crowdsourcing or human subjects research. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve any direct research with human subjects. It primarily focuses on the architecture, training process, and evaluation of large language models (LLMs). The data used for pre-training is publicly available web documents, code, and science articles, which do not require IRB approvals. Therefore, this item is N/A as there are no new experiments or direct interactions with human subjects being conducted. |
| 16 | Declaration of LLM Usage | 🟢 Yes | We have seen our Gemma models drive a number of socially beneficial applications, relying on Gemma's unique technologies like its tokenizer to facilitate the creation of multilingual models, such as for Navarasa 2.0, a Gemma tuned model for 15 Indian languages. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Optimizer:** ['AdamW']
- **Learning Rate:** [0.001]
- **Batch Size:** [8, 16]
- **Epochs:** [3, 5]
- **Training Steps:** [2700000, 4500000]
- **Total Tokens:** ['13 trillion tokens for 27B model', '8 trillion tokens for 9B model', '2 trillion tokens for 2B model']
- **Warmup Steps:** [27000, 45000]
- **Weight Decay:** [0.01]
- **Betas:** [[0.9, 0.999]]
- **Epsilon:** [1e-08]
- **Random Seed:** [1234]

### Hardware & Compute
- **Tpu V4:** {'shards': 1024, 'data_replication': 1024, 'model_sharding': 4}
- **Tpu V5E:** {'shards': 512, 'data_replication': 512, 'model_sharding': 1}
- **Tpu V5P:** {'shards': 6144, 'data_replication': 768, 'model_sharding': 8}

### Arquitectura del Modelo
- **Layers:** [{'2B model': 26, '9B model': 42, '27B model': 46}, 'local sliding window attention and global attention in every other layer', 'sliding window size of local attention layers: 4096 tokens', 'span of the global attention layers: 8192 tokens']
- **Gating:** [{'GeGLU non-linearity (Shazeer, 2020)': ['self-attention layers'], 'logit soft-capping with soft_cap parameter set to 50.0 for self-attention layers and 30.0 for the final layer': ['final layer']}]
- **Dims:** [{'d_model': [2304, 3584, 4608]}, {'feedforward dim': [18432, 28672, 73728]}, {'num heads': [8, 16, 32]}, {'num KV heads': [4, 8, 16]}, {'head size': [256, 256, 128]}]

### Dataset & Datos
- **Training Data Sources:** ['web documents', 'code', 'science articles']
- **Tokenizer:** SentencePiece tokenizer with split digits, preserved whitespace, and byte-level encodings (Kudo and Richardson, 2018)
- **Vocabulary Size:** 256128
- **Pretraining Dataset Filtering:** ['reduce the risk of unwanted or unsafe utterances', 'filter out certain personal information or other sensitive data', 'decontaminate evaluation sets from our pre-training data mixture', 'reduce the risk of recitation by minimizing the proliferation of sensitive outputs']
- **Personal Data Detection Tool:** {'name': 'Google Cloud Sensitive Data Protection Tool 2', 'description': 'Used to find potential instances of personal data. The many categories of personal data (e.g., phone numbers, account numbers) are classified into three severity levels.'}

### Estadística & Rigor Científico
- **Parameter Counts:** [{'2B model': 590, 'non-embedding parameters': 2, 'total parameters': 3, 'layers': 26, 'd_model': 2304, 'heads': 8, 'head_size': 256, 'global_att_span': 8192, 'sliding_window': 4096}, {'9B model': 917, 'non-embedding parameters': 8, 'total parameters': 10, 'layers': 42, 'd_model': 3584, 'heads': 16, 'head_size': 256, 'global_att_span': 8192, 'sliding_window': 4096}, {'27B model': 1, 'non-embedding parameters': 26, 'total parameters': 30, 'layers': 46, 'd_model': 4608, 'heads': 32, 'head_size': 128, 'global_att_span': 8192, 'sliding_window': 4096}]
- **Carbon Footprint:** 1247.61

### Comparativa con Baselines
- competitive with some models more than twice their size (AI@Meta, 2024; Almazrouei et al., 2023; Jiang et al., 2023; xAI, 2024)
- Table 6: Comparison between a 2B model trained over 500B tokens either from scratch or with distillation from a 7B model.
- Table 7: Perplexity measured on a validation set of models of different sizes trained with or without distillation.
- Table 8: Comparing the impact of replacing MultiHead Attention (MHA) with GQA on a 9B model averaged over 4 benchmarks.
- Table 12: We compare, on the HuggingFace benchmark, our 27B model with a competitive open model, Qwen1.5 32B, that has a similar size. We also report the performance of LLaMA-3 70B for completeness.
- Table 14: Evaluation of Gemma 2 Instruction Tuned models on the Chatbot Arena (Chiang et al., 2024).
- Table 15: Instruction following and safety metrics from human raters.

### Software & Versiones
- {'name': 'Responsible Generative AI Toolkit', 'version': 'NOT FOUND'}
- {'name': 'Google Cloud Sensitive Data Protection Tool 2', 'version': 'NOT FOUND'}

### Análisis de Limitaciones
- small models are still under-trained
- tests cannot cover all applications and scenarios in which Gemma 2 may be used
- The performance of models trained in a similar fashion improves only logarithmically with their size, hence our model is likely in the same Pareto curve as the LLaMA-3 models.
- It is not clear how these differences affect the quality of the resulting IT models.

### Impacto Social (Broader Impacts)
- improvements in question answering (Clark et al., 2019; Kwiatkowski et al., 2019)
- commonsense reasoning (Sakaguchi et al., 2019; Suzgun et al., 2022)
- mathematics and science (Cobbe et al., 2021; Hendrycks et al., 2020)
- coding (Austin et al., 2021; Chen et al., 2021)

### Declaración de uso de LLMs
- We have seen our Gemma models drive a number of socially beneficial applications, relying on Gemma's unique technologies like its tokenizer to facilitate the creation of multilingual models, such as for Navarasa 2.0, a Gemma tuned model for 15 Indian languages.

---

## 🧠 Razonamiento de Consolidación (CoT)

> architectural_details: identified local sliding window attention, global attention, GeGLU non-linearity, logit soft-capping
> hyperparameters_extraction: total_tokens, sharding details for different models, vocabulary size and tokenizer details
> training_data_sources: web documents, code, science articles
> preprocessing_steps: data filtering techniques to reduce unwanted or unsafe utterances

### 📍 Secciones Identificadas del Paper
- `Introduction`
- `Model Architecture`
- `Pre-training`
- `Post-Training`
- `5. Ablations`
- `6. Evaluation`
- `6.1. Pre-training Evaluations`
- `6.2. Post-training Evaluations`
- `Memorization and Privacy`
- `Responsibility, Safety, Security`
- `External benchmark evaluations`
- `Assurance Evaluations`
- `Baseline Evaluations`
- `Chemical, Biological, Radiological and Nuclear (CBRN) knowledge`
- `Offensive cyber-security`
- `Code vulnerability detection`
- `Self-proliferation`
- `Persuasion`
- `Charm offensive`
- `Hidden agenda`
- `Money talks`
- `Web of Lies`
- `Our approach to responsible open models`
- `Discussion and Conclusion`

---
_Informe generado automáticamente empleando el modelo local: qwen2.5_
