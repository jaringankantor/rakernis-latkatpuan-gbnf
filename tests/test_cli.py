import pytest

from src.main import build_parser


def test_cli_accepts_local_model_path() -> None:
    args = build_parser().parse_args(["--model-path", "model.gguf", "--prompt", "uji"])
    assert args.model_path == "model.gguf"
    assert args.model_token is False


def test_cli_accepts_grok_token() -> None:
    args = build_parser().parse_args(["--model-token", "--prompt", "uji"])
    assert args.model_token is True
    assert args.grok_model == "grok-4.5"


def test_cli_rejects_two_model_sources() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(
            [
                "--model-path",
                "model.gguf",
                "--model-token",
                "--prompt",
                "uji",
            ]
        )
