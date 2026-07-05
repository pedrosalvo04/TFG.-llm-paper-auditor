# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `Paper_13_Artificial Hivemind.pdf` |
| 📅 **Fecha de Análisis** | 2026-07-03 21:43:31 |
| ⏳ **Tiempo de Ejecución** | 49.39s |
| 📊 **Caracteres Analizados** | 568,870 |

### 🎯 Veredicto del Checklist
> **✅ CHECKLIST VÁLIDO**
> Todas las respuestas obligatorias del autor cuentan con una evidencia o justificación adecuada para los revisores. El checklist está en un estado óptimo.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 14
- **No Cumple (No):** 0
- **No Aplica (N/A):** 2
- **Ítems con Alerta:** 0

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | To address this gap, we introduce INFINITY-CHAT, a large-scale dataset of 26K diverse, real-world, open-ended user queries... Using INFINITY-CHAT, we present a large-scale study of mode collapse in LMs, revealing a pronounced Artificial Hivemind effect. |
| 2 | Limitations | 🟢 Yes | While comprehensive with 26K queries, INFINITY-CHAT represents only a snapshot of the vast space of possible open-ended queries... the focus on English-language prompts... potentially underrepresents linguistic, cultural, and regional diversity. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | — |
| 4 | Experimental Result Reproducibility | 🟢 Yes | Full details of the query mining process are provided in §Appendix B.1... Full experimental setup, complete model results, and examples are provided in §Appendix C. |
| 5 | Open Access to Data and Code | 🟢 Yes | Code : https://github.com/liweijiang/artificial-hivemind; INFINITY-CHAT Collection : liweijiang/artificial-hivemind |
| 6 | Experimental Setting / Details | 🟢 Yes | Each of the 25 models generates 50 responses using topp sampling (p = 0.9) and temperature = 1.0. |
| 7 | Experiment Statistical Significance | 🟢 Yes | We compute Spearman's correlation coefficients between human-annotated and model-generated absolute rating scores... The results show that correlations are notably lower in these two subsets. |
| 8 | Experiments Compute Resource | 🟢 Yes | For all HuggingFace models, generations are performed on NVIDIA A100 or H100 GPUs... For closed-source models... we use their respective APIs. |
| 9 | Code of Ethics | 🟢 Yes | We confirm the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics. |
| 10 | Broader Impacts | 🟢 Yes | If users increasingly rely on such systems for creative tasks, exposure to homogenized outputs could subtly influence human thinking patterns and reduce overall cultural and intellectual diversity. |
| 11 | Safeguards | 🟢 Yes | We discuss safeguards that have been put in place for responsible release of data or in §Appendix A. |
| 12 | Licenses | 🟢 Yes | We construct INFINITY-CHAT... by filtering and refining user inputs from WildChat [94]. |
| 13 | Assets | 🟢 Yes | We document all assets. (Appendix B) |
| 14 | Crowdsourcing & Human Subjects | 🟢 Yes | We recruit human annotators from Prolific... Annotators are compensated at an average rate of $15 per hour. |
| 15 | IRB Approvals | 🔵 N/A | Our human annotation is innocuous and thus does not require IRB approval. |
| 16 | Declaration of LLM Usage | 🟢 Yes | GPT-4o classifies each by whether it seeks meaningful information... We instruct GPT-4o to label each user query with one or more of the existing open-ended categories. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
topp=0.9, temperature=1.0, minp=0.1, temperature=2.0

### Hardware & Compute
NVIDIA A100 or H100 GPUs

### Arquitectura del Modelo
Various LMs (Llama, Qwen, Gemma, Mistral, etc.)

### Dataset & Datos
INFINITY-CHAT (26K queries), WildChat (source)

### Código & Repositorio
https://github.com/liweijiang/artificial-hivemind

### Estadística & Rigor Científico
Spearman's correlation, Shannon entropy, cosine similarity

### Comparativa con Baselines
Comparison across 70+ LMs, reward models, and LM judges

### Teoría & Demostraciones
N/A

### Software & Versiones
Not explicitly listed, but models are identified by version/date

### Análisis de Limitaciones
Discussed in Appendix A.1

### Licencias detectadas
WildChat [94] cited

### Impacto Social (Broader Impacts)
Discussed in Appendix A.3

### Declaración de uso de LLMs
GPT-4o used for data classification and taxonomy

### Sujetos Humanos & Crowdsourcing
Proflific annotators, $15/hr compensation

---

## 🧠 Razonamiento de Consolidación (CoT)

> The paper is a rigorous empirical study. The authors follow NeurIPS guidelines by providing extensive appendices covering methodology, limitations, and ethics. The claims are well-supported by the data provided.

### 📍 Secciones Identificadas del Paper
- `Section 1: Introduction`
- `Section 2: INFINITY-CHAT`
- `Section 3: Artificial Hivemind`
- `Section 4: Model Calibration`
- `Appendix A: Limitations`
- `Appendix B: Dataset Details`
- `Appendix C: Homogeneity Analysis`
- `Appendix D: Human Annotation`

---
_Informe generado automáticamente._
