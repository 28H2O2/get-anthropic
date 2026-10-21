#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$SCRIPT_DIR/logs"
LOG_FILE="$SCRIPT_DIR/logs/$(date +%Y-%m-%d).log"
python3 "$SCRIPT_DIR/main.py" "$@" >> "$LOG_FILE" 2>&1
python3 "$SCRIPT_DIR/build_data.py" >> "$LOG_FILE" 2>&1
python3 "$SCRIPT_DIR/main.py" --check-health >> "$LOG_FILE" 2>&1
