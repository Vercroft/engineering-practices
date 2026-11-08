# Text is CC BY 4.0 and configuration is MIT

Date: 2026-11-06
Status: accepted

## Context

This repository is meant to be adopted and adapted. Standard §7F.2 allows three licences for code; none of them is made
for prose. The repository holds prose (the rules and guides) and the workflows and configuration that check it.

## Decision

We will license the text under CC BY 4.0, so anyone may copy and adapt it with credit, and the workflows and
configuration files under MIT. Code samples and configuration blocks inside the documents are MIT, following the
common practice of documentation under CC BY with code samples under a software licence. The root `LICENSE` holds the
CC BY 4.0 text. A `REUSE.toml` declares the licence of every file, and `reuse lint` checks it. The texts in
`LICENSES/` stay verbatim.

## Consequences

Adopters may copy rules into their own repositories with credit. A new file type needs a line in `REUSE.toml`, or
`reuse lint` fails.
