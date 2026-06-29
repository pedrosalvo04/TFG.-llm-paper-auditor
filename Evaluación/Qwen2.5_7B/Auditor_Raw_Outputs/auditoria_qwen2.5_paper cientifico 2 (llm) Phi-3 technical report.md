# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 2 (llm) Phi-3 technical report.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-28 10:48:10 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 1585.17s |
| 📊 **Caracteres Analizados** | 70,371 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **2 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 7
- **No Cumple (No):** 5
- **No Aplica (N/A):** 4
- **Ítems con Alerta:** 2

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The paper's claims in the abstract and introduction are supported by the experimental results. For instance, the claim that 'phi-3-mini model achieves similar level of language understanding and reasoning ability as much larger models' is backed by Table 2 which shows comparable performance on various benchmarks (e.g., MMLU, MT-bench). Additionally, the claim about phi-3-mini being capable of running locally on a modern phone while achieving quality on par with larger models like Mixtral 8x7B and GPT-3.5 is supported by the hardware details in Section 6 Weakness, which mentions that 'phi-3-mini can be quantized to 4-bits, occupying ≈ 1.8GB of memory' and can run on a modern phone like iPhone 14 with A16 Bionic chip. |
| 2 | Limitations | 🟢 Yes | The paper explicitly mentions limitations in the 'Weakness' section, such as the model's limited factual knowledge and its restricted language to English. For example, it states that 'the model simply does not have the capacity to store too much 'factual knowledge', which can be seen for example with low performance on TriviaQA.' Additionally, there is a discussion about the need for augmentation with a search engine to address certain limitations. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper does not contain any theoretical results, proofs, or assumptions related to the Phi-3.5-Vision model's architecture, training process, or performance benchmarks. The technical specifications and experimental results are described in detail, but there is no mention of theoretical foundations or mathematical proofs that would require explicit statement of assumptions. Therefore, this item does not apply as per the NeurIPS 2026 criteria. |
| 4 | Experimental Result Reproducibility | 🔴 No | The paper lacks any information about making experimental results reproducible. Specifically, there are no URLs or instructions provided for accessing the authors' own original code, model weights, or newly collected datasets used for the main experiments. The only hardware details mentioned pertain to the device type and quantization levels but do not address the reproducibility of the results. This omission poses a transparency risk as it makes it difficult for other researchers to verify or replicate the findings. |
| 5 | Open Access to Data and Code | 🔴 No | The paper does not provide any URLs or instructions that grant access to the authors' own original code, model weights, or newly collected datasets used for the main experiments. The relevant sections of the paper mention the use of publicly available web data and synthetic data, but do not provide any details on how these were obtained or processed by the authors themselves. Additionally, there is no indication that the authors have released their own implementation of the model or the training code. This omission poses a transparency risk as it prevents other researchers from reproducing the experiments and verifying the results. |
| 6 | Experimental Setting / Details | 🟢 Yes | Architecture The Phi-3.5-Vision (4.2B parameters) is a multimodal model designed to process an image/multi-image and a textual prompt as inputs, and subsequently generate textual outputs. This model is composed of two primary components: an image encoder, i.e., CLIP ViT-L/14 [RKH + 21] and a transformer decoder, i.e., phi-3.5-mini. The visual tokens, once extracted by the image encoder, are then combined with text tokens in an interleaved way (no particular order for image and text tokens). To accommodate high-resolution images and various aspect ratios, a dynamic cropping strategy [DZZ + 24b] is utilized to split the input image into a 2d array of blocks, where the tokens of the blocks are concatenated to represent the whole image. For multi-image input, we simply concatenated tokens from each images together. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not provide any information about error bars, confidence intervals, or statistical significance tests. The statistics section only reports benchmark results such as MMLU and MT-bench scores without any indication of the variability or uncertainty associated with these results. This lack of statistical measures means that it is impossible to assess the reliability and robustness of the reported performance. According to the official criteria, this constitutes a transparency risk because readers cannot determine whether the observed differences in performance are statistically significant. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | The paper mentions hardware details such as 'Modern phone (for phi-3-mini)', 'iPhone 14 with A16 Bionic chip', and quantization levels like 'phi-3-mini can be quantized to 4-bits, occupying ≈ 1.8GB of memory'. These details provide sufficient information about the compute resources used for the experiments. |
| 9 | Code of Ethics | 🟢 Yes | The paper discusses the safety and security measures taken during the development of Phi-3-mini, including red-teaming processes and automated testing. Specifically, it states: 'Phi-3-mini was developed in accordance with Microsoft's responsible AI principles. The overall approach consisted of safety alignment in post-training, red-teaming, automated testing and evaluations across dozens of RAI harm categories.' This demonstrates that the authors have considered potential harms and taken steps to mitigate them. |
| 10 | Broader Impacts | 🔵 N/A | The paper focuses on technical specifications, benchmarks, and safety measures of the Phi-3-mini model. There is no discussion of potential negative societal impacts or broader implications of the work beyond its technical capabilities. Given that this appears to be a foundational research paper without direct application to specific societal issues, it does not require a dedicated discussion of broader impacts. |
| 11 | Safeguards | 🟢 Yes | The paper states, 'Phi-3-mini was developed in accordance with Microsoft's responsible AI principles. The overall approach consisted of safety alignment in post-training, red-teaming, automated testing and evaluations across dozens of RAI harm categories.' This indicates that the model has been subjected to rigorous safety checks and evaluations designed to mitigate risks associated with misuse. |
| 12 | Licenses | 🔴 No | The paper does not provide any specific information about the licensing terms for the model or its components. While it mentions that the code is released under the MIT license, there is no explicit statement regarding the usage guidelines or restrictions for the model itself. Given that the model has a high risk of misuse due to its capabilities in generating harmful content (as evidenced by the RAI harm categories), the lack of clear licensing terms and usage guidelines constitutes a transparency risk. |
| 13 | Assets | 🔵 N/A | The paper does not mention the creation or release of any new datasets, model weights, benchmarks, or software libraries as part of this work. The assets mentioned (training dataset and additional data) are described as existing publicly available resources that have been filtered and used for training. Therefore, since no new assets are being released, Item 13 does not apply. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not mention any hiring or compensation of human workers to collect or label new data. The training dataset is described as a scaled-up version of the one used for phi-2, composed of heavily filtered publicly available web data and synthetic data. There is no indication that the authors conducted any new research involving human subjects or paid any workers. Therefore, Item 14 does not apply. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve any direct research with human subjects. It focuses on the technical specifications and performance of a language model, phi-3, which is based on publicly available data and synthetic data generated by LLMs. The use of such models for generating training data or benchmarks does not constitute new human experiments that would require IRB approval. Therefore, N/A is applicable as per the official criteria. |
| 16 | Declaration of LLM Usage | 🟢 Yes | The paper states: 'A scaled-up version of the one used for phi-2, composed of heavily filtered publicly available web data and synthetic data.' This indicates that LLMs were used to generate synthetic data as part of the training process. Synthetic data generation is an important component of the core methods in this research. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Total Tokens:** ['3.3T tokens for phi-3-mini', '4.8T tokens for phi-3-small']

