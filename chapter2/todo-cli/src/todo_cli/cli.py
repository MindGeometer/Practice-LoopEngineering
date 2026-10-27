import argparse
import json
import os
import sys
from pathlib import Path

from todo_cli import todos as logic

TODO_PATH = Path("todo.json")

_COLORS = {"todo": "90", "in_progress": "33", "done": "32"}


def use_color(stream=None):
    stream = stream or sys.stdout
    return "NO_COLOR" not in os.environ and stream.isatty()


def render(item, color):
    line = logic.format_todo(item)
    if not color:
        return line
    return f"\033[{_COLORS[item['status']]}m{line}\033[0m"


def load(path):
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"todo 파일 형식이 잘못되었습니다: {path}")
    if not isinstance(data, list):
        raise ValueError(f"todo 파일 형식이 잘못되었습니다: {path}")
    return data


def save(path, items):
    path.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def build_parser():
    parser = argparse.ArgumentParser(prog="todo-cli")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="할 일 추가")
    p_add.add_argument("title")

    p_list = sub.add_parser("list", help="할 일 목록")
    p_list.add_argument("--status", choices=logic.STATUSES)

    for name, help_text in (("start", "진행 시작"), ("done", "완료 처리")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("id", type=int)

    return parser


def run(args, path):
    items = load(path)
    color = use_color()
    if args.command == "add":
        items, item = logic.add_todo(items, args.title)
        save(path, items)
        print(f"추가됨: {render(item, color)}")
    elif args.command == "list":
        for item in logic.filter_todos(items, args.status):
            print(render(item, color))
    else:
        action = logic.start_todo if args.command == "start" else logic.done_todo
        items = action(items, args.id)
        save(path, items)
        print(render(next(t for t in items if t["id"] == args.id), color))


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        run(args, TODO_PATH)
    except ValueError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
