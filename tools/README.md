# Neurobits CLI

Thin Python wrapper around Hugo for Neurobits content authoring.

## Installation

```bash
cd ..
mise install

cd tools
uv sync
```

If `mise` is not activated in your shell yet, prefix commands with
`mise exec --`.

## Configuration

Set the site path via environment variable:

```bash
export NEUROBITS_SITE_PATH="/path/to/neurobits/site"
```

Or create `~/.config/neurobits/config.toml`:

```toml
site_path = "~/code/neurobits/site"
```

## Commands

| Command | Description |
|---------|-------------|
| `neurobits new blog -t "Title"` | Create a new blog post |
| `neurobits new note -t "Title"` | Create a new note |
| `neurobits new project -t "Title"` | Create a new project page |
| `neurobits open <path>` | Open a content file in $EDITOR |
| `neurobits preview` | Start Hugo dev server |
| `neurobits build` | Build the site for production |
| `neurobits publish` | Validate and build (--push to actually push) |
| `neurobits doctor` | Check dependencies and config |

## Development

```bash
uv sync --extra dev
uv run pytest -v
```
