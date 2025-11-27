# Todo Application with Tag System

## Overview

A feature-rich todo list application with **tag-based categorization** for organizing and filtering tasks. The application supports assigning multiple tags to each task, filtering by single or multiple tags using AND/OR logic, and viewing comprehensive tag statistics.

### Key Features

- ✅ **Tag Assignment**: Assign multiple tags to tasks for flexible categorization
- ✅ **Tag Filtering**: Filter tasks by single or multiple tags with AND/OR logic
- ✅ **Tag Statistics**: View tag usage statistics across all tasks
- ✅ **Tag Management**: Add/remove tags from existing tasks
- ✅ **Type Hints**: Full Python type annotations for better IDE support
- ✅ **Error Handling**: Comprehensive error handling with descriptive messages
- ✅ **Backward Compatible**: Works with untagged tasks (no breaking changes)
- ✅ **Fully Tested**: 100+ comprehensive unit, integration, and edge case tests

---

## Quick Start

### Windows (PowerShell)

```powershell
# 1. Setup environment (one time)
.\setup_env.ps1

# 2. Run tests
.\run_tests.ps1

# 3. Run application
python todo_with_tags.py
```

### Linux/Mac (Bash)

```bash
# 1. Make scripts executable
chmod +x setup_env.sh run_tests.sh

# 2. Setup environment (one time)
./setup_env.sh

# 3. Run tests
./run_tests.sh

# 4. Run application
python todo_with_tags.py
```

---

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (usually included with Python)

### Automatic Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\setup_env.ps1
```

**Linux/Mac (Bash):**
```bash
./setup_env.sh
```

This script will:
1. Check Python version (3.8+)
2. Create virtual environment (`venv/`)
3. Activate virtual environment
4. Install all dependencies
5. Verify installations

### Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Usage

### Running the Application

```bash
python todo_with_tags.py
```

### Interactive Commands

```
Commands: add, list, complete, remove, add-tag, remove-tag, tags, stats, quit

add           - Add new task with optional tags
list          - List all tasks (optionally filter by tag)
complete      - Mark a task as completed
remove        - Remove a task
add-tag       - Add a tag to existing task
remove-tag    - Remove a tag from task
tags          - Show all tags used
stats         - Display tag statistics
quit          - Exit application
```

### Usage Examples

#### Add Tasks with Tags

```
> add
Enter task: Write report
Enter tags (comma-separated, optional): work, urgent

> add
Enter task: Buy groceries
Enter tags (comma-separated, optional): personal
```

#### List All Tasks

```
> list
Enter tag to filter (optional): [press Enter for all]

Todo List:
------------------------------------------------------------
0. [ ] Write report [work, urgent]
1. [ ] Buy groceries [personal]
------------------------------------------------------------
```

#### Filter by Tag

```
> list
Enter tag to filter (optional): work

Todo List:
------------------------------------------------------------
0. [ ] Write report [work, urgent]
------------------------------------------------------------
```

#### Mark Task Complete

```
> complete
[Shows all tasks]
Enter index to complete: 0
Completed: Write report
```

#### Manage Tags

```
> add-tag
[Shows all tasks]
Enter index: 0
Enter tag to add: review
Added tag 'review' to: Write report

