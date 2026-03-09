#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../scripts/check-dependencies.sh"
require_cmds gh rg

status_raw="$(gh auth status 2>&1 || true)"
echo "$status_raw"

if ! echo "$status_raw" | rg -q "Logged in to github.com"; then
  echo "AUTH_STATUS=missing"
  exit 2
fi

scopes="$(echo "$status_raw" | rg -o "Token scopes: '.*'" | head -n1 || true)"
if [[ -z "$scopes" ]]; then
  echo "AUTH_STATUS=ok-no-scope-line"
  exit 0
fi

echo "AUTH_STATUS=ok"
echo "$scopes"

echo "$scopes" | rg -q "'repo'" || echo "WARN: repo scope missing"
echo "$scopes" | rg -q "'gist'" || echo "WARN: gist scope missing"
