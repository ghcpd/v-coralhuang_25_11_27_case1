"""
Comprehensive test suite for todo_with_tags.py
Tests include unit tests, integration tests, edge cases, and backward compatibility
"""

import pytest
from todo_with_tags import (
    add_todo, remove_todo, list_todos, mark_complete, filter_by_tags,
    show_tag_stats, add_tag_to_task, remove_tag_from_task, list_all_tags,
    todos
)


@pytest.fixture(autouse=True)
def clear_todos():
    """Clear todos list before and after each test."""
    todos.clear()
    yield
    todos.clear()


@pytest.fixture
def sample_todos_fixture():
    """Fixture providing sample todos for testing."""
    todos.clear()
    add_todo("Write report", tags=["work", "urgent", "review"])
    add_todo("Buy groceries", tags=["personal"])
    add_todo("Call dentist", tags=["personal", "health"])
    add_todo("Review code", tags=["work"])
    add_todo("Untagged task")
    return todos.copy()


# ============================================================================
# UNIT TESTS - add_todo
# ============================================================================

class TestAddTodo:
    """Unit tests for add_todo function."""
    
    def test_add_todo_basic(self):
        """Test adding a basic todo without tags."""
        add_todo("Test task")
        assert len(todos) == 1
        assert todos[0]["task"] == "Test task"
        assert todos[0]["completed"] is False
        assert todos[0]["tags"] == []
    
    def test_add_todo_with_single_tag(self):
        """Test adding a todo with a single tag."""
        add_todo("Task", tags=["work"])
        assert todos[0]["tags"] == ["work"]
    
    def test_add_todo_with_multiple_tags(self):
        """Test adding a todo with multiple tags."""
        add_todo("Task", tags=["work", "urgent", "review"])
        assert set(todos[0]["tags"]) == {"work", "urgent", "review"}
    
    def test_add_todo_tags_normalized_to_lowercase(self):
        """Test that tags are normalized to lowercase."""
        add_todo("Task", tags=["WORK", "Urgent", "ReViEw"])
        assert set(todos[0]["tags"]) == {"work", "urgent", "review"}
    
    def test_add_todo_tags_duplicates_removed(self):
        """Test that duplicate tags are removed."""
        add_todo("Task", tags=["work", "WORK", "work"])
        assert todos[0]["tags"] == ["work"]
    
    def test_add_todo_tags_whitespace_trimmed(self):
        """Test that tags have whitespace trimmed."""
        add_todo("Task", tags=["  work  ", " urgent ", "review"])
        assert set(todos[0]["tags"]) == {"work", "urgent", "review"}
    
    def test_add_todo_empty_tags_list(self):
        """Test adding a todo with an empty tags list."""
        add_todo("Task", tags=[])
        assert todos[0]["tags"] == []
    
    def test_add_todo_none_tags(self):
        """Test adding a todo with None tags (default)."""
        add_todo("Task", tags=None)
        assert todos[0]["tags"] == []
    
    def test_add_todo_task_whitespace_trimmed(self):
        """Test that task description is trimmed."""
        add_todo("  My Task  ")
        assert todos[0]["task"] == "My Task"
    
    @pytest.mark.parametrize("invalid_task", [123, None, True, [], {}])
    def test_add_todo_invalid_task_type(self, invalid_task):
        """Test that TypeError is raised for invalid task types."""
        with pytest.raises(TypeError):
            add_todo(invalid_task)
    
    def test_add_todo_empty_task_string(self):
        """Test that ValueError is raised for empty task."""
        with pytest.raises(ValueError):
            add_todo("")
    
    def test_add_todo_whitespace_only_task(self):
        """Test that ValueError is raised for whitespace-only task."""
        with pytest.raises(ValueError):
            add_todo("   ")
    
    @pytest.mark.parametrize("invalid_tags", [123, "work", True, {"work"}])
    def test_add_todo_invalid_tags_type(self, invalid_tags):
        """Test that TypeError is raised for invalid tags types."""
        with pytest.raises(TypeError):
            add_todo("Task", tags=invalid_tags)
    
    def test_add_todo_multiple_times(self):
        """Test adding multiple todos."""
        add_todo("Task 1", tags=["work"])
        add_todo("Task 2", tags=["personal"])
        add_todo("Task 3")
        assert len(todos) == 3
        assert todos[1]["task"] == "Task 2"


