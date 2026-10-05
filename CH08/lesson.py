"""滞后特征分组形成简化因子，并对模拟多因子回归作限制检验。"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from common import table, figure, plt


def equal_weight_factors(market_value, pb, returns):
    N, T = returns.shape
    rows = []
    if (
        N < 10
        or market_value.shape != returns.shape
        or pb.shape != returns.shape
        or (pb <= 0).any()
    ):
        raise ValueError("输入需为同形矩阵且 PB 为正，股票数至少为十")
    for t in range(1, T):
        size = np.argsort(market_value[:, t - 1])
        value = np.argsort(1 / pb[:, t - 1])
        half = N // 2
        tail = int(0.3 * N)
        rows.append(
            {
                "period": t + 1,
                "SMB": returns[size[:half], t].mean() - returns[size[half:], t].mean(),
                "HML": returns[value[-tail:], t].mean()
                - returns[value[:tail], t].mean(),
            }
        )
    return pd.DataFrame(rows)


def run(out, data_file=None):
    rng = np.random.default_rng(123)
    N, T = 100, 240
    mv = rng.uniform(100, 1100, (N, T))
    pb = rng.uniform(1, 6, (N, T))
    r = rng.uniform(-0.05, 0.05, (N, T))
    factors = equal_weight_factors(mv, pb, r)
    factors["MKT"] = r[:, 1:].mean(axis=0)
    # 此处资产收益也为模拟量，因子载荷是生成参数。
    y = (
        0.001
        + 1.1 * factors.MKT
        + 0.4 * factors.SMB
        + 0.2 * factors.HML
        + rng.normal(0, 0.008, T - 1)
    )
    X = sm.add_constant(factors[["MKT", "SMB", "HML"]])
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    alpha = fit.t_test([1, 0, 0, 0])
    joint = fit.wald_test(np.array([[0, 0, 1, 0], [0, 0, 0, 1]]), scalar=True)
    table(out, "SIMULATED_factors", factors)
    table(
        out,
        "factor_loadings",
        {
            "term": fit.params.index,
            "estimate": fit.params.values,
            "HAC_standard_error": fit.bse.values,
        },
    )
    table(
        out,
        "restriction_tests",
        [
            {
                "test": "alpha=0",
                "statistic": float(np.asarray(alpha.statistic).item()),
                "p_value": float(alpha.pvalue),
            },
            {
                "test": "SMB=HML=0 (Wald chi-square)",
                "statistic": float(joint.statistic),
                "p_value": float(joint.pvalue),
            },
        ],
    )
    factors.plot(x="period", y=["SMB", "HML"], figsize=(8, 3.6))
    plt.ylabel("Simulated long-short return")
    figure(out, "factor_series")
    return {
        "data": "SIMULATED；按 t-1 特征分组计算 t 收益",
        "periods": len(factors),
        "method": "简化独立等权排序，非官方 Fama–French 2×3 市值加权因子",
    }
