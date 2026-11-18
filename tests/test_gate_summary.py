"""`Gate summary` is the one CI check the ruleset requires for ci.yml, so it must judge every other job there.

Three ways the gate could stop meaning anything each have a test (docs/required-checks.md, "The gate test"): a job
left out of its `needs` runs with nothing requiring it to pass, a verdict that accepts a failure lets every job fail
behind a green check, and an `if:` on another job could skip that job, which the gate counts as passed.

Standard library only, so the hook needs nothing installed: ci.yml is read as text.
Run: python3 -B -m unittest discover -s tests
"""

import json
import os
import re
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CI = ROOT / ".github" / "workflows" / "ci.yml"
GATE = "gate-summary"
# The only job with a condition is the gate itself.
CONDITIONS = {GATE: "always()"}

JOB = re.compile(r"^  ([a-z][a-z0-9_-]*):\n", re.MULTILINE)
VERDICT = re.compile(r"<<'PY'\n(.*?)\n *PY\n", re.DOTALL)


def _jobs() -> dict[str, str]:
    """Each job's id and the text of its block."""
    parts = JOB.split(CI.read_text().split("\njobs:\n", 1)[1])
    jobs = {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}
    assert len(jobs) > 1, f"{CI} read as {len(jobs)} job(s); its shape changed"
    return jobs


def _field(block: str, key: str) -> str | None:
    """A job-level key's value, or None."""
    match = re.search(rf"^    {key}: (.+)$", block, re.MULTILINE)
    return match[1] if match else None


def _gate() -> str:
    gate = _jobs().get(GATE)
    assert gate is not None, f"ci.yml has no `{GATE}` job; the ruleset requires its check"
    return gate


def _needs() -> list[str]:
    needs = _field(_gate(), "needs")
    assert needs is not None, f"`{GATE}` has no needs"
    assert needs.startswith("[") and needs.endswith("]"), "write the gate's needs as one [a, b] list"
    return [job.strip() for job in needs[1:-1].split(",")]


def _verdict(results: dict[str, str]) -> int:
    """Run the gate's own step, as CI does, on the needs results given."""
    match = VERDICT.search(_gate())
    assert match is not None, "the gate's verdict is no longer a python3 <<'PY' step"
    needs = {job: {"result": result, "outputs": {}} for job, result in results.items()}
    env = {**os.environ, "NEEDS_JSON": json.dumps(needs)}
    return subprocess.run(
        [sys.executable, "-I", "-c", textwrap.dedent(match[1])],
        env=env,
        timeout=30,
        check=False,
        capture_output=True,
    ).returncode


class GateSummary(unittest.TestCase):
    def test_the_gate_is_named_for_the_ruleset_and_always_runs(self) -> None:
        gate = _gate()
        self.assertEqual(_field(gate, "name"), "Gate summary", "the ruleset requires the check by this name")
        # Without always(), one failed job skips the gate, and a skipped required check is not red.
        self.assertEqual(_field(gate, "if"), "always()")

    def test_the_gate_needs_every_other_job(self) -> None:
        missing = sorted(set(_jobs()) - {GATE} - set(_needs()))
        self.assertEqual(missing, [], f"`{GATE}` does not need {missing}, so nothing requires them to pass")

    def test_only_the_gate_has_a_condition(self) -> None:
        conditions = {job: _field(block, "if") for job, block in _jobs().items()}
        self.assertEqual({job: c for job, c in conditions.items() if c is not None}, CONDITIONS)

    def test_the_gate_fails_when_any_job_did_not_pass(self) -> None:
        for bad in ("failure", "cancelled"):
            with self.subTest(bad=bad):
                results = dict.fromkeys(_needs(), "success")
                results["repository-checks"] = bad
                self.assertNotEqual(_verdict(results), 0)

    def test_the_gate_fails_when_it_judges_no_job(self) -> None:
        self.assertNotEqual(_verdict({}), 0)

    def test_the_gate_passes_when_every_job_passed_or_was_skipped(self) -> None:
        results = dict.fromkeys(_needs(), "success")
        results["secret-scan"] = "skipped"
        self.assertEqual(_verdict(results), 0)


if __name__ == "__main__":
    unittest.main()
