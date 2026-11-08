# How a repository documents itself

The templates, sources and reasons behind standard §11.7 and §11.8. The rules are in the standard; this page holds only
what they point to. Researched 2026-11-06.

## Sources (read in full 2026-11-06)

- [GHC] GitHub Docs, [Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors):
  a `CONTRIBUTING.md` in the root, `docs` or `.github` is linked when someone opens an issue or pull request, shown as a
  "Contributing" tab and a sidebar link, and listed on the repository's contribute page.
- [DIA] Diataxis, [home](https://diataxis.fr/), [tutorials](https://diataxis.fr/tutorials/),
  [how-to guides](https://diataxis.fr/how-to-guides/), [reference](https://diataxis.fr/reference/) and
  [explanation](https://diataxis.fr/explanation/): four needs and four forms, each kept apart.
- [KAC] [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/): a changelog is "a curated, chronologically
  ordered list of notable changes", for humans; "Don't let your friends dump git logs into changelogs"; types Added,
  Changed, Deprecated, Removed, Fixed, Security; ISO dates; an Unreleased section on top.
- [ADR] Michael Nygard, [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  (2011), the [ADR site](https://adr.github.io/) and [MADR](https://adr.github.io/madr/): one short record per decision
  with title, context, decision, status and consequences; a reversed decision is kept and marked superseded; "Large
  documents are never kept up to date. Small, modular documents have at least a chance at being updated."
- [WTD] Write the Docs, [Docs as code](https://www.writethedocs.org/guide/docs-as-code/): documentation in version
  control, reviewed and tested like code, so that a change can be blocked when its documentation is missing.

Null results and limits:
- No study was found that measures how stale documentation misleads contributors who run the commands they find. The argument is plain: a wrong command costs a failed run, or worse.
- The two numbers, "about 200 lines" for `CONTRIBUTING.md` and "one screen" for the README, are this standard's own choice, not
  sourced.
- Dated file names for decision records are our choice; [ADR] numbers records in sequence. A date orders
  records without a counter that two branches could both take.
- The Diataxis tutorials page says tutorials take "a remarkable amount of effort and time" to write and keep true,
  which is why the standard asks for one only where users must learn the product.

## Why one `CONTRIBUTING.md` for every contributor

- A short README plus a second file of commands for another audience states each command twice. Here the README is
  already one screen, and what an automation account needs (commands, conventions, commit and pull request rules) is
  what a human contributor needs too. One file states each command once.
- [GHC] makes GitHub show `CONTRIBUTING.md` to every human who opens an issue or pull request. Nothing shows a per-tool
  instruction file to humans.
- The standard keeps personal tool files out of repositories (§7E.3), so a person's own setup points at
  `CONTRIBUTING.md`.
- The cost: a contributor whose editor or automation account expects another file name must configure it to read
  `CONTRIBUTING.md`.

## Which kind of document is it

Test a `docs/` page by its reader's question [DIA]. If a page answers more than one, split it.

| Kind | The reader asks | It contains | It does not contain |
|---|---|---|---|
| How-to | "How do I get this done?" | Steps toward one goal, in order | Explanation, or a list of every option (link to the reference) |
| Reference | "What exactly is it?" | Neutral facts, in the structure of the thing described | Instructions or opinions |
| Explanation | "Why is it so?" | Context, reasons, alternatives, bounded to one topic | Steps or lookup facts |

## Template: `CONTRIBUTING.md`

````markdown
# Contributing to <repository>

<One sentence: what this repository is.> The rules for every repository are in <link to the standard; a public
repository states the behaviour instead, standard §0.3>; this file adds only what is specific here.

## Commands

| To | Run |
|---|---|
| Install, with the git hooks | `<command>` |
| Run the full tests (what CI runs) | `<command>` |
| Run one test | `<command> <path or name>` |
| Lint and format | `<command>` |
| Run the project locally | `<command>` |

## Map

| Path | Holds |
|---|---|
| `<src/>` | <what> |
| `<tests/>` | <what> |
| `docs/` | how-tos, references and explanations; `docs/decisions/` holds why |

## Boundaries

- Never edit by hand: `<generated files>`; regenerate with `<command>`.
- Secrets never go in git: <where they live>.
- Do not touch without the maintainers: `<paths>`.

## Done means

- The full tests and the linter pass, as CI runs them.
- New behaviour has a test that failed before the change.
- Every document the change makes wrong is updated or deleted in this pull request, and a changed decision has a new
  record in `docs/decisions/`.
- `CHANGELOG.md` has one line if users will notice the change.

## Commits and pull requests

<Link to the standard's section 6 (a public repository states the rules). Add only what is specific here, such as a title format.>
````

## Template: decision record

`docs/decisions/YYYY-MM-DD-short-title.md`, one page at most, written as if to a developer who arrives next year [ADR]:

````markdown
# <A short noun phrase naming the decision>

Date: YYYY-MM-DD
Status: accepted
Supersedes: [<title>](YYYY-MM-DD-title.md)   <!-- only if it does -->

## Context

<The forces at play, as plain facts: what made a decision necessary.>

## Decision

<What we do, in full sentences: "We will ...".>

## Consequences

<What changes afterwards, good, bad and neutral, including what it costs.>
````

When a later record supersedes this one, only its status line changes, to
`Status: superseded by [<title>](YYYY-MM-DD-title.md)`. Add a "Considered options" list only when the alternatives
matter [ADR].
