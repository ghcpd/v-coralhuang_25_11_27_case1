"""
Todo List Application with Tag System
Enhanced version with tag-based categorization and filtering
"""

from typing import Optional, List, Dict, Any

todos: List[Dict[str, Any]] = []


def add_todo(task: str, tags: Optional[List[str]] = None) -> None:
    """
    Add a new todo item with optional tags.
    
    Args:
        task: The task description
        tags: Optional list of tags for categorization
        
    Example:
        add_todo("Write report", tags=["work", "urgent"])
    """
    if not isinstance(task, str) or not task.strip():
        print("Error: Task must be a non-empty string")
        return
    
    if tags is not None and not isinstance(tags, list):
        print("Error: Tags must be a list")
        return
    
    # Normalize tags: convert to lowercase and remove duplicates
    normalized_tags = []
    if tags:
        normalized_tags = list(set(tag.lower().strip() for tag in tags if isinstance(tag, str) and tag.strip()))
    
    todos.append({
        "task": task,
        "completed": False,
        "tags": normalized_tags
    })
    
    if normalized_tags:
        print(f"Added: {task} [Tags: {', '.join(normalized_tags)}]")
    else:
        print(f"Added: {task}")


def remove_todo(index: int) -> None:
    """
    Remove a todo item by index.
    
    Args:
        index: The index of the todo to remove
    """
    if not isinstance(index, int):
        print("Error: Index must be an integer")
        return
        
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        print(f"Removed: {removed['task']}")
    else:
        print("Invalid index")


def list_todos(filter_tag: Optional[str] = None) -> None:
    """
    Display all todo items, optionally filtered by a single tag.
    
    Args:
        filter_tag: Optional tag to filter todos
        
    Example:
        list_todos()  # Show all
        list_todos(filter_tag="work")  # Show only work-related
    """
    display_todos = todos
    
    if filter_tag:
        filter_tag = filter_tag.lower().strip()
        display_todos = [todo for todo in todos if filter_tag in todo.get("tags", [])]
        
        if not display_todos:
            print(f"No todos found with tag '{filter_tag}'")
            return
    
    if not display_todos:
        print("No todos found")
        return
    
    print("\nTodo List:")
    if filter_tag:
        print(f"(Filtered by tag: {filter_tag})")
    print("-" * 60)
    
    for i, todo in enumerate(display_todos):
        status = "✓" if todo["completed"] else " "
        tags = todo.get("tags", [])
        tags_str = f" [Tags: {', '.join(tags)}]" if tags else ""
        
        # Find the original index for filtered lists
        original_index = todos.index(todo) if filter_tag else i
        print(f"{original_index}. [{status}] {todo['task']}{tags_str}")
    
    print("-" * 60)


def mark_complete(index: int) -> None:
    """
    Mark a todo as completed.
    
    Args:
        index: The index of the todo to mark as complete
    """
    if not isinstance(index, int):
        print("Error: Index must be an integer")
        return
        
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
        print(f"Completed: {todos[index]['task']}")
    else:
        print("Invalid index")


def filter_by_tags(tags: List[str], match_all: bool = False) -> List[Dict[str, Any]]:
    """
    Filter todos by multiple tags with AND/OR logic.
    
    Args:
        tags: List of tags to filter by
        match_all: If True, use AND logic (task must have all tags).
                  If False, use OR logic (task must have at least one tag).
    
    Returns:
        List of todos matching the filter criteria
        
    Example:
        filter_by_tags(["work", "urgent"], match_all=True)  # AND logic
        filter_by_tags(["work", "personal"], match_all=False)  # OR logic
    """
    if not isinstance(tags, list):
        print("Error: Tags must be a list")
        return []
    
    if not tags:
        return []
    
    # Normalize search tags
    normalized_tags = [tag.lower().strip() for tag in tags if isinstance(tag, str) and tag.strip()]
    
    if not normalized_tags:
        return []
    
    if match_all:
        # AND logic: task must have all tags
        filtered = [
            todo for todo in todos
            if all(tag in todo.get("tags", []) for tag in normalized_tags)
        ]
    else:
        # OR logic: task must have at least one tag
        filtered = [
            todo for todo in todos
            if any(tag in todo.get("tags", []) for tag in normalized_tags)
        ]
    
    return filtered


def show_tag_stats() -> None:
    """
    Display statistics about tag usage across all todos.
    
    Shows each tag and the count of todos using that tag.
    """
    if not todos:
        print("No todos found")
        return
    
    tag_counts: Dict[str, int] = {}
    
    for todo in todos:
        for tag in todo.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    if not tag_counts:
        print("No tags found")
        return
    
    print("\nTag Statistics:")
    print("-" * 40)
    
    # Sort by count (descending) then by name
    sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
    
    for tag, count in sorted_tags:
        print(f"{tag}: {count}")
    
    print("-" * 40)
    print(f"Total unique tags: {len(tag_counts)}")


