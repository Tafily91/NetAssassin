## 🛠️ Installation & Setup

NetAssassin is designed specifically for Linux environments (Kali, Parrot, Debian). Follow these steps to set up the tool globally on your system.

### 1. Prerequisites
Ensure you have Python 3.6 or higher installed on your machine:
```bash
python3 --version

git clone https://github.com/YOUR_USERNAME/netassassin.git
cd netassassin
chmod +x setup.sh netassassin.py
sudo ./setup.sh
netassassin --help
sudo netassassin

💻 Usage
Speed Scanning with Flags
netassassin

Fast Flags:
netassassin -t 192.168.1.1 -p 1-1024
netassassin -t 192.168.1.0/24 -p 80,443
netassassin -t 10.0.0.5 -p 22,80,443 -a


⚠️ Disclaimer
For educational and ethical testing only.
