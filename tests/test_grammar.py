from pathlib import Path

import pytest

from src.grammar_loader import GrammarNotFoundError, available_grammars, load_grammar


def test_expected_grammars_are_available() -> None:
    assert available_grammars() == ["json", "user-profile", "yes-no"]


@pytest.mark.parametrize("name", ["json", "yes-no.gbnf", "user-profile"])
def test_grammar_has_root_rule(name: str) -> None:
    assert "root" in load_grammar(name)


def test_unknown_grammar_raises_clear_error() -> None:
    with pytest.raises(GrammarNotFoundError, match="tidak ditemukan"):
        load_grammar("unknown")


def test_path_traversal_is_rejected() -> None:
    with pytest.raises(ValueError, match="tanpa direktori"):
        load_grammar("../secret")


def test_empty_grammar_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "empty.gbnf").write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="kosong"):
        load_grammar("empty", tmp_path)
