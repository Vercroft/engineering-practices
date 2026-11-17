# Paid GitHub features and the leak rule

Date: 2026-11-17
Status: accepted

## Context

GitHub's secret scanning is free on public repositories, but on a private repository on GitHub Team it is the paid
Secret Protection add-on ([about secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)).
An organisation's audit log showed that transferring a private repository with it switched on was billed for the
month; GitHub's docs do not describe this. Secret Protection and Code Security are billed per active committer
([Advanced Security billing](https://docs.github.com/en/billing/concepts/product-billing/github-advanced-security)),
and a budget does not switch them off where they are already on
([budgets](https://docs.github.com/en/billing/how-tos/set-up-budgets)). Artifact attestations are available to private
repositories only on GitHub Enterprise Cloud
([artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)).

Without secret scanning, private repositories rely on gitleaks alone. §7C.6 asked for a hook and a CI scan but did not
say what each scans, how the CI scan is shared, or which rules a repository adds. Gitleaks is feature complete and takes
security patches only, and its author now works on Betterleaks, whose v2 changes the config format
([gitleaks README](https://github.com/gitleaks/gitleaks#readme),
[Betterleaks v2 migration guide](https://github.com/betterleaks/betterleaks/blob/main/docs/v2_migration.md)).

## Decision

- Secret scanning with push protection and private vulnerability reporting run on public repositories only; artifact
  attestations and attested SBOMs are for public repositories only (§7C.1, §7C.2, §7B.10, §7B.11).
- No paid GitHub feature is switched on by accident: paid add-ons stay off, every metered product has a budget that
  stops usage, a repository's paid features are checked before a transfer, and only the people GitHub lets manage
  billing change it (§7C.7).
- Every repository runs gitleaks at commit time on the staged changes, and on every pull request a full-history scan
  from one reusable workflow in the organisation's public shared workflow repository. A public repository can call
  only public reusable workflows
  ([reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)).
  Each repository keeps its own `.gitleaks.toml` with rules for its own secret formats (§7C.6).
- We stay on gitleaks and look at Betterleaks again once its v2 is stable.

## Consequences

Private repositories have no GitHub secret scanning, so a leak there is caught only by gitleaks and by review. A
licence-based product cannot be capped by a budget, so it must stay switched off. The shared workflow must exist before a
repository can switch its own CI scan to it; until then each repository keeps the scan it runs today.
