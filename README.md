<div align="center">

# DDoSify
### Kali Linux Network Stress Testing Tool

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Scapy](https://img.shields.io/badge/Scapy-2.4.5+-green.svg)](https://scapy.net)
[![Kali](https://img.shields.io/badge/Kali%20Linux-Optimized-blue.svg)](https://kali.org)
[![License](https://img.shields.io/badge/License-Educational%20Only-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-orange.svg)](https://kali.org)
[![GUI](https://img.shields.io/badge/GUI-Available-brightgreen.svg)](https://github.com)

</div>

## Overview

**DDoSify** is a professional network stress testing tool optimized for **Kali Linux penetration testing**. It simulates various DDoS attack patterns for testing network infrastructure resilience and performance during authorized security assessments.

## Features

- **8 Advanced Attack Methods**: HTTP, SYN, UDP, DNS, NTP, Memcached, SSDP, Slowloris
- **Amplification Attacks**: DNS, NTP, Memcached, SSDP amplification vectors
- **Multi-Vector Attacks**: Attack multiple targets with different methods simultaneously
- **Kali Linux Optimized**: Automatic system optimizations for pentesting
- **Professional GUI**: User-friendly interface with real-time statistics
- **Advanced CLI**: Scriptable and automated testing with JSON configuration
- **Real-time Monitoring**: Live packet counts, byte rates, and advanced statistics
- **Configuration Files**: JSON-based attack scenarios and automation
- **Performance Optimization**: Thread pooling, randomization, and evasion techniques
- **Safety Controls**: Built-in rate limiting, duration controls, and confirmation prompts
- **Professional Logging**: Detailed attack logs and statistics export
- **Kali Tools Integration**: Detects and integrates with pentesting tools
- **Educational Focus**: Designed for learning and authorized testing

## Attack Methods

### HTTP Flood (Layer 7)
- **Description**: Overwhelms web servers with HTTP GET requests
- **Target**: Web servers and applications
- **Requirements**: None (works without root)
- **Effect**: High CPU/memory usage on target

### SYN Flood (Layer 4)
- **Description**: Floods target with TCP SYN packets
- **Target**: Any server with open ports
- **Requirements**: Root/administrator privileges
- **Effect**: Exhausts TCP connection table

### UDP Flood (Layer 4)
- **Description**: Sends massive UDP packets to target
- **Target**: UDP services and infrastructure
- **Requirements**: Root/administrator privileges
- **Effect**: Bandwidth and resource exhaustion

### Slowloris (Layer 7)
- **Description**: Keeps many HTTP connections open slowly
- **Target**: Web servers with connection limits
- **Requirements**: None (works without root)
- **Effect**: Connection table exhaustion

## Installation

### Kali Linux (Recommended)

#### Prerequisites
- Kali Linux (any version)
- Python 3.6+ (pre-installed on Kali)
- Root privileges (required for full functionality)

#### Quick Install (Kali)
```bash
git clone 
cd ddosify

# Install dependencies using Kali package manager
sudo apt update
sudo apt install python3-scapy python3-requests python3-psutil

# Or using pip
pip install -r requirements_kali.txt
```

#### Kali System Optimization
```bash
# DDoSify automatically optimizes Kali when run with sudo
sudo python3 ddosify.py --check-tools
```

### Manual Install (Kali)
```bash
# Install individual packages
sudo apt install python3-scapy python3-requests python3-psutil

# Or using pip (if preferred)
pip install scapy>=2.4.5 requests>=2.25.0 psutil>=5.8.0
```

### Other Linux Distributions
```bash
git clone https://github.com/yourusername/ddosify.git
cd ddosify
pip install -r requirements.txt
```

## Usage

### GUI Version (Recommended)

1. **Run the GUI**:
```bash
python ddosify_gui.py
```

2. **Configure Attack**:
   - Enter target IP/hostname
   - Select port
   - Choose attack method
   - Set threads and duration

3. **Start Attack**:
   - Test connection first
   - Click "Start Attack"
   - Monitor real-time statistics

### Command Line Version (Kali Linux)

#### Basic Syntax
```bash
sudo python3 ddosify.py -m <method> -t <target> -p <port> --threads <threads> --duration <seconds>
```

#### Kali Linux Examples

##### HTTP Flood Attack
```bash
sudo python3 ddosify.py -m http -t 192.168.1.100 -p 80 --threads 100 --duration 30 --check-tools
```

##### SYN Flood Attack (Kali Optimized)
```bash
sudo python3 ddosify.py -m syn -t 192.168.1.100 -p 80 --threads 200 --duration 60 --kali-optimize
```

##### UDP Flood Attack (Kali Optimized)
```bash
sudo python3 ddosify.py -m udp -t 192.168.1.100 -p 53 --threads 150 --duration 45 --check-tools
```

##### Slowloris Attack
```bash
sudo python3 ddosify.py -m slowloris -t 192.168.1.100 -p 80 --threads 50 --duration 120
```

#### Kali Tool Integration
```bash
# Check for available Kali pentesting tools
sudo python3 ddosify.py --check-tools

# Run with full Kali optimizations
sudo python3 ddosify.py -m http -t 192.168.1.100 -p 80 --threads 100 --duration 60 --kali-optimize
```

#### Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| `-m, --method` | Attack method | `http`, `syn`, `udp`, `slowloris` |
| `-t, --target` | Target IP/hostname | `192.168.1.100` |
| `-p, --port` | Target port | `80`, `443`, `53` |
| `--threads` | Number of threads | `100` |
| `--duration` | Attack duration | `60` |
| `--test` | Test connection first | (flag) |

## GUI Features

### Main Interface
- **Target Configuration**: IP/hostname and port selection
- **Attack Method Selection**: Radio buttons with descriptions
- **Parameter Controls**: Thread count and duration spinboxes
- **Live Statistics**: Real-time packet counts and rates
- **Attack Log**: Timestamped event logging

### Statistics Dashboard
- **Packets Sent**: Total packet counter
- **Attack Rate**: Packets per second
- **Active Threads**: Current thread count
- **Connections Made**: Successful connections
- **Elapsed Time**: Attack duration
- **Status Indicator**: Current attack state

## Technical Details

### Attack Architecture
```
[User Interface] -> [Attack Controller] -> [Thread Pool] -> [Target Network]
       |                   |                   |               |
   GUI/CLI            Statistics          Multiple          Network
   Input              Monitoring          Workers           Packets
```

### Rate Limiting
- **HTTP Flood**: 100ms delay between requests
- **SYN Flood**: 1ms delay between packets
- **UDP Flood**: 1ms delay between packets
- **Slowloris**: 5s delay between headers

### Safety Features
- **Duration Limits**: Maximum 300 seconds
- **Thread Limits**: Maximum 1000 threads
- **Connection Testing**: Verify target before attack
- **Graceful Shutdown**: Clean thread termination

## Performance Metrics

### Expected Rates (per thread)
- **HTTP Flood**: ~10 requests/second
- **SYN Flood**: ~1000 packets/second
- **UDP Flood**: ~1000 packets/second
- **Slowloris**: ~0.2 packets/second

### Resource Usage
- **CPU**: Moderate (depends on threads)
- **Memory**: Low (~50MB base + threads)
- **Network**: High (depends on attack type)

## Safety & Legal

### Educational Purpose Only
- **Authorized Testing Only**: Use on networks you own
- **Written Permission Required**: Get explicit consent
- **Controlled Environment**: Isolated test networks
- **Professional Use**: Security testing only

### Risk Warnings
- **Network Disruption**: Can cause service interruption
- **Resource Exhaustion**: May crash target systems
- **Legal Consequences**: Unauthorized use is illegal
- **Detection Risk**: May trigger security alerts

### Best Practices
- **Test Environment**: Use dedicated lab networks
- **Monitor Impact**: Watch target system responses
- **Start Small**: Begin with low thread counts
- **Document Results**: Record test parameters and outcomes

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Permission Denied** | Run with sudo/administrator |
| **Target Unreachable** | Check IP and firewall settings |
| **Low Performance** | Increase thread count or check network |
| **GUI Not Loading** | Install tkinter: `apt install python3-tkinter` |
| **Scapy Import Error** | Install with: `pip install scapy` |

### Debug Commands
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(scapy|requests|psutil)"

# Test network connectivity
ping -c 3 <target_ip>

# Check open ports
nmap -p 80 <target_ip>
```

## Advanced Usage

### Scripted Testing
```bash
#!/bin/bash
# Automated testing script

targets=("192.168.1.100" "192.168.1.101")
methods=("http" "slowloris")

for target in "${targets[@]}"; do
    for method in "${methods[@]}"; do
        echo "Testing $method on $target"
        python ddosify.py -m $method -t $target -p 80 --threads 50 --duration 30
        sleep 60  # Wait between tests
    done
done
```

### Configuration File
```python
# config.py
TARGETS = [
    {"ip": "192.168.1.100", "port": 80, "name": "Web Server"},
    {"ip": "192.168.1.101", "port": 443, "name": "HTTPS Server"}
]

DEFAULT_PARAMS = {
    "threads": 100,
    "duration": 60,
    "method": "http"
}
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add your improvements
4. Test thoroughly
5. Submit pull request

### Areas for Enhancement
- **New Attack Methods**: ICMP flood, DNS amplification
- **Better GUI**: Graphs and charts
- **API Integration**: REST API for remote control
- **Reporting**: PDF/HTML test reports

## License

This project is for **educational purposes only**. Use responsibly and only on networks you own or have explicit permission to test.

## Disclaimer

The author is not responsible for any misuse or damage caused by this tool. Users are solely responsible for their actions and must comply with all applicable laws and regulations.

---

<div align="center">

**Made for security education and authorized testing**  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue.svg)](https://github.com/yourusername)

</div>
