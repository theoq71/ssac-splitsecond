#!/bin/bash
cd "$(dirname "$0")"
./push-to-github.sh
echo
read -n 1 -s -r -p "Press any key to close"
