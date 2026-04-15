# Neurobits

Isolated replacement workspace for the Neurobits refactor.

- `site/` holds the new Hugo implementation.
- `tools/` is reserved for the thin Python authoring wrapper and migration utilities.
- Legacy root files stay reference-only while work moves forward here.

## Setup

Install the declared runtimes from the repo root:

```bash
mise install
```

If your shell has not been activated through `mise` yet, run commands with
`mise exec -- <command>` or enable the shell hook in your dotfiles.

Install the Python wrapper environment:

```bash
cd tools
uv sync --extra dev
```

## Local Guardrails

Install the repo hooks once:

```bash
pre-commit install
```

Run them across the repo before pushing larger changes:

```bash
pre-commit run --all-files
```

The hook set stays intentionally small:
- repo hygiene checks for whitespace, EOFs, YAML/TOML parsing, and merge markers
- `ruff` linting and formatting scoped to `tools/`

Run the wrapper test suite with:

```bash
cd tools
uv run pytest -v
```
