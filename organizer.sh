#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
archive_dir="$script_dir/archive"
workspace_file="$script_dir/grades.csv"
source_input="${1:-$workspace_file}"
timestamp="$(date +"%Y%m%d-%H%M%S")"
source_basename="$(basename "$source_input")"
source_stem="${source_basename%.csv}"
archived_file="${source_stem}_${timestamp}.csv"
log_file="$script_dir/organizer.log"
csv_header="assignment,group,score,weight"

mkdir -p "$archive_dir"

if [[ "${source_input##*.}" != "csv" ]]; then
  printf 'Error: Expected a .csv file, got "%s".\n' "$source_input" >&2
  exit 1
fi

if [[ ! -f "$source_input" ]]; then
  printf 'Error: File not found: %s\n' "$source_input" >&2
  exit 1
fi

mv "$source_input" "$archive_dir/$archived_file"
printf '%s\n' "$csv_header" > "$workspace_file"

printf '%s | %s | %s\n' \
  "$timestamp" \
  "$source_input" \
  "$archive_dir/$archived_file" >> "$log_file"

printf 'Archived %s to %s\n' "$source_input" "$archive_dir/$archived_file"
printf 'Created fresh working file at %s\n' "$workspace_file"
