# runs/ — recording index

Recordings are **committed** (ruled 2026-08-26, Spec §8.5) — except rendered
frame PNGs (`.gitignore`'s global `*.png`; re-render via `arc view`) and
local dry-run probes (`*.dryrun.jsonl`).

Layout per cell: `runs/<cell>/` where `<cell>` is `step0` or
`<game>-<arm>-<seed>` (e.g. `sb26-C-1`), holding the toolkit JSONL
recording(s) (`<scorecard>/<game>-<guid>.jsonl`), the harness annotation
stream, note snapshots at each compaction, and `cost.jsonl` (per-action token
accounting: turn, input/output/cache_read/cache_write tokens).

| Cell | Created | Status | Notes |
|---|---|---|---|
| step0 | 2026-08-26 | **executed** — 60 paid actions, 2 segments, 1 forced handoff | sb26 arm B on `claude-sonnet-5`; L1 complete, L2 parked unsolved at event 60 (replayable); 5,703 tokens/action blended, post-handoff burn 0, notes under cap ×2 — see `step0/COST_NOTES.md` and `step0/cost_segments.jsonl` |
| sb26-A-1 · sb26-A-2 | — | planned (Sept pilot, Spec §8.6) | arm A (amnesiac), seeds 1–2 |
| sb26-B-1 · sb26-B-2 | — | planned (Sept pilot, Spec §8.6) | arm B (task-model), seeds 1–2 |
| sb26-Cexp-1 · sb26-Cexp-2 | — | planned (Sept pilot, Spec §8.6) | arm C, telos EXPLORING, seeds 1–2 |
| sb26-Cperf-1 · sb26-Cperf-2 | — | planned (Sept pilot, Spec §8.6) | arm C, telos PERFORMING, seeds 1–2 |

Pilot protocol per cell: segmented Claude Code subagents (30-action segments,
arm-specific handoff per `compaction/`, cap ~250 paid actions), subscription
route — the $50 API ceiling stays in reserve (ruled 2026-08-26).
