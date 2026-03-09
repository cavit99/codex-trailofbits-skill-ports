#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../scripts/check-dependencies.sh"
require_cmds gh git

if [[ -z ${1-} ]]; then
  echo "Usage: git-lfs-usage.sh owner/repo" >&2
  exit 1
fi

repo=${1-}
tmpdir="${TMPDIR:-/tmp}/codex-gh-ls-${RANDOM}-${RANDOM}"

mkdir -p "$tmpdir"
trap 'rm -rf "$tmpdir"' EXIT

gh repo view "$repo" \
  --json name,description,defaultBranchRef,url,licenseInfo,isFork,createdAt,updatedAt,stargazerCount,forkCount,openGraphImageUrl

gh repo clone "$repo" "$tmpdir/repo" -- --depth 1 >/dev/null
cd "$tmpdir/repo"

echo "Tracked files:"
git ls-files

count=$(git ls-files | wc -l | tr -d '[:space:]')
echo "\nTracked file count: $count"

echo "Root path: $tmpdir/repo"
