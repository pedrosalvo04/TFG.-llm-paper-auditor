import json
import sys
import os

from backend.services.auditor import PaperAuditor
from backend.services.pdf_parser import convert_pdf_to_markdown

def main():
    pdf_path = "paper cientifico 4 (llms) attention is all you need.pdf"
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print("Parsing PDF...")
    paper_text = convert_pdf_to_markdown(pdf_path)

    print("Loading custom criteria...")
    with open("criterios_prueba.md", "r", encoding="utf-8") as f:
        criteria_text = f.read()

    auditor = PaperAuditor()
    print("Starting audit...")
    result = auditor.audit(paper_text, status_callback=lambda msg, idx=None: print(msg), criteria_mode="free", criteria_text=criteria_text)
    
    with open("debug_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("Done! Result saved to debug_result.json")

if __name__ == "__main__":
    main()