def add_tag_to_task(index: int, tag: str) -> None:
    """
    Add a tag to an existing todo item.
    
    Args:
        index: The index of the todo
        tag: The tag to add
        
    Example:
        add_tag_to_task(0, "urgent")
    """
    if not isinstance(index, int):
        print("Error: Index must be an integer")
        return
    
    if not isinstance(tag, str) or not tag.strip():
        print("Error: Tag must be a non-empty string")
        return
    
    if 0 <= index < len(todos):
        normalized_tag = tag.lower().strip()
        
        if "tags" not in todos[index]:
            todos[index]["tags"] = []
        
        if normalized_tag in todos[index]["tags"]:
            print(f"Tag '{normalized_tag}' already exists on this task")
        else:
            todos[index]["tags"].append(normalized_tag)
            print(f"Added tag '{normalized_tag}' to: {todos[index]['task']}")
    else:
        print("Invalid index")


def remove_tag_from_task(index: int, tag: str) -> None:
    """
    Remove a tag from an existing todo item.
    
    Args:
        index: The index of the todo
        tag: The tag to remove
        
    Example:
        remove_tag_from_task(0, "urgent")
    """
    if not isinstance(index, int):
        print("Error: Index must be an integer")
        return
    
    if not isinstance(tag, str) or not tag.strip():
        print("Error: Tag must be a non-empty string")
        return
    
    if 0 <= index < len(todos):
        normalized_tag = tag.lower().strip()
        
        if "tags" not in todos[index] or normalized_tag not in todos[index]["tags"]:
            print(f"Tag '{normalized_tag}' not found on this task")
        else:
            todos[index]["tags"].remove(normalized_tag)
            print(f"Removed tag '{normalized_tag}' from: {todos[index]['task']}")
    else:
        print("Invalid index")


def list_all_tags() -> List[str]:
    """
    Get a sorted list of all unique tags used across all todos.
    
    Returns:
        Sorted list of unique tag names
        
    Example:
        tags = list_all_tags()  # ["personal", "urgent", "work"]
    """
    all_tags = set()
    
    for todo in todos:
        all_tags.update(todo.get("tags", []))
    
    return sorted(all_tags)


def main() -> None:
    """Main application loop with interactive menu."""
    print("=== Todo List with Tags ===")
    
    while True:
        print("\nCommands: add, list, complete, remove, filter, stats, addtag, removetag, tags, quit")
        command = input("> ").strip().lower()
        
        try:
            if command == "add":
                task = input("Enter task: ").strip()
                if not task:
                    print("Task cannot be empty")
                    continue
                
                tags_input = input("Enter tags (comma-separated, optional): ").strip()
                tags = [t.strip() for t in tags_input.split(",")] if tags_input else None
                add_todo(task, tags)
                
            elif command == "list":
                filter_input = input("Filter by tag (optional, press Enter to skip): ").strip()
                list_todos(filter_tag=filter_input if filter_input else None)
                
            elif command == "complete":
                list_todos()
                if todos:
                    index_str = input("Enter index to complete: ").strip()
                    if index_str.isdigit():
                        mark_complete(int(index_str))
                    else:
                        print("Invalid input")
                        
            elif command == "remove":
                list_todos()
                if todos:
                    index_str = input("Enter index to remove: ").strip()
                    if index_str.isdigit():
                        remove_todo(int(index_str))
                    else:
                        print("Invalid input")
                        
            elif command == "filter":
                tags_input = input("Enter tags to filter (comma-separated): ").strip()
                if not tags_input:
                    print("No tags provided")
                    continue
                
                tags = [t.strip() for t in tags_input.split(",")]
                match_all_input = input("Match ALL tags? (y/n, default=n): ").strip().lower()
                match_all = match_all_input == "y"
                
                filtered = filter_by_tags(tags, match_all=match_all)
                
                if filtered:
                    logic = "AND" if match_all else "OR"
                    print(f"\nFiltered Results ({logic} logic):")
                    print("-" * 60)
                    for todo in filtered:
                        status = "✓" if todo["completed"] else " "
                        tags_str = f" [Tags: {', '.join(todo.get('tags', []))}]" if todo.get("tags") else ""
                        original_index = todos.index(todo)
                        print(f"{original_index}. [{status}] {todo['task']}{tags_str}")
                    print("-" * 60)
                else:
                    print("No matching todos found")
                    
            elif command == "stats":
                show_tag_stats()
                
            elif command == "addtag":
                list_todos()
                if todos:
                    index_str = input("Enter task index: ").strip()
                    if index_str.isdigit():
                        tag = input("Enter tag to add: ").strip()
                        add_tag_to_task(int(index_str), tag)
                    else:
                        print("Invalid input")
                        
            elif command == "removetag":
                list_todos()
                if todos:
                    index_str = input("Enter task index: ").strip()
                    if index_str.isdigit():
                        tag = input("Enter tag to remove: ").strip()
                        remove_tag_from_task(int(index_str), tag)
                    else:
                        print("Invalid input")
                        
            elif command == "tags":
                all_tags = list_all_tags()
                if all_tags:
                    print(f"\nAll tags: {', '.join(all_tags)}")
                else:
                    print("No tags found")
                    
            elif command == "quit":
                print("Goodbye!")
                break
                
            else:
                print("Unknown command")
                
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
