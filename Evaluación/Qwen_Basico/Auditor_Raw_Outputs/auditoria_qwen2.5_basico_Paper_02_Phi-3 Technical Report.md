# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `Paper_02_Phi-3 Technical Report.pdf` |
| 📅 **Fecha de Análisis** | 2026-07-04 09:55:50 |
| ⏳ **Tiempo de Ejecución** | 752.62s |
| 📊 **Caracteres Analizados** | 70,371 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **1 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 8
- **No Cumple (No):** 6
- **No Aplica (N/A):** 2
- **Ítems con Alerta:** 1

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | phi-3-mini achieves 69% on MMLU and 8.38 on MT-bench, despite being small enough to be deployed on a phone. |
| 2 | Limitations | 🔴 No | Regarding the multi-modal LLM capabilities of our Phi-3.5-Vision, it performs admirably across various fields. However, we have identified certain limitations, particularly with questions necessitating high-level reasoning abilities. Additionally, the model has been observed to occasionally generate ungrounded outputs, making it potentially unreliable in sensitive areas, such as finance. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 3 | Theory, Assumptions & Proofs | 🟢 Yes | Pre-training is performed in two disjoint and sequential phases; phase-1 comprises mostly of web sources aimed at teaching the model general knowledge and language understanding. Phase-2 merges even more heavily filtered webdata (a subset used in Phase-1) with some synthetic data that teach the model logical reasoning and various niche skills. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The phi-3-mini model is built upon a similar block structure as Llama-2 [TLI + 23] and uses the same tokenizer with vocabulary size of 32064 1 . |
| 5 | Open Access to Data and Code | 🔴 No | — |
| 6 | Experimental Setting / Details | 🟢 Yes | We trained using bfloat16 for a total of 3.3T tokens. The model is already chat-finetuned, and the chat template is as follows: <|user|> / n Question <|end|> / n <|assistant|> |
| 7 | Experiment Statistical Significance | 🟢 Yes | phi-3-mini achieves 69% on MMLU and 8.38 on MT-bench |
| 8 | Experiments Compute Resource | 🔴 No | — |
| 9 | Code of Ethics | 🟢 Yes | Phi-3-mini was developed in accordance with Microsoft's responsible AI principles. The overall approach consisted of safety alignment in post-training, red-teaming, automated testing and evaluations across dozens of RAI harm categories. |
| 10 | Broader Impacts | 🟢 Yes | Regarding the multi-modal LLM capabilities of our Phi-3.5-Vision, it performs admirably across various fields. However, we have identified certain limitations, particularly with questions necessitating high-level reasoning abilities. Additionally, the model has been observed to occasionally generate ungrounded outputs, making it potentially unreliable in sensitive areas, such as finance. |
| 11 | Safeguards | 🟢 Yes | Phi-3-mini was developed in accordance with Microsoft's responsible AI principles. The overall approach consisted of safety alignment in post-training, red-teaming, automated testing and evaluations across dozens of RAI harm categories. |
| 12 | Licenses | 🔴 No | — |
| 13 | Assets | 🔵 N/A | — |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | — |
| 15 | IRB Approvals | 🔵 N/A | — |
| 16 | Declaration of LLM Usage | 🔴 No | — |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
3072 hidden dimension, 32 heads and 32 layers. Trained using bfloat16 for a total of 3.3T tokens.

### Hardware & Compute
Not specified in the paper.

### Arquitectura del Modelo
Transformer decoder architecture [VSP + 17], with default context length 4 K .

### Dataset & Datos
Heavily filtered publicly available web data and synthetic data created by LLMs.

### Código & Repositorio
No code is provided or referenced.

### Estadística & Rigor Científico
Error bars are reported for some benchmarks, such as MMLU and MT-bench.

### Comparativa con Baselines
phi-3-mini outperforms models like Mixtral 8x7B and GPT-3.5 on certain benchmarks.

### Teoría & Demostraciones
The paper discusses the training data and methodology but does not provide detailed proofs or formal theoretical results.

### Software & Versiones
Not specified in the paper.

### Análisis de Limitaciones
Limited factual knowledge, occasional ungrounded outputs, and potential unreliability in sensitive areas like finance.

### Licencias detectadas
-

### Impacto Social (Broader Impacts)
Potential impacts include performance in sensitive areas such as finance. However, a detailed analysis is not provided.

### Declaración de uso de LLMs
-

### Sujetos Humanos & Crowdsourcing
-

---

## 🧠 Razonamiento de Consolidación (CoT)

> The paper provides details on the model's architecture, training data, and performance but lacks specific information on reproducibility, hardware, code, and licensing. It also does not provide detailed statistical methods or a thorough analysis of broader impacts.

### 📍 Secciones Identificadas del Paper
- `Technical Specifications`
- `Academic benchmarks`
- `Weakness`

---
_Informe generado automáticamente._
