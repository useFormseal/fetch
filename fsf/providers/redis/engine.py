# fsf/providers/redis/engine.py
# Redis engine

import redis as redis_client
from urllib.parse import urlparse

from fsf.ui import fail, br, C, R


def run(config, debug=False):
    from fsf.security import tokens
    from fsf.commands.config import load_config

    cfg = load_config()
    provider = cfg.get("provider")
    url = tokens.load_token(provider)
    key_prefix = config.get("key_prefix", "submissions")

    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 6379

    try:
        r = redis_client.from_url(url)
        values = r.lrange(key_prefix, 0, -1)
        r.close()
    except Exception:
        if debug:
            import traceback
            traceback.print_exc()
            br()
            raise SystemExit(1)

        fail(f"""Unable to connect to Redis. Possible causes:

        - VPN blocking port {port}
        - Firewall restricting {host}:{port}
        - Network connectivity issues

  Run {C}fsf fetch --debug{R} for details""")

    result = {}
    for i, v in enumerate(values):
        decoded = v.decode() if isinstance(v, bytes) else v
        result[f"redis_{i}"] = decoded.encode("utf-8")

    return result