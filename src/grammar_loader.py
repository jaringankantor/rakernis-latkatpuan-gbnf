"""Memuat grammar GBNF secara aman dari direktori proyek."""

from pathlib import Path


GRAMMAR_DIR = Path(__file__).resolve().parent.parent / "grammars"


class GrammarNotFoundError(FileNotFoundError):
    """Grammar yang diminta tidak tersedia."""


def available_grammars(grammar_dir: Path = GRAMMAR_DIR) -> list[str]:
    """Kembalikan nama seluruh grammar tanpa ekstensi, terurut alfabetis."""
    return sorted(path.stem for path in grammar_dir.glob("*.gbnf") if path.is_file())


def load_grammar(name: str, grammar_dir: Path = GRAMMAR_DIR) -> str:
    """Muat grammar berdasarkan nama (misalnya ``json`` atau ``json.gbnf``)."""
    safe_name = Path(name).name
    if safe_name != name or safe_name in {"", ".", ".."}:
        raise ValueError("Nama grammar harus berupa nama file tanpa direktori.")
    if not safe_name.endswith(".gbnf"):
        safe_name += ".gbnf"

    path = grammar_dir / safe_name
    if not path.is_file():
        choices = ", ".join(available_grammars(grammar_dir)) or "(tidak ada)"
        raise GrammarNotFoundError(
            f"Grammar '{name}' tidak ditemukan. Grammar tersedia: {choices}"
        )

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Grammar '{name}' kosong.")
    if "root" not in content:
        raise ValueError(f"Grammar '{name}' tidak memiliki rule root.")
    return content
