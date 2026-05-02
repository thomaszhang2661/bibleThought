#!/bin/bash
set -e
cd "$(dirname "$0")"

python3 generate_index.py

git add -A

if git diff --cached --quiet; then
  echo "没有改动，无需推送"
  exit 0
fi

git commit -m "更新笔记"
git push
echo "推送完成"
