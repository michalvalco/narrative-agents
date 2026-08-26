# Source notes — ARC-AGI Toolkit (`arc-agi`) and ARC-AGI-3 benchmarking harness

Phase-2 source documentation for the narrative-agents experiment. Claims are labeled
EXPLICIT (verbatim from the cited source), STRONG INFERENCE (directly entailed by quoted
material), or SPECULATIVE (flagged as such). Numeric and API-shaped content is quoted
verbatim.

## Citation block

All sources fetched **2026-08-26**.

1. **ARC-AGI Toolkit repository README** — https://github.com/arcprize/arc-agi
   (raw text fetched from https://raw.githubusercontent.com/arcprize/arc-agi/main/README.md,
   16,856 bytes). Status: ACQUIRED.
2. **ARC Prize documentation** — https://docs.arcprize.org (Mintlify site; individual pages
   fetched as Markdown). Pages used, all ACQUIRED:
   - https://docs.arcprize.org/toolkit/overview.md ("ARC-AGI Toolkit Quickstart")
   - https://docs.arcprize.org/toolkit/arc_agi.md ("Arcade — ARC-AGI 3 Client for Interactive Environments")
   - https://docs.arcprize.org/toolkit/competition_mode.md
   - https://docs.arcprize.org/recordings.md
   - https://docs.arcprize.org/scorecards.md
   - https://docs.arcprize.org/api-keys.md
   - https://docs.arcprize.org/local-vs-online.md
   - Index of all pages: https://docs.arcprize.org/llms.txt
3. **Benchmarking harness** — https://github.com/arcprize/arc-agi-3-benchmarking
   (README, `benchmarking/model_configs.yaml`, and `docs/add_anthropic_sdk.md` fetched raw
   from `raw.githubusercontent.com/.../main/...`). Status: ACQUIRED.

Toolkit version at access date (EXPLICIT): **0.9.9**, released 2026-06-10 (changelog,
arc-agi README and docs/toolkit/overview.md: "## [0.9.9] - 2026-06-10"). The arc-skill
harness pins exactly this version (`arc-agi==0.9.9`; see `Sources\arc-skill_notes.md`).
Install (EXPLICIT, toolkit quickstart): `uv add arc-agi` / `pip install arc-agi`.

What it is (EXPLICIT, arc-agi README, opening paragraph): "ARC-AGI Toolkit is an
open-sourced python interface (API) for ARC-AGI-3 interactive environments. It provides a
consistent API and tooling layer that lets agents interact with ARC-AGI-3 environments,
locally or via API."

---

## 1. `Arcade` constructor parameters

EXPLICIT — arc-agi README, "Constructor Parameters" table, quoted verbatim:

| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `arc_api_key` | `str` | `""` | `ARC_API_KEY` | API key for ARC API. If empty and not in offline mode, an anonymous key will be automatically fetched. |
| `arc_base_url` | `str` | `"https://three.arcprize.org"` | `ARC_BASE_URL` | Base URL for the ARC API. |
| `operation_mode` | `OperationMode` | `OperationMode.NORMAL` | `OPERATION_MODE` | `NORMAL` (local + API), `ONLINE` (API only), `OFFLINE` (local only), or `COMPETITON` (API only + [compeition scoring]). |
| `environments_dir` | `str` | `"environment_files"` | `ENVIRONMENTS_DIR` | Directory to scan for local `metadata.json` files. |
| `recordings_dir` | `str` | `"recordings"` | `RECORDINGS_DIR` | Directory to save game recordings (JSONL format). |
| `logger` | `logging.Logger` | `None` | - | Optional logger instance. If not provided, a default logger logging to STDOUT is created. |

(The typos "COMPETITON" / "compeition" are in the upstream README as fetched.) Preceding
sentence, EXPLICIT: "All parameters can be overridden by environment variables, with
constructor arguments taking precedence over environment variables." The docs page
toolkit/arc_agi.md carries the same six parameters and adds: "All parameters are optional."

