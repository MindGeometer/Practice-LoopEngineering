# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 맥락

『요즘 AI 루프엔지니어링』(박승규 지음)을 따라 하는 개인 학습 저장소입니다. 루트의 `chapterN/` 아래에 장별 프로젝트가 있고, 이 디렉터리(`chapter2/todo-cli`)는 `uv`로 관리되는 독립 파이썬 프로젝트입니다(`chapter1/quote-cli`는 `uv` 없이 표준 라이브러리 + pytest만 사용). 원본을 따라 한 부분과 직접 수정한 부분은 가능하면 구분해서 기록하는 것이 저장소 방침입니다.

## 명령어

모든 명령은 `chapter2/todo-cli/`에서 실행합니다.

```bash
uv sync                          # .venv 생성 및 의존성 설치 (Python 3.12, .python-version)
uv run todo-cli                  # 콘솔 스크립트 실행 (todo_cli:main)
uv run pytest                    # 전체 테스트
uv run pytest tests/test_x.py::test_name   # 단일 테스트
uv add <pkg> / uv add --dev <pkg>          # 의존성 추가 (pyproject.toml, uv.lock 갱신)
```

## 규칙

- 패키지 관리와 실행은 `uv`로 한다 (`pip` 대신).
- 기능을 추가하면 `uv run pytest`를 꼭 통과시킨다.
- CLI 입출력과 순수 로직(목록 조작)은 파일을 나눈다.

## 구조

- `src/` 레이아웃 + `uv_build` 빌드 백엔드. 패키지는 `src/todo_cli/`이며, `pyproject.toml`의 `[project.scripts]`가 `todo-cli = "todo_cli:main"`으로 `__init__.py`의 `main()`을 진입점으로 지정합니다. 진입점 함수 이름·위치를 바꾸면 이 항목도 함께 수정해야 합니다.
- `todos.py`: 순수 로직(`add_todo`, `start_todo`, `done_todo`, `filter_todos`, `format_todo`). 입력 리스트를 변경하지 않고 새 리스트를 반환하며, 잘못된 입력은 `ValueError`로 알립니다. 파일·print·argparse를 넣지 않습니다.
- `cli.py`: argparse 서브커맨드(`add`/`list`/`start`/`done`), `todo.json`(실행한 현재 디렉터리) 읽기/쓰기, 출력. `ValueError`를 잡아 stderr 출력 후 종료 코드 1로 끝냅니다. `__init__.py`는 `main`만 재노출합니다.
- 상태별 색(todo 회색, in_progress 노랑, done 초록)은 출력 계층인 `cli.py`의 `render`/`use_color`에서만 입힙니다. `todos.format_todo`는 색 없는 평문을 유지합니다. stdout이 TTY가 아니거나 `NO_COLOR`가 설정되면 색을 끕니다.
- 테스트: `tests/test_todos.py`는 `todos.py`의 순수 로직, `tests/test_cli.py`는 `cli.render`(평문/색 출력)를 대상으로 합니다.
- `README.md`에 사용자용 사용법(명령, 예시, 상태 표시, 데이터 파일)이 정리되어 있습니다. 명령이나 출력 형식을 바꾸면 함께 갱신합니다.
- 항목 형식은 `{"id", "title", "status"}`이고 status는 `todo` → `in_progress` → `done`입니다. 역방향 전이는 막지 않습니다.
