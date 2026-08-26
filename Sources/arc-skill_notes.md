# Source notes — arc-skill (Poobesh Gowtham)

Phase-2 source documentation for the narrative-agents experiment. All file/line references
are to the read-only clone at `vendor\arc-skill\` (repo root = that directory). Quotes are
verbatim. Claims are labeled EXPLICIT (verbatim from source), STRONG INFERENCE (directly
entailed by the quoted code/text), or SPECULATIVE (flagged as such).

## Citation block

- **Repository:** https://github.com/pbshgthm/arc-skill (verified via `git config --get remote.origin.url` in the clone)
- **Clone location:** `C:\Users\Michal Valco\Documents\OneDrive\Documents\GitHub\narrative-agents\vendor\arc-skill\`
- **Commit:** `dba53c3799eab600a512dd73ed037d7ab6958c66` (HEAD of `main` in the clone; verified with `git rev-parse HEAD`)
- **Commit date / subject:** 2026-08-19 20:55:00 +0530 — "docs: rewrite readme from site content"
- **Author (per README):** "By [Poobesh Gowtham](https://poobesh.com) · [@pbshgthm](https://x.com/pbshgthm). August 2026." (README.md:227-228)
- **Companion write-up:** https://arc-skill.vercel.app (accessed 2026-08-26; see §7 below)
- **Access date for all local reads:** 2026-08-26

What the artifact is (EXPLICIT): "The skill is 129 lines of instruction plus a 4,343-line
command line tool. Neither one mentions a single one of those 25 games." (README.md:30-31).
Verified locally: `skills/arc-skill/SKILL.md` is 129 lines; `wc -l` over `scripts/arc`,
`scripts/arc_cli.py`, `scripts/broker_server.py`, and `scripts/arc_skill/*.py` totals 4,343 lines.

Headline result (EXPLICIT, README.md:24-28): "Games finished **25 of 25** | Levels finished
**183 of 183** | RHAE **100.00** — the benchmark's own score, and its ceiling | Actions
**7,645**, where the median human needs 17,135 | Verified by ARC scorecard
[`24ddb219`](https://arcprize.org/scorecards/24ddb219-987e-464f-9050-6398a29cf5ac)".

---

## 1. The prediction gate — where a press without a prediction is refused

The gate is enforced in three layers, all before any action is spent.

**(a) The CLI refuses `arc act` without `--predict` (EXPLICIT).**
`skills/arc-skill/scripts/arc_skill/cli.py:103-108`:

```python
    act.add_argument(
        "--predict",
        required=True,
        help='what this action does, e.g. "move 12,5 1,0" (see below)',
    )
```

`required=True` means argparse itself rejects a bare `arc act ACTION1`. The parser's error
hook is overridden (cli.py:49-51) so the refusal is raised as the harness's own error type:

```python
class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ArcSkillError(message)
```

and `main()` catches it (cli.py:487-489), printing `ERROR | <message>` and exiting with
status 2. STRONG INFERENCE: since this happens during argument parsing, no game action is
ever dispatched — matching README.md:74: "A press without one is refused, and the refusal
is free."

**(b) An empty or contentless prediction is refused (EXPLICIT).**
`skills/arc-skill/scripts/arc_skill/predictions.py:61-64` (inside `parse_claims`):

```python
        raise ArcSkillError(
            f"an empty prediction predicts nothing; say what you expect\n{CLAIMS_HELP}"
        )
```

A malformed structured claim (one that starts with a claim keyword but does not parse) is
also refused: `raise ArcSkillError(f"malformed claim {part!r}\n{CLAIMS_HELP}")`
(predictions.py:103). Free text that is not a claim is kept as commentary, but the parser
then appends `{"kind": "change", "text": "change (implied by free text)"}` (predictions.py:105-109)
— with the in-code comment "A prose prediction still commits to a visible effect."
(predictions.py:107). So even prose is graded as "something visible changes".

**(c) Ordering guarantee — refusal happens before the action is spent (STRONG INFERENCE
from code order).** In `execute_action` (`skills/arc-skill/scripts/arc_skill/live.py:115-129`),
`claims = parse_claims(predict)` runs at live.py:123; the paid step (`_paid_step`, which
calls `broker_step` and actually spends the action) runs only afterwards at live.py:129.
A parse failure therefore aborts before any action is consumed.

**Batches carry the same gate per step (EXPLICIT).** `parse_step` (live.py:177-183):

```python
def parse_step(raw: str) -> tuple[str, str]:
    action, separator, predict = raw.partition("::")
    if not separator or not action.strip() or not predict.strip():
        raise ArcSkillError(
            'each step needs its own prediction: --step "ACTION1 :: <claims>"'
        )
```

`execute_steps` parses every step's claims up front (live.py:202-206) before executing any,
and a solve-plan is refused unless it has one prediction per action
(`"plan needs one prediction per action; rerun `arc rules solve`"`, live.py:290-292).

### How the grade is computed against the returned frame

The claim vocabulary (EXPLICIT, predictions.py:18-30, `CLAIMS_HELP`): `noop`, `change`,
`cell X,Y=V`, `move X,Y DX,DY`, `vanish X,Y`, `region X0:X1,Y0:Y1`, `level+1`, `win`;
"separate several with \";\" | x=column y=row (like ACTION6)".

`grade_claims(claims, before, event)` (predictions.py:131-247) grades each structured claim
independently against the settled post-action frame:

- The after-frame is `after = frame_at(event)` (predictions.py:137) — the frame the game
  actually returned, decoded from the recorded event.
- `changed = int(np.count_nonzero(before != after))` when shapes match (predictions.py:139).
- `level_advanced` compares `event["levels_completed"]` with `event["level_before"]`
  (predictions.py:140-144).
- Per-kind checks (all EXPLICIT in code): `noop` = same shape and `changed == 0`
  (152-158); `change` = shape changed or any cell changed or level advanced (159-165);
  `win` = `str(event["state"]) == "WIN"` (166-168); `level_up` = `level_advanced` (169-175);
  `cell` = `int(after[y, x]) == int(claim["value"])` (176-182); `vanish` = flood-fill the
  connected object at (x,y) in the before-frame, pass only if zero of its cells still hold
  its color (183-197); `move` = every shifted cell holds the object's color **and** every
  vacated cell no longer does — `ok = arrived and vacated`, with the failure diagnosis
  "old cells still color … (copied, not moved)" (198-226); `region` = something changed and
  no changed cell falls outside the half-open box (227-245).
- Each graded claim gets `{"ok": bool, "actual": <short description of reality>}`
  (predictions.py:246), and `grade_lines` renders them as `✓ <claim>` or
  `✗ <claim> — <actual>` (predictions.py:250-255).

In `execute_action` (live.py:130-155): `ok = all(item["ok"] for item in graded)`; the event
is stored with `predict`, `predict_ok`, and the full `grade` (live.py:133-135, persisted to
`.arc/events.jsonl` via `_record` → `append_event`); the receipt outcome is `"SURPRISE"`
with `detail = f"prediction missed: {first_failed[2:]}"` when any part missed (live.py:151-153),
`"PREDICTED"` / "result matched the prediction" otherwise (live.py:154-155). One wrong part
is a whole miss — matching README.md:52-53: "Eight claim forms, joined with `;`, each graded
on its own — one wrong part is a miss".

Batch halting (EXPLICIT, live.py:249-252): in `execute_steps`, `if not ok:` the outcome is
`"SURPRISE"`, the detail is `f"step {index + 1} missed: …; {remaining} remaining steps were
discarded"`, and the loop breaks — matching SKILL.md:64-66: "execution halts at the first
miss so a wrong theory cannot burn the rest of the queue".

---

## 2. Local cache / offline-replay mode

**Durable game cache (EXPLICIT).** `local_cache_root()` in
`skills/arc-skill/scripts/arc_skill/broker.py:39-46`: uses `ARC_SKILL_CACHE_DIR` if set,
else `XDG_CACHE_HOME`, else `~/.cache`, always suffixed `arc-skill/arcade`. Docstring:
"Return the durable shared cache used by local public-game runs." A donor cache is adopted
on first use (`_adopt_cached_game`, broker.py:49-63): it copies an already-downloaded game
from `AA3_CACHE_DIR` or `~/.cache/aa3/arcade`. A game counts as cached when
`<cache>/environment_files/<game_id>/*/metadata.json` exists (`_cached_game_exists`,
broker.py:70-72).

**Offline vs. download (EXPLICIT).** In `ArcSession.__init__` (broker.py:114-125), for a
local run:

```python
            runtime = Path(str(config.get("cache_dir") or local_cache_root()))
            ...
            mode = OperationMode.OFFLINE if game_cached else OperationMode.NORMAL
