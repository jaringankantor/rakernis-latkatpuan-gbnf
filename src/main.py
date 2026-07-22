"""CLI untuk structured generation SahabatAI."""

import argparse
from pathlib import Path

from .grammar_loader import available_grammars
from .model import GrokAPIModel, SahabatAIModel


PROJECT_DIR = Path(__file__).resolve().parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Jalankan SahabatAI dengan constraint grammar GBNF."
    )
    model_source = parser.add_mutually_exclusive_group(required=True)
    model_source.add_argument("--model-path", help="Lokasi model GGUF lokal")
    model_source.add_argument(
        "--model-token",
        action="store_true",
        help="Gunakan Grok dengan XAI_API_KEY dari file .env",
    )
    parser.add_argument(
        "--grok-model",
        default="grok-4.5",
        help="Model Grok saat --model-token digunakan (default: grok-4.5)",
    )
    parser.add_argument("--prompt", required=True, help="Instruksi untuk model")
    parser.add_argument(
        "--grammar", choices=available_grammars(), default="json", help="Grammar keluaran"
    )
    parser.add_argument("--system-prompt", help="File system prompt alternatif")
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--n-ctx", type=int, default=4096)
    parser.add_argument("--n-gpu-layers", type=int, default=0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    system_path = (
        Path(args.system_prompt)
        if args.system_prompt
        else PROJECT_DIR / "prompts" / "system-prompt.txt"
    )
    system_prompt = system_path.read_text(encoding="utf-8").strip()
    if args.model_token:
        model = GrokAPIModel.from_env(model=args.grok_model)
    else:
        model = SahabatAIModel(
            args.model_path, n_ctx=args.n_ctx, n_gpu_layers=args.n_gpu_layers
        )
    print(
        model.generate(
            args.prompt,
            args.grammar,
            system_prompt=system_prompt,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
    )


if __name__ == "__main__":
    main()
