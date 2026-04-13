# Changelog

All notable changes to DDoSify will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of DDoSify
- Multiple DDoS attack simulation methods
- Kali Linux optimizations and integration
- Professional GUI with real-time statistics
- Command-line interface with advanced options
- Rate limiting and safety controls
- Cross-platform support

### Security
- Root privilege checks for raw socket operations
- Input validation and sanitization
- Rate limiting and duration controls
- Educational warnings and disclaimers
- Safe cleanup procedures

### Documentation
- Comprehensive README with Kali-specific instructions
- Installation scripts for Kali Linux
- Contributing guidelines with security considerations
- GitHub issue templates and workflows

## [1.0.0] - 2024-04-13

### Added
- Core DDoS simulation functionality
- **Attack Methods**: HTTP Flood, SYN Flood, UDP Flood, Slowloris
- **Kali Linux Integration**: Automatic optimizations, tool detection
- **GUI Interface**: Dark theme, real-time monitoring, attack controls
- **CLI Interface**: Advanced options, Kali-specific flags
- **Safety Features**: Rate limiting, duration controls, confirmation prompts

### Kali Linux Features
- **System Optimization**: ICMP rate limiting, TCP syncookies
- **Tool Integration**: nmap, hping3, netcat, tcpdump detection
- **Performance**: Socket limit increases, network optimizations
- **Installation**: Automated setup script, package manager integration

### Attack Methods
- **HTTP Flood**: Layer 7 web server overload simulation
- **SYN Flood**: Layer 4 TCP packet flooding
- **UDP Flood**: Layer 4 UDP packet flooding
- **Slowloris**: Layer 7 slow HTTP connection attack

### GUI Features
- **Real-time Statistics**: Packet counts, rates, timing
- **Attack Controls**: Start/stop, parameter adjustment
- **Status Monitoring**: Active threads, connections, elapsed time
- **Dark Theme**: Professional appearance optimized for pentesting

### CLI Features
- **Advanced Options**: Kali optimizations, tool checking
- **Flexible Parameters**: Thread count, duration, method selection
- **Validation**: Input checking, connection testing
- **Monitoring**: Real-time statistics, progress indicators

### Platforms
- **Kali Linux**: Full support with optimizations
- **Linux**: General Linux distribution support
- **Windows**: GUI and CLI support
- **Virtual Machines**: VMware, VirtualBox compatibility

### Educational
- Clear explanations of DDoS attack methods
- Network security principles
- Safety warnings and legal disclaimers
- Step-by-step usage instructions
- Kali Linux specific guidance

---

## Educational Disclaimer

DDoSify is provided for educational purposes only. Users must:
- Only test on networks they own or have explicit permission
- Follow all applicable laws and regulations
- Use responsibly and ethically
- Understand the technical concepts behind DDoS attacks
- Never use against unauthorized targets
