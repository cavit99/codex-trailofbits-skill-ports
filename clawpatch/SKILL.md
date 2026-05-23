---
name: clawpatch
description: Use when the user asks to run or configure Clawpatch/clawpatch, automated code review, semantic feature mapping, Clawpatch reports, finding triage, explicit fix loops, revalidation, Clawpatch CI, or opening PRs from Clawpatch patch attempts. Prefer the latest npm package through npx unless the user pins a version.
---

# Clawpatch

Clawpatch maps a repository into semantic feature slices, reviews bounded context with a provider, stores findings in `.clawpatch/`, and can run an explicit fix loop for one finding at a time.

## Invocation

Prefer the latest npm package so sessions do not accidentally use a stale cached CLI:

```bash
CP="npx -y clawpatch@latest"
$CP --version
$CP --help
```

Use a pinned package only when the user asks for a specific version.

## Preflight

Before running review or fix commands:

```bash
node --version
npm --version
git --version
codex --version
$CP doctor
```

Expected baseline: Node.js 22+, Git 2.x, and a local provider CLI. The default provider is `codex`; useful alternatives include `acpx`, `claude`, `cursor`, `grok`, `opencode`, `pi`, `mock`, and `mock-fail`.

Check worktree state first:

```bash
git status --short
```

`review`, `report`, `show`, `next`, and `revalidate` are read-oriented. `fix` can edit the worktree. `open-pr` can commit and open a PR from a patch attempt. Do not run mutating commands unless they are clearly part of the user's request.

## Review Workflow

Start small, then scale:

```bash
$CP init
$CP map
$CP status
$CP review --limit 3 --jobs 3
$CP report
```

For large repos, use bounded batches:

```bash
$CP review --limit 10 --jobs 4 --rate-limit-per-minute 20
```

Useful filters and selectors:

```bash
$CP review --feature <feature-id>
$CP review --project <name-or-root>
$CP review --severity high --limit 5
$CP review --mode deslopify --limit 5
```

Use `--json` when another script or agent needs structured output. For `report --json`, prefer `total` and `items`; older aliases such as `results` and numeric `findings` may be deprecated.

## Triage Findings

Inspect findings before changing code:

```bash
$CP next
$CP show --finding <id>
$CP report --output .clawpatch/reports/latest.md
```

Update finding status when the user asks for triage or when evidence is clear:

```bash
$CP triage --finding <id> --status false-positive --note "covered by existing validation"
$CP triage --finding <id> --status wont-fix --note "accepted tradeoff"
```

Common statuses: `open`, `fixed`, `wont-fix`, `false-positive`, `uncertain`.

## Explicit Fix Loop

Fix one finding at a time:

```bash
$CP show --finding <id>
$CP fix --finding <id>
git diff
```

After reviewing the diff, run the repository's normal validation commands and then ask Clawpatch to re-check:

```bash
$CP revalidate --finding <id>
$CP report
```

If `fix` refuses because the source worktree is dirty, preserve user changes. Either finish/commit/stash only with explicit user approval, or configure an isolated branch/worktree before rerunning.

## CI And PRs

For CI-style reports:

```bash
$CP ci --since origin/main --output clawpatch-report.md
```

Opening a PR is an explicit publishing step:

```bash
$CP open-pr --patch <patchAttemptId> --draft
```

Only use `open-pr` when the user asks to publish the patch attempt. Review the diff and patch metadata first.

## Configuration

Config is loaded from `--config`, `CLAWPATCH_CONFIG`, `CLAWPATCH_STATE_DIR/config.json`, `clawpatch.config.json`, `.clawpatch/config.json`, then built-in defaults.

Common environment overrides:

```bash
CLAWPATCH_STATE_DIR=.clawpatch
CLAWPATCH_PROVIDER=codex
CLAWPATCH_MODEL=<model>
CLAWPATCH_REASONING_EFFORT=medium
CLAWPATCH_CODEX_SANDBOX=<codex-sandbox-mode>
```

Generated state is project-local by default:

```text
.clawpatch/
  config.json
  project.json
  features/*.json
  findings/*.json
  patches/*.json
  reports/*.md
  runs/*.json
```

## Safety Defaults

- Prefer `--root <path>` when operating outside the current working directory.
- Keep `.clawpatch/` state unless the user asks to remove it.
- Use `clean-locks` only for stale interrupted runs.
- Do not use destructive git commands to satisfy Clawpatch clean-worktree requirements.
- Summarize findings with severity, confidence, affected files, and recommended next action.

## Upstream Reference

If behavior or flags are unclear, check the current upstream docs:

- `https://clawpatch.ai/`
- `https://github.com/openclaw/clawpatch`
- `https://github.com/openclaw/clawpatch/tree/main/docs`
