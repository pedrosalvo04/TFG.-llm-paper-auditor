# Paper 2: Phi-3 technical report


**Ítem 1. Claims**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper's claims in the abstract and introduction are supported by the experimental results. For instance, the claim that 'phi-3-mini model achieves similar level of language understanding and reasoning ability as much larger models' is backed by Table 2 which shows comparable performance on various benchmarks (e.g., MMLU, MT-bench). Additionally, the claim about phi-3-mini being capable of running locally on a modern phone while achieving quality on par with larger models like Mixtral 8x7B and GPT-3.5 is supported by the hardware details in Section 6 Weakness, which mentions that 'phi-3-mini can be quantized to 4-bits, occupying ≈ 1.8GB of memory' and can run on a modern phone like iPhone 14 with A16 Bionic chip."
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta conecta correctamente la promesa inicial de igualar a modelos más grandes en dispositivos móviles con las tablas de resultados (Tabla 2) y la sección de hardware, extrayendo la cita literal "phi-3-mini can be quantized to 4-bits, occupying ≈ 1.8GB of memory".

**Ítem 2. Limitations**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper explicitly mentions limitations in the 'Weakness' section, such as the model's limited factual knowledge and its restricted language to English. For example, it states that 'the model simply does not have the capacity to store too much 'factual knowledge', which can be seen for example with low performance on TriviaQA.' Additionally, there is a discussion about the need for augmentation with a search engine to address certain limitations."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Localiza la sección específica llamada "Weakness" y extrae correctamente la limitación sobre la retención de datos fácticos, citando textualmente la frase sobre la falta de capacidad para almacenar "factual knowledge".

**Ítem 3. Theory, Assumptions & Proofs**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper does not contain any theoretical results, proofs, or assumptions related to the Phi-3.5-Vision model's architecture, training process, or performance benchmarks. The technical specifications and experimental results are described in detail, but there is no mention of theoretical foundations or mathematical proofs that would require explicit statement of assumptions. Therefore, this item does not apply as per the NeurIPS 2026 criteria."
- **Mi Valoración:** Correcto
- **Mi Justificación:** El dictamen de N/A es adecuado porque reconoce que el documento es un reporte técnico puramente empírico y descriptivo sobre el entrenamiento del modelo Phi-3, sin postulados teóricos ni demostraciones algebraicas que deban verificarse.

**Ítem 4. Experimental Result Reproducibility**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper lacks any information about making experimental results reproducible. Specifically, there are no URLs or instructions provided for accessing the authors' own original code, model weights, or newly collected datasets used for the main experiments. The only hardware details mentioned pertain to the device type and quantization levels but do not address the reproducibility of the results. This omission poses a transparency risk as it makes it difficult for other researchers to verify or replicate the findings."
- **Mi Valoración:** Correcto
- **Mi Justificación:** La herramienta acierta al marcar "No" al detectar que el texto del reporte técnico original en PDF no incluye enlaces directos ni URL al código de implementación o a los pesos del modelo para reproducir la experimentación.

**Ítem 5. Open Access to Data and Code**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any URLs or instructions that grant access to the authors' own original code, model weights, or newly collected datasets used for the main experiments. The relevant sections of the paper mention the use of publicly available web data and synthetic data, but do not provide any details on how these were obtained or processed by the authors themselves. Additionally, there is no indication that the authors have released their own implementation of the model or the training code. This omission poses a transparency risk as it prevents other researchers from reproducing the experiments and verifying the results."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Sigue la misma línea del ítem 4, sancionando correctamente la ausencia de repositorios de datos y código de entrenamiento abiertos. Microsoft no hace públicos los scripts ni el corpus sintético privado utilizado.

