# providers/supabase/__init__ — Supabase provider

from fsf.providers import BaseProvider
from fsf.providers.supabase.engine import run


class SupabaseProvider(BaseProvider):

    name = "supabase"

    def _do_fetch(self, config):
        return run(config, debug=config.get("debug", False))


Provider = SupabaseProvider