#!/usr/bin/env python3

from __future__ import annotations

from config import initialise_sentry, load_config


def main() -> None:
    config = load_config()
    initialise_sentry(config)
    print("Hello world")


if __name__ == "__main__":
    main()
