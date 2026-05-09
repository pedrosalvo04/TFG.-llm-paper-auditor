"""Skills especializados para detección de patrones específicos mediante regex"""
import re
from typing import Any, Dict, List, Optional, Tuple
from backend.skills.base_skill import BaseSkill


# ── Negation-aware matching ──────────────────────────────────────────────────
NEGATION_WINDOW = 60  # chars before the match to inspect

NEGATION_PATTERNS = re.compile(
    r"(?:no\s+se\s+(?:especifica|menciona|indica|reporta|incluye|proporciona|detalla))"
    r"|(?:falta(?:n)?(?:\s+informaci[oó]n)?)"
    r"|(?:sin\s+(?:especificar|detallar|mencionar|incluir|reportar|proporcionar))"
    r"|(?:not\s+(?:specified|mentioned|reported|provided|included|disclosed|found))"
    r"|(?:missing|absent|omitted|lacks?|without)"
    r"|(?:ERROR\s*\d*\s*:)",
    re.IGNORECASE,
)


def _is_negated(text: str, match_start: int) -> bool:
    """Return True if the match sits inside a negation context."""
    window_start = max(0, match_start - NEGATION_WINDOW)
    preceding = text[window_start:match_start]
    return bool(NEGATION_PATTERNS.search(preceding))


def _search_with_negation(
    pattern: str, text: str, flags: int = re.IGNORECASE
) -> Optional[re.Match]:
    """Search for *pattern* in *text*, skipping matches in negation contexts."""
    for m in re.finditer(pattern, text, flags):
        if not _is_negated(text, m.start()):
            return m
    return None


class TableExtractionHelper:
    """Helper para extraer y procesar contenido de tablas"""
    
    @staticmethod
    def extract_tables(text: str) -> List[str]:
        """Extrae contenido de tablas del texto, normalizando HTML tags"""
        tables = []
        
        # Patrón 1: Tablas con formato "Table X:" o "Table X."
        table_pattern = r"(Table|Tab\.)\s+\d+[:\.]?[^\n]*\n([\s\S]{0,2000}?)(?=\n\s*\n|Table|Tab\.|\Z)"
        matches = re.finditer(table_pattern, text, re.IGNORECASE)
        for match in matches:
            # Normalizar <br> tags a espacios para que los regex matcheen valores
            raw = match.group(0)
            normalized = re.sub(r'<br\s*/?>', ' ', raw)
            tables.append(normalized)
        
        # Patrón 2: Bloques con múltiples "|" (formato markdown/latex)
        pipe_table_pattern = r"(\|[^\n]+\|\n){3,}"
        matches = re.finditer(pipe_table_pattern, text)
        for match in matches:
            raw = match.group(0)
            normalized = re.sub(r'<br\s*/?>', ' ', raw)
            tables.append(normalized)
        
        # Patrón 3: Líneas con tabulaciones múltiples
        tab_table_pattern = r"([^\n]+\t[^\n]+\t[^\n]+\n){3,}"
        matches = re.finditer(tab_table_pattern, text)
        for match in matches:
            tables.append(match.group(0))
        
        return tables
    
    @staticmethod
    def extract_table_rows(table_text: str) -> List[str]:
        """Extrae filas individuales de una tabla"""
        # Limpiar y dividir por líneas
        lines = table_text.split('\n')
        rows = []
        
        for line in lines:
            # Ignorar líneas vacías o separadores
            if line.strip() and not re.match(r'^[\s\-\|=]+$', line):
                rows.append(line)
        
        return rows


