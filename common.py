"""各章共用的输入、输出与命令行入口。"""

from pathlib import Path
import argparse
import importlib
import json
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
plt.rcParams.update(
    {
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=["#245b92", "#c67936", "#4e8c74"]),
        "figure.dpi": 120,
    }
)


def table(out, name, data):
    pd.DataFrame(data).to_csv(Path(out) / f"{name}.csv", index=False)


def figure(out, name):
    plt.tight_layout()
    plt.savefig(Path(out) / f"{name}.png", bbox_inches="tight")
    plt.close()


def prices(path, minimum=30):
    """自备 CSV 使用 date,close；保留真实交易间隔，不插值或填零。"""
    d = pd.read_csv(path)
    if not {"date", "close"}.issubset(d):
        raise ValueError("CSV 需要 date,close 两列")
    d = d[["date", "close"]].copy()
    d["date"] = pd.to_datetime(d["date"], errors="raise")
    d["close"] = pd.to_numeric(d["close"], errors="raise")
    if d.isna().any().any() or d.date.duplicated().any():
        raise ValueError("日期和价格不得缺失，日期不得重复")
    if len(d) < minimum or not np.isfinite(d.close).all() or (d.close <= 0).any():
        raise ValueError(f"至少需要 {minimum} 行有限、正价格")
    return d.sort_values("date").reset_index(drop=True)


def cli(chapter):
    parser = argparse.ArgumentParser(description=f"第 {chapter} 章 Python bonus")
    parser.add_argument("--data", type=Path, help="自备数据；字段要求见本章 README")
    parser.add_argument("--output", type=Path, help="输出目录")
    args = parser.parse_args()
    if args.data and chapter not in {3, 5, 6}:
        parser.error("本章使用随附数据或模拟数据；--data 仅适用于第 3、5、6 章")
    out = args.output or ROOT / f"CH{chapter:02}" / "results/current"
    out.mkdir(parents=True, exist_ok=True)
    data = args.data.resolve() if args.data else None
    result = importlib.import_module(f"CH{chapter:02}.lesson").run(out, data)
    (out / "summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )
    print(f"CH{chapter:02}: {out}")
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
