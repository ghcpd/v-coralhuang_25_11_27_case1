"""
Todo List Application with Tag System
Enhanced CRUD operations with tag-based categorization
"""

from typing import Optional, List, Dict, Set
from collections import Counter

# Global todos list storing task data
todos: List[Dict[str, any]] = []


def add_todo(task: str, tags: Optional[List[str]] = None) -> None:
    """
    Add a new todo item with optional tags.
    
    Args:
        task: The task description (required)
        tags: List of tag strings (optional, defaults to empty list)
    
    Returns:
        None
    
    Raises:
        TypeError: If task is not a string or tags is not a list
        ValueError: If task is empty
    """
    if not isinstance(task, str):
        raise TypeError(f"task must be a string, got {type(task).__name__}")
    if not task.strip():
        raise ValueError("task cannot be empty")
    if tags is not None and not isinstance(tags, list):
        raise TypeError(f"tags must be a list, got {type(tags).__name__}")
    
    # Normalize tags: remove duplicates, lowercase, strip whitespace
    normalized_tags = []
    if tags:
        normalized_tags = list(set(tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()))
    
    todos.append({
        "task": task.strip(),
        "completed": False,
        "tags": normalized_tags
    })
    print(f"Added: {task}")


def remove_todo(index: int) -> None:
    """
    Remove a todo item by index.
    
    Args:
        index: The index of the todo to remove (0-based)
    
    Returns:
        None
    
    Raises:
        TypeError: If index is not an integer
        IndexError: If index is out of range
    """
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"index must be an integer, got {type(index).__name__}")
    
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        print(f"Removed: {removed['task']}")
    else:
        raise IndexError(f"Invalid index {index}, must be between 0 and {len(todos) - 1}")


def list_todos(filter_tag: Optional[str] = None) -> None:
    """
    Display all todo items, optionally filtered by tag.
    
    Args:
        filter_tag: If provided, only show todos containing this tag (case-insensitive)
    
    Returns:
        None
    """
    filtered = todos
    if filter_tag:
        if not isinstance(filter_tag, str):
            raise TypeError(f"filter_tag must be a string, got {type(filter_tag).__name__}")
        filter_tag_lower = filter_tag.strip().lower()
        filtered = [t for t in todos if filter_tag_lower in t.get("tags", [])]
    
    if not filtered:
        print("No todos found")
        return
    
    print("\nTodo List:")
    print("-" * 60)
    for i, todo in enumerate(filtered):
        status = "✓" if todo["completed"] else " "
        tags_str = f" [{', '.join(todo.get('tags', []))}]" if todo.get("tags") else ""
        print(f"{i}. [{status}] {todo['task']}{tags_str}")
    print("-" * 60)


def filter_by_tags(tags: List[str], match_all: bool = False) -> List[Dict]:
    """
    Filter todos by one or more tags using AND/OR logic.
    
    Args:
        tags: List of tags to filter by
        match_all: If True, use AND logic (must have all tags).
                  If False, use OR logic (must have any tag).
    
    Returns:
        List of todos matching the filter criteria
    
    Raises:
        TypeError: If tags is not a list or match_all is not a boolean
        ValueError: If tags is empty
    """
    if not isinstance(tags, list):
        raise TypeError(f"tags must be a list, got {type(tags).__name__}")
    if not isinstance(match_all, bool):
        raise TypeError(f"match_all must be a boolean, got {type(match_all).__name__}")
    if not tags:
        raise ValueError("tags list cannot be empty")
    
    # Normalize filter tags to lowercase
    normalized_tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
    
    if not normalized_tags:
        raise ValueError("tags list contains no valid strings")
    
    if match_all:
        # AND logic: all filter tags must be present in todo's tags
        return [
            t for t in todos
            if all(tag in t.get("tags", []) for tag in normalized_tags)
        ]
    else:
        # OR logic: at least one filter tag must be present in todo's tags
        return [
            t for t in todos
            if any(tag in t.get("tags", []) for tag in normalized_tags)
        ]


def show_tag_stats() -> None:
    """
    Display statistics about all tags used in todos.
    Shows tag name and count of todos using that tag.
    
    Returns:
        None
    """
    tag_counter: Counter = Counter()
    
    for todo in todos:
        for tag in todo.get("tags", []):
            tag_counter[tag] += 1
    
    if not tag_counter:
        print("No tags found")
        return
    
    print("\nTag Statistics:")
    print("-" * 40)
    # Sort by count (descending) then alphabetically
    for tag, count in sorted(tag_counter.items(), key=lambda x: (-x[1], x[0])):
        print(f"{tag}: {count}")
    print("-" * 40)


