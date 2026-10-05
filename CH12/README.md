# 第 12 章 · 机器学习的滚动样本外比较

对应教材：**AI 与金融计量：模型、应用与实践**
[网站导读](https://econometricswithr.com/python?chapter=12#ch12) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH12) · [返回总目录](../README.md)

模型能否预测未来，应在未参与训练的数据上进行检验。本章使用同一组模拟股票特征，比较决策树、随机森林与逻辑回归对上涨概率的预测能力。

## 动手做什么

构造模拟股票面板数据；采用 24 个月滚动训练窗口；比较 Brier 分数、AUC 与准确率。

在仓库根目录激活环境后运行：

```bash
python CH12/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH12/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

模拟 40 只股票、42 个月的数据；每个模型产生 18 个月、共计 720 条样本外预测。

## 如何阅读结果

先核对训练窗口与标签的可获得时间，再比较概率预测的表现；Brier 分数越小越好。

标准化仅在训练窗口内拟合，模型的超参数预先设定，测试窗口不参与调参。scikit-learn 与 rpart 的剪枝规则不同，因此不要求树结构完全一致。

主要输出：

- `SIMULATED_out_of_sample.csv`
- `SIMULATED_stock_panel.csv`
- `model_comparison.png`
- `model_metrics.csv`
- `summary.json`
- `time_windows.csv`
