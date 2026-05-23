# 🚀 Guía de Instalación y Primera Ejecución

> **Para colaboradores y evaluadores del TFG.** Esta guía cubre todo lo necesario para poner en marcha el sistema desde cero, partiendo únicamente del repositorio de GitHub.

---

## ⚠️ Lo que NO está en el repositorio (`.gitignore`)

Antes de empezar, ten en cuenta que los siguientes elementos **no se descargan con el `git clone`** y deben crearse/configurarse manualmente:

| Elemento | Por qué no está | Qué hacer |
|---|---|---|
| `venv/` | Entorno virtual local | Crear con Python (ver paso 2) |
| `.env` | Contiene API Keys secretas | Crear con las claves (ver paso 3) |
| `temp/` | Archivos temporales de PDFs | Se crea automáticamente al ejecutar |
| `*.log` | Logs de ejecución | Se generan automáticamente |
| `__pycache__/` | Caché de Python | Se genera automáticamente |

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10 o superior** → [python.org/downloads](https://www.python.org/downloads/)
  - Durante la instalación en Windows, marca ✅ **"Add Python to PATH"**
- **Git** → [git-scm.com](https://git-scm.com/)
- (Opcional) **CUDA** si tienes GPU NVIDIA → acelera el parsing de PDFs con Docling

Verifica las instalaciones:

```bash
python --version    # Python 3.10+
git --version       # git 2.x
```

---

## 🛠️ Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/pedrosalvo04/TFG.-llm-paper-auditor.git
cd TFG.-llm-paper-auditor
```

---

## 🐍 Paso 2 — Crear el entorno virtual e instalar dependencias

### 2.1 Crear el `venv`

```bash
# Windows (PowerShell)
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### 2.2 Activar el entorno virtual

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

> Sabrás que está activo porque el prompt muestra `(venv)` al inicio.

### 2.3 Instalar dependencias

El archivo `requirements.txt` ya viene incluido en el repositorio. Instala todo con:

```bash
pip install -r requirements.txt
```

> ⏳ La primera instalación puede tardar varios minutos, especialmente `docling` y `torch`.

---

## 🔑 Paso 3 — Configurar las API Keys

Crea un archivo llamado **`.env`** en la raíz del proyecto (mismo nivel que `app.py`) con el siguiente contenido:

```env
# Google AI Studio (para los modelos Gemini) - OBLIGATORIA
GOOGLE_API_KEY=TU_CLAVE_AQUI

# Semantic Scholar (para el análisis de estado del arte) - RECOMENDADA
SEMANTIC_SCHOLAR_API_KEY=TU_CLAVE_AQUI
```

### ¿Cómo obtener cada clave?

#### Google AI Studio (`GOOGLE_API_KEY`) — **Obligatoria**
1. Ve a [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Create API Key"**
4. Copia la clave y pégala en `.env`

> El sistema utiliza modelos de la familia Gemini de forma directa a través del SDK oficial de Google (`google-genai`). El uso gratuito tiene límites de cuota; para uso intensivo se recomienda una cuenta con facturación habilitada.

#### Semantic Scholar (`SEMANTIC_SCHOLAR_API_KEY`) — Recomendada
1. Ve a [api.semanticscholar.org](https://www.semanticscholar.org/product/api)
2. Solicita una API Key gratuita
3. La recibirás por email en unos días

> Sin esta clave, el módulo de **análisis de estado del arte (SOTA)** no funcionará (o tendrá límites de tasa estrictos de la API pública), pero el auditor principal sí.

---

## 🎮 Paso 4 — Ejecutar la aplicación

Primero activa el entorno virtual (si no lo tienes ya activo del paso 2):

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

Luego lanza la app:

```bash
streamlit run app.py
```

Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 💾 Paso 5 — Carpeta de resultados y Nombre de la App

### 5.1 Nombre de visualización en la UI
En el frontend (`frontend/config.py` y `frontend/components/loader.py`), la aplicación se titula **"Nature Auditor Pro"** y utiliza el logotipo de la ACM. Sin embargo, su funcionalidad principal de backend y todos sus prompts están dedicados al análisis de cumplimiento de la guía oficial del **checklist de NeurIPS 2026**.

### 5.2 Exportación de Informes en el Escritorio
Los informes de auditoría generados se guardan automáticamente en la ruta local:
```
C:\Users\pedro\Desktop\papers IA resultado\
```
> ⚠️ **Advertencia de ruta hardcodeada**: La ruta está configurada de forma fija para el usuario de Windows `pedro` en `frontend/components/file_uploader.py`. Si ejecutas la aplicación con un nombre de usuario diferente, el sistema no podrá escribir en dicha carpeta, lanzará una advertencia en la consola/UI, y continuará la ejecución con normalidad. Podrás seguir descargando el informe final en Markdown haciendo clic en el botón **📥 Descargar Informe Completo (.md)** del panel de la web.
>
> Si quieres que se guarde de forma automática en tu propio Escritorio, edita la línea 129 de [file_uploader.py](file:///c:/Users/pedro/Documents/GitHub/TFG.-llm-paper-auditor/frontend/components/file_uploader.py) reemplazando `"pedro"` por tu usuario de Windows.

## 🖥️ Configuración de GPU (Docling)

El sistema **detecta automáticamente** si tienes una GPU NVIDIA con CUDA disponible:
- **Con GPU**: Docling procesa los PDFs usando CUDA (mucho más rápido).
- **Sin GPU**: Usa la CPU automáticamente (más lento, pero funcional).

No es necesario configurar nada. Si quieres verificar si CUDA está disponible:

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

---

## 🧪 Verificar que todo funciona

```bash
# Con el venv activo:
python -c "
import streamlit
import google.genai
import docling
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('GOOGLE_API_KEY')
print('✅ Streamlit:', streamlit.__version__)
print('✅ google-genai: OK')
print('✅ Docling: OK')
print('✅ GOOGLE_API_KEY:', '***' + key[-6:] if key else '❌ NO ENCONTRADA')
"
```

---

## ❗ Problemas Frecuentes

### `ModuleNotFoundError: No module named 'X'`
El entorno virtual no está activo o la dependencia no se instaló:
```bash
.\venv\Scripts\Activate.ps1   # Activar venv
pip install -r requirements.txt
```

### `GOOGLE_API_KEY not found` o error de autenticación
El archivo `.env` no existe o está en el directorio incorrecto. Debe estar en la **raíz del proyecto**, junto a `app.py`.

### Error al instalar `torch` en Windows
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Error de PowerShell: `ejecución de scripts está deshabilitada`
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### `streamlit: command not found` tras instalar
Asegúrate de que el venv está activo. Si el problema persiste:
```bash
python -m streamlit run app.py
```

---

## 📁 Estructura Completa del Proyecto (Estado Actual)

```
TFG.-llm-paper-auditor/
├── .env                         ← Tú lo creas con tus API Keys (no en el repo)
├── requirements.txt             ← Dependencias de Python (Docling, Google GenAI, etc.)
├── venv/                        ← Entorno virtual local (no en el repo)
├── app.py                       ← Punto de entrada principal (Streamlit)
├── SETUP.md                     ← Esta guía de instalación
├── ARQUITECTURA_SKILLS.md       ← Documentación de la arquitectura de Skills
├── AUDITOR_WORKFLOW.md          ← Documentación del pipeline del auditor NeurIPS
├── SOTA_WORKFLOW.md             ← Documentación del pipeline del agente SOTA
├── code of ethics.md            ← NeurIPS Code of Ethics oficial (leído por el auditor)
├── criterios NeurIPS 2026.md    ← Checklist NeurIPS 2026 oficial de referencia
├── frontend/
│   ├── config.py                ← Títulos y assets (ej: "Nature Auditor Pro")
│   ├── assets/
│   │   └── logo.png             ← Imagen del logo
│   ├── styles/
│   │   └── custom_css.py        ← Estilos y paletas premium de la UI
│   ├── utils/
│   │   ├── scoring.py           ← Lógica de health scoring para el checklist
│   │   ├── session_state.py     ← Inicialización del estado de Streamlit
│   │   └── system_config.py     ← Silenciado de warnings de librerías
│   └── components/
│       ├── audit_results.py     ← Visualización de tabla e informes de auditoría
│       ├── chatbot.py           ← Chatbot de preguntas sobre el paper
│       ├── file_uploader.py     ← Subida de documentos e inicio automático
│       ├── header.py            ← Cabecera de la UI
│       ├── loader.py            ← Pantalla de carga animada inicial
│       ├── phase_tracker.py     ← Componente visual de fases en tiempo real
│       ├── sidebar.py           ← Barra lateral informativa
│       └── sota_section.py      ← Dashboard SOTA, clustering y filtros
├── backend/
│   ├── common/
│   │   ├── config.py            ← Configuración centralizada de modelos y parámetros
│   │   ├── llm_client.py        ← Cliente Gemini con reintentos y control de 503/429
│   │   ├── logger.py            ← Configuración de logs unificada
│   │   ├── neurips_criteria.py  ← Criterios del checklist en texto literal
│   │   └── prompt_engine.py     ← Motor de carga e interpolación de prompts .md
│   ├── prompts/
│   │   ├── auditor/
│   │   │   ├── 1. map_extraction.md
│   │   │   ├── 2. reduce_extraction.md
│   │   │   ├── 3a. section_mapping.md
│   │   │   ├── 3c. evaluation_high_context.md
│   │   │   └── item_rules/      ← Reglas detalladas para los 16 ítems
│   │   ├── chatbot/
│   │   │   └── conversational.md
│   │   └── sota/
│   │       ├── 1. thematic.md
│   │       ├── 2. query_generation.md
│   │       ├── 3. gap_analysis.md
│   │       └── 4. cross_validation.md
│   ├── services/
│   │   ├── auditor.py           ← Orquestador PaperAuditor (5 fases)
│   │   ├── chatbot.py           ← Orquestador PaperChatbot
│   │   ├── pdf_parser.py        ← Ingesta de PDFs mediante bloques con Docling
│   │   └── sota_analyzer.py     ← Orquestador SotaAnalyzer (clustering/ranking)
│   └── skills/
│       ├── __init__.py          ← Exportador de skills
│       ├── base_skill.py        ← Clase base BaseSkill con logging/validación
│       ├── auditor_skills.py    ← Las 5 habilidades del agente auditor
│       ├── chatbot_skills.py    ← Las 2 habilidades del chatbot interactivo
│       ├── sota_skills.py       ← Las 6 habilidades de análisis literario SOTA
│       └── clustering_skill.py  ← Habilidad local de embeddings y KMeans SOTA
└── tests/                       ← Suite de tests (imports, splitters, integración, etc.)
```

---

_Guía generada para el TFG: LLM Paper Auditor — NeurIPS 2026 Compliance System._
