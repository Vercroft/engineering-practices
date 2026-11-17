# Changelog

All notable changes to this repository are listed here, newest first, in the format of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- CI badge in the README.
- FSL-1.1-MIT as a fourth code licence in §7F, for public products sold as a hosted service.
- Two principles in §1: only what is required (7), which never cuts required work, and surgical changes (8).
- §3.6, measure before optimizing: a speed or memory change records before and after numbers from a measured baseline.
- §3.7, production behaviour: timeouts, bounded retries with backoff, idempotent handling of repeated events, transactions, no swallowed failures.
- §3.8, application layout: code grouped by feature, thin entry modules, tests mirror the feature folders.
- A Go guide (docs/go.md), adopted by §3.2 as a choice, not a requirement: where Go fits, layout, toolchain pin,
  scratch images, errors and logging, timeouts, contracts, one golangci-lint config, supply chain; Go lines in §7B.1,
  §7B.12 and §7B.13, the Dependabot template and the suppression check script.
- §7C.7, no paid GitHub feature by accident: paid add-ons stay off, metered products have a budget that stops usage,
  paid features are checked before a transfer, and only the people GitHub lets manage billing change it.

### Changed

- §7C.6: until gitleaks' default rules catch GitHub's stateless installation tokens (`ghs_APPID_JWT`), every
  repository's `.gitleaks.toml` carries the rule `github-app-installation-token-stateless`, copied from this
  repository's `.gitleaks.toml`, which now has it.
- CI's `gitleaks` job runs the full-history scan from the organisation's shared workflow (pinned by commit SHA)
  instead of its own copy; the check is now `gitleaks / gitleaks`.
- The leak patterns allow GitHub's noreply address, which GitHub uses as the committer of merge and web-edit commits.
- The leak patterns allow links to five more reviewed public hosts: files.pythonhosted.org and pypi.org, which a
  uv lockfile names, and pythonspeed.com, www.b-list.org and x.com, which the rules cite.
- The leak patterns allow links to fastapi.tiangolo.com, which the application layout rule cites.
- The leak patterns allow links to go.dev, pkg.go.dev, golangci-lint.run, docs.sqlc.dev, openapi-ts.dev and osv.dev,
  which the Go guide cites.
- The Python guide adopts a new feature release from its first bugfix release, once that is 7 days old (rule 4.1).
- §2.5: state assumptions before building, and ask first when a request can be read two ways.
- §6.14: keep each pull request reviewable, one piece of work or one batch of related changes; about 100 changed lines is a good size and 1000 usually too large.
- §2.5: a report keeps apart what was verified, what is inferred and what is assumed.
- §7C.1, §7C.2, §7B.10 and §7B.11: secret scanning, private vulnerability reporting, artifact attestations and attested
  SBOMs are for public repositories only; a transfer with secret scanning on is billed for the month.
- §7C.6: gitleaks scans the staged changes at commit time and the full history on every pull request, from one shared
  reusable workflow; each repository adds rules for its own secret formats. Look at Betterleaks again when its v2 is
  stable.
- The Go guide lets a product already in another language move a part to Go when Go is the right tool and a
  measurement shows the gain; each move is a decision record (rule 1.2).
- §0.8, §6.11 and §7F.2 state their reasons in full: why identifiers stay out of product repositories, the
  throwaway-repository guard for tests that run git, and why PolyForm Strict and not Noncommercial.
- The Python guide shows a feature layout; mirrored test folders get an empty `__init__.py` so mypy strict accepts
  same-named test files (rule 1.6).

## [0.1.0] - 2026-11-08

### Added

- The numbered rules in `STANDARD.md` and the guides for Python, TypeScript and JavaScript, Rust, Dependabot,
  suppressions and documentation.
- CI, link, CodeQL and Scorecard workflows, the Dependabot file, the leak patterns and the commit-time hook.
- CC BY 4.0 for the text and MIT for the workflows and configuration, declared per file with `REUSE.toml`.
