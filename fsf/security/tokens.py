# security/tokens — Credential storage (OS keychain)

import keyring

from fsf.ui.bodies import fail

SERVICE = "formseal-fetch"


def check_keyring() -> bool:
    try:
        keyring.get_keyring()
        keyring.set_password(SERVICE, "__probe__", "probe")
        keyring.delete_password(SERVICE, "__probe__")
        return True
    except Exception:
        return False


def save_namespace(provider: str, namespace: str, key: str = "kv-namespace") -> bool:
    try:
        keyring.set_password(SERVICE, f"{provider}:{key}", namespace)
        return True
    except Exception:
        fail("Could not save credentials to OS keychain.")


def load_namespace(provider: str, key: str = "kv-namespace") -> str | None:
    try:
        return keyring.get_password(SERVICE, f"{provider}:{key}")
    except Exception:
        fail("Could not read credentials from OS keychain.")


def delete_namespace(provider: str, key: str = "kv-namespace"):
    try:
        keyring.delete_password(SERVICE, f"{provider}:{key}")
    except Exception:
        pass


def clear_all(provider: str, extra_keys: list | None = None):
    delete_namespace(provider)
    for key in (extra_keys or []):
        delete_namespace(provider, key=key)
