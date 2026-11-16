# Go as a language choice

Date: 2026-11-16
Status: accepted

## Context

The standard had a page for Python, for TypeScript and JavaScript, and for Rust. Network services, HTTP APIs,
background workers and command-line tools are often best shipped as one static binary with low memory use and simple
concurrency, which is what Go is built for ([Go FAQ](https://go.dev/doc/faq),
[Organizing a Go module](https://go.dev/doc/modules/layout)). Without a page, a repository that picked Go would have no
rules for its layout, toolchain, lints, timeouts or supply chain, and the 7-day dependency age rule would not say how a
Go module is checked.

## Decision

We will allow Go as a choice, not a requirement, and follow [docs/go.md](../go.md), adopted by standard §3.2. Its rule 1
says where Go fits and where it does not: a product already in another language stays in it, data work and scripts stay
in Python, browser code is TypeScript, code that needs no garbage collector is Rust, and code that runs as root on a
production host is never Go. A Go service in an existing product is a maintainers' decision with its own record here.
Standard §7B.1, §7B.12 and §7B.13 name Go beside the other runtimes and package managers.

## Consequences

No repository has to move to Go. A repository that adopts it follows one golangci-lint configuration, builds `scratch`
images, pins one `toolchain` line and runs govulncheck. The go command has no release-age setting yet, so the
`dependency-age` workflow checks each new module version's `Time`, which is its commit time set by its author: it
guards against freshness, not malice. The `toolchain` line is not read by Dependabot, so it moves by hand. The
`golang` image is held at its major and minor, so a new Go release is a planned pull request.
