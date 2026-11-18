# Contributing to Engineering Practices

This repository holds the written rules in `STANDARD.md` and a guide per language or tool in `docs/`. The rules every
repository follows are in [STANDARD.md](STANDARD.md); this file adds only what is specific here.

## Commands

Set up once: `VENV="${TMPDIR:-/tmp}/ep-venv"; python3 -m venv "$VENV"`, then install the hash-pinned tools with
`"$VENV/bin/pip" install --require-hashes --only-binary :all: -r .github/requirements/pre-commit.txt -r
.github/requirements/reuse.txt -r .github/requirements/zizmor.txt` (reuse needs the system package `libmagic1t64`), and
`"$VENV/bin/pre-commit" install`. At commit time the hook runs gitleaks with `.gitleaks.toml` and the suppression check;
the `Secret scan / Full history` CI check scans the full history. Each row below is what CI runs, in the job named in
the last column.

| To | Run | CI job |
|---|---|---|
| Run every hook: suppressions, zizmor, REUSE lint (gitleaks too, which CI skips) | `PATH="$VENV/bin:$PATH" pre-commit run --all-files --hook-stage manual` | Repository checks |
| Check the links | `lychee --offline --no-progress './**/*.md'` | Local links |

## Map

| Path | Holds |
|---|---|
| `STANDARD.md` | The numbered rules |
| `docs/` | One guide per language or tool; `docs/decisions/` holds why a rule exists |
| `.github/` | CI, link, CodeQL and Scorecard workflows; the Dependabot file |
| `.github/requirements/` | Hash-pinned CI tools (pre-commit, reuse, zizmor) |
| `.suppressions`, `scripts/check-suppressions.sh` | Every lint suppression, one line each, and the check that lists them (a copy of docs/suppressions.md's script) |
| `.gitleaks.toml`, `.pre-commit-config.yaml` | The leak patterns and the hooks |
| `CHANGELOG.md` | One line per change, newest release first |
| `LICENSE`, `LICENSES/`, `REUSE.toml` | Licence texts and the licence of every file |

## Boundaries

- Never renumber a rule: other repositories cite the numbers. A rule that is retired keeps its number and says so.
- Nothing private goes here (standard §0): no private repository, machine, vendor or account names, and no personal
  data. Public links go only to well-known documentation sites.
- `.gitleaks.toml` holds patterns only, never the names of private things (standard §0.7).
- A suppression (`# noqa`, `# type: ignore` or `# zizmor: ignore[rule]`, each with a reason) is listed in
  `.suppressions` as `path: comment`, sorted; the `suppressions` hook fails on any difference (docs/suppressions.md).
- CI tools are installed from `.github/requirements/*.txt` with `--require-hashes`. Regenerate one from its `.in` file
  with `uv pip compile --generate-hashes --universal --exclude-newer <date 7 days ago> --python-version 3.12 -o <tool>.txt
  <tool>.in`. Dependabot updates these files itself, through `pip-compile`, because each `.txt` has a matching `.in`.
- Every action in a workflow is pinned by full commit SHA with its release in a comment, and the release is at least 7
  days old (standard §7B.4, §7B.1).
- This repository has no pnpm or uv lockfile and no container image, so it runs no `dependency-age` workflow and needs
  no daily re-run; its GitHub Actions pins rely on Dependabot's cooldown (standard §7B.13).
- Licence texts in `LICENSE` and `LICENSES/` stay verbatim and are exempt from the typography rule (standard §6.9),
  which covers only what we author.
- Secrets never go in git.

## Done means

- Every hook passes (the first command above) and so do the CI checks.
- Every document the change makes wrong is updated or deleted in the same pull request, and a changed decision has a
  new record in `docs/decisions/`.
- A rule change cites its sources (standard §2).
- `CHANGELOG.md` has one line if users will notice the change.

## Commits and pull requests

The rules are in standard §6: short messages, no dashes, commits credit people only, one pull request per piece of
work, and a maintainer merges. Issues and discussions are welcome; pull requests are limited to maintainers
(standard §7F.4).