# ============================================================================
# UNIT TESTS - remove_todo
# ============================================================================

class TestRemoveTodo:
    """Unit tests for remove_todo function."""
    
    def test_remove_todo_valid_index(self):
        """Test removing a todo with valid index."""
        add_todo("Task 1")
        add_todo("Task 2")
        remove_todo(0)
        assert len(todos) == 1
        assert todos[0]["task"] == "Task 2"
    
    def test_remove_todo_last_index(self):
        """Test removing the last todo."""
        add_todo("Task 1")
        add_todo("Task 2")
        remove_todo(1)
        assert len(todos) == 1
        assert todos[0]["task"] == "Task 1"
    
    def test_remove_todo_invalid_positive_index(self):
        """Test that IndexError is raised for out-of-range positive index."""
        add_todo("Task 1")
        with pytest.raises(IndexError):
            remove_todo(5)
    
    def test_remove_todo_invalid_negative_index(self):
        """Test that IndexError is raised for negative index."""
        add_todo("Task 1")
        with pytest.raises(IndexError):
            remove_todo(-1)
    
    def test_remove_todo_from_empty_list(self):
        """Test that IndexError is raised when removing from empty list."""
        with pytest.raises(IndexError):
            remove_todo(0)
    
    @pytest.mark.parametrize("invalid_index", ["0", 1.5, True, None])
    def test_remove_todo_invalid_index_type(self, invalid_index):
        """Test that TypeError is raised for invalid index types."""
        add_todo("Task 1")
        with pytest.raises(TypeError):
            remove_todo(invalid_index)


# ============================================================================
# UNIT TESTS - filter_by_tags
# ============================================================================

class TestFilterByTags:
    """Unit tests for filter_by_tags function."""
    
    def test_filter_by_tags_or_logic_single_match(self, sample_todos_fixture):
        """Test OR logic: finds todos with at least one matching tag."""
        result = filter_by_tags(["work"], match_all=False)
        assert len(result) == 2
        assert all(t["task"] in ["Write report", "Review code"] for t in result)
    
    def test_filter_by_tags_or_logic_multiple_matches(self, sample_todos_fixture):
        """Test OR logic: multiple tags, returns todos with any tag."""
        result = filter_by_tags(["work", "personal"], match_all=False)
        assert len(result) == 4
    
    def test_filter_by_tags_and_logic_all_present(self, sample_todos_fixture):
        """Test AND logic: finds todos with all specified tags."""
        result = filter_by_tags(["personal", "health"], match_all=True)
        assert len(result) == 1
        assert result[0]["task"] == "Call dentist"
    
    def test_filter_by_tags_and_logic_partial_match(self, sample_todos_fixture):
        """Test AND logic: no todos have all tags."""
        result = filter_by_tags(["work", "personal"], match_all=True)
        assert len(result) == 0
    
    def test_filter_by_tags_case_insensitive(self, sample_todos_fixture):
        """Test that filtering is case-insensitive."""
        result = filter_by_tags(["WORK"], match_all=False)
        assert len(result) == 2
    
    def test_filter_by_tags_no_matches(self, sample_todos_fixture):
        """Test filtering with no matching tags."""
        result = filter_by_tags(["nonexistent"], match_all=False)
        assert len(result) == 0
    
    def test_filter_by_tags_invalid_tags_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid tags type."""
        with pytest.raises(TypeError):
            filter_by_tags("work", match_all=False)
    
    def test_filter_by_tags_empty_list(self, sample_todos_fixture):
        """Test that ValueError is raised for empty tags list."""
        with pytest.raises(ValueError):
            filter_by_tags([], match_all=False)
    
    def test_filter_by_tags_invalid_match_all_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid match_all type."""
        with pytest.raises(TypeError):
            filter_by_tags(["work"], match_all="true")
    
    def test_filter_by_tags_empty_todos(self):
        """Test filtering when todos list is empty."""
        result = filter_by_tags(["work"], match_all=False)
        assert len(result) == 0
    
    def test_filter_by_tags_only_invalid_tags(self, sample_todos_fixture):
        """Test that ValueError is raised when tags list contains only invalid items."""
        with pytest.raises(ValueError):
            filter_by_tags(["", "  "], match_all=False)


