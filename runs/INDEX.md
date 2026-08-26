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