```

i.e. the upstream `arc-agi` toolkit is put in `OperationMode.OFFLINE` when the game is
already cached (no key, no network), and `OperationMode.NORMAL` for the one-time download.
If the game is not cached and no key is set, the error is (broker.py:149-151):
"`LOCAL_CACHE_MISS | {game_id} is not in {environments}; set ARC_API_KEY once so arc-skill
can download the public game into its durable local cache`". README.md:126-129 states the
same contract: "Needed once per game to download it into the durable local cache, and
always for `--mode competition`. Runs on an already-cached game need no key and no network."

**Local simulator with competition semantics (EXPLICIT).** `arc start` defaults to
`mode = "local"` (cli.py:282: `mode = str(args.mode or os.getenv("ARC_SKILL_MODE", LOCAL_MODE)).lower()`),
and prints "`STARTED | {game} | local simulator | competition accounting | replay recovery
enabled`" (cli.py:321-323). SKILL.md:16-18: "`start` defaults to a local simulator with
competition semantics: one logical run, append-only history, paid resets, completed levels
never lost."

**Crash-safe offline replay (EXPLICIT).** The machinery, in three files:

- Per-run state lives in `.arc/` (`RunPaths`, `skills/arc-skill/scripts/arc_skill/core.py:27-91`):
  `events.jsonl` (append-only timeline, core.py:39-41), `mutations.jsonl` (paid-action
  journal, core.py:71-73), `config.json`, `NOTES.md`, `receipts/`, `broker.json`.
  `append_event` assigns contiguous ids and appends (core.py:318-323); `load_events` refuses
  a non-contiguous timeline (core.py:308-315).
- The broker journals every paid action *before* the CLI records it. live.py:4-6 (module
  docstring): "Every paid action is journaled by the broker before the response is recorded,
  so a crash between spend and record is recovered on the next start." In the broker server
  loop, the mutation record `{"mutation_id", "action", "data", "reasoning", "observation"}`
  is appended to `mutations.jsonl` before the response is returned (broker.py:544-559).
- On every command, `reconcile_mutations(paths)` (broker.py:309-345; called at cli.py:405 and
  cli.py:237) replays any journaled mutation missing from `events.jsonl` — docstring:
  "Recover a paid step journaled by the broker before a CLI process died."
- On `arc start` of an existing local run, the broker process replays the entire recorded
  session deterministically against a fresh simulator: `_replay_local_session`
  (broker.py:428-455), docstring "Reconstruct an exact local session from the append-only
  paid-action journal." Any divergence is fatal: "`LOCAL_REPLAY_DIVERGED | fresh simulator
  state differs from event 0; cached game or seed changed`" (broker.py:435-437) and
  "`LOCAL_REPLAY_DIVERGED | mutation {id} no longer reproduces its recorded observation`"
  (broker.py:451-454); the CLI-side check is cli.py:268-271. SKILL.md:18-19: "It is
  crash-safe — after any interruption, rerun `\"$ARC\" start <GAME_ID>` and the run is
  resumed or replayed exactly."

