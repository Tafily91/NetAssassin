#!/usr/bin/env python3
import socket
import sys
import argparse
import json
import threading
import ipaddress
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- UI Colors ---
G, R, Y, B, C, W = '\033[92m', '\033[91m', '\033[93m', '\033[94m', '\033[96m', '\033[0m'

BANNER = f"""{C}
  _   _      _   _                         _      
 | \ | | ___| |_/ \   ___ ___  __ _ ___ ___(_)_ __  
 |  \| |/ _ \ __/ _ \ / __/ __|/ _` / __/ __| | '_ \ 
 | |\  |  __/ || ___ \\__ \__ \ (_| \__ \__ \ | | | |
 |_| \_|\___|\__/_/   \_\___/___/\__,_|___/___/_|_| |_|
{W}      -- High-Speed Network Port Scanner --
"""

COMMON_PORTS = {
    21:'FTP', 22:'SSH', 23:'TELNET', 25:'SMTP', 53:'DNS', 80:'HTTP', 
    110:'POP3', 143:'IMAP', 443:'HTTPS', 3306:'MySQL', 3389:'RDP'
}

class History:
    def __init__(self):
        self.path = Path.home() / '.netassassin' / 'scan_history.json'
        self.path.parent.mkdir(exist_ok=True)
    def log(self, target, found):
        data = self.get_all()
        data.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "target": target, "found": found})
        with open(self.path, 'w') as f: json.dump(data[-20:], f, indent=4)
    def get_all(self):
        if not self.path.exists(): return []
        with open(self.path, 'r') as f: return json.load(f)

class Engine:
    def __init__(self, timeout=1.0):
        self.timeout = timeout
        self.lock = threading.Lock()
    def grab_banner(self, s):
        try:
            s.send(b'HEAD / HTTP/1.1\r\n\r\n')
            return s.recv(1024).decode().strip()[:40]
        except: return ""
    def scan(self, target, port, aggressive):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((target, port)) == 0:
                    banner = self.grab_banner(s) if aggressive else ""
                    service = COMMON_PORTS.get(port, "Unknown")
                    with self.lock:
                        print(f"{G}[+] {port:<5} {W}| {service:<10} {Y}{banner}{W}")
                    return port
        except: pass
        return None

def main():
    print(BANNER)
    p = argparse.ArgumentParser()
    p.add_argument("-t", "--target")
    p.add_argument("-p", "--ports")
    p.add_argument("-a", "--aggressive", action="store_true")
    p.add_argument("--history", action="store_true")
    args = p.parse_args()

    hist = History()
    if args.history:
        print(f"{C}--- Recent Scans ---{W}")
        for e in hist.get_all(): print(f"[{e['timestamp']}] {e['target']} ({e['found']} open)")
        return

    target = args.target or input(f"{Y}Target IP/Range: {W}")
    p_in = args.ports or "1-1024"
    
    if '-' in p_in:
        low, high = map(int, p_in.split('-'))
        ports = range(low, high + 1)
    else:
        ports = [int(x) for x in p_in.split(',')]
    
    try:
        targets = [str(ip) for ip in ipaddress.ip_network(target).hosts()] if '/' in target else [target]
    except: targets = [target]

    eng, total = Engine(), 0
    for t in targets:
        print(f"{B}[*] Scanning {t}...{W}")
        with ThreadPoolExecutor(max_workers=100) as ex:
            futures = [ex.submit(eng.scan, t, port, args.aggressive) for port in ports]
            res = [f.result() for f in as_completed(futures) if f.result()]
            total += len(res)

    hist.log(target, total)
    print(f"\n{C}[!] Scan Complete. {total} ports open.{W}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{R}[!] Aborted.{W}")
