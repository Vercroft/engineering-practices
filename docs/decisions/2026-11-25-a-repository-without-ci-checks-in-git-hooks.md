# A repository without CI runs its checks in git hooks

Date: 2026-11-25
Status: accepted

## Context

The standard assumed every repository has CI: standard §4.6 puts small checks in one CI job, and §11.8 runs the link
checks in CI. Some repositories have no runner. Two items already said what such a repository does, each for one case:
§6.11 (its pre-push hook checks a clean copy of each pushed commit) and §7C.6 (its pre-push hook runs the secret scan).
Nothing said where its other checks run, where a check of the commit message runs, or what happens to a scheduled check.

## Decision

We will run every check a repository's CI would run as git hooks when it has no CI: at `pre-push`, in a clean copy of
the pushed commit, and at `commit-msg` for a check that reads the message. Its `CONTRIBUTING.md` says so. A scheduled
check is a scheduled workflow or a `manual` hook with a recorded exception, as the maintainers choose. The rule is in
standard §4.6; the configuration, tested in a throwaway repository on 2026-11-25, and the hooks' limits are in
[docs/required-checks.md](../required-checks.md#a-repository-without-ci). §6.11, §7C.6 and §11.8 link to it.

## Consequences

A repository without CI still cannot push a branch whose tip fails a check, as long as its hooks are installed and
not skipped. That is weaker than CI: hooks run on each contributor's machine and `git push --no-verify` skips them, so
review cannot rely on them the way it relies on a required check. pre-commit checks only the first branch of a push
that sends new commits, so contributors push one branch at a time. §6.11 used to say each pushed commit; pre-commit
checks the pushed tip, as CI checks a pull request's head, and the text now says so. No primary source sets this rule;
it rests on how git and pre-commit work and on practitioner reports.
