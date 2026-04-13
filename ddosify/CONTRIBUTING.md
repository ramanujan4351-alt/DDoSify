# Contributing to DDoSify

Thank you for your interest in contributing to DDoSify! This document provides guidelines for contributors.

## How to Contribute

### Reporting Bugs

- Use the [issue tracker](https://github.com/yourusername/ddosify/issues) to report bugs
- Provide detailed information about the bug
- Include steps to reproduce the issue
- Add screenshots if applicable
- Specify your operating system and Python version
- Include Kali Linux version if applicable

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature in detail
- Explain why the feature would be useful
- Consider potential implementation approaches
- Discuss educational value and safety implications

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments to complex code sections
- Include docstrings for functions and classes
- Keep lines under 100 characters

## Testing

- Test your changes on Kali Linux if possible
- Verify GUI functionality doesn't break
- Test CLI arguments and options
- Ensure error handling works correctly
- Test with different attack methods
- Verify Kali optimizations work correctly

## Security Considerations

- Never commit sensitive information
- Validate all user inputs
- Follow secure coding practices
- Consider potential misuse scenarios
- Add appropriate warnings and disclaimers
- Ensure rate limiting and safety controls work

## Educational Focus

Remember that DDoSify is an educational tool:
- Prioritize educational value over features
- Include clear explanations of attack methods
- Add safety warnings where appropriate
- Document network security principles
- Encourage ethical usage

## Kali Linux Specific Guidelines

- Test Kali-specific optimizations
- Verify root privilege handling
- Test integration with Kali pentesting tools
- Ensure system optimizations work correctly
- Test on different Kali versions

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ddosify.git
cd ddosify
```

2. Install dependencies (Kali Linux):
```bash
sudo apt update
sudo apt install python3-scapy python3-requests python3-psutil
```

3. Run tests:
```bash
sudo python3 ddosify.py --help
sudo python3 ddosify.py --check-tools
python3 ddosify_gui.py
```

## Areas for Contribution

- **New Attack Methods**: Additional DDoS simulation techniques
- **Kali Integration**: Better tool integration and optimizations
- **Documentation**: Better explanations, tutorials, examples
- **Cross-platform**: Windows, macOS compatibility
- **Performance**: Optimization for different systems
- **Safety**: Better error handling, user warnings, rate limiting
- **Testing**: Unit tests, integration tests
- **GUI**: Improved interface, better statistics

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the CHANGELOG.md if applicable
3. Ensure your PR description clearly describes the changes
4. Link to any relevant issues
5. Test on Kali Linux if possible
6. Wait for code review and feedback

## Community Guidelines

- Be respectful and constructive
- Help others learn and understand
- Share knowledge and experience
- Follow ethical hacking principles
- Promote responsible security testing
- Emphasize educational purposes

## License

By contributing to DDoSify, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions about contributing to DDoSify.

---

**Remember**: DDoSify is for educational purposes only. Always promote ethical and responsible usage, especially when dealing with DDoS testing tools.
