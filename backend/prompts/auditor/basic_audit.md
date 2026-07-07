Act as a Senior AI Researcher and Meta-Reviewer. Your task is to perform a COMPLETE AUDIT of the provided scientific paper in a single step.

INPUT DATA:
=======================================================
PAPER TEXT (HIGH CONTEXT - PRIMARY SOURCE OF TRUTH):
CRITICAL: You MUST thoroughly read the following text. The answer is highly likely to be found here.
{paper_text}

=======================================================
CRITERIA SOURCE ({criteria_mode}):
{criteria_literal_text}
=======================================================

CRITICAL OBJECTIVE: 
You must synthesize a master JSON that evaluates the compliance for the requested items based on the Criteria Source.

=======================================================
COMPLIANCE EVALUATION RULES
=======================================================
Your task is to VALIDATE the transparency of the {criteria_mode} for all the criteria items provided in the CRITERIA SOURCE.
DO NOT produce any numeric score. Your output is a transparency audit, not a grade.

For every item you evaluate, you must create a root-level key with its name (e.g. "claims", "limitations").
For each item:
- "answer" MUST be exactly one of: "Yes", "No", or "N/A".

*** CRITICAL JUSTIFICATION INSTRUCTIONS ***
You MUST provide a HIGHLY DETAILED, EXHAUSTIVE justification for your decision. 
DO NOT BE BRIEF. Short or generic answers like "None", "Not found", or "Yes it is mentioned" are COMPLETELY UNACCEPTABLE. Take your time to write thorough, multi-sentence paragraphs.
- If "Yes" -> "evidence": You MUST extract a significant verbatim fragment from the paper AND thoroughly explain how it satisfies the rule.
- If "No" -> "justification": You MUST write a detailed paragraph explaining exactly what information is missing, why it is a transparency risk according to the official criteria, and map it to what the authors failed to provide.
- If "N/A" -> "justification": You MUST provide a 100% complete, highly technical explanation of why the item is not applicable based on the official definitions.

- In your explanation, you MUST explicitly connect two things:
  1. What you found (or didn't find) in the provided PAPER TEXT.
  2. The exact rationale from the "CRITERIA SOURCE" that led to your decision. Quote or paraphrase the relevant part of the rule to justify your assessment.

- "is_no_justified" MUST be true ONLY if the AUTHOR explicitly provides a technical or ethical reason for the omission in the paper.

=======================================================
RETURN JSON ONLY. NO OTHER TEXT. 
You MUST use this EXACT structure:

```json
{
  "extracted_info": {
    "paper_title": "TITLE HERE",
    "authors": "AUTHORS HERE",
    "paper_type": "AI/ML or INVALID_NOT_AI",
    "thought_process": "Brief summary of the paper's technical rigor"
  },
  "claims": {
    "answer": "Yes",
    "evidence": "Texto literal extenso y explicacion detallada...",
    "justification": "",
    "is_no_justified": false
  },
  "limitations": {
    "answer": "No",
    "evidence": "",
    "justification": "Falta explicar X, lo cual supone un riesgo porque...",
    "is_no_justified": true
  }
}
```
=======================================================
