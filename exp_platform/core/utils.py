from datetime import datetime
from pathlib import Path


def timestamp_str() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)