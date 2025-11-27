# Todo With Tags

Enhanced Todo List Application with Tag-based Categorization

## Overview & Features
- Add tasks with multiple tags
- Filter by tags using OR/AND logic
- Show tag statistics (counts)
- Add/remove tags from tasks
- Maintain backward compatibility with tasks that don't have tags

## Quick Start

Windows (PowerShell):

```powershell
.\setup_env.ps1
. .\.venv\Scripts\Activate.ps1
.\run_tests.ps1
```

Linux / macOS:

```bash
./setup_env.sh
source .venv/bin/activate
./run_tests.sh
```

## Installation

1. Ensure Python 3.8+ is installed.
2. Run the appropriate setup script for your platform (see Quick Start).

## Usage Examples

```python
from todo_with_tags import add_todo, list_todos, filter_by_tags, show_tag_stats

add_todo("Write report", tags=["work", "urgent"])
list_todos()  # Show all
list_todos(filter_tag="work")  # Filter by a single tag

# OR/AND logic with filter_by_tags
result_or = filter_by_tags(["work", "urgent"], match_all=False)  # OR
result_and = filter_by_tags(["work", "urgent"], match_all=True)  # AND

show_tag_stats()
```

## Testing Guide

Run all tests:

```bash
# Linux / macOS
./run_tests.sh

# Windows PowerShell
.\run_tests.ps1
```

Run an individual test:

```bash
pytest -q test_todo_with_tags.py::test_add_todo_with_tags_and_normalization
```

## Project Structure
```
project_root/
├── todo.py
├── todo_with_tags.py
├── test_todo_with_tags.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── setup_env.ps1
├── setup_env.sh
├── run_tests.ps1
├── run_tests.sh
├── .gitignore
├── README.md
└── FEATURE_SPEC.md
```

## API Documentation
- add_todo(task: str, tags: list[str] = None) -> None
- list_todos(filter_tag: Optional[object] = None) -> None
- filter_by_tags(tags: list[str], match_all: bool = False) -> list
- show_tag_stats() -> None
- add_tag_to_task(index: int, tag: str) -> None
- remove_tag_from_task(index: int, tag: str) -> None
- list_all_tags() -> list[str]

## Development Setup
- Create and activate a venv (see setup scripts).
- Run tests with `pytest`.

## Before/After Comparison
- Before: todos only had task and completed fields in `todo.py`.
- After: `todo_with_tags.py` supports the `tags` field and tag-based operations.

## Troubleshooting
- If tests fail due to missing dependencies, run the setup script again.
- If Windows PowerShell prevents running ps1 scripts, update execution policy or run in an elevated shell.

