# 第 11 章 · 尾指数、VaR 与 ES

对应教材：**风险管理与尾部风险估计**
[网站导读](https://econometricswithr.com/python?chapter=11#ch11) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH11) · [返回总目录](../README.md)

极端损失的风险无法仅用平均值刻画。本章先观察 Hill 估计对阈值的敏感性，再基于历史月度收益计算 VaR 和 ES。

## 动手做什么

估计模拟 Pareto 分布的尾指数；绘制 Hill 图；计算历史分位数与尾部期望损失。

在仓库根目录激活环境后运行：

```bash
python CH11/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH11/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

Pareto 模拟样本，以及第 12 章数据目录中的 SPY 月度历史快照。

## 如何阅读结果

比较不同阈值下的尾指数估计值，并检查 95% 与 99% 置信水平对应的风险数值。

损失定义为负对数收益，风险期限为月度。ES 按经验分位数积分计算，并考虑分位点处的部分概率质量；全样本结果是描述性统计，并非事前风险预测。

主要输出：

- `Hill_plot.png`
- `SIMULATED_Hill.csv`
- `SPY_monthly_historical_risk.csv`
- `summary.json`
