# GitHub CLI Helpers

These helper scripts are available from this skill root at `gh-cli/scripts/`:

- `github-url-to-gh.sh` — map GitHub URLs to preferred `gh` workflows.
- `gh-auth-audit.sh` — check whether `gh` is authenticated and report token scope coverage.
- `gh-api-safe.sh` — safely run `gh api` with basic auth/rate-limit/error handling.
- `extract-repo.sh` — clone a repo to a deterministic path for local inspection.
- `git-lfs-usage.sh` — quick script for common Git LFS repository inspection.

## Recommended local invocation pattern

From a shell script:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/github-url-to-gh.sh" "https://github.com/owner/repo"
```

## Common one-liners

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/gh-auth-audit.sh"
"$SCRIPT_DIR/github-url-to-gh.sh" --meta owner/repo
"$SCRIPT_DIR/extract-repo.sh" owner/repo /tmp/repo-checkout
"$SCRIPT_DIR/gh-api-safe.sh" /repos/owner/repo/issues
"$SCRIPT_DIR/git-lfs-usage.sh" owner/repo
```

