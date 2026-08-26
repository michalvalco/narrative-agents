# GUIDE — sb26 (durable, revise freely)

**Game type:** color-sort puzzle. Top row = N framed buttons (READ-ONLY,
target order L-to-R). Bottom row = N scrambled swatches. Middle "box(es)"
hold N slots total. Goal: slot colors, read in the TRUE order, equal top-row
order, then submit.

**Controls:** only ACTION5 (submit, no coords) and ACTION6 (click x,y) act
on state. ACTION1-4 error "unavailable". **ACTION7=undo IS FUNCTIONAL**
(verified e60): reverts the immediately-preceding action exactly, cell-exact,
does NOT tick the meter. Cheaper than re-select+re-swap to fix one mistake.

**Interaction model (solid for single-box: L1 e5-e19, 30/35 predictions ✓
overall):**
- ACTION6 on a bottom swatch OR filled slot = SELECT (black ring, no color
  change). ACTION6 on a 2nd object while one selected = SWAP contents. Only
  way content moves. Top buttons never react to clicks. Click with nothing
  selected = no-op.
- Win (single box, confirmed L1 e19): slots L-to-R == top-row L-to-R ->
  ACTION5 -> LEVEL_COMPLETE.
- Meter (row53, full width) is COSMETIC only: +1 per swap/place AND per
  ACTION5 press (right or wrong), resets to 0 only on actual
  LEVEL_COMPLETE. Never blocks anything — ignore it.

**UNSOLVED — multi-box levels (L2: 2 boxes joined by a decorative pipe):**
"slots read in some fixed order == target order" FAILED 5x on L2 despite
placing the exact right SET of colors each time (see WORKING.md for the 5
falsified 7-tuples). Ruled out: upper-then-lower L-to-R; column-major
(up-then-down per column); column-major (down-then-up per column);
alternating box per position; upper=last-3-of-target/lower=first-4. Pipe
itself is decorative (click=noop, e52): renders as hollow outline, visually
distinct from a real empty slot (solid "22" 2x2 block). Harness nudged at 42
actions/level: "write rules.py, verify replay, then solve" — next context
should try the rules tier (`arc rules help/init/replay/solve`) instead of
more manual guesses, or question whether "reading order" is even the right
frame for >1 box (maybe per-slot identity is a hidden bijection, not
derivable from the legend sequence by any geometric rule).

**Per-level recipe:** `view --grid` -> regex '2+' runs on slot rows for
centers, non-bg runs on button/swatch rows for centers+order -> single-box:
batch (select swatch_i; place at slot i in target order) then ACTION5.
Multi-box: do NOT assume an order guess is likely right; cap manual guesses
at ~2-3 submits then escalate to rules.py.
