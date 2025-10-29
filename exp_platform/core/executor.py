import subprocess
import threading
import queue
from typing import Iterable, List, Optional
from pathlib import Path


def run_command_stream(cmd: List[str], cwd: Path) -> Iterable[Optional[str]]:
    """
    以流式方式运行命令，实时产出输出行；若无输出，yield None 作为心跳。
    """
    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    )

    q: "queue.Queue[Optional[str]]" = queue.Queue()

    def reader():
        try:
            assert process.stdout is not None
            for line in process.stdout:
                q.put(line.rstrip("\n"))
        finally:
            q.put(None)  # 结束标记

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    while True:
        try:
            item = q.get(timeout=0.2)
        except queue.Empty:
            # 心跳
            yield None
            if process.poll() is not None and q.empty():
                break
            continue
        if item is None:
            # 结束
            break
        yield item

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {process.returncode}: {' '.join(cmd)}")
