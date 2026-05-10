import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re

def test_rag_logical_splitter():
    print("Testing RAG logical block splitter...")
    
    paper_text = """# Title
Authors etc.

# Abstract
This is a paragraph.
It should stay together.

## Introduction
Another block.

| Table 1 |
|---------|
| Data 1  |

Final word.
"""
    
    paper_text_norm = paper_text.replace('\r\n', '\n')
    raw_chunks = re.split(r'\n\n+', paper_text_norm)
    chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 10]
    
    print(f"Chunks count: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"--- Chunk {i+1} ---\n{c}")
    
    # Assertions
    assert len(chunks) >= 4
    assert "| Table 1 |" in chunks[3]
    assert "Data 1" in chunks[3]
    assert "Abstract" in chunks[1]
    
    print("RAG logical splitter test PASSED")

if __name__ == "__main__":
    test_rag_logical_splitter()
