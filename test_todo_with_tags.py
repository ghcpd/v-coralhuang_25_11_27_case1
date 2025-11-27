import pytest

import todo_with_tags as twt


@pytest.fixture(autouse=True)
def clear_state():
    # Ensure clean slate for every test
    twt.clear_todos()
    yield
    twt.clear_todos()


@pytest.fixture
def sample_todos():
    return [
        {"task": "Task 1", "completed": False, "tags": ["work", "urgent"]},
        {"task": "Task 2", "completed": True, "tags": ["work"]},
        {"task": "Task 3", "completed": False, "tags": ["personal"]},
    ]


# ---- Unit tests ----
def test_add_todo_with_tags_normalizes_and_dedupes():
    todo = twt.add_todo("Write report", tags=["Work", "urgent", "work"])
    assert todo["tags"] == ["work", "urgent"]
    assert twt.todos[0]["tags"] == ["work", "urgent"]


def test_add_todo_empty_task_raises():
    with pytest.raises(ValueError):
        twt.add_todo("   ")


def test_add_todo_invalid_tags_raises():
    with pytest.raises(TypeError):
        twt.add_todo("Task", tags="not-a-list")  # type: ignore

    with pytest.raises(TypeError):
        twt.add_todo("Task", tags=[123])  # type: ignore


@pytest.mark.parametrize(
    "tags,match_all,expected",
    [
        (["work"], False, 2),
        (["urgent"], False, 1),
        (["work", "urgent"], True, 1),
        (["work", "personal"], False, 3),
        (["work", "personal"], True, 0),
    ],
)
def test_filter_by_tags_modes(tags, match_all, expected, sample_todos):
    result = twt.filter_by_tags(tags, match_all=match_all, todos_list=sample_todos)
    assert len(result) == expected


def test_filter_by_tags_empty_input_returns_empty(sample_todos):
    assert twt.filter_by_tags([], todos_list=sample_todos) == []


def test_list_todos_outputs_with_tags(capsys):
    twt.add_todo("Write report", tags=["work", "urgent"])
    twt.list_todos()
    captured = capsys.readouterr().out
    assert "Write report" in captured
    assert "work" in captured and "urgent" in captured


def test_show_tag_stats_prints_sorted(capsys, sample_todos):
    stats = twt.show_tag_stats(sample_todos)
    assert stats == {"work": 2, "urgent": 1, "personal": 1}
    out = capsys.readouterr().out
    # First line after header should be work (highest count)
    assert "work" in out.splitlines()[2]


def test_add_remove_tag_to_task():
    twt.add_todo("Task")
    assert twt.add_tag_to_task(0, "Work") is True
    assert twt.add_tag_to_task(0, "work") is False  # no dupes
    assert twt.remove_tag_from_task(0, "work") is True
    assert twt.remove_tag_from_task(0, "work") is False


def test_add_remove_tag_invalid_index():
    twt.add_todo("Task")
    with pytest.raises(IndexError):
        twt.add_tag_to_task(5, "work")
    with pytest.raises(IndexError):
        twt.remove_tag_from_task(5, "work")


def test_list_all_tags_returns_sorted(sample_todos):
    tags = twt.list_all_tags(sample_todos)
    assert tags == ["personal", "urgent", "work"]


# ---- Backward compatibility ----
def test_untagged_tasks_work():
    twt.add_todo("Plain task")
    assert len(twt.todos) == 1
    assert twt.todos[0]["tags"] == []
    # Filtering by non-existent tag yields none
    assert twt.filter_by_tags(["work"]) == []


# ---- Integration ----
def test_full_workflow():
    t1 = twt.add_todo("Write report", tags=["work", "urgent"])
    t2 = twt.add_todo("Buy milk", tags=["personal"])
    # Filter
    work_items = twt.filter_by_tags(["work"])
    assert len(work_items) == 1 and work_items[0]["task"] == t1["task"]
    # Complete
    twt.mark_complete(0)
    assert twt.todos[0]["completed"] is True
    # Tag update
    twt.add_tag_to_task(1, "errand")
    assert "errand" in twt.todos[1]["tags"]
    twt.remove_tag_from_task(1, "errand")
    # Removal
    removed = twt.remove_todo(1)
    assert removed["task"] == t2["task"]
    assert len(twt.todos) == 1


def test_tag_case_normalization():
    twt.add_todo("Task", tags=["Work"])
    assert twt.filter_by_tags(["work"])  # normalized
    assert not twt.filter_by_tags(["WORK"], match_all=True) == []  # also normalized


# ---- Error handling ----
def test_remove_todo_invalid_index_raises():
    with pytest.raises(IndexError):
        twt.remove_todo(0)


def test_mark_complete_invalid_index_raises():
    with pytest.raises(IndexError):
        twt.mark_complete(99)


def test_empty_tag_string_raises():
    with pytest.raises(ValueError):
        twt.add_todo("Task", tags=[" "])
    twt.add_todo("Task2")
    with pytest.raises(ValueError):
        twt.add_tag_to_task(0, " ")
