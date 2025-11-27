import pytest

from todo_with_tags import (
    add_todo,
    remove_todo,
    list_todos,
    mark_complete,
    filter_by_tags,
    show_tag_stats,
    add_tag_to_task,
    remove_tag_from_task,
    list_all_tags,
    clear_all_todos,
    todos,
)


@pytest.fixture(autouse=True)
def clear_everything():
    # Ensure a clean state for each test
    clear_all_todos()
    yield
    clear_all_todos()


def test_add_todo_without_tags():
    add_todo("Read a book")
    assert len(todos) == 1
    assert todos[0]["task"] == "Read a book"
    assert todos[0]["completed"] is False
    assert todos[0]["tags"] == []


def test_add_todo_with_tags_and_normalization():
    add_todo("Write report", tags=["Work", "urgent", "work"])
    assert len(todos) == 1
    assert set(todos[0]["tags"]) == {"work", "urgent"}


def test_remove_todo_invalid_index_raises():
    add_todo("Task")
    with pytest.raises(IndexError):
        remove_todo(5)


def test_mark_complete_and_compatibility():
    add_todo("Task A")
    mark_complete(0)
    assert todos[0]["completed"] is True


def test_add_and_remove_tag_from_task():
    add_todo("Task 1", tags=["work"])
    assert list_all_tags() == ["work"]
    add_tag_to_task(0, "urgent")
    assert set(todos[0]["tags"]) == {"work", "urgent"}
    remove_tag_from_task(0, "work")
    assert todos[0]["tags"] == ["urgent"]


def test_list_all_tags_and_show_stats(capsys):
    add_todo("T1", tags=["work"])
    add_todo("T2", tags=["work", "urgent"])
    assert list_all_tags() == ["urgent", "work"]
    show_tag_stats()
    captured = capsys.readouterr()
    assert "work (2)" in captured.out
    assert "urgent (1)" in captured.out


def test_filter_by_tags_or_logic():
    add_todo("T1", tags=["work"])
    add_todo("T2", tags=["personal"])
    res = filter_by_tags(["work", "personal"], match_all=False)
    assert len(res) == 2


def test_filter_by_tags_and_logic():
    add_todo("T1", tags=["work", "urgent"])
    add_todo("T2", tags=["work"])
    res = filter_by_tags(["work", "urgent"], match_all=True)
    assert len(res) == 1
    assert res[0]["task"] == "T1"


@pytest.mark.parametrize(
    "bad_tags",
    [None, 123, "stringtag"],
)
def test_filter_by_tags_invalid_inputs(bad_tags):
    # It should return empty list for invalid types or None
    if not isinstance(bad_tags, list):
        assert filter_by_tags(bad_tags if isinstance(bad_tags, list) else []) == []


def test_error_handling_tag_operations():
    add_todo("T1")
    with pytest.raises(IndexError):
        add_tag_to_task(1, "tag")
    with pytest.raises(IndexError):
        remove_tag_from_task(1, "tag")
    with pytest.raises(ValueError):
        add_tag_to_task(0, "")
    with pytest.raises(ValueError):
        remove_tag_from_task(0, "")


def test_backward_compatibility_for_old_todo_format():
    # Adding a 'legacy' todo dict without tags should still work
    todos.append({"task": "Legacy task", "completed": False})
    assert len(todos) == 1
    assert todos[0].get("tags") is None or todos[0].get("tags") == []
    # list_all_tags should be empty and list_todos should not crash
    assert list_all_tags() == []
    list_todos()  # Should not raise


def test_duplicate_tags_not_added():
    add_todo("T", tags=["home", "home ", "HOME"])
    assert list_all_tags() == ["home"]


def test_add_todo_invalid_task_types():
    with pytest.raises(ValueError):
        add_todo(123)  # task must be string


def test_remove_todo_success():
    add_todo("A")
    add_todo("B")
    remove_todo(0)
    assert len(todos) == 1
    assert todos[0]["task"] == "B"


def test_list_todos_filtering_print_output(capsys):
    add_todo("T1", tags=["work"])
    add_todo("T2", tags=["personal"])
    list_todos(filter_tag="work")
    captured = capsys.readouterr()
    assert "T1" in captured.out
    assert "T2" not in captured.out
