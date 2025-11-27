"""
Todo list application with tag support

Provides a simple in-memory todo list and helper functions for managing tags.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional

todos: List[Dict[str, Any]] = []


def _normalize_tag(tag: str) -> str:
    """Normalize tag values for consistent comparisons.

    Normalizes to lowercase and strips whitespace. Intentionally simple so
    that comparisons are case-insensitive.
    """
    return tag.strip().lower()


def add_todo(task: str, tags: Optional[List[str]] = None) -> None:
    """Add a todo item, optionally with tags.

    Args:
        task: A short text description of the task.
        tags: A list of tags to attach (optional).
    """
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")

    if tags is None:
        normalized_tags: List[str] = []
    else:
        if not isinstance(tags, list):
            raise TypeError("tags must be a list of strings")
        normalized_tags = [ _normalize_tag(t) for t in tags if isinstance(t, str) and t.strip() ]

    todos.append({"task": task, "completed": False, "tags": normalized_tags})


def list_todos(filter_tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return a list of todo items, optionally filtered by a tag.

    Args:
        filter_tag: Single tag (string) to filter the list by.

    Returns:
        A list of todo dictionaries (task, completed, tags).
    """
    if filter_tag is None:
        return list(todos)
    if not isinstance(filter_tag, str) or not filter_tag.strip():
        raise ValueError("filter_tag must be a non-empty string")

    key = _normalize_tag(filter_tag)
    return [t for t in todos if key in t.get("tags", [])]


def filter_by_tags(input_todos: Optional[List[Dict[str, Any]]], tags: List[str], match_all: bool = False) -> List[Dict[str, Any]]:
    """Filter the provided list of todos by a list of tags.

    Args:
        input_todos: The list of todos to filter. If None, defaults to module-level todos.
        tags: A list of tags to filter by.
        match_all: If True, returns items that have all tags (AND). If False, returns items with any tag (OR).
    """
    if input_todos is None:
        input_todos = todos
    if not isinstance(input_todos, list):
        raise TypeError("input_todos must be a list of todo dicts")
    if not isinstance(tags, list) or not tags:
        raise ValueError("tags must be a non-empty list of strings")

    normalized = [_normalize_tag(t) for t in tags if isinstance(t, str) and t.strip()]
    if not normalized:
        raise ValueError("tags must contain at least one non-empty string")

    if match_all:
        return [t for t in input_todos if all(tag in t.get("tags", []) for tag in normalized)]
    return [t for t in input_todos if any(tag in t.get("tags", []) for tag in normalized)]


def show_tag_stats() -> Dict[str, int]:
    """Return a mapping of tag -> count of todos using it.

    Returns:
        Dictionary mapping tag (lowercased) to usage count.
    """
    stats: Dict[str, int] = {}
    for t in todos:
        for tag in t.get("tags", []):
            stats[tag] = stats.get(tag, 0) + 1
    return stats


def add_tag_to_task(index: int, tag: str) -> None:
    """Add a tag to a task by index.

    Has no effect if the tag already exists.
    """
    if not isinstance(index, int) or index < 0 or index >= len(todos):
        raise IndexError("Invalid index")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("tag must be a non-empty string")
    key = _normalize_tag(tag)
    current = todos[index].setdefault("tags", [])
    if key not in current:
        current.append(key)


def remove_tag_from_task(index: int, tag: str) -> None:
    """Remove a tag from a task by index.

    If the tag does not exist on the task, nothing happens.
    """
    if not isinstance(index, int) or index < 0 or index >= len(todos):
        raise IndexError("Invalid index")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("tag must be a non-empty string")
    key = _normalize_tag(tag)
    current = todos[index].get("tags", [])
    if key in current:
        current.remove(key)


def list_all_tags() -> List[str]:
    """Return a sorted list of all known tags in lower-case.

    This function iterates the current todos and de-duplicates tags.
    """
    return sorted(show_tag_stats().keys())


def reset_todos():
    """Helper for testing: clear all todos."""
    todos.clear()


if __name__ == "__main__":
    # Simple interactive demo (backwards-compatible convenience wrapper)
    print("=== Todo List with Tags ===")
    while True:
        cmd = input("Commands: add, list, list_tags, stats, add_tag, remove_tag, quit\n> ").strip().lower()
        if cmd == "add":
            task = input("Enter task: ")
            tag_line = input("Enter comma-separated tags (optional): ")
            tags = [t.strip() for t in tag_line.split(",")] if tag_line.strip() else None
            add_todo(task, tags)
        elif cmd == "list":
            tag = input("Filter by tag (optional): ").strip()
            tag = tag or None
            for i, t in enumerate(list_todos(tag)):
                status = "✓" if t["completed"] else " "
                print(f"{i}. [{status}] {t['task']} (tags: {', '.join(t.get('tags', []))})")
        elif cmd == "list_tags":
            print(list_all_tags())
        elif cmd == "stats":
            print(show_tag_stats())
        elif cmd == "add_tag":
            idx = int(input("Index: "))
            tag = input("Tag: ")
            add_tag_to_task(idx, tag)
        elif cmd == "remove_tag":
            idx = int(input("Index: "))
            tag = input("Tag: ")
            remove_tag_from_task(idx, tag)
        elif cmd == "quit":
            break
        else:
            print("Unknown command")
