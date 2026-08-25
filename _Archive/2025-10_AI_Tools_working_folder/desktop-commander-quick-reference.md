# Desktop Commander Quick Reference

*A practical guide for power users*

---

## Core Principles

1. **Always use absolute paths** for reliability (unless explicitly working with relative paths)
2. **DC can't access the web** - use it for local files and processes only
3. **For local file analysis (CSV, JSON, logs)** - ALWAYS use DC, NEVER use analysis tool
4. **Chunk large writes** - Keep file writes to ~25-30 lines per operation
5. **Use processes for data work** - Start Python/Node REPLs for interactive analysis

---

## File Operations

### Reading Files

```
read_file(path, offset=0, length=1000)
```

**Best for:** Viewing file contents, checking code, reading documentation

**Examples:**
- First 50 lines: `offset=0, length=50`
- Last 20 lines: `offset=-20` (tail behavior)
- Lines 100-150: `offset=100, length=50`

**Pro tip:** Can read from URLs when `isUrl=true`

### Reading Multiple Files

```
read_multiple_files(paths=[list of paths])
```

**Best for:** Comparing files, batch reading, analyzing related files

**Example:**
```python
paths = [
    "C:/project/src/main.py",
    "C:/project/src/utils.py",
    "C:/project/tests/test_main.py"
]
```

### Writing Files

```
write_file(content, path, mode='rewrite')
```

**Modes:**
- `rewrite` - Replace entire file
- `append` - Add to end of file

**CRITICAL WORKFLOW:**
```
1. First chunk → write_file(chunk1, path, mode='rewrite')
2. Next chunks → write_file(chunk2, path, mode='append')
3. Continue → write_file(chunk3, path, mode='append')
```

**Always chunk files >25-30 lines for best performance**

### Editing Files (Surgical Changes)

```
edit_block(file_path, old_string, new_string, expected_replacements=1)
```

**Best for:** Precise edits without rewriting entire files

**Best practice:**
- Include minimal context (1-3 lines) around the change
- Match exact whitespace and indentation
- Make multiple small edits rather than one large edit

**Example:**
```python
# Change one function
old_string = """def calculate(x):
    return x * 2"""

new_string = """def calculate(x, multiplier=2):
    return x * multiplier"""
```

### File Info

```
get_file_info(path)
```

**Returns:** size, creation time, modified time, permissions, lineCount, lastLine

**Best for:** Checking file stats before operations, verifying file exists

---

## Directory Operations

### List Directory

```
list_directory(path)
```

**Returns:** Files and directories with [FILE] and [DIR] prefixes

**Best for:** Exploring project structure, finding files

### Create Directory

```
create_directory(path)
```

**Creates nested directories if needed**

### Move/Rename

```
move_file(source, destination)
```

**Use cases:** Renaming files, reorganizing projects

---

## Search Operations

### Start Search (Streaming)

```
start_search(path, pattern, searchType='files', literalSearch=false)
```

**Search Types:**
- `searchType='files'` - Search by filename
- `searchType='content'` - Search inside files

**When to Use Each:**

**Use `searchType='files'` when:**
- Looking for specific files: "find package.json"
- Pattern is a filename: "*.js", "README.md"
- Finding by extension: "all TypeScript files"

**Use `searchType='content'` when:**
- Looking for code/logic: "authentication logic"
- Finding functions/variables: "getUserData function"
- Searching text: "TODO comments"
- Code patterns: "console.log statements"

**Literal Search:**
Use `literalSearch=true` for code with special characters:
- Function calls: `getUserData()`
- Array access: `data[0]`
- Regex special chars: `.`, `*`, `+`, `?`, `^`, `$`, etc.

**Parameters:**
- `pattern` - What to search for (1-6 words for best results)
- `filePattern` - Filter by file type (e.g., "*.js|*.ts")
- `ignoreCase` - Default true
- `maxResults` - Limit results
- `earlyTermination` - Stop when exact match found

**Example:**
```python
# Find all Python files with "TODO" comments
start_search(
    path="/project",
    pattern="TODO",
    searchType="content",
    filePattern="*.py"
)
```

### Get More Results

```
get_more_search_results(sessionId, offset=0, length=100)
```

**Pagination examples:**
- First 100: `offset=0, length=100`
- Next 100: `offset=100, length=100`
- Last 20: `offset=-20`

### Stop Search

```
stop_search(sessionId)
```

**Use when:** Found what you need or search taking too long

### List Active Searches

```
list_searches()
```

---

## Process Management (CRITICAL FOR DATA ANALYSIS)

### Start Process

```
start_process(command, timeout_ms=30000, shell=None)
```

**Common patterns:**

**Python REPL (RECOMMENDED for data analysis):**
```python
start_process("python3 -i", timeout_ms=5000)
```

**Node.js REPL:**
```python
start_process("node -i", timeout_ms=5000)
```

**Shell:**
```python
start_process("bash", timeout_ms=5000)
```

**CRITICAL:** For ANY local file analysis (CSV, JSON, data processing), ALWAYS use processes.

### Interact with Process

```
interact_with_process(pid, input, timeout_ms=8000, wait_for_prompt=true)
```

**REQUIRED WORKFLOW FOR FILE ANALYSIS:**

```python
# 1. Start Python REPL
pid = start_process("python3 -i")

# 2. Load libraries
interact_with_process(pid, "import pandas as pd, numpy as np")

# 3. Read file
interact_with_process(pid, "df = pd.read_csv('/absolute/path/file.csv')")

# 4. Analyze
interact_with_process(pid, "print(df.describe())")

# 5. Continue analysis
interact_with_process(pid, "df.groupby('column').size()")
```

