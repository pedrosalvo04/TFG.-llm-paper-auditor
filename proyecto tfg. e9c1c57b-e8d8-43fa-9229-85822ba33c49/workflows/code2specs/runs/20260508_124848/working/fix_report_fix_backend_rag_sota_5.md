## Fix Report — fix_backend_rag_sota_5

### Issue #49

- **Validation report section:** Spec Consistency Issues — SC02 — HybridHP Section 3 vs Section 11 context key naming
- **Issue type:** SPEC_CONSISTENCY / INCORRECT_CLAIM (systematic wrong key name)
- **Issue description:** The spec systematically uses `hyperparameter_results` as the output context key for HybridHyperparameterExtractionSkill across §1.1 (Phase Summary Table), §1.2 (Context Keys for Phase 4), §3.5 Step 7 (merge description and GAP marker), §3.6 (Output Context Keys table), §3.7 (return shapes), and §7.x (MetadataAggregationSkill flat dict note). The actual key emitted by the skill is `extracted_hyperparameters_hybrid` (plus `triage_fragments` as a second output). This is a cross-section naming inconsistency that would cause any caller using the documented key name to miss the actual context value.
- **Spec location:** `02_functional_backend.md` §1.1 (Phase 1.5 row), §1.2 (context key table), §3.5 Step 7, §3.6, §3.7, §7.x (MetadataAggregationSkill flat dict note)

---

**Source evidence:**

- `rag_extraction_skill.py:268–271` — success return:
  ```python
  return {
      'extracted_hyperparameters_hybrid': cleaned_data,
      'triage_fragments': extracted_fragments
  }
  ```
- `rag_extraction_skill.py:32` — guard failure return:
  ```python
  return {'extracted_hyperparameters_hybrid': {}}
  ```
- `rag_extraction_skill.py:275` — exception failure return:
  ```python
  return {'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str(e)}
  ```
- `auditor.py:120` — caller checks `hybrid_hp_result.get('extracted_hyperparameters_hybrid')`
- `auditor.py:126–127` — `triage_fragments` stored in context as `hybrid_triage_fragments`
- `auditor.py:130–131` — `context['extracted_hyperparameters_hybrid']` consumed by subsequent logic
- `auditor.py:192–193` — `context['extracted_hyperparameters_hybrid']` propagated to `final_result`

---

**Changes applied:**

1. **§1.1 Phase Summary Table (line 46):** Output column changed from `hyperparameter_results` (dict) → `extracted_hyperparameters_hybrid` (dict).
2. **§1.2 Context Keys for Phase 4 (line 61):** Table row changed from `` `hyperparameter_results` | dict | Phase 1.5 `` → `` `extracted_hyperparameters_hybrid` | dict | Phase 1.5 ``.
3. **§3.5 Step 7 (line 459):** Prose changed: "merged into a single `hyperparameter_results` dict" → "merged into a single `extracted_hyperparameters_hybrid` dict".
4. **§3.5 Step 7 GAP marker (line 461):** GAP text updated: `[GAP: exact merge deduplication strategy for hyperparameter_results ...]` → `[GAP: exact merge deduplication strategy for extracted_hyperparameters_hybrid ...]`. (Note: this is a plain `[GAP: ...]` marker, not a post-purge `[GAP_ID: hall_*]` marker; renaming the key inside the text is correct.)
5. **§3.6 Output Context Keys table (lines 467–468):** Row changed from `` `hyperparameter_results` | dict | Merged hyperparameter... `` → `` `extracted_hyperparameters_hybrid` | dict | Merged hyperparameter... ``, and a second row added for `` `triage_fragments` | list | Raw per-chunk extraction fragments... `` (SOURCE: `rag_extraction_skill.py:270`).
6. **§3.7 Return shapes (lines 474–487):** Replaced incorrect `{"success": True, "hyperparameter_results": dict}` / `{"success": False, "error": str, "phase": ...}` with three accurate shapes from source:
   - Success: `{'extracted_hyperparameters_hybrid': dict, 'triage_fragments': list}`
   - Exception failure: `{'extracted_hyperparameters_hybrid': {}, 'hybrid_extraction_error': str}`
   - Guard failure: `{'extracted_hyperparameters_hybrid': {}}`
7. **§7.x MetadataAggregationSkill flat dict note (line ~849):** Prose example updated from `hyperparameter_results` → `extracted_hyperparameters_hybrid`.

- **GAP marker used:** NO (the plain `[GAP: ...]` marker text was updated to reflect the correct key name; no new gap was introduced)
- **Rationale:** SC02 identified that the wrong output context key (`hyperparameter_results`) was used consistently across six distinct locations in the spec, contradicting the actual key emitted by `rag_extraction_skill.py:268–271`. This fix replaces all occurrences with the correct key `extracted_hyperparameters_hybrid` and also documents the second output key `triage_fragments` (SOURCE: `rag_extraction_skill.py:270`) and the accurate return shapes for all three code paths (success, exception, guard), fully resolving the naming inconsistency identified in SC02.
