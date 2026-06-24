import re

file_path = r'c:\Users\pedro\Documents\GitHub\TFG.-llm-paper-auditor\resultados evaluación audiciones qwen2.5.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

leakage_keywords = ['fuga', 'leakage', 'json', 'backend', 'delata', 'expon', 'cuarta pared', 'vomit', 'ocult', 'markdown interno', 'regla algor', 'inyección', 'etiqueta interna', 'prompt']

def process_justification(just):
    lower_just = just.lower()
    has_leakage = any(kw in lower_just for kw in leakage_keywords)
    
    # We want to exclude actual logical errors that also got downgraded
    has_real_error = any(kw in lower_just for kw in ['contradice', 'genérica', 'perezosa', 'falso', 'absurdo', 'alucinación', 'inventa', 'laxa'])
    
    if has_leakage and not has_real_error:
        splitters = [
            'Sin embargo,', ' pero ', 'Degradado', 'Desciende', 'No obstante,', 
            'El castigo se aplica', 'Se degrada', 'arruinado', 'arruina', 'Reincide'
        ]
        
        best_cut = len(just)
        for s in splitters:
            idx = just.find(s)
            if idx != -1 and idx > 15:
                best_cut = min(best_cut, idx)
                
        if best_cut < len(just):
            new_just = just[:best_cut].strip()
            new_just = re.sub(r'[,\s]+$', '.', new_just)
            if not new_just.endswith('.'):
                new_just += '.'
            return new_just
        else:
            sentences = just.split('. ')
            kept = []
            for s in sentences:
                if not any(kw in s.lower() for kw in leakage_keywords):
                    kept.append(s)
            if kept:
                res = '. '.join(kept).strip()
                if not res.endswith('.'): res += '.'
                return res
            else:
                return "Evaluación fáctica correcta."
    return None

new_lines = []
i = 0
changed_count = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("- **Mi Valoración:** Medianamente correcto"):
        if i + 1 < len(lines) and lines[i+1].startswith("- **Mi Justificación:**"):
            just = lines[i+1].split("- **Mi Justificación:**", 1)[1].strip()
            new_just = process_justification(just)
            if new_just:
                new_lines.append("- **Mi Valoración:** Correcto\n")
                new_lines.append(f"- **Mi Justificación:** {new_just}\n")
                changed_count += 1
                i += 2
                continue
    new_lines.append(line)
    i += 1

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Fixed {changed_count} prompt leakage penalties.")
