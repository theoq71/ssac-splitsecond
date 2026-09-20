#!/bin/bash
# Double-click on a Mac: sets up if needed, then runs the whole test suite.
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  ./setup.sh
fi
.venv/bin/python -m pytest
echo
read -n 1 -s -r -p "Press any key to close"
