"""
Comprehensive Test Suite for Todo List with Tags
Tests include: unit tests, integration tests, edge cases, and backward compatibility
"""

import pytest
from todo_with_tags import (
    todos, add_todo, remove_todo, list_todos, mark_complete,
    filter_by_tags, show_tag_stats, add_tag_to_task,
    remove_tag_from_task, list_all_tags
)


# Fixtures
@pytest.fixture
def clean_todos():
    """Clear the todos list before each test."""
    todos.clear()
    yield
    todos.clear()


@pytest.fixture
def sample_todos(clean_todos):
    """Provide sample todos for testing."""
    add_todo("Write report", tags=["work", "urgent"])
    add_todo("Buy groceries", tags=["personal"])
    add_todo("Call mom", tags=["personal", "family"])
    add_todo("Fix bug", tags=["work", "coding"])
    return todos.copy()


@pytest.fixture
def mixed_todos(clean_todos):
    """Provide todos with and without tags."""
    add_todo("Task with tags", tags=["tag1", "tag2"])
    add_todo("Task without tags")
    add_todo("Another tagged task", tags=["tag3"])
    return todos.copy()


# Unit Tests - add_todo
class TestAddTodo:
    def test_add_todo_without_tags(self, clean_todos):
        """Test adding a todo without tags."""
        add_todo("Simple task")
        assert len(todos) == 1
        assert todos[0]["task"] == "Simple task"
        assert todos[0]["completed"] is False
        assert todos[0]["tags"] == []
    
    def test_add_todo_with_single_tag(self, clean_todos):
        """Test adding a todo with a single tag."""
        add_todo("Work task", tags=["work"])
        assert len(todos) == 1
        assert "work" in todos[0]["tags"]
    
    def test_add_todo_with_multiple_tags(self, clean_todos):
        """Test adding a todo with multiple tags."""
        add_todo("Complex task", tags=["work", "urgent", "important"])
        assert len(todos) == 1
        assert set(todos[0]["tags"]) == {"work", "urgent", "important"}
    
    def test_add_todo_normalizes_tags(self, clean_todos):
        """Test that tags are normalized to lowercase."""
        add_todo("Task", tags=["Work", "URGENT", "Personal"])
        assert set(todos[0]["tags"]) == {"work", "urgent", "personal"}
    
    def test_add_todo_removes_duplicate_tags(self, clean_todos):
        """Test that duplicate tags are removed."""
        add_todo("Task", tags=["work", "Work", "WORK", "work"])
        assert todos[0]["tags"] == ["work"]
    
    def test_add_todo_with_empty_tag_list(self, clean_todos):
        """Test adding a todo with empty tag list."""
        add_todo("Task", tags=[])
        assert len(todos) == 1
        assert todos[0]["tags"] == []
    
    def test_add_todo_with_none_tags(self, clean_todos):
        """Test adding a todo with None tags."""
        add_todo("Task", tags=None)
        assert len(todos) == 1
        assert todos[0]["tags"] == []
    
    def test_add_todo_strips_whitespace_from_tags(self, clean_todos):
        """Test that whitespace is stripped from tags."""
        add_todo("Task", tags=["  work  ", "urgent ", " personal"])
        assert set(todos[0]["tags"]) == {"work", "urgent", "personal"}
    
    def test_add_todo_ignores_empty_tags(self, clean_todos):
        """Test that empty string tags are ignored."""
        add_todo("Task", tags=["work", "", "   ", "urgent"])
        assert set(todos[0]["tags"]) == {"work", "urgent"}
    
    def test_add_todo_with_empty_task_string(self, clean_todos, capsys):
        """Test that empty task strings are rejected."""
        add_todo("")
        assert len(todos) == 0
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_add_todo_with_whitespace_only_task(self, clean_todos, capsys):
        """Test that whitespace-only task strings are rejected."""
        add_todo("   ")
        assert len(todos) == 0
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_add_todo_with_invalid_tags_type(self, clean_todos, capsys):
        """Test that invalid tag types are rejected."""
        add_todo("Task", tags="not a list")
        assert len(todos) == 0
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_add_todo_with_non_string_tags(self, clean_todos):
        """Test that non-string tags are ignored."""
        add_todo("Task", tags=["work", 123, None, "urgent"])
        assert set(todos[0]["tags"]) == {"work", "urgent"}


