# 第 3 章 · 回归系数的估计与解释

对应教材：**线性回归模型**
[网站导读](https://econometricswithr.com/python?chapter=3#ch03) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH03) · [返回总目录](../README.md)

先用汽车数据理解单位变换对回归系数的影响，再用匿名 A 公司案例估计 CAPM。比较普通标准误与 HAC 标准误，区分系数估计与统计推断。

## 动手做什么

拟合公制单位下的汽车回归；处理价格缺失值；估计 CAPM 与 HAC 标准误。

在仓库根目录激活环境后运行：

```bash
python CH03/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH03/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

使用 mtcars 与出版社提供的匿名 A 公司历史教学数据；缺失值处理会单独记录。

## 如何阅读结果

检查插值标记和收益率表，随后解释 alpha、beta 及标准误。

为与正文 R 演示对照，内部缺失值按行线性插值，无风险利率按年化百分数除以 100 和 365 近似换算。此口径用于复现教学案例，不用于构造事前交易信号。

主要输出：

- `interpolation_flags.csv`
- `mtcars_metric_coefficients.csv`
- `publisher_CAPM_coefficients.csv`
- `publisher_CAPM_returns.csv`
- `regressions.png`
- `summary.json`
## 使用自己的 CAPM 数据

运行 `python CH03/run.py --data /path/to/stock_data.csv`。CSV 字段为 `Date,stock_price,market_index,risk_free_rate`，日期严格递增；利率为年化百分数。价格内部缺失值按正文口径线性插值，端点缺失不外推。汽车回归仍使用随附的 mtcars 数据。