**Ítem 6. Experimental Setting / Details**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "Architecture The Phi-3.5-Vision (4.2B parameters) is a multimodal model designed to process an image/multi-image and a textual prompt as inputs, and subsequently generate textual outputs. This model is composed of two primary components: an image encoder, i.e., CLIP ViT-L/14 [RKH + 21] and a transformer decoder, i.e., phi-3.5-mini. The visual tokens, once extracted by the image encoder, are then combined with text tokens in an interleaved way (no particular order for image and text tokens). To accommodate high-resolution images and various aspect ratios, a dynamic cropping strategy [DZZ + 24b] is utilized to split the input image into a 2d array of blocks, where the tokens of the blocks are concatenated to represent the whole image. For multi-image input, we simply concatenated tokens from each images together."
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Evalúa con "Sí" y extrae datos arquitectónicos reales (codificador de imagen CLIP ViT-L/14, estrategia de recorte dinámico). Sin embargo, la justificación omite resumir el razonamiento y se limita a copiar y pegar un gran bloque de texto directamente del paper, denotando una falta de síntesis en su cadena de pensamiento (CoT).

**Ítem 7. Experiment Statistical Significance**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any information about error bars, confidence intervals, or statistical significance tests. The statistics section only reports benchmark results such as MMLU and MT-bench scores without any indication of the variability or uncertainty associated with these results. This lack of statistical measures means that it is impossible to assess the reliability and robustness of the reported performance. According to the official criteria, this constitutes a transparency risk because readers cannot determine whether the observed differences in performance are statistically significant. <br><br> ⚠️ Falta justificación explícita del autor para la respuesta 'No'"
- **Mi Valoración:** Correcto
- **Mi Justificación:** Penaliza adecuadamente que los autores se limitan a mostrar estimaciones puntuales planas en los benchmarks (como MMLU) sin reportar la varianza de los datos o pruebas de significancia, constatando además que el artículo no da motivos para esta omisión.

**Ítem 8. Experiments Compute Resource**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper mentions hardware details such as 'Modern phone (for phi-3-mini)', 'iPhone 14 with A16 Bionic chip', and quantization levels like 'phi-3-mini can be quantized to 4-bits, occupying ≈ 1.8GB of memory'. These details provide sufficient information about the compute resources used for the experiments."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso positivo por confusión de conceptos. Qwen da por válida la descripción del hardware utilizado para hacer inferencia en teléfonos móviles, pero ignora que las normas de NeurIPS exigen transparentar los recursos computacionales masivos, infraestructura y tiempo total empleados para entrenar el modelo original, algo que el artículo oculta.

**Ítem 9. Code of Ethics**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper discusses the safety and security measures taken during the development of Phi-3-mini, including red-teaming processes and automated testing. Specifically, it states: 'Phi-3-mini was developed in accordance with Microsoft's responsible AI principles. The overall approach consisted of safety alignment in post-training, red-teaming, automated testing and evaluations across dozens of RAI harm categories.' This demonstrates that the authors have considered potential harms and taken steps to mitigate them."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Acepta que la discusión explícita sobre los principios de IA responsable de Microsoft y las auditorías internas de red-teaming cubren el cumplimiento ético material del trabajo.

**Ítem 10. Broader Impacts**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper focuses on technical specifications, benchmarks, and safety measures of the Phi-3-mini model. There is no discussion of potential negative societal impacts or broader implications of the work beyond its technical capabilities. Given that this appears to be a foundational research paper without direct application to specific societal issues, it does not require a dedicated discussion of broader impacts."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Error de evaluación de riesgo. La IA ignora que el artículo tiene una sección discutiendo alucinaciones, toxicidad y sesgos del modelo en la Sección 6. Al ser un modelo generativo capaz de producir lenguaje tóxico de forma autónoma, tiene un riesgo directo de uso social negativo, por lo que el dictamen correcto debió ser "Yes" o "No", pero nunca "N/A".

