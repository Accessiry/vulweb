from dataclasses import dataclass
from pathlib import Path

@dataclass
class DatasetSpec:
    id: str
    name: str
    description: str
    path: Path

    def prepare(self):
        """
        可选：若需要解压/下载/预处理则在此实现；示例数据集默认无需处理。
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)