**Smart Detection:**
- Automatically waits for REPL prompt (>>>, >, $)
- Detects errors and completion
- Early exit prevents timeouts

### Read Process Output

```
read_process_output(pid, timeout_ms=5000)
```

**Use when:** Process is running and you want to check output without sending input

### Force Terminate

```
force_terminate(pid)
```

### List Sessions

```
list_sessions()
```

**Shows:** PID, blocked status, runtime

**Debugging tip:** "Blocked: true" often means REPL waiting for input

---

## Common Workflows

### Workflow 1: Analyze a CSV File

```python
# Start Python REPL
start_process("python3 -i")

# Load and analyze
interact_with_process(pid, """
import pandas as pd
df = pd.read_csv('/path/to/data.csv')
print(df.head())
print(df.describe())
print(df.info())
""")
```

### Workflow 2: Search and Edit Code

```python
# 1. Find files with pattern
start_search(
    path="/project/src",
    pattern="deprecated function",
    searchType="content",
    filePattern="*.py"
)

# 2. Get results
results = get_more_search_results(sessionId)

# 3. Edit each file
edit_block(
    file_path=result_path,
    old_string="old_function()",
    new_string="new_function()"
)
```

### Workflow 3: Build Project Documentation

```python
# 1. Read all source files
paths = [list of source files]
read_multiple_files(paths)

# 2. Create documentation
write_file(
    content=doc_chunk1,
    path="/project/docs/api.md",
    mode="rewrite"
)

# 3. Append more sections
write_file(
    content=doc_chunk2,
    path="/project/docs/api.md",
    mode="append"
)
```

### Workflow 4: Analyze Repository Structure

```python
# 1. List top-level
list_directory("/project")

# 2. Search for specific files
start_search(
    path="/project",
    pattern="config",
    searchType="files"
)

# 3. Read key files
read_multiple_files([
    "/project/package.json",
    "/project/README.md",
    "/project/.gitignore"
])
```

### Workflow 5: Data Processing Pipeline

```python
# 1. Start Python REPL
pid = start_process("python3 -i")

# 2. Load data
interact_with_process(pid, """
import pandas as pd
import json

# Read CSV
df = pd.read_csv('/data/input.csv')

# Process
df_clean = df.dropna()
df_clean['new_col'] = df_clean['old_col'] * 2

# Save
df_clean.to_csv('/data/output.csv', index=False)
print(f'Processed {len(df_clean)} rows')
""")
```

---

## Best Practices

### DO:
✅ Use absolute paths: `C:/Users/name/project/file.py`
✅ Chunk large writes (25-30 lines per write)
✅ Use processes for data analysis (CSV, JSON, logs)
✅ Make multiple small edits vs. one large edit
✅ Search with concise patterns (1-6 words)
✅ Use `literalSearch=true` for code with special characters

### DON'T:
❌ Use relative paths unless explicitly needed
❌ Write files >50 lines in one operation
❌ Use analysis tool for local file access (it WILL FAIL)
❌ Repeat similar search queries
❌ Use '-' operator or 'site:' in searches
❌ Forget to terminate long-running processes

---

## Troubleshooting

**Problem: "File not found"**
→ Check absolute path, verify file exists with `get_file_info`

**Problem: "Process blocked/hanging"**
→ Use `list_sessions` to check status, may be waiting for input

**Problem: "Search returns no results"**
→ Try broader pattern, check searchType (files vs. content)

**Problem: "Edit fails - not found"**
→ Check exact whitespace/indentation, use `literalSearch=true` if pattern has special chars

**Problem: "Data analysis not working"**
→ Make sure you're using `start_process` + `interact_with_process`, NOT analysis tool

**Problem: "Write operation slow"**
→ Chunk into smaller pieces (≤30 lines each)

---

## Power User Tips

1. **Parallel searches:** Run file search AND content search simultaneously for ambiguous queries
2. **REPL debugging:** Use `list_sessions` to verify REPL is ready before sending commands
3. **Batch operations:** Use `read_multiple_files` instead of multiple `read_file` calls
4. **Search refinement:** Start broad, narrow with filePattern and better keywords
5. **Process reuse:** Keep Python REPL running for multiple analysis operations
6. **Edit verification:** Use `read_file` with specific line range after edits to verify

---

## Configuration

### Get Config
```
get_config()
```

**Shows:** blockedCommands, defaultShell, allowedDirectories, file limits, system info

### Set Config Value
```
set_config_value(key, value)
```

**Common configs:**
- `defaultShell` - Change shell (powershell.exe, cmd, bash)
- `fileReadLineLimit` - Max lines for read_file (default: 1000)
- `fileWriteLineLimit` - Warning threshold for writes (default: 50)
- `allowedDirectories` - Restrict file access (empty array = full access)

**⚠️ WARNING:** Use set_config in separate chat from file operations for security

---

## Platform-Specific Notes

### Windows
- Default shell: `powershell.exe`
- Try `cmd` if PowerShell has execution policy issues
- File paths use backslashes or forward slashes (both work)
- Different commands: `Get-Process` vs `ps`, `dir` vs `ls`

### macOS/Linux
- Default shell: `bash` or `zsh`
- Standard Unix commands available
- Permissions may require sudo for some operations

---

*Last updated: October 2025*
*For issues or questions, check DC documentation or ask for help*