# Unit Tests - remove_todo
class TestRemoveTodo:
    def test_remove_todo_valid_index(self, sample_todos, capsys):
        """Test removing a todo with valid index."""
        initial_count = len(todos)
        remove_todo(0)
        assert len(todos) == initial_count - 1
        captured = capsys.readouterr()
        assert "Removed" in captured.out
    
    def test_remove_todo_invalid_index(self, sample_todos, capsys):
        """Test removing a todo with invalid index."""
        initial_count = len(todos)
        remove_todo(999)
        assert len(todos) == initial_count
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out
    
    def test_remove_todo_negative_index(self, sample_todos, capsys):
        """Test removing a todo with negative index."""
        initial_count = len(todos)
        remove_todo(-1)
        assert len(todos) == initial_count
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out
    
    def test_remove_todo_non_integer_index(self, sample_todos, capsys):
        """Test removing a todo with non-integer index."""
        initial_count = len(todos)
        remove_todo("0")  # type: ignore
        assert len(todos) == initial_count
        captured = capsys.readouterr()
        assert "Error" in captured.out


# Unit Tests - mark_complete
class TestMarkComplete:
    def test_mark_complete_valid_index(self, sample_todos):
        """Test marking a todo as complete."""
        mark_complete(0)
        assert todos[0]["completed"] is True
    
    def test_mark_complete_invalid_index(self, sample_todos, capsys):
        """Test marking a todo as complete with invalid index."""
        mark_complete(999)
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out
    
    def test_mark_complete_non_integer_index(self, sample_todos, capsys):
        """Test marking a todo as complete with non-integer index."""
        mark_complete("0")  # type: ignore
        captured = capsys.readouterr()
        assert "Error" in captured.out


# Unit Tests - filter_by_tags
class TestFilterByTags:
    def test_filter_by_tags_or_logic(self, sample_todos):
        """Test filtering by multiple tags with OR logic."""
        result = filter_by_tags(["work", "personal"], match_all=False)
        assert len(result) == 4  # All tasks have either work or personal
    
    def test_filter_by_tags_and_logic(self, sample_todos):
        """Test filtering by multiple tags with AND logic."""
        result = filter_by_tags(["personal", "family"], match_all=True)
        assert len(result) == 1
        assert result[0]["task"] == "Call mom"
    
    def test_filter_by_tags_single_tag_or(self, sample_todos):
        """Test filtering by single tag with OR logic."""
        result = filter_by_tags(["work"], match_all=False)
        assert len(result) == 2
    
    def test_filter_by_tags_single_tag_and(self, sample_todos):
        """Test filtering by single tag with AND logic."""
        result = filter_by_tags(["work"], match_all=True)
        assert len(result) == 2
    
    def test_filter_by_tags_no_matches(self, sample_todos):
        """Test filtering with no matching tags."""
        result = filter_by_tags(["nonexistent"], match_all=False)
        assert len(result) == 0
    
    def test_filter_by_tags_empty_list(self, sample_todos):
        """Test filtering with empty tag list."""
        result = filter_by_tags([], match_all=False)
        assert len(result) == 0
    
    def test_filter_by_tags_case_insensitive(self, sample_todos):
        """Test that filtering is case-insensitive."""
        result = filter_by_tags(["WORK", "Personal"], match_all=False)
        assert len(result) == 4
    
    def test_filter_by_tags_with_whitespace(self, sample_todos):
        """Test filtering with whitespace in tags."""
        result = filter_by_tags(["  work  ", " personal "], match_all=False)
        assert len(result) == 4
    
    def test_filter_by_tags_invalid_type(self, sample_todos, capsys):
        """Test filtering with invalid type."""
        result = filter_by_tags("not a list", match_all=False)  # type: ignore
        assert result == []
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_filter_by_tags_with_non_string_tags(self, sample_todos):
        """Test filtering with non-string tags in list."""
        result = filter_by_tags(["work", 123, None], match_all=False)  # type: ignore
        assert len(result) == 2


