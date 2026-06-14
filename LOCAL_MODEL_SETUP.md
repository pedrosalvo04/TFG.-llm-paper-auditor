# Configuración del LLM Local (Qwen 2.5 a través de Ollama)

Este documento detalla los pasos necesarios para ejecutar la aplicación **Paper Auditor** utilizando un modelo local en lugar de depender de APIs externas en la nube (como Google Gemini). 

Al migrar la inferencia a tu propio hardware, aseguras un **100% de privacidad** sobre los documentos auditados y **eliminas las restricciones** de Rate Limits y cuotas.

---

## 1. Requisitos Previos e Instalación de Ollama

Para ejecutar modelos localmente, hemos integrado el motor de inferencia **Ollama**.

1. **Instalación:** Si aún no tienes Ollama instalado, descárgalo desde la página oficial para Windows: [Ollama Windows Download](https://ollama.com/download/windows) e instálalo.
2. **Ubicación Personalizada (Opcional pero recomendado):** Los modelos suelen ocupar bastante espacio (Varios GBs). Para evitar saturar el disco `C:\`, puedes definir dónde se guardan los modelos creando una variable de entorno de Windows llamada `OLLAMA_MODELS`.
   * En tu caso, configuramos la variable `OLLAMA_MODELS` apuntando a `E:\ollama_models`.
3. **Descarga del Modelo:** Abre tu terminal de PowerShell o Símbolo del Sistema y descarga los pesos del modelo ejecutando:
   ```bash
   ollama pull qwen2.5
   ```
4. **Verificación:** Asegúrate de que el demonio de Ollama está corriendo en segundo plano (puedes ver su icono en la bandeja del sistema de Windows). Por defecto, expone el servicio en `http://localhost:11434`.

---

## 2. Cambios Realizados en el Código

Para implementar esta funcionalidad, se han modificado los siguientes elementos en el proyecto:

### A. Cliente LLM (`backend/common/llm_client.py`)
* **Sustitución de API:** Se eliminó por completo la dependencia de la librería `google-genai` y la necesidad de una `GOOGLE_API_KEY`.
* **Peticiones HTTP directas:** Se reescribió la clase `LLMClient` para utilizar la librería estándar `requests` apuntando a `http://localhost:11434/api/generate`.
* **Manejo Estricto de JSON:** Se configuró el cliente para forzar estructuración JSON en todas las respuestas (`"format": "json"`), algo nativo y vital en Ollama para mantener la compatibilidad con el auditor.
* **Tolerancia a Errores Locales:** Se eliminó la lógica de reintentos por "saturación de cuota" y se reemplazó por un mecanismo que detecta si el demonio de Ollama no está arrancado, notificando al usuario a través de Streamlit.

### B. Configuración Global (`backend/common/config.py`)
* Todos los modelos de la orquestación (Map, Reduce, Extraction, Evaluation y Verification) que antes apuntaban a variantes de `gemini-3.1-flash-lite`, han sido forzados a apuntar a `"qwen2.5"`.
* Las variables como `temperature`, `top_p` y `top_k` han sido mapeadas correctamente al esquema de `options` de la API de Ollama.

### C. Pruebas Unitarias (`tests/test_llm_retry.py`)
* Las pruebas que comprobaban cómo reaccionaba el sistema a errores HTTP 429/503 (Too Many Requests de Gemini) fueron reemplazadas por pruebas que validan el correcto uso de `requests` y la detección de fallos de conexión (ej. `ConnectionError` si Ollama está apagado).

### D. Frontend y Diagramas
* Se actualizaron todos los archivos HTML generados (`diagrama_sota.html`, `diagrama_auditor.html`) y los scripts encargados de generarlos (`scratch/generate_*.py`) para reflejar en los diagramas de arquitectura que se está empleando **Qwen 2.5 Local** y **Map-Reduce Local**.

---

## 3. ¿Cómo Ejecutar la Aplicación?

El proceso de ejecución de la aplicación no varía, únicamente debes asegurarte de que Ollama está activo antes de arrancar tu servidor.

1. Verifica que **Ollama** está encendido (icono de la llama en tu barra de tareas). Si no es así, ábrelo desde el menú de inicio de Windows o ejecuta `ollama serve` en una terminal.
2. Abre una terminal en la raíz de este proyecto y activa tu entorno virtual si dispones de uno.
3. Lanza la aplicación de Streamlit:
   ```bash
   streamlit run app.py
   ```
   *(O el comando de arranque que uses habitualmente).*

¡Todo listo! El procesamiento de los PDFs y la auditoría se realizarán aprovechando enteramente los recursos de tu PC de forma privada.
