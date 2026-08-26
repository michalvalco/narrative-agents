# Source Index — narrative-agents

One row per source; statuses per the acquisition session of 2026-08-26
(agents ran under the Phase-2 discipline: citation block, access date,
sha256 for binaries, EXPLICIT / STRONG INFERENCE / SPECULATIVE labels,
numbers quoted verbatim). Raw binaries in `_raw/`.

| Source | File | Status | Notes |
|---|---|---|---|
| AVO paper, arXiv 2603.24517 (v1, 2026-03-25) | `AVO_2026.md` (+ `_raw/AVO_arXiv2603.24517.pdf`, sha256 `1536be70…4727`; `AVO_arXiv2603.24517_fulltext.md`) | ACQUIRED — **scope caveat** | The paper is AVO for GPU-kernel optimization. **It contains no ARC-AGI-3 content**: no "ARC", no RHAE, no 6,624, no model name, no public/private statement, no Limitations section. Architecture quotes (agent loop, persistent memory, supervisor) are page-cited. |
| NVIDIA developer blog, "NVIDIA AVO Reaches 100% on ARC-AGI-3…" (2026-08-21) | `AVO_NVIDIA_blog_2026-08.md` (+ `_raw/AVO_NVIDIA_blog_2026-08-21.html`, sha256 `ca9e6d03…fc67c`) | ACQUIRED | **The only source for AVO's ARC-AGI-3 claims**: 100.00 RHAE, 25 environments, 183 levels, 6,624 actions (vs VISTA's 7,542), Claude Opus 5 backbone, public-set-only disclaimer, memory-contribution-not-isolated caveat. Carries a post-publication editor's note on its public/private wording. |
| VISTA project page (MIT; Han, Hu, Qiu, Wu, He; 2026-08-05) | `VISTA_2026.md` (+ `_raw/vista-research.github.io_index_2026-08-26.html`, sha256 `220ed4c1…f1ec6`) | ACQUIRED | Per-game table machine-parsed and checksum-verified (25 games × 2 models, 183 levels; totals 7,542 / 10,063 / 17,135). Full prompt, GUIDE/WORKING compaction paragraph, contamination caveat verbatim. **No companion paper exists** as of 2026-08-26 — cite the site's own `@misc` BibTeX. |
| pbshgthm/arc-skill (clone @ `dba53c3`) | `arc-skill_notes.md` (clone: `vendor/arc-skill/`, gitignored) | ACQUIRED | Prediction-gate code path (cli.py:103-108, predictions.py, live.py), 37.1%/2.9% at README.md:114-117, pins `arc-agi==0.9.9`, numpy≥2,<3, pillow≥10,<13. Site (arc-skill.vercel.app) captured via rendered fetch; its "900 lines of tests" claim unverified in the clone. |
| ARC-AGI Toolkit + benchmarking repo (arcprize) | `ARC_toolkit_notes.md` | ACQUIRED | Arcade params, OperationMode (NORMAL/ONLINE/OFFLINE/COMPETITION), JSONL recording format (STRONG INFERENCE — no formal upstream schema), scorecard + key scope, Anthropic provider YAML verbatim. One stale-doc discrepancy recorded. |
| Claude Code hooks reference | `claude_code_hooks_reference.md` | ACQUIRED (2026-08-25) | Canonical copy; `Claude_Protocols/PROMPT_Harness_Phase0_2026-08-22.md` references it here. |

**CPKI transfer candidates** (flagged only — earned-entry discipline, Michal decides):
the AVO paper-vs-blog scope split (a citation-integrity case study); VISTA's
"self as operator-editable file" evidence for the techno-gnosticism line; the
per-game human-baseline table as reusable benchmark data.
