# SahabatAI GBNF

Proyek contoh untuk membatasi keluaran LLM SahabatAI menggunakan **GBNF (Grammar-Based Normal Form)**. Grammar diterapkan melalui `llama-cpp-python`, sehingga model hanya menghasilkan struktur yang telah ditentukan.

## Fitur

- Grammar JSON generik
- Jawaban tegas `ya` atau `tidak`
- Profil pengguna terstruktur
- Analisis log perangkat jaringan atau server
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

Grammar yang tersedia: `json`, `yes-no`, `user-profile`, `laporan-kepolisian`, dan `analisis-log`. Jalankan `python -m src.main --help` untuk opsi lengkap.

Untuk memakai Grok API sebagai pengganti model GGUF lokal:

```bash
cp .env.example .env
# Isi XAI_API_KEY di dalam .env terlebih dahulu.
python -m src.main \
  --model-token \
  --grok-model grok-4.5 \
  --grammar analisis-log \
  --prompt "Analisis log berikut: ..."
```

Token dibaca dari `XAI_API_KEY` dalam file `.env` yang diabaikan Git. Opsi
`--model-token` dan `--model-path` tidak dapat digunakan bersamaan.

## Menjalankan examples

Jalankan skrip contoh dari root proyek setelah virtual environment aktif.

Contoh menghasilkan JSON terstruktur:

```bash
python examples/simple_json.py --model-path ../models/SahabatAI/gemma2-9b-cpt-sahabatai-v1-instruct.Q4_K_M.gguf
```

Contoh menghasilkan jawaban `ya` atau `tidak`:

```bash
python examples/yes_no.py --model-path ../models/SahabatAI/gemma2-9b-cpt-sahabatai-v1-instruct.Q4_K_M.gguf
```

Contoh menghasilkan profil pengguna terstruktur:

```bash
python examples/user_profile.py --model-path ../models/SahabatAI/gemma2-9b-cpt-sahabatai-v1-instruct.Q4_K_M.gguf
```

Contoh menghasilkan laporan masyarakat untuk kepolisian:

```bash
python examples/laporan_kepolisian.py --model-path ../models/SahabatAI/gemma2-9b-cpt-sahabatai-v1-instruct.Q4_K_M.gguf
```

Contoh menganalisis log perangkat jaringan atau server:

```bash
python examples/analisis_log.py --model-path ../models/SahabatAI/gemma2-9b-cpt-sahabatai-v1-instruct.Q4_K_M.gguf
```

Gunakan lokasi file GGUF yang sesuai apabila model disimpan di direktori lain.
Seluruh skrip contoh juga menerima flag `--model-token` sebagai
pengganti `--model-path`, serta opsi `--grok-model` bila ingin mengganti model
Grok bawaan.

## Menjalankan tes

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
