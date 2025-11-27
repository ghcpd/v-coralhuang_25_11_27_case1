# Todo List with Tags

This project enhances a simple todo app with a tag system and automated tests.

## Features
- Assign multiple tags to tasks
- Filter by single/multiple tags (AND/OR logic)
- View tag statistics
- Add/remove tags on existing tasks

## Quick Start
Windows:
```
.\setup_env.ps1; .\run_tests.ps1
```

Linux / macOS:
```
./setup_env.sh; ./run_tests.sh
```

## Installation
1. Install Python 3.8+ and ensure `python` is in PATH.
2. Run `setup_env.ps1` on Windows or `setup_env.sh` on Linux/Mac.

## Usage Examples
```
from todo_with_tags import add_todo, list_todos, show_tag_stats
add_todo("Write report", tags=["work", "urgent"])
print(list_todos("work"))
print(show_tag_stats())
```

## Testing
Run the one-command runner on your platform:
```
Windows: .\run_tests.ps1
Linux/Mac: ./run_tests.sh
```

## Project structure
See top-level `Prompt.md` for the file overview required by the task.

## API
- `add_todo(task: str, tags: list[str] = None)`
- `list_todos(filter_tag: str = None) -> list` : returns list of todo dicts
- `filter_by_tags(todos, tags, match_all=False)`
- `show_tag_stats() -> dict`
- `add_tag_to_task(index, tag)`
- `remove_tag_from_task(index, tag)`
- `list_all_tags()`

## Development Setup
- Use `venv` created by the setup scripts
- Install dev dependencies using the same setup scripts

## Before & After
Operating on a backward-compatible in-memory `todos` list, we now have `tags` field for each todo item. Untagged tasks remain supported.

## Troubleshooting
- Ensure Python 3.8+ is installed
- On Windows, run PowerShell as an elevated user or use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` if activation fails
