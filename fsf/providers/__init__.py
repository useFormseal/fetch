# providers/__init__ — Provider system

import json
import logging
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path

logger = logging.getLogger("fsf.providers")


class BaseProvider(ABC):

    name: str = None

    def __init__(self):
        self._schema = None

    @property
    def schema(self):
        if self._schema is None:
            self._schema = self._load_schema()
        return self._schema

    @property
    def display_name(self):
        return self.schema.get("display_name", self.name.capitalize())

    @property
    def storage_type(self):
        return self.schema.get("storage_type", self.name)

    def _load_schema(self):
        folder = getattr(self, "_folder", self.name)
        provider_dir = Path(__file__).parent / folder
        config_file = provider_dir / "config.json"
        if config_file.exists():
            with open(config_file, encoding="utf-8") as f:
                return json.load(f)
        logger.warning(f"No config.json found for provider '{self.name}' in folder '{folder}'")
        return {}

    def get_inputs(self):
        return self.schema.get("inputs", [])

    @abstractmethod
    def _do_fetch(self, config: dict) -> dict[str, bytes]:
        pass

    def post_connect(self, provider_name: str, config: dict):
        """Hook called after a successful connect. Override for post-setup tasks."""
        pass

    def fetch(self, config: dict) -> dict[str, bytes]:
        result = self._do_fetch(config)

        if not isinstance(result, dict):
            raise TypeError(f"Provider '{self.name}.fetch' must return dict, got {type(result).__name__}")

        for key, value in result.items():
            if not isinstance(key, str):
                raise TypeError(f"Provider '{self.name}.fetch' dict keys must be str, got {type(key).__name__}")
            if not isinstance(value, (bytes, str)):
                raise TypeError(f"Provider '{self.name}.fetch' dict values must be bytes/str, got {type(value).__name__}")

        return result


Provider = BaseProvider


def discover_providers():
    providers = {}
    seen_names = set()

    provider_dir = Path(__file__).parent

    for item in provider_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue

        init_file = item / "__init__.py"
        if not init_file.exists():
            continue

        module_name = f"{__name__}.{item.name}"

        try:
            module = import_module(module_name)
        except Exception as e:
            logger.warning(f"Failed to import provider '{item.name}': {e}")
            continue

        cls = getattr(module, "Provider", None)
        if not cls:
            logger.warning(f"Provider class not found in '{item.name}'")
            continue

        provider_name = cls.name

        if provider_name in seen_names:
            logger.warning(f"Duplicate provider name '{provider_name}' in folder '{item.name}' - skipping")
            continue
        seen_names.add(provider_name)

        try:
            instance = cls()
            instance._folder = item.name
            providers[provider_name] = instance
        except Exception as e:
            logger.warning(f"Failed to instantiate provider '{provider_name}': {e}")
            continue

    return providers


def get_providers():
    return discover_providers()


def get_provider(name):
    providers = get_providers()
    return providers.get(name)