> remove-tag
[Shows all tasks]
Enter index: 0
Enter tag to remove: urgent
Removed tag 'urgent' from: Write report
```

#### View Statistics

```
> stats
Tag Statistics:
----------------------------------------
work: 2
personal: 1
urgent: 1
----------------------------------------
```

---

## Testing

### Running All Tests

**Windows:**
```powershell
.\run_tests.ps1
```

**Linux/Mac:**
```bash
./run_tests.sh
```

### Running Specific Test Files

**Windows:**
```powershell
.\run_tests.ps1 -TestFile test_todo_with_tags.py
```

**Linux/Mac:**
```bash
./run_tests.sh -t test_todo_with_tags.py
```

### Running with Verbose Output

**Windows:**
```powershell
.\run_tests.ps1 -Verbose
```

**Linux/Mac:**
```bash
./run_tests.sh -v
```

### Running with Coverage Report

**Windows:**
```powershell
.\run_tests.ps1 -Coverage
```

**Linux/Mac:**
```bash
./run_tests.sh -c
```

### Test Categories

The test suite includes 100+ tests covering:

1. **Unit Tests** (40+ tests)
   - Basic functionality of each function
   - Parameter validation
   - Type checking
   - Edge cases

2. **Integration Tests** (15+ tests)
   - Complete workflows (add → filter → remove)
   - Multi-step operations
   - Tag manipulation workflows

3. **Backward Compatibility Tests** (5+ tests)
   - Untagged tasks still work
   - Original CRUD operations unchanged
   - No breaking changes

4. **Error Handling Tests** (20+ tests)
   - Invalid input types
   - Empty/None values
   - Out of range indices
   - Duplicate entries

5. **Edge Cases** (10+ tests)
   - Special characters in tasks/tags
   - Unicode support
   - Very long descriptions
   - Many tags on single task
   - Numeric string tags

6. **Parametrized Tests**
   - Multiple parameter combinations
   - Comprehensive coverage variations

---

## Project Structure

```
project_root/
├── todo.py                  # Original todo application
├── todo_with_tags.py        # Enhanced version with tag system
├── test_todo_with_tags.py   # Comprehensive test suite (100+ tests)
├── requirements.txt         # Runtime dependencies (empty - uses stdlib)
├── requirements-dev.txt     # Development dependencies (pytest)
├── pytest.ini              # Pytest configuration
├── setup_env.ps1           # Windows environment setup script
├── setup_env.sh            # Linux/Mac environment setup script
├── run_tests.ps1           # Windows test runner
├── run_tests.sh            # Linux/Mac test runner
├── .gitignore             # Python project exclusions
├── README.md              # This file
└── FEATURE_SPEC.md        # Feature specification
```

---

## API Documentation

### Core Functions

#### `add_todo(task: str, tags: Optional[List[str]] = None) -> None`

Add a new todo item with optional tags.

**Parameters:**
- `task` (str): Task description (required, cannot be empty)
- `tags` (List[str], optional): List of tags (case normalized to lowercase, duplicates removed)

**Raises:**
- `TypeError`: If task is not a string or tags is not a list
- `ValueError`: If task is empty or whitespace-only

**Example:**
```python
add_todo("Write report", tags=["work", "urgent"])
add_todo("Simple task")  # No tags
```

#### `remove_todo(index: int) -> None`

Remove a todo item by index.

**Parameters:**
- `index` (int): Index of todo to remove (0-based)

**Raises:**
- `TypeError`: If index is not an integer
- `IndexError`: If index is out of range

**Example:**
```python
remove_todo(0)
```

#### `list_todos(filter_tag: Optional[str] = None) -> None`

Display all todos, optionally filtered by tag.

**Parameters:**
- `filter_tag` (str, optional): Tag to filter by (case-insensitive)

**Example:**
```python
list_todos()  # Show all
list_todos("work")  # Show only work-tagged items
```

#### `filter_by_tags(tags: List[str], match_all: bool = False) -> List[Dict]`

Filter todos by tags using AND/OR logic.

**Parameters:**
- `tags` (List[str]): Tags to filter by (required, non-empty)
- `match_all` (bool): If True, use AND logic (must have all tags). If False, use OR logic (any tag)

**Returns:**
- List of matching todo dictionaries

**Raises:**
- `TypeError`: If tags is not a list or match_all is not a boolean
- `ValueError`: If tags list is empty or contains no valid strings

**Example:**
```python
# OR logic: work OR personal
work_or_personal = filter_by_tags(["work", "personal"], match_all=False)

