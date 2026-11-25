# Go standard

The Go rules for every repository that adopts them, adopted by standard §3.2. Go is a choice, not a requirement
(decision, 2026-11-16): standard §3.2 says which jobs it fits, and rule 1 when a product moves a part to it. This page
sets the shape before the first module (written 2026-11-16). Short rules, each with its source; where a tool does not
enforce a rule, it says so (standard §4.3).

## Sources (read 2026-11-16)

Primary:

- [REL] [Go release history](https://go.dev/doc/devel/release): "Each major Go release is supported until there are
  two newer major releases." go1.27.3 on 2026-10-19, go1.27.4 on 2026-11-10. [DL] [go.dev/dl JSON](https://go.dev/dl/?mode=json&include=all)
  (each archive's SHA-256)
- [TOOL] [Go toolchains](https://go.dev/doc/toolchain): the go line "sets the minimum required Go version"; toolchains
  "are downloaded like any other module, and have their checksums checked by the Go checksum database"
- [SGO] [actions/setup-go](https://github.com/actions/setup-go): reads the `toolchain` line; its `src/installer.ts`
  checks no checksum of the archive it downloads
- [EG] [Effective Go](https://go.dev/doc/effective_go); [CRC] [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments);
  [FAQ] [Go FAQ](https://go.dev/doc/faq)
- [GSD] [Google Go style: decisions](https://google.github.io/styleguide/go/decisions),
  [GSB] [best practices](https://google.github.io/styleguide/go/best-practices)
- [LAY] [Organizing a Go module](https://go.dev/doc/modules/layout)
- [SEC] [Go security best practices](https://go.dev/doc/security/best-practices)
- [GCI] golangci-lint: [install](https://golangci-lint.run/docs/welcome/install/local/),
  [configuration file](https://golangci-lint.run/docs/configuration/file/),
  [linter settings](https://golangci-lint.run/docs/linters/configuration/),
  [false positives](https://golangci-lint.run/docs/linters/false-positives/)
- [MOD] [Managing dependencies](https://go.dev/doc/modules/managing-dependencies) (go.sum, the `tool` directive);
  [REFMOD] [Go modules reference](https://go.dev/ref/mod) (a proxy's `.info` `Time` is the "commit time");
  [CMDGO] [cmd/go](https://pkg.go.dev/cmd/go) (`go list -m` `Time`, `go mod verify`, the generated-code header)
- [I76485] [golang/go #76485](https://github.com/golang/go/issues/76485): dependency cooldown in the go command, on
  hold since 2026-06-25
- [OPT] [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
  (`gomod` supports cooldown)
- [G125] [Go 1.25](https://go.dev/doc/go1.25) (`testing/synctest`), [G126] [Go 1.26](https://go.dev/doc/go1.26)
  (`go fix` modernizers)
- [HTTP] [net/http](https://pkg.go.dev/net/http) ("A Timeout of zero means no timeout"; `Shutdown` waits
  "indefinitely" unless its context ends), [SIG] [os/signal](https://pkg.go.dev/os/signal),
  [SLOG] [log/slog](https://pkg.go.dev/log/slog), [EGRP] [errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)
- [PGX] [pgx v5 pgconn](https://pkg.go.dev/github.com/jackc/pgx/v5/pgconn) (`RuntimeParams`); [SQLC]
  [sqlc with pgx](https://docs.sqlc.dev/en/latest/guides/using-go-and-pgx.html); [GOOSE]
  [goose](https://github.com/pressly/goose); [OAPI] [oapi-codegen](https://github.com/oapi-codegen/oapi-codegen);
  [OTS] [openapi-fetch](https://openapi-ts.dev/openapi-fetch/)
- [GEN] [Generating code](https://go.dev/blog/generate): the generated file "must be checked into the source code
  repository"

Practitioner evidence:

- [UBER] [Uber Go style guide](https://github.com/uber-go/guide/blob/master/style.md) (last change 2026-04-15)
- [PL] [golang-standards/project-layout](https://github.com/golang-standards/project-layout): "NOT an official
  standard"; [PL117] its [issue 117](https://github.com/golang-standards/project-layout/issues/117) by Russ Cox
- Advisory history from [OSV](https://osv.dev) and maintainer activity from GitHub, read 2026-11-16 (rule 13)

Null results: the go command has no release-age setting [I76485]; setup-go checks no archive checksum [SGO];
Dependabot's options reference does not say it updates the `toolchain` line; `go test -timeout` limits a test binary,
and no per-test limit exists; index.golang.org cannot be queried by module; sqlc's privacy page could not be read
(sqlc generated with networking turned off in the sample, so it needs no network).

## Rules

### 1. When to use Go (decision, 2026-11-16)

1. Which jobs Go fits, and which belong to another language: standard §3.2 (decision, 2026-11-25).
2. A product already in another language may move a part to Go when Go is the right tool for that part (standard
   §3.2) and a measurement shows the gain (standard §3.6), for example memory or CPU on the real server (decision,
   2026-11-17). Each move is a decision record (rule 4).
3. **Code that runs as root on a production host is never Go** (decision, 2026-11-16): it stays standard-library
   Python on the system's own `python3` (python.md rule 8.2).
4. A Go service in an existing product is a maintainers' decision with a record in `docs/decisions/`.

### 2. Layout (standard §3.8)

```text
<repo>/
  go.mod  go.sum  .golangci.yml  sqlc.yaml  Dockerfile  .suppressions
  api/openapi.yaml                    # the HTTP contract, written first
  cmd/<product>-<process>/main.go     # thin: config, wiring, run, shutdown
  internal/
    config/                           # typed configuration, read once
    database/                         # pool; migrations/ embedded with embed.FS
    api/                              # generated server code
    <feature>/                        # handler.go, service.go, queries.sql, store/, *_test.go
  tools/go.mod  tools/go.sum          # tool directives only (rule 12.6)
```

1. Everything but `cmd/` is in `internal/`: a server exports nothing [LAY]. No `pkg/` or `src/` [PL], [PL117].
2. One folder per feature (standard §3.8); tests sit beside the code as `*_test.go`.
3. Package names are short, lowercase, one word, never `util`, `common` or `helpers` [GSB]; names follow standard §3.5.

### 3. Toolchain

1. `go.mod` holds `go 1.27.0` (language version and minimum) and `toolchain go1.27.3`, an exact release at least 7
   days old (standard §7B.1) [TOOL]. go1.27.4 is adoptable from 2026-11-17; it fixes GO-2026-6859, which govulncheck
   reports against go1.27.3 (rule 12.4).
2. Patch releases follow the 7-day rule; Go supports the two newest majors [REL]. A new `1.N` is adopted from its first
   point release once that is 7 days old and CI passes with every tool (decision, 2026-11-16, as python.md rule 4.1).
3. **The first Go that runs in CI** comes from the go.dev archive checked against its SHA-256 [DL], or from the runner
   image's preinstalled Go, never from setup-go's download [SGO] (decision, 2026-11-16). The go command then switches to
   the `toolchain` line, fetching it as a module checked by the checksum database; with `GOSUMDB=off` it refuses
   [TOOL].
4. The `toolchain` line is the one pin. The by-hand upgrade routine moves it ([dependabot.md](dependabot.md) rule 5).

### 4. Container images (decision, 2026-11-16)

1. Multi-stage. The build stage is `golang:<1.N>-trixie` pinned by digest and held at major and minor (dependabot.md
   rule 15). The image sets `GOTOOLCHAIN=local`, so the Dockerfile sets `GOTOOLCHAIN=auto` and the `toolchain` line
   decides (rule 3.3). It builds with `CGO_ENABLED=0 go build -trimpath`.
2. The final stage is `scratch` with three things copied from the build stage: the binary, the CA bundle and one
   non-root passwd entry (`nobody`). A binary that uses time zones embeds them with `-tags timetzdata`.
3. Build provenance and an SBOM as standard §7B.10 and §7B.11 say.

```dockerfile
FROM golang:1.27.3-trixie@sha256:<digest> AS build
ENV GOTOOLCHAIN=auto CGO_ENABLED=0
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -trimpath -tags timetzdata -o /out/app ./cmd/<product>-<process> \
 && grep '^nobody:' /etc/passwd > /out/passwd

FROM scratch
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=build /out/passwd /etc/passwd
COPY --from=build /out/app /app
USER nobody
ENTRYPOINT ["/app"]
```

### 5. Types, methods, interfaces and composition

1. No classes: a struct with methods holds state and the behaviour that keeps it valid; `NewX` builds it. A stateless
   step is a function.
2. Composition, not inheritance: Go has "no type hierarchy" [FAQ]. Embedding only to "borrow" an implementation [EG],
   never in an exported struct [UBER].
3. Interfaces belong to the package that uses them, are small, and appear when a second implementation or a test
   needs one, never "for mocking" on the implementor's side; functions return concrete types [CRC]. Types satisfy
   them implicitly [FAQ]; `var _ I = (*T)(nil)` only where the interface is a contract (the generated server).
4. One receiver kind per type; a pointer when in doubt [CRC].
5. No mutable package-level state and no `init()` [UBER] (enforced: `gochecknoinits`; globals by review).
6. Generics only for one algorithm over several types: "Write code, don't design types" [GSD].
7. Enums are typed constants; a `switch` covers every value (enforced: `exhaustive`).
8. Every exported name has a doc comment [CRC] (enforced: revive `exported`).

### 6. Errors and logging

1. Every error is checked, type assertions included (enforced: `errcheck`). The exception is golangci-lint's
   `std-error-handling` preset: a deferred `Close`, `Flush` or print call.
2. Wrap to add context, `%w` at the end [GSB]; compare with `errors.Is` and `errors.As` (enforced: `errorlint`);
   sentinels are `ErrX`, types `XError` (enforced: `errname`, staticcheck ST1012).
3. Error strings are lowercase with no final punctuation [CRC] (enforced: staticcheck ST1005).
4. Handle an error once: log it or return it [UBER].
5. No panic for errors [CRC]; `os.Exit` and `log.Fatal` only in `main` (enforced: revive `deep-exit`).
6. Logging is `log/slog` [SLOG]. `main` builds one JSON logger on stderr and passes it in; no global logger, no
   `fmt.Print*`, no `log` package; key-value pairs, constant messages, the `Context` methods where a context exists
   (enforced: `sloglint`, `forbidigo`, `depguard`). Secrets and personal data never reach a log (review).

### 7. Context, goroutines and shutdown

1. `ctx context.Context` is the first parameter of every call that does I/O or may block, never stored in a struct
   [CRC] (enforced: `containedctx`, `contextcheck`).
2. Prefer synchronous functions [CRC]. Every goroutine is waited for by the code that starts it [UBER]; tasks that fail together
   run in `errgroup.WithContext` [EGRP].
3. `main` uses `signal.NotifyContext` for SIGINT and SIGTERM [SIG], then `Shutdown` with a bounded context [HTTP],
   then closes the pool, and exits non-zero on error.
4. Tests run with `-race` [SEC].

### 8. Standard §3.7 in Go

1. **Server:** `http.Server` with `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout` and `IdleTimeout`; never
   `http.ListenAndServe` (enforced: gosec G112, G114); bodies bounded with `http.MaxBytesHandler` or
   `http.MaxBytesReader`.
2. **Client:** an `http.Client` with `Timeout` set, since zero "means no timeout" [HTTP]; never `http.DefaultClient`
   or `http.Get` (enforced: `forbidigo`); requests carry a context (enforced: `noctx`); bodies are closed (enforced:
   `bodyclose`).
3. **Database:** `pgxpool` with `ConnectTimeout` and `statement_timeout` as a run-time parameter [PGX], plus a context
   deadline per call; rows closed and `Err()` checked (enforced: `sqlclosecheck`, `rowserrcheck`); writes that must
   succeed together in one `pgx.BeginFunc` transaction.
4. **Retries:** idempotent calls only, bounded, exponential backoff, stopped by the context; one helper in
   `internal/`, no library.
5. **Events that can repeat:** keyed by their own ID under a unique constraint, `INSERT ... ON CONFLICT DO NOTHING` in
   the effect's transaction.

### 9. Contracts

| Contract | Lives in | Generated into | Never |
|---|---|---|---|
| HTTP API, any language | The OpenAPI file is the contract whatever language each side is in, Go and Python services included. python.md's rules for it come later. | each side's generator | a side that is not generated from the file |
| HTTP API, back end to front end | `api/openapi.yaml`, written first | Go: `internal/api/` (oapi-codegen `std-http-server`, strict server, models); TypeScript: `schema.gen.ts` (openapi-typescript) called through openapi-fetch [OTS] | hand-written request or response types; a route outside the file |
| HTTP API between services | the callee's file; the caller keeps a copy, `api/<service>.openapi.yaml`, updated by pull request | the caller's oapi-codegen client | importing another service's packages |
| Schema and migrations | `internal/database/migrations/NNNNN_<name>.sql`, goose SQL migrations, embedded and applied by the product's migrate command | sqlc reads the folder as its schema | DDL in Go strings or tests; hand-run DDL in production; editing a merged migration |
| Queries | `internal/<feature>/queries.sql` | `internal/<feature>/store/` (sqlc, `sql_package: pgx/v5`) [SQLC] | SQL built with `fmt.Sprintf` or `+` (enforced: gosec G201, G202) |
| Configuration | environment variables and mounted secret files (standard §7.2), read once in `internal/config` | none | `os.Getenv` elsewhere, tests aside (enforced: `forbidigo`); a secret on a command line or in a log |
| Generated code | committed beside its source with the `// Code generated ... DO NOT EDIT.` header [CMDGO], [GEN] | `go generate ./...`, `go tool -modfile=tools/go.mod sqlc generate` | hand edits (CI regenerates and fails on a diff); a lint suppression |

### 10. Testing

1. Standard `testing`; table tests with named fields and `t.Run` [GSD]; messages `F(in) = got, want want` [CRC];
   `cmp.Diff` from go-cmp for structs [GSD]. No assertion library [GSD] (enforced: `depguard` refuses testify).
   Helpers call `t.Helper()`; tests use `t.Context()` and `t.TempDir()` (enforced: `thelper`, `usetesting`).
2. Time and concurrency are tested with `testing/synctest` [G125], never with sleeps.
3. Store and handler tests run against a real Postgres, never a mock; they skip only under `-short`.
4. A parser of untrusted input has a fuzz test; its seed corpus runs in every `go test` [SEC].
5. `-timeout` limits each test binary, so standard §4.4's limit holds per package, not per test (standard §4.3).

### 11. Lints, formatters and suppressions

1. golangci-lint v2 with the configuration below; `golangci-lint fmt` runs gofmt (simplify) and goimports [GCI].
2. `go fix -diff ./...` prints nothing, so code keeps current idioms [G126].
3. Suppressions follow [suppressions.md](suppressions.md): only `//nolint:<one-linter> // <reason>` at the end of a
   code line. nolintlint refuses a bare or unexplained one and reports a stale one [GCI]; the check script refuses
   the rest (`//nolint:all`, several linters, the form at the start of a line, which covers a block or a file,
   `//lint:ignore` and `#nosec`) and skips generated files.
4. Adopting in an existing module: findings go into `linters.exclusions.rules` by path with the reason "pre-standard
   code"; the list only shrinks.

### 12. Supply chain

1. `go.mod` and `go.sum` committed [MOD]; CI runs `go mod verify` and `go mod tidy -diff`. A new import is added with
   `go get <module>@<version>`, never by letting `go mod tidy` pick the latest.
2. `GOPROXY` and `GOSUMDB` keep their defaults; never `GOSUMDB=off`, `GONOSUMDB` or `GOINSECURE` [TOOL]. `GOPRIVATE`
   only for our own private modules. No `replace` without a maintainer-approved reason; no vendoring.
3. Dependabot's gomod cooldown of 7 days [OPT] on both modules (template in [dependabot.md](dependabot.md)).
4. `govulncheck ./...` in CI [SEC]. A finding is triaged as dependabot.md rule 12 says; a fix younger than 7 days waits
   (standard §7B.13) unless the vulnerability is actively exploited (§7B.14).
5. **Age (standard §7B.13; decision, 2026-11-16):** the `dependency-age` workflow reads the `Time` of each module version
   a pull request adds (`go list -m -json <module>@<version>`) and fails under 7 days. `Time` is the commit time
   [REFMOD], set by the author: it checks freshness, not proof. The go1.27.4 toolchain module shows 2026-11-02 for a
   release made 2026-11-10. MVS keeps transitive versions at what dependencies require. Adopt Go's own setting when
   [I76485] lands.
6. **Tool pins (decision, 2026-11-16):** golangci-lint is the release binary checked against its `checksums.txt` [GCI].
   oapi-codegen, sqlc and govulncheck are `tool` directives in `tools/go.mod`, run with `go tool -modfile=tools/go.mod`:
   go.sum and the checksum database verify them, and Dependabot updates them. A separate module keeps their
   dependencies out of the application's: adding sqlc raised `google.golang.org/protobuf` from v1.26.0 to v1.36.11
   in the tools module. sqlc builds with cgo, so CI needs a C compiler.
7. Standard library first; every module is a dependency decision (standard §3.4).

### 13. Libraries

Approved on 2026-11-16, at these versions (Go modules dated by their tag's `Time`):

| Need | Module | Version | Advisories (OSV) and maintenance |
|---|---|---|---|
| Postgres driver | `github.com/jackc/pgx/v5` | v5.12.0 (2026-10-31) | 10 entries; GO-2026-5004 (SQL injection) fixed in 5.9.2; one main maintainer |
| Queries | sqlc | v1.31.1 (2026-04-22) | none; one main maintainer |
| Migrations | `github.com/pressly/goose/v3` | v3.29.0 (2026-10-11) | none |
| OpenAPI server | `github.com/oapi-codegen/oapi-codegen/v2`, `github.com/oapi-codegen/runtime` | v2.8.2 (2026-10-31), v1.8.0 (2026-10-23) | GO-2026-6016 fixed in 2.7.1 |
| Test diffs | `github.com/google/go-cmp` | v0.7.0 (2025-01-14) | none |
| Goroutine groups | `golang.org/x/sync` | v0.25.0 (2026-10-15) | none |
| Vulnerability scan | `golang.org/x/vuln` | v1.9.0 (2026-10-11) | none |
| Lint | golangci-lint | v2.15.0 (published 2026-10-16) | none |
| TypeScript client | openapi-typescript, openapi-fetch | 7.13.0, 0.17.0 (2026-02-11) | none; openapi-typescript needs TypeScript 5 (peer `^5.x`) |

## Configuration

`go.mod` starts with the version lines; `tools/go.mod` holds only tools:

```text
module <module path>

go 1.27.0

toolchain go1.27.3
```

```text
module <module path>/tools

go 1.27.0

toolchain go1.27.3

tool (
	github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen
	github.com/sqlc-dev/sqlc/cmd/sqlc
	golang.org/x/vuln/cmd/govulncheck
)
```

`.golangci.yml` (set `local-prefixes` to the module path):

```yaml
version: "2"

run:
  timeout: 5m # every CI step has a time limit

linters:
  default: standard # errcheck, govet, ineffassign, staticcheck, unused
  enable:
    - bodyclose # response bodies closed
    - containedctx # no context stored in a struct
    - contextcheck # the caller's context is passed on
    - depguard # banned packages
    - errname # ErrX sentinels, XError types
    - errorlint # errors.Is, errors.As, %w
    - exhaustive # a switch covers every enum value
    - forbidigo # banned calls
    - gochecknoinits # no init()
    - gosec # G112, G114, G201, G202 and the rest
    - nilerr # no nil return after err != nil
    - noctx # outgoing requests carry a context
    - nolintlint # one linter, a reason, not stale
    - revive # exported doc comments, deep-exit
    - rowserrcheck # rows.Err() checked
    - sloglint # log/slog style
    - sqlclosecheck # rows and statements closed
    - thelper # helpers call t.Helper()
    - usetesting # t.Context(), t.TempDir()
  settings:
    errcheck:
      check-type-assertions: true
    govet:
      enable-all: true
      disable:
        - fieldalignment # layout, not correctness; optimise only after measuring
        - shadow # flags the usual `err` shadowing
    staticcheck:
      checks: ["all"]
    gosec:
      excludes:
        - G104 # unchecked errors: errcheck reports them
    depguard:
      rules:
        main:
          deny:
            - pkg: github.com/stretchr/testify
              desc: use testing and go-cmp; no assertion libraries
            - pkg: github.com/pkg/errors
              desc: use errors and fmt.Errorf with %w
            - pkg: log$
              desc: use log/slog
    forbidigo:
      analyze-types: true
      forbid:
        - pattern: ^fmt\.Print(f|ln)?$
          msg: log with log/slog; write CLI output to an io.Writer
        - pattern: ^http\.(Get|Head|Post|PostForm)$
          msg: use an http.Client with a Timeout
        - pattern: ^http\.DefaultClient$
          msg: its Timeout is zero, which means no timeout
        - pattern: ^os\.(Getenv|LookupEnv)$
          msg: read configuration in internal/config only
    nolintlint:
      require-explanation: true
      require-specific: true
      allow-unused: false
    revive:
      rules:
        - name: exported
        - name: deep-exit
    sloglint:
      no-global: all
      kv-only: true
      static-msg: true
      context: scope
    usetesting:
      context-background: true # off by default
      context-todo: true # off by default
  exclusions:
    generated: strict # the Go header rule
    presets:
      - std-error-handling # unchecked Close, Flush and print errors
    rules:
      - path: ^internal/config/
        linters: [forbidigo]
        text: os\.(Getenv|LookupEnv) # configuration is read here
      - path: _test\.go
        linters: [forbidigo]
        text: os\.(Getenv|LookupEnv) # tests read the test database address

formatters:
  enable: [gofmt, goimports]
  settings:
    gofmt:
      simplify: true
    goimports:
      local-prefixes: [<module path>]

issues:
  max-issues-per-linter: 0
  max-same-issues: 0
  uniq-by-line: false # report every finding, not one per line
```

`sqlc.yaml` (one `sql` entry per feature):

```yaml
version: "2"
sql:
  - engine: postgresql
    schema: internal/database/migrations
    queries: internal/<feature>/queries.sql
    gen:
      go:
        package: store
        out: internal/<feature>/store
        sql_package: pgx/v5
```

`internal/api/cfg.yaml`, run by `//go:generate go tool -modfile=../../tools/go.mod oapi-codegen -config cfg.yaml ../../api/openapi.yaml`:

```yaml
package: api
output: api.gen.go
generate:
  std-http-server: true
  strict-server: true
  models: true
```

## CI

Install the first Go and golangci-lint by checksum (rule 3.3, rule 12.6), for example:

```sh
echo "<sha256 from go.dev/dl>  go1.27.3.linux-amd64.tar.gz" | sha256sum -c -
grep ' golangci-lint-2.15.0-linux-amd64.tar.gz$' golangci-lint-2.15.0-checksums.txt | sha256sum -c -
```

Then, each step with a time limit, failing on any finding:

```sh
go mod verify
go mod tidy -diff
go -C tools mod tidy -diff
golangci-lint fmt --diff
golangci-lint run
go fix -diff ./...
go generate ./... && go tool -modfile=tools/go.mod sqlc generate && git diff --exit-code
go build ./...
go test -race -shuffle=on -timeout=5m ./...
go tool -modfile=tools/go.mod govulncheck ./...
sh scripts/check-suppressions.sh  # the script on suppressions.md
```

Verified 2026-11-16 on a sample module (`cmd/` with an API, a migrate command and an HTTPS fetcher; one
`internal/notes` feature with an oapi-codegen strict handler and a sqlc store; goose migrations; tests against
PostgreSQL 18.6) using go1.27.3 (bootstrap archive checked against its SHA-256), golangci-lint 2.15.0 (checked against
`checksums.txt`) and the modules in rule 13, every one at least 7 days old by its `Time`. Every step passes on clean
code except govulncheck, which reports GO-2026-6859 in go1.27.3's `net/http` (fixed in go1.27.4, not in CISA's KEV
catalog on 2026-11-16, so the fix waits). Shown failing: an archive with one byte changed (`sha256sum -c`); every
linter in the configuration on its own violation (once `uniq-by-line: false` was set: by default only one finding
per line is shown); a gofmt and a goimports difference; a requirement no code uses (`go mod tidy -diff`); a changed
file in the module cache (`go mod verify`); old loop and lookup idioms (`go fix -diff`); a data race (`-race`); a
hanging test ("panic: test timed out after 5s"); a called vulnerable function (govulncheck exit 3; uncalled, exit 0);
a committed edit to oapi-codegen or sqlc output and a spec change without regeneration (`git diff --exit-code`); a
handler missing a new operation (the build); `GOSUMDB=off` during the toolchain switch from a go1.26.10 bootstrap; and
`time.LoadLocation` in a `scratch` image built without `-tags timetzdata`. Also shown: the `scratch` image runs as
uid 65534 and makes an HTTPS request; goose migrates down and up; the API serves and stops on SIGTERM; store tests
skip under `-short`; `go list -m -json` marks pgx v5.13.0 (2026-11-11) as young; sqlc generates with networking off;
openapi-typescript's types pass `tsc` (TypeScript 5.9.3) and a wrong field fails; and the Dependabot template with the
gomod entry passes `check-jsonschema --builtin-schema vendor.dependabot` (0.39.0). Not verified: build provenance and
the SBOM (standard §7B.10, §7B.11), which need a GitHub Actions run.

## Settled practice and where practitioners disagree

Settled: gofmt; checking every error; `%w` with `errors.Is` and `errors.As`; the context as first parameter;
interfaces on the consumer's side; `internal/` and `cmd/` [LAY]; `-race`; govulncheck [SEC]; a committed go.sum.

Disputed, and what we chose:

- **Assertion libraries.** Google says "Do not create 'assertion libraries'" [GSD]; Uber's guide uses testify in its
  examples [UBER]. We use `testing` and go-cmp.
- **Where tools are pinned.** golangci-lint says `go tool` installs "aren't guaranteed to work" [GCI], so it is a
  checked binary; the other tools are tool directives in a separate module, so their dependencies do not move ours.
- **Project layout.** golang-standards/project-layout is widely linked but "not an official standard" [PL], and Russ
  Cox calls it "not a standard Go project layout" [PL117]. We follow [LAY].
- **Migrations.** goose and golang-migrate both fit; we chose goose for embedded SQL migrations run by the product.
- **Age of a module.** `Time` is a commit time [REFMOD]; Go's own cooldown is on hold [I76485]. We check it and accept
  the gap (decision, 2026-11-16).
- **gofumpt.** Stricter than gofmt; not used, so the format is the community's one.
