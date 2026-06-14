# Arquitectura y Adaptación para Modelos Locales (Qwen 2.5)

El objetivo de este documento es detallar a nivel técnico todas las modificaciones arquitectónicas, configuraciones de entorno y mecanismos de resiliencia que se han implementado en el **Paper Auditor** para permitir su funcionamiento autónomo y 100% en local mediante **Ollama** y el modelo **Qwen 2.5**.

Al prescindir de APIs comerciales en la nube (como Google Gemini), se han tenido que resolver múltiples desafíos intrínsecos a la inferencia local: límites de contexto, tiempos de respuesta prolongados y volatilidad en el formato de salida.

---

## 1. Configuración del Entorno de Inferencia (Ollama)

### Almacenamiento Inteligente (Disco Secundario)
Los modelos LLM con pesos en alta precisión ocupan varios Gigabytes. Para proteger el disco principal (`C:\`), se configuró el sistema operativo Windows para delegar la descarga y ejecución de los pesos al disco secundario.
- **Variable de Entorno:** Se inyectó permanentemente la variable `OLLAMA_MODELS=E:\ollama_models`.
- **Motor de Inferencia:** El demonio de Ollama se levanta exponiendo el puerto `http://localhost:11434`, consumiendo los modelos directamente del volumen `E:\`.

---

## 2. Modificaciones Críticas en el Cliente LLM (`llm_client.py`)

La clase `LLMClient` original, acoplada al SDK de Google (`google-genai`), fue reescrita por completo para interactuar con la API REST de Ollama. En este proceso se tomaron tres decisiones arquitectónicas vitales para la estabilidad:

### A. Forzado de Contexto Extendido (`num_ctx`)
Por defecto, Ollama limita drásticamente la "memoria" del modelo a **2048 tokens** para ahorrar RAM/VRAM en ordenadores modestos. Si un paper supera este límite, el modelo trunca el texto y sufre de "amnesia", arruinando las fases de Map-Reduce.
* **Solución:** Se inyectó forzosamente el parámetro `"num_ctx": 32768` en el payload HTTP. Esto obliga a Qwen 2.5 a mantener una ventana atencional de 32K tokens, permitiéndole asimilar papers completos de golpe.

### B. Inmunidad a Timeouts (`timeout=None`)
Las APIs comerciales devuelven resultados en segundos, por lo que el código original tenía límites de espera estrictos. Al correr un modelo local pesado de 4.7 GB, el hardware del usuario puede demorar más de 5-10 minutos en consolidar grandes bloques de texto.
* **Solución:** Se configuró la librería `requests` con `timeout=None`. El servidor de Python ahora espera indefinidamente a que el hardware (CPU/GPU) local termine de inferir, eliminando por completo los bloqueos por `Read timed out`.

### C. JSON Estricto y Temperaturas (Creatividad)
* Se integró `"format": "json"` nativamente en la petición para forzar al modelo a escupir estructuras informáticas válidas.
* Se heredaron las configuraciones maestras de `config.py`: `temperature=0.0` para las fases de extracción de datos (cero creatividad, cero alucinaciones) y `temperature=0.3` para apartados analíticos de resumen.

---

## 3. Resiliencia y Reparación Automática de Output (`base_skill.py`)

Uno de los mayores retos de usar modelos de 7-14 billones de parámetros (como Qwen 2.5) frente a modelos "frontier" en la nube, es que ocasionalmente cometen errores sintácticos al generar JSONs gigantescos (ej. olvidar una coma, o no escapar unas comillas dobles). Un solo error tipográfico provocaba un `JSONDecodeError` que crasheaba toda la auditoría.

* **Implementación de `json-repair`:** Se instaló e integró la librería `json-repair`.
* **Fallback en Cascada:** Cuando el método `parse_json_response` recibe el texto del LLM, primero intenta hacer un `json.loads` estándar. Si este falla por sintaxis, el bloque entra en un bloque `except` donde `json-repair` actúa quirúrgicamente: recompone brackets rotos, inyecta comas faltantes y formatea cadenas mal escapadas.
* **Resultado:** La auditoría se vuelve a prueba de balas frente a las clásicas "alucinaciones de sintaxis" de los modelos locales de código abierto.

También se añadió control de tipos dinámico en componentes visuales (como `audit_results.py`) para lidiar con variaciones de esquema (por ejemplo, cuando el LLM decide devolver un Array de pensamientos en lugar de un String plano en el nodo `thought_process`).

---

## 4. Adaptación Dinámica del Frontend y Reportes

Toda la aplicación de Streamlit y los generadores de PDF se modificaron para desvincularse del "branding" de Gemini y abrazar la inyección dinámica del modelo:

* **Descargas Dinámicas:** Los nombres de los ficheros exportados se construyen usando la variable `VERIFICATION_MODEL_NAME`. Ejemplo: `auditoria_qwen2.5_NombreDelPaper.md`.
* **Metadatos Nativos:** El informe Markdown y PDF ahora incorpora una fila técnica certificando el modelo empleado (🤖 **Modelo Local**: `qwen2.5`).
* **Gráficos HTML:** Los scripts de esquemas (`diagrama_sota.html`, etc.) fueron reescritos para reflejar un flujo **"Map-Reduce Local"**.

---

## Conclusión

El "Paper Auditor" no solo puede ejecutarse ahora fuera de la red, garantizando total privacidad sobre los PDFs subidos, sino que su base de código se ha reforzado enormemente. Las adiciones de contexto gigante (32K), el descarte de timeouts y el reparador heurístico de JSON han convertido la herramienta en un motor robusto capaz de orquestar inteligencias artificiales locales, perdonando sus limitaciones y maximizando su utilidad.
