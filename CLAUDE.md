# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Neurobits is a personal site built with Hugo and a thin Python CLI wrapper for content authoring. The repository has two main parts:

- **site/** - Hugo static site with a custom cyberpunk theme (no external theme dependency)
- **tools/** - Python CLI (`neurobits`) that wraps Hugo for content creation and site management

## Commands

### Runtime setup (run from repo root)

```bash
mise install                         # Install hugo and uv from mise.toml
```

If the shell is not activated through `mise`, prefix runtime commands with
`mise exec --`.

### Hugo (run from `site/`)

```bash
hugo server --buildDrafts          # Dev server with drafts at localhost:1313
hugo --minify --cleanDestinationDir # Production build
```

Requires Hugo extended v0.160.0+ (check with `hugo version`).

### Python CLI (run from `tools/`)

```bash
uv sync --extra dev                # Install project + dev dependencies

uv run neurobits new post -t "Title"              # Create note (default)
uv run neurobits new post -t "Title" --type blog  # Create blog post
uv run neurobits new project -t "Title"           # Create project page
uv run neurobits preview                          # Start Hugo dev server
uv run neurobits build                            # Production build
uv run neurobits doctor                           # Check dependencies and config

```

Configure site path via `NEUROBITS_SITE_PATH` env var or `~/.config/neurobits/config.toml`.

### Tests

```bash
cd tools && uv run pytest -v       # Run all tests
cd tools && uv run pytest tests/test_cli.py::test_doctor_all_ok  # Single test
```

## Architecture

### Hugo Site (`site/`)

Content types and their URL patterns:

- `content/posts/*.md` → `/posts/:slug/` (unified blog + notes, uses `postType` frontmatter)
- `content/projects/*.md` → `/projects/:slug/`
- `content/pages/*.md` → `/:slug/`

Layout structure:

- `layouts/_default/baseof.html` - Base template with head, body wrapper
- `layouts/partials/` - Header, footer, meta tags
- `layouts/{posts,projects}/` - Section-specific list and single templates
- `archetypes/` - Templates for `hugo new` (posts.md, projects.md)

Asset pipeline:

- `assets/css/main.css` - All styles, uses CSS custom properties for theming
- `assets/js/main.js` - Minimal JS (nav toggle, keyboard detection)
- Assets are fingerprinted and minified by Hugo

### Python CLI (`tools/`)

```
tools/
├── src/neurobits/
│   ├── cli.py      # Click command group: new, open, preview, build, publish, doctor
│   └── config.py   # Config loading (env vars, TOML file)
└── tests/          # pytest tests using Click's CliRunner
```

The CLI is a thin wrapper; it delegates to Hugo for actual site operations.

## Content Frontmatter

Posts use date-prefixed filenames (`2026-04-title.md`). Standard frontmatter:

```yaml
title: "Post Title"
date: 2026-04-13
draft: true
postType: note  # or "blog"
tags: ["tag1", "tag2"]
description: "Optional summary"
highlight: false  # true shows star on list pages
```
