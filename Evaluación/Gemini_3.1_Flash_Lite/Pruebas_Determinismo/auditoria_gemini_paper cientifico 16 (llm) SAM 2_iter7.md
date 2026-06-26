# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 16 (llm) SAM 2.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-24 21:34:14 |
| ⏳ **Tiempo de Ejecución** | 97.88s |
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
| 1 | Claims | 🟢 Yes | The introduction states: 'SAM 2 delivers a step-change in the video segmentation experience. SAM 2 can produce better segmentation accuracy while using 3 × fewer interactions than prior approaches. Further, SAM 2 outperforms prior work in established video object segmentation benchmarks... and delivers better performance compared to SAM on image segmentation benchmarks, while being 6 × faster.' This is supported by §6 and §A, which detail extensive benchmarking against 17 video and 37 image datasets, confirming the model's generalization capabilities and efficiency gains. |
| 2 | Limitations | 🟢 Yes | The paper includes a dedicated section, 'C Limitations', which states: 'The model may fail to segment objects across shot changes and can lose track of or confuse objects in crowded scenes, after long occlusions or in extended videos... SAM 2 also struggles with accurately tracking objects with very thin or fine details especially when they are fast-moving.' |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper presents an empirical contribution focused on a novel model architecture (SAM 2) and a large-scale dataset (SA-V). The research is grounded in deep learning engineering, architectural design, and empirical evaluation rather than the development of new mathematical theorems or formal proofs. As the NeurIPS 2026 criteria for this item specifically apply to papers 'including theoretical results' and requiring 'complete proofs of all theoretical results', this item is not applicable to this work. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The authors provide comprehensive resources for reproducibility, including the model implementation and dataset. As stated in the provided context and JSON summary, the repository is available at 'https://github.com/facebookresearch/sam2', the dataset is accessible at 'https://ai.meta.com/datasets/segment-anything-video-downloads/', and a live demo is hosted at 'https://sam2.metademolab.com'. Furthermore, the paper provides extensive details on training hyperparameters (e.g., AdamW optimizer, 256 A100 GPUs, 108 hours of training), architecture specifications (e.g., Hiera image encoder, memory bank structure), and evaluation protocols (e.g., interactive offline/online evaluation metrics). |
| 5 | Open Access to Data and Code | 🟢 Yes | The authors provide explicit access to their contributions: the code repository is hosted at https://github.com/facebookresearch/sam2, the SA-V dataset is available at https://ai.meta.com/datasets/segment-anything-video-downloads/, and a public demo is accessible at https://sam2.metademolab.com. These resources cover the core contributions of the paper, including the model implementation, the newly collected SA-V dataset, and the inference pipeline. |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides extensive experimental details across multiple sections. Section D.2 (Training) and the provided JSON summary detail the training infrastructure (256 A100 GPUs), optimizer (AdamW), batch sizes (128 for pre-training, 1 for video tasks), and iteration counts (200k for pre-training, 50k for fine-tuning). Furthermore, sections F.1.1 and F.3.1 provide comprehensive lists of the 17 zero-shot video datasets and 37 interactive segmentation datasets used for evaluation, including specific references to the source benchmarks (e.g., EndoVis 2018, Cityscapes, etc.) and the evaluation protocols (e.g., dense vs. sparse annotation handling). |
| 7 | Experiment Statistical Significance | 🔴 No | The paper provides extensive quantitative results in Tables 5, 6, 16, and 17, reporting performance metrics such as J & F, J, and mIoU across various benchmarks. However, these results are presented as single point estimates (averages). The authors do not provide error bars, confidence intervals, or statistical significance tests (e.g., p-values or standard deviations) to account for factors of variability in the experiments. According to the NeurIPS 2026 criteria, results must be accompanied by error bars or statistical significance tests to support the main claims. As the authors have not provided these measures nor explicitly stated a scientific justification for their omission, the transparency requirement is not met. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | Section D.3 states: 'We conduct all benchmarking experiments on a single A100 GPU using PyTorch 2.3.1 and CUDA 12.1... The FPS measurements for the SA task were conducted using a batch size of 10 images... For video tasks, we use a batch size of 1.' Additionally, the JSON summary and paper context confirm the training infrastructure: '256 A100 GPUs', '108 hours' of training duration, and environmental impact metrics including '12165.12 kWH' and '3.89 metric tons of CO2e'. |
| 9 | Code of Ethics | 🟢 Yes | The authors explicitly address ethical considerations throughout the paper and its appendices. Specifically, the paper details the use of human annotators, noting that they were 'compensated with hourly wage; agreed to consent forms; trained for 1-2 weeks' (Section E.2.1). Furthermore, the authors implemented privacy-preserving measures, stating that 'videos were subjected to a face blurring model' to minimize the exposure of personally identifiable information. The paper also includes a dedicated discussion on fairness evaluation (Section E.1.1) and provides a reporting mechanism (segment-anything@meta.com) for safety concerns, demonstrating adherence to the NeurIPS Code of Ethics regarding human subjects, data privacy, and responsible research practices. |
| 10 | Broader Impacts | 🟢 Yes | The authors provide a comprehensive discussion of potential societal impacts and limitations in Section C and the supplementary material. They acknowledge that 'SAM 2 often tends to segment object parts on the first click' and discuss the subjectivity inherent in selecting objects to track. Regarding potential misuse, the authors have implemented safety measures, including instructions to crowdworkers to reject objectionable content and the use of automated face-blurring to mitigate privacy risks. They also explicitly address bias by providing an analysis of geographic and demographic representation in their dataset (Section 5.2), fulfilling the requirement to communicate known or anticipated consequences and mitigation strategies as outlined in the NeurIPS criteria. |
| 11 | Safeguards | 🔵 N/A | The paper presents SAM 2, a foundational model for visual segmentation. The authors have implemented privacy-preserving measures, such as face blurring, and have established reporting mechanisms for objectionable content (segment-anything@meta.com). |
| 12 | Licenses | 🟢 Yes | The authors explicitly state the licensing for their assets: the SA-V dataset is released under CC BY 4.0, the SAM 2 model checkpoints are under a permissive open license, and the training/demo code is under the Apache 2.0 license. |
| 13 | Assets | 🟢 Yes | In Appendix H, the authors provide comprehensive documentation for the SA-V dataset and the SAM 2 model. Specifically, Section H.1 contains a 'Model card', Section H.2 contains a 'Dataset card for SA-V dataset', and Section H.3 contains a 'Data annotation card'. These cards detail the composition, collection process, preprocessing, uses, distribution, and maintenance of the assets. Furthermore, the paper provides a public download link for the SA-V dataset (https://ai.meta.com/datasets/segment-anything-video-downloads/) and a repository for the model and code (https://github.com/facebookresearch/sam2). |
| 14 | Crowdsourcing & Human Subjects | 🟢 Yes | Section E.2.1 ('Annotation protocol') and the 'human_subjects_extraction' summary detail the use of crowdworkers for data collection and annotation. The authors describe a multi-step annotation protocol involving masklet selection, tracking, and verification. Regarding compensation and ethics, the 'code_of_ethics' section confirms that workers were compensated with an hourly wage, agreed to consent forms, and were trained for 1-2 weeks. Additionally, the authors implemented safety measures such as instructing workers to avoid objectionable content and providing a reporting mechanism (segment-anything@meta.com). |
| 15 | IRB Approvals | 🟢 Yes | The paper states in the 'Code of Ethics' section: 'Project underwent an internal review process. Contracted third-party collected consents and provided revocation mechanism.' Furthermore, the 'Human subjects extraction' section confirms that crowdworkers were used for video capture and annotation, were compensated with an hourly wage, agreed to consent forms, and were trained for 1-2 weeks. |
| 16 | Declaration of LLM Usage | 🔵 N/A | The methodology described in Section 4 (Model) and Section 5 (Data) focuses on a streaming architecture for video segmentation, utilizing a memory bank, memory attention modules, and a hierarchical image encoder (Hiera). The data engine is described as a model-in-the-loop system using SAM 2 itself to assist annotators. |

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
- **Prompt Probabilities:** {'ground_truth': 0.5, 'positive_click': 0.25, 'bounding_box': 0.25}
- **Memory Bank:** {'N_frames': 'N (recent frames)', 'M_frames': 'M (prompted frames)', 'memory_frames': 6, 'memory_channel_dim': 64}
- **Image Encoder Resolution:** 1024
- **Spatial Resolution:** {'ablation_default': 512, 'final_model': 1024}
- **Interactive Eval:** {'N_frame_max': 8, 'N_click_per_frame': 3, 'IoU_threshold_online': 0.75, 'IoU_threshold_reconstruction': 0.8, 'T_loc': '1 sec', 'T_click': '1.5 sec', 'T_exam': '30 sec per 300-frame video', 'examine_fps': 10, 'correction_clicks': 7}

### Hardware & Compute
- **Inference Gpu:** Single A100 GPU
- **Training Infrastructure:** 256 A100 GPUs
- **Training Duration:** 108 hours
- **Energy Consumption:** 12165.12 kWH
- **Carbon Emissions:** 3.89 metric tons of CO2e
- **Latency Metrics:** {'SAM2_Hiera-B+_FPS': 43.8, 'SAM2_Hiera-L_FPS': 30.2, 'SAM2_Image_FPS': 130.1}

### Arquitectura del Modelo
- **Image Encoder:** Hiera (MAE pre-trained)
- **Decoder:** Two-way transformer blocks
- **Memory Attention:** Stack of L transformer blocks with self-attention and cross-attention to memory bank
- **Memory Encoder:** Convolutional module + light-weight convolutional layers
- **Prompt Encoder:** Identical to SAM (sparse prompts: positional encodings + learned embeddings; masks: convolutions)
- **Components:** ['Streaming memory', 'Memory bank (FIFO queue)', 'Object pointers (lightweight vectors)', 'Skip connections from hierarchical image encoder', 'Feature Pyramid Network', 'Mask decoder', 'Occlusion prediction head']
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
- **Average Video Duration:** 14 seconds
- **Annotation Frequency:** 6 FPS
- **Video Format:** mp4
- **Video Frame Rate:** 24 fps
- **Disappearance Rate:** 42.5% (Manual), 27.7% (Manual+Auto)
- **Data Engine Phases:** ['Phase 1: SAMperframe (16K masklets)', 'Phase 2: SAM+SAM2Mask (63.5K masklets)', 'Phase 3: SAM 2 (197.0K masklets)']
- **Other Datasets:** ['SA-1B', 'DAVIS', 'MOSE', 'YouTubeVOS', 'EndoVis 2018', 'ESD', 'LVOSv2', 'LV-VIS', 'UVO', 'VOST', 'PUMaVOS', 'Virtual KITTI 2', 'VIPSeg', 'Wildfires', 'VISOR', 'FBMS', 'Ego-Exo4D', 'Cityscapes', 'Lindenthal Camera', 'HT1080WT Cells', 'Drosophila Heart', 'LVIS', 'ADE20K', 'Hypersim', 'BBBC038v1', 'DOORS', 'DRAM', 'EgoHOS', 'GTEA', 'iShape', 'NDD20', 'NDISPark', 'OVIS', 'PPDLS', 'Plittersdorf', 'STREETS', 'TimberSeg', 'TrashCan', 'WoodScape', 'PIDRay', 'ZeroWaste-f', 'IBD', 'LCT', 'CFD', 'DH OCM', 'YTVOS 2019']

### Código & Repositorio
- **Repository Url:** https://github.com/facebookresearch/sam2
- **Demo Url:** https://sam2.metademolab.com
- **Dataset Download:** https://ai.meta.com/datasets/segment-anything-video-downloads/

### Estadística & Rigor Científico
- **Annotation Speedup:** 8.4x faster than Phase 1
- **Sam2 Vs Sam Speed:** 6x faster
- **Interaction Reduction:** 3x fewer interactions than prior approaches
- **Avg Manual Masklets Per Video:** 3.8
- **Avg Auto Masklets Per Video:** 8.9

### Comparativa con Baselines
- SAM
- XMem++
- Cutie
- STCN
- SwinB-AOT
- SwinB-DeAOT
- RDE
- XMem
- SimVOS-B
- JointFormer
- ISVOS
- DEVA
- HQ-SAM
- MiVOS
- CiVOS
- SwinB-AOT-L
- SwinB-DeAOT-L
- Cutie-base
- Cutie-base+
- DDMemory

### Software & Versiones
- **Sam 2 Version:** 2.1
- **Pytorch:** 2.3.1
- **Cuda:** 12.1

### Análisis de Limitaciones
- Ambiguous prompts (multiple compatible target masks)
- Occlusion and re-appearance
- Small objects and parts
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
- Manual masklets: Human errors may exist
- Auto masklets: Model errors such as inconsistencies in masklets may exist
- Demographics: No parity across all geographic and demographic groups
- Subjectivity: Selecting objects to mask and track is inherently subjective

### Licencias detectadas
- **Sa-V Dataset:** CC by 4.0
- **Sam 2 Model Checkpoints:** Permissive open license
- **Training Code:** Apache 2.0
- **Demo Code:** Apache 2.0

### Impacto Social (Broader Impacts)
- **Fairness Evaluation:** Minimal performance discrepancy in video segmentation based on perceived gender, and little variance among three perceived age groups.
- **Safety Measures:** ['Instructions to crowdworkers to avoid objectionable content', 'Expert annotators instructed to flag/reject objectionable content', 'Reporting mechanism: segment-anything@meta.com']
- **Privacy:** Videos were subjected to a face blurring model
- **Bias Mitigation:** Encouraged diversity in crowdworker pool; analysis of geography and demographics provided in section 5.2

### Sujetos Humanos & Crowdsourcing
- **Annotation Process:** Crowdworkers used for video capture and annotation
- **Verification:** Separate set of annotators for quality verification
- **Crowdworkers:** Compensated with hourly wage; agreed to consent forms; trained for 1-2 weeks
- **Demographics:** Not used to select annotators; crowdworker demographics presented in 5.2

---

## 🧠 Razonamiento de Consolidación (CoT)

> Consolidated technical specifications, architectural components, and performance metrics from multiple fragments. Integrated dataset documentation, training hyperparameters, and ethical/safety protocols. Ensured all unique benchmarks and baseline models were captured. The paper demonstrates high technical rigor through extensive ablation studies, diverse dataset benchmarking, and detailed documentation of the data engine phases.

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
