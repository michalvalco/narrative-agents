# Step 0 — Cost Notes (2026-08-26)

**Run:** sb26, arm B, one run, 60 paid actions in two 30-action segments with
one true forced handoff between them (fresh context resumed from
`GUIDE.md` + `WORKING.md` + `arc status` only). Model: `claude-sonnet-5`
via Claude Code subagents, effort medium. Raw per-segment records:
`cost_segments.jsonl`.

## Measured

| | Segment 1 (a1–30) | Segment 2 (a31–60) | Combined |
|---|---|---|---|
| Subagent tokens | 135,228 | 206,934 | 342,162 |
| Tokens / paid action | 4,508 | 6,898 | **5,703** |
| Predictions ✓/✗ | 26/4 | 25/5 | 51/9 (85%) |
| Wall clock | 11.7 min | 24.8 min | 36.5 min |
| Handoff note tokens (chars/4) | 967 | 1,144 | cap 1,200 ✓ both |
| Post-handoff burn | — | **0** | — |

Segment 2 ran hotter because level 2's slot-ordering rule resisted five
hypotheses (all falsified with correct predictions of the *failure*); the
harness nudged the rules-tier at 42 actions on the level. Easy-progress play
(segment 1) is the optimistic rate; puzzle-grind (segment 2) the pessimistic.

## Semantics caveat (read before quoting dollar figures)

`subagent_tokens_total` is the harness's aggregate for the agent. The API
input/output split is not observable from outside the agent, so dollars are
**bounds, not a point estimate** (Sonnet 5: $2/MTok in, $10/MTok out;
Haiku 4.5: $1/$5):

- **Upper bound** — treat the total as output-dominated (thinking + text)
  plus a cached-input overlay: ≈ **$0.07 / action** (Sonnet), ≈ $0.035 (Haiku).
- **Lower bound** — treat it as a cache-discounted blended total:
  ≈ **$0.02 / action** (Sonnet), ≈ $0.01 (Haiku).

Also: these Step 0 segments ran on the Claude Code subscription — zero
marginal API dollars. The $50 ceiling is only consumed if the pilot runs
API-billed (managed agents / routines on API keys). A pilot run the same way
as Step 0 spends subscription capacity instead.

## Pilot arithmetic against the $50 ceiling

Actions per cell: sb26 full game ≈ 150–250 actions (VISTA's Opus run: 124).
Core-four arm-seed per Spec §2: ≈ 1,500–2,500 actions.

| Pilot shape | Actions | Sonnet 5 | Haiku 4.5 |
|---|---|---|---|
| Full spec: core 4 × 3 arms × 2 seeds + telos sub-study | 12k–20k | $240–1,400 | $120–700 |
| sb26-only: 3 arms × 2 seeds | 0.9k–1.5k | $18–105 | $9–53 |
| sb26-only + telos sub-study (8 cells) | 1.2k–2k | $24–140 | **$12–70** |

**What fits $50:** the sb26-only pilot including the telos sub-study on
**Haiku 4.5** (mid-estimate ≈ $25–35), or the same on Sonnet 5 at one seed.
The full-spec pilot needs a ceiling of roughly **$300–700 (Haiku)** /
**$500–1,400 (Sonnet)** — or the subscription route, where the ceiling is
attention and usage-limits rather than dollars.

## Step 0 state

Game parked at event 60, level 2/8, `NOT_FINISHED`, exactly replayable
(`arc start sb26` in this directory resumes). Level 2's ordering rule is the
open puzzle; next context should take the harness's rules-tier nudge rather
than a sixth manual guess.
