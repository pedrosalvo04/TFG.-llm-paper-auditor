import os

replacements = {
    "Qwen 2.5 Local": "Qwen 2.5 Local",
    "Qwen 2.5 Local": "Qwen 2.5 Local",
    "Qwen Map-Reduce": "Qwen Map-Reduce",
    "Qwen CoT Batches": "Qwen CoT Batches",
    "Qwen extrae": "Qwen extrae",
    "Qwen (Map-Reduce)": "Qwen (Map-Reduce)",
    "Qwen (Context Router)": "Qwen (Context Router)",
    "Qwen + Reglas Dinámicas": "Qwen + Reglas Dinámicas",
    "El LLM local está experimentando": "El LLM local está experimentando",
    '"qwen2.5"': '"qwen2.5"',
    "usando Qwen": "usando Qwen",
    "utilizando Qwen": "utilizando Qwen",
    "(Qwen 2.5 Local)": "(Qwen 2.5 Local)",
    "modelo local": "modelo local",
}

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'venv' in root or '.venv' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements.items():
                    new_content = new_content.replace(old, new)
                    
                if new_content != content:
                    print(f'Updating {filepath}')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                pass
