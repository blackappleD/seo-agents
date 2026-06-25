#!/usr/bin/env bash
set -euo pipefail

find_python() {
  for candidate in python3 python; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      if "${candidate}" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
        printf '%s\n' "${candidate}"
        return 0
      fi
    fi
  done
  return 1
}

PYTHON_BIN="$(find_python)" || {
  echo "Python 3.10+ is required but was not found." >&2
  exit 1
}

command -v git >/dev/null 2>&1 || {
  echo "Git is required but was not found." >&2
  exit 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON_BIN}" "${SCRIPT_DIR}/scripts/install.py" "$@"
