#!/usr/bin/env bash
# One-time setup: make a virtual environment and install the dependencies.
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip >/dev/null
.venv/bin/python -m pip install -r requirements.txt
echo
echo "Done. Activate with:  source .venv/bin/activate"
