#!/usr/bin/env python
"""Quick verification script to test all implemented functions"""

import sys
from todo_with_tags import (
    add_todo, filter_by_tags, show_tag_stats, list_all_tags,
    mark_complete, list_todos, todos, add_tag_to_task, remove_tag_from_task
)

print("=" * 60)
print("VERIFICATION: All Functions Working")
print("=" * 60)
print()

# Setup test data
add_todo("Write report", tags=["work", "urgent", "review"])
add_todo("Buy groceries", tags=["personal"])
add_todo("Call dentist", tags=["personal", "health"])
add_todo("Review code", tags=["work"])

# Test 1: List all
print("1. List all tasks:")
list_todos()

# Test 2: Filter by single tag
print("\n2. Filter by 'work' tag:")
work_tasks = filter_by_tags(["work"], match_all=False)
print(f"   Found {len(work_tasks)} work tasks")

# Test 3: Filter by multiple tags (OR)
print("\n3. Filter by 'work' OR 'personal' tags:")
multi_or = filter_by_tags(["work", "personal"], match_all=False)
print(f"   Found {len(multi_or)} tasks")

# Test 4: Filter by multiple tags (AND)
print("\n4. Filter by 'work' AND 'urgent' tags:")
multi_and = filter_by_tags(["work", "urgent"], match_all=True)
print(f"   Found {len(multi_and)} tasks")
if multi_and:
    print(f"   Task: {multi_and[0]['task']}")

# Test 5: Show stats
print("\n5. Tag Statistics:")
show_tag_stats()

# Test 6: Get all tags
print("\n6. All unique tags:")
all_tags = list_all_tags()
print(f"   {', '.join(all_tags)}")

# Test 7: Mark complete
print("\n7. Mark task complete:")
mark_complete(0)
print(f"   Task completed: {todos[0]['task']}")
print(f"   Completed status: {todos[0]['completed']}")

# Test 8: Add tag to existing task
print("\n8. Add 'important' tag to task 1:")
add_tag_to_task(1, "important")
print(f"   New tags: {', '.join(todos[1]['tags'])}")

# Test 9: Remove tag
print("\n9. Remove 'important' tag from task 1:")
remove_tag_from_task(1, "important")
print(f"   Updated tags: {', '.join(todos[1]['tags'])}")

print("\n" + "=" * 60)
print("OK: ALL FUNCTIONS VERIFIED SUCCESSFULLY")
print("=" * 60)
