# Todo List with Tags

## 1. Overview & Features
A lightweight todo application enhanced with tag-based categorization.
- 🏷 Assign multiple tags to tasks (normalized to lowercase)
- 🔍 Filter by single or multiple tags (OR/AND logic)
- 📊 View tag statistics
- ➕➖ Add/remove tags from existing tasks
- ✅ Backward compatible with untagged tasks

## 2. Quick Start
### Windows (PowerShell)
```powershell
# from repo root
.\setup_env.ps1
.\run_tests.ps1
```

### Linux/Mac (Bash)
```bash
./setup_env.sh
./run_tests.sh
```

## 3. Installation
- **Prerequisite:** Python 3.8+
- **Windows:** Ensure PowerShell execution policy allows local scripts: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
- **Linux/Mac:** Make scripts executable if needed: `chmod +x setup_env.sh run_tests.sh`

### Manual steps (optional)
1. `python -m venv .venv`
2. Activate (`.venv\Scripts\activate` on Windows, `. .venv/bin/activate` on POSIX)
3. `pip install -r requirements-dev.txt`

## 4. Usage Examples
### Python API
```python
from todo_with_tags import add_todo, filter_by_tags, list_todos, show_tag_stats

add_todo("Write report", tags=["work", "urgent"])
add_todo("Buy milk", tags=["personal"])
list_todos()                      # prints all
list_todos(filter_tag="work")    # filter by single tag

filter_by_tags(["work", "urgent"], match_all=True)  # AND
show_tag_stats()                  # prints: work (1), urgent (1), personal (1)
```

### CLI (optional)
```text
python todo_with_tags.py
Commands: add, list, list-tag <tag>, complete, remove, add-tag, remove-tag, stats, quit
```

## 5. Testing Guide
- Run all tests: see **Quick Start** above
- Pass extra args to pytest:
  - Windows: `.





















































- **Stale venv:** Recreate with `.\.venv` folder deletion or `.\setup_env.ps1 -Force` / `FORCE=1 ./setup_env.sh`.- **Proxy issues:** Configure `pip` with `--proxy` as needed.- **Scripts not executable (POSIX):** `chmod +x setup_env.sh run_tests.sh`- **Execution policy (Windows):** `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`- **Python not found:** Install Python 3.8+ and ensure it's on PATH (`py -3` on Windows).## 10. Troubleshooting| Tests | None | Comprehensive pytest suite || API | CLI-only | Reusable functions + CLI || Stats | None | Tag frequency summary || Filtering | None | Single-tag filter; multi-tag AND/OR via `filter_by_tags` || Tags | Not supported | Multiple tags per task ||--------|--------------------|-----------------------------|| Aspect | Before (`todo.py`) | After (`todo_with_tags.py`) |## 9. Before/After Comparison- Tests use `pytest` with `capsys` and fixtures- Linting/formatting intentionally minimal for simplicity- Use `.venv` virtual environment (scripts handle creation)## 8. Development Setup| `get_todos(deepcopy: bool = False) -> list[dict]` | Get todos snapshot | Optional deep copy || `clear_todos() -> None` | Clear all todos | Testing utility || `remove_todo(index: int) -> dict` | Remove task by index | Returns removed todo || `mark_complete(index: int) -> None` | Mark task completed | Raises `IndexError` if invalid || `list_all_tags(todos_list: list[dict] | None = None) -> list[str]` | Return all unique tags | Alphabetically sorted || `remove_tag_from_task(index: int, tag: str) -> bool` | Remove tag from task | Returns True if removed || `add_tag_to_task(index: int, tag: str) -> bool` | Add tag to task | Returns True if added || `show_tag_stats(todos_list: list[dict] | None = None) -> dict[str,int]` | Print & return tag counts | Sorted by count desc, then tag || `filter_by_tags(tags: list[str], match_all: bool = False, todos_list: list[dict] | None = None) -> list[dict]` | Filter by tags | AND if `match_all`, else OR; defaults to module todos || `list_todos(filter_tag: str | None = None) -> list[dict]` | Print & return todos (optionally filtered) | Filter uses AND for single tag || `add_todo(task: str, tags: list[str] | None = None) -> dict` | Add task with optional tags | Tags normalized (lowercase, deduped) ||----------|-------------|-------|| Function | Description | Notes |## 7. API Documentation```└── FEATURE_SPEC.md         # Feature specification├── README.md               # This file├── run_tests.ps1 / .sh     # Test runner scripts├── setup_env.ps1 / .sh     # Env setup scripts├── pytest.ini              # Pytest config├── requirements-dev.txt    # Dev/test deps (pytest)├── requirements.txt        # Runtime deps (none)├── test_todo_with_tags.py  # Pytest suite├── todo_with_tags.py       # Enhanced module + CLI├── todo.py                 # Original simple CLI.```## 6. Project Structure  - POSIX: `./run_tests.sh -k filter`un_tests.ps1 -PytestArgs '-k filter'`