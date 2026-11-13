# Engineering Practices

The default rules for every repository that adopts them. Each repository's `CONTRIBUTING.md` and `docs/` adopt this
file and add only what is their own. Where a repository rule conflicts with this file, this file wins unless the
maintainers record an explicit exception.

Section numbers are stable, so a citation of one keeps resolving. A number that is marked "Reserved" is used by rules
that are not part of this document.

**Standing permission (decision, 2026-10-11):** anyone may propose an improvement whenever research shows a better
established practice, always as a pull request with the reason and named sources for each change, never mixed into
unrelated work, and merged as §6.3 says.

---

## 0. Public and private boundary

1. **Nothing about private work may appear in a public repository.** That includes private repository names, internal servers, hosting-provider account details used for private operations, internal hostnames, runner or VPN setup, a person's workstation setup, internal rule or section numbers when discussing private operations in public, deploy-secret names, file paths inside private repositories, and any other internal architecture. The ban covers **files, commit messages, issues, pull request titles and bodies, comments, releases, repository descriptions, topics and wiki pages**. GitHub retains edit history: do not "fix in place" a leak in a public issue or pull request; treat it as an incident (§7A).
2. **Internal tracking lives only in private repositories.**
3. **A public repository never names private repositories** and never cites internal rule numbers as authority in public issues, pull requests or docs. Public docs may describe the *behaviour* required without pointing at private rule IDs.
4. **Automation accounts check this boundary before writing anything to a public repository**, comments and pull request bodies included. If unsure, write only in a private repository and ask a maintainer.
5. Reserved.
6. **A repository is public only on purpose, never to save CI minutes. Never flip a private repository to public (decision, 2026-11-04).** Its history keeps every old secret, address and internal name, and §7A.3 shows what cleaning public history costs. Make a new repository with one clean commit instead, after a full gitleaks scan (§7C.6) and an email-address scan of the files to be committed, with noreply addresses only (§6.12).
7. **Names that never appear in a public repository (decision, 2026-11-06).** Each repository keeps its own list of forbidden names in a private place and checks every tree and every commit message against it before anything is published. The list covers the names of private repositories, the hosting provider and account of production servers, private vendors and integrations, accounts used for private operations, and real secret names. The list itself is never published.
8. **Machine and account identifiers live only in operations repositories (decision, 2026-11-04).** Machine names, server names, IP addresses and hosting account IDs are written only in the operations repositories, never in a product or site repository, public or private. A product or site repository that needs one at run time reads it from a CI secret or from configuration held outside the repository (§7.2).

---

## 1. Principles

1. **Cut real cost.** Prefer open-source and self-hosted tools we control. Never build on a SaaS free tier as a dependency; when a free tier has a limit, use the standard pattern that removes the dependency on it (example: host static sites as assets only, so requests are not billed). Paid infrastructure we cannot avoid is accepted.
2. **Industry-standard patterns only.** Use documented approaches that serious teams use. No workarounds, hacks or tricks that save effort or money today and create risk later.
3. **Root causes, not symptoms.** Find why something broke before fixing it. Where a mistake can be made impossible rather than merely discouraged, do that. If duplication cannot be removed, make divergence fail a check.
4. **Smallest enforcement that makes the error impossible.** Prefer a test, a type, or a fail-closed check over a written instruction.
5. **Think widely.** Every change is judged for its effect on all products, shared infrastructure, cost, security and the maintainers' time, not only the task in front of you.
6. **Adopt before you build (decision, 2026-10-19).** Before writing any component, check for a maintained, free, open-source tool that already does it: a server application, a library, a plugin or a skill. Use it when it is maintained, fits our resources and passes §7B; write our own code only where nothing fits, and say in the pull request what was compared. Never depend on a SaaS free tier (§1.1).
7. **Only what is required (decision, 2026-11-13).** Do everything the task requires, completely and properly, and add nothing it does not need: no feature, option, abstraction, step or error handling for a case nobody asked for or that cannot happen. Required work is never cut to make a change smaller. If a senior engineer would call the change overbuilt, make it smaller. Google's review guide calls over-engineering a kind of complexity: code "more generic than it needs to be", or "functionality that isn't presently needed" ([what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)). Andrej Karpathy lists overcomplicated code and bloated abstractions among the mistakes coding agents keep making ([post, 2026-01-26](https://x.com/karpathy/status/2015883857489522876)).
8. **Surgical changes (decision, 2026-11-13).** Every changed line traces to the task. A problem found on the way that the task does not need (dead code, an unrelated bug, style elsewhere) is reported, not fixed in passing; review findings on the change itself follow §5.3. Remove only what your own change made unused. A refactor is its own pull request. Karpathy saw coding agents change or remove code "orthogonal to the task at hand" (same post); Google's guide: "It's usually best to do refactorings in a separate CL from feature changes or bug fixes" ([small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)).

