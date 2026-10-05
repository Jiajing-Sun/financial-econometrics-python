# 第 4 章 · ARMA 识别、估计与预测

对应教材：**自回归移动平均模型**
[网站导读](https://econometricswithr.com/python?chapter=4#ch04) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH04) · [返回总目录](../README.md)

从一条已知生成机制的 AR(2) 序列出发，观察其自相关与偏自相关，再比较候选 ARMA 模型的拟合和预测表现。

## 动手做什么

模拟 AR(2) 序列；计算 Yule–Walker 估计；根据训练样本 BIC 选择模型并进行预测。

在仓库根目录激活环境后运行：

```bash
python CH04/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH04/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

模拟 AR(2) 序列，系数为 0.6 和 −0.4；预留后 200 期用于预测评价。

## 如何阅读结果

对照真实系数、估计值以及 ACF/PACF，观察预测区间如何随预测期延长而变化。

采用固定起点的多步预测，不在测试样本中反复估计模型。R 与 NumPy 的随机数生成方式不同，相同种子不意味着相同的样本路径。

主要输出：

- `ACF_PACF.png`
- `SIMULATED_AR2.csv`
- `YW_coefficients.csv`
- `holdout_forecast.csv`
- `model_selection.csv`
- `summary.json`
