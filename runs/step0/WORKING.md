# WORKING — sb26, Level 2/8 (disposable, start fresh each level)

Paid actions: 60/60 used, segment ended exactly at cap. Level 2 STILL
NOT_FINISHED after 42 paid actions on it. Run `arc status` first on resume.

**L2 layout (7 colors, upper box=3 slots, lower box=4 slots, pipe between):**
Target (top row, L-to-R): c,f,8,9,e,b,6.
Upper slot centers (y=22): x=22,28,40. Lower slot centers (y=36): x=22,28,
34,40. Decorative pipe center x=34, y=17-31 (NOT a slot; click=noop, e52).

**Current slot contents (all 7 target colors present, order unresolved):**
U22=e, U28=9, U40=6, L22=c, L28=f, L34=8, L40=b.

**5 FALSIFIED full arrangements — submitted via ACTION5, each got
NOT_FINISHED. Tuple order = (U22,U28,U40,L22,L28,L34,L40). Do not retry:**
1. c,f,8,9,e,b,6 (e34) — upper-then-lower L-to-R
2. c,8,b,f,9,e,6 (e43) — column-major, upper-then-lower per column
3. f,9,b,c,8,e,6 (e48) — alternating, lower-first per position
4. f,9,6,c,8,e,b (e51) — column-major, lower-then-upper per column
5. e,9,6,c,f,8,b (e59) — upper=last3-of-target, lower=first4 (current state,
   after undoing one extra swap at e60)

**Immediate next steps:**
1. `status` + `view --grid` to reconfirm state matches above (re-derive if
   not — may have drifted).
2. Strongly consider `arc rules init` given 42 actions already spent + the
   harness's own nudge: model select/swap/submit, `replay` against all 60
   recorded events, `solve` to search the ~5040-permutation space instead of
   hand-guessing a 6th order theory.
3. If continuing manually, untested ideas: per-box order R-to-L (upper
   L-to-R + lower R-to-L, or vice versa); treat L34 (the pipe's touch-point)
   as entry-point-first within the lower box; or abandon "reading order"
   framing — treat the 7-slot assignment as an opaque bijection.
4. ACTION7 undo confirmed working (e60, cell-exact revert, no meter tick) —
   use it to back out one bad swap cheaply instead of re-selecting.
5. On LEVEL_COMPLETE, discard this file and rebuild fresh from the new
   board (colors/layout/box-count all change per level).
