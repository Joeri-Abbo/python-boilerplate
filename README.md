# python-boilerplate

Minimal scaffolding for Python CLI utilities with Sentry integration and testing helpers.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

Copy `config.example.yml` to `config.yml` to override defaults or set `SENTRY_DSN` / `SENTRY_RATE` in the environment.

## Quality checks

```bash
. .venv/bin/activate
ruff check .
pytest
```

GitHub Actions runs the same checks on every push and pull request.
