# Size each commit and count only lines that need review

Date: 2026-11-25
Status: accepted

## Context

Standard §6.14 sized a pull request by every changed line: about 100 was a good size and 1000 usually too large. Two
facts make that count the wrong thing. Review quality depends on how much a reviewer reads at once, and a pull request
made of atomic commits is read commit by commit, so the commit is the unit that matters. And a lock file, other
generated file or block of moved text is not read line by line, so counting it overstates the work.

## Decision

We will count only lines that need review: lock files, other generated files and lines that `git diff --color-moved`
shows as only moved are not counted. Each commit is one logical change that reverts cleanly on its own, ideally under
about 400 such lines. A pull request is about 1000 such lines at most, except that a repository with a single
maintainer may hold several such commits, up to about 2000 such lines. A change to secrets, security guards or
deployment stays its own small pull request. The rule is in standard §6.14, which keeps its link to Google's small-CLs
guide.

Sources, each confirmed in its page text on 2026-11-25:

- SmartBear, [best practices for peer code review](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/),
  tip 1, on a study of a Cisco team: "developers should review no more than 200 to 400 lines of code (LOC) at a time".
- [arXiv:2606.15689](https://arxiv.org/pdf/2606.15689), abstract. The study tests AI code
  reviewers (five large language models) on 150 samples: 100 synthetic bugs and 50 real pull requests. Its finding:
  "Diff size is the dominant predictor, with F1 dropping from 0.657 on diffs under 10 lines to 0.043 on diffs over 150
  lines."

## Consequences

A large pull request of small, separate commits is acceptable, and a small pull request holding one huge commit is not.
The numbers are guidance ("ideally", "about"), not a hard limit, and a reviewer may ask to split any change. Only the
400 comes from a source, and only as a range: SmartBear gives 200 to 400 lines at a time. The 1000 lines for a pull
request and the 2000 for a repository with a single maintainer are this standard's own decisions, as the numbers in
[docs/documentation.md](../documentation.md) are; no source gives them. The arXiv study measured AI reviewers, not
people, so it supports only that a smaller diff is reviewed better, not any number.
