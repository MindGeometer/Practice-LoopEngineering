import pytest

from todo_cli.todos import (
    add_todo,
    done_todo,
    filter_todos,
    format_todo,
    start_todo,
)


def make(id, title="할 일", status="todo"):
    return {"id": id, "title": title, "status": status}


def test_add_to_empty_list_gets_id_1():
    todos, item = add_todo([], "우유 사기")
    assert item == make(1, "우유 사기")
    assert todos == [item]


def test_add_increments_from_max_id():
    todos, item = add_todo([make(1), make(5)], "새 일")
    assert item["id"] == 6
    assert len(todos) == 3


def test_add_does_not_mutate_input():
    original = [make(1)]
    add_todo(original, "새 일")
    assert original == [make(1)]


@pytest.mark.parametrize("title", ["", "   "])
def test_add_rejects_blank_title(title):
    with pytest.raises(ValueError):
        add_todo([], title)


def test_start_sets_in_progress_only_for_target():
    result = start_todo([make(1), make(2)], 2)
    assert [t["status"] for t in result] == ["todo", "in_progress"]


def test_done_sets_done():
    result = done_todo([make(1, status="in_progress")], 1)
    assert result[0]["status"] == "done"


def test_start_and_done_do_not_mutate_input():
    original = [make(1)]
    start_todo(original, 1)
    done_todo(original, 1)
    assert original == [make(1)]


@pytest.mark.parametrize("func", [start_todo, done_todo])
def test_unknown_id_raises(func):
    with pytest.raises(ValueError):
        func([make(1)], 99)


def test_filter_by_status_and_none():
    todos = [make(1), make(2, status="done"), make(3, status="todo")]
    assert [t["id"] for t in filter_todos(todos, "todo")] == [1, 3]
    assert filter_todos(todos) == todos


@pytest.mark.parametrize(
    "status, mark",
    [("todo", "[ ]"), ("in_progress", "[~]"), ("done", "[V]")],
)
def test_format_todo(status, mark):
    assert format_todo(make(1, "우유 사기", status)) == f"{mark} 1. 우유 사기"
