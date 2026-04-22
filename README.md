NetAssassin 🎯



🛠️ Installation and Setup Guide

Follow these steps to install and start using NetAssassin on your system:

1. Prerequisites

- Python 3.6+ installed.
- Linux (Kali, Parrot, Ubuntu) or macOS.
- Root privileges (Recommended for full socket access).

2. Download and Quick Start

Clone the repository

git clone https://github.com/Tafily91/NetAssassin.git

cd netassassin

Run the automated setup script

chmod +x setup.sh

sudo ./setup.sh



💻 Usage

netassassin

netassassin -t 192.168.1.1 -p 1-1024

netassassin -t 192.168.1.0/24 -p 80,443 -a

netassassin --history

📊 Arguments Reference

Argument    	 Short	      Description
--target	     -t         	Target IP, Domain, or CIDR range
--ports	       -p	          Specific ports (e.g., 80,443 or 1-1000)
--aggressive   -a           Enable banner grabbing for service info
--history	                  View your last 20 scan results
--help	      -h           	Show the help menu


⚠️ Security & Legal Notice

IMPORTANT: NetAssassin is intended for educational and authorized security testing purposes only.

Do NOT use this tool to scan networks or systems without explicit permission. Unauthorized access to computer systems is illegal. 

The author is not responsible for any misuse of this software. Always stay ethical and test responsibly.