**Ítem 11. Safeguards**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper states, 'Phi-3-mini was developed in accordance with Microsoft's responsible AI principles. The overall approach consisted of safety alignment in post-training, red-teaming, automated testing and evaluations across dozens of RAI harm categories.' This indicates that the model has been subjected to rigorous safety checks and evaluations designed to mitigate risks associated with misuse."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Fallo conceptual sistémico. Vuelve a confundir la alineación de seguridad interna y el red-teaming de los pesos con las salvaguardas de despliegue. Las salvaguardas implican restricciones de acceso o filtros coercitivos para el usuario. Un modelo ideado para descargarse y correr en un dispositivo local de forma aislada carece intrínsecamente de controles sobre quién lo usa o para qué.

**Ítem 12. Licenses**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not provide any specific information about the licensing terms for the model or its components. While it mentions that the code is released under the MIT license, there is no explicit statement regarding the usage guidelines or restrictions for the model itself. Given that the model has a high risk of misuse due to its capabilities in generating harmful content (as evidenced by the RAI harm categories), the lack of clear licensing terms and usage guidelines constitutes a transparency risk."
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** El veredicto denegatorio es acertado en la práctica, porque el documento PDF no especifica textualmente la licencia del modelo. Sin embargo, la justificación contiene una alucinación fáctica cuando afirma: "While it mentions that the code is released under the MIT license". La palabra MIT no aparece en ninguna parte del manuscrito original; el modelo inventó ese dato.

**Ítem 13. Assets**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper does not mention the creation or release of any new datasets, model weights, benchmarks, or software libraries as part of this work. The assets mentioned (training dataset and additional data) are described as existing publicly available resources that have been filtered and used for training. Therefore, since no new assets are being released, Item 13 does not apply."
- **Mi Valoración:** Incorrecto
- **Mi Justificación:** Falso negativo. La herramienta afirma que no se liberan nuevos activos, ignorando que el documento entero es el lanzamiento técnico ("Technical Report") y presentación de la familia de modelos "Phi-3". Este es un nuevo activo computacional masivo que debió documentarse con tarjetas estructuradas (Model Cards).

**Ítem 14. Crowdsourcing & Human Subjects**
- **Valoración Auditor:** No
- **Justificación Auditor:** "The paper does not mention any hiring or compensation of human workers to collect or label new data. The training dataset is described as a scaled-up version of the one used for phi-2, composed of heavily filtered publicly available web data and synthetic data. There is no indication that the authors conducted any new research involving human subjects or paid any workers. Therefore, Item 14 does not apply. <br><br> ⚠️ Falta justificación explícita del autor para la respuesta 'No'"
- **Mi Valoración:** Medianamente correcto
- **Mi Justificación:** Argumenta correctamente basándose en el texto que los datos provienen de la web y de fuentes sintéticas sin contratar nuevos anotadores humanos. No obstante, al determinar que esta práctica no aplica a la investigación ("Item 14 does not apply"), el veredicto forzado del LLM debería haber sido "N/A" en lugar de penalizar la checklist con un "No".

**Ítem 15. IRB Approvals**
- **Valoración Auditor:** N/A
- **Justificación Auditor:** "The paper does not involve any direct research with human subjects. It focuses on the technical specifications and performance of a language model, phi-3, which is based on publicly available data and synthetic data generated by LLMs. The use of such models for generating training data or benchmarks does not constitute new human experiments that would require IRB approval. Therefore, N/A is applicable as per the official criteria."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Dictamina acertadamente que entrenar un modelo con datos sintéticos y filtrados de la web no constituye un ensayo o experimentación directa con humanos que requiera la autorización formal de una junta de revisión institucional (IRB).

**Ítem 16. Declaration of LLM Usage**
- **Valoración Auditor:** Yes
- **Justificación Auditor:** "The paper states: 'A scaled-up version of the one used for phi-2, composed of heavily filtered publicly available web data and synthetic data.' This indicates that LLMs were used to generate synthetic data as part of the training process. Synthetic data generation is an important component of the core methods in this research."
- **Mi Valoración:** Correcto
- **Mi Justificación:** Identifica la alta dependencia metodológica en la generación de datos sintéticos, detectando que Phi-3 se entrenó basándose en texto creado por otros modelos y citando de forma precisa "synthetic LLM-generated data".