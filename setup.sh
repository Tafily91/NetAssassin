#!/bin/bash
echo "Installing NetAssassin..."

# Check requirements
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Install it first."
    exit 1
fi

# Permissions
chmod +x netassassin.py

# Create system link
echo "[*] Creating symlink to /usr/local/bin/netassassin"
sudo ln -sf "$(pwd)/netassassin.py" /usr/local/bin/netassassin

# Setup history dir
mkdir -p "$HOME/.netassassin"

echo "Done. Type 'netassassin' to start."