# NetAssassin 🎯

**NetAssassin** is a professional, multi-threaded port scanner built for Kali Linux and Parrot OS.

## Installation
```bash
chmod +x setup.sh
./setup.sh

Basic Scan: netassassin -t 192.168.1.1
Range Scan: netassassin -t 192.168.1.0/24 -p 80,443
Full Audit: netassassin -t target.com -p 1-65535 -a
View Logs: netassassin --history
