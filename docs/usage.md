# Panduan Penggunaan

## 1. Siapkan lingkungan

Gunakan Python 3.10 atau lebih baru. Instal dependensi di virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Siapkan model SahabatAI dalam format GGUF. File model sengaja diabaikan oleh Git karena ukurannya besar.

## 2. Jalankan CLI

Perintah dasar:

```bash
python -m src.main \
  --model-path models/sahabatai.gguf \
  --grammar user-profile \
  --prompt "Saya Budi, berusia 31 tahun, tinggal di Solo, suka musik dan lari."
```

Keluaran mengikuti urutan field yang ditentukan grammar:

```json
{"nama":"Budi","usia":31,"kota":"Solo","minat":["musik","lari"]}
```

Untuk akselerasi GPU, sesuaikan `--n-gpu-layers`. Nilai yang didukung bergantung pada backend saat `llama-cpp-python` dipasang.

## 3. Gunakan dari Python

```python
from src.model import SahabatAIModel

model = SahabatAIModel("models/sahabatai.gguf", n_ctx=4096)
result = model.generate(
    "Apakah Indonesia berada di Asia?",
    "yes-no",
    system_prompt="Jawab hanya ya atau tidak.",
    max_tokens=8,
)
print(result)
```

## 4. Menambah grammar

Tambahkan file `.gbnf` ke folder `grammars/`. Setiap grammar wajib memiliki rule `root`:

```gbnf
root ::= "pilihan-a" | "pilihan-b"
```

Nama file otomatis muncul sebagai pilihan pada CLI. Grammar membatasi bentuk sintaksis, bukan menjamin kebenaran isi; system prompt tetap diperlukan agar respons relevan.

## 5. Jalankan tes

```bash
pytest -q
```

Tes tidak memuat model GGUF. Inferensi nyata memerlukan model lokal dan resource komputasi yang sesuai.
