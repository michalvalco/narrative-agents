# STATE — narrative-agents

> Harness_Design §3.1 schema (Telos / Established / Self-knowledge / Plot / Commitment); cap 1,500 tokens. This repo is the schema's first live specimen. **Last updated:** 2026-08-26 · Claude Code · Desktop.

## 1. Telos

Run the memory-schema ablation (`Experiment_Spec.md`): a controlled comparison of amnesiac vs. task-model vs. narrative handoff notes on ARC-AGI-3, feeding both the *Minds and Machines* paper (`Paper_Outline.md`) and the `STATE.md` schema decision in `Claude_Protocols/Harness_Design.md` §3. Done = pilot data on 4 games × 3 arms × 2 seeds, metrics computed, notes snapshotted.

## 2. Established

- Selection rule ruled 2026-08-22: budgeted competitive selection, floor 0.30, pinned inaugural, displacement → `Experiment_Spec.md` §6; implemented behind `selection=` in `narrative_agents/core.py`.
- Prediction gate is harness, not memory — identical across arms (`Experiment_Spec.md` §2).
- Note budget ≈ 1,200 tokens per arm; forced compaction every 30 turns.
- `arc-agi==0.9.9` (arc-skill's pin); `vendor/arc-skill` @ `dba53c3` read-only, gitignored.
- v2 LLM run artifact: Performer/Explorer 0/10 core = threshold artifact, not finding (run log lines 200–210).
- AVO's ARC-AGI-3 claims are **blog-only**; arXiv 2603.24517 has zero ARC content (Gotchas #307). VISTA has **no paper** — cite the site's `@misc` (`Sources/Source_Index.md`).
- `.env` never tracked; `_Archive/` untracked 2026-08-26 (blobs remain in pushed history).
- Only approved spend: none — Step 0 itself is 🟡 pending Michal; budget ceiling 🔴.

## 3. Self-knowledge

- Sessions here have asserted repo state from memory before — read first (Gotchas #279; recon file is the antidote).
- Side-effect "tests" are the local trap: running an example script spends tokens (Gotchas #276) — every runner must have a `--dry-run`/offline path first.
- Selection logic once lived only in prose and got re-broken (Gotchas #270) — thresholds and rules go in code with tests, prose keeps the why.
- Do not edit `Paper_Outline.md` — revision notes go in a separate file.

## 4. Plot

2025-10 v1 (rule-based mind in Python) → 2026-03 v2 (LLM emplotment; `llm_core.py`) → 2026-08-22 Thinking-Layer session ruled the design (spec, arms, selection rule) → 2026-08-25 hooks reference captured → **2026-08-26 this session:** hygiene (`_Archive` untracked, `.env.example` committed), `ablation-setup` branch, venv + `arc-agi==0.9.9` offline-verified, sources acquisition, Task D selection rule + tests, Task E harness skeleton written (not run).

## 5. Commitment

Next action: Michal decides `Experiment_Spec.md` §8 (Step 0 approval 🟡, then budget ceiling 🔴 after the cost number exists). Verifier: `run_step0.py --dry-run` passes offline; `pytest` green; Step 0 live run NOT executed until the go.
