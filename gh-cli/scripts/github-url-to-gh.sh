#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../scripts/check-dependencies.sh"
require_cmds gh

usage() {
  cat <<EOF
Usage:
  github-url-to-gh.sh --meta owner/repo
  github-url-to-gh.sh https://github.com/...|https://api.github.com/...|https://raw.githubusercontent.com/...|https://gist.github.com/...
EOF
}

if [[ ${1-} == "--meta" ]]; then
  shift
  if [[ -z ${1-} ]]; then
    usage
    exit 1
  fi
  gh repo view "$1" --json name,description,defaultBranchRef,url,licenseInfo,isFork,createdAt,updatedAt,stargazerCount,forkCount,openGraphImageUrl
  exit 0
fi

if [[ -z ${1-} ]]; then
  usage
  exit 1
fi

url=$1

case "$url" in
  https://api.github.com/*)
    path="${url#https://api.github.com/}"
    if [[ "$path" =~ ^repos/([^/]+)/([^/]+)/pulls ]]; then
      echo "gh pr list --repo ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    elif [[ "$path" =~ ^repos/([^/]+)/([^/]+)/issues ]]; then
      echo "gh issue list --repo ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    elif [[ "$path" =~ ^repos/([^/]+)/([^/]+)/contents ]]; then
      echo "gh repo clone ${BASH_REMATCH[1]}/${BASH_REMATCH[2]} \"${TMPDIR:-/tmp}/codex-gh-clones-${BASH_REMATCH[2]}\" -- --depth 1"
      echo "# then read files from the clone"
    elif [[ "$path" =~ ^repos/([^/]+)/([^/]+)/releases ]]; then
      echo "gh release list --repo ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    elif [[ "$path" =~ ^repos/([^/]+)/([^/]+)/actions ]]; then
      echo "gh run list --repo ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    else
      echo "gh api ${path}"
    fi
    ;;

  https://raw.githubusercontent.com/*)
    path="${url#https://raw.githubusercontent.com/}"
    if [[ "$path" =~ ^([^/]+)/([^/]+)/[^/]+/(.+) ]]; then
      echo "gh repo clone ${BASH_REMATCH[1]}/${BASH_REMATCH[2]} \"${TMPDIR:-/tmp}/codex-gh-clones-${BASH_REMATCH[2]}\" -- --depth 1"
      echo "# then read ${BASH_REMATCH[3]} from the clone"
    else
      echo "# Unrecognized raw URL; identify owner/repo and clone explicitly"
    fi
    ;;

  https://gist.github.com/*)
    path="${url#https://gist.github.com/}"
    if [[ "$path" =~ ^[^/]+/([^/]+) ]]; then
      echo "gh gist view ${BASH_REMATCH[1]}"
    else
      echo "# Pass gist URL details to gh gist view"
    fi
    ;;

  https://github.com/*)
    path="${url#https://github.com/}"
    if [[ "$path" =~ ^([^/]+)/([^/]+)/pull/([0-9]+) ]]; then
      echo "gh pr view ${BASH_REMATCH[3]} --repo ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    elif [[ "$path" =~ ^([^/]+)/([^/]+)/issues/([0-9]+) ]]; then
      echo "gh issue view ${BASH_REMATCH[3]} --repo ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    elif [[ "$path" =~ ^([^/]+)/([^/]+)/blob/.+ ]]; then
      echo "gh repo clone ${BASH_REMATCH[1]}/${BASH_REMATCH[2]} \"${TMPDIR:-/tmp}/codex-gh-clones-${BASH_REMATCH[2]}\" -- --depth 1"
      echo "# then read the target file from the clone"
    elif [[ "$path" =~ ^([^/]+)/([^/]+)/tree/.+ ]]; then
      echo "gh repo clone ${BASH_REMATCH[1]}/${BASH_REMATCH[2]} \"${TMPDIR:-/tmp}/codex-gh-clones-${BASH_REMATCH[2]}\" -- --depth 1"
      echo "# then inspect files under the clone"
    elif [[ "$path" =~ ^([^/]+)/([^/]+)$ ]]; then
      echo "gh repo view ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    else
      echo "# Unrecognized github.com URL shape"
    fi
    ;;

  *)
    echo "Not a supported GitHub URL: $url" >&2
    exit 1
    ;;
esac
