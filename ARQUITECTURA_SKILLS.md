# Arquitectura Basada en Skills - Auditor de Papers

## 📋 Resumen Ejecutivo

Este documento describe la refactorización del sistema de auditoría de papers científicos hacia una **arquitectura basada en skills**. Esta arquitectura modular mejora la mantenibilidad, testabilidad y escalabilidad del sistema al descomponer la lógica de los agentes IA en habilidades especializadas y reutilizables.

## 🎯 Motivación

### Problemas del Código Original
- **Monolítico**: Lógica compleja concentrada en métodos grandes
- **Acoplamiento**: Difícil modificar un componente sin afectar otros
- **Testing**: Complicado probar funcionalidades individuales
- **Mantenimiento**: Código difícil de entender y modificar
- **Reutilización**: Lógica duplicada entre servicios

### Beneficios de la Nueva Arquitectura
✅ **Modularidad**: Cada skill tiene una responsabilidad única
✅ **Testabilidad**: Skills individuales son fáciles de probar
✅ **Reutilización**: Skills pueden compartirse entre servicios
✅ **Mantenibilidad**: Código más claro y fácil de modificar
✅ **Escalabilidad**: Fácil agregar nuevos skills
✅ **Trazabilidad**: Logging automático de ejecución de skills

## 🏗️ Estructura de la Arquitectura

### Jerarquía de Componentes

```
BaseSkill (Clase Abstracta)
    │
    ├── Auditor Skills
    │   ├── InformationExtractionSkill
    │   ├── SectionMappingSkill
    │   ├── NeurIPSComplianceSkill
    │   ├── MetricsCalculationSkill
    │   └── MetadataAggregationSkill
    │
    ├── Chatbot Skills
    │   ├── ConversationalResponseSkill
    │   └── ContextValidationSkill
    │
    └── SOTA Analysis Skills
        ├── ThematicCoverageSkill
        ├── QueryGenerationSkill
        ├── SemanticScholarSearchSkill
        ├── CoverageGapAnalysisSkill
        └── CrossValidationSkill
```

## 🔧 Componentes Principales

### 1. BaseSkill (Clase Base)

**Ubicación**: `backend/skills/base_skill.py`

**Responsabilidad**: Proporciona funcionalidad común a todos los skills

**Características**:
- Validación de contexto
- Logging automático de ejecución
- Manejo de errores consistente
- Interfaz uniforme (`execute()`)

**Código**:
```python
class BaseSkill:
    """Clase base para todos los skills del sistema"""
    
    def __init__(self, name=None, llm_client=None):
        self.name = name or self.__class__.__name__
        self.llm_client = llm_client
        self.logger = get_logger(f"backend.skills.{self.name}")
    
    def execute(self, context: dict) -> dict:
        """Método abstracto que debe implementar cada skill"""
        raise NotImplementedError("Subclases deben implementar execute()")
    
    def validate_context(self, context: dict, required_keys: list) -> bool:
        """Valida que el contexto tenga las claves requeridas"""
        # Implementación...
    
    def log_execution(self, context: dict, result: dict):
        """Registra la ejecución del skill"""
        # Implementación...
```

### 2. Auditor Skills

**Ubicación**: `backend/skills/auditor_skills.py`

#### InformationExtractionSkill
- **Entrada**: `paper_text`
- **Salida**: `extracted_info`, `paper_sections`
- **Función**: Map-Reduce para extraer datos técnicos e indexar el paper por secciones.
- **LLM**: ✅ Sí (Gemini 3.1 Flash Lite)

#### SectionMappingSkill [NUEVO]
- **Entrada**: `paper_sections`, `criterios_neurips`
- **Salida**: `section_mapping`
- **Función**: Mapea ítems de alto contexto a secciones específicas del paper.
- **LLM**: ✅ Sí (Gemini 3.1 Flash Lite)

#### NeurIPSComplianceSkill
- **Entrada**: `extracted_info`, `section_mapping`, `paper_sections`
- **Salida**: `evaluation`
- **Función**: Evaluación por lotes (Batch) y contextual con inyección de texto crudo.
- **LLM**: ✅ Sí (Gemini 3.1 Flash Lite)

#### MetricsCalculationSkill
- **Entrada**: `execution_time`, `caracteres`
- **Salida**: `metricas`
- **Función**: Calcula estadísticas de rendimiento.
- **LLM**: ❌ No requiere

#### MetadataAggregationSkill
- **Entrada**: Todos los resultados anteriores
- **Salida**: Resultado final agregado
- **Función**: Construye el objeto JSON maestro para el frontend.
- **LLM**: ❌ No requiere

### 3. Chatbot Skills

**Ubicación**: `backend/skills/chatbot_skills.py`