> ⚠️ **Behavior caveat (2026-08-26 audit, against installed 0.9.9):** the quoted
> precedence rule has one exception in the actual code — `base.py:101-111` comments
> "Priority order for competition mode is different, the env var takes precedence over
> the constructor arg": `OPERATION_MODE=competition` in the environment overrides the
> constructor's `operation_mode`. The README is quoted faithfully above; the package
> behaves differently for this one parameter.

Key method, `make()` — EXPLICIT signature from both the README and toolkit/arc_agi.md:

```
make(game_id, seed=0, scorecard_id=None, save_recording=False, include_frame_data=True, render_mode=None, renderer=None)
```

- `game_id`: "Game identifier in format `'ls20'` or `'ls20-1234abcd'`. The first 4
  characters are the game_id, everything after `'-'` is the version."
- `scorecard_id`: "If `None` is provided (the default), the system will create and maintain
  a single default scorecard that is automatically reused across all `make()` calls."
- `save_recording`: "Whether to save recordings to JSONL file. Defaults to `False`."
- `include_frame_data`: (docs wording) "Whether local JSONL recordings include frame
  arrays. Defaults to `True` and has no effect unless `save_recording=True`."
- `render_mode`: `"human"`, `"terminal"`, `"terminal-fast"`; `renderer` is a
  `Callable[[int, FrameDataRaw], None]` and "takes precedence" if both are given.
- Returns "`EnvironmentWrapper` or `None`".

The environment surface used by arc-skill (EXPLICIT, README `EnvironmentWrapper` section):
properties `observation_space` (last `FrameDataRaw`), `action_space`
(`list[GameAction]`), `info` (`EnvironmentInfo`: `game_id`, `title`, `tags`); methods
`reset()` and `step(action, data=None, reasoning=None)` where `data` carries `{"x","y"}`
for complex actions and `reasoning` is an "Optional reasoning dictionary to include in
recordings." (arc-skill passes its `--predict`/`--because` text through this `reasoning`
parameter — STRONG INFERENCE from `vendor/arc-skill/.../broker.py` `session.step(...,
reasoning=reasoning)` plus this doc.)

There is also `listen_and_serve` (EXPLICIT, README): "Start a blocking Flask server that
exposes the REST API" — parameters include `host="0.0.0.0"`, `port=8001`,
`competition_mode=False`, `save_all_recordings=False`, `include_frame_data=True`,
`scorecard_timeout`, `on_scorecard_close`, `extra_api_routes`, `renderer`.

---

## 2. `OperationMode` values and what each permits

EXPLICIT — docs toolkit/arc_agi.md, `operation_mode` table, verbatim:

| Mode                        | Description                                                         |
| --------------------------- | ------------------------------------------------------------------- |
| `OperationMode.NORMAL`      | Load both local and remote games (default)                          |
| `OperationMode.OFFLINE`     | Load local games only — fast, no rate limits                        |
| `OperationMode.ONLINE`      | Load remote games only — enables online scorecards and replays      |
| `OperationMode.COMPETITION` | Load remote games only and enforce competition scoring restrictions |

Settable via `export OPERATION_MODE=OFFLINE` (EXPLICIT). Local vs online trade-offs
(EXPLICIT, docs local-vs-online.md): Local — "~2,000 FPS (120,000 frames per minute)",
"No rate limits", "Run as many instances as you want", "No API key required"; limitations
"No online scorecards", "No shareable replays". Online — "View scorecards online",
"Shareable replays", "Results appear on leaderboard"; limitations "Anonymous access
includes fewer games", "Capped at 600 requests per minute".

**COMPETITION restrictions** (EXPLICIT, docs toolkit/competition_mode.md, verbatim list;
identical list in the arc-agi README "Competition Mode" section):

> This mode is **REQUIRED** to show up on the Unverified leaderboard and forces the
> following behavior.
> * Environments must be interacted with via the API
> * Scoring is against all available environments, even if you choose not to interact with them
> * Only *Level Resets* are permitted, *Game Resets* are not allowed and become *Level Resets*
> * Can only interact (call `make`) a single time for each environment
> * Can only open a single Scorecard
> * Cannot get scoring of an inflight scorecard, `get_scorecard` does not work
>
> **Note:** The Kaggle Competition is forced into this mode.

