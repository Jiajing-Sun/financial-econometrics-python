"""GARCH 模拟、估计、标准化残差与条件方差预测。"""

import numpy as np
from arch import arch_model
from statsmodels.stats.diagnostic import acorr_ljungbox
from common import table, figure, plt, prices


def simulate_garch(n=1500, seed=123, omega=0.01, alpha=0.05, beta=0.9):
    if omega <= 0 or min(alpha, beta) < 0 or alpha + beta >= 1:
        raise ValueError("需要正截距、非负系数及有限无条件方差")
    rng = np.random.default_rng(seed)
    h = np.empty(n)
    r = np.empty(n)
    h[0] = omega / (1 - alpha - beta)
    r[0] = np.sqrt(h[0]) * rng.normal()
    for t in range(1, n):
        h[t] = omega + alpha * r[t - 1] ** 2 + beta * h[t - 1]
        r[t] = np.sqrt(h[t]) * rng.normal()
    return r, h


def run(out, data_file=None):
    if data_file:
        d = prices(data_file, minimum=250)
        r = 100 * np.diff(np.log(d.close))
        h = None
        label = "USER_DATA；百分数对数收益"
    else:
        r, h = simulate_garch()
        label = "SIMULATED；收益单位为百分数"
    model = arch_model(
        r, mean="Zero", vol="GARCH", p=1, q=1, dist="normal", rescale=False
    )
    fit = model.fit(disp="off")
    if fit.convergence_flag != 0:
        raise RuntimeError("GARCH 优化未收敛")
    table(
        out,
        "GARCH_parameters",
        {
            "parameter": fit.params.index,
            "estimate": fit.params.values,
            "standard_error": fit.std_err.values,
        },
    )
    outdata = {"return_percent": r, "estimated_variance": fit.conditional_volatility**2}
    if h is not None:
        outdata["SIMULATED_true_variance"] = h
    table(out, "conditional_variance", outdata)
    z = np.asarray(fit.std_resid)
    diagnostics = acorr_ljungbox(z**2, lags=[10, 20], return_df=True).reset_index(
        names="lag"
    )
    table(out, "squared_standardized_residuals_LB", diagnostics)
    forecast = fit.forecast(horizon=10, reindex=False).variance.iloc[-1].to_numpy()
    table(
        out,
        "variance_forecast",
        {"horizon": np.arange(1, 11), "variance_percent_squared": forecast},
    )
    fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    ax[0].plot(r, lw=0.6)
    ax[0].set_ylabel("Return (%)")
    ax[1].plot(fit.conditional_volatility**2, lw=0.8)
    ax[1].set_ylabel("Conditional variance")
    figure(out, "GARCH")
    return {
        "data": label,
        "converged": True,
        "persistence": float(fit.params["alpha[1]"] + fit.params["beta[1]"]),
        "note": "残差检验是诊断，不证明模型正确；预测方差单位为百分数的平方",
    }