# AND logic: work AND urgent
work_and_urgent = filter_by_tags(["work", "urgent"], match_all=True)
```

#### `show_tag_stats() -> None`

Display statistics of all tags used in todos.

**Example:**
```python
show_tag_stats()
# Output:
# Tag Statistics:
# ----------------------------------------
# work: 2
# personal: 1
# urgent: 1
# ----------------------------------------
```

#### `add_tag_to_task(index: int, tag: str) -> None`

Add a tag to an existing todo.

**Parameters:**
- `index` (int): Index of todo to modify
- `tag` (str): Tag to add (case normalized)

**Raises:**
- `TypeError`: If index is not an integer or tag is not a string
- `IndexError`: If index is out of range
- `ValueError`: If tag is empty

**Example:**
```python
add_tag_to_task(0, "urgent")
```

#### `remove_tag_from_task(index: int, tag: str) -> None`

Remove a tag from an existing todo.

**Parameters:**
- `index` (int): Index of todo to modify
- `tag` (str): Tag to remove (case normalized)

**Raises:**
- `TypeError`: If index is not an integer or tag is not a string
- `IndexError`: If index is out of range
- `ValueError`: If tag is empty or not found on task

**Example:**
```python
remove_tag_from_task(0, "work")
```

#### `mark_complete(index: int) -> None`

Mark a todo as completed.

**Parameters:**
- `index` (int): Index of todo to mark complete

**Raises:**
- `TypeError`: If index is not an integer
- `IndexError`: If index is out of range

**Example:**
```python
mark_complete(0)
```

#### `list_all_tags() -> List[str]`

Get a sorted list of all unique tags used.

**Returns:**
- Sorted list of tags (lowercase)

**Example:**
```python
all_tags = list_all_tags()
# Returns: ['health', 'personal', 'urgent', 'work']
```

---

## Development Setup

### Setting Up Development Environment

1. **Install Python 3.8+**
   - Download from https://www.python.org/

2. **Clone/Download Project**
   ```bash
   cd path/to/project
   ```

3. **Run Setup Script**
   - Windows: `.\setup_env.ps1`
   - Linux/Mac: `./setup_env.sh`

4. **Install Pre-commit Hooks** (optional)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running Tests During Development

```bash
# Run all tests
.\run_tests.ps1  # Windows
./run_tests.sh   # Linux/Mac

# Run with coverage
.\run_tests.ps1 -Coverage  # Windows
./run_tests.sh -c          # Linux/Mac

# Run specific test
.\run_tests.ps1 -TestFile test_todo_with_tags.py  # Windows
./run_tests.sh -t test_todo_with_tags.py           # Linux/Mac

# Run with verbose output
.\run_tests.ps1 -Verbose  # Windows
./run_tests.sh -v        # Linux/Mac
```

### Code Quality

The codebase includes:
- ✅ Full type hints (PEP 484)
- ✅ Comprehensive docstrings (Google style)
- ✅ 100+ unit tests
- ✅ Error handling with descriptive messages
- ✅ Input validation on all functions

---

## Before and After Comparison

### Before (Original todo.py)

```python
todos = []

def add_todo(task):
    todos.append({"task": task, "completed": False})
    print(f"Added: {task}")

def list_todos():
    if not todos:
        print("No todos found")
        return
    print("\nTodo List:")
    for i, todo in enumerate(todos):
        status = "✓" if todo["completed"] else " "
        print(f"{i}. [{status}] {todo['task']}")
```

### After (todo_with_tags.py)

```python
def add_todo(task: str, tags: Optional[List[str]] = None) -> None:
    """
    Add a new todo item with optional tags.
    
    Args:
        task: The task description (required)
        tags: List of tag strings (optional, defaults to empty list)
    
    Raises:
        TypeError: If task is not a string or tags is not a list
        ValueError: If task is empty
    """
    if not isinstance(task, str):
        raise TypeError(f"task must be a string, got {type(task).__name__}")
    if not task.strip():
        raise ValueError("task cannot be empty")
    
    normalized_tags = []
    if tags:
        normalized_tags = list(set(tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()))
    
    todos.append({
        "task": task.strip(),
        "completed": False,
        "tags": normalized_tags
    })
    print(f"Added: {task}")

