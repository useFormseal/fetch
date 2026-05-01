# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 2.6.x   | :white_check_mark: |


## Reporting vulnerabilities

If you find a security vulnerability, please report it privately to allow time for a fix before public disclosure.

**Do NOT** open a public GitHub issue for security vulnerabilities.

### How to report

**GitHub Security Advisories**: Use the "Report a vulnerability" button on this repo's `Security` tab

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

### Response timeline

- **Acknowledgment**: Best effort (typically within a few days)
- **Assessment**: Best effort based on availability
- **Fix timeline**: Depends on severity and maintainer bandwidth

---

## Credential storage

formseal-fetch stores sensitive data (API tokens, namespace IDs) in your operating system's secure credential storage:

| OS | Storage location |
|---|------------------|
| Windows | Credential Manager |
| macOS | Keychain |
| Linux | Secret Service API (libsecret) |

### Why OS keychain?

- **Encrypted at rest**: Most operating systems protect stored credentials using OS-level encryption tied to your user account
- **Access controlled**: Requires your user account to access
- **Managed by OS**: Leverages built-in security features

### Fallback behavior

If the OS keychain is unavailable, credentials are stored in base64-encoded JSON at:

```
~/.config/formseal-fetch/secrets.json
```

:warning: **This fallback is NOT secure.** Base64 encoding is not encryption. Any process with access to this file can read the credentials.

This mode should only be used in environments where secure credential storage (keyring) is unavailable.

---

## What gets stored

| Data | Stored As | Location |
|------|-----------|----------|
| API Token | Encrypted | OS Keychain (preferred) or secrets.json |
| Namespace/Table ID | OS Keychain | OS Keychain (preferred), or config.json |
| Provider name | Plaintext | config.json |
| Output folder path | Plaintext | config.json |

---

## Security considerations

- **Token visibility**: `fsf status` masks tokens as `****`
- **No telemetry**: The tool does not send usage data, analytics, or logs externally
- **Direct network communication**: Data is sent only to the configured storage backend

---

## Threat model

formseal-fetch is a local CLI tool. It assumes:

- The system is trusted by the user
- The user account is not compromised
- The tool is not exposed to untrusted remote input

It does **NOT** protect against:
- Malware on the system
- Other local users with access to your files
- Compromise of the configured backend
- Physical access to the machine

---

## Best practices

1. **Use minimum-required permissions** for your API token
2. **Rotate tokens periodically** — disconnect and reconnect
3. **Never share your output folder** — contains encrypted form data
4. **Use `fsf disconnect`** when done, especially on shared machines

---

## Clearing credentials

```bash
fsf disconnect
```

This deletes:
- API token from OS Keychain
- KV namespace ID from OS Keychain  
- Configuration file (`config.json`)

Downloaded ciphertexts are **NOT** affected.