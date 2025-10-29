# 实验平台（模型选择 / 训练 / 验证 / 数据集管理）

该平台旨在以极少步骤把“你本地已有的训练代码”接入系统：
- 在 UI 中选择“模型适配器 + 数据集”，填写超参，点击“开始训练”即可启动本地训练命令；
- 训练过程的日志与指标（metrics.csv）会被实时读取并可视化；
- 新增模型：仅需新增一个适配器文件，描述“如何构造训练命令”和“指标文件位置”，无需改你原来的训练脚本；
- 新增数据集：新增一个数据集适配器，提供名称/路径/准备函数等。

> 注：本仓库内提供了一个示例训练脚本 `examples/dummy_train.py`，用于演示实时指标可视化。你可以替换为自己的训练入口（如 `python train.py ...`），只需修改适配器即可。

---

## 快速开始

1) 安装依赖（建议 Python 3.10+）
```bash
cd exp_platform
pip install -e .  # 或者 pip install -r requirements.txt（若你更偏好 requirements）
```

2) 运行系统（本地）
```bash
streamlit run exp_platform/app.py
```

3) 打开浏览器（Streamlit 会显示本地 URL），在侧边栏：
- 选择模型（适配器）
- 选择数据集
- 配置超参数
- 点击“开始训练”

系统将：
- 在 `exp_platform/runs/{时间戳}_{模型ID}_{数据集ID}` 下创建本次实验目录
- 以子进程方式运行你的训练命令（来自模型适配器）
- 实时读取 `metrics.csv` 绘制曲线，并展示训练日志

---

## 目录结构与约定

```
exp_platform/
  app.py                 # Streamlit UI
  core/
    __init__.py
    schemas.py           # Pydantic 数据结构
    registry.py          # 动态加载适配器
    executor.py          # 子进程与日志
    utils.py             # 工具函数
  adapters/
    __init__.py
    base.py              # 模型适配器基类/协议
    example_cmd.py       # 示例模型适配器（命令行形式）
  datasets/
    __init__.py
    base.py              # 数据集适配器基类/协议
    example_toy.py       # 示例数据集
  examples/
    dummy_train.py       # 示例训练脚本（会输出 metrics.csv）
    data/toy.csv         # toy 数据
  pyproject.toml         # 依赖
  README.md              # 本文件
```

- 日志与产物：默认写入 `exp_platform/runs/`。
- 指标文件：默认约定为 `metrics.csv`（逗号分隔，含 header；至少包含 step, loss/acc 等列）。示例脚本会按此格式输出。

---

## 如何接入“你的训练代码”（新增一个模型）

以 `adapters/example_cmd.py` 为模板，新建一个适配器，比如 `adapters/my_model.py`，核心是实现：
- 基本信息：`id`, `name`, `description`
- 超参数模式：`params_schema`（系统将据此自动渲染 UI 表单）
- 命令构造：`build_train_command(dataset, params, run_dir)` 返回一个命令行参数列表，例如：
  ```python
  return [sys.executable, "train.py", "--data", dataset.path, "--epochs", str(params["epochs"]), "--out", str(run_dir)]
  ```
- 指标位置：`metrics_path(run_dir)` 指定你的训练脚本写出的指标文件路径（如 `run_dir/"metrics.csv"`）

新增文件后无需改其他代码，UI 会自动发现它。

---

## 如何接入“你的数据集”（新增一个数据集）

以 `datasets/example_toy.py` 为模板，新建 `datasets/my_dataset.py`，核心字段：
- `id`, `name`, `description`
- `path`（本地路径或挂载路径）
- `prepare()`（可选：若是初次运行需解压/下载/预处理，可在此实现）

新增文件后，UI 会自动发现它。

---

## 可视化与日志

- UI 会实时读取 `metrics.csv` 并绘制曲线（Streamlit line chart）。
- 控制台日志（stdout/stderr）会流式显示在 UI。
- 若你的训练已集成 TensorBoard，也可在适配器里补充 `tb_logdir(run_dir)`，后续版本可内嵌或提供“一键打开 TB”按钮（当前版本以 CSV 为主）。

---

## 典型工作流

1) 把你现有的训练脚本放在仓库某处（或外部路径）
2) 写一个模型适配器，返回运行该脚本的命令
3) 在 UI 里选择该模型 + 数据集，点开始
4) 训练过程中可见实时 loss/acc 曲线与日志；训练结束后可在 `exp_platform/runs/` 查看产物

---

## 常见问题

- Q: 我有很多模型，如何管理？
  - A: 每个模型一个适配器文件，系统自动发现；也可以在一个文件里导出多个适配器。
- Q: 我只想执行 shell 脚本/Makefile 可以吗？
  - A: 可以，命令列表里用你熟悉的可执行入口即可（例如 "[bash, scripts/train.sh, ...]"）。
- Q: 我已经有 TensorBoard 了，还需要 CSV 吗？
  - A: 当前版本以 CSV 实时绘图为主；若你已经写入 TB，可在适配器中标出 `tb_logdir`，我们后续可以增强 UI 内嵌 TB。