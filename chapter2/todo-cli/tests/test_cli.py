from todo_cli.cli import render


def item(status):
    return {"id": 1, "title": "우유 사기", "status": status}


def test_render_without_color_is_plain():
    assert render(item("done"), False) == "[V] 1. 우유 사기"


def test_render_color_differs_per_status():
    lines = {s: render(item(s), True) for s in ("todo", "in_progress", "done")}
    assert len(set(lines.values())) == 3
    assert all(line.endswith("\033[0m") for line in lines.values())
