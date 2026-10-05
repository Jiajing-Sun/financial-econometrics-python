# 第 9 章 · 高频观测与波动率估计

对应教材：**连续时间模型与高频波动率估计**
[网站导读](https://econometricswithr.com/python?chapter=9#ch09) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH09) · [返回总目录](../README.md)

采样越密，波动率估计一定越好吗？将连续价格路径与带有测量噪声的观测放在一起，观察采样频率如何改变已实现方差。

## 动手做什么

模拟布朗运动和几何布朗运动；计算不同采样间隔的已实现方差；绘制波动率特征图。

在仓库根目录激活环境后运行：

```bash
python CH09/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH09/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

模拟连续价格路径及独立观测噪声，时间区间长度为 1。

## 如何阅读结果

将两类已实现方差与已知积分方差比较，理解高频噪声的影响。

本例展示基础已实现方差和噪声机制，不包含双尺度估计量或已实现核的完整实现。

主要输出：

- `Brownian_and_RV.png`
- `SIMULATED_paths.csv`
- `summary.json`
- `volatility_signature.csv`
