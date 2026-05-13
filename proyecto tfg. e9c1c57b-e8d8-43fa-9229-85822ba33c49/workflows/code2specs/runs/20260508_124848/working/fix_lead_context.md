### Token budget precalculation

=== TOKEN BUDGET PRECALCULATION ===
Total spec files size: 494,658 chars ≈ 148,397 tokens
Total source code: 4,927 LOC ≈ 14,781 tokens
Total validation reports: 12,181 chars ≈ 3,654 tokens
Combined: ≈ 166,832 tokens
Agent context window: ~120K tokens (usable ~80K after prompt+output)
==================================


### Validation reports

### validation_report_val_backward_coverage.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_backward_coverage.md
  size_chars: 14616
  yaml_metadata:
```yaml
validator_id: val_backward_coverage
validator_type: backward_coverage
target_specs:
  - 01_data_model.md
  - 02_functional_specs.md
  - 03_api_specs.md
  - 04_look_and_feel.md
  - 05_business_rules.md
  - 06_glossary.md
  - 07_module_index.md
  - 08_dependency_graph.md
  - 08_dependency_graph.json
  - extracted_*.md (working)
  - cross_ref_resolution_*.md (working)
forward_coverage_pct: N/A
backward_coverage_pct: 100.00
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
total_candidate_files: 27
covered_files: 27
partial_files: 0
fidelity_issues: 0
coverage_gaps: 0
depth_gaps: 0
spec_consistency_issues: 0
total_issues: 0
overall_status: pass
```

### validation_report_val_cross_check.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_cross_check.md
  size_chars: 22018
  yaml_metadata:
```yaml
validator_id: val_cross_check
validator_type: cross_check
target_specs:
  - 01_data_model.md
  - 02_functional_specs.md
  - 02_functional_backend.md
  - 03_technical_specs.md
  - 04_look_and_feel.md
  - 07_module_index.md
  - 08_dependency_graph.json
  - 08_dependency_graph.md
forward_coverage_pct: N/A
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 0
coverage_gaps: 1
depth_gaps: 0
spec_consistency_issues: 8
total_issues: 9
overall_status: needs_review
```

### validation_report_val_data_model_completeness.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_data_model_completeness.md
  size_chars: 23045
  yaml_metadata:
```yaml
validator_id: val_data_model_completeness
validator_type: data_model_completeness
target_specs: [01_data_model.md]
forward_coverage_pct: 75
backward_coverage_pct: 78
depth_pct: 85
entity_completeness_pct: 58
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 0
coverage_gaps: 5
depth_gaps: 0
spec_consistency_issues: 0
total_issues: 5
overall_status: fail
```

### validation_report_val_dep_graph_schema.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_dep_graph_schema.md
  size_chars: 10452
  yaml_metadata:
```yaml
validator_id: val_dep_graph_schema
validator_type: dependency_graph_schema
target_specs: [08_dependency_graph.json, 08_dependency_graph.md]
forward_coverage_pct: N/A
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: 76.4
consolidator_preservation_pct: N/A
fidelity_issues: 0
coverage_gaps: 0
depth_gaps: 0
spec_consistency_issues: 0
total_issues: 115
overall_status: fail
```

### validation_report_val_depth_apis.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_depth_apis.md
  size_chars: 14097
  yaml_metadata:
```yaml
validator_id: val_depth_apis
validator_type: depth
target_specs: [03_technical_specs.md]
forward_coverage_pct: 91
backward_coverage_pct: N/A
depth_pct: 75
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 0
depth_gaps: 7
spec_consistency_issues: 0
total_issues: 9
overall_status: needs_review
```

### validation_report_val_depth_business_rules.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_depth_business_rules.md
  size_chars: 36930
  yaml_metadata:
```yaml
validator_id: val_depth_business_rules
validator_type: depth
target_specs: [02_functional_backend.md, 02_functional_frontend.md]
forward_coverage_pct: 75.0
backward_coverage_pct: N/A
depth_pct: 55.2
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 12
coverage_gaps: 0
depth_gaps: 14
spec_consistency_issues: 2
total_issues: 28
overall_status: fail
```

### validation_report_val_depth_entities.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_depth_entities.md
  size_chars: 25052
  yaml_metadata:
```yaml
validator_id: val_depth_entities
validator_type: depth
target_specs: [01_data_model.md]
forward_coverage_pct: 92
backward_coverage_pct: N/A
depth_pct: 91
entity_completeness_pct: 50
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 3
depth_gaps: 10
spec_consistency_issues: 0
total_issues: 15
overall_status: fail
```

### validation_report_val_forward_backend_pipeline.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_forward_backend_pipeline.md
  size_chars: 32742
  yaml_metadata:
```yaml
validator_id: val_forward_backend_pipeline
validator_type: forward_coverage
target_specs: [02_functional_backend.md]
forward_coverage_pct: 24.4
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 34
coverage_gaps: 0
depth_gaps: 3
spec_consistency_issues: 0
total_issues: 37
overall_status: fail
```

