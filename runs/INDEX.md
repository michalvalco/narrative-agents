# runs/ — recording index

Recordings are **not committed** (`.gitignore`: `runs/*` except this file).
This index is the committed record of what exists locally.

Layout per cell: `runs/<cell>/` where `<cell>` is `step0` or
`<game>-<arm>-<seed>` (e.g. `sb26-C-1`), holding the toolkit JSONL
recording(s) (`<scorecard>/<game>-<guid>.jsonl`), the harness annotation
stream, note snapshots at each compaction, and `cost.jsonl` (per-action token
accounting: turn, input/output/cache_read/cache_write tokens).

| Cell | Created | Status | Notes |
|---|---|---|---|
| step0 | 2026-08-26 | dry-run only | `cost.dryrun.jsonl` probe; live run pending Michal's go (Spec §8) |
