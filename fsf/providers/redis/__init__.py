# providers/redis/__init__ — Redis provider

from fsf.providers import BaseProvider
from fsf.providers.redis.engine import run


class RedisProvider(BaseProvider):

    name = "redis"

    def _do_fetch(self, config):
        return run(config, debug=config.get("debug", False))


Provider = RedisProvider