### Hardware & Compute
- **Device:** ['Modern phone (for phi-3-mini)', 'iPhone 14 with A16 Bionic chip']
- **Quantization:** ['phi-3-mini can be quantized to 4-bits, occupying ≈ 1.8GB of memory']

### Arquitectura del Modelo
- **Phi-3-Mini:** ['Transformer decoder architecture', 'Default context length: 4K', 'LongRope version extends context length to 128K (called phi-3-mini-128K)']
- **Phi-3-Small:** ['7B parameters, 32 heads, 32 layers, hidden size of 4096', 'GEGLU activation', 'Maximal Update Parametrization (muP) for hyperparameter tuning on a small proxy model and transfer to the target 7B model', 'Grouped-query attention with 4 queries sharing 1 key']
- **Phi-3.5-Moe:** ['Mixture-of-Experts (MoE) architecture', 'Top2 routing among 16 expert networks, each a separate GLU network', 'Routing module selectively activates 2 out of 16 expert networks for each token', 'Total parameters: 6.6B activated from 16 × 3.8B model']

### Dataset & Datos
- **Training Dataset:** ['A scaled-up version of the one used for phi-2, composed of heavily filtered publicly available web data and synthetic data.']
- **Additional Data:** ["Heavily filtered publicly available web data according to 'educational level'", 'Synthetic LLM-generated data']

### Estadística & Rigor Científico
- **Benchmarks:** [{'model': 'phi-3-mini', 'benchmark': 'MMLU', 'result': 69}, {'model': 'phi-3-mini', 'benchmark': 'MT-bench', 'result': 8.38}, {'model': 'phi-3-small', 'benchmark': 'MMLU', 'result': [75, 78]}, {'model': 'phi-3-small', 'benchmark': 'MT-bench', 'result': [8.7, 8.9]}]
- **Scaling Laws:** ['phi-1.5, phi-2, phi-3-mini, phi-3small vs Llama-2 family of models (7B, 13B, 34B, 70B) trained on the same fixed data: Log of MMLU error versus log of model size']

### Comparativa con Baselines
- {'model_name': 'phi-3-mini vs Mixtral 8x7B and GPT-3.5 on MMLU and MT-bench benchmarks', 'results': {}}
- {'model_name': 'phi-3.5-MoE vs Llama 3.1 and the Mixtral series, and on par with Gemini-1.5-Flash and GPT-4O-mini'}

### Análisis de Limitaciones
- The development of a compact language model that rivals the capabilities of ChatGPT while fitting on a phone is achieved solely by changing the training data.

---

## 🧠 Razonamiento de Consolidación (CoT)

> Identified the key technical components and architectural choices, such as transformer decoder architecture, LongRope for extended context length, MoE with top2 routing, and specific hyperparameters.
> Captured detailed statistics from benchmarks and training data usage.
> Noted hardware details including device type and quantization levels.
> Extracted all relevant information about the models' performance on various benchmarks.

### 📍 Secciones Identificadas del Paper
- `Abstract`
- `1 Introduction`
- `2 Technical Specifications`
- `3 Academic benchmarks`
- `4 Multilingual and Long Context`
- `5 Safety`
- `6 Weakness`
- `7 Phi-3.5-Vision`
- `7.1 Technical Specifications`
- `7.2 Academic benchmarks`

---
_Informe generado automáticamente empleando el modelo local: qwen2.5_
