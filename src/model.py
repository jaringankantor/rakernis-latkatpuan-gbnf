"""Wrapper tipis llama.cpp untuk inferensi yang dibatasi grammar."""

from pathlib import Path
from typing import Any

from .grammar_loader import load_grammar


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