The per-run game session is owned by a separate process (`scripts/broker_server.py`, 19
lines) reached over an AF_UNIX socket with a 0600 token (broker.py:348-386, 458-587;
socket path in core.py:79-87).

---

## 3. The competition-mode flag

- Flag surface (EXPLICIT): `arc start --mode {local,competition}` — cli.py:67-71, choices
  `(LOCAL_MODE, REMOTE_MODE)`; constants `LOCAL_MODE = "local"`, `REMOTE_MODE = "competition"`
  (broker.py:35-36). Default may also come from the environment: `ARC_SKILL_MODE`
  (cli.py:282; README.md:220 table: "Default mode when `--mode` is absent (`local` \| `competition`)").
- What it does (EXPLICIT): in `ArcSession.__init__`, a remote run sets
  `mode = OperationMode.COMPETITION` for the upstream `arc-agi` Arcade (broker.py:114-116)
  and requires `ARC_API_KEY` plus network ("could not initialize remote competition run …;
  ARC_API_KEY and network access are required", broker.py:144-147).
- Lease semantics (EXPLICIT): resuming a remote run checks idle time and refuses after
  15 minutes — "`REMOTE_LEASE_EXPIRED | no live action was recorded for at least 15 minutes.
  The remote competition run is not recoverable; preserve this directory and use a fresh
  one`" (cli.py:244-248). A new remote run prints "`STARTED | {game} | REMOTE competition |
  single run | ~15m action-idle lease | no replay recovery`" (cli.py:316-319). Divergence
  guard: "`REMOTE_STATE_DIVERGED | the live remote observation differs from the append-only
  timeline; stop using this run`" (cli.py:253-256).
- Doctrine (EXPLICIT, SKILL.md:19-21): "Use `--mode competition` (live remote server,
  ~15-minute idle lease, no replay recovery) only when the user explicitly asks."
  README.md:179-180: "Use `--mode competition` for the live remote server (single run,
  ~15-minute idle lease, no replay recovery)."
- Mode is sticky (EXPLICIT): "this directory already owns a {mode} run; mode cannot be
  changed in place" (cli.py:233-236).

---

## 4. Dependencies — exact pins

**PEP 723 inline metadata (EXPLICIT).** `skills/arc-skill/scripts/arc_cli.py:1-9`:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "arc-agi==0.9.9",
#   "numpy>=2.0,<3",
#   "pillow>=10,<13",
# ]
# ///
```

**Launcher fingerprint (EXPLICIT).** `skills/arc-skill/scripts/arc` line 10 asserts the
running interpreter matches exactly:

```bash
compatible='import sys, importlib.metadata as m; assert sys.version_info >= (3, 12); assert m.version("arc-agi") == "0.9.9"; import numpy, PIL; assert 2 <= int(numpy.__version__.split(".")[0]) < 3; assert 10 <= int(PIL.__version__.split(".")[0]) < 13'
```

and, when it must bootstrap a private venv, installs (arc:42-43):
`'arc-agi==0.9.9' 'numpy>=2,<3' 'pillow>=10,<13'`. (Note the cosmetic difference
`numpy>=2.0,<3` in arc_cli.py vs `numpy>=2,<3` in the launcher/README — semantically the
same range.)

**README statement (EXPLICIT, README.md:121-125):** "**Python 3.12+**, or **uv** — the
launcher bootstraps a private runtime when the system Python is unsuitable (first use only)
/ Runtime dependencies, installed automatically: `arc-agi==0.9.9`, `numpy>=2,<3`,
`pillow>=10,<13`". The launcher falls back to
`uv run --quiet --python '>=3.12' --script … arc_cli.py` when no usable python3 exists (arc:16-22).

**The exact `arc-agi` pin is therefore `arc-agi==0.9.9`** — stated identically in
arc_cli.py:5, arc:10, arc:43, and README.md:124.

---

## 5. The 37.1% / 2.9% figures

EXPLICIT — README.md:114-117 (single sentence spanning those lines):

> "The skill also never says when a mechanic counts as verified — only to batch proven ones
> and never batch exploration. The agent drew that line itself, and the two modes came out
> far apart: single test presses missed **37.1%** of the time, planned sequences **2.9%**,
> and 91.6% of all presses went into plans."

These figures do NOT appear in SKILL.md (verified by search of the 129-line file; SKILL.md
contains no percentages). The companion website states the same two rates with slightly
different framing (see §7): "A single test act missed 37.1% of the time. A planned sequence
missed 2.9%, about 13 times fewer, and Claude put 92% of its acts into plans." — the site
rounds 91.6% to 92% and gives the underlying counts: "642 acts, 8% of the campaign" (single
tests) vs "6,985 acts, 91% of the campaign" (planned sequences).

Related campaign totals (EXPLICIT, README.md:49-50): "Across the campaign the agent wrote
**7,627 graded predictions**; **443 missed**. Every one of the 25 games contained at least
one."

---

## 6. Other mechanics worth recording (context for the experiment)

- **One page of notes** (EXPLICIT, README.md:81-89 and SKILL.md:50-53): each run keeps
  `.arc/NOTES.md` with sections "Verified (cite event ids)", "Assumed / open questions",
  "Plan" (template written by `_write_notes`, cli.py:194-205). "Claude Code compacted its
  own context 115 times over this campaign … The pages stayed at a median of 60 lines"
  (README.md:82-88). Notes are archived to `.arc/levels/level-N.md` on level completion
  (`_archive_notes`, live.py:58-65).
- **Rules tier** (EXPLICIT): optional executable model — `arc rules {help,init,replay,solve}`
  (cli.py:146-160; contract in rules.py:37-59 `RULES_HELP`: required functions
  `initial/step/actions/goal/observe`, optional `key/heuristic/render/dead`; "Model only
  verified mechanics; mark gaps Unknown — replay reports them as INCOMPLETE, never as a
  fit"). README.md:109-112: the tier was "Taken once, and it never fitted. The game was won
  on the rung above."
- **Escalation ladder** (EXPLICIT, README.md:103-112): sentences → Python (24 of 25 games,
  1,727 calls) → a tool → a world model.
- **Reset discipline** (EXPLICIT, live.py:437-443): reset requires
  `--because "<why this board is worth abandoning>"` unless the state is GAME_OVER.

---

## 7. Companion write-up — https://arc-skill.vercel.app

- **URL:** https://arc-skill.vercel.app/ — **accessed 2026-08-26.**
- **Acquisition note (honest record):** a plain HTTP fetch returns only a ~3 KB React SPA
  shell (`<div id="root">` + `/assets/main-BEHIt-uh.js`); the static HTML contains no body
  text. Content below was captured from the fully rendered page (browser rendering,
  2026-08-26). Page title: "ARC-AGI-3 is a skill issue". Meta description (EXPLICIT, from
  the HTML shell): "One rule, say what an action will do before you spend it, let an
  unchanged Claude Code finish all 25 public ARC-AGI-3 games at 100.00 RHAE. 129 lines of
  skill. Every run is on this page."

### Content summary (rendered page, 2026-08-26)

Byline: "By Poobesh Gowtham · @pbshgthm", dated August 2026. Headline stats: RHAE 100.00 of
100; games 25 of 25; levels 183 of 183.

Sections, in page order:

1. **Lede / mechanic.** "The mechanic is one rule. Every act has to arrive with a written
   prediction of the next frame, cell by cell, and the tool refuses to send an act that has
   none. It then grades the prediction against the frame the game actually returned." Adds
   a count not in the README: the campaign is "11,344 claims deep" (claims = semicolon-
   separated parts; 7,627 predictions graded, 443 missed). "Only 642 of 7,627 graded acts
   went on finding things out, which is why 7,645 actions did what a median human player
   needs 17,135 for."
2. **What is ARC-AGI-3?** — 25 games, grid of colored cells, seven buttons, nothing
   explained; meanings change between games; embedded replayable board (lp85).
3. **What Claude gets** — the five instruments (See / Act / Plan / Compute / Model),
   matching README.md:69-77.
4. **Predict, then act** — the gate, with act 1 of the lp85 run quoted (same command as
   README.md:40-43); "Claude wrote 7,627 predictions. 443 missed."
5. **One miss turned an impossible level into an easy one** — case study of tu93 level 9:
   Claude proved no safe path existed (patrols rolled forward 250 ticks, every corridor
   node a cut vertex), then spent one act walking into a patroller while predicting the
   patroller would survive; the ✗ on `cell 40,17=c` revealed "Walking onto a patroller
   kills it", which was the intended solution. Quotes the run's own notes: "ENTERING A
   PATROLLER'S OWN NODE DESTROYS IT, exactly like a blue guard (e193)."
6. **How a claim is written** — the 8-form grammar; "The grammar is deliberately small:
   every form describes something the next frame can contradict." Loop diagram: Look →
   Predict → Act → Compare, "once for each of the 7,645 actions".
7. **One page of notes** — 115 compactions; median 60 lines; runs grew their own headings
   ("ls20 · REFUTED", "su15 · DANGER, the mistake that lost L9").
8. **Tight rules, free thinking** — gate hard / thinking free; the four-rung ladder with
   named runs: sb26 (prose only, eight levels, one miss, no Python), Python (24 of 25
   games; 1,727 calls), sp80 (built a fluid simulator, searched 16 versions of the physics,
   then placed 30 blocks in one plan), bp35 (world-model tier taken once, never fitted).
9. **It learned when to probe and when to commit** — "A single test act missed 37.1% of
   the time. A planned sequence missed 2.9%, about 13 times fewer, and Claude put 92% of
   its acts into plans." Counts: single tests "642 acts, 8% of the campaign"; planned
   "6,985 acts, 91% of the campaign". "On the first level of a game 29% of acts were
   single tests, and after that the rate falls away and stays down."
10. **The field** — comparison table (RHAE / actions): arc-skill (Claude Code, Opus 5)
    100.00 / 7,645; Tycho (Opus 5) 100.00 / 6,641; VISTA (Opus 5.0, Claude Code) 100.00 /
    7,542; Retrodict (gpt-5.6-sol, ThinHarness) 99.86 / 7,703; Schema (Opus 4.8, Fable 5)
    98.98 / 10,303; ewma_sv_v1.6 (gpt-5.6-sol, Codex) 98.97 / 8,347; Human Intelligence
    Harness (real humans) 95.35 / 14,798; Human median baseline n/a / 17,135. Cost note:
    "All 25 runs together cost $728.17 in tokens at list price, for 7,645 paid actions."
    VISTA and Schema scores are flagged as self-reported (no scorecard).
11. **Every run** — interactive replayer for all 25 games decoded from the recorded grids,
    plus a per-game table (game / levels / actions / % of human / predictions held);
    campaign row: 183 levels, 7,645 actions, 45% of human, 94.2% predictions held.
12. **Run it yourself** — `npx skills add pbshgthm/arc-skill`; works with Claude Code and
    Codex.
13. **Evidence** ("Everything the claim rests on") — the sessions (2,520 messages from
    Claude, 4,378 tool calls, 191 board images), run logs (3.1 MB), the skill (56 KB,
    "4,343 lines of command line tool … and the 900 lines of tests"), the replay script
    (12 KB) that re-sent all 7,645 acts to the live API on a competition card ("Every step
    is checked against the local run: game state, levels completed, frame count, and a
    sha256 over every frame"), and SKILL.md alone (6 KB). Caveat stated on the page:
    thinking blocks are not carried ("all 3,857 blocks in this archive are empty of text").
    Footer: "Every act was replayed against the live API on a competition card and verified
    by ARC on scorecard 24ddb219. 25 of 25 games reproduced, none diverged, in 66 minutes."

**Discrepancy log (honest record):**
- README.md:117 says "91.6% of all presses went into plans"; the site rounds to "92% of its
  acts into plans" (642 + 6,985 = 7,627 graded acts; 6,985/7,627 = 91.58%). Consistent.
- The site's "11,344 claims" counts semicolon-separated claim parts; README counts 7,627
  predictions (one per act). Different units, not a contradiction (STRONG INFERENCE from
  predictions.py's parts-vs-prediction structure).
- The clone's README states the repo layout includes no test directory; the site mentions
  "900 lines of tests" as part of its evidence bundle. No tests are present in the clone at
  commit dba53c3 (verified by file listing) — the tests evidently live in the site's
  archive, not this repo. UNVERIFIED beyond the site's statement.
