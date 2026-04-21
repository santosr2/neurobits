---
title: "Luma"
date: 2025-12-04
summary: "A language-agnostic, Lua-powered templating engine."
description: "Clean, directive-based templating that works anywhere. Lua core with bindings for Go, Python, Node.js, and WASM."
status: "in development"
tags:
  - templating
  - lua
  - polyglot
github: "https://github.com/santosr2/luma"
stack:
  - Lua
  - Go
  - Python
  - WASM
weight: 2
draft: false
---

Luma is a templating engine powered by Lua with a clean, directive-based syntax.

## Why Lua?

Lua is small, fast, and embeddable. Luma leverages this to provide consistent templating across languages without shipping a full runtime.

## Features

- **Language bindings** — Go, Python, Node.js, and WASM
- **Directive syntax** — Clean separators between logic and content
- **Composable** — Partials, inheritance, and macros
- **Safe** — Sandboxed execution with configurable limits

```lua
@for item in items
  - $item
@else
  No items found
@end
```

Works with YAML, JSON, HTML, Helm charts, and any text format.
