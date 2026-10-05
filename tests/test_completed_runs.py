"""对已运行的全章结果核对跨步骤约束；未运行章节时跳过。"""

import json
import numpy as np
import pandas as pd
import pytest
from common import ROOT


def output(chapter, filename):
    p = ROOT / chapter / "results/current" / filename
    if not p.exists():
        pytest.skip("先运行 python run_all.py 生成本地结果")
    return p


def test_rolling_predictions_and_label_availability():
    windows = pd.read_csv(output("CH12", "time_windows.csv"))
    assert (windows.latest_training_label_known_at <= windows.prediction_month).all()
    assert (windows.training_feature_last < windows.prediction_month).all()
    predictions = pd.read_csv(output("CH12", "SIMULATED_out_of_sample.csv"))
    assert predictions.groupby("model").size().eq(720).all()
    assert not predictions.duplicated(["model", "month", "id"]).any()
    assert predictions.probability_up.between(0, 1).all()
    # 所有模型必须在同一组测试观测上评价。
    assert predictions.groupby(["month", "id"]).actual.nunique().eq(1).all()


def test_holdout_prediction_intervals():
    d = pd.read_csv(output("CH04", "holdout_forecast.csv"))
    assert len(d) == 200
    assert (d.lower95 <= d.forecast).all() and (d.forecast <= d.upper95).all()
    assert np.isfinite(d.to_numpy()).all()


def test_summary_for_every_chapter():
    for n in range(1, 13):
        p = output(f"CH{n:02}", "summary.json")
        result = json.loads(p.read_text())
        assert result and any(k in result for k in ["data", "historical_data"])
