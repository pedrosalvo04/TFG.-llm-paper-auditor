# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 16 (llm) SAM 2.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-24 21:26:48 |
| ⏳ **Tiempo de Ejecución** | 68.54s |
| 📊 **Caracteres Analizados** | 172,737 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **1 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 12
- **No Cumple (No):** 1
- **No Aplica (N/A):** 3
- **Ítems con Alerta:** 1

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The introduction states: 'SAM 2 delivers a step-change in the video segmentation experience. SAM 2 can produce better segmentation accuracy while using 3 × fewer interactions than prior approaches. Further, SAM 2 outperforms prior work in established video object segmentation benchmarks... and delivers better performance compared to SAM on image segmentation benchmarks, while being 6 × faster.' |
| 2 | Limitations | 🟢 Yes | Section C (Limitations) states: 'The model may fail to segment objects across shot changes and can lose track of or confuse objects in crowded scenes, after long occlusions or in extended videos... SAM 2 also struggles with accurately tracking objects with very thin or fine details especially when they are fast-moving. Another challenging scenario occurs when there are nearby objects with similar appearance.' |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper focuses on the architecture and empirical evaluation of the SAM 2 model for promptable visual segmentation. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The authors provide a dedicated repository at https://github.com/facebookresearch/sam2 and the SA-V dataset at https://ai.meta.com/datasets/segment-anything-video/. Section 4 and Appendix D provide detailed architectural descriptions, including the Hiera image encoder, memory attention mechanisms, and training hyperparameters. |
| 5 | Open Access to Data and Code | 🟢 Yes | The authors provide explicit access to both the code and the dataset used for the main experimental results. As stated in the provided context and summary, the code is hosted at 'https://github.com/facebookresearch/sam2' (Apache 2.0 license), and the SA-V dataset is available at 'https://ai.meta.com/datasets/segment-anything-video/' (CC by 4.0 license). This fulfills the NeurIPS 2026 criteria for Item 5, which requires that authors include the code, data, and instructions needed to reproduce the main experimental results, either in the supplemental material or via a URL. |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides comprehensive experimental details across multiple sections. Section 'D.2 Training' and the 'hyperparameters' section in the JSON summary detail the optimizer (AdamW), batch sizes (128 for pre-training, 1 for video tasks), learning rate strategies, and sequence lengths. Furthermore, Section 'F.1.1 Video dataset details' and 'F.3.1 Dataset details' explicitly list the 17 zero-shot video datasets and 37 interactive segmentation datasets used, including specific references for each (e.g., EndoVis 2018, LVOSv2, etc.). The criteria for Item 6 require specifying training details such as data splits, hyperparameters, and how they were chosen; the authors have provided these details in the main paper and supplementary materials, satisfying the transparency requirement. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper provides extensive quantitative results in Tables 5, 6, 16, and 17, reporting performance metrics such as J & F, mIoU, and FPS. However, these results are presented as point estimates (averages) without accompanying error bars, confidence intervals, or statistical significance tests. According to the NeurIPS 2026 criteria, authors must report error bars or other information about statistical significance for experiments supporting the main claims. As the authors have not provided these measures nor explicitly stated a scientific justification for their omission (such as prohibitive computational cost for multiple runs), the requirement for statistical transparency is not met. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | Section D.3 states: 'We conduct all benchmarking experiments on a single A100 GPU using PyTorch 2.3.1 and CUDA 12.1... For video tasks, we use a batch size of 1 following the common protocol in video segmentation.' Additionally, the JSON summary and paper context confirm: 'training_infrastructure': '256 A100 GPUs', 'training_duration': '108 hours', 'energy_consumption': '12165.12 kWH', 'carbon_emissions': '3.89 metric tons of CO2e'. |
| 9 | Code of Ethics | 🟢 Yes | The authors explicitly address ethical considerations throughout the paper, particularly in the context of data collection and human subject involvement. As noted in the provided context, the project underwent an internal review process, and the authors utilized a third-party vendor to manage crowdsourcing, ensuring that participants were compensated with an hourly wage and provided consent. Furthermore, the authors implemented specific safety measures, such as instructing crowdworkers to avoid objectionable content and providing a reporting mechanism (segment-anything@meta.com) for any concerns. This demonstrates adherence to the NeurIPS Code of Ethics regarding fair wages, human participant protocols, and data-related concerns. |
| 10 | Broader Impacts | 🟢 Yes | The authors provide a comprehensive discussion of broader impacts, including environmental considerations and potential societal harms. They explicitly report the carbon footprint of their training process (3.89 metric tons of CO2e) and discuss fairness, noting that they performed an evaluation of performance discrepancies across perceived gender and age groups. Additionally, they address privacy by applying a face-blurring model to the videos in their dataset. This aligns with the NeurIPS criteria to 'transparently communicate the known or anticipated consequences of research' and to discuss mitigation strategies for potential negative impacts. |
| 11 | Safeguards | 🔵 N/A | The paper presents SAM 2, a foundational model for promptable visual segmentation in images and videos. The authors have implemented privacy-preserving measures, such as applying a face-blurring model to the videos in the SA-V dataset, and have provided a reporting mechanism (segment-anything@meta.com) for addressing concerns. Given that the model is a perception tool for segmentation rather than a generative model capable of creating harmful content, misinformation, or weaponized data, it does not present a high risk for misuse as defined by the NeurIPS criteria. Therefore, specific usage restrictions or access controls are not required for this foundational research. |
| 12 | Licenses | 🟢 Yes | The authors explicitly state the licensing terms for their contributions: the SA-V dataset is released under the CC BY 4.0 license, and the SAM 2 code is released under the Apache 2.0 license. These are documented in the provided metadata and align with the requirement to respect the license and terms of use for assets. |
| 13 | Assets | 🟢 Yes | Appendix H, specifically sections H.1 (Model card), H.2 (Dataset card for SA-V dataset), and H.3 (Data annotation card), provide structured documentation for the newly released SA-V dataset and SAM 2 model. The paper explicitly states: 'In Appendix H, we provide model, data and annotation cards for SA-V.' These cards include details on composition, collection process, preprocessing, labeling, uses, distribution, and maintenance, fulfilling the NeurIPS 2026 requirement to document new assets via structured templates. |
| 14 | Crowdsourcing & Human Subjects | 🟢 Yes | The paper details the use of human annotators in Section E.2.1 ('Annotation protocol') and Appendix H.3 ('Data annotation card'). It describes the annotation tasks (masklet selection, tracking, and verification), the use of a data engine with human-in-the-loop, and the training of annotators. Regarding compensation, the 'human_subjects_extraction' summary confirms: 'Crowdworkers used for video capture and annotation; compensated with hourly wage; consented via third-party vendor.' This aligns with the NeurIPS Code of Ethics requirement to pay workers at least the minimum wage and provide details on the annotation process. |
| 15 | IRB Approvals | 🟢 Yes | The paper states in the 'Code of Ethics' section: 'Project underwent an internal review process' and 'Contracted third-party provided representations regarding notices and consents'. Furthermore, the 'Human subjects extraction' notes that crowdworkers were used for video capture and annotation, were compensated with an hourly wage, and consented via a third-party vendor. |
| 16 | Declaration of LLM Usage | 🔵 N/A | The paper describes the methodology for SAM 2, which is a vision-based foundation model for promptable visual segmentation. The architecture is explicitly defined as a combination of a hierarchical image encoder (Hiera), a memory attention module, a prompt encoder, and a mask decoder. There is no mention of Large Language Models (LLMs) being used as a component of the core methodology, synthetic data generation, or distillation process. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Optimizer:** AdamW
- **Learning Rate:** Half of original for fine-tuning
- **Batch Size:** {'pre_training': 128, 'SA_task_FPS': 10, 'video_tasks': 1}
- **Iterations:** {'pre_training': '200k', 'fine_tuning': '50k'}
- **Sequence Length:** 8
- **Frames Per Sequence:** {'default': 8, 'fine_tuning': 16}
- **Prompt Probabilities:** {'ground_truth_mask': 0.5, 'positive_click': 0.25, 'bounding_box': 0.25}
- **Memory Bank:** {'N_recent_frames': 'N', 'M_prompted_frames': 'M', 'memory_frames': 6, 'memory_channel_dim': 64}
- **Image Encoder Resolution:** 1024
- **Spatial Resolution:** {'ablation_default': 512, 'final_model': 1024}
- **Correction Clicks:** 7
- **N Click Per Frame:** 3
- **Iou Thresholds:** {'online': 0.75, 'construction': 0.8}
- **Annotation Time Assumptions:** {'T_loc': '1 sec', 'T_click': '1.5 sec', 'T_exam_300_frames': '30 sec'}

