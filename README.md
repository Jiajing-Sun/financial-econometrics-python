# 金融计量经济学 · Python 补充实践

《金融计量经济学：理论、案例与 R 语言》配套实践
**孙佳婧 · 洪永淼 · Oliver Linton**

[配套网站](https://econometricswithr.com/python) · [正文 R 代码](https://github.com/Jiajing-Sun/financial-econometrics-r) · [数据来源](DATA_SOURCES.csv)

除 R 示例外，每章均配有 Python 实践，帮助读者使用熟悉的语言学习金融计量。每章选取核心方法，串联数据处理、模型估计、图形展示与结果解释，适合与教材及 R 代码对照学习。

本仓库选编了十二章的核心演示，并补充了 Python 实践；并非对正文中所有 R 片段的逐行翻译。具体方法、数据口径以及与 R 实现的差异，请参见各章说明。

## 开始运行

本版本已在 Python 3.14 上运行验证。请先安装 Python 和 Git，在终端执行：

```bash
git clone https://github.com/Jiajing-Sun/financial-econometrics-python.git
cd financial-econometrics-python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python CH03/run.py
```

Windows 用户可用 `py -3` 创建虚拟环境，再运行 `.venv\Scripts\activate` 激活。

```bash
python run_all.py                       # 运行十二章
python run_all.py --chapters=1,3,7       # 运行指定章节
python CH10/run.py --output my_results  # 自选输出目录
python -m pytest -q                     # 检查数学关系和数据口径
```

依赖安装完成后，十二章默认示例均可离线运行，无需 API 密钥。结果写入各章 `results/current/`；已生成的图表与数值示例在 `results/reference/`。复现本次环境可安装 `requirements-lock.txt` 中的版本。模拟数据使用固定随机种子，但 R 与 NumPy 的随机数序列不同，不要求两种语言产生相同样本路径。

## 按章学习

| 章节 | 对应教材内容 | Python 实践 |
| --- | --- | --- |
| [01](CH01/) | R 语言概述 | 从 R 到 Python：数据与函数 |
| [02](CH02/) | 引言和背景 | 收益率与投资组合 |
| [03](CH03/) | 线性回归模型 | 回归系数的估计与解释 |
| [04](CH04/) | 自回归移动平均模型 | ARMA 识别、估计与预测 |
| [05](CH05/) | 波动率模型 | GARCH 条件波动率 |
| [06](CH06/) | 收益可预测性与有效市场假说 | 用方差比检验收益可预测性 |
| [07](CH07/) | 非参数方法 | 核密度与局部线性回归 |
| [08](CH08/) | 金融资产定价模型 | 从特征排序到多因子回归 |
| [09](CH09/) | 连续时间模型与高频波动率估计 | 高频观测与波动率估计 |
| [10](CH10/) | 收益率曲线（Yield Curve） | Nelson–Siegel 收益率曲线 |
| [11](CH11/) | 风险管理与尾部风险估计 | 尾指数、VaR 与 ES |
| [12](CH12/) | AI 与金融计量：模型、应用与实践 | 机器学习的滚动样本外比较 |

## 文件说明

每章的 `README.md` 介绍学习内容、数据和结果，`run.py` 是运行入口，`lesson.py` 包含计算步骤。数据集中放在相应章节的 `data/` 下；第 11 章与第 12 章共用 SPY 历史快照。

第 3、5、6 章支持自备 CSV，字段要求见本章说明。历史数据、模拟数据和给定参数的演示分别标注，不将模拟结果当作真实市场证据。

## 对照与来源

汽车回归和匿名 A 公司 CAPM 使用与 R 版一致的数据与处理口径，回归系数及普通标准误已作数值对照。程序还检查收益率累积、GARCH 方差递推、因子分组时间、Nelson–Siegel 曲线关系和 ES 的分位点权重。

数据来源见 [DATA_SOURCES.csv](DATA_SOURCES.csv)，来源版本和文件校验值见 [data_manifest.json](data_manifest.json)。版权与使用说明见 [LICENSE-NOTICE.txt](LICENSE-NOTICE.txt)。
