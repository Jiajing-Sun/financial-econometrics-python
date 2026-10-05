"""Nelson–Siegel 曲线及 GSW 历史零息收益率的截面拟合。"""

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from common import ROOT, table, figure, plt


def ns_curves(t, theta):
    t = np.asarray(t, dtype=float)
    b0, b1, b2, tau = theta
    if tau <= 0 or (t < 0).any():
        raise ValueError("tau 必须为正，期限必须非负")
    u = t / tau
    E = np.exp(-u)
    one_minus_E = -np.expm1(-u)
    # 稳定地计算 (1-exp(-u))/u，含零期限的连续延拓。
    loading = np.divide(one_minus_E, u, out=np.ones_like(u), where=u != 0)
    spot = b0 + b1 * loading + b2 * (loading - E)
    forward = b0 + (b1 + b2 * u) * E
    return np.exp(-t * spot), spot, forward


def run(out, data_file=None):
    t = np.linspace(0, 30, 601)
    theta = [0.03, -0.02, 0.025, 2.0]
    disc, spot, fwd = ns_curves(t, theta)
    table(
        out,
        "DEMONSTRATION_NS",
        {"years": t, "discount": disc, "spot": spot, "forward": fwd},
    )
    path = ROOT / "CH10/data/feds200628.csv"
    # 前九行保留来源说明；SVENY 为连续复利零息收益率，单位为年化百分数。
    data = pd.read_csv(path, skiprows=9, na_values=["NA"])
    cols = [f"SVENY{i:02}" for i in range(1, 31)]
    clean = data[["Date", *cols]].copy()
    clean[cols] = clean[cols].apply(pd.to_numeric, errors="coerce")
    clean = clean.dropna(subset=["Date", *cols]).sort_values("Date")
    if clean.empty:
        raise ValueError("GSW 快照没有完整截面")
    row = clean.iloc[-1]
    maturity = np.arange(1, 31, dtype=float)
    y = row[cols].to_numpy(dtype=float) / 100
    fits = []
    for tau in [1.0, 3.0, 8.0]:
        fit = least_squares(
            lambda b: ns_curves(maturity, b)[1] - y,
            [0.03, -0.01, 0.02, tau],
            bounds=([-0.2, -1, -1, 0.05], [0.3, 1, 1, 50]),
            max_nfev=3000,
        )
        if fit.success:
            fits.append(fit)
    if not fits:
        raise RuntimeError("NS 拟合未收敛")
    best = min(fits, key=lambda f: np.sum(f.fun**2))
    fitted = ns_curves(maturity, best.x)[1]
    table(
        out,
        "GSW_snapshot_NS_fit",
        {"years": maturity, "observed_zero_yield": y, "NS_yield": fitted},
    )
    table(
        out,
        "NS_fitted_parameters",
        {"parameter": ["beta0", "beta1", "beta2", "tau"], "estimate": best.x},
    )
    plt.plot(maturity, y, "o", label="GSW snapshot")
    plt.plot(maturity, fitted, label="NS fit")
    plt.xlabel("Years")
    plt.ylabel("Continuous zero yield")
    plt.legend()
    figure(out, "GSW_NS_fit")
    return {
        "data": "美国联储 GSW 历史研究数据快照",
        "snapshot_date": str(row.Date),
        "fit": "零息收益率最小二乘；不是息票债券价格最小二乘",
        "RMSE_basis_points": float(np.sqrt(np.mean((fitted - y) ** 2)) * 10000),
    }
