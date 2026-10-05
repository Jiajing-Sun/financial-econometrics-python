"""价格增量、对数收益相关检验与异方差稳健的固定持有期方差比。"""
import numpy as np
from arch.unitroot import VarianceRatio
from statsmodels.stats.diagnostic import acorr_ljungbox
from common import table, figure, plt, prices

def run(out,data_file=None):
    if data_file:
        d=prices(data_file,minimum=100);p=d.close.to_numpy();label="USER_DATA；来源由读者记录"
    else:
        rng=np.random.default_rng(123);r=rng.normal(.0002,.012,1500)
        p=100*np.exp(np.r_[0,np.cumsum(r)]);label="SIMULATED 对数随机游走；非贵州茅台行情"
    dp=np.diff(p);logp=np.log(p);r=np.diff(logp)
    lb=acorr_ljungbox(dp,lags=[10],boxpierce=True,return_df=True).reset_index(names="lag")
    table(out,"price_increment_tests",lb)
    log_lb=acorr_ljungbox(r,lags=[10],boxpierce=True,return_df=True).reset_index(names="lag")
    table(out,"log_return_tests",log_lb)
    rows=[]
    for lag in [2,5,10,20]:
        # arch.VarianceRatio 接收水平序列，而非再次差分后的收益率。
        vr=VarianceRatio(logp,lags=lag,trend="c",robust=True,overlap=True,debiased=True)
        rows.append({"holding_period":lag,"variance_ratio":vr.vr,"statistic":vr.stat,"p_value":vr.pvalue})
    table(out,"robust_variance_ratios",rows)
    table(out,"analysis_input",{"observation":np.arange(len(p)),"close":p})
    plt.plot(r,lw=.6);plt.xlabel("Observation");plt.ylabel("Log return");figure(out,"log_returns")
    return {"data":label,"price_observations":len(p),"test":"固定持有期、重叠、异方差稳健 VR；不是 R AutoBoot.test 的逐项替代",
            "interpretation":"同时考察多个持有期涉及多重检验；未拒绝不等于证明市场有效"}
