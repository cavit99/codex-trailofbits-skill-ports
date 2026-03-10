# Codex Trail of Bits Skill Ports

This repository contains Codex-adapted versions of selected skills from the Claude-oriented `trailofbits/skills` ecosystem.

## Included skills

- `audit-context-building`
- `gh-cli`
- `modern-python`
- `polymarket-api`

These were built as Codex-compatible `SKILL.md`-first ports while preserving the practical utility of the original Claude plugin workflows.

## Notes on provenance

The `gh-cli` skill started from ideas in:
https://github.com/trailofbits/skills/tree/main/plugins/gh-cli

`audit-context-building` and `modern-python` are also adapted to match Codex skill conventions.

## Usage

Install directly from this repo with the Codex skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo cavit99/codex-trailofbits-skill-ports \
  --path audit-context-building gh-cli modern-python polymarket-api
```

(Use `--path` values as needed for a subset.)

## Sync helper

This repo stores the source of truth for skill ports. Use this helper to keep your local Codex skills directory in sync with the repo:

```bash
./scripts/sync-skills.sh [options]
```

Defaults:

- source: this repo root
- destination: `$CODEX_HOME/skills` (falls back to `~/.codex/skills`)
- delete behavior: mirrors each synced skill directory (deletes files that were removed from the repo)

Common examples:

```bash
# Full sync (all known skills)
./scripts/sync-skills.sh

# Sync a single skill by name
./scripts/sync-skills.sh --skill gh-cli

# Preview what would change
./scripts/sync-skills.sh --dry-run

# Sync all, then remove stale skill dirs from the destination
./scripts/sync-skills.sh --prune --force
```

Use `--help` for the full options list.

## Dependencies

Before running helper scripts, ensure required commands are available:

- `gh` (GitHub CLI)
- `rg` (ripgrep)
- `rsync` (used by the sync helper)
- `git` (used by the GH helpers that clone/review repository contents)

You can check/install all required dependencies at once with:

```bash
./scripts/check-dependencies.sh gh rg rsync git
```

Examples:

- macOS: `brew install gh ripgrep rsync git`
- Ubuntu/Debian: `sudo apt-get install -y gh ripgrep rsync git`
- Fedora/RHEL: `sudo dnf install -y gh ripgrep rsync git`
