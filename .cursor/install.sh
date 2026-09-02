#!/usr/bin/env bash
set -euo pipefail

# Resolve repository root (parent of the .cursor directory holding this script).
cd "$(dirname "$0")/.."

# The default image ships Python 3.12 but may lack venv/ensurepip support.
# Snapshots already include it; guard so fresh images bootstrap too.
if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-venv
fi

python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
