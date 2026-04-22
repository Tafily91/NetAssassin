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

# UI Colors
G = '\033[92m' # Green
R = '\033[91m' # Red
Y = '\033[93m' # Yellow
B = '\033[94m' # Blue
C = '\033[96m' # Cyan
W = '\033[0m'  # White/Reset

COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'TELNET', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 3306: 'MySQL',
    3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Proxy'
}

class HistoryManager:
    def __init__(self):
        self.dir = Path.home() / '.netassassin'
        self.dir.mkdir(exist_ok=True)
        self.file = self.dir / 'scan_history.json'

    def save(self, target, count):
        history = self.load()
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": str(target),
            "open_ports": count
        }
        history.append(entry)
        with open(self.file, 'w') as f:
            json.dump(history[-20:], f, indent=4)

    def load(self):
        if not self.file.exists(): return []
        with open(self.file, 'r') as f:
            return json.load(f)

class Scanner:
    def __init__(self, timeout=1.0, threads=100):
        self.timeout = timeout
        self.threads = threads
        self.lock = threading.Lock()

    def grab_banner(self, sock):
        try:
            sock.send(b'GET / HTTP/1.1\r\n\r\n')
            return sock.recv(1024).decode().strip()[:50]
        except:
            return "No banner"

    def check_port(self, host, port, aggressive):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            if sock.connect_ex((host, port)) == 0:
                banner = self.grab_banner(sock) if aggressive else ""
                sock.close()
                return {"port": port, "service": COMMON_PORTS.get(port, "Unknown"), "banner": banner}
            sock.close()
        except:
            pass
        return None

    def execute(self, target, ports, aggressive):
        print(f"{B}[*] Starting scan on {target}...{W}")
        results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            tasks = [executor.submit(self.check_port, target, p, aggressive) for p in ports]
            for task in as_completed(tasks):
                res = task.result()
                if res:
                    with self.lock:
                        print(f"{G}[+] {res['port']}{W} | {res['service']}")
                        if res['banner']: print(f"    {Y}└── {res['banner']}{W}")
                    results.append(res)
        return results

def get_args():
    p = argparse.ArgumentParser(description="NetAssassin - Multi-threaded Port Scanner")
    p.add_argument("-t", "--target", help="Target IP or CIDR range")
    p.add_argument("-p", "--ports", help="Ports (e.g. 1-1000 or 80,443)")
    p.add_argument("-a", "--aggressive", action="store_true", help="Enable banner grabbing")
    p.add_argument("-i", "--interactive", action="store_true", help="Launch menu mode")
    p.add_argument("--history", action="store_true", help="Show recent scans")
    return p.parse_args()

def main():
    args = get_args()
    history = HistoryManager()
    
    if args.history:
        for h in history.load():
            print(f"[{h['date']}] {h['target']} - {h['open_ports']} ports found")
        return

    # If interactive or no target
    if args.interactive or not args.target:
        print(f"{C}NetAssassin Interactive Mode{W}")
        target = input("Target (IP/Range): ")
        port_input = input("Ports (1-1000): ")
    else:
        target = args.target
        port_input = args.ports or "1-1000"

    # Port parsing
    if '-' in port_input:
        s, e = map(int, port_input.split('-'))
        ports = range(s, e + 1)
    else:
        ports = [int(x.strip()) for x in port_input.split(',')]

    scanner = Scanner()
    
    try:
        if '/' in target:
            hosts = [str(ip) for ip in ipaddress.ip_network(target).hosts()]
        else:
            hosts = [socket.gethostbyname(target)]
    except Exception as e:
        print(f"{R}[!] Error: {e}{W}")
        return

    found_total = 0
    for h in hosts:
        found = scanner.execute(h, ports, args.aggressive)
        found_total += len(found)
    
    history.save(target, found_total)
    print(f"\n{C}[*] Finished. Found {found_total} open ports.{W}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] User Interrupted.{W}")