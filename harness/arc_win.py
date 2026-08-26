"""
Windows shim for the vendor arc CLI - the vendor clone stays pristine.

arc_cli.py calls os.getuid() (absent on Windows) in exactly two places,
both only to name per-user temp paths (broker.py:115, core.py:82), so a
constant is safe on a single-user machine. The bash launcher also breaks
on Windows venv layout (bin/ vs Scripts/); this shim replaces it: the
repo .venv already satisfies the launcher's dependency fingerprint
(arc-agi==0.9.9, numpy 2.x, pillow 12.x, Python >= 3.12).

Usage: .venv/Scripts/python.exe harness/arc_win.py start sb26 ...
"""

import os
import runpy
import sys

if not hasattr(os, "getuid"):
    os.getuid = lambda: 0  # type: ignore[attr-defined]

_SCRIPTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "vendor", "arc-skill", "skills", "arc-skill", "scripts",
)
_CLI = os.path.join(_SCRIPTS, "arc_cli.py")

sys.path.insert(0, _SCRIPTS)  # arc_cli.py imports the arc_skill package beside it
# arc_cli exits via SystemExit itself; run_path returns a globals dict on any
# other path, which must not become the process exit status.
runpy.run_path(_CLI, run_name="__main__")
