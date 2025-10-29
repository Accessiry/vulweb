from dataclasses import dataclass
from pathlib import Path

from exp_platform.datasets.base import DatasetSpec
from exp_platform.datasets import register_dataset

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "examples" / "data"
TOY_FILE = DATA_DIR / "toy.csv"

@dataclass
class ToyDataset(DatasetSpec):
    pass

# 确保存在 toy 数据（示例）
TOY_FILE.parent.mkdir(parents=True, exist_ok=True)
if not TOY_FILE.exists():
    TOY_FILE.write_text("code,label\nprint('hello'),0\nx=1/0,1\n", encoding="utf-8")

register_dataset(ToyDataset(
    id="toy",
    name="Toy 漏洞分类样例",
    description="极小的示例数据集，用于演示平台功能。",
    path=TOY_FILE
))
