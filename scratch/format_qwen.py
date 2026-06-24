import re

input_path = r'c:\Users\pedro\Documents\GitHub\TFG.-llm-paper-auditor\resultados evaluación audiciones qwen2.5.md'

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

papers = []
current_paper = None
current_item = None
current_field = None
current_val_lines = []

field_mappings = {
    'Valoración Auditor:': 'val_auditor',
    'Valoracion Auditor:': 'val_auditor',
    'Justificación Auditor:': 'just_auditor',
    'Justificacion Auditor:': 'just_auditor',
    'Mi Valoración:': 'mi_val',
    'Mi Valoracion:': 'mi_val',
    'Mi Justificación:': 'mi_just',
    'Mi Justificacion:': 'mi_just'
}

def clean_value(val_str):
    val_str = val_str.strip()
    return val_str

for line_idx, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        if current_field:
            current_val_lines.append(line)
        continue
    
    # Check for Paper header
    if stripped.startswith('Paper ') and ':' in stripped:
        if current_field and current_item:
            current_item[current_field] = clean_value(''.join(current_val_lines))
            current_field = None
            current_val_lines = []
            
        current_paper = {'title': stripped, 'items': []}
        papers.append(current_paper)
        current_item = None
        continue
        
    # Check for Item header
    if stripped.startswith('Ítem ') or stripped.startswith('Item '):
        if current_field and current_item:
            current_item[current_field] = clean_value(''.join(current_val_lines))
            current_field = None
            current_val_lines = []
            
        current_item = {'title': stripped}
        if current_paper is not None:
            current_paper['items'].append(current_item)
        continue

    # Check for field
    matched_key = None
    for prefix, key in field_mappings.items():
        if stripped.startswith(prefix):
            matched_key = key
            val_part = line.split(prefix, 1)[1]
            break
            
    if matched_key:
        if current_field and current_item:
            current_item[current_field] = clean_value(''.join(current_val_lines))
            
        current_field = matched_key
        current_val_lines = [val_part]
    else:
        if current_field:
            current_val_lines.append(line)

if current_field and current_item:
    current_item[current_field] = clean_value(''.join(current_val_lines))

# Now, generate markdown output
md_lines = []
for paper_idx, paper in enumerate(papers):
    # Two empty lines between papers, except for the first one
    if paper_idx > 0:
        md_lines.append('')
        md_lines.append('')
    
    md_lines.append(f"# {paper['title']}")
    md_lines.append('')
    
    for item_idx, item in enumerate(paper['items']):
        md_lines.append(f"**{item['title']}**")
        md_lines.append(f"- **Valoración Auditor:** {item.get('val_auditor', '')}")
        md_lines.append(f"- **Justificación Auditor:** {item.get('just_auditor', '')}")
        md_lines.append(f"- **Mi Valoración:** {item.get('mi_val', '')}")
        md_lines.append(f"- **Mi Justificación:** {item.get('mi_just', '')}")
        
        # Add an empty line after the item, unless it's the last item in the paper
        if item_idx < len(paper['items']) - 1:
            md_lines.append('')

# Write to output file directly
with open(input_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines) + '\n')

print(f"Markdown formatting generated to {input_path}")
