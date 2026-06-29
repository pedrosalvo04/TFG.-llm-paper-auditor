# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 16 (llm) SAM 2.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-28 17:20:26 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 382.21s |
| 📊 **Caracteres Analizados** | 172,737 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **1 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 8
- **No Cumple (No):** 3
- **No Aplica (N/A):** 5
- **Ítems con Alerta:** 1

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The paper's claims in the abstract and introduction are accurately reflected by the experimental results. The introduction states that SAM 2 demonstrates strong performance in both static image and video domains, yet it encounters difficulties in certain scenarios (such as shot changes, crowded scenes, occlusions, and thin details). These limitations are supported by the detailed discussion of challenges faced by SAM 2 in various scenarios. Additionally, the paper claims that SAM 2 can produce better segmentation accuracy while using fewer interactions than prior approaches, which is validated through experiments showing a step-change improvement over existing methods. |
| 2 | Limitations | 🟢 Yes | The paper explicitly includes a 'Limitations' section that discusses various challenges and limitations faced by SAM 2. The authors mention difficulties in tracking objects across shot changes, handling crowded scenes, dealing with thin or fast-moving details, and accurately segmenting objects with similar appearances. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper does not contain any theoretical results, proofs, or assumptions. The official criteria for Item 3 require that if the paper includes theoretical results, it must state all assumptions and include complete proofs. Since there are no such elements in this paper, the item is N/A. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The paper provides a GitHub repository URL (https://github.com/facebookresearch/sam2) where the authors' own implementation is publicly accessible. This satisfies the requirement for experimental result reproducibility as per the official criteria, which states that making it possible for others to replicate the model with the same dataset or providing access to the model are acceptable ways of ensuring reproducibility. |
| 5 | Open Access to Data and Code | 🟢 Yes | The paper provides a URL to the GitHub repository for SAM2, which is an open-source implementation of their model: `https://github.com/facebookresearch/sam2`. Additionally, the authors mention that they have released the code and data needed to reproduce the main experimental results. This aligns with the criteria stating that if you ran experiments, you should include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL). |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides detailed information about the training setup, including data splits and hyperparameters. For instance, it mentions that the results reported in the zero-shot experiments section follow a default setup using Hiera-B+ image encoder with a resolution of 1024 and trained on the full combination of datasets (SA-V dataset). The paper also specifies the optimizer used (`AdamW`), learning rate schedule, batch size for different tasks, and other relevant training details. This information is crucial for understanding how the experiments were conducted. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not provide error bars, confidence intervals, or any other form of statistical significance measures for the reported results. While the paper reports metrics such as J & F and mIoU, it lacks the necessary statistical information to assess the reliability and robustness of these measurements. This omission is particularly concerning given that machine learning experiments often involve variability due to factors like data sampling, initialization, and batch processing. Without this information, readers cannot properly evaluate the significance of the reported results. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | The paper provides sufficient details about the compute resources used for experiments. Specifically, it mentions that SAM2 runs at real-time speeds on an A100 GPU with a batch size of one, achieving 43.8 FPS and 30.2 FPS for different model configurations (Hiera-B+ and Hiera-L). This information allows readers to understand the computational requirements needed to reproduce the experiments. |
| 9 | Code of Ethics | 🟢 Yes | The paper includes a discussion of ethical considerations in the limitations section, specifically mentioning demographic group performance analysis and suggesting researchers perform their own fairness evaluation. Additionally, the dataset card for SA-V contains information about the geographic diversity and self-reported demographics of crowdworkers, which aligns with the NeurIPS Code of Ethics regarding privacy and consent. |
| 10 | Broader Impacts | 🟢 Yes | The paper discusses potential negative societal impacts, particularly in terms of fairness considerations. The limitations section mentions the need for researchers to perform their own fairness evaluation when using SAM 2 in new settings. |
| 11 | Safeguards | 🔵 N/A | The paper does not present a high-risk artefact that could be misused for generating harmful content, enabling surveillance, synthesising dangerous information, or being weaponised. The work focuses on improving video segmentation capabilities and does not involve any direct path to misuse as defined by the criteria. Therefore, it is not applicable to require safeguards in this context. |
| 12 | Licenses | 🔴 No | The paper uses existing assets such as datasets and models but does not explicitly cite the creators or respect their licenses. The only license mentioned is 'Creative Commons Attribution 4.0 International Public License', which applies to a video segmentation dataset, while no specific license for code or other resources is provided. This omission constitutes a transparency risk because it fails to acknowledge the original creators and terms of use, potentially violating intellectual property rights. |
| 13 | Assets | 🔵 N/A | The paper does not mention the creation or release of any new datasets, model weights, benchmarks, or software libraries as part of this work. The assets mentioned (such as SA-V dataset and EgoExo4D dataset) are described as existing public resources that were used in the experiments. Therefore, since no new assets are being released, there is no documentation obligation for these items under Item 13. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not explicitly mention hiring or compensating human workers to collect or label new data. The EgoExo4D dataset is mentioned as containing self-reported demographic information, but this appears to be from existing videos rather than newly collected data through crowdsourcing. Therefore, there is no evidence of new human research or compensation for workers in the paper, and Item 14 does not apply. |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve direct research with human subjects. It primarily focuses on the development and evaluation of a video segmentation model, SAM 2, using existing datasets such as SA-V Manual, SA-V Manual+Auto, Internal, and EgoExo4D. The dataset descriptions do not indicate any new human experiments or interactions that would require IRB approval. Therefore, based on the official criteria, this item is N/A. |
| 16 | Declaration of LLM Usage | 🔵 N/A | The paper does not mention any usage of LLMs as a core component of the methodology. The LLM usage section is empty, and there are no indications that LLMs were used for synthetic data generation or distillation. Therefore, based on the official criteria, this item is N/A. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Optimizer:** ['AdamW']
- **Learning Rate:** ['reciprocal square-root schedule (Zhai et al., 2022)']
- **Batch Size:** {'image_task': 16, 'video_task': 1}
- **Epochs:** ['not explicitly mentioned']
- **Training Steps:** ['7 correction clicks in SAM 2 training', '50k iterations for fine-tuning on challenging videos']
- **Iterations:** ['7 correction clicks in SAM 2 training', '50k iterations for fine-tuning on challenging videos']
- **Total Tokens:** ['not explicitly mentioned']
- **Warmup Steps:** ['not explicitly mentioned']
- **Weight Decay:** ['not explicitly mentioned']
- **Betas:** ['not explicitly mentioned']
- **Epsilon:** ['not explicitly mentioned']
- **Random Seed:** ['not explicitly mentioned']

