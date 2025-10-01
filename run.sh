#!/usr/bin/env bash
# Simple runner for Lingrow app
# Usage: ./run.sh

set -euo pipefail

# change to script directory (so it works when double-clicked from Finder if using .command)
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo ".venv not found — creating a virtual environment..."
  python3 -m venv .venv
  echo "Virtual environment created at ./.venv"
  echo "Activating .venv..."
  # shellcheck disable=SC1091
  source .venv/bin/activate
  echo "Upgrading pip..."
  pip install --upgrade pip
  # Offer to install optional image libraries for better image support
  read -r -p "Install optional image libraries (pillow, cairosvg)? [Y/n] " reply
  reply=${reply:-Y}
  if [[ $reply =~ ^[Yy]$ ]]; then
    echo "Installing pillow and cairosvg..."
    pip install pillow cairosvg
  else
    echo "Skipping optional image libraries. You can install them later with: pip install pillow cairosvg"
  fi
else
  # activate existing venv
  echo "Activating existing .venv"
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "Running main.py..."
python3 main.py

