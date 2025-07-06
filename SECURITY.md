# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| 0.2.x   | :x:                |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

We take the security of this project seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Reporting Process

1. **Do not create a public GitHub issue** for the vulnerability
2. **Email us directly** at usmanabiola.ayobami@wmich.edu
3. **Include detailed information** about the vulnerability
4. **Allow time for response** before public disclosure

### Information to Include

When reporting a vulnerability, please include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** assessment
- **Suggested fix** (if available)
- **Affected versions** of the software
- **Environment details** (OS, Python version, etc.)

### Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 1 week
- **Resolution**: Within 30 days (depending on complexity)

## Security Considerations

### API Key Protection

- **Never commit API keys** to the repository
- **Use environment variables** for sensitive data
- **Rotate keys regularly** and monitor usage
- **Limit API permissions** to minimum required

### Data Privacy

- **No PII included** in the dataset
- **Anonymized health questions** only
- **Compliance with medical ethics** guidelines
- **Secure data handling** practices

### Code Security

- **Regular dependency updates** to patch vulnerabilities
- **Input validation** for all user inputs
- **Error handling** that doesn't expose sensitive information
- **Secure coding practices** throughout

## Best Practices

### For Contributors

1. **Review code** for security issues before submitting
2. **Test thoroughly** to avoid introducing vulnerabilities
3. **Follow secure coding** guidelines
4. **Report any concerns** immediately

### For Users

1. **Keep dependencies updated**
2. **Use virtual environments** for isolation
3. **Monitor API usage** and costs
4. **Review generated content** for accuracy
5. **Follow medical disclaimers** and consult professionals

## Responsible Disclosure

We are committed to:

- **Acknowledging** security reports promptly
- **Investigating** all reported issues thoroughly
- **Fixing** vulnerabilities in a timely manner
- **Crediting** reporters in security advisories
- **Coordinating** disclosure with affected parties

## Security Updates

Security updates will be:

- **Released promptly** when vulnerabilities are confirmed
- **Clearly documented** in release notes
- **Backported** to supported versions when possible
- **Communicated** through appropriate channels

## Contact Information

For security-related issues:

- **Email**: usmanabiola.ayobami@wmich.edu
- **Subject**: [SECURITY] Vulnerability Report
- **Response time**: Within 48 hours

## Acknowledgments

We thank the security research community for their contributions to making this project more secure. Responsible disclosure helps us maintain the highest standards of security and reliability.

---

**Note**: This security policy applies to the LLM Health Evaluation project. For issues related to the underlying LLM models (GPT-3.5-turbo, GPT-4, GPT-4-turbo), please contact the respective model providers directly.
