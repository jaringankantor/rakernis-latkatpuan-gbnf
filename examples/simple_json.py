"""Contoh menghasilkan JSON terstruktur."""

import argparse
import sys
from pathlib import Path

# Saat skrip dijalankan sebagai `python examples/simple_json.py`, Python hanya
# menambahkan direktori `examples` ke import path. Tambahkan root proyek agar
# paket `src` tetap dapat diimpor.
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

    system_prompt = (PROJECT_DIR / "prompts" / "system-prompt.txt").read_text(
        encoding="utf-8"
    )
    model = (
        GrokAPIModel.from_env(model=args.grok_model)
        if args.model_token
        else SahabatAIModel(args.model_path)
    )
    print(
        model.generate(
            "Buat objek satu produk kopi dengan atribut nama, harga, dan tersedia.",
            "json",
            system_prompt=system_prompt,
        )
    )


if __name__ == "__main__":
    main()
