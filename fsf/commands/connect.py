# commands/connect — Connect to a storage provider

import sys
from pathlib import Path

from fsf.ui import br, fail, ok, info, G, W, D, R, C, OK, header
from fsf.commands.config import load_config, save_config
from fsf.security import tokens
from fsf.providers import get_providers


def _parse_args(args):
    if not args:
        fail("Usage: fsf connect <provider> [key:value ...]")

    provider = args[0].lower()
    parsed = {"provider": provider}

    for arg in args[1:]:
        if ":" not in arg:
            fail(f"Invalid format: {arg}\n         Use key:value (e.g., field:value)")
        key, value = arg.split(":", 1)
        parsed[key] = value

    return parsed


def run(args):
    if not args:
        fail("Usage: fsf connect <provider> [key:value ...]")

    if not tokens.check_keyring():
        fail("""No supported credential store found.

          This application requires an OS keyring.

          Supported:
          - Windows Credential Manager
          - macOS Keychain
          - Secret Service (GNOME Keyring)
          - KWallet

  Headless environments are not currently supported.""")

    parsed = _parse_args(args)

    cfg = load_config()
    if cfg.get("provider"):
        fail(f"Provider already set: {cfg['provider']}\n         Run {C}fsf disconnect{R} first.")

    provider = parsed["provider"].lower()
    providers = get_providers()
    if provider not in providers:
        fail(f"Unknown provider: {provider}\n         Run {C}fsf providers{R} to see available.")

    _setup_flow(provider, parsed, providers[provider])


def _setup_flow(provider, parsed, provider_obj):
    print()
    header("setup")
    print()

    cfg = load_config()
    cfg["provider"] = provider

    inputs = provider_obj.get_inputs()
    collected = {}

    for field in inputs:
        key = field["name"]
        prompt = field.get("description", key)
        sensitive = field.get("sensitive", False)

        value = parsed.get(key)
        if not value:
            try:
                sys.stdout.write(f"  {prompt}: ")
                sys.stdout.flush()
                value = input().strip()
            except KeyboardInterrupt:
                br()
                info("Cancelled.")
                br()
                return

        if field.get("required") and not value:
            fail(f"{prompt} is required")

        if value:
            collected[key] = value
            if sensitive:
                tokens.save_namespace(provider, value, key=key)
            else:
                cfg[key] = value

    provider_obj.post_connect(provider, collected)

    if "output" in parsed:
        output_folder = parsed["output"]
    else:
        try:
            sys.stdout.write(f"  Output Folder [{D}data{R}]: ")
            sys.stdout.flush()
            output_folder = input().strip()
            if not output_folder:
                output_folder = "data"
        except KeyboardInterrupt:
            br()
            info("Cancelled.")
            br()
            return

    output_folder = Path(output_folder).expanduser().resolve()
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
    except Exception:
        fail("Could not create output folder. Check permissions.")

    cfg["output_folder"] = str(output_folder)
    print()

    save_config(cfg)

    print(f"{G}{OK}{R} Saved!")
    print()
    print(f"  Run {W}fsf fetch{R} to download ciphertexts")
    print()
