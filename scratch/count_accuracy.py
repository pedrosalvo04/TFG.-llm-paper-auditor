import re
import json

def analyze_file_per_item(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by Paper
    papers = re.split(r'# Paper \d+:', content)[1:]
    
    # We want to track correct counts per item (1 to 16)
    item_stats = {str(i): {'total': 0, 'correct': 0} for i in range(1, 17)}
    
    for paper in papers:
        items = re.findall(r'\*\*Ítem (\d+)\..*?\*\*(.*?)(?=\*\*Ítem \d+\.|\Z)', paper, re.DOTALL)
        for item_num, item_content in items:
            if item_num in item_stats:
                val_match = re.search(r'- \*\*Mi Valoración:\*\* (.*)', item_content)
                if val_match:
                    val = val_match.group(1).strip().lower()
                    item_stats[item_num]['total'] += 1
                    if 'correcto' in val and 'medianamente' not in val and 'incorrecto' not in val:
                        item_stats[item_num]['correct'] += 1
    
    # Calculate accuracy percentage per item
    accuracy_per_item = {}
    for i in range(1, 17):
        i_str = str(i)
        stats = item_stats[i_str]
        acc = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        accuracy_per_item[i_str] = round(acc, 1)
        
    return accuracy_per_item

gemini = analyze_file_per_item('c:/Users/pedro/Documents/GitHub/TFG.-llm-paper-auditor/resultados evaluación audiciones gemini.md')
qwen = analyze_file_per_item('c:/Users/pedro/Documents/GitHub/TFG.-llm-paper-auditor/resultados evaluación audiciones qwen2.5.md')

print("Gemini Item Accuracy:", json.dumps(gemini))
print("Qwen2.5 Item Accuracy:", json.dumps(qwen))
