"""
Enhanced Todo List Application with tag-based categorization.

Core features:
- Assign multiple tags to tasks
- Filter by tags (AND/OR logic)
- View tag statistics
- Add/remove tags from existing tasks
- Backward compatible with untagged tasks
"""
from __future__ import annotations

from typing import Iterable, List, Optional, Dict
import copy

# Public, mutable in-memory store (kept for simplicity and backward compatibility)
todos: List[dict] = []


# ---------- Helpers ----------
def _normalize_tags(tags: Optional[Iterable[str]]) -> List[str]:
    """Normalize tags to a unique, lower-cased list preserving order.

    Args:
        tags: Iterable of tag strings or None.

    Returns:
        List of unique, normalized tags (lowercase, stripped). Empty if input is None/empty.

    Raises:
        TypeError: if any tag is not a string.
        ValueError: if any tag is an empty string after stripping.
    """
    if tags is None:
        return []
    # Reject bare strings/bytes to avoid iterating characters
    if isinstance(tags, (str, bytes)):
        raise TypeError("Tags must be an iterable of strings, not a string")

    normalized: List[str] = []
    seen = set()
    for tag in tags:
        if not isinstance(tag, str):
            raise TypeError("Tags must be strings")
        t = tag.strip().lower()
        if t == "":
            raise ValueError("Tags cannot be empty")
        if t not in seen:
            seen.add(t)
            normalized.append(t)
    return normalized

def _validate_index(index: int) -> None:
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if index < 0 or index >= len(todos):
        raise IndexError("Invalid index")


# ---------- Core API ----------
def add_todo(task: str, tags: Optional[Iterable[str]] = None) -> dict:
    """Add a new todo item.

    Args:
        task: Task description.
        tags: Optional iterable of tags.

    Returns:
        The created todo dictionary.

    Raises:
        ValueError: if task is empty.
        TypeError/ValueError: propagated from _normalize_tags.
    """
    if not isinstance(task, str):
        raise TypeError("Task must be a string")
    if not task.strip():
        raise ValueError("Task cannot be empty")

    todo = {"task": task, "completed": False, "tags": _normalize_tags(tags)}
    todos.append(todo)
    return todo


def list_todos(filter_tag: Optional[str] = None) -> List[dict]:
    """Display todos, optionally filtered by a single tag.

    Returns the list of todos that were displayed to ease testing.
    """
    if filter_tag is None:
        items = todos
    else:
        items = filter_by_tags([filter_tag], match_all=True)

    if not items:
        print("No todos found")
        return []

    print("\nTodo List:")
    print("-" * 60)
    for i, todo in enumerate(items):
        status = "✓" if todo.get("completed") else " "
        tag_str = f" tags: {', '.join(todo.get('tags', []))}" if todo.get("tags") else ""
        print(f"{i}. [{status}] {todo.get('task')}" + tag_str)
    print("-" * 60)
    return items


def filter_by_tags(tags: Iterable[str], match_all: bool = False, todos_list: Optional[List[dict]] = None) -> List[dict]:
    """Filter todos by tags.

    Args:
        tags: Iterable of tags to match.
        match_all: AND logic if True, else OR logic.
        todos_list: Optional explicit todos list; defaults to module-level `todos`.

    Returns:
        Filtered list of todo dicts.
    """
    normalized = _normalize_tags(tags)
    if not normalized:
        return []
    source = todos if todos_list is None else todos_list
    if match_all:
        return [t for t in source if all(tag in t.get("tags", []) for tag in normalized)]
    return [t for t in source if any(tag in t.get("tags", []) for tag in normalized)]


