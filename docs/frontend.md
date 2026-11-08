# TypeScript and JavaScript standard

The rules for TypeScript and JavaScript in every repository that adopts them, adopted by standard §3.2. Short rules, each with
its source; where a tool does not enforce a rule, it says so (standard §4.3). Researched 2026-10-21.

## Sources (read 2026-10-21)

Primary:

- [BIO] Biome: [suppressions](https://biomejs.dev/analyzer/suppressions/),
  [language support](https://biomejs.dev/internals/language-support/), [domains](https://biomejs.dev/linter/domains/),
  [Biome v2](https://biomejs.dev/blog/biome-v2/) and [type inference with Vercel](https://biomejs.dev/blog/vercel-partners-biome-type-inference)
- [OXC] Oxlint: [type-aware linting stable](https://oxc.rs/blog/2026-07-22-type-aware-linting-stable) (2026-07-22),
  [CLI](https://oxc.rs/docs/guide/usage/linter/cli.html)
- [ESL] ESLint: [configure rules](https://eslint.org/docs/latest/use/configure/rules) (disable directives)
- [EOPT] TypeScript: [`exactOptionalPropertyTypes`](https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html);
  library issues: [radix-ui/primitives #3535](https://github.com/radix-ui/primitives/issues/3535) (closed 2026-10-06
  by PR #4173), [strapi/design-system #2045](https://github.com/strapi/design-system/issues/2045),
  [vuejs/router #2820](https://github.com/vuejs/router/issues/2820)
- [TSE] typescript-eslint: [typed linting](https://typescript-eslint.io/getting-started/typed-linting/); its peer
  range, read with `npm view typescript-eslint@8.71.2 peerDependencies`: `typescript: '>=4.8.4 <6.1.0'`
- [TS7] [Announcing TypeScript 7.0](https://devblogs.microsoft.com/typescript/?p=5246) (2026-07-08)
- [NEXT] [Next.js: upgrading to version 16](https://nextjs.org/docs/app/guides/upgrading/version-16)
- [EXPO] [Expo: using ESLint](https://docs.expo.dev/guides/using-eslint/)
- [PNPM] pnpm settings: [dependency resolution](https://pnpm.io/settings/dependency-resolution),
  [build](https://pnpm.io/settings/build)

Practitioner evidence:

- [PKG] pkgpulse, [Biome vs ESLint vs Oxlint 2026](https://www.pkgpulse.com/guides/biome-vs-eslint-vs-oxlint-2026) (2026-03-17)

Null results: no independent benchmark of the three was found, only vendor and blog figures, which disagree.

## Choice

1. **Default: Biome for lint and format.** Evidence: one tool and one config
   replace ESLint plus Prettier [PKG]; it does not load TypeScript's API, so it is unaffected by TypeScript 7 shipping
   without one [TS7]; it lints and formats TypeScript, JSX, JSON and CSS fully [BIO]; its domains turn on Next.js,
   React and React Native rules from `package.json` [BIO]; Next.js 16 removed `next lint` and points to "Biome or the
   ESLint CLI" [NEXT].
2. **Add Oxlint with `--type-aware` beside Biome where code has its own async logic** (API clients, server code, data
   fetching): it runs 59 of typescript-eslint's 61 type-aware rules on TypeScript 7 [OXC], such as
   `no-floating-promises`. Biome's own type inference is deliberately a subset ("we have no intention to rebuild" tsc)
   [BIO]. Oxlint only lints; Biome still formats. A static content site does not need it.
3. **ESLint with typescript-eslint and Prettier only where a framework's official linting is ESLint**: Expo and React
   Native, whose guide is `npx expo lint` with `eslint-config-expo` [EXPO]. Its typed linting needs TypeScript 6 or
   older (the peer range above); under TypeScript 7 that means the `@typescript/typescript6` alias [TS7].
4. **Astro:** Biome lints the `.ts` and `.tsx` files; its `.astro` support is experimental and opt-in [BIO];
   `astro check` does the type check.

## Rules

1. **TypeScript strict, no emit, in CI.** `tsc --noEmit` (or `tsc -b` with project references, `astro check` for
   Astro). `strict` is on by default from TypeScript 7 [TS7]; state it anyway, with the stricter flags below.
2. **Formatting is checked, never left to editors:** `biome ci` checks formatting with linting (Prettier `--check`
   in the ESLint set).
3. **Lint at error level.** Rules are set to `"error"`, and CI fails on any warning (`biome ci --error-on-warnings`,
   `oxlint --deny-warnings`, `eslint --max-warnings 0`).
4. **Suppressions follow [suppressions.md](suppressions.md):** one rule, a reason on the line, a stale check, and a
   line in `.suppressions`. Allowed: `// biome-ignore lint/<group>/<rule>: reason`,
   `// eslint-disable-next-line <rule> -- reason` (or `oxlint-`), and `// @ts-expect-error -- reason`, never
   `@ts-ignore` or `@ts-nocheck`. Stale ones fail: Biome reports "Suppression comment has no effect", ESLint with
   `reportUnusedDisableDirectives: "error"` [ESL], Oxlint with `--report-unused-disable-directives`, and `tsc` with
   "Unused '@ts-expect-error' directive". Config exceptions (Biome `overrides`, ESLint `files` blocks) are only for
   whole categories of files, each with a reason.
5. **pnpm with the supply-chain settings** (standard §7B): `packageManager` names an exact pnpm version; versions are
   exact (`savePrefix: ""`) with the lockfile committed; CI installs with `--frozen-lockfile`. `pnpm-workspace.yaml`
   carries the block below. pnpm 11 and newer default `minimumReleaseAge` to 1440 minutes (one day) [PNPM], so 10080
   must be set. `onlyBuiltDependencies` was removed in pnpm 11; `allowBuilds` replaced it [PNPM].
6. **`exactOptionalPropertyTypes` is on**, unless a dependency's types make it impossible. `strict` does not include
   it (verified: `strict` alone accepts `{ theme: undefined }` for an optional `theme`; the flag rejects it with
   TS2375), and it "makes TypeScript truly enforce the definition provided as an optional property" [EOPT]. Library
   types can break under it ([EOPT]: Radix's issue, fixed 2026-10-06, and others). If one does, the repository leaves
   the flag off with a comment beside it naming the dependency and its upstream issue, and turns it on once a fixed
   release is at least 7 days old.

## Configuration

`tsconfig.json` (compiler options; add the framework's own):

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noPropertyAccessFromIndexSignature": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

`biome.jsonc`:

```jsonc
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "formatter": { "indentStyle": "space", "lineWidth": 100 },
  "assist": { "actions": { "source": { "organizeImports": "on" } } },
  "linter": {
    "rules": {
      "preset": "recommended",
      "suspicious": { "noExplicitAny": "error", "noConsole": "error" },
      "style": { "noNonNullAssertion": "error" },
      "correctness": { "noUnusedImports": "error", "noUnusedVariables": "error" }
    }
  },
  "overrides": [
    {
      // Each override names its files and says why. Example: the CLI's output is console output.
      "includes": ["src/cli.ts"],
      "linter": { "rules": { "suspicious": { "noConsole": "off" } } }
    }
  ]
}
```

`.oxlintrc.json` (only with rule 2 of the choice):

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "categories": { "correctness": "error" },
  "rules": {
    "typescript/no-floating-promises": "error",
    "typescript/no-misused-promises": "error",
    "typescript/await-thenable": "error",
    "typescript/no-unnecessary-type-assertion": "error"
  }
}
```

`eslint.config.js` (only with rule 3 of the choice; Expo adds `eslint-config-expo/flat`):

```js
import js from "@eslint/js";
import { defineConfig } from "eslint/config";
import tseslint from "typescript-eslint";

export default defineConfig([
  { ignores: ["dist/", "eslint.config.js"] },
  {
    // A disable comment names one rule and a reason; one that no longer applies fails.
    linterOptions: { reportUnusedDisableDirectives: "error" },
  },
  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
]);
```

`pnpm-workspace.yaml`:

```yaml
# Supply-chain settings, stated even where pnpm's default already matches.
minimumReleaseAge: 10080        # 7 days, in minutes
minimumReleaseAgeStrict: true   # fail rather than pick a too-new version
trustPolicy: no-downgrade       # fail if a release lost the provenance its predecessors had
blockExoticSubdeps: true        # only direct dependencies may come from git or tarball URLs
strictDepBuilds: true           # an unreviewed install script fails the install
savePrefix: ""                  # pnpm add writes exact versions
allowBuilds:
  # Each entry: true (runs) or false (skipped), with the reason.
  {}
```

## CI

```sh
pnpm install --frozen-lockfile
pnpm exec tsc --noEmit
pnpm exec biome ci --error-on-warnings .
pnpm exec oxlint --type-aware --deny-warnings --report-unused-disable-directives  # with Oxlint
sh scripts/check-suppressions.sh  # the script on suppressions.md
```

The ESLint set replaces the Biome line with `pnpm exec prettier --check .` and `pnpm exec eslint --max-warnings 0 .`.

Verified 2026-10-21 on sample projects with pnpm 12.9.1 and Node 24.16.0 (Biome 2.5.15 and TypeScript 7.0.2; Oxlint
1.88.0 with oxlint-tsgolint 7.0.2004; ESLint 10.12.0, typescript-eslint 8.71.2, Prettier 3.9.10, TypeScript 6.0.3;
each the newest release at least 7 days old). Clean code passes. Each set fails on: a `biome-ignore`, `eslint-disable`
or `@ts-expect-error` comment, a lint error, a type error, `as any`, a floating promise (Oxlint, ESLint) and a
formatting difference. The suppression rules were re-verified with the check script: one specific suppression with a
reason passes once listed (Biome, ESLint, Oxlint and `@ts-expect-error` were each shown to accept their form), and
stale, blanket, file-level, reasonless, unlisted and duplicated ones fail. The configuration blocks above pass
`biome ci` and `prettier --check` as written.

## Adopting in an existing repository

1. **Lint findings:** existing ones go into Biome `overrides` or ESLint `files` blocks, each naming its files and
   rules with the reason "pre-standard code"; the list only shrinks, and new files get no entry.
2. **tsconfig flags:** turn the stricter flags on one at a time, each in its own PR with all its errors fixed. A type
   error is never suppressed to adopt a flag. Each PR that turns a flag on says which one.

## Settled practice and where practitioners disagree

Settled: `strict` TypeScript checked by `tsc` in CI (TypeScript 7 makes it the default [TS7]); a formatter checked in
CI; lockfile installs.

Disputed, and what we chose:

- **Default tool.** [PKG] calls ESLint the default "for mature apps with plugin-heavy rules" and Biome the choice for
  new projects; Next.js offers both [NEXT]. We default to Biome: plugin needs are mostly framework rules Biome's domains cover, and it is unaffected by TypeScript 7's missing API.
- **Type-aware rules.** [PKG] (March 2026) rates Oxlint's typed coverage narrower; Oxc's July 2026 release reports 59
  of 61 typescript-eslint rules [OXC]. We take the newer primary source and add Oxlint where async code needs it.
- **Speed figures** (10x to 100x) come from vendors and blogs and disagree; they did not decide anything here.
