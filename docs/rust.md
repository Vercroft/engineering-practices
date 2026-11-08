# Rust standard

The Rust rules for every repository that adopts them, adopted by standard §3.2. This page sets the shape before the first crate (written 2026-10-21). Short rules, each with its source; where a tool does
not enforce a rule, it says so (standard §4.3).

## Sources (read 2026-10-21)

Primary:

- [WS] [Cargo: workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html),
  [manifest `[lints]`](https://doc.rust-lang.org/cargo/reference/manifest.html),
  [resolver](https://doc.rust-lang.org/cargo/reference/resolver.html),
  [`rust-version`](https://doc.rust-lang.org/cargo/reference/rust-version.html)
- [CI] [Cargo: continuous integration](https://doc.rust-lang.org/cargo/guide/continuous-integration.html),
  [FAQ: Cargo.lock in version control](https://doc.rust-lang.org/cargo/faq.html),
  [`--locked`](https://doc.rust-lang.org/cargo/commands/cargo-build.html),
  [unstable `min-publish-age`](https://doc.rust-lang.org/cargo/reference/unstable.html)
- [TC] [rustup: overrides and `rust-toolchain.toml`](https://rust-lang.github.io/rustup/overrides.html);
  [Rust releases](https://blog.rust-lang.org/releases/): 1.99.0 on 2026-10-01, 1.99.1 on 2026-10-15
- [CLIP] [Clippy lint groups](https://doc.rust-lang.org/stable/clippy/lints.html) and
  [lint list](https://clippy.rust-lang.org/master/index.html) (`allow_attributes`, `allow_attributes_without_reason`)
- [REF] [Rust reference: lint attributes](https://doc.rust-lang.org/reference/attributes/diagnostics.html) (`expect`,
  `reason`, `forbid`)
- [DENY] [cargo-deny checks](https://embarkstudios.github.io/cargo-deny/checks/index.html)
- [NT] [cargo-nextest](https://nexte.st/) and [slow tests and timeouts](https://nexte.st/docs/features/slow-tests/)
- [DBT] [Dependabot options](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference)
  (cooldown supports Cargo and the Rust toolchain)

Practitioner evidence:

- [BL] [blessed.rs crate list](https://blessed.rs/crates)
- [CIO] crates.io downloads, last 90 days, read 2026-10-21 from its API: thiserror 444M, log 336M, tokio 267M, anyhow
  251M, tracing 230M, eyre 24M, snafu 23M, async-std 12M
- [CJ] coreyja, [clippy::pedantic and workspace lints](https://coreyja.com/til/clippy-pedantic-workspace)

Null results: Cargo has no stable release-age setting (`min-publish-age` is nightly only); libtest has no stable
per-test timeout that was found, which is why nextest is used (rule 7).

## Rules

### 1. Layout

```text
<repo>/
  Cargo.toml              # [workspace]: members, shared package keys, dependencies, lints
  Cargo.lock
  rust-toolchain.toml
  clippy.toml  deny.toml  .config/nextest.toml
  crates/
    <product>-<component>/   # a library crate: src/lib.rs, tests/ for integration tests
    <product>-cli/           # a binary crate: src/main.rs
```

One workspace per repository: its crates "share a common `Cargo.lock`" and output directory [WS]. Each crate inherits
`edition`, `rust-version`, `license` and dependency versions from `[workspace.package]` and `[workspace.dependencies]`,
and lints with `[lints] workspace = true` [WS]. A virtual workspace sets `resolver = "3"` itself, since it has "no
`package.edition` to infer it from" [WS]. Crate names follow standard §3.5. Unit tests sit in the module under
`#[cfg(test)]`; integration tests in the crate's `tests/`.

### 2. Toolchain and MSRV

1. `rust-toolchain.toml` pins an exact stable release at least 7 days old (standard §7B.1), with `clippy` and
   `rustfmt` and the `minimal` profile [TC]. On 2026-10-21 that is 1.99.0; 1.99.1 is adoptable from 2026-10-22.
2. Edition 2024. `rust-version` equals the pinned release's minor version, so CI on the pin proves the MSRV, and
   resolver 3 (the edition 2024 default) prefers dependencies that support it [WS].
3. A published library may keep a lower MSRV; CI then also runs
   `cargo hack check --rust-version --workspace --all-targets --ignore-private`, as the Cargo guide shows [CI].

### 3. Lints

1. **Formatting and lints in CI, warnings as errors:** `cargo fmt --check`, and Clippy with `-D warnings` on every
   target.
2. **Lint levels live in `[workspace.lints]`** [WS], not in code:
   - Clippy's default groups stay as they are: `correctness` denies; `suspicious`, `complexity`, `perf` and `style`
     warn [CLIP], which `-D warnings` makes errors.
   - `pedantic` warns, at `priority = -1` so single lints can override it [WS]. Practitioners keep it on and allow a
     few noisy lints by name [CJ]; each such `allow` in `[workspace.lints.clippy]` gets a comment saying why.
   - Not `nursery` or `restriction` as groups: Clippy says "It is **not** recommended to enable the whole group" for
     both [CLIP]. Cherry-picked restriction lints instead: `allow_attributes`, `allow_attributes_without_reason`,
     `dbg_macro`, `todo`, `unimplemented`, `unwrap_used` (deny), `print_stdout`, `print_stderr` (warn).
   - Not `cargo`: it checks publishing metadata; a published crate adds it.
3. **`unsafe_code = "forbid"`**: `forbid` "also forbids changing the lint level afterwards" [REF], so no attribute can
   switch it back (verified: `#[expect(unsafe_code)]` fails with E0453). A crate that needs `unsafe` is a maintainers'
   decision, recorded in that crate's manifest with the reason.

### 4. Suppressions

The shared policy is [suppressions.md](suppressions.md): one rule, a reason, a stale check, and a line in
`.suppressions` that a maintainer approves. In Rust:

1. **Only `#[expect(one_lint, reason = "...")]`**, one lint per attribute. `expect` turns into a warning, and so an
   error in CI, when the lint no longer fires (`unfulfilled_lint_expectations` [REF]), so a stale suppression cannot
   linger.
2. `allow_attributes` refuses `#[allow]` and `allow_attributes_without_reason` refuses an attribute with no reason
   [CLIP]. Clippy's `allow_attributes` "only warns outer attributes (`#[allow]`)" and ignores `#[allow]` inside macros
   [CLIP]; the check script refuses inner `#![allow]` and `#![expect]` (crate or module wide), `cfg_attr` forms and
   several lints in one attribute.
3. Config exceptions (`[workspace.lints]`, `clippy.toml`, for example `allow-unwrap-in-tests`) only for whole
   categories of code, each with a comment.

### 5. Supply chain

1. `Cargo.lock` is committed: it gives "deterministic builds at different times and on different systems" [CI].
2. Every cargo command in CI runs with `--locked`, which fails if "the lock file is missing" or would change [CI].
3. `cargo deny check` runs all four checks: advisories (vulnerable, unmaintained, yanked), licences, bans (named crates
   and duplicates) and sources (crates.io only) [DENY].
4. Cooldown through Dependabot (`cargo` and `rust-toolchain` ecosystems, `default-days: 7` [DBT]; template in
   [dependabot.md](dependabot.md)). Its cooldown covers only the crate it updates, and Cargo has no stable release-age
   check, so transitive crates are covered by the cooldown alone (standard §7B.13; until a repository adopts the
   `dependency-age` workflow the author checks by hand, dependabot.md rule 4). Adopt Cargo's `min-publish-age` once it is
   stable [CI].
5. CI installs `cargo-deny`, `cargo-nextest` and `cargo-hack` as exact versions: release binaries checked against
   their published SHA-256, or `cargo install --locked <tool>@<version>`.

### 6. Crates

Chosen on evidence [BL], [CIO]; each is still a dependency decision (standard §3.4):

| Need | Crate | Evidence |
|---|---|---|
| Library error types | `thiserror` | [BL]: "for libraries"; most downloaded of the error crates [CIO] |
| Application errors | `anyhow` | [BL]: "for applications" |
| Logging | `tracing` (+ `tracing-subscriber` in binaries) | [BL]: "now the go-to crate for logging"; `log` only for simple synchronous code |
| Async runtime | `tokio`, only when the code is async | [BL]: "Recommended for new projects"; async-std's downloads are under a twentieth of tokio's [CIO] |

### 7. Tests

`cargo-nextest` runs the tests, because standard §4.4 needs a time limit on every test: nextest's `slow-timeout` with
`terminate-after` kills a test and reports it failed [NT] (verified: a hanging test ended as `TIMEOUT`). It also runs
each test in its own process and claims "Up to 3x" the speed of `cargo test` [NT]. Doctests are "not supported" by
nextest [NT], so CI also runs `cargo test --doc`.

## Configuration

`Cargo.toml` (workspace root; add `[workspace.dependencies]`):

```toml
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.package]
edition = "2024"
rust-version = "1.99"
publish = false

[workspace.lints.rust]
unsafe_code = "forbid"

[workspace.lints.clippy]
pedantic = { level = "warn", priority = -1 }
allow_attributes = "deny"
allow_attributes_without_reason = "deny"
dbg_macro = "deny"
todo = "deny"
unimplemented = "deny"
unwrap_used = "deny"
print_stdout = "warn"
print_stderr = "warn"
```

Each crate's `Cargo.toml` inherits with `edition.workspace = true` (and the other keys) and `[lints] workspace = true`.

`rust-toolchain.toml`:

```toml
[toolchain]
channel = "1.99.0"
components = ["clippy", "rustfmt"]
profile = "minimal"
```

`clippy.toml`:

```toml
# Tests may unwrap: a panic is how a test fails.
allow-unwrap-in-tests = true
```

`.config/nextest.toml`:

```toml
[profile.default]
# Every test has a time limit: slow after 60 s, killed after 120 s.
slow-timeout = { period = "60s", terminate-after = 2 }
```

`deny.toml` (the licence list is what our dependencies need today; adding one is a reviewed change):

```toml
[graph]
all-features = true

[advisories]
# Every RustSec advisory (vulnerable, unmaintained, unsound, yanked) fails the check.
unmaintained = "all"
yanked = "deny"

[licenses]
allow = ["Apache-2.0", "MIT", "Unicode-3.0"]
confidence-threshold = 0.93

[licenses.private]
ignore = true

[bans]
multiple-versions = "warn"
wildcards = "deny"
allow-wildcard-paths = true

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
```

## CI

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo nextest run --workspace --all-features --locked
cargo test --doc --workspace --locked
cargo deny --locked check
sh scripts/check-suppressions.sh  # the script on suppressions.md
```

Verified 2026-10-21 on a sample workspace (a library and a binary, with thiserror and anyhow) using Rust 1.99.0,
cargo-deny 0.20.2 and cargo-nextest 0.9.148 (each checked against its published SHA-256), with every locked crate at
least 7 days old. Clean code passes. These fail: `#[allow]`, `#![allow]` without a reason, `#![allow]` with a reason
(the check script), `#[expect]` without a reason or with two lints, `#![expect]`, an unfulfilled `#[expect]`, an
`unsafe` block, `#[expect(unsafe_code)]`, `.unwrap()` outside tests, a formatting difference, a licence outside the
list, a test that hangs past its limit, and a `#[expect]` (rustfmt split over four lines) missing from
`.suppressions`; listed, it passes.

## Settled practice and where practitioners disagree

Settled: rustfmt and Clippy in CI; a committed lockfile for applications; `#[expect]` over `#[allow]` since it reports
stale suppressions [REF]; `thiserror` for libraries and `anyhow` for applications [BL].

Disputed, and what we chose:

- **`pedantic`.** Clippy describes it as making Clippy "even more _pedantic_" [CLIP]; practitioners who enable it
  allow some lints by name [CJ]. We enable it and record each allowed lint's reason.
- **Lockfile for libraries.** The Cargo FAQ leaves it "dependent on the needs of your package" [CI]. We commit it
  everywhere for deterministic CI, and a published library adds the Cargo guide's latest-dependencies job.
- **Error crates.** `snafu` and `eyre` have users [CIO]; `color-eyre` suits errors shown to end users [BL]. We default
  to `thiserror` and `anyhow`.
- **nextest.** Doctests still need `cargo test` [NT]; we accept two commands for the per-test time limit.
