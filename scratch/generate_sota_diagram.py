import os
import json
import re

def main():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(workspace_dir, "backend")
    prompts_dir = os.path.join(backend_dir, "prompts", "sota")
    
    print(f"Workspace: {workspace_dir}")
    print(f"Backend: {backend_dir}")
    print(f"Prompts: {prompts_dir}")

    # 1. Load Prompts
    prompts = {}
    try:
        prompts['thematic'] = open(os.path.join(prompts_dir, "1. thematic.md"), "r", encoding="utf-8").read()
        prompts['query_generation'] = open(os.path.join(prompts_dir, "2. query_generation.md"), "r", encoding="utf-8").read()
        prompts['gap_analysis'] = open(os.path.join(prompts_dir, "3. gap_analysis.md"), "r", encoding="utf-8").read()
        prompts['cross_validation'] = open(os.path.join(prompts_dir, "4. cross_validation.md"), "r", encoding="utf-8").read()
    except Exception as e:
        print(f"Error reading prompts: {e}")

    # 2. Extract Python Code Snippets
    code_snippets = {}
    
    sota_py = os.path.join(backend_dir, "services", "sota_analyzer.py")
    if os.path.exists(sota_py):
        try:
            content = open(sota_py, "r", encoding="utf-8").read()
            analyze_match = re.search(r'def analyze_sota\(.*?\):.*?return final_results', content, re.DOTALL)
            if analyze_match:
                code_snippets['sota_analyze'] = analyze_match.group(0).strip()
            
            update_match = re.search(r'def update_ranking_and_reanalyze\(.*?\):.*?return final_results', content, re.DOTALL)
            if update_match:
                code_snippets['sota_update_ranking'] = update_match.group(0).strip()
        except Exception as e:
            print(f"Error reading sota_analyzer.py: {e}")

    skills_py = os.path.join(backend_dir, "skills", "sota_skills.py")
    if os.path.exists(skills_py):
        try:
            content = open(skills_py, "r", encoding="utf-8").read()
            skills = [
                ("ThematicCoverageSkill", "thematic_skill"),
                ("QueryGenerationSkill", "query_skill"),
                ("SemanticScholarSearchSkill", "search_skill"),
                ("CoverageGapAnalysisSkill", "gap_skill"),
                ("CrossValidationSkill", "validation_skill"),
                ("PaperRankingSkill", "ranking_skill")
            ]
            for class_name, key in skills:
                pattern = rf'class {class_name}\(BaseSkill\):.*?def execute\(self, context: Dict\[str, Any\]\) -> Dict\[str, Any\]:(.*?)(?=class |\Z)'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    code_snippets[key] = f"def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:" + match.group(1)
        except Exception as e:
            print(f"Error reading sota_skills.py: {e}")

    clustering_py = os.path.join(backend_dir, "skills", "clustering_skill.py")
    if os.path.exists(clustering_py):
        try:
            content = open(clustering_py, "r", encoding="utf-8").read()
            pattern = r'class PaperClusteringSkill\(BaseSkill\):.*?def execute\(self, context: Dict\[str, Any\]\) -> Dict\[str, Any\]:(.*?)(?=def _empty_result|\Z)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                code_snippets['clustering_skill'] = f"def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:" + match.group(1)
            
            naming_match = re.search(r'def _name_clusters\(self, cluster_summary: Dict\[int, Dict\]\) -> None:(.*?)(?=def _determine_n_clusters|\Z)', content, re.DOTALL)
            if naming_match:
                code_snippets['clustering_naming'] = f"def _name_clusters(self, cluster_summary: Dict[int, Dict]) -> None:" + naming_match.group(1)
        except Exception as e:
            print(f"Error reading clustering_skill.py: {e}")

    data = {
        'prompts': prompts,
        'code_snippets': code_snippets
    }

    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOTA Agent - Diagrama de Flujo Interactivo</title>
    
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
            --border-glow: rgba(16, 185, 129, 0.3);
            
            --primary: #10b981; /* Emerald */
            --primary-glow: rgba(16, 185, 129, 0.4);
            --secondary: #8b5cf6; /* Violet */
            --secondary-glow: rgba(139, 92, 246, 0.4);
            --accent: #a855f7; /* Purple */
            --accent-glow: rgba(168, 85, 247, 0.4);
            --info: #3b82f6; /* Blue */
            
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --text-accent: #34d399;
            
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
                radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.05) 0%, transparent 40%);
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
            background: linear-gradient(to right, #34d399, #a855f7, #6366f1);
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
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
            padding: 0.3rem 0.8rem;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .badge.purple {
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.3);
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
            background: linear-gradient(to bottom, var(--primary), var(--secondary), var(--accent));
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
            border-color: #34d399;
            box-shadow: 0 0 15px var(--primary-glow);
            color: white;
        }

        .flow-node.clustering.active .node-icon-circle {
            background: var(--secondary);
            border-color: #a78bfa;
            box-shadow: 0 0 15px var(--secondary-glow);
        }

        .flow-node.ranking.active .node-icon-circle {
            background: var(--accent);
            border-color: #c084fc;
            box-shadow: 0 0 15px var(--accent-glow);
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
            background: rgba(16, 185, 129, 0.08);
            border-color: rgba(16, 185, 129, 0.35);
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.05);
        }

        .flow-node.clustering.active .node-content-card {
            background: rgba(139, 92, 246, 0.08);
            border-color: rgba(139, 92, 246, 0.35);
        }

        .flow-node.ranking.active .node-content-card {
            background: rgba(168, 85, 247, 0.08);
            border-color: rgba(168, 85, 247, 0.35);
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
        
        .flow-node.clustering .node-phase-tag {
            color: var(--secondary);
        }
        
        .flow-node.ranking .node-phase-tag {
            color: var(--accent);
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
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
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

        /* CLUSTERING & CACHE VISUAL EXPLAINER */
        .explainers-section {
            grid-column: 1 / -1;
            margin-top: 1rem;
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
        }

        @media (min-width: 992px) {
            .explainers-section {
                grid-template-columns: 1fr 1fr;
            }
        }

        .explainer-card {
            background: rgba(15, 23, 42, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .explainer-card h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .explainer-card p {
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        .formula-box {
            background: rgba(16, 185, 129, 0.05);
            border: 1px dashed rgba(16, 185, 129, 0.25);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            font-family: 'Fira Code', monospace;
            font-size: 1rem;
            color: #34d399;
            margin: 0.5rem 0;
        }

        .k-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }

        .k-table th, .k-table td {
            border: 1px solid var(--border-color);
            padding: 0.5rem;
            text-align: center;
        }

        .k-table th {
            background: rgba(30, 41, 59, 0.5);
            color: var(--text-main);
        }

        .k-table td {
            color: var(--text-muted);
        }

        .cache-diagram {
            display: flex;
            align-items: center;
            justify-content: space-around;
            padding: 1.5rem;
            background: rgba(30, 41, 59, 0.2);
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin-top: 0.5rem;
        }

        .cache-box {
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.4);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            text-align: center;
            font-size: 0.8rem;
            font-weight: 600;
            color: #c084fc;
        }

        .cache-arrow {
            color: var(--text-muted);
            font-size: 1.5rem;
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
        @media (min-width: 1000px) {
            .tfg-h-step {
                flex: 1 1 calc(14.28% - 1rem);
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
            <h1>🔬 SOTA Agent: Estado del Arte</h1>
            <p>Diagrama de Arquitectura de Flujo & Análisis de Literatura</p>
        </div>
        <div class="badge-container">
            <button class="badge purple" onclick="toggleCaptureMode()" id="capture_mode_btn" style="cursor: pointer; outline: none;">📸 Modo Captura TFG</button>
            <span class="badge">Pipeline de 7 Fases</span>
            <span class="badge purple">sentence-transformers</span>
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
                Esquema de Fases del SOTA Agent (Memoria TFG)
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
                                <div class="tfg-table-fase">Fase 1</div>
                                <div class="tfg-table-tech">ThematicCoverageSkill</div>
                            </td>
                            <td>Texto completo del manuscrito del usuario.</td>
                            <td>Análisis mediante LLM para clasificar subtemas técnicos, taxonomía del área y extraer el año de publicación real.</td>
                            <td>JSON con subtemas identificados y año.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 2</div>
                                <div class="tfg-table-tech">QueryGenerationSkill</div>
                            </td>
                            <td>Subtemas identificados, áreas y año.</td>
                            <td>Conversión de los subtemas a estrategias de búsqueda (2 consultas amplias, 1 ultra-específica en inglés) optimizadas para el motor académico.</td>
                            <td>3 a 5 consultas (queries) en inglés.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 3</div>
                                <div class="tfg-table-tech">Semantic Scholar Search</div>
                            </td>
                            <td>Consultas en inglés generadas en Fase 2.</td>
                            <td>Búsqueda paralela contra la API de Semantic Scholar con gestión de rate-limits, filtrado por fecha y deduplicación.</td>
                            <td>Lista de hasta 20 papers únicos de SOTA.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 3b</div>
                                <div class="tfg-table-tech">PaperClusteringSkill</div>
                            </td>
                            <td>Abstracts recuperados y texto del manuscrito.</td>
                            <td>Clustering local de abstracts: codificación con sentence-transformers (all-MiniLM-L6-v2), cálculo de matriz coseno, diversidad global, KMeans y renombrado temático de clusters mediante LLM.</td>
                            <td>Diversidad, clusters etiquetados y similitudes coseno.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 3c</div>
                                <div class="tfg-table-tech">PaperRankingSkill</div>
                            </td>
                            <td>Corpus recuperado, clúster y criterio.</td>
                            <td>Filtrado por clúster temático y ordenación interactiva según: citas, similitud coseno con el usuario, o relevancia evaluada por el LLM.</td>
                            <td>Top-10 papers finalistas más representativos.</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 4</div>
                                <div class="tfg-table-tech">CoverageGapAnalysisSkill</div>
                            </td>
                            <td>Referencias citadas en el paper y subtemas.</td>
                            <td>Análisis bibliométrico y cualitativo de las referencias del manuscrito para detectar qué subtemas técnicos carecen de suficiente cobertura bibliográfica.</td>
                            <td>JSON de gaps detectados (áreas sin citas y justificación).</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="tfg-table-fase">Fase 5</div>
                                <div class="tfg-table-tech">CrossValidationSkill</div>
                            </td>
                            <td>Top-10 papers candidatos, referencias y gaps.</td>
                            <td>Cruce semántico final entre la literatura de SOTA y el estado del arte del paper. Recomienda de forma justificada papers de alto impacto omitidos.</td>
                            <td>JSON de validación final (papers omitidos, diagnóstico y recomendaciones).</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- VIEW 2: HORIZONTAL DIAGRAM -->
            <div id="tfg_view_diagram" class="tfg-sub-view" style="display: none;">
                <div class="tfg-horizontal-flow">
                    <!-- STEP 1 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #10b981;">Fase 1</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Temática</span>
                            <span class="tfg-h-step-desc">Identifica subtemas y año de publicación del manuscrito.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Manuscrito completo</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Subtemas & Año</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 2 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #059669;">Fase 2</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Queries</span>
                            <span class="tfg-h-step-desc">Traduce subtemas a consultas optimizadas en inglés.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Subtemas & Año</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">3-5 consultas</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 3 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #3b82f6;">Fase 3</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Búsqueda</span>
                            <span class="tfg-h-step-desc">Recupera literatura relevante en Semantic Scholar.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Consultas</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Hasta 20 papers</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 3b -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #8b5cf6;">Fase 3b</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Clustering</span>
                            <span class="tfg-h-step-desc">Sentence Embeddings + KMeans. Nombra los clusters.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Abstracts + Texto</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Clusters etiquetados</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 3c -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #c084fc;">Fase 3c</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Ranking</span>
                            <span class="tfg-h-step-desc">Filtra clusters y ordena por citas/similitud/LLM.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Papers + Criterio</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">Top-10 finalistas</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 4 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #ec4899;">Fase 4</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Gap Analysis</span>
                            <span class="tfg-h-step-desc">Detecta subtemas del manuscrito sin citas de apoyo.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Referencias citadas</span>
                                <span class="tfg-h-step-io-title">OUT</span>
                                <span class="tfg-h-step-io-content">JSON de Gaps</span>
                            </div>
                        </div>
                    </div>
                    <!-- STEP 5 -->
                    <div class="tfg-h-step">
                        <div class="tfg-h-step-header" style="background: #6b7280;">Fase 5</div>
                        <div class="tfg-h-step-body">
                            <span class="tfg-h-step-title">Validación</span>
                            <span class="tfg-h-step-desc">Identifica papers omitidos y justifica su citación.</span>
                            <div class="tfg-h-step-io">
                                <span class="tfg-h-step-io-title">IN</span>
                                <span class="tfg-h-step-io-content">Top-10 + Referencias</span>
                                <span class="tfg-h-step-io-content">OUT</span>
                                <span class="tfg-h-step-io-content">Recomendaciones</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- VIEW 3: DETAILED CARDS -->
            <div id="tfg_view_cards" class="tfg-sub-view" style="display: none;">
                <!-- STEP 1 -->
                <div class="tfg-flow-step" style="border-left-color: #10b981;">
                    <div class="tfg-step-num" style="background: #10b981;">1</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 1: Cobertura Temática (ThematicCoverageSkill)</span>
                            <span class="tfg-step-tech">Gemini 3.1 Flash Lite</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Texto completo del manuscrito del usuario.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">JSON con subtemas identificados, áreas técnicas y año de publicación.</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> El LLM analiza los metadatos y secciones del paper para extraer los subtemas específicos y el año real de publicación. Esto servirá para configurar la posterior búsqueda y filtrado de Semantic Scholar.
                        </div>
                    </div>
                </div>

                <!-- STEP 2 -->
                <div class="tfg-flow-step" style="border-left-color: #059669;">
                    <div class="tfg-step-num" style="background: #059669;">2</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 2: Generación de Queries (QueryGenerationSkill)</span>
                            <span class="tfg-step-tech">Gemini 3.1 Flash Lite</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Subtemas, áreas técnicas y un fragmento del paper del usuario.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Lista de 3 a 5 consultas de búsqueda optimizadas en inglés.</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Traduce la temática del manuscrito a estrategias de búsqueda académica efectivas, generando dos consultas amplias y una ultra-específica para capturar la literatura más representativa.
                        </div>
                    </div>
                </div>

                <!-- STEP 3 -->
                <div class="tfg-flow-step" style="border-left-color: #3b82f6;">
                    <div class="tfg-step-num" style="background: #3b82f6;">3</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 3: Recuperación de Literatura (SemanticScholarSearchSkill)</span>
                            <span class="tfg-step-tech">API Semantic Scholar</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Consultas de búsqueda generadas.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Lista de hasta 20 papers únicos de SOTA, ordenados por citas.</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Búsqueda paralela en Semantic Scholar con control de límites (rate-limits), filtrado opcional por años e impacto. Combina y deduplica los hallazgos para quedarse con el corpus de literatura canónica.
                        </div>
                    </div>
                </div>

                <!-- STEP 3b -->
                <div class="tfg-flow-step" style="border-left-color: #8b5cf6;">
                    <div class="tfg-step-num" style="background: #8b5cf6;">3b</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 3b: Clustering Semántico (PaperClusteringSkill)</span>
                            <span class="tfg-step-tech">all-MiniLM-L6-v2 + KMeans</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Abstracts de papers recuperados y texto del paper del usuario.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Métrica de diversidad, similitudes coseno y agrupación en clusters con nombres y emojis.</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Codifica en vectores locales los abstracts, calcula la similitud coseno N×N y la diversidad global. Divide mediante KMeans en <em>k</em> clusters. Un LLM lee los títulos de cada cluster en un solo prompt y les asigna un nombre temático humano.
                        </div>
                    </div>
                </div>

                <!-- STEP 3c -->
                <div class="tfg-flow-step" style="border-left-color: #c084fc;">
                    <div class="tfg-step-num" style="background: #c084fc;">3c</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 3c: Ranking y Filtrado (PaperRankingSkill)</span>
                            <span class="tfg-step-tech">Lógica Python / LLM (Opcional)</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Papers recuperados, criterio de ordenación y filtro de clúster.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">Lista de los Top-10 papers más representativos.</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Permite filtrar por un cluster de interés y ordenar los papers según tres criterios: citas totales, similitud coseno con el paper del usuario, o relevancia subjetiva evaluada bajo demanda por el LLM.
                        </div>
                    </div>
                </div>

                <!-- STEP 4 -->
                <div class="tfg-flow-step" style="border-left-color: #ec4899;">
                    <div class="tfg-step-num" style="background: #ec4899;">4</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 4: Análisis de Gaps (CoverageGapAnalysisSkill)</span>
                            <span class="tfg-step-tech">Gemini 3.1 Flash Lite</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Referencias citadas en el paper y subtemas identificados.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">JSON de gaps (Áreas débiles con diagnóstico de por qué carecen de citas).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Analiza las referencias bibliográficas y la sección de trabajo relacionado del paper original para determinar si alguno de los subtemas técnicos del manuscrito carece de soporte académico suficiente.
                        </div>
                    </div>
                </div>

                <!-- STEP 5 -->
                <div class="tfg-flow-step" style="border-left-color: #6b7280;">
                    <div class="tfg-step-num" style="background: #6b7280;">5</div>
                    <div class="tfg-step-details">
                        <div class="tfg-step-header">
                            <span class="tfg-step-title">Fase 5: Validación Cruzada (CrossValidationSkill)</span>
                            <span class="tfg-step-tech">Gemini 3.1 Flash Lite</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Entradas (Inputs)</span>
                            <span class="tfg-io-content">Referencias del paper, Top-10 papers candidatos y gaps detectados.</span>
                        </div>
                        <div class="tfg-step-io">
                            <span class="tfg-io-title">Salidas (Outputs)</span>
                            <span class="tfg-io-content">JSON final de validación (Lista de papers omitidos, justificación y conclusión SOTA).</span>
                        </div>
                        <div class="tfg-step-desc">
                            <strong>Descripción del proceso:</strong> Cruza los abstracts de la búsqueda académica contra las referencias del usuario. Identifica falsos positivos y recomienda de forma justificada qué papers relevantes han sido omitidos por el autor y en qué sección deberían citarse.
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
                    Pipeline del Agente SOTA
                </h2>
                <span style="color: var(--text-muted); font-size: 0.8rem;">Haz clic en una fase para inspeccionarla</span>
            </div>
            
            <div class="pipeline-container">
                <div class="pipeline-connector"></div>
                
                <!-- NODE 1 -->
                <div class="flow-node active" onclick="selectPhase('phase1')" id="node_phase1">
                    <div class="node-icon-circle">1</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 1</span>
                        <h3>Análisis Temático (ThematicCoverageSkill)</h3>
                        <p>Extrae del paper original los subtemas, áreas técnicas y año usando Gemini.</p>
                    </div>
                </div>

                <!-- NODE 2 -->
                <div class="flow-node" onclick="selectPhase('phase2')" id="node_phase2">
                    <div class="node-icon-circle">2</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 2</span>
                        <h3>Generación de Estrategia (QueryGenerationSkill)</h3>
                        <p>Traduce los temas a 3 queries optimizadas para Semantic Scholar.</p>
                    </div>
                </div>

                <!-- NODE 3 -->
                <div class="flow-node" onclick="selectPhase('phase3')" id="node_phase3">
                    <div class="node-icon-circle">3</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 3</span>
                        <h3>Recuperación de Literatura (SemanticScholarSearchSkill)</h3>
                        <p>Busca literatura de alto impacto mediante API externa, ordenando por citas.</p>
                    </div>
                </div>

                <!-- NODE 3b -->
                <div class="flow-node clustering" onclick="selectPhase('phase3b')" id="node_phase3b">
                    <div class="node-icon-circle">3b</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 3b</span>
                        <h3>Clustering Semántico Local (PaperClusteringSkill)</h3>
                        <p>KMeans, similitud coseno (all-MiniLM-L6-v2) y diversity score del corpus.</p>
                    </div>
                </div>

                <!-- NODE 3c -->
                <div class="flow-node ranking" onclick="selectPhase('phase3c')" id="node_phase3c">
                    <div class="node-icon-circle">3c</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 3c</span>
                        <h3>Ranking y Filtrado (PaperRankingSkill)</h3>
                        <p>Selecciona los top-10 papers por citas, similitud coseno o criterio LLM.</p>
                    </div>
                </div>

                <!-- NODE 4 -->
                <div class="flow-node" onclick="selectPhase('phase4')" id="node_phase4">
                    <div class="node-icon-circle">4</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 4</span>
                        <h3>Análisis de Gaps (CoverageGapAnalysisSkill)</h3>
                        <p>Evalúa qué subtemas del paper original tienen baja cobertura bibliográfica.</p>
                    </div>
                </div>

                <!-- NODE 5 -->
                <div class="flow-node" onclick="selectPhase('phase5')" id="node_phase5">
                    <div class="node-icon-circle">5</div>
                    <div class="node-content-card">
                        <span class="node-phase-tag">Fase 5</span>
                        <h3>Validación Cruzada (CrossValidationSkill)</h3>
                        <p>Identifica papers omitidos (no citados) sugiriendo justificación para el autor.</p>
                    </div>
                </div>

            </div>
        </section>

        <!-- RIGHT COLUMN: DETAILS INSPECTOR -->
        <section class="glass-card inspector-panel">
            <div class="inspector-title-area">
                <h2 id="inspector_title">Fase 1: Cobertura Temática</h2>
                <p id="inspector_description">Extrae subtemas y áreas técnicas utilizando Gemini.</p>
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
                    Extracción del ADN del paper.
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

        <!-- EXPLAINERS SECTION -->
        <section class="explainers-section">
            
            <!-- EXPLAINER 1: CLUSTERING SEMÁNTICO -->
            <div class="glass-card explainer-card">
                <h3>
                    <svg class="svg-icon" viewBox="0 0 24 24" style="color: var(--secondary);"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                    Métricas del Clustering Semántico
                </h3>
                <p>El clustering analiza localmente los abstracts de la literatura recuperada. Produce dos métricas clave:</p>
                
                <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--secondary);">1. DIVERSITY SCORE OF THE CORPUS</div>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.3rem;">Mide la variedad del corpus recuperado (1 = muy diverso, 0 = idénticos abstracts):</p>
                    <div class="formula-box">Diversity Score = 1 - mean_similarity_off_diagonal</div>
                </div>

                <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--secondary);">2. DETERMINACIÓN DE CLUSTERS K-MEANS</div>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.3rem;">El número de clusters <em>k</em> se ajusta dinámicamente según el número de papers recuperados (N):</p>
                    <table class="k-table">
                        <thead>
                            <tr>
                                <th>N papers</th>
                                <th>k clusters</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>≤ 4</td>
                                <td>2 clusters</td>
                            </tr>
                            <tr>
                                <td>5 – 8</td>
                                <td>3 clusters</td>
                            </tr>
                            <tr>
                                <td>9 – 15</td>
                                <td>4 clusters</td>
                            </tr>
                            <tr>
                                <td>16 – 25</td>
                                <td>5 clusters</td>
                            </tr>
                            <tr>
                                <td>&gt; 25</td>
                                <td>6 clusters</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- EXPLAINER 2: CACHE HOT-RELOAD -->
            <div class="glass-card explainer-card">
                <h3>
                    <svg class="svg-icon" viewBox="0 0 24 24" style="color: var(--accent);"><path d="M19 8l-4 4h3c0 3.31-2.69 6-6 6-1.01 0-1.97-.25-2.8-.7l-1.46 1.46C8.97 19.54 10.43 20 12 20c4.42 0 8-3.58 8-8h3l-4-4zM6 12c0-3.31 2.69-6 6-6 1.01 0 1.97.25 2.8.7l1.46-1.46C15.03 4.46 13.57 4 12 4c-4.42 0-8 3.58-8 8H1l4 4 4-4H6z"/></svg>
                    Mecanismo de Caché (Hot-Reload) en UI
                </h3>
                <p>Para mejorar la interactividad, el sistema cuenta con un flujo rápido de re-análisis en memoria:</p>
                
                <div class="cache-diagram">
                    <div class="cache-box">
                        Cambio de Criterio / Cluster<br><span style="font-size: 0.7rem; font-weight: normal; opacity: 0.8;">citations / similarity / llm</span>
                    </div>
                    <div class="cache-arrow">➔</div>
                    <div class="cache-box" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.4); color: #34d399;">
                        Orquestador: last_context<br><span style="font-size: 0.7rem; font-weight: normal; opacity: 0.8;">Sin llamar Semantic Scholar</span>
                    </div>
                    <div class="cache-arrow">➔</div>
                    <div class="cache-box" style="background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.4); color: #60a5fa;">
                        Actualización de UI<br><span style="font-size: 0.7rem; font-weight: normal; opacity: 0.8;">Respuesta en &lt; 1 segundo</span>
                    </div>
                </div>

                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">
                    Al cambiar el cluster filtrado o el criterio de relevancia en el selector de Streamlit, el sistema invoca el método <code>update_ranking_and_reanalyze(...)</code>. Esto recupera los papers previamente analizados en memoria, vuelve a rankear el top-10 y relanza la validación sin consumir cuotas de API de búsqueda externa.
                </div>
            </div>

        </section>
    </main>

    <footer class="footer">
        <div>TFG - LLM Scientific Paper Auditor (SOTA Agent)</div>
        <div>Visualización Interactiva © 2026</div>
    </footer>

    <!-- Prism JS for syntax highlighting -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markdown.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>

    <script>
        const data = __INJECTED_DATA__;

        const phasesConfig = {
            phase1: {
                title: "Fase 1: Cobertura Temática (ThematicCoverageSkill)",
                description: "Extracción del ADN conceptual y año del manuscrito",
                summary: "En este primer paso, el LLM (Gemini 3.1 Flash Lite) analiza el manuscrito científico (primeras y últimas secciones) para identificar los 3-5 subtemas principales que trata, las áreas técnicas y el año de publicación (obtenido del copyright, cabeceras o fechas de revisión). Esta información es fundamental para contextualizar la búsqueda bibliográfica en las fases posteriores.",
                inputs: [
                    { key: "paper_text", type: "string" }
                ],
                outputs: [
                    { key: "thematic_data", type: "JSON {subtemas, areas_tecnicas, año_paper}" }
                ],
                prompt: "thematic",
                codeFile: "backend/skills/sota_skills.py -> ThematicCoverageSkill",
                codeSnippet: data.code_snippets.thematic_skill || ""
            },
            phase2: {
                title: "Fase 2: Generación de Queries (QueryGenerationSkill)",
                description: "Conversión de temas a términos de búsqueda técnicos",
                summary: "Utilizando los subtemas y áreas técnicas extraídos en la Fase 1, el LLM genera de 3 a 5 búsquedas especializadas en inglés (queries). El prompt le instruye a formular dos búsquedas amplias (generales) y una específica sobre el subtema más relevante. Se priorizan términos estándar y consolidados del dominio para asegurar un alto índice de recuperación en la API académica.",
                inputs: [
                    { key: "thematic_data", type: "JSON" },
                    { key: "paper_text", type: "string (fragmento)" }
                ],
                outputs: [
                    { key: "search_queries", type: "Array of Strings" }
                ],
                prompt: "query_generation",
                codeFile: "backend/skills/sota_skills.py -> QueryGenerationSkill",
                codeSnippet: data.code_snippets.query_skill || ""
            },
            phase3: {
                title: "Fase 3: Recuperación de Literatura (SemanticScholarSearchSkill)",
                description: "Búsqueda en Semantic Scholar con filtrado de impacto",
                summary: "Esta fase realiza peticiones REST HTTP a la API pública (o usando API Key si está configurada) de **Semantic Scholar**. Ejecuta búsquedas para cada una de las queries generadas en la Fase 2, filtra los resultados por año de publicación si se configura y unifica las colecciones de papers resultantes. Posteriormente, realiza una deduplicación por identificador único y ordena los artículos por número de citas (<code>citationCount</code>) para quedarse con los 20 más relevantes.",
                inputs: [
                    { key: "search_queries", type: "Array of Strings" }
                ],
                outputs: [
                    { key: "sota_papers", type: "Array of up to 20 Papers" }
                ],
                prompt: null,
                codeFile: "backend/skills/sota_skills.py -> SemanticScholarSearchSkill",
                codeSnippet: data.code_snippets.search_skill || ""
            },
            phase3b: {
                title: "Fase 3b: Clustering Semántico (PaperClusteringSkill)",
                description: "Clustering local de abstracts y análisis de diversidad",
                summary: "Una fase 100% matemática y local que no depende de APIs externas:\\n1. Genera vectores numéricos (embeddings de 384 dimensiones) de los abstracts utilizando el modelo **all-MiniLM-L6-v2** locally.\\n2. Calcula la similitud coseno de cada paper contra las primeras 1500 letras del paper del usuario.\\n3. Mide la homogeneidad de la búsqueda con el **Diversity Score** basado en la similitud coseno N×N.\\n4. Agrupa en clusters con **KMeans** de scikit-learn.\\n5. Envía los títulos de cada cluster en una única llamada LLM rápida para asignarle un nombre descriptivo humano y un emoji.",
                inputs: [
                    { key: "sota_papers", type: "Array of Papers" },
                    { key: "paper_text", type: "string" }
                ],
                outputs: [
                    { key: "sota_papers", type: "Array of Papers (enriquecidos)" },
                    { key: "user_similarities", type: "Array of JSONs" },
                    { key: "diversity_score", type: "float" },
                    { key: "cluster_summary", type: "JSON [cluster_id -> metadata]" }
                ],
                prompt: null,
                codeFile: "backend/skills/clustering_skill.py -> PaperClusteringSkill",
                codeSnippet: data.code_snippets.clustering_skill || ""
            },
            phase3c: {
                title: "Fase 3c: Ranking y Filtrado (PaperRankingSkill)",
                description: "Selección del Top-10 basándose en criterios interactivos",
                summary: "Filtra la lista según el clúster seleccionado por el usuario en la UI (o los mantiene todos si la opción es 'all'). Posteriormente, selecciona el Top-10 sobre el cual se ejecutará el análisis en profundidad, ordenándolo según el criterio interactivo elegido por el usuario:\\n- **Citas ('citations')**: Orden determinista por volumen de citas.\\n- **Similitud Coseno ('similarity')**: Ordenado por la similitud del embedding local contra el abstract del usuario.\\n- **Relevancia LLM ('llm')**: El LLM evalúa y puntúa de 0 a 10 qué tan prioritario es citar cada paper.",
                inputs: [
                    { key: "sota_papers", type: "Array of Papers" },
                    { key: "ranking_criterion", type: "string ('citations'/'similarity'/'llm')" },
                    { key: "target_cluster_id", type: "string/int" }
                ],
                outputs: [
                    { key: "ranked_papers", type: "Array of 10 Papers" }
                ],
                prompt: null,
                codeFile: "backend/skills/sota_skills.py -> PaperRankingSkill",
                codeSnippet: data.code_snippets.ranking_skill || ""
            },
            phase4: {
                title: "Fase 4: Análisis de Gaps (CoverageGapAnalysisSkill)",
                description: "Análisis preliminar de las referencias del autor",
                summary: "El LLM lee el inicio del paper del usuario y su sección de referencias bibliográficas para contrastarlas con los subtemas identificados en la Fase 1. Determina cuáles de estos subtemas tienen baja o nula representación en la bibliografía actual del manuscrito, generando un JSON con un diagnóstico explicativo de cada deficiencia detectada.",
                inputs: [
                    { key: "paper_text", type: "string" },
                    { key: "thematic_data", type: "JSON" }
                ],
                outputs: [
                    { key: "coverage_gaps", type: "JSON {areas_debiles}" }
                ],
                prompt: "gap_analysis",
                codeFile: "backend/skills/sota_skills.py -> CoverageGapAnalysisSkill",
                codeSnippet: data.code_snippets.gap_skill || ""
            },
            phase5: {
                title: "Fase 5: Validación Cruzada (CrossValidationSkill)",
                description: "Detección de omisiones y justificación bibliográfica",
                summary: "Es el juez final del análisis de literatura. El LLM contrasta el texto completo del paper y sus referencias reales contra los abstracts de los top-10 papers seleccionados en la Fase 3c. Filtra los falsos positivos (papers que el autor ya citó pero bajo otro formato). Posteriormente, genera un veredicto detallado que incluye la lista de los papers que el autor ha omitido injustificadamente, una justificación de su relevancia y una conclusión del estado actual de frescura bibliográfica del manuscrito.",
                inputs: [
                    { key: "paper_text", type: "string" },
                    { key: "ranked_papers", type: "Array of 10 Papers" },
                    { key: "coverage_gaps", type: "JSON" }
                ],
                outputs: [
                    { key: "validation_results", type: "JSON {papers_omitidos, conclusion_sota, ...}" }
                ],
                prompt: "cross_validation",
                codeFile: "backend/skills/sota_skills.py -> CrossValidationSkill",
                codeSnippet: data.code_snippets.validation_skill || ""
            }
        };

        let currentActivePhase = 'phase1';
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
                if (config.prompt === "thematic") {
                    promptFilename = "1. thematic.md";
                    promptContent = data.prompts.thematic || "";
                } else if (config.prompt === "query_generation") {
                    promptFilename = "2. query_generation.md";
                    promptContent = data.prompts.query_generation || "";
                } else if (config.prompt === "gap_analysis") {
                    promptFilename = "3. gap_analysis.md";
                    promptContent = data.prompts.gap_analysis || "";
                } else if (config.prompt === "cross_validation") {
                    promptFilename = "4. cross_validation.md";
                    promptContent = data.prompts.cross_validation || "";
                }
                
                document.getElementById('prompt_filename').innerText = promptFilename;
                document.getElementById('prompt_code').textContent = promptContent;
            } else {
                promptBtn.style.display = 'none';
                if (currentActiveTab === 'tab_prompt') {
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

        // Initialize view
        window.addEventListener('DOMContentLoaded', () => {
            selectPhase('phase1');
        });
    </script>
</body>
</html>"""

    # Replace injected data token
    injected_data_json = json.dumps(data, ensure_ascii=False, indent=2)
    html_output = html_template.replace("const data = __INJECTED_DATA__;", f"const data = {injected_data_json};")

    output_path = os.path.join(workspace_dir, "diagrama_sota.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"Success! SOTA Diagram generated at: {output_path}")
    except Exception as e:
        print(f"Error writing output HTML: {e}")

if __name__ == "__main__":
    main()
