import importlib
import pkgutil
from typing import Dict
from pathlib import Path

from exp_platform.adapters.base import ModelAdapter
from exp_platform.datasets.base import DatasetSpec


def _load_modules_in(package_name: str):
    pkg = importlib.import_module(package_name)
    pkg_path = Path(pkg.__file__).parent
    for info in pkgutil.iter_modules([str(pkg_path)]):
        if info.name.startswith("_") or info.name in ("base",):
            continue
        importlib.import_module(f"{package_name}.{info.name}")


def load_adapters() -> Dict[str, ModelAdapter]:
    # 动态导入 adapters 下的模块，收集 ADAPTERS
    _load_modules_in("exp_platform.adapters")
    from exp_platform.adapters import ADAPTERS  # type: ignore
    return ADAPTERS


def load_datasets() -> Dict[str, DatasetSpec]:
    # 动态导入 datasets 下的模块，收集 DATASETS
    _load_modules_in("exp_platform.datasets")
    from exp_platform.datasets import DATASETS  # type: ignore
    return DATASETS
