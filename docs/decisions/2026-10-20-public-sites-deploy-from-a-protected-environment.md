# A public repository's static site deploys from a protected environment

Date: 2026-10-20
Status: accepted

## Context

A site built from a public repository needs a deploy credential. Giving it to every workflow run, or deploying from a
server that pulls the repository, widens the attack surface of a repository that anyone can read and fork.

## Decision

We will deploy a public repository's static site from that repository's own GitHub Actions on push to `main`, with the
hosting provider's documented action. The build job holds no secret. The deploy job runs in a protected Environment
whose deployment branches are `main` only, so [environment secrets are released only after its protection rules
pass](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) and the
job receives only the built files and the token. The token is scoped to that one site, expires within one year with an
alert, and is a secret of the Environment only. This is standard §7B.16.

## Consequences

The deploy does not depend on any server of ours. A leaked repository secret list cannot expose the token, because the
token is in the Environment. The cost is one Environment per site, and the first deploy needs a one-time setup of the
site in the provider's dashboard.
