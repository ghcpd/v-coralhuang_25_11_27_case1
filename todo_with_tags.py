"""
Enhanced Todo List Application with Tagging Support

This module provides a simple in-memory todo list with support for tags,
filtering, and tag statistics. It is backward compatible with the previous
`todo.py` module: all functions which operate on `todos` continue to work
when items do not have tags.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any

# Global todo storage
todos: List[Dict[str, Any]] = []


def _normalize_tag(tag: str) -> str:
    """Return a normalized version of a tag for consistent matching.

    The normalization converts tags to lowercase and strips whitespace.
    """
    return tag.strip().lower()


def add_todo(task: str, tags: Optional[List[str]] = None) -> None:
    """Add a new todo item with optional tags.

    Tags will be normalized (lowercase, stripped). Duplicate tags are
    ignored.
    """
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")

    tag_list: List[str] = []
    if tags:
        if not isinstance(tags, list):
            raise TypeError("tags must be a list of strings")
        for t in tags:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("each tag must be a non-empty string")
            normalized = _normalize_tag(t)
            if normalized not in tag_list:
                tag_list.append(normalized)

    todos.append({"task": task.strip(), "completed": False, "tags": tag_list})


def list_todos(filter_tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return and print all todos optionally filtered by a single tag.

    The `filter_tag` matches items that contain the provided tag. Tag
    matching is case-insensitive due to normalization.
    """
    results = todos
    if filter_tag:
        filter_norm = _normalize_tag(filter_tag)
        results = [t for t in todos if filter_norm in t.get("tags", [])]

    # Print in friendly format for CLI compatibility
    if not results:
        print("No todos found")
        return []

    print("\nTodo List:")
    print("-" * 40)
    # Print original index of todo in the global list for clarity
    for global_i, todo in enumerate(todos):
        if todo not in results:
            continue
        status = "✓" if todo["completed"] else " "
        tags = ",".join(todo.get("tags", []))
        print(f"{global_i}. [{status}] {todo['task']} (tags: {tags})")
    print("-" * 40)

    return results


def filter_by_tags(tags: List[str], match_all: bool = False, source_todos: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Filter todos by tags.

    - `source_todos`: list of todos to search (or use global `todos` if None)
    - `tags`: list of tags to match
    - `match_all`: if True, todo must contain all tags (AND); otherwise any tag (OR)
    Returns a list of matched todos.
    """
    if source_todos is None:
        source_todos = todos

    if not isinstance(tags, list) or not tags:
        raise ValueError("tags must be a non-empty list of strings")

    norm_tags = [_normalize_tag(t) for t in tags]

    def matches(todo: Dict[str, Any]) -> bool:
        todo_tags = [ _normalize_tag(t) for t in todo.get("tags", []) ]
        if match_all:
            return all(tag in todo_tags for tag in norm_tags)
        return any(tag in todo_tags for tag in norm_tags)

    return [t for t in source_todos if matches(t)]


def show_tag_stats() -> Dict[str, int]:
    """Return and print tag statistics: a mapping from tag to count.
    """
    stats: Dict[str, int] = {}
    for t in todos:
        for tag in t.get("tags", []):
            stats[tag] = stats.get(tag, 0) + 1

    if not stats:
        print("No tags found")
        return {}

    print("\nTag Statistics:")
    for tag, count in sorted(stats.items()):
        print(f"{tag} ({count})")

    return stats


def add_tag_to_task(index: int, tag: str) -> None:
    """Add a tag to an existing todo specified by index in the global list.

    Tag is normalized. Duplicates are ignored.
    """
    if not isinstance(index, int):
        raise TypeError("index must be an integer")
    if index < 0 or index >= len(todos):
        raise IndexError("index out of range")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("tag must be a non-empty string")

    normalized = _normalize_tag(tag)
    t = todos[index]
    if "tags" not in t:
        t["tags"] = []
    if normalized not in t["tags"]:
        t["tags"].append(normalized)


def remove_tag_from_task(index: int, tag: str) -> None:
    """Remove a tag from an existing todo specified by index.
    No error if tag not present.
    """
    if not isinstance(index, int):
        raise TypeError("index must be an integer")
    if index < 0 or index >= len(todos):
        raise IndexError("index out of range")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("tag must be a non-empty string")

    normalized = _normalize_tag(tag)
    t = todos[index]
    if normalized in t.get("tags", []):
        t["tags"].remove(normalized)


def list_all_tags() -> List[str]:
    """Return a unique list of all tags across todos (sorted alphabetical).
    """
    s = set()
    for t in todos:
        for tag in t.get("tags", []):
            s.add(tag)
    return sorted(s)


def clear_all_todos() -> None:
    """Helper for tests: clear the global todos list."""
    todos.clear()


if __name__ == "__main__":
    # Minimal CLI compatibility with original `todo.py`
    print("=== Todo List (with tags) ===")
    try:
        while True:
            print("\nCommands: add, list, complete, remove, addtag, removetag, tags, stats, quit")
            command = input("> ").strip().lower()
            if command == "add":
                task = input("Enter task: ").strip()
                tags_input = input("Enter comma-separated tags (optional): ").strip()
                tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None
                add_todo(task, tags)
            elif command == "list":
                tag = input("Filter by tag (optional): ").strip()
                list_todos(tag if tag else None)
            elif command == "complete":
                list_todos()
                index = int(input("Enter index to complete: "))
                if 0 <= index < len(todos):
                    todos[index]["completed"] = True
                    print(f"Completed: {todos[index]['task']}")
                else:
                    print("Invalid index")
            elif command == "remove":
                list_todos()
                index = int(input("Enter index to remove: "))
                if 0 <= index < len(todos):
                    removed = todos.pop(index)
                    print(f"Removed: {removed['task']}")
                else:
                    print("Invalid index")
            elif command == "addtag":
                list_todos()
                index = int(input("Enter index to add tag: "))
                tag = input("Tag: ").strip()
                add_tag_to_task(index, tag)
            elif command == "removetag":
                list_todos()
                index = int(input("Enter index to remove tag: "))
                tag = input("Tag: ").strip()
                remove_tag_from_task(index, tag)
            elif command == "tags":
                all_tags = list_all_tags()
                print("Tags:", ", ".join(all_tags))
            elif command == "stats":
                show_tag_stats()
            elif command == "quit":
                print("Goodbye!")
                break
            else:
                print("Unknown command")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting")
