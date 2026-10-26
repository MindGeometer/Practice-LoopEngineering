# quote-cli

터미널에서 명언을 출력하는 간단한 CLI 도구입니다. 명언 데이터는 `quotes.json`에 분리되어 있습니다.

## 구성

| 파일 | 설명 |
| --- | --- |
| `quote.py` | CLI 본체 |
| `quotes.json` | 명언 데이터 (`text`, `author`) |
| `test_quote.py` | pytest 테스트 |

## 설치

Python 3 이상이 필요합니다. 실행 자체에는 외부 패키지가 필요 없습니다(표준 라이브러리만 사용).

```bash
git clone <저장소 URL>
cd quote-cli
```

테스트를 실행하려면 pytest를 설치하세요.

```bash
pip install pytest
```

## 실행 예시

인수 없이 실행하면 무작위 명언 하나를 출력합니다.

```console
$ python quote.py
"오늘 할 수 있는 일을 내일로 미루지 마라." - 벤자민 프랭클린
```

`--list`를 주면 전체 목록을 번호와 함께 출력합니다.

```console
$ python quote.py --list
1. "배움에는 왕도가 없다." - 유클리드
2. "천 리 길도 한 걸음부터." - 노자
3. "가장 어두운 밤도 결국은 끝나고 해는 떠오른다." - 빅토르 위고
...
```

항목 수는 `quotes.json`에 따라 달라집니다.

`quotes.json`이 없거나, 형식이 잘못되었거나, 비어 있으면 오류 메시지를 stderr에 출력하고 종료 코드 1로 끝납니다.

```console
$ python quote.py
오류: 명언 파일을 찾을 수 없습니다: /path/to/quotes.json
```

## 명언 추가

`quotes.json`에 항목을 추가하면 됩니다. 문장이 중복되지 않게 해주세요.

```json
{"text": "명언 내용", "author": "저자"}
```

## 테스트

```bash
python -m pytest test_quote.py -v
```

다음 내용을 검증합니다.

- 인수 없이 실행하면 `quotes.json`에 있는 명언이 한 줄 출력된다.
- `--list`를 주면 전체 항목이 순서대로 출력된다.
- `quotes.json`의 모든 항목에 `text`와 `author`가 있고, 문장이 중복되지 않는다.
