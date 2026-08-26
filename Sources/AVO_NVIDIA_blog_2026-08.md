# Source: NVIDIA Technical Blog — AVO Reaches 100% on ARC-AGI-3 (2026-08-21)

**Status: ACQUIRED.**

## Citation block

- **Authors:** Terry Chen, Yeyin (Eva) Zhu, Zhifan Ye, Jean-Francois Puget, Humphrey Shi
- **Title:** *NVIDIA AVO Reaches 100% on ARC-AGI-3, Demonstrating a Frontier-Level General-Purpose Architecture for Long-Horizon Autonomous Agents*
- **Venue:** NVIDIA Technical Blog (developer.nvidia.com), category "Agentic AI / Generative AI"
- **Publication date:** Aug 21, 2026
- **URL:** https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/
- **Access date:** 2026-08-26
- **Local archive:** `Sources\_raw\AVO_NVIDIA_blog_2026-08-21.html` (273,281 bytes) — sha256 `ca9e6d03feaa4771e1c7881463202c59d551896207c9745bad76ad56066fc67c`. Note: the archived HTML is a live-page snapshot; a re-fetch may differ in dynamic page furniture (the sha256 fixes *this* snapshot, not the article for all time).
- **Post subtitle (dek), verbatim:** "The research project elevates Claude Opus 5 from a 30% model baseline to 100% as part of the complete AVO agent system, showing that system design—not model capability alone—can unlock frontier-level long-horizon performance"
- **Editor's note on the page, verbatim:** "Editor's note: We updated the wording to more precisely distinguish the ARC-AGI-3 public set from the semi-private and private competition sets." (The page has been revised at least once since first publication; the wording quoted below is the revised wording as of 2026-08-26.)
- **Companion source:** the post's "Read the paper" link points to https://arxiv.org/pdf/2603.24517 — the March 2026 AVO kernel-optimization paper documented in `Sources\AVO_2026.md`. The ARC-AGI-3 results below appear **only in this blog post**, not in that paper.

## Section headings (in order)

What is AVO? · Improving performance with autonomous GPU-kernel optimization · Sustaining long-running agentic work · Evolving from high-performance engineering to general-purpose reasoning · Evaluating AVO on ARC-AGI-3 · AVO performance results on the ARC-AGI-3 benchmark · What we learned from benchmarking AVO on ARC-AGI-3 · Looking ahead

## Labeled extraction

Labels: **EXPLICIT** = verbatim quote verified against the fetched page HTML (2026-08-26; cited by section, since a blog has no pages). **STRONG INFERENCE** = follows directly from the text. **SPECULATIVE** = not supported by this document.

### Headline result

- **EXPLICIT (section "Evolving from high-performance engineering to general-purpose reasoning"):** "AVO achieved a 100.00 RHAE score across all 25 environments in the ARC-AGI-3 public set, completing all 183 levels."
- **EXPLICIT (section "AVO performance results on the ARC-AGI-3 benchmark") — the action counts:** "Using Claude Opus 5, AVO completed the full 25-environment public set with a 100.00 RHAE score, solving all 183 levels in 6,624 environment actions. For reference, VISTA reports 7,542 environment actions with Claude Opus 5 while completing the same 183 public-set levels. AVO therefore used approximately 12% fewer actions in this cross-system comparison."

### What AVO is; the "harness" framing

- **EXPLICIT (lede):** "A frontier language model is only one component of an AI agent. The surrounding agent system—often called a harness—determines how the model receives context, uses tools, maintains state, responds to feedback, recovers from failure, and sustains progress over long-running tasks."
- **EXPLICIT (section "What is AVO?"):** "AVO is a general-purpose coding agent system developed by NVIDIA. Like modern coding agents, AVO can inspect and edit code, run commands, consult documentation, and validate its work through execution. Its distinguishing focus is sustained autonomous operation across long horizons."

### Architecture — main loop, persistent memory, supervisor

- **EXPLICIT (Figure 1 caption):** "AVO architecture for long-horizon autonomous agent work. The main agent iteratively inspects context, plans, implements changes, and evaluates results using persistent memory and tools, while a supervisor monitors the broader search trajectory and can intervene when progress stalls"
- **EXPLICIT (section "Sustaining long-running agentic work"):** "AVO is designed to preserve progress beyond a single model context. Two mechanisms are particularly important: persistent memory and supervision. Persistent memory carries forward prior implementations, evaluation results, compiler and profiler outputs, and accumulated reasoning, allowing the agent to resume from the current state rather than repeatedly reconstructing the search. The supervisor monitors the broader trajectory for stagnation or repeated unproductive cycles and can redirect the main agent toward alternative strategies when needed."
- **EXPLICIT (same section):** "During the seven-day attention-kernel run, the main agent remained responsible for deciding what to inspect, change, test, and evaluate, while the supervisor helped maintain forward progress when the search plateaued."
- **EXPLICIT (section "Evaluating AVO on ARC-AGI-3"), on the agent backend:** "...our system uses AVO, the NVIDIA long-horizon agent architecture with persistent memory, supervision, and its own execution loop."