#### ConversationalResponseSkill
- **Entrada**: `paper_text`, `question`, `history_text`
- **Salida**: `response` (respuesta conversacional)
- **Función**: Genera respuestas contextuales
- **LLM**: ✅ Sí (Gemini)

#### ContextValidationSkill
- **Entrada**: `paper_text`, `question`, `history_text`
- **Salida**: `is_valid`, `error` (validación)
- **Función**: Valida que el contexto sea adecuado
- **LLM**: ❌ No requiere

### 4. SOTA Analysis Skills

**Ubicación**: `backend/skills/sota_skills.py`

#### ThematicCoverageSkill
- **Entrada**: `paper_text`
- **Salida**: `tematicas` (áreas temáticas)
- **Función**: Extrae temas del paper
- **LLM**: ✅ Sí (Gemini)

#### QueryGenerationSkill
- **Entrada**: `tematicas`
- **Salida**: `search_queries` (queries optimizadas)
- **Función**: Genera queries para búsqueda
- **LLM**: ✅ Sí (Gemini)

#### SemanticScholarSearchSkill
- **Entrada**: `search_queries`
- **Salida**: `sota_papers` (papers encontrados)
- **Función**: Busca en Semantic Scholar API
- **LLM**: ❌ No requiere (API externa)

#### CoverageGapAnalysisSkill
- **Entrada**: `tematicas`, `sota_papers`
- **Salida**: `analisis_gaps` (análisis de cobertura)
- **Función**: Compara con estado del arte
- **LLM**: ✅ Sí (Gemini)

#### CrossValidationSkill
- **Entrada**: `analisis_gaps`, `sota_papers`
- **Salida**: `validacion_cruzada` (validación)
- **Función**: Valida consistencia de resultados
- **LLM**: ✅ Sí (Gemini)

## 🔄 Flujo de Ejecución

### Auditoría de Paper (PaperAuditor)

```
1. Preparar contexto inicial
   └── context = {'paper_text': texto}

2. InformationExtractionSkill.execute(context)
   └── Extrae info y construye mapa de secciones
   └── Actualiza context con 'extracted_info' y 'paper_sections'

3. SectionMappingSkill.execute(context)
   └── Mapea ítems a secciones físicas
   └── Actualiza context con 'section_mapping'

4. NeurIPSComplianceSkill.execute(context)
   └── Evaluación Batch + High Context (Inyectada)
   └── Actualiza context con 'evaluation'

5. MetricsCalculationSkill.execute(context)
   └── Calcula métricas de rendimiento
   └── Actualiza context con 'metricas'

6. MetadataAggregationSkill.execute(context)
   └── Agrega todo en resultado final
   └── Retorna resultado completo
```

### Chatbot (PaperChatbot)

```
1. Preparar contexto
   └── context = {
       'paper_text': texto,
       'question': pregunta,
       'history_text': historial
   }

2. ContextValidationSkill.execute(context)
   └── Valida contexto
   └── Si no válido → error

3. ConversationalResponseSkill.execute(context)
   └── Genera respuesta
   └── Retorna respuesta
```

### Análisis SOTA (SotaAnalyzer)

```
1. Preparar contexto
   └── context = {'paper_text': texto}

2. ThematicCoverageSkill.execute(context)
   └── Extrae temáticas
   └── Actualiza context con 'tematicas'

3. QueryGenerationSkill.execute(context)
   └── Genera queries
   └── Actualiza context con 'search_queries'

4. SemanticScholarSearchSkill.execute(context)
   └── Busca papers
   └── Actualiza context con 'sota_papers'

5. CoverageGapAnalysisSkill.execute(context)
   └── Analiza gaps
   └── Actualiza context con 'analisis_gaps'

6. CrossValidationSkill.execute(context)
   └── Valida resultados
   └── Retorna análisis completo
```

## 📁 Estructura de Archivos

