# Security Policy
## Supported Versions

| Version | Supported |
| :--- | :--- |
| v1.0.x | :white_check_mark: |

## Reporting a Vulnerability
Please do not open a public issue for security vulnerabilities. Instead, contact the repository owner (`@dorinalunar`) directly or open a private vulnerability report via GitHub Security Advisories.
## Architecture Safeguards
- **Consensus Protection**: Employs `gl.vm.run_nondet_unsafe` to ensure deterministic execution matching between Leader and Validator nodes.
- **Hash Verification**: Strict validation of remote JSON payloads via SHA-256 before LLM execution.
