# PROMPT — Ablation Setup (Claude Code, Execution Layer)

**Created:** 2026-08-22 (Thinking-Layer session; Claude Fable 5) · **Repo:** `narrative-agents` · **Paste into a fresh Claude Code Desktop session bound to this repo.**

> Signal line for the session: **"Working on narrative-agents, v3 ablation setup, task: acquire sources, prepare environment, write (do not run) the Step 0 dry-run harness."**

---

## 0. Read first (in this order; read-only)

1. `Experiment_Spec.md` — the design (arms, games, controls, metrics, cost gate, v3 layout). It is the contract for everything below.
2. `Paper_Outline.md` — Michal's document; **do not edit it** (see Task F).
3. `README.md`, `.claude/` (any CLAUDE.md or rules there), `narrative_agents/core.py` (skim headers + the relevance/threshold path), `examples/compare_rule_vs_llm.py`, `examples/llm_identity_formation.py`, and the run log `Narrative agents experiment 01 - Comparison and LLM identity formation.txt`.
4. `C:\Users\Michal Valco\GitHub\Claude_Protocols\Harness_Design.md` §7 and §12, `Loop_Design.md` §1–3, `Rules/Behavioral_Rules.md`, `Workflows/Document_Conversion.md`, and Gotchas **#276** (no side-effect "tests"), **#270** (rules that live only as prose), **#279** (read-before-assert).

Report the repo's actual state in ten lines before touching anything (files, branch, `.gitignore` coverage of `.env`, whether `STATE.md` exists). Gotcha #279 exists because the last session asserted this repo's state from memory.

## 1. Decision zones for this session

