#!/bin/sh
set -e
f=/ws/sgdailyhub/site/scripts/update_study.py
tmp=/tmp/update_study.py
old='        ("Explain why Group 1 metals form +1 ions.", "They lose 1 valence electron to achieve a stable configuration."),'
new='        ("How many moles are in 4.90 g of H2SO4 (Mr = 98)?", "0.050 mol"),'
while IFS= read -r line; do
  if [ "$line" = "$old" ]; then
    echo "$new" >> "$tmp"
  else
    echo "$line" >> "$tmp"
  fi
done < "$f"
mv "$tmp" "$f"
grep -n 'Group 1 metals\|H2SO4 (Mr = 98)' "$f" || true
