# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `Paper_11_LLMs get lost in multi-turn conversation.pdf` |
| 🤖 **Modelo** | Gemini Básico (Single Prompt) |
| 📅 **Fecha de Análisis** | 2026-07-05 13:18:00 |
| ⏳ **Tiempo de Ejecución** | 6.51s |
| 📊 **Caracteres Analizados** | 156,326 |

### 🎯 Veredicto del Checklist
> **✅ CHECKLIST VÁLIDO**
> Todas las respuestas obligatorias del autor cuentan con una evidencia o justificación adecuada para los revisores. El checklist está en un estado óptimo.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 10
- **No Cumple (No):** 0
- **No Aplica (N/A):** 2
- **Ítems con Alerta:** 0

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | In this work, we perform large-scale simulation experiments to compare LLM performance in single- and multi-turn settings. Our experiments confirm that all the top open- and closed-weight LLMs we test exhibit significantly lower performance in multi-turn conversations than single-turn, with an average drop of 39% across six generation tasks. Analysis of 200,000+ simulated conversations decomposes the performance degradation into two components: a minor loss in aptitude and a significant increase in unreliability. |
| 2 | Limitations | 🟢 Yes | The authors provide a dedicated Section 9 titled 'Limitations'. They explicitly discuss the reliance on fully automated simulation, the focus on analytical tasks, and the focus on text-only tasks in the English language. They acknowledge that the simulation environment is 'simplistic and idealized' and that the observed degradations are likely 'underestimates of what occurs in real-world, underspecified multi-turn Human-AI conversations.' |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | — |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The authors provide a GitHub repository (Microsoft/lost_in_conversation) and a Hugging Face dataset (datasets/Microsoft/lost_in_conversation). They also provide detailed appendices (A-O) covering the sharding process, simulation parameters, model versions, and prompts used for the user simulator, strategy classifier, and answer extractor. |
| 5 | Open Access to Data and Code | 🔵 N/A | — |
| 6 | Experimental Setting / Details | 🟢 Yes | The paper provides extensive details on the experimental setup in Section 5 and the appendices. Appendix H lists model versions and access providers, Appendix I details task-specific implementation (including evaluation metrics and system prompts), and Appendix O provides the full text of the prompts used for simulation. |
| 7 | Experiment Statistical Significance | 🟢 Yes | The authors define metrics (Aptitude A90 and Unreliability U90-10) based on percentile estimates from 10 repeated simulations per instruction. They explicitly state: 'Although simulating ten conversations for each (LLM, instruction, simulation type) increases experimental costs ten-fold, it allows us to not only measure averaged performance (P) more accurately, but also study aptitude and reliability of LLM systems in depth.' |
| 8 | Experiments Compute Resource | 🟢 Yes | The authors provide an estimate of the total cost of conducting simulations: 'We estimate the total cost of conducting simulations to be around $5,000.' They also specify the scale of the experiment (200,000+ simulated conversations) and the use of API-based models, which implicitly defines the compute resource requirements. |
| 9 | Code of Ethics | 🟢 Yes | The research involves automated simulation of LLMs and does not involve human subjects or sensitive personal data. The authors follow standard practices for AI research, and the work does not violate the NeurIPS Code of Ethics regarding safety, security, or discrimination. |
| 10 | Broader Impacts | 🟢 Yes | The authors discuss the implications of their findings for system builders, LLM builders, NLP practitioners, and end-users in Section 7. They explicitly address the potential for low uptake of AI systems due to performance degradation and provide actionable recommendations for users to mitigate these issues. |
| 11 | Safeguards | 🔵 N/A | The paper does not release a new, high-risk pretrained model; it uses existing, publicly available models via APIs or local execution for evaluation purposes. Therefore, the requirement for safeguards for high-risk model release is not applicable. |
| 12 | Licenses | 🟢 Yes | The authors cite the datasets used (HumanEval, LiveCodeBench, Spider, BFCL, GSM8K, ToTTo, Summary of a Haystack, WMT 2019) and acknowledge the use of existing models, respecting the terms of use for these assets. |
| 13 | Assets | 🟢 Yes | The authors document the new assets (the sharded instruction datasets) in the paper and provide them via the linked Hugging Face repository, including details on the sharding process in Appendix C. |
| 14 | Crowdsourcing & Human Subjects | 🔵 N/A | — |
| 15 | IRB Approvals | 🔵 N/A | As the research does not involve human subjects, IRB approval is not required. |
| 16 | Declaration of LLM Usage | 🔵 N/A | — |
---

## 🧠 Razonamiento de Consolidación (CoT)

> The paper presents a rigorous, large-scale simulation study of LLM performance in multi-turn, underspecified conversations. It introduces a sharding methodology to transform single-turn benchmarks into multi-turn tasks, evaluates 15 LLMs across 200,000+ simulated conversations, and provides a detailed decomposition of performance degradation into aptitude and reliability metrics.

---
_Informe generado automáticamente._
