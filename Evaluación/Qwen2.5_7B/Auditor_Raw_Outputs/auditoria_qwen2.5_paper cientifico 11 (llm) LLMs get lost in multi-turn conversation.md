# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 11 (llm) LLMs get lost in multi-turn conversation.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-28 13:56:56 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 664.09s |
| 📊 **Caracteres Analizados** | 156,326 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **2 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 10
- **No Cumple (No):** 3
- **No Aplica (N/A):** 3
- **Ítems con Alerta:** 2

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The paper's claims in the abstract and introduction are accurately reflected by the results presented. For instance, the claim that 'models engaged in multi-turn underspecified conversations achieved an average performance of 65% - a 25-point drop from single-turn performances of 90%' is supported by Table 1 in Section 6.2, which shows this exact performance degradation. Additionally, the paper claims that models exhibit both loss in aptitude and increase in unreliability in multi-turn settings, as detailed in Section 6.3. These claims are substantiated by the experimental results presented throughout the paper. |
| 2 | Limitations | 🟢 Yes | The paper explicitly discusses several limitations, including reliance on fully automated simulation (Section 9), focus on analytical tasks (Section 9), and text-only tasks in the English language (Section 9). These limitations are clearly stated and discussed in a separate 'Limitations' section. |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper does not present any theoretical results, proofs, or assumptions. The content is primarily experimental and empirical in nature, focusing on the performance of large language models (LLMs) in multi-turn conversations. Therefore, there are no theoretical results to state assumptions for, nor include proofs of. This makes the item N/A as per the official criteria. |
| 4 | Experimental Result Reproducibility | 🟢 Yes | The paper provides a public repository URL (https://github.com/microsoft/lost_in_conversation) where the authors' own original code and data can be accessed. The repository includes datasets, models, and instructions for reproducing the experiments. Specifically, the summary mentions: 'code': [{'repository_url': 'Microsoft/lost_in_conversation', 'release_mention': 'datasets/Microsoft/lost_in_conversation'}]. This satisfies the requirement of making results reproducible. |
| 5 | Open Access to Data and Code | 🟢 Yes | "The Code instructions are sourced from a combination of HumanEval [10], a dataset of 164 basic Python programming problems given the function header and the docstring that specifies the problem, and LiveCodeBench [31], an evolving dataset of Python algorithmic challenges. In particular, we source from the 'call-based' problem subset in LiveCodeBench v5, with the difficulty of either 'Easy' and 'Medium', to align the solution formats between the two sources." This text indicates that the authors have provided access to their own original code or datasets used for the main experiments. Additionally, the repository URL is mentioned: "datasets/Microsoft/lost_in_conversation". |
| 6 | Experimental Setting / Details | 🟢 Yes | "In the main simulation experiment, we leveraged the totality of instructions we sharded across six tasks (a total of 600 instructions), and simulated conversations across three types: FULL, CONCAT, and SHARDED. We experimented with 15 LLMs, running N = 10 simulations for each pair of model and simulation type, totaling more than 200,000 simulated conversations. All simulations were conducted with a default temperature of T = 1 , however, we conducted a supplementary experiment (Section 7.2) that explores the effect of temperature on aptitude and reliability." This text provides detailed experimental settings including the number of tasks, types of simulations, models used, and simulation parameters. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not provide error bars, confidence intervals, or statistical significance tests for the experiments. The results are reported as averages without any indication of variability or uncertainty. For instance, in Section 6.2, the performance degradation (P) is averaged across multiple simulations but no error bars or other measures of statistical significance are provided. Similarly, in the gradual sharding experiment described in Section 6.3, there is no mention of statistical tests or confidence intervals to support the reported results. The lack of these statistical measures means that readers cannot assess the reliability and robustness of the findings, which is a critical aspect of scientific reporting. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🔴 No | The paper does not provide sufficient information on the computer resources needed to reproduce the experiments. While it mentions the hardware used (Section 5 Simulation Scale and Parameters), it does not specify the amount of compute required for each experimental run or estimate the total compute. For example, in Section 6.3 Gradual Sharding Experiment, it states that simulations were conducted with a default temperature but does not provide details on the number of runs, time taken per run, or the overall computational budget. This omission makes it difficult to reproduce the experiments and assess their reproducibility. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 9 | Code of Ethics | 🟢 Yes | The paper discusses the potential negative societal impacts of LLMs in multi-turn conversations, particularly focusing on performance degradation and reliability issues. The authors highlight that these models often make assumptions early in the conversation and may prematurely attempt to generate final solutions, which can lead to incorrect or bloated answers (see 'problematic_phrases' section). This addresses potential harms related to misinformation and incorrect information dissemination. |
| 10 | Broader Impacts | 🟢 Yes | The paper discusses the potential negative societal impacts of LLMs in multi-turn conversations, particularly focusing on performance degradation and reliability issues. The authors highlight that these models often make assumptions early in the conversation and may prematurely attempt to generate final solutions, which can lead to incorrect or bloated answers (see 'problematic_phrases' section). This addresses potential harms related to misinformation and incorrect information dissemination. |
| 11 | Safeguards | 🔵 N/A | The paper focuses on evaluating the performance of large language models (LLMs) in multi-turn conversations and does not release any high-risk artefacts such as harmful content generation, surveillance tools, or dangerous information synthesis. The work is primarily theoretical and foundational research aimed at understanding the behavior of LLMs in conversational settings. Therefore, there is no need for explicit access restrictions, usage guidelines, or technical guardrails to mitigate misuse risks. |
| 12 | Licenses | 🟢 Yes | The paper mentions that the code and model URLs are available at https://github.com/microsoft/lost_in_conversation. The license used is MIT, as stated in the extracted data facts: 'LICENSES FOUND: ['MIT']'. This indicates that the authors have provided a permissive open-source license for their work. |
| 13 | Assets | 🟢 Yes | "The Summary instructions are based on samples of the Summary of a Haystack dataset [40]. We reuse the entire instructions from Summary of a Haystack to produce 92 sharded instructions. The original instructions each consist of a haystack - 100 documents for a total of 100,000 tokens of content - and a user query." This text indicates that new assets are being released, specifically the sharded instructions derived from the Summary of a Haystack dataset. Furthermore, "The Code instructions are sourced from a combination of HumanEval [10], a dataset of 164 basic Python programming problems given the function header and the docstring that specifies the problem, and LiveCodeBench [31], an evolving dataset of Python algorithmic challenges." This also confirms the creation of new assets. The paper provides details about these datasets, including their sources and how they were sharded. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not mention any hiring or compensating of human workers to collect or label new data. All the datasets and instructions used are either existing public resources (like Spider, GSM8K, etc.) or derived from them without involving new human subjects. Therefore, this item is applicable but answered as 'No' because no new crowdsourcing was conducted. |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve any direct research with human subjects. It primarily focuses on simulating multi-turn conversations using existing datasets and LLMs, which do not require new IRB approvals as per the official criteria. The authors use publicly available data from Microsoft/lost_in_conversation for their experiments, and there is no mention of conducting new human experiments or interactions. |
| 16 | Declaration of LLM Usage | 🟢 Yes | Today's large language models (LLMs) function as conversational interfaces ( e.g. , ChatGPT, Gemini, Claude), enabling users to interact with the LLM through multiple conversation turns. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
- **Total Tokens:** [1000]
- **Hardware:** ['GPT-4o, GPT-4o-mini, GPT-4.1, o3, Claude 3 Haiku, Claude 3.7 Sonnet, Gemini 2.5 Flash, Gemini 2.5 Pro, Llama-3.1-8B-Instruct, Llama-3.3-70B-Instruct, Llama-4 Scout-17B-16E, Command-A, Deepseek-R1, OLMo2-13B, Phi-4']

### Arquitectura del Modelo

### Dataset & Datos
- {'dataset_name': 'Microsoft/lost_in_conversation', 'access_url': 'https://github.com/microsoft/lost_in_conversation', 'preprocessing': 'Not specified in the provided fragments.'}
- {'table': 'Table 1, Table 2, Table 3, Table 4', 'description': ['Averaged performance degradation (P)', 'Experimental Results with additional simulation types: Recap and Snowball', 'Unreliability of models when changing assistant temperature (AT) and user temperature (UT) in FULL, CONCAT and SHARDED settings', 'Performance on the translation task for FULL, CONCAT, and SHARDED simulations']}

### Código & Repositorio
- {'repository_url': 'Microsoft/lost_in_conversation', 'release_mention': 'datasets/Microsoft/lost_in_conversation'}

### Comparativa con Baselines
- {'setting': 'models engaged in multi-turn underspecified conversations achieved an average performance of 65%-a 25-point drop from single-turn performances of 90% when they receive the entire instruction at the beginning of the conversation.'}
- {'setting': 'FULL vs SHARDED', 'metric': 'Unreliability', 'value': '112% increase (more than doubling)'}
- {'setting': 'RECAP vs SNOWBALL', 'metric': 'Performance improvement over SHARDED simulations', 'value': 'SNOWBALL gives a sense of realistic performance gains achievable through user-turn repetition: it can mitigate the FULL-to-SHARDED performance deterioration by 15-20%'}

### Análisis de Limitaciones
- {'description': 'Reliance on fully automated simulation', 'impact': 'Simulations are not representative of natural human-AI conversation'}
- {'description': 'Focus on analytical tasks', 'impact': 'Does not establish whether models get lost in conversation on more open-ended tasks, such as creative writing'}
- {'description': 'Text-only tasks in the English language', 'impact': 'Establishing whether models get lost in conversation in other languages or in tasks involving multiple modalities is needed'}

### Impacto Social (Broader Impacts)
- {'impact': 'Ubiquitous performance degradation over multi-turn interactions is likely a reason for low uptake of AI systems [73, 4, 28], particularly with novice users who are less skilled at providing complete, detailed instructions from the onset of conversation [87, 35].', 'recommendations': ['If time allows, try again', 'Consolidate before retrying']}

### Declaración de uso de LLMs
- Today's large language models (LLMs) function as conversational interfaces ( e.g. , ChatGPT, Gemini, Claude), enabling users to interact with the LLM through multiple conversation turns.

---

## 🧠 Razonamiento de Consolidación (CoT)

> {'section_6_2': 'Identified metrics A and U for aptitude and unreliability analysis. Extracted results from Table 1 on performance degradation (P). Noted the relationship between model aptitude and reliability in single-turn settings. Documented the findings of the sharded setting, including the average drop in aptitude and increase in unreliability.'}
> {'section_6_3': 'Extracted details on the gradual sharding experiment setup and results. Identified the performance degradation observed with two-shard instructions and beyond. Noted the limitations of the sharded setting as a realistic representation of user interactions.'}
> {'section_7': 'Summarized implications for system and agent builders, LLM builders, NLP practitioners, and users of conversational systems. Extracted experimental results from Tables 2, 3, and 4 on various simulation types and models. Documented the recommendations for improving reliability in multi-turn settings.'}
> {'section_8': 'Summarized key findings and called out limitations of the work. Noted the need for future research to address the limitations identified.'}

### 📍 Secciones Identificadas del Paper
- `## LLMS GET LOST IN MULTI-TURN CONVERSATION`
- `## ABSTRACT`
- `## 1 Introduction`
- `## 2 Background and Related Work`
- `## 3 Simulating Underspecified, Multi-Turn Conversation`
- `## 4 Task and Metric Selection`
- `## 5 Simulation Scale and Parameters`
- `## Lost in Conversation Experiment`
- `6.2 Aptitude vs. Reliability Analysis`
- `6.3 Gradual Sharding Experiment`
- `7 Implications`
- `8 Conclusion`
- `9 Limitations`
- `References`

---
_Informe generado automáticamente empleando el modelo local: qwen2.5_
