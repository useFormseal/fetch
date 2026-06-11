# providers/s3/__init__ — S3-compatible provider

from fsf.providers import BaseProvider
from fsf.providers.s3.engine import run


class S3Provider(BaseProvider):

    name = "s3"

    def _do_fetch(self, config):
        return run(config, debug=config.get("debug", False))


Provider = S3Provider
