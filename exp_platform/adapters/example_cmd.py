import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from exp_platform.adapters.base import ModelAdapter
from exp_platform.datasets.base import DatasetSpec
from exp_platform.adapters import register_adapter

@dataclass
class ExampleCmdAdapter(ModelAdapter):
    id: str = "example-cmd"
    name: str = "示例（命令行训练脚本）"
    description: str = "演示如何通过命令对接本地训练脚本：examples/dummy_train.py"

    def params_schema(self) -> Dict[str, dict]:
        return {
            "epochs": {"type": "int", "default": 30, "help": "训练轮数"},
            "lr": {"type": "float", "default": 0.001, "help": "学习率"},
            "seed": {"type": "int", "default": 42, "help": "随机种子"},
        }

    def build_train_command(self, dataset: DatasetSpec, params: Dict[str, object], run_dir: Path) -> List[str]:
        script = Path(__file__).resolve().parents[1] / "examples" / "dummy_train.py"
        return [
            sys.executable,
            str(script),
            "--data", str(dataset.path),
            "--epochs", str(int(params["epochs"])),
            "--lr", str(float(params["lr"])),
            "--out", str(run_dir),
            "--seed", str(int(params["seed"])),
        ]

    def metrics_path(self, run_dir: Path) -> Path:
        return run_dir / "metrics.csv"

# 注册该适配器
register_adapter(ExampleCmdAdapter())
