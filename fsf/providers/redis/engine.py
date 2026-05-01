# fsf/providers/redis/engine.py
# Redis engine

import redis as redis_client
from urllib.parse import urlparse

from fsf.ui import fail


def run(config, debug=False):
    from fsf.security import tokens
    from fsf.commands.config.config import load_config

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
    except Exception as e:
        err = str(e)

        if debug:
            import traceback
            traceback.print_exc()

        if "10054" in err or "10055" in err or "reset" in err.lower():
            fail(f"""Unable to connect to Redis

Possible causes:
- VPN blocking port {port}
- Firewall restricting {host}:{port}
- Network connectivity issues

Run 'fsf fetch --debug' for details""")

        if "Name or service not known" in err or "[Errno" in err:
            fail(f"""Unable to resolve Redis host

Run 'fsf fetch --debug' for details

Try:
- Check if hostname '{host}' is correct
- Check DNS connectivity""")

        if "Authentication" in err or "NOAUTH" in err:
            fail(f"""Redis authentication failed

Check your credentials in:
- Run 'fsf connect redis' to reset""")

        fail("Redis connection failed. Run 'fsf fetch --debug' for details.")

    result = {}
    for i, v in enumerate(values):
        decoded = v.decode() if isinstance(v, bytes) else v
        result[f"redis_{i}"] = decoded.encode("utf-8")

    return result