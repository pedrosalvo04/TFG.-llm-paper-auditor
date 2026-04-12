"""Servicio de auditoría de papers"""
import json
import time
import re
from backend.common.llm_client import LLMClient
from backend.common.config import AUDIT_CONFIG
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class PaperAuditor:
    """Auditor de reproducibilidad en papers científicos"""
    
    def __init__(self):
        """Inicializa el auditor con configuración determinista"""
        self.llm_client = LLMClient(generation_config=AUDIT_CONFIG)
        logger.info("✅ Auditor de papers inicializado correctamente")
    
    def _preprocess_paper(self, paper_text):
        """
        Detecta patrones problemáticos mediante regex antes del análisis LLM
        
        Args:
            paper_text: Texto del paper
            
        Returns:
            Diccionario con red flags detectadas
        """
        logger.info("🔍 Fase 0: Pre-procesamiento con detección de patrones...")
        
        red_flags = {
            # Datos propietarios o no disponibles
            "datos_propietarios": bool(re.search(
                r"(proprietary|confidential|cannot\s+(disclose|release|share)|not\s+available|restricted|internal)\s+.{0,50}(data|dataset|corpus)",
                paper_text, re.IGNORECASE
            )),
            "datos_sin_acceso": not bool(re.search(
                r"(available\s+at|download|DOI|zenodo|figshare|huggingface\.co/datasets|github\.com/.+/data)",
                paper_text, re.IGNORECASE
            )),
            
            # Código no disponible
            "codigo_propietario": bool(re.search(
                r"(proprietary|confidential|cannot\s+(disclose|release|share)|not\s+available|restricted|internal)\s+.{0,50}(code|implementation|source|repository)",
                paper_text, re.IGNORECASE
            )),
            "sin_repositorio": not bool(re.search(
                r"(github|gitlab|bitbucket|sourceforge)\.com/[\w-]+/[\w-]+",
                paper_text, re.IGNORECASE
            )),
            
            # Hiperparámetros vagos o no especificados
            "hiperparametros_vacios": bool(re.search(
                r"(standard\s+settings|default\s+parameters|typical\s+configuration|not\s+disclosed|internal\s+experimentation)",
                paper_text, re.IGNORECASE
            )),
            "sin_learning_rate": not bool(re.search(
                r"learning\s+rate.{0,30}(\d+\.\d+[eE][-+]?\d+|\d+\.\d+)",
                paper_text, re.IGNORECASE
            )),
            "sin_batch_size": not bool(re.search(
                r"batch\s+size.{0,30}\d+",
                paper_text, re.IGNORECASE
            )),
            "sin_optimizer": not bool(re.search(
                r"(Adam|AdamW|SGD|RMSprop|Adagrad)\s+(optimizer|optimiser)",
                paper_text, re.IGNORECASE
            )),
            
            # Falta de información estadística
            "sin_intervalos_confianza": not bool(re.search(
                r"(confidence\s+interval|standard\s+deviation|std|error\s+bar|±|\+/-)",
                paper_text, re.IGNORECASE
            )),
            "sin_significancia": not bool(re.search(
                r"(p-value|statistical\s+significance|t-test|ANOVA|Mann-Whitney|Wilcoxon)",
                paper_text, re.IGNORECASE
            )),
            
            # Indicadores positivos
            "tiene_github": bool(re.search(r"github\.com", paper_text, re.IGNORECASE)),
            "tiene_doi_datos": bool(re.search(r"DOI.{0,20}(dataset|data)", paper_text, re.IGNORECASE)),
            "menciona_reproducibilidad": bool(re.search(r"(reproducib|replicab|open\s+science)", paper_text, re.IGNORECASE))
        }
        
        # Log de red flags detectadas
        critical_flags = [k for k, v in red_flags.items() if v and not k.startswith("tiene_") and not k.startswith("menciona_")]
        if critical_flags:
            logger.warning(f"⚠️ Red flags detectadas: {', '.join(critical_flags)}")
        else:
            logger.info("✅ No se detectaron red flags críticas en pre-procesamiento")
        
        return red_flags

    def _extract_information(self, paper_text, red_flags):
        """
        FASE 1: Extrae información estructurada del paper
        
        Args:
            paper_text: Texto del paper
            red_flags: Red flags del pre-procesamiento
            
        Returns:
            Diccionario con información extraída
        """
        logger.info("🔍 Fase 1: Extracción de información estructurada...")
        
        extraction_prompt = f"""
Eres un extractor de información especializado en papers de Ciencias de la Computación (IA, ML, Software Engineering, Computer Vision, NLP, etc.).

Tu tarea es EXTRAER información específica del paper, NO evaluarla todavía.

IMPORTANTE: Lee TODO el paper, incluyendo tablas, figuras y apéndices.

EXTRAE LA SIGUIENTE INFORMACIÓN (responde "NO ENCONTRADO" si no está presente):

1. CÓDIGO Y SOFTWARE:
   - ¿Menciona repositorio público? (GitHub/GitLab/Bitbucket URL o mención explícita)
   - ¿Dice explícitamente que el código NO está disponible? (cita textual)
   - ¿Menciona dependencias/librerías con versiones?
   - ¿Proporciona instrucciones de instalación o ejecución?
   - Busca frases como: "we release", "available at", "open source", "code is available"

2. DATOS:
   - ¿Nombre del dataset usado?
   - ¿Proporciona acceso al dataset? (URL/DOI/enlace o mención de disponibilidad)
   - ¿Dice explícitamente que los datos NO están disponibles? (cita textual)
   - ¿Describe preprocesamiento de datos?
   - ¿Especifica splits (train/val/test) o menciona "single epoch", "training data"?
   - Busca secciones como "Data", "Dataset", "Pretraining Data"

3. HIPERPARÁMETROS:
   - ¿Qué optimizer usa? (Adam/AdamW/SGD/etc.)
   - ¿Learning rate? (busca "learning rate", "LR", "peak LR")
   - ¿Batch size? (busca "batch size", "global batch", "micro-batch")
   - ¿Número de epochs? (busca "epochs", "training steps", "tokens")
   - ¿Warmup steps?
   - ¿Weight decay?
   - ¿Dice "standard settings" o "not disclosed"? (cita textual)
   - Busca TABLAS con hiperparámetros

4. HARDWARE:
   - ¿Tipo de GPU/CPU usado? (busca "GPU", "A100", "V100", "TPU")
   - ¿Cantidad de memoria?
   - ¿Tiempo de entrenamiento?

5. ESTADÍSTICAS:
   - ¿Reporta intervalos de confianza o desviaciones estándar?
   - ¿Incluye tests de significancia estadística?
   - ¿Número de ejecuciones/seeds?

6. ARQUITECTURA:
   - ¿Describe la arquitectura del modelo?
   - ¿Proporciona pesos/checkpoints? (busca "weights", "checkpoints", "model available")

7. COMPARACIÓN CON BASELINES:
   - ¿Compara con otros modelos/métodos? (busca nombres: LLaMA, GPT, BERT, Falcon, MPT, Pythia, etc.)
   - ¿Hay TABLAS de resultados comparativos? (busca "Table", "comparison", "baseline")
   - ¿Usa mismas métricas que los baselines?
   - Busca secciones como "Results", "Evaluation", "Comparison", "Downstream Evaluation"
   - IMPORTANTE: Si ves tablas con múltiples modelos y métricas → tiene_tablas_comparativas: "sí"

8. FRASES PROBLEMÁTICAS:
   Busca y cita TEXTUALMENTE cualquier frase que diga:
   - "cannot release", "cannot disclose", "proprietary", "confidential"
   - "not available", "restricted", "internal"
   - "due to competitive concerns", "legal constraints"

RED FLAGS DETECTADAS EN PRE-PROCESAMIENTO:
{json.dumps(red_flags, indent=2)}

DEVUELVE UN JSON CON ESTA ESTRUCTURA:
{{
  "codigo": {{
    "repositorio_url": "URL o mención explícita o NO ENCONTRADO",
    "frase_negativa": "cita textual o NO ENCONTRADO",
    "dependencias": "descripción o NO ENCONTRADO",
    "instrucciones": "sí/no",
    "mencion_liberacion": "cita de 'we release code' o NO ENCONTRADO"
  }},
  "datos": {{
    "nombre_dataset": "nombre o NO ENCONTRADO",
    "acceso_url": "URL/DOI o mención de disponibilidad o NO ENCONTRADO",
    "frase_negativa": "cita textual o NO ENCONTRADO",
    "preprocesamiento": "descripción o NO ENCONTRADO",
    "splits": "descripción o NO ENCONTRADO",
    "mencion_liberacion": "cita de 'we release data' o NO ENCONTRADO"
  }},
  "hiperparametros": {{
    "optimizer": "nombre o NO ENCONTRADO",
    "learning_rate": "valor o NO ENCONTRADO",
    "batch_size": "valor o NO ENCONTRADO",
    "epochs": "valor o NO ENCONTRADO",
    "warmup": "valor o NO ENCONTRADO",
    "weight_decay": "valor o NO ENCONTRADO",
    "frase_vaga": "cita textual de 'standard settings' o NO ENCONTRADO"
  }},
  "hardware": {{
    "gpu_cpu": "descripción o NO ENCONTRADO",
    "memoria": "cantidad o NO ENCONTRADO",
    "tiempo": "duración o NO ENCONTRADO"
  }},
  "estadisticas": {{
    "intervalos_confianza": "sí/no",
    "tests_significancia": "sí/no",
    "num_ejecuciones": "número o NO ENCONTRADO"
  }},
  "arquitectura": {{
    "descripcion": "resumen o NO ENCONTRADO",
    "pesos_disponibles": "sí/no",
    "mencion_liberacion": "cita de 'weights available' o NO ENCONTRADO"
  }},
  "comparacion_baselines": {{
    "modelos_comparados": ["lista de modelos encontrados en tablas o vacío"],
    "tiene_tablas_comparativas": "sí/no",
    "mismas_metricas": "sí/no",
    "seccion_resultados": "resumen de sección Results/Evaluation o NO ENCONTRADO"
  }},
  "frases_problematicas": [
    "cita textual 1",
    "cita textual 2"
  ]
}}

CONSEJOS PARA EXTRACCIÓN:
- Lee las secciones "Results", "Evaluation", "Experiments" cuidadosamente
- Busca tablas numeradas (Table 1, Table 2, etc.)
- Si ves nombres de modelos como LLaMA, GPT, BERT en tablas → hay comparación
- Si dice "we release", "available at", "open source" → anótalo
- Si dice "cannot", "proprietary", "not available" → anótalo como frase problemática

TEXTO DEL PAPER:
{paper_text[:50000]}
"""
        
        try:
            response = self.llm_client.generate(extraction_prompt)
            extracted_info = json.loads(response.text)
            logger.info("✅ Fase 1 completada: Información extraída")
            return extracted_info
        except Exception as e:
            logger.error(f"❌ Error en Fase 1: {str(e)}")
            return {}
    
    def _evaluate_reproducibility(self, extracted_info, red_flags):
        """
        FASE 2: Evalúa reproducibilidad basándose en la información extraída
        
        Args:
            extracted_info: Información extraída en Fase 1
            red_flags: Red flags del pre-procesamiento
            
        Returns:
            Diccionario con evaluación completa
        """
        logger.info("📊 Fase 2: Evaluación de reproducibilidad...")
        
        evaluation_prompt = f"""
Eres un Auditor Editorial EXTREMADAMENTE ESTRICTO de revistas de alto impacto en Ciencias de la Computación.

Has recibido información EXTRAÍDA del paper. Ahora debes EVALUAR la reproducibilidad.

INFORMACIÓN EXTRAÍDA:
{json.dumps(extracted_info, indent=2, ensure_ascii=False)}

RED FLAGS DETECTADAS:
{json.dumps(red_flags, indent=2)}

REGLAS DE EVALUACIÓN ESTRICTAS:

🔴 MARCA "NO CUMPLE" SI:
- Código: "frase_negativa" contiene "cannot release/disclose" O "repositorio_url" es "NO ENCONTRADO"
- Datos: "frase_negativa" contiene "proprietary/confidential" O "acceso_url" es "NO ENCONTRADO"
- Hiperparámetros: "frase_vaga" contiene "standard settings" O faltan optimizer/learning_rate/batch_size
- Reproducibilidad: Faltan 2+ elementos críticos (código, datos, hiperparámetros)
- Estadística: No hay intervalos de confianza NI tests de significancia

🟡 MARCA "CUMPLE PARCIALMENTE" SI:
- Estadística: Tiene métricas pero sin intervalos de confianza
- Código: Tiene repositorio pero sin dependencias exactas
- Datos: Dataset público pero preprocesamiento incompleto
- Hiperparámetros: Tiene algunos pero faltan detalles menores

✅ MARCA "CUMPLE TOTALMENTE" SI:
- Toda la información crítica está presente y accesible públicamente
- No hay frases negativas ni red flags

⚪ MARCA "N/A" SOLO SI:
- La categoría genuinamente no aplica al tipo de estudio (ej: paper teórico sin experimentos)
- NO uses N/A como escape cuando falta información - usa 🔴 NO CUMPLE

EJEMPLOS DE EVALUACIÓN:

EJEMPLO 1 - 🔴 NO CUMPLE en Datos:
Extracción: {{"frase_negativa": "We used a proprietary dataset that cannot be disclosed"}}
→ Evaluación: 🔴 NO CUMPLE
→ Hallazgo: "El paper declara explícitamente: 'We used a proprietary dataset that cannot be disclosed'"

EJEMPLO 2 - ✅ CUMPLE en Código:
Extracción: {{"repositorio_url": "github.com/org/repo", "dependencias": "requirements.txt incluido"}}
→ Evaluación: ✅ CUMPLE TOTALMENTE
→ Hallazgo: "Código completo disponible en GitHub con dependencias especificadas"

EJEMPLO 3 - 🔴 NO CUMPLE en Hiperparámetros:
Extracción: {{"frase_vaga": "We used standard settings", "optimizer": "NO ENCONTRADO"}}
→ Evaluación: 🔴 NO CUMPLE
→ Hallazgo: "El paper indica 'standard settings' sin especificar valores. Optimizer no especificado."

EJEMPLO 4 - ✅ CUMPLE en Comparación con Baselines:
Si el paper tiene tablas comparando con LLaMA, GPT, BERT, etc. en mismas métricas
→ Evaluación: ✅ CUMPLE TOTALMENTE
→ Hallazgo: "Se compara exhaustivamente con modelos SOTA usando métricas estandarizadas"

EJEMPLO 5 - 🔴 NO CUMPLE en Comparación con Baselines:
Si el paper NO compara con otros métodos o solo menciona trabajos relacionados sin evaluación
→ Evaluación: 🔴 NO CUMPLE
→ Hallazgo: "No se realiza comparación experimental con métodos del estado del arte"

INSTRUCCIONES ESPECÍFICAS POR CATEGORÍA:

1. ESTADÍSTICA Y EXPERIMENTACIÓN:
   - Si tiene métricas + intervalos + tests → ✅ CUMPLE TOTALMENTE
   - Si tiene métricas + (intervalos O tests) → ✅ CUMPLE TOTALMENTE (menciona en recomendación que sería ideal tener ambos)
   - Si tiene métricas robustas + comparaciones extensivas pero sin intervalos/tests → ✅ CUMPLE TOTALMENTE
     * IMPORTANTE: En la recomendación menciona "Aunque no es obligatorio en papers de LLMs, sería ideal incluir intervalos de confianza"
   - Si tiene métricas básicas sin comparaciones → 🟡 CUMPLE PARCIALMENTE
   - Si NO tiene métricas o experimentos → 🔴 NO CUMPLE
   - CONTEXTO: Papers de ML/LLMs modernos raramente incluyen intervalos de confianza
   - CONTEXTO: Papers de sistemas/redes DEBEN incluir análisis de varianza
   - CONTEXTO: Papers teóricos pueden tener menos énfasis en estadística

2. CÓDIGO Y SOFTWARE:
   - Si "frase_negativa" != "NO ENCONTRADO" → 🔴 NO CUMPLE (cita la frase)
   - Si "repositorio_url" == "NO ENCONTRADO" Y es paper experimental → 🔴 NO CUMPLE
   - Si "repositorio_url" == "NO ENCONTRADO" Y es paper teórico → 🟡 CUMPLE PARCIALMENTE
   - Si tiene repo pero sin dependencias → 🟡 CUMPLE PARCIALMENTE
   - Si tiene repo + dependencias + instrucciones → ✅ CUMPLE TOTALMENTE
   - CONTEXTO: Papers de sistemas, ML, software engineering DEBEN liberar código
   - CONTEXTO: Papers teóricos (complejidad, algoritmos) pueden no tener implementación

3. DATOS Y DATASETS:
   - Si "frase_negativa" != "NO ENCONTRADO" → 🔴 NO CUMPLE (cita la frase)
   - Si "acceso_url" == "NO ENCONTRADO" Y usa datos experimentales → 🔴 NO CUMPLE
   - Si "acceso_url" == "NO ENCONTRADO" Y es paper teórico/simulación → 🟡 CUMPLE PARCIALMENTE
   - Si tiene dataset pero preprocesamiento vago → 🟡 CUMPLE PARCIALMENTE
   - Si tiene dataset + preprocesamiento + splits → ✅ CUMPLE TOTALMENTE
   - CONTEXTO: Papers de ML, NLP, CV DEBEN especificar datasets
   - CONTEXTO: Papers de arquitectura software pueden usar estudios de caso privados

4. DISEÑO EXPERIMENTAL:
   - Si "frase_vaga" != "NO ENCONTRADO" → 🔴 NO CUMPLE (cita la frase)
   - Si faltan hiperparámetros CRÍTICOS (optimizer, LR, batch) en paper de ML → 🔴 NO CUMPLE
   - Si faltan hiperparámetros MENORES (weight decay, warmup steps) → ✅ CUMPLE TOTALMENTE
     * IMPORTANTE: En la recomendación menciona "Sería útil documentar también [parámetro faltante] para completitud"
   - Si tiene todos los parámetros críticos + hardware → ✅ CUMPLE TOTALMENTE
   - CONTEXTO: Parámetros CRÍTICOS en ML: optimizer, learning rate, batch size, epochs
   - CONTEXTO: Parámetros MENORES en ML: weight decay, warmup, gradient clipping
   - CONTEXTO: Parámetros CRÍTICOS en Sistemas: CPU, memoria, red, latencia
   - CONTEXTO: Papers experimentales DEBEN especificar configuración completa de parámetros críticos

5. MODELOS Y ARQUITECTURAS:
   - Si "descripcion" == "NO ENCONTRADO" → 🔴 NO CUMPLE
   - Si tiene descripción pero "pesos_disponibles": "no" → 🟡 CUMPLE PARCIALMENTE
   - Si tiene todo → ✅ CUMPLE TOTALMENTE

6. REPRODUCIBILIDAD:
   - Cuenta elementos faltantes: código (si), datos (si), hiperparámetros (si)
   - Si faltan 2+ → 🔴 NO CUMPLE
   - Si falta 1 → 🟡 CUMPLE PARCIALMENTE
   - Si tiene todo → ✅ CUMPLE TOTALMENTE

7. COMPARACIÓN CON BASELINES:
   - Si "modelos_comparados" tiene 3+ modelos Y "tiene_tablas_comparativas": "sí" → ✅ CUMPLE TOTALMENTE
   - Si compara con 1-2 baselines → 🟡 CUMPLE PARCIALMENTE
   - Si solo menciona trabajos relacionados sin comparar → 🔴 NO CUMPLE
   - Si "seccion_resultados" == "NO ENCONTRADO" → 🔴 NO CUMPLE
   - NO uses ⚪ N/A a menos que sea paper puramente teórico sin implementación
   - CONTEXTO: Papers experimentales DEBEN comparar con estado del arte
   - CONTEXTO: Papers de nuevas arquitecturas/lenguajes DEBEN mostrar ventajas vs existentes

DEVUELVE UN JSON CON ESTA ESTRUCTURA:
{{
  "revision": [
    {{
      "categoria": "Estadística y Experimentación",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }},
    {{
      "categoria": "Código y Software",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }},
    {{
      "categoria": "Datos y Datasets",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }},
    {{
      "categoria": "Diseño Experimental",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }},
    {{
      "categoria": "Modelos y Arquitecturas",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }},
    {{
      "categoria": "Reproducibilidad",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }},
    {{
      "categoria": "Comparación con Baselines",
      "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
      "hallazgo": "Descripción específica citando información extraída",
      "recomendacion": "Acción concreta requerida"
    }}
  ],
  "veredicto_final": "Resumen crítico de la evaluación general"
}}

⚠️ IMPORTANTE: 
- Si extracted_info contiene frases como "cannot release", "proprietary", "not disclosed" → 🔴 NO CUMPLE
- Si red_flags tiene valores true en campos críticos → penaliza la evaluación
- Cita TEXTUALMENTE las frases problemáticas en el hallazgo
- NO uses ⚪ N/A como escape - solo para casos genuinamente no aplicables
"""
        
        try:
            response = self.llm_client.generate(evaluation_prompt)
            evaluation = json.loads(response.text)
            logger.info("✅ Fase 2 completada: Evaluación finalizada")
            return evaluation
        except Exception as e:
            logger.error(f"❌ Error en Fase 2: {str(e)}")
            return {"error": str(e)}
    
    def audit(self, paper_text):
        """
        Analiza el paper en 3 fases: Pre-procesamiento, Extracción y Evaluación
        
        Args:
            paper_text: Texto del paper en formato markdown
            
        Returns:
            Diccionario con resultados de la auditoría
        """
        caracteres = len(paper_text)
        logger.info(f"🚀 Iniciando auditoría en 3 fases. Tamaño: {caracteres} caracteres")
        
        prompt = f"""
        Actúa como un Auditor Editorial EXTREMADAMENTE ESTRICTO de revistas de alto impacto en Ciencias de la Computación.
        Tu trabajo es RECHAZAR papers que no cumplan con estándares de reproducibilidad.
        
        ⚠️ IMPORTANTE: Si el paper dice EXPLÍCITAMENTE que NO libera algo crítico, debes marcar 🔴 NO CUMPLE.
        
        EJEMPLOS DE FRASES QUE INDICAN 🔴 NO CUMPLE:
        - "cannot release", "cannot disclose", "cannot be disclosed"
        - "proprietary", "confidential", "internal"
        - "not disclosed", "not available", "restricted"
        - "standard settings" sin especificar valores
        - "due to competitive concerns", "legal constraints"
        
        CRITERIOS ESTRICTOS:
        
        1. Estadística y Experimentación:
           ✅ CUMPLE: Métricas + intervalos de confianza + tests estadísticos
           🟡 PARCIAL: Métricas sin intervalos de confianza
           🔴 NO CUMPLE: Sin métricas o sin tests estadísticos
        
        2. Código y Software:
           ✅ CUMPLE: Repositorio público + código completo + dependencias
           🟡 PARCIAL: Código parcial o sin dependencias exactas
           🔴 NO CUMPLE: Si dice "cannot release code", "proprietary code", "not disclosed"
        
        3. Datos y Datasets:
           ✅ CUMPLE: Dataset público + preprocesamiento + splits documentados
           🟡 PARCIAL: Dataset público pero preprocesamiento incompleto
           🔴 NO CUMPLE: Si dice "proprietary data", "cannot disclose", "confidential"
        
        4. Diseño Experimental:
           ✅ CUMPLE: TODOS los hiperparámetros + semillas + hardware
           🟡 PARCIAL: Faltan algunos hiperparámetros menores
           🔴 NO CUMPLE: Si dice "not disclosed", "standard settings", "internal experimentation"
        
        5. Modelos y Arquitecturas:
           ✅ CUMPLE: Arquitectura completa + pesos públicos
           🟡 PARCIAL: Arquitectura completa pero sin pesos
           🔴 NO CUMPLE: Arquitectura incompleta o pesos no disponibles
        
        6. Reproducibilidad:
           ✅ CUMPLE: Código + datos + hiperparámetros completos
           🟡 PARCIAL: Falta uno de los tres elementos
           🔴 NO CUMPLE: Faltan dos o más elementos críticos
        
        7. Comparación con Baselines:
           ✅ CUMPLE: Comparación justa con SOTA en mismas condiciones
           🟡 PARCIAL: Comparación con SOTA pero condiciones diferentes
           🔴 NO CUMPLE: Sin comparación con SOTA

        REGLAS CRÍTICAS (APLICAR SIN EXCEPCIONES):
        
        🔴 Marca "NO CUMPLE" si encuentras CUALQUIERA de estas frases:
        - "cannot release"
        - "cannot disclose" 
        - "proprietary"
        - "confidential"
        - "not disclosed"
        - "internal experimentation"
        - "standard settings" (sin valores específicos)
        - "due to competitive concerns"
        - "legal constraints" (como excusa para no liberar)
        
        🔴 Marca "NO CUMPLE" en Código si:
        - No menciona repositorio público (GitHub/GitLab)
        - Dice que el código no está disponible
        - Solo menciona "framework" sin código de entrenamiento
        
        🔴 Marca "NO CUMPLE" en Datos si:
        - No especifica cómo acceder al dataset
        - Dice que los datos son propietarios
        - No proporciona DOI o enlace permanente
        
        🔴 Marca "NO CUMPLE" en Diseño Experimental si:
        - Tabla de hiperparámetros dice "standard settings"
        - No especifica optimizer exacto (Adam, AdamW, SGD, etc.)
        - No especifica learning rate, batch size, o epochs
        
        INSTRUCCIÓN DE SALIDA:
        Devuelve EXCLUSIVAMENTE un objeto JSON:
        {{
          "revision": [
            {{
              "categoria": "Nombre",
              "estado": "🟢/🔵/🟡/🟠/🔴/⚪",
              "hallazgo": "CITA TEXTUALMENTE las frases problemáticas del paper entre comillas",
              "recomendacion": "Acción específica requerida"
            }}
          ],
          "veredicto_final": "Resumen CRÍTICO"
        }}
        
        ⚠️ RECUERDA: Si el paper dice explícitamente que NO libera algo → 🔴 NO CUMPLE (sin excepciones)

        TEXTO DEL ARTÍCULO:
        {paper_text}
        """
        
        start_time = time.time()
        
        try:
            # FASE 0: Pre-procesamiento con regex
            red_flags = self._preprocess_paper(paper_text)
            
            # FASE 1: Extracción de información
            extracted_info = self._extract_information(paper_text, red_flags)
            
            # FASE 2: Evaluación de reproducibilidad
            evaluation = self._evaluate_reproducibility(extracted_info, red_flags)
            
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            
            logger.info(f"✅ Auditoría completada en {execution_time} segundos")
            
            # Inyectamos métricas y metadatos
            evaluation["metricas"] = {
                "tiempo_segundos": execution_time,
                "caracteres_leidos": caracteres,
                "red_flags_detectadas": sum(1 for k, v in red_flags.items() if v and not k.startswith("tiene_"))
            }
            evaluation["metadatos"] = {
                "red_flags": red_flags,
                "informacion_extraida": extracted_info
            }
            
            return evaluation

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
