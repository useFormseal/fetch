# Contributing to formseal-fetch

Thanks for your interest in contributing! Contributions of all kinds are welcome — bug fixes, new features, docs, and more. **Provider and security contributions are especially valued since the tool is designed to be backend-agnostic.**

---

## Table of contents

- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Adding a new provider](#adding-a-new-provider)
- [Versioning](#versioning)
- [Code style](#code-style)
- [Submitting changes](#submitting-changes)
- [Testing](#testing)
- [Reporting issues](#reporting-issues)
- [Security](#security)

---

## Getting started

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/useFormseal/fetch.git
   cd formseal-fetch
   ```

2. Install in development mode using `pipx` (recommended) or `pip`:
   ```bash
   pipx install -e .
    ```
3. Verify it works:
   ```bash
   fsf
   ```

> **Note:** Always use `pipx install -e .` for local dev — it gives you an isolated environment and the version header will display correctly from source.

---

## Project structure

```
formseal-fetch/
├── fsf/
│   ├── cli.py               # Entry point, command dispatch
│   ├── __main__.py          # python -m fsf support
│   ├── ui/                  # Terminal output helpers (styles, headers, bodies)
│   ├── commands/            # CLI commands (flat: fetch, connect, config)
│   ├── helpers/             # Aliases, errors
│   ├── providers/           # Storage backend implementations
│   │   ├── __init__.py     # Provider base class + registry
│   │   ├── cloudflare/     # Cloudflare KV provider
│   │   ├── supabase/       # Supabase provider
│   │   └── redis/          # Redis provider
│   └── security/
│       └── tokens.py       # Keyring-backed credential storage
├── docs/                    # Documentation
├── .github/                 # GitHub workflows, issue templates
├── pyproject.toml           # Package config
└── version.txt              # Version (single source of truth)
```

---

## Adding a new provider

Providers are storage backends that `fsf fetch` reads ciphertexts from. Each lives in its own sub-package under `fsf/providers/`.

**Detailed specs:** See [docs/providers/README.md](docs/providers/README.md)

---

## Versioning

The version string lives in **`version.txt`** and is the single source of truth. The publish workflow reads it and injects it into the code at build time.

---

## Code style

- Add a comment at the top of each logical block explaining what it does
- Follow the patterns already in the file you're editing
- Use the `fsf.ui` module helpers (`ok`, `neutral`, `fail`, `warn`, `br`, `header`) for all terminal output
- Validate before writing — never persist invalid state
- Never expose secrets or keys in output

---

## Submitting changes

1. Create a branch off `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. Make your changes and test locally (see [Testing](#testing))

3. Commit with clear, descriptive messages

4. Push and open a pull request against `main`

---

## Testing

There is no automated test suite yet. Test the relevant commands manually before opening a PR:

```bash
fsf                          # check version header displays correctly
fsf --providers              # verify your provider appears (if adding one)
fsf connect cloudflare          # walk through the setup flow
fsf status                   # confirm credentials were saved
fsf fetch                    # fetch ciphertexts end-to-end
fsf disconnect               # confirm credentials are cleared
```

---

## Reporting issues

Report bugs via [GitHub Issues](https://github.com/useFormseal/fetch/issues/new).

Please include:
- Steps to reproduce
- Expected vs actual behavior
- Your OS and Python version

---

## Security

If you find a security vulnerability, please report it privately via GitHub Security Advisories.

**Do NOT** open a public issue for security vulnerabilities.