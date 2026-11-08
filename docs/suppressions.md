# Lint suppressions

One policy for suppressing a lint or type-check finding in code, for Python, TypeScript/JavaScript and Rust, adopted
by standard §3.2 and linked from [python.md](python.md), [frontend.md](frontend.md) and [rust.md](rust.md).
Researched 2026-10-21.

## Sources (read 2026-10-21)

Primary:

- [RUFF] ruff: [error suppression](https://docs.astral.sh/ruff/linter/#error-suppression),
  [RUF100 unused-noqa](https://docs.astral.sh/ruff/rules/unused-noqa/), [PGH004 blanket-noqa](https://docs.astral.sh/ruff/rules/blanket-noqa/)
- [MYPY] mypy: [error codes](https://mypy.readthedocs.io/en/stable/error_codes.html),
  [configuration](https://mypy.readthedocs.io/en/stable/config_file.html) (`warn_unused_ignores` is part of `--strict`)
- [BIO] Biome: [suppressions](https://biomejs.dev/analyzer/suppressions/)
- [ESL] ESLint: [disable comments and descriptions](https://eslint.org/docs/latest/use/configure/rules)
- [OXC] Oxlint: [ignore comments](https://oxc.rs/docs/guide/usage/linter/ignore-comments.html)
- [TS] TypeScript 3.9: [`@ts-expect-error`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html)
- [REF] Rust reference: [lint attributes](https://doc.rust-lang.org/reference/attributes/diagnostics.html) (`expect`,
  `reason`); Clippy [lint list](https://clippy.rust-lang.org/master/index.html) (`allow_attributes`)

Practitioner evidence:

- [PDT] pydevtools, [How to suppress a Ruff warning on one line](https://pydevtools.com/handbook/how-to/how-to-suppress-a-ruff-warning-on-one-line/)
  (updated 2026-09-15): a bare `# noqa` "suppresses every rule on the line, including rules that start firing there
  later"; name the code so a dead one is reported.
- [THAI] thai-lint, [lazy ignores linter](https://thai-lint.readthedocs.io/en/latest/lazy-ignores-linter/):
  "Justifications explain WHY, not WHAT"; an inline reason of at least 10 characters.

Compared and not adopted (standard §1.6): thai-lint itself, which declares suppressions in file headers, adds a
dependency and does not cover Rust. Null results: no tool requires a reason on ruff, mypy, ESLint or Oxlint comments
(Biome does), and none lists suppressions for review, so the check script below does both.

## Rules

A suppression in code is allowed only when all four hold:

1. **It names exactly one rule.** No blanket, file-level or range form.
2. **It gives the reason on the same line**: why the rule does not apply here, not what the rule says, in at least 10
   characters [THAI].
3. **It fails when it goes stale**, so a suppression cannot outlive its cause.
4. **It is listed in `.suppressions`**, one committed file per repository: each suppression as `path: comment`,
   sorted, duplicates kept, no line numbers. CI regenerates the listing and fails on any difference, so a new,
   changed, swapped or duplicated suppression always changes `.suppressions` in the same pull request, where a
   maintainer approves it. The PR description lists every line it adds (standard §6.10). Where the repository has a
   CODEOWNERS file, it names the maintainers for `.suppressions`.

Config ignores (`per-file-ignores`, Biome `overrides`, ESLint `files` blocks, `[workspace.lints]`) remain only for
whole categories of files, each with a reason (for example: tests assert, so `S101` is off in `tests/`), and for the
"pre-standard code" lists of a repository adopting the standard, which only shrink.

| Tool | Allowed form | Stale check (verified) | Refused |
|---|---|---|---|
| ruff | `# noqa: CODE  # reason` | `RUF100` [RUFF] | bare `# noqa` (also `PGH004`), several codes, `# ruff: noqa` (any form), `# ruff: disable` |
| mypy | `# type: ignore[code]  # reason` | `unused-ignore` (`--strict`) [MYPY] | no code (also `ignore-without-code`), several codes, `# mypy:`, `# pyright:` |
| Biome | `// biome-ignore lint/<group>/<rule>: reason` | "Suppression comment has no effect" [BIO] | `biome-ignore lint:` with no rule, `biome-ignore-all`, `-start`/`-end`, `biome-ignore format` |
| ESLint | `// eslint-disable-next-line <rule> -- reason` | `reportUnusedDisableDirectives: "error"` [ESL] | `/* eslint-disable */`, `-line`, several rules, no reason |
| Oxlint | `// oxlint-disable-next-line <rule> -- reason` | `--report-unused-disable-directives` [OXC] | as ESLint |
| TypeScript | `// @ts-expect-error -- reason` | "Unused '@ts-expect-error' directive" [TS] | `@ts-ignore`, `@ts-nocheck` |
| Rust | `#[expect(one_lint, reason = "...")]` | `unfulfilled_lint_expectations` [REF] | `#[allow]`, inner `#![allow]`/`#![expect]`, `cfg_attr(..., allow(...))`, several lints |

Formatter ignores (`prettier-ignore`, `biome-ignore format`) name no rule, so they are refused; reformat the code
instead. ruff and mypy accept the trailing `# reason` but do not require it; Biome requires a reason ("Reason is
missing and can't be empty"); Clippy's `allow_attributes` does not check inner attributes [REF]. The script covers
each gap.

## Check script

Copy to `scripts/check-suppressions.sh` and run it in CI; commit `.suppressions`, empty if there are none. It needs
`git`, POSIX `sh` and `perl`; perl reads each Rust file whole because rustfmt splits long attributes over lines.

```sh
#!/bin/sh
# Every lint suppression names one rule and gives a reason of 10 or more characters, and
# .suppressions lists each one (path: comment, sorted, duplicates kept). A new or changed
# suppression therefore changes .suppressions in the same pull request.
set -eu
export LC_ALL=C
found=$(mktemp)
trap 'rm -f "$found"' EXIT

git ls-files -z -- '*.py' '*.pyi' '*.ts' '*.tsx' '*.js' '*.jsx' '*.mjs' '*.cjs' '*.mts' '*.cts' \
  '*.astro' '*.vue' '*.svelte' '*.rs' | xargs -0 -r perl -e '
my $bad = 0;
my $why = qr/\S.{9,}/;    # the reason: 10 or more characters
sub refuse { my ($p, $n, $c) = @_; warn "$p:$n: refused: $c\n"; $bad = 1 }
for my $p (@ARGV) {
  open my $fh, "<", $p or die "$p: $!\n";
  my $text = do { local $/; <$fh> };
  if ($p =~ /\.rs$/) {
    # Attributes may span lines (rustfmt splits long ones), so read the whole file.
    while ($text =~ /#(!?)\[((?:[^\]"]|"(?:[^"\\]|\\.)*")*)\]/g) {
      my ($inner, $body, $at) = ($1, $2, $-[0]);
      next unless $body =~ /\b(?:allow|expect)\s*\(/;
      my $n = 1 + (substr($text, 0, $at) =~ tr/\n//);
      (my $flat = $body) =~ s/\s+/ /g;
      if (!$inner && $flat =~ /^ ?expect\( ?([a-z_]+(?:::[a-z_]+)?) ?, ?reason ?= ?"((?:[^"\\]|\\.){10,})" ?,? ?\) ?$/) {
        print "$p: #[expect($1, reason = \"$2\")]\n";
      } else { refuse($p, $n, "#$inner\[$flat\]") }
    }
    next;
  }
  my $n = 0;
  for my $line (split /\n/, $text) {
    $n++;
    if ($p =~ /\.pyi?$/) {
      next unless $line =~ /(#\s*(?:noqa|ruff\s*:|type\s*:\s*ignore|mypy\s*:|pyright\s*:).*)$/;
      my $c = $1;
      if ($c =~ /^#\s*noqa:\s*[A-Z]+[0-9]+\s+#\s+$why$/ || $c =~ /^#\s*type:\s*ignore\[[a-z-]+\]\s+#\s+$why$/) {
        print "$p: $c\n";
      } else { refuse($p, $n, $c) }
    } else {
      next unless $line =~ /((?:\/\/|\/\*|<!--)\s*(?:biome-ignore|(?:eslint|oxlint)-(?:disable|enable)|prettier-ignore|\@ts-(?:ignore|nocheck|expect-error)).*)$/;
      (my $c = $1) =~ s/\s*(?:\*\/\}?|-->)\s*$//;
      if ($c =~ /^(?:\/\/|\/\*|<!--)\s*(?:biome-ignore lint\/[A-Za-z0-9]+\/[A-Za-z0-9]+: $why|(?:eslint|oxlint)-disable-next-line [\w\@\/.-]+ -- $why|\@ts-expect-error -- $why)$/) {
        print "$p: $c\n";
      } else { refuse($p, $n, $c) }
    }
  }
}
exit $bad;
' > "$found"

if ! sort "$found" | diff -u .suppressions -; then
  echo "check-suppressions: .suppressions does not match the code (diff above)" >&2
  exit 1
fi
```

Verified 2026-10-21 on the Python, TypeScript (Biome and Oxlint; ESLint) and Rust sample projects of the language
pages. Passes: no suppressions with an empty listing; one specific suppression with a reason once listed, including a
JSX comment and a Rust `#[expect]` that rustfmt split over four lines. Fails: the same suppression unlisted; a second
identical one in the same file; a changed reason; and every refused form in the table, each reported with its file
and line. Each tool's stale check above was shown to fail on a stale suppression.

## Settled practice and where practitioners disagree

Settled: name the rule instead of a bare suppression, and let the tool report a dead one [PDT], [RUFF];
`@ts-expect-error` over `@ts-ignore` where a fix is expected [TS]; `#[expect]` over `#[allow]` [REF].

Disputed, and what we chose:

- **Inline suppressions at all.** This standard first refused them outright; practitioners name the code and justify
  it [PDT], [THAI]. A total ban pushes exceptions into whole-file config, which hides more than one justified line. We
  allow one rule per line, with a reason and maintainer approval.
- **Approval by count or by listing.** A count misses a swap (one removed, one added). We list each suppression.
- **Where the reason goes.** thai-lint prefers a file-header declaration [THAI]; we keep it on the line, where the
  tool's own syntax puts it.
