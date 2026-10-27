"""todo 목록을 다루는 순수 로직. 파일 입출력, print, argparse는 cli.py에서만 한다."""

STATUSES = ("todo", "in_progress", "done")
_MARKS = {"todo": "[ ]", "in_progress": "[~]", "done": "[V]"}


def add_todo(todos, title):
    title = title.strip()
    if not title:
        raise ValueError("제목이 비어 있습니다.")
    next_id = max((t["id"] for t in todos), default=0) + 1
    item = {"id": next_id, "title": title, "status": "todo"}
    return [*todos, item], item


def _set_status(todos, todo_id, status):
    if not any(t["id"] == todo_id for t in todos):
        raise ValueError(f"id {todo_id}번 할 일을 찾을 수 없습니다.")
    return [{**t, "status": status} if t["id"] == todo_id else t for t in todos]


def start_todo(todos, todo_id):
    return _set_status(todos, todo_id, "in_progress")


def done_todo(todos, todo_id):
    return _set_status(todos, todo_id, "done")


def filter_todos(todos, status=None):
    if status is None:
        return list(todos)
    return [t for t in todos if t["status"] == status]


def format_todo(item):
    return f"{_MARKS[item['status']]} {item['id']}. {item['title']}"
