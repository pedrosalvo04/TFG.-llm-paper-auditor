import re
import sys

files = [
    r'c:\Users\pedro\Documents\GitHub\TFG.-llm-paper-auditor\resultados evaluación audiciones gemini.md',
    r'c:\Users\pedro\Documents\GitHub\TFG.-llm-paper-auditor\resultados evaluación audiciones qwen2.5.md'
]

safe_mente = {
    'solamente', 'únicamente', 'realmente', 'simplemente', 'frecuentemente', 
    'previamente', 'posteriormente', 'obviamente', 'lógicamente', 'directamente', 
    'indirectamente', 'básicamente', 'prácticamente', 'totalmente', 'completamente', 
    'finalmente', 'inicialmente', 'actualmente', 'probablemente', 'posiblemente', 
    'seguramente', 'precisamente', 'específicamente', 'especialmente', 'generalmente', 
    'normalmente', 'mayormente', 'igualmente', 'respectivamente', 'conjuntamente', 
    'independientemente', 'efectivamente', 'solamente', 'literalmente', 'textualmente'
}

# Actually, the user might want 'literalmente' and 'textualmente' removed. "cita textualmente" -> "cita"
safe_mente.discard('literalmente')
safe_mente.discard('textualmente')

def clean_text(text):
    # Remove AI bloat adjectives/phrases
    phrases_to_remove = [
        r'\ba la perfección\b',
        r'\bcon total exactitud\b',
        r'\bcon total fidelidad\b',
        r'\bcon gran precisión\b',
        r'\bcon extrema precisión\b',
        r'\bcon gran criterio\b',
        r'\bcon maestría\b',
        r'\bde forma incomprensible\b',
        r'\bde manera exacta\b',
        r'\bde manera explícita\b',
        r'\bde manera indudable\b',
        r'\bde manera impecable\b',
        r'\bde forma intachable\b',
        r'\bde manera autónoma\b',
        r'\bflagrante e inaceptable\b',
        r'\bflagrante\b',
        r'\bsumamente\b'
    ]
    
    for phrase in phrases_to_remove:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)
    
    # Replace overly formal adjectives
    adj_replacements = {
        r'\bimpecable(s?)\b': 'bueno\\1',
        r'\bsoberbio(s?)\b': 'bueno\\1',
        r'\bsoberbia(s?)\b': 'buena\\1',
        r'\bmagistral(es?)\b': 'bueno\\1',
        r'\bbrillante(s?)\b': 'bueno\\1',
        r'\bquirúrgico(s?)\b': 'preciso\\1',
        r'\bquirúrgica(s?)\b': 'precisa\\1',
        r'\bintachable(s?)\b': 'bueno\\1',
        r'\bimplacable(s?)\b': 'estricto\\1'
    }
    
    for pat, rep in adj_replacements.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    
    # Process -mente words
    words = text.split()
    new_words = []
    for w in words:
        # Strip punctuation to check the word
        clean_w = re.sub(r'[^a-záéíóúñ]', '', w.lower())
        if clean_w.endswith('mente') and clean_w not in safe_mente:
            # Skip this word
            continue
        new_words.append(w)
        
    text = ' '.join(new_words)
    
    # Clean up double spaces and punctuation issues caused by removals
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([,\.])', r'\1', text)
    text = re.sub(r'([¿¡])\s+', r'\1', text)
    
    # Capitalize sentences properly
    def capitalize_match(m):
        return m.group(1) + m.group(2).upper()
    
    text = text.strip()
    if len(text) > 0:
        text = text[0].upper() + text[1:]
    text = re.sub(r'([\.!?]\s+)([a-z])', capitalize_match, text)
    
    return text

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if line.startswith('- **Mi Justificación:**') or line.startswith('Mi Justificación:'):
            prefix_match = re.match(r'^(- \*\*Mi Justificación:\*\*|Mi Justificación:)(.*)', line)
            if prefix_match:
                prefix = prefix_match.group(1)
                content = prefix_match.group(2)
                cleaned_content = clean_text(content)
                new_lines.append(f"{prefix} {cleaned_content}\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Text simplified in both files.")
