# Dependabot

How we use Dependabot (decision, 2026-10-21; monthly, grouped and tool-checked since 2026-11-06), adopted by
standard §7B.1, §7B.12 to §7B.14 and §7C.4. Researched 2026-10-21; the runtime-versions rule (15) researched
2026-10-26; the monthly policy and the 7-day tools researched and run 2026-11-06.

## Sources (read 2026-10-21)

Primary:

- [OPT] [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
  (read again 2026-11-06 at this address; the old path redirects here): `schedule.interval: monthly` runs on the first of
  the month; `cooldown` applies to version updates only; `groups` take `applies-to: version-updates` or
  `security-updates`, and a dependency joins the first group it matches; `ignore.update-types` affects version updates
  only
- [OPR] [Optimizing the creation of pull requests for Dependabot version updates](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates)
- [DSU] [Dependabot security updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates)
- [CHG] [Dependabot version updates introduce default package cooldown](https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/)
  (2026-07-14): a 3-day default; we keep an explicit 7
- [UVS] [uv settings](https://docs.astral.sh/uv/reference/settings/): `exclude-newer`, `exclude-newer-package`
- [IMG] [docker buildx imagetools inspect](https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/) and the
  [OCI image configuration](https://github.com/opencontainers/image-spec/blob/main/config.md) (`created`: "the combined date and time at which the image was created")
- [KEV] CISA, [Known Exploited Vulnerabilities catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [ECO] [Supported ecosystems and repositories](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)
- [ACT] [Dependabot on GitHub Actions runners](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-on-actions)
- [REV] [Dependabot reviewers option replaced by code owners](https://github.blog/changelog/2025-08-08-dependabot-reviewers-configuration-option-is-replaced-by-code-owners/) (2025-08-08)
- [UVD] [uv: using Dependabot](https://docs.astral.sh/uv/guides/integration/dependabot/)
- [PNPM] [pnpm dependency-resolution settings](https://pnpm.io/settings/dependency-resolution)
- [CARGO] [Cargo unstable features: `min-publish-age`](https://doc.rust-lang.org/cargo/reference/unstable.html)
- [TRB] [Troubleshooting Dependabot on GitHub Actions](https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions)
- [CMD] [Dependabot pull request comment commands](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-pull-request-comment-commands),
  [managing Dependabot PRs](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/managing-pull-requests-for-dependency-updates)
- [ZIZ] [zizmor audits](https://docs.zizmor.sh/audits/): `bot-conditions`, `dangerous-triggers`, `template-injection`,
  `dependabot-cooldown`
- [ALR] [Dependabot alerts REST API](https://docs.github.com/en/rest/dependabot/alerts) (`dismissed_reason`)
- Support policies behind rule 15 (read 2026-10-26):
  - [PGV] [PostgreSQL, versioning policy](https://www.postgresql.org/support/versioning/)
  - [PYV] [Python developer's guide, status of Python versions](https://devguide.python.org/versions/)
  - [NODE] [Node.js, previous releases](https://nodejs.org/en/about/previous-releases)
  - [DEB] [Debian releases](https://www.debian.org/releases/)

Practitioner evidence:

- [CM] Classmethod, [pnpm v11 minimumReleaseAge causes Dependabot CI failures](https://dev.classmethod.jp/en/articles/pnpm-11-minimum-release-age-dependabot-ci-failure/) (2026-07-11)
- [DC] [dependabot-core #13405](https://github.com/dependabot/dependabot-core/issues/13405): read pnpm's `minimumReleaseAge` as a cooldown (open; author said on 2026-06-01 that work had not started)
- [P11068] [pnpm #11068](https://github.com/pnpm/pnpm/issues/11068): transitive versions that break `minimumReleaseAge` (closed 2026-09-22)
- [COOL] William Woodruff, [We should all be using dependency cooldowns](https://blog.yossarian.net/2025/11/21/We-should-all-be-using-dependency-cooldowns) (2025-11-21)
- [BST] BoostSecurity, [Weaponizing Dependabot: Pwn Request at its Finest](https://labs.boostsecurity.io/articles/weaponizing-dependabot-pwn-request-at-its-finest/)
  (2025-06-01, updated 2026-01)
- [FV] Filippo Valsorda, [Turn Dependabot Off](https://words.filippo.io/dependabot/) (2026-02-20); coverage:
  [The Register](https://www.theregister.com/2026/02/24/github_dependabot_noise_machine/) (2026-02-24),
  [DevClass](https://www.devclass.com/security/2026/02/26/github-dependabot-is-a-noise-machine-and-should-be-turned-off-says-go-library-maintainer/4091858)
  (2026-02-26)

Null results: GitHub's ecosystem table names no pnpm version above 10 and no uv version above 0.11, and no
GitHub announcement of support for either was found; Cargo has no stable release-age setting. [OPT] does not say whether the
`ignore` option's `update-types` applies to Docker; it works there (see rule 15).

## Rules

1. **Version updates on, monthly, grouped, with a 7-day cooldown and an open-PR limit** (template below; decision,
   2026-11-06). Minor and patch updates share one PR per ecosystem [OPR]; a major update gets its own PR (Dependabot ignores a
   language runtime's new language version, that is Node majors and Python 3.x minors such as 3.14 to 3.15, a database's
   major and a base image's major; each is planned instead, rule 15). Cooldown: Dependabot's own default is 3 days [OPT],
   [CHG]; we set `default-days: 7`, the standard's cooldown and [COOL]'s figure, and keep it with a monthly run because
   a release made on the 30th is only a day old on the 1st. uv's docs say to match
   `exclude-newer` with the same cooldown "to avoid ending up with pull requests where uv would not be able to lock the
   dependencies" [UVD].
2. **Security updates on, grouped per ecosystem, and still immediate** (Dependabot opens a pull request for every open alert that has a patch [DSU]). A group with `applies-to: security-updates`
   groups them; Dependabot does not group security updates with version updates [OPT]. They skip the cooldown ("The
   `cooldown` option is only available for *version* updates, not *security* updates", read 2026-10-21) and the PR limit
   (a "separate, fixed limit of 10 open pull requests") [OPT]. **A young security fix waits (decision, 2026-11-06):** the
   `dependency-age` check keeps its pull request red until the version is 7 days old, and the daily re-run turns it
   green. Only an emergency (standard §7B.14; an actively exploited vulnerability, for example one listed in [KEV]) uses an exception, made in a separate pull request that is merged first
   (rule 10 forbids pushing to the Dependabot branch). Whether `schedule` leaves grouped security updates immediate,
   and how a group behaves when alerts arrive on different days, is checked on the first run in the first repository
   that adopts this.
3. **Dependabot opens the PR; it never merges.** Check CI on the exact head and request a maintainer's review
   (Dependabot's `reviewers` option was removed in 2025 in favour of CODEOWNERS [REV]); a maintainer merges it as
   standard §6.13 says.
4. **Tools check the whole diff (decision, 2026-11-06; standard §7B.13).** Dependabot's cooldown applies to the
   dependency it updates, not to the transitive versions resolved with it [CM], so the `dependency-age` workflow
   checks everything a pull request adds (section "The dependency-age workflow"). **Until a repository adopts that
   workflow, this rule and rule 13 stay in force as before:** before asking for approval, check that every
   new lockfile version is at least 7 days old, or is a recorded security exception that names the advisory.
5. **A routine upgrade by hand covers only what Dependabot cannot:**
   - pnpm 11 and 12 lockfiles: [ECO] lists pnpm "v7, v8, v9, v10". Practitioners report Dependabot PRs on pnpm 11
     [CM]; try it, and hand a failing ecosystem to the by-hand routine. A plain npm project moves to pnpm when its
     repository adopts the `dependency-age` workflow (decision, 2026-11-06), so its versions get pnpm's age check.
   - uv: [ECO] lists "v0.11"; uv's docs say "some use cases ... are not yet working" [UVD]. Same approach. An exact
     `required-version = "==X"` in `[tool.uv]` stops Dependabot's own uv, which is newer than a pinned one
     (`tool_version_not_supported`). Practitioners fix it with a range and keep CI's exact pin. Write `required-version`
     as a range whose floor is no higher than the uv that a Dependabot run's log names and whose ceiling stays above it
     as Dependabot's uv advances, keep CI's exact pin and `--locked` (reproducible builds), and keep the pin inside the
     range.
   - Pins Dependabot does not read: tool versions inside `run:` lines, `.python-version` and `.node-version` files,
     digests in scripts.
   - Security fixes for Docker, Docker Compose and Bun: [ECO] lists no security updates for them.
6. **Keep pnpm's own age check strict.** With `minimumReleaseAge` set, pnpm fails rather than install a too-new
   transitive version, so a Dependabot PR can fail CI until that version is 7 days old [CM]. That is the check working:
   the daily re-run (below) turns it green once the version is old enough. Do not switch to `minimumReleaseAgeStrict: false`, which lets pnpm write
   exclusions for too-new versions itself [P11068], [PNPM].
7. **Cost:** Dependabot's jobs on standard GitHub-hosted runners do not count toward Actions minutes [ACT]. The PR's
   own CI runs where the repository's CI always runs. Dependabot on self-hosted runners "will not run on public
   repositories" [ACT]; we do not use it there.
8. **Never trust the Dependabot identity.** No workflow approves, merges or grants anything because the actor or the
   author is `dependabot[bot]`: `github.actor` "refers to the user who caused the latest event that triggered the
   workflow", so an attacker can make it read `dependabot[bot]` [BST]. No `pull_request_target`. Never put a branch
   name or another PR field into a `run:` step; pass it through `env:` (a branch named `$(id)` runs `id` [BST]).
   zizmor reports all three (`bot-conditions`, `dangerous-triggers`, `template-injection`) [ZIZ], and poutine has a
   Confused Deputy Auto-Merge rule [BST]; standard §7B.7 already runs zizmor. Where a step must be skipped for
   Dependabot PRs, the condition reads `github.event.pull_request.user.login`, not `github.actor` [ZIZ].
9. **An approval counts only after Dependabot's last push**, so every `@dependabot rebase` or `recreate` needs a
   fresh approval.
10. **To bring a PR up to date, comment `@dependabot rebase`** [CMD]; never push to a `dependabot/*` branch
    (extra commits also stop Dependabot rebasing the PR [CMD]). Then CI runs on the new head, then approval is asked.
    Dependabot's own update commits are the only non-human authored commits the standard allows (standard §6.15).
11. **Dependabot runs get a read-only `GITHUB_TOKEN` and only Dependabot secrets** ("the only secrets available to the
    workflow are Dependabot secrets" [TRB]). When a repository adopts Dependabot, check each workflow: give
    a step the minimum Dependabot secret it needs, or skip it for Dependabot PRs (rule 8's condition), with the reason
    recorded in the workflow.
12. **Noise:** [FV] calls Dependabot "a noise machine" whose alerts flag code an application never reaches; the
    coverage reports thousands of PRs against unaffected repositories. Monthly runs, grouping, the cooldown and the PR
    limit stay. Triage every security alert before treating it as urgent: does our code use the affected
    package, module or function? Record the finding in the PR, or, when the code is not used, propose dismissal to
    a maintainer with GitHub's `not_used` reason [ALR].
13. **Known gap: no cooldown for some registries.** Dependabot dates a release from its registry, and for some it has
    no source: an update run's log says "No verified registry publication date source for quay.io; skipping
    cooldown for <image>", and the same for ghcr.io; Docker Hub tags honour the
    cooldown ("Skipping tag ... due to cooldown period"). **An image-age check closes it (standard §7B.13):** it reads
    the image's own build date, which the registry returns for MCR, ghcr, Docker Hub and quay alike (section "What
    was run"). **Until a repository adopts the `dependency-age` workflow,** for an image from a registry Dependabot
    cannot date, check by hand that the release is at least 7 days old before asking for approval: the
    release date on the project's own release page, and the image's creation date
    (`docker buildx imagetools inspect <image>:<tag> --format '{{json .Image}}'` prints `created` per platform), and
    say both in the request.
14. **A pin Dependabot updates is written once.** Dependabot changes the one line it reads. A test, installer, tag or
    document that repeats the version fails or goes stale on every bump (for example, a test that greps a log for the old version string). Every other place reads the version from that line
    or names its file, and a check fails on a copy.

15. **Runtimes, databases and base images run only supported versions (decision, 2026-10-26; standard §7B.12).**
    - Dependabot proposes their minor and patch updates only. Their majors are ignored (`ignore` with
      `update-types: ["version-update:semver-major"]`, the Dependabot name of the image as `dependency-name`), and a
      major is a planned pull request that moves every pin of the image together: a Dockerfile, a compose file, a test
      image and a script. For Python the feature release is the unit of support, which semver calls a minor (3.13 to
      3.14), so its minors are ignored too.
    - **Why:** a version outside its support window gets no fixes, and a major of a database can leave the data behind.
      For example, a database image bumped by one major version passes CI when the test database is created fresh, and
      then fails to start on an existing data directory; PostgreSQL says a major upgrade needs a dump and reload or
      `pg_upgrade` [PGV].
    - **Never ignore a patch or a digest refresh.** For a digest-pinned image they are the only way the pin is kept
      current (Docker has no security updates on GitHub, rule 5). An ignore rule lists `update-types` within the table's
      "Ignored" column and no `versions`.
    - **Each ecosystem that reads the image needs the rule.** A Dockerfile image can be read by the `docker` ecosystem
      while only `docker-compose` ignores its major, and Dependabot then proposes the next major. Keep a check that derives
      which entry reads which image and fails on a missing ignore, and on an image nobody has classified as held or not.
      The check compares this table with its own list, so the table cannot go stale.
    - **Confirm it for Docker.** [OPT] documents `update-types` in general but does not say whether it applies to Docker
      images; confirm it in your own update job's log, and use the dependency name exactly as the log shows it.
    - **Pins Dependabot cannot read** (image pins in a JSON file, `.python-version`, scripts) follow the same rule by the
      by-hand routine (rule 5).

## Runtime versions

The table of rule 15. `Ignored` is the update types the repository's Dependabot entries ignore for the image. "Support"
is the project's own rule, from its page (read 2026-10-26); check the page, not this table, for a date.

| Dependabot name | Ignored | Support |
|---|---|---|
| `debian` | major | Each release gets five years: three of full support, then two of Long Term Support [DEB]. |
| `node` | major | Even-numbered lines become Active LTS after six months as Current and odd-numbered lines are unsupported after six months; production uses Active or Maintenance LTS. From Node 27 every major reaches LTS, so read the schedule when a line is chosen [NODE]. |
| `postgres` | major | Each major is supported for five years; minors are bug and security fixes only; a major upgrade needs a dump and reload or `pg_upgrade` [PGV]. |
| `python` | major, minor | Each feature release (3.N) is supported for five years [PYV]. |

Not held (a major is its own reviewed pull request): the images that are not runtimes, databases or base images (a
reverse proxy, a monitoring tool, a mail catcher). A repository lists them so a new image is a decision.

## What was run (2026-11-06)

Each in a scratch folder outside every repository, with pnpm 11.27.1 and uv 0.13.7.

- **pnpm:** a lockfile holding `vite 8.3.6` (published the day before) and, through `normalize-package-data`, `semver 7.8.6`
  (four days old). With `minimumReleaseAge: 10080` and `minimumReleaseAgeStrict: true`, a clean
  `pnpm install --frozen-lockfile` exits 1 with `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION` naming both; with the direct
  one removed it still names `semver`; with age 0 it exits 0. `pnpm install --frozen-lockfile --lockfile-only` runs the
  same check and installs nothing. `minimumReleaseAgeExclude: [semver@7.8.6]` passes it, `semver@7.8.5` does not.
- **uv:** with `exclude-newer = "7 days"`, a lock made under the policy passes `uv lock --check` and
  `uv sync --locked`. A lock made with a newer cutoff (so a 5-day-old `anyio` is locked) fails both with exit 1
  ("Resolving despite existing lockfile due to addition of exclude newer span `P7D`"). `uv sync --frozen` exits 0 for
  that lock, so CI never uses it for this. **A lock whose `[options]` block is edited to claim the policy passes**
  both checks with the young version inside (the gap below). `exclude-newer-package = { anyio = false }` is accepted.
- **Images:** `docker buildx imagetools inspect <image> --format '{{json .Image}}'` returns `created` per platform [IMG]
  for MCR, ghcr, Docker Hub and quay, for a tag or a digest, and for a single manifest or an index. A reproducible-build
  image returns `1970-01-01T00:00:00Z` on every platform, which an age check must treat as unknown.

## The dependency-age workflow

Standard §7B.13 says what it enforces. A repository builds the workflow and the daily re-run when it adopts the rule;
this section is the design they follow.

| Pin | Enforced by | Notes |
|---|---|---|
| pnpm lockfile | `minimumReleaseAge` in `pnpm-workspace.yaml`; `pnpm install --frozen-lockfile --lockfile-only` | direct and transitive entries |
| uv lockfile | `exclude-newer = "7 days"`; `uv lock --check` | never `uv sync --frozen` |
| Actions, Cargo | Dependabot cooldown | Cargo has no stable release-age setting [CARGO] |
| Images | the image config's `created` date, below | no package manager checks it |

- **One workflow, `dependency-age`,** holds these steps and nothing else, so a re-run repeats nothing but the age check.
  `pull_request` trigger only, `contents: read`, a job timeout, and checkout with `fetch-depth: 0` and
  `persist-credentials: false` (an image check needs the merge base).
- **Checking an image's age.** `docker buildx imagetools inspect <image>@<digest> --format '{{json .Image}}'` prints the
  image config, including `created` for every platform [IMG]; the newest platform counts. The check lists the image
  references the head has and the merge base does not (`name@<digest>` in any text file, and the images a Dockerfile
  names in `FROM` or `COPY --from`, skipping build stage names and `scratch`), and fails for an image younger than 7
  days, a missing or pre-1990 date, or a registry that does not answer. It needs git and Docker with buildx.
- **Exceptions** for images: an entry naming the image reference, a reason that names a CVE, a GHSA id or an advisory URL,
  and an end date at most 30 days ahead, in a file read from the head so it is in the diff a maintainer approves. An
  entry that matches no added image is reported so it gets removed. For pnpm and uv the exception is the tool's own
  setting, with the same CVE or advisory in a comment: `minimumReleaseAgeExclude: [name@version]`, or
  `exclude-newer-package = { name = false }` ([PNPM], [UVS]).
- **Daily re-run:** a scheduled workflow lists open pull requests whose `pull_request.user.login` is `dependabot[bot]`
  (rule 8) and re-runs only the failed `dependency-age` run of each. It needs `actions: write` and
  `pull-requests: read`.
- **Gaps accepted (decision, 2026-11-06):**
  - A `uv.lock` whose `[options]` block was edited by hand to claim the policy passes with a young version inside.
    Only a deliberate edit does that; Dependabot's uv follows `pyproject.toml` [UVD].
  - GitHub Actions are covered only by the cooldown: a SHA bump made by hand, and pins inside
    `run:` lines, are unchecked. The same holds for Cargo.
  - An image's `created` time is set by its builder. It can be forged or predate the push, so the check guards against
    freshness, not malice. A reproducible-build image (1970) fails and needs an exception. `FROM ${VARIABLE}` is not
    resolved, and an image named by tag only in a compose or JSON file is not read (only digest pins are, there).
  - A monthly refresh of a tag that is rebuilt daily can be under 7 days old; its pull request stays red until it ages,
    and the daily re-run turns it green.
  - Rules 4 and 13 stay as by-hand checks until a repository adopts the workflow.
- **Checked during a repository's adoption:** that a re-run of a Dependabot-triggered run keeps its read-only
  token and Dependabot secrets (not verified here); and that the runner has Docker with buildx and reaches the
  registries, and Docker Hub's anonymous rate limit.

## Template

Copy to `.github/dependabot.yml` and keep only the ecosystems the repository uses (a plain npm project moves to pnpm first, rule 5). For several manifests, replace
`directory` with `directories: ["/", "/frontend"]`. Add `docker-compose` in the same shape as `docker` where compose
files pin images. The comments name no internal rules, so any repository copies it as is.

```yaml
version: 2

updates:
  # npm, pnpm and yarn all use the "npm" ecosystem.
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: monthly
    cooldown:
      default-days: 7 # must match pnpm minimumReleaseAge (10080 minutes)
    groups:
      npm-minor-and-patch:
        applies-to: version-updates
        patterns: ["*"]
        update-types: ["minor", "patch"]
      npm-security:
        applies-to: security-updates
        patterns: ["*"]
    open-pull-requests-limit: 3

  - package-ecosystem: uv
    directory: /
    schedule:
      interval: monthly
    cooldown:
      default-days: 7 # must match uv exclude-newer = "7 days"
    groups:
      uv-minor-and-patch:
        applies-to: version-updates
        patterns: ["*"]
        update-types: ["minor", "patch"]
      uv-security:
        applies-to: security-updates
        patterns: ["*"]
    open-pull-requests-limit: 3

  - package-ecosystem: cargo
    directory: /
    schedule:
      interval: monthly
    cooldown:
      default-days: 7
    groups:
      cargo-minor-and-patch:
        applies-to: version-updates
        patterns: ["*"]
        update-types: ["minor", "patch"]
      cargo-security:
        applies-to: security-updates
        patterns: ["*"]
    open-pull-requests-limit: 3

  # Updates the channel in rust-toolchain.toml.
  - package-ecosystem: rust-toolchain
    directory: /
    schedule:
      interval: monthly
    cooldown:
      default-days: 7
    open-pull-requests-limit: 1

  # A runtime, database or base image is a held image (rule 15): list its majors under `ignore`, in every
  # docker and docker-compose entry that reads it. Python also ignores "version-update:semver-minor".
  # GitHub offers no security updates for Docker, so there is no security group here (rule 5).
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: monthly
    cooldown:
      default-days: 7
    groups:
      docker-minor-and-patch:
        applies-to: version-updates
        patterns: ["*"]
        update-types: ["minor", "patch"]
    ignore:
      - dependency-name: node
        update-types: ["version-update:semver-major"]
      - dependency-name: python
        update-types: ["version-update:semver-major", "version-update:semver-minor"]
    open-pull-requests-limit: 3

  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: monthly
    cooldown:
      default-days: 7
    groups:
      github-actions-minor-and-patch:
        applies-to: version-updates
        patterns: ["*"]
        update-types: ["minor", "patch"]
      github-actions-security:
        applies-to: security-updates
        patterns: ["*"]
    open-pull-requests-limit: 3
```

Checked 2026-11-06 against the Dependabot schema with `check-jsonschema --builtin-schema vendor.dependabot` (0.39.0); the same file with `security-update` for `security-updates` fails it. Whether GitHub accepts each ecosystem is only shown by its first run in a repository.

## Settled practice and where practitioners disagree

Settled: grouping version updates to cut PR noise [OPT]; a cooldown on version updates and none on security updates
[OPT], [COOL]; Dependabot jobs not billed as Actions minutes [ACT].

Disputed, and what we chose:

- **Cooldown length.** Dependabot defaults to 3 days [OPT]; [COOL] finds 7 days stops most attacks and 14 days all
  but one. We use 7, the standard's cooldown everywhere.
- **Cooldowns versus pnpm's age check.** [CM] lists turning the check off or relaxing it as fixes; [DC] asks
  Dependabot to read pnpm's setting instead. We keep the check strict and re-run (rule 6).
- **Update cadence.** Weekly grouped runs were the first choice; monthly was chosen on 2026-11-06 so that many
  repositories produce few pull requests. The cost is that a base image's non-urgent patch (GitHub offers no security
  updates for Docker, rule 5) can wait about five weeks; an actively exploited one does not (standard §7B.14).
- **Tools for the 7-day rule.** A tool that checks lockfile ages must be judged before it is adopted: the age of its
  repository and of its releases, how many maintainers it has, whether its commits and tags are signed, whether its
  package metadata matches its repository, and whether it reads the pins that matter here (container images among them).
  Package managers' own settings and Dependabot's cooldown already cover most pins, so only a tool that closes a real gap
  is worth the new dependency; a repository checks image ages itself because no package manager does.
- **Dependabot at all.** [FV] turns it off for a scheduled reachability scan (govulncheck, for Go) and a CI job that
  tests against the latest versions. We keep it and add the triage step (rule 12): a check of how
  the code uses the affected package before acting on an alert.

## Decisions

| Date | Decision | Where |
|---|---|---|
| 2026-11-06 | Version updates monthly; minor and patch grouped per ecosystem; security updates grouped per ecosystem and immediate; a young security fix waits for the 7-day age; the 7-day rule is checked by tools (package-manager settings, Dependabot's cooldown, an image-age check) in a `dependency-age` workflow, with a daily re-run on Dependabot pull requests; an actively exploited vulnerability in a runtime, base image or OS is patched at once; a plain npm project moves to pnpm when its repository adopts this. | standard §7B.1, §7B.13, §7B.14; rules 1, 2, 4, 13 |
