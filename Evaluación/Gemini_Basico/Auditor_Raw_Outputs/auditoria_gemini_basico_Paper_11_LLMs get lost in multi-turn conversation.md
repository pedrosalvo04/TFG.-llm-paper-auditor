# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `Paper_11_LLMs get lost in multi-turn conversation.pdf` |
| 📅 **Fecha de Análisis** | 2026-07-03 21:39:11 |
| ⏳ **Tiempo de Ejecución** | 6.36s |
| 📊 **Caracteres Analizados** | 156,326 |

### 🎯 Veredicto del Checklist
> **✅ CHECKLIST VÁLIDO**
> Todas las respuestas obligatorias del autor cuentan con una evidencia o justificación adecuada para los revisores. El checklist está en un estado óptimo.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 12
- **No Cumple (No):** 0
- **No Aplica (N/A):** 4
- **Ítems con Alerta:** 0

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | In this work, we perform large-scale simulation experiments to compare LLM performance in single- and multi-turn settings. Our experiments confirm that all the top open- and closed-weight LLMs we test exhibit significantly lower performance in multi-turn conversations than single-turn, with an average drop of 39% across six generation tasks. |
| 2 | Limitations | 🟢 Yes | A first limitation of our work is the reliance on fully automated simulation... A second limitation of our work is the focus on analytical tasks... A third limitation of the work is the focus on text-only tasks in the English language. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | — |
| 4 | Experimental Result Reproducibility | 🟢 Yes | https://github.com/Microsoft/lost_in_conversation |
| 5 | Open Access to Data and Code | 🟢 Yes | https://github.com/Microsoft/lost_in_conversation; https://huggingface.co/datasets/Microsoft/lost_in_conversation |
| 6 | Experimental Setting / Details | 🟢 Yes | All simulations were conducted with a default temperature of T = 1... Details on model versioning and access are listed in Appendix H. |
| 7 | Experiment Statistical Significance | 🟢 Yes | We leverage this property to conduct repeated simulations for a given instruction and observe the variations that occur... Based on the set of scores S = { S i } N i =1 obtained from running N simulations for an instruction, we define three metrics... |
| 8 | Experiments Compute Resource | 🟢 Yes | We estimate the total cost of conducting simulations to be around $5,000. |
| 9 | Code of Ethics | 🟢 Yes | — |
| 10 | Broader Impacts | 🟢 Yes | Section 7: Implications |
| 11 | Safeguards | 🔵 N/A | — |
| 12 | Licenses | 🟢 Yes | References section cites [10], [86], [14], etc. |
| 13 | Assets | 🟢 Yes | https://huggingface.co/datasets/Microsoft/lost_in_conversation |
| 14 | Crowdsourcing & Human Subjects | 🔵 N/A | — |
| 15 | IRB Approvals | 🔵 N/A | — |
| 16 | Declaration of LLM Usage | 🟢 Yes | We instantiate the user simulator as a low-cost LLM (specifically, GPT-4o-mini)... Apart from the user simulator, the strategy classifier and answer extractor components are also implemented with prompt-based GPT-4o-mini. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
Temperature T=1.0 (default), T=0.0/0.5 for ablation. Max response length 1,000 tokens (10,000 for reasoning models).

### Hardware & Compute
Not explicitly listed, but cost estimated at $5,000 for API-based simulations.

### Arquitectura del Modelo
15 LLMs tested: GPT-4o, GPT-4o-mini, o3, GPT-4.1, Claude 3 Haiku, Claude 3.7 Sonnet, Gemini 2.5 Flash/Pro, Llama 3.1/3.3/4, OLMo-2, Phi-4, Deepseek-R1, Command-A.

### Dataset & Datos
GSM8K, HumanEval, LiveCodeBench, Spider, BFCL, ToTTo, Summary of a Haystack, WMT 2019.

### Código & Repositorio
https://github.com/Microsoft/lost_in_conversation

### Estadística & Rigor Científico
N=10 simulations per instruction/model pair. Metrics: Averaged Performance (P), Aptitude (A), Unreliability (U).

### Comparativa con Baselines
FULL (single-turn), CONCAT (single-turn with shards), SHARDED (multi-turn).

### Teoría & Demostraciones
N/A

### Software & Versiones
See Appendix H for model versions.

### Análisis de Limitaciones
High; authors acknowledge simulation limitations and scope.

### Licencias detectadas
Standard academic benchmarks cited.

### Impacto Social (Broader Impacts)
Discussed in Section 7 regarding reliability and user trust.

### Declaración de uso de LLMs
Used for user simulation, strategy classification, and answer extraction.

### Sujetos Humanos & Crowdsourcing
None.

---

## 🧠 Razonamiento de Consolidación (CoT)

> The paper is a rigorous empirical study. It follows the NeurIPS checklist structure well, providing clear evidence for its claims and methodology. The use of LLMs in the simulation loop is transparently declared and justified.

### 📍 Secciones Identificadas del Paper
- `Section 3: Simulation Environment`
- `Section 6: Results`
- `Section 7: Implications`
- `Appendix C: Sharding Process`

---
_Informe generado automáticamente._
