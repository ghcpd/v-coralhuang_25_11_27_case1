# Feature Specification: Tag System for Todo Application

## Executive Summary

This document defines the tag-based categorization system for the todo application. The system enables users to assign multiple tags to tasks, filter by tags using AND/OR logic, view statistics, and manage tags dynamically. The implementation prioritizes backward compatibility, comprehensive testing, and ease of use.

---

## Problem Statement

The original todo application had no way to categorize or organize tasks beyond a linear list. Users needed:

1. **Organization**: Group related tasks without losing other context
2. **Filtering**: Quickly find tasks by category/type
3. **Analysis**: Understand task distribution across categories
4. **Flexibility**: Assign multiple categories per task
5. **Dynamic Management**: Add/remove categories from tasks

**Example Scenario:**
```
User has tasks:
- "Write report" (work, urgent, review)
- "Buy groceries" (personal)
- "Call dentist" (personal, health)
- "Review code" (work, review)

User wants to see only "work" items or find tasks that are both "work" AND "urgent"
```

---

## Use Cases

### Use Case 1: Task Organization
**Actor:** Daily planner  
**Scenario:** User wants to organize tasks by multiple categories

```
1. User adds task "Write report" with tags ["work", "urgent", "review"]
2. System stores task with all tags normalized to lowercase
3. System prevents duplicate tags
4. Display shows: "1. [ ] Write report [work, urgent, review]"
```

**Success Criteria:**
- Tags stored correctly
- Duplicates removed
- Display includes tags
- Case-normalized storage

### Use Case 2: Single-Tag Filtering
**Actor:** Work-focused user  
**Scenario:** User wants to see only work-related tasks

```
1. User executes list_todos("work")
2. System filters to tasks containing "work" tag
3. System displays: "Write report" and "Review code"
4. Untagged and non-matching tasks hidden
```

**Success Criteria:**
- Correct filtering
- Case-insensitive matching
- No false positives/negatives

### Use Case 3: Multi-Tag AND Filtering
**Actor:** Manager  
**Scenario:** User wants urgent work tasks

```
1. User calls filter_by_tags(["work", "urgent"], match_all=True)
2. System returns only tasks with BOTH tags
3. Returns only "Write report"
4. Excludes "Review code" (has work but not urgent)
```

**Success Criteria:**
- AND logic working
- All specified tags required
- Correct filtering

### Use Case 4: Multi-Tag OR Filtering
**Actor:** Busy professional  
**Scenario:** User wants work or personal tasks (all non-health tasks)

```
1. User calls filter_by_tags(["work", "personal"], match_all=False)
2. System returns tasks with ANY of the tags
3. Returns 3 tasks: "Write report", "Buy groceries", "Review code"
4. Excludes "Call dentist" (only has "health", not in filter)
```

**Success Criteria:**
- OR logic working
- Any tag matches
- Correct filtering

### Use Case 5: Dynamic Tag Management
**Actor:** Task maintainer  
**Scenario:** User changes task categorization

```
1. User adds "work" tag to "Buy groceries" (now work + personal)
2. System prevents duplicate tags
3. User removes "personal" tag from "Buy groceries" (now only work)
4. Tags updated immediately
```

**Success Criteria:**
- Tags added successfully
- Tags removed successfully
- Duplicates prevented
- Changes immediately visible

### Use Case 6: Tag Statistics
**Actor:** Analyst  
**Scenario:** User wants overview of task distribution

```
1. User calls show_tag_stats()
2. System displays:
   - work: 2
   - urgent: 1
   - review: 2
   - personal: 2
   - health: 1
3. Tags sorted by frequency then alphabetically
```

**Success Criteria:**
- Accurate counts
- Clear presentation
- Sorted output

### Use Case 7: Tag Listing
**Actor:** Reference-seeking user  
**Scenario:** User wants to see all available tags

```
1. User calls list_all_tags()
2. System returns: ['health', 'personal', 'review', 'urgent', 'work']
3. Tags sorted alphabetically
4. No duplicates
```

