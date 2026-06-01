import os
import json
import re

def main():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(workspace_dir, "backend")
    prompts_dir = os.path.join(backend_dir, "prompts", "auditor")
    item_rules_dir = os.path.join(prompts_dir, "item_rules")
    
    print(f"Workspace: {workspace_dir}")
    print(f"Backend: {backend_dir}")
    print(f"Prompts: {prompts_dir}")
    print(f"Item rules: {item_rules_dir}")

    # 1. Load Prompts
    prompts = {}
    try:
        prompts['map_extraction'] = open(os.path.join(prompts_dir, "1. map_extraction.md"), "r", encoding="utf-8").read()
        prompts['reduce_extraction'] = open(os.path.join(prompts_dir, "2. reduce_extraction.md"), "r", encoding="utf-8").read()
        prompts['section_mapping'] = open(os.path.join(prompts_dir, "3a. section_mapping.md"), "r", encoding="utf-8").read()
        prompts['evaluation_high_context'] = open(os.path.join(prompts_dir, "3c. evaluation_high_context.md"), "r", encoding="utf-8").read()
    except Exception as e:
        print(f"Error reading prompts: {e}")

    # 2. Load Item Rules
    item_rules = {}
    if os.path.exists(item_rules_dir):
        for f_name in os.listdir(item_rules_dir):
            if f_name.endswith(".md"):
                item_key = f_name[:-3]
                try:
                    content = open(os.path.join(item_rules_dir, f_name), "r", encoding="utf-8").read()
                    item_rules[item_key] = content.strip()
                except Exception as e:
                    print(f"Error reading rule for {item_key}: {e}")

    # 3. Load NeurIPS Criteria Literals from neurips_criteria.py
    criteria_literals = {}
    criteria_file = os.path.join(backend_dir, "common", "neurips_criteria.py")
    if os.path.exists(criteria_file):
        try:
            content = open(criteria_file, "r", encoding="utf-8").read()
            matches = re.findall(r'"([a-z_0-9]+)"\s*:\s*"""(.*?)"""', content, re.DOTALL)
            for k, v in matches:
                criteria_literals[k] = v.strip()
            
            matches_single = re.findall(r'"([a-z_0-9]+)"\s*:\s*"([^"]+)"', content)
            for k, v in matches_single:
                if k not in criteria_literals:
                    criteria_literals[k] = v.strip()
        except Exception as e:
            print(f"Error parsing neurips_criteria.py: {e}")

    # 4. Extract Python Code Snippets
    code_snippets = {}
    
    auditor_py = os.path.join(backend_dir, "services", "auditor.py")
    if os.path.exists(auditor_py):
        try:
            content = open(auditor_py, "r", encoding="utf-8").read()
            init_match = re.search(r'def __init__\(self\):.*?(self\.phases = \[.*?\])', content, re.DOTALL)
            if init_match:
                code_snippets['auditor_init'] = init_match.group(1).strip()
            
            audit_match = re.search(r'def audit\(self, paper_text, status_callback=None\):.*?return final_result', content, re.DOTALL)
            if audit_match:
                code_snippets['auditor_audit'] = audit_match.group(0).strip()
        except Exception as e:
            print(f"Error reading auditor.py: {e}")

    skills_py = os.path.join(backend_dir, "skills", "auditor_skills.py")
    if os.path.exists(skills_py):
        try:
            content = open(skills_py, "r", encoding="utf-8").read()
            skills = [
                ("InformationExtractionSkill", "extraction_skill"),
                ("SectionMappingSkill", "mapping_skill"),
                ("NeurIPSComplianceSkill", "compliance_skill"),
                ("MetricsCalculationSkill", "metrics_skill"),
                ("MetadataAggregationSkill", "metadata_skill")
            ]
            for class_name, key in skills:
                pattern = rf'class {class_name}\(BaseSkill\):.*?def execute\(self, context: Dict\[str, Any\]\) -> Dict\[str, Any\]:(.*?)(?=class |\Z)'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    code_snippets[key] = f"def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:" + match.group(1)
        except Exception as e:
            print(f"Error reading auditor_skills.py: {e}")

    prompt_engine_py = os.path.join(backend_dir, "common", "prompt_engine.py")
    if os.path.exists(prompt_engine_py):
        try:
            content = open(prompt_engine_py, "r", encoding="utf-8").read()
            match = re.search(r'def get_extraction_assistance_helps\(info: dict\) -> dict:.*?(?=def |\Z)', content, re.DOTALL)
            if match:
                code_snippets['assistance_helps'] = match.group(0).strip()
        except Exception as e:
            print(f"Error reading prompt_engine.py: {e}")

    data = {
        'prompts': prompts,
        'item_rules': item_rules,
        'criteria_literals': criteria_literals,
        'code_snippets': code_snippets
    }

    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeurIPS 2026 Paper Auditor - Diagrama de Flujo Interactivo</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Prism.js Syntax Highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    
    <style>
        :root {
            --bg-dark: #0b0f19;
            --bg-card: rgba(17, 24, 39, 0.7);
            --bg-card-hover: rgba(31, 41, 55, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.3);
            
            --primary: #6366f1; /* Indigo */
            --primary-glow: rgba(99, 102, 241, 0.4);
            --secondary: #10b981; /* Emerald */
            --secondary-glow: rgba(16, 185, 129, 0.4);
            --accent: #a855f7; /* Purple */
            --accent-glow: rgba(168, 85, 247, 0.4);
            --info: #3b82f6; /* Blue */
            
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --text-accent: #818cf8;
            
            --transition-speed: 0.3s;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }

        header {
            padding: 2rem 4rem;
            border-bottom: 1px solid var(--border-color);
            background: rgba(11, 15, 25, 0.8);
            backdrop-filter: blur(12px);
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-title h1 {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.8rem;
            background: linear-gradient(to right, #818cf8, #a855f7, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }

        .header-title p {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        .badge-container {
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }

        .badge {
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            padding: 0.3rem 0.8rem;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .badge.emerald {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
        }
        
        .badge.purple {
            background: rgba(168, 85, 247, 0.15);
            border: 1px solid rgba(168, 85, 247, 0.3);
            color: #c084fc;
        }

        main {
            max-width: 1600px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
        }

        @media (min-width: 1200px) {
            main {
                grid-template-columns: 45% 55%;
                align-items: start;
            }
        }

        /* CARD CONTENEDORA GENERAL */
        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            backdrop-filter: blur(16px);
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            transition: all var(--transition-speed) ease;
        }

        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.12);
        }

        .card-header-section {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header-section h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* PIPELINE VISUAL SYSTEM */
        .pipeline-container {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            position: relative;
        }

        .pipeline-connector {
            position: absolute;
            left: 28px;
            top: 20px;
            bottom: 20px;
            width: 3px;
            background: linear-gradient(to bottom, var(--primary), var(--accent), var(--secondary));
            opacity: 0.4;
            z-index: 0;
        }

        .flow-node {
            display: flex;
            gap: 1.25rem;
            z-index: 1;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .flow-node:hover {
            transform: translateX(6px);
        }

        .node-icon-circle {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: #1e293b;
            border: 2px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            flex-shrink: 0;
            transition: all var(--transition-speed) ease;
            position: relative;
        }

        .flow-node.active .node-icon-circle {
            background: var(--primary);
            border-color: #818cf8;
            box-shadow: 0 0 15px var(--primary-glow);
            color: white;
        }

        .flow-node.phase-1_5.active .node-icon-circle {
            background: var(--accent);
            border-color: #c084fc;
            box-shadow: 0 0 15px var(--accent-glow);
        }

        .flow-node.phase-2.active .node-icon-circle {
            background: var(--secondary);
            border-color: #34d399;
            box-shadow: 0 0 15px var(--secondary-glow);
        }

        .node-content-card {
            flex-grow: 1;
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            transition: all var(--transition-speed) ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .flow-node.active .node-content-card {
            background: rgba(99, 102, 241, 0.08);
            border-color: rgba(99, 102, 241, 0.35);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.05);
        }

        .flow-node.phase-1_5.active .node-content-card {
            background: rgba(168, 85, 247, 0.08);
            border-color: rgba(168, 85, 247, 0.35);
        }

        .flow-node.phase-2.active .node-content-card {
            background: rgba(16, 185, 129, 0.08);
            border-color: rgba(16, 185, 129, 0.35);
        }

        .node-content-card h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .node-content-card p {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }

        .node-phase-tag {
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--primary);
        }
        
        .flow-node.phase-1_5 .node-phase-tag {
            color: var(--accent);
        }
        
        .flow-node.phase-2 .node-phase-tag {
            color: var(--secondary);
        }

        /* DETAILS INSPECTOR PANEL */
        .inspector-panel {
            min-height: 600px;
            display: flex;
            flex-direction: column;
        }

        .inspector-title-area {
            margin-bottom: 1.5rem;
        }

        .inspector-title-area h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: white;
        }

        .inspector-title-area p {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }

        /* NAVIGATION TABS */
        .tabs-header {
            display: flex;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.25rem;
            margin-bottom: 1.5rem;
        }

        .tab-btn {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.6rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .tab-btn:hover {
            color: white;
            background: rgba(255, 255, 255, 0.04);
        }

        .tab-btn.active {
            color: white;
            background: var(--primary);
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
        }

        .tab-pane {
            display: none;
            animation: fadeIn 0.35s ease;
        }

        .tab-pane.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* TECHNICAL BLOCKS & SCHEMAS */
        .tech-summary-box {
            background: rgba(15, 23, 42, 0.4);
            border-left: 3px solid var(--primary);
            border-radius: 0 8px 8px 0;
            padding: 1rem;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }

        .tech-io-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
            margin-bottom: 1.5rem;
        }

        @media (min-width: 768px) {
            .tech-io-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        .io-card {
            background: rgba(15, 23, 42, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
        }

        .io-card h4 {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-accent);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .io-card ul {
            list-style: none;
            font-size: 0.85rem;
        }

        .io-card ul li {
            margin-bottom: 0.3rem;
            display: flex;
            justify-content: space-between;
        }

        .io-card ul li span.key {
            color: var(--text-muted);
            font-family: 'Fira Code', monospace;
        }
        
        .io-card ul li span.type {
            color: #f43f5e;
            font-size: 0.75rem;
        }

        /* CODE VIEW WINDOWS */
        .code-window-header {
            background: #1e293b;
            border: 1px solid var(--border-color);
            border-bottom: none;
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .code-window-header .dots {
            display: flex;
            gap: 6px;
        }

        .code-window-header .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.15);
        }

        .code-window-header .dot.red { background: #ef4444; }
        .code-window-header .dot.yellow { background: #f59e0b; }
        .code-window-header .dot.green { background: #10b981; }

        .code-window-body {
            position: relative;
            margin-bottom: 1.5rem;
        }

        pre[class*="language-"] {
            margin: 0;
            border-radius: 0 0 8px 8px;
            max-height: 480px;
            font-size: 0.85rem !important;
            font-family: 'Fira Code', monospace !important;
        }

        code[class*="language-"] {
            font-family: 'Fira Code', monospace !important;
        }

        /* EXPLORADOR DE CRITERIOS CHECKLIST */
        .checklist-explorer-section {
            grid-column: 1 / -1;
            margin-top: 1rem;
        }

        .explorer-grid {
            display: grid;
            grid-template-columns: 15% 85%;
            gap: 1.5rem;
            margin-top: 1rem;
            border-top: 1px solid var(--border-color);
            padding-top: 1.5rem;
            min-height: 400px;
        }

        @media (max-width: 992px) {
            .explorer-grid {
                grid-template-columns: 1fr;
            }
        }

        .explorer-sidebar {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 0.5rem;
        }

        /* Custom Scrollbar for sidebar */
        .explorer-sidebar::-webkit-scrollbar {
            width: 4px;
        }
        .explorer-sidebar::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }

        .item-selector-btn {
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.6rem 0.8rem;
            border-radius: 8px;
            cursor: pointer;
            text-align: left;
            font-size: 0.8rem;
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .item-selector-btn:hover {
            color: white;
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.15);
        }

        .item-selector-btn.active {
            color: white;
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.1);
        }

        .item-display-card {
            background: rgba(15, 23, 42, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .item-display-title {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
        }

        .item-display-title h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: white;
        }

        .criteria-box-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-accent);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.4rem;
        }

        .criteria-literal-box {
            background: rgba(30, 41, 59, 0.25);
            border-left: 3px solid var(--accent);
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.9rem;
            color: #cbd5e1;
        }

        .criteria-rule-box {
            background: rgba(30, 41, 59, 0.25);
            border-left: 3px solid var(--secondary);
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.9rem;
            color: #cbd5e1;
            font-family: 'Inter', sans-serif;
        }

        .criteria-help-box {
            background: rgba(99, 102, 241, 0.03);
            border: 1px solid rgba(99, 102, 241, 0.15);
            padding: 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-family: 'Fira Code', monospace;
            color: #c084fc;
        }

        .empty-explorer {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            color: var(--text-muted);
            gap: 1rem;
        }

        .empty-explorer svg {
            width: 48px;
            height: 48px;
            stroke: var(--text-muted);
            opacity: 0.5;
        }
        
        .footer {
            margin-top: 4rem;
            padding: 2rem 4rem;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-muted);
            font-size: 0.8rem;
            background: rgba(11, 15, 25, 0.9);
        }

        /* SVG flow connectors */
        .svg-icon {
            width: 1.2rem;
            height: 1.2rem;
            fill: currentColor;
            vertical-align: middle;
        }

        /* SCREENSHOT TFG CAPTURE VIEW */
        .tfg-capture-view {
            display: none;
            max-width: 950px;
            margin: 1.5rem auto;
            background: #ffffff !important;
            color: #1e293b !important;
            padding: 2.5rem;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            font-family: 'Inter', sans-serif;
        }

        .tfg-capture-view h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            color: #0f172a;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
            font-weight: 800;
        }

        .tfg-flow-step {
            display: flex;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            margin-bottom: 1.25rem;
            overflow: hidden;
            background: #f8fafc;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            border-left: 5px solid #0f172a;
        }

        .tfg-step-num {
            width: 55px;
            background: #0f172a;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            flex-shrink: 0;
        }

        .tfg-step-details {
            padding: 1rem 1.25rem;
            flex-grow: 1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
        }

        .tfg-step-header {
            grid-column: 1 / -1;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 0.4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tfg-step-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
        }

        .tfg-step-tech {
            font-size: 0.75rem;
            font-weight: 600;
            background: #e2e8f0;
            color: #334155;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }

        .tfg-step-io {
            display: flex;
            flex-direction: column;
        }

        .tfg-io-title {
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            margin-bottom: 0.15rem;
        }

        .tfg-io-content {
            font-size: 0.8rem;
            color: #334155;
            line-height: 1.4;
        }

        .tfg-step-desc {
            grid-column: 1 / -1;
            font-size: 0.8rem;
            color: #475569;
            background: #ffffff;
            padding: 0.6rem 0.8rem;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            line-height: 1.45;
        }

        body.capture-mode {
            background: #f1f5f9 !important;
            background-image: none !important;
            color: #1e293b !important;
        }

        /* CAPTURE FORMAT SELECTOR */
        .tfg-selector-bar {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px dashed #cbd5e1;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #475569;
        }
        .tfg-selector-bar span {
            font-weight: 600;
            margin-right: 0.5rem;
        }
        .tfg-btn {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: #334155;
            padding: 0.45rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            outline: none;
        }
        .tfg-btn:hover {
            background: #e2e8f0;
        }
        .tfg-btn.active {
            background: #4f46e5;
            color: #ffffff;
            border-color: #4f46e5;
        }
        
        .tfg-canvas {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 1.5rem;
        }

        /* TABLE VIEW */
        .tfg-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
            color: #1e293b;
            margin-top: 1rem;
        }
        .tfg-table th {
            background: #f8fafc;
            color: #0f172a;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            border-bottom: 2px solid #cbd5e1;
            border-top: 1px solid #e2e8f0;
            padding: 0.75rem 0.5rem;
            text-align: left;
        }
        .tfg-table td {
            border-bottom: 1px solid #e2e8f0;
            padding: 0.85rem 0.5rem;
            vertical-align: top;
            line-height: 1.45;
        }
        .tfg-table tr:nth-child(even) {
            background: #f8fafc;
        }
        .tfg-table-fase {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 0.95rem;
            color: #0f172a;
        }
        .tfg-table-tech {
            font-size: 0.7rem;
            font-weight: 600;
            background: #e2e8f0;
            color: #334155;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            display: inline-block;
            margin-top: 0.25rem;
            text-transform: uppercase;
        }

        /* HORIZONTAL FLOW DIAGRAM */
        .tfg-horizontal-flow {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
        }
        .tfg-h-step {
            flex: 1 1 calc(33.33% - 1rem);
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background: #f8fafc;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }
        @media (min-width: 900px) {
            .tfg-h-step {
                flex: 1 1 calc(16.6% - 1rem);
            }
        }
        .tfg-h-step-header {
            color: #ffffff;
            padding: 0.5rem;
            text-align: center;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 0.9rem;
        }
        .tfg-h-step-body {
            padding: 0.75rem;
            font-size: 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            flex-grow: 1;
        }
        .tfg-h-step-title {
            font-weight: 700;
            color: #0f172a;
            font-size: 0.8rem;
            line-height: 1.2;
        }
        .tfg-h-step-desc {
            color: #475569;
            font-size: 0.7rem;
            line-height: 1.35;
        }
        .tfg-h-step-io {
            border-top: 1px dashed #cbd5e1;
            padding-top: 0.4rem;
            margin-top: auto;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        .tfg-h-step-io-title {
            font-weight: 700;
            font-size: 0.65rem;
            text-transform: uppercase;
            color: #64748b;
            letter-spacing: 0.02em;
        }
        .tfg-h-step-io-content {
            font-size: 0.65rem;
            color: #334155;
            line-height: 1.2;
        }
    </style>
</head>
<body>

    <header>
        <div class="header-title">
            <h1>🔬 NeurIPS 2026 Paper Auditor</h1>
            <p>Diagrama de Arquitectura de Flujo & Orquestación de Agente</p>
        </div>
        <div class="badge-container">
            <button class="badge purple" onclick="toggleCaptureMode()" id="capture_mode_btn" style="cursor: pointer; outline: none;">📸 Modo Captura TFG</button>
            <span class="badge">Pipeline de 5 Fases</span>
            <span class="badge emerald">Gemini 3.5 Flash</span>
        </div>
    </header>

    <!-- SIMPLE SCHEME FOR SCREENSHOTS (TFG MEMORY) -->
    <div class="tfg-capture-view" id="tfg_capture_view">
        <div class="tfg-selector-bar">
            <span>Esquema para TFG:</span>
            <button class="tfg-btn active" onclick="switchTfgView('table', this)">📋 Tabla Resumen</button>
            <button class="tfg-btn" onclick="switchTfgView('diagram', this)">🗺️ Diagrama Horizontal</button>
            <button class="tfg-btn" onclick="switchTfgView('cards', this)">🗂️ Lista de Fases</button>
        </div>
        
        <div class="tfg-canvas" id="tfg_canvas">
            <h2 style="margin-top: 0; margin-bottom: 1.5rem; text-align: center; border-bottom: 2px solid #0f172a; padding-bottom: 0.5rem; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.5rem; color: #0f172a;">
                Esquema de Fases del Auditor (Memoria TFG)
            </h2>
            
            <!-- VIEW 1: TABLE VIEW (DEFAULT) -->
            <div id="tfg_view_table" class="tfg-sub-view">
                <table class="tfg-table">
                    <thead>
                        <tr>
                            <th style="width: 15%;">Fase / Módulo</th>
                            <th style="width: 25%;">Entradas (Inputs)</th>
                            <th style="width: 35%;">Proceso Clave y Metodología</th>
                            <th style="width: 25%;">Salidas (Outputs)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 0</div>
                                <div class="tfg-table-tech">Docling Parser</div>
                            </td>
                            <td>PDF, TXT o Markdown original del paper.</td>
                            <td>Lectura mediante Docling (IBM), parseo jerárquico acelerado por GPU (CUDA) y segmentación por encabezados.</td>
                            <td>Markdown estructurado y diccionario de secciones.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 1</div>
                                <div class="tfg-table-tech">Gemini Map-Reduce</div>
                            </td>
                            <td>Secciones estructuradas del texto del paper.</td>
                            <td>Fase MAP: extracción atómica de parámetros de entrenamiento, hardware, datos y software. Fase REDUCE: consolidación unificada y triage de validez científica.</td>
                            <td>Master Extracted JSON y triage (ML/AI).</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 1.5</div>
                                <div class="tfg-table-tech">Context Router</div>
                            </td>
                            <td>Títulos del paper e ítems checklist NeurIPS.</td>
                            <td>Enrutador LLM inteligente que mapea cada uno de los 16 ítems del checklist a las secciones granulares de texto crudo del paper.</td>
                            <td>JSON de Mapeo (Ítem ➔ Secciones asociadas).</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 2</div>
                                <div class="tfg-table-tech">Gemini CoT Batches</div>
                            </td>
                            <td>Master JSON, Mapeo de Secciones, Reglas locales y Ayudas precalculadas.</td>
                            <td>Orquestación en 8 batches de 2 ítems (pares High Context). Inyección de reglas específicas y Chain-of-Thought para veredicto preciso.</td>
                            <td>Checklist evaluado (16 ítems) con justificación y ayudas.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 3</div>
                                <div class="tfg-table-tech">Métricas Python</div>
                            </td>
                            <td>Texto del paper y temporizadores del sistema.</td>
                            <td>Cálculo exacto determinista del tiempo de ejecución total y volumen de caracteres analizados del artículo.</td>
                            <td>Métricas de rendimiento.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 4</div>
                                <div class="tfg-table-tech">Consolidación</div>
                            </td>
                            <td>Checklist evaluado, Métricas y Master JSON.</td>
                            <td>Fusión final de datos aplicando heurísticas de justificación (un "No" sin justificación del autor genera alerta de Desk Reject).</td>
                            <td>JSON Maestro Final con Veredicto unificado (Valid / Desk Reject Risk).</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- VIEW 2: HORIZONTAL DIAGRAM -->
            <div id="tfg_view_diagram" class="tfg-sub-view" style="display: none;">
                <div class="tfg-horizontal-flow">
                    <!-- STEP 0 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #6366f1;">Fase 0</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Ingesta</span>
                            <span class="tfg-h-step-desc">Docling (IBM) segmenta el PDF jerárquicamente.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">PDF, TXT, MD</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Markdown + Secciones</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 1 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #4f46e5;">Fase 1</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Extracción Map-Reduce</span>
                            <span class="tfg-h-step-desc">Gemini extrae parámetros, hardware, datos y triage.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Texto del paper</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Master Extracted JSON</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 1.5 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #a855f7;">Fase 1.5</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Mapeo Contexto</span>
                            <span class="tfg-h-step-desc">Router asocia ítems del checklist a secciones.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Títulos e ítems checklist</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">JSON Mapeo Ítem-Texto</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 2 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #10b981;">Fase 2</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Evaluación Batches</span>
                            <span class="tfg-h-step-desc">LLM evalúa 8 batches bajo reglas específicas.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Mapeo, Reglas, Ayudas</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Checklist de 16 ítems</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 3 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #3b82f6;">Fase 3</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Métricas</span>
                            <span class="tfg-h-step-desc">Mide tiempo exacto y volumen de caracteres.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Paper & Cronómetro</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Tiempo (s), Volumen</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 4 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #6b7280;">Fase 4</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Consolidación</span>
                            <span class="tfg-h-step-desc">Aplica heurística de justificación y veredicto.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Checklist + Métricas</span>
                                <span class="tfg-h-step-io-content">OUT</span>
                                <span class="tfg-h-step-io-content">JSON Maestro Final</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- VIEW 3: DETAILED CARDS -->
            <div id="tfg_view_cards" class="tfg-sub-view" style="display: none;">
                <!-- STEP 0 -->
                <div class="tfg-flow-step" style="border-left-color: #6366f1;">
                    <div class="tfg-step-num" style="background: #6366f1;">0</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 0: Ingesta y Preprocesamiento</span>
                            <span class="tfg-step-tech">Docling Parser (IBM)</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Artículos científicos en formato PDF, TXT o MD.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Texto estructurado en Markdown y Diccionario de Secciones (Título ➔ Texto crudo).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Lectura del documento mediante Docling, con detección automática y aceleración por GPU (CUDA) si está disponible, y segmentación en Python basada en encabezados para mantener la coherencia espacial y estructura jerárquica del paper.
                        </div>
                    </div>
                </div>

                <!-- STEP 1 -->
                <div class="tfg-flow-step" style="border-left-color: #4f46e5;">
                    <div class="tfg-step-num" style="background: #4f46e5;">1</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 1: Extracción General (InformationExtractionSkill)</span>
                            <span class="tfg-step-tech">Gemini (Map-Reduce)</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Texto estructurado del paper.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Master Extracted JSON y comprobación de validez científica (ML/AI Triage).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Fragmentación lógica de secciones (Fase MAP) para extraer hechos atómicos mediante LLM y posterior unificación global (Fase REDUCE) para consolidar hiperparámetros, hardware, datos y software sin pérdida de contexto.
                        </div>
                    </div>
                </div>

                <!-- STEP 1.5 -->
                <div class="tfg-flow-step" style="border-left-color: #a855f7;">
                    <div class="tfg-step-num" style="background: #a855f7;">1.5</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 1.5: Mapeo de Contexto (SectionMappingSkill)</span>
                            <span class="tfg-step-tech">Gemini (Context Router)</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Títulos de secciones e ítems del checklist de NeurIPS 2026.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">JSON de mapeo de contexto (Ítem ➔ Lista de secciones relevantes).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Enrutamiento inteligente de contexto. Asocia cada uno de los 16 ítems con las secciones de texto crudo correspondientes (priorizando subsecciones granulares) para inyectar solo la información relevante en la posterior evaluación.
                        </div>
                    </div>
                </div>

                <!-- STEP 2 -->
                <div class="tfg-flow-step" style="border-left-color: #10b981;">
                    <div class="tfg-step-num" style="background: #10b981;">2</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 2: Evaluación NeurIPS (NeurIPSComplianceSkill)</span>
                            <span class="tfg-step-tech">Gemini + Reglas Dinámicas</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Master JSON, Mapeo de Secciones, Texto crudo de secciones y Reglas por Item.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Checklist de Cumplimiento (16 ítems evaluados con justificación detallada y helps).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Agrupación en 8 batches de 2 ítems (pares High Context). Carga dinámica de reglas locales de <code>item_rules/</code>, inyección de ayudas precalculadas en Python y del texto real mapeado para un razonamiento en cadena (CoT) y veredicto preciso.
                        </div>
                    </div>
                </div>

                <!-- STEP 3 -->
                <div class="tfg-flow-step" style="border-left-color: #3b82f6;">
                    <div class="tfg-step-num" style="background: #3b82f6;">3</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 3: Consolidación de Métricas (MetricsCalculationSkill)</span>
                            <span class="tfg-step-tech">Lógica Python (Determinista)</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Texto completo del paper y tiempo total de ejecución.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Métricas de rendimiento (tiempo en segundos y caracteres leídos).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Medición exacta del tiempo de procesamiento total y conteo del volumen de caracteres analizados del artículo científico para auditoría de eficiencia del sistema.
                        </div>
                    </div>
                </div>

                <!-- STEP 4 -->
                <div class="tfg-flow-step" style="border-left-color: #6b7280;">
                    <div class="tfg-step-num" style="background: #6b7280;">4</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 4: Consolidación y Veredicto (MetadataAggregationSkill)</span>
                            <span class="tfg-step-tech">Lógica Python / Heurísticas</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Checklist evaluado, Métricas y Master JSON.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">JSON Maestro Final con Veredicto unificado (Valid / Desk Reject Risk).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Aplicación de la heurística de transparencia. Un "No" solo se acepta si el autor proporciona una justificación en el paper (<code>is_no_justified: true</code>). En caso de tener "No"s sin justificación del autor, se determina riesgo de rechazo de escritorio.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <main>
        <!-- LEFT COLUMN: PIPELINE NODES -->
        <section class="glass-card">
            <div class="card-header-section">
                <h2>
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 3.99L19.53 19H4.47L12 5.99zM13 16h-2v2h2v-2zm0-6h-2v4h2v-4z"/></svg>
                    Pipeline de Ejecución Secuencial
                </h2>
                <span style="color: var(--text-muted); font-size: 0.8rem;">Haz clic en una fase para inspeccionarla</span>
            </div>
            
            <div class="pipeline-container">
                <div class="pipeline-connector"></div>
                
                <!-- NODE 0 -->
                <div class="flow-node active" onclick="selectPhase('phase0')" id="node_phase0">
                    <div class="node-icon-circle">0</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Ingesta</span>
                        <h3>Docling Parser & Segmenter <span class="badge">GPU (CUDA)</span></h3>
                        <p>Parseo del PDF y segmentación por encabezados lógicos en secciones crudas.</p>
                    </div>
                </div>

                <!-- NODE 1 -->
                <div class="flow-node" onclick="selectPhase('phase1')" id="node_phase1">
                    <div class="node-icon-circle">1</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 1</span>
                        <h3>Extracción General (Map-Reduce)</h3>
                        <p>Fases MAP & REDUCE mediante LLM para extraer hechos detallados del paper.</p>
                    </div>
                </div>

                <!-- NODE 1.5 -->
                <div class="flow-node phase-1_5" onclick="selectPhase('phase1_5')" id="node_phase1_5">
                    <div class="node-icon-circle">1.5</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 1.5</span>
                        <h3>Mapeo Inteligente (Context Routing)</h3>
                        <p>El Router vincula los 16 ítems del checklist con las secciones de texto crudo correspondientes.</p>
                    </div>
                </div>

                <!-- NODE 2 -->
                <div class="flow-node phase-2" onclick="selectPhase('phase2')" id="node_phase2">
                    <div class="node-icon-circle">2</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 2</span>
                        <h3>Evaluación de Cumplimiento (Pares High Context)</h3>
                        <p>Llamadas agrupadas de 2 en 2 inyectando texto real del paper + reglas específicas del ítem.</p>
                    </div>
                </div>

                <!-- NODE 3 -->
                <div class="flow-node" onclick="selectPhase('phase3')" id="node_phase3">
                    <div class="node-icon-circle">3</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 3</span>
                        <h3>Consolidación de Métricas</h3>
                        <p>Cálculo matemático del tiempo de ejecución total y velocidad de procesamiento de caracteres.</p>
                    </div>
                </div>

                <!-- NODE 4 -->
                <div class="flow-node" onclick="selectPhase('phase4')" id="node_phase4">
                    <div class="node-icon-circle">4</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 4</span>
                        <h3>Informe Final y Veredicto</h3>
                        <p>Health scoring, veredicto final (Desk Reject Risk vs Válido) y agregación de metadatos.</p>
                    </div>
                </div>

            </div>
        </section>

        <!-- RIGHT COLUMN: DETAILS INSPECTOR -->
        <section class="glass-card inspector-panel">
            <div class="inspector-title-area">
                <h2 id="inspector_title">Fase 0: Ingesta y Preprocesamiento</h2>
                <p id="inspector_description">Docling Parser parsea y segmenta el documento.</p>
            </div>

            <div class="tabs-header">
                <button class="tab-btn active" onclick="switchTab('tab_flow', this)">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                    Flujo y Datos
                </button>
                <button class="tab-btn" onclick="switchTab('tab_prompt', this)" id="tab_prompt_btn">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                    Plantillas (.md)
                </button>
                <button class="tab-btn" onclick="switchTab('tab_code', this)">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
                    Código (.py)
                </button>
            </div>

            <!-- TAB 1: FLOW AND DATA -->
            <div id="tab_flow" class="tab-pane active">
                <div class="tech-summary-box" id="tech_summary">
                    Carga inicial del PDF.
                </div>
                
                <div class="tech-io-grid">
                    <div class="io-card">
                        <h4>Entradas (Input)</h4>
                        <ul id="tech_inputs">
                            <li><span>Ninguno</span></li>
                        </ul>
                    </div>
                    <div class="io-card">
                        <h4>Salidas (Output)</h4>
                        <ul id="tech_outputs">
                            <li><span>Ninguno</span></li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- TAB 2: PROMPT TEMPLATE -->
            <div id="tab_prompt" class="tab-pane">
                <div class="code-window-header">
                    <div class="dots">
                        <div class="dot red"></div>
                        <div class="dot yellow"></div>
                        <div class="dot green"></div>
                    </div>
                    <span id="prompt_filename">prompt.md</span>
                </div>
                <div class="code-window-body">
                    <pre><code class="language-markdown" id="prompt_code">// Cargar prompt...</code></pre>
                </div>
            </div>

            <!-- TAB 3: CODE SNIPPET -->
            <div id="tab_code" class="tab-pane">
                <div class="code-window-header">
                    <div class="dots">
                        <div class="dot red"></div>
                        <div class="dot yellow"></div>
                        <div class="dot green"></div>
                    </div>
                    <span id="code_filename">skill.py</span>
                </div>
                <div class="code-window-body">
                    <pre><code class="language-python" id="python_code">// Cargar código...</code></pre>
                </div>
            </div>
        </section>

        <!-- CHECKLIST EXPLORER SECTION -->
        <section class="glass-card checklist-explorer-section">
            <div class="card-header-section">
                <h2>
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                    Explorador de Reglas de Cumplimiento (Checklist NeurIPS 2026)
                </h2>
                <span style="color: var(--text-muted); font-size: 0.8rem;">Inspecciona las reglas y descripciones oficiales de cada uno de los 16 ítems</span>
            </div>

            <div class="explorer-grid">
                <div class="explorer-sidebar" id="explorer_sidebar">
                    <!-- Dinamizado por javascript -->
                </div>
                <div class="item-display-card" id="item_display_card">
                    <div class="empty-explorer">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                        <span>Selecciona un ítem de la izquierda para ver su detalle de auditoría.</span>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div>TFG - LLM Scientific Paper Auditor (NeurIPS 2026)</div>
        <div>Visualización Interactiva © 2026</div>
    </footer>

    <!-- Prism JS for syntax highlighting -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markdown.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>

    <script>
        // Inyección de datos recopilados por Python
        const data = __INJECTED_DATA__;

        const phasesConfig = {
            phase0: {
                title: "Fase 0: Ingesta y Preprocesamiento",
                description: "Docling Parser y Segmentación de Secciones en Python",
                summary: "En este paso inicial, se lee el archivo del artículo (PDF, TXT o MD). Si es un PDF, la librería **Docling (IBM)** lo procesa utilizando aceleración por GPU (CUDA) si está disponible para extraer el texto estructurado en Markdown. Posteriormente, la lógica en Python segmenta el texto crudo utilizando los encabezados lógicos (#, ##) creados por Docling.",
                inputs: [
                    { key: "paper_text (PDF/TXT/MD)", type: "Archivo crudo" }
                ],
                outputs: [
                    { key: "paper_text", type: "string" },
                    { key: "paper_sections", type: "Dictionary [Título -> Texto Crudo]" }
                ],
                prompt: null,
                codeFile: "backend/services/pdf_parser.py",
                codeSnippet: `def parse_pdf(file_path):\\n    # Lógica de Docling Parser\\n    # Detecta GPU/CUDA y parsea el archivo a Markdown\\n    ...`
            },
            phase1: {
                title: "Fase 1: Extracción General (InformationExtractionSkill)",
                description: "Procesamiento de texto con Map-Reduce",
                summary: "Debido a la gran longitud de los papers, el sistema utiliza un enfoque Map-Reduce para evitar pérdidas de contexto y desbordamiento de ventanas de tokens:\\n1. **Fase MAP**: El texto se divide en fragmentos lógicos. Cada fragmento se envía de forma concurrente/secuencial al LLM para extraer hechos locales en un JSON atómico.\\n2. **Fase REDUCE**: Un LLM consolida las extracciones en un único JSON maestro (Master Extracted JSON) resolviendo contradicciones y garantizando cero pérdida de información.",
                inputs: [
                    { key: "paper_text", type: "string" },
                    { key: "paper_sections", type: "Dictionary" }
                ],
                outputs: [
                    { key: "extracted_info", type: "Master JSON" },
                    { key: "map_steps", type: "Array of JSONs" },
                    { key: "reduce_step", type: "JSON" }
                ],
                prompt: "map_extraction", // custom loader keys
                codeFile: "backend/skills/auditor_skills.py -> InformationExtractionSkill",
                codeSnippet: data.code_snippets.extraction_skill || ""
            },
            phase1_5: {
                title: "Fase 1.5: Mapeo de Secciones (SectionMappingSkill)",
                description: "Indexador y Enrutador de Contexto Inteligente",
                summary: "Esta fase actúa como un router inteligente. Recibe todos los títulos de secciones extraídos de Docling y los mapea a cada uno de los 16 ítems de la lista de verificación NeurIPS 2026. Utiliza un LLM para asociar, por ejemplo, '4.1 Data Collection' al ítem 'crowdsourcing_human_subjects'. Aplica una regla de granularidad para seleccionar subsecciones específicas en lugar de títulos principales genéricos, evitando inyectar ruido innecesario en la posterior evaluación.",
                inputs: [
                    { key: "paper_sections", type: "Dictionary [Títulos]" }
                ],
                outputs: [
                    { key: "section_mapping", type: "JSON [Item -> [Títulos]]" }
                ],
                prompt: "section_mapping",
                codeFile: "backend/skills/auditor_skills.py -> SectionMappingSkill",
                codeSnippet: data.code_snippets.mapping_skill || ""
            },
            phase2: {
                title: "Fase 2: Evaluación NeurIPS Contextual (NeurIPSComplianceSkill)",
                description: "Evaluación exhaustiva por pares de ítems (Pares High Context)",
                summary: "Es el motor crítico de la auditoría. Evalúa los 16 ítems agrupándolos de 2 en 2 (8 llamadas en total). En cada llamada, se inyectan en el prompt:\\n- El JSON resumido maestro (Fase 1).\\n- Las pistas precalculadas de ayuda (Helps).\\n- El **texto crudo** de las secciones mapeadas para esos ítems en la Fase 1.5.\\n- **Únicamente las 2 reglas de validación específicas** asociadas a esos dos ítems (cargadas desde item_rules/). Esto previene alucinaciones y focaliza la atención del LLM.",
                inputs: [
                    { key: "extracted_info", type: "Master JSON" },
                    { key: "section_mapping", type: "JSON" },
                    { key: "paper_sections", type: "Dictionary" }
                ],
                outputs: [
                    { key: "evaluation", type: "JSON [Checklist de 16 Items]" },
                    { key: "evaluation_helps", type: "JSON [Pistas de Ayuda]" }
                ],
                prompt: "evaluation_high_context",
                codeFile: "backend/skills/auditor_skills.py -> NeurIPSComplianceSkill",
                codeSnippet: data.code_snippets.compliance_skill || ""
            },
            phase3: {
                title: "Fase 3: Consolidación de Métricas (MetricsCalculationSkill)",
                description: "Cálculo determinista de rendimiento y volumen de datos",
                summary: "Ejecuta cálculos deterministas en Python (sin llamadas de LLM) para medir las estadísticas del proceso de auditoría científica:\\n- Calcula el tiempo de ejecución en segundos que le ha llevado a todas las fases procesar el paper.\\n- Registra el tamaño total en caracteres analizados del paper científico parseado.",
                inputs: [
                    { key: "paper_text", type: "string" },
                    { key: "execution_time", type: "float (seconds)" }
                ],
                outputs: [
                    { key: "metrics", type: "JSON {tiempo_segundos, caracteres_leidos}" }
                ],
                prompt: null,
                codeFile: "backend/skills/auditor_skills.py -> MetricsCalculationSkill",
                codeSnippet: data.code_snippets.metrics_skill || ""
            },
            phase4: {
                title: "Fase 4: Consolidación y Veredicto (MetadataAggregationSkill)",
                description: "Generación de resultado final e informe maestro",
                summary: "Fase de cierre que empaqueta todo el contexto recolectado y determina el veredicto final. Implementa la lógica de 'Health Scoring' y Veredicto NeurIPS:\\n- **Checklist Válido (🟢)**: Si todos los ítems marcados como 'No' tienen una justificación explícita de los autores ('is_no_justified': true).\\n- **Desk Reject Risk (🔴)**: Si hay ítems marcados como 'No' que no están justificados por el autor, constituyendo un riesgo de rechazo de escritorio por falta de transparencia.",
                inputs: [
                    { key: "evaluation", type: "JSON" },
                    { key: "metrics", type: "JSON" },
                    { key: "extracted_info", type: "JSON" }
                ],
                outputs: [
                    { key: "Master Final JSON", type: "JSON completo" }
                ],
                prompt: null,
                codeFile: "backend/skills/auditor_skills.py -> MetadataAggregationSkill",
                codeSnippet: data.code_snippets.metadata_skill || ""
            }
        };

        let currentActivePhase = 'phase0';
        let currentActiveTab = 'tab_flow';

        function toggleCaptureMode() {
            const isCapture = document.body.classList.toggle('capture-mode');
            const mainNode = document.querySelector('main');
            const footerNode = document.querySelector('footer');
            const tfgNode = document.getElementById('tfg_capture_view');
            const headerNode = document.querySelector('header');
            
            if (isCapture) {
                mainNode.style.display = 'none';
                footerNode.style.display = 'none';
                tfgNode.style.display = 'block';
                document.getElementById('capture_mode_btn').innerText = "🌙 Modo Interactivo";
                headerNode.style.background = '#ffffff';
                headerNode.style.borderBottom = '1px solid #cbd5e1';
                headerNode.querySelector('h1').style.background = 'none';
                headerNode.querySelector('h1').style.webkitTextFillColor = '#0f172a';
                headerNode.querySelector('p').style.color = '#64748b';
            } else {
                mainNode.style.display = '';
                footerNode.style.display = '';
                tfgNode.style.display = 'none';
                document.getElementById('capture_mode_btn').innerText = "📸 Modo Captura TFG";
                headerNode.style.background = '';
                headerNode.style.borderBottom = '';
                headerNode.querySelector('h1').style.background = '';
                headerNode.querySelector('h1').style.webkitTextFillColor = '';
                headerNode.querySelector('p').style.color = '';
            }
        }

        function switchTfgView(viewType, btnElement) {
            // Hide all sub-views inside the TFG canvas
            document.querySelectorAll('.tfg-sub-view').forEach(view => {
                view.style.display = 'none';
            });
            // Show the selected sub-view
            document.getElementById(`tfg_view_${viewType}`).style.display = 'block';
            
            // Remove active class from all selector buttons
            document.querySelectorAll('.tfg-selector-bar .tfg-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            // Add active class to clicked button
            btnElement.classList.add('active');
        }

        function selectPhase(phaseKey) {
            currentActivePhase = phaseKey;
            
            // Update active states in DOM list
            document.querySelectorAll('.flow-node').forEach(node => {
                node.classList.remove('active');
            });
            document.getElementById(`node_${phaseKey}`).classList.add('active');

            // Update Inspector Panel Title & Descriptions
            const config = phasesConfig[phaseKey];
            document.getElementById('inspector_title').innerText = config.title;
            document.getElementById('inspector_description').innerText = config.description;

            // 1. Update Flow tab contents
            document.getElementById('tech_summary').innerHTML = config.summary.replace(/\\n/g, '<br>');
            
            const inputsList = document.getElementById('tech_inputs');
            inputsList.innerHTML = '';
            config.inputs.forEach(inp => {
                inputsList.innerHTML += `<li><span class="key">${inp.key}</span><span class="type">${inp.type}</span></li>`;
            });

            const outputsList = document.getElementById('tech_outputs');
            outputsList.innerHTML = '';
            config.outputs.forEach(out => {
                outputsList.innerHTML += `<li><span class="key">${out.key}</span><span class="type">${out.type}</span></li>`;
            });

            // 2. Update Prompt tab contents
            const promptBtn = document.getElementById('tab_prompt_btn');
            if (config.prompt) {
                promptBtn.style.display = 'flex';
                let promptFilename = "";
                let promptContent = "";
                if (config.prompt === "map_extraction") {
                    promptFilename = "1. map_extraction.md";
                    promptContent = data.prompts.map_extraction || "";
                } else if (config.prompt === "reduce_extraction") {
                    promptFilename = "2. reduce_extraction.md";
                    promptContent = data.prompts.reduce_extraction || "";
                } else if (config.prompt === "section_mapping") {
                    promptFilename = "3a. section_mapping.md";
                    promptContent = data.prompts.section_mapping || "";
                } else if (config.prompt === "evaluation_high_context") {
                    promptFilename = "3c. evaluation_high_context.md";
                    promptContent = data.prompts.evaluation_high_context || "";
                }
                
                document.getElementById('prompt_filename').innerText = promptFilename;
                document.getElementById('prompt_code').textContent = promptContent;
            } else {
                promptBtn.style.display = 'none';
                if (currentActiveTab === 'tab_prompt') {
                    // Switch to flow tab if prompt tab is hidden
                    const flowBtn = document.querySelector('.tab-btn');
                    switchTab('tab_flow', flowBtn);
                }
            }

            // 3. Update Code tab contents
            document.getElementById('code_filename').innerText = config.codeFile;
            document.getElementById('python_code').textContent = config.codeSnippet;

            // Re-apply Prism syntax highlighting
            Prism.highlightAll();
        }

        function switchTab(tabId, btnElement) {
            currentActiveTab = tabId;
            
            // Update active states of tab buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            btnElement.classList.add('active');

            // Hide/Show tab panes
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');
        }

        // Checklist Items metadata
        const checklistItems = [
            { key: 'claims', label: '1. Claims' },
            { key: 'limitations', label: '2. Limitations' },
            { key: 'theory_assumptions_proofs', label: '3. Theory & Proofs' },
            { key: 'experimental_result_reproducibility', label: '4. Reproducibility' },
            { key: 'open_access_data_code', label: '5. Open Access' },
            { key: 'experimental_setting_details', label: '6. Experimental Setting' },
            { key: 'experiment_statistical_significance', label: '7. Statistical Significance' },
            { key: 'experiments_compute_resource', label: '8. Compute Resources' },
            { key: 'code_of_ethics', label: '9. Code Of Ethics' },
            { key: 'broader_impacts', label: '10. Broader Impacts' },
            { key: 'safeguards', label: '11. Safeguards' },
            { key: 'licenses', label: '12. Licenses' },
            { key: 'assets', label: '13. Assets' },
            { key: 'crowdsourcing_human_subjects', label: '14. Crowdsourcing' },
            { key: 'irb_approvals', label: '15. IRB Approvals' },
            { key: 'declaration_llm_usage', label: '16. LLM Usage' }
        ];

        // Renders the checklist items sidebar in the explorer section
        function setupChecklistExplorer() {
            const sidebar = document.getElementById('explorer_sidebar');
            sidebar.innerHTML = '';

            checklistItems.forEach(item => {
                sidebar.innerHTML += `
                    <button class="item-selector-btn" id="btn_item_${item.key}" onclick="selectChecklistItem('${item.key}')">
                        ${item.label}
                    </button>
                `;
            });
        }

        // Pre-computed help logic snippets mapping for visualization
        const helpLogicMap = {
            experimental_result_reproducibility: `// Lógica de Ayuda (helps['reproducibility'])
// Detecta presencia de URLs de repositorios de código y pesos de modelos
CODE/MODEL URLS: {url_str}. WEIGHTS: {weights}.
NeurIPS Rule: If ANY code/model URL is present, answer 'Yes'.
If NO code/URL is found, answer 'No' and set is_no_justified: false.`,
            open_access_data_code: `// Lógica de Ayuda (helps['open_access'])
// Busca si existen conjuntos de datos públicos
DATA/RESOURCE URLS: {url_str}.
If ANY public URL (project, demo, HF, github) exists -> 'Yes'.
If only private/proprietary mentioned -> 'No' and set is_no_justified: true ONLY if they explain why.`,
            experiment_statistical_significance: `// Lógica de Ayuda (helps['statistics'])
// Busca intervalos de confianza, p-values, número de corridas
CI/Variance: {ci}, Significance Tests: {st}, Runs: {runs}. {greedy_note}
Rule: If NO intervals/variance/runs found -> answer 'No' and set is_no_justified: false.
EXCEPTIONAL RULE: For deterministic LLM benchmarks, 'Yes' is acceptable if greedy decoding is used.`,
            experiments_compute_resource: `// Lógica de Ayuda (helps['compute_resource'])
// Busca hardware, clusters de cómputo y métricas de consumo ambiental (CO2)
DETECTED hardware/cluster: {hw_str}.
CRITICAL RULE: If ANY hardware, cluster, or CO2 emissions are mentioned -> answer 'Yes'.
If hardware is mentioned but BOTH time and efficiency/CO2 are missing -> 'No'.`,
            licenses: `// Lógica de Ayuda (helps['licenses'])
// Detecta nombres de licencias de software/recursos (MIT, Apache, CC)
LICENSES FOUND: {lic_found}.
Rule: If NO specific license (MIT, Apache, CC) is named -> answer 'No' and set is_no_justified: false.`,
            crowdsourcing_human_subjects: `// Lógica de Ayuda (helps['crowdsourcing'])
// Identifica datos de feedback humano, RLHF, MTurk, compensación
USES HUMAN/PREFERENCE DATA: {uses_human_flag}, COMP: {comp}.
Rule: If human-derived data is used, Items 14/15 MUST be addressed (Yes/No).
N/A is ONLY for purely algorithmic papers with NO human data interaction.`
        };

        function selectChecklistItem(itemKey) {
            // Update active sidebar buttons
            document.querySelectorAll('.item-selector-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(`btn_item_${itemKey}`).classList.add('active');

            const item = checklistItems.find(i => i.key === itemKey);
            const literal = data.criteria_literals[itemKey] || "Literal oficial de NeurIPS 2026 no encontrado.";
            const rule = data.item_rules[itemKey] || "Regla de validación CoT específica no definida.";
            const helpLogic = helpLogicMap[itemKey] || "// No se requiere pre-cálculo de ayudas computadas en Python para este ítem.\\n// Se valida directamente mediante LLM a partir de los fragmentos de texto crudo.";

            const displayCard = document.getElementById('item_display_card');
            displayCard.innerHTML = `
                <div class="item-display-title">
                    <h3>${item.label} (${itemKey})</h3>
                    <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3);">Checklist Criterio</span>
                </div>
                
                <div>
                    <div class="criteria-box-title">Criterio NeurIPS 2026 Oficial (Pregunta Literal)</div>
                    <div class="criteria-literal-box">${literal}</div>
                </div>

                <div>
                    <div class="criteria-box-title">Instrucciones de Auditoría CoT (item_rules/${itemKey}.md)</div>
                    <div class="criteria-rule-box">${rule.replace(/\\n/g, '<br>')}</div>
                </div>

                <div>
                    <div class="criteria-box-title">Ayudas & Lógica de Soporte Python (Fase 1 -> Fase 2)</div>
                    <pre><code class="language-python">${helpLogic}</code></pre>
                </div>
            `;
            Prism.highlightAll();
        }

        // Initialize view
        window.addEventListener('DOMContentLoaded', () => {
            selectPhase('phase0');
            setupChecklistExplorer();
        });
    </script>
</body>
</html>"""

    # Inject data as a json object
    injected_data_json = json.dumps(data, ensure_ascii=False, indent=2)
    html_output = html_template.replace("const data = __INJECTED_DATA__;", f"const data = {injected_data_json};")

    output_path = os.path.join(workspace_dir, "diagrama_auditor.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"Success! Diagram generated at: {output_path}")
    except Exception as e:
        print(f"Error writing output HTML: {e}")

if __name__ == "__main__":
    main()
