#!/bin/bash
# NetAssassin Installation Script

echo "[*] Initializing NetAssassin Setup..."

if ! command -v python3 &> /dev/null; then
    echo "[-] Error: Python3 is required. Please install it to continue."
    exit 1
fi

# Set permissions for execution
chmod +x netassassin.py
mkdir -p "$HOME/.netassassin"

echo "[*] Creating system link in /usr/local/bin..."
sudo ln -sf "$(pwd)/netassassin.py" /usr/local/bin/netassassin

echo "[+] Installation complete. You can now run the tool using: netassassin"
