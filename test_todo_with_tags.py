import pytest

from todo_with_tags import (
    add_todo,
    list_todos,
    filter_by_tags,
    show_tag_stats,
    add_tag_to_task,
    remove_tag_from_task,
    list_all_tags,
    todos,
    clear_all_todos,
)


@pytest.fixture(autouse=True)
def clean_todos():
    # Runs before each test
    clear_all_todos()
    yield
    clear_all_todos()


def test_add_todo_with_tags_and_list():
    add_todo("Write report", tags=["Work", "urgent"])
    assert len(todos) == 1
    assert todos[0]["task"] == "Write report"
    assert sorted(todos[0]["tags"]) == ["urgent", "work"]

    listed = list_todos()
    assert len(listed) == 1


def test_filter_by_single_tag():
    add_todo("Task 1", tags=["work"])
    add_todo("Task 2", tags=["personal"])
    matches = filter_by_tags(["work"])
    assert len(matches) == 1
    assert matches[0]["task"] == "Task 1"


def test_list_todos_with_filter_tag():
    add_todo("T1", tags=["work"])
    add_todo("T2", tags=["personal"])
    res = list_todos(filter_tag="work")
    assert len(res) == 1
    assert res[0]["task"] == "T1"


def test_filter_by_tags_and_logic():
    add_todo("Task 1", tags=["work", "urgent"])
    add_todo("Task 2", tags=["work"])
    result_and = filter_by_tags(["work", "urgent"], match_all=True)
    assert len(result_and) == 1
    assert result_and[0]["task"] == "Task 1"


def test_filter_by_tags_or_logic():
    add_todo("Task 1", tags=["work", "urgent"])
    add_todo("Task 2", tags=["personal"])
    result_or = filter_by_tags(["urgent", "personal"], match_all=False)
    assert len(result_or) == 2


def test_tag_stats_and_list_all_tags():
    add_todo("One", tags=["a", "b"])
    add_todo("Two", tags=["b"])
    stats = show_tag_stats()
    assert stats["a"] == 1
    assert stats["b"] == 2

    all_tags = list_all_tags()
    assert sorted(all_tags) == ["a", "b"]


def test_add_and_remove_tag_from_task():
    add_todo("Task", tags=["tag1"])
    add_tag_to_task(0, "tag2")
    assert "tag2" in todos[0]["tags"]
    # duplicate add should not create duplicates
    add_tag_to_task(0, "TAG2")
    assert todos[0]["tags"].count("tag2") == 1

    remove_tag_from_task(0, "tag2")
    assert "tag2" not in todos[0]["tags"]


def test_backwards_compatibility_untagged_task():
    # Should allow tasks without tags
    todos.append({"task": "old task", "completed": False})
    assert list_todos() != []
    # show_tag_stats should not crash
    stats = show_tag_stats()
    assert isinstance(stats, dict)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        add_todo(123)  # type: ignore[arg-type]

    # invalid tags
    with pytest.raises(TypeError):
        add_todo("task", tags="notalist")  # type: ignore[arg-type]

    add_todo("T")
    with pytest.raises(IndexError):
        add_tag_to_task(5, "x")
    with pytest.raises(IndexError):
        remove_tag_from_task(5, "x")


def test_filter_empty_tags_list_raises():
    add_todo("T", tags=["x"])
    with pytest.raises(ValueError):
        filter_by_tags([])


@pytest.mark.parametrize("tags, expected_count", [
    (["Work"], 1),
    (["work", "urgent"], 1),
    (["Personal"], 1),
])
def test_case_insensitivity_and_parametrized(tags, expected_count):
    add_todo("One", tags=["Work", "urgent"])
    add_todo("Two", tags=["Personal"])
    result = filter_by_tags(tags, match_all=False)
    assert len(result) == expected_count

def test_filter_by_tags_with_source_list():
    local_todos = [
        {"task": "A", "completed": False, "tags": ["x"]},
        {"task": "B", "completed": False, "tags": ["y"]},
    ]
    res = filter_by_tags(["y"], match_all=False, source_todos=local_todos)
    assert len(res) == 1
    assert res[0]["task"] == "B"
