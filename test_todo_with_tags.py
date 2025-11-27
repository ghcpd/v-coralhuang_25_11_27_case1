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
    reset_todos,
)


@pytest.fixture(autouse=True)
def clear_todos():
    reset_todos()
    yield
    reset_todos()


def test_add_todo_and_list():
    add_todo("Write report", tags=["Work", "Urgent"])
    add_todo("Call mom")
    all_items = list_todos()
    assert len(all_items) == 2
    assert all_items[0]["task"] == "Write report"
    assert "work" in all_items[0]["tags"]
    assert all_items[1]["tags"] == []


def test_list_todos_filter_tag():
    add_todo("Buy milk", tags=["errand", "grocery"])
    add_todo("Pay bills", tags=["finance"])
    assert len(list_todos("errand")) == 1
    assert list_todos("errand")[0]["task"] == "Buy milk"


def test_filter_by_tags_and_or():
    add_todo("Task 1", tags=["work", "urgent"])
    add_todo("Task 2", tags=["work"])
    add_todo("Task 3", tags=["personal"])

    # OR: any with work or urgent
    result_or = filter_by_tags(None, ["work", "urgent"], match_all=False)
    assert len(result_or) == 2

    # AND: only Task 1
    result_and = filter_by_tags(None, ["work", "urgent"], match_all=True)
    assert len(result_and) == 1
    assert result_and[0]["task"] == "Task 1"


def test_show_tag_stats_and_list_all_tags():
    add_todo("A", tags=["x", "y"])
    add_todo("B", tags=["x"])
    stats = show_tag_stats()
    assert stats.get("x") == 2
    assert stats.get("y") == 1
    assert "x" in list_all_tags()


def test_add_remove_tags_and_duplicates():
    add_todo("Task", tags=["t1"])
    add_tag_to_task(0, "T2")
    add_tag_to_task(0, "t1")  # duplicate should be harmless
    assert set(todos[0]["tags"]) == {"t1", "t2"}
    remove_tag_from_task(0, "t1")
    assert "t1" not in todos[0]["tags"]


def test_errors_and_edge_cases():
    with pytest.raises(ValueError):
        add_todo(123)  # not a string
    with pytest.raises(TypeError):
        add_todo("T", tags="notalist")
    add_todo("ok")
    with pytest.raises(IndexError):
        add_tag_to_task(5, "x")
    with pytest.raises(IndexError):
        remove_tag_from_task(5, "x")
    with pytest.raises(ValueError):
        list_todos(filter_tag=" ")
    with pytest.raises(ValueError):
        filter_by_tags(None, [])
