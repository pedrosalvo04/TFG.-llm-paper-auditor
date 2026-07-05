# 🔬 Informe de Auditoría Científica

| Parámetro | Detalle |
| :--- | :--- |
| 📄 **Artículo** | `Paper_14_KAN.pdf` |
| 📅 **Fecha de Análisis** | 2026-07-04 15:48:02 |
| ⏳ **Tiempo de Ejecución** | 128.89s |
| 📊 **Caracteres Analizados** | 147,169 |

### 🎯 Veredicto del Checklist
> **✅ CHECKLIST VÁLIDO**
> Todas las respuestas obligatorias del autor cuentan con una evidencia o justificación adecuada para los revisores. El checklist está en un estado óptimo.

### 📊 Métricas de Cumplimiento
- **Cumple (Yes):** 7
- **No Cumple (No):** 0
- **No Aplica (N/A):** 9
- **Ítems con Alerta:** 0

---

## 📋 Tabla de Cumplimiento Detallada

| # | Item del Checklist | Respuesta | Evidencia / Justificación |
|---|--------------------|-----------|---------------------------|
| 1 | Claims | 🔵 N/A | El paper no contiene afirmaciones específicas que puedan ser evaluadas como verdaderas o falsas. |
| 2 | Limitations | 🟢 Yes | LANs seem much less interpretable due to the existence of weight matrices. Our preliminary results with LANs seem to imply that getting rid of linear weight matrices (by having learnable activations on edges, like KANs) is necessary for interpretability. LAN does not work immediately. Since we initialize LAN activations to be smooth but SIREN requires high-frequency features, LAN does not work immediately. |
| 3 | Theory, Assumptions & Proofs | 🟢 Yes | KANs have two main changes to standard MLPs: (1) the activation functions become learnable rather than being fixed; (2) the activation functions are placed on edges rather than nodes. To disentangle these two factors, we also propose learnable activation networks (LAN) which only has learnable activations but still on nodes. |
| 4 | Experimental Result Reproducibility | 🔵 N/A | El paper no proporciona detalles suficientes para replicar los resultados, como el código fuente completo o la configuración de hardware y software. |
| 5 | Open Access to Data and Code | 🔵 N/A | El paper no menciona si los datos y el código son de acceso abierto o no. |
| 6 | Experimental Setting / Details | 🟢 Yes | For a LAN with width N , depth L , and grid point number G , the number of parameters is N 2 L + NLG where N 2 L is the number of parameters for weight matrices and NLG is the number of parameters for spline activations, which causes little overhead in addition to MLP since usually G ≪ N so NLG ≪ N 2 L . |
| 7 | Experiment Statistical Significance | 🔵 N/A | El paper no realiza pruebas estadísticas para evaluar la significancia de los resultados. |
| 8 | Experiments Compute Resource | 🟢 Yes | For a LAN with width N , depth L , and grid point number G , the number of parameters is N 2 L + NLG where N 2 L is the number of parameters for weight matrices and NLG is the number of parameters for spline activations, which causes little overhead in addition to MLP since usually G ≪ N so NLG ≪ N 2 L . |
| 9 | Code of Ethics | 🔵 N/A | El paper no menciona un código de ética específico. |
| 10 | Broader Impacts | 🟢 Yes | Our preliminary results with LANs seem to imply that getting rid of linear weight matrices (by having learnable activations on edges, like KANs) is necessary for interpretability. We show that it is also possible to initialize a LAN from an MLP and further fine tune the LAN (green) for better PSNR. |
| 11 | Safeguards | 🔵 N/A | El paper no menciona medidas de seguridad o garantías específicas. |
| 12 | Licenses | 🔵 N/A | El paper no menciona la licencia bajo la cual se distribuye el código y los datos. |
| 13 | Assets | 🟢 Yes | For a LAN with width N , depth L , and grid point number G , the number of parameters is N 2 L + NLG where N 2 L is the number of parameters for weight matrices and NLG is the number of parameters for spline activations, which causes little overhead in addition to MLP since usually G ≪ N so NLG ≪ N 2 L . |
| 14 | Crowdsourcing & Human Subjects | 🔵 N/A | El paper no menciona el uso de crowdsourcing o sujetos humanos en la investigación. |
| 15 | IRB Approvals | 🔵 N/A | El paper no menciona aprobaciones de comités éticos (IRB). |
| 16 | Declaration of LLM Usage | 🟢 Yes | This paper was generated with the help of large language models. However, all claims and statements are made by the authors, and no model has been instructed to generate or modify any part of this text. |

---

## 🔍 Ficha Técnica y Datos Consolidados

Esta sección consolida la base de datos técnica extraída y validada del artículo científico durante la auditoría.

### Hiperparámetros
El paper discute la importancia de los hiperparámetros como el número de activaciones, la entropía y la penalización en la interpretabilidad de las redes. También se menciona que el tamaño del grid puede afectar la interpretabilidad.

### Hardware & Compute
No se proporciona información específica sobre el hardware utilizado.

### Arquitectura del Modelo
Se discuten arquitecturas como KANs (Knowledge-Aided Neural Networks) y LANs (Learnable Activation Networks).

### Dataset & Datos
El paper utiliza datos sintéticos, datasets Feynman y funciones especiales para evaluar las redes. No se proporciona información sobre la fuente de los datos.

### Código & Repositorio
Se menciona el uso de KANs y LANs pero no se proporciona código fuente completo.

### Estadística & Rigor Científico
No se realizan pruebas estadísticas en el paper.

### Comparativa con Baselines
Se compara KANs con MLPs (Multi-Layer Perceptrons) y LANs.

### Teoría & Demostraciones
Se discuten teorías sobre la interpretabilidad de las redes y se proporcionan pruebas para KANs y LANs.

### Software & Versiones
No se menciona ninguna versión específica de software.

### Análisis de Limitaciones
El paper reconoce limitaciones en la interpretabilidad de las LANs y la necesidad de una implementación completa y reproducible del código.

### Licencias detectadas
No se proporciona información sobre licencias.

### Impacto Social (Broader Impacts)
Se discuten aplicaciones potenciales como la interpretabilidad de las redes neuronales.

### Declaración de uso de LLMs
El paper reconoce el uso de LLMs en su generación pero afirma que todas las afirmaciones son del autor.

### Sujetos Humanos & Crowdsourcing
No se menciona el uso de sujetos humanos o crowdsourcing.

---

## 🧠 Razonamiento de Consolidación (CoT)

> El proceso de pensamiento involucra la evaluación de la interpretabilidad, la arquitectura de las redes y los datos utilizados. Se reconoce que hay limitaciones en la implementación y reproducibilidad del trabajo.

### 📍 Secciones Identificadas del Paper
- `A. KAN Functionalities`
- `B. Learnable activation networks (LANs)`
- `C. Dependence on hyperparameters`
- `D. Feynman KANs`
- `E. Remark on grid size`
- `F. KANs for special functions`

---
_Informe generado automáticamente._
