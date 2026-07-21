# SahabatAI GBNF

Proyek contoh untuk membatasi keluaran LLM SahabatAI menggunakan **GBNF (Grammar-Based Normal Form)**. Grammar diterapkan melalui `llama-cpp-python`, sehingga model hanya menghasilkan struktur yang telah ditentukan.

## Fitur

- Grammar JSON generik
- Jawaban tegas `ya` atau `tidak`
- Profil pengguna terstruktur
- CLI dan contoh penggunaan Python
- Validasi grammar dan keluaran melalui `pytest`

## Persiapan

Prasyarat: Python 3.10+ dan model SahabatAI berformat GGUF.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Penggunaan cepat

```bash
python -m src.main --model-path ../models/SahabatAI/gemma2-9b-cpt-sahabatai-v1-instruct.Q4_K_M.gguf --grammar json --prompt "Pengguna bernama Anwar dan tinggal di Jakarta. Keluarkan objek JSON dengan field nama dan kota."
```

Grammar yang tersedia: `json`, `yes-no`, dan `user-profile`. Jalankan `python -m src.main --help` untuk opsi lengkap.

```bash
pytest
```

Lihat [docs/usage.md](docs/usage.md) untuk panduan lebih lengkap.

## Struktur

```text
grammars/   Definisi constraint GBNF
prompts/    System prompt dan contoh few-shot
src/        Loader grammar, wrapper model, dan CLI
tests/      Tes grammar dan validasi keluaran
examples/   Contoh skrip siap jalan
outputs/    Lokasi keluaran lokal (tidak dilacak Git)
docs/       Dokumentasi penggunaan
```

## Lisensi

MIT — lihat [LICENSE](LICENSE).
