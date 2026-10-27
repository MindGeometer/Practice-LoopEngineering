# todo-cli

할 일을 `todo.json`에 저장하는 간단한 CLI 도구입니다. 명령은 `add`, `list`, `start`, `done` 네 가지입니다.

## 설치

Python 3.12 이상과 [uv](https://docs.astral.sh/uv/)가 필요합니다.

```bash
cd chapter2/todo-cli
uv sync
```

## 실행

`todo-cli`는 이 프로젝트의 가상환경(`.venv`) 안에 설치되므로 `uv run`으로 실행합니다.

```bash
uv run todo-cli <명령> [인수]
```

`.venv`를 활성화(`source .venv/bin/activate`)하면 `uv run` 없이 `todo-cli`만 입력해도 됩니다.

## 명령

| 명령 | 설명 |
| --- | --- |
| `add <제목>` | 할 일을 추가합니다. 새 항목은 `todo` 상태로 시작합니다. |
| `list [--status <상태>]` | 목록을 출력합니다. `--status`는 `todo`, `in_progress`, `done` 중 하나입니다. |
| `start <id>` | 해당 항목을 `in_progress`(진행 중)로 바꿉니다. |
| `done <id>` | 해당 항목을 `done`(완료)으로 바꿉니다. |

## 사용 예시

```console
$ uv run todo-cli add "우유 사기"
추가됨: [ ] 1. 우유 사기
$ uv run todo-cli add 빨래
추가됨: [ ] 2. 빨래
$ uv run todo-cli start 1
[~] 1. 우유 사기
$ uv run todo-cli done 1
[V] 1. 우유 사기
$ uv run todo-cli list
[V] 1. 우유 사기
[ ] 2. 빨래
$ uv run todo-cli list --status todo
[ ] 2. 빨래
```

### 상태 표시

| 상태 | 표시 | 색 |
| --- | --- | --- |
| `todo` | `[ ]` | 회색 |
| `in_progress` | `[~]` | 노랑 |
| `done` | `[V]` | 초록 |

터미널에 출력할 때만 색이 입혀집니다. 출력을 파이프나 파일로 넘기거나 `NO_COLOR` 환경 변수를 설정하면 색 없이 출력됩니다.

## 데이터 파일

- 데이터는 명령을 실행한 **현재 디렉터리**의 `todo.json`에 저장됩니다. 파일이 없으면 `add` 때 만들어집니다.
- 디렉터리마다 별도의 `todo.json`이 생기므로, 같은 목록을 계속 쓰려면 같은 디렉터리에서 실행하세요.
- 항목 형식은 `{"id": 1, "title": "우유 사기", "status": "todo"}`입니다. id는 현재 최대 id + 1로 매겨집니다.
- 상태 전이를 제한하지 않습니다. 이미 `done`인 항목에 `start`를 해도 `in_progress`로 바뀝니다.

## 오류

없는 id를 지정하거나, 제목이 비어 있거나, `todo.json` 형식이 잘못되었으면 stderr에 메시지를 출력하고 종료 코드 1로 끝납니다.

```console
$ uv run todo-cli done 99
오류: id 99번 할 일을 찾을 수 없습니다.
```

## 구조

| 파일 | 설명 |
| --- | --- |
| `src/todo_cli/todos.py` | 목록 조작 순수 로직 (파일·출력 없음) |
| `src/todo_cli/cli.py` | 명령 처리, `todo.json` 읽기/쓰기, 색 출력 |
| `tests/` | pytest 테스트 |

## 테스트

```bash
uv run pytest
```