### Hardware & Compute
- **Training Infrastructure:** 256 A100 GPUs
- **Training Duration:** 108 hours
- **Inference Device:** Single A100 GPU (80GB)
- **Energy Consumption:** 12165.12 kWH
- **Carbon Emissions:** 3.89 metric tons of CO2e

### Arquitectura del Modelo
- **Image Encoder:** MAE pre-trained Hiera (hierarchical)
- **Image Encoder Variants:** ['Hiera-T', 'Hiera-S', 'Hiera-B+', 'Hiera-L']
- **Memory Attention:** Stack of L transformer blocks with self-attention and cross-attention to memory bank
- **Prompt Encoder:** Identical to SAM (sparse prompts: positional encodings + learned embeddings; masks: convolutions)
- **Mask Decoder:** Two-way transformer blocks, skip connections from hierarchical image encoder
- **Memory Encoder:** Convolutional module + light-weight convolutional layers
- **Memory Bank:** FIFO queue for N recent frames and M prompted frames; stores spatial feature maps and object pointers
- **Additional Components:** ['Feature Pyramid Network', 'Occlusion prediction head']
- **Positional Encoding:** ['2d-RoPE', 'Sinusoidal absolute positional embeddings', 'Windowed absolute positional embeddings']
- **Dims:** {'memory_bank_projection': 64, 'object_pointer': 256}

