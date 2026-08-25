# _Archive — provenance

## 2025-10_AI_Tools_working_folder/

**What this is.** The entire contents of the former working folder `OneDrive\Documents\AI Tools\narrative-agents\` (59 content files, September–October 2025), **moved here unchanged on 2026-08-22** to end a split-brain: the canonical repo had lived at `GitHub\narrative-agents\` since early 2026 while this folder survived at the old location. Diffed before the move: no file with the same relative path differed; everything here is *additional* to the repo, not a competing version of it.

**Git hygiene.** `narrative-agents-repo\` inside it was an October 2025 clone of the same origin (single commit `da681b8`, already in the live repo's history). Its `.git` directory was renamed to `_dot_git_2025-10_neutralized` so the live repo does not see a nested repository. Nothing was deleted. **Add `_Archive/` to `.gitignore` before any `git add -A`** (the folder holds ~1.5 MB of `.docx` drafts and PNGs that do not belong in version control; OneDrive already backs them up).

**What is worth porting into the live repo (Stage 0 / ablation setup; port + test, do not copy blind — the October `core.py` predates `llm_core.py`):**

| In the archive | Why it matters | Suggested home |
|---|---|---|
| `narrative-agents-repo\examples\visualizations.py`, `memory_efficiency_viz.py`, `test_visualization.py`; `Vizualizations Matpotlib\*.md` | the paper's §5 figure pipeline (memory efficiency, character traits, coherence scatter, decision patterns); not in the live repo | `examples/` or `metrics/viz/` after porting against the current `core.py` |
| `old files\tests\test_narrative_agents.py` | the only unit-test file the project ever had | `tests/` (extend for the new selection rule) |
| `Medium Article\` (md + docx drafts from three models, four figures, benchmark PNG, social-media strategy, community playbook) | the popular counterpart of the paper ("We Are the Stories We Tell" / "Memory Is Story, Not Storage"); candidate Substack prelude material (Jan 2027 engine) | keep here; index in `STATE.md` and the Registry row; copy only the final `.md` + figures into `communications/` if/when published |
| `narrative-agents-project-instructions.md` | the October 2025 Claude Project instructions (historical; paths in it are stale) | keep here; superseded by `.claude/` + `STATE.md` |
| `strategic files and notes to be deleted\` (repo assessment, strategic analysis, visualization plan, session summary) | Michal's own label says "to be deleted"; preservation-first keeps them as the October 2025 decision record | keep here; never load |
| `Prompts.docx`, `desktop-commander-quick-reference.md` | convenience files | keep here |

**Rule for this folder:** read-only history. Nothing in `_Archive/` is canonical; if something here is needed, port it into the repo proper with a dated note.
