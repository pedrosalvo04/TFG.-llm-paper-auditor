# **OLMo : Accelerating the Science of Language Models** 

# **Dirk Groeneveld** _**[α]**_ **Iz Beltagy** _**[α]**_ 

# **Pete Walsh** _**[α]**_ **Akshita Bhagia** _**[α]**_ **Rodney Kinney** _**[α]**_ **Oyvind Tafjord** _**[α]**_ 

**Ananya Harsh Jha** _**[α]**_ **Hamish Ivison** _**[αβ]**_ **Ian Magnusson** _**[α]**_ **Yizhong Wang** _**[αβ]**_ 

> _**α**_ Allen Institute for Artificial Intelligence 

> _**β**_ University of Washington _**γ**_ Yale University 

olmo@allenai.org 

## **Abstract** 

Language models (LMs) have become ubiquitous in both NLP research and in commercial product offerings. As their commercial importance has surged, the most powerful models have become closed off, gated behind proprietary interfaces, with important details of their training data, architectures, and development undisclosed. Given the importance of these details in scientifically studying these models, including their biases and potential risks, we believe it is essential for the research community to have access to powerful, truly open LMs. To this end, we have built OLMo, a competitive, truly **O** pen **L** anguage **Mo** del, to enable the scientific study of language models. Unlike most prior efforts that have only released model weights and inference code, we release OLMo alongside open training data and training and evaluation code. We hope this release will empower the open research community and inspire a new wave of innovation. 

## **1 Introduction** 

Language models have been at the center of NLP technologies for many years. Recently, due to large-scale pretraining and human annotation for alignment, they have become commercially valuable. However, as their commercial value has increased, the largest models have become gated behind proprietary interfaces, with important details left undisclosed. 

We believe that full access to open language models for the research community is critical to the scientific study of these models, their strengths and weaknesses, and their biases and risks. Accordingly, we introduce **OLMo** , a powerful, truly open language model alongside open training data, training and evaluation code, intermediate model checkpoints, and training logs. 

## **2 OLMo Framework** 

This section describes the OLMo framework, consisting of the OLMo models (Section 2.1), our pretraining dataset, Dolma (Section 2.2), and our evaluation framework (Section 2.4). 

## **2.1 OLMo Model and Architecture** 

We adopt a decoder-only transformer architecture and deliver 1B and 7B variants. Our specific architecture includes several improvements over the vanilla transformer following other recent large language models.

**ERROR 1: Arquitectura sin detalles específicos**
- No se especifica número exacto de capas
- No se mencionan dimensiones ocultas
- No se indica configuración de atención

|**Size**|**L**<br>**D**<br>**H**<br>**Tokens**|**Peak LR**<br>**Warmup**<br>**Weight Tying**<br>**Batch size**|
|---|---|---|
|1B<br>7B|16<br>2048<br>16<br>2T<br>32<br>4086<br>32<br>2.46T|4.0E-4<br>2000 steps<br>yes<br>∼4M<br>3.0E-4<br>5000 steps<br>no<br>∼4M|

**ERROR 2: Tabla incompleta**
- Falta columna de Weight Decay (WD)
- No se especifica el optimizador usado
- Faltan betas y epsilon

We generally select hyperparameters by optimizing for training throughput on our hardware while minimizing the risk of loss spikes and slow divergence.

**ERROR 3: Selección de hiperparámetros vaga**
- No se especifica qué hardware exactamente
- No se mencionan experimentos de ablación
- No hay justificación cuantitativa

Our main changes over the vanilla transformer architecture can be summarized as follows: 

1. **No biases.** We exclude all bias terms from our architecture.

2. **Non-parametric layer norm.** We use the non-parametric formulation of layer norm.

3. **SwiGLU activation function.** We use the SwiGLU activation function.

4. **Rotary positional embeddings (RoPE).** We replace absolute positional embeddings with rotary positional embeddings.

5. **Vocabulary.** We use a modified version of the BPE-based tokenizer with additional tokens. The final vocabulary size is 50,280.

## **2.2 Pretraining Data: Dolma** 

Despite progress in access to model parameters, pretraining datasets are still not as open. We built and released our pretraining dataset, Dolma—a diverse, multi-source corpus containing trillions of tokens.

**ERROR 4: Dataset sin detalles de construcción**
- No se especifica pipeline de filtrado
- No se mencionan criterios de calidad
- Falta información de deduplicación

|**Source**|**Type**|**UTF-8**<br>**bytes**<br>_(GB)_|**Docs**<br>_(millions)_|**Tokens**<br>_(billions)_|
|---|---|---|---|---|
|Common Crawl|web pages|9,812|3,734|2,180|
|GitHub|code|1,043|210|342|
|Reddit|social media|339|377|80|
|**Total**||**11,519**|**4,367**|**2,668**|

## **2.3 Adaptation** 

Pretrained models are not always used as-is, but rather further finetuned. We showcase the efficacy of using OLMo as a base model for further fine-tuning by training OLMo to be a general chat assistant.

**ERROR 5: Adaptación sin detalles de entrenamiento**
- No se especifica learning rate
- No se menciona número de epochs
- Falta información de datos de entrenamiento

