NetAssassin - Advanced Port Scanner 🎯

NetAssassin is a high-performance, multi-threaded network port scanner built for Kali Linux, Parrot OS, and Debian. It is designed for rapid network discovery, service identification, and security auditing.

Installation and Usage Guide

1. Prerequisites

- Python 3.6+ installed.
- Linux (Kali, Parrot, Ubuntu) or macOS.
- Root privileges (Recommended for full socket access).

Step 1: Clone the Project

Clone the repository

git clone https://github.com/Tafily91/NetAssassin.git

cd netassassin

pip3 install -r requirements.txt

chmod +x setup.sh netassassin.py

sudo ./setup.sh



💻 Usage

netassassin

netassassin -t 192.168.1.1 -p 1-1024

netassassin -t 192.168.1.0/24 -p 80,443 -a

netassassin --history

# Arguments Reference
  
-t		                       Target IP address, domain name, or CIDR range.   --target


-p	  --ports		            Specific ports (e.g., 80,443) or ranges (e.g., 1-1000).


-a  	--aggressive         	Enables banner grabbing to identify service versions.


-i	  --interactive           	Launches the tool in the guided menu-driven mode.


-h	  --help		            Displays the help menu with all available options.


--history		                 Displays your last 20 scans from local storage.
 

Usage Examples
1. Scan a Website (Common Ports):
code
Bash


Pro-Tips for Arguments:

Target Flexibility: You can use a single IP (192.168.1.1), a website (example.com), or a whole network range (192.168.1.0/24).

Port Selection: If you don't specify the -p flag, NetAssassin defaults to scanning the most common 1-1024 ports.

Permissions: For scanning large ranges or protected ports, it is always recommended to run the tool with sudo:




⚠️ Security & Legal Notice

IMPORTANT: NetAssassin is intended for educational and authorized security testing purposes only.

Do NOT use this tool to scan networks or systems without explicit permission. Unauthorized access to computer systems is illegal. 

The author is not responsible for any misuse of this software. Always stay ethical and test responsibly.


Stay Secure. Test Responsibly. 🔒
