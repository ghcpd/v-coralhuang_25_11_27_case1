# Todo List with Tags

This repository provides a small in-memory todo list application with support for multiple tags per task, filtering, and tag statistics.

Quick start
------------
- Windows:
  - PowerShell: `./setup_env.ps1; ./run_tests.ps1`
- Linux/Mac:
  - Bash: `./setup_env.sh && ./run_tests.sh`

Installation
------------
1. Ensure Python 3.8+ is installed and on PATH.
2. Run `setup_env.ps1` (Windows) or `./setup_env.sh` (Bash).

Usage
-----
Import and use functions from `todo_with_tags.py`:

Examples:
```
from todo_with_tags import add_todo, list_todos, show_tag_stats
add_todo("Write report", tags=["work", "urgent"])
list_todos(filter_tag="work")
show_tag_stats()
```

Testing
-------
- Setup the environment (`setup_env.*`) and run the tests using `run_tests.*`.
- To run a single test: `pytest -k test_name` or `pytest path/to/test::test_fn`.

Project Structure
-----------------
```
project_root/
├── todo.py                  # Original (provided)
├── todo_with_tags.py        # Enhanced with tags
├── test_todo_with_tags.py   # Test suite
├── requirements.txt         # Runtime (empty)
├── requirements-dev.txt     # Test dependencies (pytest)
├── pytest.ini               # Pytest config
├── setup_env.ps1
├── setup_env.sh
├── run_tests.ps1
├── run_tests.sh
├── .gitignore
├── README.md
└── FEATURE_SPEC.md
```

API Documentation
-----------------
- add_todo(task: str, tags: list[str] | None) -> None
- list_todos(filter_tag: Optional[str] = None) -> List[Dict[str, Any]]
- filter_by_tags(source_todos: Optional[List[Dict]], tags: List[str], match_all: bool = False) -> List[Dict]
- show_tag_stats() -> Dict[str, int]
- add_tag_to_task(index: int, tag: str) -> None
- remove_tag_from_task(index: int, tag: str) -> None
- list_all_tags() -> List[str]

Development Setup
-----------------
1. Clone repo, run setup script
2. Run `pytest` using the venv python or `run_tests.*` script

Before/After
--------------
- Before: simple todo list with only tasks and completion
- After: tasks may have multiple normalized tags; filterable, manageable, and test-covered

Troubleshooting
---------------
- If PS scripts fail due to execution policy, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell.
- If Python is not found, ensure installation and PATH are configured.
