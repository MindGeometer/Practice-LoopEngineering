# Practice-LoopEngineering

『요즘 AI 루프엔지니어링』(박승규 지음, Golden Rabbit 출판)을 따라 하며 실습하는 저장소입니다.

## 목적

- 책의 예제와 내용을 **그대로 따라 해 보며** 개념을 익힙니다.
- 필요에 따라 **일부를 수정·변형**해 보며 직접 실험하고 이해를 넓힙니다.

## 구성

- 책의 장(Chapter)별로 디렉터리를 나누어 실습 코드와 메모를 정리합니다.
- 원본을 따라 한 부분과 직접 수정한 부분은 가능한 한 구분해서 기록합니다.

### 디렉터리

| 경로 | 설명 |
| --- | --- |
| `chapter1/` | Chapter 1 실습 |
| `chapter1/quote-cli/` | 터미널에서 명언을 출력하는 간단한 CLI 도구 |

### Chapter 1: quote-cli

명언 데이터(`quotes.json`)를 읽어 무작위로 하나 출력하거나(`python quote.py`), `--list`로 전체 목록을 번호와 함께 출력하는 CLI입니다. 표준 라이브러리만 사용하며, 테스트에만 pytest가 필요합니다.

| 파일 | 설명 |
| --- | --- |
| `quote.py` | CLI 본체 |
| `quotes.json` | 명언 데이터 (`text`, `author`) |
| `test_quote.py` | pytest 테스트 |

자세한 설치, 실행 방법과 테스트 내용은 [`chapter1/quote-cli/README.md`](chapter1/quote-cli/README.md)를 참고하세요.

## 참고

- 이 저장소는 개인 학습용이며, 책의 저작권은 저자와 출판사에 있습니다.
