from typing import Dict
from exp_platform.adapters.base import ModelAdapter


ADAPTERS: Dict[str, ModelAdapter] = {}


def register_adapter(adapter: ModelAdapter):
    ADAPTERS[adapter.id] = adapter
