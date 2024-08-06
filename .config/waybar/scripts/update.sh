#!/usr/bin/env bash

# This file is part of 'custom/updates' module

LOG="/tmp/update_$(date +%F_%T).log"
MANAGERS=("dnf")

for manager in "${MANAGERS[@]}"; do
  if which $manager &>/dev/null; then
    $manager update -y >"$LOG" 2>&1
    exit 0
  fi
done

echo -e "No known package manager found.\nUpdate failed.">>"$LOG"
exit 1
