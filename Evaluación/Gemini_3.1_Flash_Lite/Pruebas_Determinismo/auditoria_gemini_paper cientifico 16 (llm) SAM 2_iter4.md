# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 16 (llm) SAM 2.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-24 21:30:41 |
| ⏳ **Tiempo de Ejecución** | 75.76s |
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
| 1 | Claims | 🟢 Yes | The introduction states: 'SAM 2 delivers a step-change in the video segmentation experience. SAM 2 can produce better segmentation accuracy while using 3 × fewer interactions than prior approaches. Further, SAM 2 outperforms prior work in established video object segmentation benchmarks... while being 6 × faster.' This is supported by the experimental results in Section 6 and the summary statistics provided in the paper, which detail performance across 17 video segmentation benchmarks and 37 single-image benchmarks, confirming the model's generalization capabilities and efficiency gains. |
| 2 | Limitations | 🟢 Yes | The paper includes a dedicated section titled 'C Limitations' which states: 'SAM 2 demonstrates strong performance in both static image and video domains, yet it encounters difficulties in certain scenarios. The model may fail to segment objects across shot changes and can lose track of or confuse objects in crowded scenes, after long occlusions or in extended videos.' It further notes: 'SAM 2 also struggles with accurately tracking objects with very thin or fine details especially when they are fast-moving.' |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper focuses on the architecture and empirical evaluation of a deep learning model (SAM 2) for video segmentation. It does not propose or rely on novel theoretical theorems or mathematical proofs that require formal assumptions. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The authors provide comprehensive resources for reproducibility, including the model code and dataset. As stated in the provided context: 'repository_url': 'https://github.com/facebookresearch/sam2', 'website': 'https://sam2.metademolab.com', and 'dataset_download': 'https://ai.meta.com/datasets/segment-anything-video-downloads/'. Furthermore, the paper details the architecture in §4 and §D.1, and provides extensive evaluation protocols in §F.1.2 and §F.1.3. |
| 5 | Open Access to Data and Code | 🟢 Yes | The authors provide explicit access to their contributions: the code repository is hosted at https://github.com/facebookresearch/sam2, the project website is available at https://sam2.metademolab.com, and the SA-V dataset is accessible via https://ai.meta.com/datasets/segment-anything-video-downloads/. This fulfills the NeurIPS 2026 criteria for Open Access to Data and Code, which requires that authors include the code, data, and instructions needed to reproduce the main experimental results. |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides extensive experimental details across multiple sections. Section D.2, F.1.1, F.3.1, and the provided JSON summary detail the training infrastructure (256 A100 GPUs), dataset splits (17 zero-shot video datasets and 37 interactive segmentation datasets), and specific hyperparameters such as sequence length (8), N_click_per_frame (3), and various prompt probabilities (e.g., 0.5 for ground truth). Furthermore, the authors specify how hyperparameters were selected and provide comprehensive dataset cards (H.2, H.3) and a model card (H.1), satisfying the requirement that all training details and hyperparameter selection information be provided in the paper or supplementary materials. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper provides extensive quantitative results in Tables 5, 6, 16, and 17, reporting performance metrics such as J & F, J, and F scores across various benchmarks. However, these results are presented as single point estimates (averages). The authors do not provide error bars, confidence intervals, or statistical significance tests (e.g., p-values) for any of the reported experiments. Furthermore, the authors do not provide an explicit justification for the omission of these statistical measures, such as citing prohibitive computational costs for multiple runs. According to the NeurIPS 2026 criteria, results must be accompanied by error bars, confidence intervals, or statistical significance tests to support the main claims, and the absence of these, without a stated justification, fails the transparency requirement. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🟢 Yes | Section D.3 states: 'We conduct all benchmarking experiments on a single A100 GPU using PyTorch 2.3.1 and CUDA 12.1... For video tasks, we use a batch size of 1 following the common protocol in video segmentation.' Additionally, the JSON summary and paper context confirm: 'training_infrastructure: 256 A100 GPUs', 'training_duration: 108 hours', 'energy_consumption: 12165.12 kWH', and 'carbon_emissions: 3.89 metric tons of CO2e'. |
| 9 | Code of Ethics | 🟢 Yes | The authors explicitly address the ethical dimensions of their research through a comprehensive data annotation card and internal review process. As noted in the JSON summary and supported by the acknowledgments and data documentation, the project underwent an internal review process, and the authors implemented rigorous protocols for human subjects, including the use of contracted third-party services to collect consent and provide revocation mechanisms. Furthermore, the authors explicitly address bias and fairness by providing demographic analysis in section 5.2 and implementing safety measures such as instructions to crowdworkers to reject objectionable content, which aligns with the NeurIPS Code of Ethics requirement to ensure fair wages, privacy, and consent in research involving human participants. |
| 10 | Broader Impacts | 🟢 Yes | The authors provide a transparent discussion of potential negative societal impacts and mitigation strategies. Specifically, they acknowledge risks related to performance on people across demographic groups and provide a fairness evaluation showing minimal performance discrepancy. They also address privacy concerns by noting that videos were processed through a face-blurring model. The authors explicitly recommend that researchers perform their own fairness evaluations, which satisfies the NeurIPS requirement to communicate known or anticipated consequences and potential harms, such as fairness considerations and privacy, as outlined in the Broader Impacts criteria. |
| 11 | Safeguards | 🔵 N/A | The paper presents SAM 2, a foundational model for promptable visual segmentation in images and videos. The model is designed for general-purpose segmentation tasks and does not inherently generate harmful content, synthesize dangerous information, or facilitate surveillance beyond the capabilities of standard computer vision tools. The authors have implemented safety measures for the data collection process, including face blurring for privacy and instructions to annotators to reject objectionable content, which mitigates risks associated with the dataset release. |
| 12 | Licenses | 🟢 Yes | The authors explicitly state the licensing terms for their contributions: 'The SA-V dataset is released under the Creative Commons Attribution 4.0 International Public License. The SAM 2 model checkpoints are released under a permissive open license, and the training and demo code are released under the Apache 2.0 license.' |
| 13 | Assets | 🟢 Yes | The authors provide comprehensive documentation for the SA-V dataset and the SAM 2 model in Appendix H, specifically sections H.1 (Model card), H.2 (Dataset card for SA-V dataset), and H.3 (Data annotation card). These sections detail the training, license, limitations, and composition of the assets. For instance, the paper states: 'In Appendix H, we provide model, data and annotation cards for SA-V.' Furthermore, the JSON summary confirms the availability of the dataset and model via public URLs (https://ai.meta.com/datasets/segment-anything-video-downloads/ and https://github.com/facebookresearch/sam2). |
| 14 | Crowdsourcing & Human Subjects | 🟢 Yes | The paper explicitly details the annotation protocol in section E.2.1, describing the multi-step process involving different annotators for masklet selection, tracking, and quality verification. The authors state: 'The annotation task was separated into steps each carried out by a different annotator: Steps 1 and 2 focus on object selection, Steps 3 and 4 on masklet tracking, and Step 5 on quality verification.' Additionally, the 'human_subjects_extraction' data confirms that crowdworkers were compensated with an hourly wage, underwent training, and were subject to an internal review process, adhering to the NeurIPS Code of Ethics regarding fair labor practices. |
| 15 | IRB Approvals | 🟢 Yes | The paper explicitly addresses the ethical and procedural oversight of the data collection process in the 'Code of Ethics' section and the 'Broader Impacts' section. Specifically, the authors state: 'The project underwent an internal review process' and 'Contracted third-party collected consents and provided revocation mechanism.' Furthermore, the paper details the use of crowdworkers for video capture and annotation, noting that they were 'compensated with hourly wage; agreed to consent forms; demographic distribution collected.' |
| 16 | Declaration of LLM Usage | 🔵 N/A | The NeurIPS 2026 criteria for LLM declaration state that a declaration is required if the LLM is an important, original, or non-standard component of the core methods. The provided text describes the SAM 2 architecture as a vision-based model utilizing a hierarchical image encoder (Hiera), a memory attention module, and a mask decoder. There is no evidence in the provided text that an LLM (such as GPT-4, Llama, etc.) was used as a core component of the methodology, synthetic data generation, or distillation process. As the model is a specialized computer vision system for segmentation, the usage of LLMs as defined by the criteria is not applicable. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Sequence Length:** 8
- **N Frame Max:** 8
- **N Click Per Frame:** 3
- **Prompt Probability Ground Truth:** 0.5
- **Prompt Probability Positive Click:** 0.25
- **Prompt Probability Bounding Box:** 0.25
- **Memory Bank N Frames:** N (recent frames)
- **Memory Bank M Frames:** M (prompted frames)
- **Image Encoder Resolution:** 1024
- **Iou Threshold Online:** 0.75
- **Iou Threshold Reconstruction:** 0.8
- **T Loc:** 1 sec
- **T Click:** 1.5 sec
- **T Exam:** 30 sec per 300-frame video
- **Examine Fps:** 10

### Hardware & Compute
- **Training Infrastructure:** 256 A100 GPUs
- **Training Duration:** 108 hours
- **Inference Gpu:** Single A100 GPU
- **Energy Consumption:** 12165.12 kWH
- **Carbon Emissions:** 3.89 metric tons of CO2e

### Arquitectura del Modelo
- **Image Encoder:** Hiera (MAE pre-trained)
- **Image Encoder Variants:** ['Hiera-B+', 'Hiera-L', 'Hiera-T', 'Hiera-S', 'ViT-H', 'ViT-B']
- **Decoder:** Two-way transformer blocks
- **Memory Attention:** Stack of L transformer blocks with self-attention and cross-attention to memory bank
- **Memory Encoder:** Convolutional module + light-weight convolutional layers
- **Prompt Encoder:** Identical to SAM (sparse prompts: positional encodings + learned embeddings; masks: convolutions)
- **Components:** ['Streaming memory', 'Memory bank (FIFO queue)', 'Object pointers (lightweight vectors)', 'Skip connections from hierarchical image encoder']

### Dataset & Datos
- **Dataset Name:** SA-V
- **Total Videos:** 50.9K
- **Total Masks:** 35.5M
- **Total Masklets:** 642.6K
- **Composition:** 54% indoor, 46% outdoor
- **Average Video Duration:** 14 seconds
- **Disappearance Rate:** 42.5% (Manual), 27.7% (Manual+Auto)
- **Annotation Frequency:** 6 FPS
- **Video Format:** mp4
- **Video Frame Rate:** 24 fps
- **Average Manual Masklets Per Video:** 3.8
- **Average Auto Masklets Per Video:** 8.9
- **Data Engine Phases:** ['Phase 1: SAMperframe (16K masklets)', 'Phase 2: SAM+SAM2Mask (63.5K masklets)', 'Phase 3: SAM 2 (197.0K masklets)']
- **Internal Dataset:** {'videos': '62.9K', 'masklets': '69.6K'}
- **Other Datasets Used:** ['EndoVis', 'ESD', 'LVOSv2', 'LV-VIS', 'UVO', 'VOST', 'PUMaVOS', 'Virtual KITTI 2', 'VIPSeg', 'LVIS', 'ADE20K', 'Hypersim', 'Cityscapes', 'BBBC038v1', 'DOORS', 'DRAM', 'EgoHOS', 'GTEA', 'iShape', 'NDD20', 'NDISPark', 'OVIS', 'PPDLS', 'Plittersdorf', 'STREETS', 'TimberSeg', 'TrashCan', 'VISOR', 'WoodScape', 'PIDRay', 'ZeroWaste-f', 'IBD', 'LCT', 'FBMS', 'CFD', 'DH OCM', 'Ego-Exo4d', 'HT1080WT', 'SA-1B', 'DAVIS', 'MOSE', 'YTVOS 2019']

### Código & Repositorio
- **Repository Url:** https://github.com/facebookresearch/sam2
- **Website:** https://sam2.metademolab.com
- **Dataset Download:** https://ai.meta.com/datasets/segment-anything-video-downloads/

### Estadística & Rigor Científico
- **Annotation Speedup:** 8.4x faster than Phase 1
- **Sam2 Vs Sam Speed:** 6x faster
- **Sam2 Vs Sam Accuracy:** More accurate
- **Interaction Reduction:** 3x fewer interactions than prior approaches
- **Latency Metrics:** {'SAM2_Hiera-B+_FPS': 43.8, 'SAM2_Hiera-L_FPS': 30.2, 'SAM2_Image_FPS': 130.1}

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
- SAM+XMem++
- SAM+Cutie
- MiVOS
- CiVOS
- SwinB-AOT-L
- SwinB-DeAOT-L
- Cutie-base
- Cutie-base+
- DDMemory

### Software & Versiones
- **Sam 2 Version:** SAM 2.1
- **Sam 2 Base:** 1.0

### Análisis de Limitaciones
- Ambiguous prompts (multiple compatible target masks)
- Occlusion and re-appearance
- Small objects and parts
- SAM 2 often tends to segment object parts on the first click while DAVIS contains whole objects
- Estimation of annotation time does not account for model's tracking FPS
- Manual masklets: Human errors may exist (annotators may miss frames)
- Auto masklets: Model errors such as inconsistencies in masklets may exist
- Demographics: No parity across all geographic and demographic groups
- Subjectivity: Selecting objects to mask and track is inherently subjective

### Licencias detectadas
- **Sa-V Dataset:** Creative Commons Attribution 4.0 International Public License
- **Sam 2 Model Checkpoints:** Permissive open license
- **Training Code:** Apache 2.0
- **Demo Code:** Apache 2.0
- **Sam 2:** Apache 2.0

### Impacto Social (Broader Impacts)
- **Fairness Evaluation:** Minimal performance discrepancy in video segmentation based on perceived gender, and little variance among three perceived age groups.
- **Risks:** Performance on people across demographic groups
- **Recommendations:** Researchers should perform their own fairness evaluation
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

> Consolidated technical specifications, architectural components, and performance metrics from three distinct fragments. Merged dataset statistics, hardware/environmental impact data, and ethical/licensing documentation. Resolved versioning (SAM 2.1 vs 1.0) and ensured all baseline models and dataset lists were unified. The paper demonstrates high technical rigor through extensive benchmarking and detailed data-engine documentation.

### 📍 Secciones Identificadas del Paper
- `Introduction`
- `Related work`
- `Task: promptable visual segmentation`
- `Model`
- `Data`
- `Zero-shot experiments`
- `Comparison to state-of-the-art in semi-supervised VOS`
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