**Success Criteria:**
- All tags returned
- Sorted alphabetically
- No duplicates

---

## Requirements

### Functional Requirements

#### FR1: Tag Assignment
- **FR1.1:** Users can assign multiple tags when adding a task
- **FR1.2:** Tags are optional (tasks without tags supported)
- **FR1.3:** Tags are normalized to lowercase for consistency
- **FR1.4:** Duplicate tags are automatically removed
- **FR1.5:** Whitespace in tags is trimmed
- **FR1.6:** Tags can contain alphanumeric characters and common symbols

#### FR2: Tag Filtering
- **FR2.1:** Users can filter by a single tag
- **FR2.2:** Filtering is case-insensitive
- **FR2.3:** Users can filter by multiple tags with AND logic (all tags required)
- **FR2.4:** Users can filter by multiple tags with OR logic (any tag matches)
- **FR2.5:** Filtered results exclude untagged tasks when applicable
- **FR2.6:** Empty filter results handled gracefully

#### FR3: Tag Management
- **FR3.1:** Users can add tags to existing tasks
- **FR3.2:** Users can remove tags from existing tasks
- **FR3.3:** Adding duplicate tags is prevented with feedback
- **FR3.4:** Removing non-existent tags raises error with feedback
- **FR3.5:** All tag operations are immediate (no delay)

#### FR4: Tag Statistics
- **FR4.1:** Tag statistics show count of tasks using each tag
- **FR4.2:** Statistics are accurate and up-to-date
- **FR4.3:** Uncompleted and completed tasks both count in statistics
- **FR4.4:** Statistics sorted by frequency (descending) then alphabetically
- **FR4.5:** Empty tag list handled gracefully

#### FR5: Tag Listing
- **FR5.1:** Users can retrieve list of all unique tags
- **FR5.2:** Tags returned in sorted alphabetical order
- **FR5.3:** No duplicate tags in list
- **FR5.4:** Empty tag list handled gracefully

#### FR6: Backward Compatibility
- **FR6.1:** Tasks without tags work correctly
- **FR6.2:** Original CRUD operations unchanged
- **FR6.3:** No breaking changes to existing API
- **FR6.4:** Untagged tasks don't cause errors

#### FR7: Error Handling
- **FR7.1:** Invalid task type raises TypeError
- **FR7.2:** Empty task raises ValueError
- **FR7.3:** Invalid tags type raises TypeError
- **FR7.4:** Invalid index raises IndexError
- **FR7.5:** All errors include descriptive messages

### Non-Functional Requirements

#### NFR1: Performance
- **NFR1.1:** Adding task completes in < 10ms
- **NFR1.2:** Filtering 1000 tasks completes in < 100ms
- **NFR1.3:** Tag operations complete in < 10ms

#### NFR2: Usability
- **NFR2.1:** User can setup and run tests in < 5 minutes
- **NFR2.2:** One-command setup on Windows and Linux/Mac
- **NFR2.3:** One-command testing
- **NFR2.4:** Clear error messages for troubleshooting

#### NFR3: Testing
- **NFR3.1:** 100+ automated tests covering all functions
- **NFR3.2:** Unit tests for individual functions
- **NFR3.3:** Integration tests for workflows
- **NFR3.4:** Edge case coverage
- **NFR3.5:** Test pass rate 100%

#### NFR4: Code Quality
- **NFR4.1:** Full type hints (PEP 484)
- **NFR4.2:** Comprehensive docstrings (Google style)
- **NFR4.3:** Error handling on all functions
- **NFR4.4:** Input validation on all parameters

#### NFR5: Documentation
- **NFR5.1:** README with 10+ sections
- **NFR5.2:** API documentation for all functions
- **NFR5.3:** Platform-specific instructions (Windows/Linux/Mac)
- **NFR5.4:** Troubleshooting guide
- **NFR5.5:** Usage examples

---

## Architecture

### Data Structure

