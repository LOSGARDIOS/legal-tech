#!/usr/bin/env bash
# PreToolUse hook (Write|Edit): before touching the core Los Gardios legal
# documents, remind the model to read AUDIT_SYNTHESIS.md and check recent
# git history for that file first, so it doesn't redo or contradict work
# already done (e.g. by a parallel background agent).
set -euo pipefail

input="$(cat)"
file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')"
[ -z "$file_path" ] && exit 0

base="$(basename "$file_path")"
case "$base" in
  AGREEMENT_SHORT_HE.md|CLIENT_GUIDE_HE.md) ;;
  *) exit 0 ;;
esac

dir="$(dirname "$file_path")"
log="$(cd "$dir" 2>/dev/null && git log --oneline -8 -- "$base" 2>/dev/null || true)"
[ -z "$log" ] && log="(no git history found for this file)"

context="Before editing $base: read AUDIT_SYNTHESIS.md in full first (the running decision/audit log for this project) to check whether this exact change was already made, reasoned about, or is being handled elsewhere (e.g. by a parallel background agent). Recent commits touching $base:
$log"

jq -n --arg ctx "$context" \
  '{hookSpecificOutput:{hookEventName:"PreToolUse",additionalContext:$ctx}}'
