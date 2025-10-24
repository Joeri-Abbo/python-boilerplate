from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import sentry_sdk
import yaml

DEFAULT_CONFIG: Dict[str, Any] = {"sentry": {"dsn": "", "rate": 0.0}}


def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Load the application configuration from YAML or environment defaults."""
    if config_path is None:
        candidate = Path(__file__).resolve().parent / "config.yml"
    else:
        candidate = Path(config_path).expanduser().resolve()

    merged: Dict[str, Any] = {
        "sentry": DEFAULT_CONFIG["sentry"].copy(),
    }

    if candidate.exists():
        with candidate.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle) or {}
        sentry_data = raw.get("sentry", {})
        merged["sentry"].update({k: v for k, v in sentry_data.items() if v is not None})

    env_dsn = os.getenv("SENTRY_DSN")
    if env_dsn:
        merged["sentry"]["dsn"] = env_dsn

    env_rate = os.getenv("SENTRY_RATE")
    if env_rate:
        try:
            merged["sentry"]["rate"] = float(env_rate)
        except ValueError:
            pass

    return merged


def initialise_sentry(config: Dict[str, Any]) -> None:
    """Initialise Sentry from the provided configuration if a DSN is set."""
    sentry_cfg = config.get("sentry", {})
    dsn = sentry_cfg.get("dsn") or ""
    if not dsn:
        return

    rate = sentry_cfg.get("rate", DEFAULT_CONFIG["sentry"]["rate"])
    sentry_sdk.init(dsn, traces_sample_rate=rate)
