# Python code standard

The Python rules for every repository that adopts them, adopted by standard §3.2. Short rules, each with its source. Where a
rule is not enforced by a tool, it says so (standard §4.3). Researched 2026-10-21.

## Sources (read 2026-10-21)

Primary:

- [PEP8] [PEP 8, Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP257] [PEP 257, Docstring Conventions](https://peps.python.org/pep-0257/)
- [TYP] [Python typing documentation](https://typing.python.org/en/latest/) and the typing PEPs it builds on:
  [544](https://peps.python.org/pep-0544/) (protocols), [585](https://peps.python.org/pep-0585/) (`list[int]`),
  [591](https://peps.python.org/pep-0591/) (`Final`), [604](https://peps.python.org/pep-0604/) (`X | None`),
  [695](https://peps.python.org/pep-0695/) (`def f[T]`, `type X = ...`), [749](https://peps.python.org/pep-0749/)
  (deferred annotations, 3.14)
- [DC] [dataclasses](https://docs.python.org/3/library/dataclasses.html) ([PEP 557](https://peps.python.org/pep-0557/))
- [PUG] [Packaging User Guide: src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [PT] [pytest: Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) and
  [import mechanisms](https://docs.pytest.org/en/stable/explanation/pythonpath.html) (re-read 2026-11-13)
- [RUFF] [ruff rules](https://docs.astral.sh/ruff/rules/), [settings](https://docs.astral.sh/ruff/settings/),
  [error suppression](https://docs.astral.sh/ruff/linter/#error-suppression); `ruff check --help` (0.17.0)
- [MYPY] [mypy configuration](https://mypy.readthedocs.io/en/stable/config_file.html); `mypy --help` (2.4.0)
- [MYPYMAP] [mypy: mapping file paths to modules](https://mypy.readthedocs.io/en/stable/running_mypy.html#mapping-file-paths-to-modules)
  (2.4.1, read 2026-11-13)
- [FAPI] [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) (read 2026-11-13)
- [GSG] [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [LOG] [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [CF] [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html),
  [AIO] [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html)
- [UV] [uv settings](https://docs.astral.sh/uv/reference/settings/), [PIP] [pip: secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [RUF100] [ruff: unused-noqa (RUF100)](https://docs.astral.sh/ruff/rules/unused-noqa/)
- [PYDL] [python.org downloads](https://www.python.org/downloads/): 3.15.0 released 2026-10-09, 3.15.1 on 2026-10-21

Practitioner evidence:

- [HYN] Hynek Schlawack, [Testing & Packaging](https://hynek.me/articles/testing-packaging/) (updated 2021)
- [UV12] [uv 0.12.0 release notes](https://github.com/astral-sh/uv/releases/tag/0.12.0) (2026-07-28)
- [BLIST] James Bennett, [A Python 3.11 "gotcha"](https://www.b-list.org/weblog/2022/nov/08/python-311-gotcha/)
  (2022-11-08): "I usually wait until the first bugfix release ... before seriously considering an upgrade"
- [PYSPEED] Itamar Turner-Trauring, [When should you upgrade to Python 3.13?](https://pythonspeed.com/articles/upgrade-python-3.13)
  (updated 2024-12-05): wait until "All your libraries" and "All the tools you rely on" explicitly support it
- [SWC] Jack Diederich, [Stop Writing Classes](https://us.pycon.org/2012/schedule/presentation/352/), PyCon US 2012
- [COOL] William Woodruff, [We should all be using dependency cooldowns](https://blog.yossarian.net/2025/11/21/We-should-all-be-using-dependency-cooldowns) (2025-11-21)
- [PATH] discuss.python.org: [pathlib and os.path parity](https://discuss.python.org/t/pathlib-and-os-path-feature-parity-and-code-de-duplication/9239),
  [making paths absolute](https://discuss.python.org/t/making-paths-absolute-in-os-path-and-pathlib/43196)
- [TC] pydevtools handbook, [How do Python type checkers compare?](https://pydevtools.com/handbook/explanation/how-do-mypy-pyright-and-ty-compare/) (2026)
- [FBP] zhanymkanov/fastapi-best-practices, [Project Structure](https://github.com/zhanymkanov/fastapi-best-practices#project-structure)
  (read 2026-11-13): grouping by file type "didn't scale well for our monolith with many domains and modules"

Null results: r/Python could not be read (the site refused automated requests); no 2025-2026 discuss.python.org thread on src
layout was found; neither ruff nor mypy requires a reason on a suppression comment (see
[suppressions.md](suppressions.md)).

## Rules

### 1. Layout and naming

```text
<repo>/
  pyproject.toml          # one per distribution; uv.lock beside it
  src/<package>/          # the import package
    __init__.py
    py.typed              # libraries only (PEP 561)
    testing/              # shared test helpers, imported by tests
  tests/
    conftest.py           # fixtures
    test_<module>.py
```

1. **src layout** for every package, library or application. [PUG]: it "helps prevent accidental usage of the
   in-development copy of the code"; [PT]: tests then run against the installed package. [UV12]: `uv init` makes this
   the default since 0.12.0.
2. **Tests in `tests/`** at the repository root, named `test_<module>.py`, run with `--import-mode=importlib`, which
   [PT] recommends "for new projects".
3. **Shared test helpers are an importable package, never a `sys.path` edit.** Under importlib mode "testing utility
   modules in the tests directories ... are not importable"; [PT] says to place them with the code, "for example
   `app.testing.helpers`". Fixtures go in `conftest.py`. If the helpers need test-only dependencies, make them a
   separate package in a uv workspace, installed as a dev dependency. `sys.path`, `PYTHONPATH` and pytest's
   `pythonpath` are not used: `uv sync` installs the project (enforced: `sys.path` is a banned API).
4. **Naming** [PEP8]: modules short, lowercase, underscores only where they help; packages short and lowercase;
   classes `CapWords`; functions and variables `snake_case`; constants `UPPER_CASE`. The distribution is
   `<product>-<component>` and the import package `<product>_<component>`, named by product, component and purpose
   (standard §3.5). Folders that are packages follow package names (enforced: `N`).
5. A single-file script run directly (for example on a production host) needs no package; every other rule still applies.
6. **Application layout: by feature** (standard §3.8). A feature with two or more modules gets its own folder;
   one-module features, shared infrastructure and settings used by several features stay at the package root, and a
   setting only one feature uses goes in that feature's folder. Each process is a thin entry module that only wires
   the features together [FAPI]. Tests mirror the feature folders. Once `tests/` has subfolders, it and each
   subfolder get an empty `__init__.py`: pytest's importlib mode accepts same-named test files in different folders
   [PT], but mypy maps files to modules through `__init__.py` files [MYPYMAP] and without them stops with
   `Duplicate module named "test_router"`. The `[tool.mypy]` block (rule 10) stays unchanged.

   ```text
   src/<package>/
     __init__.py
     web.py              # the web process: creates the app, includes each feature's router
     worker.py           # the worker process: registers each feature's jobs
     settings.py         # settings used by several features
     database.py
     models.py
     migrations/
     templates/          # server-rendered pages
     static/
     search.py           # a one-module feature stays a module
     billing/
       __init__.py
       router.py
       service.py
     auth/
       __init__.py
       config.py         # a setting only auth uses
       router.py
       service.py
   tests/
     __init__.py         # empty, once tests/ has subfolders
     test_search.py
     billing/
       __init__.py
       test_router.py
     auth/
       __init__.py
       test_router.py
   ```

### 2. Imports, constants, globals and docstrings

1. **Imports at the top**, "just after any module comments and docstrings" [PEP8], sorted (enforced: `E402`, `I`).
   Absolute imports only [PEP8], [GSG] 2.2 (enforced: `ban-relative-imports = "all"`). No wildcard imports [PEP8].
2. **Module constants at the top**, after the imports, in capitals [PEP8], annotated `Final` [TYP] so mypy refuses a
   reassignment. Constants shared by several modules live in one `constants.py` (fixed values) or `settings.py`
   (values read from the environment or files at start-up).
3. **No mutable globals.** [GSG] 2.5: "Avoid mutable global state." Constant collections are `tuple`, `frozenset` or
   `types.MappingProxyType`; state lives in an object passed to whoever needs it. (Enforced: `global` statements by
   `PLW0603`, mutable class defaults by `RUF012`; a mutated module-level list is caught only in review.)
4. **Docstrings** on every module and on every class and function a module exports [PEP257], in triple double
   quotes, with a one-line summary first (enforced: `D` with the `pep257` convention; tests are exempt).

### 3. Paths

`pathlib` only, never `os.path` (enforced: `PTH`, and `os.path` is a banned API). `os` stays for what pathlib does not
cover (`os.environ`, process calls). When porting old code, check behaviour: pathlib normalises paths and os.path
does not [PATH].

### 4. Python version and typing

1. **Products run the newest stable CPython** [PYDL] (decision, 2026-11-13). A new feature release (3.16) is adopted from its
   first bugfix release (3.16.1), once that is at least 7 days old (standard §7B.1) and the product's CI passes with
   every dependency installed from wheels (`no-build = true`), using tool versions that are themselves at least 7 days
   old. Later bugfix releases (3.16.2 and on) follow the 7-day rule alone. Why: practitioners wait for the first bugfix
   release [BLIST], and until every library and tool they rely on supports the new release [PYSPEED]. Example: 3.15.0
   was released on 2026-10-09 and 3.15.1 on 2026-10-21 [PYDL], so 3.15 was adoptable from 2026-10-28.
2. **If one dependency is not ready** (no wheel for the new version, or its tests fail), the product stays on the
   previous version and records why: a comment beside `requires-python` naming the dependency and its upstream issue.
   The upgrade routine re-checks it.
3. One version, stated everywhere it appears (`requires-python`, `.python-version`, mypy's `python_version`, the
   Docker base image), and a check that they agree.
4. **Scripts run by a system's own `python3` follow that version** and move when the system moves; their
   `requires-python` and mypy `python_version` name it. They stay standard library only (rule 8.2).
5. A published library keeps a supported range instead, since its users choose their Python.
6. **Full hints and mypy strict** on `src` and `tests` (`disallow-untyped-defs` and the rest of `--strict` [MYPY]).
7. **Current syntax for the project's minimum Python** (`requires-python`): `list[int]` (585), `X | None` (604),
   `def f[T]` and `type Alias = ...` from 3.12 (695). ruff reads the minimum from `requires-python` and rewrites old
   forms (enforced: `UP`). Do not add `from __future__ import annotations` where the minimum is 3.14: annotations are
   deferred by default there, and the import will be deprecated [PEP 749].
8. Libraries ship `py.typed` ([PEP 561](https://peps.python.org/pep-0561/)).

### 5. Classes, functions, data and interfaces

1. **A class bundles state with the behaviour that keeps it valid.** A stateless step is a module-level function;
   [GSG] 2.17: "Never use `staticmethod`" ... "Write a module-level function instead."
2. **No class that is only `__init__` plus one method**: that is a function [SWC] ("If your class only has two
   methods and one of them is init you probably meant to write a function"). Not enforced by any tool; review checks it.
3. **Data is a `dataclass`** [DC], `frozen=True, slots=True` unless it must change; `TypedDict` for dict-shaped
   external data; `Enum` for a fixed set of choices.
4. **Interfaces are `typing.Protocol`** [TYP], [PEP 544]: structural subtyping, "a static equivalent of duck typing",
   so callers and test doubles need no shared base class. Use an ABC only to share implementation.
5. No public attribute hidden behind a trivial getter and setter [GSG] 3.15; no nested function or class except to
   close over a local value [GSG] 2.6.

### 6. Errors and logging

1. **Specific exceptions.** Each package defines its own errors, derived from `Exception` [PEP8]. Chain with
   `raise ... from err` [PEP8] (enforced: `B904`).
2. **No bare `except:`** [PEP8] (enforced: `E722`). Catch `Exception` only at an isolation point (a request handler, a
   job runner) that logs it with `logger.exception` or re-raises [GSG] 2.4 (enforced: `BLE001`, which accepts those
   two cases; `S110` refuses `except: pass`).
3. **Logging** through `logger = logging.getLogger(__name__)` in each module [LOG]. Libraries add no handler but
   `NullHandler`; only the application's entry point configures logging [LOG] (enforced: `LOG`).
4. **No `print` in library code** (enforced: `T20`). A CLI's ordinary output is `print` [LOG]; its entry module gets a
   `T201` per-file ignore with that reason.

### 7. Concurrency

1. **Blocking work:** `concurrent.futures`, "a high-level interface for asynchronously executing callables" [CF]:
   `ThreadPoolExecutor` for I/O, `ProcessPoolExecutor` (or `InterpreterPoolExecutor`, 3.14) for CPU.
2. **Async I/O:** `asyncio` with `TaskGroup`, which, unlike `gather`, cancels the remaining tasks when one fails
   [AIO]; `asyncio.to_thread` for a blocking call inside async code (enforced: `ASYNC`). An established
   library (such as `anyio`) only where the framework already uses it.
3. **No hand-rolled threads** (enforced: `threading.Thread` and `_thread` are banned APIs). Pass data between workers
   through the executor's futures or a `queue.Queue` [GSG] 2.18.

### 8. Dependencies

1. **Adopt before you build** (standard §1.6), with the supply-chain rules (§7B) as uv settings [UV]:
   - 7-day cooldown: `exclude-newer = "7 days"` (uv accepts a relative duration). [COOL]: a 7-day cooldown "would have
     prevented the vast majority" of the attacks reviewed. A young security fix waits; only an emergency (§7B.14) is an exception:
     `exclude-newer-package = { <name> = false }` with the CVE or advisory ID in a comment, as §7B.13 says.
   - Lockfile committed; CI runs `uv sync --locked`. Applications pin exact versions (`==`); a published library
     declares ranges (exact pins in a library break its users) and its lockfile pins CI.
   - Wheels only: `no-build = true`. Building a source distribution runs its code [PIP]. A package with no wheel is a
     dependency decision for the maintainers (§3.4), recorded in the config with its reason.
2. **Code that runs as root on a production host is standard-library only.** Every package, and each of its dependencies, is
   code running as root; the standard library ships with the interpreter the host already trusts. Dev tools (ruff,
   mypy, pytest) are allowed: they run in CI and on workstations, never as root on a production host.

### 9. Lint suppressions

The shared policy is [suppressions.md](suppressions.md): one rule, a reason on the line, a stale check, and a line
in `.suppressions` that a maintainer approves. In Python:

1. **Allowed:** `# noqa: CODE  # reason` and `# type: ignore[code]  # reason`. Stale ones fail: `RUF100` [RUF100]
   ("likely included by mistake, and should be removed") and mypy's `unused-ignore` (`--strict`).
2. **Refused:** bare `# noqa` (also `PGH004`), several codes, any `# ruff: noqa` or `# ruff: disable`, `# type: ignore`
   without a code (also `ignore-without-code`), `# mypy:` and `# pyright:` comments, and `@no_type_check` (a banned
   API).
3. **Config ignores** (`[tool.ruff.lint.per-file-ignores]`, `[[tool.mypy.overrides]]`) only for whole categories of
   files, each with a reason (for example `tests/**`), plus the adoption list below.

### 10. Enforcement

Every repository copies this block into `pyproject.toml` unchanged, except `python_version` (rule 4) and the
per-file ignores it needs. It carries no internal names, so public repositories copy it as is.
Verified 2026-10-21 on a sample project with ruff 0.17.0, mypy 2.4.0, pytest 9.1.1 and uv 0.12.19: the block parses,
mypy accepts every listed error code, pytest's strict mode refuses unknown options, and the banned APIs, `E402`,
`E722`, `BLE001`, `S110`, `PTH`, `T201`, `UP` and `PLW0603` were each shown firing. Re-run the same day on CPython
3.15.0 (uv 0.13.0): it passes. Mirrored test folders (rule 1.6) were checked on 2026-11-13 with pytest 9.2.0,
mypy 2.4.1 and ruff 0.17.4 on CPython 3.15.2: without the test `__init__.py` files mypy stops with `Duplicate
module named`; with them all three pass, with this block unchanged.

```toml
[tool.ruff]
line-length = 99  # PEP 8's maximum for a team that agrees on it
# target-version is read from [project] requires-python

[tool.ruff.lint]
select = [
    "F", "E", "W",  # pyflakes, pycodestyle (E402 imports at top, E722 bare except)
    "I",            # import sorting
    "N",            # PEP 8 naming
    "UP",           # current syntax for the minimum Python
    "B",            # likely bugs (B904 raise from)
    "SIM",          # simpler equivalents
    "PTH",          # pathlib, not os.path
    "RUF",          # ruff's own checks (RUF012 mutable class defaults)
    "BLE",          # catch-all except only when logged or re-raised
    "T20",          # no print
    "LOG",          # logging misuse
    "PGH",          # blanket suppressions
    "TID",          # banned APIs, absolute imports
    "ASYNC",        # blocking calls in async code
    "PT",           # pytest style
    "S",            # security (bandit)
    "D",            # PEP 257 docstrings
    "PLW0603",      # no global statement
]

[tool.ruff.lint.pydocstyle]
convention = "pep257"

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"os.path".msg = "Use pathlib."
"sys.path".msg = "Install the project (uv sync); never edit sys.path."
"threading.Thread".msg = "Use concurrent.futures or asyncio."
"_thread".msg = "Use concurrent.futures or asyncio."
"typing.no_type_check".msg = "Fix the types instead."

[tool.ruff.lint.per-file-ignores]
# Every entry says why. Tests assert (S101), and their names are their documentation (D).
"tests/**" = ["S101", "D"]

[tool.ruff.format]
docstring-code-format = true

[tool.mypy]
python_version = "3.15"  # the product's Python (rule 4)
files = ["src", "tests"]
strict = true
warn_unreachable = true
enable_error_code = [
    "deprecated", "exhaustive-match", "explicit-override", "ignore-without-code",
    "mutable-override", "possibly-undefined", "redundant-expr", "truthy-bool",
    "truthy-iterable", "unimported-reveal", "unused-awaitable",
]

[tool.pytest]
testpaths = ["tests"]
addopts = ["--import-mode=importlib"]
strict = true

[tool.uv]
exclude-newer = "7 days"
no-build = true
```

CI runs, and fails on any finding:

```sh
uv sync --locked
uv run --locked ruff format --check
uv run --locked ruff check
uv run --locked mypy
sh scripts/check-suppressions.sh
uv run --locked pytest
```

`scripts/check-suppressions.sh` is the script on [suppressions.md](suppressions.md).

**Adopting in an existing repository:** existing findings go into per-file ignores (ruff) and overrides (mypy), each
naming the rules it fails and the reason "pre-standard code"; the list only shrinks. New files get no entry.

**Known gap:** ruff's `extend` reads only a local file, so each repository holds a copy of this block. A drift check
against this page is follow-up work.

## Settled practice and where practitioners disagree

Settled (primary sources agree, no serious dissent found): PEP 8 naming and import placement; no bare `except`;
`raise from`; module-level loggers and no handlers in libraries; `concurrent.futures` and `TaskGroup` over raw
threads and `gather`; dataclasses for data; protocols for structural interfaces; type hints checked in CI.

Disputed, and what we chose:

- **src layout for applications.** [PUG] takes no side and notes that src requires installing the project; [HYN]
  and [PT] favour src, and [HYN] notes the layout is still debated. uv 0.12.0 moved its application default to src
  [UV12]. We use src everywhere: one shape, and tests
  always run against the installed code.
- **Where test helpers live.** [PT]'s `app.testing` ships the helpers in the wheel; some teams refuse that. We allow
  either `<package>/testing` or a separate workspace package; never `sys.path`.
- **Which type checker.** [TC] (updated 2026-10-06): on the typing-spec conformance suite mypy scores 77.3%, pyrefly
  (1.0, May 2026) 97.9% and ty (beta) 86.5%; it calls mypy the safe default for projects that already use it. We keep
  mypy strict as the gate (every repository already runs it) and pyright in the editor. Revisit when a second checker is worth its cost.
- **pathlib over os.path.** os.path is not deprecated, and porting needs care because pathlib normalises paths
  [PATH]. We choose pathlib for one way of doing it, with exceptions in config.
- **Classes.** [SWC] is one maintainer's talk, and no linter enforces it; the rule rests on review.
- **Line length.** PEP 8 says 79, up to 99 for a team; ruff and Black default to 88; [GSG] says 80; repositories vary
  from 88 to 140. We take 99, PEP 8's own team maximum.
- **Suppression comments.** This page first allowed config entries only; practitioners name the code and justify it
  on the line. We allow one code per line with a reason and maintainer approval ([suppressions.md](suppressions.md)).
- **Cooldown length.** [COOL] finds 7 days blocks most attacks and 14 days all but one (xz-utils). We keep 7 days
  with the advisory exception.
- **Folder per feature or per file type.** [FAPI]'s own example keeps every router in one `routers/` folder, which
  is grouping by file type; [FBP] found that grouping "didn't scale well" for a monolith with many domains. We
  group by feature (standard §3.8), starting flat.
