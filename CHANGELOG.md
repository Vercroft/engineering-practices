# Changelog

All notable changes to this repository are listed here, newest first, in the format of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- CI badge in the README.
- FSL-1.1-MIT as a fourth code licence in §7F, for public products sold as a hosted service.
- Two principles in §1: simplicity first (7) and surgical changes (8).

### Changed

- The leak patterns allow GitHub's noreply address, which GitHub uses as the committer of merge and web-edit commits.
- The leak patterns allow links to five more reviewed public hosts: files.pythonhosted.org and pypi.org, which a
  uv lockfile names, and pythonspeed.com, www.b-list.org and x.com, which the rules cite.
- The Python guide adopts a new feature release from its first bugfix release, once that is 7 days old (rule 4.1).
- §2.5: state assumptions before building, and ask first when a request can be read two ways.
- §6.14: keep each pull request reviewable, one piece of work or one batch of related changes; about 100 changed lines is a good size and 1000 usually too large.

## [0.1.0] - 2026-11-08

### Added

- The numbered rules in `STANDARD.md` and the guides for Python, TypeScript and JavaScript, Rust, Dependabot,
  suppressions and documentation.
- CI, link, CodeQL and Scorecard workflows, the Dependabot file, the leak patterns and the commit-time hook.
- CC BY 4.0 for the text and MIT for the workflows and configuration, declared per file with `REUSE.toml`.
