# 第 1 章 · 从 R 到 Python：数据与函数

对应教材：**R 语言概述**
[网站导读](https://econometricswithr.com/python?chapter=1#ch01) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH01) · [返回总目录](../README.md)

同一个计算问题，换一种语言如何实现？本章从自然常数的近似计算入手，练习数组操作、函数定义、分组汇总和绘图，为后续建模做好准备。

## 动手做什么

计算自然常数的两种近似；汇总汽车数据；绘制直方图和散点图。

在仓库根目录激活环境后运行：

```bash
python CH01/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH01/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

mtcars 为公开历史样本，包含 32 款汽车；自然常数示例为确定性计算。

## 如何阅读结果

比较极限近似与级数近似的误差，再观察汽车重量与燃油经济性之间的关系。

第 1 章以 R 入门为主，此处补充对应的 Python 基础。汽车原始字段沿用 R 数据集的单位。

主要输出：

- `e_approximations.csv`
- `fuel_economy_by_cylinders.csv`
- `mtcars_overview.png`
- `summary.json`