### Dataset & Datos
- **Dataset Name:** SA-V
- **Total Videos:** 50.9K
- **Total Masklets:** 642.6K
- **Total Masks:** 35.5M
- **Total Frames:** 4.2M
- **Total Hours:** 196
- **Composition:** 54% indoor, 46% outdoor
- **Average Duration:** 13.8 seconds
- **Disappearance Rate:** 42.5% (SA-V Manual)
- **Annotation Fps:** 6
- **Video Fps:** 24
- **Video Format:** mp4
- **Content Types:** ['locations', 'objects', 'scenes']
- **Dataset List:** ['SA-V', 'SA-1B', 'DAVIS', 'MOSE', 'YouTubeVOS', 'Internal-train', 'Internal-test', 'EndoVis 2018', 'ESD', 'LVOSv2', 'LV-VIS', 'UVO', 'VOST', 'PUMaVOS', 'Virtual KITTI 2', 'VIPSeg', 'Wildfires', 'VISOR', 'FBMS', 'Ego-Exo4D', 'Cityscapes', 'Lindenthal Camera', 'HT1080WT Cells', 'Drosophila Heart', 'LVIS', 'ADE20K', 'Hypersim', 'BBBC038v1', 'DOORS', 'DRAM', 'EgoHOS', 'GTEA', 'iShape', 'NDD20', 'NDISPark', 'OVIS', 'PPDLS', 'Plittersdorf', 'STREETS', 'TimberSeg', 'TrashCan', 'WoodScape', 'PIDRay', 'ZeroWaste-f', 'IBD', 'LCT', 'CFD', 'DH OCM']
- **Data Engine Phases:** ['Phase 1: SAMperframe', 'Phase 2: SAM+SAM2Mask', 'Phase 3: SAM 2']

### Código & Repositorio
- **Repository Url:** https://github.com/facebookresearch/sam2
- **Dataset Download:** https://ai.meta.com/datasets/segment-anything-video/

### Estadística & Rigor Científico
- **Annotation Speedup:** 8.4x faster than Phase 1
- **Sam2 Vs Sam Speed:** 6x faster
- **Interaction Reduction:** 3x fewer interactions than prior approaches
- **Video Collection Timeframe:** November 2023 - March 2024
- **Annotation Timeframe:** April 2024 - July 2024

