# 第 2 章 · 收益率与投资组合

对应教材：**引言和背景**
[网站导读](https://econometricswithr.com/python?chapter=2#ch02) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH02) · [返回总目录](../README.md)

单期收益看似简单，但跨期累积与资产加权遵循不同的规则。本章通过简短的数值例子，说明简单收益率、对数收益率和组合权重之间的关系。

## 动手做什么

计算简单与对数收益率；核对持仓价值与组合收益；观察圣彼得堡赌局的截断期望。

在仓库根目录激活环境后运行：

```bash
python CH02/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH02/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

给定价格路径与持仓数量，不使用市场行情数据。

## 如何阅读结果

先观察价格从 100 降至 50 再回到 100 的变化，再验证组合收益与期初权重的关系。

圣彼得堡赌局的奖金为 2^(N−1)。有限截断的期望并非无限赌局的期望，图形仅展示截断上限变化的效果。

主要输出：

- `DEMONSTRATION_portfolio.csv`
- `DEMONSTRATION_returns.csv`
- `st_petersburg.csv`
- `st_petersburg.png`
- `summary.json`
