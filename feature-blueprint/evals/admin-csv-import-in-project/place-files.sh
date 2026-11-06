#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
# Stored under another name so that the skill's repository holds no CLAUDE.md.
mv project-CLAUDE.md CLAUDE.md
