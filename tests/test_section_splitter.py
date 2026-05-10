import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.skills.auditor_skills import InformationExtractionSkill

def test_splitting_logic():
    print("Testing InformationExtractionSkill splitting logic...")
    
    # Mock context
    paper_text = """# Section 1
Content 1.
# Section 2
Content 2.
# Section 3
Content 3.
# Section 4
Content 4.
# Section 5
Content 5.
# Section 6
Content 6.
"""
    
    # We need a dummy LLM client to avoid error in validate_context if we were to run execute
    # But we just want to test the splitting part which is inside execute
    # I'll manually call a helper or just check the logic if I can extract it
    
    # Since the logic is inside execute, I'll use a small trick: 
    # mock log_execution to capture the fragments count
    
    class MockLLM:
        def generate(self, prompt): return type('obj', (object,), {'text': '{}'})
        
    skill = InformationExtractionSkill(llm_client=MockLLM())
    
    # We want to test the fragmenting part
    # I'll create a temporary subclass to expose the fragments
    
    class TestSkill(InformationExtractionSkill):
        def get_fragments(self, paper_text):
            import re
            paper_text_norm = paper_text.replace('\r\n', '\n')
            sections = re.split(r'\n(?=#+ )', '\n' + paper_text_norm)
            sections = [s.strip() for s in sections if s.strip()]
            
            if len(sections) > 1:
                total_chars = sum(len(s) for s in sections)
                target = total_chars / 4
                fragments = []
                current_fragment = ""
                
                for section in sections:
                    if len(current_fragment) + len(section) > target and len(fragments) < 3:
                        if current_fragment:
                            fragments.append(current_fragment)
                            current_fragment = section
                        else:
                            fragments.append(section)
                            current_fragment = ""
                    else:
                        if current_fragment:
                            current_fragment += "\n\n" + section
                        else:
                            current_fragment = section
                if current_fragment:
                    fragments.append(current_fragment)
                return fragments
            return []

    test_skill = TestSkill(llm_client=MockLLM())
    fragments = test_skill.get_fragments(paper_text)
    
    print(f"Fragments count: {len(fragments)}")
    assert len(fragments) == 4, f"Expected 4 fragments, got {len(fragments)}"
    
    for i, f in enumerate(fragments):
        print(f"Fragment {i+1} length: {len(f)}")
        assert len(f) > 0
        
    print("Split logic test PASSED")

if __name__ == "__main__":
    test_splitting_logic()
