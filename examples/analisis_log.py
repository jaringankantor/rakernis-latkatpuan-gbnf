"""Contoh menganalisis log perangkat jaringan atau server."""

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

    log = """Sumber: core-switch-01
2026-07-23T08:14:02+07:00 %LINK-3-UPDOWN: Interface GigabitEthernet1/0/24, changed state to down
2026-07-23T08:14:04+07:00 %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0/24, changed state to down
2026-07-23T08:14:10+07:00 %SW_MATM-4-MACFLAP_NOTIF: Host 00aa.11bb.22cc in vlan 120 is flapping between port Gi1/0/23 and port Gi1/0/24
2026-07-23T08:14:16+07:00 %LINK-3-UPDOWN: Interface GigabitEthernet1/0/24, changed state to up
2026-07-23T08:14:21+07:00 %SW_MATM-4-MACFLAP_NOTIF: Host 00aa.11bb.22cc in vlan 120 is flapping between port Gi1/0/23 and port Gi1/0/24
"""

    model = SahabatAIModel(args.model_path)
    print(
        model.generate(
            f"Analisis log berikut:\n\n{log}",
            "analisis-log",
            system_prompt=(
                "Analisis log perangkat jaringan atau server dan keluarkan JSON sesuai grammar. "
                "Gunakan hanya fakta dari log; jangan mengarang. Bedakan gejala, dampak, dan dugaan "
                "masalah. Tetapkan perlu_tindak_lanjut=true dan urgensi=segera hanya jika terdapat "
                "insiden aktif, gangguan layanan, risiko keamanan, kehilangan data, atau kondisi kritis. "
                "Masukkan baris log relevan ke bukti_log, langkah aman ke rekomendasi, dan data yang "
                "belum tersedia ke informasi_tambahan_dibutuhkan. Jangan menampilkan kredensial atau "
                "data rahasia yang mungkin terdapat dalam log."
            ),
            max_tokens=1024,
        )
    )


if __name__ == "__main__":
    main()