def add_tag_to_task(index: int, tag: str) -> None:
    """
    Add a tag to an existing todo item.
    
    Args:
        index: The index of the todo to modify (0-based)
        tag: The tag to add (case will be normalized to lowercase)
    
    Returns:
        None
    
    Raises:
        TypeError: If index is not an integer or tag is not a string
        IndexError: If index is out of range
        ValueError: If tag is empty
    """
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"index must be an integer, got {type(index).__name__}")
    if not isinstance(tag, str):
        raise TypeError(f"tag must be a string, got {type(tag).__name__}")
    
    tag_normalized = tag.strip().lower()
    if not tag_normalized:
        raise ValueError("tag cannot be empty")
    
    if not (0 <= index < len(todos)):
        raise IndexError(f"Invalid index {index}, must be between 0 and {len(todos) - 1}")
    
    if tag_normalized not in todos[index]["tags"]:
        todos[index]["tags"].append(tag_normalized)
        print(f"Added tag '{tag_normalized}' to: {todos[index]['task']}")
    else:
        print(f"Tag '{tag_normalized}' already exists on this task")


def remove_tag_from_task(index: int, tag: str) -> None:
    """
    Remove a tag from an existing todo item.
    
    Args:
        index: The index of the todo to modify (0-based)
        tag: The tag to remove (case will be normalized to lowercase)
    
    Returns:
        None
    
    Raises:
        TypeError: If index is not an integer or tag is not a string
        IndexError: If index is out of range
        ValueError: If tag is empty or not found on task
    """
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"index must be an integer, got {type(index).__name__}")
    if not isinstance(tag, str):
        raise TypeError(f"tag must be a string, got {type(tag).__name__}")
    
    tag_normalized = tag.strip().lower()
    if not tag_normalized:
        raise ValueError("tag cannot be empty")
    
    if not (0 <= index < len(todos)):
        raise IndexError(f"Invalid index {index}, must be between 0 and {len(todos) - 1}")
    
    if tag_normalized in todos[index]["tags"]:
        todos[index]["tags"].remove(tag_normalized)
        print(f"Removed tag '{tag_normalized}' from: {todos[index]['task']}")
    else:
        raise ValueError(f"Tag '{tag_normalized}' not found on this task")


def mark_complete(index: int) -> None:
    """
    Mark a todo as completed.
    
    Args:
        index: The index of the todo to mark complete (0-based)
    
    Returns:
        None
    
    Raises:
        TypeError: If index is not an integer
        IndexError: If index is out of range
    """
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"index must be an integer, got {type(index).__name__}")
    
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
        print(f"Completed: {todos[index]['task']}")
    else:
        raise IndexError(f"Invalid index {index}, must be between 0 and {len(todos) - 1}")


def list_all_tags() -> List[str]:
    """
    Get a list of all unique tags used in todos.
    
    Returns:
        Sorted list of unique tags (lowercase)
    """
    all_tags: Set[str] = set()
    for todo in todos:
        all_tags.update(todo.get("tags", []))
    return sorted(list(all_tags))


def main() -> None:
    """Main application loop with enhanced tag support."""
    print("=== Todo List with Tags ===")
    
    while True:
        print("\nCommands: add, list, complete, remove, add-tag, remove-tag, tags, stats, quit")
        command = input("> ").strip().lower()
        
        try:
            if command == "add":
                task = input("Enter task: ").strip()
                tags_input = input("Enter tags (comma-separated, optional): ").strip()
                tags = [t.strip() for t in tags_input.split(",")] if tags_input else None
                add_todo(task, tags)
            
            elif command == "list":
                filter_tag = input("Enter tag to filter (optional): ").strip()
                list_todos(filter_tag if filter_tag else None)
            
            elif command == "complete":
                list_todos()
                index = int(input("Enter index to complete: "))
                mark_complete(index)
            
            elif command == "remove":
                list_todos()
                index = int(input("Enter index to remove: "))
                remove_todo(index)
            
            elif command == "add-tag":
                list_todos()
                index = int(input("Enter index: "))
                tag = input("Enter tag to add: ").strip()
                add_tag_to_task(index, tag)
            
            elif command == "remove-tag":
                list_todos()
                index = int(input("Enter index: "))
                tag = input("Enter tag to remove: ").strip()
                remove_tag_from_task(index, tag)
            
            elif command == "tags":
                all_tags = list_all_tags()
                if all_tags:
                    print(f"All tags: {', '.join(all_tags)}")
                else:
                    print("No tags found")
            
            elif command == "stats":
                show_tag_stats()
            
            elif command == "quit":
                print("Goodbye!")
                break
            
            else:
                print("Unknown command. Try: add, list, complete, remove, add-tag, remove-tag, tags, stats, quit")
        
        except (ValueError, IndexError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
