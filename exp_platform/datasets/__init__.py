from typing import Dict
from exp_platform.datasets.base import DatasetSpec


DATASETS: Dict[str, DatasetSpec] = {}


def register_dataset(ds: DatasetSpec):
    DATASETS[ds.id] = ds
