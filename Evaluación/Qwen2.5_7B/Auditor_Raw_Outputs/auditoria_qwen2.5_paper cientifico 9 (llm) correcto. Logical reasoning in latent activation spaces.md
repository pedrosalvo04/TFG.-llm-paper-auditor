# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 9 (llm) correcto. Logical reasoning in latent activation spaces.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-28 15:33:09 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 698.3s |
| 📊 **Caracteres Analizados** | 90,066 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **2 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 9
- **No Cumple (No):** 4
- **No Aplica (N/A):** 3
- **Ítems con Alerta:** 2

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The paper's claims in the abstract and introduction are supported by the experimental results. The abstract states that AR improves transparency, robustness, and control across various tasks, which is corroborated by the experimental evaluations on PrOntoQA, ProverQA, BeaverTails, and Rail2Country. Specifically, the paper mentions that AR outperforms baselines in multi-hop reasoning (PrOntoQA), handles implicit or noisy cues (Rail2Country), generalizes to diverse linguistic scenarios (ProverQA), and captures abstract concepts (BeaverTails). These claims are substantiated by the detailed statistics provided in the supplementary material, which show significant improvements over various models including larger instruction-tuned models like GPT-4o. |
| 2 | Limitations | 🟢 Yes | The paper explicitly mentions limitations in the 'Limitations' section. It states that current SAEs may have issues with polysemous features, context-dependency, and failure to capture abstract notions. Additionally, it notes that pretrained SAEs offer limited control over concept discovery and representation. |
| 3 | Theory, Assumptions & Proofs | 🟢 Yes | "For the PrOntoQA experiments, we instantiate AR with multi-feature concept representations R multi . Unless otherwise noted, activations are aggregated using the mean operator and steering follows the mean-shift update rule."  "For the ProverQA experiments, we instantiate AR with multi-feature concept representations R multi . Unless otherwise noted, activations are aggregated using the mean operator and steering follows the mean-shift update rule with a uniform weighing of steering vectors." |
| 4 | Experimental Result Reproducibility | 🔴 No | The paper does not provide any code or model URLs that grant access to the authors' own original code, model weights, or newly collected datasets used for the main experiments. The only hardware requirements and runtime efficiency details are provided, but no instructions or links are given to reproduce the results. This constitutes a transparency risk as it makes it difficult for other researchers to verify the experimental results. |
| 5 | Open Access to Data and Code | 🔴 No | The paper does not provide any URLs or instructions that grant access to the authors' own original code, model weights, or newly collected datasets used for the main experiments. The relevant sections describe the models and experimental setups in detail but do not include links or instructions for accessing the code or data necessary to reproduce the results. This omission poses a transparency risk as it prevents other researchers from verifying the experiments and replicating the findings. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 6 | Experimental Setting / Details | 🟢 Yes | === ## A EXPERIMENTAL SETUP ===  Models. For our experiments, AR is evaluated on two backbone models: Llama-3.1-8B AI@Meta (2024) with the EleutherAI sae-llama-3.1-8b-64x EleutherAI (2024) attached at layer 23, and Gemma-2-9B Team (2024) with the gemma-scope-9b-pt-res-canonical SAE Lieberum et al. (2024) attached at layer 20. All experiments are conducted with greedy decoding.  === ## A.1 PRONTOQA EXPERIMENTAL SETUP ===  For the PrOntoQA experiments, we instantiate AR with multi-feature concept representations R multi . Unless otherwise noted, activations are aggregated using the mean operator and steering follows the mean-shift update rule. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not report error bars, confidence intervals, or statistical significance tests for the experiments. The results are presented as exact match accuracies without any indication of variability or uncertainty in the measurements. This lack of reporting is a transparency risk because it makes it difficult to assess the robustness and reliability of the reported findings. While the paper mentions that greedy decoding was used, this does not eliminate the presence of variance due to factors such as data sampling, initialization, and batching. Therefore, according to NeurIPS criteria, statistical measures should be provided to ensure transparency. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | The paper provides detailed information on the hardware resources used for the experiments. Specifically, it mentions that the experiments were conducted using a cluster with 8 NVIDIA A100-SXM4 GPUs (each with 80GB of memory) and 2048GB of RAM. The compute node details include the GPU model, count, and memory, as well as the CPU model and core count. |
| 9 | Code of Ethics | 🟢 Yes | The paper adheres to the ICLR Code of Ethics and explicitly states that their experiments use public benchmarks (PrOntoQA, ProverQA, BeaverTails) and a newly introduced synthetic dataset Rail2Country. Although Rail2Country contains no personal data, BeaverTails may include sensitive or privacy-invasive text; they use it strictly for research on safety evaluation in accordance with its license. |
| 10 | Broader Impacts | 🟢 Yes | The paper discusses the broader impacts of their work, particularly in terms of logical reasoning and model transparency. They state that AR turns latent activations into a substrate for logical reasoning, enhancing LLM abilities across several dimensions, which not only improves reasoning performance but also increases transparency and control. |
| 11 | Safeguards | 🔵 N/A | The paper does not present a high-risk artefact that could be misused for generating harmful content, enabling surveillance, synthesising dangerous information, or being weaponised. The usage of LLMs in this research is limited to aiding in polishing and rephrasing parts of the manuscript, which does not pose a significant risk for misuse as per the provided context. Therefore, the item 'Safeguards' is not applicable under the official criteria. |
| 12 | Licenses | 🟢 Yes | G ETHICS STATEMENT: Our framework enables model steering, which could in principle be misused; we explicitly condemn such uses and stress that AR was developed to improve transparency, safety, and alignment. |
| 13 | Assets | 🔵 N/A | The paper does not mention the creation or release of any new datasets, models, benchmarks, or software libraries as part of this work. The experimental setups and models used are based on existing public resources such as Llama-3.1-8B AI@Meta (2024), EleutherAI sae-llama-3.1-8b-64x, Gemma-2-9B Team (2024), and gemma-scope-9b-pt-res-canonical SAE Lieberum et al. (2024). Since no new assets are created or released by the authors, this item does not apply. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not mention any use of crowdsourcing or conducting research with human subjects. The experimental setups and datasets used are based on existing public benchmarks such as PrOntoQA, ProverQA, BeaverTails, and Rail2Country. There is no indication that the authors hired or compensated workers to collect or label new data. Therefore, this item does not apply. |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve any direct research with human subjects. It primarily focuses on the logical reasoning capabilities of latent activation spaces and uses existing public datasets such as PrOntoQA, ProverQA, BeaverTails, and Rail2Country for experimental evaluations. Since no new human experiments are conducted, and only standard open datasets are used, IRB approvals are not required according to NeurIPS 2026 criteria. |
| 16 | Declaration of LLM Usage | 🟢 Yes | We used LLMs to aid in polishing and rephrasing parts of the manuscript, including improving readability. The model was not used for generating ideas, designing methods, running experiments, or analyzing results. All scientific content, claims, and conclusions are solely the responsibility of the authors. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Optimizer:** ['NOT FOUND']
- **Learning Rate:** [0.9, 0.95]
- **Betas:** [[0.9, 0.95], [0.9, 0.95]]

