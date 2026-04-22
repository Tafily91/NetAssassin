#!/bin/bash
echo "[*] NetAssassin Linux Setup..."
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 required."
    exit 1
fi
chmod +x netassassin.py
mkdir -p "$HOME/.netassassin"
echo "[*] Creating system link..."
sudo ln -sf "$(pwd)/netassassin.py" /usr/local/bin/netassassin
echo "[+] Done. Run with: netassassin"
