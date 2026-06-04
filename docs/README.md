# Documentation

Welcome to the formseal-fetch documentation.

| Guide | Description |
|-------|-------------|
| [Getting Started](./0.%20getting-started.md) | Installation and first-time setup |
| [Commands Reference](./1.%20commands.md) | All available commands |
| [Configuration](./2.%20configuration.md) | Config files and credential storage |
| [Backends](./3.%20backends.md) | Connecting to Cloudflare, Supabase, Redis |
| [How it works](./4.%20how-it-works.md) | Fetch flow and pipeline |
| [Security](./5.%20security.md) | Security model and credential storage |
| [Troubleshooting](./6.%20troubleshooting.md) | Common issues and solutions |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contributing guide |
| [SECURITY.md](../.github/SECURITY.md) | Security policy |

## What is formseal-fetch?

formseal-fetch is a CLI tool that downloads encrypted form submissions from your storage backend.

## Ecosystem

formseal-fetch is part of the formseal ecosystem:

| Tool | Description |
|------|-------------|
| [formseal-embed](https://github.com/useFormseal/embed) | Client-side form encryption library |
| formseal-fetch | Downloads encrypted ciphertexts from storage |
| [formseal-decrypt](https://github.com/useFormseal/decrypt) | Decrypts ciphertexts locally |

## Supported backends

| Backend | Type |
|---------|------|
| Cloudflare KV | Key-Value store |
| Supabase | PostgreSQL |
| Redis | Redis DB |

## Workflow

```
formseal-embed (browser encryption)
       |
       v (encrypted submissions)
  Storage backend
       |
       v (fsf fetch)
  formseal.ct.jsonl
       |
       v (fsd decrypt)
  formseal.decrypted.jsonl
       |
       v
  You
```

1. [formseal-embed](https://github.com/useFormseal/embed) encrypts form submissions in the browser
2. Ciphertexts are stored at your backend
3. `fsf fetch` downloads them to `formseal.ct.jsonl`
4. [formseal-decrypt](https://github.com/useFormseal/decrypt) decrypts them locally
