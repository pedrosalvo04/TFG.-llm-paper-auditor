#!/usr/bin/env python3
"""Cross-reference analyzer — scans extracted_*.md files for GAP markers
and checks resolution status. Informational tool for the extraction fix lead."""

import os, re, json, argparse

def scan_gaps(output_dir):
    gaps = []
    gap_patterns = [
        re.compile(r'GAP_ID:\s*(GAP-\S+)'),
        re.compile(r'CROSS-REFERENCE:\s*(.+)'),
        re.compile(r'CROSS_REFERENCE:\s*(.+)'),
        re.compile(r'GAP:\s*(.+)'),
    ]
    for fname in sorted(os.listdir(output_dir)):
        if not (fname.startswith("extracted_") and fname.endswith(".md")):
            continue
        filepath = os.path.join(output_dir, fname)
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in gap_patterns:
                    match = pattern.search(line)
                    if match:
                        gaps.append({
                            "source_file": fname, "line": line_num,
                            "marker": match.group(0),
                            "detail": match.group(1).strip(),
                        })
    return gaps

def check_resolutions(gaps, output_dir):
    entity_index = {}
    for fname in sorted(os.listdir(output_dir)):
        if not (fname.startswith("extracted_") and fname.endswith(".md")):
            continue
        with open(os.path.join(output_dir, fname), 'r',
                  encoding='utf-8', errors='replace') as f:
            for m in re.finditer(r'SOURCE:\s*(\S+):(\d+)', f.read()):
                entity_index[m.group(1)] = fname
    resolved, unresolved, malformed = [], [], []
    for gap in gaps:
        file_refs = re.findall(r'(\w+\.\w+)', gap['detail'])
        if not file_refs:
            malformed.append(gap)
            continue
        found = False
        for ref in file_refs:
            if ref in entity_index:
                gap['resolved_in'] = entity_index[ref]
                resolved.append(gap)
                found = True
                break
        if not found:
            unresolved.append(gap)
    return resolved, unresolved, malformed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    gaps = scan_gaps(args.output_dir)
    resolved, unresolved, malformed = check_resolutions(gaps, args.output_dir)
    report = {
        "total_gaps": len(gaps), "resolved": len(resolved),
        "unresolved": len(unresolved), "malformed": len(malformed),
        "unresolved_details": unresolved[:50],
        "malformed_details": malformed[:20],
    }
    report_path = os.path.join(args.output_dir, "cross_ref_analysis.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Total GAPs: {len(gaps)} | Resolved: {len(resolved)} | "
          f"Unresolved: {len(unresolved)} | Malformed: {len(malformed)}")

if __name__ == '__main__':
    main()
