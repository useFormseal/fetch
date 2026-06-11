# commands/config — Config management (load, save, status, disconnect)

import json
import sys
from pathlib import Path

from fsf.ui import br, ok, info, warn, G, W, D, Y, R, header, truncate
from fsf.security import tokens
from fsf.providers import get_provider


CONFIG_DIR = Path.home() / ".config" / "formseal-fetch"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def run_status():
    cfg = load_config()

    br()
    header("status")
    br()

    print(f"  {D}Configuration Status:{R}")
    br()

    provider_name = cfg.get("provider")
    if not provider_name:
        warn("No provider configured. Run: fsf connect provider:<name>")
        br()
        return

    provider = get_provider(provider_name)

    def row(label, value, color=W):
        print(f"  {D}{label:<26}{R}{color}{value}{R}")

    row("Provider:", provider.display_name if provider else provider_name)

    if provider:
        account_id = tokens.load_namespace(provider_name, key="account_id")
        if account_id:
            trunc = truncate(account_id)
            row("Account ID:", trunc)

        for field in provider.get_inputs():
            key = field["name"]
            sensitive = field.get("sensitive", False)
            if sensitive:
                value = tokens.load_namespace(provider_name, key=key)
            else:
                value = cfg.get(key)
            desc = field.get("description", key)
            if value:
                if sensitive:
                    trunc = truncate(value)
                else:
                    trunc = str(value)
            else:
                trunc = "(not set)"
            row(f"{desc}:", trunc, W if value else D)

        has_keychain = any(
            tokens.load_namespace(provider_name, key=f["name"])
            for f in provider.get_inputs() if f.get("sensitive")
        )
        row("Credentials:", "OS Keychain" if has_keychain else "Not set", G if has_keychain else D)

        br()
        row("Storage Type:", provider.storage_type)

    output_folder = cfg.get("output_folder")
    row("Output Folder:", output_folder or "(not set)", W if output_folder else D)

    br()


def run_disconnect(args=None):
    args = args or []
    wipe = "--wipe" in args

    if wipe:
        br()
        print(f"  {Y}THIS WILL DELETE EVERYTHING.{R}")
        print(f"  Config, credentials, AND ciphertexts will be deleted.")
    else:
        br()
        print(f"  {Y}This will delete all config and credentials.{R}")
        print(f"  Downloaded ciphertexts will NOT be affected.")
    br()
    sys.stdout.write(f"  Continue? [y/N]: ")
    sys.stdout.flush()
    confirm = input().strip().lower()

    if confirm != "y":
        br()
        info("Cancelled.")
        br()
        return

    cfg = load_config()
    provider = cfg.get("provider")

    if wipe:
        output_folder = cfg.get("output_folder")
        if output_folder:
            ciphertext_path = Path(output_folder) / "ciphertexts.jsonl"
            if ciphertext_path.exists():
                ciphertext_path.unlink()

    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()

    if provider:
        provider_obj = get_provider(provider)
        sensitive_keys = [f["name"] for f in (provider_obj.get_inputs() if provider_obj else []) if f.get("sensitive")]
        tokens.clear_all(provider, extra_keys=sensitive_keys)

    br()
    if wipe:
        ok("Disconnected. Everything wiped.")
    else:
        ok("Disconnected. All config and credentials cleared.")
    br()



