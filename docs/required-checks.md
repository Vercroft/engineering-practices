# Required checks

The job and its test behind standard §4.6. Read 2026-11-18.

## Sources

- [NEEDS] GitHub Docs, [`jobs.<job_id>.needs`](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idneeds):
  "If a job fails or is skipped, all jobs that need it are skipped unless the jobs use a conditional expression".
- [CTXT] GitHub Docs, [`needs` context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#needs-context):
  `needs.<job_id>.result` "Possible values are `success`, `failure`, `cancelled`, or `skipped`."
- [EXP] GitHub Docs, [status check functions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions):
  `always()` "returns `true`, even when canceled"; "Avoid using `always` for any task that could suffer from a critical
  failure", with `!cancelled()` as the alternative.
- [TRB] GitHub Docs, [Troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks):
  "Successful check statuses are `success`, `skipped`, and `neutral`."; for a job that depends on a failed job: "Use
  `always()` with `needs` for required checks that depend on other jobs."
- [BILL] GitHub Docs, [Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing):
  "GitHub rounds the minutes and partial minutes each job uses up to the nearest whole minute."
- [PC] pre-commit, [docs](https://pre-commit.com/): in CI, "adding `pre-commit run --all-files` as a CI step";
  `fail_fast` "(optional: default `false`)"; `unsupported` is "_new in 4.4.0_: previously `language: system`"; the
  `manual` stage "will not be automatically triggered by any `git` hook"; "The `SKIP` environment variable is a comma
  separated list of hook ids."; `default_install_hook_types` "(optional: default [pre-commit]) a list of --hook-types
  which will be used by default when running pre-commit install"; commit-msg "hooks will be passed a single filename";
  pre-push sets `PRE_COMMIT_TO_REF`, "the local revision that is being pushed to the remote" (read 2026-11-25).
- [PCSRC] pre-commit 4.7.0, [`hook_impl.py`](https://github.com/pre-commit/pre-commit/blob/v4.7.0/pre_commit/commands/hook_impl.py)
  (read 2026-11-25): `_pre_push_ns` returns at the first pushed ref with new commits, so later refs of the same push are
  not checked; when the push includes the root commit it sets `all_files=True` and no `to_ref`.
- [GL] gitleaks v8.30.1, [README](https://github.com/gitleaks/gitleaks/blob/v8.30.1/README.md#git) and
  [`sources/git.go`](https://github.com/gitleaks/gitleaks/blob/v8.30.1/sources/git.go) (read 2026-11-25): "You can
  configure the behavior of `git log -p` with the `log-opts` option"; the flag is `--log-opts string   git log
  options`; without it gitleaks runs `git log -p -U0 --full-history --all --diff-filter=tuxdb`, with it
  `git log -p -U0` followed by the given options.
- [GITH] Git, [githooks](https://git-scm.com/docs/githooks) (read 2026-11-25): pre-push "can be used to prevent a push
  from taking place"; "If this hook exits with a non-zero status, git push will abort without pushing anything";
  `commit-msg` "can be bypassed with the --no-verify option", and `git push` takes `--no-verify` too.
- [DEV] Camille Hodoul, [Pre-commit, pre-push or pre-merge ?](https://dev.to/camillehdl/pre-commit-pre-push-or-pre-merge-8i9)
  (read 2026-11-25), practitioner: "The slower the task, the later and less often it should run"; pre-push for "less
  than 10 seconds", pre-merge (CI) above.
- [TW] Thoughtworks, [Pre-commit: Don’t git hooked!](https://www.thoughtworks.com/en-au/insights/blog/pre-commit-don-t-git-hooked)
  (read 2026-11-25), practitioner: "when developers feel impeded, they will find a workaround"; "you could just
  bypass the hooks altogether with --no-verify".

## Where a check lives

Each CI job costs at least a minute on a private repository [BILL] and one more entry in the gate's `needs`, so small
checks share one job.

| The check | Lives in | Example |
|---|---|---|
| Reads the repository's files; needs no service, secret or write permission; under about a minute | A hook in `.pre-commit-config.yaml`, run by the one `Repository checks` job | No em or en dashes; suppressions are listed; zizmor; REUSE lint |
| Must pass on each supported runtime version | A matrix job | scrift-js: lint, types, tests and build on Node 24 and 26 |
| Needs a service, a secret or a write permission, or takes over about a minute | Its own job | Burnbird's `Python`, with Postgres and Mailpit |
| Has another trigger, or is a shared workflow | Its own workflow | the weekly external link check; the shared secret scan |

- A step that needs the project's installed dependencies (formatter, linter, type checker, tests) stays in the job
  that installs them.
- A check that reads the pull request, not the files (a commit range, the title, an organisation variable), is a step
  in `Repository checks` after the hooks, with `if: ${{ !cancelled() }}`, so it reports even when a hook failed.
- Local hooks (`repo: local`) use `language: pygrep`, or `language: unsupported` for a tool installed from a
  hash-pinned requirements file; `unsupported` needs pre-commit 4.4.0 [PC], hence `minimum_pre_commit_version`. A
  hook for which pre-commit would install packages itself (`language: python` installs without hashes) becomes a
  local hook running the hash-pinned tool. A remote hook repository is pinned by full commit SHA with its tag in a
  comment (standard §7C.6).
- `fail_fast` stays `false`, the default, so every hook reports [PC].
- A hook that needs a tool most contributors do not have gets `stages: [manual]`; CI runs `--hook-stage manual`,
  which also runs every hook that sets no `stages`.
- CI skips the gitleaks hook (`SKIP: gitleaks`): it scans staged changes, and CI has none; the `Secret scan` check
  scans the full history.

The job. Its Python only runs the tools, so it is pinned to a version every pinned package has a wheel for, which
may trail the project's own: `--only-binary :all:` never builds from source (so never fetches an unpinned build
backend) and fails when a wheel is missing. No cache: the local hooks install nothing and gitleaks is skipped.

```yaml
  repository-checks:
    name: Repository checks
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0
        with:
          python-version: "3.14.10"
      # gitleaks scans staged changes, and CI has none; the Secret scan check scans the full history.
      - name: Run every hook
        env:
          SKIP: gitleaks
        run: |
          python -m venv "$RUNNER_TEMP/venv"
          "$RUNNER_TEMP/venv/bin/pip" install --quiet --require-hashes --only-binary :all: \
            -r .github/requirements/pre-commit.txt -r .github/requirements/zizmor.txt
          export PATH="$RUNNER_TEMP/venv/bin:$PATH"
          pre-commit run --all-files --hook-stage manual --show-diff-on-failure
```

The hooks. pygrep matches bytes, so the dash pattern is the UTF-8 of U+2013 and U+2014; a class of the characters
themselves would match their single bytes, and so also `’`. A generated lockfile is exempted with `exclude:`.

```yaml
minimum_pre_commit_version: "4.4.0"
default_language_version:
  golang: 1.27.3
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: 83d9cd684c87d95d656c1458ef04895a7f1cbd8e  # v8.30.1
    hooks:
      - id: gitleaks
        args: [--config=.gitleaks.toml]
  - repo: local
    hooks:
      - id: dashes
        name: No em or en dashes (use a hyphen, a colon or a new sentence)
        language: pygrep
        entry: '\xe2\x80[\x93\x94]'
        exclude: ^package-lock\.json$
      - id: suppressions
        name: Suppressions are listed
        language: unsupported
        entry: sh scripts/check-suppressions.sh
        pass_filenames: false
        always_run: true
      - id: zizmor
        name: zizmor
        language: unsupported
        entry: zizmor --offline .github/workflows
        files: ^\.github/workflows/
        pass_filenames: false
        stages: [manual]
```

zizmor gets the directory, as before, because its docs do not say how a single file is classified; a repository with
composite actions adds their directory to `files` and `entry`.

## The gate job

Add it last to the CI workflow, and list every other job of that file in `needs`.

```yaml
  gate-summary:
    name: Gate summary
    if: always()
    needs: [repository-checks, <every other job in this file>]
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions: {}
    steps:
      - name: Require every needed job to have passed or been skipped
        env:
          NEEDS_JSON: ${{ toJSON(needs) }}
        run: |
          python3 - <<'PY'
          import json, os, sys
          results = {job: need["result"] for job, need in json.loads(os.environ["NEEDS_JSON"]).items()}
          for job, result in sorted(results.items()):
              print(f"{job}: {result}")
          bad = sorted(f"{job}={result}" for job, result in results.items() if result not in ("success", "skipped"))
          if not results or bad:
              sys.exit("not every needed job passed or was skipped: " + (", ".join(bad) or "no jobs"))
          PY
```

`always()`, not `!cancelled()`: the gate only reads results, it must still report on a cancelled run, and its verdict
fails on `cancelled` [EXP].

## The gate test

A test in the repository's own language reads the CI workflow and fails when:

1. the gate is not named `Gate summary` or has no `if: always()`;
2. a job of the file is missing from the gate's `needs`;
3. the gate's own step, run on given results, passes a `failure`, a `cancelled` or no result;
4. a job other than the gate has an `if:` the test does not list with its reason, because a job skipped by its own
   condition counts as passed.

Example: [Burnbird's test](https://github.com/Vercroft/burnbird/blob/f0e1f3c89a2bd216d0c5ecc0433e8dde009c6313/tests/test_gate_summary.py).

## A repository without CI

Standard §4.6, read 2026-11-25. A repository with no runner runs every check its CI would run as git hooks, installed
by one `pre-commit install`. When the pre-push hook fails, "git push will abort without pushing anything" [GITH]. It
is weaker than CI: it runs on the contributor's machine, and `git push --no-verify` skips it [GITH], [TW].

- Every check CI would run runs at `pre-push`, in a clean copy of the pushed commit (a detached `git worktree`,
  standard §6.11), so a fix left uncommitted cannot make a failing commit pass. One `pushed-commit` hook runs every
  `manual`-stage hook there; CI's "Run every hook" step is the same command.
- A check that reads the commit message (dashes, standard §6.9; identities and trailers, §6.8) runs at `commit-msg`,
  whose hook "will be passed a single filename" holding the message [PC].
- `default_install_hook_types` makes `pre-commit install` install all three hook types [PC]; `default_stages` keeps
  every other hook off `pre-push`, where it would read the working tree.
- The full-history secret scan of standard §7C.6 is gitleaks' own hook a second time, at the `manual` stage, with its
  entry changed to scan the full history of the pushed commit, like CI's scan of a pull request's history:
  `--log-opts=HEAD`, because the clean copy is detached at that commit; without it gitleaks scans every local branch
  [GL]. Both gitleaks hooks take the repository's `--config=.gitleaks.toml`, as above.
- pre-commit checks only the first branch of a push that sends new commits [PCSRC], so push one branch at a time.
- `CONTRIBUTING.md` says the repository has no CI and that these hooks stand in for it.
- A scheduled check (the weekly external link check of standard §11.8) is a scheduled workflow, or a `manual` hook a
  maintainer runs on that schedule, recorded as an exception in `docs/decisions/`. The maintainers choose.

No primary source sets this rule. Practitioners place a check by how long it takes, pre-push for "less than 10
seconds" and CI for the rest [DEV], and warn that slow hooks get skipped [TW]; here the pre-push hook is the only gate.

```yaml
minimum_pre_commit_version: "4.4.0"
default_install_hook_types: [pre-commit, pre-push, commit-msg]
default_stages: [pre-commit, manual]
default_language_version:
  golang: 1.27.3
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: 83d9cd684c87d95d656c1458ef04895a7f1cbd8e  # v8.30.1
    hooks:
      - id: gitleaks
        args: [--config=.gitleaks.toml]
      - id: gitleaks
        alias: gitleaks-history
        name: Secret scan of the full history
        entry: gitleaks git --redact --verbose --log-opts=HEAD
        args: [--config=.gitleaks.toml]
        stages: [manual]
  - repo: local
    hooks:
      - id: dashes
        name: No em or en dashes
        language: pygrep
        entry: '\xe2\x80[\x93\x94]'
        stages: [pre-commit, commit-msg, manual]
      # A push that includes the root commit gets no PRE_COMMIT_TO_REF [PCSRC], so the pushed branch is used.
      - id: pushed-commit
        name: Every check, on a clean copy of the pushed commit
        language: unsupported
        entry: >-
          sh -c 'set -eu; dir=$(mktemp -d);
          trap "git worktree remove --force \"$dir\"" EXIT;
          git worktree add --quiet --detach "$dir" "${PRE_COMMIT_TO_REF:-$PRE_COMMIT_LOCAL_BRANCH}";
          cd "$dir"; pre-commit run --all-files --hook-stage manual'
        pass_filenames: false
        always_run: true
        stages: [pre-push]
```
