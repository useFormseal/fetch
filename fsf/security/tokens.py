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


def save_token(provider: str, token: str) -> bool:
    try:
        keyring.set_password(SERVICE, f"{provider}:api-token", token)
        return True
    except Exception:
        fail("Could not save token to OS keychain.")


def load_token(provider: str) -> str | None:
    try:
        return keyring.get_password(SERVICE, f"{provider}:api-token")
    except Exception:
        fail("Could not read token from OS keychain.")


def delete_token(provider: str):
    try:
        keyring.delete_password(SERVICE, f"{provider}:api-token")
    except Exception:
        pass


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


def token_location(provider: str) -> str:
    try:
        if keyring.get_password(SERVICE, f"{provider}:api-token"):
            return "OS Keychain"
    except Exception:
        pass
    return "Not set"


def clear_all(provider: str):
    delete_token(provider)
    delete_namespace(provider)