### Hardware & Compute
- **Compute Node:** {'gpu_count': 8, 'gpu_model': 'NVIDIA A100-SXM4', 'gpu_memory': 80, 'cpu_model': 'AMD EPYC 7313', 'cpu_cores': 16}
- **Ram:** 2048

### Arquitectura del Modelo
- **Layers:** ['Llama-3.1-8B AI@Meta (2024) with the EleutherAI sae-llama-3.1-8b-64x EleutherAI (2024) attached at layer 23', 'Gemma-2-9B Team (2024) with the gemma-scope-9b-pt-res-canonical SAE Lieberum et al. (2024) attached at layer 20']
- **Gating:** ['Gated Attention']
- **Moe:** [{'EleutherAI sae-llama-3.1-8b-64x': {'width': 262}}, {'gemma-scope-9b-pt-res': {'width': 131}}]
- **Dims:** [{'model': 'EleutherAI sae-llama-3.1-8b-64x', 'width': 262}, {'model': 'gemma-scope-9b-pt-res', 'width': 131}]

### Dataset & Datos
- **Dataset Name:** ['PrOntoQA, ProverQA, BeaverTails, Rail2Country']

### Estadística & Rigor Científico
- **A.3 Proverqa Experimental Setup:** [{'Llama3.1 8B': 51.0, 'w/ instruct': 71.0, 'w/ instruct CoT': 77.8}, {'Gemma2 9B': 48.5, 'w/ instruct': 77.0, 'w/ instruct CoT': 86.3}]
- **A.4 Safety Experimental Setup:** [{'Llama3.1 8B': 0.1066, 'Llama3.1 8B IT (CoT)': 1.6474, 'DeepSeek-R1-Distill-Llama-8B': 14.9902, 'AR (Llama3.1 8B)': 0.3747}]
- **A.4.1 Dataset Details:** [{'PrOntoQA': [51.0, 50.8, 50.3], 'Rail2Country (R2C-Mono)': [41.0], 'Rail2Country (R2C-Meta)': [29.7], 'ProverQA (Easy)': [43.6], 'ProverQA (Medium)': [33.6], 'ProverQA (Hard)': [36.8]}, {'Llama3.1 8B': [51.0, 50.8, 50.3], 'w/ instruct': [71.0, 60.2, 58.5], 'w/ instruct CoT': [77.8, 70.6, 59.7]}, {'Gemma2 9B': [48.5, 47.5, 47.9], 'w/ instruct': [77.0, 57.9, 55.0], 'w/ instruct CoT': [86.3, 64.4, 45.1]}, {'AR (our)': [95.0, 95.6, 95.3, 74.7, 62.7, 92.8, 91.0, 70.8]}]

