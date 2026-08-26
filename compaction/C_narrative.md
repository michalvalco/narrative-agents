# Arm C — Narrative handoff (five-part schema)

At each forced compaction (every 30 turns), rewrite **one** file, `NOTE.md`, to
exactly this schema (selection principle: **narrative identity** — what
survives a context cut is what is constitutive of your ongoing story here,
including what you have learned about yourself):

1. **Telos** — what counts as success *for me* in this game, right now
   (finishing? understanding? efficiency?). Two sentences.
2. **Established** — rules I would bet on, each citing the event id that
   verified it. No prose.
3. **Self-knowledge** — my recurring errors in this game and the corrections I
   owe myself. When the hexis rule (`hexis/detector.py`) reports a stagnation
   disposition line, it is appended here verbatim. Five lines, no more.
4. **Plot** — what I tried, what failed, what changed my mind since the last
   handoff; older moves collapse into section 2 once they harden into rules.
5. **Commitment** — the next concrete action and how I will know it worked
   (the prediction I will write for it).

The next context resumes from `NOTE.md` plus `arc status` output alone.

**Note budget:** `NOTE.md` is capped at ~1,200 tokens (counted by
`metrics/tokens.py::count_tokens`) — equal across all arms.
