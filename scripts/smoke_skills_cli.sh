#!/usr/bin/env bash
set -euo pipefail

source_dir="$(cd "${1:-.}" && pwd)"
work_dir="$(mktemp -d -t project-to-resume-skills-cli-XXXXXX)"
trap 'rm -rf "$work_dir"' EXIT

export CI=1
export DO_NOT_TRACK=1
export NO_COLOR=1

cd "$work_dir"

cli_help="$(npx --yes skills@1 add --help 2>&1)"
if ! grep -q -- '--agent' <<<"$cli_help"; then
  echo "skills CLI no longer exposes the expected --agent option" >&2
  exit 1
fi

args=(add "$source_dir" --yes --agent codex)
if grep -q -- '--copy' <<<"$cli_help"; then
  args+=(--copy)
fi

npx --yes skills@1 "${args[@]}"

skill_file="$(find -L "$work_dir" -type f -path '*/project-to-resume/SKILL.md' -print -quit)"
if [[ -z "$skill_file" ]]; then
  echo "skills CLI did not install project-to-resume into the isolated workspace" >&2
  find "$work_dir" -maxdepth 5 -print >&2
  exit 1
fi

installed_dir="$(dirname "$skill_file")"
python3 "$source_dir/scripts/validate_package.py" "$installed_dir"
printf 'skills CLI install valid: %s\n' "$installed_dir"