# ============================================================================
# UNIT TESTS - show_tag_stats
# ============================================================================

class TestShowTagStats:
    """Unit tests for show_tag_stats function."""
    
    def test_show_tag_stats_no_tags(self, capsys):
        """Test showing stats when no tags exist."""
        show_tag_stats()
        captured = capsys.readouterr()
        assert "No tags found" in captured.out
    
    def test_show_tag_stats_multiple_tags(self, sample_todos_fixture, capsys):
        """Test showing stats with multiple tags."""
        show_tag_stats()
        captured = capsys.readouterr()
        assert "work: 2" in captured.out
        assert "personal: 2" in captured.out
        assert "urgent: 1" in captured.out
        assert "review: 1" in captured.out
        assert "health: 1" in captured.out


# ============================================================================
# UNIT TESTS - add_tag_to_task
# ============================================================================

class TestAddTagToTask:
    """Unit tests for add_tag_to_task function."""
    
    def test_add_tag_to_task_success(self, sample_todos_fixture):
        """Test adding a tag to an existing task."""
        add_tag_to_task(1, "urgent")
        assert "urgent" in todos[1]["tags"]
    
    def test_add_tag_to_task_case_normalized(self, sample_todos_fixture):
        """Test that added tag is normalized to lowercase."""
        add_tag_to_task(1, "URGENT")
        assert "urgent" in todos[1]["tags"]
    
    def test_add_tag_to_task_already_exists(self, sample_todos_fixture, capsys):
        """Test adding a tag that already exists."""
        add_tag_to_task(0, "work")
        captured = capsys.readouterr()
        assert "already exists" in captured.out
    
    def test_add_tag_to_task_invalid_index(self, sample_todos_fixture):
        """Test that IndexError is raised for invalid index."""
        with pytest.raises(IndexError):
            add_tag_to_task(10, "work")
    
    def test_add_tag_to_task_invalid_index_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid index type."""
        with pytest.raises(TypeError):
            add_tag_to_task("0", "work")
    
    def test_add_tag_to_task_invalid_tag_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid tag type."""
        with pytest.raises(TypeError):
            add_tag_to_task(0, 123)
    
    def test_add_tag_to_task_empty_tag(self, sample_todos_fixture):
        """Test that ValueError is raised for empty tag."""
        with pytest.raises(ValueError):
            add_tag_to_task(0, "")
    
    def test_add_tag_to_task_whitespace_tag(self, sample_todos_fixture):
        """Test that ValueError is raised for whitespace-only tag."""
        with pytest.raises(ValueError):
            add_tag_to_task(0, "   ")


# ============================================================================
# UNIT TESTS - remove_tag_from_task
# ============================================================================

class TestRemoveTagFromTask:
    """Unit tests for remove_tag_from_task function."""
    
    def test_remove_tag_from_task_success(self, sample_todos_fixture):
        """Test removing a tag from an existing task."""
        remove_tag_from_task(0, "work")
        assert "work" not in todos[0]["tags"]
    
    def test_remove_tag_from_task_case_normalized(self, sample_todos_fixture):
        """Test that tag to remove is normalized to lowercase."""
        remove_tag_from_task(0, "WORK")
        assert "work" not in todos[0]["tags"]
    
    def test_remove_tag_from_task_not_exists(self, sample_todos_fixture):
        """Test that ValueError is raised when removing non-existent tag."""
        with pytest.raises(ValueError):
            remove_tag_from_task(0, "nonexistent")
    
    def test_remove_tag_from_task_invalid_index(self, sample_todos_fixture):
        """Test that IndexError is raised for invalid index."""
        with pytest.raises(IndexError):
            remove_tag_from_task(10, "work")
    
    def test_remove_tag_from_task_invalid_index_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid index type."""
        with pytest.raises(TypeError):
            remove_tag_from_task("0", "work")
    
    def test_remove_tag_from_task_invalid_tag_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid tag type."""
        with pytest.raises(TypeError):
            remove_tag_from_task(0, 123)
    
    def test_remove_tag_from_task_empty_tag(self, sample_todos_fixture):
        """Test that ValueError is raised for empty tag."""
        with pytest.raises(ValueError):
            remove_tag_from_task(0, "")


