# Arm B — Task-model handoff (VISTA schema)

At each forced compaction (every 30 turns), rewrite two files in the run
directory (selection principle: **task relevance**):

1. **`GUIDE.md`** — a compact, revisable model of the game, durable across
   levels: the rules you would bet on, controls and their verified effects,
   level-independent mechanics, known traps. Revise freely; never append-only.
2. **`WORKING.md`** — current-level scratch: where you are, the immediate plan,
   the hypothesis under test. Disposable — start it fresh at each level.

The next context resumes from these two files plus `arc status` output alone.

**Note budget:** GUIDE.md + WORKING.md combined are capped at ~1,200 tokens
(counted by `metrics/tokens.py::count_tokens`) — equal across all arms.
