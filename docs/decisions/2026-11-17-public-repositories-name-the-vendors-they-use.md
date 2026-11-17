# Public repositories name the vendors they use

Date: 2026-11-17
Status: accepted

## Context

§0.7 kept the names of private vendors out of every public repository. A public repository's own code has to call
the services it uses: an API address, an SDK in its dependencies, an authorisation scheme, a step in its deploy
workflow. Its privacy page has to tell users who receives their personal data and in which country, as the GDPR
requires of the information given to them (Article 13(1)(e) and (f)). Keeping those names out was therefore
impossible where the repository works at all, and it protected nothing: anyone can read the code or the privacy page.
What has to stay secret is the key, not the name of the vendor that issued it.

## Decision

A vendor stops being private where a public repository's own code, dependencies or deploy workflow use it. The
repository may name it there and in the docs for that code, and its privacy page names everyone who receives users'
personal data and in which country. Planning notes, research and issues still never name a private vendor. A product
name the organisation's own website publishes is public; its private repository's name, paths and links stay
forbidden (§0.7).

## Consequences

A repository's forbidden-names check allows the vendors that repository uses, in the places this decision names. The
keys stay protected as before: secret scanning, its own gitleaks rules (§7C.6) and the rule that secrets never go into
git (§7.1). A vendor that a public repository does not use stays on its list.
