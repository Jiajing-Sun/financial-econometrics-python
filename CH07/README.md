# 第 7 章 · 核密度与局部线性回归

对应教材：**非参数方法**
[网站导读](https://econometricswithr.com/python?chapter=7#ch07) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH07) · [返回总目录](../README.md)

不预先指定完整的函数形式，能否从数据中看出收益分布与市场间的关系？通过核函数、带宽和局部拟合，体会非参数估计的灵活性与取舍。

## 动手做什么

绘制三种核函数；估计 DAX 收益密度；局部拟合 FTSE 与 DAX 收益的关系。

在仓库根目录激活环境后运行：

```bash
python CH07/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH07/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

使用 EuStockMarkets 公开历史样本；以观测序号保存，不补造交易日期。

## 如何阅读结果

改变带宽并观察曲线的平滑程度，留意尾部和样本稀疏区域。

DAX 与 FTSE 均采用百分数简单收益。核密度使用 SciPy 的 Scott 带宽，其默认值可能不同于 R density()，不能将曲线差异直接视为计算错误。

主要输出：

- `DAX_density.csv`
- `DAX_given_FTSE.csv`
- `kernels.csv`
- `kernel_functions.png`
- `nonparametric.png`
- `summary.json`
