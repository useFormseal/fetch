# providers/cloudflare/__init__ — Cloudflare provider

from fsf.providers import BaseProvider
from fsf.providers.cloudflare.engine import run


class CloudflareProvider(BaseProvider):

    name = "cloudflare"

    def _do_fetch(self, config):
        return run(config, debug=config.get("debug", False))

    def post_connect(self, provider_name: str, config: dict):
        from fsf.providers.cloudflare.account import get_account_id
        from fsf.security import tokens
        token = config.get("token")
        if token:
            try:
                account_id = get_account_id(token)
                tokens.save_namespace(provider_name, account_id, key="account_id")
            except Exception:
                pass


Provider = CloudflareProvider