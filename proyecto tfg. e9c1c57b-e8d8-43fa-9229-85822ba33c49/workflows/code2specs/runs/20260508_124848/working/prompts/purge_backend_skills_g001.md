## PATH SANDBOX

- READ-ONLY (source code): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input`
- READ-ONLY (pipeline output / existing extractions): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working`
- WRITE-ONLY (corrected extraction): `/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_skills_01.md`

**DO NOT read or write ANY other directory.**

---

## AGENT IDENTITY

Agent ID: `purge_backend_skills_g001`
Agent type: `purge_hallucination`
Cluster: `cluster_backend_skills_01`
Estimated complexity: small (1 gap, 1 file, 1 prose correction)

---

## MISSION

You are a hallucination-purge agent. Your sole task is to remove or correct one confirmed hallucinated claim in the existing extraction file `extracted_backend_skills_01.md`. You do NOT add new content, you do NOT rewrite sections beyond the narrow correction scope, and you do NOT insert `[GAP]` markers (see scope note below). The runner has already tagged a pre-fix git snapshot — your output will be written IN PLACE as a full file replacement, and the original is recoverable.

---

## REVIEWER FEEDBACK — ADDRESS EACH ITEM

```
FIDELITY_ISSUE | id: g_001 | severity: LOW | legitimacy: hallucinated_content | action: targeted_fix | source: extracted_backend_skills_01.md | location: backend/skills/__init__.py:36–51 | detail: Section 1.1 prose states "The `__all__` list (lines 36-52) exports exactly **14** symbols" — verified count against `__init__.py:36–51` is **15** (BaseSkill + 4 auditor + 2 chatbot + 5 sota + 3 regex). The accompanying table in the same section correctly lists 15 entries; the prose count is wrong. Additionally, `SOURCE: __init__.py:1` points to the module docstring line (`"""Módulo de skills para agentes IA"""`), not to the `__all__` declaration at lines 36–51. Fix: correct count to 15 and update SOURCE to `__init__.py:36`.
```

---

## SCOPE CONSTRAINT (CRITICAL — READ BEFORE ACTING)

This gap involves a **single wrong number in prose text** and a **wrong SOURCE line annotation**. The correct value (15) is independently confirmed by:
1. The accompanying table in Section 1.1 of `extracted_backend_skills_01.md` — which already lists all 15 symbols correctly and **MUST NOT be changed**.
2. The source file `backend/skills/__init__.py` lines 36–51.

Because the correct value is confirmed and the surrounding table is accurate, **do NOT insert a `[GAP_ID: hall_...]` marker** in place of the removed content. This is a correction of a wrong number, not a removal of fabricated content requiring a placeholder. Simply correct the prose and the SOURCE annotation.

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1 — Read the existing extraction file

Read the full file:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_skills_01.md
```

Locate **Section 1.1**. Find:
- The prose sentence containing `"exports exactly **14** symbols"` (or equivalent wording with the number 14).
- The `SOURCE: __init__.py:1` annotation that accompanies the `__all__` description in that section.

Record both the exact original sentence and the exact original SOURCE annotation verbatim — you will need them for the PURGE LOG.

### Step 2 — Verify the hallucination against source

Read the source file:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/input/TFG.-llm-paper-auditor-multimodels/backend/skills/__init__.py
```

Read lines 36–51 (±5 lines for context). Count the entries in the `__all__` list exactly as they appear. Confirm:
- The actual count is **15** (expected breakdown: BaseSkill × 1, auditor × 4, chatbot × 2, sota × 5, regex × 3).
- The `__all__` declaration begins at approximately **line 36**, NOT at line 1.
- Line 1 (or nearby) contains the module docstring `"""Módulo de skills para agentes IA"""`, which is irrelevant to the `__all__` export count.

If your count differs from 15, count again carefully. Do NOT proceed until you have confirmed the exact count from source. Whatever count the source actually shows is the correct value — use it.

