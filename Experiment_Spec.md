# Experiment Spec — Memory-Schema Ablation on ARC-AGI-3

**Version 0.1 — DRAFT, 2026-08-22** (Thinking-Layer design session; execution belongs to Claude Code). Status: proposed; Step 0 is the only approved action until Michal sets a budget ceiling (🔴). Companion documents: `Paper_Outline.md` (this repo), `Claude_Protocols/Harness_Design.md` §7 (why this experiment doubles as infrastructure R&D).

---

## 1. Why this experiment, and why now

`Paper_Outline.md` §5.4 names the paper's own weak points: custom coherence metrics, small scale, no external benchmark, and (until v2) rule-based interpretation. The v2 runs (`examples/compare_rule_vs_llm.py`, `examples/llm_identity_formation.py`) fixed the last one: emplotment is now done by Claude. What remains is that "memory efficiency" is measured as *fewer core memories*, with no task in which memory has consequences. A reviewer at *Minds and Machines* will not accept that as superiority. They will accept: **fewer note tokens, equal or better task performance across context handoffs, on a public benchmark with published human and frontier-model baselines.**

Three August 2026 results make that benchmark available and make the question urgent. NVIDIA's AVO and MIT's VISTA both reach 100 RHAE on the ARC-AGI-3 public set by wrapping Claude Opus 5 in a harness whose persistent memory carries understanding across levels and across context boundaries; VISTA's memory is a compact, revisable `GUIDE.md` plus a scratch `WORKING.md`, selected by *task relevance*. NVIDIA states that memory's individual contribution was not isolated. Our claim is that the selection principle should be *teleological*: what survives a context cut is what is constitutive of the agent's ongoing story, including what it has learned about itself. Nobody has run that ablation. It is small, cheap to design, and it falls directly out of the existing code.

One caveat to carry into the paper: public-set results only, and VISTA's authors note the models post-date the public games, so contamination cannot be excluded. We are not claiming a benchmark result. We are claiming a controlled comparison *between memory schemas* under identical conditions.

---

## 2. Design

**Environment.** ARC-AGI-3 public games via the ARC-AGI Toolkit (`pip install arc-agi`; local mode; JSONL recordings). Registered API key from three.arcprize.org.

**Base harness.** Fork `pbshgthm/arc-skill` (Claude Code skill, 129 lines of instruction + CLI). Its **prediction gate** (no press without a written prediction; prediction graded against the returned frame) stays **identical across all arms** — it is harness, not memory, and the repo's own numbers show it does heavy lifting (single test presses missed 37.1%, planned sequences 2.9%). The three arms differ only in the *handoff note* written at each compaction.

**Arms.**

| Arm | Handoff note at compaction | What it tests |
|---|---|---|
| A — Amnesiac | "Summarize the conversation so far." No notes files. | the cost of no designed continuity |
| B — Task-model (VISTA) | `GUIDE.md` (compact, revisable model of the game, durable across levels) + `WORKING.md` (current level scratch) | selection by task relevance |
| C — Narrative | one note to a five-part schema: **Telos** (what counts as success for me here) · **Established** (rules I would bet on) · **Self-knowledge** (my recurring errors in this game; corrections I owe myself) · **Plot** (what I tried, what failed, what changed my mind) · **Commitment** (next action + how I will know it worked) | selection by narrative identity; the hexis ledger as an *internalized supervisor* (AVO needed a second agent to notice stagnation; can a self-record do it?) |

**Controls.**
- Same model for every arm (a Sonnet- or Haiku-class model, *not* Opus at xhigh: with Opus already at 100 there is no headroom to show anything; on a smaller model the harness contribution is visible). Same settings, same prompt except the compaction instruction.
- **Forced compaction every 30 turns** regardless of context fill. This turns handoff frequency into a controlled variable and makes even short games exercise memory several times.
- **Equal note budget:** every arm's notes capped at ~1,200 tokens. Otherwise a reviewer will say arm C simply got more prompt.
- Two seeds per cell.

