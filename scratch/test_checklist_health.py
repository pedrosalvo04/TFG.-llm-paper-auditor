# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from frontend.utils.scoring import get_checklist_health

mock_eval = {
    'claims': {'answer': 'Yes', 'evidence': 'See Section 1', 'justification': '', 'is_no_justified': False},
    'limitations': {'answer': 'Yes', 'evidence': 'Section 6', 'justification': '', 'is_no_justified': False},
    'theory_assumptions_proofs': {'answer': 'N/A', 'evidence': '', 'justification': 'No theoretical results', 'is_no_justified': False},
    'experimental_result_reproducibility': {'answer': 'Yes', 'evidence': 'Appendix A', 'justification': '', 'is_no_justified': False},
    'open_access_data_code': {'answer': 'No', 'evidence': '', 'justification': 'Code is proprietary', 'is_no_justified': True},
    'experimental_setting_details': {'answer': 'Yes', 'evidence': 'Section 4.1', 'justification': '', 'is_no_justified': False},
    'experiment_statistical_significance': {'answer': 'No', 'evidence': '', 'justification': '', 'is_no_justified': False},
    'experiments_compute_resource': {'answer': 'Yes', 'evidence': 'Section 5', 'justification': '', 'is_no_justified': False},
    'code_of_ethics': {'answer': 'Yes', 'evidence': 'Ethics statement', 'justification': '', 'is_no_justified': False},
    'broader_impacts': {'answer': 'Yes', 'evidence': 'Appendix C', 'justification': '', 'is_no_justified': False},
    'safeguards': {'answer': 'N/A', 'evidence': '', 'justification': 'No high-risk models released', 'is_no_justified': False},
    'licenses': {'answer': 'Yes', 'evidence': 'Section 2.1', 'justification': '', 'is_no_justified': False},
    'assets': {'answer': 'N/A', 'evidence': '', 'justification': 'No new assets released', 'is_no_justified': False},
    'crowdsourcing_human_subjects': {'answer': 'N/A', 'evidence': '', 'justification': 'No human subjects', 'is_no_justified': False},
    'irb_approvals': {'answer': 'N/A', 'evidence': '', 'justification': 'No human subjects', 'is_no_justified': False},
    'declaration_llm_usage': {'answer': 'N/A', 'evidence': '', 'justification': 'LLM used only for writing', 'is_no_justified': False},
}

health = get_checklist_health(mock_eval)
print("Status:", health["status"])
print("Pending:", health["pending_count"], "/", health["total"])
for item in health['items']:
    if item['alert_msg']:
        print("  ALERT [" + item["label"] + "]:", item["alert_msg"])

# Verify item 7 (stats) is flagged as risk
stats_item = next(i for i in health['items'] if i['key'] == 'experiment_statistical_significance')
assert stats_item['pending_justification'] == True, "Item 7 should be flagged!"
assert health['status'] == 'risk', "Should be risk with unjustified No!"
print("Assertion passed: Item 7 (stats) correctly flagged as risk!")
print("All tests passed!")
