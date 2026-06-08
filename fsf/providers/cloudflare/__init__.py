# providers/cloudflare/__init__ — Cloudflare provider

from fsf.providers import BaseProvider
from fsf.providers.cloudflare.engine import run


class CloudflareProvider(BaseProvider):

    name = "cloudflare"

    def _do_fetch(self, config):
        return run(config, debug=config.get("debug", False))


Provider = CloudflareProvider