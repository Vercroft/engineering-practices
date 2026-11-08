# Public repositories run CI on hosted runners only

Date: 2026-11-04
Status: accepted

## Context

Anyone can open a pull request against a public repository. A self-hosted runner executes the code of whatever
workflow runs on it, so a pull request from a stranger could run code on our own machines. GitHub's guidance is that
"self-hosted runners should almost never be used for public repositories on GitHub, because any user can open pull
requests against the repository and compromise the environment"
([secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)). GitHub-hosted runners are
free for public repositories.

## Decision

We will run every public repository's CI on GitHub-hosted runners only. Private repositories choose their runners in
their own rules. This is standard §7B.15.

## Consequences

Public CI cannot reach anything on a private network, and cannot read a private repository, so it holds no secret
meant for private tooling. The cost is that a public job needing private resources cannot run in the public repository;
that work moves to a private one.
