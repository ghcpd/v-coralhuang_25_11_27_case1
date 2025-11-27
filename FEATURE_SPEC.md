# Feature Specification: Tag-based Todo System

## Problem Statement
The existing todo app stores tasks without tags. Users want to categorize tasks with tags, filter by tags (AND/OR), show tag usage statistics, and dynamically add/remove tags from tasks.

## Goals & Success Metrics
- Allow multiple tags per task.
- Provide filtering by tag(s) with AND/OR semantics.
- Provide tag statistics (counts).
- Add/remove tags to/from existing tasks.
- Backward-compatible with existing untagged tasks.
- Unit & integration tests ensuring correctness.
- One-command environment setup and tests for Windows & Linux/Mac.

## Use Cases
1. Add a task with tags
2. Add tags to an existing task
3. Remove tags from a task
4. Filter tasks by tags (single, multiple, AND/OR)
5. View tag statistics
6. Ensure untagged or legacy tasks still work

## Constraints & Decisions
- Tags are case-insensitive; stored normalized as lowercase.
- Duplicates in tags lists are ignored.
- Functions provide clear error messages for invalid inputs.
- Minimal third-party dependencies; testing uses pytest.

## API
- add_todo(task: str, tags: list[str] | None)
- list_todos(filter_tag: str | list[str] | None)
- filter_by_tags(tags: list[str], match_all: bool = False) -> list
- show_tag_stats()
- add_tag_to_task(index: int, tag: str)
- remove_tag_from_task(index: int, tag: str)
- list_all_tags() -> list[str]

## Acceptance Criteria
- All functions implemented and documented
- Tests covering unit & integration scenarios
- Setup & test scripts work on major platforms
- Readme provides usage and developer setup
