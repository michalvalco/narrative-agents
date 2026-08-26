# Notes — sb26

## Verified (cite event ids)
- Only ACTION5/6/7 public (ACTION1-4 errors as unavailable).
- ACTION6 on a bottom-row color swatch selects it (adds black ring, +margin1 box). e5.
- ACTION6 on a selected swatch/slot target SWAPS the two objects (positions exchange). e6,e8,e10,e12,e14,e16,e18.
- Middle box = 4 slots to arrange; goal = match the TOP ROW color order exactly, then press ACTION5 (interact, no coords) to submit -> LEVEL_COMPLETE. e19.
- Clicking top-row buttons themselves does nothing (e1,e2) - they are the read-only target pattern.
- Clicking an unselected middle slot directly (no prior selection) also did nothing (e3) - must select a swatch/slot FIRST, then click destination.
- A red/green meter (row53, full board width) ticks +1 per real placement/swap action; cosmetic progress indicator only, not a hard limit observed yet.
- Level completion swaps in a whole new board (new colors appear e.g. c,6,8) - re-verify layout per level.

## Assumed / open questions
- Unknown if meter reaching 0 (red) causes failure - never got close.
- Unknown if slots-count / colors-count varies per level (L2 shows more colors: 8,c,6 added).
- Unknown exact selection-ring pixel formula per object size - derive fresh from a DIFF each level rather than assuming.

## Plan
- L2: read new top-row order + how many slots/colors, verify swap mechanic still holds with 1 test click, then batch swaps to sort, then ACTION5 submit.
