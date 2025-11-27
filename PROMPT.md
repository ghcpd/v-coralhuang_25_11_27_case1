# Task: Add Tag System to Basic Todo Application

You are a software engineer tasked with enhancing a minimal todo list application. Your goal is to analyze the existing code, identify its limitations, and propose a **new feature** that adds significant value.

---

## Goal
Propose and implement a tag-based categorization and filtering system that allows users to organize and find tasks efficiently.

---

## Proposed New Feature: Tag System

### Feature Description
Add ability to:
1. **Assign tags** to tasks (multiple tags per task)
2. **Filter by tags** (show only tasks with specific tags)
3. **View tag statistics** (count tasks per tag)
4. **Combine filters** (AND/OR logic for multiple tags)

### Example Usage
```python
# Add task with tags
add_todo("Write project report", tags=["work", "urgent"])
add_todo("Buy groceries", tags=["personal", "shopping"])
add_todo("Review code PR", tags=["work", "code-review"])

# Filter by single tag
list_todos(filter_tag="work")  # Shows 2 tasks

# Filter by multiple tags (AND logic)
list_todos(filter_tags=["work", "urgent"], match_all=True)  # Shows 1 task

# Show tag statistics
show_tag_stats()
# Output:
# work (2)
# personal (1)
# urgent (1)
# shopping (1)
# code-review (1)
```

---

## Expected Deliverables

### 1. Feature Specification Document
- **Problem statement**: Why this feature is needed
- **Use cases**: At least 3 real-world scenarios
- **Feature requirements**: Functional and non-functional
- **Success metrics**: How to measure feature success

### 2. Enhanced Code Implementation
- `todo_original.py` - Keep original as reference
- `todo_with_tags.py` - Implement tag system with:
  - Type hints and docstrings
  - Backward compatibility (works with existing tasks)
  - Clean, maintainable code
  - Error handling

### 3. Implementation Requirements

**New/Modified Functions**:
```python
def add_todo(task: str, tags: list[str] = None) -> None:
    """Add task with optional tags"""
    
def list_todos(filter_tag: str = None) -> None:
    """List tasks, optionally filtered by tag"""
    
def filter_by_tags(tags: list[str], match_all: bool = False) -> list:
    """Filter tasks by multiple tags with AND/OR logic"""
    
def show_tag_stats() -> None:
    """Display statistics for all tags"""
    
def add_tag_to_task(index: int, tag: str) -> None:
    """Add tag to existing task"""
    
def remove_tag_from_task(index: int, tag: str) -> None:
    """Remove tag from task"""
    
def list_all_tags() -> list[str]:
    """Get all unique tags used in system"""
```

### 4. Documentation
- `README.md` - Feature overview, usage examples, setup instructions
- `FEATURE_SPEC.md` - Detailed feature specification
- Before/after comparison showing improvement

---

## Project Structure

```
project_root/
├── todo_original.py              # Original baseline (reference)
├── todo_with_tags.py             # Enhanced with tag system
├── README.md                     # Feature overview and usage examples
└── FEATURE_SPEC.md               # Detailed feature specification
```

---

## Feature Requirements

### Functional Requirements
1. Tasks can have 0 or more tags
2. Tags are case-insensitive strings
3. Filter tasks by single tag
4. Filter tasks by multiple tags (AND/OR logic)
5. View all unique tags in system
6. View task count per tag
7. Add/remove tags from existing tasks
8. Backward compatible with untagged tasks

### Non-Functional Requirements
1. Clean, readable code with type hints
2. Comprehensive error handling
3. User-friendly command interface

### Success Metrics
- Feature allows categorizing tasks efficiently
- Filtering reduces visible tasks by 50-90% (depending on filter)
- User can find tasks 3x faster with tags vs scrolling
- Zero breaking changes to existing functionality

---

## Rationale

### Why This Feature?
1. **Flexibility**: Tags are more flexible than rigid categories
2. **Scalability**: Works well as task list grows
3. **Discoverability**: Easy to find related tasks
4. **Minimal overhead**: Simple to implement, easy to use
5. **Common pattern**: Users familiar with tags from other apps

### Fits Product Roadmap
- Aligns with "improve task organization" goal
- Addresses user pain point: "hard to find tasks"
- Low complexity, high value feature
- Foundation for future features (tag colors, tag hierarchies)

---

## Implementation Hints

### Data Structure Change
```python
# Before
todos = [{"task": "...", "completed": False}]

# After
todos = [{"task": "...", "completed": False, "tags": ["work", "urgent"]}]
```

### Filtering Logic
```python
# Single tag
filtered = [t for t in todos if filter_tag in t.get("tags", [])]

# Multiple tags (AND)
filtered = [t for t in todos if all(tag in t.get("tags", []) for tag in filter_tags)]

# Multiple tags (OR)
filtered = [t for t in todos if any(tag in t.get("tags", []) for tag in filter_tags)]
```

---

## Execution Plan

1. Analyze the provided `todo.py` and identify limitations
2. Design tag system architecture
3. Create `FEATURE_SPEC.md` with detailed requirements and rationale
4. Implement `todo_with_tags.py` with the new tag system
5. Write `README.md` with feature overview and usage examples
6. Provide before/after comparison demonstrating the improvement

**Proceed**: Analyze → Design → Specify → Implement → Document
