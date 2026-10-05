# 第 8 章 · 从特征排序到多因子回归

对应教材：**金融资产定价模型**
[网站导读](https://econometricswithr.com/python?chapter=8#ch08) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH08) · [返回总目录](../README.md)

规模和价值特征如何转化为因子？先按上期特征构造组合，再用模拟资产收益估计因子载荷，理解因子构造与回归检验的衔接。

## 动手做什么

按滞后特征构造简化的 SMB/HML；估计多因子模型；检验 alpha 与因子载荷限制。

在仓库根目录激活环境后运行：

```bash
python CH08/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH08/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

模拟 100 只股票、240 期的特征与收益。

## 如何阅读结果

核对分组使用的时间点，再阅读 HAC 标准误和联合限制检验结果。

采用独立等权排序进行演示，并非官方 Fama–French 2×3 市值加权因子的复现。模拟因子不能用于推断真实市场溢价。

主要输出：

- `SIMULATED_factors.csv`
- `factor_loadings.csv`
- `factor_series.png`
- `restriction_tests.csv`
- `summary.json`