### Comparativa con Baselines
- **Models:** ['SAM', 'XMem++', 'Cutie', 'STCN', 'SwinB-AOT', 'SwinB-DeAOT', 'RDE', 'XMem', 'SimVOS-B', 'JointFormer', 'ISVOS', 'DEVA', 'HQ-SAM', 'MiVOS', 'CiVOS']
- **Performance Summary:** SAM 2 outperforms SAM+XMem++ and SAM+Cutie on all datasets; outperforms prior work on semi-supervised VOS benchmarks; outperforms MiVOS and CiVOS on DAVIS interactive benchmark.

### Software & Versiones
- **Sam 2:** 2.1
- **Pytorch:** 2.3.1
- **Cuda:** 12.1

### Análisis de Limitaciones
- Ambiguous prompts (single click) may result in multiple masks
- Model may lose object (occlusion)
- Failure across shot changes
- Tracking/confusion in crowded scenes
- Failure after long occlusions
- Failure in extended videos
- Struggles with thin/fine details
- Struggles with fast-moving objects
- Struggles with nearby objects of similar appearance
- No inter-object communication
- SAM 2 often tends to segment object parts on the first click while DAVIS contains whole objects
- Estimation of annotation time does not account for model's tracking FPS
- Manual masklets: Human errors (missed frames)
- Auto masklets: Model errors (inconsistencies)
- No parity across all geographic and demographic groups

### Licencias detectadas
- **Sa-V Dataset:** CC by 4.0
- **Sam 2 Code:** Apache 2.0

### Impacto Social (Broader Impacts)
- **Fairness:** Minimal performance discrepancy in video segmentation based on perceived gender/age; researchers encouraged to perform own evaluation.
- **Environmental Impact:** Equivalent to ~10k miles driven by an average gasoline-powered passenger vehicle.
- **Safety Measures:** ['Instructions to crowdworkers to avoid objectionable content', 'Expert annotators instructed to flag/reject objectionable content', 'Reporting mechanism: segment-anything@meta.com']
- **Privacy:** Face blurring model applied to videos
- **Bias Mitigation:** Encouraged diversity in crowdworker pool

### Sujetos Humanos & Crowdsourcing
- **Annotation Process:** Crowdworkers used for video capture and annotation; compensated with hourly wage; consented via third-party vendor.
- **Verification:** Separate set of annotators for quality verification; trained for 1-2 weeks.
- **Demographics:** Collected for SA-V dataset; diversity emphasized for video collection.

---

## 🧠 Razonamiento de Consolidación (CoT)

> Consolidated technical specifications, architectural components (Hiera, memory bank, mask decoder), training hyperparameters, and performance metrics from all fragments. Ensured dataset statistics and ethical/safety protocols were merged without loss. The model demonstrates high technical rigor through extensive benchmarking and ablation studies.

### 📍 Secciones Identificadas del Paper
- `Introduction`
- `Related work`
- `Task: promptable visual segmentation`
- `Model`
- `Data`
- `Zero-shot experiments`
- `Comparison to state-of-the-art in semi-supervised VOS`
- `8 Conclusion`
- `Acknowledgements`
- `Appendix`
- `A Data and model ablations`
- `A.1 Data ablations`
- `A.2 Model architecture ablations`
- `A.2.1 Capacity ablations`
- `A.2.2 Relative positional encoding`
- `A.2.3 Memory architecture ablations`
- `B Details on the PVS Task`
- `C Limitations`
- `D SAM2 details`
- `D.1 Architecture`
- `D.2 Training`
- `D.3 Speed benchmarking`
- `E Data details`
- `E.1 SA-V dataset details`
- `E.1.1 Fairness evaluation`
- `E.2 Data engine details`
- `E.2.1 Annotation protocol`
- `E.2.2 Data engine phase comparison`
- `F Details on zero-shot transfer experiments`
- `F.1 Zero-shot video tasks`
- `F.1.2 Interactive offline and online evaluation details`
- `F.1.3 Semi-supervised VOS evaluation details`
- `F.1.4 SAM+XMem++ and SAM+Cutie baseline details`
- `F.2 DAVIS interactive benchmark`
- `F.3 Zero-shot image tasks`
- `G Details on comparison to state-of-the-art in semi-supervised VOS`
- `H Model, data and annotation cards`
- `Composition`
- `Collection Process`
- `Preprocessing / Cleaning / Labeling`
- `Uses`
- `Distribution`
- `Maintenance`
- `H.3 Data annotation card`
- `References`

---
_Informe generado automáticamente._
