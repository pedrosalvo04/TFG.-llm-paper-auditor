# -*- coding: utf-8 -*-
"""Script para parchear las skills de crowdsourcing y licencias"""
import re

filepath = 'backend/skills/regex_detection_skills.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── Reemplazar CrowdsourcingDetectionSkill ──────────────────────────────────
crowd_start = content.index('class CrowdsourcingDetectionSkill(BaseSkill):')
license_start = content.index('class LicenseDetectionSkill(BaseSkill):')
limitations_start = content.index('class LimitationsQualityDetectionSkill(BaseSkill):')

new_crowd = '''class CrowdsourcingDetectionSkill(BaseSkill):
    """Detecta el uso de anotadores humanos o crowdsourcing"""
    
    # Crowdsourcing ACTIVO: el paper mismo recluta anotadores
    # Usar lookahead negativo para excluir frases de negacion ("no human subjects", "without human annotators")
    CROWDSOURCING_ACTIVE = [
        r"(?<!no\\s)(?<!without\\s)(?<!not\\s)\\b(crowdsourc|Mechanical\\s+Turk|MTurk|Prolific|Scale\\s+AI)\\b",
        r"\\b(we\\s+(?:hired|recruited|employed|paid)\\s+.{0,30}(?:annotator|worker|participant))",
        r"\\b(human\\s+annotators?\\s+(?:were|are|were\\s+asked|labeled|annotated))",
        r"\\b(participants?\\s+(?:were\\s+)?(?:recruited|compensated|paid))",
    ]
    # Uso de datasets de terceros con etiquetas humanas
    HUMAN_DATASET_USE = [
        r"\\b(human[\\s-]?label(?:ed|ing)|human[\\s-]?annotat(?:ed|ion))\\b",
        r"\\b(SFT|RLHF|human\\s+feedback|preference\\s+data).{0,40}(?:dataset|data|corpus)",
    ]
    COMPENSATION = r"\\b(compensation|wage|paid\\s+(?:at|\\$)|minimum\\s+wage|hourly\\s+rate|instructions\\s+provided|consent\\s+form)\\b"
    # Frases de negacion de crowdsourcing
    NEGATION_CROWD = r"(?:no|not|without|does\\s+not\\s+use|did\\s+not\\s+use).{0,20}(?:human\\s+subject|human\\s+annotator|crowdsourc|human\\s+participant)"
    
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

'''

new_license = '''class LicenseDetectionSkill(BaseSkill):
    """Detecta menciones a licencias de software y datos"""
    
    # Licencias nombradas explicitamente
    EXPLICIT_LICENSE = r"(CC[\\s-]BY(?:[\\s-]\\d\\.\\d)?(?:[\\s-](?:SA|NC|ND))*|MIT\\s+[Ll]icense|Apache\\s+2\\.0|GPL(?:[\\s-]\\d)?|BSD(?:[\\s-]\\d[\\s-][Cc]lause)?|Creative\\s+Commons|\\bCC0\\b)"
    # Datasets conocidos que requieren citar su licencia
    KNOWN_DATASETS = r"\\b(ImageNet|COCO|CIFAR|MNIST|WikiText|RedPajama|OpenWebText|Alpaca|ShareGPT|LAION|WMT\\d+|SQuAD|GLUE|SuperGLUE|HumanEval|GSM8K|MMLU|CommonCrawl|BookCorpus|The\\s+Pile)\\b"
    
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

'''

before_crowd = content[:crowd_start]
after_license = content[limitations_start:]
new_content = before_crowd + new_crowd + new_license + after_license

open(filepath, 'w', encoding='utf-8').write(new_content)

import ast
ast.parse(new_content)
print("Done. Syntax OK. Chars:", len(new_content))
