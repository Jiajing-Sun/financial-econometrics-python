# 第 6 章 · 用方差比检验收益可预测性

对应教材：**收益可预测性与有效市场假说**
[网站导读](https://econometricswithr.com/python?chapter=6#ch06) · [R 版目录](https://github.com/Jiajing-Sun/financial-econometrics-r/tree/main/CH06) · [返回总目录](../README.md)

若对数价格服从随机游走，不同期限的增量方差应呈现怎样的关系？本章将这一问题转化为方差比检验，并与收益序列相关检验进行对照。

## 动手做什么

生成随机游走序列；进行 Ljung–Box 检验；计算多个期限的异方差稳健方差比检验。

在仓库根目录激活环境后运行：

```bash
python CH06/run.py
```

计算步骤见 [lesson.py](lesson.py)。输出位于 `CH06/results/current/`，可对照 [参考图表与数值](results/reference/)。

## 数据

默认使用模拟对数随机游走；可提供 date,close 价格 CSV，至少 100 行。

## 如何阅读结果

比较不同期限的统计量与 p 值，结合检验原假设解释结果。

方差比函数输入对数价格水平，不能误传收益率。此处实现固定期限的稳健检验，不等同于 R 示例中的自动期限选择与 bootstrap 程序。

主要输出：

- `analysis_input.csv`
- `log_returns.png`
- `price_increment_tests.csv`
- `log_return_tests.csv`
- `robust_variance_ratios.csv`
- `summary.json`
## 使用自己的价格数据

CSV 至少包含 100 行，字段为 `date,close`。日期不得缺失或重复，价格必须为有限正数；程序按日期排序，不对交易日空缺插值。价格序列的复权方式须前后一致。

```csv
date,close
2024-01-02,100.0
2024-01-03,101.2
```

```bash
python CH06/run.py --data /path/to/prices.csv
```
