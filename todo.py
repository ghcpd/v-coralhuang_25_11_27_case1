"""
Simple Todo List Application
Basic CRUD operations only
"""

todos = []

def add_todo(task):
    """Add a new todo item"""
    todos.append({"task": task, "completed": False})
    print(f"Added: {task}")

def remove_todo(index):
    """Remove a todo item by index"""
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        print(f"Removed: {removed['task']}")
    else:
        print("Invalid index")

def list_todos():
    """Display all todo items"""
    if not todos:
        print("No todos found")
        return
    
    print("\nTodo List:")
    print("-" * 40)
    for i, todo in enumerate(todos):
        status = "✓" if todo["completed"] else " "
        print(f"{i}. [{status}] {todo['task']}")
    print("-" * 40)

def mark_complete(index):
    """Mark a todo as completed"""
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
        print(f"Completed: {todos[index]['task']}")
    else:
        print("Invalid index")

def main():
    """Main application loop"""
    print("=== Simple Todo List ===")
    
    while True:
        print("\nCommands: add, list, complete, remove, quit")
        command = input("> ").strip().lower()
        
        if command == "add":
            task = input("Enter task: ")
            add_todo(task)
        elif command == "list":
            list_todos()
        elif command == "complete":
            list_todos()
            index = int(input("Enter index to complete: "))
            mark_complete(index)
        elif command == "remove":
            list_todos()
            index = int(input("Enter index to remove: "))
            remove_todo(index)
        elif command == "quit":
            print("Goodbye!")
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
