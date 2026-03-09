#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/check-dependencies.sh"
require_cmds rsync

usage() {
  cat <<'USAGE'
Usage: sync-skills.sh [options]

Synchronize skill directories from this repo into a Codex skills root.

Options:
  --source DIR         Source repository root (default: script directory)
  --dest DIR           Destination skills root (default: ${CODEX_HOME:-$HOME/.codex}/skills)
  --skill NAME         Sync only this skill (can be repeated)
  --skills a,b,c       Sync a comma-separated list of skills
  --dry-run            Show what would happen without writing changes
  --no-delete          Do not delete extra files in destination skill directories
  --prune              Remove destination skill directories that no longer exist upstream
  --force              Required with --prune (prevents accidental destructive cleanup)
  -h, --help          Show this message and exit

Examples:
  ./scripts/sync-skills.sh
  ./scripts/sync-skills.sh --dest "$CODEX_HOME/skills" --dry-run
  ./scripts/sync-skills.sh --skill gh-cli --skill modern-python
  ./scripts/sync-skills.sh --prune --force
USAGE
}

die() {
  echo "error: $*" >&2
  exit 1
}

SCRIPT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

source_dir=""
dest_root="${CODEX_HOME:-$HOME/.codex}/skills"
delete=true
dry_run=false
prune=false
force=false
selected_skills=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_dir="${2-}"
      [[ -n "${source_dir}" ]] || die "--source requires a directory path"
      shift 2
      ;;
    --dest)
      dest_root="${2-}"
      [[ -n "${dest_root}" ]] || die "--dest requires a directory path"
      shift 2
      ;;
    --skill)
      skill_name="${2-}"
      [[ -n "$skill_name" ]] || die "--skill requires a value"
      selected_skills+=("$skill_name")
      shift 2
      ;;
    --skills)
      IFS=',' read -r -a parsed <<< "${2-}"
      if [[ ${#parsed[@]} -eq 0 || -z "${parsed[0]}" ]]; then
        die "--skills requires a comma-separated list"
      fi
      for skill in "${parsed[@]}"; do
        selected_skills+=("$skill")
      done
      shift 2
      ;;
    --dry-run)
      dry_run=true
      shift
      ;;
    --no-delete)
      delete=false
      shift
      ;;
    --prune)
      prune=true
      shift
      ;;
    --force)
      force=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

source_dir="${source_dir:-$SCRIPT_DIR}"

if [[ ! -d "$source_dir" ]]; then
  die "Source directory not found: $source_dir"
fi

if [[ ! -d "$dest_root" ]]; then
  mkdir -p "$dest_root"
fi

if ! [[ -w "$dest_root" ]]; then
  die "Destination is not writable: $dest_root"
fi

all_skill_paths=()
while IFS= read -r -d '' path; do
  all_skill_paths+=("$path")
done < <(find "$source_dir" -mindepth 1 -maxdepth 1 -type d -print0)

all_skills=()
for path in "${all_skill_paths[@]}"; do
  skill_name="${path##*/}"

  [[ "$skill_name" == .* ]] && continue
  [[ -f "$path/SKILL.md" ]] || continue
  all_skills+=("$skill_name")
done

if (( ${#selected_skills[@]} == 0 )); then
  selected_skills=("${all_skills[@]}")
  all_mode=true
else
  all_mode=false
fi

if (( ${#selected_skills[@]} == 0 )); then
  die "No skills found in source: $source_dir"
fi

for skill in "${selected_skills[@]}"; do
  if ! [[ -f "$source_dir/$skill/SKILL.md" ]]; then
    die "Skill '$skill' not found in source: $source_dir/$skill"
  fi
done

sync_options=(--archive --checksum)
if [[ "$delete" == true ]]; then
  sync_options+=(--delete)
fi
if [[ "$dry_run" == true ]]; then
  sync_options+=(--dry-run)
fi

for skill in "${selected_skills[@]}"; do
  src="$source_dir/$skill/"
  dst="$dest_root/$skill/"

  mkdir -p "$dst"
  echo "Syncing: $skill"
  rsync "${sync_options[@]}" "$src" "$dst"
done

if [[ "$prune" == true ]]; then
  if [[ "$all_mode" == false ]]; then
    echo "--prune is only applied when syncing all discovered skills."
    exit 0
  fi

  if [[ "$force" == false ]]; then
    die "--prune requires --force because it removes destination skill directories"
  fi

  while IFS= read -r -d '' candidate; do
    skill_name="${candidate##*/}"

    [[ "$skill_name" == .* ]] && continue
    if [[ -f "$source_dir/$skill_name/SKILL.md" ]]; then
      continue
    fi

    if [[ "$dry_run" == true ]]; then
      echo "[prune] would remove stale skill directory: $candidate"
    else
      echo "[prune] removing stale skill directory: $candidate"
      rm -rf "$candidate"
    fi
  done < <(find "$dest_root" -mindepth 1 -maxdepth 1 -type d -print0)
fi
