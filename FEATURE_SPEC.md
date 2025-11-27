# Feature Specification: Tag System for Todo Application

## Problem Statement
The existing `todo.py` supports only basic CRUD without categorization. Users need a lightweight way to organize tasks using tags, filter tasks by tags, and view tag statistics, with minimal setup and automated testing.

## Goals & Objectives
- Add tag-based categorization to todo items
- Provide filtering (single tag, AND/OR multi-tag)
- Expose tag statistics and tag management (add/remove per task)
- Maintain backward compatibility for untagged tasks
- Deliver one-command environment setup and automated testing

## Use Cases
1. **Categorize tasks:** Assign `work`, `personal`, `urgent` tags at creation time.
2. **Filter tasks:** View tasks matching one or multiple tags (e.g., all `work` AND `urgent` tasks).
3. **Manage tags:** Add/remove tags from existing tasks as priorities evolve.
4. **Tag insights:** View tag frequency to understand workload distribution.
5. **Developer onboarding:** Set up environment and run tests in <5 minutes.

## Functional Requirements
- Data model: `{"task": str, "completed": bool, "tags": list[str]}`
- Functions:
  - `add_todo(task: str, tags: list[str] | None = None) -> None`
  - `list_todos(filter_tag: str | None = None) -> None`
  - `filter_by_tags(tags: list[str], match_all: bool = False) -> list`
  - `show_tag_stats() -> None`
  - `add_tag_to_task(index: int, tag: str) -> None`
  - `remove_tag_from_task(index: int, tag: str) -> None`
  - `list_all_tags() -> list[str]`
- Tag normalization: lowercase, trimmed, deduplicated
- Error handling: invalid indices, non-string tags, empty tags, type validation
- Backward compatibility: untagged todos remain valid
- Optional CLI for manual usage

## Non-Functional Requirements
- Python 3.8+
- Automated tests with `pytest`
- One-command setup scripts for Windows (PowerShell) and POSIX (Bash)
- Documentation covering setup, usage, API, and troubleshooting

## Success Metrics
- ✅ All new features implemented and documented
- ✅ Pytest suite passes consistently
- ✅ Setup scripts create venv and install deps in one command
- ✅ New developer can set up and run tests in <5 minutes
- ✅ No breaking changes for existing untagged workflow

## Deliverables
- `todo_with_tags.py`, `test_todo_with_tags.py`
- `requirements.txt`, `requirements-dev.txt`, `pytest.ini`
- `setup_env.ps1/.sh`, `run_tests.ps1/.sh`
- `.gitignore`, `README.md`, `FEATURE_SPEC.md`

## Notes
- Tags are case-insensitive (normalized to lowercase)
- Utility helpers (`clear_todos`, `get_todos`) provided for tests and scripting
