#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
archive_dir="$script_dir/archive"
workspace_file="$script_dir/grades.csv"
source_input="${1:-$workspace_file}"
timestamp="$(date +"%Y%m%d-%H%M%S")"
log_file="$script_dir/organizer.log"
csv_header="assignment,group,score,weight"

print_usage() {
  cat <<EOF
Usage: bash organizer.sh [csv_file]

Archives the selected CSV file into the archive folder, then creates a fresh
working grades.csv file with the expected header.
EOF
}

ensure_csv_file() {
  if [[ "${source_input##*.}" != "csv" ]]; then
    printf 'Error: Expected a .csv file, got "%s".\n' "$source_input" >&2
    exit 1
  fi

  if [[ ! -f "$source_input" ]]; then
    printf 'Error: File not found: %s\n' "$source_input" >&2
    exit 1
  fi
}

ensure_archive_dir() {
  mkdir -p "$archive_dir"
}

build_archive_name() {
  local source_basename source_stem
  source_basename="$(basename "$source_input")"
  source_stem="${source_basename%.csv}"
  archived_file="${source_stem}_${timestamp}.csv"
}

is_header_only_file() {
  local line_count
  line_count="$(wc -l < "$source_input")"
  [[ "$line_count" -le 1 ]]
}

write_log_entry() {
  printf '%s | %s | %s\n' \
    "$timestamp" \
    "$source_input" \
    "$archive_dir/$archived_file" >> "$log_file"
}

reset_workspace_file() {
  printf '%s\n' "$csv_header" > "$workspace_file"
}

archive_source_file() {
  mv "$source_input" "$archive_dir/$archived_file"
  write_log_entry
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  print_usage
  exit 0
fi

ensure_archive_dir
ensure_csv_file
build_archive_name

if is_header_only_file; then
  printf 'Notice: %s only contains the header, so no archive was created.\n' "$source_input"
  reset_workspace_file
  printf 'Ready for new records in %s\n' "$workspace_file"
  exit 0
fi

archive_source_file
reset_workspace_file

printf 'Archived %s to %s\n' "$source_input" "$archive_dir/$archived_file"
printf 'Created fresh working file at %s\n' "$workspace_file"
