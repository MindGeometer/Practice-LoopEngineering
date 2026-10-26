import json
import subprocess
import sys
from pathlib import Path

import pytest

import quote

BASE_DIR = Path(__file__).parent
SCRIPT = BASE_DIR / "quote.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=BASE_DIR,
    )


def load_expected():
    with (BASE_DIR / "quotes.json").open(encoding="utf-8") as f:
        return json.load(f)


def test_quotes_json_is_valid():
    quotes = load_expected()
    assert quotes
    for q in quotes:
        assert q["text"].strip()
        assert q["author"].strip()


def test_quotes_json_has_no_duplicate_text():
    texts = [q["text"] for q in load_expected()]
    assert len(texts) == len(set(texts))


def test_no_args_prints_single_quote_line():
    result = run_cli()
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 1
    assert lines[0] in {quote.format_quote(q) for q in load_expected()}


@pytest.mark.parametrize("index", [0, -1])
def test_no_args_prints_the_chosen_quote(monkeypatch, capsys, index):
    quotes = load_expected()
    monkeypatch.setattr(sys, "argv", ["quote.py"])
    monkeypatch.setattr(quote.random, "choice", lambda seq: seq[index])
    assert quote.main() == 0
    assert capsys.readouterr().out == quote.format_quote(quotes[index]) + "\n"


def test_no_args_is_not_always_the_same_quote(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["quote.py"])
    outputs = set()
    for _ in range(200):
        quote.main()
        outputs.add(capsys.readouterr().out)
    assert len(outputs) > 1


def test_list_prints_all_quotes():
    expected = load_expected()
    result = run_cli("--list")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == len(expected)
    for i, (line, q) in enumerate(zip(lines, expected), 1):
        assert line == f"{i}. {quote.format_quote(q)}"


def write_quotes(tmp_path, content):
    path = tmp_path / "quotes.json"
    path.write_text(content, encoding="utf-8")
    return path


def test_load_quotes_missing_file(tmp_path):
    with pytest.raises(quote.QuoteError, match="찾을 수 없습니다"):
        quote.load_quotes(tmp_path / "none.json")


def test_load_quotes_invalid_json(tmp_path):
    with pytest.raises(quote.QuoteError, match="JSON"):
        quote.load_quotes(write_quotes(tmp_path, "{not json"))


def test_load_quotes_empty_list(tmp_path):
    with pytest.raises(quote.QuoteError, match="명언이 없습니다"):
        quote.load_quotes(write_quotes(tmp_path, "[]"))


@pytest.mark.parametrize(
    "content",
    ['[{"text": "a"}]', '[{"author": "b"}]', '[{"text": " ", "author": "b"}]', '["a"]'],
)
def test_load_quotes_invalid_entry(tmp_path, content):
    with pytest.raises(quote.QuoteError, match="1번째 항목"):
        quote.load_quotes(write_quotes(tmp_path, content))


def test_cli_reports_error_and_exits_nonzero(monkeypatch, capsys):
    monkeypatch.setattr(quote, "QUOTES_PATH", Path("/nonexistent/quotes.json"))
    monkeypatch.setattr(sys, "argv", ["quote.py"])
    assert quote.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("오류:")


def test_format_quote():
    assert quote.format_quote({"text": "안녕", "author": "나"}) == '"안녕" - 나'
