# Paper Outline — Revision Notes (2026-08-26)

**Proposals only.** `Paper_Outline.md` is Michal's document; nothing there was
edited. These notes carry Experiment_Spec.md §7 into outline-shaped changes,
corrected against the sources actually acquired on 2026-08-26 (see
`Sources/Source_Index.md`). Filename dated to the session that wrote it (the
setup prompt of 2026-08-22 anticipated same-day execution).

---

## §2 (State of the Art) — engage the 2026 harness literature

Add a **2.2b Harness-era memory (2026)** block between the current 2.2 and 2.3:

- **AVO (NVIDIA)** — main agent loop + persistent memory + supervisor agent.
  ⚠️ **Citation discipline**: arXiv 2603.24517 is the AVO *architecture* paper
  (GPU-kernel optimization) and contains **no ARC-AGI-3 content whatsoever**.
  Every ARC-AGI-3 claim — 100.00 RHAE, 6,624 actions, Claude Opus 5 backbone,
  "memory's individual contribution was not isolated" — exists **only in the
  NVIDIA developer blog post** (2026-08-21), which itself disclaims controlled
  ablation and is explicit that results are public-set only. Cite the paper
  for the architecture, the blog for the ARC result, and never let one stand
  in for the other. (`Sources/AVO_2026.md`, `Sources/AVO_NVIDIA_blog_2026-08.md`)
- **VISTA (MIT)** — compact revisable `GUIDE.md` + scratch `WORKING.md`,
  selection by task relevance; continuation across context boundaries.
  ⚠️ **No paper exists** (verified 2026-08-26): the citable object is the
  project site's own `@misc` BibTeX. Their contamination caveat (models
  post-date the public games) must appear wherever their numbers do.
  (`Sources/VISTA_2026.md` — per-game table machine-verified)
- **arc-skill (pbshgthm)** — the prediction gate as harness discipline: no
  press without a written prediction, graded against the returned frame;
  single test presses missed 37.1% vs 2.9% for planned sequences
  (README.md:114–117 of the pinned clone). This is the *held-constant* term
  in our design, which is what makes the memory comparison clean.
- Keep Generative Agents, Reflexion, MemGPT in 2.1–2.2 as the pre-harness
  generation; the 2026 systems differ in that memory now has *task
  consequences across context cuts*, which is exactly the condition §5's v2
  experiments lacked.

**2.3 (the gap) — narrow and sharpen the novelty claim** per Spec §7: not
"first to implement narrative identity as agent memory" but **"first
controlled comparison of task-relevance vs. teleological selection under
context compaction, with the self-record tested as an internalized
supervisor"** (AVO needed a second agent to notice stagnation; arm C asks
whether a self-record suffices — the hexis ledger, now implemented in
`hexis/detector.py`).

## §4 (Architecture) — the selection rule changed under us

- 4.1's "relevance > 0.7" line describes the v2 rule only. As of 2026-08-22
  the architecture is **budgeted competitive selection with a floor and a
  pinned inaugural memory** (`core.py`, `selection="budgeted"`), with the
  absolute rule kept behind `selection="absolute"` for v2 reproducibility.
  The configurational reading (an event's significance is its place among
  the others) is *more* Ricoeurian than the absolute threshold was — worth a
  sentence in §3.1 tying emplotment to competitive selection.
- 4.3 should report the cold-start bistability the absolute rule created
  (character forms only from core entries; relevance reads character; an
  empty core never seeds) — it is an honest and instructive design lesson.

## §5 (Experimental Results) — external benchmark, new metrics

- Reframe per Spec §5: v1 simulated a mind in Python; v2 let Claude do the
  emplotment; **v3 puts the same schema inside an embedded agent where memory
  has consequences** (ARC-AGI-3, three arms, identical prediction-gate
  harness, forced compaction every 30 turns, equal ~1,200-token note budget).
- 5.1's Performer/Explorer **0/10 core-memory result is an artifact** of the
  absolute threshold plus an error-heavy experience set (Spec §6); any
  reported re-run uses the balanced fixture (`narrative_agents/fixtures.py`)
  and reports selection-under-budget with the raw score distribution.
- New metrics section (implemented, offline-tested, in `metrics/`):
  per-level actions vs. human baseline (VISTA table), **post-handoff burn**,
  **stagnation count**, prediction accuracy split pre/post handoff, note
  tokens per compaction. Note-token counts use an offline chars/4
  approximation until Step 0's `cost.jsonl` calibrates it — say so.
- 5.4 limitations shrink (external benchmark: yes; LLM interpretation: yes)
  but gain: public-set-only comparability, VISTA's contamination caveat
  inherited, two seeds per cell, and the null-result commitment (if B ≥ C,
  task-relevance selection suffices at this scale — the paper survives it).

## §6 (Discussion) — the sharpest new line

- **"In these systems the 'self' that persists across context death is a
  markdown file the operator can edit."** VISTA's GUIDE.md and our arm-C
  NOTE.md are literal, inspectable, editable identity documents. That is a
  sharper objection to substrate-independence and mind-uploading than the
  techno-gnosticism paper could mount from outside: the experiment *builds*
  the uploadable self and shows what it is — a text under a token budget,
  selected by someone's principle. Fits 6.1 as its empirical anchor.
- 6.3 (selective forgetting) gains a visible mechanism: displacement with a
  flag (`displaced` memories keep their interpretation) — forgetting as
  demotion, not deletion.

## Venue note (unchanged from Spec §7)

*Minds and Machines* or *Philosophy & Technology* for the philosophical
claim; a short harness-track note (the ablation alone) possible for an
ARC-adjacent venue. Decide after the pilot.

## Verification status

All numeric claims above trace to `Sources/` documents with EXPLICIT labels;
the AVO scope split and the VISTA no-paper finding are the two corrections a
draft written from memory would have gotten wrong. `[GAP: none]`.
