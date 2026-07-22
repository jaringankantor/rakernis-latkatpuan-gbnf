"""Wrapper model lokal dan Grok API untuk structured generation."""

import os
from pathlib import Path
from typing import Any

from .grammar_loader import load_grammar


PROJECT_DIR = Path(__file__).resolve().parent.parent


def load_xai_api_key(env_path: Path = PROJECT_DIR / ".env") -> str:
    """Ambil XAI_API_KEY dari environment atau file .env proyek."""
    token = os.environ.get("XAI_API_KEY", "").strip()
    if not token and env_path.is_file():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() == "XAI_API_KEY":
                token = value.strip().strip('"\'').strip()
                break
    if not token:
        raise RuntimeError(
            "XAI_API_KEY belum diisi. Salin .env.example menjadi .env lalu isi token xAI."
        )
    return token


JSON_SCHEMAS: dict[str, dict[str, Any]] = {
    "user-profile": {
        "type": "object",
        "properties": {
            "nama": {"type": "string"},
            "usia": {"type": "integer", "minimum": 0, "maximum": 150},
            "kota": {"type": "string"},
            "minat": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["nama", "usia", "kota", "minat"],
        "additionalProperties": False,
    },
    "laporan-kepolisian": {
        "type": "object",
        "properties": {
            "nama_pelapor": {"type": "string"},
            "kontak_pelapor": {"type": "string"},
            "jenis_laporan": {
                "type": "string",
                "enum": [
                    "kehilangan",
                    "pencurian",
                    "penipuan",
                    "kekerasan",
                    "gangguan_kamtibmas",
                    "lainnya",
                ],
            },
            "waktu_kejadian": {"type": "string"},
            "lokasi_kejadian": {"type": "string"},
            "uraian": {"type": "string"},
            "terlapor": {"type": "string"},
            "saksi": {"type": "array", "items": {"type": "string"}},
            "barang_bukti": {"type": "array", "items": {"type": "string"}},
            "tindakan_segera": {"type": "boolean"},
        },
        "required": [
            "nama_pelapor",
            "kontak_pelapor",
            "jenis_laporan",
            "waktu_kejadian",
            "lokasi_kejadian",
            "uraian",
            "terlapor",
            "saksi",
            "barang_bukti",
            "tindakan_segera",
        ],
        "additionalProperties": False,
    },
    "analisis-log": {
        "type": "object",
        "properties": {
            "sumber_log": {"type": "string"},
            "jenis_perangkat": {
                "type": "string",
                "enum": ["perangkat_jaringan", "server", "tidak_diketahui"],
            },
            "waktu_kejadian": {"type": "string"},
            "tingkat_keparahan": {
                "type": "string",
                "enum": ["info", "peringatan", "kritis"],
            },
            "status": {
                "type": "string",
                "enum": [
                    "normal",
                    "perlu_dipantau",
                    "perlu_tindak_lanjut",
                    "insiden_aktif",
                ],
            },
            "masalah_terdeteksi": {"type": "string"},
            "bukti_log": {"type": "array", "items": {"type": "string"}},
            "dampak": {"type": "string"},
            "perlu_tindak_lanjut": {"type": "boolean"},
            "urgensi": {
                "type": "string",
                "enum": ["tidak_perlu", "terjadwal", "segera"],
            },
            "rekomendasi": {"type": "array", "items": {"type": "string"}},
            "informasi_tambahan_dibutuhkan": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "sumber_log",
            "jenis_perangkat",
            "waktu_kejadian",
            "tingkat_keparahan",
            "status",
            "masalah_terdeteksi",
            "bukti_log",
            "dampak",
            "perlu_tindak_lanjut",
            "urgensi",
            "rekomendasi",
            "informasi_tambahan_dibutuhkan",
        ],
        "additionalProperties": False,
    },
}


class SahabatAIModel:
    """Model GGUF SahabatAI dengan structured generation berbasis GBNF."""

    def __init__(
        self,
        model_path: str | Path,
        *,
        n_ctx: int = 4096,
        n_gpu_layers: int = 0,
        verbose: bool = False,
        **model_options: Any,
    ) -> None:
        path = Path(model_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Model GGUF tidak ditemukan: {path}")

        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError(
                "llama-cpp-python belum terpasang. Jalankan: pip install -r requirements.txt"
            ) from exc

        self._llm = Llama(
            model_path=str(path),
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=verbose,
            **model_options,
        )

    def generate(
        self,
        prompt: str,
        grammar_name: str,
        *,
        system_prompt: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.1,
    ) -> str:
        """Hasilkan teks yang valid menurut grammar yang dipilih."""
        if not prompt.strip():
            raise ValueError("Prompt tidak boleh kosong.")

        from llama_cpp import LlamaGrammar

        grammar = LlamaGrammar.from_string(load_grammar(grammar_name))
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._llm.create_chat_completion(
            messages=messages,
            grammar=grammar,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        content = response["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise RuntimeError("Model tidak mengembalikan teks.")
        return content.strip()


class GrokAPIModel:
    """Klien Grok melalui endpoint xAI yang kompatibel dengan OpenAI."""

    def __init__(self, token: str, *, model: str = "grok-4.5") -> None:
        if not token.strip():
            raise ValueError("Token Grok tidak boleh kosong.")
        if not model.strip():
            raise ValueError("Nama model Grok tidak boleh kosong.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Paket openai belum terpasang. Jalankan: pip install -r requirements.txt"
            ) from exc

        self._client = OpenAI(api_key=token, base_url="https://api.x.ai/v1")
        self._model = model

    @classmethod
    def from_env(cls, *, model: str = "grok-4.5") -> "GrokAPIModel":
        """Buat klien menggunakan XAI_API_KEY dari environment atau file .env."""
        return cls(load_xai_api_key(), model=model)

    def generate(
        self,
        prompt: str,
        grammar_name: str,
        *,
        system_prompt: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.1,
    ) -> str:
        """Hasilkan teks melalui Grok dengan structured output jika tersedia."""
        if not prompt.strip():
            raise ValueError("Prompt tidak boleh kosong.")

        grammar = load_grammar(grammar_name)
        constraint = (
            "Ikuti bentuk keluaran grammar GBNF berikut secara ketat. "
            "Jangan tambahkan markdown atau penjelasan di luar hasil:\n" + grammar
        )
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "system", "content": constraint})
        messages.append({"role": "user", "content": prompt})

        request: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if grammar_name == "json":
            request["response_format"] = {"type": "json_object"}
        elif grammar_name in JSON_SCHEMAS:
            request["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": grammar_name.replace("-", "_"),
                    "schema": JSON_SCHEMAS[grammar_name],
                    "strict": True,
                },
            }

        response = self._client.chat.completions.create(**request)
        content = response.choices[0].message.content
        if not isinstance(content, str):
            raise RuntimeError("Grok API tidak mengembalikan teks.")
        result = content.strip()
        if grammar_name == "yes-no" and result not in {"ya", "tidak"}:
            raise RuntimeError("Grok API mengembalikan jawaban di luar grammar yes-no.")
        return result
