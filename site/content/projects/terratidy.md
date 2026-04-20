---
title: "TerraTidy"
date: 2025-12-16
summary: "A comprehensive quality platform for Terraform and Terragrunt."
description: "Unified formatting, linting, and policy enforcement for infrastructure code. Bundles tflint, OPA policies, and style checks into one tool."
status: "active"
tags:
  - terraform
  - terragrunt
  - linting
github: "https://github.com/santosr2/TerraTidy"
stack:
  - Go
  - Terraform
  - OPA
weight: 1
draft: false
---

TerraTidy is a quality platform that unifies formatting, linting, and policy enforcement for Terraform and Terragrunt codebases, with a plus on style enforcement for kind of "convention as code".

## What it does

- **Formatting** — Consistent HCL formatting across your entire codebase
- **Linting** — Integrates tflint with custom rulesets
- **Policy** — OPA policy bundles for security and compliance checks
- **Style** — Enforces naming conventions and structural patterns

## Why one tool?

Running `terraform fmt`, `tflint`, and `conftest` separately is tedious and error-prone. Even when using orchestration tools such as `pre-commit`, still you need specify all of them. TerraTidy combines them with sensible defaults and a single configuration file.

```bash
# Check everything
terratidy check ./modules/

# Auto-fix what can be fixed
terratidy fix ./modules/
```

See the [documentation](https://santosr2.github.io/TerraTidy/) for configuration options.
