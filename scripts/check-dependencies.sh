#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: check-dependencies.sh command...

Check required commands and print platform install hints when missing.
USAGE
}

package_name() {
  case "$1" in
    rg) echo "ripgrep" ;;
    *) echo "$1" ;;
  esac
}

print_install_hints() {
  if [[ ${#MISSING[@]} -eq 0 ]]; then
    return
  fi

  local join=""
  local packages=()
  for cmd in "${MISSING[@]}"; do
    packages+=("$(package_name "$cmd")")
  done
  join="$(printf "%s " "${packages[@]}")"

  echo "" >&2
  echo "Missing required command(s): ${MISSING[*]}" >&2
  if [[ "$(uname -s)" == Darwin* ]]; then
    echo "Install with Homebrew: brew install ${join% }" >&2
  elif command -v apt-get >/dev/null 2>&1; then
    echo "Install with apt: sudo apt-get update && sudo apt-get install -y ${join% }" >&2
  elif command -v dnf >/dev/null 2>&1; then
    echo "Install with dnf: sudo dnf install -y ${join% }" >&2
  elif command -v pacman >/dev/null 2>&1; then
    echo "Install with pacman: sudo pacman -Syu --needed ${join% }" >&2
  elif command -v yum >/dev/null 2>&1; then
    echo "Install with yum: sudo yum install -y ${join% }" >&2
  elif command -v apk >/dev/null 2>&1; then
    echo "Install with apk: sudo apk add --no-cache ${join% }" >&2
  else
    echo "Install these tools using your OS package manager:" >&2
    echo "  ${packages[*]}" >&2
  fi
}

require_cmds() {
  local missing=()
  local cmd

  for cmd in "$@"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      missing+=("$cmd")
    fi
  done

  if (( ${#missing[@]} > 0 )); then
    MISSING=("${missing[@]}")
    print_install_hints
    exit 1
  fi
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  if (( $# == 0 )); then
    usage
    exit 1
  fi
  require_cmds "$@"
fi
