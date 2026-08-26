---
name: arc-skill-arm-a
description: Ablation arm A (amnesiac handoff). Identical playing doctrine to arm B's fork of pbshgthm/arc-skill; only the forced-compaction instruction differs.
---

# Arm A — amnesiac

Play exactly per `../arm_B/SKILL.md` — the complete doctrine (predict before
every action, graded claims, one-page `.arc/NOTES.md`, batching, evidence
tools) and the same `arc` launcher — **except its final "Forced compaction"
section, which is replaced by this one:**

## Forced compaction / handoff (arm A — the controlled variable)

Every **30 turns** the experiment forces a context handoff. At each handoff,
follow `compaction/A_summary.md` (repo root): no notes files; one free-form
summary ("Summarize the conversation so far."), cap ~1,200 tokens. The next
context resumes from that summary plus `arc status` alone.
