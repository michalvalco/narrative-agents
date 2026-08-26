"""
Step 0 — the cost-measurement run (Experiment_Spec.md §4).

One game (sb26), arm B, one seed, forced compaction every 30 turns, note
cap 1,200 tokens, token accounting per action to runs/step0/cost.jsonl.
Its number (tokens per action / per compaction, with prompt caching on the
skill text) x 24 cells prices the pilot; Michal sets the budget ceiling
AFTER that number exists.

Two modes:

  --dry-run   Validates config, paths, skill text, compaction trigger, the
              cost writer, and the offline toolkit path — zero network,
              zero model calls, zero ARC requests (Gotchas #276: the
              no-side-effect path exists BEFORE the live path). Prints the
              exact live command without executing it.

  --live      GATED. Step 0 spends model tokens and ARC API requests, which
              is a Yellow-zone action pending Michal's explicit go
              (Experiment_Spec.md §8, decisions 1-3: approval, budget
              ceiling, model tier). This flag therefore refuses and prints
              the launch instructions. The live run is driven by a Claude
              Code session playing through harness/arm_B/SKILL.md - not by
              this script - because the arm skill IS the agent loop; this
              script owns config, validation, and cost accounting.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "game_id": "sb26",          # 8 levels, cheapest of the core four
    "arm": "B",
    "seed": 1,
    "compact_every": 30,        # forced compaction period, in turns
    "note_cap_tokens": 1200,
    "model": "claude-sonnet-5",  # ruled 2026-08-26 (Spec §8.3); fallback claude-haiku-4-5
    "budget_usd": 50,            # ceiling ruled 2026-08-26 (Spec §8.2)
    "approved": "2026-08-26",    # Step 0 approved by Michal (Spec §8.1)
    "run_dir": os.path.join(REPO, "runs", "step0"),
    "skill": os.path.join(REPO, "harness", "arm_B", "SKILL.md"),
    "compaction_prompt": os.path.join(REPO, "compaction", "B_task_model.md"),
    "arc_launcher": os.path.join(
        REPO, "vendor", "arc-skill", "skills", "arc-skill", "scripts", "arc"
    ),
}

LIVE_COMMAND = (
    'cd "{run_dir}" && claude -p "Play ARC-AGI-3 game {game_id} (seed {seed}). '
    'Read and follow {skill} completely before starting. Forced compaction '
    'every {compact_every} turns per {compaction_prompt}; note cap '
    '{note_cap_tokens} tokens." --model <tier-per-Spec-§8.3>'
)


def compaction_turns(total_turns: int, every: int) -> list:
    """The turns at which a forced handoff fires (pure; unit-tested)."""
    return list(range(every, total_turns + 1, every))


def write_cost_record(path: str, record: dict) -> None:
    """Append one per-action accounting line to cost.jsonl."""
    required = {"turn", "input_tokens", "output_tokens",
                "cache_read_tokens", "cache_write_tokens"}
    missing = required - record.keys()
    if missing:
        raise ValueError(f"cost record missing fields: {sorted(missing)}")
    line = dict(record)
    line["recorded_at"] = datetime.now(timezone.utc).isoformat()
    with open(path, "a", encoding="utf-8") as f:
        json.dump(line, f)
        f.write("\n")


def dry_run() -> int:
    """Exercise the whole configuration path with zero side effects."""
    sys.path.insert(0, REPO)
    from metrics.tokens import count_tokens, within_cap

    checks = []

    def check(name, ok, detail=""):
        checks.append((name, ok, detail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))

    print("Step 0 dry run (no network, no model calls, no ARC requests)\n")

    # 1. Files the live run needs
    for key in ("skill", "compaction_prompt", "arc_launcher"):
        check(f"{key} exists", os.path.isfile(CONFIG[key]), CONFIG[key])

    # 2. The skill carries the compaction instruction
    with open(CONFIG["skill"], encoding="utf-8") as f:
        skill_text = f.read()
    check("skill names the compaction prompt",
          "B_task_model.md" in skill_text and "30" in skill_text)
    check("skill text within a cacheable size",
          0 < count_tokens(skill_text) < 8000,
          f"~{count_tokens(skill_text)} tokens (prompt-cached in live run)")

    # 3. Compaction prompt states the cap; counter agrees a small note fits
    with open(CONFIG["compaction_prompt"], encoding="utf-8") as f:
        comp_text = f.read()
    check("compaction prompt states the 1,200-token cap", "1,200" in comp_text)
    check("token counter enforces the cap",
          within_cap("x" * 4000, CONFIG["note_cap_tokens"])
          and not within_cap("x" * 5000, CONFIG["note_cap_tokens"]))

    # 4. Compaction trigger schedule
    check("compaction trigger fires at 30/60/90 over a 100-turn run",
          compaction_turns(100, CONFIG["compact_every"]) == [30, 60, 90])

    # 5. Run dir + cost writer round-trip
    os.makedirs(CONFIG["run_dir"], exist_ok=True)
    probe = os.path.join(CONFIG["run_dir"], "cost.dryrun.jsonl")
    if os.path.exists(probe):
        os.remove(probe)
    write_cost_record(probe, {
        "turn": 1, "input_tokens": 1000, "output_tokens": 50,
        "cache_read_tokens": 900, "cache_write_tokens": 0,
    })
    with open(probe, encoding="utf-8") as f:
        rec = json.loads(f.read().strip())
    check("cost.jsonl writer round-trips",
          rec["turn"] == 1 and "recorded_at" in rec, probe)

    # 6. Toolkit importable and offline-instantiable, no key, no network
    try:
        import socket
        real_connect = socket.socket.connect

        def _blocked(*a, **k):
            raise RuntimeError("network blocked in dry run")
        socket.socket.connect = _blocked
        try:
            from arc_agi import Arcade, OperationMode
            Arcade(arc_api_key=None,
                   operation_mode=OperationMode.OFFLINE,
                   recordings_dir=CONFIG["run_dir"])
            check("arc-agi offline instantiation (no key, network blocked)", True)
        finally:
            socket.socket.connect = real_connect
    except Exception as exc:  # report, don't crash the report
        check("arc-agi offline instantiation", False, repr(exc))

    failed = [c for c in checks if not c[1]]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed.")
    print("\nLive command (NOT executed; gated on Experiment_Spec §8 decisions 1-3):")
    print("  " + LIVE_COMMAND.format(**CONFIG))
    return 1 if failed else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)

    if args.live:
        print("REFUSED: this script does not drive the model itself.")
        print("Step 0 is approved (2026-08-26, ceiling $50, model "
              f"{CONFIG['model']}), but the vendor harness is POSIX-only, so")
        print("the live run goes through WSL2 as segmented Claude Code agent "
              "sessions (30 paid actions per segment = one forced handoff);")
        print("this script owns config, validation, and cost accounting only.")
        print("Reference command shape:")
        print("  " + LIVE_COMMAND.format(**CONFIG))
        return 2

    return dry_run()


if __name__ == "__main__":
    sys.exit(main())
