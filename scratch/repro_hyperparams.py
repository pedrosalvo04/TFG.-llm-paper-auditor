import sys
import os

# Añadir el directorio actual al path para poder importar backend
sys.path.append(os.getcwd())

from backend.skills.regex_detection_skills import HyperparameterDetectionSkill

def test_hyperparameter_detection():
    paper_path = "paper_cientifico_3_CON_ERRORES.md"
    if not os.path.exists(paper_path):
        print(f"File {paper_path} not found")
        return

    with open(paper_path, "r", encoding="utf-8") as f:
        text = f.read()

    skill = HyperparameterDetectionSkill()
    context = {"paper_text": text}
    
    # Redirigir logs a la consola para ver qué pasa
    skill.log_execution = lambda msg, level="info": print(f"[{level.upper()}] {msg}")
    
    print(f"--- Testing detection on {paper_path} ---")
    results = skill.execute(context)
    
    print("\n--- Final Results ---")
    import json
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    test_hyperparameter_detection()
