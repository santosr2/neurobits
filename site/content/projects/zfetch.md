---
title: "zfetch"
date: 2025-04-25
summary: "Neofetch-like system info tool written in Zig."
description: "Fast, minimal system information display. Built in Zig for low overhead and easy cross-compilation."
status: "stable"
tags:
  - cli
  - zig
  - tools
github: "https://github.com/santosr2/zfetch"
stack:
  - Zig
weight: 6
draft: false
---

zfetch displays system information in your terminal, similar to neofetch but written in Zig.

## Why Zig?

- **Fast compilation** — Builds in seconds
- **No dependencies** — Single static binary
- **Cross-compile** — Target any platform from any platform
- **Small binary** — Under 1MB

```bash
$ zfetch
        .:''
    __ :'__   zfetch
 .'`__`-'__``.
:__________.-'
:_________:
 :_________`-;
  `.__.-.__.'

user@hostname
-------------
OS: macOS
Version: 14.0
Kernel: 23.0.0
Uptime: 2 days, 5 hours, 30 mins
Packages: 150 (brew)
Shell: zsh
Terminal: iTerm2
DE: Aqua
WM: Quartz Compositor
CPU: Apple M2 Pro (12 cores)
Memory: 8192 MiB / 16384 MiB (50.0%)
Disk (/): 250 GiB / 500 GiB (50.0%)
Local IP: 192.168.1.100
Locale: en_US.UTF-8

███████████████████████████
```

Displays OS, kernel, shell, terminal, CPU, memory, and uptime.