class HyperparameterDetectionSkill(BaseSkill):
    """Detecta hiperparámetros de entrenamiento ML"""
    
    PATTERNS = {
        'optimizer': [
            r"(?:we\s+use|using|with)\s+(?:the\s+)?(AdamW|Adam|SGD|RMSprop|Adagrad|LAMB|LARS)\s*(?:optimizer)?",
            r"optimizer[:\s=]+\s*(AdamW|Adam|SGD|RMSprop|LAMB)",
            r"(AdamW|Adam|SGD|RMSprop|LAMB)\s+optimizer",
        ],
        'learning_rate': [
            r"learning\s+rate.{0,20}(?:is|of|at)?\s*([\d\.e\-×\^]+)",
            r"(?:LR|lr)\s*[:=]\s*([\d\.e\-×\^]+)",
            r"learning\s+rate\s+is\s+linearly\s+increased\s+from\s+0\s+to\s+([\d\.e\-×\^]+)",
            r"rate\s+of\s+([\d\.e\-]+)"
        ],
        'batch_size': [
            r"(?:batch[\s_-]size|global[\s_-]batch|micro[\s-]?batch)[\s:=]+.{0,20}(\d{2,})",
            r"(\d{2,})\s*(?:samples?|examples?)\s*per\s*(?:batch|GPU)",
        ],
        'epochs': [
            r"(?:trained?\s+for|over)\s+(\d+)\s*(?:epochs?)",
            r"(?:epochs?)[\s:=]+(\d+)",
            r"(\d+)\s*(?:epochs?)",
        ],
        'training_steps': [
            r"(?:trained?\s+for|over)\s+([\d,]+)\s*(?:steps?|iterations?)",
            r"(?:training[\s_-]steps?|iterations?)[\s:=]+([\d,]+)",
            r"([\d,]+)\s*(?:training\s+steps|iterations?)",
        ],
        'warmup': [
            r"warmup[\s:=]+(\d+)",
            r"(\d+)\s*warmup\s*steps?",
            r"warm[\s-]?up.{0,20}(?:of|for|=|:)\s*(\d+)",
            r"Warmup-Stable-Decay"
        ],
        'weight_decay': [
            r"(?:weight[\s_-]decay|\$\\lambda\$|L2[\s_-]regularization)[\s:=,]+.{0,30}(\d+\.\d+)",
            r"(?:decay|wd)\s*[=:]\s*(\d+\.\d+)",
            r"(?:weight.decay|regularization)\s+(?:of|is|coefficient)\s+(\d+\.\d+)",
        ],
        'betas': [
            r"(?:\$\\beta_[12]\$|beta[\s_-]?[12]|betas?)[\s:=,]+.{0,30}\d+\.\d+",
            r"\(\s*(?:β|beta)?\s*0\.9\d*\s*,\s*0\.9\d*\s*\)",
            r"(?:momentum|beta)\s+(?:coefficients?|parameters?).{0,40}\d+\.\d+",
        ],
        'epsilon': [
            r"(?:epsilon|\$\\epsilon\$|eps)[\s:=]+(\d+\.?\d*[eE][-+]?\d+)",
            r"(\d+\.\d+[eE][-+]?\d+).{0,20}(?:epsilon|numerical[\s_-]stability)",
        ],
        'vague': [
            r"(?:standard\s+settings|default\s+parameters|typical\s+configuration|not\s+disclosed|internal\s+experimentation|cannot\s+be\s+disclosed|hyperparameters?\s+(?:were\s+)?(?:not\s+)?tuned)",
        ]
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        results = {}
        
        # Extraer tablas primero
        tables = TableExtractionHelper.extract_tables(text)
        table_text = '\n'.join(tables)
        
        self.log_execution(f"=== HYPERPARAMETER DETECTION (NEGATION-AWARE) ===")
        self.log_execution(f"📋 Extrajimos {len(tables)} tablas para búsqueda prioritaria")
        
        for key, patterns in self.PATTERNS.items():
            found = False
            matched_snippet = None
            search_location = None
            
            for i, pattern in enumerate(patterns):
                # PRIORIDAD 1: tablas (no aplica negación en tablas numéricas)
                if table_text:
                    match = re.search(pattern, table_text, re.IGNORECASE)
                    if match:
                        found = True
                        matched_snippet = match.group(0)[:100]
                        search_location = "TABLE"
                        self.log_execution(f"✅ {key} (p{i+1}) [TABLA]: '{matched_snippet}'")
                        break
                
                # PRIORIDAD 2: texto completo CON filtro de negación
                match = _search_with_negation(pattern, text)
                if match:
                    found = True
                    matched_snippet = match.group(0)[:100]
                    search_location = "TEXT"
                    self.log_execution(f"✅ {key} (p{i+1}) [TEXTO]: '{matched_snippet}'")
                    break
            
            if not found:
                self.log_execution(f"❌ {key}: NOT FOUND ({len(patterns)} patterns, negation-filtered)")
            
            results[f'has_{key}'] = found
            if found and key != 'vague' and matched_snippet:
                results[f'{key}_value'] = matched_snippet
                results[f'{key}_location'] = search_location
        
        missing = [k.replace('has_', '') for k, v in results.items() if k.startswith('has_') and not v and k != 'has_vague']
        self.log_execution(f"📊 RESUMEN: {len(missing)} hiperparámetros faltantes: {missing}")
        
        return {'hyperparameter_flags': results}


class DataAvailabilityDetectionSkill(BaseSkill):
    """Detecta disponibilidad de datos"""
    
    PATTERNS = {
        'proprietary': r"(our|the|this)\s+(proprietary|confidential|internal|restricted)\s+.{0,50}(data|dataset)|cannot\s+(disclose|release|share)\s+.{0,30}(data|dataset)|data.{0,30}(not\s+(publicly\s+)?available|remain\s+confidential)",
        'available': r"(available\s+at|download|DOI|zenodo|figshare|huggingface\.co/datasets|github\.com/.+/data|data\s+is\s+released)",
        'doi': r"DOI[\s:]+.{0,20}(dataset|data)",
        'cannot_release': r"cannot\s+(release|disclose|share)\s+.{0,30}(data|dataset)"
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        
        self.log_execution("=== DATA AVAILABILITY DETECTION ===")
        found_matches = {}
        for key, patterns in self.PATTERNS.items():
            if isinstance(patterns, str):
                patterns = [patterns]
            
            found = False
            for pat in patterns:
                match = re.search(pat, text, re.IGNORECASE)
                if match:
                    found = True
                    snippet = match.group(0)[:80]
                    self.log_execution(f"✅ {key}: FOUND - '{snippet}...'")
                    break
            
            if not found:
                self.log_execution(f"❌ {key}: NOT FOUND")
            found_matches[key] = found
        
        results = {
            'datos_propietarios': found_matches.get('proprietary', False),
            'datos_sin_acceso': not found_matches.get('available', False),
            'tiene_doi_datos': found_matches.get('doi', False),
            'cannot_release_data': found_matches.get('cannot_release', False)
        }
        
        self.log_execution(f"📊 RESUMEN: propietarios={results['datos_propietarios']}, sin_acceso={results['datos_sin_acceso']}")
        return {'data_flags': results}


class CodeAvailabilityDetectionSkill(BaseSkill):
    """Detecta disponibilidad de código"""
    
    PATTERNS = {
        'proprietary': r"(proprietary|confidential|cannot\s+(disclose|release|share)|not\s+(publicly\s+)?available|internal|competitive\s+concerns?)\s+.{0,80}(code|implementation|source|repository|training\s+code)|restricted\s+(?!to\s+a\s+(computational|budget)).{0,50}(code|implementation|source|repository)",
        'repository': [
            r"(?:https?://)?(?:www\.)?(github|gitlab|bitbucket|sourceforge)\.(?:com|org)/[\w.-]+/[\w.-]+",
            r"github\.com/[\w.-]+",
            r"[\w.-]+\.github\.io",
            r"(?:huggingface\.co|hf\.co)/[\w.-]+/",
            r"project\s+page\s+at\s+(https?://\S+)",
            r"code\s+(?:available|released)\s+at\s+(https?://\S+)"
        ],
        'github': r"github\.com/[\w.-]+",
        'cannot_release': r"cannot\s+(release|disclose|share)\s+.{0,30}(code|implementation)"
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        
        self.log_execution("=== CODE AVAILABILITY DETECTION ===")
        found_matches = {}
        for key, patterns in self.PATTERNS.items():
            if isinstance(patterns, str):
                patterns = [patterns]
            
            found = False
            for pat in patterns:
                match = re.search(pat, text, re.IGNORECASE)
                if match:
                    found = True
                    snippet = match.group(0)[:80]
                    self.log_execution(f"✅ {key}: FOUND - '{snippet}...'")
                    break
            
            if not found:
                self.log_execution(f"❌ {key}: NOT FOUND")
            found_matches[key] = found
        
        results = {
            'codigo_propietario': found_matches.get('proprietary', False),
            'sin_repositorio': not found_matches.get('repository', False),
            'tiene_github': found_matches.get('github', False),
            'cannot_release_code': found_matches.get('cannot_release', False)
        }
        
        self.log_execution(f"📊 RESUMEN: propietario={results['codigo_propietario']}, sin_repo={results['sin_repositorio']}")
        return {'code_flags': results}


class StatisticsDetectionSkill(BaseSkill):
    """Detecta información estadística"""
    
    PATTERNS = {
        'confidence_intervals': [
            r"(confidence\s+interval|standard\s+deviation|std\.?\s+dev|error\s+bar|±|\+/-|variance|std\s+err)",
            r"CI\s*=\s*\d+",
            r"\d+\.\d+\s*±\s*\d+\.\d+",
            r"error\s+bars?",
            r"standard\s+errors?",
            r"confidence\s+level"
        ],
        'significance': [
            r"(p-value|p\s*<|statistical\s+significance|t-test|ANOVA|Mann-Whitney|Wilcoxon|chi-square)",
            r"p\s*=\s*\d+\.\d+",
            r"statistically\s+significant",
            r"significance\s+test",
            r"benchmarks?\s+(?:evaluation|results|performance).{0,50}(?:MMLU|GSM8K|HumanEval|ImageNet|COCO|Cityscapes|Atari|Gym|standard\s+benchmarks)"
        ],
        'multiple_runs': [
            r"(multiple\s+runs?|\d+\s+seeds?|random\s+seeds?|\d+\s+executions?|\d+\s+trials?)",
            r"repeated\s+\d+\s+times",
            r"average\s+(of|over)\s+\d+\s+(runs?|experiments?)",
            r"\d+\s+independent\s+(runs?|experiments?)",
            r"seed\s*=\s*\d+"
        ]
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        tables = TableExtractionHelper.extract_tables(text)
        table_text = '\n'.join(tables)
        
        self.log_execution("=== STATISTICS DETECTION (NEGATION-AWARE) ===")
        found_flags = {}
        
        for key, patterns in self.PATTERNS.items():
            found = False
            for i, pattern in enumerate(patterns):
                if table_text:
                    match = re.search(pattern, table_text, re.IGNORECASE)
                    if match:
                        found = True
                        self.log_execution(f"✅ {key} (p{i+1}) [TABLA]: '{match.group(0)[:80]}'")
                        break
                match = _search_with_negation(pattern, text)
                if match:
                    found = True
                    self.log_execution(f"✅ {key} (p{i+1}) [TEXTO]: '{match.group(0)[:80]}'")
                    break
            if not found:
                self.log_execution(f"❌ {key}: NOT FOUND")
            found_flags[key] = found
        
        results = {
            'sin_intervalos_confianza': not found_flags.get('confidence_intervals', False),
            'sin_significancia': not found_flags.get('significance', False),
            'sin_multiple_runs': not found_flags.get('multiple_runs', False)
        }
        
        self.log_execution(f"📊 RESUMEN: intervalos={not results['sin_intervalos_confianza']}, significancia={not results['sin_significancia']}, runs={not results['sin_multiple_runs']}")
        return {'statistics_flags': results}


class EnvironmentalImpactDetectionSkill(BaseSkill):
    """Detecta información de impacto ambiental"""
    
    PATTERNS = {
        'carbon_footprint': [
            r"(\d+\.\d+\s*tCO2eq|carbon\s+footprint|CO2\s+emissions|environmental\s+impact|Table\s+6)",
            r"carbon.{0,30}emissions?",
            r"greenhouse\s+gas",
            r"CO2.{0,30}(footprint|impact|emissions?)",
            r"environmental.{0,30}(cost|impact|footprint)"
        ],
        'energy_consumption': [
            r"(\d+\s*MWh|\d+\s*kWh|energy\s+consumption|power\s+consumption)",
            r"energy.{0,30}(usage|used|consumption)",
            r"power.{0,30}(usage|consumption|draw)",
            r"\d+.{0,20}(kilowatt|megawatt).{0,20}hours?"
        ],
        'pue': [
            r"(PUE|Power\s+Usage\s+Effectiveness)[\s:=]+.{0,20}(1\.\d+|\d+\.\d+)",
            r"efficiency.{0,30}(of|is|=|:).{0,30}\d+\.\d+",
            r"PUE\s*=\s*\d+\.\d+"
        ]
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        
        self.log_execution("=== ENVIRONMENTAL IMPACT DETECTION (MULTI-PATTERN) ===")
        found_flags = {}
        
        for key, patterns in self.PATTERNS.items():
            found = False
            if isinstance(patterns, list):
                for i, pattern in enumerate(patterns):
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        found = True
                        snippet = match.group(0)[:80]
                        self.log_execution(f"✅ {key} (pattern {i+1}/{len(patterns)}): FOUND - '{snippet}...'")
                        break
            else:
                match = re.search(patterns, text, re.IGNORECASE)
                if match:
                    found = True
                    snippet = match.group(0)[:80]
                    self.log_execution(f"✅ {key}: FOUND - '{snippet}...'")
            
            if not found:
                self.log_execution(f"❌ {key}: NOT FOUND (tried {len(patterns) if isinstance(patterns, list) else 1} patterns)")
            
            found_flags[key] = found
        
        results = {
            'tiene_carbon_footprint': found_flags.get('carbon_footprint', False),
            'tiene_energy_consumption': found_flags.get('energy_consumption', False),
            'tiene_pue': found_flags.get('pue', False)
        }
        
        self.log_execution(f"📊 RESUMEN: carbon={results['tiene_carbon_footprint']}, energy={results['tiene_energy_consumption']}, pue={results['tiene_pue']}")
        return {'environmental_flags': results}


class ProblematicPhrasesDetectionSkill(BaseSkill):
    """Detecta frases problemáticas"""
    
    PATTERNS = {
        'competitive_concerns': r"(competitive\s+concerns?|intellectual\s+property|legal\s+constraints?|business\s+reasons?)",
        'cannot_release': r"(cannot\s+(release|disclose|share)|unable\s+to\s+(release|disclose|share)|not\s+permitted\s+to)",
        'remain_confidential': r"(data|code|implementation).{0,30}(remain\s+confidential|kept\s+confidential|undisclosed)"
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        
        self.log_execution("=== PROBLEMATIC PHRASES DETECTION ===")
        for key, pattern in self.PATTERNS.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                snippet = match.group(0)[:80]
                self.log_execution(f"⚠️ {key}: FOUND - '{snippet}...'")
            else:
                self.log_execution(f"✅ {key}: NOT FOUND (good)")
        
        results = {
            'competitive_concerns': bool(re.search(self.PATTERNS['competitive_concerns'], text, re.IGNORECASE)),
            'cannot_release': bool(re.search(self.PATTERNS['cannot_release'], text, re.IGNORECASE)),
            'remain_confidential': bool(re.search(self.PATTERNS['remain_confidential'], text, re.IGNORECASE))
        }
        
        count = sum(results.values())
        self.log_execution(f"📊 RESUMEN: {count} frases problemáticas detectadas")
        return {'problematic_flags': results}


class LlmUsageDetectionSkill(BaseSkill):
    """Detecta uso de LLMs en la metodología"""
    
    PATTERNS = {
        'llm_usage': r"(ChatGPT|GPT-4|GPT-3|Claude|LLaMA|BERT|RoBERTa|T5|LLM|Large\s+Language\s+Model).{0,60}(annotat|filter|evaluat|generat|process|label)"
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        self.log_execution("=== LLM USAGE DETECTION ===")
        
        match = re.search(self.PATTERNS['llm_usage'], text, re.IGNORECASE)
        found = bool(match)
        if found:
            self.log_execution(f"✅ LLM Usage: FOUND - '{match.group(0)[:80]}...'")
        else:
            self.log_execution("❌ LLM Usage: NOT FOUND")
            
        return {'llm_usage_flags': {'usa_llm_como_herramienta': found}}


class CrowdsourcingDetectionSkill(BaseSkill):
    """Detecta el uso de anotadores humanos o crowdsourcing"""
    
    # Crowdsourcing ACTIVO: el paper mismo recluta anotadores
    # Usar lookahead negativo para excluir frases de negacion ("no human subjects", "without human annotators")
    CROWDSOURCING_ACTIVE = [
        r"(?<!no\s)(?<!without\s)(?<!not\s)\b(crowdsourc|Mechanical\s+Turk|MTurk|Prolific|Scale\s+AI)\b",
        r"\b(we\s+(?:hired|recruited|employed|paid)\s+.{0,30}(?:annotator|worker|participant))",
        r"\b(human\s+annotators?\s+(?:were|are|were\s+asked|labeled|annotated))",
        r"\b(participants?\s+(?:were\s+)?(?:recruited|compensated|paid))",
    ]
    # Uso de datasets de terceros con etiquetas humanas
    HUMAN_DATASET_USE = [
        r"\b(human[\s-]?label(?:ed|ing)|human[\s-]?annotat(?:ed|ion))\b",
        r"\b(SFT|RLHF|human\s+feedback|preference\s+data).{0,40}(?:dataset|data|corpus)",
    ]
    COMPENSATION = r"\b(compensation|wage|paid\s+(?:at|\$)|minimum\s+wage|hourly\s+rate|instructions\s+provided|consent\s+form)\b"
    # Frases de negacion de crowdsourcing
    NEGATION_CROWD = r"(?:no|not|without|does\s+not\s+use|did\s+not\s+use).{0,20}(?:human\s+subject|human\s+annotator|crowdsourc|human\s+participant)"
    
    def execute(self, context):
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        self.log_execution("=== CROWDSOURCING DETECTION ===")
        
        # Verificar primero si hay negacion explicita
        has_negation = bool(re.search(self.NEGATION_CROWD, text, re.IGNORECASE))
        
        has_active_crowd = False
        if not has_negation:
            has_active_crowd = any(
                re.search(p, text, re.IGNORECASE) for p in self.CROWDSOURCING_ACTIVE
            )
        
        has_human_dataset = any(
            re.search(p, text, re.IGNORECASE) for p in self.HUMAN_DATASET_USE
        )
        has_comp = bool(re.search(self.COMPENSATION, text, re.IGNORECASE))
        
        self.log_execution(f"negation={has_negation}, active_crowd={has_active_crowd}, human_dataset={has_human_dataset}, compensation={has_comp}")
        
        return {'crowdsourcing_flags': {
            'usa_crowdsourcing': has_active_crowd,
            'usa_datasets_humanos': has_human_dataset,
            'sin_compensacion_mencionada': has_active_crowd and not has_comp
        }}

class LicenseDetectionSkill(BaseSkill):
    """Detecta menciones a licencias de software y datos"""
    
    # Licencias nombradas explicitamente
    EXPLICIT_LICENSE = r"(CC[\s-]BY(?:[\s-]\d\.\d)?(?:[\s-](?:SA|NC|ND))*|MIT\s+[Ll]icense|Apache\s+2\.0|GPL(?:[\s-]\d)?|BSD(?:[\s-]\d[\s-][Cc]lause)?|Creative\s+Commons|\bCC0\b)"
    # Datasets conocidos que requieren citar su licencia
    KNOWN_DATASETS = r"\b(ImageNet|COCO|CIFAR|MNIST|WikiText|RedPajama|OpenWebText|Alpaca|ShareGPT|LAION|WMT\d+|SQuAD|GLUE|SuperGLUE|HumanEval|GSM8K|MMLU|CommonCrawl|BookCorpus|The\s+Pile)\b"
    
    def execute(self, context):
        if not self.validate_context(context, ['paper_text']):
            return {}
        
        text = context['paper_text']
        self.log_execution("=== LICENSE DETECTION ===")
        
        license_match = re.search(self.EXPLICIT_LICENSE, text, re.IGNORECASE)
        dataset_match = re.search(self.KNOWN_DATASETS, text, re.IGNORECASE)
        
        found_license = bool(license_match)
        uses_known_dataset = bool(dataset_match)
        
        if found_license:
            self.log_execution(f"Explicit license FOUND: '{license_match.group(0)[:60]}'")
        else:
            self.log_execution("Explicit license: NOT FOUND")
        if uses_known_dataset:
            self.log_execution(f"Known dataset FOUND: '{dataset_match.group(0)[:60]}'")
        
        return {'license_flags': {
            'menciona_licencia': found_license,
            'usa_datasets_conocidos': uses_known_dataset,
            'posible_licencia_faltante': uses_known_dataset and not found_license
        }}

class LimitationsQualityDetectionSkill(BaseSkill):
    """Detecta si la sección de limitaciones es específica o vaga"""
    
    SPECIFIC_PATTERNS = [
        r"(?:limitation|weakness).{0,60}(?:\d+|specific|quantif|measur|metric)",
        r"(?:bias|toxicity|fairness).{0,40}(?:evaluat|measur|test|audit|analyz)",
        r"(?:fail|error|degrad).{0,40}(?:when|if|under|specific|certain)",
    ]
    SECTION_PATTERN = r"(?:^|\n)\s*(?:#+\s*[\*_]{0,2}(?:Limitation|Broader\s+Impact|Conclusion|Discussion|Social\s+Impact)[\*_]{0,2}|(?:\*\*|__)Limitations?[\.\s:]|Limitations?[\.\s:])"
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        text = context['paper_text']
        self.log_execution("=== LIMITATIONS QUALITY DETECTION ===")
        
        has_section = bool(re.search(self.SECTION_PATTERN, text, re.IGNORECASE))
        specific_count = 0
        for pat in self.SPECIFIC_PATTERNS:
            if _search_with_negation(pat, text):
                specific_count += 1
        
        is_vague = has_section and specific_count == 0
        self.log_execution(f"📊 section={has_section}, specific_points={specific_count}, vague={is_vague}")
        return {'limitations_flags': {
            'tiene_seccion_limitaciones': has_section,
            'limitaciones_vagas': is_vague,
            'puntos_especificos_limitaciones': specific_count,
        }}


class SoftwareVersionDetectionSkill(BaseSkill):
    """Detecta si se reportan versiones de software/frameworks"""
    
    PATTERNS = [
        r"(?:PyTorch|TensorFlow|JAX|Keras|Transformers)\s*(?:v|version)?\s*\d+\.\d+",
        r"(?:Python|CUDA|cuDNN)\s*(?:v|version)?\s*\d+\.\d+",
        r"(?:numpy|scipy|pandas|scikit)\S*\s*(?:v|version)?\s*\d+\.\d+",
        r"requirements\.txt|environment\.yml|setup\.py|pyproject\.toml",
    ]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        text = context['paper_text']
        self.log_execution("=== SOFTWARE VERSION DETECTION ===")
        
        found_count = 0
        for pat in self.PATTERNS:
            m = _search_with_negation(pat, text)
            if m:
                found_count += 1
                self.log_execution(f"✅ version: '{m.group(0)[:60]}'")
        
        self.log_execution(f"📊 {found_count} software version mentions found")
        return {'software_flags': {
            'tiene_versiones_software': found_count > 0,
            'cantidad_versiones': found_count,
        }}


class HardwareDetailDetectionSkill(BaseSkill):
    """Detecta detalles específicos de hardware"""
    
    PATTERNS = {
        'gpu_model': [
            r"(?:A100|V100|H100|A6000|RTX\s*\d{4}|MI\d{3}|TPU\s*v\d)",
            r"(?:NVIDIA|AMD|Google)\s+(?:GPU|TPU)\s*\S+",
        ],
        'gpu_count': [
            r"(\d+)\s*(?:x\s*)?(?:GPU|TPU|A100|V100|H100)",
            r"(?:GPU|TPU)s?\s*(?:x\s*)?(\d+)",
        ],
        'gpu_memory': [
            r"(\d+)\s*GB\s*(?:GPU|VRAM|HBM|memory)",
            r"(?:GPU|VRAM|HBM)\s*(?:memory)?\s*(?:of)?\s*(\d+)\s*GB",
        ],
        'training_time': [
            r"(?:train|took|required)\S*\s+(?:for\s+)?(?:approximately\s+)?\d+\s*(?:hours?|days?|weeks?|GPU[\s-]hours?)",
            r"\d+\s*(?:GPU[\s-]hours?|GPU[\s-]days?|node[\s-]hours?)",
        ],
    }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {}
        text = context['paper_text']
        self.log_execution("=== HARDWARE DETAIL DETECTION ===")
        
        results = {}
        for key, patterns in self.PATTERNS.items():
            found = False
            for pat in patterns:
                m = _search_with_negation(pat, text)
                if m:
                    found = True
                    self.log_execution(f"✅ {key}: '{m.group(0)[:60]}'")
                    break
            if not found:
                self.log_execution(f"❌ {key}: NOT FOUND")
            results[f'tiene_{key}'] = found
        
        return {'hardware_detail_flags': results}
