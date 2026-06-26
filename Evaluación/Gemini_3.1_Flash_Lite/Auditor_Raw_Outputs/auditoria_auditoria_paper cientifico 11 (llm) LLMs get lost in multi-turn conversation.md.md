# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `auditoria_paper cientifico 11 (llm) LLMs get lost in multi-turn conversation.md` |
| 📅 **Fecha de Análisis** | 2026-06-16 17:54:48 |
| ⏳ **Tiempo de Ejecución** | 49.09s |
| 📊 **Caracteres Analizados** | 7,493 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **3 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 9
- **No Cumple (No):** 3
- **No Aplica (N/A):** 4
- **Ítems con Alerta:** 3

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The abstract and introduction claim that LLMs suffer from a 'lost in conversation' phenomenon, characterized by performance degradation in multi-turn, underspecified settings. The paper supports these claims through a systematic evaluation across 200,000+ simulated conversations, demonstrating a 39% average performance drop and identifying specific failure modes such as 'answer bloat' and 'loss-of-middle-turns'. |
| 2 | Limitations | 🟢 Yes | Section 9, titled 'Limitations', explicitly states: 'Simulated conversations are not representative of human-AI conversations', 'Simulation environment is simplistic and idealized', 'Conversations are guaranteed to end with sufficient information', and 'Degradations observed are likely underestimates of real-world scenarios'. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper focuses on empirical analysis of LLM behavior in multi-turn conversations rather than proposing new mathematical theorems or formal proofs. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation, which includes the implementation of the simulation pipeline, the sharding process, and the evaluation logic used to generate the reported results. |
| 5 | Open Access to Data and Code | 🟢 Yes | The authors provide a dedicated repository at https://github.com/Microsoft/lost_in_conversation. This repository contains the implementation of the simulation framework, the sharding pipeline, and the evaluation logic used to generate the results presented in the paper. This fulfills the NeurIPS 2026 criteria for Open Access to Data and Code, which requires that authors include the code, data, and instructions needed to reproduce the main experimental results. |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides extensive documentation of experimental settings across the main text and appendices. Specifically, Appendix I (Task-specific Implementation details), Appendix K (Gradual Sharding Implementation), Appendix L (Temperature Experiment Implementation), and Appendix M (Recap & Snowball Experiment Implementation) detail the methodology. Furthermore, the summary explicitly lists temperature settings (0.0, 0.5, 1.0), simulation counts (10 to 20 per pair), and performance thresholds (0.8). This satisfies the NeurIPS 2026 criteria, which mandates that authors specify all training details, such as data splits and hyperparameters, and explain how these were chosen. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper fails to meet the NeurIPS 2026 criteria for statistical significance. While the authors report performance metrics such as 'average performance drop' and 'multi-turn performance average', they do not provide error bars, confidence intervals, or formal statistical significance tests (e.g., p-values or hypothesis testing) to accompany these results. The NeurIPS criteria explicitly require that results supporting the main claims be accompanied by such measures to account for factors of variability. Furthermore, the authors do not provide an explicit scientific or computational justification for the omission of these statistics, meaning the 'is_no_justified' flag must be set to false. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🔴 No | The paper does not provide sufficient information regarding the compute resources used for the experiments. According to the NeurIPS 2026 criteria, authors must indicate the type of compute workers (CPU/GPU), memory, and storage, as well as provide an estimate of the total compute required for the experimental runs. The provided text contains no mention of the hardware infrastructure, execution time, or efficiency metrics for the 200,000+ simulated conversations. Because the authors failed to disclose these technical details and provided no justification for their absence, this constitutes a transparency risk regarding reproducibility. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 9 | Code of Ethics | 🔴 No | The authors have failed to include a dedicated 'Code of Ethics' statement or an explicit declaration of adherence to the NeurIPS Code of Ethics. While the research involves human-in-the-loop simulations and validation processes, there is no mention of IRB approval, ethical review processes, or compliance with the NeurIPS requirement regarding fair wages for human participants as outlined in the 'Potential Harms Caused by the Research Process' section. The absence of an ethical disclosure constitutes a transparency risk, as the paper does not address the potential societal impacts or ethical considerations of using LLMs as judges and simulators in a way that conforms to the conference's expectations. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 10 | Broader Impacts | 🟢 Yes | The paper includes dedicated sections: 7.1 'Implications for System and Agent Builders', 7.2 'Implications for LLM Builders', 7.3 'Implications for NLP Practitioners', and 7.4 'Implications for Users of Conversational Systems'. |
| 11 | Safeguards | 🔵 N/A | The paper presents a diagnostic framework for evaluating LLM performance in multi-turn, underspecified conversations using existing, publicly available models (e.g., GPT-4o, Claude 3.7, Llama 3.1). |
| 12 | Licenses | 🟢 Yes | The repository at https://github.com/Microsoft/lost_in_conversation is associated with the authors' work and is released under the MIT License. |
| 13 | Assets | 🟢 Yes | The authors provide a comprehensive repository at https://github.com/Microsoft/lost_in_conversation, which includes the simulation framework, the sharding pipeline, and the evaluation toolkits used to generate the results. The paper details the 'Semi-Automatic Sharding Process' in Appendix C and provides specific task-specific implementation details in Appendix I. |
| 14 | Crowdsourcing & Human Subjects | 🔵 N/A | The paper relies on a fully automated simulation environment using LLMs as agents, judges, and strategy classifiers. The 'human_subjects_extraction' section notes that manual inspection and validation of shards were performed by the authors themselves as part of the research process. |
| 15 | IRB Approvals | 🔵 N/A | The research utilizes established, publicly available datasets such as HumanEval, Spider 1.0, GSM8K, ToTTo, and WMT 2019, alongside a semi-automated simulation pipeline where LLMs act as both the user and the assistant. As the study does not involve direct human subjects or the collection of new human-derived data, and relies on existing public benchmarks, IRB approval is not applicable under the NeurIPS 2026 criteria for human subjects research. |
| 16 | Declaration of LLM Usage | 🟢 Yes | The paper explicitly states in the methodology: 'The methodology relies on a semi-automated sharding pipeline and a multi-agent simulation environment.' Furthermore, the 'llm_usage_extraction' section details that LLMs are used as a judge, user simulator, strategy classifier, answer extractor, and for the sharding process itself. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Latency Metrics:** 136.65s execution time
- **Temperature:** [0.0, 0.5, 1.0]
- **Simulation Counts:** 10 to 20 per pair
- **Performance Thresholds:** 0.8

