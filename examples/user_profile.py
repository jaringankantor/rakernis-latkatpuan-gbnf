"""Contoh menghasilkan profil pengguna terstruktur."""

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
            "Saya Purnomo, berusia 46 tahun, tinggal di Lamongan, dan menyukai musik serta lari.",
            "user-profile",
            system_prompt=(
                "Ubah informasi pengguna menjadi profil JSON dengan field nama, usia, "
                "kota, dan minat. Jangan menambahkan informasi yang tidak diberikan."
            ),
        )
    )


if __name__ == "__main__":
    main()