# Unit Tests - add_tag_to_task
class TestAddTagToTask:
    def test_add_tag_to_task_valid(self, sample_todos):
        """Test adding a tag to an existing task."""
        initial_tags = len(todos[0]["tags"])
        add_tag_to_task(0, "newtag")
        assert len(todos[0]["tags"]) == initial_tags + 1
        assert "newtag" in todos[0]["tags"]
    
    def test_add_tag_to_task_duplicate(self, sample_todos, capsys):
        """Test adding a duplicate tag to a task."""
        initial_tags = len(todos[0]["tags"])
        add_tag_to_task(0, "work")
        assert len(todos[0]["tags"]) == initial_tags
        captured = capsys.readouterr()
        assert "already exists" in captured.out
    
    def test_add_tag_to_task_invalid_index(self, sample_todos, capsys):
        """Test adding a tag with invalid index."""
        add_tag_to_task(999, "tag")
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out
    
    def test_add_tag_to_task_case_normalization(self, sample_todos):
        """Test that added tags are normalized."""
        add_tag_to_task(0, "NewTag")
        assert "newtag" in todos[0]["tags"]
        assert "NewTag" not in todos[0]["tags"]
    
    def test_add_tag_to_task_empty_string(self, sample_todos, capsys):
        """Test adding an empty string as tag."""
        initial_tags = len(todos[0]["tags"])
        add_tag_to_task(0, "")
        assert len(todos[0]["tags"]) == initial_tags
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_add_tag_to_task_non_integer_index(self, sample_todos, capsys):
        """Test adding tag with non-integer index."""
        add_tag_to_task("0", "tag")  # type: ignore
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_add_tag_to_task_without_tags_field(self, clean_todos):
        """Test adding tag to task that doesn't have tags field."""
        # Manually create a task without tags field
        todos.append({"task": "Old task", "completed": False})
        add_tag_to_task(0, "newtag")
        assert "tags" in todos[0]
        assert "newtag" in todos[0]["tags"]


# Unit Tests - remove_tag_from_task
class TestRemoveTagFromTask:
    def test_remove_tag_from_task_valid(self, sample_todos):
        """Test removing a tag from a task."""
        initial_tags = len(todos[0]["tags"])
        remove_tag_from_task(0, "work")
        assert len(todos[0]["tags"]) == initial_tags - 1
        assert "work" not in todos[0]["tags"]
    
    def test_remove_tag_from_task_nonexistent(self, sample_todos, capsys):
        """Test removing a nonexistent tag."""
        initial_tags = len(todos[0]["tags"])
        remove_tag_from_task(0, "nonexistent")
        assert len(todos[0]["tags"]) == initial_tags
        captured = capsys.readouterr()
        assert "not found" in captured.out
    
    def test_remove_tag_from_task_invalid_index(self, sample_todos, capsys):
        """Test removing a tag with invalid index."""
        remove_tag_from_task(999, "tag")
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out
    
    def test_remove_tag_from_task_case_insensitive(self, sample_todos):
        """Test that tag removal is case-insensitive."""
        initial_tags = len(todos[0]["tags"])
        remove_tag_from_task(0, "WORK")
        assert len(todos[0]["tags"]) == initial_tags - 1
    
    def test_remove_tag_from_task_empty_string(self, sample_todos, capsys):
        """Test removing an empty string tag."""
        remove_tag_from_task(0, "")
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_remove_tag_from_task_non_integer_index(self, sample_todos, capsys):
        """Test removing tag with non-integer index."""
        remove_tag_from_task("0", "tag")  # type: ignore
        captured = capsys.readouterr()
        assert "Error" in captured.out


# Unit Tests - list_all_tags
class TestListAllTags:
    def test_list_all_tags_with_todos(self, sample_todos):
        """Test listing all unique tags."""
        tags = list_all_tags()
        assert set(tags) == {"coding", "family", "personal", "urgent", "work"}
        assert tags == sorted(tags)  # Check sorting
    
    def test_list_all_tags_empty(self, clean_todos):
        """Test listing tags with no todos."""
        tags = list_all_tags()
        assert tags == []
    
    def test_list_all_tags_no_tags(self, clean_todos):
        """Test listing tags when todos have no tags."""
        add_todo("Task 1")
        add_todo("Task 2")
        tags = list_all_tags()
        assert tags == []
    
    def test_list_all_tags_sorting(self, clean_todos):
        """Test that tags are returned in sorted order."""
        add_todo("Task", tags=["zebra", "apple", "banana"])
        tags = list_all_tags()
        assert tags == ["apple", "banana", "zebra"]


