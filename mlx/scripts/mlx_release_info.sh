#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is required for mlx_release_info.sh" >&2
  exit 1
fi

repos=("ml-explore/mlx" "ml-explore/mlx-lm")

for repo in "${repos[@]}"; do
  tmp_json="$(mktemp)"
  gh api "repos/$repo/releases/latest" --jq '{tag: .tag_name, published_at: .published_at, url: .html_url}' > "$tmp_json"
  python3 - "$repo" "$tmp_json" <<'PY'
import json
import pathlib
import sys

repo = sys.argv[1]
path = pathlib.Path(sys.argv[2])
data = json.loads(path.read_text())
data["repo"] = repo
print(json.dumps(data))
PY
  rm -f "$tmp_json"
done
