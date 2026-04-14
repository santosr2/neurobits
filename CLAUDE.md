# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Neurobits is a personal site built with Hugo and a thin Python CLI wrapper for content authoring. The repository has two main parts:

- **site/** - Hugo static site with a custom cyberpunk theme (no external theme dependency)
- **tools/** - Python CLI (`neurobits`) that wraps Hugo for content creation and site management

## Commands

### Hugo (run from `site/`)

```bash
hugo server --buildDrafts          # Dev server with drafts at localhost:1313
hugo --minify --cleanDestinationDir # Production build
```

Requires Hugo extended v0.160.0+ (check with `hugo version`).

### Python CLI (run from `tools/`)

```bash
pip install -e ".[dev]"            # Install with dev dependencies

neurobits new blog -t "Title"      # Create blog post, opens in $EDITOR
neurobits new note -t "Title"      # Create note
neurobits new project -t "Title"   # Create project page
neurobits preview                  # Start Hugo dev server
neurobits build                    # Production build
neurobits doctor                   # Check dependencies and config
```

Configure site path via `NEUROBITS_SITE_PATH` env var or `~/.config/neurobits/config.toml`.

### Tests

```bash
cd tools && pytest                 # Run all tests
cd tools && pytest tests/test_cli.py::test_doctor_all_ok  # Single test
```

## Architecture

### Hugo Site (`site/`)

Content types and their URL patterns:
- `content/blog/*.md` → `/blog/:year/:month/:slug/`
- `content/notes/*.md` → `/notes/:slug/`
- `content/projects/*.md` → `/projects/:slug/`
- `content/pages/*.md` → `/:slug/`

Layout structure:
- `layouts/_default/baseof.html` - Base template with head, body wrapper
- `layouts/partials/` - Header, footer, meta tags
- `layouts/{blog,notes,projects}/` - Section-specific list and single templates
- `archetypes/` - Templates for `hugo new` (blog.md, notes.md, projects.md)

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

Blog posts use date-prefixed filenames (`2026-04-title.md`). Standard frontmatter:

```yaml
title: "Post Title"
date: 2026-04-13
draft: true
tags: ["tag1", "tag2"]
description: "Optional summary"
```
