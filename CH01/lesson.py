"""Python 基础：函数、数值计算、分组整理和图形。"""
import math
import numpy as np
import pandas as pd
from common import ROOT, table, figure, plt

def e_series(n):
    """递推 1/k!，避免直接计算巨大阶乘。"""
    term = total = 1.0
    for k in range(1, n + 1):
        term /= k
        total += term
    return total

def run(out, data_file=None):
    n = np.array([10, 100, 1000, 10000])
    # log1p 对很小的 1/n 更稳定。
    limit = np.exp(n * np.log1p(1 / n))
    table(out, "e_approximations", {"n": n, "limit": limit,
          "series": [e_series(int(k)) for k in n], "exact": math.e})
    cars = pd.read_csv(ROOT / "CH01/data/mtcars.csv")
    grouped = cars.groupby("cyl").agg(count=("mpg", "count"), mean_mpg=("mpg", "mean"))
    table(out, "fuel_economy_by_cylinders", grouped.reset_index())
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    ax[0].hist(cars.mpg, bins=10); ax[0].set(xlabel="Miles / US gallon", ylabel="Count")
    ax[1].scatter(cars.wt, cars.mpg); ax[1].set(xlabel="Weight (1000 lb)", ylabel="Miles / US gallon")
    figure(out, "mtcars_overview")
    return {"data": "R datasets::mtcars 历史样本", "rows": len(cars),
            "series_absolute_error": abs(e_series(20)-math.e)}