### The benchmark and the RHAE metric

- **EXPLICIT (section "Evaluating AVO on ARC-AGI-3"):** "ARC-AGI-3 is an interactive reasoning benchmark. An agent enters unfamiliar game-like environments without instructions, explicit rules, or a stated goal."
- **EXPLICIT (same section):** "The benchmark uses Relative Human Action Efficiency (RHAE), a metric that combines task completion with per-level action efficiency relative to first-time human baselines. Performance is aggregated across levels and environments."

### Model used

- **EXPLICIT:** "Using Claude Opus 5, AVO completed the full 25-environment public set with a 100.00 RHAE score..." (see Headline result above for the full sentence).
- **EXPLICIT (section "AVO performance results..."), cross-model experiments:** "AVO is also designed to operate across frontier models. While our full public-set result used Claude Opus 5, we additionally paired AVO with GPT-5.6 Sol on a challenging subset of games. In these limited experiments, Sol reached matched levels faster in wall-clock time in several cases, while Opus used fewer environment actions in matched-level comparisons. These preliminary results suggest complementary operating profiles across models, and we leave a broader systematic comparison to future work."
- **EXPLICIT (section "Evaluating AVO on ARC-AGI-3"), on VISTA's backends:** "VISTA instantiates the harness with Claude Opus 5 through Claude Code or GPT-5.6 Sol through Codex..."

### Public set vs. semi-private/private sets

- **EXPLICIT (section "AVO performance results on the ARC-AGI-3 benchmark"):** "These results cover the 25-environment ARC-AGI-3 public set using the official scorecard and RHAE metric. They are not results on the semi-private or fully private competition sets."

### Caveats / limitations stated in the post

- **EXPLICIT (section "AVO performance results...") — not a controlled ablation:** "This should not be interpreted as a controlled ablation: the two systems differ in agent backend, observation representation, memory, context management, and other implementation details."
- **EXPLICIT (same passage) — memory contribution not isolated:** "One architectural difference that may matter over long horizons is the AVO memory system, which is designed to carry useful understanding forward and reduce repeated exploration, although this experiment does not isolate its individual contribution."
- **EXPLICIT (same section) — on the 30% baseline comparison:** "ARC Prize separately reports approximately 30% for Claude Opus 5 at High reasoning effort. Our run used the same model family under a different reasoning setting and a substantially different agent system and evaluation setup. These numbers therefore should not be interpreted as a direct measurement of the performance contribution of AVO; rather, they illustrate that model-level evaluation alone does not characterize the performance of a complete agent."
- **STRONG INFERENCE:** The widely repeated framing "AVO lifts Claude Opus 5 from 30% to 100%" originates in the post's own dek, but the post's body explicitly warns against reading the 30%-vs-100 comparison as a measurement of AVO's contribution (different reasoning setting, agent system, and evaluation setup). Citing the 30%→100 jump without that caveat misrepresents the source.

### Related systems named

- **EXPLICIT (section "AVO performance results..."):** "Recent ARC-AGI-3 systems have explored substantially different agent architectures, from explicit executable world models such as Tycho to direct-interaction harnesses such as VISTA."
- **EXPLICIT (section "Evaluating AVO on ARC-AGI-3"):** "Several elements of the task interface were informed by VISTA, but the agent backend was fundamentally different." Also: "VISTA's primary configuration uses a rendered 512 x 512 PNG, while also exploring textual-grid representations."
- The post's "Browse related work" links name: "VISTA: A Visual Harness For Reasoning in an Interactive World" and "Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3".

### Kernel-work summary as retold by the blog (context for the arXiv paper)

- **EXPLICIT (AI-generated summary box on the page — note: the page itself labels this passage "AI-Generated Summary ... AI-generated content may summarize information incompletely. Verify important information."):** "...AVO autonomously explored over 500 directions, committing 40 kernel versions, and achieved up to 10.5% better performance than FlashAttention-4 on NVIDIA DGX B200 systems, demonstrating productive engineering loops without manual intervention."
- These figures (500 directions, 40 versions, 10.5% over FlashAttention-4) match the arXiv paper's own EXPLICIT claims (see `AVO_2026.md`, extraction (c)).

## Verification notes

- All EXPLICIT quotes were verified against the raw page HTML fetched 2026-08-26 (tags stripped, entities decoded); typographic apostrophes/em-dashes normalized to their Unicode forms. The archived snapshot is in `Sources\_raw\AVO_NVIDIA_blog_2026-08-21.html`.
- What this source **cannot** establish: any semi-private/private-set performance; wall-clock time, token, or cost figures for the ARC-AGI-3 run (none are given); the isolated contribution of memory or supervision (explicitly disclaimed); per-environment RHAE breakdowns (a figure is referenced but numeric per-environment data is not in the text).
