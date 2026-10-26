import argparse
import json
import random
import sys
from pathlib import Path

QUOTES_PATH = Path(__file__).with_name("quotes.json")


class QuoteError(Exception):
    pass


def load_quotes(path=None):
    path = path or QUOTES_PATH
    try:
        with Path(path).open(encoding="utf-8") as f:
            quotes = json.load(f)
    except FileNotFoundError:
        raise QuoteError(f"명언 파일을 찾을 수 없습니다: {path}")
    except json.JSONDecodeError as e:
        raise QuoteError(f"{path}이(가) 올바른 JSON이 아닙니다: {e}")

    if not isinstance(quotes, list):
        raise QuoteError(f"{path}의 최상위 값은 목록이어야 합니다.")
    if not quotes:
        raise QuoteError(f"{path}에 명언이 없습니다.")
    for i, quote in enumerate(quotes, 1):
        if not isinstance(quote, dict) or not all(
            isinstance(quote.get(key), str) and quote[key].strip()
            for key in ("text", "author")
        ):
            raise QuoteError(
                f"{path}의 {i}번째 항목에는 비어 있지 않은 text와 author가 필요합니다."
            )
    return quotes


def format_quote(quote):
    return f'"{quote["text"]}" - {quote["author"]}'


def main():
    parser = argparse.ArgumentParser(description="명언을 출력합니다.")
    parser.add_argument("--list", action="store_true", help="전체 명언 목록 출력")
    args = parser.parse_args()

    try:
        quotes = load_quotes()
    except QuoteError as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1

    if args.list:
        for i, quote in enumerate(quotes, 1):
            print(f"{i}. {format_quote(quote)}")
    else:
        print(format_quote(random.choice(quotes)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
