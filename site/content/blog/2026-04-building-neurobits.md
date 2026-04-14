---
title: "Building NeuroBits: A Fresh Start"
date: 2026-04-13
description: "Why I rebuilt my personal site from scratch, what I learned, and where it's going."
summary: "A look at the decisions behind rebuilding NeuroBits with Hugo, a cleaner design system, and a focus on notes and quick captures."
tags:
  - neurobits
  - meta
  - hugo
  - web
draft: false
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

I kept the neon/cyberpunk aesthetic from the old site, but consolidated it into a single CSS file with clear tokens:

```css
:root {
  --bg: #07111f;
  --cyan: #53f3ff;
  --magenta: #ff58d1;
  --green: #9eff6b;
  /* ... */
}
```

Everything references these tokens. No more hunting through multiple CSS files to figure out which shade of cyan I used where.

## Notes vs. blog

The biggest structural change: separating **notes** from **blog posts**.

Notes are quick captures. Links I found interesting, ideas I want to remember, things I'm learning. They don't need to be polished.

Blog posts are arguments. They take time to write and should be worth reading.

Having both means I actually publish things. Notes lower the bar for quick captures; the blog stays reserved for posts that deserve more attention.

## What's next

The core is done. What's left:

1. **Migration** — pulling in old content from the previous site
2. **CLI wrapper** — a thin Python tool to make creating content fast
3. **CI/CD** — GitHub Actions to build and deploy on push

The goal is a site I actually enjoy using. Fast to write, fast to read, and visually distinct enough to feel like *mine*.