def show_tag_stats(todos_list: Optional[List[dict]] = None) -> Dict[str, int]:
    """Print and return tag frequency statistics.

    Args:
        todos_list: Optional explicit todos list; defaults to module-level `todos`.

    Returns:
        Dict mapping tag -> frequency count, sorted by count desc then tag asc.
    """
    source = todos if todos_list is None else todos_list
    stats: Dict[str, int] = {}
    for t in source:
        for tag in _normalize_tags(t.get("tags", [])):
            stats[tag] = stats.get(tag, 0) + 1

    # Print nicely
    if not stats:
        print("No tags found")
        return {}
    print("Tag Stats:")
    print("-" * 40)
    for tag, count in sorted(stats.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{tag}: {count}")
    print("-" * 40)
    return stats


def add_tag_to_task(index: int, tag: str) -> bool:
    """Add a tag to an existing task.

    Returns True if the tag was added, False if it already existed.
    """
    _validate_index(index)
    todo = todos[index]
    tag_norm = _normalize_tags([tag])[0]
    if tag_norm in todo.get("tags", []):
        return False
    todo.setdefault("tags", []).append(tag_norm)
    return True


def remove_tag_from_task(index: int, tag: str) -> bool:
    """Remove a tag from an existing task.

    Returns True if removed, False if the tag was not present.
    """
    _validate_index(index)
    todo = todos[index]
    tag_norm = _normalize_tags([tag])[0]
    if tag_norm in todo.get("tags", []):
        todo["tags"].remove(tag_norm)
        return True
    return False


def list_all_tags(todos_list: Optional[List[dict]] = None) -> List[str]:
    """Return all unique tags across todos, sorted alphabetically."""
    stats = show_tag_stats(todos_list)
    return sorted(stats.keys()) if stats else []


def mark_complete(index: int) -> None:
    """Mark a todo as completed."""
    _validate_index(index)
    todos[index]["completed"] = True


def remove_todo(index: int) -> dict:
    """Remove a todo item by index and return it."""
    _validate_index(index)
    return todos.pop(index)


def clear_todos() -> None:
    """Utility to clear todos (primarily for tests)."""
    todos.clear()


def get_todos(deepcopy: bool = False) -> List[dict]:
    """Utility to get todos (optionally deep-copied)."""
    return copy.deepcopy(todos) if deepcopy else list(todos)


# ---------- Simple CLI for manual use ----------
def _parse_tags_input(raw: str) -> List[str]:
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def main() -> None:
    """Main application loop (interactive CLI)."""
    print("=== Todo List with Tags ===")

    while True:
        print("\nCommands: add, list, list-tag <tag>, complete, remove, add-tag, remove-tag, stats, quit")
        raw = input("> ").strip()
        if not raw:
            continue
        parts = raw.split()
        command = parts[0].lower()

        try:
            if command == "add":
                task = input("Enter task: ")
                tags_raw = input("Enter tags (comma-separated, optional): ")
                add_todo(task, _parse_tags_input(tags_raw))
            elif command == "list":
                list_todos()
            elif command == "list-tag":
                if len(parts) < 2:
                    print("Usage: list-tag <tag>")
                else:
                    list_todos(filter_tag=parts[1])
            elif command == "complete":
                list_todos()
                idx = int(input("Enter index to complete: "))
                mark_complete(idx)
                print("Completed.")
            elif command == "remove":
                list_todos()
                idx = int(input("Enter index to remove: "))
                removed = remove_todo(idx)
                print(f"Removed: {removed['task']}")
            elif command == "add-tag":
                list_todos()
                idx = int(input("Enter index: "))
                tag = input("Enter tag to add: ")
                added = add_tag_to_task(idx, tag)
                print("Added." if added else "Tag already present.")
            elif command == "remove-tag":
                list_todos()
                idx = int(input("Enter index: "))
                tag = input("Enter tag to remove: ")
                removed = remove_tag_from_task(idx, tag)
                print("Removed." if removed else "Tag not present.")
            elif command == "stats":
                show_tag_stats()
            elif command == "quit":
                print("Goodbye!")
                break
            else:
                print("Unknown command")
        except Exception as exc:  # noqa: BLE001 - simple CLI
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
