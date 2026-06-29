# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `paper cientifico 12 (llm) LiveCodeBench.pdf` |
| 📅 **Fecha de Análisis** | 2026-06-28 13:44:52 |
| 🤖 **Modelo Local** | `qwen2.5` |
| ⏳ **Tiempo de Ejecución** | 1960.89s |
| 📊 **Caracteres Analizados** | 112,564 |

### 🎯 Veredicto del Checklist
> **⚠️ ATENCIÓN REQUERIDA**
> Se han detectado **2 de 16** ítem(s) que requieren atención o justificación adicional.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 7
- **No Cumple (No):** 5
- **No Aplica (N/A):** 4
- **Ítems con Alerta:** 2

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🟢 Yes | The paper's claims in the abstract and introduction accurately reflect the paper's contributions and scope. The authors state that LiveCodeBench is a holistic and contamination-free benchmark for evaluating code capabilities, which aligns with their empirical findings presented in the results section (Section 5). Specifically, they claim to address issues of data contamination by using live updates and time-segmented evaluations, as evidenced by Figure 1. The paper also claims that current benchmarks like HumanEval may be subject to overfitting due to insufficient tests and ambiguous problem descriptions, which is supported by their findings in Section 5 (e.g., Figure 5). |
| 2 | Limitations | 🟢 Yes | The paper explicitly includes a 'Limitations' section (Section 7) that discusses several limitations, including benchmark size, focus on Python, robustness to prompts, and problem domain. For example, the authors mention that LiveCodeBench currently only focuses on Python, which might not provide enough signal about model capabilities in other languages (Section 7). |
| 3 | Theory, Assumptions & Proofs | 🔵 N/A | The paper does not contain any theoretical results, proofs, or assumptions. The focus of the work is on empirical evaluation and benchmarking of large language models for code generation tasks. Since there are no theoretical contributions in this paper, the criteria related to theory, assumptions, and proofs do not apply. This is consistent with the official NeurIPS 2026 criteria which state that items should be evaluated only if relevant. |
| 4 | Experimental Result Reproducibility | 🔴 No | The paper does not provide any code or model URLs, and the authors have not made their own implementation or data publicly accessible. The only information provided is that the dataset was scraped from public websites (LeetCode, AtCoder, CodeForces) under certain conditions. However, this does not meet the requirement for making experimental results reproducible as stated in the NeurIPS 2026 criteria. Specifically, the authors should have either released their own code or provided detailed instructions on how to replicate the experiments. |
| 5 | Open Access to Data and Code | 🔴 No | The paper does not provide any URLs or instructions for accessing the authors' own original code, model weights, or newly collected datasets used for the main experiments. The experimental setup section mentions evaluating various models across different sizes and classes, but it does not include links to the authors' repositories or detailed instructions on how to access their data and code. This omission poses a transparency risk as it makes it difficult for other researchers to reproduce the results. While the paper cites third-party dependencies such as LeetCode, AtCoder, and CodeForces for problem sources, these are insufficient to meet the criteria for open access to data and code. |
| 6 | Experimental Setting / Details | 🟢 Yes | We describe the experimental setup in this section. First, we provide the common setup across the scenarios, followed by the scenario-specific setups in Section 4.1.  Models. We evaluate 52 models across various sizes, ranging from 1 . 3B to 70B, including base models, instruction models, and both open and closed models. Our experiments include models from different classes, such as GPTs ( GPT-3.5-turbo , GPT-4 , GPT-4-Turbo , GPT-4-O ), Claudes ( Claude-Ins-1 , Claude-2 , Claude-3s ), Geminis ( Gemini-Pro , Gemini-Flash ), Mistral among closedaccess and LLaMa-3s ( L3-Base-{ 7, 70 } B , L3-Ins-{ 7, 70 } B ), DeepSeeks ( DS-Base-{ 1.3, 6.7, 33 } B , DS-Ins-{ 1.3, 6.7, 33 } B ), CodeLLaMas ( CL-Ins-{ 7, 13, 34 } B , CL-Base-{ 7, 13, 34 } B ), StarCoder2 ( SC2-Base-{ 3,7,15 } B ), CodeQwen among open. Additionally, we also include fine-tuned models Phind-34B from CL-Base-34B , and MagiCoders ( MC-{ 6.7, 7 } B ) from CL-Base-7B and DS-Base6.7B . See Appendix C.1 for a complete list of models and estimated cutoff dates.  Evaluation Metrics. We use the Pass@ 1 (Kulal et al., 2019; Chen et al., 2021) metric for our evaluations. Specifically, we generate 10 candidate answers for each problem either using API or using vLLM (Kwon et al., 2023). We use nucleus sampling with temperature 0 . 2 and top p 0 . 95 and calculate the fraction of programs or answers that are correct. For the code generation and self-repair scenarios, we use tests to verify the correctness of the programs. For these scenarios, programs must pass all tests to be considered correct. For the code execution scenario, we use an execution-based correctness metric between the generated output and the ground truth output. For the test output prediction scenario, we parse the generated response to extract the answer and use equivalence checks for grading as specified in Section 2. |
| 7 | Experiment Statistical Significance | 🔴 No | The paper does not provide any error bars, confidence intervals, or statistical significance tests for the experiments. The results are reported as averages without any indication of variability or uncertainty. This lack of statistical measures makes it difficult to assess the robustness and reliability of the experimental findings. According to the official criteria, this is a requirement for reporting experiment results in NeurIPS 2026. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 8 | Experiments Compute Resource | 🔴 No | The paper does not provide any information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments. While it mentions the models evaluated and some evaluation metrics, there is no detail provided about the hardware or computational requirements for running these experiments. This omission makes it challenging for other researchers to replicate the results, which is a critical aspect of scientific transparency in machine learning research. |
| 9 | Code of Ethics | 🟢 Yes | The paper does not explicitly mention an 'Ethics Statement' or a dedicated section on broader impacts. However, the authors have demonstrated awareness of ethical considerations by addressing potential harms and limitations in their work. Specifically, they discuss issues such as problem set contamination, overfitting to existing benchmarks, and the need for more comprehensive evaluation scenarios (e.g., different programming languages, real-world usage). These discussions align with the NeurIPS Code of Ethics, particularly under 'Societal Impact and Potential Harmful Consequences' and 'Impact Mitigation Measures'. The authors have shown a commitment to transparency and ethical research practices by acknowledging these limitations and proposing solutions. |
| 10 | Broader Impacts | 🟢 Yes | The paper discusses potential negative societal impacts, such as overfitting to existing benchmarks (which could lead to misuse) and the need for more comprehensive evaluation scenarios. The authors also highlight the importance of evaluating LLMs on a broader range of capabilities beyond just code generation, which is crucial for understanding their real-world applicability and limitations. |
| 11 | Safeguards | 🔵 N/A | The paper focuses on the evaluation of large language models for code generation and does not involve releasing a model with high risk for misuse. The work is primarily theoretical and foundational, aiming to evaluate LLMs across various scenarios such as code generation, self-repair, and test case output prediction. Given that the primary objective is academic research rather than practical deployment, there is no need for explicit access restrictions or usage guidelines. Therefore, answering 'N/A' aligns with the official criteria which state that safeguards are not required for theoretical or low-risk work. |
| 12 | Licenses | 🟢 Yes | The paper states: 'We scrape only the problem statements, ground-truth solutions, and test cases from competition websites LeetCode , AtCoder , and CodeForces . Further, we only scrape publicly visible portions of websites, avoiding any data collection that might be paywalled or require login or interaction with the website. Following, Hendrycks et al. (2021) we abide by Fair Use § 107: 'the fair use of a copyrighted work, including such use by ... scholarship, or research, is not an infringement of copyright', where fair use is determined by 'the purpose and character of the use, including whether such use is of a commercial nature or is for nonprofit educational purposes', 'the amount and substantiality of the portion used in relation to the copyrighted work as a whole', and 'the effect of the use upon the potential market for or value of the copyrighted work.' Finally, we use the collected problems for academic purposes only and in addition, do not train on the collected problems.' |
| 13 | Assets | 🔵 N/A | The paper does not appear to introduce any new datasets, models, benchmarks, or software libraries. The assets mentioned (problems collected from LeetCode, AtCoder, and CodeForces) are reusing existing public resources without creating new ones. Therefore, this item is N/A as per the official criteria. |
| 14 | Crowdsourcing & Human Subjects | 🔴 No | The paper does not mention hiring or compensating human workers to collect or label new data. The datasets used are scraped from publicly available websites, and no new human-derived data was created for this research. Hence, the authors did not engage in crowdsourcing activities as defined by the NeurIPS criteria. <br><br> ⚠️ *Falta justificación explícita del autor para la respuesta 'No'* |
| 15 | IRB Approvals | 🔵 N/A | The paper does not involve any direct research with human subjects. It primarily focuses on evaluating large language models (LLMs) using curated code problems from public platforms such as LeetCode, AtCoder, and CodeForces. The data used is publicly available and scraped for academic purposes only, adhering to the Fair Use guidelines. Therefore, no new IRB approval is required according to NeurIPS 2026 criteria. |
| 16 | Declaration of LLM Usage | 🟢 Yes | The paper extensively uses LLMs as a core component of the methodology, particularly in generating synthetic code problems and self-repair scenarios. For instance, the paper mentions 'self-repair' as one of the key evaluation scenarios (see context mapping). This indicates that LLMs are not merely used for writing or editing but are integral to the research methods. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Arquitectura del Modelo
- **Gating:** ['Gated Attention']