```
backend/
├── skills/
│   ├── __init__.py              # Exporta todos los skills
│   ├── base_skill.py            # Clase base BaseSkill
│   ├── auditor_skills.py        # 5 skills del auditor
│   ├── chatbot_skills.py        # 2 skills del chatbot
│   └── sota_skills.py           # 5 skills de SOTA
│
├── services/
│   ├── auditor.py               # PaperAuditor (pipeline de 5 fases)
│   ├── chatbot.py               # PaperChatbot
│   ├── sota_analyzer.py         # SotaAnalyzer
│   └── pdf_parser.py            # Docling con detección automática de GPU
│
├── common/
│   ├── config.py                # Configuraciones y modelos LLM
│   ├── llm_client.py            # Cliente LLM (Gemini)
│   ├── logger.py                # Sistema de logging
│   ├── neurips_criteria.py      # Criterios literales de NeurIPS 2026
│   └── prompt_engine.py         # Motor de prompts: carga .md + inyección dinámica
│
└── prompts/
    ├── auditor/
    │   ├── 1. map_extraction.md
    │   ├── 2. reduce_extraction.md
    │   ├── 3a. section_mapping.md
    │   ├── 3c. evaluation_high_context.md  # Plantilla base de evaluación
    │   └── item_rules/              # Reglas específicas por ítem (1 .md por ítem)
    │       ├── claims.md
    │       ├── limitations.md
    │       ├── theory_assumptions_proofs.md
    │       ├── experimental_result_reproducibility.md
    │       ├── open_access_data_code.md
    │       ├── experimental_setting_details.md
    │       ├── experiment_statistical_significance.md
    │       ├── experiments_compute_resource.md
    │       ├── code_of_ethics.md
    │       ├── broader_impacts.md
    │       ├── safeguards.md
    │       ├── licenses.md
    │       ├── assets.md
    │       ├── crowdsourcing_human_subjects.md
    │       ├── irb_approvals.md
    │       └── declaration_llm_usage.md
    ├── chatbot/
    │   └── conversational.md
    └── sota/
        ├── 1. thematic.md
        ├── 2. query_generation.md
        ├── 3. gap_analysis.md
        └── 4. cross_validation.md

tests/
├── test_skills_integration.py   # Test de integración
└── test_auditor_refactor.py     # Tests legacy
```

## 🧪 Testing

### Test de Integración

**Archivo**: `test_skills_integration.py`

**Tests Incluidos**:
1. ✅ Importación de módulos
2. ✅ Importación de servicios refactorizados
3. ✅ Inicialización de servicios
4. ✅ Verificación de estructura de skills
5. ✅ Verificación de herencia
6. ✅ Verificación de métodos base
7. ✅ Ejecución de skill simple
8. ✅ Verificación de logging

**Ejecución**:
```bash
python test_skills_integration.py
```

## 🔍 Ventajas de la Arquitectura

### 1. Separación de Responsabilidades
Cada skill tiene una única responsabilidad bien definida.

### 2. Reutilización de Código
Skills pueden ser compartidos entre diferentes servicios.

### 3. Testing Simplificado
Cada skill puede ser testeado de forma independiente.

### 4. Mantenimiento Mejorado
Cambios en un skill no afectan a otros.

### 5. Escalabilidad
Fácil agregar nuevos skills sin modificar código existente.

### 6. Trazabilidad
Logging automático de ejecución de cada skill.

### 7. Flexibilidad
Skills pueden ser combinados de diferentes maneras.

## 📊 Comparación: Antes vs Después

### Antes (Código Monolítico)

```python
class PaperAuditor:
    def audit(self, paper_text):
        # 200+ líneas de código
        # Regex + Prompts + LLM + Métricas
        # Todo en un solo método
        # Difícil de testear
        # Difícil de mantener
```

### Después (Arquitectura Skills)

```python
class PaperAuditor:
    def __init__(self):
        self.red_flag_skill = RedFlagDetectionSkill()
        self.extraction_skill = InformationExtractionSkill(llm_client)
        self.evaluation_skill = ReproducibilityEvaluationSkill(llm_client)
        self.metrics_skill = MetricsCalculationSkill()
        self.metadata_skill = MetadataAggregationSkill()
    
    def audit(self, paper_text):
        context = {'paper_text': paper_text}
        context.update(self.red_flag_skill.execute(context))
        context.update(self.extraction_skill.execute(context))
        context.update(self.evaluation_skill.execute(context))
        # ... flujo claro y modular
```

## 🚀 Cómo Extender la Arquitectura

### Agregar un Nuevo Skill

1. **Crear el Skill** en el archivo correspondiente:

```python
# backend/skills/auditor_skills.py

class NewAuditorSkill(BaseSkill):
    """Descripción del nuevo skill"""
    
    def __init__(self, llm_client=None):
        super().__init__(name="NewAuditorSkill", llm_client=llm_client)
    
    def execute(self, context: dict) -> dict:
        # Validar contexto
        if not self.validate_context(context, ['required_key']):
            return {'error': 'Contexto inválido'}
        
        # Lógica del skill
        result = self._process(context)
        
        # Logging
        self.log_execution(context, result)
        
        return result
    
    def _process(self, context: dict) -> dict:
        # Implementación específica
        pass
```

2. **Exportar en `__init__.py`**:

```python
from .auditor_skills import (
    # ... otros skills
    NewAuditorSkill
)
```

3. **Usar en el Servicio**:

```python
class PaperAuditor:
    def __init__(self):
        # ... otros skills
        self.new_skill = NewAuditorSkill(llm_client=self.llm_client)
    
    def audit(self, paper_text):
        # ... flujo existente
        new_result = self.new_skill.execute(context)
        context.update(new_result)
```

## 📈 Métricas del Sistema

### Código Refactorizado
- **12 Skills** implementados
- **1 Clase Base** (BaseSkill
