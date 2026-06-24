import json
import sys

json_file = r'C:\Users\pedro\Documents\GitHub\TFG.-llm-paper-auditor\json a unificar.json'
md_file = r'C:\Users\pedro\Desktop\resultados evaluación eudiciones gemini.md'

try:
    with open(json_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading JSON: {e}")
    sys.exit(1)

lines = []

for paper_data in data.get('auditorias_neurips_2026', []):
    paper_title = paper_data.get('paper', '')
    if lines:
        lines.append('')
    lines.append(f'# {paper_title}')
    lines.append('')
    
    items = paper_data.get('items', [])
    for idx, item_data in enumerate(items):
        item_title = item_data.get('item', '')
        # Handle the case if "Ítem" is not already in the title
        if not item_title.lower().startswith("ítem") and not item_title.lower().startswith("item"):
            item_header = f"**Ítem {item_title}**"
        else:
            item_header = f"**{item_title}**"
        
        lines.append(item_header)
        
        val_auditor = item_data.get('valoracion_auditor', '')
        just_auditor = item_data.get('justificacion_auditor', '')
        mi_val = item_data.get('mi_valoracion', '')
        mi_just = item_data.get('mi_justificacion', '')
        
        lines.append(f'- **Valoración Auditor:** {val_auditor}')
        lines.append(f'- **Justificación Auditor:** {just_auditor}')
        lines.append(f'- **Mi Valoración:** {mi_val}')
        lines.append(f'- **Mi Justificación:** {mi_just}')
        
        lines.append('')

with open(md_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines).strip() + '\n')

print("Markdown update successful.")