### Dataset & Datos
- **Total Problems Collected:** 511
- **Platforms:** ['LeetCode', 'AtCoder', 'CodeForces']
- **Problem Difficulty Distribution:** [{'platform': 'LCB (May-end)', 'easy': 182, 'medium': 206, 'hard': 123}, {'platform': 'LCB (Sep-end)', 'easy': 125, 'medium': 136, 'hard': 88}]
- **Test Cases Per Problem:** {'average': 17, 'LCB (May-end)': 17, 'LCB (Sep-end)': 18}
- **Problem Sources:** [{'platform': 'AtCoder', 'easy': 99, 'medium': 91, 'hard': 77}, {'platform': 'LeetCode', 'easy': 79, 'medium': 113, 'hard': 43}, {'platform': 'CodeForces', 'easy': 4, 'medium': 2, 'hard': 3}]
- **Scenario Specific Datasets:** [{'name': 'Code Generation and Self-Repair', 'total_instances': 511, 'platforms': ['LeetCode', 'AtCoder', 'CodeForces']}, {'name': 'Code Execution', 'total_samples': 479, 'problems': 85}, {'name': 'Test Case Output Prediction', 'total_instances': 442, 'problems': 181}]

### Estadística & Rigor Científico
- {'platform': 'LCB (May-end)', 'easy': 182, 'medium': 206, 'hard': 123}
- {'platform': 'LCB (Sep-end)', 'easy': 125, 'medium': 136, 'hard': 88}

