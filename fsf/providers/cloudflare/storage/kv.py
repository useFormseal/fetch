# Cloudflare KV storage

import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

from fsf.ui import fail


def _get(url, token, debug=False):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if debug:
            fail(f"HTTP {e.code}: {e.read().decode()}")
        fail(f"HTTP {e.code}: API request failed (run with --debug for details)")


def _get_raw(url, token, debug=False):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8").strip()
    except urllib.error.HTTPError as e:
        if debug:
            fail(f"HTTP {e.code}: {e.read().decode()}")
        fail(f"HTTP {e.code}: API request failed (run with --debug for details)")


def fetch(namespace, token, debug=False):
    """Fetch all values from a KV namespace. Returns dict[str, bytes] with single key 'ciphertexts'."""
    account_id = _get_account_id(token, debug)
    base = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace}"

    all_keys = []
    cursor = None

    while True:
        url = f"{base}/keys" + (f"?cursor={cursor}" if cursor else "")
        data = _get(url, token, debug)
        if not data.get("success"):
            fail(f"API error: {data.get('errors')}")
        all_keys.extend(k["name"] for k in data.get("result", []))
        cursor = data.get("result_info", {}).get("cursor")
        if not cursor:
            break

    if not all_keys:
        return {"ciphertexts": b""}

    result = {}
    for key in all_keys:
        value = _get_raw(f"{base}/values/{urllib.parse.quote(key, safe='')}", token, debug)
        if value:
            result[key] = value.encode("utf-8")

    return result


def _get_account_id(token, debug=False):
    url = "https://api.cloudflare.com/client/v4/accounts"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if debug:
            fail(f"HTTP {e.code}: {body}")
        fail(f"Cloudflare API error: HTTP {e.code} (run with --debug for details)")
    except urllib.error.URLError as e:
        if debug:
            fail(f"Network error: {e.reason}")
        fail(f"Network error: Unable to reach Cloudflare API (run with --debug for details)")
    except json.JSONDecodeError as e:
        fail(f"Invalid API response: {e}")

    if not data.get("success"):
        errors = data.get("errors", [])
        if errors:
            msg = errors[0].get("message", "Unknown error")
            if "token" in msg.lower():
                fail(f"""Invalid Cloudflare token

Run 'fsf connect cloudflare' to update your token""")
            fail(f"Cloudflare API error: {msg} (run with --debug for details)")
        fail("Cloudflare API error (run with --debug for details)")

    accounts = data.get("result", [])
    if not accounts:
        fail("No accounts found. Token needs 'Account Settings: Read' scope.")

    return accounts[0]["id"]