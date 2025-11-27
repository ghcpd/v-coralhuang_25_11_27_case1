"""
Enhanced Todo List with Tag System
"""
from typing import List, Optional, Dict

# Global todo storage; each todo: {'task': str, 'completed': bool, 'tags': List[str]}
todos: List[Dict[str, object]] = []


def _normalize_tag(tag: str) -> str:
    """Normalize tag text for case-insensitive handling."""
    return tag.strip().lower()


def add_todo(task: str, tags: Optional[List[str]] = None) -> None:
    """Add a new todo with optional tags.

    Args:
        task: The task description
        tags: Optional list of tag names
    """
    if not isinstance(task, str) or not task.strip():
        raise ValueError("Task must be a non-empty string")

    normalized_tags = []
    if tags:
        if not isinstance(tags, list):
            raise ValueError("Tags must be a list of strings")
        for t in tags:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("Each tag must be a non-empty string")
            nt = _normalize_tag(t)
            if nt not in normalized_tags:
                normalized_tags.append(nt)

    todos.append({"task": task, "completed": False, "tags": normalized_tags})


def remove_todo(index: int) -> None:
    """Remove a todo item by index. Raises IndexError on bad index."""
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if 0 <= index < len(todos):
        todos.pop(index)
    else:
        raise IndexError("Invalid index")


def list_todos(filter_tag: Optional[object] = None) -> None:
    """Print all todos. Optionally filter by a single tag, or list of tags.

    Args:
        filter_tag: A string or list of strings to filter by (show only matching todos).
    """
    if filter_tag is not None:
        # Accept string or list
        if isinstance(filter_tag, str):
            filter_tags = [_normalize_tag(filter_tag)]
            match_all = False
        elif isinstance(filter_tag, list):
            filter_tags = [_normalize_tag(t) for t in filter_tag]
            match_all = False
        else:
            raise ValueError("filter_tag must be a string, list, or None")

        to_show = filter_by_tags(filter_tags, match_all=match_all)
    else:
        to_show = todos

    if not to_show:
        print("No todos found")
        return

    print("\nTodo List:")
    print("-" * 40)
    for i, todo in enumerate(to_show):
        status = "✓" if todo["completed"] else " "
        tags_display = f"[{', '.join(todo.get('tags', []))}]" if todo.get('tags') else ""
        print(f"{i}. [{status}] {todo['task']} {tags_display}")
    print("-" * 40)


def mark_complete(index: int) -> None:
    """Mark a todo as completed."""
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
    else:
        raise IndexError("Invalid index")


def filter_by_tags(tags: List[str], match_all: bool = False) -> List[Dict[str, object]]:
    """Return todos filtered by tag list.

    Args:
        tags: List of tags to filter by (case-insensitive)
        match_all: If True, todo must contain all tags (AND). If False, any tag matches (OR).

    Returns:
        List of todo dicts that match.
    """
    if not isinstance(tags, list) or not tags:
        return []

    normalized = [_normalize_tag(t) for t in tags]

    if match_all:
        return [t for t in todos if all(tag in t.get("tags", []) for tag in normalized)]
    else:
        return [t for t in todos if any(tag in t.get("tags", []) for tag in normalized)]


def show_tag_stats() -> None:
    """Display tag statistics (counts per tag)."""
    stats = {}
    for t in todos:
        for tag in t.get("tags", []):
            stats[tag] = stats.get(tag, 0) + 1

    if not stats:
        print("No tags found")
        return

    print("\nTag Statistics:")
    for tag, count in sorted(stats.items()):
        print(f"{tag} ({count})")


def add_tag_to_task(index: int, tag: str) -> None:
    """Add a tag to a specific task by index."""
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("Tag must be a non-empty string")
    if not 0 <= index < len(todos):
        raise IndexError("Invalid index")

    t = _normalize_tag(tag)
    tags_list: List[str] = todos[index].get("tags", [])
    if t not in tags_list:
        tags_list.append(t)
        todos[index]["tags"] = tags_list


def remove_tag_from_task(index: int, tag: str) -> None:
    """Remove a tag from a task by index."""
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("Tag must be a non-empty string")
    if not 0 <= index < len(todos):
        raise IndexError("Invalid index")

    t = _normalize_tag(tag)
    tags_list: List[str] = todos[index].get("tags", [])
    if t in tags_list:
        tags_list.remove(t)
        todos[index]["tags"] = tags_list


def list_all_tags() -> List[str]:
    """Return a unique, sorted list of all tags used across todos."""
    tag_set = set()
    for t in todos:
        tag_set.update(t.get("tags", []))
    return sorted(tag_set)


def clear_all_todos() -> None:
    """Utility for tests: clear the global todo list."""
    todos.clear()


# Backward compatible main similar to original for command-line usage
if __name__ == "__main__":
    print("=== Todo List (with Tags) ===")
    while True:
        print("\nCommands: add, list, complete, remove, addtag, rmtag, stats, tags, quit")
        command = input("> ").strip().lower()
        if command == "add":
            task = input("Enter task: ")
            tags_raw = input("Enter tags (comma separated, optional): ")
            tags = [s.strip() for s in tags_raw.split(",") if s.strip()] if tags_raw else None
            add_todo(task, tags)
        elif command == "list":
            f = input("Filter by tag (leave blank for all): ")
            if f.strip():
                list_todos(f)
            else:
                list_todos()
        elif command == "complete":
            list_todos()
            index = int(input("Enter index to complete: "))
            mark_complete(index)
        elif command == "remove":
            list_todos()
            index = int(input("Enter index to remove: "))
            remove_todo(index)
        elif command == "addtag":
            list_todos()
            index = int(input("Task index to add tag: "))
            tag = input("Tag to add: ")
            add_tag_to_task(index, tag)
        elif command == "rmtag":
            list_todos()
            index = int(input("Task index to remove tag: "))
            tag = input("Tag to remove: ")
            remove_tag_from_task(index, tag)
        elif command == "stats":
            show_tag_stats()
        elif command == "tags":
            print(list_all_tags())
        elif command == "quit":
            print("Goodbye!")
            break
        else:
            print("Unknown command")
