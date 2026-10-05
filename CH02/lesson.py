"""收益率、持仓权重与圣彼得堡赌局的正文演示。"""

import numpy as np
from common import table, figure, plt


def returns(price):
    p = np.asarray(price, dtype=float)
    if p.ndim != 1 or len(p) < 2 or not np.isfinite(p).all() or (p <= 0).any():
        raise ValueError("价格必须是长度至少为二的有限正数序列")
    return p[1:] / p[:-1] - 1, np.diff(np.log(p))


def run(out, data_file=None):
    prices = np.array([100.0, 50.0, 100.0, 110.0])
    simple, log = returns(prices)
    table(
        out,
        "DEMONSTRATION_returns",
        {
            "period": np.arange(1, len(prices)),
            "simple": simple,
            "log": log,
            "cumulative_simple": np.cumprod(1 + simple) - 1,
            "cumulative_log": np.cumsum(log),
        },
    )
    initial = np.array([20.0, 50.0])
    final = np.array([22.0, 47.0])
    shares = np.array([3.0, 2.0])
    weights = shares * initial / (shares @ initial)
    asset_returns = final / initial - 1
    table(
        out,
        "DEMONSTRATION_portfolio",
        {
            "shares": shares,
            "initial_price": initial,
            "final_price": final,
            "initial_weight": weights,
            "asset_return": asset_returns,
        },
    )
    k = np.arange(1, 101)
    prob = 2.0 ** (-k)
    prize = 2.0 ** (k - 1)
    table(
        out,
        "st_petersburg",
        {
            "truncation": k,
            "partial_expected_prize": np.cumsum(prob * prize),
            "partial_expected_log_prize": np.cumsum(prob * np.log(prize)),
        },
    )
    plt.plot(k, np.cumsum(prob * prize))
    plt.xlabel("Truncation")
    plt.ylabel("Partial expected prize")
    figure(out, "st_petersburg")
    return {
        "data": "确定性教学示例；赌局奖金为 2^(N-1)",
        "portfolio_return": float((shares @ final) / (shares @ initial) - 1),
        "weighted_simple_return": float(weights @ asset_returns),
        "expected_log_prize_partial": float(np.sum(prob * np.log(prize))),
    }
