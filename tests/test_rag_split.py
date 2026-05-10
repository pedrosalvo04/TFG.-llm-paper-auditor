import re

def get_rag_chunks(paper_text):
    # Normalizar saltos de línea
    paper_text = paper_text.replace('\r\n', '\n')
    
    # Dividir por párrafos (doble salto de línea) o por encabezados
    # Usamos lookahead para no perder los encabezados
    # El patrón \n\n+ divide por párrafos
    # El patrón \n(?=#+ ) divide por encabezados
    
    # Una forma sencilla es split por \n\n y luego limpiar
    chunks = re.split(r'\n\n+', paper_text)
    
    # Pero queremos mantener los encabezados como parte del chunk siguiente o como chunks propios
    # Si usamos re.split(r'\n\n+|(?=\n#+ )', paper_text)
    
    # Intentemos una aproximación que respete la estructura de Docling:
    # Docling separa elementos con \n\n. 
    # Cada elemento es una "sección identificada" (párrafo, tabla, encabezado).
    
    raw_chunks = re.split(r'\n\n+', paper_text)
    chunks = [c.strip() for c in raw_chunks if c.strip()]
    
    return chunks

# Test
test_text = """# Title
Authors etc.

# Abstract
This is the abstract.
It has two sentences.

# Introduction
Hello world.

| Table 1 | Val |
|---------|-----|
| Param   | 1.0 |

Final text.
"""

chunks = get_rag_chunks(test_text)
print(f"Total chunks: {len(chunks)}")
for i, c in enumerate(chunks):
    print(f"--- Chunk {i+1} ---\n{c}")