### validation_report_val_forward_backend_rag_sota.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_forward_backend_rag_sota.md
  size_chars: 37113
  yaml_metadata:
```yaml
validator_id: val_forward_backend_rag_sota
validator_type: forward_coverage
target_specs: [02_functional_backend.md]
forward_coverage_pct: 42
backward_coverage_pct: N/A
depth_pct: 55
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 32
coverage_gaps: 0
depth_gaps: 15
spec_consistency_issues: 2
total_issues: 49
overall_status: fail
```

### validation_report_val_forward_data_model.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_forward_data_model.md
  size_chars: 27474
  yaml_metadata:
```yaml
validator_id: val_forward_data_model
validator_type: forward_coverage
target_specs: [01_data_model.md]
forward_coverage_pct: 99
backward_coverage_pct: N/A
depth_pct: 67
entity_completeness_pct: 50
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 2
depth_gaps: 3
spec_consistency_issues: 0
total_issues: 7
overall_status: needs_review
```

### validation_report_val_forward_frontend.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_forward_frontend.md
  size_chars: 32427
  yaml_metadata:
```yaml
validator_id: val_forward_frontend
validator_type: forward_coverage
target_specs: [02_functional_frontend.md]
forward_coverage_pct: 92
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 8
coverage_gaps: 1
depth_gaps: 2
spec_consistency_issues: 0
total_issues: 11
overall_status: needs_review
```

### validation_report_val_forward_technical.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_forward_technical.md
  size_chars: 24370
  yaml_metadata:
```yaml
validator_id: val_forward_technical
validator_type: forward_coverage
target_specs: [03_technical_specs.md]
forward_coverage_pct: 98
backward_coverage_pct: N/A
depth_pct: 86
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 1
coverage_gaps: 5
depth_gaps: 2
spec_consistency_issues: 0
total_issues: 8
overall_status: needs_review
```

### validation_report_val_glossary_completeness.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_glossary_completeness.md
  size_chars: 32901
  yaml_metadata:
```yaml
validator_id: val_glossary_completeness
validator_type: glossary_completeness
target_specs: [06_glossary.md]
forward_coverage_pct: 93.75
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: 93.75
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 2
coverage_gaps: 2
depth_gaps: 1
spec_consistency_issues: 0
total_issues: 5
overall_status: needs_review
```

### validation_report_val_laf_completeness.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_laf_completeness.md
  size_chars: 26543
  yaml_metadata:
```yaml
validator_id: val_laf_completeness
validator_type: look_and_feel_completeness
target_specs: [04_look_and_feel.md]
forward_coverage_pct: 91.1
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: 78.9
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 4
coverage_gaps: 1
depth_gaps: 8
spec_consistency_issues: 0
total_issues: 13
overall_status: needs_review
```

### validation_report_val_module_index_completeness.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_module_index_completeness.md
  size_chars: 9873
  yaml_metadata:
```yaml
validator_id: val_module_index_completeness
validator_type: module_index_completeness
target_specs: [07_module_index.md]
forward_coverage_pct: 95
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: 100
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 1
coverage_gaps: 0
depth_gaps: 0
spec_consistency_issues: 1
total_issues: 2
overall_status: needs_review
```

### validation_report_val_test_scenarios_coverage.md
  abs_path: /app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/validation_report_val_test_scenarios_coverage.md
  size_chars: 23072
  yaml_metadata:
```yaml
validator_id: val_test_scenarios_coverage
validator_type: forward_coverage
target_specs: [05_test_scenarios.md]
forward_coverage_pct: 86.6
backward_coverage_pct: N/A
depth_pct: N/A
entity_completeness_pct: N/A
ui_detail_pct: N/A
glossary_completeness_pct: N/A
module_index_completeness_pct: N/A
schema_compliance_pct: N/A
consolidator_preservation_pct: N/A
fidelity_issues: 0
coverage_gaps: 0
depth_gaps: 0
spec_consistency_issues: 0
total_issues: 0
overall_status: needs_review
```


### Inventory summary (metadata only)
{
  "summary": {
    "total_files": 54,
    "total_loc": 4927,
    "total_size_bytes": 256409,
    "project_types": [],
    "tech_distribution": {
      "unknown": 54
    },
    "group_distribution": {
      "other": 54
    },
    "directory_count": 13
  },
  "project_types": [],
  "tech_distribution": {
    "unknown": 54
  },
  "group_distribution": {
    "other": 54
  }
}

### Specs file list

### 01_data_model.md (47926 chars)

### 02_functional_backend.md (87727 chars)

### 02_functional_frontend.md (58700 chars)

### 03_technical_specs.md (34793 chars)

### 04_look_and_feel.md (36902 chars)

### 05_test_scenarios.md (56604 chars)

### 06_glossary.md (42669 chars)

### 07_module_index.md (67990 chars)

### 08_dependency_graph.md (61347 chars)