### Arquitectura del Modelo

### Dataset & Datos
- HumanEval
- Spider 1.0
- GSM8K
- ToTTo
- WMT 2019

### Código & Repositorio
- **Repository Url:** https://github.com/Microsoft/lost_in_conversation

### Estadística & Rigor Científico
- **Characters Analyzed:** 156326
- **Checklist Items With Problems:** 3
- **Total Checklist Items:** 16
- **Reported Metrics:** ['average performance drop', 'multi-turn performance average']
- **Significance Measures:** None provided (no error bars, confidence intervals, or p-values)

### Comparativa con Baselines
- GPT-4o
- Claude 3.7
- Llama 3.1

### Análisis de Limitaciones
- Requiere Atencion (Faltan justificaciones)
- Simulated conversations are not representative of human-AI conversations
- Simulation environment is simplistic and idealized
- Conversations are guaranteed to end with sufficient information
- Degradations observed are likely underestimates of real-world scenarios

### Licencias detectadas
MIT License

### Impacto Social (Broader Impacts)
- Implications for System and Agent Builders
- Implications for LLM Builders
- Implications for NLP Practitioners
- Implications for Users of Conversational Systems

### Declaración de uso de LLMs
- **Roles:** ['judge', 'user simulator', 'strategy classifier', 'answer extractor', 'sharding process']
- **Models Used:** ['GPT-4o', 'Claude 3.7', 'Llama 3.1']

### Sujetos Humanos & Crowdsourcing
Manual inspection and validation of shards performed by authors; no external human subjects or crowdsourcing.

---

## 🧠 Razonamiento de Consolidación (CoT)

> Consolidated audit report and technical metadata. The paper exhibits significant transparency gaps regarding statistical rigor, compute resource disclosure, and ethical documentation, despite providing clear simulation parameters and baseline models. The technical architecture remains undefined, focusing instead on the evaluation of multi-turn conversation degradation.

### 📍 Secciones Identificadas del Paper
- `NeurIPS 2026 Checklist Audit Report`
- `1. Claims`
- `2. Limitations`
- `3. Theory, Assumptions & Proofs`
- `4. Experimental Result Reproducibility`
- `5. Open Access to Data and Code`
- `6. Experimental Setting / Details`
- `7. Experiment Statistical Significance`
- `8. Experiments Compute Resource`
- `9. Code of Ethics`
- `10. Broader Impacts`
- `11. Safeguards`
- `12. Licenses`
- `13. Assets`
- `14. Crowdsourcing & Human Subjects`
- `15. IRB Approvals`
- `16. Declaration of LLM Usage`

---
_Informe generado automáticamente._
