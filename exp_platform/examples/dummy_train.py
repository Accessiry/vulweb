import argparse
import csv
import random
import sys
import time
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, required=True)
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--out", type=str, required=True)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()

def main():
    args = parse_args()
    random.seed(args.seed)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_file = out_dir / "metrics.csv"
    log_file = out_dir / "train.log"

    # 伪训练：读取数据行数作为样本量，按 epoch 写入指标
    data_rows = 0
    with open(args.data, "r", encoding="utf-8") as f:
        data_rows = sum(1 for _ in f) - 1  # 跳过 header

    with open(metrics_file, "w", newline="", encoding="utf-8") as mf, open(log_file, "w", encoding="utf-8") as lf:
        writer = csv.DictWriter(mf, fieldnames=["step", "loss", "acc"])
        writer.writeheader()
        loss = 1.0
        acc = 0.0
        for step in range(1, args.epochs + 1):
            # 模拟收敛
            loss = max(0.01, loss * (0.90 + random.uniform(-0.02, 0.02)))
            acc = min(1.0, acc + (0.04 + random.uniform(-0.01, 0.01)))
            writer.writerow({"step": step, "loss": round(loss, 6), "acc": round(acc, 6)})
            mf.flush()
            msg = f"[epoch {step:03d}] loss={loss:.4f} acc={acc:.4f} data_rows={data_rows} lr={args.lr}"
            print(msg, flush=True)
            lf.write(msg + "\n")
            lf.flush()
            time.sleep(0.2)

    # 产出一个“模型文件”
    (out_dir / "model.bin").write_bytes(b"dummy-model")
    print("Training finished.", flush=True)

if __name__ == "__main__":
    sys.exit(main())
