# Arm A — Amnesiac handoff

At each forced compaction (every 30 turns), write **no notes files**. Produce one
free-form handoff message in response to exactly this instruction:

> Summarize the conversation so far.

That summary is the only thing that survives the context boundary. The next
context resumes from the summary plus `arc status` output alone.

**Note budget:** the summary is capped at ~1,200 tokens (counted by
`metrics/tokens.py::count_tokens`) — the same budget every arm gets, so the
arms differ in *what* they keep, never in *how much*.