# ============================================================================
# UNIT TESTS - list_all_tags
# ============================================================================

class TestListAllTags:
    """Unit tests for list_all_tags function."""
    
    def test_list_all_tags_empty(self):
        """Test listing tags when no tags exist."""
        result = list_all_tags()
        assert result == []
    
    def test_list_all_tags_multiple_tags(self, sample_todos_fixture):
        """Test listing all tags."""
        result = list_all_tags()
        expected = ["health", "personal", "review", "urgent", "work"]
        assert result == expected  # Should be sorted
    
    def test_list_all_tags_no_duplicates(self, sample_todos_fixture):
        """Test that returned tags have no duplicates."""
        result = list_all_tags()
        assert len(result) == len(set(result))
    
    def test_list_all_tags_sorted(self, sample_todos_fixture):
        """Test that tags are returned in sorted order."""
        result = list_all_tags()
        assert result == sorted(result)


# ============================================================================
# UNIT TESTS - mark_complete
# ============================================================================

class TestMarkComplete:
    """Unit tests for mark_complete function."""
    
    def test_mark_complete_valid(self, sample_todos_fixture):
        """Test marking a todo as complete."""
        mark_complete(0)
        assert todos[0]["completed"] is True
    
    def test_mark_complete_invalid_index(self, sample_todos_fixture):
        """Test that IndexError is raised for invalid index."""
        with pytest.raises(IndexError):
            mark_complete(10)
    
    def test_mark_complete_invalid_type(self, sample_todos_fixture):
        """Test that TypeError is raised for invalid index type."""
        with pytest.raises(TypeError):
            mark_complete("0")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_workflow_add_filter_remove(self):
        """Test complete workflow: add tasks with tags, filter, remove."""
        add_todo("Task 1", tags=["work"])
        add_todo("Task 2", tags=["personal"])
        add_todo("Task 3", tags=["work", "urgent"])
        
        work_tasks = filter_by_tags(["work"], match_all=False)
        assert len(work_tasks) == 2
        
        remove_todo(0)
        assert len(todos) == 2
    
    def test_workflow_add_modify_tags(self):
        """Test workflow: add task, modify tags."""
        add_todo("Task", tags=["work"])
        add_tag_to_task(0, "urgent")
        assert len(todos[0]["tags"]) == 2
        
        remove_tag_from_task(0, "work")
        assert len(todos[0]["tags"]) == 1
        assert todos[0]["tags"] == ["urgent"]
    
    def test_workflow_complete_and_filter(self):
        """Test workflow: complete task and filter."""
        add_todo("Task 1", tags=["work"])
        add_todo("Task 2", tags=["work"])
        
        mark_complete(0)
        assert todos[0]["completed"] is True
        
        work_tasks = filter_by_tags(["work"], match_all=False)
        assert len(work_tasks) == 2  # Both should still be in filter
    
    def test_workflow_and_or_filtering(self):
        """Test workflow with both AND and OR filtering."""
        add_todo("Task 1", tags=["work", "urgent"])
        add_todo("Task 2", tags=["work", "review"])
        add_todo("Task 3", tags=["personal"])
        
        # OR: work or personal
        or_result = filter_by_tags(["work", "personal"], match_all=False)
        assert len(or_result) == 3
        
        # AND: work and urgent
        and_result = filter_by_tags(["work", "urgent"], match_all=True)
        assert len(and_result) == 1
        assert and_result[0]["task"] == "Task 1"