### Comparativa con Baselines
- {'model': 'Llama3.1 8B', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 51.0}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 50.8}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 50.3}]}
- {'model': 'w/ AR (our)', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 95.0, '+44.0%': True}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 95.6, '+44.8%': True}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 95.3, '+45.0%': True}]}
- {'model': 'Gemma2 9B', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 48.5}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 47.5}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 47.9}]}
- {'model': 'w/ AR (our)', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 93.5, '+45.0%': True}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 93.5, '+46.0%': True}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 93.5, '+45.6%': True}]}
- {'model': 'Llama3.1 70B it', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 96.2}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 66.7}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 62.1}]}
- {'model': 'Gemma2 27B it', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 91.3}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 77.6}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 73.9}]}
- {'model': 'GPT-4o', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 97.3}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 74.4}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 66.4}]}
- {'model': 'DeepSeek-R1-8B', 'results': [{'task': 'PrOntoQA (1-hop)', 'accuracy': 97.3}, {'task': 'PrOntoQA (3-hops)', 'accuracy': 66.4}, {'task': 'PrOntoQA (5-hops)', 'accuracy': 82.7}]}

### Software & Versiones
- **Sae:** ["EleutherAI's SAE", 'Gemma-Scope SAE']
- **Backbone Models:** ['Llama-3.1-8B AI@Meta (2024)', 'Gemma-2-9B Team (2024)']

### Análisis de Limitaciones
- Current SAEs offer a practical way to surface sparse, often interpretable features, but they are not always perfect. Features may be polysemous, overly context-dependent, or fail to capture abstract notions.
- Pretrained SAEs allow only limited control over which concepts are discovered and how they are represented.

### Licencias detectadas
- G ETHICS STATEMENT: Our framework enables model steering, which could in principle be misused; we explicitly condemn such uses and stress that AR was developed to improve transparency, safety, and alignment.

### Impacto Social (Broader Impacts)
- AR turns latent activations into a substrate for logical reasoning, enhancing LLM abilities across several dimensions.
- AR provides a model-agnostic mechanism that not only improves reasoning performance but also increases transparency and control.

### Declaración de uso de LLMs
- Large language models (LLMs) excel at generating fluent text, but their internal reasoning remains opaque and difficult to control.
- Large language models (LLMs) demonstrate remarkable abilities in semantic disambiguation, knowledge retrieval, and generative tasks (Brown et al., 2020; OpenAI, 2023).

---

## 🧠 Razonamiento de Consolidación (CoT)

> Resumen de consolidación no generado por el modelo.

### 📍 Secciones Identificadas del Paper
- `INTRODUCTION`
- `RELATED WORK`
- `ACTIVATIONREASONING`
- `3.4 INTEGRATION INTO DOWNSTREAM TASKS`
- `4 EXPERIMENTAL EVALUATIONS`
- `6 CONCLUSION`
- `ACKNOWLEDGEMENTS`
- `A.2 RAIL2COUNTRY EXPERIMENTAL SETUP`
- `A.2.1 RAIL2COUNTRY DATASET`
- `A.3 PROVERQA EXPERIMENTAL SETUP`
- `A.4 SAFETY EXPERIMENTAL SETUP`
- `A.4.1 DATASET DETAILS`
- `B RUNTIME EFFICIENCY`
- `C HARDWARE REQUIREMENTS`
- `D LOGICAL SEMANTICS OF AR`
- `E COMPARISON TO INSTRUCT AND COT`
- `F RAIL2COUNTRY: EXTENDED RESULTS`
- `G ETHICS STATEMENT`
- `H REPRODUCIBILITY STATEMENT`
- `I LLM USAGE`

---
_Informe generado automáticamente empleando el modelo local: qwen2.5_
