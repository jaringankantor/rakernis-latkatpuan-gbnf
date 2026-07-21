"""Contoh menghasilkan jawaban ya/tidak."""

import argparse

from src.model import SahabatAIModel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", help="Lokasi model SahabatAI GGUF")
    args = parser.parse_args()

    model = SahabatAIModel(args.model_path)
    print(
        model.generate(
            "Apakah air membeku pada suhu 0 derajat Celsius pada tekanan normal?",
            "yes-no",
            system_prompt="Jawab pertanyaan hanya dengan ya atau tidak.",
            max_tokens=8,
        )
    )


if __name__ == "__main__":
    main()