# ============================================================================
# BACKWARD COMPATIBILITY TESTS
# ============================================================================

class TestBackwardCompatibility:
    """Tests ensuring backward compatibility with original todo functionality."""
    
    def test_untagged_tasks_work(self):
        """Test that tasks without tags work correctly."""
        add_todo("Simple task")
        assert len(todos) == 1
        assert todos[0]["tags"] == []
    
    def test_list_todos_without_filter(self, sample_todos_fixture, capsys):
        """Test listing todos without tag filter."""
        list_todos()
        captured = capsys.readouterr()
        assert "Write report" in captured.out
        assert "Untagged task" in captured.out
    
    def test_basic_crud_operations(self):
        """Test that basic CRUD operations still work."""
        add_todo("Task 1")
        add_todo("Task 2")
        assert len(todos) == 2
        
        mark_complete(0)
        assert todos[0]["completed"] is True
        
        remove_todo(1)
        assert len(todos) == 1


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_special_characters_in_task(self):
        """Test tasks with special characters."""
        add_todo("Task with @#$%^&*() special chars")
        assert todos[0]["task"] == "Task with @#$%^&*() special chars"
    
    def test_unicode_characters_in_task(self):
        """Test tasks with unicode characters."""
        add_todo("Task with émojis 🎉 and ñ")
        assert "émojis 🎉" in todos[0]["task"]
    
    def test_very_long_task_description(self):
        """Test adding a very long task description."""
        long_task = "A" * 1000
        add_todo(long_task)
        assert todos[0]["task"] == long_task
    
    def test_many_tags_on_single_task(self):
        """Test adding many tags to a single task."""
        tags = [f"tag{i}" for i in range(50)]
        add_todo("Task", tags=tags)
        assert len(todos[0]["tags"]) == 50
    
    def test_numeric_string_tags(self):
        """Test tags that are numeric strings."""
        add_todo("Task", tags=["123", "456"])
        assert set(todos[0]["tags"]) == {"123", "456"}
    
    def test_tag_with_special_characters(self):
        """Test tags with special characters and numbers."""
        add_todo("Task", tags=["tag-1", "tag_2", "tag.3"])
        assert set(todos[0]["tags"]) == {"tag-1", "tag_2", "tag.3"}
    
    def test_filter_with_nonexistent_tags_and_existing_todos(self):
        """Test filtering for tags that don't exist when todos exist."""
        add_todo("Task 1", tags=["work"])
        add_todo("Task 2", tags=["personal"])
        
        result = filter_by_tags(["nonexistent"], match_all=False)
        assert result == []
    
    def test_remove_last_tag_from_task(self):
        """Test removing the last tag from a task."""
        add_todo("Task", tags=["work"])
        remove_tag_from_task(0, "work")
        assert todos[0]["tags"] == []
    
    def test_tag_stats_with_mixed_completed_states(self):
        """Test tag stats regardless of completion status."""
        add_todo("Task 1", tags=["work"])
        add_todo("Task 2", tags=["work"])
        mark_complete(0)
        
        result = filter_by_tags(["work"], match_all=False)
        assert len(result) == 2  # Both should be in stats


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================

class TestParametrized:
    """Parametrized tests for comprehensive coverage."""
    
    @pytest.mark.parametrize("task,tags", [
        ("Task 1", ["work"]),
        ("Task 2", ["work", "urgent"]),
        ("Task 3", []),
        ("Task 4", None),
    ])
    def test_add_multiple_todo_variations(self, task, tags):
        """Test adding todos with various configurations."""
        add_todo(task, tags=tags)
        assert len(todos) == 1
        assert todos[0]["task"] == task
    
    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_mark_complete_various_indices(self, index):
        """Test marking various indices as complete."""
        for i in range(3):
            add_todo(f"Task {i}")
        
        mark_complete(index)
        assert todos[index]["completed"] is True
        assert all(not todos[j]["completed"] for j in range(3) if j != index)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
