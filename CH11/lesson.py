"""Hill 尾指数与可处理分位点概率质量的历史 VaR/ES。"""
import numpy as np
from common import ROOT, table, figure, plt
import pandas as pd

def hill(loss,k):
    x=np.sort(np.asarray(loss,dtype=float))[::-1]
    if not np.isfinite(x).all() or (x<=0).any() or not 1<=k<len(x):raise ValueError("需要有限正损失和有效阈值阶数")
    h=np.mean(np.log(x[:k]/x[k]))
    if h<=0:raise ValueError("尾部对数超额均值须为正")
    return 1/h

def historical_risk(loss,confidence=.95):
    """经验分布的分位数和分位数积分 ES；包含边界观测的分数权重。"""
    x=np.sort(np.asarray(loss,dtype=float));n=len(x)
    if n==0 or not np.isfinite(x).all() or not 0<confidence<1:raise ValueError("无效损失样本或置信水平")
    var=x[int(np.ceil(n*confidence))-1]
    # 每个排序观测占据 ((i-1)/n,i/n]，只积分置信水平以上的部分。
    left=np.arange(n)/n;right=np.arange(1,n+1)/n
    weights=np.maximum(0,right-np.maximum(left,confidence))
    es=float(x@weights/(1-confidence))
    return float(var),es

def run(out,data_file=None):
    rng=np.random.default_rng(123);loss=1+rng.pareto(3,3000);ks=np.arange(50,501,50)
    estimates=[hill(loss,int(k)) for k in ks]
    table(out,"SIMULATED_Hill",{"k":ks,"estimated_exponent":estimates,"true_exponent":3})
    # 与正文 R 仓库相同的历史 SPY 月度快照；这里不声称是日度风险。
    d=pd.read_csv(ROOT/'CH12/data/SPY_monthly_2000_2024.csv');monthly_loss=-np.diff(np.log(d.price))
    rows=[]
    for p in [.95,.99]:
        var,es=historical_risk(monthly_loss,p)
        rows.append({"confidence":p,"monthly_log_loss_VaR":var,"monthly_log_loss_ES":es})
    table(out,"SPY_monthly_historical_risk",rows)
    plt.plot(ks,estimates,'o-');plt.axhline(3,color='#c67936');plt.xlabel('Tail observations k');plt.ylabel('Tail exponent');figure(out,"Hill_plot")
    return {"tail_demo":"SIMULATED Pareto，尾指数 3", "historical_data":"SPY 月度快照，2000—2024；非实时行情",
            "risk":"负对数收益口径；全样本描述性风险，不是事前预测或策略回测"}
