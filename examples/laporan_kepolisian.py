"""Contoh menghasilkan laporan masyarakat untuk kepolisian."""

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
            (
                "Saya Rina, nomor telepon 081234567890. Ponsel saya dicuri pada "
                "20 Juli 2026 sekitar pukul 19.30 di area parkir Pasar Baru, Jakarta. "
                "Saya tidak melihat pelakunya. Pak Dedi, petugas parkir, melihat seseorang "
                "membawa ponsel saya. Bukti yang saya miliki adalah rekaman CCTV dan nota "
                "pembelian ponsel. Situasi saat ini sudah aman."
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