### Hardware & Compute
- {'model_name': 'Hiera-B+', 'resolution': 1024, 'speed_fps': 43.8}
- {'model_name': 'Hiera-L', 'speed_fps': 30.2}

### Dataset & Datos
- {'dataset_name': 'SA-V Manual', 'num_videos': 50.9, 'duration': '196.0 hr', 'num_masklets': 190.9, 'num_masks': 10000000.0, 'num_frames': 4200000.0}
- {'dataset_name': 'SA-V Manual+Auto', 'num_videos': 50.9, 'duration': '196.0 hr', 'num_masklets': 642.6, 'num_masks': 35500000.0, 'num_frames': 4200000.0}
- {'dataset_name': 'Internal', 'num_videos': 62.9, 'duration': '281.8 hr', 'num_masklets': 69.6, 'num_masks': 5400000.0, 'num_frames': 6000000.0}
- {'dataset_name': 'SA-V dataset', 'videos': {'resolutions': ['range from 240p to 4K with average of 1,401 × 1,037'], 'duration': {'range': [4, 2.3], 'average': 13.8}, 'total_frames': 4200000.0, 'total_hours': 196}, 'masklets': {'size_distribution': {'normalized_by_resolution': '>88% have a normalized mask area less than 0.1'}, 'geographic_diversity': ['recorded across 47 countries'], 'demographics': ['self-reported demographics of the crowdworkers who recorded the videos']}, 'automatic_masklets': {'generation_method': {'grid_prompting': [32, 16, 4]}, 'post_processing_steps': [{'remove_tiny_components': '<200 pixels'}, {'fill_holes': '<200 pixels'}]}}
- {'dataset_name': 'EgoExo4D dataset', 'annotations': ['gender', 'age']}

### Código & Repositorio
- {'repository_url': 'https://github.com/facebookresearch/sam2', 'release_mention': 'NOT FOUND'}

### Estadística & Rigor Científico
- {'metric': 'J & F', 'value': 76.6, 'dataset': 'SA-V val'}
- {'metric': 'J & F', 'value': 88.6, 'dataset': 'YTVOS 2019 val'}

### Comparativa con Baselines
- {'method_name': 'SAM+XMem++', 'accuracy': 56.9}
- {'method_name': 'SAM+Cutie', 'accuracy': 56.7}
- {'method_name': 'SAM2', 'accuracy': 64.7}

### Software & Versiones
- {'PyTorch': '2.3.1', 'CUDA': '12.1'}

### Análisis de Limitaciones
- The SA-V dataset has a high disappearance rate of 36.4%.
- SAM 2 can generate better segmentation accuracy, with > 3 × fewer interactions.

### Licencias detectadas
- {'license': 'Creative Commons Attribution 4.0 International Public License at https://ai.meta.com/datasets/segment-anything-video/', 'type': 'Video segmentation dataset'}
- {'license': 'Apache 2.0', 'type': 'NOT FOUND'}

### Impacto Social (Broader Impacts)
- In Section E.1.1 of the main text we analyze SAM 2 performance on people across demographic groups.
- When using SAM 2 in new settings, we suggest that researchers perform their own fairness evaluation for SAM 2 specific to their use case.

### Sujetos Humanos & Crowdsourcing
- EgoExo4D dataset contains self-reported demographic information supplied by the subject of the video.

### 📍 Secciones Identificadas del Paper
- `Introduction`
- `5.1 Data collection and annotation`
- `6 Zero-shot experiments`
- `6.1 Promptable video segmentation`
- `6.2 Semi-supervised video object segmentation`
- `D.1 Pre-training`
- `D.2 Training details`
- `D.3 Speed benchmarking`
- `E Data details`
- `F Details on zero-shot transfer experiments`
- `## H Model, data and annotation cards`
- `## H.1 Model card`
- `## H.2 Dataset card for SA-V dataset`

---
_Informe generado automáticamente empleando el modelo local: qwen2.5_
