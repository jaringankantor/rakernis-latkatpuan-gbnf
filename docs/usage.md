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

### Menggunakan Grok API

Gunakan `--model-token` sebagai pengganti `--model-path` untuk mengirim permintaan
ke Grok melalui xAI API:

```bash
cp .env.example .env
# Edit .env dan isi XAI_API_KEY.
python -m src.main \
  --model-token \
  --grok-model grok-4.5 \
  --grammar analisis-log \
  --prompt "Analisis log berikut: ..."
```

Model bawaan untuk mode API adalah `grok-4.5` dan dapat diganti melalui
`--grok-model`. Jangan menyimpan token di source code, file konfigurasi yang
dilacak Git, atau riwayat terminal. Grammar JSON khusus dikirim sebagai JSON
Schema strict; grammar `json` menggunakan JSON object, sedangkan `yes-no`
divalidasi setelah respons diterima.

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

## 4. Jalankan skrip contoh

Skrip pada direktori `examples/` dapat dijalankan langsung dari root proyek.

Menghasilkan JSON terstruktur:

```bash
python examples/simple_json.py --model-path models/sahabatai.gguf
```

Menghasilkan jawaban `ya` atau `tidak`:

```bash
python examples/yes_no.py --model-path models/sahabatai.gguf
```

Menghasilkan profil pengguna dengan field `nama`, `usia`, `kota`, dan `minat`:

```bash
python examples/user_profile.py --model-path models/sahabatai.gguf
```

Menghasilkan laporan masyarakat untuk kepolisian:

```bash
python examples/laporan_kepolisian.py --model-path models/sahabatai.gguf
```

Grammar `laporan-kepolisian` menghasilkan JSON berisi identitas dan kontak pelapor,
jenis laporan, waktu dan lokasi kejadian, uraian, terlapor, saksi, barang bukti,
serta penanda `tindakan_segera`. Gunakan string atau array kosong untuk informasi
yang tidak diberikan dan jangan menambahkan informasi hasil asumsi.

Menganalisis log perangkat jaringan atau server:

```bash
python examples/analisis_log.py --model-path models/sahabatai.gguf
```

Grammar `analisis-log` menghasilkan diagnosis terstruktur berisi sumber dan jenis
perangkat, waktu kejadian, tingkat keparahan, status, masalah yang terdeteksi,
bukti log, dampak, keputusan perlu tidaknya tindak lanjut, urgensi, rekomendasi,
dan informasi tambahan yang masih dibutuhkan. Nilai `urgensi` membedakan kondisi
yang tidak perlu ditindaklanjuti, dapat dijadwalkan, atau harus segera ditangani.
Grammar menjamin bentuk keluaran, sedangkan keputusan operasional tetap perlu
divalidasi oleh petugas yang berwenang.

Sesuaikan nilai `--model-path` dengan lokasi file model GGUF Anda.
Semua skrip di direktori `examples/` juga dapat dijalankan dengan
flag `--model-token` sebagai pengganti `--model-path`. Token dibaca dari
`XAI_API_KEY` di file `.env`. Tambahkan
`--grok-model NAMA_MODEL` jika ingin menggunakan model selain bawaan.

## 5. Menambah grammar

Tambahkan file `.gbnf` ke folder `grammars/`. Setiap grammar wajib memiliki rule `root`:

```gbnf
root ::= "pilihan-a" | "pilihan-b"
```

Nama file otomatis muncul sebagai pilihan pada CLI. Grammar membatasi bentuk sintaksis, bukan menjamin kebenaran isi; system prompt tetap diperlukan agar respons relevan.

## 6. Jalankan tes

```bash
pytest -q
```

Tes tidak memuat model GGUF. Inferensi nyata memerlukan model lokal dan resource komputasi yang sesuai.
