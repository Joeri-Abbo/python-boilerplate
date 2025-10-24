from __future__ import annotations

from pathlib import Path

import pytest

from config import DEFAULT_CONFIG, initialise_sentry, load_config


def test_load_config_falls_back_to_defaults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    monkeypatch.delenv("SENTRY_RATE", raising=False)

    missing = tmp_path / "missing.yml"
    config = load_config(missing)

    assert config["sentry"]["dsn"] == ""
    assert config["sentry"]["rate"] == DEFAULT_CONFIG["sentry"]["rate"]


def test_load_config_reads_file_and_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("sentry:\n  dsn: file-dsn\n  rate: 0.1\n", encoding="utf-8")

    monkeypatch.setenv("SENTRY_DSN", "env-dsn")
    monkeypatch.setenv("SENTRY_RATE", "0.5")

    config = load_config(config_file)
    assert config["sentry"]["dsn"] == "env-dsn"
    assert config["sentry"]["rate"] == pytest.approx(0.5)


def test_initialise_sentry_no_dsn_does_not_initialise(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def fake_init(*args, **kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr("config.sentry_sdk.init", fake_init)

    initialise_sentry({"sentry": {"dsn": "", "rate": 0.1}})
    assert called is False


def test_initialise_sentry_with_dsn(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}

    def fake_init(dsn: str, traces_sample_rate: float) -> None:
        captured["dsn"] = dsn
        captured["rate"] = traces_sample_rate

    monkeypatch.setattr("config.sentry_sdk.init", fake_init)

    initialise_sentry({"sentry": {"dsn": "dsn-value", "rate": 0.7}})
    assert captured == {"dsn": "dsn-value", "rate": 0.7}
