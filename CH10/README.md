# 第 10 章 · Nelson–Siegel 收益率曲线

对应教材：**收益率曲线（Yield Curve）**
[网站导读](https://econometricswithr.com/python?chapter=10#ch10) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH10) · [返回总目录](../README.md)

一条收益率曲线怎样同时描述短端与长端？先考察 Nelson–Siegel 参数的含义，再用美国国债历史零息收益率截面拟合曲线。

## 动手做什么

计算贴现因子、即期与远期利率；处理零期限极限；用多组初值拟合历史截面。

在仓库根目录激活环境后运行：

```bash
python CH10/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH10/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

使用美国联储 GSW 研究数据的固定快照；脚本自动选择快照中最后一个完整的 1—30 年期限截面。

## 如何阅读结果

比较观测收益率与拟合曲线，结合误差和参数解释曲线形状。

SVENY 字段为年化百分数形式的连续复利零息收益率，建模时需除以 100。此处最小化的是零息收益率的误差，而非息票债券的价格误差。

主要输出：

- `DEMONSTRATION_NS.csv`
- `GSW_NS_fit.png`
- `GSW_snapshot_NS_fit.csv`
- `NS_fitted_parameters.csv`
- `summary.json`
