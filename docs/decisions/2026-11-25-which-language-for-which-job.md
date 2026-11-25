# Which language for which job

Date: 2026-11-25
Status: accepted

## Context

The standard had a page per language but said when to use only one of them: the Go guide's rule 1 said where Go fits,
and in passing where Python, TypeScript and Rust do. Nothing said when to use Rust, Python or TypeScript on their own
terms, or when shell is enough. A reader choosing a language for a new job had to piece it together from the Go guide,
and the same fact sat in two places when it moved.

## Decision

We will keep one rule for which language does which job, in standard §3.2, with a source for each line: Python for
scripts, git hooks, data work, ML and standard-library tools run by a system's `python3`; Go for network services,
background workers and command-line tools shipped as one binary; Rust for code without a garbage collector or with tight
memory control, and for performance-critical or embedded code; TypeScript for browser code; shell for short glue, and
Python once it passes about 100 lines or has real logic. The Go guide's rule 1 links to it instead of restating it, and
keeps its own rules for moving a part to Go and for code that runs as root on a production host.

It lives in §3.2, not on a new page, because §3.2 already names every language's page, so the choice and the page it
leads to are read together, and a new page would add one more place to keep true (§11.8, one fact in one place).

## Consequences

A new job's language is looked up in one place. The list moves no existing code: a product keeps its language, and a
part moves to Go only as the Go guide's rule 1.2 says. Each line rests on its language's own description or a
published style guide, not on a measurement of ours; ML has no quote of its own (the Python line's sources name its
operating system interfaces and scientific and numeric computing).
