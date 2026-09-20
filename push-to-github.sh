#!/usr/bin/env bash
# Commit everything and push to Theo's GitHub repo.
# Called by "Push to GitHub.command"; can also be run from a terminal.
set -euo pipefail
cd "$(dirname "$0")"

REPO_NAME="ssac-splitsecond"
OWNER="theoq71"
AUTHOR_NAME="theoq71"
AUTHOR_EMAIL="133422938+theoq71@users.noreply.github.com"

# Clear leftovers from interrupted git runs.
rm -f .git/*.lock 2>/dev/null || true
rm -f .git/objects/tmp_obj_* 2>/dev/null || true
rm -rf _to_delete 2>/dev/null || true

if [ ! -d .git ]; then
  git init -q
fi
git config user.name "$AUTHOR_NAME"
git config user.email "$AUTHOR_EMAIL"
git symbolic-ref HEAD refs/heads/main 2>/dev/null || git checkout -q main

git add -A

# Never push settings or secrets by accident.
if git ls-files | grep -Ei '(^|/)\.env|secret|password|settings\.json' ; then
  echo "Stop: the files above look like settings or secrets. Remove them or add them to .gitignore."
  exit 1
fi

if ! git diff --cached --quiet || ! git rev-parse HEAD >/dev/null 2>&1; then
  git -c user.name="$AUTHOR_NAME" -c user.email="$AUTHOR_EMAIL" \
    commit -q --author="$AUTHOR_NAME <$AUTHOR_EMAIL>" -m "Update $(date +%Y-%m-%d)"
  echo "committed"
else
  echo "nothing new to commit"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  if command -v gh >/dev/null 2>&1; then
    gh repo create "$OWNER/$REPO_NAME" --public --source=. --remote=origin
  else
    echo
    echo "No 'origin' remote yet and gh is not installed."
    echo "1. Sign in to GitHub as $OWNER and create an EMPTY public repo called $REPO_NAME (no README)."
    echo "2. Run this script again."
    git remote add origin "https://github.com/$OWNER/$REPO_NAME.git"
    exit 1
  fi
fi

git push --force -u origin main
echo
echo "Pushed. Check https://github.com/$OWNER/$REPO_NAME"