Relevant changelog entries (EXPLICIT): 0.9.3 added "`OperationMode.COMPETITION`" and
official scoring ("The average for an individual game is now weighted by the level index
(1-indexed)"; "Score for an individual level is now squared. A score of `0.5` now becomes
`0.25`"); 0.9.7 "Increased the per-level score cap from 100% to 115% and capped each game
by the weighted maximum for its completed levels"; 0.9.8 fixed "Full game resets occurring
in competition mode".

---

## 3. JSONL recording format

EXPLICIT — docs recordings.md. Availability table: API — "Yes — viewable online via
scorecard"; Benchmarking harness — "Yes — saved locally and viewable online"; Python
Toolkit — "Optional — set `save_recording=True` when calling `make()`".

File layout (verbatim): `recordings/<scorecard_id>/<game_id>-<guid>.jsonl`

"Recordings are stored in JSONL format with timestamped entries" — example lines quoted
verbatim from the docs:

```json
{"timestamp": "2026-07-22T10:30:45.123456+00:00", "data": {"game_id": "ls20-016295f7601e", "state": "NOT_FINISHED", "levels_completed": 0, "win_levels": 7, "action_input": {"id": "RESET", "data": {}, "reasoning": null}, "guid": "...", "full_reset": true, "available_actions": [1, 2, 3, 4, 6], "frame": [...]}}
{"timestamp": "2026-07-22T10:30:46.234567+00:00", "data": {"game_id": "ls20-016295f7601e", "state": "NOT_FINISHED", "levels_completed": 0, "win_levels": 7, "action_input": {"id": "ACTION1", "data": {}, "reasoning": {"thought": "move up"}}, "guid": "...", "full_reset": false, "available_actions": [1, 2, 3, 4, 6], "frame": [...]}}
```

STRONG INFERENCE (field inventory read off those examples — the docs give no separate
schema table): each line = `{"timestamp": <ISO-8601 UTC>, "data": {...}}` where `data`
carries `game_id` (with version suffix), `state` (e.g. `NOT_FINISHED`), `levels_completed`,
`win_levels`, `action_input` (`{"id": <action name>, "data": {...}, "reasoning": <dict or
null>}`), `guid`, `full_reset` (bool), `available_actions` (list of ints), `frame` (nested
frame arrays). "Set `include_frame_data=False` to omit frame arrays and reduce file size."
(EXPLICIT). The docs add: "The benchmarking harness also writes run recordings, model
responses, token usage, and per-step records beneath `recordings/`." (EXPLICIT).

Note: the `reasoning` dict inside `action_input` is the hook arc-skill uses to embed its
`--predict` / `--because` text into the official recording stream (STRONG INFERENCE; see
§1 above and `vendor/arc-skill/.../broker.py`).

---

## 4. Scorecard semantics

EXPLICIT — docs scorecards.md: "Scorecards aggregate the results from your agent's game
performance." Viewable online at `https://arcprize.org/scorecards` and
`https://arcprize.org/scorecards/<scorecard_id>` for API runs.

Scorecard fields table (EXPLICIT, verbatim):

| Field | Description |
| --- | --- |
| `card_id` | Unique scorecard ID |
| `score` | Average of the best score for each environment |
| `environments` | Per-environment runs, scores, action counts, completed levels, and reset counts |
| `tags_scores` | Aggregate results grouped by game metadata tags |
| `total_environments_completed` | Number of environments with a winning run |
| `total_levels_completed` | Levels completed across the best environment runs |
| `total_actions` | Actions taken across all recorded runs |
| `tags` | Labels used to categorize and filter scorecards (e.g., `["experiment1", "v2.0", "test"]`) |
| `source_url` | Optional source or provenance URL |
| `opaque` | Optional JSON-serializable metadata |
| `competition_mode` | Whether competition restrictions apply to the scorecard |

Lifecycle (EXPLICIT, toolkit/arc_agi.md): `create_scorecard(source_url=None, tags=None,
opaque=None)` returns the new scorecard ID ("Online scorecards default to `["wrapper"]`;
local scorecards leave tags unset"); `open_scorecard()` is an alias; `get_scorecard()` /
`close_scorecard()` with `scorecard_id=None` operate on the automatically maintained
default scorecard, and "After closing, the default scorecard is cleared and a new one will
be created on the next `make()` call."

Operational notes (EXPLICIT, scorecards.md "Notes"): "Scorecards auto close after 15
minutes"; "Agent scorecards are automatically added to the leaderboard in batch every ~15
minutes"; "Stopping the program prematurely with Ctrl-C mid-run will not allow you to see
the scorecard results." Sharing: "Scorecards are not public, however you can share replays
from scorecards created via the API with others. Local scorecards cannot be shared."

Scoring math (EXPLICIT, changelog, versions 0.9.3 and 0.9.7 — see §2). SPECULATIVE: the
"RHAE" name used by arc-skill's write-up for the 0-100 score is not used anywhere in these
toolkit docs/README; the mapping of `score` to "RHAE" rests on the arc-skill site's own
gloss ("RHAE is the benchmark's own score. It compares your actions against a median human
player, level by level, and it stops at 100.00").

---

## 5. Anonymous key vs registered key

- EXPLICIT (arc-agi README, Prerequisites): "You can optionally set the `ARC_API_KEY`
  environment variable with your API key. If no key is provided, an anonymous key will be
  used. However, registering for an API key will give you access to more games at release.
  [Register for an API key at https://three.arcprize.org]". Constructor doc: "If empty and
  not in offline mode, an anonymous key will be automatically fetched."
- EXPLICIT (docs api-keys.md): registering allows you to "**Track your progress** across
  games and sessions" and "**Access the full list of games** when launch goes out";
  "Registered keys provide access to the full set of public games available on the
  platform." Keys are created at arcprize.org/platform (login via Google or GitHub, user
  profile → API Keys) and assigned to `ARC_API_KEY` in the environment or a `.env` file
  (the toolkit auto-loads it, python-dotenv).
- EXPLICIT (docs local-vs-online.md): "If `ARC_API_KEY` is unset, the Toolkit fetches an
  anonymous key automatically. Register for an API key to access additional games." Online
  limitation: "Anonymous access includes fewer games". Local/OFFLINE play needs no key at
  all ("No API key required").
- STRONG INFERENCE: an anonymous key suffices to play the anonymously-available games
  online and to appear in scorecard flows, but the registered key is required for the full
  25-game public set — consistent with the benchmarking README instruction to "Get an API
  key from the Arc Prize Website" before its 25 games are all listable.

---

## 6. Anthropic provider configuration in `arc-agi-3-benchmarking`

Repo: https://github.com/arcprize/arc-agi-3-benchmarking (MIT). Quickstart (EXPLICIT,
README): clone; `uv venv`; `uv sync`; `cp .env.example .env`; set
`ARC_API_KEY=your_api_key_here`; run `uv run main.py --game=ls20`. Discovery commands:
`uv run main.py --list-games` ("there should be 25") and `uv run main.py --list-configs`.

Provider key (EXPLICIT, README): `ANTHROPIC_API_KEY=your_anthropic_key_here` in `.env`
(alongside OPENAI/GOOGLE/XAI/GROK/DEEPSEEK/GROQ/OPENROUTER/FIREWORKS keys).

README invocation examples (EXPLICIT): "Native Anthropic configs are also available:"

```bash
uv run main.py --game=ls20 --config=anthropic-opus-4-7-low
uv run main.py --game=ls20 --config=anthropic-opus-4-7-low-thinking
```

The actual config store is `benchmarking/model_configs.yaml`. Its two Anthropic entries as
of 2026-08-26, quoted verbatim:

```yaml
- id: "anthropic-opus-4-7-medium"
  agent:
    MAX_ACTIONS_BASELINE_MULTIPLIER: 5.0
    MAX_CONTEXT_LENGTH: 175_000
  runtime:
    sdk: "anthropic-python"
    api: "messages"
    state: "manual_rolling"
  client:
    api_key_env: "ANTHROPIC_API_KEY"
  request:
    model: "claude-opus-4-7"
    max_tokens: 120000
    stream: true
    thinking:
      type: "adaptive"
    output_config:
      effort: "medium"
  pricing:
    input: 5.00
    output: 25.00

- id: "anthropic-opus-4-7-low-thinking"
  agent:
    MAX_ACTIONS_BASELINE_MULTIPLIER: 5.0
    MAX_CONTEXT_LENGTH: 175_000
  runtime:
    sdk: "anthropic-python"
    api: "messages"
    state: "manual_rolling"
  client:
    api_key_env: "ANTHROPIC_API_KEY"
  request:
    model: "claude-opus-4-7"
    max_tokens: 128_000
    thinking:
      type: "adaptive"
    output_config:
      effort: "low"
  pricing:
    input: 5.00
    output: 25.00
```

So the Anthropic provider runs through the **native Anthropic Python SDK Messages API**
(`sdk: "anthropic-python"`, `api: "messages"`), model `claude-opus-4-7`, with adaptive
thinking (`thinking: {type: "adaptive"}`) and an `output_config.effort` knob, keyed by the
`ANTHROPIC_API_KEY` env var, agent-side rolling context (`state: "manual_rolling"`,
`MAX_CONTEXT_LENGTH: 175_000`), and pricing metadata $5.00 / $25.00 per Mtok in/out
(STRONG INFERENCE on the pricing units; the YAML gives bare numbers under `pricing:
input/output` and the design doc treats them as list-price accounting).

**Discrepancy (honest record):** the README's first example names a config id
`anthropic-opus-4-7-low`, which does NOT exist in `model_configs.yaml` at access date —
the YAML has `anthropic-opus-4-7-medium` and `anthropic-opus-4-7-low-thinking`. The design
document `docs/add_anthropic_sdk.md` ("Native Anthropic SDK Plan") shows
`anthropic-opus-4-7-low` as the originally proposed/implemented id ("- [x] Use the existing
ID `anthropic-opus-4-7-low`.") with `max_tokens: 20_000` in its "Proposed Config Shape";
STRONG INFERENCE: the id was later renamed/split into the two current entries and the
README example is stale. The same doc fixes the supported runtime pairs verbatim:

```text
("openai-python", "chat_completions")
("openai-python", "responses")
("anthropic-python", "messages")
```

and notes "Native Anthropic configs should not use `extra_body`." plus the native request
mapping `model="claude-opus-4-7", thinking={"type": "adaptive"},
output_config={"effort": "low"}`.

Scorecard integration (EXPLICIT, README): "When you run a benchmark, a scorecard is saved
on the ARC server. If you are logged in, you can browse your saved scorecards at
arcprize.org/scorecards."

---

## 7. Per-source status summary

| Source | Status | Notes |
| --- | --- | --- |
| github.com/arcprize/arc-agi README | ACQUIRED | raw README fetched in full, 2026-08-26 |
| docs.arcprize.org quickstart (toolkit/overview) | ACQUIRED | fetched as .md, includes changelog through 0.9.9 |
| docs.arcprize.org toolkit/arc_agi, competition_mode, recordings, scorecards, api-keys, local-vs-online | ACQUIRED | fetched as .md, 2026-08-26 |
| github.com/arcprize/arc-agi-3-benchmarking README | ACQUIRED | raw README fetched in full |
| benchmarking/model_configs.yaml | ACQUIRED | full file fetched; Anthropic entries quoted verbatim |
| docs/add_anthropic_sdk.md | ACQUIRED (partial read) | headers + config-shape sections read; 21,311 bytes total |

Nothing in this file is UNVERIFIABLE; the one SPECULATIVE item is the RHAE naming gloss in
§4, and the one stale-documentation discrepancy is recorded in §6.
