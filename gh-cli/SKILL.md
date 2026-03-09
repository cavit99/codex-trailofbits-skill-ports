---
name: gh-cli
description: Prefer authenticated GitHub CLI workflows over unauthenticated curl, wget, raw GitHub URLs, or web fetches when Codex needs to inspect GitHub repositories, files, trees, pull requests, issues, releases, Actions runs, gists, or GitHub API endpoints. Use when a task includes github.com, api.github.com, raw.githubusercontent.com, gist.github.com, private GitHub repos, rate-limit-sensitive GitHub access, or an explicit request to use gh.
---

# gh-cli

Use authenticated `gh` workflows for GitHub work.

## Operating Rules

1. Check whether `gh` is available before relying on it.
2. Prefer `gh` over `curl`, `wget`, raw GitHub URLs, or web fetches for:
   - `github.com`
   - `api.github.com`
   - `raw.githubusercontent.com`
   - `gist.github.com`
3. Treat repo file access as a local-read problem, not an API-decoding problem.
4. Fall back to ordinary web access only when `gh` is unavailable, unauthenticated, or the target is not really GitHub repo data.

## Quick Checks

Use:

```bash
command -v gh
gh auth status
```

If `gh` is missing or unauthenticated, say so briefly and use the next best approach.

If you need explicit auth diagnostics:

```bash
GH_CLI_SKILL_ROOT="${GH_CLI_SKILL_ROOT:-}"
if [ -z "${GH_CLI_SKILL_ROOT}" ]; then
  if [ -x "$(pwd)/gh-cli/scripts/gh-auth-audit.sh" ]; then
    GH_CLI_SKILL_ROOT="$(pwd)"
  elif [ -x "$(pwd)/scripts/gh-auth-audit.sh" ] && [ -f "$(pwd)/SKILL.md" ]; then
    GH_CLI_SKILL_ROOT="$(cd "$(dirname "$(pwd)")" && pwd)"
  elif [ -x "$(dirname "$(pwd)")/gh-cli/scripts/gh-auth-audit.sh" ]; then
    GH_CLI_SKILL_ROOT="$(cd "$(dirname "$(pwd)")" && pwd)"
  elif [ -x "${CODEX_HOME:-$HOME/.codex}/skills/gh-cli/scripts/gh-auth-audit.sh" ]; then
    GH_CLI_SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
  else
    GH_CLI_SKILL_ROOT="$(pwd)"
  fi
fi
if [ -x "${GH_CLI_SKILL_ROOT}/scripts/gh-auth-audit.sh" ] && [ -f "${GH_CLI_SKILL_ROOT}/SKILL.md" ]; then
  GH_CLI_SKILL_ROOT="$(cd "$(dirname "${GH_CLI_SKILL_ROOT}")" && pwd)"
fi
if [ ! -x "${GH_CLI_SKILL_ROOT}/gh-cli/scripts/gh-auth-audit.sh" ]; then
  echo "Set GH_CLI_SKILL_ROOT to the parent directory that contains the 'gh-cli/' folder."
  exit 1
fi
"${GH_CLI_SKILL_ROOT}/gh-cli/scripts/gh-auth-audit.sh"
```

For stable metadata retrieval, use:

```bash
"${GH_CLI_SKILL_ROOT}/gh-cli/scripts/github-url-to-gh.sh" --meta owner/repo
```

This helper uses `defaultBranchRef` instead of the deprecated `defaultBranch` field.

## Preferred Replacements

Map common GitHub tasks to `gh` commands:

- Repo page: `gh repo view owner/repo`
- Clone repo for inspection: `gh repo clone owner/repo <dest> -- --depth 1`
- Pull requests list: `gh pr list --repo owner/repo`
- Pull request view: `gh pr view <number> --repo owner/repo`
- Issues list: `gh issue list --repo owner/repo`
- Issue view: `gh issue view <number> --repo owner/repo`
- Releases list: `gh release list --repo owner/repo`
- Release download: `gh release download --repo owner/repo`
- Actions runs: `gh run list --repo owner/repo`
- Gist view: `gh gist view <gist-id>`
- Generic API endpoint: `gh api <endpoint>`

When calling REST endpoints with query parameters, be explicit about the HTTP method:

- Use `gh api -X GET ... -f key=value` for list/search/read endpoints
- Do not rely on bare `-f` for these cases, because `gh api` may switch the request to `POST`

Common examples:

- Commits since a timestamp:
  - `gh api -X GET repos/owner/repo/commits -f since=... -f per_page=10`
- Repository search:
  - `gh api -X GET search/repositories -f q='...' -f sort=updated -f order=desc`

## URL Handling

Translate GitHub URLs into `gh` workflows:

- `https://github.com/owner/repo`
  - Use `gh repo view owner/repo`
- `https://github.com/owner/repo/pull/123`
  - Use `gh pr view 123 --repo owner/repo`
- `https://github.com/owner/repo/issues/45`
  - Use `gh issue view 45 --repo owner/repo`
- `https://api.github.com/repos/owner/repo/pulls`
  - Use `gh pr list --repo owner/repo`
- `https://api.github.com/repos/owner/repo/issues`
  - Use `gh issue list --repo owner/repo`
- `https://api.github.com/...`
  - Use `gh api ...`

## Repo File Access

Do not fetch repository files via:

- `curl` or `wget` against `raw.githubusercontent.com`
- `gh api repos/<owner>/<repo>/contents/...`
- base64-decoding `/contents` responses

Instead:

1. Create a temporary clone destination.
2. Shallow-clone the repo with `gh repo clone`.
3. Read the needed files locally.
4. Remove the temporary clone when it is no longer needed and cleanup is safe.

Example:

```bash
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/codex-gh-repo.XXXXXX")"
gh repo clone owner/repo "$tmpdir/repo" -- --depth 1
```

Apply the same rule to:

- `github.com/.../blob/...`
- `github.com/.../tree/...`
- `raw.githubusercontent.com/...`

To inspect a full repo quickly:

```bash
"${GH_CLI_SKILL_ROOT}/gh-cli/scripts/git-lfs-usage.sh" owner/repo
```

## Pass-Through Cases

Do not force `gh` for:

- Non-GitHub domains
- `*.github.io` pages
- Existing `git clone`, `git fetch`, `git push`, or other normal git workflows
- Local search commands that merely mention GitHub URLs

## Working Style

When this skill is active:

1. Prefer `gh` first for GitHub metadata and authenticated access.
2. Prefer a shallow clone for repository file contents.
3. Avoid unauthenticated GitHub fetches unless there is no better option.
4. State the fallback clearly if `gh` cannot be used.
5. For REST reads with query params, force `-X GET` so search and commit endpoints do not fail due to an accidental `POST`.

## Helper Scripts

- `${GH_CLI_SKILL_ROOT}/gh-cli/scripts/github-url-to-gh.sh <github_url>`  
  Map URL forms to stable `gh` commands.
- `${GH_CLI_SKILL_ROOT}/gh-cli/scripts/extract-repo.sh owner/repo [dest]`  
  Shallow-clone to a deterministic local path and print cleanup command.
- `${GH_CLI_SKILL_ROOT}/gh-cli/scripts/gh-api-safe.sh <endpoint>`  
  Call `gh api` with error handling for auth/rate/access failures.

## Helper

Use this helper for deterministic URL-to-`gh` mapping:

```bash
"${GH_CLI_SKILL_ROOT}/gh-cli/scripts/github-url-to-gh.sh" <github_url>
```
