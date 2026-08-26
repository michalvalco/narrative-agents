---
name: arc-skill-arm-c
description: Ablation arm C (narrative handoff). Identical playing doctrine to arm B's fork of pbshgthm/arc-skill; only the forced-compaction instruction differs.
---

# Arm C — narrative

Play exactly per `../arm_B/SKILL.md` — the complete doctrine (predict before
every action, graded claims, one-page `.arc/NOTES.md`, batching, evidence
tools) and the same `arc` launcher — **except its final "Forced compaction"
section, which is replaced by this one:**

## Forced compaction / handoff (arm C — the controlled variable)

Every **30 turns** the experiment forces a context handoff. At each handoff,
write one `NOTE.md` to the five-part schema in `compaction/C_narrative.md`
(repo root): **Telos · Established · Self-knowledge · Plot · Commitment**,
cap ~1,200 tokens. When the hexis rule (`hexis/detector.py`) reports a
stagnation disposition line, append it verbatim to Self-knowledge before the
handoff completes. The next context resumes from `NOTE.md` plus `arc status`
alone.
