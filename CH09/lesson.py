"""布朗运动、几何布朗运动与高频噪声下的已实现方差。"""

import numpy as np
from common import table, figure, plt


def run(out, data_file=None):
    rng = np.random.default_rng(123)
    n = 24000
    T = 1.0
    dt = T / n
    dW = rng.normal(0, np.sqrt(dt), n)
    W = np.r_[0, np.cumsum(dW)]
    t = np.linspace(0, T, n + 1)
    mu, sigma = 0.05, 0.2
    logp = np.log(100) + (mu - 0.5 * sigma**2) * t + sigma * W
    noise = rng.normal(0, 0.001, n + 1)
    observed = logp + noise
    rows = []
    for step in [1, 2, 5, 10, 30, 60, 120, 240]:
        index = np.arange(0, n + 1, step)
        rows.append(
            {
                "sampling_step": step,
                "latent_RV": np.sum(np.diff(logp[index]) ** 2),
                "noisy_RV": np.sum(np.diff(observed[index]) ** 2),
                "true_integrated_variance": sigma**2 * T,
            }
        )
    table(
        out,
        "SIMULATED_paths",
        {
            "time": t,
            "Brownian": W,
            "latent_log_price": logp,
            "noisy_log_price": observed,
        },
    )
    table(out, "volatility_signature", rows)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    ax[0].plot(t, W, lw=0.6)
    ax[0].set(xlabel="Time", ylabel="W(t)")
    ax[1].plot(
        [r["sampling_step"] for r in rows],
        [r["noisy_RV"] for r in rows],
        label="Noisy RV",
    )
    ax[1].plot(
        [r["sampling_step"] for r in rows],
        [r["latent_RV"] for r in rows],
        label="Latent RV",
    )
    ax[1].set(xlabel="Sampling step", ylabel="Realized variance")
    ax[1].axhline(sigma**2, color="#c67936", label="True IV")
    ax[1].set_xscale("log")
    ax[1].legend()
    figure(out, "Brownian_and_RV")
    return {
        "data": "SIMULATED GBM 与独立观测噪声",
        "true_integrated_variance": sigma**2 * T,
        "Brownian_quadratic_variation": float(np.sum(dW**2)),
        "seed": 123,
    }
