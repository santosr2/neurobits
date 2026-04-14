---
title: "Zig comptime is surprisingly useful"
date: 2026-04-10
summary: "Zig's compile-time evaluation lets you do things that would require code generation in other languages."
tags:
  - zig
  - programming
  - low-level
draft: false
---

Been playing with Zig's `comptime` feature. It's not just "compile-time constants" — it's actual code execution at compile time.

You can:

- Generate lookup tables at compile time
- Do type introspection and conditional compilation
- Build data structures based on compile-time inputs

```zig
fn fibonacci(comptime n: u32) u32 {
    if (n < 2) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Computed at compile time, no runtime cost
const fib_10 = fibonacci(10);
```

This sits somewhere between C macros (too primitive) and Rust proc macros (heavyweight). Zig just... runs your code at compile time.

The tradeoff: compile times go up if you abuse it. But for the right problems — parsers, protocol implementations, embedded tables — it's elegant.
