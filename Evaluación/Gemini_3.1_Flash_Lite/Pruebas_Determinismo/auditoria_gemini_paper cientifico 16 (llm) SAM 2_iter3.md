# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 16 (llm) SAM 2.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-24 21:29:25 |
| ⏳ **Tiempo de Ejecución** | 97.53s |
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
| 2 | Limitations | 🟢 Yes | Section C, titled 'Limitations', states: 'The model may fail to segment objects across shot changes and can lose track of or confuse objects in crowded scenes, after long occlusions or in extended videos... SAM 2 also struggles with accurately tracking objects with very thin or fine details especially when they are fast-moving. Another challenging scenario occurs when there are nearby objects with similar appearance.' |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper focuses on the empirical development of a foundational model for promptable visual segmentation (SAM 2). |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The authors provide comprehensive resources for reproducibility: 'We release the SAM 2 model checkpoints, the SA-V dataset, and the training and inference code at https://github.com/facebookresearch/sam2.' Additionally, the paper provides detailed architectural specifications in §4 and §D.1, training protocols in §D.2, and extensive evaluation details in §F.1.2 and §F.1.3. |
| 5 | Open Access to Data and Code | 🟢 Yes | The authors provide comprehensive access to their contributions: the code is hosted at https://github.com/facebookresearch/sam2, the SA-V dataset is available at https://ai.meta.com/datasets/segment-anything-video-downloads/, and a public demo is accessible at https://sam2.metademolab.com. These resources directly support the main experimental results presented in the paper. |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides extensive training and evaluation details across multiple sections. Specifically, Section D.2 (Training) outlines the optimization strategy (AdamW), batch sizes (128 for pre-training, 1 for video tasks), and iteration counts (200k for pre-training, 50k for fine-tuning). Furthermore, Section F.1.1 and F.3.1 provide detailed breakdowns of the 17 zero-shot video datasets and 37 interactive segmentation datasets, including specific evaluation protocols, frame sampling, and IoU thresholds used for performance metrics. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper provides extensive quantitative results in Tables 5, 6, 16, and 17, comparing SAM 2 against various baselines across multiple benchmarks. However, these tables report only point estimates (e.g., J & F, mIoU) without accompanying error bars, confidence intervals, or statistical significance tests. The NeurIPS 2026 criteria explicitly require that results be accompanied by error bars, confidence intervals, or statistical significance tests for the main claims. As the authors have not provided these measures nor an explicit justification for their omission (such as prohibitive computational cost), the transparency requirement for statistical significance is not met. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | Section D.3 states: 'We conduct all benchmarking experiments on a single A100 GPU using PyTorch 2.3.1 and CUDA 12.1... The FPS measurements for the SA task were conducted using a batch size of 10 images... For video tasks, we use a batch size of 1.' Additionally, the paper provides training infrastructure details: '256 A100 GPUs' for '108 hours', and reports environmental impact: '12165.12 kWH' and '3.89 metric tons of CO2e'. |
| 9 | Code of Ethics | 🟢 Yes | The paper includes extensive documentation regarding the data collection process, human subject involvement, and ethical safeguards. Specifically, the authors state: 'Videos were subjected to a face blurring model' to address privacy, and 'Instructions to crowdworkers to avoid objectionable content' were provided. Furthermore, the authors detail an internal review process and provide a reporting mechanism (segment-anything@meta.com) for potential issues. The paper also includes a dedicated section on fairness evaluation (E.1.1) and provides demographic analysis of the dataset, demonstrating adherence to the NeurIPS Code of Ethics regarding privacy, consent, and representative evaluation practices. |
| 10 | Broader Impacts | 🟢 Yes | The authors explicitly address potential societal impacts and mitigation strategies. In the context of the SA-V dataset and the SAM 2 model, they discuss privacy (face blurring), safety (instructions to avoid objectionable content), and bias (fairness evaluation across demographic groups). The paper acknowledges that 'Selecting objects to mask and track is inherently subjective' and provides a transparent discussion of model limitations in Section C, which aligns with the NeurIPS requirement to communicate known or anticipated consequences of research and potential harmful consequences. |
| 11 | Safeguards | 🔵 N/A | The paper presents SAM 2, a foundational model for promptable visual segmentation. The authors have implemented proactive safety measures, including the use of a face-blurring model on the SA-V dataset to protect privacy and the establishment of a reporting mechanism (segment-anything@meta.com) for any concerns regarding the dataset or model. Furthermore, the annotation process involved strict instructions to crowdworkers to avoid objectionable content, with expert oversight to flag and reject such material. |
| 12 | Licenses | 🟢 Yes | The authors explicitly state the licensing terms for their contributions: the SA-V dataset is released under the CC BY 4.0 license, the SAM 2 model checkpoints are provided under a permissive open license, and both the training and demo code are released under the Apache 2.0 license. |
| 13 | Assets | 🟢 Yes | In Appendix H, the authors provide comprehensive documentation for the SA-V dataset and the SAM 2 model. Specifically, Section H.1 contains a 'Model card', Section H.2 provides a 'Dataset card for SA-V dataset', and Section H.3 provides a 'Data annotation card'. These sections detail the composition, collection process, preprocessing, uses, distribution, and maintenance of the assets. Furthermore, the paper explicitly states that the SA-V dataset is released under a CC by 4.0 license, and the SAM 2 model checkpoints are released under a permissive open license. |
| 14 | Crowdsourcing & Human Subjects | 🟢 Yes | Section E.2.1, 'Annotation protocol', and Figure 11 describe the multi-step annotation process involving human annotators. The paper notes that annotators were trained for 1-2 weeks and were compensated with an hourly wage. Furthermore, the 'broader_impacts_extraction' and 'human_subjects_extraction' sections confirm that the project involved crowdworkers for video capture and annotation, who were subject to consent forms and provided with a revocation mechanism. The authors also detail the demographic distribution of the crowdworkers in Figure 10(c). |
| 15 | IRB Approvals | 🟢 Yes | The paper states in the 'Code of Ethics' section: 'Project underwent an internal review process' and 'Contracted third-party collected consents and provided revocation mechanism.' Furthermore, the 'Human subjects extraction' data confirms that crowdworkers were used for video capture and annotation, were compensated with an hourly wage, and agreed to consent forms. |
| 16 | Declaration of LLM Usage | 🔵 N/A | The methodology described in Section 4 (Model) and Section 5 (Data engine) focuses on a streaming memory architecture, hierarchical image encoders (Hiera), and a data engine utilizing human-in-the-loop annotation. There is no mention of Large Language Models (LLMs) being used as a component of the core methodology, synthetic data generation, or distillation processes. |

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
- **Image Encoder Variants:** ['Hiera-T', 'Hiera-S', 'Hiera-B+', 'Hiera-L', 'ViT-H', 'ViT-B']
- **Decoder:** Two-way transformer blocks
- **Memory Attention:** Stack of L transformer blocks with self-attention and cross-attention to memory bank
- **Memory Encoder:** Convolutional module + light-weight convolutional layers
- **Prompt Encoder:** Identical to SAM (sparse prompts: positional encodings + learned embeddings; masks: convolutions)
- **Components:** ['Streaming memory', 'Memory bank (FIFO queue)', 'Object pointers (lightweight vectors)', 'Skip connections from hierarchical image encoder', 'Feature Pyramid Network', 'Mask decoder', 'Occlusion prediction head']
- **Dims:** {'memory_bank_projection': 64, 'object_pointer': 256}
- **Positional Encoding:** ['2d-RoPE', 'Sinusoidal absolute positional embeddings', 'Windowed absolute positional embeddings']

