"""Contoh menghasilkan JSON terstruktur."""

import argparse
from pathlib import Path

from src.model import SahabatAIModel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", help="Lokasi model SahabatAI GGUF")
    args = parser.parse_args()

    system_prompt = (Path(__file__).parents[1] / "prompts" / "system-prompt.txt").read_text(
        encoding="utf-8"
    )
    model = SahabatAIModel(args.model_path)
    print(
        model.generate(
            "Buat objek satu produk kopi dengan atribut nama, harga, dan tersedia.",
            "json",
            system_prompt=system_prompt,
        )
    )


if __name__ == "__main__":
    main()
