---
title: "Building NeuroBits: A Fresh Start"
date: 2026-04-20
description: "Why I rebuilt my personal site from scratch, what I learned, and where it's going."
summary: "A look at the decisions behind rebuilding NeuroBits with Hugo, a refined design system, and a unified content model."
tags:
  - neurobits
  - meta
  - hugo
  - web
draft: false
postType: blog
---

Every few years, I rebuild my personal site. Not because the old one broke, but because my thinking changed.

This time, I wanted something that fits how I actually work: quick captures, dense notes, and occasional longer posts. No complicated CMS, no framework overhead, just static files and a clean workflow.

## Why Hugo

I've used Hugo before, and it does exactly what I need:

- **Fast builds** — rebuilds in milliseconds, even with hundreds of pages
- **Flexible content model** — sections, taxonomies, and custom outputs without fighting the framework
- **Static output** — deploys anywhere, no server to maintain

```bash
# The whole build is this simple
hugo --minify
```

The alternatives (Next.js, Astro, etc.) are great for apps, but overkill for a personal site. I want to focus on content, not build pipelines.

## The design system

I moved away from heavy cyberpunk effects (perspective grids, noise textures, glitch animations) toward a refined, content-first aesthetic. Light mode by default with a dark mode toggle. A single accent color (pink) instead of competing neons.

```css
:root {
  /* Light Mode (default) */
  --bg: #F5F5F7;
  --text: #1A1A1D;
  --accent: #C91F6B;
  /* ... */
}

[data-theme="dark"] {
  --bg: #0C0C10;
  --text: #FAFAFA;
  --accent: #F472B6;
}
```

Everything references these tokens. The CSS went from 1700 lines to under 400. No more hunting through multiple files to figure out which shade I used where.

## Unified posts

Instead of separate sections for notes and blog posts, everything lives under `/posts/`. A `postType` field in frontmatter distinguishes them:

- **Notes** — quick captures, ideas, things I'm learning
- **Blog posts** — longer arguments that deserve more polish

Same URL structure, same templates, different intent. The unified model keeps things simple while preserving the conceptual distinction.

## The CLI

A thin Python wrapper (`neurobits`) handles content creation:

```bash
neurobits new post -t "Title"              # Creates a note
neurobits new post -t "Title" --type blog  # Creates a blog post
neurobits preview                          # Starts Hugo dev server
```

It's just Hugo underneath, but the CLI adds sensible defaults and date-prefixed filenames.

## What's next

1. **Migration** — pulling in old content from the previous site
2. **CI/CD** — GitHub Actions to build and deploy on push

The goal is a site I actually enjoy using. Fast to write, fast to read, and visually distinct enough to feel like *mine*.
