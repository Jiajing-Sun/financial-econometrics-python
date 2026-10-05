# 第 5 章 · GARCH 条件波动率

对应教材：**波动率模型**
[网站导读](https://econometricswithr.com/python?chapter=5#ch05) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH05) · [返回总目录](../README.md)

波动率为何会持续升高，又逐渐回落？通过模拟、估计和预测，理解 GARCH 模型如何将过去的冲击传递到未来的条件方差。

## 动手做什么

模拟并估计 GARCH(1,1)；检查标准化残差平方；计算十期条件方差预测。

在仓库根目录激活环境后运行：

```bash
python CH05/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH05/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

默认使用模拟收益；也可提供包含 date, close 两列的价格 CSV 文件，至少 250 行。

## 如何阅读结果

将估计方差与模拟真实方差对照，再查看参数持续性、残差诊断和预测表。

收益使用百分数，条件方差单位为百分数的平方。采用零条件均值和正态创新设定；残差检验不能单独证明模型正确。

主要输出：

- `GARCH.png`
- `GARCH_parameters.csv`
- `conditional_variance.csv`
- `squared_standardized_residuals_LB.csv`
- `summary.json`
- `variance_forecast.csv`
## 使用自己的价格数据

CSV 至少包含 250 行，字段为 `date,close`。日期不得缺失或重复，价格必须为有限正数；程序按日期排序，不对交易日空缺插值。价格序列的复权方式须前后一致。

```csv
date,close
2024-01-02,100.0
2024-01-03,101.2
```

```bash
python CH05/run.py --data /path/to/prices.csv
```
