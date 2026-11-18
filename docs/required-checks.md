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

## The job

Add it last to the CI workflow, and list every other job of that file in `needs`.

```yaml
  gate-summary:
    name: Gate summary
    if: always()
    needs: [<every other job in this file>]
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

## The test

A test in the repository's own language reads the CI workflow and fails when:

1. the gate is not named `Gate summary` or has no `if: always()`;
2. a job of the file is missing from the gate's `needs`;
3. the gate's own step, run on given results, passes a `failure`, a `cancelled` or no result;
4. a job other than the gate has an `if:` the test does not list with its reason, because a job skipped by its own
   condition counts as passed.

Example: [Burnbird's test](https://github.com/Vercroft/burnbird/blob/f0e1f3c89a2bd216d0c5ecc0433e8dde009c6313/tests/test_gate_summary.py).
