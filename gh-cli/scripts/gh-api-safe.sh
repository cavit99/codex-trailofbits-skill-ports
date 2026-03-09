#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../scripts/check-dependencies.sh"
require_cmds gh rg

if [[ -z ${1-} ]]; then
  echo "Usage: gh-api-safe.sh <endpoint>" >&2
  exit 1
fi

endpoint=$1
max_attempts=3
attempt=1

while [[ $attempt -le $max_attempts ]]; do
  if output="$(gh api "$endpoint" 2>&1)"; then
    echo "$output"
    exit 0
  fi

  msg="$output"
  code=""
  if echo "$msg" | rg -q 'HTTP (401|403|404)'; then
    code=$(echo "$msg" | rg -o 'HTTP [0-9]+' | head -n1 | awk '{print $2}')
  fi

  if [[ "$code" == "401" || "$code" == "403" ]]; then
    echo "Auth issue: check gh auth status and token scopes" >&2
    exit 2
  fi

  if [[ "$code" == "404" ]]; then
    echo "Endpoint not found or no access for endpoint: $endpoint" >&2
    exit 3
  fi

  if [[ "$attempt" -eq "$max_attempts" ]]; then
    echo "$msg" >&2
    exit 4
  fi

  sleep $((attempt))
  attempt=$((attempt + 1))
done
