#!/bin/bash

# NetAssassin - Professional Linux Setup Script
# Developed for Kali Linux, Parrot OS, and Debian-based systems.

# 1. Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then 
  echo "[-] Error: Please run this script with sudo."
  exit 1
fi

echo "[*] Starting NetAssassin installation..."

# 2. Handle Python dependencies
if [ -f "requirements.txt" ]; then
    echo "[*] Checking for dependencies in requirements.txt..."
    # This covers both standard pip and Debian's managed environments
    python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
fi

# 3. Prepare the main script
echo "[*] Configuring execution permissions..."
chmod +x netassassin.py

# 4. Create the Global Command (The .py remover)
# We link the script to /usr/local/bin/ and rename the link 'netassassin'
echo "[*] Creating global system link: /usr/local/bin/netassassin"
ln -sf "$(pwd)/netassassin.py" /usr/local/bin/netassassin

# 5. Setup Local History Directory
# We want the folder to be in the user's home, not the root's home.
REAL_USER=$SUDO_USER
USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)

echo "[*] Initializing local history at $USER_HOME/.netassassin"
mkdir -p "$USER_HOME/.netassassin"
chown "$REAL_USER":"$REAL_USER" "$USER_HOME/.netassassin"

echo ""
echo "=========================================================="
echo " [+] NetAssassin Installation Successful!"
echo " [+] You can now use the command: netassassin"
echo "=========================================================="
echo ""