### Comparativa con Baselines
- {'benchmark': 'HumanEval', 'finding': 'Models cluster into two groups: ones that perform well on both benchmarks and others that perform well on HumanEval but not on LiveCodeBench'}
- {'benchmark': 'LiveCodeBench vs. HumanEval', 'finding': 'The latter group primarily comprises fine-tuned open-access models while the former group comprises base models and closed models, indicating potential overfitting to HumanEval'}

### Análisis de Limitaciones
- {'platform': 'CodeForces', 'difficulty': 'problems are harder than AtCoder and LeetCode problems'}
- {'platform': 'LeetCode', 'starter_code': 'starter code is provided for each problem in the STDIN format'}

### Licencias detectadas
- {'license_type': 'NOT FOUND', 'description': "We scrape only the problem statements, ground-truth solutions, and test cases from competition websites LeetCode , AtCoder , and CodeForces . Further, we only scrape publicly visible portions of websites, avoiding any data collection that might be paywalled or require login or interaction with the website. Following, Hendrycks et al. (2021) we abide by Fair Use § 107: 'the fair use of a copyrighted work, including such use by ... scholarship, or research, is not an infringement of copyright', where fair use is determined by 'the purpose and character of the use, including whether such use is of a commercial nature or is for nonprofit educational purposes', 'the amount and substantiality of the portion used in relation to the copyrighted work as a whole', and 'the effect of the use upon the potential market for or value of the copyrighted work.' Finally, we use the collected problems for academic purposes only and in addition, do not train on the collected problems."}

### Impacto Social (Broader Impacts)
- Evaluating LLMs on a broader range of capabilities beyond just code generation
- Highlighting potential contamination and overfitting issues in existing benchmarks
- Improving the quality, maintainability, and reliability of generated code through holistic evaluation

---

## 🧠 Razonamiento de Consolidación (CoT)

> Identified specific architectural components such as 'self-repair', 'code execution', and 'test output prediction' scenarios.
> Captured ALL hyperparameters even if they seem minor (betas, epsilon, warmup steps, weight decay, training_steps, iterations).
> Noted specific benchmarks and their corresponding results if present in tables or text.
> Documented the context mapping to sections within this fragment for clarity.

### 📍 Secciones Identificadas del Paper
- `Introduction`
- `1 Introduction`
- `2 Holistic Evaluation`
- `3 Benchmark Curation`
- `## 4 Experiment Setup`
- `## 5 Results`
- `## 6 Related Work`

---
_Informe generado automáticamente empleando el modelo local: qwen2.5_