```python
# Tag-enhanced todo item structure
{
    "task": "Write report",           # str: task description
    "completed": False,               # bool: completion status
    "tags": ["work", "urgent", "review"]  # list[str]: normalized tags
}

# Global todos list
todos = [
    {"task": "Task 1", "completed": False, "tags": ["work"]},
    {"task": "Task 2", "completed": True, "tags": ["personal", "health"]},
    ...
]
```

### Tag Normalization

All tags undergo the following normalization:
1. Strip whitespace (leading/trailing)
2. Convert to lowercase
3. Remove duplicates (set conversion)
4. Filter out empty strings

### Filter Logic

**OR Logic (match_all=False):**
```python
# Returns todos with ANY of the specified tags
result = [t for t in todos if any(tag in t.get("tags", []) for tag in filter_tags)]
```

**AND Logic (match_all=True):**
```python
# Returns todos with ALL of the specified tags
result = [t for t in todos if all(tag in t.get("tags", []) for tag in filter_tags)]
```

---

## API Functions

### 1. add_todo(task: str, tags: Optional[List[str]] = None) -> None

**Purpose:** Add new task with optional tags

**Parameters:**
- `task` (str): Task description
- `tags` (List[str], optional): Tags for task

**Behavior:**
- Normalizes tags (lowercase, duplicates removed)
- Validates input types
- Appends to global todos list
- Prints confirmation message

**Error Handling:**
- TypeError if task not string or tags not list
- ValueError if task empty or whitespace-only

---

### 2. list_todos(filter_tag: Optional[str] = None) -> None

**Purpose:** Display todos, optionally filtered by tag

**Parameters:**
- `filter_tag` (str, optional): Tag to filter by

**Behavior:**
- Filters by tag if provided (case-insensitive)
- Displays formatted list with completion status and tags
- Shows "No todos found" if list empty

**Error Handling:**
- TypeError if filter_tag not string

---

### 3. filter_by_tags(tags: List[str], match_all: bool = False) -> List[Dict]

**Purpose:** Get todos matching tag criteria

**Parameters:**
- `tags` (List[str]): Tags to filter by
- `match_all` (bool): AND logic if True, OR if False

**Returns:** List of matching todo dictionaries

**Behavior:**
- Normalizes filter tags to lowercase
- Applies AND or OR logic
- Returns empty list if no matches

**Error Handling:**
- TypeError if tags not list or match_all not bool
- ValueError if tags empty

---

### 4. show_tag_stats() -> None

**Purpose:** Display tag usage statistics

**Behavior:**
- Counts todos using each tag
- Displays sorted by count (descending) then name (ascending)
- Shows "No tags found" if none exist

---

### 5. add_tag_to_task(index: int, tag: str) -> None

**Purpose:** Add tag to existing task

**Parameters:**
- `index` (int): Task index
- `tag` (str): Tag to add

**Behavior:**
- Normalizes tag
- Prevents duplicate tags
- Updates task immediately
- Prints status message

**Error Handling:**
- TypeError if index not int or tag not string
- IndexError if index out of range
- ValueError if tag empty

---

### 6. remove_tag_from_task(index: int, tag: str) -> None

**Purpose:** Remove tag from existing task

**Parameters:**
- `index` (int): Task index
- `tag` (str): Tag to remove

**Behavior:**
- Normalizes tag
- Removes tag if exists
- Updates task immediately
- Prints status message

**Error Handling:**
- TypeError if index not int or tag not string
- IndexError if index out of range
- ValueError if tag empty or not found

---

### 7. list_all_tags() -> List[str]

**Purpose:** Get all unique tags

**Returns:** Sorted list of tag strings

**Behavior:**
- Collects all unique tags from todos
- Returns sorted alphabetically
- Returns empty list if no tags exist

---

## Testing Strategy

### Test Categories

1. **Unit Tests** (40+ tests)
   - Individual function tests
   - Parameter validation
   - Type checking
   - Return value verification

