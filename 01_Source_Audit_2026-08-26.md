# Source Audit — 2026-08-26

Cross-examination of the five source documents acquired 2026-08-26, per the
`source-audit` skill: five independent verifiers (one per source, checking
every EXPLICIT-labeled claim against the raw artifact), an adversarial
skeptic pass on consequential findings, and a K-layer coherence sweep across
the consuming documents. Four-eyes held throughout: no verifier audited its
own author-agent's output. 7 agents, 217 items checked in total.

## Verdict

**The acquisition corpus is sound: zero major content errors in 183
source-doc items.** Every verbatim quote, every number, every sha256, and
the load-bearing negative claims (AVO paper contains no ARC content; VISTA
has no companion paper) held under independent re-derivation. Six minor
locator slips were found and are now corrected in place. The coherence sweep
found **one major internal contradiction** — not in the sources but in this
repo's own state files — also now fixed.

## Per-source results

| Source doc | Checked | Verified | Major | Minor | Unverifiable |
|---|---|---|---|---|---|
| `AVO_2026.md` (arXiv PDF) | 34 | 33 | 0 | 1 | 0 |
| `AVO_NVIDIA_blog_2026-08.md` | 30 | 30 | 0 | 0 | 0 |
| `VISTA_2026.md` | 19 | 19 | 0 | 0 | 0 |
| `arc-skill_notes.md` (clone @ dba53c3) | 72 | 69 | 0 | 3 | 0 |
| `ARC_toolkit_notes.md` (installed 0.9.9) | 28 | 26 | 0 | 1 | 1 → cleared |
| Coherence sweep (consuming docs) | 34 | 30 | 1 | 3 | 0 |

## Findings and resolutions

**Minor locator corrections, applied to the source docs:**
1. `AVO_2026.md` — the §5.4 "in isolation" parenthetical sits on PDF **p. 10**, not p. 8 (the enclosing ABSENT claim was re-confirmed correct).
2. `arc-skill_notes.md` — `live.py:133-135` → **132-135** (the range had excluded the `predict` assignment).
3. `arc-skill_notes.md` — verbatim-labeled quote had `{mode}` where the f-string reads `{existing_mode}` (cli.py:235).
4. `arc-skill_notes.md` — `README.md:82-88` → **81-88** (quote opens on line 81).

**Substantive caveat, added to `ARC_toolkit_notes.md`:** the upstream README's
"constructor arguments take precedence over environment variables" is quoted
faithfully but is **false for one parameter** in the installed 0.9.9:
`base.py:101-111` makes `OPERATION_MODE=competition` in the environment
override the constructor. A warning block now sits beside the quote.

**Skeptic clearance (the adversarial layer working as designed):** the one
UNVERIFIABLE — two web-artifact byte counts with no local archive — was
**refuted by the skeptic**, who re-fetched both URLs and matched both figures
exactly (16,856 / 21,311 bytes). Following its recommendation, both files
are now archived: `_raw/arcprize_arc-agi_README_2026-08-26.md`
(sha256 `26176d96…3864`) and
`_raw/arc-agi-3-benchmarking_add_anthropic_sdk_2026-08-26.md`
(sha256 `684b1489…4e66b`) — this session's own re-fetch reproduced both
byte counts a third time.

**Coherence findings (K layer), all fixed this session:**
1. **MAJOR:** `STATE.md` still described Step 0 as 🟡-pending and the budget
   as 🔴-unset while `Experiment_Spec.md` §8 recorded both as ruled, same
   date — a cold-reading session would have refused approved work. STATE.md
   §2/§5 now carry the rulings.
2. Spec header line 3 still said "Status: proposed" → now "ruled 2026-08-26".
3. Spec §4's "set after this number exists, not before" contradicted §8.2's
   $50-ahead ruling → annotated with the ruling and the surviving principle.
4. Spec footer's 2026-08-22 "blog + arXiv" source pairing blurred the
   blog-only scope split (Gotchas #307) → rewritten to point at
   `Sources/Source_Index.md`.

## Residuals

None open. All findings either corrected in place or cleared by the skeptic;
no confabulated closures — every correction traces to a primary-artifact
read logged in the workflow journal (`wf_33a9d05d-132`).
