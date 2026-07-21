"""Contoh menghasilkan profil pengguna terstruktur."""

import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.model import SahabatAIModel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True, help="Lokasi model SahabatAI GGUF")
    args = parser.parse_args()

    model = SahabatAIModel(args.model_path)
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