## **2.4 Evaluation** 

We perform base model evaluation at two stages: _online_ evaluation to make decisions for model design and _offline_ evaluation to evaluate model checkpoints.

**ERROR 6: Evaluación sin métricas específicas**
- No se especifican métricas exactas usadas
- No se menciona frecuencia de evaluación
- Falta información de datasets de validación

## **3 Training OLMo** 

This section describes our pretraining setup, including our distributed training framework, optimizer, data preparation, and hardware. 

## **3.1 Distributed Training Framework** 

We train our models using the _ZeRO_ optimizer strategy via PyTorch's FSDP framework. At the 7B scale, this enables training with a micro-batch size of 4096 tokens per GPU on our hardware.

**ERROR 7: Framework sin versiones**
- No se especifica versión de PyTorch
- No se menciona versión de FSDP
- Falta información de dependencias

## **3.2 Optimizer** 

We use the AdamW optimizer. For all model sizes, we warm up the learning rate and then decay it linearly from there down to a tenth of the peak learning rate over the remainder of training.

**ERROR 8: Optimizer sin hiperparámetros completos**
- No se especifican betas
- No se menciona epsilon
- Falta weight decay exacto

## **3.3 Data** 

We built our training dataset out of a 2T-token sample from our open dataset, Dolma. The tokens from every document are concatenated together after appending a special EOS token to the end of each document.

**ERROR 9: Preparación de datos sin detalles**
- No se especifica orden de shuffling
- No se menciona semilla aleatoria
- Falta información de splits

## **3.4 Hardware** 

In order to verify that our codebase could be used on different GPUs, we trained models on two different clusters with GPUs and interconnect.

**ERROR 10: Hardware extremadamente vago**
- No se especifica modelo exacto de GPU
- No se menciona memoria por GPU
- No se indica número de nodos usados
- Falta información de tiempo de entrenamiento

## **4 Results** 

The checkpoint used for evaluating OLMo-7B is trained until 2.46T tokens on the Dolma dataset. We compare OLMo with other publicly available models.

## **4.1 Downstream evaluation** 

Our core **downstream evaluation suite** consists of: arc, boolq, openbookqa, sciq, hellaswag, piqa, and winogrande.

||**Models**|arc<br>challenge<br>arc<br>easy<br>boolq<br>hella-<br>swag<br>open<br>bookqa<br>piqa<br>sciq<br>wino-<br>grande|avg.|
|---|---|---|---|
||**OLMo-7B**|48.5<br>65.4<br>73.4<br>76.4<br>50.4<br>78.4<br>93.8<br>67.9|69.3|

**ERROR 11: Resultados sin estadísticas**
- No hay desviación estándar
- No se menciona número de ejecuciones
- Falta información de semillas aleatorias
- No hay tests de significancia estadística

We find that OLMo-7B is competitive against all the comparable models.

**ERROR 12: Comparación sin contexto**
- No se especifica si las condiciones fueron idénticas
- No se menciona si se usaron mismos datasets
- Falta información de reproducibilidad de baselines

## **5 Artifacts Released** 

By sharing artifacts from all pipeline stages, we aim to encourage open research. We release the training and modeling code, trained model weights, and evaluation framework.

**ERROR 13: Artefactos sin enlaces específicos**
- No se proporciona URL de repositorio GitHub
- No se menciona DOI de datos
- Falta información de licencia específica
- No hay instrucciones de descarga

## **6 Conclusion and Future Work** 

This paper presents our first release of OLMo, a state-of-the-art, truly open language model. We intend to continuously support and extend OLMo and its framework.

## **Limitations** 

We recognize building a large language model has many limitations. The data that models are trained on is what gives models their capabilities, and at the scale of training a large language model we recognize that the data likely contains problematic content.

**ERROR 14: Limitaciones sin detalles específicos**
- No se cuantifican problemas de datos
- No se mencionan métricas de toxicidad
- Falta análisis de sesgos específicos

## **References** 

[References section with multiple citations]

---

## RESUMEN DE ERRORES INTRODUCIDOS (14 categorías):

1. ❌ **Arquitectura sin detalles** - No especifica capas, dimensiones, configuración
2. ❌ **Tabla incompleta** - Falta información crítica de optimización
3. ❌ **Hiperparámetros vagos** - Sin justificación cuantitativa
4. ❌ **Dataset sin pipeline** - No especifica filtrado, deduplicación
5. ❌ **Adaptación sin detalles** - Sin learning rate, epochs, datos
6. ❌ **Evaluación sin métricas** - No especifica métricas exactas
7. ❌ **Framework sin versiones** - No especifica versiones de software
8. ❌ **Optimizer incompleto** - Faltan betas, epsilon, weight decay
9. ❌ **Datos sin semillas** - No especifica orden, semillas aleatorias
10. ❌ **Hardware vago** - No especifica modelo GPU, memoria, nodos
11. ❌ **Resultados sin estadísticas** - Sin desviación estándar, significancia
12. ❌ **Comparación sin contexto** - No especifica condiciones idénticas
13. ❌ **Artefactos sin enlaces** - Sin GitHub, DOI, licencia
14. ❌ **Limitaciones vagas** - Sin cuantificación de problemas