Also confirm what exact line number the `__all__` assignment starts on. Use that line number for the corrected SOURCE annotation (expected: line 36, but use the actual line if it differs).

### Step 3 — Perform the correction

Make exactly two targeted changes in Section 1.1:

**Change A — Prose count:**
Replace the hallucinated number `14` with the confirmed number (`15`, or whatever your count from Step 2 yields) in the prose sentence that describes how many symbols `__all__` exports. Change nothing else in that sentence or paragraph.

**Change B — SOURCE annotation:**
Replace `SOURCE: __init__.py:1` with `SOURCE: __init__.py:36` (or the actual line number where `__all__` begins, as confirmed in Step 2).

**Do NOT:**
- Alter the accompanying table (it is already correct).
- Rephrase, expand, or condense any other prose.
- Add `[GAP]` markers anywhere.
- Remove any other content from the file.
- Change headings, formatting, or any section outside Section 1.1.
- Add new extraction content.

### Step 4 — Write the PURGE LOG

Prepend the following section at the very top of the file (before all other content), formatted exactly as shown:

```markdown
## PURGE LOG
Agent: purge_backend_skills_g001
Run date: <ISO-8601 date>

| gap_id | original claim | source check performed | correction applied |
|--------|---------------|----------------------|-------------------|
| g_001 | Prose in Section 1.1 stated "exports exactly **14** symbols"; SOURCE annotation pointed to `__init__.py:1` (module docstring line) | Read `backend/skills/__init__.py:36–51`; counted entries in `__all__` literal; confirmed actual count is **15** (BaseSkill + 4 auditor + 2 chatbot + 5 sota + 3 regex); confirmed `__all__` declaration starts at line 36, not line 1 | Changed prose count from `14` to `15`; updated SOURCE from `__init__.py:1` to `__init__.py:36`; table left unchanged (already correct) |

No [GAP] markers inserted: the correct value is confirmed by source and by the existing table — a structured absence placeholder is not appropriate here.
```

### Step 5 — Write the corrected file IN PLACE

Write the complete corrected file (full replacement) to:
```
/app/projects/e9c1c57b-e8d8-43fa-9229-85822ba33c49/workflows/code2specs/runs/20260508_124848/working/extracted_backend_skills_01.md
```

The file must contain:
1. The `## PURGE LOG` section at the top (from Step 4).
2. The rest of the original `extracted_backend_skills_01.md` content, with exactly the two corrections from Step 3 applied to Section 1.1.
3. Nothing else added or removed.

Do NOT create a sidecar file such as `fixed_extracted_backend_skills_01.md` or `purge_g001.md`. Synthesis reads only `extracted_*.md` files. Sidecar outputs will be ignored.

---

## FIDELITY RULE

Extract ONLY what the source code demonstrates. Never invent. Every element MUST include `SOURCE: file:line`. If something cannot be determined, mark as `UNRESOLVABLE`. The correction you are making here restores fidelity — the table was already correct, and you are aligning the prose to match both the table and the source.

## LEGITIMACY-FIRST RULE

The hallucination here is a wrong number in prose (`14` instead of `15`) and a wrong line citation (`__init__.py:1` instead of `__init__.py:36`). The content is not fabricated in the sense of inventing non-existent symbols — the symbols are real and the table is correct. The prose count is simply wrong. Because the correct value is verifiable and confirmed, do NOT replace the prose with a `[GAP]` block. Correct it directly.

---

## WHAT SUCCESS LOOKS LIKE

After your write:
- `extracted_backend_skills_01.md` opens with `## PURGE LOG`.
- Section 1.1 prose reads `"exports exactly **15** symbols"` (or equivalent).
- Section 1.1 SOURCE annotation for `__all__` reads `SOURCE: __init__.py:36`.
- The 15-row symbol table in Section 1.1 is byte-for-byte identical to the original.
- All other sections of the file are byte-for-byte identical to the original.
- No `fixed_*.md` or sidecar files were created.