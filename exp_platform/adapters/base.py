from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Protocol

from exp_platform.datasets.base import DatasetSpec


class ModelAdapter(Protocol):
    id: str
    name: str
    description: str

    def params_schema(self) -> Dict[str, dict]:
        """
        返回用于渲染超参数表单的 schema。
        例：
        {
          "epochs": {"type": "int", "default": 10, "help": "训练轮数"},
          "lr": {"type": "float", "default": 1e-3, "help": "学习率"},
        }
        """
        ...

    def build_train_command(self, dataset: DatasetSpec, params: Dict[str, object], run_dir: Path) -> List[str]:
        """
        构造训练命令（列表形式）。可执行入口可以是 python 脚本、shell、make 等。
        """
        ...

    def metrics_path(self, run_dir: Path) -> Path:
        """
        指定指标文件路径；默认约定为 run_dir / 'metrics.csv'
        """
        return run_dir / "metrics.csv"