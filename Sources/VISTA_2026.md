# VISTA (MIT, 2026) — Source Documentation

**Status: ACQUIRED** (primary source fetched in full; raw HTML archived)
**Access date:** 2026-08-26
**URL:** https://vista-research.github.io/
**Fetch method:** direct HTTP GET (curl, HTTP 200, 396,427 bytes) plus WebFetch verification pass. Raw page archived at `Sources/_raw/vista-research.github.io_index_2026-08-26.html` — SHA-256 `220ed4c18eee568a0c6747e137c2896f56411c1084fca22909de0598846f1ec6`. All tables in §8–§9 below were extracted programmatically from that archived HTML/markdown conversion, not retyped by hand.

**Labeling convention:** **EXPLICIT** = verbatim from the page (quoted; numbers copied exactly). **STRONG INFERENCE** = follows from explicit statements with near-certainty (basis stated). **SPECULATIVE** = plausible but unconfirmed.

---

## 1. Citation

> Han, Qiushi; Hu, Keya; Qiu, Linlu; Wu, Cathy; He, Kaiming. "VISTA: A Visual Harness for Reasoning in an Interactive World." Massachusetts Institute of Technology, August 5, 2026. https://vista-research.github.io/. Accessed August 26, 2026.

Authorship as listed on the page (EXPLICIT): "Qiushi Han\* Keya Hu\* Linlu Qiu\* Cathy Wu Kaiming He — Massachusetts Institute of Technology — \* co-leads". Date shown on page: "Aug 5, 2026".

BibTeX published on the page (EXPLICIT, verbatim):

```bibtex
@misc{vista2026,
  title  = {{VISTA}: A Visual Harness for Reasoning in an Interactive World},
  author = {Han, Qiushi and Hu, Keya and Qiu, Linlu and Wu, Cathy and He, Kaiming},
  year   = {2026},
  month  = {aug},
  day    = {5},
  url    = {https://vista-research.github.io/}
}
```

The site's own citation is a `@misc` entry pointing at the website itself; the page publishes no paper/preprint reference (see §12).

---

## 2. Headline claims

EXPLICIT (page subtitle): "VISTA completes all 25 public ARC-AGI-3 games with a perfect score."

EXPLICIT (abstract paragraph): "Using Claude Opus 5.0 as the base model, VISTA completes all 25 public games, with a **100% win rate** and a perfect **100** Relative Human Action Efficiency (RHAE) score. It is also efficient, using **56.0%** fewer actions than first-time human players, and robust to different sensory inputs."

EXPLICIT (results section): "With Opus 5.0, VISTA completes all 183 levels across all 25 games. Its mean game score is **100.00**, with **25 perfect game scores**, using 7,542 game actions (**56%** fewer than humans). With GPT-5.6 Sol, VISTA also completes all 183 levels across the 25 public games. Its mean game score is 98.27, with 22 perfect game scores. The remaining 1.73 points are concentrated in a small number of levels where the model spends extra actions discovering a mechanism or recovering from an incorrect game model."

EXPLICIT (backends): "We instantiate VISTA with two general-purpose multimodal model backends: Opus 5.0 through the Claude Code CLI and GPT-5.6 Sol through the Codex CLI." Dashboard header values (EXPLICIT): Claude Opus 5.0 — Effort "xhigh", Mean score 100.00, Games completed 25 / 25, Perfect games 25 / 25, Actions agent/human **7,542** / 17,135. GPT-5.6 Sol — Effort "max", Mean score 98.27, Games completed 25 / 25, Perfect games 22 / 25, Actions agent/human **10,063** / 17,135.

EXPLICIT (visual input): "In our experiments, the agent receives a 512 by 512 PNG image of the current rendered state, a nearest-neighbor upscaling (8x) of the official 64 by 64 frame with one-pixel grid lines between cells. We note that the agent is never told that the world is a 64 by 64 grid; the 512 by 512 PNG images are all it receives. It can also request an enlarged view of any rectangular region of the board, and thus, in principle, has intact information access."

---

## 3. The agent prompt (published in full)

EXPLICIT — the page presents this as "The agent prompt", reproduced verbatim and complete:

```
# Visual game task

Complete the game with as few game actions as possible.

Build and use a compact, revisable model of the game and its current state. Update it as new evidence changes what is supported.

Before each `play`, briefly state what you expect to see. Afterward, briefly state all visible changes, expected or not.

Keep concise, durable, revisable game understanding in `GUIDE.md`; use `WORKING.md` as a scratchpad when useful.
```

EXPLICIT (design rationale for the prompt wording): "We ask the agent to write notes that build and use a compact, revisable model of the game and its current state (see prompt below). The word `compact` encourages the model to organize its observations into higher-level abstractions, in the spirit of Occam’s razor; the word `revisable` allows for updates and corrections as new evidence becomes available."

---

## 4. The three tools

The page names exactly three game-facing tools — `play`, `inspect`, `read_pixels` — in prose and in its pipeline figure. It publishes **no formal tool schema** (no parameter table or API signature). STRONG INFERENCE (basis: the pipeline figure lists only "play executes one action", "inspect · read_pixels" on visual memory, and "read · update" on the notes files; no other tool is named anywhere on the page): these three tools plus reading/updating the two notes files constitute the agent's full interface.

- **`play`** — EXPLICIT: "On each turn it observes, reasons, and executes one game action." Pipeline figure caption: "play executes one action". EXPLICIT: "Before calling `play`, the prompt asks it to state the visual result it expects."
- **`inspect`** — EXPLICIT: "The agent can then use an `inspect` tool to select earlier states, intermediate animation frames, or spatial regions and view them again through the same visual input. Several views can be requested together for read-only comparison."
- **`read_pixels`** — EXPLICIT: "For small discrete details, `read_pixels` returns exact color samples from a selected region."

EXPLICIT (optionality): "Looking back is available but optional. The model may act on the current frame alone, or call `inspect` to bring an earlier state, an intermediate animation frame, or an enlarged region back into view, and `read_pixels` to look at details. Which past moment to re-examine, and whether to re-examine anything at all, is the model’s decision rather than a fixed step in the loop."