### Dataset & Datos
- **Dataset Name:** SA-V
- **Total Videos:** 50.9K
- **Total Masklets:** 642.6K
- **Total Masks:** 35.5M
- **Total Frames:** 4.2M
- **Total Hours:** 196
- **Composition:** 54% indoor, 46% outdoor
- **Average Video Duration:** 14 seconds
- **Disappearance Rate:** 42.5% (Manual), 27.7% (Manual+Auto)
- **Annotation Frequency:** 6 FPS
- **Video Format:** mp4
- **Video Frame Rate:** 24 fps
- **Other Datasets:** ['SA-1B', 'DAVIS', 'MOSE', 'YouTubeVOS', 'Internal-train', 'Internal-test', 'EndoVis 2018', 'ESD', 'LVOSv2', 'LV-VIS', 'UVO', 'VOST', 'PUMaVOS', 'Virtual KITTI 2', 'VIPSeg', 'Wildfires', 'VISOR', 'FBMS', 'Ego-Exo4D', 'Cityscapes', 'Lindenthal Camera', 'HT1080WT Cells', 'Drosophila Heart', 'LVIS', 'ADE20K', 'Hypersim', 'BBBC038v1', 'DOORS', 'DRAM', 'EgoHOS', 'GTEA', 'iShape', 'NDD20', 'NDISPark', 'OVIS', 'PPDLS', 'Plittersdorf', 'STREETS', 'TimberSeg', 'TrashCan', 'WoodScape', 'PIDRay', 'ZeroWaste-f', 'IBD', 'LCT', 'CFD', 'DH OCM', 'YTVOS 2019']

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
- HQ-SAM
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
- MiVOS
- CiVOS
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
- **Crowdworkers:** Compensated with hourly wage; agreed to consent forms; demographic distribution collected
- **Annotators:** Compensated with hourly wage; trained for 1-2 weeks; internal review process

---

## 🧠 Razonamiento de Consolidación (CoT)

> The paper presents SAM 2, a foundational model for promptable visual segmentation in images and videos. The technical rigor is high, evidenced by a massive data engine (SA-V dataset with 50.9K videos), a novel streaming memory architecture, and extensive benchmarking against 30+ baselines. Reproducibility is supported by the release of code, checkpoints, and detailed dataset documentation. The inclusion of fairness evaluations and safety protocols (face blurring, reporting mechanisms) demonstrates a commitment to responsible AI development.

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
