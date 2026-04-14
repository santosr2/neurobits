---
title: "NeuroBits CLI"
date: 2026-04-01
summary: "A thin Python wrapper around Hugo for fast content authoring from anywhere."
description: "Command-line tool for creating and managing NeuroBits content. Wraps Hugo with sensible defaults and editor integration."
status: "in development"
tags:
  - cli
  - python
  - tooling
  - neurobits
github: "https://github.com/santosr2/neurobits"
stack:
  - Python
  - Hugo
  - Click
draft: false
---

The NeuroBits CLI is a thin wrapper around Hugo that makes creating content fast and predictable.

## Why a wrapper?

Hugo is great at building sites, but creating content requires remembering paths, archetypes, and front matter fields. The CLI handles the boilerplate:

```bash
# Create a new blog post
neurobits new blog --title "My New Post"

# Create a quick note
neurobits new note --title "Something I learned"

# Preview the site
neurobits preview
```

## Design principles

1. **Thin wrapper** — delegates to Hugo for anything Hugo does well
2. **Work from anywhere** — resolves the site path from config, not `pwd`
3. **Editor integration** — opens files in your preferred editor after creation
4. **Fail loudly** — clear errors when dependencies are missing

## Commands

| Command | Description |
|---------|-------------|
| `new blog` | Create a new blog post |
| `new note` | Create a new note |
| `new project` | Create a new project page |
| `preview` | Start Hugo dev server |
| `build` | Build the site |
| `publish` | Validate and optionally push changes |
| `doctor` | Check dependencies and config |

## Configuration

The CLI reads config from environment variables and `~/.config/neurobits/config.toml`:

```toml
[neurobits]
site_path = "~/code/neurobits/site"
editor = "nvim"
```

Site path can also be set via `NEUROBITS_SITE_PATH` for scripting.