## 2. Research before every decision

1. Research first, every time. Primary sources come first: official documentation, specifications, changelogs, security advisories, maintainers. Practitioner reports (forums, issue trackers, write-ups) are evidence of real-world behaviour, never the sole authority.
2. Name what you checked in the reply. A decision with no sources named means the research was skipped.
3. Report null results as findings ("checked X, found nothing").
4. Treat the codebase as the source of truth and every document as a claim to verify. Where they disagree, report it, and correct the document in the same change that proves it wrong.
5. Say plainly what you could not verify. Never present a guess as a fact. State your assumptions before building, and when a request can be read two ways, ask first (decision, 2026-11-13). In a report, keep apart what was verified (checked against a source, the code or a run), what is inferred, and what is assumed (decision, 2026-11-13).

## 3. Code quality

1. Choose the optimal time and space complexity wherever input can grow, and state it. For small, fixed inputs, the simplest correct code wins. Never accidental quadratic behaviour; never work repeated per item that can be done once.
2. Small, single-purpose modules; current idioms; typed wherever the language supports it. Python follows [docs/python.md](docs/python.md) (PEP 8, mypy strict, one shared ruff configuration); TypeScript and JavaScript follow [docs/frontend.md](docs/frontend.md); Rust follows [docs/rust.md](docs/rust.md); lint suppressions in all three follow [docs/suppressions.md](docs/suppressions.md).
3. Prefer well-maintained, widely adopted open-source libraries over hand-written code, chosen on evidence, pinned (exact versions, lockfiles, action commit SHAs verified against the official tag) and licence-checked.
4. Adding a dependency is a design decision agreed with the maintainers. Check the package's advisory history and maintainer status first.
5. Name everything by product, component and purpose. No vague or misleading names. **Public repositories must not use names that reveal private infrastructure.**
6. **Measure before optimizing (decision, 2026-11-13).** A change made for speed or memory starts from a measured baseline on a representative workload, compares the alternative on the same workload, and records the before and after numbers in the pull request. Without a measurement, the simpler code stays. Correctness and security are never traded for an unmeasured gain. Python's documentation: profiling statistics "help identify performance bottlenecks and guide optimization efforts", and "For benchmarking, use the timeit module" ([profiling](https://docs.python.org/3/library/profiling.html#introduction-to-profiling)), which "avoids a number of common traps for measuring execution times" ([timeit](https://docs.python.org/3/library/timeit.html)); memory is measured with [tracemalloc](https://docs.python.org/3/library/tracemalloc.html). Google's guide lists "benchmark results" among what a change description includes ([CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)).
7. **Production behaviour (decision, 2026-11-13).** Every call to a network service or a database has a timeout. A retry is only for an operation that is safe to repeat, and it is bounded and backs off. An event that can arrive more than once (a webhook delivery, a queued job, a resubmitted form) is handled idempotently, keyed by its own ID. Writes that must succeed or fail together run in one transaction. A failure is reported clearly, never swallowed ([docs/python.md](docs/python.md) rule 6). The defaults wait forever: Python's default socket timeout is `None`, which "indicates that new socket objects have no timeout" ([socket](https://docs.python.org/3/library/socket.html#socket.getdefaulttimeout)), and for PostgreSQL's `statement_timeout` "A value of zero (the default) disables the timeout" ([client connection defaults](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-STATEMENT-TIMEOUT)). GitHub: "wait for an exponentially increasing amount of time between retries, and throw an error after a specific number of retries" ([REST API best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api#handle-rate-limit-errors-appropriately)). A webhook's `X-GitHub-Delivery` header is "A globally unique identifier (GUID) to identify the event" ([delivery headers](https://docs.github.com/en/webhooks/webhook-events-and-payloads#delivery-headers)), and on a redelivery it "will be the same as in the original delivery" ([webhook best practices](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks#use-the-x-github-delivery-header)). PostgreSQL: a transaction "bundles multiple steps into a single, all-or-nothing operation" ([transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)).
8. **Application layout: by feature (decision, 2026-11-13).** An application groups its code by feature (domain), not by file type: one folder per feature holds its routes and logic, and shared infrastructure (database, models, migrations, and settings used by several features) sits at the package root; a setting only one feature uses lives in that feature's folder. Each process the application runs (for example web, worker) is a thin entry module that only wires the features together. Where a framework fixes the layout (for example Next.js routing), the framework's layout wins. Split into `backend/` and `frontend/` only when the front end has its own toolchain; server-rendered templates and static files live inside the package. Start flat: a feature gets its own folder once it has two or more modules, and no folder is made in advance. Tests mirror the feature folders. Grouping by file type "works well for microservices or smaller projects" but "didn't scale well for our monolith with many domains and modules", says a widely cited practitioner guide ([zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices#project-structure)); FastAPI's main module "ties everything together" by including each area's router ([bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)). Python: [docs/python.md](docs/python.md) rule 1.6.

## 4. Testing and CI runners

1. Every fix gets a regression test that is shown to fail against the old code before the fix exists ("red first"), then pass.
2. Prove tests can fail: deliberately break the code (mutation) and show the test catches it, in both directions.
3. Where a guarantee genuinely cannot be tested, say so plainly instead of claiming coverage.
4. Every test and CI step has a time limit, so a hang fails fast instead of burning minutes.
5. Where CI runs: §7B.15 for public repositories.

## 5. Reviews

1. Default: the author reviews their own change against a written checklist (correctness, security, tests) and relies on CI's automated checks.
2. High-risk changes only (authentication, billing, deploy gates, server security, secrets, workflows): exactly one independent reviewer, with a bounded report. Never several reviewers in parallel.
3. Only must-fix findings block. Cheap should-fix items are fixed in the same pull request. Genuinely separate work becomes one follow-up issue per batch.

## 6. Git, pull requests and merging

1. Merge commits only. Never force-push; never rewrite shared history **except** the personal-data incident procedure in §7A (`git filter-repo --sensitive-data-removal` and GitHub Support, directed by a maintainer).
2. Reserved.
3. **A maintainer's approval on the head commit is the decision to merge (decision, 2026-10-20; survives clean merges of the base, 2026-10-31).** There is no separate merge word. An approval covers the head it was given on. It covers a later head only when every commit pushed since is a clean merge of the base branch (two parents, the second already on the base, no conflict resolved by hand) and the pull request's own diff is identical to the approved head's (`git patch-id`, and the same file modes), with CI green on the final head; any other change needs a fresh approval. GitHub moves an approval onto a new head when a push keeps the pull request's changes, so the approved head is read from the branch's recorded push history, never from the review's commit. A ruleset that dismisses stale approvals and requires approval of the last push (§7C.5) dismisses on any push, so there the maintainer approves again. Who merges: §6.13.
4. A pull request must contain the latest target-branch tip and pass CI on its exact head before approval is requested. Ask for approval only when it is the last thing missing.
5. Reserved.
6. Batch related issues by area. Pull requests that touch the same files merge one at a time, in an order stated up front, each re-checked on the new `main`.
7. Commit messages contain no email addresses, phone numbers, secrets, private repository names or internal architecture.
8. **Commits credit people only (decision, 2026-10-07; widened 2026-10-22).** A commit's author, committer and co-author are people with approved identities, and no tool is named as any of them or anywhere in commit or pull request text, for every contributor in every repository.
   - **Default-deny:** only approved identities (GitHub noreply addresses), trailer keys and link hosts pass. Adding a person, trailer or host is one reviewed line. Automation accounts are a separate list, refused as authors and committers. A list of known tools only words error messages and never decides.
   - Tools' own attribution settings are turned off. History is reported, never rewritten, except by the incident rewrites of §7A.
   - **No tool wording anywhere in a repository (decision, 2026-11-05).** Commits, branch names, pull request titles and bodies, READMEs and docs never name or credit the tools used.
9. Commit messages, pull request titles and bodies, issues, comments and every file we author never use an em dash (U+2014) or en dash (U+2013). Use a normal hyphen, a colon, or rewrite the sentence. A repository may exempt user-contributed content (for example people's own profile text) and must say so in its own `CONTRIBUTING.md`.
10. **Short commit and pull request messages (decision, 2026-10-19).** A commit's first line says what changed in at most 72 characters (Git's documentation: a short summary line); its body says why in a few lines, not how. A pull request description fits on one screen: what changed, why, the proof (one line each, linking to the run, test or document that holds the detail), the risks, every lint suppression it adds ([docs/suppressions.md](docs/suppressions.md)), and a "Docs updated" section (§11.3). Detail belongs in the docs and tests, not in the message.
11. **Work in the real local folder (decision, 2026-10-20).** Work happens in the repository's own local folder, on a branch, or in a `git worktree` of that folder for parallel work; never in an ad-hoc clone elsewhere. Tests and linters run in that folder too, and the clean-copy check is CI on the pull request. A local folder is named after the repository. If the local folder is in a bad state (for example detached on a commit no remote has, or holding changes you did not make), report it and stop.
12. **Authorship (decision, 2026-10-21).** **Credit goes to the developer.** Every commit with real changes is authored and committed under the developer's own GitHub account, with its noreply address. GitHub counts a commit on a profile only when it is "made with an email address that is connected to your account" and is in "the default branch or the `gh-pages` branch" ([contributions](https://docs.github.com/en/account-and-profile/reference/why-are-my-contributions-not-showing-up-on-my-profile)), so the work counts for that developer once it merges. Automation accounts never author or commit a content commit.
13. **Only a maintainer merges (decision, 2026-11-05).** A maintainer merges every pull request, in the GitHub UI, with the merge-commit method, so every merge commit is authored by a human. Automation accounts open pull requests, push branches, comment and run checks; they never merge and never enable auto-merge (the account that enables it authors the merge commit). Dependabot-authored commits are accepted on `main`; a maintainer merges its pull requests like any other. The approval rules of §6.3 are unchanged: the approval on the head comes first, and the merge is the last click.
14. **One pull request per piece of work (decision, 2026-11-05).** Docs, README and decision records travel in the same pull request as the change they describe (§11.3). Exception: never push to Dependabot's branches; a docs follow-up for a Dependabot pull request rides with the next real one instead. Keep each pull request reviewable: one piece of work, or one batch of related changes (§6.6); about 100 changed lines, not counting generated files such as lockfiles, is a good size, and 1000 is usually too large ([small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)) (decision, 2026-11-13).
15. **Contributor identities (decision, 2026-11-05).** Every commit's author, committer and `Co-authored-by` must be an approved person, listed in the repository's approved-identities list, or Dependabot (its own update commits, [docs/dependabot.md](docs/dependabot.md)) or GitHub's own merge identity. In community repositories that accept outside pull requests (§7F.4), they must be the pull request's author themselves. A pull request check enforces it, and the check names no tools.

## 7. Security (secrets and access)

1. Secrets never appear in git, on a command line, in logs, in chat or in reports. Report metadata only (names, sizes, counts, hashes). Every commit and every CI run is scanned for them in every repository: §7C.6.
2. Production secrets live in root-owned files read at the last moment (mounted secret files), not in environment variables or `.env` files where avoidable.
3. Least privilege everywhere: one token per product and purpose, scoped to the minimum resources, IP-filtered to the server where the provider supports it, with an expiry date and an alert before it expires.
4. Reserved.
5. Web: HTTPS only (HSTS at the CDN), framing forbidden (`frame-ancestors 'none'`), a content security policy, and login tokens in `HttpOnly` cookies, never in `localStorage`. Credential pages and everything that builds them are protected paths.
6. Reserved.
7. Treat rate-limit counters, client addresses and forwarded headers as security-critical: trust a forwarded address only from a known proxy.
8. Reserved.

## 7A. Personal data (public repositories and everything published)

1. **No phone numbers or street addresses in any public repository, or in anything published** (websites, releases, packages, public artefacts), whatever repository they are built from, in any format, including PDFs, images and image metadata (EXIF/XMP). Prefer contact forms or request-a-call flows over publishing phones.
2. **A leak guard is required in every public repository** (tree, staged and commit-range scans as appropriate), and must be a **required status check** on the default branch.
3. **Incident procedure if personal data or other secrets leak into a public repository or a published artefact** (prevention: a private repository is never flipped to public, §0.6):
   1. Rotate or revoke any leaked credential first.
   2. Stop further pushes that could spread the leak.
   3. Remove the data from tip files immediately.
   4. Rewrite history with `git filter-repo --sensitive-data-removal` (directed by a maintainer; this is the sole exception to "never rewrite shared history"). Binary files (PDF, images) need blob removal (`--strip-blobs-with-ids`); text replacement does not clean them.
   5. Open a GitHub Support ticket for cached views, pull request refs and forks as needed.
   6. Take down or rebuild any deployed copies that still serve the leak. Check every published copy, including old deployments and preview URLs.
   7. Record an explicit maintainer exception for the rewrite.
   8. Re-clone every working copy and CI cache that may still hold the old objects.

## 7B. Supply chain

1. **Dependency updates are monthly, grouped and checked by tools (decision, 2026-11-06).** New package versions must be at least 7 days old before adoption; §7B.13 enforces it in CI. **Dependabot:** alerts on for every repo; version updates on, monthly, with `cooldown: default-days: 7` and an open-PR limit; all minor and patch updates of an ecosystem arrive in one pull request and each major in its own; security updates on, grouped per ecosystem, and still opened at once because the cooldown applies to version updates only ([GitHub's docs](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)). Dependabot ignores a language runtime's new language version (Node majors; Python 3.x minor versions such as 3.14 to 3.15), a database's major and a base image's major; each is updated only in a planned pull request (§7B.12). Template and known gaps: [docs/dependabot.md](docs/dependabot.md).
2. **Exact pins and lockfiles.** Application dependencies use exact versions (no `^` / `~`). Commit the lockfile. CI installs with `--frozen-lockfile` (or equivalent).
3. **Install scripts blocked by default.** Allow only named packages that need a build/postinstall (pnpm `allowBuilds` with `strictDepBuilds: true`, which replaced `onlyBuiltDependencies` in pnpm 11; uv `no-build = true`; or equivalent), each with a one-line reason.
4. **GitHub Actions pinned by full 40-character commit SHA**, with a version comment. **Verify the SHA is the official tag's commit on the upstream repository** (not a fork "imposter" commit). Tools such as zizmor's `impostor-commit` check help automate this.
5. **`permissions:` least privilege** on every workflow (default deny; grant only what the job needs). Prefer `contents: read` unless the job must write.
6. **`persist-credentials: false`** on `actions/checkout` unless the job truly needs to push or call the API with the default token.
7. **Static analysis of workflows** (for example zizmor) in CI for public repos and for private repos that run untrusted automation.
8. **Never use `pull_request_target` in a way that checks out and executes pull request code.** Prefer `pull_request` on GitHub-hosted runners for public repos.
9. **OpenSSF Scorecard** enabled for public repositories; triage and fix actionable findings.
10. **Build provenance / artifact attestations** for deployable build outputs (GitHub artifact attestations; aim for SLSA Build Level 2+, Level 3 via reusable workflows where practical).
11. **SBOM** generated for release/deploy artifacts (and attested where attestations are used).
12. **Runtimes, databases and base images run only supported versions (decision, 2026-10-26).** A language runtime, a database or an operating-system base image runs only a release its project still supports, and an LTS line where the project has one. Dependabot proposes only updates within the current language version or major (Python 3.14.x patches, Node 24.x, Postgres 18.x and the like); a new language version or major is a planned pull request that moves every pin of the image together. [docs/dependabot.md](docs/dependabot.md) ("Runtime versions", rule 15) holds the table and the sources, and a repository's own check holds its Dependabot file to it.
13. **The 7-day rule is enforced by tools, not by hand (decision, 2026-11-06).** Every repository with a pnpm lockfile, a uv lockfile or a container image runs a workflow, `dependency-age`, on every pull request. It fails when the pull request adds a version younger than 7 days. Pins of GitHub Actions and Cargo crates rely on Dependabot's cooldown, not on a workflow. It is a required status check where rulesets exist (§7C.5), and where rulesets are not available the maintainer checks it before merging. Until a repository adopts it, [docs/dependabot.md](docs/dependabot.md) rules 4 and 13 stay in force as the by-hand checks.
    - **pnpm lockfiles:** `minimumReleaseAge: 10080` with `minimumReleaseAgeStrict: true`; the workflow runs `pnpm install --frozen-lockfile --lockfile-only`, which checks every entry, transitive ones included, without installing. A plain npm project moves to pnpm when its repository adopts this rule (decision, 2026-11-06), so the same setting covers it.
    - **uv lockfiles:** `exclude-newer = "7 days"` in `pyproject.toml`; the workflow runs `uv lock --check`, never `uv sync --frozen`, which ignores the setting.
    - **GitHub Actions pins and Cargo:** Dependabot's cooldown of 7 days (Cargo's own release-age setting is not stable yet, [docs/rust.md](docs/rust.md)).
    - **Container images** (Dockerfile, compose and JSON pins): a pull request that adds an image younger than 7 days fails. The age is the `created` date in the image's config, which `docker buildx imagetools inspect <ref> --format '{{json .Image}}'` prints per platform ([docs](https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/)); the newest platform counts. A missing or 1970 date (reproducible builds), or a registry that does not answer, fails. A repository checks this in its own `dependency-age` workflow.
    - **A young security fix waits (decision, 2026-11-06).** Its Dependabot pull request stays red until the version is 7 days old; the daily re-run below turns it green. Only an emergency (§7B.14) uses an exception.
    - **An emergency exception** is made in a separate pull request that is merged first, never on a Dependabot branch: pnpm `minimumReleaseAgeExclude` with the exact `name@version`, uv `exclude-newer-package`, or for an image an entry in the repository's exception file. It names the CVE or advisory, ends within 30 days, and a maintainer approves it with its diff.
    - **Daily re-run:** needed only where the age check can fail while it waits on a fix (images or lockfiles). A repository with neither needs none. Where it applies, a scheduled workflow re-runs only the failed `dependency-age` run of each open pull request authored by `dependabot[bot]` (read from `pull_request.user.login`, never the actor), so a pull request turns green by itself once its versions come of age.
14. **Emergencies: an actively exploited vulnerability is patched at once (decision, 2026-11-06).** A vulnerability in a language runtime, a base image or the operating system that is listed in CISA's [Known Exploited Vulnerabilities catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) or that the vendor confirms is exploited is patched without the 7-day wait. The pull request cites the CVE and the source, and the `dependency-age` check passes it through an exception (§7B.13). Afterwards every running copy (every container, host and runner that uses the component) is confirmed updated, and the confirmation is recorded in the pull request.
15. **Public repositories run CI on GitHub-hosted runners only (decision, 2026-11-04).** Any user can open a pull request against a public repository, and GitHub says that "self-hosted runners should almost never be used for public repositories ... because any user can open pull requests against the repository and compromise the environment" ([secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)). Hosted runners are free for public repositories. Private repositories choose their runners in their own rules. Record: [docs/decisions/2026-11-04-public-repositories-use-hosted-runners.md](docs/decisions/2026-11-04-public-repositories-use-hosted-runners.md).
16. **A public repository's static site deploys from a protected environment (decision, 2026-10-20).** The site deploys from its own repository's GitHub Actions on push to `main`, with the hosting provider's documented action, not from a server. A build job holds no secret. A deploy job runs in a protected Environment whose deployment branches are `main` only and receives only the built files and the token ([environment secrets are released only after its protection rules pass](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)). Every action is pinned by full SHA (§7B.4); the deploy tool's version is pinned exactly and is at least 7 days old (§7B.1). No `pull_request` or `pull_request_target` trigger. The token is scoped to that one site and expires within one year, with an expiry record and an alert; it is a secret of the protected Environment only, never a repository or organisation secret. Record: [docs/decisions/2026-10-20-public-sites-deploy-from-a-protected-environment.md](docs/decisions/2026-10-20-public-sites-deploy-from-a-protected-environment.md).

## 7C. Repository security baseline

1. **Secret scanning with push protection** on every repository that supports it (required for public).
2. **Private vulnerability reporting** enabled, plus a root `SECURITY.md` describing how to report.
3. **CodeQL** (or equivalent) for public repositories on default branch and pull requests.
4. **Dependabot alerts, version updates and security updates** on, configured as §7B.1 says; their pull requests merge only as §6.3 says.
5. **Rulesets** on the default branch: required status checks, required review by the code's maintainers where CODEOWNERS exists, dismiss stale reviews, **require last-push approval**, block force-push and deletion.
6. **gitleaks on every commit and in CI, in every repository (decision, 2026-11-04).** Secrets never go into git (§7.1), and every repository, public or private, scans for them twice: at commit time with a hook, and in CI as a required check. Where a repository has no runner, its pre-push hook runs the same scan. The action or binary is pinned (the action by commit SHA, §7B.4; a binary by checksum) and the repository commits its `.gitleaks.toml`.

## 7D. Web front ends

1. **Hashed Content-Security-Policy** generated at build time from the actual HTML (script hashes; no `'unsafe-inline'` for scripts). Prove in CI with a real browser where the repo already does so.
2. **Self-hosted fonts** only (no third-party font CDNs).
3. **No third-party requests by default** (no analytics or widgets unless a maintainer explicitly approves and the CSP allowlists them).
4. Standard security headers on static responses: CSP, `frame-ancestors` / `X-Frame-Options` denial of framing, `Referrer-Policy`, `X-Content-Type-Options: nosniff`, HSTS at the CDN edge.

## 7E. Automation accounts

1. Reserved.
2. Deny rules for automation: never rewrite shared history without a maintainer's incident approval; never bypass git hooks without a maintainer's approval; never print personal data, secrets or private architecture into public surfaces; never merge without a maintainer's approval on the exact head commit (§6.3), and, in a repository that has adopted §6.13, never merge at all. An automation account never authors or commits a content commit, approves a pull request or acts for another developer.
3. **Tool and editor config is personal, never repository content (decision, 2026-11-05).**
   - **Repositories hold only the rules everyone must follow, written tool-neutral:** `CONTRIBUTING.md` and `docs/`.
   - **Personal tool and editor config** (tool settings folders, per-tool instruction files, editor recommendations) **lives in each person's own setup, never in a repository.** A global git ignore keeps it from being committed by accident.
   - **A repository that still tracks such files removes them in a planned clean-up.** Tracked files are unaffected by the global ignore ([gitignore](https://git-scm.com/docs/gitignore): "Files already tracked by Git are not affected").

## 7F. Licensing and protection of public repositories

1. **Private by default (decision, 2026-11-05).** Paid features, server code and secret logic never go in a public repository, except the server code of an FSL-1.1-MIT product (item 2), which is public on purpose so users can inspect it (decision, 2026-11-11). Paid features and secret logic stay private there too.
2. **Standard licences only, never a custom text: four for code, one for documentation.** The licence's published text goes in unchanged. Choose by kind of repository:
   - **All rights reserved** for business sites and brand repositories. Without a licence "the default copyright laws apply, meaning that you retain all rights to your source code and no one may reproduce, distribute, or create derivative works" ([GitHub Docs, licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)); the `LICENSE` file says so with a copyright line.
   - **PolyForm Strict 1.0.0** for products that are free for personal use only ([text](https://polyformproject.org/licenses/strict/1.0.0)). It permits any noncommercial purpose, personal use included, and forbids distributing the software or making changes or new works from it.
   - **MIT** for SDKs, tools and community repositories, on purpose.
   - **FSL-1.1-MIT** (decision, 2026-11-11) for public products sold as a hosted service, whose code users must be able to inspect, with paid features only in a separate private repository. The Functional Source License permits every purpose except a Competing Use, which means making the Software available to others in a commercial product or service that (1) substitutes for the Software, (2) substitutes for any other product or service we offer using the Software that exists as of the date we make the Software available, or (3) offers the same or substantially similar functionality as the Software ([FSL](https://fsl.software/), [template](https://fsl.software/FSL-1.1-MIT.template.md)). Each version becomes available under MIT on the second anniversary of the date it was made available. It differs from PolyForm Strict, which allows noncommercial use only and forbids changes, and from MIT, which lets a competitor sell the code. The `LICENSE` file is the published template unchanged, with only its copyright line filled in: the year and the licensor. Record: [docs/decisions/2026-11-11-fsl-for-public-hosted-products.md](docs/decisions/2026-11-11-fsl-for-public-hosted-products.md).
   - **CC BY 4.0** for documentation and rules that others are meant to adopt and adapt. Code samples and configuration blocks inside such documentation, and the workflows and configuration of the same repository, are MIT. A repository with both declares each file's licence in a `REUSE.toml` ([REUSE tool](https://github.com/fsfe/reuse-tool)). Record: [docs/decisions/2026-11-06-licences-for-the-public-repository.md](docs/decisions/2026-11-06-licences-for-the-public-repository.md).
3. **State it three times:** in `LICENSE`, in one README line, and in the package metadata. npm: `"license": "UNLICENSED"` and `"private": true` for all rights reserved ([npm docs](https://docs.npmjs.com/cli/v11/configuring-npm/package-json): `UNLICENSED` grants no rights, and `private` prevents accidental publication); `"license": "MIT"` for MIT; `"license": "FSL-1.1-MIT"` for FSL-1.1-MIT, which has an SPDX identifier (checked in the [SPDX license list](https://spdx.org/licenses/FSL-1.1-MIT.html) on 2026-11-11); `"license": "SEE LICENSE IN LICENSE"` for PolyForm Strict, which has no SPDX identifier (checked in the SPDX license list on 2026-11-05: only the Noncommercial and Small Business PolyForm licences are listed). Other ecosystems use their equivalent field.
4. **Contributions (decision, 2026-11-05).**
   - **Products, business sites and SDKs take no outside code.** Set Settings > General > Features > Pull requests to "Collaborators only": everyone can still see and comment on pull requests, but only users with write access can create them ([GitHub changelog, 2026-02-13](https://github.blog/changelog/2026-02-13-new-repository-settings-for-configuring-pull-request-access/)).
   - **Issues and Discussions stay open.** Bug reports, ideas and translations are the welcome contributions.
   - **Community repositories whose purpose is outside pull requests** keep pull requests open, with MIT.
   - **No CLA is needed, because no outside code comes in.** A rare invited collaborator signs a one-page agreement first.
   - **After switching a repository, confirm that the next Dependabot pull request still opens.**
   - **Why.** "Open-Source, not Open-Contribution": SQLite is open source but takes no patches from people who have not submitted a public-domain affidavit ([SQLite](https://sqlite.org/copyright.html)). Since January 2026 projects have closed or gated outside pull requests and reports because of a flood of low-quality ones: tldraw ([CONTRIBUTING.md](https://github.com/tldraw/tldraw/blob/main/CONTRIBUTING.md): "not accepting contributions ... Pull requests are turned off"), Ghostty (a vouch system for first-time contributors, [CONTRIBUTING.md](https://github.com/ghostty-org/ghostty/blob/main/CONTRIBUTING.md)) and curl, which ended its bug bounty after a flood of low-quality automated reports ([curl's maintainer](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)).
5. **Signing (decision, 2026-11-05).** Merge commits are made by a maintainer in the GitHub UI, which GitHub signs ([about signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)). Release tags are annotated and signed by a maintainer; an annotated tag carries a creation date and the tagger ([git-tag](https://git-scm.com/docs/git-tag)). Signing of branch commits is not required yet; it is a separate decision.
6. **Copies are reported by a maintainer** through GitHub's DMCA form, <https://github.com/contact/dmca> ([guide to submitting a DMCA takedown notice](https://docs.github.com/en/site-policy/content-removal-policies/guide-to-submitting-a-dmca-takedown-notice)).
7. **Trademark is optional:** register one when a product earns money, and check the name before launch.

## 8. Reserved

## 9. Reserved

## 10. Reserved

## 11. Documentation and handoffs

1. Durable rules live in the repository's tool-neutral docs, laid out as item 7 says; a person's own tool may point at them. Never only in a tool's memory.
2. Working handoffs stay outside every repository: one current handoff file per working stream. When a new one is written, superseded handoffs are deleted after anything still true is moved in. Backups, evidence and tools are kept and listed with their reason.
3. No stale content anywhere: when a change makes a document wrong, the same change corrects it. **Search first, and say so (decision, 2026-10-26).**
   - Every pull request updates or deletes, in the same pull request, every document its change makes stale: READMEs, `docs/`, runbooks, `CONTRIBUTING.md`, `CHANGELOG.md`, manifest descriptions, code comments, and the text of the issues it cites.
   - Before opening one, search the repository for the names, paths, versions and behaviours the change touched or removed, and fix or justify each hit.
   - A decision record is history: never rewritten. A changed decision gets a new record that supersedes the old one (item 7).
   - The pull request description has a **"Docs updated"** section: every document changed, or "none needed" with one line why.
4. Issues are triaged weekly: fixed ones closed with proof, duplicates merged, the rest grouped by priority.
5. Public repository documentation must obey §0 (no private names, no internal rule IDs, no personal data).
6. **Every repository's README has the same shape, and fits one screen (decision, 2026-11-05; one screen, 2026-11-06).** In this order, each part only where it is real:
   1. a screenshot or banner (a light and a dark version in a `<picture>` element if the project has both themes);
   2. a one-line description and the live link;
   3. only real badges: CI, deploy and OpenSSF Scorecard (§7B.9);
   4. a Mermaid diagram of how a change ships, without naming the hosting product (§0.7);
   5. a quick start that runs the project (install, tests, lint and the git hooks are in `CONTRIBUTING.md`);
   6. links to `CONTRIBUTING.md` and the docs;
   7. the license (§7F).

   Sources: GitHub Docs on [Mermaid diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) (a `mermaid` code block renders as a diagram), on the [`<picture>` element](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) ("The `<picture>` HTML element is supported") and on [alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (`> [!NOTE]` and its siblings, for the few points a reader must not miss).

7. **A repository documents itself in these files and no others (decision, 2026-11-06)**, so the next person understands it quickly. Templates, sources and reasons: [docs/documentation.md](docs/documentation.md).
   - `README.md`, for humans: what the project is, how to run it, links (shape: item 6).
   - `CONTRIBUTING.md`, for every contributor, under about 200 lines: the exact commands (install, full test, one test, lint), a short repository map, the boundaries (generated files, secrets, areas never to touch), what "done" means, and the commit and pull request rules by link to §6, not by copy. It takes the place of the extra instruction files some projects add: personal tool files stay out of repositories (§7E.3).
   - `docs/`: one document, one purpose, and the purpose is one of a how-to (a task to get done), a reference (facts to look up) or an explanation (why). A tutorial only for a product whose users must learn it.
   - `docs/decisions/`: one short dated record per decision, with why it was made and what it costs, named `YYYY-MM-DD-title.md`. Only the status line of a superseded record changes.
   - `CHANGELOG.md`: one line per change, for the users of the project, newest release first. A repository nobody installs or depends on has none.
8. **How documentation is written and kept true (decision, 2026-11-06).**
   - One fact, one place: link, never copy. A repository links to this standard instead of restating a rule.
   - Write only what code, config or CI cannot show. Explain why, and let code and tests prove how.
   - No logs, history or session notes in a repository: git and pull requests hold the history, issues hold open work, and handoffs stay outside (item 2).
   - Keep it true as item 3 says. CI checks links with [lychee](https://github.com/lycheeverse/lychee), through its official action [lycheeverse/lychee-action](https://github.com/lycheeverse/lychee-action) pinned by full commit SHA (§7B.4); it is the established Markdown checker, adopted under §1.6. On every pull request it runs with `--offline` (lychee's option to "Only check local files and block network requests"), so the links between the repository's own files are checked and no website can block a pull request. A scheduled weekly run checks the external links with the action's `fail: true` input, so a dead or flaky site fails the scheduled run, and a failed scheduled run notifies the person who created the workflow, or whoever last changed its schedule ([notifications for workflow runs](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/notifications-for-workflow-runs)); no pull request is affected. Every command in `CONTRIBUTING.md` is one that CI runs, so it cannot drift.

## 12. Reserved

## 13. Reserved