EXPLICIT (scoring interaction): "Only environment actions enter this count; internal reasoning and read-only inspection are free under the scoring protocol."

---

## 5. GUIDE.md and WORKING.md

EXPLICIT: "The notes externalize the agent’s understanding of the world. `GUIDE.md` holds what may remain useful across levels, while `WORKING.md` is a scratchpad for the current level. Together they give us a readable view of the abstractions the agent uses when exploring the world."

EXPLICIT (memory section): "We also allow the model to take notes in a minimal file, `GUIDE.md`, that describes the core idea of the game. This gives it an additional way to keep information, but in a high-level and abstract form."

EXPLICIT — sample of actual GUIDE.md content the agent wrote for the LF52 game ("Three of the core jumping rules the agent wrote in `GUIDE.md` for this game"):

> - Green pegs make standard orthogonal jumps on 48 px-spaced gray holes: click source, then an empty landing two cells away. A jumped standard green is removed.
> - Purple/pink pedestal pieces are fixed persistent jump posts. Any movable piece can jump across one; the post remains.
> - Red cross pieces are movable persistent jumpers/posts. Red and green can jump over each other without removing either, so alternating jumps moves a persistent pair along a line.

EXPLICIT (size contrast, same LF52 rule set): program-based world model (Schema team's release) is "Roughly **4,000** lines of Python for this game"; VISTA's language notes are "A page of notes."

---

## 6. Compaction / continuation across context boundaries

EXPLICIT — the complete pipeline paragraph, verbatim:

> "One agent plays each game from its first observation to completion. It begins with only the current visual state and available actions: no instructions, stated rules, or goal. On each turn it observes, reasons, and executes one game action. The same agent can revisit visual memory or maintain two notes whenever useful. When the model approaches its context limit, it writes a concise continuation state, then resumes from the current visual state in a fresh context. Its notes, visual memory, and action history remain available. Every game uses the same interface and short prompt."

STRONG INFERENCE (basis: notes are external files and the paragraph states notes "remain available" after the fresh context begins): `GUIDE.md` and `WORKING.md` survive context boundaries because they live outside the context window as files, and the fresh context re-reads them; the page does not further specify the mechanism (e.g., whether the continuation state is written into the notes files or into a separate handoff message — unspecified on the page).

EXPLICIT (memory-mechanism comparison table, "Written text notes" row): kept — "The model’s own description of what happened"; lost — "Everything not written down. The model chooses what to drop."; comes back by "Re-reading its own text." EXPLICIT ("Lossless visual memory" row): kept — "Every returned frame at full resolution, indexed by turn and frame."; lost — "Nothing."; comes back via "`inspect` and `read_pixels`, on the model’s own decision."

---

## 7. Scoring metric as stated

EXPLICIT: "ARC-AGI-3 uses Relative Human Action Efficiency (RHAE): completed levels are scored by the squared ratio between a first-time human action baseline and the agent’s actions, later levels receive greater weight, and the final score is averaged across games. Only environment actions enter this count; internal reasoning and read-only inspection are free under the scoring protocol. See the official scoring methodology for the complete definition." (links to https://docs.arcprize.org/methodology)

STRONG INFERENCE (basis: arithmetic verified on multiple level rows in §8, e.g. tu93 L1: agent 18, human 19, (19/18)² × 100 = 111.42 = listed score; sb26 L8: (18/17)² × 100 = 112.11 = listed score; bp35 L2: (48/50)² × 100 = 92.16 = listed score): per-level score = 100 × (human actions / agent actions)², capped at 115.00 — no level score above 115.00 appears anywhere in either table.

---

## 8. Per-game results tables (VERBATIM data)

Transcription note: on the live page each game row embeds an interactive cumulative-progress chart; the chart's per-level cumulative action counts are redundant with (derivable from) the per-level breakdowns reproduced in full below. Every number below is machine-extracted from the archived page; thousands separators (e.g. 1,107) are presentational only and match the page's chart labels. The "Ratio" column is the page's "Cumulative progress … × human" figure; "Actions" is agent/human; Status is the page's status cell. For byte-level verification, consult the archived HTML in `Sources/_raw/`.

### 8.1 Claude Opus 5.0 (Claude Code CLI, effort xhigh) — 25-game table

| Game | Score | Actions (agent / human) | Cumulative ratio | Levels | Status |
| --- | --- | --- | --- | --- | --- |
| ar25 | 100.00 | 270 / 748 | 0.36× human | 8 / 8 | WIN |
| bp35 | 100.00 | 449 / 651 | 0.69× human | 9 / 9 | WIN |
| cd82 | 100.00 | 92 / 171 | 0.54× human | 6 / 6 | WIN |
| cn04 | 100.00 | 235 / 789 | 0.30× human | 6 / 6 | WIN |
| dc22 | 100.00 | 635 / 1,228 | 0.52× human | 6 / 6 | WIN |
| ft09 | 100.00 | 80 / 208 | 0.38× human | 6 / 6 | WIN |
| g50t | 100.00 | 321 / 879 | 0.37× human | 7 / 7 | WIN |
| ka59 | 100.00 | 302 / 730 | 0.41× human | 7 / 7 | WIN |
| lf52 | 100.00 | 881 / 1,339 | 0.66× human | 10 / 10 | WIN |
| lp85 | 100.00 | 111 / 388 | 0.29× human | 8 / 8 | WIN |
| ls20 | 100.00 | 517 / 776 | 0.67× human | 7 / 7 | WIN |
| m0r0 | 100.00 | 256 / 1,107 | 0.23× human | 6 / 6 | WIN |
| r11l | 100.00 | 68 / 233 | 0.29× human | 6 / 6 | WIN |
| re86 | 100.00 | 593 / 1,255 | 0.47× human | 8 / 8 | WIN |
| s5i5 | 100.00 | 251 / 638 | 0.39× human | 8 / 8 | WIN |
| sb26 | 100.00 | 124 / 213 | 0.58× human | 8 / 8 | WIN |
| sc25 | 100.00 | 176 / 350 | 0.50× human | 6 / 6 | WIN |
| sk48 | 100.00 | 525 / 1,070 | 0.49× human | 8 / 8 | WIN |
| sp80 | 100.00 | 121 / 518 | 0.23× human | 6 / 6 | WIN |
| su15 | 100.00 | 90 / 361 | 0.25× human | 9 / 9 | WIN |
| tn36 | 100.00 | 156 / 317 | 0.49× human | 7 / 7 | WIN |
| tr87 | 100.00 | 204 / 414 | 0.49× human | 6 / 6 | WIN |
| tu93 | 100.00 | 192 / 462 | 0.42× human | 9 / 9 | WIN |
| vc33 | 100.00 | 180 / 447 | 0.40× human | 7 / 7 | WIN |
| wa30 | 100.00 | 713 / 1,843 | 0.39× human | 9 / 9 | WIN |

#### Per-level breakdowns — Claude Opus 5.0

**ar25** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 16 | 32 | 0.50× | 115.00 |
| 2 | 17 | 50 | 0.34× | 115.00 |
| 3 | 41 | 75 | 0.55× | 115.00 |
| 4 | 23 | 37 | 0.62× | 115.00 |
| 5 | 29 | 89 | 0.33× | 115.00 |
| 6 | 58 | 159 | 0.36× | 115.00 |
| 7 | 38 | 233 | 0.16× | 115.00 |
| 8 | 48 | 73 | 0.66× | 115.00 |

**bp35** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 16 | 21 | 0.76× | 115.00 |
| 2 | 50 | 48 | 1.04× | 92.16 |
| 3 | 34 | 44 | 0.77× | 115.00 |
| 4 | 21 | 38 | 0.55× | 115.00 |
| 5 | 56 | 33 | 1.70× | 34.73 |
| 6 | 43 | 87 | 0.49× | 115.00 |
| 7 | 54 | 86 | 0.63× | 115.00 |
| 8 | 63 | 131 | 0.48× | 115.00 |
| 9 | 112 | 163 | 0.69× | 115.00 |

**cd82** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 23 | 55 | 0.42× | 115.00 |
| 2 | 6 | 8 | 0.75× | 115.00 |
| 3 | 16 | 41 | 0.39× | 115.00 |
| 4 | 14 | 21 | 0.67× | 115.00 |
| 5 | 13 | 23 | 0.57× | 115.00 |
| 6 | 20 | 23 | 0.87× | 115.00 |

**cn04** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 15 | 29 | 0.52× | 115.00 |
| 2 | 33 | 54 | 0.61× | 115.00 |
| 3 | 23 | 85 | 0.27× | 115.00 |
| 4 | 30 | 300 | 0.10× | 115.00 |
| 5 | 93 | 208 | 0.45× | 115.00 |
| 6 | 41 | 113 | 0.36× | 115.00 |

**dc22** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 31 | 59 | 0.53× | 115.00 |
| 2 | 43 | 102 | 0.42× | 115.00 |
| 3 | 45 | 67 | 0.67× | 115.00 |
| 4 | 62 | 98 | 0.63× | 115.00 |
| 5 | 178 | 324 | 0.55× | 115.00 |
| 6 | 276 | 578 | 0.48× | 115.00 |

**ft09** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 4 | 43 | 0.09× | 115.00 |
| 2 | 7 | 12 | 0.58× | 115.00 |
| 3 | 14 | 23 | 0.61× | 115.00 |
| 4 | 21 | 28 | 0.75× | 115.00 |
| 5 | 21 | 65 | 0.32× | 115.00 |
| 6 | 13 | 37 | 0.35× | 115.00 |

**g50t** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 39 | 78 | 0.50× | 115.00 |
| 2 | 31 | 175 | 0.18× | 115.00 |
| 3 | 68 | 179 | 0.38× | 115.00 |
| 4 | 31 | 230 | 0.13× | 115.00 |
| 5 | 50 | 96 | 0.52× | 115.00 |
| 6 | 59 | 54 | 1.09× | 83.77 |
| 7 | 43 | 67 | 0.64× | 115.00 |

**ka59** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 13 | 28 | 0.46× | 115.00 |
| 2 | 34 | 109 | 0.31× | 115.00 |
| 3 | 33 | 51 | 0.65× | 115.00 |
| 4 | 38 | 51 | 0.75× | 115.00 |
| 5 | 20 | 33 | 0.61× | 115.00 |
| 6 | 52 | 132 | 0.39× | 115.00 |
| 7 | 112 | 326 | 0.34× | 115.00 |

**lf52** (10 / 10 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 10 | 32 | 0.31× | 115.00 |
| 2 | 50 | 81 | 0.62× | 115.00 |
| 3 | 53 | 60 | 0.88× | 115.00 |
| 4 | 50 | 71 | 0.70× | 115.00 |
| 5 | 102 | 205 | 0.50× | 115.00 |
| 6 | 199 | 148 | 1.34× | 55.31 |
| 7 | 185 | 244 | 0.76× | 115.00 |
| 8 | 70 | 109 | 0.64× | 115.00 |
| 9 | 109 | 164 | 0.66× | 115.00 |
| 10 | 53 | 225 | 0.24× | 115.00 |

**lp85** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 9 | 17 | 0.53× | 115.00 |
| 2 | 13 | 38 | 0.34× | 115.00 |
| 3 | 16 | 31 | 0.52× | 115.00 |
| 4 | 13 | 16 | 0.81× | 115.00 |
| 5 | 11 | 41 | 0.27× | 115.00 |
| 6 | 20 | 60 | 0.33× | 115.00 |
| 7 | 7 | 26 | 0.27× | 115.00 |
| 8 | 22 | 159 | 0.14× | 115.00 |

**ls20** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 22 | 22 | 1.00× | 100.00 |
| 2 | 79 | 123 | 0.64× | 115.00 |
| 3 | 49 | 73 | 0.67× | 115.00 |
| 4 | 65 | 84 | 0.77× | 115.00 |
| 5 | 72 | 96 | 0.75× | 115.00 |
| 6 | 114 | 192 | 0.59× | 115.00 |
| 7 | 116 | 186 | 0.62× | 115.00 |

**m0r0** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 18 | 30 | 0.60× | 115.00 |
| 2 | 23 | 111 | 0.21× | 115.00 |
| 3 | 67 | 203 | 0.33× | 115.00 |
| 4 | 15 | 26 | 0.58× | 115.00 |
| 5 | 54 | 500 | 0.11× | 115.00 |
| 6 | 79 | 237 | 0.33× | 115.00 |

**r11l** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 3 | 22 | 0.14× | 115.00 |
| 2 | 10 | 33 | 0.30× | 115.00 |
| 3 | 11 | 51 | 0.22× | 115.00 |
| 4 | 13 | 26 | 0.50× | 115.00 |
| 5 | 15 | 52 | 0.29× | 115.00 |
| 6 | 16 | 49 | 0.33× | 115.00 |

**re86** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 21 | 26 | 0.81× | 115.00 |
| 2 | 38 | 42 | 0.90× | 115.00 |
| 3 | 47 | 86 | 0.55× | 115.00 |
| 4 | 55 | 108 | 0.51× | 115.00 |
| 5 | 63 | 189 | 0.33× | 115.00 |
| 6 | 61 | 139 | 0.44× | 115.00 |
| 7 | 107 | 424 | 0.25× | 115.00 |
| 8 | 201 | 241 | 0.83× | 115.00 |

**s5i5** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 13 | 20 | 0.65× | 115.00 |
| 2 | 26 | 89 | 0.29× | 115.00 |
| 3 | 38 | 106 | 0.36× | 115.00 |
| 4 | 35 | 54 | 0.65× | 115.00 |
| 5 | 28 | 162 | 0.17× | 115.00 |
| 6 | 27 | 38 | 0.71× | 115.00 |
| 7 | 46 | 86 | 0.53× | 115.00 |
| 8 | 38 | 83 | 0.46× | 115.00 |

**sb26** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 9 | 18 | 0.50× | 115.00 |
| 2 | 15 | 28 | 0.54× | 115.00 |
| 3 | 15 | 18 | 0.83× | 115.00 |
| 4 | 15 | 19 | 0.79× | 115.00 |
| 5 | 17 | 31 | 0.55× | 115.00 |
| 6 | 19 | 23 | 0.83× | 115.00 |
| 7 | 17 | 58 | 0.29× | 115.00 |
| 8 | 17 | 18 | 0.94× | 112.11 |

**sc25** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 19 | 36 | 0.53× | 115.00 |
| 2 | 6 | 6 | 1.00× | 100.00 |
| 3 | 33 | 32 | 1.03× | 94.03 |
| 4 | 22 | 83 | 0.27× | 115.00 |
| 5 | 61 | 143 | 0.43× | 115.00 |
| 6 | 35 | 50 | 0.70× | 115.00 |

**sk48** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 15 | 61 | 0.25× | 115.00 |
| 2 | 30 | 177 | 0.17× | 115.00 |
| 3 | 46 | 101 | 0.46× | 115.00 |
| 4 | 59 | 103 | 0.57× | 115.00 |
| 5 | 103 | 230 | 0.45× | 115.00 |
| 6 | 62 | 181 | 0.34× | 115.00 |
| 7 | 79 | 125 | 0.63× | 115.00 |
| 8 | 131 | 92 | 1.42× | 49.32 |

**sp80** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 7 | 39 | 0.18× | 115.00 |
| 2 | 8 | 58 | 0.14× | 115.00 |
| 3 | 10 | 25 | 0.40× | 115.00 |
| 4 | 28 | 148 | 0.19× | 115.00 |
| 5 | 32 | 96 | 0.33× | 115.00 |
| 6 | 36 | 152 | 0.24× | 115.00 |

**su15** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 10 | 22 | 0.45× | 115.00 |
| 2 | 10 | 42 | 0.24× | 115.00 |
| 3 | 13 | 26 | 0.50× | 115.00 |
| 4 | 9 | 115 | 0.08× | 115.00 |
| 5 | 6 | 36 | 0.17× | 115.00 |
| 6 | 15 | 31 | 0.48× | 115.00 |
| 7 | 5 | 8 | 0.63× | 115.00 |
| 8 | 8 | 40 | 0.20× | 115.00 |
| 9 | 14 | 41 | 0.34× | 115.00 |

**tn36** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 16 | 32 | 0.50× | 115.00 |
| 2 | 21 | 72 | 0.29× | 115.00 |
| 3 | 12 | 26 | 0.46× | 115.00 |
| 4 | 15 | 40 | 0.38× | 115.00 |
| 5 | 20 | 30 | 0.67× | 115.00 |
| 6 | 27 | 55 | 0.49× | 115.00 |
| 7 | 45 | 62 | 0.73× | 115.00 |

**tr87** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 68 | 54 | 1.26× | 63.06 |
| 2 | 29 | 58 | 0.50× | 115.00 |
| 3 | 26 | 40 | 0.65× | 115.00 |
| 4 | 21 | 45 | 0.47× | 115.00 |
| 5 | 23 | 71 | 0.32× | 115.00 |
| 6 | 37 | 146 | 0.25× | 115.00 |

**tu93** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 18 | 19 | 0.95× | 111.42 |
| 2 | 15 | 16 | 0.94× | 113.78 |
| 3 | 19 | 34 | 0.56× | 115.00 |
| 4 | 17 | 42 | 0.40× | 115.00 |
| 5 | 29 | 123 | 0.24× | 115.00 |
| 6 | 30 | 80 | 0.38× | 115.00 |
| 7 | 14 | 14 | 1.00× | 100.00 |
| 8 | 21 | 23 | 0.91× | 115.00 |
| 9 | 29 | 111 | 0.26× | 115.00 |

**vc33** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 8 | 7 | 1.14× | 76.56 |
| 2 | 8 | 18 | 0.44× | 115.00 |
| 3 | 23 | 44 | 0.52× | 115.00 |
| 4 | 21 | 61 | 0.34× | 115.00 |
| 5 | 49 | 131 | 0.37× | 115.00 |
| 6 | 22 | 34 | 0.65× | 115.00 |
| 7 | 49 | 152 | 0.32× | 115.00 |

**wa30** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 39 | 71 | 0.55× | 115.00 |
| 2 | 60 | 119 | 0.50× | 115.00 |
| 3 | 80 | 183 | 0.44× | 115.00 |
| 4 | 149 | 98 | 1.52× | 43.26 |
| 5 | 121 | 368 | 0.33× | 115.00 |
| 6 | 55 | 68 | 0.81× | 115.00 |
| 7 | 38 | 79 | 0.48× | 115.00 |
| 8 | 109 | 442 | 0.25× | 115.00 |
| 9 | 62 | 415 | 0.15× | 115.00 |

### 8.2 GPT-5.6 Sol (Codex CLI, effort max) — 25-game table

| Game | Score | Actions (agent / human) | Cumulative ratio | Levels | Status |
| --- | --- | --- | --- | --- | --- |
| ar25 | 100.00 | 327 / 748 | 0.44× human | 8 / 8 | WIN |
| bp35 | 85.25 | 638 / 651 | 0.98× human | 9 / 9 | WIN |
| cd82 | 100.00 | 84 / 171 | 0.49× human | 6 / 6 | WIN |
| cn04 | 100.00 | 264 / 789 | 0.33× human | 6 / 6 | WIN |
| dc22 | 100.00 | 805 / 1,228 | 0.66× human | 6 / 6 | WIN |
| ft09 | 100.00 | 75 / 208 | 0.36× human | 6 / 6 | WIN |
| g50t | 100.00 | 376 / 879 | 0.43× human | 7 / 7 | WIN |
| ka59 | 100.00 | 395 / 730 | 0.54× human | 7 / 7 | WIN |
| lf52 | 100.00 | 982 / 1,339 | 0.73× human | 10 / 10 | WIN |
| lp85 | 100.00 | 102 / 388 | 0.26× human | 8 / 8 | WIN |
| ls20 | 93.59 | 696 / 776 | 0.90× human | 7 / 7 | WIN |
| m0r0 | 100.00 | 264 / 1,107 | 0.24× human | 6 / 6 | WIN |
| r11l | 100.00 | 128 / 233 | 0.55× human | 6 / 6 | WIN |
| re86 | 100.00 | 684 / 1,255 | 0.55× human | 8 / 8 | WIN |
| s5i5 | 100.00 | 304 / 638 | 0.48× human | 8 / 8 | WIN |
| sb26 | 100.00 | 131 / 213 | 0.62× human | 8 / 8 | WIN |
| sc25 | 77.88 | 346 / 350 | 0.99× human | 6 / 6 | WIN |
| sk48 | 100.00 | 949 / 1,070 | 0.89× human | 8 / 8 | WIN |
| sp80 | 100.00 | 239 / 518 | 0.46× human | 6 / 6 | WIN |
| su15 | 100.00 | 129 / 361 | 0.36× human | 9 / 9 | WIN |
| tn36 | 100.00 | 191 / 317 | 0.60× human | 7 / 7 | WIN |
| tr87 | 100.00 | 180 / 414 | 0.43× human | 6 / 6 | WIN |
| tu93 | 100.00 | 238 / 462 | 0.52× human | 9 / 9 | WIN |
| vc33 | 100.00 | 300 / 447 | 0.67× human | 7 / 7 | WIN |
| wa30 | 100.00 | 1,236 / 1,843 | 0.67× human | 9 / 9 | WIN |

#### Per-level breakdowns — GPT-5.6 Sol

**ar25** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 84 | 32 | 2.63× | 14.51 |
| 2 | 15 | 50 | 0.30× | 115.00 |
| 3 | 40 | 75 | 0.53× | 115.00 |
| 4 | 22 | 37 | 0.59× | 115.00 |
| 5 | 29 | 89 | 0.33× | 115.00 |
| 6 | 53 | 159 | 0.33× | 115.00 |
| 7 | 37 | 233 | 0.16× | 115.00 |
| 8 | 47 | 73 | 0.64× | 115.00 |

**bp35** (9 / 9 levels, score 85.25)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 35 | 21 | 1.67× | 36.00 |
| 2 | 68 | 48 | 1.42× | 49.83 |
| 3 | 36 | 44 | 0.82× | 115.00 |
| 4 | 40 | 38 | 1.05× | 90.25 |
| 5 | 95 | 33 | 2.88× | 12.07 |
| 6 | 124 | 87 | 1.43× | 49.23 |
| 7 | 87 | 86 | 1.01× | 97.71 |
| 8 | 72 | 131 | 0.55× | 115.00 |
| 9 | 81 | 163 | 0.50× | 115.00 |

**cd82** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 13 | 55 | 0.24× | 115.00 |
| 2 | 6 | 8 | 0.75× | 115.00 |
| 3 | 19 | 41 | 0.46× | 115.00 |
| 4 | 14 | 21 | 0.67× | 115.00 |
| 5 | 16 | 23 | 0.70× | 115.00 |
| 6 | 16 | 23 | 0.70× | 115.00 |

**cn04** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 14 | 29 | 0.48× | 115.00 |
| 2 | 53 | 54 | 0.98× | 103.81 |
| 3 | 31 | 85 | 0.36× | 115.00 |
| 4 | 32 | 300 | 0.11× | 115.00 |
| 5 | 91 | 208 | 0.44× | 115.00 |
| 6 | 43 | 113 | 0.38× | 115.00 |

**dc22** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 22 | 59 | 0.37× | 115.00 |
| 2 | 42 | 102 | 0.41× | 115.00 |
| 3 | 57 | 67 | 0.85× | 115.00 |
| 4 | 69 | 98 | 0.70× | 115.00 |
| 5 | 200 | 324 | 0.62× | 115.00 |
| 6 | 415 | 578 | 0.72× | 115.00 |

**ft09** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 4 | 43 | 0.09× | 115.00 |
| 2 | 7 | 12 | 0.58× | 115.00 |
| 3 | 14 | 23 | 0.61× | 115.00 |
| 4 | 16 | 28 | 0.57× | 115.00 |
| 5 | 21 | 65 | 0.32× | 115.00 |
| 6 | 13 | 37 | 0.35× | 115.00 |

**g50t** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 25 | 78 | 0.32× | 115.00 |
| 2 | 31 | 175 | 0.18× | 115.00 |
| 3 | 64 | 179 | 0.36× | 115.00 |
| 4 | 77 | 230 | 0.33× | 115.00 |
| 5 | 59 | 96 | 0.61× | 115.00 |
| 6 | 77 | 54 | 1.43× | 49.18 |
| 7 | 43 | 67 | 0.64× | 115.00 |

**ka59** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 28 | 28 | 1.00× | 100.00 |
| 2 | 44 | 109 | 0.40× | 115.00 |
| 3 | 82 | 51 | 1.61× | 38.68 |
| 4 | 42 | 51 | 0.82× | 115.00 |
| 5 | 20 | 33 | 0.61× | 115.00 |
| 6 | 70 | 132 | 0.53× | 115.00 |
| 7 | 109 | 326 | 0.33× | 115.00 |

**lf52** (10 / 10 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 9 | 32 | 0.28× | 115.00 |
| 2 | 67 | 81 | 0.83× | 115.00 |
| 3 | 46 | 60 | 0.77× | 115.00 |
| 4 | 52 | 71 | 0.73× | 115.00 |
| 5 | 88 | 205 | 0.43× | 115.00 |
| 6 | 122 | 148 | 0.82× | 115.00 |
| 7 | 220 | 244 | 0.90× | 115.00 |
| 8 | 71 | 109 | 0.65× | 115.00 |
| 9 | 209 | 164 | 1.27× | 61.57 |
| 10 | 98 | 225 | 0.44× | 115.00 |

**lp85** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 5 | 17 | 0.29× | 115.00 |
| 2 | 10 | 38 | 0.26× | 115.00 |
| 3 | 16 | 31 | 0.52× | 115.00 |
| 4 | 13 | 16 | 0.81× | 115.00 |
| 5 | 16 | 41 | 0.39× | 115.00 |
| 6 | 19 | 60 | 0.32× | 115.00 |
| 7 | 8 | 26 | 0.31× | 115.00 |
| 8 | 15 | 159 | 0.09× | 115.00 |

**ls20** (7 / 7 levels, score 93.59)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 16 | 22 | 0.73× | 115.00 |
| 2 | 47 | 123 | 0.38× | 115.00 |
| 3 | 40 | 73 | 0.55× | 115.00 |
| 4 | 65 | 84 | 0.77× | 115.00 |
| 5 | 141 | 96 | 1.47× | 46.36 |
| 6 | 195 | 192 | 1.02× | 96.95 |
| 7 | 192 | 186 | 1.03× | 93.85 |

**m0r0** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 18 | 30 | 0.60× | 115.00 |
| 2 | 35 | 111 | 0.32× | 115.00 |
| 3 | 71 | 203 | 0.35× | 115.00 |
| 4 | 11 | 26 | 0.42× | 115.00 |
| 5 | 53 | 500 | 0.11× | 115.00 |
| 6 | 76 | 237 | 0.32× | 115.00 |

**r11l** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 27 | 22 | 1.23× | 66.39 |
| 2 | 11 | 33 | 0.33× | 115.00 |
| 3 | 31 | 51 | 0.61× | 115.00 |
| 4 | 25 | 26 | 0.96× | 108.16 |
| 5 | 18 | 52 | 0.35× | 115.00 |
| 6 | 16 | 49 | 0.33× | 115.00 |

**re86** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 24 | 26 | 0.92× | 115.00 |
| 2 | 36 | 42 | 0.86× | 115.00 |
| 3 | 47 | 86 | 0.55× | 115.00 |
| 4 | 44 | 108 | 0.41× | 115.00 |
| 5 | 63 | 189 | 0.33× | 115.00 |
| 6 | 62 | 139 | 0.45× | 115.00 |
| 7 | 139 | 424 | 0.33× | 115.00 |
| 8 | 269 | 241 | 1.12× | 80.27 |

**s5i5** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 13 | 20 | 0.65× | 115.00 |
| 2 | 49 | 89 | 0.55× | 115.00 |
| 3 | 53 | 106 | 0.50× | 115.00 |
| 4 | 42 | 54 | 0.78× | 115.00 |
| 5 | 29 | 162 | 0.18× | 115.00 |
| 6 | 29 | 38 | 0.76× | 115.00 |
| 7 | 47 | 86 | 0.55× | 115.00 |
| 8 | 42 | 83 | 0.51× | 115.00 |

**sb26** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 16 | 18 | 0.89× | 115.00 |
| 2 | 15 | 28 | 0.54× | 115.00 |
| 3 | 15 | 18 | 0.83× | 115.00 |
| 4 | 15 | 19 | 0.79× | 115.00 |
| 5 | 17 | 31 | 0.55× | 115.00 |
| 6 | 19 | 23 | 0.83× | 115.00 |
| 7 | 17 | 58 | 0.29× | 115.00 |
| 8 | 17 | 18 | 0.94× | 112.11 |

**sc25** (6 / 6 levels, score 77.88)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 33 | 36 | 0.92× | 115.00 |
| 2 | 8 | 6 | 1.33× | 56.25 |
| 3 | 38 | 32 | 1.19× | 70.91 |
| 4 | 38 | 83 | 0.46× | 115.00 |
| 5 | 164 | 143 | 1.15× | 76.03 |
| 6 | 65 | 50 | 1.30× | 59.17 |

**sk48** (8 / 8 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 18 | 61 | 0.30× | 115.00 |
| 2 | 113 | 177 | 0.64× | 115.00 |
| 3 | 59 | 101 | 0.58× | 115.00 |
| 4 | 98 | 103 | 0.95× | 110.46 |
| 5 | 183 | 230 | 0.80× | 115.00 |
| 6 | 329 | 181 | 1.82× | 30.27 |
| 7 | 79 | 125 | 0.63× | 115.00 |
| 8 | 70 | 92 | 0.76× | 115.00 |

**sp80** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 45 | 39 | 1.15× | 75.11 |
| 2 | 7 | 58 | 0.12× | 115.00 |
| 3 | 21 | 25 | 0.84× | 115.00 |
| 4 | 26 | 148 | 0.18× | 115.00 |
| 5 | 54 | 96 | 0.56× | 115.00 |
| 6 | 86 | 152 | 0.57× | 115.00 |

**su15** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 11 | 22 | 0.50× | 115.00 |
| 2 | 14 | 42 | 0.33× | 115.00 |
| 3 | 18 | 26 | 0.69× | 115.00 |
| 4 | 13 | 115 | 0.11× | 115.00 |
| 5 | 20 | 36 | 0.56× | 115.00 |
| 6 | 13 | 31 | 0.42× | 115.00 |
| 7 | 10 | 8 | 1.25× | 64.00 |
| 8 | 8 | 40 | 0.20× | 115.00 |
| 9 | 22 | 41 | 0.54× | 115.00 |

**tn36** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 10 | 32 | 0.31× | 115.00 |
| 2 | 12 | 72 | 0.17× | 115.00 |
| 3 | 9 | 26 | 0.35× | 115.00 |
| 4 | 23 | 40 | 0.57× | 115.00 |
| 5 | 33 | 30 | 1.10× | 82.64 |
| 6 | 53 | 55 | 0.96× | 107.69 |
| 7 | 51 | 62 | 0.82× | 115.00 |

**tr87** (6 / 6 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 50 | 54 | 0.93× | 115.00 |
| 2 | 32 | 58 | 0.55× | 115.00 |
| 3 | 32 | 40 | 0.80× | 115.00 |
| 4 | 21 | 45 | 0.47× | 115.00 |
| 5 | 21 | 71 | 0.30× | 115.00 |
| 6 | 24 | 146 | 0.16× | 115.00 |

**tu93** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 21 | 19 | 1.11× | 81.86 |
| 2 | 10 | 16 | 0.63× | 115.00 |
| 3 | 24 | 34 | 0.71× | 115.00 |
| 4 | 18 | 42 | 0.43× | 115.00 |
| 5 | 29 | 123 | 0.24× | 115.00 |
| 6 | 28 | 80 | 0.35× | 115.00 |
| 7 | 14 | 14 | 1.00× | 100.00 |
| 8 | 23 | 23 | 1.00× | 100.00 |
| 9 | 71 | 111 | 0.64× | 115.00 |

**vc33** (7 / 7 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 6 | 7 | 0.86× | 115.00 |
| 2 | 10 | 18 | 0.56× | 115.00 |
| 3 | 46 | 44 | 1.05× | 91.49 |
| 4 | 86 | 61 | 1.41× | 50.31 |
| 5 | 83 | 131 | 0.63× | 115.00 |
| 6 | 20 | 34 | 0.59× | 115.00 |
| 7 | 49 | 152 | 0.32× | 115.00 |

**wa30** (9 / 9 levels, score 100.00)

| Level | Agent actions | Human actions | Agent / Human | Level score |
| --- | --- | --- | --- | --- |
| 1 | 30 | 71 | 0.42× | 115.00 |
| 2 | 48 | 119 | 0.40× | 115.00 |
| 3 | 91 | 183 | 0.50× | 115.00 |
| 4 | 85 | 98 | 0.87× | 115.00 |
| 5 | 373 | 368 | 1.01× | 97.34 |
| 6 | 70 | 68 | 1.03× | 94.37 |
| 7 | 47 | 79 | 0.59× | 115.00 |
| 8 | 289 | 442 | 0.65× | 115.00 |
| 9 | 203 | 415 | 0.49× | 115.00 |

---

## 9. System-level comparison (verbatim table)

EXPLICIT — "In the table below, we compare VISTA with state-of-the-art methods on the ARC-AGI Community Leaderboard, most of which are concurrent work released within the past few days." Table reproduced exactly (two-row systems list two model backends):

| System | Program-based | Model | Reasoning effort | RHAE |
| --- | --- | --- | --- | --- |
| Official minimal interface | No | GPT-5.6 Sol | max | 13.33 |
|  |  | Opus 5.0 | high | 30.16 |
| Schema | Yes | GPT-5.6 Sol | xhigh → max | 95.35 |
|  |  | Opus 4.8 → Fable 5 | max | 98.98 |
| ewma_sv_v1.6 | Yes | GPT-5.6 Sol | xhigh | 98.97 |
| Retrodict | Yes | GPT-5.6 Sol | max | 99.86 |
| Tycho | Yes | GPT-5.6 Sol | max | **100.00** |
|  |  | Opus 5.0 | xhigh | **100.00** |
| **VISTA** (ours) | **No** | GPT-5.6 Sol | max | 98.27 |
|  |  | Opus 5.0 | xhigh | **100.00** |

EXPLICIT (table footnote): "An arrow marks a fallback: Schema runs Opus 4.8 and Sol at xhigh first, reruns any game scoring below 80 with Fable 5 and Sol at max, and keeps the higher per-game score. Efforts for the other systems are taken from their published configurations and traces."

EXPLICIT: "VISTA reaches a perfect **100.00** RHAE with Opus 5.0 and 98.27 with GPT-5.6 Sol. Notably, to our knowledge, it is the first system to reach a perfect or near-perfect score **without** program synthesis. As a reference, the official baselines from the ARC-AGI-3 organizers, which also do not use program synthesis, score 30.16 with Opus 5.0 and 13.33 with GPT-5.6 Sol."

Linked systems (EXPLICIT link targets on the page): Official minimal interface → arcprize.org/results/openai-gpt-5-6; Schema → schema-harness.github.io; ewma_sv_v1.6 → github.com/astroseger/arc-3-agents-baseline1; Retrodict → github.com/ryanbbrown/Retrodict; Tycho → github.com/NIMI-research/Tycho.

---

## 10. Contamination caveat

EXPLICIT — verbatim, from "What This Shows and What's Next":

> "We acknowledge that the model’s existing capabilities are a key factor in this success, and that the visual harness is a simple but effective way of eliciting them. In addition, the models we use were released after the public ARC-AGI-3 games, so we cannot rule out that these games were seen during training; the private set remains the real test of generalization."

---

## 11. Other extracted claims

- **Representation robustness** — EXPLICIT: "We asked VISTA to play S5I5 and CD82 from each representation alone. It inferred how both games worked and completed Level 1 in all three settings. These are independent trajectories rather than identical action sequences." The three representations (EXPLICIT): "Text grid — 64 by 64 integers, one color is represented by one integer"; "2D image — A 512 by 512 PNG, an image render of the same 64 by 64 integer grid"; "3D render — A 3D rendering of the same game." EXPLICIT (finding): "We find that while the agent is still able to perform well with the textual grid, it is less efficient in terms of token usage. We also find that the agent is still able to act effectively in the 3D scene, a form that is closer to how humans perceive the real physical world."
- **Free-form language vs. program world models** — EXPLICIT: "We think much of the reasoning that leads to a good action can be carried out in a fuzzy manner. Natural language reasoning behaves more similarly to human beings and turns out to suffice for even these challenging ARC-AGI-3 games."
- **Lossless visual memory** — EXPLICIT: "A core design of VISTA is to maintain the game states as an explicit visual memory, which stores every frame returned by the environment, together with its turn and frame index, in a *lossless way*." EXPLICIT: memory-comparison table row for lossless visual memory — kept: "Every returned frame at full resolution, indexed by turn and frame."; lost: "Nothing."
- **Replays** — EXPLICIT: "Each available replay link opens the recorded trajectory, including game actions, public model output, visual inspections, and agent notes." (Replay URLs are relative to the site, e.g. `replays/claude-opus-5/games/<game>/index.html`.)
- **Benchmark framing** — EXPLICIT: "Nevertheless, ARC-AGI-3 is a testbed, not the target. The design is not restricted to 2D visual games, and extends straightforwardly to any interactive environment."
- **Minimalism** — EXPLICIT: "We aim for a minimalist design, avoiding complex systems and task-specific engineering, instead focusing on a simple setup that supports the model to perceive and reason about the world in a natural way."

---

## 12. Companion paper / tech report search

Searches performed on 2026-08-26:

1. Web search: `VISTA ARC-AGI-3 MIT visual harness Kaiming He arXiv` — hits: the project site itself; announcement post by co-author Keya Hu on X (x.com/HuLillian39250/status/2085184679280521530); news-style coverage (digg.com/tech/ey3apt71; dev.to/p0rt/the-model-scored-30-the-harness-scored-100-which-one-did-you-benchmark-3mp4); an aggregator "paper" page (theresanaiforthat.com — returned HTTP 403 on fetch, could not be inspected; it is a secondary aggregator, not a publication venue). No arXiv entry for VISTA.
2. Web search: `"VISTA" ARC-AGI-3 "GUIDE.md" arXiv 2026` — no VISTA paper; only the ARC-AGI-3 benchmark report and unrelated ARC-AGI-3 papers.
3. arXiv search (paper-search API): `VISTA Visual Harness Reasoning Interactive World` — no match (nearest hits are unrelated: driving world model "Vista" arXiv:2405.17398; ViSTA-SLAM arXiv:2509.01584).
4. arXiv search (paper-search API) by authors/topic: `Qiushi Han Keya Hu Linlu Qiu ARC-AGI-3 harness` — no VISTA paper. Same-group related-but-distinct work found: "ARC Is a Vision Problem!" (VARC), Hu, Cy, Qiu, Ding, Wang, Zhu, Andreas, He, arXiv:2511.14761; and "ELF: Embedded Language Flows," arXiv:2605.10938.

**Conclusion: as of 2026-08-26 no companion paper, preprint, or tech report for VISTA exists.** Corroborating evidence: the site's own "Cite this work" BibTeX is a `@misc` entry whose only locator is the website URL (§1). Consequently no PDF was downloaded and no `VISTA_paper_fulltext.md` was produced. Re-check arXiv (search "VISTA visual harness") before final citation freeze of any paper using this source.

Related primary sources a reader may want alongside this page (verified to exist, not VISTA itself):

- ARC-AGI-3 benchmark: "ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence," arXiv:2603.24621; official scoring methodology at docs.arcprize.org/methodology.
- Program-synthesis competitor systems referenced by the page: Schema (schema-harness.github.io), Tycho, Retrodict, ewma_sv_v1.6 (see §9 links).

SPECULATIVE (flagged, not load-bearing): co-author Keya Hu's X announcement thanks "my incredible co-authors Josh and Linlu," while the site lists five authors (Qiushi Han, Keya Hu, Linlu Qiu, Cathy Wu, Kaiming He); "Josh" is plausibly an English name used by Qiushi Han. The site's author list is authoritative.

---

## 13. Provenance and integrity

- Attempted URL: https://vista-research.github.io/ — HTTP 200 on 2026-08-26 (curl -sL; also fetched via WebFetch). No redirects, no paywall.
- Archived copy: `Sources/_raw/vista-research.github.io_index_2026-08-26.html`, 396,427 bytes, SHA-256 `220ed4c18eee568a0c6747e137c2896f56411c1084fca22909de0598846f1ec6`.
- Tables in §8–§9 were parsed programmatically (Python, regex over the markitdown conversion of the archived HTML) to avoid transcription error; the parser asserted 25 games and level-count consistency per game, and verified that each game's per-level agent/human actions sum to the game's total agent/human actions.
- Known site content NOT captured in this file: embedded videos/figures (mp4/png assets), the interactive per-game cumulative-progress chart annotations (redundant with the per-level breakdowns), and the per-game replay pages (linked from §8 row data on the live site).