# Unit Tests - show_tag_stats
class TestShowTagStats:
    def test_show_tag_stats_with_todos(self, sample_todos, capsys):
        """Test showing tag statistics."""
        show_tag_stats()
        captured = capsys.readouterr()
        assert "work: 2" in captured.out
        assert "personal: 2" in captured.out
        assert "urgent: 1" in captured.out
    
    def test_show_tag_stats_empty(self, clean_todos, capsys):
        """Test showing stats with no todos."""
        show_tag_stats()
        captured = capsys.readouterr()
        assert "No todos found" in captured.out
    
    def test_show_tag_stats_no_tags(self, clean_todos, capsys):
        """Test showing stats when todos have no tags."""
        add_todo("Task 1")
        add_todo("Task 2")
        show_tag_stats()
        captured = capsys.readouterr()
        assert "No tags found" in captured.out


# Unit Tests - list_todos
class TestListTodos:
    def test_list_todos_all(self, sample_todos, capsys):
        """Test listing all todos."""
        list_todos()
        captured = capsys.readouterr()
        assert "Write report" in captured.out
        assert "Buy groceries" in captured.out
    
    def test_list_todos_filtered(self, sample_todos, capsys):
        """Test listing todos filtered by tag."""
        list_todos(filter_tag="work")
        captured = capsys.readouterr()
        assert "Write report" in captured.out
        assert "Fix bug" in captured.out
        assert "Buy groceries" not in captured.out
    
    def test_list_todos_empty(self, clean_todos, capsys):
        """Test listing when no todos exist."""
        list_todos()
        captured = capsys.readouterr()
        assert "No todos found" in captured.out
    
    def test_list_todos_no_match_for_filter(self, sample_todos, capsys):
        """Test listing with filter that matches nothing."""
        list_todos(filter_tag="nonexistent")
        captured = capsys.readouterr()
        assert "No todos found" in captured.out


# Integration Tests
class TestIntegration:
    def test_complete_workflow(self, clean_todos):
        """Test a complete workflow: add, filter, modify, remove."""
        # Add tasks
        add_todo("Task 1", tags=["work", "urgent"])
        add_todo("Task 2", tags=["personal"])
        add_todo("Task 3", tags=["work"])
        
        assert len(todos) == 3
        
        # Filter by tag
        work_tasks = filter_by_tags(["work"], match_all=False)
        assert len(work_tasks) == 2
        
        # Add tag
        add_tag_to_task(1, "shopping")
        assert "shopping" in todos[1]["tags"]
        
        # Mark complete
        mark_complete(0)
        assert todos[0]["completed"] is True
        
        # Remove tag
        remove_tag_from_task(0, "urgent")
        assert "urgent" not in todos[0]["tags"]
        
        # Get all tags
        all_tags = list_all_tags()
        assert "work" in all_tags
        assert "personal" in all_tags
        assert "shopping" in all_tags
        
        # Remove todo
        remove_todo(1)
        assert len(todos) == 2
    
    def test_complex_filtering_workflow(self, clean_todos):
        """Test complex filtering scenarios."""
        add_todo("Task 1", tags=["a", "b", "c"])
        add_todo("Task 2", tags=["a", "b"])
        add_todo("Task 3", tags=["a"])
        add_todo("Task 4", tags=["d"])
        
        # OR logic
        result = filter_by_tags(["a", "d"], match_all=False)
        assert len(result) == 4
        
        # AND logic
        result = filter_by_tags(["a", "b"], match_all=True)
        assert len(result) == 2
        
        # Multiple AND
        result = filter_by_tags(["a", "b", "c"], match_all=True)
        assert len(result) == 1
        assert result[0]["task"] == "Task 1"
    
    def test_tag_modification_workflow(self, clean_todos):
        """Test adding and removing tags from tasks."""
        add_todo("Task", tags=["initial"])
        
        # Add multiple tags
        add_tag_to_task(0, "tag1")
        add_tag_to_task(0, "tag2")
        add_tag_to_task(0, "tag3")
        
        assert len(todos[0]["tags"]) == 4
        
        # Remove some tags
        remove_tag_from_task(0, "initial")
        remove_tag_from_task(0, "tag2")
        
        assert len(todos[0]["tags"]) == 2
        assert "tag1" in todos[0]["tags"]
        assert "tag3" in todos[0]["tags"]