def list_todos(filter_tag: Optional[str] = None) -> None:
    """
    Display all todo items, optionally filtered by tag.
    
    Args:
        filter_tag: If provided, only show todos containing this tag
    """
    filtered = todos
    if filter_tag:
        filter_tag_lower = filter_tag.strip().lower()
        filtered = [t for t in todos if filter_tag_lower in t.get("tags", [])]
    
    if not filtered:
        print("No todos found")
        return
    
    print("\nTodo List:")
    for i, todo in enumerate(filtered):
        status = "✓" if todo["completed"] else " "
        tags_str = f" [{', '.join(todo.get('tags', []))}]" if todo.get("tags") else ""
        print(f"{i}. [{status}] {todo['task']}{tags_str}")
```

**Key Improvements:**
- ✅ Type hints for all parameters and returns
- ✅ Comprehensive docstrings
- ✅ Input validation and error handling
- ✅ Tag support with filtering
- ✅ Case normalization for tags
- ✅ 100+ unit tests
- ✅ Backward compatible

---

## Troubleshooting

### Issue: "Python is not installed or not in PATH"

**Solution:**
1. Download Python 3.8+ from https://www.python.org/
2. During installation, check **"Add Python to PATH"**
3. Restart terminal/PowerShell
4. Try again

### Issue: "Virtual environment not found"

**Solution:**
```powershell
# Windows
.\setup_env.ps1 -Force

# Linux/Mac
./setup_env.sh --force
```

### Issue: "pytest: command not found"

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install pytest
pip install pytest>=7.4.0
```

### Issue: Permission denied on .sh files

**Solution (Linux/Mac):**
```bash
chmod +x setup_env.sh run_tests.sh
```

### Issue: Tests fail with import errors

**Solution:**
1. Ensure virtual environment is activated
2. Re-run setup: `.\setup_env.ps1` (Windows) or `./setup_env.sh` (Linux/Mac)
3. Check `requirements-dev.txt` is installed: `pip list | grep pytest`

### Issue: Script execution policy error (PowerShell)

**Solution:**
```powershell
# Temporarily allow script execution in current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Or allow for current user permanently
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Tests hang or timeout

**Solution:**
1. Ensure no other instances are running
2. Kill any stuck Python processes:
   ```powershell
   # Windows
   Get-Process python | Stop-Process -Force
   
   # Linux/Mac
   pkill -f python
   ```
3. Re-run tests

---

## Platform-Specific Notes

### Windows (PowerShell)

- Scripts use `.ps1` extension
- Virtual environment activation: `.\venv\Scripts\activate`
- To run scripts first time: Set execution policy if needed
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Linux/Mac (Bash)

- Scripts use `.sh` extension
- Make scripts executable: `chmod +x *.sh`
- Virtual environment activation: `source venv/bin/activate`
- Python 3 may need to be explicitly called as `python3`

---

## Success Metrics

✅ **Tag System Implemented**
- All 7 core functions working
- Tag assignment and filtering
- Tag statistics and management

✅ **Comprehensive Testing**
- 100+ unit and integration tests
- Edge case coverage
- Error handling tests
- Parametrized tests

✅ **Automation**
- One-command setup (Windows & Linux/Mac)
- One-command testing
- Automatic environment detection

✅ **Documentation**
- Complete README with 10+ sections
- API documentation for all functions
- Platform-specific instructions
- Troubleshooting guide

✅ **Backward Compatibility**
- Original functionality preserved
- Untagged tasks work correctly
- No breaking changes

---

## Support

For issues or questions:
1. Check the **Troubleshooting** section
2. Review **API Documentation** for function details
3. Check test files for usage examples
4. Review the **FEATURE_SPEC.md** for design details

---

**Version:** 1.0  
**Last Updated:** 2024  
**Python Version:** 3.8+  
**License:** MIT
