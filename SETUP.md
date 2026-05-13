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
# Google AI Studio (para los modelos Gemini)
GOOGLE_API_KEY=TU_CLAVE_AQUI

# Semantic Scholar (para el análisis de estado del arte)
SEMANTIC_SCHOLAR_API_KEY=TU_CLAVE_AQUI

# OpenRouter (opcional, si se configura como backend alternativo)
OPENROUTER_API_KEY=TU_CLAVE_AQUI
```

### ¿Cómo obtener cada clave?

#### Google AI Studio (`GOOGLE_API_KEY`) — **Obligatoria**
1. Ve a [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Create API Key"**
4. Copia la clave y pégala en `.env`

> El sistema utiliza modelos de la familia Gemini. El uso gratuito tiene límites de cuota; para uso intensivo se recomienda una cuenta con facturación habilitada.

#### Semantic Scholar (`SEMANTIC_SCHOLAR_API_KEY`) — Recomendada
1. Ve a [api.semanticscholar.org](https://www.semanticscholar.org/product/api)
2. Solicita una API Key gratuita
3. La recibirás por email en unos días

> Sin esta clave, el módulo de **análisis de estado del arte (SOTA)** no funcionará, pero el auditor principal sí.

#### OpenRouter (`OPENROUTER_API_KEY`) — Opcional
Solo necesaria si el proyecto se configura para usar OpenRouter como proveedor de LLM alternativo.
1. Ve a [openrouter.ai](https://openrouter.ai/)
2. Crea una cuenta y genera una API Key

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

## 💾 Paso 5 — Carpeta de resultados (opcional)

Los informes de auditoría se guardan automáticamente en:

```
C:\Users\<TU_USUARIO>\Desktop\papers IA resultado\
```

Si la carpeta no existe, se crea automáticamente en la primera auditoría. También puedes descargar el informe manualmente desde la propia interfaz web.

---

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

## 📁 Estructura del Proyecto (tras la configuración)

```
TFG.-llm-paper-auditor/
├── .env                    ← ✋ Tú lo creas (no está en el repo)
├── requirements.txt        ← ✅ Incluido en el repo
├── venv/                   ← ✋ Tú lo creas (entorno virtual)
├── app.py                  ← Punto de entrada
├── frontend/
│   └── assets/logo.png     ← ✅ Incluido en el repo
├── backend/
│   ├── common/
│   │   ├── config.py       ← Modelos y configuración
│   │   └── prompt_engine.py
│   ├── prompts/auditor/
│   │   └── item_rules/     ← 16 reglas NeurIPS (1 .md por ítem)
│   └── services/
└── AUDITOR_WORKFLOW.md     ← Documentación técnica del pipeline
```

---

_Guía generada para el TFG: LLM Paper Auditor — NeurIPS 2026 Compliance System._