# Backward Compatibility Tests
class TestBackwardCompatibility:
    def test_untagged_tasks_work(self, clean_todos):
        """Test that tasks without tags work correctly."""
        add_todo("Untagged task")
        
        assert len(todos) == 1
        assert todos[0]["task"] == "Untagged task"
        assert todos[0]["tags"] == []
        
        # Can still mark complete
        mark_complete(0)
        assert todos[0]["completed"] is True
        
        # Can still remove
        remove_todo(0)
        assert len(todos) == 0
    
    def test_mixed_tagged_untagged(self, mixed_todos):
        """Test that tagged and untagged tasks coexist."""
        assert len(todos) == 3
        
        # Filter should only return tagged tasks
        result = filter_by_tags(["tag1"], match_all=False)
        assert len(result) == 1
        
        # All tags should work
        all_tags = list_all_tags()
        assert len(all_tags) == 3
    
    def test_manual_todos_without_tags_field(self, clean_todos):
        """Test handling of todos created without tags field."""
        # Simulate old-style todo
        todos.append({"task": "Old task", "completed": False})
        
        # Should work with filtering (empty result)
        result = filter_by_tags(["tag"], match_all=False)
        assert len(result) == 0
        
        # Should work with list_all_tags
        tags = list_all_tags()
        assert len(tags) == 0


# Parametrized Tests
class TestParametrized:
    @pytest.mark.parametrize("task,tags,expected_tag_count", [
        ("Task 1", ["a"], 1),
        ("Task 2", ["a", "b"], 2),
        ("Task 3", ["a", "b", "c"], 3),
        ("Task 4", [], 0),
        ("Task 5", None, 0),
    ])
    def test_add_todo_various_tag_counts(self, clean_todos, task, tags, expected_tag_count):
        """Test adding todos with various tag counts."""
        add_todo(task, tags=tags)
        assert len(todos[0]["tags"]) == expected_tag_count
    
    @pytest.mark.parametrize("tags,match_all,expected_count", [
        (["work"], False, 2),
        (["personal"], False, 2),
        (["work", "urgent"], True, 1),
        (["personal", "family"], True, 1),
        (["work", "personal"], False, 4),
        (["nonexistent"], False, 0),
    ])
    def test_filter_by_tags_various_combinations(self, sample_todos, tags, match_all, expected_count):
        """Test filtering with various tag combinations."""
        result = filter_by_tags(tags, match_all=match_all)
        assert len(result) == expected_count
    
    @pytest.mark.parametrize("index", [0, 1, 2, 3])
    def test_mark_complete_all_indices(self, sample_todos, index):
        """Test marking various todos as complete."""
        mark_complete(index)
        assert todos[index]["completed"] is True
    
    @pytest.mark.parametrize("index", [-1, 999, 100])
    def test_invalid_indices(self, sample_todos, index, capsys):
        """Test various invalid indices."""
        mark_complete(index)
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out


# Edge Cases
class TestEdgeCases:
    def test_unicode_in_tags(self, clean_todos):
        """Test that unicode characters work in tags."""
        add_todo("Task", tags=["🚀", "日本語", "café"])
        assert len(todos[0]["tags"]) == 3
    
    def test_special_characters_in_tags(self, clean_todos):
        """Test special characters in tags."""
        add_todo("Task", tags=["tag-with-dash", "tag_with_underscore", "tag.with.dot"])
        assert len(todos[0]["tags"]) == 3
    
    def test_very_long_tag(self, clean_todos):
        """Test with a very long tag."""
        long_tag = "a" * 1000
        add_todo("Task", tags=[long_tag])
        assert todos[0]["tags"][0] == long_tag
    
    def test_many_tags_on_single_task(self, clean_todos):
        """Test adding many tags to a single task."""
        tags = [f"tag{i}" for i in range(100)]
        add_todo("Task", tags=tags)
        assert len(todos[0]["tags"]) == 100
    
    def test_many_todos(self, clean_todos):
        """Test with many todos."""
        for i in range(100):
            add_todo(f"Task {i}", tags=[f"tag{i % 10}"])
        
        assert len(todos) == 100
        
        # Test filtering still works
        result = filter_by_tags(["tag0"], match_all=False)
        assert len(result) == 10
    
    def test_empty_todos_list_operations(self, clean_todos, capsys):
        """Test operations on empty todos list."""
        list_todos()
        show_tag_stats()
        tags = list_all_tags()
        result = filter_by_tags(["tag"], match_all=False)
        
        assert len(tags) == 0
        assert len(result) == 0
    
    def test_whitespace_only_tags(self, clean_todos):
        """Test that whitespace-only tags are filtered out."""
        add_todo("Task", tags=["   ", "\t", "\n", "valid"])
        assert todos[0]["tags"] == ["valid"]
