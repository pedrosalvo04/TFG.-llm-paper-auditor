# 🔬 Informe de Auditoría Científica - NeurIPS 2026

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 11 (llm) LLMs get lost in multi-turn conversation.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-14 20:56:00 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 574.59s |
| 📊 **Caracteres Analizados** | 156,326 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **3 de 16** ítem(s) que requieren atención o justificación adicional antes del envío oficial.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 7
- **No Cumple (No):** 4
- **No Aplica (N/A):** 4
- **Ítems con Alerta:** 3

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | "This paper investigates the performance degradation of large language models (LLMs) in multi-turn conversations, focusing on significant performance degradation and reliability issues. The study highlights that LLMs struggle to maintain context across turns, especially in underspecified settings." This statement is directly supported by the experimental results showing significant performance degradation in multi-turn and underspecified settings. |
| 2 | Limitations | 🟢 Yes | "The authors acknowledge limitations of the study, including reliance on automated simulation and task scope. The focus on analytical tasks limits the generalizability to other domains such as creative writing or multi-modal tasks. Experiments conducted only in English language also narrow the applicability of findings." These statements directly address potential limitations. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper does not contain any theoretical results, proofs, or assumptions. The focus is on empirical studies and observations of LLM performance in multi-turn conversations. Given that the NeurIPS 2026 criteria for Theory, Assumptions and Proofs specifically require the inclusion of such elements if present, this item is not applicable to the paper as it does not meet the criteria's definition of a theoretical contribution. |
| 4 | Experimental Result Reproducibility | 🔴 No | The paper does not provide any code, model weights, or instructions that would allow others to reproduce the experimental results. According to the NeurIPS 2026 criteria for Experimental Result Reproducibility, this is a critical requirement for contributions involving datasets or models. The lack of such information constitutes a transparency risk as it prevents other researchers from verifying and building upon the findings. |
| 5 | Open Access to Data and Code | 🔴 No | The paper does not provide any information about the availability of its own original code, model weights, or newly collected datasets used for the main experiments. The pre-computed help indicates that no code/model URLs are found and that the data/resource URLs are also not present. According to the NeurIPS 2026 official criteria, if ANY public URL (project, demo, HF, github) exists, the answer should be 'Yes'. Since no such URLs or instructions for accessing these resources are provided by the authors, this paper fails to meet the transparency requirement for open access to data and code. The omission of these details poses a significant risk as it hinders reproducibility and verification of the experimental results. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides detailed descriptions of the training data splits, hyperparameters, and how they were chosen. For instance, in the 'Methodology' section, it states: 'We designed a simulation setup using LLMs to generate user utterances for both single-turn (FULL) and multi-turn (CONCAT and SHARDED) settings.' Additionally, the paper mentions specific hyperparameter choices and their rationale, such as the use of greedy decoding in the experiments. This information is crucial for understanding the experimental design and can be found either directly in the main paper or in the supplementary materials. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not provide error bars, confidence intervals, or any other form of statistical significance measures. The only information provided is that there was significant performance degradation in multi-turn and underspecified settings, but no statistical tests or measures are reported to support these claims. According to the NeurIPS 2026 official criteria for Experiment Statistical Significance (Item 7), 'The authors should answer <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🔵 N/A | — |
| 9 | Code of Ethics | 🟢 Yes | The paper does not explicitly contain a dedicated 'Ethics Statement' or a separate section discussing broader impacts. However, the authors demonstrate ethical awareness by considering potential harms and negative societal impacts in their discussion of LLM unreliability and future research directions. Specifically, they mention that users should be aware of LLM unreliability, especially in multi-turn settings, and recommend retrying conversations and consolidating instructions to mitigate these issues. |
| 10 | Broader Impacts | 🟢 Yes | The paper discusses the user experience and future research directions related to LLM unreliability. Specifically, it states: 'Users should be aware of LLM unreliability, especially in multi-turn settings. Recommendations include retrying conversations and consolidating instructions.' This addresses potential negative impacts on users. |
| 11 | Safeguards | 🔵 N/A | The paper focuses on a foundational study of the performance degradation in multi-turn conversations with large language models (LLMs). The research does not involve releasing any artefacts that present a high risk for misuse, such as generating harmful content, enabling surveillance, synthesising dangerous information, or being easily weaponised. Therefore, there is no need to apply safeguards as per NeurIPS 2026 criteria. The paper's primary contribution lies in the analysis of LLMs' performance and the identification of issues related to context maintenance and reliability, which are theoretical findings without direct implications for misuse. |
| 12 | Licenses | 🟢 Yes | The paper acknowledges the use of an MIT-licensed code package for generating user utterances in its simulation setup. The authors have cited the original creators and respected the license terms, as evidenced by the inclusion of a URL to the MIT License (https://choosealicense.com/licenses/mit/). This adherence to licensing requirements ensures transparency regarding the usage rights and conditions of any external assets employed in the research. |
| 13 | Assets | 🔵 N/A | The paper does not mention the release of any new assets such as datasets, model weights, benchmarks, or software libraries. The work primarily involves the use of existing LLMs and automated simulations for generating user utterances. According to the NeurIPS 2026 official criteria, this item is applicable only if the authors are releasing new assets created as part of their research. Since no such new assets were released, answering 'N/A' is appropriate. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not mention the use of crowdsourcing or conducting research with human subjects. The experiments are based on automated simulations using LLMs to generate user utterances, and no new data was collected from human participants. According to the NeurIPS 2026 official criteria, this item should be answered 'Yes' if the authors used crowdsourcing or conducted research involving human subjects, which is not the case here. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve any direct research with human subjects. It uses fully automated simulation with LLMs to generate user utterances, which is a synthetic dataset and does not require new IRB approvals according to the NeurIPS 2026 official criteria. The study focuses on analyzing performance degradation in multi-turn conversations using existing datasets without conducting any new experiments involving human participants. |
| 16 | Declaration of LLM Usage | 🟢 Yes | LLMs are more prone to confusion in generative tasks, especially those involving multiple explicit specifications. (Step: Methodology) |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Estadística & Rigor Científico
- **Performance Degradation:** [{'setting': 'multi-turn', 'degradation': 'significant'}, {'setting': 'underspecified', 'degradation': 'significant'}]
- **Reliability Decrease:** True
- **Context Maintenance Issues:** ['struggle to maintain context across turns']
- **Premature Assumptions:** True
- **Over Reliance On Previous Responses:** True

### Análisis de Limitaciones
- {'type': 'reliance_on_automated_simulation', 'description': 'Reliance on fully automated simulation with LLMs for user utterances, leading to narrow and potentially unrealistic conversation structures.'}
- {'type': 'task_scope', 'description': 'Focus on analytical tasks, limiting findings to such tasks; no exploration of creative writing or multi-modal tasks.'}
- {'type': 'language_scope', 'description': 'Experiments conducted only in English language, not exploring other languages or modalities.'}

### Impacto Social (Broader Impacts)
- {'impact_type': 'user_experience', 'description': 'Users should be aware of LLM unreliability, especially in multi-turn settings. Recommendations include retrying conversations and consolidating instructions.'}
- {'impact_type': 'future_research', 'description': 'Future work could explore degradation on creative tasks and other languages/modalities.'}

### Declaración de uso de LLMs
- {'type': 'task_complexity', 'description': 'LLMs are more prone to confusion in generative tasks, especially those involving multiple explicit specifications.'}
- {'type': 'solution_decomposability', 'description': 'Tasks that can be decomposed into turn-level subtasks may help prevent LLMs from getting lost in conversation.'}

---

## 🧠 Razonamiento de Consolidación (CoT)

> {'step': 'Introduction and Background', 'description': 'Introduces the problem of LLMs losing context in multi-turn conversations, highlighting existing work on this issue.'}
> {'step': 'Methodology', 'description': 'Describes the simulation setup using LLMs to generate user utterances, focusing on single- and multi-turn settings.'}
> {'step': 'Experiments and Results', 'description': 'Details experiments comparing performance in different settings (FULL, CONCAT, SHARDED) across various tasks.'}
> {'step': 'Discussion and Findings', 'description': 'Analyzes results, identifying significant degradation in multi-turn, underspecified settings. Calls for remediation efforts.'}
> {'step': 'Conclusion', 'description': 'Summarizes findings, emphasizing the need to prioritize LLM reliability in multi-turn conversations.'}
> {'step': 'Limitations', 'description': 'Acknowledges limitations of the study, including reliance on automated simulation and task scope.'}

### 📍 Secciones Identificadas del Paper
- `Introduction and Background`
- `Methodology`
- `Experiments and Results`
- `Discussion and Findings`
- `Conclusion`
- `Limitations`

---
_Informe generado automáticamente por Auditor NeurIPS 2026 empleando el modelo local: qwen2.5_