2. **Integration Tests** (15+ tests)
   - Multi-function workflows
   - Data consistency
   - End-to-end scenarios

3. **Edge Cases** (20+ tests)
   - Unicode characters
   - Special characters
   - Very long inputs
   - Empty collections
   - Boundary values

4. **Backward Compatibility** (5+ tests)
   - Untagged task support
   - Original API compatibility
   - No breaking changes

5. **Error Handling** (20+ tests)
   - Invalid input types
   - Out of range indices
   - Empty/None values
   - Duplicate operations

6. **Parametrized Tests**
   - Multiple input combinations
   - Comprehensive variations

### Test Tools

- **Framework:** pytest 7.4.0+
- **Fixtures:** Sample data for consistent testing
- **Parametrize:** Multiple test cases per function
- **Coverage:** Tracks code coverage

### Test Execution

```bash
# All tests
pytest test_todo_with_tags.py -v

# Specific test class
pytest test_todo_with_tags.py::TestAddTodo -v

# Specific test
pytest test_todo_with_tags.py::TestAddTodo::test_add_todo_basic -v

# With coverage
pytest test_todo_with_tags.py --cov=. --cov-report=html
```

---

## Success Criteria

### Implementation

✅ All 7 functions implemented with full functionality  
✅ Type hints on all functions  
✅ Comprehensive docstrings  
✅ Input validation and error handling  
✅ Backward compatible with original todo app  

### Testing

✅ 100+ tests covering all scenarios  
✅ Unit tests for each function  
✅ Integration tests for workflows  
✅ Edge case coverage  
✅ 100% test pass rate  

### Automation

✅ One-command setup (Windows: `.\setup_env.ps1`)  
✅ One-command setup (Linux/Mac: `./setup_env.sh`)  
✅ One-command testing (Windows: `.\run_tests.ps1`)  
✅ One-command testing (Linux/Mac: `./run_tests.sh`)  
✅ Automatic dependency installation  

### Documentation

✅ README with all required sections  
✅ API documentation for all functions  
✅ Platform-specific instructions  
✅ Usage examples  
✅ Troubleshooting guide  

### Quality

✅ New developer setup < 5 minutes  
✅ All tests pass consistently  
✅ Code follows PEP 8 style  
✅ Full input validation  
✅ Clear error messages  

---

## Implementation Timeline

### Phase 1: Core Implementation
- Implement 7 tag functions
- Add type hints
- Add docstrings
- Add error handling

### Phase 2: Testing
- Write unit tests
- Write integration tests
- Write edge case tests
- Achieve 100+ tests

### Phase 3: Automation
- Create setup scripts
- Create test runners
- Add configuration files
- Test on Windows and Linux/Mac

### Phase 4: Documentation
- Write README
- Write FEATURE_SPEC
- Add usage examples
- Add troubleshooting guide

---

## Future Enhancements

Potential improvements for future versions:

1. **Tag Hierarchy:** Parent-child tag relationships
2. **Tag Colors:** Color-coded tags for visual organization
3. **Saved Filters:** Save frequently used filter combinations
4. **Tag Search:** Search tags by prefix
5. **Export/Import:** Save/load todos with tags
6. **Database Storage:** Persistent storage instead of in-memory
7. **Tag Suggestions:** Auto-complete for tag entry
8. **Tag Rules:** Automatic tagging based on rules
9. **Cloud Sync:** Synchronize across devices
10. **Mobile App:** Native mobile application

---

## Glossary

**Tag:** A category label assigned to a task for organization

**Normalization:** Process of standardizing tag format (lowercase, whitespace trimmed, duplicates removed)

**Filter:** Selection criteria to display subset of todos

**AND Logic:** Filter returns todos with ALL specified tags

**OR Logic:** Filter returns todos with ANY specified tag

**Fixture:** Pre-configured test data used in multiple tests

**Parametrize:** Test technique running same test with multiple parameter values

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024 | Development Team | Initial specification |

---

**Status:** Complete  
**Priority:** High  
**Owner:** Development Team
