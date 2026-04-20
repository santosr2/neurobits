---
title: "Sift"
date: 2025-12-05
summary: "A unified log querying and correlation engine for the command line."
description: "Query logs across multiple sources with a single syntax. Correlates events, filters noise, and outputs structured data."
status: "active"
tags:
  - cli
  - logging
  - observability
github: "https://github.com/santosr2/sift"
stack:
  - Perl
weight: 3
draft: false
---

Sift is a command-line tool for querying and correlating logs across multiple sources.

## What it does

- Query logs from files, stdin, or remote sources with unified syntax
- Correlate events across different log formats
- Filter noise with pattern matching and time windows
- Output structured JSON for downstream processing

```bash
# Find errors in the last hour
sift --since 1h 'level:error' /var/log/*.log

# Correlate requests across services
sift --correlate request_id app.log nginx.log
```

Built in Perl for portability and text processing speed.
