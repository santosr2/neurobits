# Neurobits

[![CI](https://github.com/santosr2/neurobits/actions/workflows/ci.yml/badge.svg)](https://github.com/santosr2/neurobits/actions/workflows/ci.yml)
![Hugo](https://img.shields.io/badge/Hugo-0.160+-ff4088?logo=hugo)
![Python](https://img.shields.io/badge/Python-3.12+-3776ab?logo=python&logoColor=white)

Personal site built with Hugo and a thin Python CLI for content authoring.

## Setup

```bash
mise install                 # Install Hugo and uv
cd tools && uv sync          # Install CLI
```

## Usage

```bash
neurobits new post -t "Title"              # Create a note
neurobits new post -t "Title" --type blog  # Create a blog post
neurobits preview                          # Start dev server
neurobits build                            # Production build
```

## Development

```bash
pre-commit install           # Install hooks
cd tools && uv run pytest    # Run tests
```
