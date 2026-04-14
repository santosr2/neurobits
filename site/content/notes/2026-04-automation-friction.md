---
title: "Automation should reduce friction, not add it"
date: 2026-04-08
summary: "The goal of automation isn't to automate everything — it's to remove the parts that slow you down."
tags:
  - automation
  - workflow
  - tools
draft: false
---

I keep seeing automation that makes things worse.

Scripts that require 15 flags to run. "Helpful" wrappers that hide what's actually happening. CI pipelines that take longer to configure than the feature they're testing.

Good automation has a pattern:

1. **Understand the manual workflow first** — actually do the thing by hand
2. **Identify the friction** — what's slow, error-prone, or tedious?
3. **Automate just that part** — not the whole thing, just the friction

The best automation is invisible. You don't notice it because it just... works. The worst automation is the kind that makes you fight the tool more than the problem.

Related: [[2026-04-zig-comptime]] — Zig's comptime is good automation. It removes boilerplate without hiding what's happening.
