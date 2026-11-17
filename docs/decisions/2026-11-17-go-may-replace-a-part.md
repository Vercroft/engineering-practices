# A product may move a part to Go

Date: 2026-11-17
Status: accepted
Amends: [2026-11-16, Go as a language choice](2026-11-16-go-as-a-language-choice.md)

## Context

The 2026-11-16 record said a product already in another language stays in it. A part of such a product (a service, a
worker, a tool) can still be the kind of program Go is built for (Go guide rule 1.1), and moving it can lower memory or
CPU use on the real server. Standard §3.6 already requires a measured baseline before any change made for speed or
memory.

## Decision

A product already in another language may move a part to Go when Go is the right tool for that part and a measurement
shows the gain (Go guide rule 1.2). Each move is a decision record (Go guide rule 1.4). Data work, scripts and ML stay
in Python, browser code is TypeScript, and code that needs no garbage collector or tight memory control is Rust. Code
that runs as root on a production host is still never Go (rule 1.3).

## Consequences

A move is justified by numbers from a measured baseline, recorded before and after, not by preference. A product with a
Go part follows the Go guide for that part and its own language's guide for the rest.
