import time
from pathlib import Path
import streamlit as st
import pandas as pd

from exp_platform.core.registry import load_adapters, load_datasets
from exp_platform.core.schemas import ExperimentConfig
from exp_platform.core.executor import run_command_stream
from exp_platform.core.utils import timestamp_str, ensure_dir

BASE_DIR = Path(__file__).resolve().parent
RUNS_DIR = BASE_DIR / "runs"
LOGS_DIR = BASE_DIR / "logs"

st.set_page_config(page_title="VulWeb 实验平台", layout="wide")

@st.cache_resource
def lazy_load():
    adapters = load_adapters()
    datasets = load_datasets()
    return adapters, datasets


def render_params_form(params_schema: dict) -> dict:
    st.subheader("超参数")
    values = {}
    for name, spec in params_schema.items():
        ptype = spec.get("type", "str")
        default = spec.get("default")
        help_ = spec.get("help", "")
        options = spec.get("options")
        if options:
            default_idx = options.index(default) if default in options else 0
            values[name] = st.selectbox(f"{name}", options=options, index=default_idx, help=help_)
        elif ptype == "int":
            values[name] = st.number_input(f"{name} (int)", value=int(default) if default is not None else 0, step=1, help=help_)
        elif ptype == "float":
            values[name] = st.number_input(f"{name} (float)", value=float(default) if default is not None else 0.0, step=0.0001, format="%.6f", help=help_)
        elif ptype == "bool":
            values[name] = st.checkbox(f"{name}", value=bool(default), help=help_)
        else:
            values[name] = st.text_input(f"{name}", value=str(default) if default is not None else "", help=help_)
    return values

def main():
    st.title("VulWeb 实验平台（MVP）")
    st.caption("选择模型与数据集，填写超参数，点击开始训练；运行你本地训练代码，并实时可视化。")
    
    adapters, datasets = lazy_load()
    
    cols = st.columns(2)
    with cols[0]:
        st.header("模型")
        model_ids = list(adapters.keys())
        if not model_ids:
            st.error("未发现任何模型适配器，请在 exp_platform/adapters 下添加。")
            st.stop()
        sel_model_id = st.selectbox("选择模型", options=model_ids, format_func=lambda k: f"{k} - {adapters[k].name}")
        model = adapters[sel_model_id]
        st.write(model.description)
    
    with cols[1]:
        st.header("数据集")
        dataset_ids = list(datasets.keys())
        if not dataset_ids:
            st.error("未发现任何数据集适配器，请在 exp_platform/datasets 下添加。")
            st.stop()
        sel_dataset_id = st.selectbox("选择数据集", options=dataset_ids, format_func=lambda k: f"{k} - {datasets[k].name}")
        dataset = datasets[sel_dataset_id]
        st.write(dataset.description)
        if st.button("准备数据集（可选）"):
            with st.spinner("准备数据集..."):
                dataset.prepare()
            st.success("数据集已准备就绪。")
    
    params = render_params_form(model.params_schema())
    run_name = st.text_input("实验名称（可选）", value=f"{timestamp_str()}_{model.id}_{dataset.id}")
    run_dir = RUNS_DIR / run_name
    
    start = st.button("开始训练", type="primary", use_container_width=True)
    if start:
        ensure_dir(run_dir)
        _ = ExperimentConfig(model_id=model.id, dataset_id=dataset.id, params=params, run_dir=str(run_dir))
        cmd = model.build_train_command(dataset, params, run_dir)
        st.info(f"启动命令：{' '.join(cmd)}")
        log_placeholder = st.empty()
        chart_placeholder = st.empty()
        status_placeholder = st.empty()

        metrics_path = model.metrics_path(run_dir)
        df_last_mtime = None
        df_cache = None

        try:
            with st.spinner("训练进行中..."):
                for line in run_command_stream(cmd, cwd=BASE_DIR):
                    if line is None:
                        # 子进程空闲，尝试刷新曲线
                        if metrics_path.exists():
                            mtime = metrics_path.stat().st_mtime
                            if mtime != df_last_mtime:
                                try:
                                    df_cache = pd.read_csv(metrics_path)
                                    chart_placeholder.line_chart(df_cache.set_index("step"))
                                    df_last_mtime = mtime
                                except Exception:
                                    pass
                        time.sleep(0.2)
                        continue
                    log_placeholder.code(line, language="bash")
                    # 同步刷新曲线
                    if metrics_path.exists():
                        mtime = metrics_path.stat().st_mtime
                        if mtime != df_last_mtime:
                            try:
                                df_cache = pd.read_csv(metrics_path)
                                chart_placeholder.line_chart(df_cache.set_index("step"))
                                df_last_mtime = mtime
                            except Exception:
                                pass
            status_placeholder.success(f"训练完成，产物位于：{run_dir}")
        except Exception as e:
            st.error(f"训练失败：{e}")

    st.divider()
    st.subheader("最近的实验")
    ensure_dir(RUNS_DIR)
    runs = sorted([p for p in RUNS_DIR.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)[:10]
    for r in runs:
        st.write(f"- {r.name}")
        mp = r / "metrics.csv"
        if mp.exists():
            try:
                df = pd.read_csv(mp)
                st.line_chart(df.set_index("step"))
            except Exception:
                st.write("无法读取指标文件。")

if __name__ == "__main__":
    main()