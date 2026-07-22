"""Contoh menghasilkan jawaban ya/tidak."""

import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.model import GrokAPIModel, SahabatAIModel


def main() -> None:
    parser = argparse.ArgumentParser()
    model_source = parser.add_mutually_exclusive_group(required=True)
    model_source.add_argument("--model-path", help="Lokasi model SahabatAI GGUF")
    model_source.add_argument("--model-token", action="store_true", help="Gunakan XAI_API_KEY dari .env")
    parser.add_argument("--grok-model", default="grok-4.5", help="Nama model Grok")
    args = parser.parse_args()

    model = (
        GrokAPIModel.from_env(model=args.grok_model)
        if args.model_token
        else SahabatAIModel(args.model_path)
    )
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
