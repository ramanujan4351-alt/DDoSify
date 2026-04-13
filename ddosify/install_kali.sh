#!/bin/bash
# DDoSify Kali Linux Installation Script
# Automated setup for Kali Linux systems

echo "DDoSify - Kali Linux Installation"
echo "=================================="
echo

# Check if running on Kali Linux
if [ -f /etc/os-release ]; then
    if grep -q "kali" /etc/os-release; then
        echo "[+] Kali Linux detected"
    else
        echo "[-] This script is designed for Kali Linux"
        echo "    Installation may not work on other distributions"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "[-] Cannot detect operating system"
    exit 1
fi

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "[-] This script requires root privileges"
    echo "    Run with: sudo ./install_kali.sh"
    exit 1
fi

echo "[+] Running with root privileges"

# Update package lists
echo "[*] Updating package lists..."
apt update

# Install Python packages using apt (Kali preferred method)
echo "[*] Installing Python packages..."
apt install -y python3 python3-pip python3-dev

# Install required packages
echo "[*] Installing DDoSify dependencies..."
apt install -y python3-scapy python3-requests python3-psutil

# Install additional pentesting tools (optional)
echo "[*] Installing recommended Kali tools..."
apt install -y nmap hping3 netcat tcpdump

# Install GUI dependencies
echo "[*] Installing GUI dependencies..."
apt install -y python3-tk

# Create symbolic link for easy access
echo "[*] Creating symbolic link..."
ln -sf "$(pwd)/ddosify.py" /usr/local/bin/ddosify
ln -sf "$(pwd)/ddosify_gui.py" /usr/local/bin/ddosify-gui

# Set executable permissions
echo "[*] Setting executable permissions..."
chmod +x ddosify.py
chmod +x ddosify_gui.py
chmod +x install_kali.sh

# Test installation
echo "[*] Testing installation..."
if python3 -c "import scapy, requests, psutil" 2>/dev/null; then
    echo "[+] All dependencies installed successfully"
else
    echo "[-] Dependency installation failed"
    echo "    Try manual installation: pip install -r requirements_kali.txt"
    exit 1
fi

echo
echo "Installation complete!"
echo "====================="
echo
echo "Usage examples:"
echo "  sudo ddosify -m http -t 192.168.1.100 -p 80 --threads 100 --duration 30"
echo "  sudo ddosify -m syn -t 192.168.1.100 -p 80 --threads 200 --duration 60"
echo "  ddosify-gui  # Launch GUI version"
echo
echo "Check available tools:"
echo "  sudo ddosify --check-tools"
echo
echo "WARNING: Use only for authorized security testing!"
echo