- 🟢 **Green (do):** acquisition of primary sources, source documentation, environment setup, code written but not executed against any paid API, unit tests that run offline, branch commits.
- 🟡 **Yellow (stop and ask):** **any action that spends model tokens or ARC API requests** (Step 0 itself, re-running the v2 LLM examples), any edit to `narrative_agents/core.py` beyond the threshold fix in Task D, any change to `Paper_Outline.md`.
- 🔴 **Red (never in this session):** budget decisions, publication claims, `git push` (no push without Michal's commit trigger phrase), handling or printing any API key.

Work on branch `ablation-setup`. Commit locally with conventional messages. UTF-8 everywhere.

## 2. Tasks

### A — Reconnaissance (read-only)
Produce `00_Recon_2026-08-22.md`: repo inventory; where the relevance threshold (0.7) lives and how `llm_identity_formation.py` scores relevance (the 0/10 core-memory artifact in the run log — Experiment_Spec §6); whether the v2 scripts read the model name from `.env` or hard-code it; current test coverage. Create `STATE.md` from `Claude_Protocols/_Project_Template/` if absent.

### B — Acquire and document primary sources (Green)
Create `Sources/` (and `Sources/_raw/` for binaries). For each source: fetch, convert with **markitdown** per `Workflows/Document_Conversion.md` (page-keyed markdown for PDFs), then write a source document with: full citation block, URL, access date, sha256 of any binary, **EXPLICIT / STRONG INFERENCE / SPECULATIVE** labels on every extracted claim, and verbatim page-cited quotes for anything numeric. Never paraphrase a number.

1. **AVO** — arXiv `2603.24517` (PDF → `Sources/_raw/AVO_arXiv2603.24517.pdf` → `Sources/AVO_2026.md`). Extract: architecture components (main loop, persistent memory, supervisor: exact wording and page), the sentence stating memory's contribution was not isolated, action counts (6,624), model used, the public-vs-private-set statement, limitations section.
2. **NVIDIA developer blog post** on AVO (URL in `Harness_Design.md` §12) → `Sources/AVO_NVIDIA_blog_2026-08.md`.
3. **VISTA** — `https://vista-research.github.io/` → `Sources/VISTA_2026.md`. Capture the **per-game table verbatim** (it is data we reuse in Experiment_Spec §2), the full prompt text, the three-tool spec, the compaction/continuation paragraph, and the contamination caveat. Search for an accompanying paper/tech report (arXiv, MIT); if one exists, acquire it the same way. Report if not.
4. **pbshgthm/arc-skill** — `git clone https://github.com/pbshgthm/arc-skill vendor/arc-skill` as a **read-only reference** (add `vendor/` to `.gitignore`; record the commit hash). **Do not run `npx skills add` and do not execute the CLI in this session.** Read `SKILL.md` and the CLI source; write `Sources/arc-skill_notes.md`: the prediction-gate mechanics (where the refusal happens, how the grade is computed), the local cache / offline-replay mode, the competition-mode flag, dependencies (`arc-agi` pin, numpy, pillow), and the 37.1% / 2.9% figures with the exact lines they come from. Also fetch the write-up at `https://arc-skill.vercel.app` → markdown.
5. **ARC-AGI Toolkit** — `https://github.com/arcprize/arc-agi` README (+ `docs.arcprize.org` quickstart) and **`arcprize/arc-agi-3-benchmarking`** README → `Sources/ARC_toolkit_notes.md`: `Arcade` constructor parameters, `OperationMode` values (NORMAL / ONLINE / OFFLINE / COMPETITION), recording format (JSONL, what fields), scorecard semantics, anonymous-key vs registered-key scope, the Anthropic provider configuration the benchmarking repo uses.
6. **Claude Code hooks reference** — `https://code.claude.com/docs/en/hooks` → `Sources/claude_code_hooks_reference.md`: verbatim sections for `PreCompact`, `PostCompact`, `Stop`, `SessionEnd`, `PostToolUse`, `PostToolBatch`, `SubagentStop`; exit-code semantics; handler types (`command`, `prompt`, `agent`, `http`, `mcp_tool`); stdin JSON fields. This document is shared with `Claude_Protocols/PROMPT_Harness_Phase0_2026-08-22.md` — write it here, reference it there.

Seed `Sources/Source_Index.md` (one row per source; status column). Flag CPKI transfer candidates in the report; **do not write to `Cross_Project_Knowledge_Index.md`** (earned-entry discipline; Michal decides).

### C — Environment (Green)
- Create a project venv (`uv` if present, else `python -m venv .venv`); `pip install arc-agi` pinned to the version `arc-skill` pins, plus `numpy`, `pillow`, `pytest`.
- `.env` exists. **Never print it, never commit it.** Verify `.gitignore` covers it; add an `.env.example` line `ARC_API_KEY=` with a comment pointing to `https://three.arcprize.org` (Michal registers; you never handle the key).
- Smoke-test the toolkit **offline only**: instantiate `Arcade` in `OperationMode.OFFLINE` with no key and no network, confirm the import path and the recording directory setting. Do not open a scorecard. Report what the anonymous key does and does not allow, from the docs, without exercising it.

### D — Selection rule (Green on the branch; **ruled by Michal 2026-08-22 — implement exactly Experiment_Spec §6**)
Implement **budgeted competitive selection with a floor and an inaugural memory** in `core.py` behind `selection=` (`"absolute"` = current 0.7 rule, kept for reproducing v2; `"budgeted"` = new default): parameters `budget` (int; default `ceil(expected_n/3)` or explicit), `floor` (0.30), pinned inaugural memory, displacement of the weakest non-inaugural member into `peripheral` with a `displaced` flag, raw score always logged on the `Memory`. Update `RELEVANCE_SYSTEM_PROMPT` to stop announcing the 0.7 threshold (telos-relative anchors only). Add a **balanced experience fixture** (two per type: error / failure / success / discovery / neutral). Offline tests (no API): (1) cold start — an empty-core Performer acquires an inaugural memory from the balanced set under synthetic scores; (2) displacement — a full core admits a stronger memory and flags the displaced one; (3) floor — trivia stays out of an empty core; (4) `selection="absolute"` reproduces the run-log counts from synthetic scores. Extend `memory_efficiency()` to report budget, floor, raw-score distribution per telos, and core composition by type. **Do not rerun the LLM examples** (tokens → Yellow); list the rerun as pending Michal's go.

### D′ — Archive hygiene (Green; the move already happened 2026-08-22)
`_Archive/2025-10_AI_Tools_working_folder/` now holds the former `AI Tools\narrative-agents\` working folder (59 content files; nested `.git` neutralized). **Add `_Archive/` to `.gitignore` before any `git add`.** Read `_Archive/README.md`; port (with tests, against the current `core.py`) the visualization scripts and `tests/test_narrative_agents.py` it names; leave the Medium drafts in place and index them in `STATE.md`.

### E — Step 0 harness skeleton: written, tested offline, **not run** (Green)
Build the v3 layout from Experiment_Spec §5:
- `harness/arm_B/SKILL.md` forked from `vendor/arc-skill/SKILL.md`, unchanged except the compaction instruction; `harness/arm_A/`, `harness/arm_C/` as stubs carrying their compaction prompts from `compaction/`.
- `compaction/A_summary.md`, `compaction/B_task_model.md`, `compaction/C_narrative.md` (the five-part schema, with the ~1,200-token cap stated in the prompt and enforced by a token counter).
- `metrics/` reading the toolkit's JSONL: per-level actions vs. human baseline, post-handoff burn (first 20 turns after each compaction), stagnation count, note tokens per compaction, prediction accuracy split pre/post handoff. Offline tests on a synthetic JSONL fixture.
- `run_step0.py`: one game (`sb26`), arm B, one seed, forced compaction every 30 turns, note cap, **token accounting per action** (input/output/cached) written to `runs/step0/cost.jsonl`. **It must ship with `--dry-run`** that validates config, paths, skill text, and the compaction trigger without any network or model call (Gotcha #276: a no-side-effect path is mandatory *before* the live path exists). `runs/` is gitignored; `runs/INDEX.md` is committed.
- `hexis/`: a pure function over a JSONL window that detects repeated action sequences with no frame change and returns a one-line disposition for arm C's Self-knowledge slot; offline tests.

### F — Paper implications (Yellow → write notes, not edits)
Write `Paper_Outline_Revision_Notes_2026-08-22.md` proposing the §2 / §5 / §6 changes from Experiment_Spec §7 (engage AVO, VISTA, arc-skill; narrowed novelty claim; new metrics; the "self as operator-editable file" line). Michal edits `Paper_Outline.md` himself.

## 3. Close (mandatory)
- Refresh `STATE.md` (telos / established / self-knowledge / plot / commitment; ≤ 1,500 tokens — use the Harness_Design §3.1 schema so this repo is its first live specimen).
- Append a `Session_Log.md` entry in `Claude_Protocols` (format: `## YYYY-MM-DD (cont. N) — [title] | [layers] | [repos]`), and a `Gotchas.md` entry for any corrected mistake.
- Commit on `ablation-setup`. **No push.**
- Final report to Michal: files created; sources acquired with hashes; what the toolkit permits anonymously vs. registered; the exact command that would run Step 0 live (not executed); open questions; and the unchanged decision list from `Experiment_Spec.md` §8.
