#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../scripts/check-dependencies.sh"
require_cmds gh git

if [[ -z ${1-} ]]; then
  echo "Usage: extract-repo.sh owner/repo [dest]" >&2
  exit 1
fi

repo=${1-}
dest="${2-}"

if [[ -z "$dest" ]]; then
  dest="${TMPDIR:-/tmp}/codex-gh-clones-${RANDOM}-${RANDOM}"
fi

mkdir -p "$dest"
echo "Cloning $repo into $dest"
gh repo clone "$repo" "$dest" -- --depth 1
trap 'rm -rf "$dest"' EXIT
echo "Repo path: $dest"
echo "Cleanup when done:"
echo "rm -rf \"$dest\""