**Games** (chosen from VISTA's per-game table so each has a published Opus reference):

| Game | Levels | VISTA actions | Why |
|---|---|---|---|
| sb26 | 8 | 124 | cheap, many level boundaries → cross-level transfer |
| tu93 | 9 | 192 | same logic, harder |
| s5i5 | 8 | 251 | VISTA ran it in text / 2D / 3D → cleanest comparability |
| bp35 | 9 | 449 | VISTA stumbled at level 5 (1.70× human) → the recovery test |
| *lf52 (stretch)* | 10 | 881 | VISTA published its `GUIDE.md` rules for this game → compare note *content* across arms; expensive; only if the pilot shows signal |

Core four ≈ 1,000 actions at Opus efficiency; budget 1.5–2.5× that per arm-seed with a smaller model.

**Telos variation (sub-study).** Arm C only: same games, two teloi (EXPLORING vs PERFORMING). If trajectories diverge measurably from identical experiences, `examples/llm_identity_formation.py` becomes data rather than illustration.

---

## 3. Metrics (all from the toolkit's JSONL + the note snapshots)

1. Levels completed; actions per level vs. human baseline (RHAE, as ARC Prize computes it).
2. **Post-handoff burn**: actions in the first 20 turns after each compaction before the first state-changing press (the cost of discontinuity).
3. **Stagnation count**: repeated action sequences with no frame change.
4. **Prediction accuracy** per arm (the gate's own grade), split by pre- vs post-handoff.
5. **Note tokens** at each compaction (the memory-efficiency question, now with a task attached).
6. Qualitative: the note texts themselves, snapshotted at every compaction. For the paper these are primary data: what each schema chose to keep.

Primary hypothesis: C ≥ B on (1) with lower (2) and (3), at equal (5). Null result is publishable: it would show task-relevance selection suffices and narrative structure is ornament at this scale, which is itself a finding the paper must be able to survive.

---

## 4. Cost control — Step 0 before anything else

**Step 0 (approved in principle; ~1 hour of Michal's time):** one game (sb26), arm B, one seed. Purpose: measure tokens per action and per compaction with prompt caching on the skill text. Multiply by 24 cells → the pilot's price. **Budget ceiling is Michal's decision (🔴) and is set after this number exists, not before.**

If Step 0's number is acceptable: the pilot runs as a Claude Code routine / managed agent in the background during September–October; Michal reads results in November. Zero attention before then.

---

## 5. What the repo becomes (v3 layout, proposed)

```
narrative-agents/
├── harness/            three arm skills (SKILL.md each) forking arc-skill; shared prediction gate
├── compaction/         the three handoff prompts (A / B / C) + the note schema for C
├── hexis/              rule that scans the JSONL for repeated no-change sequences and
│                       appends a disposition line to C's Self-knowledge (the ledger update)
├── metrics/            per-level RHAE, post-handoff burn, stagnation, prediction accuracy, note tokens
├── runs/               JSONL recordings + note snapshots per cell (git-lfs or ignored; index committed)
├── narrative_agents/   v2 core stays: Telos enum, narrative_core/peripheral split, trait ledger
│                       → now the *schema* of arm C's note rather than a simulated mind
└── examples/           v2 scripts kept as the paper's §5.1–5.3 demonstrations
```

Honest reframing for the paper: v1 simulated a mind in Python; v2 let Claude do the emplotment on text experiences; v3 puts the same schema inside an embedded agent where memory has consequences. The data structures survive; the interpretation moved into the model; the Python became the compaction routine and the metrics.

---

## 6. The selection rule — **RULED 2026-08-22: budgeted competitive selection with a floor and an inaugural memory**

**Diagnosis (from the code, 2026-08-22).** `core.py` admits a memory to the core only if `relevance > 0.7`. In the LLM path `_assess_relevance` asks the fast model for one decimal in isolation, with a prompt that itself states "0.7+ = identity-forming (will become a core memory)". `_update_character` runs only on core memories and `_character_summary` feeds character back into the next relevance call, so an agent that never gets a first core memory never forms character and never gets one: a cold-start bistability. The v2 experience set (six of ten are errors/failures) favors the learning telos. Performer's and Explorer's 0/10 is therefore an artifact of an absolute threshold plus a biased set, not a finding.

**The rule (configurational: an event's significance is its place among the others, which is the Ricoeurian reading).**

```
parameters: budget B (core capacity: v2 = explicit int, default ceil(N/3); v3 = the note token cap),
            floor F (default 0.30), scorer S (rule-based or LLM)
for each experience e:
    r = S(e)                                  # raw relevance, always logged
    if r < F:            peripheral            # trivia never enters, even into an empty core
    elif core not full:  core (inaugural if core was empty → pinned as the story's beginning)
    elif r > min(core \ {inaugural}): displace the weakest non-inaugural member → peripheral (flag: displaced)
    else:                peripheral
character update fires on entry to core (as now); displaced memories keep their interpretation.
```

- **Inaugural memory is pinned.** A story needs a stable beginning (`tell_story` already reads `narrative_core[0]`). Re-choosing the beginning is re-emplotment, a larger event reserved for a later version.
- **Displaced ≠ forgotten.** Displaced memories move to `peripheral` with a flag; selective forgetting stays the paper's §6.3 claim, now with a visible mechanism.
- **Reporting.** "Memory efficiency" is reported as *selection under budget B*, alongside the **raw score distribution per telos** (so a reader can see calibration) and the core's composition by experience type. The old absolute rule stays available behind `selection="absolute"` to reproduce the v2 numbers.
- **Prompt change.** `RELEVANCE_SYSTEM_PROMPT` stops announcing the selection threshold; it asks for significance to *this* agent's ongoing story on the 0–1 scale with telos-relative anchors. v3 may move to a comparative prompt ("more identity-forming than the weakest current core memory?"), which is the form the rule actually needs; keep the numeric scorer for v2 comparability.
- **Balanced experience set** for any re-run whose numbers are reported: two experiences per type across error / failure / success / discovery / neutral.

Implementation: `PROMPT_Ablation_Setup_2026-08-22.md` Task D (flag-switched, offline tests including the cold-start case: an empty-core Performer must acquire an inaugural memory from a balanced set; and a displacement case). Re-running the LLM examples spends tokens and waits for Michal's go.

---

## 7. Paper implications (for `Paper_Outline.md`)

- §2 must now engage the 2026 harness literature: AVO (persistent memory + supervisor), VISTA (`GUIDE.md`/`WORKING.md`, compaction), arc-skill (prediction gate), alongside Generative Agents, Reflexion, MemGPT. The novelty claim narrows and sharpens: *not* "first to implement narrative identity as agent memory" in a vacuum, but "first controlled comparison of task-relevance vs. teleological selection under context compaction, with the self-record tested as an internalized supervisor."
- §5 gets an external benchmark and the metrics above; §5.4's limitations list shrinks.
- §6 gains its best line: in these systems the "self" that persists is a markdown file the operator can edit. That is a sharper objection to substrate-independence and mind-uploading than the techno-gnosticism paper could make from the outside.
- Venue note: *Minds and Machines* or *Philosophy & Technology* remain right for the philosophical claim; a short harness-track note (the ablation alone) could go to a venue that reads ARC-AGI-3 results. Decide after the pilot.

---

## 8. Open decisions (Michal)

1. Approve Step 0 (one game, one arm, one seed) — 🟡.
2. Budget ceiling after Step 0 — 🔴.
3. Model tier for the pilot (Sonnet-class recommended; Haiku-class if Step 0 prices high).
4. Whether the telos sub-study runs in the pilot or waits for signal.
5. Whether `runs/` recordings are committed (git-lfs) or kept local with an index.

*Sources verified 2026-08-22: VISTA project page (vista-research.github.io), NVIDIA AVO blog + arXiv 2603.24517, pbshgthm/arc-skill README, arcprize/arc-agi toolkit README, ARC Prize's arc-agi-3-benchmarking repo. Re-verify before citation.*
