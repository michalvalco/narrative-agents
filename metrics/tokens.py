"""
Offline token counting for note caps and note-token metrics.

One implementation for the whole repo (compaction prompts, metrics,
run_step0) so the cap can never drift between enforcer and reporter.

Approximation: ceil(len(text) / 4) — the standard ~4-chars-per-token
heuristic for English prose. It is deliberately offline (no API, no
tokenizer download). Step 0's cost.jsonl exists precisely to calibrate
this number against real API usage; until then treat counts as ±15%.
"""


def count_tokens(text: str) -> int:
    """Approximate token count of `text` (offline heuristic, see module doc)."""
    return -(-len(text) // 4)


def within_cap(text: str, cap: int = 1200) -> bool:
    """True if `text` fits the note budget."""
    return count_tokens(text) <= cap
