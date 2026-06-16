import json
import os
import sys

# Setup PYTHONPATH manually
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from backend.skills.auditor_skills import SectionMappingSkill
from backend.common.llm_client import LLMClient

def main():
    llm = LLMClient(model_name="qwen2.5")
    skill = SectionMappingSkill(llm_client=llm)

    # Dummy custom criteria
    custom_criteria = {
        "objective_clarity": "Is the objective clear?",
        "architecture_description": "Are there diagrams and layer descriptions?",
        "dataset_availability": "Are datasets public?"
    }

    # Dummy sections extracted from a paper
    paper_sections_dict = {
        "Abstract": "...",
        "1 Introduction": "...",
        "2 Background": "...",
        "3 Model Architecture": "...",
        "3.1 Attention": "...",
        "4 Training": "...",
        "5 Results": "...",
        "6 Conclusion": "..."
    }

    context = {
        "criteria_mode": "free",
        "custom_criteria": custom_criteria,
        "paper_sections": paper_sections_dict
    }

    print("Running SectionMappingSkill...")
    result = skill.execute(context)
    
    print("\n==== RESULT ====")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
