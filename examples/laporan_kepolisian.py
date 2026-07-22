"""Contoh menghasilkan laporan masyarakat untuk kepolisian."""

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
            (
                "Saya Andi nomor telepon 081298765432. Saat ini ada seorang pria tidak dikenal yang mencoba mendobrak pintu rumah saya di Jalan Melati Nomor 15, Jakarta Selatan. Kejadian mulai sekitar pukul 02.10 pada 22 Juli 2026. Pria tersebut membawa benda yang menyerupai linggis dan masih berada di depan rumah. Saya bersama istri dan anak sedang mengunci diri di kamar. Tetangga saya, Ibu Sari, juga melihat pelaku dari rumahnya. Rekaman kamera keamanan tersedia. Mohon petugas segera datang karena kami merasa terancam."
            ),
            "laporan-kepolisian",
            system_prompt=(
                "Ubah keterangan masyarakat menjadi laporan kepolisian berformat JSON. "
                "Gunakan string kosong atau array kosong untuk informasi yang tidak tersedia. "
                "Jangan mengarang informasi. Isi tindakan_segera dengan true hanya jika ada "
                "ancaman atau bahaya yang sedang berlangsung."
            ),
        )
    )


if __name__ == "__main__":
    main()
